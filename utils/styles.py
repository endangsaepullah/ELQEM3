import streamlit as st
from utils.database import get_setting


# ── Global CSS ─────────────────────────────────────────────
def apply_global_style():
    accent = get_setting("ui_accent_color", "#00d4ff")
    bg     = get_setting("ui_bg_color",     "#070b14")
    bg2    = get_setting("ui_bg2_color",    "#0d1321")

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {{
        --accent:  {accent};
        --bg:      {bg};
        --bg2:     {bg2};
        --bg3:     #111827;
        --text:    #e8edf5;
        --muted:   #7a9bb5;
        --dim:     #3d5470;
        --border:  rgba(0,212,255,0.15);
        --border2: rgba(0,212,255,0.30);
        --green:   #00ff88;
        --yellow:  #ffd700;
        --orange:  #ff6b35;
        --red:     #ff3366;
        --purple:  #a78bfa;
    }}

    html, .stApp {{
        background: var(--bg) !important;
        font-family: 'Inter', sans-serif;
        color: var(--text);
    }}

    /* Hide default Streamlit header */
    header[data-testid="stHeader"] {{ display: none !important; }}
    .stMainBlockContainer {{ padding-top: 0 !important; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--bg2) !important;
        border-right: 1px solid var(--border);
    }}

    /* Typography */
    h1,h2,h3,h4 {{
        font-family: 'Rajdhani', sans-serif !important;
        letter-spacing: 1px;
        color: var(--text) !important;
    }}

    /* Metrics */
    [data-testid="metric-container"] {{
        background: var(--bg3) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        transition: all 0.2s;
    }}
    [data-testid="metric-container"]:hover {{
        border-color: var(--border2) !important;
        box-shadow: 0 0 20px rgba(0,212,255,0.08) !important;
    }}
    [data-testid="stMetricValue"] {{
        font-family: 'Rajdhani', sans-serif !important;
        font-size: 1.8rem !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--bg2);
        border-radius: 8px;
        border: 1px solid var(--border);
        padding: 4px; gap: 4px;
    }}
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        color: var(--muted);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600; letter-spacing: 1px;
        border-radius: 6px;
    }}
    .stTabs [aria-selected="true"] {{
        background: rgba(0,212,255,0.12) !important;
        color: var(--accent) !important;
    }}

    /* Buttons */
    .stButton > button {{
        background: rgba(0,212,255,0.07);
        border: 1px solid rgba(0,212,255,0.35);
        color: var(--accent);
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600; letter-spacing: 1px;
        border-radius: 6px;
        transition: all 0.2s;
    }}
    .stButton > button:hover {{
        background: rgba(0,212,255,0.18);
        box-shadow: 0 0 16px rgba(0,212,255,0.2);
        transform: translateY(-1px);
    }}
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, var(--accent), #0066ff);
        color: #000 !important;
        border: none; font-weight: 700;
    }}

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div {{
        background: var(--bg2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text) !important;
    }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: var(--bg3) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        color: var(--accent) !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 600 !important;
    }}

    /* Dataframe */
    .stDataFrame {{ border: 1px solid var(--border); border-radius: 8px; }}

    /* Divider */
    hr {{ border-color: var(--border) !important; }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 5px; height: 5px; }}
    ::-webkit-scrollbar-track {{ background: var(--bg); }}
    ::-webkit-scrollbar-thumb {{ background: rgba(0,212,255,0.3); border-radius: 3px; }}

    /* Custom alert boxes */
    .alert-info {{
        padding: .75rem 1rem; border-radius: 8px; margin-bottom: .75rem;
        background: rgba(0,212,255,.08); border: 1px solid rgba(0,212,255,.3);
        color: #c5d5e8; font-size: .85rem; line-height: 1.6;
    }}
    .alert-warn {{
        padding: .75rem 1rem; border-radius: 8px; margin-bottom: .75rem;
        background: rgba(255,215,0,.08); border: 1px solid rgba(255,215,0,.3);
        color: #e8d5a0; font-size: .85rem;
    }}
    .alert-success {{
        padding: .75rem 1rem; border-radius: 8px; margin-bottom: .75rem;
        background: rgba(0,255,136,.08); border: 1px solid rgba(0,255,136,.3);
        color: #a0e8c0; font-size: .85rem;
    }}
    </style>
    """, unsafe_allow_html=True)


# ── Header ─────────────────────────────────────────────────
def render_header():
    title      = get_setting("header_title",    "IQLE PLATFORM")
    subtitle   = get_setting("header_subtitle", "Integrated Engineering Quality Lifecycle Evaluation")
    org        = get_setting("header_org",      "PT Pindad (Persero) · Universitas Pertahanan RI")
    show_badge = get_setting("header_show_badge", "true")
    accent     = get_setting("ui_accent_color", "#00d4ff")

    badge_html = ""
    if show_badge == "true":
        badge_html = f"""
        <div style="display:flex; gap:.5rem; flex-wrap:wrap; margin-top:.75rem;">
            <span style="background:rgba(0,212,255,.12); border:1px solid rgba(0,212,255,.3);
                         border-radius:4px; padding:2px 10px; font-size:.65rem;
                         color:{accent}; font-family:Rajdhani; font-weight:700; letter-spacing:1.5px;">
                QUALITY 4.0
            </span>
            <span style="background:rgba(0,255,136,.1); border:1px solid rgba(0,255,136,.3);
                         border-radius:4px; padding:2px 10px; font-size:.65rem;
                         color:#00ff88; font-family:Rajdhani; font-weight:700; letter-spacing:1.5px;">
                ENGINEERING LIFECYCLE
            </span>
            <span style="background:rgba(255,215,0,.1); border:1px solid rgba(255,215,0,.3);
                         border-radius:4px; padding:2px 10px; font-size:.65rem;
                         color:#ffd700; font-family:Rajdhani; font-weight:700; letter-spacing:1.5px;">
                PLS-SEM VALIDATED
            </span>
        </div>
        """

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #0d1321 0%, #111827 100%);
                border-bottom:2px solid {accent}33;
                padding:1.25rem 2rem 1rem; margin-bottom:1.5rem;
                position:relative; overflow:hidden;">

        <!-- Decorative grid lines -->
        <div style="position:absolute; top:0; left:0; right:0; bottom:0;
                    background-image: linear-gradient(rgba(0,212,255,0.03) 1px, transparent 1px),
                                      linear-gradient(90deg, rgba(0,212,255,0.03) 1px, transparent 1px);
                    background-size: 30px 30px; pointer-events:none;"></div>

        <!-- Accent bar left -->
        <div style="position:absolute; left:0; top:0; bottom:0; width:4px;
                    background:linear-gradient(180deg, {accent}, #0066ff);"></div>

        <div style="padding-left:.5rem;">
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.7rem; font-weight:700;
                        color:{accent}; letter-spacing:3px; line-height:1; margin-bottom:.15rem;">
                ⚙️ {title}
            </div>
            <div style="font-size:.8rem; color:#7a9bb5; letter-spacing:2px;
                        text-transform:uppercase; margin-bottom:.1rem;">
                {subtitle}
            </div>
            <div style="font-size:.7rem; color:#4a6fa5; letter-spacing:1px;">
                {org}
            </div>
            {badge_html}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────
def render_footer():
    line1 = get_setting("footer_line1", "IQLE Platform · Prototype Akademik Magister Teknik")
    line2 = get_setting("footer_line2", "PT Pindad (Persero) · Universitas Pertahanan RI · Quality 4.0")
    year  = get_setting("footer_year",  "2025")
    accent= get_setting("ui_accent_color", "#00d4ff")

    st.markdown(f"""
    <div style="margin-top:3rem; padding:1.25rem 2rem;
                background:#0d1321; border-top:1px solid rgba(0,212,255,0.12);">
        <div style="display:flex; justify-content:space-between; align-items:center;
                    flex-wrap:wrap; gap:.5rem;">
            <div>
                <div style="font-family:'Rajdhani',sans-serif; font-size:.8rem;
                            color:{accent}; letter-spacing:2px; font-weight:600;">
                    {line1}
                </div>
                <div style="font-size:.7rem; color:#3d5470; margin-top:.15rem;
                            letter-spacing:1px;">
                    {line2}
                </div>
            </div>
            <div style="font-size:.7rem; color:#3d5470; text-align:right;">
                <div style="font-family:'JetBrains Mono',monospace; color:#4a6fa5;">
                    v2.0 · Railway · PostgreSQL
                </div>
                <div>&copy; {year} · All Rights Reserved</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── Page Header ────────────────────────────────────────────
