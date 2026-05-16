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
from utils.styles import apply_global_style, render_header, render_footer

try:
    init_database()
    create_default_admin()
    seed_dummy_data()
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

apply_global_style()
accent = get_setting("ui_accent_color", "#00d4ff")

if not st.session_state.get('logged_in'):
    from modules.pg_login import show_login
    show_login()
    st.stop()

user = st.session_state.get('user', {})
role = st.session_state.get('role', 'viewer')
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Global CSS
st.markdown(f"""
<style>
/* Full width */
.stMainBlockContainer,.block-container{{
    max-width:100%!important;
    padding:0 1.5rem!important;
    padding-top:84px!important;
}}
/* Hide default sidebar collapse button */
[data-testid="stSidebarCollapsedControl"]{{display:none!important;}}
header[data-testid="stHeader"]{{display:none!important;}}

/* Sidebar mobile: hidden by default, shown when sb-open class added */
@media(max-width:768px){{
    [data-testid="stSidebar"]{{
        position:fixed!important;z-index:999!important;
        transform:translateX(-110%)!important;
        transition:transform .25s ease!important;
        height:100vh!important;top:0!important;left:0!important;
        min-width:260px!important;max-width:260px!important;
        box-shadow:4px 0 24px rgba(0,0,0,.6)!important;
    }}
    section[data-testid="stSidebar"].open{{
        transform:translateX(0)!important;
    }}
    .stMainBlockContainer,.block-container{{padding:.5rem!important;padding-top:84px!important;}}
}}

/* nav handled by iqle-nav CSS below */
</style>
""", unsafe_allow_html=True)

MENU_GROUPS = {
    "Evaluasi": [
        ("Dashboard Utama",        "home"),
        ("ISO 9001",               "iso9001"),
        ("IATF 16949",             "iatf"),
        ("Engineering Lifecycle",  "lifecycle"),
        ("Konsistensi Mutu",       "consistency"),
        ("Evaluasi Batch",         "batch"),
    ],
    "Analisis": [
        ("Integrated Quality Score","iqscore"),
        ("Analisis Mutu MAUNG MV3", "maung"),
        ("Simulasi What-If",        "whatif"),
        ("Kesimpulan & Hipotesis",  "hipotesis"),
        ("Data Wawancara",          "interview"),
    ],
    "Platform": [
        ("About Platform",          "about"),
        ("Teori & Referensi",       "theory"),
        ("Manajemen User",          "users"),
        ("Pengaturan Platform",     "settings"),
    ],
}

def _active_group(pid):
    for grp, items in MENU_GROUPS.items():
        if any(p == pid for _, p in items):
            return grp
    return "Evaluasi"

p_cur      = st.session_state.get('page', 'home')
active_grp = _active_group(p_cur)
_uname     = user.get('full_name') or user.get('username','')
_is_admin  = role == "admin"
_rc        = "#00d4ff" if _is_admin else "#ffd700"
_rl        = "ADMIN" if _is_admin else "VIEWER"

