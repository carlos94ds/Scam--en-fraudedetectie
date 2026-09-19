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
