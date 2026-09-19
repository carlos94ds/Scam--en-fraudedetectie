import os
import streamlit as st

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

st.set_page_config(page_title="Over VerdachtLink", page_icon=LOGO_PATH, layout="centered")

st.title("Over VerdachtLink")

st.markdown("""
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

- De opgegeven website wordt niet bezocht. Er wordt alleen naar de tekst
  van de link gekeken.
- Bij e-mail, sms en social media wordt alleen de link in het bericht
  beoordeeld, niet de afzender of de rest van de inhoud.
- De inschatting is geen garantie. Een link met een lage risico-score kan
  in zeldzame gevallen alsnog onveilig zijn, en andersom.

### Achtergrond

Dit project is ontwikkeld als onderwijs- en portfolioproject binnen de
opleiding HBO-ICT, richting Data Science & Artificial Intelligence, gericht
op het toegankelijker maken van fraude- en phishingherkenning voor mensen
zonder technische achtergrond.
""")
