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

/* Radio nav */
div[data-testid="stRadio"]>label{{display:none!important;}}
div[data-testid="stRadio"]>div{{
    display:flex!important;flex-direction:row!important;
    flex-wrap:nowrap!important;gap:0!important;
    background:#0d1117!important;border:none!important;
    overflow-x:auto!important;padding:0!important;
    border-bottom:1px solid #21262d;
    position:fixed!important;top:0!important;left:0!important;right:0!important;
    z-index:200;
}}
div[data-testid="stRadio"]>div>label{{
    display:flex!important;align-items:center!important;
    padding:0 .85rem!important;height:46px!important;
    cursor:pointer!important;white-space:nowrap!important;
    font-family:Inter,sans-serif!important;font-size:.77rem!important;
    font-weight:500!important;color:#8b949e!important;
    background:transparent!important;border:none!important;border-radius:0!important;
    border-bottom:2px solid transparent!important;
    margin:0!important;flex-shrink:0!important;
    transition:color .15s,border-color .15s!important;
}}
div[data-testid="stRadio"]>div>label:hover{{
    color:#e6edf3!important;border-bottom-color:#484f58!important;
    background:rgba(255,255,255,.04)!important;
}}
div[data-testid="stRadio"]>div>label:has(input:checked){{
    color:#e6edf3!important;font-weight:600!important;
    border-bottom-color:{accent}!important;
}}
div[data-testid="stRadio"]>div>label>div:first-child{{display:none!important;}}
@media(max-width:768px){{
    div[data-testid="stRadio"]>div{{left:0!important;}}
    div[data-testid="stRadio"]>div>label{{
        padding:0 .5rem!important;font-size:.68rem!important;height:42px!important;
    }}
}}
</style>

<script>
function toggleSidebar(){{
    var sb = window.parent.document.querySelector('[data-testid="stSidebar"]');
    if(sb) sb.classList.toggle('open');
}}
</script>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if 'sb_wide' not in st.session_state:
        st.session_state.sb_wide = True
    wide = st.session_state.sb_wide
    sb_w2 = 255 if wide else 72
    st.markdown(f'<style>section[data-testid="stSidebar"]>div{{min-width:{sb_w2}px!important;max-width:{sb_w2}px!important;}}</style>', unsafe_allow_html=True)

    tc1, tc2 = st.columns([1,3])
    with tc1:
        if st.button("◀" if wide else "▶", key="sb_tog"):
            st.session_state.sb_wide = not wide; st.rerun()
    with tc2:
        if wide:
            st.markdown(f'<span style="font-size:.6rem;color:#3d5470;">CIUTKAN</span>', unsafe_allow_html=True)

    st.markdown('<div style="border-bottom:1px solid rgba(0,212,255,0.1);margin:.4rem 0;"></div>', unsafe_allow_html=True)

    MENU = [
        (None,"EVALUASI"),("home","Dashboard Utama"),("iso9001","ISO 9001"),
        ("iatf","IATF 16949"),("lifecycle","Engineering Lifecycle"),
        ("consistency","Konsistensi Mutu"),("batch","Evaluasi Batch"),
        (None,"ANALISIS"),("iqscore","Integrated Quality Score"),
        ("maung","Analisis Mutu MAUNG MV3"),("whatif","Simulasi What-If"),
        ("hipotesis","Kesimpulan & Hipotesis"),("interview","Data Wawancara"),
        (None,"PLATFORM"),("about","About Platform"),("theory","Teori & Referensi"),
        ("users","Manajemen User"),("settings","Pengaturan Platform"),
    ]

    if not wide:
        ICONS={"home":"⌂","iso9001":"①","iatf":"②","lifecycle":"③","consistency":"④",
               "batch":"⑤","iqscore":"⑥","maung":"⑦","whatif":"⑧","hipotesis":"⑨",
               "interview":"⑩","about":"◉","theory":"◎","users":"◈","settings":"◇"}
        for pid,label in [(p,l) for p,l in MENU if p]:
            if pid in ["users","settings"] and not is_admin(): continue
            if st.button(ICONS.get(pid,"·"), key=f"sbc_{pid}",
                         use_container_width=True, help=label,
                         type="primary" if st.session_state.page==pid else "secondary"):
                st.session_state.page=pid; st.rerun()
    else:
        st.markdown(f'''<div style="padding:.4rem 0 .6rem;text-align:center;">
<div style="font-family:Rajdhani;font-size:1rem;font-weight:700;color:{accent};letter-spacing:2px;">IQLE PLATFORM</div>
<div style="font-size:.58rem;color:#3d5470;letter-spacing:2px;text-transform:uppercase;">PT Pindad</div>
</div>''', unsafe_allow_html=True)

        _rc = "#00d4ff" if role=="admin" else "#ffd700"
        _rl = "ADMIN" if role=="admin" else "VIEWER"
        _rd = "Akses penuh: input, edit & setting" if role=="admin" else "Akses baca semua modul"
        st.markdown(f'''<div style="padding:.4rem .7rem;margin-bottom:.5rem;
background:rgba(0,212,255,0.04);border:1px solid rgba(0,212,255,0.12);border-radius:7px;">
<div style="font-size:.55rem;color:#3d5470;text-transform:uppercase;letter-spacing:1px;">Logged in as</div>
<div style="font-family:Rajdhani;font-size:.88rem;font-weight:600;color:#e8edf5;
overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{user.get("full_name") or user.get("username","")}</div>
<div style="margin-top:2px;">
<span style="font-size:.6rem;color:{_rc};font-weight:700;text-transform:uppercase;
border:1px solid {_rc}44;border-radius:3px;padding:1px 5px;">{_rl}</span>
<span style="font-size:.58rem;color:#3d5470;margin-left:.35rem;">{_rd}</span>
</div></div>''', unsafe_allow_html=True)

        p = st.session_state.page
        for pid,label in MENU:
            if pid is None:
                st.markdown(f'''<div style="font-size:.58rem;color:#2a3f55;
letter-spacing:2px;text-transform:uppercase;padding:.3rem .2rem .1rem;font-family:Rajdhani;">{label}</div>''', unsafe_allow_html=True)
                continue
            if pid in ["users","settings"] and not is_admin(): continue
            if st.button(label, key=f"nav_{pid}", use_container_width=True,
                         type="primary" if p==pid else "secondary"):
                st.session_state.page=pid; st.rerun()

    st.markdown("---")
    if st.button("Logout", use_container_width=True): logout()


