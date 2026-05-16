import streamlit as st
import os

st.set_page_config(
    page_title="IQLE Platform | PT Pindad",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Init ───────────────────────────────────────────────────
from utils.database import init_database, get_setting
from utils.auth import create_default_admin, is_admin, logout
from utils.seed_data import seed_dummy_data
from utils.styles import apply_global_style, render_header, render_footer

try:
    init_database()
    create_default_admin()
    seed_dummy_data()
except Exception as e:
    st.error(f"Database Error: {e}")
    st.info("Pastikan DATABASE_URL sudah diset di Railway environment variables.")
    st.stop()

apply_global_style()

# ── Auth gate ──────────────────────────────────────────────
if not st.session_state.get('logged_in'):
    from modules.pg_login import show_login
    show_login()
    st.stop()

user = st.session_state.get('user', {})
role = st.session_state.get('role', 'viewer')
accent = get_setting("ui_accent_color", "#00d4ff")

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    # Brand
    st.markdown(f"""
    <div style="text-align:center; padding:1rem 0 1.25rem;
                border-bottom:1px solid rgba(0,212,255,0.15); margin-bottom:1rem;">
        <div style="font-size:1.8rem; margin-bottom:.25rem;">⚙️</div>
        <div style="font-family:'Rajdhani',sans-serif; font-size:1.05rem; font-weight:700;
                    color:{accent}; letter-spacing:2px;">IQLE PLATFORM</div>
        <div style="font-size:.58rem; color:#4a6fa5; letter-spacing:2px;
                    text-transform:uppercase; margin-top:2px;">PT Pindad (Persero)</div>
    </div>
    """, unsafe_allow_html=True)

    # User badge
    st.markdown(f"""
    <div style="padding:.6rem .85rem; margin-bottom:1rem;
                background:rgba(0,212,255,0.05); border:1px solid rgba(0,212,255,0.15);
                border-radius:8px;">
        <div style="font-size:.6rem; color:#4a6fa5; letter-spacing:1px;
                    text-transform:uppercase; margin-bottom:2px;">Logged in as</div>
        <div style="font-family:'Rajdhani',sans-serif; font-size:.9rem;
                    font-weight:600; color:#e8edf5; white-space:nowrap; overflow:hidden;
                    text-overflow:ellipsis;">
            {user.get('full_name') or user.get('username','User')}
        </div>
        <div style="font-size:.62rem; letter-spacing:1px; text-transform:uppercase;
                    color:{'#00d4ff' if role=='admin' else '#ffd700'}; margin-top:1px;">
            {'🔑 ADMIN' if role=='admin' else '👁 VIEWER'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    menu = [
        ("🏠  Dashboard Utama",         "home"),
        ("📊  ISO 9001",                "iso9001"),
        ("🏭  IATF 16949",              "iatf"),
        ("⚙️  Engineering Lifecycle",   "lifecycle"),
        ("✅  Konsistensi Mutu",         "consistency"),
        ("📦  Evaluasi Batch",           "batch"),
        ("🎯  Integrated Quality Score", "iqscore"),
        ("🚗  Analisis Mutu MAUNG MV3",  "maung"),
        ("💬  Data Wawancara",           "interview"),
        ("👤  About Platform",           "about"),
        ("📚  Teori & Referensi",        "theory"),
        ("👥  Manajemen User",           "users"),
        ("🔧  Pengaturan Platform",      "settings"),
    ]

    st.markdown('<div style="font-size:.65rem;color:#4a6fa5;letter-spacing:2px;'
                'text-transform:uppercase;margin-bottom:.4rem;padding:0 .25rem;">MENU</div>',
                unsafe_allow_html=True)

    for label, pid in menu:
        if pid == "users" and not is_admin():
            continue
        if pid == "settings" and not is_admin():
            continue
        active = st.session_state.page == pid
        if st.button(label, key=f"nav_{pid}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = pid
            st.rerun()

    st.markdown("---")
    if st.button("🚪  Logout", use_container_width=True):
        logout()

    # Sidebar version info
    st.markdown("""
    <div style="margin-top:.5rem; padding:.5rem; text-align:center;
                font-size:.6rem; color:#2a3f55; font-family:'JetBrains Mono',monospace;">
        v2.0 · Railway · PostgreSQL<br>Quality 4.0 Dashboard
    </div>""", unsafe_allow_html=True)

# ── Render Header ──────────────────────────────────────────
render_header()

# ── Page routing ───────────────────────────────────────────
p = st.session_state.page

if   p == "home":        from modules.pg_home        import show
elif p == "iso9001":     from modules.pg_iso9001     import show
elif p == "iatf":        from modules.pg_iatf        import show
elif p == "lifecycle":   from modules.pg_lifecycle   import show
elif p == "consistency": from modules.pg_consistency import show
elif p == "batch":       from modules.pg_batch       import show
elif p == "iqscore":     from modules.pg_iqscore     import show
elif p == "maung":       from modules.pg_maung      import show
elif p == "interview":   from modules.pg_interview   import show
elif p == "about":       from modules.pg_about       import show
elif p == "theory":      from modules.pg_theory      import show
elif p == "users":       from modules.pg_users       import show
elif p == "settings":    from modules.pg_settings    import show
else:                    from modules.pg_home        import show

show()

# ── Render Footer ──────────────────────────────────────────
render_footer()
