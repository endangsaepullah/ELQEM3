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

# ── Sidebar collapse state ─────────────────────────────────
if 'sidebar_collapsed' not in st.session_state:
    st.session_state.sidebar_collapsed = False

# ── CSS untuk sidebar collapse ─────────────────────────────
# Saat collapsed, sembunyikan teks menu dan perkecil sidebar
st.markdown(f"""
<style>
/* ── Sidebar collapse toggle button ── */
.sidebar-toggle-btn {{
    position: fixed;
    top: 50%;
    left: {'72px' if st.session_state.sidebar_collapsed else '258px'};
    transform: translateY(-50%);
    z-index: 9999;
    background: #0d1b2a;
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: left 0.3s ease;
    color: #00d4ff;
    font-size: 12px;
    box-shadow: 0 0 8px rgba(0,212,255,0.2);
}}
.sidebar-toggle-btn:hover {{
    background: rgba(0,212,255,0.1);
    box-shadow: 0 0 12px rgba(0,212,255,0.35);
}}

/* ── Collapsed sidebar: sembunyikan teks, hanya tampilkan emoji ── */
{'[data-testid="stSidebar"] { min-width: 80px !important; max-width: 80px !important; }' if st.session_state.sidebar_collapsed else ''}
{'[data-testid="stSidebar"] .sidebar-label-text { display: none !important; }' if st.session_state.sidebar_collapsed else ''}
{'[data-testid="stSidebar"] .sidebar-brand-full { display: none !important; }' if st.session_state.sidebar_collapsed else ''}
{'[data-testid="stSidebar"] .sidebar-user-badge { display: none !important; }' if st.session_state.sidebar_collapsed else ''}
{'[data-testid="stSidebar"] .stButton > button { padding: 0.4rem 0.5rem !important; font-size: 1.1rem !important; }' if st.session_state.sidebar_collapsed else ''}
{'[data-testid="stSidebar"] .stButton > button > div { display: flex; justify-content: center; }' if st.session_state.sidebar_collapsed else ''}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    # ── Toggle button (collapse / expand) ─────────────────
    col_toggle, col_space = st.columns([1, 4]) if not st.session_state.sidebar_collapsed else [st.columns(1)[0], None]

    toggle_label = "▶" if not st.session_state.sidebar_collapsed else "◀"
    toggle_help  = "Ciutkan sidebar" if not st.session_state.sidebar_collapsed else "Lebarkan sidebar"

    # Tombol collapse di baris pertama sidebar (atas kanan)
    btn_col1, btn_col2 = st.columns([4, 1]) if not st.session_state.sidebar_collapsed else st.columns([1, 1])

    with btn_col2 if not st.session_state.sidebar_collapsed else btn_col1:
        if st.button(
            toggle_label,
            key="sidebar_toggle",
            help=toggle_help,
            use_container_width=False
        ):
            st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
            st.rerun()

    # ── Brand (hanya tampil saat expanded) ────────────────
    if not st.session_state.sidebar_collapsed:
        st.markdown(f"""
        <div class="sidebar-brand-full" style="text-align:center; padding:.5rem 0 1.25rem;
                    border-bottom:1px solid rgba(0,212,255,0.15); margin-bottom:1rem;">
            <div style="font-size:1.8rem; margin-bottom:.25rem;">⚙️</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.05rem; font-weight:700;
                        color:{accent}; letter-spacing:2px;">IQLE PLATFORM</div>
            <div style="font-size:.58rem; color:#4a6fa5; letter-spacing:2px;
                        text-transform:uppercase; margin-top:2px;">PT Pindad (Persero)</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Mini brand: hanya ikon
        st.markdown(f"""
        <div style="text-align:center; padding:.4rem 0 .6rem;
                    border-bottom:1px solid rgba(0,212,255,0.15); margin-bottom:.6rem;">
            <div style="font-size:1.5rem;">⚙️</div>
        </div>
        """, unsafe_allow_html=True)

    # ── User badge (hanya tampil saat expanded) ────────────
    if not st.session_state.sidebar_collapsed:
        st.markdown(f"""
        <div class="sidebar-user-badge" style="padding:.6rem .85rem; margin-bottom:1rem;
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

    # ── Navigation ─────────────────────────────────────────
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    # Menu: (emoji, label_text, page_id)
    menu = [
        ("🏠", "Dashboard Utama",          "home"),
        ("📊", "ISO 9001",                 "iso9001"),
        ("🏭", "IATF 16949",               "iatf"),
        ("⚙️", "Engineering Lifecycle",    "lifecycle"),
        ("✅", "Konsistensi Mutu",          "consistency"),
        ("📦", "Evaluasi Batch",            "batch"),
        ("🎯", "Integrated Quality Score",  "iqscore"),
        ("🚗", "Analisis Mutu MAUNG MV3",   "maung"),
        ("💬", "Data Wawancara",            "interview"),
        ("👤", "About Platform",            "about"),
        ("📚", "Teori & Referensi",         "theory"),
        ("👥", "Manajemen User",            "users"),
        ("🔧", "Pengaturan Platform",       "settings"),
    ]

    if not st.session_state.sidebar_collapsed:
        st.markdown(
            '<div style="font-size:.65rem;color:#4a6fa5;letter-spacing:2px;'
            'text-transform:uppercase;margin-bottom:.4rem;padding:0 .25rem;">MENU</div>',
            unsafe_allow_html=True
        )

    for emoji, label, pid in menu:
        if pid == "users" and not is_admin():
            continue
        if pid == "settings" and not is_admin():
            continue

        active = st.session_state.page == pid

        # Label: tampilkan emoji saja saat collapsed, emoji+teks saat expanded
        if st.session_state.sidebar_collapsed:
            btn_label = emoji
            btn_help  = label          # tooltip saat hover
        else:
            btn_label = f"{emoji}  {label}"
            btn_help  = None

        if st.button(
            btn_label,
            key=f"nav_{pid}",
            help=btn_help,
            use_container_width=True,
            type="primary" if active else "secondary"
        ):
            st.session_state.page = pid
            st.rerun()

    st.markdown("---")

    # Logout
    if st.session_state.sidebar_collapsed:
        if st.button("🚪", key="logout_btn", help="Logout", use_container_width=True):
            logout()
    else:
        if st.button("🚪  Logout", key="logout_btn", use_container_width=True):
            logout()

    # ── Versi info (hanya saat expanded) ──────────────────
    if not st.session_state.sidebar_collapsed:
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
elif p == "maung":       from modules.pg_maung       import show
elif p == "interview":   from modules.pg_interview   import show
elif p == "about":       from modules.pg_about       import show
elif p == "theory":      from modules.pg_theory      import show
elif p == "users":       from modules.pg_users       import show
elif p == "settings":    from modules.pg_settings    import show
else:                    from modules.pg_home        import show

show()

# ── Render Footer ──────────────────────────────────────────
render_footer()
