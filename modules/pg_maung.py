import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.database import fetch, fetchone, run, qdf
from utils.styles import section_header, plotly_layout, render_footer
from utils.auth import is_admin

KATEGORI_LIST = ["Sistem Kelistrikan","Sistem Wiper & Cairan","Sistem Assembly & Fitting",
                 "Estetika & Body","Sistem Mekanik","Kelengkapan & Keselamatan","Dokumentasi & Admin"]
JENIS_LIST    = ["Assembly Error","Electrical Failure","Missing Part","Surface Defect",
                 "Mechanical Failure","Dimensional Error","Documentation Error"]
BATCH_LIST    = [f"Batch-{i}" for i in range(1, 10)]
KAT_COLOR     = {
    "Sistem Kelistrikan":"#ff3366","Sistem Wiper & Cairan":"#0066ff",
    "Sistem Assembly & Fitting":"#ffd700","Estetika & Body":"#ff6b35",
    "Sistem Mekanik":"#00ff88","Kelengkapan & Keselamatan":"#a78bfa","Dokumentasi & Admin":"#00d4ff"
}

MOM_DATA = [
    ("Batch-1","29 Jul-1 Agt 2024","Seat belt belakang lepas","Kelengkapan & Keselamatan","Assembly Error"),
    ("Batch-1","29 Jul-1 Agt 2024","Roof lamp mati","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-1","29 Jul-1 Agt 2024","Pintu belakang tidak bisa dibuka","Sistem Assembly & Fitting","Assembly Error"),
    ("Batch-1","29 Jul-1 Agt 2024","Pintu belakang tidak bisa tertutup","Sistem Assembly & Fitting","Assembly Error"),
    ("Batch-1","29 Jul-1 Agt 2024","Belum ada logo","Estetika & Body","Missing Part"),
    ("Batch-1","29 Jul-1 Agt 2024","Head unit tidak nyala","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-1","29 Jul-1 Agt 2024","Tutup tangki tidak terkunci","Sistem Mekanik","Assembly Error"),
    ("Batch-1","29 Jul-1 Agt 2024","Gap pintu-body bervariasi","Sistem Assembly & Fitting","Dimensional Error"),
    ("Batch-1","29 Jul-1 Agt 2024","Wiper touching cover cowl","Sistem Wiper & Cairan","Assembly Error"),
    ("Batch-2","13-15 Nov 2024","Emblem tangguh mudah terlepas","Estetika & Body","Assembly Error"),
    ("Batch-2","13-15 Nov 2024","Selang wiper lepas","Sistem Wiper & Cairan","Assembly Error"),
    ("Batch-2","13-15 Nov 2024","Tuas engine hood lepas","Sistem Mekanik","Assembly Error"),
    ("Batch-2","13-15 Nov 2024","Unit tidak ada tank","Kelengkapan & Keselamatan","Missing Part"),
    ("Batch-2","13-15 Nov 2024","Lampu kota mati","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-2","13-15 Nov 2024","Salah pengetikan nomor engine","Dokumentasi & Admin","Documentation Error"),
    ("Batch-2","13-15 Nov 2024","Lampu ada yang mati","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-2","13-15 Nov 2024","Body baret","Estetika & Body","Surface Defect"),
    ("Batch-3","24-25 Feb 2025","Logo tangguh kurang kokoh","Estetika & Body","Assembly Error"),
    ("Batch-3","24-25 Feb 2025","Nozzle wiper tidak berfungsi","Sistem Wiper & Cairan","Electrical Failure"),
    ("Batch-3","24-25 Feb 2025","Tuas engine hood lepas","Sistem Mekanik","Assembly Error"),
    ("Batch-3","24-25 Feb 2025","Lampu kota (DRL) mati","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-3","24-25 Feb 2025","Kesalahan penulisan nomor mesin","Dokumentasi & Admin","Documentation Error"),
    ("Batch-3","24-25 Feb 2025","Toolkit kurang (tang tidak ada)","Kelengkapan & Keselamatan","Missing Part"),
    ("Batch-3","24-25 Feb 2025","Lampu belakang rem/sein tidak fungsi","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-3","24-25 Feb 2025","Lampu depan kiri tidak fungsi","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-3","24-25 Feb 2025","Body depan baret","Estetika & Body","Surface Defect"),
    ("Batch-3","24-25 Feb 2025","Selang air wiper terlepas","Sistem Wiper & Cairan","Assembly Error"),
    ("Batch-4","14-15 Mei 2025","Logo tangguh tidak ada","Estetika & Body","Missing Part"),
    ("Batch-4","14-15 Mei 2025","Room lamp tidak ada","Sistem Kelistrikan","Missing Part"),
    ("Batch-4","14-15 Mei 2025","Side sign lamp RH tidak ada","Sistem Kelistrikan","Missing Part"),
    ("Batch-4","14-15 Mei 2025","Adaptor wiper cabang patah","Sistem Wiper & Cairan","Assembly Error"),
    ("Batch-4","14-15 Mei 2025","Tuas engine hood lepas (4 unit)","Sistem Mekanik","Assembly Error"),
    ("Batch-4","14-15 Mei 2025","Kunci pas 10 tidak ada","Kelengkapan & Keselamatan","Missing Part"),
    ("Batch-5","26-27 Agt 2025","Lampu kota mati","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-5","26-27 Agt 2025","Lampu rem mati","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-5","26-27 Agt 2025","Selang wiper lepas","Sistem Wiper & Cairan","Assembly Error"),
    ("Batch-5","26-27 Agt 2025","Emblem tangguh lepas","Estetika & Body","Assembly Error"),
    ("Batch-5","26-27 Agt 2025","Emblem kurang kokoh","Estetika & Body","Assembly Error"),
    ("Batch-5","26-27 Agt 2025","Spooring ulang","Sistem Mekanik","Mechanical Failure"),
    ("Batch-5","26-27 Agt 2025","Head lamp longgar RH","Sistem Kelistrikan","Assembly Error"),
    ("Batch-5","26-27 Agt 2025","Wiper lepas","Sistem Wiper & Cairan","Assembly Error"),
    ("Batch-6","3-4 Okt 2025","Lampu kota mati (multi unit)","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-6","3-4 Okt 2025","Lampu rem mati","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-6","3-4 Okt 2025","Selang wiper lepas (multi unit)","Sistem Wiper & Cairan","Assembly Error"),
    ("Batch-6","3-4 Okt 2025","Emblem tangguh lepas (multi)","Estetika & Body","Assembly Error"),
    ("Batch-6","3-4 Okt 2025","Emblem miring/kurang kokoh","Estetika & Body","Assembly Error"),
    ("Batch-6","3-4 Okt 2025","Spooring ulang","Sistem Mekanik","Mechanical Failure"),
    ("Batch-6","3-4 Okt 2025","Head lamp longgar RH","Sistem Kelistrikan","Assembly Error"),
    ("Batch-6","3-4 Okt 2025","Setting pintu FRT RH","Sistem Assembly & Fitting","Assembly Error"),
    ("Batch-6","3-4 Okt 2025","Tuas engine hood lepas (2 unit)","Sistem Mekanik","Assembly Error"),
    ("Batch-6","3-4 Okt 2025","Fender depan baret","Estetika & Body","Surface Defect"),
    ("Batch-6","3-4 Okt 2025","Tang tidak ada","Kelengkapan & Keselamatan","Missing Part"),
    ("Batch-6","3-4 Okt 2025","P3K dan manual book tidak ada","Dokumentasi & Admin","Missing Part"),
    ("Batch-6","3-4 Okt 2025","Batang dongkrak kurang","Kelengkapan & Keselamatan","Missing Part"),
    ("Batch-7","13-15 Nov 2025","Central lock kurang sensitif","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-7","13-15 Nov 2025","Rubber tambahan lepas","Sistem Assembly & Fitting","Assembly Error"),
    ("Batch-7","13-15 Nov 2025","Pintu flush (2 unit)","Sistem Assembly & Fitting","Dimensional Error"),
    ("Batch-7","13-15 Nov 2025","Kebersihan 100% kotor","Estetika & Body","Surface Defect"),
    ("Batch-7","13-15 Nov 2025","Pintu melenting (efek bengkek)","Sistem Assembly & Fitting","Assembly Error"),
    ("Batch-7","13-15 Nov 2025","Tuas engine hood lepas","Sistem Mekanik","Assembly Error"),
    ("Batch-7","13-15 Nov 2025","Oil bocor","Sistem Mekanik","Mechanical Failure"),
    ("Batch-8","21-23 Des 2025","Body depan masih cat dasar","Estetika & Body","Surface Defect"),
    ("Batch-8","21-23 Des 2025","Penutup no chasis tidak rapih","Estetika & Body","Surface Defect"),
    ("Batch-8","21-23 Des 2025","Body belakang masih cat dasar","Estetika & Body","Surface Defect"),
    ("Batch-8","21-23 Des 2025","Washer nozzle NG (2 unit)","Sistem Wiper & Cairan","Electrical Failure"),
    ("Batch-8","21-23 Des 2025","Power window tidak fungsi (4 unit)","Sistem Kelistrikan","Electrical Failure"),
    ("Batch-8","21-23 Des 2025","Selang air wiper lepas","Sistem Wiper & Cairan","Assembly Error"),
    ("Batch-8","21-23 Des 2025","Kunci kurang 1 pcs","Kelengkapan & Keselamatan","Missing Part"),
    ("Batch-8","21-23 Des 2025","Air coolant kurang (3 unit)","Sistem Wiper & Cairan","Mechanical Failure"),
    ("Batch-9","13-15 Jan 2026","Tuas winch terhalang bumper","Sistem Mekanik","Assembly Error"),
    ("Batch-9","13-15 Jan 2026","Posisi hole manual winch kurang","Sistem Mekanik","Dimensional Error"),
    ("Batch-9","13-15 Jan 2026","Visual chasis tidak rapih","Estetika & Body","Surface Defect"),
    ("Batch-9","13-15 Jan 2026","Body belang (cat tidak rata)","Estetika & Body","Surface Defect"),
    ("Batch-9","13-15 Jan 2026","Posisi kondensor & intercooler","Sistem Mekanik","Assembly Error"),
    ("Batch-9","13-15 Jan 2026","Reflektor RH tidak ada","Sistem Kelistrikan","Missing Part"),
    ("Batch-9","13-15 Jan 2026","Cover ACCU dan brkt tidak ada","Kelengkapan & Keselamatan","Missing Part"),
    ("Batch-9","13-15 Jan 2026","Air coolant dibawah batas min","Sistem Wiper & Cairan","Mechanical Failure"),
    ("Batch-9","13-15 Jan 2026","Kerapihan door flush","Sistem Assembly & Fitting","Dimensional Error"),
    ("Batch-9","13-15 Jan 2026","Kerapihan weatherstrip door","Sistem Assembly & Fitting","Assembly Error"),
    ("Batch-9","13-15 Jan 2026","Kerapihan karet backdoor glass","Sistem Assembly & Fitting","Assembly Error"),
    ("Batch-9","13-15 Jan 2026","Body noise","Sistem Mekanik","Mechanical Failure"),
]

