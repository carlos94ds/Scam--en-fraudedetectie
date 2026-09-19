"""
VerdachtLink - hoofdpagina: gebruiker plakt een link, e-mail, sms of
social-media-bericht, het systeem haalt de link(en) eruit en geeft per link
een begrijpelijke risico-inschatting. Analyseert alleen de tekst van de
link, bezoekt de website zelf niet. De logica staat in app/logic.py.
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

TAB_CONFIG = [
    {
        "titel": "Link",
        "uitleg": "Plak een kale link, bijvoorbeeld uit je browser of een bericht.",
        "placeholder": "https://voorbeeld.nl/pagina",
        "key": "link",
    },
    {
        "titel": "E-mail",
        "uitleg": "Plak de tekst van een verdachte e-mail. We halen de link(en) eruit en beoordelen die; de afzender en de rest van de tekst worden niet meegewogen.",
        "placeholder": "Bijvoorbeeld: \"Uw account wordt geblokkeerd. Log direct in via ...\"",
        "key": "email",
    },
    {
        "titel": "Sms",
        "uitleg": "Plak de tekst van een verdacht sms-bericht. We halen de link(en) eruit en beoordelen die.",
        "placeholder": "Bijvoorbeeld: \"Uw pakket kon niet worden bezorgd. Bevestig via ...\"",
        "key": "sms",
    },
    {
        "titel": "Social media",
        "uitleg": "Plak een bericht of link van Instagram, Facebook, WhatsApp of een ander platform.",
        "placeholder": "Bijvoorbeeld een link uit een DM of een reactie onder een post.",
        "key": "social",
    },
]


@st.cache_resource
def cached_resources():
    return load_resources(MODEL_DIR)


def inject_css():
    st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 16px; }
    h1 { font-size: 2rem !important; font-weight: 700; margin-bottom: 0.1rem; }
    .tagline { color: #555555; font-size: 1.05rem; margin-bottom: 1.5rem; }
    p, li, label { font-size: 1rem; }
    .stButton>button { font-size: 1rem; padding: 0.6rem 1.6rem; border-radius: 8px; font-weight: 600; }
    .stTextArea textarea { font-size: 1rem; }
    .result-card { border-left: 5px solid; border-radius: 6px; padding: 1rem 1.25rem; margin: 0.75rem 0; }
    .result-label { font-size: 1.3rem; font-weight: 700; margin-bottom: 0.25rem; }
    .result-url { font-size: 0.9rem; color: #555555; word-break: break-all; margin-bottom: 0.5rem; }
    .tab-uitleg { color: #444444; margin-bottom: 0.75rem; }
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


def render_checker_tab(config):
    st.markdown(f'<div class="tab-uitleg">{config["uitleg"]}</div>', unsafe_allow_html=True)

    text = st.text_area(
        f"invoer-{config['key']}",
        placeholder=config["placeholder"],
        height=110,
        label_visibility="collapsed",
        key=f"input-{config['key']}",
    )

    if st.button("Controleer", key=f"button-{config['key']}"):
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


def main():
    st.set_page_config(page_title="VerdachtLink", page_icon=":shield:", layout="centered")
    inject_css()

    st.title("VerdachtLink")
    st.markdown(
        '<div class="tagline">Controleer snel of een link, e-mail, sms of social-mediabericht mogelijk onveilig is.</div>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs([c["titel"] for c in TAB_CONFIG])
    for tab, config in zip(tabs, TAB_CONFIG):
        with tab:
            render_checker_tab(config)

    with st.expander("Meer over deze inschatting"):
        st.caption(
            "Dit is een inschatting op basis van kenmerken van de link zelf, geen garantie. "
            "De website wordt niet bezocht; alleen de tekst van de link wordt beoordeeld. "
            "Voer nooit wachtwoorden, pincodes of andere gevoelige gegevens in op een "
            "website waarover je twijfelt, en open een link bij twijfel liever niet — "
            "controleer in plaats daarvan via een officiële app of website."
        )

    st.sidebar.markdown("### VerdachtLink")
    st.sidebar.caption(
        "Gebruik het menu hierboven om meer te lezen over deze app, "
        "veelvoorkomende soorten fraude en algemene veiligheidstips."
    )


if __name__ == "__main__":
    main()
