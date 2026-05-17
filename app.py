"""
IQLE Platform — app.py
Navigation: sidebar only, st.session_state router
No HTML navbar, no hidden buttons, no JS hacks
"""
import streamlit as st

st.set_page_config(
    page_title="IQLE Platform | PT Pindad",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── DB + Auth init (runs once per session) ──────────────────
from utils.database import init_database, get_setting
from utils.auth import create_default_admin, is_admin, logout
from utils.seed_data import seed_dummy_data
from utils.styles import apply_global_style, render_header, render_footer

@st.cache_resource
def _bootstrap():
    init_database()
    create_default_admin()
    seed_dummy_data()
    return True

try:
    _bootstrap()
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

apply_global_style()

# ── Auth gate ────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    from modules.pg_login import show_login
    show_login()
    st.stop()

user   = st.session_state.get("user", {})
role   = st.session_state.get("role", "viewer")
accent = get_setting("ui_accent_color", "#00d4ff")

if "page" not in st.session_state:
    st.session_state.page = "home"

# ── Page registry ────────────────────────────────────────────
PAGE_MODULES = {
    "home":        "modules.pg_home",
    "iso9001":     "modules.pg_iso9001",
    "iatf":        "modules.pg_iatf",
    "lifecycle":   "modules.pg_lifecycle",
    "consistency": "modules.pg_consistency",
    "batch":       "modules.pg_batch",
    "iqscore":     "modules.pg_iqscore",
    "maung":       "modules.pg_maung",
    "whatif":      "modules.pg_whatif",
    "hipotesis":   "modules.pg_hipotesis",
    "interview":   "modules.pg_interview",
    "about":       "modules.pg_about",
    "theory":      "modules.pg_theory",
    "users":       "modules.pg_users",
    "settings":    "modules.pg_settings",
}

MENU = [
    # (pid, label, group)
    ("home",        "Dashboard Utama",          "EVALUASI"),
    ("iso9001",     "ISO 9001",                 "EVALUASI"),
    ("iatf",        "IATF 16949",               "EVALUASI"),
    ("lifecycle",   "Engineering Lifecycle",    "EVALUASI"),
    ("consistency", "Konsistensi Mutu",         "EVALUASI"),
    ("batch",       "Evaluasi Batch",           "EVALUASI"),
    ("iqscore",     "Integrated Quality Score", "ANALISIS"),
    ("maung",       "Analisis Mutu MAUNG MV3",  "ANALISIS"),
    ("whatif",      "Simulasi What-If",         "ANALISIS"),
    ("hipotesis",   "Kesimpulan & Hipotesis",   "ANALISIS"),
    ("interview",   "Data Wawancara",           "ANALISIS"),
    ("about",       "About Platform",           "PLATFORM"),
    ("theory",      "Teori & Referensi",        "PLATFORM"),
    ("users",       "Manajemen User",           "PLATFORM"),
    ("settings",    "Pengaturan Platform",      "PLATFORM"),
]

def nav(pid):
    st.session_state.page = pid
    st.rerun()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(
        f"<div style='text-align:center;padding:.4rem 0 .6rem;'>"
        f"<div style='font-family:Rajdhani,sans-serif;font-size:1.05rem;"
        f"font-weight:700;color:{accent};letter-spacing:2px;'>IQLE PLATFORM</div>"
        f"<div style='font-size:.58rem;color:#3d5470;letter-spacing:2px;"
        f"text-transform:uppercase;'>PT Pindad (Persero)</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

    # User badge
    _rc  = "#00d4ff" if role == "admin" else "#ffd700"
    _rl  = "ADMIN"  if role == "admin" else "VIEWER"
    _rd  = "Akses penuh & pengaturan" if role == "admin" else "Akses baca semua modul"
    _un  = user.get("full_name") or user.get("username", "")
    st.markdown(
        f"<div style='padding:.4rem .7rem;margin-bottom:.5rem;"
        f"background:rgba(0,212,255,.04);border:1px solid rgba(0,212,255,.12);"
        f"border-radius:7px;'>"
        f"<div style='font-size:.55rem;color:#3d5470;text-transform:uppercase;"
        f"letter-spacing:1px;'>Logged in as</div>"
        f"<div style='font-family:Rajdhani;font-size:.88rem;font-weight:600;"
        f"color:#e8edf5;overflow:hidden;text-overflow:ellipsis;"
        f"white-space:nowrap;'>{_un}</div>"
        f"<div style='margin-top:2px;display:flex;align-items:center;gap:.35rem;'>"
        f"<span style='font-size:.6rem;color:{_rc};font-weight:700;"
        f"text-transform:uppercase;border:1px solid {_rc}44;"
        f"border-radius:3px;padding:1px 5px;'>{_rl}</span>"
        f"<span style='font-size:.58rem;color:#3d5470;'>{_rd}</span>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    st.divider()

    # Nav buttons grouped
    cur    = st.session_state.page
    groups = ["EVALUASI", "ANALISIS", "PLATFORM"]
    for grp in groups:
        st.markdown(
            f"<div style='font-size:.58rem;color:#2a3f55;letter-spacing:1.5px;"
            f"padding:.35rem .1rem .1rem;font-family:Rajdhani;font-weight:600;"
            f"text-transform:uppercase;'>{grp}</div>",
            unsafe_allow_html=True,
        )
        for pid, label, g in MENU:
            if g != grp:
                continue
            if pid in ("users", "settings") and not is_admin():
                continue
            if st.button(
                label,
                key=f"sb_{pid}",
                use_container_width=True,
                type="primary" if cur == pid else "secondary",
            ):
                nav(pid)

    st.divider()
    if st.button("Logout", key="sb_logout", use_container_width=True):
        logout()

# ── Main content ─────────────────────────────────────────────
render_header()

cur = st.session_state.page
mod_path = PAGE_MODULES.get(cur, "modules.pg_home")

import importlib
try:
    mod = importlib.import_module(mod_path)
    mod.show()
except Exception as e:
    st.error(f"Error loading page '{cur}': {e}")
    import traceback
    st.code(traceback.format_exc())

render_footer()
