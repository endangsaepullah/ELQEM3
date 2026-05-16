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

# Hamburger + nav CSS
st.markdown(f"""
<style>
.sb-tog-btn {{
    display:none; position:fixed; top:10px; left:10px; z-index:9999;
    background:{accent}; color:#000; border:none; border-radius:5px;
    padding:5px 10px; cursor:pointer; font-size:1.1rem; font-weight:700;
    box-shadow:0 2px 12px rgba(0,212,255,0.35);
}}
.sb-overlay {{ display:none; position:fixed; inset:0; background:rgba(0,0,0,0.65); z-index:998; backdrop-filter:blur(2px); }}
@media(max-width:768px) {{
    .sb-tog-btn {{ display:block !important; }}
    [data-testid="stSidebar"] {{ position:fixed !important; z-index:999 !important; transform:translateX(-110%) !important; transition:transform .25s !important; height:100vh !important; top:0 !important; left:0 !important; min-width:260px !important; max-width:260px !important; box-shadow:4px 0 24px rgba(0,0,0,0.6) !important; }}
    [data-testid="stSidebar"].sb-open {{ transform:translateX(0) !important; }}
    .sb-overlay.sb-open {{ display:block; }}
    .stMainBlockContainer {{ padding:.5rem !important; margin-left:0 !important; }}
}}
.top-navbar {{ background:#0a0e1a; border-bottom:1px solid rgba(0,212,255,0.12); padding:.4rem 1rem; display:flex; gap:.25rem; flex-wrap:wrap; align-items:center; position:sticky; top:0; z-index:100; overflow-x:auto; }}
.nav-pill {{ font-family:Rajdhani,sans-serif; font-size:.7rem; font-weight:600; letter-spacing:.8px; text-transform:uppercase; padding:.22rem .65rem; border-radius:4px; border:1px solid rgba(255,255,255,0.07); color:#4a6fa5; background:transparent; white-space:nowrap; display:inline-block; }}
.nav-pill.active {{ color:#000 !important; font-weight:700; background:{accent}; border-color:{accent}; }}
</style>
<button class="sb-tog-btn" onclick="(function(){{var s=document.querySelector('[data-testid=stSidebar]'),o=document.getElementById('sbo');s.classList.toggle('sb-open');o.classList.toggle('sb-open');}})()">&#9776;</button>
<div class="sb-overlay" id="sbo" onclick="(function(){{var s=document.querySelector('[data-testid=stSidebar]'),o=document.getElementById('sbo');s.classList.remove('sb-open');o.classList.remove('sb-open');}})()"></div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if 'sb_wide' not in st.session_state:
        st.session_state.sb_wide = True
    wide = st.session_state.sb_wide
    sb_w = 255 if wide else 72
    st.markdown(f'<style>section[data-testid="stSidebar"]>div{{min-width:{sb_w}px!important;max-width:{sb_w}px!important;}}</style>', unsafe_allow_html=True)

    c1, c2 = st.columns([1,3])
    with c1:
        if st.button("◀" if wide else "▶", key="sb_tog"):
            st.session_state.sb_wide = not wide; st.rerun()
    with c2:
        if wide:
            st.markdown('<span style="font-size:.6rem;color:#3d5470;letter-spacing:1px;">CIUTKAN</span>', unsafe_allow_html=True)

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
        ICONS={"home":"⌂","iso9001":"①","iatf":"②","lifecycle":"③","consistency":"④","batch":"⑤","iqscore":"⑥","maung":"⑦","whatif":"⑧","hipotesis":"⑨","interview":"⑩","about":"◉","theory":"◎","users":"◈","settings":"◇"}
        for pid,label in [(p,l) for p,l in MENU if p]:
            if pid in ["users","settings"] and not is_admin(): continue
            if st.button(ICONS.get(pid,"·"), key=f"sbc_{pid}", use_container_width=True, help=label, type="primary" if st.session_state.page==pid else "secondary"):
                st.session_state.page=pid; st.rerun()
    else:
        st.markdown(f'<div style="padding:.4rem 0 .6rem;text-align:center;"><div style="font-family:Rajdhani;font-size:1rem;font-weight:700;color:{accent};letter-spacing:2px;">IQLE PLATFORM</div><div style="font-size:.58rem;color:#3d5470;letter-spacing:2px;text-transform:uppercase;">PT Pindad</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="padding:.4rem .7rem;margin-bottom:.5rem;background:rgba(0,212,255,0.04);border:1px solid rgba(0,212,255,0.12);border-radius:7px;"><div style="font-size:.58rem;color:#3d5470;text-transform:uppercase;letter-spacing:1px;">Logged in as</div><div style="font-family:Rajdhani;font-size:.88rem;font-weight:600;color:#e8edf5;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{user.get("full_name") or user.get("username","")}</div><div style="font-size:.6rem;color:{"#00d4ff" if role=="admin" else "#ffd700"};text-transform:uppercase;">{"ADMIN" if role=="admin" else "VIEWER"}</div></div>', unsafe_allow_html=True)

        p = st.session_state.page
        for pid,label in MENU:
            if pid is None:
                st.markdown(f'<div style="font-size:.58rem;color:#2a3f55;letter-spacing:2px;text-transform:uppercase;padding:.3rem .2rem .1rem;font-family:Rajdhani;">{label}</div>', unsafe_allow_html=True)
                continue
            if pid in ["users","settings"] and not is_admin(): continue
            if st.button(label, key=f"nav_{pid}", use_container_width=True, type="primary" if p==pid else "secondary"):
                st.session_state.page=pid; st.rerun()

    st.markdown("---")
    if st.button("Logout", use_container_width=True): logout()

# Top navbar pills
p_cur = st.session_state.page
NAV = [("Dashboard","home"),("ISO 9001","iso9001"),("IATF 16949","iatf"),
       ("Lifecycle","lifecycle"),("Konsistensi","consistency"),("Batch","batch"),
       ("IQ Score","iqscore"),("MAUNG MV3","maung"),("What-If","whatif"),
       ("Hipotesis","hipotesis"),("Wawancara","interview"),("About","about")]

pills = "".join(f'<span class="nav-pill{" active" if p_cur==pid else ""}">{name}</span>' for name,pid in NAV)
st.markdown(f'<div class="top-navbar">{pills}</div>', unsafe_allow_html=True)

# Invisible functional buttons
nav_cols = st.columns(len(NAV))
for i,(name,pid) in enumerate(NAV):
    with nav_cols[i]:
        st.markdown('<div style="margin-top:-2.6rem;height:2.2rem;overflow:hidden;">', unsafe_allow_html=True)
        if st.button(name, key=f"tnav_{pid}", use_container_width=True):
            st.session_state.page=pid; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

render_header()

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
