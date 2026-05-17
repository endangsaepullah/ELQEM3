import streamlit as st

st.set_page_config(
    page_title="IQLE Platform | PT Pindad",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.database import init_database, get_setting
from utils.auth import create_default_admin, is_admin, logout
from utils.seed_data import seed_dummy_data
from utils.styles import apply_global_style, render_topnav, render_header, render_footer

try:
    init_database()
    create_default_admin()
    seed_dummy_data()
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

apply_global_style()

if not st.session_state.get('logged_in'):
    from modules.pg_login import show_login
    show_login()
    st.stop()

user   = st.session_state.get('user', {})
role   = st.session_state.get('role', 'viewer')
accent = get_setting("ui_accent_color", "#00d4ff")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Navigation handled via hidden buttons in render_topnav()

# ── Global CSS ──────────────────────────────────────────────
st.markdown("""
<style>
header[data-testid="stHeader"] { display:none !important; }
.stMainBlockContainer, .block-container {
    max-width: 100% !important;
    /* padding-top diatur oleh render_topnav (44px) */
}
/* Show sidebar collapse button */
[data-testid="stSidebarCollapsedControl"] {
    display: flex !important;
}
button[data-testid="baseButton-headerNoPadding"] {
    display: flex !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(f"""
    <div style="text-align:center;padding:.5rem 0 .75rem;">
      <div style="font-family:Rajdhani,sans-serif;font-size:1.05rem;font-weight:700;
                  color:{accent};letter-spacing:2px;">IQLE PLATFORM</div>
      <div style="font-size:.6rem;color:#3d5470;letter-spacing:2px;
                  text-transform:uppercase;margin-top:2px;">PT Pindad (Persero)</div>
    </div>
    """, unsafe_allow_html=True)

    # User info
    _rc = "#00d4ff" if role == "admin" else "#ffd700"
    _rl = "ADMIN" if role == "admin" else "VIEWER"
    _rd = "Akses penuh & pengaturan" if role == "admin" else "Akses baca semua modul"
    _uname = user.get('full_name') or user.get('username', '')
    st.markdown(f"""
    <div style="padding:.5rem .75rem;margin-bottom:.75rem;
                background:rgba(0,212,255,0.04);border:1px solid rgba(0,212,255,0.12);
                border-radius:8px;">
      <div style="font-size:.58rem;color:#3d5470;text-transform:uppercase;
                  letter-spacing:1px;margin-bottom:2px;">Logged in as</div>
      <div style="font-family:Rajdhani;font-size:.9rem;font-weight:600;
                  color:#e8edf5;overflow:hidden;text-overflow:ellipsis;
                  white-space:nowrap;">{_uname}</div>
      <div style="margin-top:3px;display:flex;align-items:center;gap:.4rem;">
        <span style="font-size:.6rem;color:{_rc};font-weight:700;
                     text-transform:uppercase;border:1px solid {_rc}44;
                     border-radius:3px;padding:1px 5px;">{_rl}</span>
        <span style="font-size:.58rem;color:#3d5470;">{_rd}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    MENU = [
        (None, "── EVALUASI ──────────"),
        ("home",        "Dashboard Utama"),
        ("iso9001",     "ISO 9001"),
        ("iatf",        "IATF 16949"),
        ("lifecycle",   "Engineering Lifecycle"),
        ("consistency", "Konsistensi Mutu"),
        ("batch",       "Evaluasi Batch"),
        (None, "── ANALISIS ──────────"),
        ("iqscore",     "Integrated Quality Score"),
        ("maung",       "Analisis Mutu MAUNG MV3"),
        ("whatif",      "Simulasi What-If"),
        ("hipotesis",   "Kesimpulan & Hipotesis"),
        ("interview",   "Data Wawancara"),
        (None, "── PLATFORM ──────────"),
        ("about",       "About Platform"),
        ("theory",      "Teori & Referensi"),
        ("users",       "Manajemen User"),
        ("settings",    "Pengaturan Platform"),
    ]

    p = st.session_state.page
    for pid, label in MENU:
        if pid is None:
            st.markdown(
                f'<div style="font-size:.58rem;color:#2a3f55;letter-spacing:1.5px;'
                f'padding:.4rem .1rem .1rem;font-family:Rajdhani;'
                f'font-weight:600;">{label}</div>',
                unsafe_allow_html=True
            )
            continue
        if pid in ["users", "settings"] and not is_admin():
            continue
        if st.button(label, key=f"nav_{pid}",
                     use_container_width=True,
                     type="primary" if p == pid else "secondary"):
            st.session_state.page = pid
            st.rerun()

    st.markdown("---")
    if st.button("Logout", key="logout_btn", use_container_width=True):
        logout()

# ── Top Navbar + Header + Content ───────────────────────────
render_topnav()
render_header()

p = st.session_state.page
if   p == "home":        from modules.pg_home        import show
elif p == "iso9001":     from modules.pg_iso9001     import show
elif p == "iatf":        from modules.pg_iatf        import show
elif p == "lifecycle":   from modules.pg_lifecycle   import show
elif p == "consistency": from modules.pg_consistency import show
elif p == "batch":       from modules.pg_batch       import show
elif p == "iqscore":     from modules.pg_iqscore     import show
elif p == "maung":       from modules.pg_maung       import show
elif p == "whatif":      from modules.pg_whatif      import show
elif p == "hipotesis":   from modules.pg_hipotesis   import show
elif p == "interview":   from modules.pg_interview   import show
elif p == "about":       from modules.pg_about       import show
elif p == "theory":      from modules.pg_theory      import show
elif p == "users":       from modules.pg_users       import show
elif p == "settings":    from modules.pg_settings    import show
else:                    from modules.pg_home        import show

show()
render_footer()
