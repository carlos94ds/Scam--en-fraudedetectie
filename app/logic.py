"""
De 'brein'-logica van de applicatie, los van de Streamlit-UI. Dit maakt het
apart testbaar met pytest, zonder de webserver te hoeven starten.
"""
import os
import json
import joblib

import pandas as pd

from src.feature_extraction import extract_full_features
from src.train_production_model import FEATURE_ORDER
from src.website_features import fetch_website, compute_website_features, encode_for_model_b, WebsiteFetchError

FEATURE_EXPLANATIONS = {
    "nl": {
        "URLLength": ("Deze link is ongewoon lang.", "Deze link heeft een gewone lengte."),
        "DomainLength": ("De domeinnaam is ongewoon lang.", "De domeinnaam heeft een gewone lengte."),
        "IsDomainIP": ("De link gebruikt een kaal IP-adres in plaats van een domeinnaam.", "De link gebruikt een normale domeinnaam."),
        "TLDLength": ("Het laatste stukje van het domein is ongewoon lang.", "Het laatste stukje van het domein heeft een gewone lengte."),
        "NoOfSubDomain": ("De link heeft veel onderdelen voor de domeinnaam.", "De link heeft een eenvoudige domeinopbouw."),
        "HasObfuscation": ("De link bevat vreemde gecodeerde tekens.", "De link bevat geen vreemde gecodeerde tekens."),
        "NoOfObfuscatedChar": ("De link bevat meerdere vreemde gecodeerde tekens.", "De link bevat geen vreemde gecodeerde tekens."),
        "ObfuscationRatio": ("Een groot deel van de link bestaat uit gecodeerde tekens.", "De link bevat nauwelijks gecodeerde tekens."),
        "NoOfLettersInURL": ("De link bevat weinig gewone letters.", "De link bevat vooral gewone letters."),
        "LetterRatioInURL": ("De link bestaat voor een klein deel uit letters.", "De link bestaat grotendeels uit letters."),
        "NoOfDegitsInURL": ("De link bevat ongewoon veel cijfers.", "De link bevat weinig cijfers."),
        "DegitRatioInURL": ("Een groot deel van de link bestaat uit cijfers.", "De link bevat weinig cijfers."),
        "NoOfEqualsInURL": ("De link bevat veel is-gelijk-tekens.", "De link bevat weinig is-gelijk-tekens."),
        "NoOfQMarkInURL": ("De link bevat veel vraagtekens.", "De link bevat weinig vraagtekens."),
        "NoOfAmpersandInURL": ("De link bevat veel &-tekens.", "De link bevat weinig &-tekens."),
        "NoOfOtherSpecialCharsInURL": ("De link bevat veel ongewone tekens.", "De link bevat weinig ongewone tekens."),
        "SpacialCharRatioInURL": ("Een groot deel van de link bestaat uit ongewone tekens.", "De link bevat weinig ongewone tekens."),
        "IsHTTPS": ("Deze link gebruikt geen beveiligde verbinding (https).", "Deze link gebruikt een beveiligde verbinding (https)."),
        "CharContinuationRate": ("De opbouw van de link wisselt sterk tussen letters, cijfers en tekens.", "De link heeft een rustige, herkenbare opbouw."),
        "URLCharProb": ("De link bevat tekencombinaties die ongebruikelijk zijn.", "De link bevat gewone, herkenbare tekencombinaties."),
        "TLDLegitimateProb": ("Dit soort domeinextensie komt vaker voor bij nepwebsites.", "Dit soort domeinextensie komt vaker voor bij betrouwbare websites."),
        # Website-kenmerken (alleen aanwezig bij een gecombineerde analyse mét bezoek aan de website)
        "LineOfCode": ("De pagina bestaat uit ongewoon weinig broncode.", "De pagina heeft een gewone hoeveelheid broncode."),
        "LargestLineLength": ("De pagina bevat een ongewoon lange, samengeperste regel code.", "De code van de pagina is normaal opgebouwd."),
        "HasTitle": ("De pagina heeft geen paginatitel.", "De pagina heeft een paginatitel."),
        "DomainTitleMatchScore": ("De paginatitel lijkt niet op de domeinnaam.", "De paginatitel past bij de domeinnaam."),
        "URLTitleMatchScore": ("De paginatitel lijkt niet op de link.", "De paginatitel past bij de link."),
        "HasFavicon": ("De pagina heeft geen favicon (browericoontje).", "De pagina heeft een favicon (browericoontje)."),
        "IsResponsive": ("De pagina is niet geschikt gemaakt voor mobiel gebruik.", "De pagina is geschikt gemaakt voor mobiel gebruik."),
        "NoOfURLRedirect": ("De link stuurt je via meerdere tussenstappen door.", "De link stuurt je niet onnodig door."),
        "NoOfSelfRedirect": ("De pagina stuurt zichzelf meerdere keren door.", "De pagina stuurt zichzelf niet onnodig door."),
        "HasDescription": ("De pagina heeft geen paginabeschrijving.", "De pagina heeft een paginabeschrijving."),
        "NoOfPopup": ("De pagina probeert pop-upvensters te openen.", "De pagina probeert geen pop-upvensters te openen."),
        "NoOfiFrame": ("De pagina bevat verborgen ingesloten vensters (iframes).", "De pagina bevat geen verborgen ingesloten vensters."),
        "HasExternalFormSubmit": ("Een formulier op de pagina stuurt gegevens naar een ander domein.", "Formulieren op de pagina sturen gegevens niet naar een ander domein."),
        "HasSocialNet": ("De pagina verwijst naar bekende social-mediaplatforms.", "De pagina verwijst niet naar bekende social-mediaplatforms."),
        "HasSubmitButton": ("De pagina heeft een verzendknop, bijvoorbeeld voor een formulier.", "De pagina heeft geen verzendknop."),
        "HasHiddenFields": ("De pagina bevat verborgen formuliervelden.", "De pagina bevat geen verborgen formuliervelden."),
        "HasPasswordField": ("De pagina vraagt om een wachtwoord.", "De pagina vraagt niet om een wachtwoord."),
        "Bank": ("De pagina bevat woorden die met bankzaken te maken hebben.", "De pagina bevat geen bankgerelateerde woorden."),
        "Pay": ("De pagina bevat woorden die met betalen te maken hebben.", "De pagina bevat geen betaalgerelateerde woorden."),
        "Crypto": ("De pagina bevat woorden die met cryptomunten te maken hebben.", "De pagina bevat geen crypto-gerelateerde woorden."),
        "HasCopyrightInfo": ("De pagina bevat geen copyright-vermelding.", "De pagina bevat een copyright-vermelding."),
        "NoOfImage": ("De pagina bevat ongewoon weinig afbeeldingen.", "De pagina heeft een gewone hoeveelheid afbeeldingen."),
        "NoOfCSS": ("De pagina bevat ongewoon weinig opmaakbestanden.", "De pagina heeft een gewone hoeveelheid opmaakbestanden."),
        "NoOfJS": ("De pagina bevat ongewoon veel scriptbestanden.", "De pagina heeft een gewone hoeveelheid scriptbestanden."),
        "NoOfSelfRef": ("De pagina verwijst weinig naar zichzelf.", "De pagina verwijst op een gewone manier naar zichzelf."),
        "NoOfEmptyRef": ("De pagina bevat veel lege of kapotte links.", "De pagina bevat weinig lege of kapotte links."),
        "NoOfExternalRef": ("De pagina verwijst veel naar andere websites.", "De pagina verwijst weinig naar andere websites."),
    },
    "en": {
        "URLLength": ("This link is unusually long.", "This link has a normal length."),
        "DomainLength": ("The domain name is unusually long.", "The domain name has a normal length."),
        "IsDomainIP": ("The link uses a bare IP address instead of a domain name.", "The link uses a normal domain name."),
        "TLDLength": ("The last part of the domain is unusually long.", "The last part of the domain has a normal length."),
        "NoOfSubDomain": ("The link has many parts before the domain name.", "The link has a simple domain structure."),
        "HasObfuscation": ("The link contains strange encoded characters.", "The link does not contain strange encoded characters."),
        "NoOfObfuscatedChar": ("The link contains multiple strange encoded characters.", "The link does not contain strange encoded characters."),
        "ObfuscationRatio": ("A large part of the link consists of encoded characters.", "The link barely contains encoded characters."),
        "NoOfLettersInURL": ("The link contains few ordinary letters.", "The link mostly consists of ordinary letters."),
        "LetterRatioInURL": ("Only a small part of the link consists of letters.", "The link largely consists of letters."),
        "NoOfDegitsInURL": ("The link contains an unusually high number of digits.", "The link contains few digits."),
        "DegitRatioInURL": ("A large part of the link consists of digits.", "The link contains few digits."),
        "NoOfEqualsInURL": ("The link contains many equals signs.", "The link contains few equals signs."),
        "NoOfQMarkInURL": ("The link contains many question marks.", "The link contains few question marks."),
        "NoOfAmpersandInURL": ("The link contains many & characters.", "The link contains few & characters."),
        "NoOfOtherSpecialCharsInURL": ("The link contains many unusual characters.", "The link contains few unusual characters."),
        "SpacialCharRatioInURL": ("A large part of the link consists of unusual characters.", "The link contains few unusual characters."),
        "IsHTTPS": ("This link does not use a secure connection (https).", "This link uses a secure connection (https)."),
        "CharContinuationRate": ("The structure of the link shifts strongly between letters, digits and characters.", "The link has a calm, recognizable structure."),
        "URLCharProb": ("The link contains character combinations that are unusual.", "The link contains ordinary, recognizable character combinations."),
        "TLDLegitimateProb": ("This type of domain extension is more common on fake websites.", "This type of domain extension is more common on trustworthy websites."),
        # Website features (only present in a combined analysis that also visits the website)
        "LineOfCode": ("The page consists of an unusually small amount of source code.", "The page has a normal amount of source code."),
        "LargestLineLength": ("The page contains an unusually long, compressed line of code.", "The page's code is normally structured."),
        "HasTitle": ("The page has no page title.", "The page has a page title."),
        "DomainTitleMatchScore": ("The page title doesn't resemble the domain name.", "The page title matches the domain name."),
        "URLTitleMatchScore": ("The page title doesn't resemble the link.", "The page title matches the link."),
        "HasFavicon": ("The page has no favicon (browser icon).", "The page has a favicon (browser icon)."),
        "IsResponsive": ("The page hasn't been made suitable for mobile use.", "The page has been made suitable for mobile use."),
        "NoOfURLRedirect": ("The link redirects you through several intermediate steps.", "The link doesn't redirect you unnecessarily."),
        "NoOfSelfRedirect": ("The page redirects to itself several times.", "The page doesn't unnecessarily redirect to itself."),
        "HasDescription": ("The page has no page description.", "The page has a page description."),
        "NoOfPopup": ("The page tries to open pop-up windows.", "The page doesn't try to open pop-up windows."),
        "NoOfiFrame": ("The page contains hidden embedded windows (iframes).", "The page contains no hidden embedded windows."),
        "HasExternalFormSubmit": ("A form on the page sends data to a different domain.", "Forms on the page don't send data to a different domain."),
        "HasSocialNet": ("The page links to known social media platforms.", "The page doesn't link to known social media platforms."),
        "HasSubmitButton": ("The page has a submit button, for example for a form.", "The page has no submit button."),
        "HasHiddenFields": ("The page contains hidden form fields.", "The page contains no hidden form fields."),
        "HasPasswordField": ("The page asks for a password.", "The page doesn't ask for a password."),
        "Bank": ("The page contains words related to banking.", "The page contains no banking-related words."),
        "Pay": ("The page contains words related to making payments.", "The page contains no payment-related words."),
        "Crypto": ("The page contains words related to cryptocurrency.", "The page contains no crypto-related words."),
        "HasCopyrightInfo": ("The page contains no copyright notice.", "The page contains a copyright notice."),
        "NoOfImage": ("The page contains an unusually small number of images.", "The page has a normal number of images."),
        "NoOfCSS": ("The page contains an unusually small number of style files.", "The page has a normal number of style files."),
        "NoOfJS": ("The page contains an unusually high number of script files.", "The page has a normal number of script files."),
        "NoOfSelfRef": ("The page has few links pointing back to itself.", "The page links back to itself in a normal way."),
        "NoOfEmptyRef": ("The page contains many empty or broken links.", "The page contains few empty or broken links."),
        "NoOfExternalRef": ("The page links heavily to other websites.", "The page links only a little to other websites."),
    },
    "fr": {
        "URLLength": ("Ce lien est anormalement long.", "Ce lien a une longueur normale."),
        "DomainLength": ("Le nom de domaine est anormalement long.", "Le nom de domaine a une longueur normale."),
        "IsDomainIP": ("Le lien utilise une adresse IP nue au lieu d'un nom de domaine.", "Le lien utilise un nom de domaine normal."),
        "TLDLength": ("La dernière partie du domaine est anormalement longue.", "La dernière partie du domaine a une longueur normale."),
        "NoOfSubDomain": ("Le lien comporte de nombreuses parties avant le nom de domaine.", "Le lien a une structure de domaine simple."),
        "HasObfuscation": ("Le lien contient des caractères codés étranges.", "Le lien ne contient pas de caractères codés étranges."),
        "NoOfObfuscatedChar": ("Le lien contient plusieurs caractères codés étranges.", "Le lien ne contient pas de caractères codés étranges."),
        "ObfuscationRatio": ("Une grande partie du lien est constituée de caractères codés.", "Le lien contient à peine des caractères codés."),
        "NoOfLettersInURL": ("Le lien contient peu de lettres ordinaires.", "Le lien est composé surtout de lettres ordinaires."),
        "LetterRatioInURL": ("Seule une petite partie du lien est composée de lettres.", "Le lien est en grande partie composé de lettres."),
        "NoOfDegitsInURL": ("Le lien contient un nombre anormalement élevé de chiffres.", "Le lien contient peu de chiffres."),
        "DegitRatioInURL": ("Une grande partie du lien est constituée de chiffres.", "Le lien contient peu de chiffres."),
        "NoOfEqualsInURL": ("Le lien contient de nombreux signes égal.", "Le lien contient peu de signes égal."),
        "NoOfQMarkInURL": ("Le lien contient de nombreux points d'interrogation.", "Le lien contient peu de points d'interrogation."),
        "NoOfAmpersandInURL": ("Le lien contient de nombreux caractères &.", "Le lien contient peu de caractères &."),
        "NoOfOtherSpecialCharsInURL": ("Le lien contient de nombreux caractères inhabituels.", "Le lien contient peu de caractères inhabituels."),
        "SpacialCharRatioInURL": ("Une grande partie du lien est constituée de caractères inhabituels.", "Le lien contient peu de caractères inhabituels."),
        "IsHTTPS": ("Ce lien n'utilise pas de connexion sécurisée (https).", "Ce lien utilise une connexion sécurisée (https)."),
        "CharContinuationRate": ("La structure du lien varie fortement entre lettres, chiffres et caractères.", "Le lien a une structure calme et reconnaissable."),
        "URLCharProb": ("Le lien contient des combinaisons de caractères inhabituelles.", "Le lien contient des combinaisons de caractères ordinaires et reconnaissables."),
        "TLDLegitimateProb": ("Ce type d'extension de domaine est plus fréquent sur les faux sites.", "Ce type d'extension de domaine est plus fréquent sur les sites fiables."),
        # Caractéristiques du site (uniquement présentes lors d'une analyse combinée avec visite du site)
        "LineOfCode": ("La page est constituée d'une quantité inhabituellement faible de code source.", "La page a une quantité normale de code source."),
        "LargestLineLength": ("La page contient une ligne de code anormalement longue et compressée.", "Le code de la page est structuré normalement."),
        "HasTitle": ("La page n'a pas de titre.", "La page a un titre."),
        "DomainTitleMatchScore": ("Le titre de la page ne ressemble pas au nom de domaine.", "Le titre de la page correspond au nom de domaine."),
        "URLTitleMatchScore": ("Le titre de la page ne ressemble pas au lien.", "Le titre de la page correspond au lien."),
        "HasFavicon": ("La page n'a pas de favicon (icône du navigateur).", "La page a un favicon (icône du navigateur)."),
        "IsResponsive": ("La page n'a pas été adaptée à l'utilisation mobile.", "La page a été adaptée à l'utilisation mobile."),
        "NoOfURLRedirect": ("Le lien vous redirige via plusieurs étapes intermédiaires.", "Le lien ne vous redirige pas inutilement."),
        "NoOfSelfRedirect": ("La page se redirige elle-même plusieurs fois.", "La page ne se redirige pas inutilement elle-même."),
        "HasDescription": ("La page n'a pas de description.", "La page a une description."),
        "NoOfPopup": ("La page essaie d'ouvrir des fenêtres pop-up.", "La page n'essaie pas d'ouvrir de fenêtres pop-up."),
        "NoOfiFrame": ("La page contient des fenêtres intégrées cachées (iframes).", "La page ne contient pas de fenêtres intégrées cachées."),
        "HasExternalFormSubmit": ("Un formulaire de la page envoie des données vers un autre domaine.", "Les formulaires de la page n'envoient pas de données vers un autre domaine."),
        "HasSocialNet": ("La page renvoie vers des plateformes de réseaux sociaux connues.", "La page ne renvoie pas vers des plateformes de réseaux sociaux connues."),
        "HasSubmitButton": ("La page a un bouton d'envoi, par exemple pour un formulaire.", "La page n'a pas de bouton d'envoi."),
        "HasHiddenFields": ("La page contient des champs de formulaire cachés.", "La page ne contient pas de champs de formulaire cachés."),
        "HasPasswordField": ("La page demande un mot de passe.", "La page ne demande pas de mot de passe."),
        "Bank": ("La page contient des mots liés aux opérations bancaires.", "La page ne contient pas de mots liés aux opérations bancaires."),
        "Pay": ("La page contient des mots liés au paiement.", "La page ne contient pas de mots liés au paiement."),
        "Crypto": ("La page contient des mots liés aux cryptomonnaies.", "La page ne contient pas de mots liés aux cryptomonnaies."),
        "HasCopyrightInfo": ("La page ne contient pas de mention de droits d'auteur.", "La page contient une mention de droits d'auteur."),
        "NoOfImage": ("La page contient un nombre inhabituellement faible d'images.", "La page a un nombre normal d'images."),
        "NoOfCSS": ("La page contient un nombre inhabituellement faible de fichiers de style.", "La page a un nombre normal de fichiers de style."),
        "NoOfJS": ("La page contient un nombre inhabituellement élevé de fichiers de script.", "La page a un nombre normal de fichiers de script."),
        "NoOfSelfRef": ("La page renvoie peu vers elle-même.", "La page renvoie vers elle-même de manière normale."),
        "NoOfEmptyRef": ("La page contient beaucoup de liens vides ou cassés.", "La page contient peu de liens vides ou cassés."),
        "NoOfExternalRef": ("La page renvoie beaucoup vers d'autres sites web.", "La page renvoie peu vers d'autres sites web."),
    },
    "es": {
        "URLLength": ("Este enlace es inusualmente largo.", "Este enlace tiene una longitud normal."),
        "DomainLength": ("El nombre de dominio es inusualmente largo.", "El nombre de dominio tiene una longitud normal."),
        "IsDomainIP": ("El enlace usa una dirección IP directa en lugar de un nombre de dominio.", "El enlace usa un nombre de dominio normal."),
        "TLDLength": ("La última parte del dominio es inusualmente larga.", "La última parte del dominio tiene una longitud normal."),
        "NoOfSubDomain": ("El enlace tiene muchas partes antes del nombre de dominio.", "El enlace tiene una estructura de dominio sencilla."),
        "HasObfuscation": ("El enlace contiene caracteres codificados extraños.", "El enlace no contiene caracteres codificados extraños."),
        "NoOfObfuscatedChar": ("El enlace contiene varios caracteres codificados extraños.", "El enlace no contiene caracteres codificados extraños."),
        "ObfuscationRatio": ("Una gran parte del enlace consiste en caracteres codificados.", "El enlace apenas contiene caracteres codificados."),
        "NoOfLettersInURL": ("El enlace contiene pocas letras normales.", "El enlace consiste principalmente en letras normales."),
        "LetterRatioInURL": ("Solo una pequeña parte del enlace consiste en letras.", "El enlace consiste en gran parte en letras."),
        "NoOfDegitsInURL": ("El enlace contiene un número inusualmente alto de dígitos.", "El enlace contiene pocos dígitos."),
        "DegitRatioInURL": ("Una gran parte del enlace consiste en dígitos.", "El enlace contiene pocos dígitos."),
        "NoOfEqualsInURL": ("El enlace contiene muchos signos de igual.", "El enlace contiene pocos signos de igual."),
        "NoOfQMarkInURL": ("El enlace contiene muchos signos de interrogación.", "El enlace contiene pocos signos de interrogación."),
        "NoOfAmpersandInURL": ("El enlace contiene muchos caracteres &.", "El enlace contiene pocos caracteres &."),
        "NoOfOtherSpecialCharsInURL": ("El enlace contiene muchos caracteres inusuales.", "El enlace contiene pocos caracteres inusuales."),
        "SpacialCharRatioInURL": ("Una gran parte del enlace consiste en caracteres inusuales.", "El enlace contiene pocos caracteres inusuales."),
        "IsHTTPS": ("Este enlace no usa una conexión segura (https).", "Este enlace usa una conexión segura (https)."),
        "CharContinuationRate": ("La estructura del enlace varía mucho entre letras, dígitos y caracteres.", "El enlace tiene una estructura tranquila y reconocible."),
        "URLCharProb": ("El enlace contiene combinaciones de caracteres inusuales.", "El enlace contiene combinaciones de caracteres normales y reconocibles."),
        "TLDLegitimateProb": ("Este tipo de extensión de dominio es más frecuente en sitios web falsos.", "Este tipo de extensión de dominio es más frecuente en sitios web fiables."),
        # Características del sitio web (solo presentes en un análisis combinado que también visita el sitio)
        "LineOfCode": ("La página consta de una cantidad inusualmente pequeña de código fuente.", "La página tiene una cantidad normal de código fuente."),
        "LargestLineLength": ("La página contiene una línea de código inusualmente larga y comprimida.", "El código de la página está estructurado de forma normal."),
        "HasTitle": ("La página no tiene título.", "La página tiene un título."),
        "DomainTitleMatchScore": ("El título de la página no se parece al nombre de dominio.", "El título de la página coincide con el nombre de dominio."),
        "URLTitleMatchScore": ("El título de la página no se parece al enlace.", "El título de la página coincide con el enlace."),
        "HasFavicon": ("La página no tiene favicon (icono del navegador).", "La página tiene un favicon (icono del navegador)."),
        "IsResponsive": ("La página no se ha adaptado para uso móvil.", "La página se ha adaptado para uso móvil."),
        "NoOfURLRedirect": ("El enlace te redirige a través de varios pasos intermedios.", "El enlace no te redirige innecesariamente."),
        "NoOfSelfRedirect": ("La página se redirige a sí misma varias veces.", "La página no se redirige innecesariamente a sí misma."),
        "HasDescription": ("La página no tiene descripción.", "La página tiene una descripción."),
        "NoOfPopup": ("La página intenta abrir ventanas emergentes.", "La página no intenta abrir ventanas emergentes."),
        "NoOfiFrame": ("La página contiene ventanas incrustadas ocultas (iframes).", "La página no contiene ventanas incrustadas ocultas."),
        "HasExternalFormSubmit": ("Un formulario de la página envía datos a otro dominio.", "Los formularios de la página no envían datos a otro dominio."),
        "HasSocialNet": ("La página enlaza con plataformas de redes sociales conocidas.", "La página no enlaza con plataformas de redes sociales conocidas."),
        "HasSubmitButton": ("La página tiene un botón de envío, por ejemplo para un formulario.", "La página no tiene botón de envío."),
        "HasHiddenFields": ("La página contiene campos de formulario ocultos.", "La página no contiene campos de formulario ocultos."),
        "HasPasswordField": ("La página pide una contraseña.", "La página no pide contraseña."),
        "Bank": ("La página contiene palabras relacionadas con operaciones bancarias.", "La página no contiene palabras relacionadas con operaciones bancarias."),
        "Pay": ("La página contiene palabras relacionadas con pagos.", "La página no contiene palabras relacionadas con pagos."),
        "Crypto": ("La página contiene palabras relacionadas con criptomonedas.", "La página no contiene palabras relacionadas con criptomonedas."),
        "HasCopyrightInfo": ("La página no contiene aviso de derechos de autor.", "La página contiene un aviso de derechos de autor."),
        "NoOfImage": ("La página contiene un número inusualmente bajo de imágenes.", "La página tiene un número normal de imágenes."),
        "NoOfCSS": ("La página contiene un número inusualmente bajo de archivos de estilo.", "La página tiene un número normal de archivos de estilo."),
        "NoOfJS": ("La página contiene un número inusualmente alto de archivos de script.", "La página tiene un número normal de archivos de script."),
        "NoOfSelfRef": ("La página enlaza poco consigo misma.", "La página enlaza consigo misma de forma normal."),
        "NoOfEmptyRef": ("La página contiene muchos enlaces vacíos o rotos.", "La página contiene pocos enlaces vacíos o rotos."),
        "NoOfExternalRef": ("La página enlaza mucho con otros sitios web.", "La página enlaza poco con otros sitios web."),
    },
    "de": {
        "URLLength": ("Dieser Link ist ungewöhnlich lang.", "Dieser Link hat eine normale Länge."),
        "DomainLength": ("Der Domainname ist ungewöhnlich lang.", "Der Domainname hat eine normale Länge."),
        "IsDomainIP": ("Der Link verwendet eine reine IP-Adresse anstelle eines Domainnamens.", "Der Link verwendet einen normalen Domainnamen."),
        "TLDLength": ("Der letzte Teil der Domain ist ungewöhnlich lang.", "Der letzte Teil der Domain hat eine normale Länge."),
        "NoOfSubDomain": ("Der Link hat viele Teile vor dem Domainnamen.", "Der Link hat eine einfache Domainstruktur."),
        "HasObfuscation": ("Der Link enthält merkwürdige kodierte Zeichen.", "Der Link enthält keine merkwürdigen kodierten Zeichen."),
        "NoOfObfuscatedChar": ("Der Link enthält mehrere merkwürdige kodierte Zeichen.", "Der Link enthält keine merkwürdigen kodierten Zeichen."),
        "ObfuscationRatio": ("Ein großer Teil des Links besteht aus kodierten Zeichen.", "Der Link enthält kaum kodierte Zeichen."),
        "NoOfLettersInURL": ("Der Link enthält wenige gewöhnliche Buchstaben.", "Der Link besteht überwiegend aus gewöhnlichen Buchstaben."),
        "LetterRatioInURL": ("Nur ein kleiner Teil des Links besteht aus Buchstaben.", "Der Link besteht größtenteils aus Buchstaben."),
        "NoOfDegitsInURL": ("Der Link enthält ungewöhnlich viele Ziffern.", "Der Link enthält wenige Ziffern."),
        "DegitRatioInURL": ("Ein großer Teil des Links besteht aus Ziffern.", "Der Link enthält wenige Ziffern."),
        "NoOfEqualsInURL": ("Der Link enthält viele Gleichheitszeichen.", "Der Link enthält wenige Gleichheitszeichen."),
        "NoOfQMarkInURL": ("Der Link enthält viele Fragezeichen.", "Der Link enthält wenige Fragezeichen."),
        "NoOfAmpersandInURL": ("Der Link enthält viele &-Zeichen.", "Der Link enthält wenige &-Zeichen."),
        "NoOfOtherSpecialCharsInURL": ("Der Link enthält viele ungewöhnliche Zeichen.", "Der Link enthält wenige ungewöhnliche Zeichen."),
        "SpacialCharRatioInURL": ("Ein großer Teil des Links besteht aus ungewöhnlichen Zeichen.", "Der Link enthält wenige ungewöhnliche Zeichen."),
        "IsHTTPS": ("Dieser Link verwendet keine sichere Verbindung (https).", "Dieser Link verwendet eine sichere Verbindung (https)."),
        "CharContinuationRate": ("Der Aufbau des Links wechselt stark zwischen Buchstaben, Ziffern und Zeichen.", "Der Link hat einen ruhigen, wiedererkennbaren Aufbau."),
        "URLCharProb": ("Der Link enthält ungewöhnliche Zeichenkombinationen.", "Der Link enthält gewöhnliche, wiedererkennbare Zeichenkombinationen."),
        "TLDLegitimateProb": ("Diese Art von Domainendung kommt häufiger bei gefälschten Websites vor.", "Diese Art von Domainendung kommt häufiger bei vertrauenswürdigen Websites vor."),
        # Website-Merkmale (nur vorhanden bei einer kombinierten Analyse, die die Website auch besucht)
        "LineOfCode": ("Die Seite besteht aus ungewöhnlich wenig Quellcode.", "Die Seite hat eine normale Menge an Quellcode."),
        "LargestLineLength": ("Die Seite enthält eine ungewöhnlich lange, komprimierte Codezeile.", "Der Code der Seite ist normal aufgebaut."),
        "HasTitle": ("Die Seite hat keinen Seitentitel.", "Die Seite hat einen Seitentitel."),
        "DomainTitleMatchScore": ("Der Seitentitel ähnelt nicht dem Domainnamen.", "Der Seitentitel passt zum Domainnamen."),
        "URLTitleMatchScore": ("Der Seitentitel ähnelt nicht dem Link.", "Der Seitentitel passt zum Link."),
        "HasFavicon": ("Die Seite hat kein Favicon (Browser-Symbol).", "Die Seite hat ein Favicon (Browser-Symbol)."),
        "IsResponsive": ("Die Seite wurde nicht für die mobile Nutzung optimiert.", "Die Seite wurde für die mobile Nutzung optimiert."),
        "NoOfURLRedirect": ("Der Link leitet Sie über mehrere Zwischenschritte weiter.", "Der Link leitet Sie nicht unnötig weiter."),
        "NoOfSelfRedirect": ("Die Seite leitet sich mehrfach selbst weiter.", "Die Seite leitet sich nicht unnötig selbst weiter."),
        "HasDescription": ("Die Seite hat keine Seitenbeschreibung.", "Die Seite hat eine Seitenbeschreibung."),
        "NoOfPopup": ("Die Seite versucht, Pop-up-Fenster zu öffnen.", "Die Seite versucht nicht, Pop-up-Fenster zu öffnen."),
        "NoOfiFrame": ("Die Seite enthält versteckte eingebettete Fenster (iframes).", "Die Seite enthält keine versteckten eingebetteten Fenster."),
        "HasExternalFormSubmit": ("Ein Formular auf der Seite sendet Daten an eine andere Domain.", "Formulare auf der Seite senden keine Daten an eine andere Domain."),
        "HasSocialNet": ("Die Seite verweist auf bekannte Social-Media-Plattformen.", "Die Seite verweist nicht auf bekannte Social-Media-Plattformen."),
        "HasSubmitButton": ("Die Seite hat eine Sende-Schaltfläche, z. B. für ein Formular.", "Die Seite hat keine Sende-Schaltfläche."),
        "HasHiddenFields": ("Die Seite enthält versteckte Formularfelder.", "Die Seite enthält keine versteckten Formularfelder."),
        "HasPasswordField": ("Die Seite fragt nach einem Passwort.", "Die Seite fragt nicht nach einem Passwort."),
        "Bank": ("Die Seite enthält Wörter, die mit Bankgeschäften zu tun haben.", "Die Seite enthält keine bankbezogenen Wörter."),
        "Pay": ("Die Seite enthält Wörter, die mit Bezahlen zu tun haben.", "Die Seite enthält keine zahlungsbezogenen Wörter."),
        "Crypto": ("Die Seite enthält Wörter, die mit Kryptowährungen zu tun haben.", "Die Seite enthält keine kryptobezogenen Wörter."),
        "HasCopyrightInfo": ("Die Seite enthält keinen Urheberrechtshinweis.", "Die Seite enthält einen Urheberrechtshinweis."),
        "NoOfImage": ("Die Seite enthält ungewöhnlich wenige Bilder.", "Die Seite hat eine normale Anzahl an Bildern."),
        "NoOfCSS": ("Die Seite enthält ungewöhnlich wenige Stildateien.", "Die Seite hat eine normale Anzahl an Stildateien."),
        "NoOfJS": ("Die Seite enthält ungewöhnlich viele Skriptdateien.", "Die Seite hat eine normale Anzahl an Skriptdateien."),
        "NoOfSelfRef": ("Die Seite verweist wenig auf sich selbst.", "Die Seite verweist auf normale Weise auf sich selbst."),
        "NoOfEmptyRef": ("Die Seite enthält viele leere oder defekte Links.", "Die Seite enthält wenige leere oder defekte Links."),
        "NoOfExternalRef": ("Die Seite verweist stark auf andere Websites.", "Die Seite verweist wenig auf andere Websites."),
    },
    "pt": {
        "URLLength": ("Este link é invulgarmente longo.", "Este link tem um comprimento normal."),
        "DomainLength": ("O nome de domínio é invulgarmente longo.", "O nome de domínio tem um comprimento normal."),
        "IsDomainIP": ("O link usa um endereço IP direto em vez de um nome de domínio.", "O link usa um nome de domínio normal."),
        "TLDLength": ("A última parte do domínio é invulgarmente longa.", "A última parte do domínio tem um comprimento normal."),
        "NoOfSubDomain": ("O link tem muitas partes antes do nome de domínio.", "O link tem uma estrutura de domínio simples."),
        "HasObfuscation": ("O link contém caracteres codificados estranhos.", "O link não contém caracteres codificados estranhos."),
        "NoOfObfuscatedChar": ("O link contém vários caracteres codificados estranhos.", "O link não contém caracteres codificados estranhos."),
        "ObfuscationRatio": ("Uma grande parte do link é composta por caracteres codificados.", "O link quase não contém caracteres codificados."),
        "NoOfLettersInURL": ("O link contém poucas letras normais.", "O link é composto principalmente por letras normais."),
        "LetterRatioInURL": ("Apenas uma pequena parte do link é composta por letras.", "O link é composto em grande parte por letras."),
        "NoOfDegitsInURL": ("O link contém um número invulgarmente elevado de dígitos.", "O link contém poucos dígitos."),
        "DegitRatioInURL": ("Uma grande parte do link é composta por dígitos.", "O link contém poucos dígitos."),
        "NoOfEqualsInURL": ("O link contém muitos sinais de igual.", "O link contém poucos sinais de igual."),
        "NoOfQMarkInURL": ("O link contém muitos pontos de interrogação.", "O link contém poucos pontos de interrogação."),
        "NoOfAmpersandInURL": ("O link contém muitos caracteres &.", "O link contém poucos caracteres &."),
        "NoOfOtherSpecialCharsInURL": ("O link contém muitos caracteres invulgares.", "O link contém poucos caracteres invulgares."),
        "SpacialCharRatioInURL": ("Uma grande parte do link é composta por caracteres invulgares.", "O link contém poucos caracteres invulgares."),
        "IsHTTPS": ("Este link não usa uma ligação segura (https).", "Este link usa uma ligação segura (https)."),
        "CharContinuationRate": ("A estrutura do link varia muito entre letras, dígitos e caracteres.", "O link tem uma estrutura calma e reconhecível."),
        "URLCharProb": ("O link contém combinações de caracteres invulgares.", "O link contém combinações de caracteres normais e reconhecíveis."),
        "TLDLegitimateProb": ("Este tipo de extensão de domínio é mais comum em sites falsos.", "Este tipo de extensão de domínio é mais comum em sites fiáveis."),
        # Características do site (apenas presentes numa análise combinada que também visita o site)
        "LineOfCode": ("A página é composta por uma quantidade invulgarmente pequena de código-fonte.", "A página tem uma quantidade normal de código-fonte."),
        "LargestLineLength": ("A página contém uma linha de código invulgarmente longa e comprimida.", "O código da página está estruturado de forma normal."),
        "HasTitle": ("A página não tem título.", "A página tem um título."),
        "DomainTitleMatchScore": ("O título da página não se assemelha ao nome de domínio.", "O título da página corresponde ao nome de domínio."),
        "URLTitleMatchScore": ("O título da página não se assemelha ao link.", "O título da página corresponde ao link."),
        "HasFavicon": ("A página não tem favicon (ícone do navegador).", "A página tem um favicon (ícone do navegador)."),
        "IsResponsive": ("A página não foi adaptada para utilização móvel.", "A página foi adaptada para utilização móvel."),
        "NoOfURLRedirect": ("O link redireciona-o através de vários passos intermédios.", "O link não o redireciona desnecessariamente."),
        "NoOfSelfRedirect": ("A página redireciona-se a si própria várias vezes.", "A página não se redireciona desnecessariamente a si própria."),
        "HasDescription": ("A página não tem descrição.", "A página tem uma descrição."),
        "NoOfPopup": ("A página tenta abrir janelas pop-up.", "A página não tenta abrir janelas pop-up."),
        "NoOfiFrame": ("A página contém janelas incorporadas ocultas (iframes).", "A página não contém janelas incorporadas ocultas."),
        "HasExternalFormSubmit": ("Um formulário da página envia dados para outro domínio.", "Os formulários da página não enviam dados para outro domínio."),
        "HasSocialNet": ("A página liga a plataformas de redes sociais conhecidas.", "A página não liga a plataformas de redes sociais conhecidas."),
        "HasSubmitButton": ("A página tem um botão de envio, por exemplo para um formulário.", "A página não tem botão de envio."),
        "HasHiddenFields": ("A página contém campos de formulário ocultos.", "A página não contém campos de formulário ocultos."),
        "HasPasswordField": ("A página pede uma palavra-passe.", "A página não pede palavra-passe."),
        "Bank": ("A página contém palavras relacionadas com operações bancárias.", "A página não contém palavras relacionadas com operações bancárias."),
        "Pay": ("A página contém palavras relacionadas com pagamentos.", "A página não contém palavras relacionadas com pagamentos."),
        "Crypto": ("A página contém palavras relacionadas com criptomoedas.", "A página não contém palavras relacionadas com criptomoedas."),
        "HasCopyrightInfo": ("A página não contém aviso de direitos de autor.", "A página contém um aviso de direitos de autor."),
        "NoOfImage": ("A página contém um número invulgarmente baixo de imagens.", "A página tem um número normal de imagens."),
        "NoOfCSS": ("A página contém um número invulgarmente baixo de ficheiros de estilo.", "A página tem um número normal de ficheiros de estilo."),
        "NoOfJS": ("A página contém um número invulgarmente elevado de ficheiros de script.", "A página tem um número normal de ficheiros de script."),
        "NoOfSelfRef": ("A página faz poucas referências a si própria.", "A página faz referências a si própria de forma normal."),
        "NoOfEmptyRef": ("A página contém muitos links vazios ou quebrados.", "A página contém poucos links vazios ou quebrados."),
        "NoOfExternalRef": ("A página faz muitas referências a outros sites.", "A página faz poucas referências a outros sites."),
    },
    "it": {
        "URLLength": ("Questo link è insolitamente lungo.", "Questo link ha una lunghezza normale."),
        "DomainLength": ("Il nome di dominio è insolitamente lungo.", "Il nome di dominio ha una lunghezza normale."),
        "IsDomainIP": ("Il link utilizza un indirizzo IP nudo invece di un nome di dominio.", "Il link utilizza un normale nome di dominio."),
        "TLDLength": ("L'ultima parte del dominio è insolitamente lunga.", "L'ultima parte del dominio ha una lunghezza normale."),
        "NoOfSubDomain": ("Il link ha molte parti prima del nome di dominio.", "Il link ha una struttura di dominio semplice."),
        "HasObfuscation": ("Il link contiene caratteri codificati strani.", "Il link non contiene caratteri codificati strani."),
        "NoOfObfuscatedChar": ("Il link contiene diversi caratteri codificati strani.", "Il link non contiene caratteri codificati strani."),
        "ObfuscationRatio": ("Una grande parte del link è costituita da caratteri codificati.", "Il link contiene a malapena caratteri codificati."),
        "NoOfLettersInURL": ("Il link contiene poche lettere normali.", "Il link è composto principalmente da lettere normali."),
        "LetterRatioInURL": ("Solo una piccola parte del link è composta da lettere.", "Il link è in gran parte composto da lettere."),
        "NoOfDegitsInURL": ("Il link contiene un numero insolitamente elevato di cifre.", "Il link contiene poche cifre."),
        "DegitRatioInURL": ("Una grande parte del link è costituita da cifre.", "Il link contiene poche cifre."),
        "NoOfEqualsInURL": ("Il link contiene molti segni di uguale.", "Il link contiene pochi segni di uguale."),
        "NoOfQMarkInURL": ("Il link contiene molti punti interrogativi.", "Il link contiene pochi punti interrogativi."),
        "NoOfAmpersandInURL": ("Il link contiene molti caratteri &.", "Il link contiene pochi caratteri &."),
        "NoOfOtherSpecialCharsInURL": ("Il link contiene molti caratteri insoliti.", "Il link contiene pochi caratteri insoliti."),
        "SpacialCharRatioInURL": ("Una grande parte del link è costituita da caratteri insoliti.", "Il link contiene pochi caratteri insoliti."),
        "IsHTTPS": ("Questo link non utilizza una connessione sicura (https).", "Questo link utilizza una connessione sicura (https)."),
        "CharContinuationRate": ("La struttura del link varia molto tra lettere, cifre e caratteri.", "Il link ha una struttura calma e riconoscibile."),
        "URLCharProb": ("Il link contiene combinazioni di caratteri insolite.", "Il link contiene combinazioni di caratteri normali e riconoscibili."),
        "TLDLegitimateProb": ("Questo tipo di estensione di dominio è più comune nei siti falsi.", "Questo tipo di estensione di dominio è più comune nei siti affidabili."),
        # Caratteristiche del sito (presenti solo in un'analisi combinata che visita anche il sito)
        "LineOfCode": ("La pagina è composta da una quantità insolitamente ridotta di codice sorgente.", "La pagina ha una quantità normale di codice sorgente."),
        "LargestLineLength": ("La pagina contiene una riga di codice insolitamente lunga e compressa.", "Il codice della pagina è strutturato normalmente."),
        "HasTitle": ("La pagina non ha un titolo.", "La pagina ha un titolo."),
        "DomainTitleMatchScore": ("Il titolo della pagina non assomiglia al nome di dominio.", "Il titolo della pagina corrisponde al nome di dominio."),
        "URLTitleMatchScore": ("Il titolo della pagina non assomiglia al link.", "Il titolo della pagina corrisponde al link."),
        "HasFavicon": ("La pagina non ha una favicon (icona del browser).", "La pagina ha una favicon (icona del browser)."),
        "IsResponsive": ("La pagina non è stata resa adatta all'uso mobile.", "La pagina è stata resa adatta all'uso mobile."),
        "NoOfURLRedirect": ("Il link ti reindirizza attraverso diversi passaggi intermedi.", "Il link non ti reindirizza inutilmente."),
        "NoOfSelfRedirect": ("La pagina si reindirizza a se stessa più volte.", "La pagina non si reindirizza inutilmente a se stessa."),
        "HasDescription": ("La pagina non ha una descrizione.", "La pagina ha una descrizione."),
        "NoOfPopup": ("La pagina cerca di aprire finestre pop-up.", "La pagina non cerca di aprire finestre pop-up."),
        "NoOfiFrame": ("La pagina contiene finestre incorporate nascoste (iframe).", "La pagina non contiene finestre incorporate nascoste."),
        "HasExternalFormSubmit": ("Un modulo della pagina invia dati a un altro dominio.", "I moduli della pagina non inviano dati a un altro dominio."),
        "HasSocialNet": ("La pagina rimanda a piattaforme social note.", "La pagina non rimanda a piattaforme social note."),
        "HasSubmitButton": ("La pagina ha un pulsante di invio, ad esempio per un modulo.", "La pagina non ha un pulsante di invio."),
        "HasHiddenFields": ("La pagina contiene campi modulo nascosti.", "La pagina non contiene campi modulo nascosti."),
        "HasPasswordField": ("La pagina richiede una password.", "La pagina non richiede una password."),
        "Bank": ("La pagina contiene parole legate ad attività bancarie.", "La pagina non contiene parole legate ad attività bancarie."),
        "Pay": ("La pagina contiene parole legate ai pagamenti.", "La pagina non contiene parole legate ai pagamenti."),
        "Crypto": ("La pagina contiene parole legate alle criptovalute.", "La pagina non contiene parole legate alle criptovalute."),
        "HasCopyrightInfo": ("La pagina non contiene un avviso di copyright.", "La pagina contiene un avviso di copyright."),
        "NoOfImage": ("La pagina contiene un numero insolitamente basso di immagini.", "La pagina ha un numero normale di immagini."),
        "NoOfCSS": ("La pagina contiene un numero insolitamente basso di file di stile.", "La pagina ha un numero normale di file di stile."),
        "NoOfJS": ("La pagina contiene un numero insolitamente alto di file di script.", "La pagina ha un numero normale di file di script."),
        "NoOfSelfRef": ("La pagina rimanda poco a se stessa.", "La pagina rimanda a se stessa in modo normale."),
        "NoOfEmptyRef": ("La pagina contiene molti link vuoti o non funzionanti.", "La pagina contiene pochi link vuoti o non funzionanti."),
        "NoOfExternalRef": ("La pagina rimanda molto ad altri siti web.", "La pagina rimanda poco ad altri siti web."),
    },
}


