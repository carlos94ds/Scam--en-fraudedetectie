# Scam & Fraud Detection Platform

Data Science & AI portfolio-project: een webapplicatie waarmee gebruikers een URL
kunnen invoeren en een begrijpelijke risico-inschatting krijgen (laag / mogelijk /
hoog risico) op basis van kenmerken die vaak voorkomen bij phishing.

Dit is een leerproject, ontwikkeld als onderdeel van de HBO-ICT-opleiding
(Applied Data Science & AI) bij Windesheim.

## Status
Project in opbouw. Zie `docs/` voor het projectverslag.

## Structuur
- `data/` — datasets (niet in git, zie .gitignore)
- `notebooks/` — Jupyter notebooks voor EDA en experimenten
- `src/` — herbruikbare Python-code (preprocessing, features, model)
- `models/` — getrainde modellen
- `app/` — de webapplicatie (Streamlit)
- `tests/` — tests
- `docs/` — projectdocumentatie

## Draaien

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Deployment

De app draait live op Streamlit Community Cloud — zie
[`docs/deployment.md`](docs/deployment.md) voor hoe dat is opgezet en hoe
je 'm bijwerkt.
