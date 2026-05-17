"""
IQLE Platform — styles.py
Centralized theme + reusable components
"""
import streamlit as st
from utils.database import get_setting


def apply_global_style():
    """Inject global CSS. Called once at app start."""
    accent = get_setting("ui_accent_color", "#00d4ff")
    bg     = get_setting("ui_bg_color",     "#070b14")

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* ── Reset & base ── */
    html, .stApp {{ background:{bg} !important; color:#e8edf5; }}
    header[data-testid="stHeader"] {{ display:none !important; }}
    .stMainBlockContainer, .block-container {{
        max-width:100% !important;
        padding-left:1.5rem !important;
        padding-right:1.5rem !important;
        padding-top:.75rem !important;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background:#0d1321 !important;
        border-right:1px solid rgba(0,212,255,.12) !important;
    }}
    [data-testid="stSidebar"] > div {{
        padding-top:.75rem !important;
    }}
    [data-testid="stSidebarCollapsedControl"] {{
        display:flex !important;
    }}

    /* ── Sidebar nav buttons ── */
    [data-testid="stSidebar"] button[kind="secondary"] {{
        background:transparent !important;
        border:none !important;
        border-left:3px solid transparent !important;
        border-radius:0 4px 4px 0 !important;
        color:#5a7a9a !important;
        font-family:Inter,sans-serif !important;
        font-size:.8rem !important;
        text-align:left !important;
        justify-content:flex-start !important;
        padding-left:.6rem !important;
        box-shadow:none !important;
        transition:all .15s !important;
    }}
    [data-testid="stSidebar"] button[kind="secondary"]:hover {{
        background:rgba(0,212,255,.05) !important;
        border-left-color:rgba(0,212,255,.35) !important;
        color:#a8c4d8 !important;
    }}
    [data-testid="stSidebar"] button[kind="primary"] {{
        background:rgba(0,212,255,.1) !important;
        border:none !important;
        border-left:3px solid {accent} !important;
        border-radius:0 4px 4px 0 !important;
        color:{accent} !important;
        font-weight:700 !important;
        font-family:Inter,sans-serif !important;
        font-size:.8rem !important;
        text-align:left !important;
        justify-content:flex-start !important;
        padding-left:.6rem !important;
        box-shadow:none !important;
    }}

    /* ── Metrics ── */
    [data-testid="metric-container"] {{
        background:#111827 !important;
        border:1px solid rgba(0,212,255,.15) !important;
        border-radius:10px !important;
        padding:1rem !important;
    }}

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {{
        background:#111827;
        border-radius:8px;
        border:1px solid rgba(0,212,255,.15);
        padding:3px; gap:3px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background:transparent;
        color:#5a7a9a;
        font-family:Rajdhani,sans-serif;
        font-weight:600;
        border-radius:6px;
    }}
    .stTabs [aria-selected="true"] {{
        background:rgba(0,212,255,.12) !important;
        color:{accent} !important;
    }}

    /* ── Inputs ── */
    .stTextInput input, .stTextArea textarea, .stSelectbox > div > div {{
        background:#111827 !important;
        border:1px solid rgba(0,212,255,.2) !important;
        border-radius:6px !important;
        color:#e8edf5 !important;
    }}

    /* ── Main buttons ── */
    .stButton > button {{
        background:rgba(0,212,255,.07);
        border:1px solid rgba(0,212,255,.3);
        color:{accent};
        font-family:Rajdhani,sans-serif;
        font-weight:600;
        letter-spacing:.5px;
        border-radius:6px;
        transition:all .2s;
    }}
    .stButton > button:hover {{
        background:rgba(0,212,255,.15);
        box-shadow:0 0 12px rgba(0,212,255,.15);
    }}
    .stButton > button[kind="primary"] {{
        background:linear-gradient(135deg,{accent},{accent}99);
        color:#000 !important;
        border:none;
        font-weight:700;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width:4px; height:4px; }}
    ::-webkit-scrollbar-thumb {{ background:rgba(0,212,255,.2); border-radius:2px; }}

    /* ── Footer buttons ── */
    div.footer-nav button {{
        background:transparent !important;
        border:none !important;
        color:#4a6fa5 !important;
        font-size:.72rem !important;
        padding:2px 4px !important;
        height:auto !important;
        box-shadow:none !important;
        font-family:Inter,sans-serif !important;
    }}
    div.footer-nav button:hover {{ color:#00d4ff !important; }}
    </style>
    """, unsafe_allow_html=True)


def render_header():
    """Platform header bar."""
    accent = get_setting("ui_accent_color", "#00d4ff")
    title  = get_setting("header_title",    "IQLE PLATFORM")
    sub    = get_setting("header_subtitle", "Integrated Engineering Quality Lifecycle Evaluation")
    org    = get_setting("header_org",      "PT Pindad (Persero) · Universitas Pertahanan RI")

    st.markdown(
        '<div style="background:linear-gradient(135deg,#0d1321,#111827);'
        f'border-left:4px solid {accent};border-bottom:1px solid {accent}22;'
        'padding:.85rem 1.5rem .75rem;margin-bottom:.75rem;">'
        f'<div style="font-family:Rajdhani,sans-serif;font-size:1.6rem;'
        f'font-weight:700;color:{accent};letter-spacing:3px;line-height:1;">⚙ {title}</div>'
        f'<div style="font-size:.72rem;color:#7a9bb5;letter-spacing:2px;'
        f'text-transform:uppercase;margin-top:2px;">{sub}</div>'
        f'<div style="font-size:.65rem;color:#4a6fa5;margin-top:1px;">{org}</div>'
        '<div style="display:flex;gap:.4rem;margin-top:.5rem;">'
        f'<span style="background:rgba(0,212,255,.1);border:1px solid rgba(0,212,255,.3);'
        f'border-radius:3px;padding:1px 8px;font-size:.6rem;color:{accent};'
        f'font-family:Rajdhani;font-weight:700;letter-spacing:1px;">QUALITY 4.0</span>'
        '<span style="background:rgba(0,255,136,.08);border:1px solid rgba(0,255,136,.3);'
        'border-radius:3px;padding:1px 8px;font-size:.6rem;color:#00ff88;'
        'font-family:Rajdhani;font-weight:700;letter-spacing:1px;">ENGINEERING LIFECYCLE</span>'
        '<span style="background:rgba(255,215,0,.08);border:1px solid rgba(255,215,0,.3);'
        'border-radius:3px;padding:1px 8px;font-size:.6rem;color:#ffd700;'
        'font-family:Rajdhani;font-weight:700;letter-spacing:1px;">PLS-SEM VALIDATED</span>'
        '</div></div>',
        unsafe_allow_html=True,
    )


def render_footer():
    """Footer with quick-nav + copyright."""
    accent = get_setting("ui_accent_color", "#00d4ff")
    year   = get_setting("footer_year", "2025")

    st.markdown(
        '<div style="margin-top:2.5rem;border-top:1px solid #21262d;'
        'padding-top:.75rem;"></div>',
        unsafe_allow_html=True,
    )

    NAV_ROWS = [
        [("home","Dashboard"),("iso9001","ISO 9001"),("iatf","IATF 16949"),
         ("lifecycle","Lifecycle"),("consistency","Konsistensi")],
        [("batch","Eval. Batch"),("iqscore","IQ Score"),("maung","MAUNG MV3"),
         ("whatif","What-If"),("hipotesis","Hipotesis")],
        [("interview","Wawancara"),("about","About"),("theory","Teori"),
         ("users","Users"),("settings","Settings")],
    ]

    st.markdown('<div class="footer-nav">', unsafe_allow_html=True)
    for row in NAV_ROWS:
        cols = st.columns(len(row))
        for col, (pid, lbl) in zip(cols, row):
            with col:
                cur = st.session_state.get("page","home")
                clr = accent if cur == pid else "#4a6fa5"
                fw  = "700"  if cur == pid else "400"
                st.markdown(
                    f'<div style="text-align:center;">'
                    f'<span style="font-size:.72rem;color:{clr};'
                    f'font-weight:{fw};">{lbl}</span></div>',
                    unsafe_allow_html=True,
                )
                if st.button(lbl, key=f"ft_{pid}",
                             use_container_width=True):
                    st.session_state.page = pid
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    col_copy, col_logout = st.columns([5, 1])
    with col_copy:
        st.markdown(
            f'<div style="padding:.35rem 0;">'
            f'<span style="font-family:Rajdhani;font-size:.68rem;color:{accent};">'
            f'IQLE Platform</span>'
            f'<span style="font-size:.62rem;color:#3d5470;"> &nbsp;·&nbsp; '
            f'PT Pindad &nbsp;·&nbsp; Universitas Pertahanan RI &nbsp;·&nbsp; © {year}'
            f'</span></div>',
            unsafe_allow_html=True,
        )
    with col_logout:
        if st.button("⏻ Logout", key="ft_logout", use_container_width=True):
            from utils.auth import logout
            logout()


# ── Reusable UI components ────────────────────────────────────

def section_header(title, subtitle=None, icon=""):
    sub_html = (
        f'<p style="font-size:.72rem;color:#4a6fa5;margin:0;'
        f'letter-spacing:2px;text-transform:uppercase;">{subtitle}</p>'
    ) if subtitle else ""
    st.markdown(
        '<div style="margin-bottom:1.25rem;padding-bottom:.75rem;'
        'border-bottom:1px solid rgba(0,212,255,.1);">'
        f'<h2 style="font-family:Rajdhani,sans-serif;font-size:1.75rem;'
        f'font-weight:700;color:#e8edf5;margin:0;letter-spacing:2px;">'
        f'{icon} {title.upper()}</h2>'
        + sub_html + '</div>',
        unsafe_allow_html=True,
    )


def score_bar(label, value, color="#00d4ff"):
    st.markdown(
        f'<div style="margin-bottom:.6rem;padding:.65rem .9rem;background:#111827;'
        f'border:1px solid {color}22;border-left:3px solid {color};border-radius:7px;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<span style="font-size:.78rem;color:#7a9bb5;">{label}</span>'
        f'<span style="font-family:Rajdhani;font-size:1.1rem;font-weight:700;'
        f'color:{color};">{value:.1f}</span></div>'
        f'<div style="background:#0d1321;border-radius:3px;height:4px;'
        f'margin-top:5px;overflow:hidden;">'
        f'<div style="background:{color};height:100%;width:{min(value,100)}%;'
        f'border-radius:3px;opacity:.8;"></div></div></div>',
        unsafe_allow_html=True,
    )


def category_banner(score, category):
    clr = {"Sangat Baik":"#00ff88","Baik":"#00d4ff",
           "Cukup":"#ffd700","Perlu Perbaikan":"#ff3366"}.get(category,"#7a9bb5")
    st.markdown(
        f'<div style="padding:.75rem 1rem;background:{clr}11;'
        f'border:1px solid {clr}44;border-radius:8px;text-align:center;">'
        f'<span style="font-size:.78rem;color:#7a9bb5;">Kategori: </span>'
        f'<span style="font-family:Rajdhani;font-size:1.1rem;font-weight:700;'
        f'color:{clr};">{category} ({score:.1f}/100)</span></div>',
        unsafe_allow_html=True,
    )


def plotly_layout():
    return dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,19,33,0.5)',
        font=dict(family='Inter', color='#7a9bb5', size=11),
        xaxis=dict(gridcolor='rgba(0,212,255,.07)',
                   linecolor='rgba(0,212,255,.15)'),
        yaxis=dict(gridcolor='rgba(0,212,255,.07)',
                   linecolor='rgba(0,212,255,.15)'),
        margin=dict(l=40, r=20, t=45, b=40),
        legend=dict(bgcolor='rgba(0,0,0,0)',
                    bordercolor='rgba(0,212,255,.15)', borderwidth=1),
    )
