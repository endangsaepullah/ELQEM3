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
    # ── Toggle sidebar width ───────────────────────────────
    if 'sb_wide' not in st.session_state:
        st.session_state.sb_wide = True
    wide = st.session_state.sb_wide
    sb_w = 255 if wide else 68

    st.markdown(
        f'<style>'
        f'section[data-testid="stSidebar"]>div{{min-width:{sb_w}px!important;'
        f'max-width:{sb_w}px!important;transition:min-width .25s,max-width .25s;}}'
        f'</style>',
        unsafe_allow_html=True
    )

    # Toggle button row
    tc1, tc2 = st.columns([1, 3])
    with tc1:
        if st.button("◀" if wide else "▶", key="sb_tog",
                     help="Ciutkan sidebar" if wide else "Lebarkan sidebar"):
            st.session_state.sb_wide = not wide
            st.rerun()
    with tc2:
        if wide:
            st.markdown(
                '<div style="font-size:.6rem;color:#4a6fa5;padding-top:.45rem;'
                'letter-spacing:1px;">CIUTKAN</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div style="border-bottom:1px solid rgba(0,212,255,0.12);margin:.5rem 0;"></div>',
        unsafe_allow_html=True)

    if not wide:
        # ── Compact mode: icons only ───────────────────────
        compact = [
            ("🏠","home"),("📊","iso9001"),("🏭","iatf"),("⚙️","lifecycle"),
            ("✅","consistency"),("📦","batch"),("🎯","iqscore"),("🚗","maung"),
            ("🔮","whatif"),("🏆","hipotesis"),("💬","interview"),
            ("👤","about"),("📚","theory"),
        ]
        if is_admin():
            compact += [("👥","users"),("🔧","settings")]

        if 'page' not in st.session_state:
            st.session_state.page = 'home'

        for ico, pid in compact:
            active = st.session_state.page == pid
            if st.button(ico, key=f"sbc_{pid}", use_container_width=True,
                         type="primary" if active else "secondary",
                         help=pid.replace("_"," ").upper()):
                st.session_state.page = pid
                st.rerun()
        st.markdown("---")
        if st.button("🚪", use_container_width=True, help="Logout"):
            logout()

    else:
        # ── Full sidebar ───────────────────────────────────
        # Brand
        st.markdown(f"""
        <div style="text-align:center; padding:.5rem 0 1rem;
                    border-bottom:1px solid rgba(0,212,255,0.15); margin-bottom:.75rem;">
            <div style="font-size:1.6rem; margin-bottom:.2rem;">⚙️</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1rem; font-weight:700;
                        color:{accent}; letter-spacing:2px;">IQLE PLATFORM</div>
            <div style="font-size:.58rem; color:#4a6fa5; letter-spacing:2px;
                        text-transform:uppercase; margin-top:2px;">PT Pindad (Persero)</div>
        </div>
        """, unsafe_allow_html=True)

        # User badge
        st.markdown(f"""
        <div style="padding:.5rem .75rem; margin-bottom:.75rem;
                    background:rgba(0,212,255,0.05); border:1px solid rgba(0,212,255,0.15);
                    border-radius:8px;">
            <div style="font-size:.58rem; color:#4a6fa5; letter-spacing:1px;
                        text-transform:uppercase; margin-bottom:2px;">Logged in as</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:.88rem;
                        font-weight:600; color:#e8edf5; white-space:nowrap;
                        overflow:hidden; text-overflow:ellipsis;">
                {user.get('full_name') or user.get('username','User')}
            </div>
            <div style="font-size:.6rem; letter-spacing:1px; text-transform:uppercase;
                        color:{'#00d4ff' if role=='admin' else '#ffd700'}; margin-top:1px;">
                {'🔑 ADMIN' if role=='admin' else '👁 VIEWER'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if 'page' not in st.session_state:
            st.session_state.page = 'home'

        menus = [
            ("── EVALUASI ──────", None),
            ("🏠  Dashboard Utama",         "home"),
            ("📊  ISO 9001",                "iso9001"),
            ("🏭  IATF 16949",              "iatf"),
            ("⚙️  Engineering Lifecycle",   "lifecycle"),
            ("✅  Konsistensi Mutu",         "consistency"),
            ("📦  Evaluasi Batch",           "batch"),
            ("── ANALISIS ──────", None),
            ("🎯  Integrated Quality Score", "iqscore"),
            ("🚗  Analisis Mutu MAUNG MV3",  "maung"),
            ("🔮  Simulasi What-If",          "whatif"),
            ("🏆  Kesimpulan & Hipotesis",    "hipotesis"),
            ("💬  Data Wawancara",            "interview"),
            ("── PLATFORM ──────", None),
            ("👤  About Platform",            "about"),
            ("📚  Teori & Referensi",         "theory"),
            ("👥  Manajemen User",            "users"),
            ("🔧  Pengaturan Platform",       "settings"),
        ]

        for label, pid in menus:
            if pid is None:
                st.markdown(
                    f'<div style="font-size:.58rem;color:#2a3f55;letter-spacing:2px;'
                    f'padding:.3rem .25rem .1rem;font-family:Rajdhani;">{label}</div>',
                    unsafe_allow_html=True)
                continue
            if pid in ["users","settings"] and not is_admin():
                continue
            active = st.session_state.page == pid
            if st.button(label, key=f"nav_{pid}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.page = pid
                st.rerun()

        st.markdown("---")
        if st.button("🚪  Logout", use_container_width=True):
            logout()

        st.markdown("""
        <div style="margin-top:.5rem;padding:.4rem;text-align:center;
                    font-size:.58rem;color:#1e2d42;font-family:'JetBrains Mono',monospace;">
            v2.0 · Railway · PostgreSQL
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
elif p == "whatif":      from modules.pg_whatif     import show
elif p == "hipotesis":   from modules.pg_hipotesis  import show
elif p == "interview":   from modules.pg_interview   import show
elif p == "about":       from modules.pg_about       import show
elif p == "theory":      from modules.pg_theory      import show
elif p == "users":       from modules.pg_users       import show
elif p == "settings":    from modules.pg_settings    import show
else:                    from modules.pg_home        import show

show()

# ── Render Footer ──────────────────────────────────────────
render_footer()
