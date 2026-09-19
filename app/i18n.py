"""
Vertalingen voor de VerdachtLink-UI. Eén dict per taal met alle teksten die
de hoofdpagina gebruikt, plus de lijst talen voor de taalkiezer bovenaan.
"""

LANGUAGES = {
    "nl": "🇳🇱 Nederlands",
    "en": "🇬🇧 English",
    "fr": "🇫🇷 Français",
    "es": "🇪🇸 Español",
    "de": "🇩🇪 Deutsch",
    "pt": "🇵🇹 Português",
    "it": "🇮🇹 Italiano",
}

UI_TEXT = {
    "nl": {
        "lang_label": "🌐 Taal",
        "tagline": "Controleer snel of een link, e-mail, sms of social-mediabericht mogelijk onveilig is.",
        "tabs": [
            {
                "titel": "Link",
                "uitleg": "Plak een kale link, bijvoorbeeld uit je browser of een bericht.",
                "placeholder": "https://voorbeeld.nl/pagina",
            },
            {
                "titel": "E-mail",
                "uitleg": "Plak de tekst van een verdachte e-mail. We halen de link(en) eruit en beoordelen die; de afzender en de rest van de tekst worden niet meegewogen.",
                "placeholder": 'Bijvoorbeeld: "Uw account wordt geblokkeerd. Log direct in via ..."',
            },
            {
                "titel": "Sms",
                "uitleg": "Plak de tekst van een verdacht sms-bericht. We halen de link(en) eruit en beoordelen die.",
                "placeholder": 'Bijvoorbeeld: "Uw pakket kon niet worden bezorgd. Bevestig via ..."',
            },
            {
                "titel": "Social media",
                "uitleg": "Plak een bericht of link van Instagram, Facebook, WhatsApp of een ander platform.",
                "placeholder": "Bijvoorbeeld een link uit een DM of een reactie onder een post.",
            },
        ],
        "button": "Controleer",
        "warning_empty": "Vul eerst een link of bericht in.",
        "warning_no_url": "Er is geen link gevonden in de tekst. Controleer of de link volledig is geplakt.",
        "why_label": "**Waarom deze inschatting:**",
        "risk_labels": {"laag": "Laag risico", "mogelijk": "Mogelijk risico", "hoog": "Hoog risico"},
        "expander_title": "Meer over deze inschatting",
        "expander_text": (
            "Dit is een inschatting op basis van kenmerken van de link zelf, geen garantie. "
            "De website wordt niet bezocht; alleen de tekst van de link wordt beoordeeld. "
            "Voer nooit wachtwoorden, pincodes of andere gevoelige gegevens in op een "
            "website waarover je twijfelt, en open een link bij twijfel liever niet — "
            "controleer in plaats daarvan via een officiële app of website."
        ),
        "sidebar_caption": (
            "Gebruik het menu hierboven om meer te lezen over deze app, "
            "veelvoorkomende soorten fraude en algemene veiligheidstips."
        ),
    },
    "en": {
        "lang_label": "🌐 Language",
        "tagline": "Quickly check whether a link, email, text message or social media message might be unsafe.",
        "tabs": [
            {
                "titel": "Link",
                "uitleg": "Paste a bare link, for example from your browser or a message.",
                "placeholder": "https://example.com/page",
            },
            {
                "titel": "Email",
                "uitleg": "Paste the text of a suspicious email. We extract the link(s) and assess those; the sender and the rest of the text are not taken into account.",
                "placeholder": 'For example: "Your account will be blocked. Log in immediately via ..."',
            },
            {
                "titel": "Text message",
                "uitleg": "Paste the text of a suspicious text message. We extract the link(s) and assess those.",
                "placeholder": 'For example: "Your parcel could not be delivered. Confirm via ..."',
            },
            {
                "titel": "Social media",
                "uitleg": "Paste a message or link from Instagram, Facebook, WhatsApp or another platform.",
                "placeholder": "For example a link from a DM or a comment under a post.",
            },
        ],
        "button": "Check",
        "warning_empty": "Please enter a link or message first.",
        "warning_no_url": "No link was found in the text. Check that the link was pasted in full.",
        "why_label": "**Why this assessment:**",
        "risk_labels": {"laag": "Low risk", "mogelijk": "Possible risk", "hoog": "High risk"},
        "expander_title": "More about this assessment",
        "expander_text": (
            "This is an estimate based on characteristics of the link itself, not a guarantee. "
            "The website itself is not visited; only the text of the link is assessed. "
            "Never enter passwords, PIN codes or other sensitive information on a "
            "website you're unsure about, and if in doubt, don't open a link — "
            "check via an official app or website instead."
        ),
        "sidebar_caption": (
            "Use the menu above to read more about this app, "
            "common types of fraud and general safety tips."
        ),
    },
    "fr": {
        "lang_label": "🌐 Langue",
        "tagline": "Vérifiez rapidement si un lien, un e-mail, un SMS ou un message sur les réseaux sociaux est potentiellement dangereux.",
        "tabs": [
            {
                "titel": "Lien",
                "uitleg": "Collez un lien seul, par exemple depuis votre navigateur ou un message.",
                "placeholder": "https://exemple.fr/page",
            },
            {
                "titel": "E-mail",
                "uitleg": "Collez le texte d'un e-mail suspect. Nous extrayons le(s) lien(s) et les évaluons ; l'expéditeur et le reste du texte ne sont pas pris en compte.",
                "placeholder": 'Par exemple : "Votre compte va être bloqué. Connectez-vous immédiatement via ..."',
            },
            {
                "titel": "SMS",
                "uitleg": "Collez le texte d'un SMS suspect. Nous extrayons le(s) lien(s) et les évaluons.",
                "placeholder": 'Par exemple : "Votre colis n\'a pas pu être livré. Confirmez via ..."',
            },
            {
                "titel": "Réseaux sociaux",
                "uitleg": "Collez un message ou un lien provenant d'Instagram, Facebook, WhatsApp ou d'une autre plateforme.",
                "placeholder": "Par exemple un lien issu d'un message privé ou d'un commentaire.",
            },
        ],
        "button": "Vérifier",
        "warning_empty": "Veuillez d'abord saisir un lien ou un message.",
        "warning_no_url": "Aucun lien n'a été trouvé dans le texte. Vérifiez que le lien a été collé en entier.",
        "why_label": "**Pourquoi cette évaluation :**",
        "risk_labels": {"laag": "Risque faible", "mogelijk": "Risque possible", "hoog": "Risque élevé"},
        "expander_title": "En savoir plus sur cette évaluation",
        "expander_text": (
            "Il s'agit d'une estimation basée sur les caractéristiques du lien lui-même, pas d'une garantie. "
            "Le site web n'est pas visité ; seul le texte du lien est évalué. "
            "Ne saisissez jamais de mots de passe, codes PIN ou autres données sensibles sur un "
            "site dont vous n'êtes pas sûr, et en cas de doute, n'ouvrez pas le lien — "
            "vérifiez plutôt via une application ou un site officiel."
        ),
        "sidebar_caption": (
            "Utilisez le menu ci-dessus pour en savoir plus sur cette application, "
            "les types de fraude courants et les conseils de sécurité généraux."
        ),
    },
    "es": {
        "lang_label": "🌐 Idioma",
        "tagline": "Comprueba rápidamente si un enlace, correo electrónico, SMS o mensaje de redes sociales podría ser inseguro.",
        "tabs": [
            {
                "titel": "Enlace",
                "uitleg": "Pega un enlace sin más, por ejemplo desde tu navegador o un mensaje.",
                "placeholder": "https://ejemplo.es/pagina",
            },
            {
                "titel": "Correo",
                "uitleg": "Pega el texto de un correo sospechoso. Extraemos el o los enlaces y los evaluamos; el remitente y el resto del texto no se tienen en cuenta.",
                "placeholder": 'Por ejemplo: "Tu cuenta será bloqueada. Inicia sesión de inmediato en ..."',
            },
            {
                "titel": "SMS",
                "uitleg": "Pega el texto de un SMS sospechoso. Extraemos el o los enlaces y los evaluamos.",
                "placeholder": 'Por ejemplo: "No se pudo entregar tu paquete. Confirma en ..."',
            },
            {
                "titel": "Redes sociales",
                "uitleg": "Pega un mensaje o enlace de Instagram, Facebook, WhatsApp u otra plataforma.",
                "placeholder": "Por ejemplo un enlace de un mensaje directo o un comentario.",
            },
        ],
        "button": "Comprobar",
        "warning_empty": "Introduce primero un enlace o mensaje.",
        "warning_no_url": "No se ha encontrado ningún enlace en el texto. Comprueba que el enlace se haya pegado completo.",
        "why_label": "**Por qué esta valoración:**",
        "risk_labels": {"laag": "Riesgo bajo", "mogelijk": "Riesgo posible", "hoog": "Riesgo alto"},
        "expander_title": "Más información sobre esta valoración",
        "expander_text": (
            "Esto es una estimación basada en características del propio enlace, no una garantía. "
            "No se visita el sitio web; solo se evalúa el texto del enlace. "
            "Nunca introduzcas contraseñas, PIN u otros datos sensibles en un "
            "sitio del que dudes, y si tienes dudas, mejor no abras el enlace — "
            "compruébalo mejor a través de una app o sitio web oficial."
        ),
        "sidebar_caption": (
            "Usa el menú de arriba para leer más sobre esta app, "
            "los tipos de fraude más comunes y consejos generales de seguridad."
        ),
    },
    "de": {
        "lang_label": "🌐 Sprache",
        "tagline": "Prüfe schnell, ob ein Link, eine E-Mail, SMS oder Social-Media-Nachricht möglicherweise unsicher ist.",
        "tabs": [
            {
                "titel": "Link",
                "uitleg": "Füge einen einzelnen Link ein, zum Beispiel aus deinem Browser oder einer Nachricht.",
                "placeholder": "https://beispiel.de/seite",
            },
            {
                "titel": "E-Mail",
                "uitleg": "Füge den Text einer verdächtigen E-Mail ein. Wir extrahieren die Links und bewerten diese; Absender und übriger Text werden nicht berücksichtigt.",
                "placeholder": 'Zum Beispiel: "Ihr Konto wird gesperrt. Melden Sie sich sofort an über ..."',
            },
            {
                "titel": "SMS",
                "uitleg": "Füge den Text einer verdächtigen SMS ein. Wir extrahieren die Links und bewerten diese.",
                "placeholder": 'Zum Beispiel: "Ihr Paket konnte nicht zugestellt werden. Bestätigen Sie über ..."',
            },
            {
                "titel": "Social Media",
                "uitleg": "Füge eine Nachricht oder einen Link von Instagram, Facebook, WhatsApp oder einer anderen Plattform ein.",
                "placeholder": "Zum Beispiel ein Link aus einer DM oder einem Kommentar.",
            },
        ],
        "button": "Prüfen",
        "warning_empty": "Gib zuerst einen Link oder eine Nachricht ein.",
        "warning_no_url": "Im Text wurde kein Link gefunden. Prüfe, ob der Link vollständig eingefügt wurde.",
        "why_label": "**Warum diese Einschätzung:**",
        "risk_labels": {"laag": "Geringes Risiko", "mogelijk": "Mögliches Risiko", "hoog": "Hohes Risiko"},
        "expander_title": "Mehr über diese Einschätzung",
        "expander_text": (
            "Dies ist eine Einschätzung anhand von Merkmalen des Links selbst, keine Garantie. "
            "Die Website wird nicht besucht; es wird nur der Text des Links bewertet. "
            "Gib niemals Passwörter, PINs oder andere sensible Daten auf einer "
            "Website ein, bei der du unsicher bist, und öffne im Zweifel lieber keinen Link — "
            "prüfe stattdessen über eine offizielle App oder Website."
        ),
        "sidebar_caption": (
            "Nutze das Menü oben, um mehr über diese App, "
            "häufige Betrugsarten und allgemeine Sicherheitstipps zu lesen."
        ),
    },
    "pt": {
        "lang_label": "🌐 Idioma",
        "tagline": "Verifique rapidamente se um link, e-mail, SMS ou mensagem de rede social pode ser inseguro.",
        "tabs": [
            {
                "titel": "Link",
                "uitleg": "Cole um link simples, por exemplo do seu navegador ou de uma mensagem.",
                "placeholder": "https://exemplo.pt/pagina",
            },
            {
                "titel": "E-mail",
                "uitleg": "Cole o texto de um e-mail suspeito. Extraímos o(s) link(s) e avaliamos-os; o remetente e o resto do texto não são considerados.",
                "placeholder": 'Por exemplo: "A sua conta vai ser bloqueada. Inicie sessão já em ..."',
            },
            {
                "titel": "SMS",
                "uitleg": "Cole o texto de um SMS suspeito. Extraímos o(s) link(s) e avaliamos-os.",
                "placeholder": 'Por exemplo: "Não foi possível entregar a sua encomenda. Confirme em ..."',
            },
            {
                "titel": "Redes sociais",
                "uitleg": "Cole uma mensagem ou link do Instagram, Facebook, WhatsApp ou outra plataforma.",
                "placeholder": "Por exemplo um link de uma mensagem direta ou de um comentário.",
            },
        ],
        "button": "Verificar",
        "warning_empty": "Introduza primeiro um link ou mensagem.",
        "warning_no_url": "Não foi encontrado nenhum link no texto. Verifique se o link foi colado por completo.",
        "why_label": "**Porquê esta avaliação:**",
        "risk_labels": {"laag": "Risco baixo", "mogelijk": "Risco possível", "hoog": "Risco elevado"},
        "expander_title": "Mais sobre esta avaliação",
        "expander_text": (
            "Esta é uma estimativa baseada em características do próprio link, não é uma garantia. "
            "O website não é visitado; apenas o texto do link é avaliado. "
            "Nunca introduza palavras-passe, PINs ou outros dados sensíveis num "
            "site sobre o qual tenha dúvidas, e em caso de dúvida, não abra o link — "
            "verifique antes através de uma app ou site oficial."
        ),
        "sidebar_caption": (
            "Utilize o menu acima para ler mais sobre esta app, "
            "os tipos de fraude mais comuns e dicas gerais de segurança."
        ),
    },
    "it": {
        "lang_label": "🌐 Lingua",
        "tagline": "Verifica rapidamente se un link, un'email, un SMS o un messaggio sui social media potrebbe non essere sicuro.",
        "tabs": [
            {
                "titel": "Link",
                "uitleg": "Incolla un link semplice, ad esempio dal tuo browser o da un messaggio.",
                "placeholder": "https://esempio.it/pagina",
            },
            {
                "titel": "Email",
                "uitleg": "Incolla il testo di un'email sospetta. Estraiamo il/i link e li valutiamo; il mittente e il resto del testo non vengono considerati.",
                "placeholder": 'Ad esempio: "Il tuo account verrà bloccato. Accedi subito tramite ..."',
            },
            {
                "titel": "SMS",
                "uitleg": "Incolla il testo di un SMS sospetto. Estraiamo il/i link e li valutiamo.",
                "placeholder": 'Ad esempio: "Non è stato possibile consegnare il tuo pacco. Conferma tramite ..."',
            },
            {
                "titel": "Social media",
                "uitleg": "Incolla un messaggio o un link da Instagram, Facebook, WhatsApp o un'altra piattaforma.",
                "placeholder": "Ad esempio un link da un messaggio diretto o da un commento.",
            },
        ],
        "button": "Verifica",
        "warning_empty": "Inserisci prima un link o un messaggio.",
        "warning_no_url": "Non è stato trovato alcun link nel testo. Controlla che il link sia stato incollato per intero.",
        "why_label": "**Perché questa valutazione:**",
        "risk_labels": {"laag": "Rischio basso", "mogelijk": "Rischio possibile", "hoog": "Rischio alto"},
        "expander_title": "Maggiori informazioni su questa valutazione",
        "expander_text": (
            "Questa è una stima basata sulle caratteristiche del link stesso, non una garanzia. "
            "Il sito web non viene visitato; viene valutato solo il testo del link. "
            "Non inserire mai password, PIN o altri dati sensibili su un "
            "sito di cui non sei sicuro e, in caso di dubbio, evita di aprire il link — "
            "verifica invece tramite un'app o un sito ufficiale."
        ),
        "sidebar_caption": (
            "Usa il menu qui sopra per saperne di più su questa app, "
            "i tipi di frode più comuni e i consigli generali di sicurezza."
        ),
    },
}
