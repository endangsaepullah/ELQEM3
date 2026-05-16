"""
modules/pg_sitemap.py
Halaman Sitemap — navigasi visual ke semua halaman IQLE Platform
"""
import streamlit as st
from utils.auth import is_admin


def show():
    st.markdown("""
    <style>
    .sitemap-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin-top: 1rem;
    }
    .sitemap-section {
        font-size: .68rem;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #4a6fa5;
        margin: 1.5rem 0 .5rem;
        padding-bottom: .3rem;
        border-bottom: 1px solid rgba(0,212,255,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🗺️ Sitemap Platform")
    st.caption("Klik tombol di bawah untuk berpindah halaman secara langsung.")

    # ── Definisi semua halaman ─────────────────────────────
    sections = {
        "🏠 Halaman Utama": [
            ("🏠", "Dashboard Utama",       "home"),
            ("👤", "About Platform",        "about"),
            ("📚", "Teori & Referensi",     "theory"),
        ],
        "📋 Modul Standar Mutu": [
            ("📊", "ISO 9001",              "iso9001"),
            ("🏭", "IATF 16949",            "iatf"),
            ("⚙️", "Engineering Lifecycle", "lifecycle"),
        ],
        "🔬 Modul Analisis Mutu": [
            ("✅", "Konsistensi Mutu",       "consistency"),
            ("📦", "Evaluasi Batch",         "batch"),
            ("🎯", "IQ Score",              "iqscore"),
            ("🚗", "Analisis Mutu MAUNG",   "maung"),
            ("💬", "Data Wawancara",        "interview"),
        ],
        "🔑 Admin Only": [
            ("👥", "Manajemen User",        "users"),
            ("🔧", "Pengaturan Platform",   "settings"),
        ],
    }

    for section_title, pages in sections.items():
        st.markdown(f'<div class="sitemap-section">{section_title}</div>', unsafe_allow_html=True)

        cols = st.columns(3)
        for i, (emoji, label, pid) in enumerate(pages):
            # Lewati halaman admin jika bukan admin
            if pid in ("users", "settings") and not is_admin():
                continue

            active = st.session_state.get("page") == pid
            with cols[i % 3]:
                btn_type = "primary" if active else "secondary"
                if st.button(
                    f"{emoji}  {label}",
                    key=f"sitemap_{pid}",
                    use_container_width=True,
                    type=btn_type,
                    help=f"Buka halaman {label}"
                ):
                    st.session_state.page = pid
                    st.rerun()
