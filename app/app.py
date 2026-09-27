"""
ScamCheck - hoofdpagina: gebruiker plakt een link, e-mail, sms of
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
from src.website_features import WebsiteFetchError
from logic import (
    load_resources,
    analyse_url,
    analyse_url_and_website,
    website_resources_available,
    load_website_resources,
)
from i18n import LANGUAGES, UI_TEXT
from styles import inject_css, inject_pwa_tags

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")

RISK_STYLES = {
    "laag": {"color": "#1E7D32", "bg": "#F0F7F1", "border": "#1E7D32"},
    "mogelijk": {"color": "#9A5B00", "bg": "#FBF4EA", "border": "#9A5B00"},
    "hoog": {"color": "#B3261E", "bg": "#FBEEED", "border": "#B3261E"},
}

TAB_KEYS = ["link", "email", "sms", "social"]


@st.cache_resource
def cached_resources():
    return load_resources(MODEL_DIR)


@st.cache_resource
def cached_website_resources():
    return load_website_resources(MODEL_DIR)


def render_result(url, risk, reasons, text, used_website=False):
    style = RISK_STYLES[risk]
    label = text["risk_labels"][risk]
    method_label = text["method_badge_url_website"] if used_website else text["method_badge_url_only"]
    st.markdown(f"""
    <div class="result-card" style="--accent-color:{style['border']}; background-color:{style['bg']};">
        <div class="result-label" style="color:{style['color']};">
            <span style="display:inline-block; width:10px; height:10px; border-radius:50%; background-color:{style['border']};"></span>
            {label}
            <span class="method-badge">{method_label}</span>
        </div>
        <div class="result-url">{url}</div>
    </div>
    """, unsafe_allow_html=True)
    if reasons:
        st.markdown(text["why_label"])
        for reason in reasons:
            st.markdown(f"- {reason}")


def render_checker_tab(tab_config, tab_key, lang, text):
    st.markdown(f'<div class="tab-uitleg">{tab_config["uitleg"]}</div>', unsafe_allow_html=True)

    input_text = st.text_area(
        f"invoer-{tab_key}",
        placeholder=tab_config["placeholder"],
        height=110,
        label_visibility="collapsed",
        key=f"input-{tab_key}",
    )

    visit_website = False
    if website_resources_available(MODEL_DIR):
        visit_website = st.checkbox(
            text["website_checkbox_label"],
            help=text["website_checkbox_help"],
            key=f"visit-website-{tab_key}",
        )

    if st.button(text["button"], key=f"button-{tab_key}"):
        if not input_text.strip():
            st.warning(text["warning_empty"])
            return

        urls = extract_urls_from_text(input_text)
        if not urls:
            st.warning(text["warning_no_url"])
            return

        model, scaler, tld_data, char_data = cached_resources()

        for url in urls:
            if visit_website:
                try:
                    model_b, scaler_b, feature_columns_b, vocab = cached_website_resources()
                    risk, reasons, _ = analyse_url_and_website(
                        url, model_b, scaler_b, feature_columns_b, vocab,
                        tld_data, char_data, lang=lang,
                    )
                    render_result(url, risk, reasons, text, used_website=True)
                    continue
                except WebsiteFetchError:
                    st.warning(text["website_fetch_error"])

            risk, reasons, _ = analyse_url(url, model, scaler, tld_data, char_data, lang=lang)
            render_result(url, risk, reasons, text, used_website=False)


def main():
    st.set_page_config(page_title="ScamCheck", page_icon="🔎", layout="wide")
    inject_css()
    inject_pwa_tags()

    if "lang" not in st.session_state:
        st.session_state["lang"] = "nl"

    col_title, col_lang = st.columns([5, 2])
    with col_title:
        st.title("ScamCheck")
    with col_lang:
        lang_codes = list(LANGUAGES.keys())
        selected = st.selectbox(
            UI_TEXT[st.session_state["lang"]]["lang_label"],
            options=lang_codes,
            format_func=lambda code: LANGUAGES[code],
            index=lang_codes.index(st.session_state["lang"]),
            key="lang_select",
        )
        st.session_state["lang"] = selected

    lang = st.session_state["lang"]
    text = UI_TEXT[lang]

    st.markdown(
        f'<div class="slogan">{text["slogan"]}</div>'
        f'<div class="tagline">{text["tagline"]}</div>',
        unsafe_allow_html=True,
    )

    tabs = st.tabs([tab["titel"] for tab in text["tabs"]])
    for tab, tab_key, tab_config in zip(tabs, TAB_KEYS, text["tabs"]):
        with tab:
            render_checker_tab(tab_config, tab_key, lang, text)

    with st.expander(text["expander_title"]):
        st.caption(text["expander_text"])

    st.sidebar.markdown("### ScamCheck")
    st.sidebar.caption(text["sidebar_caption"])


if __name__ == "__main__":
    main()
