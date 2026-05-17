import streamlit as st
from utils.database import get_setting


def apply_global_style():
    accent = get_setting("ui_accent_color", "#00d4ff")
    bg     = get_setting("ui_bg_color",     "#070b14")
    bg2    = get_setting("ui_bg2_color",    "#0d1321")

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
    :root {{
        --accent:{accent}; --bg:{bg}; --bg2:{bg2}; --bg3:#111827;
        --text:#e8edf5; --muted:#7a9bb5; --dim:#3d5470;
        --border:rgba(0,212,255,0.15); --border2:rgba(0,212,255,0.30);
        --green:#00ff88; --yellow:#ffd700; --red:#ff3366;
    }}
    html,.stApp {{ background:var(--bg) !important; font-family:'Inter',sans-serif; color:var(--text); }}
    header[data-testid="stHeader"] {{ display:none !important; }}
    .stMainBlockContainer {{ padding-top:0 !important; }}
    [data-testid="stSidebar"] {{ background:var(--bg2) !important; border-right:1px solid var(--border); }}
    [data-testid="stSidebarCollapsedControl"] {{ display:none !important; }}
    section[data-testid="stSidebar"]>div {{ min-width:var(--sb-w,255px) !important; max-width:var(--sb-w,255px) !important; transition:.25s; }}
    h1,h2,h3,h4 {{ font-family:'Rajdhani',sans-serif !important; letter-spacing:1px; color:var(--text) !important; }}
    [data-testid="metric-container"] {{ background:var(--bg3) !important; border:1px solid var(--border) !important; border-radius:10px !important; padding:1rem !important; }}
    [data-testid="stMetricValue"] {{ font-family:'Rajdhani',sans-serif !important; font-size:1.8rem !important; }}
    .stTabs [data-baseweb="tab-list"] {{ background:var(--bg2); border-radius:8px; border:1px solid var(--border); padding:4px; gap:4px; }}
    .stTabs [data-baseweb="tab"] {{ background:transparent; color:var(--muted); font-family:'Rajdhani',sans-serif; font-weight:600; letter-spacing:1px; border-radius:6px; }}
    .stTabs [aria-selected="true"] {{ background:rgba(0,212,255,0.12) !important; color:var(--accent) !important; }}
    .stButton>button {{ background:rgba(0,212,255,0.07); border:1px solid rgba(0,212,255,0.3); color:var(--accent); font-family:'Rajdhani',sans-serif; font-weight:600; letter-spacing:1px; border-radius:6px; transition:all .2s; }}
    .stButton>button:hover {{ background:rgba(0,212,255,0.15); box-shadow:0 0 14px rgba(0,212,255,0.18); }}
    .stButton>button[kind="primary"] {{ background:linear-gradient(135deg,var(--accent),#0066ff); color:#000 !important; border:none; font-weight:700; }}
    .stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div {{
        background:var(--bg2) !important; border:1px solid var(--border) !important; border-radius:6px !important; color:var(--text) !important; }}
    .streamlit-expanderHeader {{ background:var(--bg3) !important; border:1px solid var(--border) !important; border-radius:8px !important; color:var(--accent) !important; font-family:'Rajdhani',sans-serif !important; font-weight:600 !important; }}
    hr {{ border-color:var(--border) !important; }}
    ::-webkit-scrollbar {{ width:4px; height:4px; }}
    ::-webkit-scrollbar-thumb {{ background:rgba(0,212,255,0.25); border-radius:2px; }}
    @media(max-width:768px) {{
        [data-testid="stSidebar"] {{ display:none !important; }}
        .stMainBlockContainer {{ padding:.5rem !important; }}
    }}
    </style>
    """, unsafe_allow_html=True)


def render_topnav():
    """
    Renders a slim fixed top navbar with user greeting + logout button.
    Must be called ONCE per page, before render_header().
    The logout button uses a hidden Streamlit button trick via JS click.
    """
    accent = get_setting("ui_accent_color", "#00d4ff")
    user   = st.session_state.get('user', {})
    role   = st.session_state.get('role', 'viewer')

    uname  = user.get('full_name') or user.get('username', 'User')
    role_label = "ADMIN" if role == "admin" else "USER"
    role_color = accent if role == "admin" else "#ffd700"

    # Inject CSS: push all content down so navbar doesn't overlap
    st.markdown("""
    <style>
    .iqle-topnav {
        position: fixed;
        top: 0; left: 0; right: 0;
        height: 40px;
        z-index: 9999;
        background: #080c17;
        border-bottom: 1px solid rgba(0,212,255,0.18);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 1.25rem;
        font-family: 'Rajdhani', sans-serif;
        backdrop-filter: blur(8px);
    }
    .iqle-topnav-left {
        display: flex;
        align-items: center;
        gap: .6rem;
    }
    .iqle-topnav-logo {
        font-size: .75rem;
        font-weight: 700;
        letter-spacing: 2px;
        color: var(--accent, #00d4ff);
        opacity: .7;
    }
    .iqle-topnav-sep {
        width: 1px; height: 16px;
        background: rgba(0,212,255,0.2);
    }
    .iqle-topnav-greeting {
        font-size: .72rem;
        color: #7a9bb5;
        letter-spacing: .5px;
    }
    .iqle-topnav-greeting strong {
        color: #e8edf5;
        font-weight: 600;
    }
    .iqle-topnav-right {
        display: flex;
        align-items: center;
        gap: .75rem;
    }
    .iqle-role-badge {
        font-size: .58rem;
        font-weight: 700;
        letter-spacing: 1px;
        padding: 2px 7px;
        border-radius: 3px;
        border: 1px solid;
    }
    /* Logout button styling - targets the hidden streamlit button */
    div[data-testid="stButton"].iqle-logout-btn > button {
        background: rgba(255,51,102,0.08) !important;
        border: 1px solid rgba(255,51,102,0.35) !important;
        color: #ff3366 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-size: .65rem !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        padding: 2px 12px !important;
        height: 26px !important;
        line-height: 1 !important;
        border-radius: 4px !important;
        cursor: pointer !important;
        transition: all .2s !important;
    }
    div[data-testid="stButton"].iqle-logout-btn > button:hover {
        background: rgba(255,51,102,0.18) !important;
        box-shadow: 0 0 10px rgba(255,51,102,0.2) !important;
    }
    /* Push main content below the navbar */
    .stMainBlockContainer, .block-container {
        padding-top: 52px !important;
        margin-top: 0 !important;
    }
    /* Also push sidebar content down */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 52px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # HTML navbar (visual only - logo + greeting + role badge)
    st.markdown(f"""
    <div class="iqle-topnav">
        <div class="iqle-topnav-left">
            <span class="iqle-topnav-logo">⚙ IQLE</span>
            <div class="iqle-topnav-sep"></div>
            <span class="iqle-topnav-greeting">
                Selamat datang, <strong>{uname}</strong>
            </span>
            <span class="iqle-role-badge"
                  style="color:{role_color};border-color:{role_color}44;">
                {role_label}
            </span>
        </div>
        <div class="iqle-topnav-right" id="iqle-logout-slot">
            <!-- logout button will be injected by Streamlit below -->
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Invisible container for the logout button, positioned into the navbar via CSS
    st.markdown("""
    <style>
    /* Float the logout button container up into the fixed navbar */
    div[data-testid="stVerticalBlock"]:has(> div[data-testid="stButton"].iqle-logout-btn) {
        position: fixed !important;
        top: 7px !important;
        right: 1.25rem !important;
        z-index: 10000 !important;
        width: auto !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Actual Streamlit logout button (gets hoisted visually into navbar)
    col = st.container()
    with col:
        # We use a unique key and inject the class via markdown trick
        st.markdown('<div class="iqle-logout-btn">', unsafe_allow_html=True)
        if st.button("⏻  LOGOUT", key="topnav_logout_btn"):
            from utils.auth import logout
            logout()
        st.markdown('</div>', unsafe_allow_html=True)


def render_header():
    title  = get_setting("header_title",    "IQLE PLATFORM")
    sub    = get_setting("header_subtitle", "Integrated Engineering Quality Lifecycle Evaluation")
    org    = get_setting("header_org",      "PT Pindad (Persero) · Universitas Pertahanan RI")
    badge  = get_setting("header_show_badge","true")
    accent = get_setting("ui_accent_color", "#00d4ff")

    badge_html = ""
    if badge == "true":
        badge_html = (
            '<div style="display:flex;gap:.5rem;flex-wrap:wrap;margin-top:.6rem;">'
            f'<span style="background:rgba(0,212,255,.12);border:1px solid rgba(0,212,255,.3);border-radius:4px;padding:2px 10px;font-size:.62rem;color:{accent};font-family:Rajdhani;font-weight:700;letter-spacing:1.5px;">QUALITY 4.0</span>'
            '<span style="background:rgba(0,255,136,.1);border:1px solid rgba(0,255,136,.3);border-radius:4px;padding:2px 10px;font-size:.62rem;color:#00ff88;font-family:Rajdhani;font-weight:700;letter-spacing:1.5px;">ENGINEERING LIFECYCLE</span>'
            '<span style="background:rgba(255,215,0,.1);border:1px solid rgba(255,215,0,.3);border-radius:4px;padding:2px 10px;font-size:.62rem;color:#ffd700;font-family:Rajdhani;font-weight:700;letter-spacing:1.5px;">PLS-SEM VALIDATED</span>'
            '</div>'
        )

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0d1321,#111827);'
        f'border-bottom:2px solid {accent}33;padding:1.25rem 2rem 1rem;margin-bottom:.5rem;'
        'position:relative;overflow:hidden;">'
        f'<div style="position:absolute;left:0;top:0;bottom:0;width:4px;background:linear-gradient(180deg,{accent},#0066ff);"></div>'
        '<div style="padding-left:.5rem;">'
        f'<div style="font-family:Rajdhani,sans-serif;font-size:1.7rem;font-weight:700;color:{accent};letter-spacing:3px;line-height:1;margin-bottom:.15rem;">⚙️ {title}</div>'
        f'<div style="font-size:.78rem;color:#7a9bb5;letter-spacing:2px;text-transform:uppercase;margin-bottom:.1rem;">{sub}</div>'
        f'<div style="font-size:.68rem;color:#4a6fa5;letter-spacing:1px;">{org}</div>'
        + badge_html +
        '</div></div>',
        unsafe_allow_html=True
    )


def render_footer():
    import streamlit as st
    accent = get_setting("ui_accent_color", "#00d4ff")
    year   = get_setting("footer_year", "2025")

    cols = [
        ("Modul Evaluasi", [
            "Dashboard Utama", "ISO 9001", "IATF 16949",
            "Engineering Lifecycle", "Konsistensi Mutu", "Evaluasi Batch",
        ]),
        ("Analisis & Laporan", [
            "Integrated Quality Score", "Analisis Mutu MAUNG MV3",
            "Simulasi What-If", "Kesimpulan & Hipotesis", "Data Wawancara",
        ]),
        ("Platform", [
            "About Platform", "Teori & Referensi",
            "Manajemen User", "Pengaturan Platform",
        ]),
        ("Tentang", [
            "Endang Saefullah, ST, CLA",
            "Universitas Pertahanan RI",
            "PT Pindad (Persero)",
            "Magister Teknik Industri Pertahanan",
        ]),
    ]

    col_divs = ""
    for title, items in cols:
        rows = "".join(f'<div style="padding:2px 0;color:#4a6fa5;font-size:.71rem;">{i}</div>' for i in items)
        col_divs += (
            '<div style="min-width:0;">'
            '<div style="font-family:Rajdhani,sans-serif;font-size:.6rem;font-weight:700;'
            'color:' + accent + ';letter-spacing:2px;text-transform:uppercase;'
            'margin-bottom:.5rem;padding-bottom:.3rem;'
            'border-bottom:1px solid #21262d;">' + title + '</div>'
            + rows + '</div>'
        )

    html = (
        '<div style="margin-top:3rem;background:#0a0e1a;border-top:1px solid #21262d;'
        'padding:1.5rem 2rem 0;">'
        '<div style="display:grid;grid-template-columns:repeat(4,1fr);'
        'gap:1.5rem;margin-bottom:1.25rem;">'
        + col_divs +
        '</div>'
        '<div style="border-top:1px solid #21262d;padding:.65rem 0;'
        'display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:.35rem;">'
        '<span style="font-family:Rajdhani,sans-serif;font-size:.68rem;'
        'color:' + accent + ';font-weight:600;letter-spacing:1px;">'
        'IQLE Platform &nbsp;&middot;&nbsp; Quality 4.0 Dashboard'
        '</span>'
        '<span style="font-size:.62rem;color:#3d5470;font-family:Rajdhani;">'
        'PT Pindad &nbsp;&middot;&nbsp; Universitas Pertahanan RI'
        ' &nbsp;&middot;&nbsp; &copy; ' + year + '</span>'
        '</div></div>'
    )
    st.markdown(html, unsafe_allow_html=True)


def section_header(title, subtitle=None, icon=""):
    sub = (f'<p style="font-size:.75rem;color:#4a6fa5;margin:0;letter-spacing:2px;text-transform:uppercase;">{subtitle}</p>') if subtitle else ""
    st.markdown(
        '<div style="margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:1px solid rgba(0,212,255,0.12);">'
        f'<h2 style="font-family:Rajdhani,sans-serif;font-size:1.8rem;font-weight:700;color:#e8edf5;margin:0;letter-spacing:2px;">{icon} {title.upper()}</h2>'
        + sub + '</div>',
        unsafe_allow_html=True
    )


def score_bar(label, value, color="#00d4ff"):
    st.markdown(
        f'<div style="margin-bottom:.7rem;padding:.75rem 1rem;background:#111827;'
        f'border:1px solid {color}22;border-left:3px solid {color};border-radius:8px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="font-size:.8rem;color:#7a9bb5;">{label}</span>'
        f'<span style="font-family:Rajdhani,sans-serif;font-size:1.15rem;font-weight:700;color:{color};">{value:.1f}</span>'
        f'</div>'
        f'<div style="background:#0d1321;border-radius:4px;height:5px;margin-top:6px;overflow:hidden;">'
        f'<div style="background:{color};height:100%;width:{value}%;border-radius:4px;opacity:.85;"></div></div></div>',
        unsafe_allow_html=True
    )


def category_banner(score, category):
    colors = {"Sangat Baik":"#00ff88","Baik":"#00d4ff","Cukup":"#ffd700","Perlu Perbaikan":"#ff3366"}
    c = colors.get(category, "#7a9bb5")
    st.markdown(
        f'<div style="padding:.85rem 1.25rem;background:{c}11;border:1px solid {c}44;border-radius:8px;text-align:center;margin-top:.5rem;">'
        f'<span style="font-size:.8rem;color:#7a9bb5;">Kategori: </span>'
        f'<span style="font-family:Rajdhani;font-size:1.15rem;font-weight:700;color:{c};">{category} ({score:.1f}/100)</span></div>',
        unsafe_allow_html=True
    )


def plotly_layout():
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,19,33,0.5)',
        font=dict(family='Inter', color='#7a9bb5', size=11),
        xaxis=dict(gridcolor='rgba(0,212,255,0.07)', linecolor='rgba(0,212,255,0.15)'),
        yaxis=dict(gridcolor='rgba(0,212,255,0.07)', linecolor='rgba(0,212,255,0.15)'),
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,212,255,0.15)', borderwidth=1),
    )
