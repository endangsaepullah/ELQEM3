import streamlit as st
import base64
from utils.database import get_setting, get_media
from utils.styles import section_header, score_bar, category_banner, plotly_layout
from utils.auth import is_admin


DEFAULTS = {
    "profile_name":   "Endang Saefullah, ST, CLA",
    "profile_title":  "Quality Management System Engineer",
    "profile_thesis": (
        "Pengaruh ISO 9001, IATF 16949, dan Engineering Lifecycle terhadap "
        "Konsistensi Mutu Produksi Kendaraan Multifungsi Nasional PT Pindad (Persero)"
    ),
    "profile_bg": (
        "IQLE Platform (Integrated Engineering Quality Lifecycle Evaluation) dikembangkan "
        "sebagai prototype akademik berbasis Quality 4.0 untuk penelitian tesis Magister "
        "Teknik di Universitas Pertahanan RI."
    ),
    "profile_vision": (
        "Mengembangkan sistem evaluasi mutu berbasis digital untuk industri pertahanan "
        "nasional menuju kemandirian strategis."
    ),
}


def _g(key):
    return get_setting(key, DEFAULTS.get(key, ""))


def _label(text):
    return (f'<p style="font-size:.65rem;color:#4a6fa5;letter-spacing:1px;'
            f'text-transform:uppercase;margin:0 0 3px 0;">{text}</p>')


def _value(text, color="#c5d5e8"):
    return f'<p style="font-size:.85rem;color:{color};margin:0 0 .75rem 0;">{text}</p>'


