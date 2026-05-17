"""IQLE Platform — clean sidebar nav, no HTML tricks"""
import streamlit as st

st.set_page_config(
    page_title="IQLE Platform | PT Pindad",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.database import init_database, get_setting
from utils.auth import create_default_admin, is_admin, logout
from utils.seed_data import seed_dummy_data
from utils.styles import apply_global_style, render_header, render_footer

@st.cache_resource
def _bootstrap():
    init_database(); create_default_admin(); seed_dummy_data()
    return True

try:
    _bootstrap()
except Exception as e:
    st.error(f"Database Error: {e}"); st.stop()

apply_global_style()

if not st.session_state.get("logged_in"):
    from modules.pg_login import show_login
    show_login(); st.stop()

user   = st.session_state.get("user", {})
role   = st.session_state.get("role", "viewer")
accent = get_setting("ui_accent_color", "#00d4ff")

if "page" not in st.session_state:
    st.session_state.page = "home"

PAGE_MODULES = {
    "home":"modules.pg_home","iso9001":"modules.pg_iso9001",
    "iatf":"modules.pg_iatf","lifecycle":"modules.pg_lifecycle",
    "consistency":"modules.pg_consistency","batch":"modules.pg_batch",
    "iqscore":"modules.pg_iqscore","maung":"modules.pg_maung",
    "whatif":"modules.pg_whatif","hipotesis":"modules.pg_hipotesis",
    "interview":"modules.pg_interview","about":"modules.pg_about",
    "theory":"modules.pg_theory","users":"modules.pg_users",
    "settings":"modules.pg_settings",
}

MENU = [
    ("home","Dashboard Utama","EVALUASI"),
    ("iso9001","ISO 9001","EVALUASI"),
    ("iatf","IATF 16949","EVALUASI"),
    ("lifecycle","Engineering Lifecycle","EVALUASI"),
    ("consistency","Konsistensi Mutu","EVALUASI"),
    ("batch","Evaluasi Batch","EVALUASI"),
    ("iqscore","Integrated Quality Score","ANALISIS"),
    ("maung","Analisis Mutu MAUNG MV3","ANALISIS"),
    ("whatif","Simulasi What-If","ANALISIS"),
    ("hipotesis","Kesimpulan & Hipotesis","ANALISIS"),
    ("interview","Data Wawancara","ANALISIS"),
    ("about","About Platform","PLATFORM"),
    ("theory","Teori & Referensi","PLATFORM"),
    ("users","Manajemen User","PLATFORM"),
    ("settings","Pengaturan Platform","PLATFORM"),
]

def go(pid):
    st.session_state.page = pid
    st.rerun()

# ── CSS: pastikan sidebar selalu kelihatan, full height ──────
st.markdown(f"""
<style>
/* Paksa sidebar kelihatan */
section[data-testid="stSidebar"] {{
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    min-width: 240px !important;
    max-width: 300px !important;
}}
section[data-testid="stSidebar"] > div:first-child {{
    background: #0d1321 !important;
    padding-top: 1rem !important;
}}
/* Sidebar collapse button tetap kelihatan */
[data-testid="stSidebarCollapsedControl"] {{
    display: flex !important;
    visibility: visible !important;
}}
/* Hilangkan default Streamlit header */
header[data-testid="stHeader"] {{ display:none !important; }}
/* Main area full width */
.stMainBlockContainer, .block-container {{
    max-width: 100% !important;
    padding-top: 1rem !important;
    padding-left: 1.5rem !important;
    padding-right: 1.5rem !important;
}}
/* Button sidebar: active = primary (cyan), inactive = ghost */
div[data-testid="stSidebar"] button[kind="primary"] {{
    background: linear-gradient(135deg, {accent}22, {accent}11) !important;
    border-left: 3px solid {accent} !important;
    color: {accent} !important;
    font-weight: 700 !important;
}}
div[data-testid="stSidebar"] button[kind="secondary"] {{
    background: transparent !important;
    border: none !important;
    border-left: 3px solid transparent !important;
    color: #7a9bb5 !important;
    text-align: left !important;
}}
div[data-testid="stSidebar"] button[kind="secondary"]:hover {{
    background: rgba(0,212,255,0.05) !important;
    border-left-color: rgba(0,212,255,0.3) !important;
    color: #c9d1d9 !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    _un  = user.get("full_name") or user.get("username","")
    _rc  = "#00d4ff" if role=="admin" else "#ffd700"
    _rl  = "ADMIN"   if role=="admin" else "VIEWER"

    st.markdown(f"""
    <div style="padding:.3rem .5rem .6rem;border-bottom:1px solid rgba(0,212,255,.12);
                margin-bottom:.5rem;">
      <div style="font-family:Rajdhani,sans-serif;font-size:1rem;font-weight:700;
                  color:{accent};letter-spacing:2px;">IQLE PLATFORM</div>
      <div style="font-size:.6rem;color:#3d5470;margin-top:1px;">PT Pindad (Persero)</div>
      <div style="margin-top:.4rem;display:flex;align-items:center;gap:.4rem;">
        <span style="font-size:.62rem;font-weight:600;color:#c9d1d9;">{_un}</span>
        <span style="font-size:.58rem;color:{_rc};border:1px solid {_rc}44;
                     border-radius:3px;padding:0 4px;font-family:Rajdhani;
                     font-weight:700;">{_rl}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    cur = st.session_state.page
    for grp in ("EVALUASI","ANALISIS","PLATFORM"):
        st.markdown(
            f"<div style='font-size:.6rem;color:#2a3f55;letter-spacing:1.5px;"
            f"padding:.4rem .1rem .15rem;font-family:Rajdhani;font-weight:700;"
            f"text-transform:uppercase;'>{grp}</div>",
            unsafe_allow_html=True,
        )
        for pid, label, g in MENU:
            if g != grp: continue
            if pid in ("users","settings") and not is_admin(): continue
            if st.button(label, key=f"sb_{pid}", use_container_width=True,
                         type="primary" if cur==pid else "secondary"):
                go(pid)

    st.markdown("---")
    if st.button("⏻  Logout", key="sb_logout", use_container_width=True):
        logout()

# ── Header ───────────────────────────────────────────────────
render_header()

# ── Page loader ──────────────────────────────────────────────
import importlib
cur = st.session_state.page
try:
    mod = importlib.import_module(PAGE_MODULES.get(cur,"modules.pg_home"))
    mod.show()
except Exception as e:
    st.error(f"Error: {e}")
    import traceback; st.code(traceback.format_exc())

# ── Footer as quick nav ──────────────────────────────────────
render_footer()
