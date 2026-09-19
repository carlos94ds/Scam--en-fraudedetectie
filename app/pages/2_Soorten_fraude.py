import os
import streamlit as st

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

st.set_page_config(page_title="Soorten fraude", page_icon=LOGO_PATH, layout="centered")

st.title("Veelvoorkomende soorten fraude en scams")

st.markdown("""
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
""")