def show():
    section_header("About Platform", "Profil Peneliti & Latar Belakang IQLE Platform", "👤")

    # ── Hero section ───────────────────────────────────────
    col_photo, col_info = st.columns([1, 2.5])

    with col_photo:
        pp = get_media('profile_photo')
        if pp and pp['data']:
            src = "data:" + pp['mime_type'] + ";base64," + pp['data']
            st.markdown(
                f'<div style="text-align:center;">'
                f'<img src="{src}" style="width:160px;height:160px;object-fit:cover;'
                f'border-radius:50%;border:3px solid #00d4ff;'
                f'box-shadow:0 0 30px rgba(0,212,255,0.3);display:block;margin:0 auto;">'
                f'</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center;">
                <svg width="160" height="160" viewBox="0 0 160 160" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="80" cy="80" r="80" fill="#0d1321"/>
                    <circle cx="80" cy="62" r="30" fill="#1e3a5f"/>
                    <ellipse cx="80" cy="145" rx="50" ry="35" fill="#1e3a5f"/>
                    <circle cx="80" cy="80" r="78" fill="none" stroke="#00d4ff"
                            stroke-width="2" stroke-dasharray="6 3" opacity="0.4"/>
                </svg>
                <div style="font-size:.7rem;color:#3d5470;margin-top:4px;">No Photo</div>
            </div>""", unsafe_allow_html=True)

        if is_admin():
            st.markdown("<br>", unsafe_allow_html=True)
            st.info("Upload foto di menu ⚙️ Pengaturan → Logo & Media")

    with col_info:
        name  = _g("profile_name")
        title = _g("profile_title")

        st.markdown(f"""
        <div style="padding:1.25rem 1.5rem;
                    background:linear-gradient(135deg,#0d1321,#111827);
                    border:1px solid rgba(0,212,255,0.2);
                    border-left:4px solid #00d4ff;
                    border-radius:12px; margin-bottom:.6rem;">
            <div style="font-family:Rajdhani,sans-serif;font-size:1.85rem;
                        font-weight:700;color:#e8edf5;letter-spacing:1px;
                        line-height:1.1;margin-bottom:.3rem;">{name}</div>
            <div style="font-size:.85rem;color:#00d4ff;font-weight:500;">{title}</div>
        </div>
        """, unsafe_allow_html=True)

        tags = ["Quality 4.0", "Engineering Lifecycle", "Defence Manufacturing"]
        tags_html = " ".join(
            f'<span style="display:inline-block;margin:0 4px 4px 0;'
            f'background:rgba(0,212,255,0.1);border:1px solid rgba(0,212,255,0.35);'
            f'border-radius:4px;padding:2px 10px;font-size:.72rem;color:#00d4ff;'
            f'font-family:Rajdhani;font-weight:700;letter-spacing:1px;">{t}</span>'
            for t in tags
        )
        st.markdown(f'<div style="margin-bottom:.75rem;">{tags_html}</div>',
                    unsafe_allow_html=True)

        ga, gb = st.columns(2)
        with ga:
            st.markdown(
                _label("Program Studi") + _value("Magister Teknik — S2 Defence Industry") +
                _label("S1 Industrial Engineering") +
                _value('Universitas Mercu Buana <span style="color:#00ff88;font-size:.78rem;">IPK 3.69 (2020)</span>'),
                unsafe_allow_html=True)
        with gb:
            st.markdown(
                _label("Institusi S2") + _value("Universitas Pertahanan RI (UNHAN)") +
                _label("Pengalaman Kerja") +
                _value('PT Wijaya Karya Beton <span style="color:#ffd700;font-size:.78rem;">Jan 2017 — Sekarang</span>'),
                unsafe_allow_html=True)

    st.markdown("---")

    # ── Latar belakang ─────────────────────────────────────
    st.markdown("#### Latar Belakang IQLE Platform")
    st.markdown(
        f'<div style="padding:1rem 1.25rem;background:#111827;'
        f'border:1px solid rgba(0,212,255,0.15);border-radius:10px;'
        f'font-size:.87rem;color:#c5d5e8;line-height:1.75;">'
        f'{_g("profile_bg")}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tesis ──────────────────────────────────────────────
    st.markdown("#### Keterkaitan dengan Tesis")
    t1, t2 = st.columns(2)
    with t1:
        st.markdown(
            f'<div style="padding:1rem 1.25rem;background:#111827;'
            f'border:1px solid rgba(255,215,0,0.2);border-left:3px solid #ffd700;'
            f'border-radius:8px;">'
            f'{_label("Judul Tesis")}'
            f'<p style="font-size:.85rem;color:#e8edf5;font-style:italic;margin:0;">'
            f'&ldquo;{_g("profile_thesis")}&rdquo;</p></div>',
            unsafe_allow_html=True)

    with t2:
        st.markdown(
            f'<div style="padding:1rem 1.25rem;background:#111827;'
            f'border:1px solid rgba(0,255,136,0.2);border-left:3px solid #00ff88;'
            f'border-radius:8px;">'
            f'{_label("Metode & Temuan")}'
            f'<p style="font-size:.85rem;color:#c5d5e8;margin:0;">Mixed Methods Sequential Explanatory '
            f'(PLS-SEM + Wawancara). Engineering Lifecycle terbukti dominan '
            f'(koefisien <b style="color:#00ff88;">0,532</b>, R²=0,729).</p></div>',
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # PLS-SEM bars
    results = [
        ("ISO 9001 (X1)",              0.318, "#00d4ff"),
        ("IATF 16949 (X2)",            0.217, "#0066ff"),
        ("Engineering Lifecycle (X3)", 0.532, "#00ff88"),
    ]
    rc1, rc2, rc3 = st.columns(3)
    for col, (label, coef, color) in zip([rc1,rc2,rc3], results):
        pct = int(coef/0.6*100)
        col.markdown(
            f'<div style="padding:.85rem 1rem;background:#111827;'
            f'border:1px solid {color}33;border-radius:8px;text-align:center;">'
            f'<div style="font-size:.7rem;color:#7a9bb5;margin-bottom:.4rem;">{label}</div>'
            f'<div style="font-family:Rajdhani;font-size:1.8rem;font-weight:700;color:{color};">{coef}</div>'
            f'<div style="background:#0d1321;border-radius:4px;height:5px;margin-top:.5rem;overflow:hidden;">'
            f'<div style="background:{color};height:100%;width:{pct}%;border-radius:4px;"></div></div>'
            f'<div style="font-size:.65rem;color:{color};margin-top:.3rem;">koefisien jalur</div></div>',
            unsafe_allow_html=True)

    st.markdown("---")

    # ── Sertifikasi ────────────────────────────────────────
    st.markdown("#### Sertifikasi & Keahlian")
    sk1, sk2 = st.columns(2)

    with sk1:
        skills = ["Pengembangan Sistem Manajemen Mutu","Penyusunan Prosedur & Dokumen Kerja",
                  "Audit Internal & Eksternal","Process Digitalization",
                  "Industrial Management","System Design & Engineering"]
        items = "".join(
            f'<div style="display:flex;align-items:center;gap:.6rem;padding:.35rem 0;'
            f'border-bottom:1px solid rgba(255,255,255,0.04);">'
            f'<div style="width:6px;height:6px;border-radius:50%;background:#00d4ff;flex-shrink:0;"></div>'
            f'<span style="font-size:.83rem;color:#c5d5e8;">{s}</span></div>'
            for s in skills)
        st.markdown(
            f'<div style="padding:1rem 1.25rem;background:#111827;'
            f'border:1px solid rgba(0,212,255,0.15);border-radius:10px;">'
            f'{_label("Keahlian Utama")}{items}</div>',
            unsafe_allow_html=True)

    with sk2:
        certs = [
            ("Certified Lead Auditor ISO 9001:2015 (IRCA)","#00ff88","CLA"),
            ("K3 Expert — PP 50/2012","#ffd700","K3"),
            ("ISO 37001, 27001, 45001, 14001, 17025","#00d4ff","ISO"),
        ]
        items2 = "".join(
            f'<div style="display:flex;align-items:center;gap:.6rem;padding:.35rem 0;'
            f'border-bottom:1px solid rgba(255,255,255,0.04);">'
            f'<span style="background:rgba(0,0,0,0.3);border:1px solid {c}55;border-radius:3px;'
            f'padding:1px 5px;font-size:.6rem;color:{c};font-family:Rajdhani;font-weight:700;'
            f'flex-shrink:0;">{badge}</span>'
            f'<span style="font-size:.82rem;color:#c5d5e8;">{cert}</span></div>'
            for cert,c,badge in certs)
        st.markdown(
            f'<div style="padding:1rem 1.25rem;background:#111827;'
            f'border:1px solid rgba(0,255,136,0.15);border-radius:10px;">'
            f'{_label("Sertifikasi")}{items2}</div>',
            unsafe_allow_html=True)

    st.markdown("---")

    # ── Visi ───────────────────────────────────────────────
    st.markdown("#### Visi Pengembangan")
    st.markdown(
        f'<div style="padding:1.1rem 1.4rem;'
        f'background:linear-gradient(135deg,rgba(0,212,255,0.05),rgba(0,255,136,0.05));'
        f'border:1px solid rgba(0,255,136,0.2);border-radius:10px;'
        f'font-size:.87rem;color:#c5d5e8;line-height:1.75;">'
        f'{_g("profile_vision")}</div>', unsafe_allow_html=True)
