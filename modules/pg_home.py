import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.database import fetch, fetchone, run, qdf, get_category, get_lifecycle_maturity
from utils.styles import section_header, score_bar, category_banner, plotly_layout


def show():
    section_header("Dashboard Utama", "Integrated Engineering Quality Lifecycle Evaluation Platform", "🏠")

    # Role banner
    import streamlit as _st
    user = _st.session_state.get("user", {})
    role = _st.session_state.get("role", "viewer")
    name = user.get("full_name") or user.get("username", "")

    ROLE_INFO = {
        "admin":    ("#00d4ff", "ADMINISTRATOR",
                     "Akses penuh: input evaluasi, manajemen user, pengaturan platform, semua modul."),
        "viewer":   ("#ffd700", "VIEWER",
                     "Akses baca: lihat semua dashboard dan laporan, tidak dapat input data."),
        "evaluator":("#00ff88", "EVALUATOR",
                     "Akses evaluasi: dapat mengisi data evaluasi mutu & batch, tidak dapat atur sistem."),
    }
    rc, rl, rd = ROLE_INFO.get(role, ("#7a9bb5","USER","Akses terbatas."))
    _st.markdown(
        f'<div style="padding:.65rem 1.25rem;background:{rc}0d;border:1px solid {rc}33;'
        f'border-left:4px solid {rc};border-radius:8px;margin-bottom:1.25rem;'
        f'display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:.5rem;">' 
        f'<div><div style="font-family:Rajdhani;font-size:.88rem;font-weight:700;color:{rc};">'
        f'Selamat datang, {name}</div>'
        f'<div style="font-size:.75rem;color:#7a9bb5;margin-top:.1rem;">{rd}</div></div>'
        f'<span style="background:{rc}22;border:1px solid {rc}44;border-radius:4px;'
        f'padding:3px 14px;font-family:Rajdhani;font-size:.75rem;font-weight:700;color:{rc};">{rl}</span>' 
        f'</div>',
        unsafe_allow_html=True
    )

    batch_df = qdf("SELECT * FROM batch_production ORDER BY production_date")
    defect_df = qdf("SELECT * FROM defect_records")

    total_batch  = len(batch_df)
    total_units  = int(batch_df['total_units'].sum())  if not batch_df.empty else 0
    total_defect = int(batch_df['total_defect'].sum()) if not batch_df.empty else 0
    total_rework = int(batch_df['total_rework'].sum()) if not batch_df.empty else 0
    avg_dr = round(batch_df['defect_rate'].mean(),  2) if not batch_df.empty else 0
    avg_rr = round(batch_df['rework_rate'].mean(),  2) if not batch_df.empty else 0

    iso_s  = qdf("SELECT average_score FROM iso9001_evaluation      ORDER BY eval_date DESC LIMIT 1")
    iatf_s = qdf("SELECT average_score FROM iatf16949_evaluation     ORDER BY eval_date DESC LIMIT 1")
    lc_s   = qdf("SELECT average_score FROM engineering_lifecycle    ORDER BY eval_date DESC LIMIT 1")
    qc_s   = qdf("SELECT average_score FROM quality_consistency      ORDER BY eval_date DESC LIMIT 1")
    iso  = float(iso_s.iloc[0]['average_score'])  if not iso_s.empty  else 0
    iatf = float(iatf_s.iloc[0]['average_score']) if not iatf_s.empty else 0
    lc   = float(lc_s.iloc[0]['average_score'])   if not lc_s.empty   else 0
    qc   = float(qc_s.iloc[0]['average_score'])   if not qc_s.empty   else 0
    iqls = round(iso*0.25 + iatf*0.20 + lc*0.35 + qc*0.20, 1)

    # ── KPI row ─────────────────────────────────────────────
    st.markdown("#### 📊 Key Performance Indicators")
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Total Batch",    total_batch)
    c2.metric("Total Unit",     total_units)
    c3.metric("Total Defect",   total_defect)
    c4.metric("Defect Rate",    f"{avg_dr}%")
    c5.metric("Rework Rate",    f"{avg_rr}%")
    c6.metric("IQLS Score",     iqls)

    st.markdown("---")

    # ── Score bars + Trend ───────────────────────────────────
    col_l, col_r = st.columns([1, 2])

    with col_l:
        st.markdown("#### 🏆 Skor Evaluasi Terkini")
        score_bar("📊 ISO 9001 (X1)",              iso,  "#00d4ff")
        score_bar("🏭 IATF 16949 (X2)",             iatf, "#0066ff")
        score_bar("⚙️ Eng. Lifecycle (X3) ⭐",      lc,   "#00ff88")
        score_bar("✅ Konsistensi Mutu (Y)",          qc,   "#ffd700")

        cat = get_category(iqls)
        colors = {"Sangat Baik":"#00ff88","Baik":"#00d4ff","Cukup":"#ffd700","Perlu Perbaikan":"#ff3366"}
        c = colors.get(cat,"#7a9bb5")
        st.markdown(f"""
        <div style="margin-top:1rem; padding:1rem; text-align:center;
                    background:{c}11; border:2px solid {c}44; border-radius:10px;">
            <div style="font-size:0.65rem; color:#7a9bb5; letter-spacing:2px; text-transform:uppercase;">
                INTEGRATED QUALITY LIFECYCLE SCORE
            </div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:3.2rem;
                        font-weight:700; color:{c}; line-height:1.1;">{iqls}</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1rem;
                        font-weight:600; color:{c};">{cat}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown("#### 📈 Trend Defect & Rework per Batch")
        if not batch_df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=batch_df['batch_number'], y=batch_df['defect_rate'],
                mode='lines+markers', name='Defect Rate (%)',
                line=dict(color='#ff3366', width=2),
                fill='tozeroy', fillcolor='rgba(255,51,102,0.08)'
            ))
            fig.add_trace(go.Scatter(
                x=batch_df['batch_number'], y=batch_df['rework_rate'],
                mode='lines+markers', name='Rework Rate (%)',
                line=dict(color='#ffd700', width=2)
            ))
            lay = plotly_layout()
            lay.update(height=270, xaxis=dict(**lay['xaxis'], tickangle=45, tickfont=dict(size=8)))
            fig.update_layout(**lay)
            st.plotly_chart(fig, use_container_width=True)

        if not batch_df.empty:
            sc = batch_df['status'].value_counts()
            fig2 = go.Figure(go.Bar(
                x=sc.values, y=sc.index, orientation='h',
                marker=dict(color=['#00ff88' if s=='Completed' else '#ffd700' if s=='In Progress' else '#00d4ff'
                                   for s in sc.index], opacity=0.8)
            ))
            lay2 = plotly_layout()
            lay2.update(height=160, margin=dict(l=90,r=20,t=30,b=10))
            fig2.update_layout(**lay2)
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### 🔍 Defect per Tahap Produksi")
        if not defect_df.empty:
            sc2 = defect_df.groupby('defect_stage')['quantity'].sum().sort_values()
            fig3 = go.Figure(go.Bar(
                x=sc2.values, y=sc2.index, orientation='h',
                marker=dict(color='#0066ff', opacity=0.8)
            ))
            lay3 = plotly_layout()
            lay3.update(height=300, margin=dict(l=130,r=20,t=30,b=20))
            fig3.update_layout(**lay3)
            st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown("#### 🏆 Top Jenis Defect")
        if not defect_df.empty:
            td = defect_df.groupby('defect_type')['quantity'].sum().sort_values(ascending=False).head(7)
            fig4 = go.Figure(go.Pie(
                labels=td.index, values=td.values, hole=0.5,
                marker=dict(colors=['#ff3366','#ff6b35','#ffd700','#00d4ff',
                                    '#0066ff','#00ff88','#a78bfa']),
                textfont=dict(size=10)
            ))
            lay4 = plotly_layout()
            lay4.update(height=300)
            fig4.update_layout(**lay4)
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📋 Batch Terkini")
    if not batch_df.empty:
        show_df = batch_df[['batch_number','production_date','total_units',
                             'total_defect','defect_rate','rework_rate','status']].tail(8).copy()
        show_df.columns = ['No. Batch','Tanggal','Unit','Defect','Defect Rate(%)','Rework Rate(%)','Status']
        st.dataframe(show_df, use_container_width=True, hide_index=True)

    # ── Generate PDF Report ──────────────────────────────────
    st.markdown("---")
    st.markdown("#### 📄 Generate Laporan PDF")

    col_pdf1, col_pdf2, col_pdf3 = st.columns([2, 1, 2])
    with col_pdf2:
        gen = st.button("📥 Generate PDF", key="gen_pdf",
                        use_container_width=True, type="primary")

    if gen:
        _generate_dashboard_pdf(batch_df, defect_df, kpi)


def _generate_dashboard_pdf(batch_df, defect_df, kpi):
    """Generate dashboard PDF report using reportlab."""
    import streamlit as st
    from io import BytesIO
    from datetime import datetime

    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                         Table, TableStyle, HRFlowable)
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
    except ImportError:
        st.error("❌ Modul reportlab belum terinstall. Tambahkan `reportlab` ke requirements.txt")
        return

    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                             topMargin=2*cm, bottomMargin=2*cm,
                             leftMargin=2*cm, rightMargin=2*cm)

    # Colors
    NAVY   = colors.HexColor("#0d1321")
    CYAN   = colors.HexColor("#00d4ff")
    GOLD   = colors.HexColor("#ffd700")
    WHITE  = colors.HexColor("#e8edf5")
    GRAY   = colors.HexColor("#7a9bb5")
    DARK   = colors.HexColor("#111827")

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", parent=styles["Heading1"],
        fontSize=18, textColor=CYAN, spaceAfter=4,
        fontName="Helvetica-Bold", alignment=TA_CENTER)
    sub_style = ParagraphStyle("sub", parent=styles["Normal"],
        fontSize=9, textColor=GRAY, alignment=TA_CENTER, spaceAfter=2)
    h2_style = ParagraphStyle("h2", parent=styles["Heading2"],
        fontSize=12, textColor=CYAN, spaceBefore=12, spaceAfter=6,
        fontName="Helvetica-Bold")
    body_style = ParagraphStyle("body", parent=styles["Normal"],
        fontSize=9, textColor=colors.HexColor("#4a6fa5"), spaceAfter=4)

    story = []
    now = datetime.now().strftime("%d %B %Y, %H:%M WIB")

    # Header
    story.append(Paragraph("IQLE PLATFORM", title_style))
    story.append(Paragraph("Integrated Engineering Quality Lifecycle Evaluation", sub_style))
    story.append(Paragraph("PT Pindad (Persero) · Universitas Pertahanan RI", sub_style))
    story.append(HRFlowable(width="100%", thickness=1, color=CYAN, spaceAfter=8))
    story.append(Paragraph(f"LAPORAN DASHBOARD UTAMA", h2_style))
    story.append(Paragraph(f"Digenerate: {now}", body_style))
    story.append(Spacer(1, 0.3*cm))

    # KPI Table
    story.append(Paragraph("KEY PERFORMANCE INDICATORS", h2_style))
    kpi_data = [
        ["Indikator", "Nilai"],
        ["Total Batch Produksi", str(kpi.get("total_batch", 0))],
        ["Total Unit Diproduksi", str(kpi.get("total_units", 0))],
        ["Total Defect", str(kpi.get("total_defect", 0))],
        ["Defect Rate", f"{kpi.get('defect_rate', 0):.2f}%"],
        ["Rework Rate", f"{kpi.get('rework_rate', 0):.2f}%"],
        ["IQLS Score", f"{kpi.get('iqls', 0):.1f}"],
    ]
    kpi_table = Table(kpi_data, colWidths=[10*cm, 6*cm])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,0),  CYAN),
        ("TEXTCOLOR",   (0,0), (-1,0),  NAVY),
        ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 9),
        ("BACKGROUND",  (0,1), (-1,-1), DARK),
        ("TEXTCOLOR",   (0,1), (-1,-1), WHITE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [DARK, colors.HexColor("#0d1321")]),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#21262d")),
        ("ALIGN",       (1,0), (1,-1),  "CENTER"),
        ("PADDING",     (0,0), (-1,-1), 6),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.5*cm))

    # Batch table
    if not batch_df.empty:
        story.append(Paragraph("DATA BATCH PRODUKSI", h2_style))
        cols_show = ["batch_number","production_date","total_units",
                     "total_defect","defect_rate","rework_rate","status"]
        col_labels = ["No. Batch","Tanggal","Unit","Defect","DR(%)","RR(%)","Status"]
        b_data = [col_labels]
        for _, row in batch_df[cols_show].iterrows():
            b_data.append([str(row[c]) for c in cols_show])
        b_table = Table(b_data, repeatRows=1)
        b_table.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0),  CYAN),
            ("TEXTCOLOR",   (0,0), (-1,0),  NAVY),
            ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
            ("FONTSIZE",    (0,0), (-1,-1), 8),
            ("BACKGROUND",  (0,1), (-1,-1), DARK),
            ("TEXTCOLOR",   (0,1), (-1,-1), WHITE),
            ("ROWBACKGROUNDS", (0,1),(-1,-1),[DARK, colors.HexColor("#0d1321")]),
            ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#21262d")),
            ("PADDING",     (0,0), (-1,-1), 5),
        ]))
        story.append(b_table)
        story.append(Spacer(1, 0.5*cm))

    # Defect summary
    if not defect_df.empty:
        story.append(Paragraph("RINGKASAN DEFECT PER JENIS", h2_style))
        td = defect_df.groupby("defect_type")["quantity"].sum().sort_values(ascending=False)
        total_def = td.sum()
        d_data = [["Jenis Defect", "Jumlah", "Persentase"]]
        for dtype, qty in td.items():
            pct = f"{qty/total_def*100:.1f}%" if total_def > 0 else "0%"
            d_data.append([dtype, str(qty), pct])
        d_table = Table(d_data, colWidths=[9*cm, 4*cm, 3*cm])
        d_table.setStyle(TableStyle([
            ("BACKGROUND",  (0,0), (-1,0),  CYAN),
            ("TEXTCOLOR",   (0,0), (-1,0),  NAVY),
            ("FONTNAME",    (0,0), (-1,0),  "Helvetica-Bold"),
            ("FONTSIZE",    (0,0), (-1,-1), 8),
            ("BACKGROUND",  (0,1), (-1,-1), DARK),
            ("TEXTCOLOR",   (0,1), (-1,-1), WHITE),
            ("GRID",        (0,0), (-1,-1), 0.4, colors.HexColor("#21262d")),
            ("PADDING",     (0,0), (-1,-1), 5),
            ("ALIGN",       (1,0), (2,-1),  "CENTER"),
        ]))
        story.append(d_table)

    # Footer
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY))
    story.append(Paragraph(
        f"IQLE Platform · PT Pindad (Persero) · Universitas Pertahanan RI · {now}",
        sub_style))

    doc.build(story)
    buf.seek(0)

    fn = f"IQLE_Dashboard_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    st.download_button(
        label="⬇️ Download Laporan PDF",
        data=buf,
        file_name=fn,
        mime="application/pdf",
        key="download_pdf",
        type="primary",
        use_container_width=False,
    )
    st.success(f"✅ Laporan '{fn}' siap didownload!")