def load_resources(model_dir):
    model = joblib.load(os.path.join(model_dir, "production_model.pkl"))
    scaler = joblib.load(os.path.join(model_dir, "production_scaler.pkl"))
    with open(os.path.join(model_dir, "tld_probability_table.json")) as f:
        tld_data = json.load(f)
    with open(os.path.join(model_dir, "char_frequency_table.json")) as f:
        char_data = json.load(f)
    return model, scaler, tld_data, char_data


def website_resources_available(model_dir):
    """True als model B (URL + website) getraind en opgeslagen is. Voordat
    src/train_url_website_model.py lokaal met de dataset is gedraaid, staan
    deze bestanden er nog niet, en valt de app terug op URL-only."""
    required = (
        "url_website_logreg.pkl",
        "url_website_scaler.pkl",
        "url_website_feature_columns.pkl",
        "url_website_vocab.json",
    )
    return all(os.path.exists(os.path.join(model_dir, name)) for name in required)


def load_website_resources(model_dir):
    model_b = joblib.load(os.path.join(model_dir, "url_website_logreg.pkl"))
    scaler_b = joblib.load(os.path.join(model_dir, "url_website_scaler.pkl"))
    feature_columns_b = joblib.load(os.path.join(model_dir, "url_website_feature_columns.pkl"))
    with open(os.path.join(model_dir, "url_website_vocab.json")) as f:
        vocab = json.load(f)
    return model_b, scaler_b, list(feature_columns_b), vocab


