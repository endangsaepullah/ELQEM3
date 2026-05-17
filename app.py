"""
IQLE Platform — app.py
Arsitektur: Streamlit sidebar-only navigation
Prinsip: session_state router, tidak ada HTML/JS hack
"""
import importlib
import streamlit as st

st.set_page_config(
    page_title="IQLE Platform | PT Pindad",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Bootstrap (cached, hanya sekali per session) ─────────────
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

# ── Auth ─────────────────────────────────────────────────────
if not st.session_state.get("logged_in"):
    from modules.pg_login import show_login
    show_login()
    st.stop()

# ── State defaults ────────────────────────────────────────────
user   = st.session_state.get("user", {})
role   = st.session_state.get("role", "viewer")
accent = get_setting("ui_accent_color", "#00d4ff")
if "page" not in st.session_state:
    st.session_state.page = "home"

# ── Route registry ────────────────────────────────────────────
PAGES = {
    "home":        ("Dashboard Utama",          "EVALUASI", "modules.pg_home"),
    "iso9001":     ("ISO 9001",                 "EVALUASI", "modules.pg_iso9001"),
    "iatf":        ("IATF 16949",               "EVALUASI", "modules.pg_iatf"),
    "lifecycle":   ("Engineering Lifecycle",    "EVALUASI", "modules.pg_lifecycle"),
    "consistency": ("Konsistensi Mutu",         "EVALUASI", "modules.pg_consistency"),
    "batch":       ("Evaluasi Batch",           "EVALUASI", "modules.pg_batch"),
    "iqscore":     ("Integrated Quality Score", "ANALISIS", "modules.pg_iqscore"),
    "maung":       ("Analisis Mutu MAUNG MV3",  "ANALISIS", "modules.pg_maung"),
    "whatif":      ("Simulasi What-If",         "ANALISIS", "modules.pg_whatif"),
    "hipotesis":   ("Kesimpulan & Hipotesis",   "ANALISIS", "modules.pg_hipotesis"),
    "interview":   ("Data Wawancara",           "ANALISIS", "modules.pg_interview"),
    "about":       ("About Platform",           "PLATFORM", "modules.pg_about"),
    "theory":      ("Teori & Referensi",        "PLATFORM", "modules.pg_theory"),
    "users":       ("Manajemen User",           "PLATFORM", "modules.pg_users"),
    "settings":    ("Pengaturan Platform",      "PLATFORM", "modules.pg_settings"),
}

def go(pid: str):
    """Navigate to page."""
    st.session_state.page = pid
    st.rerun()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    _un = user.get("full_name") or user.get("username", "")
    _rc = "#00d4ff" if role == "admin" else "#ffd700"
    _rl = "ADMIN"   if role == "admin" else "VIEWER"

    # Brand + user
    st.markdown(
        f"<div style='padding:.4rem .2rem .7rem;"
        f"border-bottom:1px solid rgba(0,212,255,.15);margin-bottom:.4rem;'>"
        f"<div style='font-family:Rajdhani,sans-serif;font-size:1rem;"
        f"font-weight:700;color:{accent};letter-spacing:2px;'>IQLE PLATFORM</div>"
        f"<div style='font-size:.58rem;color:#3d5470;'>PT Pindad (Persero)</div>"
        f"<div style='margin-top:.35rem;display:flex;align-items:center;gap:.35rem;'>"
        f"<span style='font-size:.75rem;color:#c9d1d9;font-weight:600;'>{_un}</span>"
        f"<span style='font-size:.6rem;color:{_rc};border:1px solid {_rc}55;"
        f"border-radius:3px;padding:0 4px;font-family:Rajdhani;font-weight:700;'>{_rl}</span>"
        f"</div></div>",
        unsafe_allow_html=True,
    )

    # Menu per group
    cur = st.session_state.page
    for grp in ("EVALUASI", "ANALISIS", "PLATFORM"):
        st.caption(grp)
        for pid, (label, g, _) in PAGES.items():
            if g != grp:
                continue
            if pid in ("users", "settings") and not is_admin():
                continue
            if st.button(
                label,
                key=f"nav_{pid}",
                use_container_width=True,
                type="primary" if cur == pid else "secondary",
            ):
                go(pid)

    st.divider()
    if st.button("⏻  Logout", key="nav_logout", use_container_width=True):
        logout()

# ── Content ──────────────────────────────────────────────────
render_header()

cur = st.session_state.page
if cur not in PAGES:
    cur = "home"

_, _, mod_path = PAGES[cur]
try:
    mod = importlib.import_module(mod_path)
    mod.show()
except Exception as exc:
    st.error(f"Error loading page: {exc}")
    import traceback
    st.code(traceback.format_exc())

render_footer()
