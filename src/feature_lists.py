"""
Centrale plek waar we vastleggen welke kolommen bij welke fase horen.

We gebruiken deze lijsten zowel in de EDA als later bij het trainen van het
model, zodat we niet op meerdere plekken los dezelfde kolomnamen typen.
"""

LABEL_COLUMN = "label"
# label = 1 -> legitiem, label = 0 -> phishing (zo staat het gedefinieerd door
# de makers van de PhiUSIIL-dataset)

ID_COLUMNS = ["URL", "Domain"]  # identificatie, geen features om op te trainen

# URLSimilarityIndex is bewust uitgesloten: zie docs/data-decisions.md
# (datalekkage — de kolom herhaalt in de praktijk het label).

# Kenmerken die je puur uit de URL-tekst zelf kan afleiden, zonder de website
# te hoeven bezoeken. Dit is de scope van onze MVP.
URL_ONLY_FEATURES = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "TLD",
    "TLDLength",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS",
    "CharContinuationRate",
    "URLCharProb",
    "TLDLegitimateProb",
]

# Kenmerken die alleen te bepalen zijn door de website te bezoeken en de HTML
# te analyseren. Dit voegen we pas toe in fase 2 (de "website"-uitbreiding).
WEBSITE_FEATURES = [
    "LineOfCode",
    "LargestLineLength",
    "HasTitle",
    "Title",
    "DomainTitleMatchScore",
    "URLTitleMatchScore",
    "HasFavicon",
    "Robots",
    "IsResponsive",
    "NoOfURLRedirect",
    "NoOfSelfRedirect",
    "HasDescription",
    "NoOfPopup",
    "NoOfiFrame",
    "HasExternalFormSubmit",
    "HasSocialNet",
    "HasSubmitButton",
    "HasHiddenFields",
    "HasPasswordField",
    "Bank",
    "Pay",
    "Crypto",
    "HasCopyrightInfo",
    "NoOfImage",
    "NoOfCSS",
    "NoOfJS",
    "NoOfSelfRef",
    "NoOfEmptyRef",
    "NoOfExternalRef",
]
