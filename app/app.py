"""
Webapplicatie: gebruiker plakt een link of een bericht (e-mail/sms), het
systeem haalt de link(en) eruit en geeft per link een begrijpelijke
risico-inschatting. Analyseert alleen de tekst van de link, bezoekt de
website zelf niet. De logica zelf staat in app/logic.py (apart testbaar).
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from src.feature_extraction import extract_urls_from_text
from app.logic import load_resources, analyse_url

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

RISK_STYLES = {
    "laag": {"color": "#1E7D32", "bg": "#F0F7F1", "border": "#1E7D32", "label": "Laag risico"},
    "mogelijk": {"color": "#9A5B00", "bg": "#FBF4EA", "border": "#9A5B00", "label": "Mogelijk risico"},
    "hoog": {"color": "#B3261E", "bg": "#FBEEED", "border": "#B3261E", "label": "Hoog risico"},
}


@st.cache_resource
def cached_resources():
    return load_resources(MODEL_DIR)


def inject_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 16px; }
    h1 { font-size: 1.9rem !important; font-weight: 700; }
    p, li, label { font-size: 1rem; }
    .stButton>button { font-size: 1rem; padding: 0.6rem 1.6rem; border-radius: 8px; font-weight: 600; }
    .stTextArea textarea { font-size: 1rem; }
    .result-card { border-left: 5px solid; border-radius: 6px; padding: 1rem 1.25rem; margin: 0.75rem 0; }
    .result-label { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.25rem; }
    .result-url { font-size: 0.9rem; color: #555555; word-break: break-all; margin-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)


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
    st.write("Twijfel je over een link uit een e-mail, sms of ander bericht? Plak de link, of het hele bericht, hieronder.")

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

        model, scaler, tld_data, char_data = cached_resources()

        for url in urls:
            risk, reasons, _ = analyse_url(url, model, scaler, tld_data, char_data)
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
