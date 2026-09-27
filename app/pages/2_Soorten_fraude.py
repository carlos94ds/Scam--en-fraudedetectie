import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st

from i18n import PAGES_TEXT, sidebar_language_selector
from styles import inject_css, inject_pwa_tags

st.set_page_config(page_title="ScamCheck", page_icon="🔎", layout="wide")
inject_css()
inject_pwa_tags()

lang = sidebar_language_selector()
text = PAGES_TEXT["fraude"][lang]

st.title(text["title"])
st.markdown(text["body"])
