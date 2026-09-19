"""
Webapplicatie: gebruiker plakt een link of een bericht (e-mail/sms), het
systeem haalt de link(en) eruit en geeft per link een begrijpelijke
risico-inschatting. Analyseert alleen de tekst van de link, bezoekt de
website zelf niet.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import json
import joblib
import streamlit as st

from src.feature_extraction import extract_full_features, extract_urls_from_text
from src.train_production_model import FEATURE_ORDER

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

FEATURE_EXPLANATIONS = {
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
}

RISK_STYLES = {
    "laag": {"color": "#1E7D32", "bg": "#F0F7F1", "border": "#1E7D32", "label": "Laag risico"},
    "mogelijk": {"color": "#9A5B00", "bg": "#FBF4EA", "border": "#9A5B00", "label": "Mogelijk risico"},
    "hoog": {"color": "#B3261E", "bg": "#FBEEED", "border": "#B3261E", "label": "Hoog risico"},
}


@st.cache_resource
def load_resources():
    model = joblib.load(os.path.join(MODEL_DIR, "production_model.pkl"))
    scaler = joblib.load(os.path.join(MODEL_DIR, "production_scaler.pkl"))
    with open(os.path.join(MODEL_DIR, "tld_probability_table.json")) as f:
        tld_data = json.load(f)
    with open(os.path.join(MODEL_DIR, "char_frequency_table.json")) as f:
        char_data = json.load(f)
    return model, scaler, tld_data, char_data


def classify_risk(p_phishing: float) -> str:
    if p_phishing < 0.2:
        return "laag"
    if p_phishing < 0.6:
        return "mogelijk"
    return "hoog"


def explain(model, feature_values_scaled, feature_names, top_n=3):
    contributions = model.coef_[0] * feature_values_scaled
    order = sorted(range(len(feature_names)), key=lambda i: abs(contributions[i]), reverse=True)
    reasons = []
    for i in order[:top_n]:
        name = feature_names[i]
        pushes_to_phishing = contributions[i] < 0
        pair = FEATURE_EXPLANATIONS.get(name)
        if pair:
            reasons.append(pair[0] if pushes_to_phishing else pair[1])
    return reasons


def inject_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 16px; }
    h1 { font-size: 1.9rem !important; font-weight: 700; }
    p, li, label { font-size: 1rem; }
    .stButton>button {
        font-size: 1rem;
        padding: 0.6rem 1.6rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .stTextArea textarea {
        font-size: 1rem;
    }
    .result-card {
        border-left: 5px solid;
        border-radius: 6px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
    }
    .result-label {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .result-url {
        font-size: 0.9rem;
        color: #555555;
        word-break: break-all;
        margin-bottom: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


def analyse_url(url, model, scaler, tld_data, char_data):
    features = extract_full_features(
        url,
        tld_prob_table=tld_data["table"],
        char_freq_table=char_data["table"],
        default_tld_prob=tld_data["default"],
        default_char_prob=char_data["default"],
    )
    X = [[features[name] for name in FEATURE_ORDER]]
    X_scaled = scaler.transform(X)
    proba = model.predict_proba(X_scaled)[0]
    p_phishing = proba[0]
    risk = classify_risk(p_phishing)
    reasons = explain(model, X_scaled[0], FEATURE_ORDER)
    return risk, reasons


def render_result(url, risk, reasons):
    style = RISK_STYLES[risk]
    st.markdown(f"""
    <div class="result-card" style="border-color:{style['border']}; background-color:{style['bg']};">
        <div class="result-label" style="color:{style['color']};">{style['label']}</div>
        <div class="result-url">{url}</div>
    </div>
    """, unsafe_allow_html=True)

    if reasons:
        st.markdown("**Waarom deze inschatting:**")
        for reason in reasons:
            st.markdown(f"- {reason}")


def main():
    st.set_page_config(page_title="Linkchecker", page_icon=":mag:", layout="centered")
    inject_css()

    st.title("Linkchecker")
    st.write(
        "Twijfel je over een link uit een e-mail, sms of ander bericht? "
        "Plak de link, of het hele bericht, hieronder."
    )

    text = st.text_area(
        "Link of bericht",
        placeholder="Plak hier een link, of een e-mail-/sms-bericht met daarin een link.",
        height=120,
        label_visibility="collapsed",
    )

    if st.button("Controleer"):
        if not text.strip():
            st.warning("Vul eerst een link of bericht in.")
            return

        urls = extract_urls_from_text(text)
        if not urls:
            st.warning("Er is geen link gevonden in de tekst. Controleer of de link volledig is geplakt.")
            return

        model, scaler, tld_data, char_data = load_resources()

        for url in urls:
            risk, reasons = analyse_url(url, model, scaler, tld_data, char_data)
            render_result(url, risk, reasons)

        with st.expander("Meer over deze inschatting"):
            st.caption(
                "Dit is een inschatting op basis van kenmerken van de link zelf, geen garantie. "
                "De website wordt niet bezocht; alleen de tekst van de link wordt beoordeeld. "
                "Voer nooit wachtwoorden, pincodes of andere gevoelige gegevens in op een "
                "website waarover je twijfelt, en open een link bij twijfel liever niet — "
                "controleer in plaats daarvan via een officiële app of website."
            )


if __name__ == "__main__":
    main()