# ── Simple CSS tab navbar ────────────────────────────────────
st.markdown(f"""
<style>
/* Hide Streamlit default header */
header[data-testid="stHeader"]{{display:none!important;}}
[data-testid="stSidebarCollapsedControl"]{{display:none!important;}}

/* Main content spacing */
.stMainBlockContainer,.block-container{{
    max-width:100%!important;
    padding-top:0!important;
    padding-left:1rem!important;
    padding-right:1rem!important;
}}

/* Navbar group buttons — top level */
div.nav-group-row > div[data-testid="column"] > div > div > div > button {{
    background:transparent!important;
    border:none!important;
    border-bottom:2px solid transparent!important;
    border-radius:0!important;
    color:#8b949e!important;
    font-family:Inter,sans-serif!important;
    font-size:.82rem!important;
    font-weight:500!important;
    padding:0 .85rem!important;
    height:46px!important;
    box-shadow:none!important;
    letter-spacing:.3px!important;
    transition:color .15s,border-color .15s!important;
}}
div.nav-group-row > div[data-testid="column"] > div > div > div > button:hover {{
    color:#e6edf3!important;
    border-bottom-color:#484f58!important;
    background:rgba(255,255,255,.04)!important;
}}
div.nav-group-row > div[data-testid="column"] > div > div > div > button[kind="primary"] {{
    color:{accent}!important;
    font-weight:700!important;
    border-bottom-color:{accent}!important;
    background:transparent!important;
}}

/* Sub-menu buttons */
div.nav-sub-row > div[data-testid="column"] > div > div > div > button {{
    background:transparent!important;
    border:none!important;
    border-bottom:2px solid transparent!important;
    border-radius:0!important;
    color:#6e7681!important;
    font-family:Inter,sans-serif!important;
    font-size:.76rem!important;
    font-weight:400!important;
    padding:0 .75rem!important;
    height:36px!important;
    box-shadow:none!important;
    transition:color .15s,border-color .15s!important;
}}
div.nav-sub-row > div[data-testid="column"] > div > div > div > button:hover {{
    color:#c9d1d9!important;
    border-bottom-color:#484f58!important;
    background:rgba(255,255,255,.03)!important;
}}
div.nav-sub-row > div[data-testid="column"] > div > div > div > button[kind="primary"] {{
    color:#e6edf3!important;
    font-weight:600!important;
    border-bottom-color:{accent}!important;
    background:transparent!important;
}}

/* Logout button */
div.nav-logout-col > div > div > div > button {{
    background:rgba(255,51,102,.1)!important;
    border:1px solid rgba(255,51,102,.35)!important;
    color:#ff3366!important;
    font-family:Rajdhani,sans-serif!important;
    font-size:.72rem!important;
    font-weight:700!important;
    padding:0 .75rem!important;
    height:30px!important;
    border-radius:5px!important;
    box-shadow:none!important;
    letter-spacing:.5px!important;
}}
div.nav-logout-col > div > div > div > button:hover {{
    background:rgba(255,51,102,.22)!important;
}}

/* Nav wrappers */
.nav-top-bar {{
    background:#0d1117;
    border-bottom:1px solid #21262d;
    padding:0 .5rem;
    display:flex; align-items:center;
}}
.nav-sub-bar {{
    background:#161b22;
    border-bottom:1px solid #21262d;
    padding:0 .5rem;
}}
.nav-brand {{
    font-family:Rajdhani,sans-serif;font-size:.9rem;font-weight:700;
    color:{accent};letter-spacing:2px;padding:0 1rem 0 .25rem;
    display:flex;align-items:center;height:46px;
    border-right:1px solid #21262d;flex-shrink:0;white-space:nowrap;
}}
.nav-user {{
    margin-left:auto;display:flex;align-items:center;gap:.5rem;
    padding:0 .5rem;flex-shrink:0;font-size:.72rem;
    color:#8b949e;font-family:Inter,sans-serif;white-space:nowrap;
}}
.nav-user strong{{color:#c9d1d9;}}
.role-badge{{
    font-family:Rajdhani;font-size:.6rem;font-weight:700;
    letter-spacing:1px;border-radius:3px;padding:1px 5px;
    border:1px solid currentColor;
}}
</style>
""", unsafe_allow_html=True)

# ── Top bar: brand + group tabs + user + logout ──────────────
st.markdown('<div class="nav-top-bar">', unsafe_allow_html=True)

brand_col, *grp_cols, user_col, logout_col = st.columns(
    [1] + [1.2]*len(MENU_GROUPS) + [2, 0.6]
)
with brand_col:
    st.markdown(f'<div class="nav-brand">⚙ IQLE</div>', unsafe_allow_html=True)

st.markdown('<div class="nav-group-row" style="display:contents;">', unsafe_allow_html=True)
for col, (grp, _) in zip(grp_cols, MENU_GROUPS.items()):
    with col:
        active = grp == active_grp
        if st.button(grp, key=f"grp_{grp}",
                     use_container_width=True,
                     type="primary" if active else "secondary"):
            first = MENU_GROUPS[grp][0][1]
            st.session_state.page = first
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

with user_col:
    st.markdown(
        f'<div class="nav-user">'
        f'Halo, <strong>{_uname}</strong>'
        f'&nbsp;<span class="role-badge" style="color:{_rc};">{_rl}</span>'
        f'</div>',
        unsafe_allow_html=True
    )
with logout_col:
    st.markdown('<div class="nav-logout-col">', unsafe_allow_html=True)
    if st.button("⏻ Keluar", key="nav_logout", use_container_width=True):
        logout()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close nav-top-bar

# ── Sub-menu bar ─────────────────────────────────────────────
st.markdown('<div class="nav-sub-bar">', unsafe_allow_html=True)
sub_items = MENU_GROUPS[active_grp]
st.markdown('<div class="nav-sub-row">', unsafe_allow_html=True)
sub_cols = st.columns(len(sub_items))
for col, (lbl, pid) in zip(sub_cols, sub_items):
    with col:
        active = pid == p_cur
        if st.button(lbl, key=f"sub_{pid}",
                     use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.page = pid
            st.rerun()
st.markdown('</div></div>', unsafe_allow_html=True)  # close nav-sub-row + nav-sub-bar



p = st.session_state.page
if   p=="home":        from modules.pg_home        import show
elif p=="iso9001":     from modules.pg_iso9001     import show
elif p=="iatf":        from modules.pg_iatf        import show
elif p=="lifecycle":   from modules.pg_lifecycle   import show
elif p=="consistency": from modules.pg_consistency import show
elif p=="batch":       from modules.pg_batch       import show
elif p=="iqscore":     from modules.pg_iqscore     import show
elif p=="maung":       from modules.pg_maung       import show
elif p=="whatif":      from modules.pg_whatif      import show
elif p=="hipotesis":   from modules.pg_hipotesis   import show
elif p=="interview":   from modules.pg_interview   import show
elif p=="about":       from modules.pg_about       import show
elif p=="theory":      from modules.pg_theory      import show
elif p=="users":       from modules.pg_users       import show
elif p=="settings":    from modules.pg_settings    import show
else:                  from modules.pg_home        import show

show()
render_footer()
