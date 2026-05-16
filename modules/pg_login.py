import streamlit as st
from utils.auth import authenticate, get_login_logo_b64
from utils.database import get_setting


def show_login():
    accent = get_setting("ui_accent_color", "#00d4ff")
    title  = get_setting("header_title", "IQLE PLATFORM")
    org    = get_setting("header_org", "PT Pindad (Persero) · Quality 4.0")

    logo_src = get_login_logo_b64()

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@600;700&family=Inter:wght@400;500&display=swap');
    html, .stApp {{ background: #070b14 !important; }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.1, 1])

    with col:
        # Logo / icon
        if logo_src:
            st.markdown(
                '<div style="text-align:center;margin-bottom:1.25rem;">'
                f'<img src="{logo_src}" style="width:110px;height:110px;'
                'object-fit:contain;border-radius:16px;'
                f'box-shadow:0 0 40px {accent}44;border:1px solid {accent}33;">'
                '</div>', unsafe_allow_html=True)
        else:
            st.markdown(
                '<div style="text-align:center;margin-bottom:1rem;">'
                f'<div style="width:90px;height:90px;margin:0 auto;'
                f'background:linear-gradient(135deg,{accent}22,#0066ff22);'
                f'border:2px solid {accent}44;border-radius:20px;'
                'display:flex;align-items:center;justify-content:center;">'
                f'<span style="font-size:2.5rem;">⚙️</span></div></div>',
                unsafe_allow_html=True)

        # Title
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:2rem;">
            <div style="font-family:Rajdhani,sans-serif; font-size:1.9rem;
                        font-weight:700; color:{accent}; letter-spacing:4px;
                        text-shadow:0 0 20px {accent}44;">
                {title}
            </div>
            <div style="font-size:.7rem; color:#4a6fa5; letter-spacing:3px;
                        text-transform:uppercase; margin-top:4px;">
                {org}
            </div>
            <div style="width:60px; height:2px; background:linear-gradient(90deg,transparent,{accent},transparent);
                        margin:.75rem auto 0;"></div>
        </div>
        """, unsafe_allow_html=True)

        # Form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Masukkan username")
            password = st.text_input("Password", type="password", placeholder="Masukkan password")
            submitted = st.form_submit_button("LOGIN", use_container_width=True, type="primary")

            if submitted:
                if username and password:
                    user = authenticate(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user      = user
                        st.session_state.role      = user['role']
                        st.rerun()
                    else:
                        st.error("Username atau password salah.")
                else:
                    st.warning("Harap isi username dan password.")

        # Footer login
        footer1 = get_setting("footer_line1", "IQLE Platform · Prototype Akademik Magister Teknik")
        footer2 = get_setting("footer_line2", "PT Pindad (Persero) · Universitas Pertahanan RI")
        st.markdown(f"""
        <div style="text-align:center; margin-top:1.5rem;
                    font-family:Rajdhani,sans-serif; font-size:.7rem;
                    color:#3d5470; letter-spacing:1.5px; line-height:1.8;
                    text-transform:uppercase;">
            {footer1}<br>{footer2}
        </div>
        """, unsafe_allow_html=True)
