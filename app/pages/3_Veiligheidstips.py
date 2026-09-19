import streamlit as st

st.set_page_config(page_title="Veiligheidstips", page_icon=":lock:", layout="centered")

st.title("Veiligheidstips")

st.markdown("""
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
""")
