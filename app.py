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
    padding-top:50px!important;
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
    .stMainBlockContainer,.block-container{{padding:.5rem!important;padding-top:50px!important;}}
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

# CSS: hide ALL st.radio/selectbox default styling
st.markdown(f"""
<style>
/* Dropdown navbar wrapper */
.iqle-nav {{
    position:fixed; top:0; left:0; right:0; z-index:500;
    background:#0d1117; border-bottom:1px solid #21262d;
    display:flex; align-items:center; height:46px;
    padding:0; overflow:hidden;
}}
.iqle-nav-brand {{
    font-family:Rajdhani,sans-serif; font-size:.9rem; font-weight:700;
    color:{accent}; letter-spacing:2px; padding:0 1.25rem;
    border-right:1px solid #21262d; height:100%;
    display:flex; align-items:center; flex-shrink:0; white-space:nowrap;
}}
/* Group tabs */
.iqle-nav-tabs {{
    display:flex; align-items:stretch; height:100%; gap:0;
}}
.iqle-nav-tab {{
    display:flex; align-items:center; padding:0 1rem; cursor:pointer;
    font-family:Inter,sans-serif; font-size:.78rem; font-weight:500;
    color:#8b949e; border-bottom:2px solid transparent;
    border-right:1px solid #21262d; white-space:nowrap;
    transition:color .15s, border-color .15s;
    text-decoration:none; height:100%;
}}
.iqle-nav-tab:hover {{ color:#e6edf3; border-bottom-color:#484f58; background:rgba(255,255,255,.04); }}
.iqle-nav-tab.active {{ color:{accent}; font-weight:700; border-bottom-color:{accent}; }}
/* Submenu bar */
.iqle-subnav {{
    position:fixed; top:46px; left:0; right:0; z-index:499;
    background:#161b22; border-bottom:1px solid #21262d;
    display:flex; align-items:center; gap:0; padding:0 1rem;
    height:38px; overflow-x:auto; white-space:nowrap;
}}
.iqle-subnav a {{
    font-family:Inter,sans-serif; font-size:.74rem; font-weight:500;
    color:#6e7681; text-decoration:none; padding:0 .85rem; height:38px;
    display:inline-flex; align-items:center;
    border-bottom:2px solid transparent;
    transition:color .15s, border-color .15s; flex-shrink:0;
}}
.iqle-subnav a:hover {{ color:#e6edf3; border-bottom-color:#484f58; }}
.iqle-subnav a.active {{ color:#e6edf3; font-weight:600; border-bottom-color:{accent}; }}
/* User info right side */
.iqle-nav-right {{
    margin-left:auto; display:flex; align-items:center; gap:.6rem;
    padding:0 .75rem; border-left:1px solid #21262d; flex-shrink:0;
}}
.iqle-user {{ font-size:.72rem; color:#6e7681; white-space:nowrap; max-width:120px;
    overflow:hidden; text-overflow:ellipsis; font-family:Inter,sans-serif; }}
.iqle-role {{ font-size:.62rem; font-weight:700; font-family:Rajdhani,sans-serif;
    letter-spacing:1px; border-radius:3px; padding:1px 5px;
    border:1px solid currentColor; opacity:.8; }}
/* Logout button */
div[data-testid="column"]:has(button[data-testid="baseButton-secondary"][title="Logout"]) {{
    position:fixed; top:5px; right:8px; z-index:9999; width:auto!important;
}}
button[title="Logout"] {{
    background:rgba(255,51,102,0.12)!important;
    border:1px solid rgba(255,51,102,0.4)!important;
    color:#ff3366!important; font-size:.8rem!important;
    width:32px!important; height:32px!important;
    padding:0!important; border-radius:6px!important;
    box-shadow:none!important;
}}
button[title="Logout"]:hover {{
    background:rgba(255,51,102,0.25)!important;
}}
/* Push content below both navbars */
.stMainBlockContainer, .block-container {{
    padding-top:88px !important;
    max-width:100% !important;
    padding-left:1.5rem !important;
    padding-right:1.5rem !important;
}}
@media(max-width:768px) {{
    .iqle-nav-tab {{ padding:0 .65rem; font-size:.72rem; }}
    .iqle-nav-brand {{ padding:0 .75rem; font-size:.78rem; letter-spacing:1px; }}
    .iqle-subnav a {{ padding:0 .55rem; font-size:.68rem; }}
    .stMainBlockContainer, .block-container {{ padding-left:.5rem!important; padding-right:.5rem!important; }}
}}
</style>
""", unsafe_allow_html=True)