def classify_risk(p_phishing: float) -> str:
    """Zet een phishing-kans om in een van drie risiconiveaus.

    Grenzen (0,2 / 0,6) zijn een eerste, beargumenteerde keuze: onder 20%
    kans laag risico, boven 60% kans hoog risico, daartussen "mogelijk".
    """
    if p_phishing < 0.2:
        return "laag"
    if p_phishing < 0.6:
        return "mogelijk"
    return "hoog"


def explain(model, feature_values_scaled, feature_names, lang="nl", top_n=3):
    explanations = FEATURE_EXPLANATIONS.get(lang, FEATURE_EXPLANATIONS["nl"])
    contributions = model.coef_[0] * feature_values_scaled
    order = sorted(range(len(feature_names)), key=lambda i: abs(contributions[i]), reverse=True)
    reasons = []
    for i in order[:top_n]:
        name = feature_names[i]
        pushes_to_phishing = contributions[i] < 0
        pair = explanations.get(name)
        if pair:
            reasons.append(pair[0] if pushes_to_phishing else pair[1])
    return reasons


def analyse_url(url, model, scaler, tld_data, char_data, feature_order=FEATURE_ORDER, lang="nl"):
    features = extract_full_features(
        url,
        tld_prob_table=tld_data["table"],
        char_freq_table=char_data["table"],
        default_tld_prob=tld_data["default"],
        default_char_prob=char_data["default"],
    )
    X = pd.DataFrame([[features[name] for name in feature_order]], columns=feature_order)
    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[0]
    p_phishing = proba[0]
    risk = classify_risk(p_phishing)
    reasons = explain(model, X_scaled[0], feature_order, lang=lang)
    return risk, reasons, p_phishing


