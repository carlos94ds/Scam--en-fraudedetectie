"""
Webapplicatie: gebruiker plakt een URL, het systeem geeft een begrijpelijke
risico-inschatting. Analyseert alleen de tekst van de link, bezoekt de
website zelf niet.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import json
import joblib
import streamlit as st

from src.feature_extraction import extract_full_features
from src.train_production_model import FEATURE_ORDER

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

# --- Uitleg per kenmerk, in gewone taal. Elke tuple is (tekst als het risico
# verhoogt, tekst als het risico juist verlaagt). ---
FEATURE_EXPLANATIONS = {
    "URLLength": ("Deze link is ongewoon lang.", "Deze link heeft een gewone lengte."),
    "DomainLength": ("De domeinnaam is ongewoon lang.", "De domeinnaam heeft een gewone lengte."),
    "IsDomainIP": ("De link gebruikt een kaal IP-adres in plaats van een domeinnaam.", "De link gebruikt een normale domeinnaam."),
    "TLDLength": ("Het laatste stukje van het domein (bijv. \".com\") is ongewoon lang.", "Het laatste stukje van het domein heeft een gewone lengte."),
    "NoOfSubDomain": ("De link heeft veel onderdelen voor de domeinnaam.", "De link heeft een eenvoudige domeinopbouw."),
    "HasObfuscation": ("De link bevat vreemde gecodeerde tekens.", "De link bevat geen vreemde gecodeerde tekens."),
    "NoOfObfuscatedChar": ("De link bevat meerdere vreemde gecodeerde tekens.", "De link bevat geen vreemde gecodeerde tekens."),
    "ObfuscationRatio": ("Een groot deel van de link bestaat uit gecodeerde tekens.", "De link bevat nauwelijks gecodeerde tekens."),
    "NoOfLettersInURL": ("De link bevat weinig gewone letters.", "De link bevat vooral gewone letters."),
    "LetterRatioInURL": ("De link bestaat voor een klein deel uit letters.", "De link bestaat grotendeels uit letters."),
    "NoOfDegitsInURL": ("De link bevat ongewoon veel cijfers.", "De link bevat weinig cijfers."),
    "DegitRatioInURL": ("Een groot deel van de link bestaat uit cijfers.", "De link bevat weinig cijfers."),
    "NoOfEqualsInURL": ("De link bevat veel is-gelijk-tekens (=).", "De link bevat weinig is-gelijk-tekens."),
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
    "laag": {"color": "#1E7D32", "bg": "#E8F5E9", "emoji": "🟢", "label": "Laag risico"},
    "mogelijk": {"color": "#B45300", "bg": "#FFF3E0", "emoji": "🟠", "label": "Mogelijk risico"},
    "hoog": {"color": "#C62828", "bg": "#FDECEA", "emoji": "🔴", "label": "Hoog risico"},
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
    """Geeft de top-N kenmerken die het meest bijdroegen aan deze specifieke
    voorspelling (coëfficiënt x waarde van dat kenmerk voor deze URL)."""
    contributions = model.coef_[0] * feature_values_scaled
    order = sorted(range(len(feature_names)), key=lambda i: abs(contributions[i]), reverse=True)

    reasons = []
    for i in order[:top_n]:
        name = feature_names[i]
        pushes_to_phishing = contributions[i] < 0  # label 1 = legitiem, dus negatief duwt naar phishing
        explanation_pair = FEATURE_EXPLANATIONS.get(name)
        if explanation_pair is None:
            continue
        reasons.append(explanation_pair[0] if pushes_to_phishing else explanation_pair[1])
    return reasons


def inject_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 18px; }
    h1 { font-size: 2.4rem !important; }
    .stButton>button {
        font-size: 1.2rem;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
    }
    .stTextInput input {
        font-size: 1.2rem;
        padding: 0.75rem;
    }
    </style>
    """, unsafe_allow_html=True)


def main():
    st.set_page_config(page_title="Linkchecker", page_icon="🔍", layout="centered")
    inject_css()

    st.title("🔍 Linkchecker")
    st.write(
        "Twijfel je over een link uit een e-mail, sms of bericht? "
        "Plak 'm hieronder. Je hoeft niets te begrijpen van techniek — "
        "wij leggen het resultaat in gewone taal uit."
    )

    url = st.text_input("Plak hier de link (URL):", placeholder="bijvoorbeeld: voorbeeld-bezorgdienst.nl/pakket")

    if st.button("Controleer deze link"):
        if not url.strip():
            st.warning("Vul eerst een link in.")
            return

        model, scaler, tld_data, char_data = load_resources()

        features = extract_full_features(
            url,
            tld_prob_table=tld_data["table"],
            char_freq_table=char_data["table"],
            default_tld_prob=tld_data["default"],
            default_char_prob=char_data["default"],
        )
        X = [[features[name] for name in FEATURE_ORDER]]
        X_scaled = scaler.transform(X)

        # model.classes_ is [0, 1] -> index 0 = phishing, index 1 = legitiem
        proba = model.predict_proba(X_scaled)[0]
        p_phishing = proba[0]

        risk = classify_risk(p_phishing)
        style = RISK_STYLES[risk]

        st.markdown(f"""
        <div style="background-color:{style['bg']}; border-radius:14px; padding:1.5rem; margin-top:1rem;">
            <div style="font-size:2rem; font-weight:700; color:{style['color']};">
                {style['emoji']} {style['label']}
            </div>
        </div>
        """, unsafe_allow_html=True)

        reasons = explain(model, X_scaled[0], FEATURE_ORDER)
        if reasons:
            st.markdown("**Waarom deze inschatting:**")
            for reason in reasons:
                st.markdown(f"- {reason}")

        st.info(
            "Dit is een inschatting op basis van kenmerken van de link zelf, "
            "geen garantie. De website wordt niet bezocht; alleen de tekst "
            "van de link wordt bekeken. Twijfel je nog steeds? Open de link "
            "dan niet en controleer via een officiële app of website."
        )
        st.warning(
            "Voer nooit wachtwoorden, pincodes of andere gevoelige gegevens "
            "in op een website waar je over twijfelt."
        )


if __name__ == "__main__":
    main()
