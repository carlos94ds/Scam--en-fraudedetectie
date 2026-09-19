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
        "website_checkbox_label": "Ook de website bezoeken voor een preciezere inschatting",
        "website_checkbox_help": "Haalt de opgegeven pagina op en kijkt naar kenmerken zoals een wachtwoordveld, doorverwijzingen en of de titel bij het domein past. Duurt een paar seconden langer.",
        "website_fetch_error": "De website kon niet (veilig) bezocht worden, dus is alleen de link zelf beoordeeld.",
        "method_badge_url_only": "URL-only analyse",
        "method_badge_url_website": "URL + website-analyse",
        "risk_labels": {"laag": "Laag risico", "mogelijk": "Mogelijk risico", "hoog": "Hoog risico"},
        "expander_title": "Meer over deze inschatting",
        "expander_text": (
            "Dit is een inschatting op basis van kenmerken van de link zelf, geen garantie. "
            "Standaard wordt de website zelf niet bezocht; alleen de tekst van de link wordt beoordeeld. "
            "Optioneel kun je aanvinken dat de website ook echt bezocht wordt, voor een preciezere inschatting. "
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
        "website_checkbox_label": "Also visit the website for a more precise assessment",
        "website_checkbox_help": "Fetches the given page and looks at features such as a password field, redirects, and whether the title matches the domain. Takes a few seconds longer.",
        "website_fetch_error": "The website could not be visited (safely), so only the link itself was assessed.",
        "method_badge_url_only": "URL-only analysis",
        "method_badge_url_website": "URL + website analysis",
        "risk_labels": {"laag": "Low risk", "mogelijk": "Possible risk", "hoog": "High risk"},
        "expander_title": "More about this assessment",
        "expander_text": (
            "This is an estimate based on characteristics of the link itself, not a guarantee. "
            "By default the website itself is not visited; only the text of the link is assessed. "
            "You can optionally tick a box to have the website actually visited, for a more precise assessment. "
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
        "website_checkbox_label": "Visiter aussi le site pour une évaluation plus précise",
        "website_checkbox_help": "Récupère la page indiquée et examine des éléments tels qu'un champ de mot de passe, des redirections, et si le titre correspond au domaine. Prend quelques secondes de plus.",
        "website_fetch_error": "Le site n'a pas pu être visité (en toute sécurité), seul le lien lui-même a donc été évalué.",
        "method_badge_url_only": "Analyse URL uniquement",
        "method_badge_url_website": "Analyse URL + site web",
        "risk_labels": {"laag": "Risque faible", "mogelijk": "Risque possible", "hoog": "Risque élevé"},
        "expander_title": "En savoir plus sur cette évaluation",
        "expander_text": (
            "Il s'agit d'une estimation basée sur les caractéristiques du lien lui-même, pas d'une garantie. "
            "Par défaut, le site web lui-même n'est pas visité ; seul le texte du lien est évalué. "
            "Vous pouvez cocher une case pour que le site soit réellement visité, pour une évaluation plus précise. "
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
        "website_checkbox_label": "Visitar también el sitio web para una valoración más precisa",
        "website_checkbox_help": "Obtiene la página indicada y analiza aspectos como un campo de contraseña, redirecciones, y si el título coincide con el dominio. Tarda unos segundos más.",
        "website_fetch_error": "No se pudo visitar el sitio web (de forma segura), así que solo se evaluó el enlace en sí.",
        "method_badge_url_only": "Análisis solo de URL",
        "method_badge_url_website": "Análisis de URL + sitio web",
        "risk_labels": {"laag": "Riesgo bajo", "mogelijk": "Riesgo posible", "hoog": "Riesgo alto"},
        "expander_title": "Más información sobre esta valoración",
        "expander_text": (
            "Esto es una estimación basada en características del propio enlace, no una garantía. "
            "Por defecto no se visita el propio sitio web; solo se evalúa el texto del enlace. "
            "Puedes marcar una casilla para que el sitio se visite de verdad, para una valoración más precisa. "
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
        "website_checkbox_label": "Auch die Website besuchen für eine genauere Einschätzung",
        "website_checkbox_help": "Ruft die angegebene Seite ab und prüft Merkmale wie ein Passwortfeld, Weiterleitungen und ob der Titel zur Domain passt. Dauert ein paar Sekunden länger.",
        "website_fetch_error": "Die Website konnte nicht (sicher) besucht werden, daher wurde nur der Link selbst bewertet.",
        "method_badge_url_only": "Nur-URL-Analyse",
        "method_badge_url_website": "URL + Website-Analyse",
        "risk_labels": {"laag": "Geringes Risiko", "mogelijk": "Mögliches Risiko", "hoog": "Hohes Risiko"},
        "expander_title": "Mehr über diese Einschätzung",
        "expander_text": (
            "Dies ist eine Einschätzung anhand von Merkmalen des Links selbst, keine Garantie. "
            "Standardmäßig wird die Website selbst nicht besucht; es wird nur der Text des Links bewertet. "
            "Optional kannst du ein Kästchen ankreuzen, damit die Website tatsächlich besucht wird, für eine genauere Einschätzung. "
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
        "website_checkbox_label": "Visitar também o site para uma avaliação mais precisa",
        "website_checkbox_help": "Obtém a página indicada e analisa características como um campo de palavra-passe, redirecionamentos, e se o título corresponde ao domínio. Demora mais alguns segundos.",
        "website_fetch_error": "Não foi possível visitar o site (com segurança), por isso apenas o link em si foi avaliado.",
        "method_badge_url_only": "Análise apenas do URL",
        "method_badge_url_website": "Análise de URL + site",
        "risk_labels": {"laag": "Risco baixo", "mogelijk": "Risco possível", "hoog": "Risco elevado"},
        "expander_title": "Mais sobre esta avaliação",
        "expander_text": (
            "Esta é uma estimativa baseada em características do próprio link, não é uma garantia. "
            "Por predefinição, o próprio site não é visitado; apenas o texto do link é avaliado. "
            "Pode assinalar uma opção para que o site seja mesmo visitado, para uma avaliação mais precisa. "
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
        "website_checkbox_label": "Visita anche il sito web per una valutazione più precisa",
        "website_checkbox_help": "Recupera la pagina indicata e analizza caratteristiche come un campo password, reindirizzamenti, e se il titolo corrisponde al dominio. Richiede qualche secondo in più.",
        "website_fetch_error": "Non è stato possibile visitare il sito web (in modo sicuro), quindi è stato valutato solo il link stesso.",
        "method_badge_url_only": "Analisi solo URL",
        "method_badge_url_website": "Analisi URL + sito web",
        "risk_labels": {"laag": "Rischio basso", "mogelijk": "Rischio possibile", "hoog": "Rischio alto"},
        "expander_title": "Maggiori informazioni su questa valutazione",
        "expander_text": (
            "Questa è una stima basata sulle caratteristiche del link stesso, non una garanzia. "
            "Per impostazione predefinita il sito web non viene visitato; viene valutato solo il testo del link. "
            "Puoi selezionare una casella per far visitare davvero il sito, per una valutazione più precisa. "
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


def sidebar_language_selector():
    """Toont een taalkiezer in de sidebar en houdt de keuze bij in session_state.
    Wordt gebruikt door de subpagina's (de hoofdpagina heeft zijn eigen kiezer
    bovenaan). Retourneert de actieve taalcode."""
    import streamlit as st

    if "lang" not in st.session_state:
        st.session_state["lang"] = "nl"

    lang_codes = list(LANGUAGES.keys())
    selected = st.sidebar.selectbox(
        UI_TEXT[st.session_state["lang"]]["lang_label"],
        options=lang_codes,
        format_func=lambda code: LANGUAGES[code],
        index=lang_codes.index(st.session_state["lang"]),
        key="lang_select_sidebar",
    )
    st.session_state["lang"] = selected
    return selected


PAGES_TEXT = {
    "over": {
        "nl": {
            "page_title": "Over VerdachtLink",
            "title": "Over VerdachtLink",
            "body": """
### Doel van deze applicatie

Veel mensen vinden het lastig om in te schatten of een link, e-mail, sms of
bericht op social media te vertrouwen is. Verdachte berichten zien er vaak
overtuigend uit, en de meeste mensen hebben geen technische kennis van
phishing, domeinen of beveiligde verbindingen om dat zelf te controleren.

VerdachtLink is gebouwd om die inschatting toegankelijker te maken. Je plakt
een link of bericht, en de applicatie geeft in gewone taal een indicatie van
het risico — zonder dat je zelf iets hoeft te begrijpen van de techniek
erachter.

### Hoe het werkt

Op de achtergrond analyseert een Machine Learning-model kenmerken van de
link zelf: de lengte, het gebruikte domein, of de verbinding beveiligd is,
en meer van dat soort structuurkenmerken. Op basis daarvan geeft het systeem
een risico-inschatting: laag, mogelijk of hoog.

### Wat deze applicatie niet doet

- De opgegeven website wordt standaard niet bezocht. Er wordt alleen naar de
  tekst van de link gekeken. Optioneel kun je aanvinken dat de website ook
  echt bezocht wordt, voor een preciezere inschatting.
- Bij e-mail, sms en social media wordt alleen de link in het bericht
  beoordeeld, niet de afzender of de rest van de inhoud.
- De inschatting is geen garantie. Een link met een lage risico-score kan
  in zeldzame gevallen alsnog onveilig zijn, en andersom.

### Achtergrond

Dit project is ontwikkeld als onderwijs- en portfolioproject binnen de
opleiding HBO-ICT, richting Data Science & Artificial Intelligence, gericht
op het toegankelijker maken van fraude- en phishingherkenning voor mensen
zonder technische achtergrond.
""",
        },
        "en": {
            "page_title": "About VerdachtLink",
            "title": "About VerdachtLink",
            "body": """
### Purpose of this application

Many people find it hard to judge whether a link, email, text message or
social media message can be trusted. Suspicious messages often look
convincing, and most people don't have the technical knowledge of
phishing, domains or secure connections to check this themselves.

VerdachtLink was built to make that assessment more accessible. You paste
a link or message, and the application gives a plain-language indication
of the risk — without you needing to understand the technology behind it.

### How it works

Behind the scenes, a machine learning model analyses characteristics of
the link itself: its length, the domain used, whether the connection is
secure, and other structural features like these. Based on that, the
system gives a risk assessment: low, possible or high.

### What this application does not do

- By default, the website itself is not visited. Only the text of the
  link is examined. You can optionally tick a box to have the website
  actually visited, for a more precise assessment.
- For email, text messages and social media, only the link in the
  message is assessed, not the sender or the rest of the content.
- The assessment is not a guarantee. A link with a low risk score can, in
  rare cases, still be unsafe, and vice versa.

### Background

This project was developed as an educational and portfolio project within
the HBO-ICT programme, Data Science & Artificial Intelligence
specialization, aimed at making fraud and phishing recognition more
accessible for people without a technical background.
""",
        },
        "fr": {
            "page_title": "À propos de VerdachtLink",
            "title": "À propos de VerdachtLink",
            "body": """
### Objectif de cette application

Beaucoup de gens ont du mal à évaluer si un lien, un e-mail, un SMS ou un
message sur les réseaux sociaux est fiable. Les messages suspects
paraissent souvent convaincants, et la plupart des gens n'ont pas les
connaissances techniques sur le phishing, les domaines ou les connexions
sécurisées pour le vérifier eux-mêmes.

VerdachtLink a été conçu pour rendre cette évaluation plus accessible.
Vous collez un lien ou un message, et l'application donne en langage
simple une indication du risque — sans que vous ayez besoin de comprendre
la technique sous-jacente.

### Comment ça marche

En arrière-plan, un modèle de Machine Learning analyse les
caractéristiques du lien lui-même : sa longueur, le domaine utilisé, si la
connexion est sécurisée, et d'autres caractéristiques structurelles de ce
type. Sur cette base, le système donne une évaluation du risque : faible,
possible ou élevé.

### Ce que cette application ne fait pas

- Par défaut, le site web indiqué n'est pas visité. Seul le texte du lien
  est examiné. Vous pouvez cocher une case pour que le site soit
  réellement visité, pour une évaluation plus précise.
- Pour les e-mails, SMS et réseaux sociaux, seul le lien contenu dans le
  message est évalué, pas l'expéditeur ni le reste du contenu.
- L'évaluation n'est pas une garantie. Un lien avec un score de risque
  faible peut, dans de rares cas, être malgré tout dangereux, et
  inversement.

### Contexte

Ce projet a été développé comme projet pédagogique et de portfolio dans le
cadre de la formation HBO-ICT, spécialisation Data Science &
Intelligence Artificielle, visant à rendre la détection de fraude et de
phishing plus accessible aux personnes sans formation technique.
""",
        },
        "es": {
            "page_title": "Acerca de VerdachtLink",
            "title": "Acerca de VerdachtLink",
            "body": """
### Objetivo de esta aplicación

A muchas personas les resulta difícil evaluar si se puede confiar en un
enlace, correo electrónico, SMS o mensaje de redes sociales. Los mensajes
sospechosos suelen parecer convincentes, y la mayoría de las personas no
tienen conocimientos técnicos sobre phishing, dominios o conexiones
seguras para comprobarlo por sí mismas.

VerdachtLink se creó para hacer esa evaluación más accesible. Pegas un
enlace o mensaje, y la aplicación da una indicación del riesgo en lenguaje
sencillo, sin que tengas que entender la tecnología detrás de ello.

### Cómo funciona

Detrás de escena, un modelo de Machine Learning analiza características
del propio enlace: su longitud, el dominio utilizado, si la conexión es
segura y otras características estructurales de ese tipo. Con base en
ello, el sistema da una valoración del riesgo: bajo, posible o alto.

### Lo que esta aplicación no hace

- Por defecto no se visita el sitio web indicado. Solo se examina el texto
  del enlace. Puedes marcar una casilla para que el sitio se visite de
  verdad, para una valoración más precisa.
- En correos, SMS y redes sociales, solo se evalúa el enlace del mensaje,
  no el remitente ni el resto del contenido.
- La valoración no es una garantía. Un enlace con una puntuación de
  riesgo baja puede, en casos excepcionales, seguir siendo inseguro, y
  viceversa.

### Contexto

Este proyecto se desarrolló como proyecto educativo y de portfolio dentro
de la formación HBO-ICT, especialización en Data Science e Inteligencia
Artificial, con el objetivo de hacer la detección de fraude y phishing
más accesible para personas sin formación técnica.
""",
        },
        "de": {
            "page_title": "Über VerdachtLink",
            "title": "Über VerdachtLink",
            "body": """
### Zweck dieser Anwendung

Viele Menschen finden es schwierig einzuschätzen, ob ein Link, eine
E-Mail, SMS oder Social-Media-Nachricht vertrauenswürdig ist. Verdächtige
Nachrichten wirken oft überzeugend, und die meisten Menschen haben nicht
das technische Wissen über Phishing, Domains oder sichere Verbindungen,
um das selbst zu prüfen.

VerdachtLink wurde entwickelt, um diese Einschätzung zugänglicher zu
machen. Du fügst einen Link oder eine Nachricht ein, und die Anwendung
gibt in einfacher Sprache eine Einschätzung des Risikos — ohne dass du
die dahinterliegende Technik verstehen musst.

### Wie es funktioniert

Im Hintergrund analysiert ein Machine-Learning-Modell Merkmale des Links
selbst: die Länge, die verwendete Domain, ob die Verbindung sicher ist,
und weitere derartige Strukturmerkmale. Auf dieser Grundlage gibt das
System eine Risikoeinschätzung ab: gering, möglich oder hoch.

### Was diese Anwendung nicht tut

- Standardmäßig wird die angegebene Website nicht besucht. Es wird nur der
  Text des Links betrachtet. Optional kannst du ein Kästchen ankreuzen,
  damit die Website tatsächlich besucht wird, für eine genauere
  Einschätzung.
- Bei E-Mail, SMS und Social Media wird nur der Link in der Nachricht
  bewertet, nicht der Absender oder der übrige Inhalt.
- Die Einschätzung ist keine Garantie. Ein Link mit niedrigem
  Risiko-Score kann in seltenen Fällen dennoch unsicher sein, und
  umgekehrt.

### Hintergrund

Dieses Projekt wurde als Bildungs- und Portfolioprojekt im Rahmen des
HBO-ICT-Studiengangs, Schwerpunkt Data Science & Artificial Intelligence,
entwickelt, mit dem Ziel, Betrugs- und Phishing-Erkennung für Menschen
ohne technischen Hintergrund zugänglicher zu machen.
""",
        },
        "pt": {
            "page_title": "Sobre a VerdachtLink",
            "title": "Sobre a VerdachtLink",
            "body": """
### Objetivo desta aplicação

Muitas pessoas acham difícil avaliar se um link, e-mail, SMS ou mensagem
de rede social é de confiança. As mensagens suspeitas costumam parecer
convincentes, e a maioria das pessoas não tem conhecimento técnico sobre
phishing, domínios ou ligações seguras para verificar isso por si
mesmas.

A VerdachtLink foi criada para tornar essa avaliação mais acessível. Colas
um link ou mensagem, e a aplicação dá uma indicação do risco em linguagem
simples — sem que precises de perceber a tecnologia por trás disso.

### Como funciona

Por trás dos bastidores, um modelo de Machine Learning analisa
características do próprio link: o seu comprimento, o domínio utilizado,
se a ligação é segura, e outras características estruturais deste tipo.
Com base nisso, o sistema dá uma avaliação de risco: baixo, possível ou
elevado.

### O que esta aplicação não faz

- Por predefinição, o site indicado não é visitado. Apenas o texto do link
  é examinado. Pode assinalar uma opção para que o site seja mesmo
  visitado, para uma avaliação mais precisa.
- Em e-mail, SMS e redes sociais, apenas o link na mensagem é avaliado,
  não o remetente nem o resto do conteúdo.
- A avaliação não é uma garantia. Um link com uma pontuação de risco
  baixa pode, em casos raros, ainda assim ser inseguro, e vice-versa.

### Contexto

Este projeto foi desenvolvido como projeto educativo e de portfólio no
âmbito do curso HBO-ICT, especialização em Data Science & Artificial
Intelligence, com o objetivo de tornar o reconhecimento de fraude e
phishing mais acessível para pessoas sem formação técnica.
""",
        },
        "it": {
            "page_title": "Informazioni su VerdachtLink",
            "title": "Informazioni su VerdachtLink",
            "body": """
### Obiettivo di questa applicazione

Molte persone trovano difficile valutare se un link, un'email, un SMS o
un messaggio sui social media sia affidabile. I messaggi sospetti spesso
sembrano convincenti, e la maggior parte delle persone non ha le
conoscenze tecniche su phishing, domini o connessioni sicure per
verificarlo da sola.

VerdachtLink è stata creata per rendere questa valutazione più
accessibile. Incolli un link o un messaggio, e l'applicazione fornisce
un'indicazione del rischio in linguaggio semplice — senza che tu debba
capire la tecnologia che c'è dietro.

### Come funziona

Dietro le quinte, un modello di Machine Learning analizza le
caratteristiche del link stesso: la lunghezza, il dominio utilizzato, se
la connessione è sicura e altre caratteristiche strutturali di questo
tipo. Sulla base di ciò, il sistema fornisce una valutazione del rischio:
basso, possibile o alto.

### Cosa non fa questa applicazione

- Per impostazione predefinita il sito indicato non viene visitato. Viene
  esaminato solo il testo del link. Puoi selezionare una casella per far
  visitare davvero il sito, per una valutazione più precisa.
- Per email, SMS e social media, viene valutato solo il link nel
  messaggio, non il mittente né il resto del contenuto.
- La valutazione non è una garanzia. Un link con un punteggio di rischio
  basso può, in rari casi, essere comunque pericoloso, e viceversa.

### Contesto

Questo progetto è stato sviluppato come progetto didattico e di
portfolio nell'ambito del corso di laurea HBO-ICT, specializzazione Data
Science & Artificial Intelligence, con l'obiettivo di rendere il
riconoscimento di frodi e phishing più accessibile a persone senza un
background tecnico.
""",
        },
    },
    "fraude": {
        "nl": {
            "page_title": "Soorten fraude",
            "title": "Veelvoorkomende soorten fraude en scams",
            "body": """
Online fraude komt in verschillende vormen voor. Hieronder staan de meest
voorkomende soorten, zodat je weet waar je op kunt letten.

### Phishing (e-mail)
Een e-mail die eruitziet alsof hij van een bank, webshop of overheidsinstantie
komt, met de vraag om in te loggen, gegevens te bevestigen of een betaling te
doen via een bijgevoegde link. De link leidt naar een nagemaakte website die
inloggegevens of betaalgegevens steelt.

### Smishing (sms-phishing)
Dezelfde aanpak als phishing, maar dan via sms. Vaak met een boodschap over
een pakket dat niet bezorgd kon worden, een openstaande betaling, of een
account dat geblokkeerd dreigt te worden.

### Vishing (telefonische fraude)
Fraude via een telefoongesprek, waarbij iemand zich voordoet als bijvoorbeeld
een bankmedewerker of helpdeskmedewerker, met als doel gegevens, codes of
toegang tot je apparaat te krijgen.

### Nepwebshops
Websites die net echte webshops lijken, met aantrekkelijke aanbiedingen, maar
waar je product na betaling nooit wordt geleverd.

### Social-media-scams
Nepaccounts die zich voordoen als een bekend persoon, bedrijf of vriend(in),
vaak met een verzoek om geld te lenen, op een link te klikken, of mee te doen
aan een "actie" of winactie die niet bestaat.

### Factuurfraude / CEO-fraude
Vooral gericht op bedrijven: een bericht dat lijkt te komen van een
leidinggevende of vaste leverancier, met het verzoek om snel een betaling uit
te voeren naar een (frauduleus) rekeningnummer.

### Investerings- en cryptofraude
Beloftes van snelle, hoge en gegarandeerde winst op een investering of
cryptomunt, vaak met kunstmatige tijdsdruk ("nog maar enkele plekken
beschikbaar").

### Romancefraude
Iemand bouwt via een datingapp of social media een (nep)relatie op, om
uiteindelijk om geld te vragen, bijvoorbeeld voor een noodgeval of een
vliegticket.
""",
        },
        "en": {
            "page_title": "Types of fraud",
            "title": "Common types of fraud and scams",
            "body": """
Online fraud comes in various forms. Below are the most common types, so
you know what to watch out for.

### Phishing (email)
An email that looks like it comes from a bank, webshop or government
agency, asking you to log in, confirm details or make a payment via an
attached link. The link leads to a fake website that steals login or
payment details.

### Smishing (SMS phishing)
The same approach as phishing, but via text message. Often with a message
about a parcel that could not be delivered, an outstanding payment, or an
account that is about to be blocked.

### Vishing (phone fraud)
Fraud via a phone call, where someone pretends to be, for example, a bank
employee or help desk employee, aiming to obtain data, codes or access to
your device.

### Fake webshops
Websites that look just like real webshops, with attractive offers, but
where your product is never delivered after payment.

### Social media scams
Fake accounts pretending to be a known person, company or friend, often
asking to borrow money, to click a link, or to join a "promotion" or prize
draw that doesn't actually exist.

### Invoice fraud / CEO fraud
Mainly targeted at businesses: a message that appears to come from a
manager or regular supplier, requesting an urgent payment to a
(fraudulent) account number.

### Investment and crypto fraud
Promises of fast, high and guaranteed returns on an investment or
cryptocurrency, often with artificial time pressure ("only a few spots
left").

### Romance fraud
Someone builds a (fake) relationship via a dating app or social media, in
order to eventually ask for money, for example for an emergency or a
plane ticket.
""",
        },
        "fr": {
            "page_title": "Types de fraude",
            "title": "Types courants de fraude et d'arnaques",
            "body": """
La fraude en ligne prend différentes formes. Voici les types les plus
courants, afin que vous sachiez à quoi faire attention.

### Phishing (e-mail)
Un e-mail qui semble provenir d'une banque, d'une boutique en ligne ou
d'une administration, demandant de se connecter, de confirmer des
informations ou d'effectuer un paiement via un lien joint. Le lien mène
vers un faux site qui vole des identifiants ou des données de paiement.

### Smishing (phishing par SMS)
La même approche que le phishing, mais par SMS. Souvent avec un message
concernant un colis qui n'a pas pu être livré, un paiement en attente, ou
un compte sur le point d'être bloqué.

### Vishing (fraude téléphonique)
Fraude par appel téléphonique, où quelqu'un se fait passer par exemple
pour un employé de banque ou du service d'assistance, dans le but
d'obtenir des données, des codes ou l'accès à votre appareil.

### Faux sites de vente en ligne
Des sites qui ressemblent à de vraies boutiques en ligne, avec des offres
attrayantes, mais où votre produit n'est jamais livré après paiement.

### Arnaques sur les réseaux sociaux
Des faux comptes se faisant passer pour une personne connue, une
entreprise ou un(e) ami(e), demandant souvent de prêter de l'argent, de
cliquer sur un lien, ou de participer à une "promotion" ou un concours
qui n'existe pas.

### Fraude à la facture / fraude au président
Principalement dirigée contre les entreprises : un message semblant venir
d'un responsable ou d'un fournisseur habituel, demandant d'effectuer
rapidement un paiement vers un numéro de compte (frauduleux).

### Fraude aux investissements et aux cryptomonnaies
Promesses de gains rapides, élevés et garantis sur un investissement ou
une cryptomonnaie, souvent avec une pression temporelle artificielle
("il ne reste que quelques places").

### Fraude sentimentale (romance scam)
Quelqu'un construit une (fausse) relation via une application de
rencontre ou les réseaux sociaux, pour finalement demander de l'argent,
par exemple pour une urgence ou un billet d'avion.
""",
        },
        "es": {
            "page_title": "Tipos de fraude",
            "title": "Tipos comunes de fraude y estafas",
            "body": """
El fraude en línea se presenta de varias formas. A continuación, los
tipos más comunes, para que sepas a qué prestar atención.

### Phishing (correo electrónico)
Un correo que parece venir de un banco, tienda online o administración
pública, pidiendo iniciar sesión, confirmar datos o realizar un pago a
través de un enlace adjunto. El enlace lleva a un sitio falso que roba
credenciales o datos de pago.

### Smishing (phishing por SMS)
El mismo enfoque que el phishing, pero por SMS. A menudo con un mensaje
sobre un paquete que no se pudo entregar, un pago pendiente, o una cuenta
a punto de ser bloqueada.

### Vishing (fraude telefónico)
Fraude mediante una llamada telefónica, en la que alguien se hace pasar,
por ejemplo, por un empleado del banco o del servicio de asistencia, con
el objetivo de obtener datos, códigos o acceso a tu dispositivo.

### Tiendas online falsas
Sitios que parecen tiendas online reales, con ofertas atractivas, pero
donde tu producto nunca se entrega tras el pago.

### Estafas en redes sociales
Cuentas falsas que se hacen pasar por una persona conocida, empresa o
amigo/a, a menudo pidiendo prestar dinero, hacer clic en un enlace, o
participar en una "promoción" o sorteo que no existe.

### Fraude de facturas / fraude del CEO
Dirigido principalmente a empresas: un mensaje que parece provenir de un
directivo o proveedor habitual, solicitando realizar rápidamente un pago
a un número de cuenta (fraudulento).

### Fraude de inversiones y criptomonedas
Promesas de beneficios rápidos, altos y garantizados en una inversión o
criptomoneda, a menudo con presión de tiempo artificial ("solo quedan
unas pocas plazas").

### Fraude romántico
Alguien construye una (falsa) relación a través de una app de citas o
redes sociales, para finalmente pedir dinero, por ejemplo para una
emergencia o un billete de avión.
""",
        },
        "de": {
            "page_title": "Betrugsarten",
            "title": "Häufige Betrugs- und Scam-Arten",
            "body": """
Online-Betrug kommt in verschiedenen Formen vor. Nachfolgend die
häufigsten Arten, damit du weißt, worauf du achten musst.

### Phishing (E-Mail)
Eine E-Mail, die aussieht, als käme sie von einer Bank, einem Webshop
oder einer Behörde, mit der Bitte, sich anzumelden, Daten zu bestätigen
oder eine Zahlung über einen beigefügten Link vorzunehmen. Der Link führt
zu einer gefälschten Website, die Login- oder Zahlungsdaten stiehlt.

### Smishing (SMS-Phishing)
Der gleiche Ansatz wie Phishing, jedoch per SMS. Oft mit einer Nachricht
über ein Paket, das nicht zugestellt werden konnte, eine offene Zahlung
oder ein Konto, das gesperrt zu werden droht.

### Vishing (Telefonbetrug)
Betrug per Telefonanruf, bei dem sich jemand zum Beispiel als
Bankmitarbeiter oder Helpdesk-Mitarbeiter ausgibt, mit dem Ziel, Daten,
Codes oder Zugang zu deinem Gerät zu erhalten.

### Gefälschte Webshops
Websites, die wie echte Webshops aussehen, mit attraktiven Angeboten,
aber bei denen dein Produkt nach der Zahlung nie geliefert wird.

### Social-Media-Betrug
Fake-Konten, die sich als bekannte Person, Unternehmen oder Freund(in)
ausgeben, oft mit der Bitte, Geld zu leihen, auf einen Link zu klicken,
oder an einer "Aktion" oder Gewinnspiel teilzunehmen, die nicht
existiert.

### Rechnungsbetrug / CEO-Betrug
Vor allem gegen Unternehmen gerichtet: eine Nachricht, die scheinbar von
einer Führungskraft oder einem festen Lieferanten stammt, mit der Bitte,
schnell eine Zahlung auf eine (betrügerische) Kontonummer zu leisten.

### Investment- und Kryptobetrug
Versprechen von schnellen, hohen und garantierten Gewinnen bei einer
Investition oder Kryptowährung, oft mit künstlichem Zeitdruck ("nur noch
wenige Plätze verfügbar").

### Romance Scam (Liebesbetrug)
Jemand baut über eine Dating-App oder Social Media eine (falsche)
Beziehung auf, um schließlich um Geld zu bitten, zum Beispiel für einen
Notfall oder ein Flugticket.
""",
        },
        "pt": {
            "page_title": "Tipos de fraude",
            "title": "Tipos comuns de fraude e burlas",
            "body": """
A fraude online surge de várias formas. Abaixo estão os tipos mais
comuns, para que saibas o que deves ter em atenção.

### Phishing (e-mail)
Um e-mail que parece vir de um banco, loja online ou entidade
governamental, pedindo para iniciar sessão, confirmar dados ou fazer um
pagamento através de um link anexado. O link leva a um site falso que
rouba credenciais ou dados de pagamento.

### Smishing (phishing por SMS)
A mesma abordagem do phishing, mas por SMS. Muitas vezes com uma
mensagem sobre uma encomenda que não pôde ser entregue, um pagamento em
aberto, ou uma conta prestes a ser bloqueada.

### Vishing (fraude telefónica)
Fraude através de uma chamada telefónica, em que alguém se faz passar,
por exemplo, por um funcionário do banco ou do apoio ao cliente, com o
objetivo de obter dados, códigos ou acesso ao teu dispositivo.

### Lojas online falsas
Sites que se parecem com lojas online verdadeiras, com ofertas
apelativas, mas onde o teu produto nunca é entregue após o pagamento.

### Burlas nas redes sociais
Contas falsas que se fazem passar por uma pessoa conhecida, empresa ou
amigo(a), muitas vezes pedindo para emprestar dinheiro, clicar num link,
ou participar numa "promoção" ou sorteio que não existe.

### Fraude de faturas / fraude do CEO
Dirigida sobretudo a empresas: uma mensagem que parece vir de um
superior hierárquico ou fornecedor habitual, pedindo para efetuar
rapidamente um pagamento para um número de conta (fraudulento).

### Fraude de investimentos e criptomoedas
Promessas de lucros rápidos, elevados e garantidos num investimento ou
criptomoeda, muitas vezes com pressão de tempo artificial ("restam
apenas algumas vagas").

### Fraude romântica
Alguém constrói uma (falsa) relação através de uma app de encontros ou
redes sociais, para no final pedir dinheiro, por exemplo para uma
emergência ou um bilhete de avião.
""",
        },
        "it": {
            "page_title": "Tipi di frode",
            "title": "Tipi comuni di frode e truffe",
            "body": """
La frode online si presenta in diverse forme. Di seguito i tipi più
comuni, così sai a cosa prestare attenzione.

### Phishing (email)
Un'email che sembra provenire da una banca, un negozio online o un ente
pubblico, che chiede di accedere, confermare dati o effettuare un
pagamento tramite un link allegato. Il link porta a un sito falso che
ruba credenziali o dati di pagamento.

### Smishing (phishing via SMS)
Lo stesso approccio del phishing, ma via SMS. Spesso con un messaggio su
un pacco che non è stato possibile consegnare, un pagamento in sospeso,
o un account sul punto di essere bloccato.

### Vishing (frode telefonica)
Frode tramite una telefonata, in cui qualcuno si finge, ad esempio, un
dipendente della banca o dell'assistenza clienti, con l'obiettivo di
ottenere dati, codici o accesso al tuo dispositivo.

### Negozi online falsi
Siti che sembrano veri negozi online, con offerte allettanti, ma dove il
tuo prodotto non viene mai consegnato dopo il pagamento.

### Truffe sui social media
Account falsi che si fingono una persona conosciuta, un'azienda o
un'amico/a, spesso chiedendo di prestare denaro, cliccare su un link, o
partecipare a una "promozione" o concorso a premi inesistente.

### Frode delle fatture / frode del CEO
Rivolta soprattutto alle aziende: un messaggio che sembra provenire da
un dirigente o da un fornitore abituale, con la richiesta di effettuare
rapidamente un pagamento verso un numero di conto (fraudolento).

### Frode di investimenti e criptovalute
Promesse di guadagni rapidi, elevati e garantiti su un investimento o
una criptovaluta, spesso con una pressione temporale artificiale
("restano solo pochi posti disponibili").

### Truffa romantica
Qualcuno costruisce una (falsa) relazione tramite un'app di incontri o i
social media, per poi chiedere denaro, ad esempio per un'emergenza o un
biglietto aereo.
""",
        },
    },
    "tips": {
        "nl": {
            "page_title": "Veiligheidstips",
            "title": "Veiligheidstips",
            "body": """
### Voordat je op een link klikt

- Controleer het volledige webadres, niet alleen de eerste paar letters.
- Twijfel je? Klik niet op de link. Typ het adres van de organisatie zelf in
  je browser, of open de officiële app.
- Let op een gevoel van urgentie ("direct actie vereist", "anders wordt uw
  account geblokkeerd"). Dat is een veelgebruikte truc om je minder kritisch
  te laten nadenken.

### Bij e-mail en sms

- Controleer het volledige e-mailadres van de afzender, niet alleen de
  weergavenaam.
- Een organisatie vraagt normaal gesproken nooit naar je volledige
  wachtwoord, pincode, of creditcardgegevens via e-mail of sms.
- Slechte spelling of een onpersoonlijke aanhef ("Geachte klant") kan een
  signaal zijn, maar ontbreekt steeds vaker bij professioneel gemaakte
  phishingberichten. Vertrouw er niet blindelings op.

### Algemene voorzorgsmaatregelen

- Gebruik voor belangrijke accounts tweestapsverificatie.
- Gebruik unieke wachtwoorden per website of dienst, bijvoorbeeld met een
  wachtwoordmanager.
- Houd apps, browsers en je besturingssysteem up-to-date.
- Maak regelmatig een back-up van belangrijke bestanden.

### Als je toch hebt geklikt of gegevens hebt ingevuld

- Wijzig direct je wachtwoord, en bij hergebruik van dat wachtwoord ook bij
  andere accounts.
- Neem bij een mogelijke financiële fraude direct contact op met je bank.
- Overweeg aangifte te doen bij de politie.
- Meld het bericht bij de organisatie waarvan de afzender zich voordeed, en
  waar mogelijk bij een officiële meldpunt voor phishing en fraude.

VerdachtLink helpt bij het inschatten van risico, maar vervangt geen
gezond wantrouwen: bij twijfel is het altijd veiliger om een link niet te
openen.
""",
        },
        "en": {
            "page_title": "Safety tips",
            "title": "Safety tips",
            "body": """
### Before you click a link

- Check the full web address, not just the first few letters.
- Not sure? Don't click the link. Type the organisation's address
  yourself into your browser, or open the official app.
- Watch out for a sense of urgency ("action required immediately",
  "otherwise your account will be blocked"). That's a common trick to
  make you think less critically.

### With email and text messages

- Check the sender's full email address, not just the display name.
- An organisation normally never asks for your full password, PIN code,
  or credit card details via email or text message.
- Poor spelling or an impersonal greeting ("Dear customer") can be a
  warning sign, but is increasingly absent from professionally made
  phishing messages. Don't rely on it blindly.

### General precautions

- Use two-factor authentication for important accounts.
- Use unique passwords per website or service, for example with a
  password manager.
- Keep apps, browsers and your operating system up to date.
- Back up important files regularly.

### If you did click or entered information anyway

- Change your password immediately, and also for other accounts if you
  reused that password.
- Contact your bank immediately in case of possible financial fraud.
- Consider filing a police report.
- Report the message to the organisation the sender pretended to be, and
  where possible to an official reporting point for phishing and fraud.

VerdachtLink helps assess risk, but doesn't replace healthy suspicion: if
in doubt, it's always safer not to open a link.
""",
        },
        "fr": {
            "page_title": "Conseils de sécurité",
            "title": "Conseils de sécurité",
            "body": """
### Avant de cliquer sur un lien

- Vérifiez l'adresse web complète, pas seulement les premières lettres.
- Un doute ? Ne cliquez pas sur le lien. Tapez vous-même l'adresse de
  l'organisation dans votre navigateur, ou ouvrez l'application
  officielle.
- Méfiez-vous d'un sentiment d'urgence ("action immédiate requise",
  "sinon votre compte sera bloqué"). C'est une technique courante pour
  vous faire réfléchir de façon moins critique.

### Pour les e-mails et SMS

- Vérifiez l'adresse e-mail complète de l'expéditeur, pas seulement le
  nom affiché.
- Une organisation ne demande normalement jamais votre mot de passe
  complet, code PIN ou données de carte bancaire par e-mail ou SMS.
- Une mauvaise orthographe ou une formule impersonnelle ("Cher client")
  peut être un signal, mais elle est de moins en moins présente dans les
  messages de phishing bien conçus. Ne vous y fiez pas aveuglément.

### Précautions générales

- Utilisez l'authentification à deux facteurs pour les comptes
  importants.
- Utilisez des mots de passe uniques par site ou service, par exemple
  avec un gestionnaire de mots de passe.
- Maintenez vos applications, navigateurs et système d'exploitation à
  jour.
- Sauvegardez régulièrement vos fichiers importants.

### Si vous avez quand même cliqué ou saisi des informations

- Changez immédiatement votre mot de passe, ainsi que pour les autres
  comptes si vous l'avez réutilisé.
- En cas de fraude financière potentielle, contactez immédiatement votre
  banque.
- Envisagez de porter plainte auprès de la police.
- Signalez le message à l'organisation dont l'expéditeur a usurpé
  l'identité, et si possible à un point de signalement officiel pour le
  phishing et la fraude.

VerdachtLink aide à évaluer le risque, mais ne remplace pas une méfiance
saine : en cas de doute, il est toujours plus sûr de ne pas ouvrir un
lien.
""",
        },
        "es": {
            "page_title": "Consejos de seguridad",
            "title": "Consejos de seguridad",
            "body": """
### Antes de hacer clic en un enlace

- Comprueba la dirección web completa, no solo las primeras letras.
- ¿Tienes dudas? No hagas clic en el enlace. Escribe tú mismo la
  dirección de la organización en tu navegador, o abre la app oficial.
- Presta atención a una sensación de urgencia ("se requiere acción
  inmediata", "de lo contrario se bloqueará tu cuenta"). Es un truco muy
  usado para que pienses de forma menos crítica.

### En correos electrónicos y SMS

- Comprueba la dirección de correo completa del remitente, no solo el
  nombre mostrado.
- Una organización normalmente nunca pide tu contraseña completa, PIN o
  datos de tarjeta de crédito por correo o SMS.
- Una mala ortografía o un saludo impersonal ("Estimado cliente") puede
  ser una señal, pero cada vez está más ausente en mensajes de phishing
  elaborados profesionalmente. No confíes en ello ciegamente.

### Precauciones generales

- Usa verificación en dos pasos para cuentas importantes.
- Usa contraseñas únicas por sitio web o servicio, por ejemplo con un
  gestor de contraseñas.
- Mantén apps, navegadores y tu sistema operativo actualizados.
- Haz copias de seguridad de archivos importantes con regularidad.

### Si aun así hiciste clic o introdujiste datos

- Cambia tu contraseña de inmediato, y también en otras cuentas si
  reutilizaste esa contraseña.
- Ante un posible fraude financiero, contacta de inmediato con tu banco.
- Considera presentar una denuncia ante la policía.
- Informa del mensaje a la organización suplantada, y si es posible a un
  punto de denuncia oficial de phishing y fraude.

VerdachtLink ayuda a valorar el riesgo, pero no sustituye una sana
desconfianza: si tienes dudas, siempre es más seguro no abrir un enlace.
""",
        },
        "de": {
            "page_title": "Sicherheitstipps",
            "title": "Sicherheitstipps",
            "body": """
### Bevor du auf einen Link klickst

- Prüfe die vollständige Webadresse, nicht nur die ersten paar
  Buchstaben.
- Unsicher? Klicke nicht auf den Link. Tippe die Adresse der
  Organisation selbst in deinen Browser ein, oder öffne die offizielle
  App.
- Achte auf ein Gefühl der Dringlichkeit ("sofortiges Handeln
  erforderlich", "sonst wird Ihr Konto gesperrt"). Das ist ein häufiger
  Trick, um dich weniger kritisch denken zu lassen.

### Bei E-Mail und SMS

- Prüfe die vollständige E-Mail-Adresse des Absenders, nicht nur den
  Anzeigenamen.
- Eine Organisation fragt normalerweise nie per E-Mail oder SMS nach
  deinem vollständigen Passwort, PIN-Code oder Kreditkartendaten.
- Schlechte Rechtschreibung oder eine unpersönliche Anrede ("Sehr
  geehrter Kunde") kann ein Warnsignal sein, fehlt aber zunehmend bei
  professionell gemachten Phishing-Nachrichten. Verlasse dich nicht
  blind darauf.

### Allgemeine Vorsichtsmaßnahmen

- Nutze Zwei-Faktor-Authentifizierung für wichtige Konten.
- Verwende einzigartige Passwörter pro Website oder Dienst, zum Beispiel
  mit einem Passwort-Manager.
- Halte Apps, Browser und dein Betriebssystem auf dem neuesten Stand.
- Erstelle regelmäßig Backups wichtiger Dateien.

### Wenn du trotzdem geklickt oder Daten eingegeben hast

- Ändere sofort dein Passwort, und bei Wiederverwendung auch bei anderen
  Konten.
- Kontaktiere bei möglichem Finanzbetrug sofort deine Bank.
- Erwäge eine Anzeige bei der Polizei.
- Melde die Nachricht der Organisation, als die sich der Absender
  ausgegeben hat, und wo möglich bei einer offiziellen Meldestelle für
  Phishing und Betrug.

VerdachtLink hilft bei der Risikoeinschätzung, ersetzt aber kein
gesundes Misstrauen: im Zweifel ist es immer sicherer, einen Link nicht
zu öffnen.
""",
        },
        "pt": {
            "page_title": "Dicas de segurança",
            "title": "Dicas de segurança",
            "body": """
### Antes de clicares num link

- Verifica o endereço web completo, não apenas as primeiras letras.
- Tens dúvidas? Não cliques no link. Digita tu próprio o endereço da
  organização no navegador, ou abre a app oficial.
- Presta atenção a uma sensação de urgência ("ação imediata necessária",
  "caso contrário a sua conta será bloqueada"). É um truque comum para
  te fazer pensar de forma menos crítica.

### Em e-mails e SMS

- Verifica o endereço de e-mail completo do remetente, não apenas o
  nome apresentado.
- Uma organização normalmente nunca pede a tua palavra-passe completa,
  PIN ou dados do cartão de crédito por e-mail ou SMS.
- Erros ortográficos ou uma saudação impessoal ("Caro cliente") podem
  ser um sinal, mas estão cada vez mais ausentes em mensagens de
  phishing bem elaboradas. Não confies cegamente nisso.

### Precauções gerais

- Usa verificação em dois passos para contas importantes.
- Usa palavras-passe únicas por site ou serviço, por exemplo com um
  gestor de palavras-passe.
- Mantém apps, navegadores e o sistema operativo atualizados.
- Faz cópias de segurança regulares de ficheiros importantes.

### Se ainda assim clicaste ou introduziste dados

- Muda imediatamente a tua palavra-passe, e também noutras contas caso
  a tenhas reutilizado.
- Em caso de possível fraude financeira, contacta imediatamente o teu
  banco.
- Considera apresentar queixa à polícia.
- Reporta a mensagem à organização que o remetente fingiu ser, e, se
  possível, a um ponto de denúncia oficial de phishing e fraude.

A VerdachtLink ajuda a avaliar o risco, mas não substitui uma
desconfiança saudável: em caso de dúvida, é sempre mais seguro não abrir
um link.
""",
        },
        "it": {
            "page_title": "Consigli di sicurezza",
            "title": "Consigli di sicurezza",
            "body": """
### Prima di cliccare su un link

- Controlla l'indirizzo web completo, non solo le prime lettere.
- Hai dei dubbi? Non cliccare sul link. Digita tu stesso l'indirizzo
  dell'organizzazione nel browser, oppure apri l'app ufficiale.
- Fai attenzione a una sensazione di urgenza ("azione immediata
  richiesta", "altrimenti il tuo account verrà bloccato"). È un trucco
  comune per farti pensare in modo meno critico.

### Con email e SMS

- Controlla l'indirizzo email completo del mittente, non solo il nome
  visualizzato.
- Un'organizzazione normalmente non chiede mai la tua password completa,
  il PIN o i dati della carta di credito via email o SMS.
- Un'ortografia scorretta o un saluto impersonale ("Gentile cliente")
  può essere un segnale, ma è sempre più assente nei messaggi di
  phishing realizzati professionalmente. Non fidarti ciecamente di
  questo.

### Precauzioni generali

- Usa l'autenticazione a due fattori per gli account importanti.
- Usa password uniche per ogni sito o servizio, ad esempio con un
  gestore di password.
- Mantieni app, browser e sistema operativo aggiornati.
- Esegui regolarmente il backup dei file importanti.

### Se hai comunque cliccato o inserito dati

- Cambia subito la password, e anche negli altri account se l'hai
  riutilizzata.
- In caso di possibile frode finanziaria, contatta subito la tua banca.
- Valuta di sporgere denuncia alla polizia.
- Segnala il messaggio all'organizzazione di cui il mittente si è
  finto, e, dove possibile, a un punto di segnalazione ufficiale per
  phishing e frodi.

VerdachtLink aiuta a valutare il rischio, ma non sostituisce una sana
diffidenza: in caso di dubbio, è sempre più sicuro non aprire un link.
""",
        },
    },
}