render_header()

# ── Top Navigation ──────────────────────────────────────────
p_cur = st.session_state.get('page', 'home')
NAV_ITEMS = [
    ("Dashboard",   "home"),
    ("ISO 9001",    "iso9001"),
    ("IATF 16949",  "iatf"),
    ("Lifecycle",   "lifecycle"),
    ("Konsistensi", "consistency"),
    ("Batch",       "batch"),
    ("IQ Score",    "iqscore"),
    ("MAUNG MV3",   "maung"),
    ("What-If",     "whatif"),
    ("Hipotesis",   "hipotesis"),
    ("Wawancara",   "interview"),
    ("About",       "about"),
]
if is_admin():
    NAV_ITEMS += [("Users","users"),("Settings","settings")]

labels  = [n for n,_ in NAV_ITEMS]
pids    = [p for _,p in NAV_ITEMS]
cur_idx = pids.index(p_cur) if p_cur in pids else 0

chosen = st.radio("nav", labels, index=cur_idx, horizontal=True,
                  key="topnav", label_visibility="collapsed")
chosen_pid = pids[labels.index(chosen)]
if chosen_pid != p_cur:
    st.session_state.page = chosen_pid
    st.rerun()

# Mobile hamburger button (inside Streamlit, position fixed via CSS)
st.markdown(f"""
<style>
.hbg-wrap{{position:fixed;top:4px;right:8px;z-index:9999;}}
@media(min-width:769px){{.hbg-wrap{{display:none!important;}}}}
.hbg-wrap button{{
    background:{accent}!important;color:#000!important;
    border:none!important;border-radius:6px!important;
    width:36px!important;height:36px!important;
    font-size:1.1rem!important;font-weight:700!important;
    cursor:pointer!important;padding:0!important;
    box-shadow:0 2px 12px rgba(0,212,255,.4)!important;
}}
</style>
<div class="hbg-wrap">
  <button onclick="toggleSidebar()">&#9776;</button>
</div>
""", unsafe_allow_html=True)

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