# Build top navbar HTML
tabs_html = ""
for grp in MENU_GROUPS:
    is_act = "active" if grp == active_grp else ""
    tabs_html += f'<span class="iqle-nav-tab {is_act}" id="grp-{grp}">{grp}</span>'

# User info + logout in navbar
_uname = user.get('full_name') or user.get('username','')
_role_color = "#00d4ff" if role=="admin" else "#ffd700"
_role_label = "ADMIN" if role=="admin" else "VIEWER"

st.markdown(
    f'<div class="iqle-nav">'
    f'<div class="iqle-nav-brand">⚙ IQLE</div>'
    f'<div class="iqle-nav-tabs">{tabs_html}</div>'
    f'<div class="iqle-nav-right">'
    f'<span class="iqle-user">{_uname}</span>'
    f'<span class="iqle-role" style="color:{_role_color};">{_role_label}</span>'
    f'</div>'
    f'</div>',
    unsafe_allow_html=True
)

# Logout button positioned at top right
_lo_col, _ = st.columns([1, 20])
with _lo_col:
    st.markdown('<div style="position:fixed;top:6px;right:8px;z-index:9999;">',
                unsafe_allow_html=True)
    if st.button("⏻", key="nav_logout", help="Logout"):
        logout()
    st.markdown('</div>', unsafe_allow_html=True)

# Build submenu HTML
sub_html = ""
for lbl, pid in MENU_GROUPS[active_grp]:
    is_act = "active" if pid == p_cur else ""
    sub_html += f'<a class="{is_act}" data-pid="{pid}">{lbl}</a>'

st.markdown(f'<div class="iqle-subnav">{sub_html}</div>', unsafe_allow_html=True)

# Actual navigation: selectbox hidden via CSS but functional
# Group selector
_grp_list = list(MENU_GROUPS.keys())
_grp_idx  = _grp_list.index(active_grp)

st.markdown("""<style>
div[data-testid="stSelectbox"]:has(> label[data-nav="grp"]) {
    position:fixed; top:0; left:120px; right:0; z-index:501;
    height:46px; background:transparent;
}
div[data-testid="stSelectbox"]:has(> label[data-nav="grp"]) > div {
    height:46px; background:transparent; border:none;
}
</style>""", unsafe_allow_html=True)

_chosen_grp = st.selectbox("grp", _grp_list, index=_grp_idx,
                            key="nav_grp", label_visibility="collapsed")
if _chosen_grp != active_grp:
    # Navigate to first page of new group
    first_pid = MENU_GROUPS[_chosen_grp][0][1]
    st.session_state.page = first_pid
    st.rerun()

# Sub-page selector
_sub_items  = MENU_GROUPS[active_grp]
_sub_labels = [l for l,_ in _sub_items]
_sub_pids   = [p for _,p in _sub_items]
_sub_idx    = _sub_pids.index(p_cur) if p_cur in _sub_pids else 0

_chosen_sub = st.selectbox("page", _sub_labels, index=_sub_idx,
                            key="nav_sub", label_visibility="collapsed")
_chosen_pid = _sub_pids[_sub_labels.index(_chosen_sub)]
if _chosen_pid != p_cur:
    st.session_state.page = _chosen_pid
    st.rerun()



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
