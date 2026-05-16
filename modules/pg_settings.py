import streamlit as st
import base64
from utils.database import get_setting, set_setting, get_media, save_media, delete_media, get_pls, set_pls
from utils.styles import section_header, score_bar, category_banner, plotly_layout
from utils.auth import require_admin, save_login_logo, delete_login_logo, get_login_logo_b64


def show():
    require_admin()
    section_header("Pengaturan Platform", "Kustomisasi Tampilan & Konten", "⚙️")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎨 Tampilan & Warna",
        "🔤 Header & Footer",
        "🖼️ Logo & Media",
        "👤 Profil Peneliti",
        "📊 PLS-SEM Input",
    ])

    # ── Tab 1: Tampilan ────────────────────────────────────
    with tab1:
        st.markdown("#### 🎨 Kustomisasi Warna & Tema")
        st.info("Perubahan warna akan aktif setelah refresh halaman.")

        c1, c2, c3 = st.columns(3)
        with c1:
            accent = st.color_picker("Warna Aksen Utama",
                                     get_setting("ui_accent_color","#00d4ff"))
        with c2:
            bg = st.color_picker("Background Utama",
                                  get_setting("ui_bg_color","#070b14"))
        with c3:
            bg2 = st.color_picker("Background Sekunder",
                                   get_setting("ui_bg2_color","#0d1321"))

        # Preview
        st.markdown(f"""
        <div style="padding:1rem 1.5rem; border-radius:10px; margin:1rem 0;
                    background:{bg}; border:2px solid {accent}44;">
            <div style="font-family:Rajdhani; font-size:1.2rem; color:{accent};
                        letter-spacing:2px; font-weight:700;">PREVIEW TEMA</div>
            <div style="background:{bg2}; padding:.5rem .75rem; border-radius:6px;
                        margin-top:.5rem; border:1px solid {accent}22;">
                <span style="color:{accent}; font-size:.8rem;">Contoh card dengan warna aksen</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("💾 Simpan Pengaturan Warna", type="primary", use_container_width=True):
            set_setting("ui_accent_color", accent)
            set_setting("ui_bg_color",     bg)
            set_setting("ui_bg2_color",    bg2)
            st.success("✅ Warna tersimpan! Refresh untuk melihat perubahan.")

    # ── Tab 2: Header & Footer ─────────────────────────────
    with tab2:
        st.markdown("#### 🔤 Kustomisasi Header")

        with st.form("header_form"):
            h_title = st.text_input("Judul Utama (Header)",
                                     get_setting("header_title", "IQLE PLATFORM"))
            h_sub   = st.text_input("Subjudul Header",
                                     get_setting("header_subtitle",
                                                 "Integrated Engineering Quality Lifecycle Evaluation"))
            h_org   = st.text_input("Organisasi / Institusi",
                                     get_setting("header_org",
                                                 "PT Pindad (Persero) · Universitas Pertahanan RI"))
            h_badge = st.selectbox("Tampilkan Badge (Quality 4.0 dll)",
                                   ["true", "false"],
                                   index=0 if get_setting("header_show_badge","true")=="true" else 1)
            if st.form_submit_button("💾 Simpan Header", use_container_width=True, type="primary"):
                set_setting("header_title",      h_title)
                set_setting("header_subtitle",   h_sub)
                set_setting("header_org",        h_org)
                set_setting("header_show_badge", h_badge)
                st.success("✅ Header tersimpan!")
                st.rerun()

        st.markdown("#### 🔤 Kustomisasi Footer")
        with st.form("footer_form"):
            f1 = st.text_input("Baris 1 Footer",
                                get_setting("footer_line1",
                                            "IQLE Platform · Prototype Akademik Magister Teknik"))
            f2 = st.text_input("Baris 2 Footer",
                                get_setting("footer_line2",
                                            "PT Pindad (Persero) · Universitas Pertahanan RI · Quality 4.0"))
            fy = st.text_input("Tahun", get_setting("footer_year","2025"))
            if st.form_submit_button("💾 Simpan Footer", use_container_width=True, type="primary"):
                set_setting("footer_line1", f1)
                set_setting("footer_line2", f2)
                set_setting("footer_year",  fy)
                st.success("✅ Footer tersimpan!")
                st.rerun()

    # ── Tab 3: Logo & Media ────────────────────────────────
    with tab3:
        st.markdown("#### 🖼️ Logo Halaman Login")
        c1, c2 = st.columns([1, 2])
        with c1:
            current = get_login_logo_b64()
            if current:
                st.markdown(f'<img src="{current}" style="width:120px;height:120px;'
                            'object-fit:contain;border-radius:12px;'
                            'border:1px solid rgba(0,212,255,0.3);">',
                            unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Hapus Logo", key="del_logo"):
                    delete_login_logo()
                    st.success("Logo dihapus.")
                    st.rerun()
            else:
                st.markdown("""
                <div style="width:120px;height:120px;border-radius:12px;
                            border:2px dashed rgba(0,212,255,0.2);
                            display:flex;align-items:center;justify-content:center;
                            color:#3d5470;font-size:.75rem;text-align:center;">
                    Belum ada logo
                </div>""", unsafe_allow_html=True)

        with c2:
            st.markdown("""
            <p style="color:#c5d5e8;font-size:.85rem;line-height:1.6;">
            Upload logo/gambar untuk halaman login.<br>
            Format: PNG (transparan) atau JPG.<br>
            Ukuran tampil: 110×110px.<br>
            Rekomendasi: gambar persegi 500×500px.
            </p>""", unsafe_allow_html=True)
            logo_file = st.file_uploader("Upload Logo (PNG/JPG, maks 2MB)",
                                         type=["png","jpg","jpeg"],
                                         key="logo_uploader")
            if logo_file:
                if logo_file.size > 2*1024*1024:
                    st.error("File terlalu besar (maks 2MB).")
                else:
                    mime = "image/png" if logo_file.name.endswith(".png") else "image/jpeg"
                    save_login_logo(logo_file.read(), mime, logo_file.name)
                    st.success("✅ Logo berhasil disimpan!")
                    st.rerun()

        st.markdown("---")
        st.markdown("#### 🖼️ Foto Profil About Page")
        c1, c2 = st.columns([1, 2])
        with c1:
            pp = get_media('profile_photo')
            if pp:
                src = "data:" + pp['mime_type'] + ";base64," + pp['data']
                st.markdown(f'<img src="{src}" style="width:120px;height:120px;'
                            'object-fit:cover;border-radius:50%;'
                            'border:3px solid rgba(0,212,255,0.4);">',
                            unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Hapus Foto", key="del_photo"):
                    delete_media('profile_photo')
                    st.success("Foto dihapus.")
                    st.rerun()
            else:
                st.markdown("""
                <div style="width:120px;height:120px;border-radius:50%;
                            border:2px dashed rgba(0,212,255,0.2);
                            display:flex;align-items:center;justify-content:center;
                            color:#3d5470;font-size:.75rem;">
                    No Photo
                </div>""", unsafe_allow_html=True)
        with c2:
            photo_file = st.file_uploader("Upload Foto Profil (PNG/JPG, maks 2MB)",
                                          type=["png","jpg","jpeg"],
                                          key="photo_uploader")
            if photo_file:
                if photo_file.size > 2*1024*1024:
                    st.error("File terlalu besar.")
                else:
                    mime = "image/png" if photo_file.name.endswith(".png") else "image/jpeg"
                    b64 = base64.b64encode(photo_file.read()).decode()
                    save_media('profile_photo', photo_file.name, b64, mime)
                    st.success("✅ Foto berhasil disimpan!")
                    st.rerun()

    # ── Tab 4: Profil Peneliti ─────────────────────────────
    with tab4:
        st.markdown("#### 👤 Edit Profil Peneliti (About Page)")
        with st.form("profile_form"):
            p_name  = st.text_input("Nama Lengkap",
                                     get_setting("profile_name","Endang Saefullah, ST, CLA"))
            p_title = st.text_input("Jabatan",
                                     get_setting("profile_title","Quality Management System Engineer"))
            p_thesis= st.text_area("Judul Tesis", height=80,
                                    value=get_setting("profile_thesis",
                                        "Pengaruh ISO 9001, IATF 16949, dan Engineering Lifecycle terhadap "
                                        "Konsistensi Mutu Produksi Kendaraan Multifungsi Nasional PT Pindad (Persero)"))
            p_bg    = st.text_area("Latar Belakang Platform", height=100,
                                    value=get_setting("profile_bg",
                                        "IQLE Platform dikembangkan sebagai prototype akademik berbasis Quality 4.0 "
                                        "untuk penelitian tesis Magister Teknik di Universitas Pertahanan RI."))
            p_vision= st.text_area("Visi Pengembangan", height=80,
                                    value=get_setting("profile_vision",
                                        "Mengembangkan sistem evaluasi mutu berbasis digital untuk industri pertahanan nasional."))

            if st.form_submit_button("💾 Simpan Profil", use_container_width=True, type="primary"):
                set_setting("profile_name",   p_name)
                set_setting("profile_title",  p_title)
                set_setting("profile_thesis", p_thesis)
                set_setting("profile_bg",     p_bg)
                set_setting("profile_vision", p_vision)
                st.success("✅ Profil berhasil disimpan!")
                st.rerun()

    # ── Tab 5: PLS-SEM Input ──────────────────────────────
    with tab5:
        st.markdown("#### 📊 Input Hasil PLS-SEM")

        # Status data
        st.markdown("""
        <div style="padding:.75rem 1rem;background:rgba(255,215,0,0.08);
                    border:1px solid rgba(255,215,0,0.3);border-radius:8px;
                    font-size:.85rem;color:#e8d5a0;margin-bottom:1rem;">
            <b style="color:#ffd700;">ℹ️ Petunjuk:</b>
            Isi form ini setelah data kuesioner diolah di SmartPLS.
            Semua nilai akan otomatis digunakan di halaman Kesimpulan & Hipotesis.
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            n_resp = st.text_input("Jumlah Responden", get_pls("n_responden"))
            periode = st.text_input("Periode Pengumpulan Data", get_pls("periode"))
        with c2:
            status = st.selectbox("Status Data",
                ["Dummy — Menunggu Data Riil Kuesioner",
                 "Data Riil — Kuesioner Selesai",
                 "Data Parsial — Sebagian Terkumpul"],
                index=["Dummy — Menunggu Data Riil Kuesioner",
                       "Data Riil — Kuesioner Selesai",
                       "Data Parsial — Sebagian Terkumpul"].index(
                           get_pls("data_status"))
                if get_pls("data_status") in [
                    "Dummy — Menunggu Data Riil Kuesioner",
                    "Data Riil — Kuesioner Selesai",
                    "Data Parsial — Sebagian Terkumpul"] else 0)

        if st.button("💾 Simpan Info Data", key="save_info"):
            set_pls("n_responden", n_resp)
            set_pls("periode", periode)
            set_pls("data_status", status)
            st.success("✅ Info data tersimpan!")

        st.markdown("---")
        st.markdown("#### 🔢 Koefisien Jalur (Path Coefficients)")

        hipotesis_data = [
            ("H1", "ISO 9001 (X1) → Konsistensi Mutu (Y)", "h1"),
            ("H2", "IATF 16949 (X2) → Konsistensi Mutu (Y)", "h2"),
            ("H3", "Engineering Lifecycle (X3) → Konsistensi Mutu (Y)", "h3"),
        ]

        for hid, hlabel, hkey in hipotesis_data:
            colors = {"H1":"#00d4ff","H2":"#0066ff","H3":"#00ff88"}
            c = colors[hid]
            st.markdown(
                f'<div style="padding:.6rem .85rem;background:#111827;'
                f'border-left:3px solid {c};border-radius:6px;margin-bottom:.4rem;">'
                f'<span style="font-family:Rajdhani;color:{c};font-weight:700;">{hid}</span>'
                f' <span style="font-size:.8rem;color:#7a9bb5;">{hlabel}</span></div>',
                unsafe_allow_html=True)

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                beta = st.text_input(f"β (Koefisien)", get_pls(f"{hkey}_beta"),
                                     key=f"{hkey}_beta_in")
            with col2:
                tstat = st.text_input(f"T-Statistik", get_pls(f"{hkey}_tstat"),
                                      key=f"{hkey}_tstat_in")
            with col3:
                pval = st.text_input(f"P-Value", get_pls(f"{hkey}_pval"),
                                     key=f"{hkey}_pval_in")
            with col4:
                stat_opt = ["Diterima","Ditolak"]
                stat_cur = get_pls(f"{hkey}_status")
                hstat = st.selectbox("Status",stat_opt,
                                     index=0 if stat_cur=="Diterima" else 1,
                                     key=f"{hkey}_stat_in")

            if st.button(f"💾 Simpan {hid}", key=f"save_{hkey}"):
                set_pls(f"{hkey}_beta",   beta)
                set_pls(f"{hkey}_tstat",  tstat)
                set_pls(f"{hkey}_pval",   pval)
                set_pls(f"{hkey}_status", hstat)
                st.success(f"✅ {hid} tersimpan!")
                st.rerun()

        st.markdown("---")
        st.markdown("#### 📐 Model Fit & Validitas")

        col_mf1, col_mf2 = st.columns(2)
        with col_mf1:
            st.markdown("**Model Fit**")
            r2 = st.text_input("R² (Koefisien Determinasi)", get_pls("model_r2"))
            q2 = st.text_input("Q² (Predictive Relevance)", get_pls("model_q2"))
            if st.button("💾 Simpan Model Fit", key="save_mf"):
                set_pls("model_r2", r2); set_pls("model_q2", q2)
                st.success("✅ Model fit tersimpan!")

        with col_mf2:
            st.markdown("**AVE (Average Variance Extracted)**")
            vars_ave = [("X1 ISO 9001","ave_x1"),("X2 IATF 16949","ave_x2"),
                        ("X3 Eng. Lifecycle","ave_x3"),("Y Konsistensi","ave_y")]
            ave_vals = {}
            for vl, vk in vars_ave:
                ave_vals[vk] = st.text_input(vl, get_pls(vk), key=f"ave_{vk}")
            if st.button("💾 Simpan AVE", key="save_ave"):
                for vk, vv in ave_vals.items():
                    set_pls(vk, vv)
                st.success("✅ AVE tersimpan!")

        st.markdown("---")
        col_r1, col_r2_c = st.columns(2)
        with col_r1:
            st.markdown("**Composite Reliability (CR)**")
            vars_cr = [("X1","cr_x1"),("X2","cr_x2"),("X3","cr_x3"),("Y","cr_y")]
            cr_vals = {}
            for vl, vk in vars_cr:
                cr_vals[vk] = st.text_input(f"CR {vl}", get_pls(vk), key=f"cr_{vk}")
            if st.button("💾 Simpan CR", key="save_cr"):
                for vk, vv in cr_vals.items():
                    set_pls(vk, vv)
                st.success("✅ CR tersimpan!")

        with col_r2_c:
            st.markdown("**Cronbach Alpha (CA)**")
            vars_ca = [("X1","ca_x1"),("X2","ca_x2"),("X3","ca_x3"),("Y","ca_y")]
            ca_vals = {}
            for vl, vk in vars_ca:
                ca_vals[vk] = st.text_input(f"CA {vl}", get_pls(vk), key=f"ca_{vk}")
            if st.button("💾 Simpan CA", key="save_ca"):
                for vk, vv in ca_vals.items():
                    set_pls(vk, vv)
                st.success("✅ Cronbach Alpha tersimpan!")
