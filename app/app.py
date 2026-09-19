"""
VerdachtLink - hoofdpagina: gebruiker plakt een link, e-mail, sms of
social-media-bericht, het systeem haalt de link(en) eruit en geeft per link
een begrijpelijke risico-inschatting. Analyseert alleen de tekst van de
link, bezoekt de website zelf niet. De logica staat in app/logic.py.
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(os.path.dirname(__file__))

import streamlit as st

from src.feature_extraction import extract_urls_from_text
from logic import load_resources, analyse_url

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 16px;
    }
    .stApp {
        background: linear-gradient(180deg, #F7F8FD 0%, #FFFFFF 320px);
    }
    h1 {
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
        background: linear-gradient(90deg, #4F46E5, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem !important;
    }
    .tagline { color: #5B5F73; font-size: 1.05rem; margin-bottom: 1.75rem; }
    p, li, label { font-size: 1rem; }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid #E4E6F1;
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 8px 8px 0 0;
        font-weight: 600;
        color: #5B5F73;
    }
    .stTabs [aria-selected="true"] {
        color: #4F46E5 !important;
        background-color: #EEF0FC;
    }

    .stButton>button {
        font-size: 0.95rem;
        padding: 0.6rem 1.8rem;
        border-radius: 10px;
        font-weight: 600;
        background: linear-gradient(90deg, #4F46E5, #6D28D9);
        color: white;
        border: none;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .stButton>button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(79, 70, 229, 0.35);
        color: white;
    }

    .stTextArea textarea {
        font-size: 1rem;
        border-radius: 10px !important;
        border: 1.5px solid #E4E6F1 !important;
    }
    .stTextArea textarea:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important;
    }

    .result-card {
        border-radius: 12px;
        padding: 1.1rem 1.4rem;
        margin: 0.9rem 0;
        box-shadow: 0 2px 10px rgba(18, 20, 28, 0.06);
        border: 1px solid rgba(18, 20, 28, 0.04);
        position: relative;
        overflow: hidden;
    }
    .result-card::before {
        content: "";
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 5px;
        background-color: var(--accent-color, #4F46E5);
    }
    .result-label {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .result-url {
        font-size: 0.88rem;
        color: #5B5F73;
        word-break: break-all;
        margin-bottom: 0.5rem;
        font-family: 'SFMono-Regular', Consolas, monospace;
    }
    .tab-uitleg { color: #5B5F73; margin-bottom: 0.9rem; }

    [data-testid="stSidebar"] {
        background-color: #F7F8FD;
        border-right: 1px solid #E4E6F1;
    }
    </style>
    """, unsafe_allow_html=True)


def render_result(url, risk, reasons):
    style = RISK_STYLES[risk]
    st.markdown(f"""
    <div class="result-card" style="--accent-color:{style['border']}; background-color:{style['bg']};">
        <div class="result-label" style="color:{style['color']};">
            <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background-color:{style['border']};"></span>
            {style['label']}
        </div>
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
    st.set_page_config(page_title="VerdachtLink", page_icon=LOGO_PATH, layout="centered")
    inject_css()

    col_logo, col_title = st.columns([1, 6])
    with col_logo:
        st.image(LOGO_PATH, width=64)
    with col_title:
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

    st.sidebar.image(LOGO_PATH, width=56)
    st.sidebar.markdown("### VerdachtLink")
    st.sidebar.caption(
        "Gebruik het menu hierboven om meer te lezen over deze app, "
        "veelvoorkomende soorten fraude en algemene veiligheidstips."
    )


if __name__ == "__main__":
    main()
