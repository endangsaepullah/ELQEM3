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

collapsed = st.session_state.sidebar_collapsed

# ── CSS Sidebar Collapse (inject ke DOM Streamlit) ─────────
# Streamlit menyimpan sidebar di [data-testid="stSidebar"]
# Kita override min/max width lewat CSS !important
sidebar_width = "72px" if collapsed else "260px"

st.markdown(f"""
<style>
/* ── Sembunyikan tombol collapse bawaan Streamlit ── */
button[data-testid="collapsedControl"] {{
    display: none !important;
}}

/* ── Override lebar sidebar ── */
[data-testid="stSidebar"] > div:first-child {{
    width: {sidebar_width} !important;
    min-width: {sidebar_width} !important;
    max-width: {sidebar_width} !important;
    overflow: hidden !important;
    transition: width 0.25s ease, min-width 0.25s ease !important;
}}

/* ── Saat collapsed: sembunyikan semua elemen teks panjang ── */
{''.join([
    '[data-testid="stSidebar"] .sidebar-brand-text { display: none !important; }',
    '[data-testid="stSidebar"] .sidebar-user-full  { display: none !important; }',
    '[data-testid="stSidebar"] .sidebar-menu-label { display: none !important; }',
    '[data-testid="stSidebar"] .sidebar-version    { display: none !important; }',
    '[data-testid="stSidebar"] hr { margin: 4px 0 !important; }',
    # Paksa tombol jadi kotak kecil saat collapsed
    '[data-testid="stSidebar"] .stButton > button { padding: 6px 4px !important; font-size: 16px !important; justify-content: center !important; }',
]) if collapsed else ''}

/* ── Floating toggle button di tepi sidebar ── */
.sidebar-float-btn {{
    position: fixed;
    top: 50%;
    left: calc({sidebar_width} + 0px);
    transform: translateY(-50%);
    z-index: 99999;
    width: 20px;
    height: 48px;
    background: #0d1b2a;
    border: 1px solid rgba(0,212,255,0.35);
    border-left: none;
    border-radius: 0 8px 8px 0;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #00d4ff;
    font-size: 11px;
    transition: left 0.25s ease, background 0.15s;
}}
.sidebar-float-btn:hover {{
    background: rgba(0,212,255,0.12);
}}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:

    # ── Tombol toggle di bagian paling atas ───────────────
    toggle_icon = "▶" if collapsed else "◀"
    toggle_tip  = "Lebarkan sidebar" if collapsed else "Ciutkan sidebar"

    if st.button(toggle_icon, key="sb_toggle", help=toggle_tip, use_container_width=True):
        st.session_state.sidebar_collapsed = not collapsed
        st.rerun()

    # ── Brand ─────────────────────────────────────────────
    if not collapsed:
        st.markdown(f"""
        <div style="text-align:center; padding:.6rem 0 1rem;
                    border-bottom:1px solid rgba(0,212,255,0.15); margin-bottom:1rem;">
            <div style="font-size:1.8rem; margin-bottom:.2rem;">⚙️</div>
            <div class="sidebar-brand-text"
                 style="font-family:'Rajdhani',sans-serif; font-size:1.05rem; font-weight:700;
                        color:{accent}; letter-spacing:2px;">IQLE PLATFORM</div>
            <div class="sidebar-brand-text"
                 style="font-size:.58rem; color:#4a6fa5; letter-spacing:2px;
                        text-transform:uppercase; margin-top:2px;">PT Pindad (Persero)</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:.3rem 0 .6rem;
                    border-bottom:1px solid rgba(0,212,255,0.15); margin-bottom:.5rem;">
            <div style="font-size:1.4rem;">⚙️</div>
        </div>
        """, unsafe_allow_html=True)

    # ── User badge ────────────────────────────────────────
    if not collapsed:
        st.markdown(f"""
        <div class="sidebar-user-full"
             style="padding:.5rem .75rem; margin-bottom:.75rem;
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

    # ── Navigation ────────────────────────────────────────
    if 'page' not in st.session_state:
        st.session_state.page = 'home'

    # (emoji, label, page_id)
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

    if not collapsed:
        st.markdown(
            '<div class="sidebar-menu-label" style="font-size:.63rem; color:#4a6fa5; '
            'letter-spacing:2px; text-transform:uppercase; margin-bottom:.3rem; '
            'padding:0 .2rem;">MENU</div>',
            unsafe_allow_html=True
        )

    for emoji, label, pid in menu:
        if pid == "users"    and not is_admin(): continue
        if pid == "settings" and not is_admin(): continue

        active     = st.session_state.page == pid
        btn_label  = emoji if collapsed else f"{emoji}  {label}"
        btn_help   = label if collapsed else None

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

    # ── Logout ────────────────────────────────────────────
    logout_label = "🚪" if collapsed else "🚪  Logout"
    logout_help  = "Logout" if collapsed else None
    if st.button(logout_label, key="btn_logout", help=logout_help, use_container_width=True):
        logout()

    # ── Versi (hanya saat expanded) ───────────────────────
    if not collapsed:
        st.markdown("""
        <div class="sidebar-version"
             style="margin-top:.5rem; padding:.4rem; text-align:center;
                    font-size:.58rem; color:#2a3f55;
                    font-family:'JetBrains Mono',monospace;">
            v2.0 · Railway · PostgreSQL<br>Quality 4.0 Dashboard
        </div>""", unsafe_allow_html=True)

# ── Handle navigasi dari sitemap (chat command) ────────────
# Modul sitemap mengirim pesan "Buka halaman <pid>"
# Kita tangkap lewat query param atau session state
# Cara termudah: tambahkan halaman "sitemap" ke menu routing

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
elif p == "sitemap":
    # ── Halaman Sitemap ────────────────────────────────────
    st.markdown("## 🗺️ Sitemap Platform")
    st.markdown("Pilih halaman yang ingin dituju:")

    pages_all = [
        ("🏠", "Dashboard Utama",          "home",        False),
        ("📊", "ISO 9001",                 "iso9001",     False),
        ("🏭", "IATF 16949",               "iatf",        False),
        ("⚙️", "Engineering Lifecycle",    "lifecycle",   False),
        ("✅", "Konsistensi Mutu",          "consistency", False),
        ("📦", "Evaluasi Batch",            "batch",       False),
        ("🎯", "Integrated Quality Score",  "iqscore",     False),
        ("🚗", "Analisis Mutu MAUNG MV3",   "maung",       False),
        ("💬", "Data Wawancara",            "interview",   False),
        ("👤", "About Platform",            "about",       False),
        ("📚", "Teori & Referensi",         "theory",      False),
        ("👥", "Manajemen User",            "users",       True),
        ("🔧", "Pengaturan Platform",       "settings",    True),
    ]

    cols = st.columns(3)
    for i, (emoji, label, pid, admin_only) in enumerate(pages_all):
        if admin_only and not is_admin():
            continue
        with cols[i % 3]:
            if st.button(f"{emoji} {label}", key=f"sitemap_nav_{pid}", use_container_width=True):
                st.session_state.page = pid
                st.rerun()
else:
    from modules.pg_home import show

show()

# ── Render Footer ──────────────────────────────────────────
render_footer()