def _ensure_seeded():
    row = fetchone("SELECT COUNT(*) as cnt FROM maung_defects WHERE source='MoM'")
    if row and int(row.get('cnt', 0)) == 0:
        for b,t,d,k,j in MOM_DATA:
            run("INSERT INTO maung_defects (batch,tanggal,defect,kategori,jenis,source) VALUES (%s,%s,%s,%s,%s,'MoM')",(b,t,d,k,j))

def _get_df():
    rows = fetch("SELECT * FROM maung_defects ORDER BY batch, id")
    return pd.DataFrame(rows) if rows else pd.DataFrame(columns=["id","batch","tanggal","defect","kategori","jenis","source"])

def show():
    section_header("Analisis Mutu MAUNG MV3","7 Parameter Mutu — Data MoM Batch 1-9 + Input Lapangan","🚗")
    _ensure_seeded()
    df = _get_df()

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["📊 Dashboard","📈 Skor Parameter","➕ Input Defect","📋 Data","🔗 Kaitan Penelitian"])

    with tab1:
        if df.empty: st.info("Belum ada data."); return
        total = len(df)
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Defect", total)
        c2.metric("Batch", df["batch"].nunique())
        c3.metric("Data MoM", len(df[df["source"]=="MoM"]))
        c4.metric("Data Baru", len(df[df["source"]!="MoM"]))

        cl1,cl2 = st.columns(2)
        with cl1:
            bc = df.groupby("batch").size().reset_index(name="n")
            fig = go.Figure(go.Bar(x=bc["batch"],y=bc["n"],marker=dict(color="#00d4ff",opacity=0.85),text=bc["n"],textposition="outside"))
            fig.add_hline(y=bc["n"].mean(),line_dash="dash",line_color="#ffd700",annotation_text=f"Avg {bc['n'].mean():.1f}")
            l=plotly_layout(); l.update(height=300,title="Defect per Batch"); fig.update_layout(**l)
            st.plotly_chart(fig, use_container_width=True)
        with cl2:
            kc = df["kategori"].value_counts()
            fig2=go.Figure(go.Pie(labels=[k.replace("Sistem ","") for k in kc.index],values=kc.values,hole=0.5,marker=dict(colors=[KAT_COLOR.get(k,"#7a9bb5") for k in kc.index])))
            l2=plotly_layout(); l2.update(height=300,title="Distribusi Kategori"); fig2.update_layout(**l2)
            st.plotly_chart(fig2, use_container_width=True)

        pivot=df.groupby(["batch","kategori"]).size().unstack(fill_value=0)
        fig3=go.Figure()
        for kat in pivot.columns:
            fig3.add_trace(go.Bar(name=kat.replace("Sistem ",""),x=pivot.index,y=pivot[kat],marker=dict(color=KAT_COLOR.get(kat,"#7a9bb5"),opacity=0.85)))
        l3=plotly_layout(); l3.update(barmode="stack",height=320,title="Komposisi Defect per Batch"); fig3.update_layout(**l3)
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        if df.empty: st.info("Belum ada data."); return
        total_d=len(df); kc=df["kategori"].value_counts()
        scores={kat:max(0,round(100-(kc.get(kat,0)/total_d*150),1)) for kat in KATEGORI_LIST}
        labels=[k.replace("Sistem ","").replace(" & ","&\n") for k in scores]; vals=list(scores.values())
        fig_r=go.Figure()
        fig_r.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=labels+[labels[0]],fill="toself",name="Aktual",line=dict(color="#00d4ff",width=2),fillcolor="rgba(0,212,255,0.1)"))
        fig_r.add_trace(go.Scatterpolar(r=[75]*len(labels)+[75],theta=labels+[labels[0]],fill="toself",name="Target 75",line=dict(color="#ffd700",width=1,dash="dot"),fillcolor="rgba(255,215,0,0.04)"))
        lr=plotly_layout(); lr.update(polar=dict(radialaxis=dict(visible=True,range=[0,100],gridcolor="rgba(0,212,255,0.1)"),bgcolor="rgba(0,0,0,0)"),height=400)
        fig_r.update_layout(**lr); st.plotly_chart(fig_r, use_container_width=True)

        cols=st.columns(len(KATEGORI_LIST))
        for i,(kat,skor) in enumerate(scores.items()):
            c=KAT_COLOR.get(kat,"#7a9bb5"); cnt=kc.get(kat,0)
            sc="#00ff88" if skor>=75 else "#ffd700" if skor>=60 else "#ff3366"
            status="Baik" if skor>=75 else "Cukup" if skor>=60 else "Perlu Perbaikan"
            cols[i].markdown(f'<div style="padding:.6rem .5rem;background:#111827;border-top:3px solid {c};border-radius:8px;text-align:center;"><div style="font-size:.6rem;color:#7a9bb5;">{kat.replace("Sistem ","")}</div><div style="font-family:Rajdhani;font-size:1.6rem;font-weight:700;color:{c};">{skor}</div><div style="font-size:.6rem;color:{sc};">{status}</div><div style="font-size:.6rem;color:#4a6fa5;">{cnt} defect</div></div>', unsafe_allow_html=True)

        overall=round(sum(vals)/len(vals),1); ov_c="#00ff88" if overall>=75 else "#ffd700" if overall>=60 else "#ff3366"
        st.markdown(f'<div style="margin-top:1rem;padding:1rem;text-align:center;background:{ov_c}11;border:2px solid {ov_c}44;border-radius:10px;"><div style="font-size:.65rem;color:#7a9bb5;letter-spacing:2px;text-transform:uppercase;">OVERALL QUALITY SCORE</div><div style="font-family:Rajdhani;font-size:3.5rem;font-weight:700;color:{ov_c};">{overall}</div></div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("#### Tambah Data Defect")
        if not is_admin(): st.warning("Hanya Admin yang dapat menambah data."); return
        with st.form("add_defect"):
            c1,c2=st.columns(2)
            batch=c1.selectbox("Batch*",BATCH_LIST+["Batch-10+"])
            tgl=c1.text_input("Tanggal Uji*",placeholder="contoh: 15 Feb 2026")
            defect=c1.text_input("Deskripsi Defect*")
            kategori=c2.selectbox("Kategori*",KATEGORI_LIST)
            jenis=c2.selectbox("Jenis Defect*",JENIS_LIST)
            source=c2.text_input("Sumber",value="Lapangan")
            if st.form_submit_button("Tambah",type="primary",use_container_width=True):
                if defect and kategori:
                    run("INSERT INTO maung_defects (batch,tanggal,defect,kategori,jenis,source) VALUES (%s,%s,%s,%s,%s,%s)",(batch,tgl,defect,kategori,jenis,source))
                    st.success("Berhasil ditambahkan!"); st.rerun()
                else: st.error("Lengkapi field wajib.")

    with tab4:
        if df.empty: st.info("Belum ada data."); return
        fc1,fc2=st.columns(2)
        f_batch=fc1.multiselect("Batch",sorted(df["batch"].unique()),default=sorted(df["batch"].unique()))
        f_kat=fc2.multiselect("Kategori",KATEGORI_LIST,default=KATEGORI_LIST)
        filtered=df[df["batch"].isin(f_batch)&df["kategori"].isin(f_kat)]
        st.dataframe(filtered[["batch","tanggal","defect","kategori","jenis","source"]].reset_index(drop=True),use_container_width=True,height=400)
        if is_admin():
            new_d=df[df["source"]!="MoM"]
            if not new_d.empty:
                del_id=st.selectbox("Hapus ID (lapangan only)",new_d["id"].tolist(),format_func=lambda x: f"ID {x} — {new_d[new_d['id']==x]['defect'].values[0]}")
                if st.button("Hapus"): run("DELETE FROM maung_defects WHERE id=%s",(del_id,)); st.rerun()

    with tab5:
        for var,color,text in [
            ("ISO 9001 (X1) β=0.318","#00d4ff","Kesalahan nomor mesin, P3K/manual book tidak ada → lemahnya Document Control. Mendukung H1 diterima."),
            ("IATF 16949 (X2) β=0.217","#0066ff","Parts supplier bermasalah berulang (emblem, selang, nozzle) → lemahnya Supplier Quality. Mendukung H2 diterima."),
            ("Engineering Lifecycle (X3) β=0.532 DOMINAN","#00ff88","Selang wiper 8/9 batch, tuas hood 6/9 batch — corrective action tidak masuk ke Engineering Change Control. Bukti terkuat H3. Mendukung H3 diterima."),
            ("Konsistensi Mutu (Y)","#ffd700",f"Variasi defect min {df.groupby('batch').size().min() if not df.empty else 0} — max {df.groupby('batch').size().max() if not df.empty else 0} per batch membuktikan inkonsistensi dan urgensi penelitian."),
        ]:
            st.markdown(f'<div style="padding:1rem 1.25rem;background:#111827;border-left:4px solid {color};border-radius:8px;margin-bottom:.6rem;"><div style="font-family:Rajdhani;color:{color};font-weight:700;margin-bottom:.3rem;">{var}</div><div style="font-size:.83rem;color:#c5d5e8;line-height:1.65;">{text}</div></div>',unsafe_allow_html=True)
        render_footer()