def section_header(title, subtitle=None, icon=""):
    sub = (f'<p style="font-size:.78rem;color:#4a6fa5;margin:0;letter-spacing:2px;'
           f'text-transform:uppercase;">{subtitle}</p>') if subtitle else ""
    st.markdown(f"""
    <div style="margin-bottom:1.5rem; padding-bottom:1rem;
                border-bottom:1px solid rgba(0,212,255,0.12);">
        <h2 style="font-family:Rajdhani,sans-serif; font-size:1.8rem; font-weight:700;
                   color:#e8edf5; margin:0; letter-spacing:2px;">
            {icon} {title.upper()}
        </h2>
        {sub}
    </div>
    """, unsafe_allow_html=True)


# ── Score bar ──────────────────────────────────────────────
def score_bar(label, value, color="#00d4ff"):
    st.markdown(f"""
    <div style="margin-bottom:.7rem; padding:.75rem 1rem;
                background:#111827; border:1px solid {color}22;
                border-left:3px solid {color}; border-radius:8px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:.8rem; color:#7a9bb5;">{label}</span>
            <span style="font-family:Rajdhani,sans-serif; font-size:1.15rem;
                         font-weight:700; color:{color};">{value:.1f}</span>
        </div>
        <div style="background:#0d1321; border-radius:4px; height:5px; margin-top:6px; overflow:hidden;">
            <div style="background:{color}; height:100%; width:{value}%; border-radius:4px; opacity:.85;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def category_banner(score, category):
    colors = {"Sangat Baik":"#00ff88","Baik":"#00d4ff","Cukup":"#ffd700","Perlu Perbaikan":"#ff3366"}
    c = colors.get(category, "#7a9bb5")
    st.markdown(f"""
    <div style="padding:.85rem 1.25rem; background:{c}11; border:1px solid {c}44;
                border-radius:8px; text-align:center; margin-top:.5rem;">
        <span style="font-size:.8rem; color:#7a9bb5;">Kategori: </span>
        <span style="font-family:Rajdhani; font-size:1.15rem; font-weight:700; color:{c};">
            {category} ({score:.1f}/100)
        </span>
    </div>
    """, unsafe_allow_html=True)


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
