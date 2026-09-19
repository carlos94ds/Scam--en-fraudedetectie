# Deployment (Streamlit Community Cloud)

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
