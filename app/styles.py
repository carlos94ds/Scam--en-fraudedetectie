"""
Gedeelde styling voor alle ScamCheck-pagina's: lettertypen, formaat en
kleuren. inject_css() wordt op elke pagina aangeroepen zodat de look
overal hetzelfde is.
"""
import streamlit as st
import streamlit.components.v1 as components

# Tags die ScamCheck installeerbaar maken als PWA ("Toevoegen aan
# beginscherm" op Android/iOS). Streamlit geeft geen toegang tot de echte
# document-<head>, dus we zetten ze erin via een iframe-script dat
# window.parent.document gebruikt (Streamlit's components.html draait in
# hetzelfde origin als de app, zie de docstring van components.v1.html).
PWA_HEAD_JS = """
<script>
(function () {
  const head = window.parent.document.head;
  const tags = [
    {tag: "link", attrs: {rel: "manifest", href: "/app/static/manifest.json"}},
    {tag: "meta", attrs: {name: "theme-color", content: "#4F46E5"}},
    {tag: "link", attrs: {rel: "apple-touch-icon", href: "/app/static/apple-touch-icon.png"}},
    {tag: "meta", attrs: {name: "apple-mobile-web-app-capable", content: "yes"}},
    {tag: "meta", attrs: {name: "apple-mobile-web-app-status-bar-style", content: "default"}},
    {tag: "meta", attrs: {name: "apple-mobile-web-app-title", content: "ScamCheck"}},
    {tag: "meta", attrs: {name: "mobile-web-app-capable", content: "yes"}},
  ];
  tags.forEach(function (t) {
    const firstKey = Object.keys(t.attrs)[0];
    const selector = t.tag + '[' + firstKey + '="' + t.attrs[firstKey] + '"]';
    if (head.querySelector(selector)) return;
    const el = document.createElement(t.tag);
    Object.keys(t.attrs).forEach(function (k) { el.setAttribute(k, t.attrs[k]); });
    head.appendChild(el);
  });
})();
</script>
"""


def inject_pwa_tags():
    components.html(PWA_HEAD_JS, height=0, width=0)


GOOGLE_FONTS_LINK = (
    '<link href="https://fonts.googleapis.com/css2?'
    'family=Inter:wght@400;500;600;700;800&family=Manrope:wght@700;800'
    '&display=swap" rel="stylesheet">'
)

CSS = """
<style>
html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; font-size: 18px; }
.stApp { background: linear-gradient(180deg, #F7F8FD 0%, #FFFFFF 320px); }
.block-container { max-width: 1000px; padding-top: 2.5rem; }
h1 { font-family: 'Manrope', 'Inter', sans-serif !important; font-size: 3.2rem !important; font-weight: 800 !important; letter-spacing: -0.02em; background: linear-gradient(90deg, #4F46E5, #7C3AED); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem !important; }
.slogan { color: #1E1F2B; font-size: 1.35rem; font-weight: 600; margin-bottom: 0.4rem; }
.tagline { color: #5B5F73; font-size: 1.2rem; margin-bottom: 2rem; }
p, li, label { font-size: 1.1rem; }
.stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid #E4E6F1; }
.stTabs [data-baseweb="tab"] { height: 50px; border-radius: 8px 8px 0 0; font-weight: 600; font-size: 1.05rem; color: #5B5F73; }
.stTabs [aria-selected="true"] { color: #4F46E5 !important; background-color: #EEF0FC; }
.stButton>button { font-size: 1.05rem; padding: 0.7rem 2rem; border-radius: 10px; font-weight: 600; background: linear-gradient(90deg, #4F46E5, #6D28D9); color: white; border: none; box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25); transition: transform 0.15s ease, box-shadow 0.15s ease; }
.stButton>button:hover { transform: translateY(-1px); box-shadow: 0 6px 18px rgba(79, 70, 229, 0.35); color: white; }
.stTextArea textarea { font-size: 1.1rem; border-radius: 10px !important; border: 1.5px solid #E4E6F1 !important; }
.stTextArea textarea:focus { border-color: #4F46E5 !important; box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.12) !important; }
.result-card { border-radius: 12px; padding: 1.3rem 1.6rem; margin: 1rem 0; box-shadow: 0 2px 10px rgba(18, 20, 28, 0.06); border: 1px solid rgba(18, 20, 28, 0.04); position: relative; overflow: hidden; }
.result-card::before { content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 5px; background-color: var(--accent-color, #4F46E5); }
.result-label { font-size: 1.4rem; font-weight: 700; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.5rem; }
.method-badge { margin-left: auto; font-size: 0.8rem; font-weight: 600; color: #5B5F73; background-color: rgba(18, 20, 28, 0.05); border-radius: 999px; padding: 0.25rem 0.75rem; letter-spacing: 0.01em; }
.result-url { font-size: 0.95rem; color: #5B5F73; word-break: break-all; margin-bottom: 0.5rem; font-family: 'SFMono-Regular', Consolas, monospace; }
.tab-uitleg { color: #5B5F73; margin-bottom: 1rem; font-size: 1.05rem; }
[data-testid="stSidebar"] { background-color: #F7F8FD; border-right: 1px solid #E4E6F1; }
</style>
"""


def inject_css():
    st.markdown(GOOGLE_FONTS_LINK, unsafe_allow_html=True)
    st.markdown(CSS, unsafe_allow_html=True)