def analyse_url_and_website(url, model_b, scaler_b, feature_columns_b, vocab,
                             tld_data, char_data, lang="nl"):
    """Combineert de URL-tekst-kenmerken met live opgehaalde website-kenmerken
    en voorspelt met model B. Gooit WebsiteFetchError als de website niet
    (veilig) bezocht kon worden — de aanroeper vangt dat op en valt dan terug
    op analyse_url() (URL-only)."""
    url_features = extract_full_features(
        url,
        tld_prob_table=tld_data["table"],
        char_freq_table=char_data["table"],
        default_tld_prob=tld_data["default"],
        default_char_prob=char_data["default"],
    )
    # URLCharProb/TLDLegitimateProb horen niet bij de WEBSITE_FEATURES-kolommen
    # van model B; TLD blijft wel nodig voor de one-hot-encoding hieronder.
    raw_features = {k: v for k, v in url_features.items() if k not in ("URLCharProb", "TLDLegitimateProb")}

    html, final_url, n_redirects = fetch_website(url)
    website_features = compute_website_features(html, url, final_url, n_redirects)
    raw_features.update(website_features)

    X = encode_for_model_b(raw_features, vocab.get("tld", []), vocab.get("robots", []), feature_columns_b)
    X_scaled = scaler_b.transform(X)
    proba = model_b.predict_proba(X_scaled)[0]
    p_phishing = proba[0]
    risk = classify_risk(p_phishing)
    reasons = explain(model_b, X_scaled[0], feature_columns_b, lang=lang)
    return risk, reasons, p_phishing
