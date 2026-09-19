import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from i18n import PAGES_TEXT, sidebar_language_selector

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.png")

st.set_page_config(page_title="VerdachtLink", page_icon=LOGO_PATH, layout="centered")

lang = sidebar_language_selector()
text = PAGES_TEXT["over"][lang]

st.title(text["title"])
st.markdown(text["body"])
