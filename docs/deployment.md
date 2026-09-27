# Deployment

De app kan op twee plekken gehost worden: Streamlit Community Cloud (huidige
hosting) of Railway. Beide draaien dezelfde code zonder aanpassingen nodig.

## Optie A: Streamlit Community Cloud

Deze app wordt gehost op [Streamlit Community Cloud](https://share.streamlit.io),
gratis hosting voor Streamlit-apps die rechtstreeks vanaf een GitHub-repo
draait. Streamlit Cloud kloont alleen deze repository en heeft geen toegang
tot lokale bestanden of de dataset — daarom staan de getrainde modellen
(`models/*.pkl`, `models/*.json`) bewust wél in git, in tegenstelling tot
`data/` (zie `.gitignore`).

## Eenmalig: modellen committen

De modelbestanden worden lokaal gegenereerd (met de dataset die je zelf
hebt) en horen dus niet automatisch in de repo totdat je ze zelf toevoegt:

```bash
python -m src.train_production_model      # produceert models/production_*.{pkl,json}
python -m src.train_url_website_model     # produceert models/url_website_*.{pkl,json}  (optioneel, voor de website-analyse)

git add models/*.pkl models/*.json .gitignore docs/deployment.md
git commit -m "Voeg getrainde modellen toe voor deployment op Streamlit Cloud"
git push
```

Herhaal de `train_...`-stap en commit opnieuw wanneer je het model
verbetert of opnieuw traint — de modellen in git zijn een snapshot, geen
live gegenereerd resultaat.

## App aanmaken op Streamlit Cloud

1. Ga naar <https://share.streamlit.io> en log in met je GitHub-account
   (`carlos94ds`).
2. Klik op **New app**.
3. Kies:
   - **Repository**: `carlos94ds/Scam--en-fraudedetectie`
   - **Branch**: `main`
   - **Main file path**: `app/app.py`
4. Klik op **Deploy**. De eerste build duurt een paar minuten (installeert
   `requirements.txt`).
5. Zodra de build klaar is, krijg je een publieke URL
   (`https://<naam>.streamlit.app`) die je kunt delen, bijvoorbeeld voor je
   portfolio of beoordeling.

Geen secrets/API-keys nodig — de app gebruikt alleen de meegecommitte
modelbestanden en, optioneel, live requests naar de door de gebruiker
opgegeven website (zie `src/website_features.py`).

## Bijwerken

Elke push naar de `main`-branch (die de modelbestanden en code bevat)
wordt automatisch opnieuw gedeployed door Streamlit Cloud — geen aparte
deploy-stap nodig na de eerste keer.

## Bekende beperking

Als je de website-analyse (Model B) hebt getraind maar de bijbehorende
bestanden niet hebt gecommit (of andersom), valt de app automatisch terug
op URL-only-analyse — zie `website_resources_available()` in
`app/logic.py`. Er gaat dus niets stuk als een van de twee modellen
ontbreekt, de bijbehorende functionaliteit is dan alleen niet zichtbaar.

## Optie B: Railway

[Railway](https://railway.app) draait de app vanuit dezelfde repo, maar als
een "gewone" webserver op een zelfgekozen poort in plaats van Streamlit's
eigen platform. Het `Procfile` in de root van de repo regelt het
opstartcommando; Railway (via Nixpacks) herkent Python automatisch aan
`requirements.txt`.

1. Ga naar <https://railway.app>, log in met GitHub en klik **New Project
   → Deploy from GitHub repo**.
2. Kies deze repository (`main`-branch).
3. Railway detecteert `requirements.txt` en `Procfile` automatisch — geen
   extra configuratie nodig. De `$PORT`-omgevingsvariabele wordt door
   Railway zelf gezet; het `Procfile` gebruikt die al
   (`--server.port=$PORT --server.address=0.0.0.0`).
4. Na de build krijg je een publieke `*.up.railway.app`-URL (onder
   **Settings → Networking → Generate Domain**).

Net als bij Streamlit Cloud zijn er geen secrets nodig — alleen de
meegecommitte modelbestanden in `models/`.

### Installeren als app op de telefoon (PWA)

De app is een Progressive Web App: eenmaal live (op Railway of Streamlit
Cloud) kunnen bezoekers 'm op hun startscherm zetten zonder App
Store/Play Store.

- **Android (Chrome)**: menu (⋮) → **App installeren** / **Toevoegen aan
  startscherm**.
- **iPhone (Safari)**: deelknop (□↑) → **Zet op beginscherm**.

Dit werkt via `app/static/manifest.json` en de iconen in `app/static/`
(`enableStaticServing = true` in `.streamlit/config.toml`), die via een
klein script in `app/styles.py` (`inject_pwa_tags()`) in de paginakop
gezet worden — Streamlit ondersteunt dit niet standaard. Belangrijk: dit
werkt alléén via de publieke `https://`-URL na deployment, niet via
`localhost`.
