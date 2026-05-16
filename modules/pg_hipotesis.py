import streamlit as st
import plotly.graph_objects as go
from utils.database import fetch, qdf
from utils.styles import section_header, plotly_layout, render_footer


COEF  = {"X1": 0.318, "X2": 0.217, "X3": 0.532}
TSTAT = {"X1": 3.847, "X2": 2.913, "X3": 6.124}
PVAL  = {"X1": 0.001, "X2": 0.004, "X3": 0.000}
R2    = 0.729
Q2    = 0.548
AVE   = {"X1": 0.624, "X2": 0.587, "X3": 0.671, "Y": 0.612}
CR    = {"X1": 0.891, "X2": 0.857, "X3": 0.908, "Y": 0.884}
CA    = {"X1": 0.852, "X2": 0.801, "X3": 0.876, "Y": 0.841}


def show():
    section_header(
        "Kesimpulan & Hipotesis",
        "Hasil Uji Hipotesis & Validasi Model Struktural PLS-SEM",
        "🏆"
    )

    # ── Status hipotesis ───────────────────────────────────
    st.markdown("#### ✅ Hasil Uji Hipotesis")

    hipotesis = [
        ("H1", "ISO 9001 (X1)", "Konsistensi Mutu (Y)",
         0.318, 3.847, 0.001, True,
         "ISO 9001 berpengaruh signifikan positif terhadap konsistensi mutu "
         "produksi MAUNG MV3 di PT Pindad. Process documentation dan corrective "
         "action menjadi sub-variabel terkuat."),
        ("H2", "IATF 16949 (X2)", "Konsistensi Mutu (Y)",
         0.217, 2.913, 0.004, True,
         "IATF 16949 berpengaruh signifikan positif terhadap konsistensi mutu. "
         "Defect prevention dan supplier quality management terbukti berkontribusi "
         "pada penurunan variasi antar batch."),
        ("H3", "Engineering Lifecycle (X3)", "Konsistensi Mutu (Y)",
         0.532, 6.124, 0.000, True,
         "Engineering Lifecycle berpengaruh dominan terhadap konsistensi mutu "
         "(β=0.532, t=6.124, p<0.001). Change control dan traceability adalah "
         "sub-variabel paling kritis — dibuktikan oleh recurring issues di MAUNG MV3."),
    ]

    for h, from_var, to_var, beta, tstat, pval, accepted, narasi in hipotesis:
        status_color = "#00ff88" if accepted else "#ff3366"
        status_text  = "DITERIMA ✓" if accepted else "DITOLAK ✗"
        is_dominant  = h == "H3"
        border_color = "#00ff88" if is_dominant else "#00d4ff"

        st.markdown(
            f'<div style="padding:1.25rem 1.5rem;background:#111827;'
            f'border:1px solid {border_color}33;border-left:5px solid {border_color};'
            f'border-radius:10px;margin-bottom:1rem;">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start;'
            f'flex-wrap:wrap;gap:.5rem;margin-bottom:.75rem;">'
            f'<div>'
            f'<span style="font-family:Rajdhani;font-size:1.3rem;font-weight:700;'
            f'color:{border_color};">{h}</span>'
            f'<span style="font-size:.85rem;color:#c5d5e8;margin-left:.75rem;">'
            f'{from_var} → {to_var}</span>'
            f'{"<span style=\"background:rgba(0,255,136,.15);border:1px solid rgba(0,255,136,.4);border-radius:4px;padding:2px 8px;font-size:.65rem;color:#00ff88;font-family:Rajdhani;font-weight:700;margin-left:.5rem;\">DOMINAN</span>" if is_dominant else ""}'
            f'</div>'
            f'<span style="background:{status_color}22;border:1px solid {status_color}55;'
            f'border-radius:6px;padding:3px 12px;font-family:Rajdhani;font-size:.85rem;'
            f'font-weight:700;color:{status_color};">{status_text}</span>'
            f'</div>'
            f'<div style="display:flex;gap:2rem;margin-bottom:.75rem;flex-wrap:wrap;">'
            f'<div><span style="font-size:.65rem;color:#4a6fa5;text-transform:uppercase;'
            f'letter-spacing:1px;">Koefisien (β)</span><br>'
            f'<span style="font-family:Rajdhani;font-size:1.4rem;font-weight:700;'
            f'color:{border_color};">{beta}</span></div>'
            f'<div><span style="font-size:.65rem;color:#4a6fa5;text-transform:uppercase;'
            f'letter-spacing:1px;">T-Statistik</span><br>'
            f'<span style="font-family:Rajdhani;font-size:1.4rem;font-weight:700;'
            f'color:#ffd700;">{tstat}</span></div>'
            f'<div><span style="font-size:.65rem;color:#4a6fa5;text-transform:uppercase;'
            f'letter-spacing:1px;">P-Value</span><br>'
            f'<span style="font-family:Rajdhani;font-size:1.4rem;font-weight:700;'
            f'color:#00ff88;">{pval}</span></div>'
            f'<div><span style="font-size:.65rem;color:#4a6fa5;text-transform:uppercase;'
            f'letter-spacing:1px;">Signifikansi (α=0.05)</span><br>'
            f'<span style="font-family:Rajdhani;font-size:1.4rem;font-weight:700;'
            f'color:#00ff88;">{"Signifikan ✓" if pval < 0.05 else "Tidak Signifikan"}</span></div>'
            f'</div>'
            f'<div style="font-size:.83rem;color:#c5d5e8;line-height:1.65;'
            f'padding-top:.5rem;border-top:1px solid rgba(255,255,255,0.06);">{narasi}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")

    # ── Model Struktural Visual ────────────────────────────
    st.markdown("#### 🗺️ Model Struktural PLS-SEM")
    col_path, col_r2 = st.columns([2, 1])

    with col_path:
        fig = go.Figure()

        # Variabel eksogen
        boxes = {
            "ISO 9001\n(X1)":              (0.1, 0.85, "#00d4ff", "β=0.318***"),
            "IATF 16949\n(X2)":            (0.1, 0.50, "#0066ff", "β=0.217**"),
            "Engineering\nLifecycle (X3)": (0.1, 0.15, "#00ff88", "β=0.532***"),
            "Konsistensi\nMutu (Y)":        (0.75, 0.50, "#ffd700", f"R²={R2}"),
        }
        colors_map = {
            "ISO 9001\n(X1)":              "#00d4ff",
            "IATF 16949\n(X2)":            "#0066ff",
            "Engineering\nLifecycle (X3)": "#00ff88",
            "Konsistensi\nMutu (Y)":        "#ffd700",
        }

        # Draw arrows
        arrow_specs = [
            (0.1, 0.85, "#00d4ff", "β=0.318***"),
            (0.1, 0.50, "#0066ff", "β=0.217**"),
            (0.1, 0.15, "#00ff88", "β=0.532***"),
        ]
        for (x_start, y_start, c, label) in arrow_specs:
            fig.add_annotation(
                x=0.72, y=0.50, ax=x_start+0.18, ay=y_start,
                xref="paper", yref="paper", axref="paper", ayref="paper",
                arrowhead=2, arrowsize=1.2, arrowwidth=2.5, arrowcolor=c,
                text="", showarrow=True
            )
            mid_x = (x_start + 0.18 + 0.72) / 2
            mid_y = (y_start + 0.50) / 2
            fig.add_annotation(
                x=mid_x, y=mid_y + 0.04,
                xref="paper", yref="paper",
                text=f"<b>{label}</b>",
                showarrow=False,
                font=dict(color=c, size=11, family="Rajdhani"),
                bgcolor="rgba(13,19,33,0.8)"
            )

        # Draw boxes
        for name, (bx, by, bc, extra) in boxes.items():
            is_y = "Konsistensi" in name
            fig.add_shape(type="rect",
                x0=bx, y0=by-0.12, x1=bx+0.18, y1=by+0.12,
                xref="paper", yref="paper",
                fillcolor=bc+"22", line=dict(color=bc, width=2),
            )
            fig.add_annotation(
                x=bx+0.09, y=by+0.03,
                xref="paper", yref="paper",
                text=f"<b>{name}</b>",
                showarrow=False,
                font=dict(color=bc, size=11 if is_y else 10, family="Rajdhani"),
                align="center"
            )
            fig.add_annotation(
                x=bx+0.09, y=by-0.07,
                xref="paper", yref="paper",
                text=extra,
                showarrow=False,
                font=dict(color=bc, size=10),
                align="center"
            )

        lay = plotly_layout()
        lay.update(
            height=360,
            xaxis=dict(visible=False), yaxis=dict(visible=False),
            margin=dict(l=10, r=10, t=30, b=10),
            title="Path Diagram PLS-SEM"
        )
        fig.update_layout(**lay)
        st.plotly_chart(fig, use_container_width=True)

    with col_r2:
        st.markdown("<br>", unsafe_allow_html=True)
        metrics = [
            ("R² (Koefisien Determinasi)", R2, "#ffd700",
             "72.9% variasi konsistensi mutu dapat dijelaskan oleh ketiga variabel"),
            ("Q² (Predictive Relevance)", Q2, "#00ff88",
             "Model memiliki relevansi prediktif yang baik (Q²>0)"),
        ]
        for label, val, color, desc in metrics:
            st.markdown(
                f'<div style="padding:.85rem 1rem;background:#111827;'
                f'border:1px solid {color}33;border-left:3px solid {color};'
                f'border-radius:8px;margin-bottom:.75rem;">'
                f'<div style="font-size:.65rem;color:#4a6fa5;letter-spacing:1px;'
                f'text-transform:uppercase;">{label}</div>'
                f'<div style="font-family:Rajdhani;font-size:2.2rem;font-weight:700;'
                f'color:{color};line-height:1;">{val}</div>'
                f'<div style="font-size:.72rem;color:#7a9bb5;margin-top:.3rem;">{desc}</div>'
                f'</div>', unsafe_allow_html=True)

        # Kontribusi pie
        fig_pie = go.Figure(go.Pie(
            labels=["X3 Lifecycle\nβ=0.532","X1 ISO 9001\nβ=0.318","X2 IATF\nβ=0.217"],
            values=[0.532, 0.318, 0.217],
            hole=0.5,
            marker=dict(colors=["#00ff88","#00d4ff","#0066ff"]),
        ))
        lay_pie = plotly_layout()
        lay_pie.update(height=220, margin=dict(l=5,r=5,t=30,b=5),
                       title="Distribusi Koefisien")
        fig_pie.update_layout(**lay_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # ── Validitas & Reliabilitas ───────────────────────────
    st.markdown("#### 🔬 Uji Validitas & Reliabilitas (Outer Model)")

    tab1, tab2, tab3 = st.tabs(["📐 Convergent Validity (AVE)",
                                  "🔗 Composite Reliability (CR)",
                                  "α Cronbach Alpha"])

    vars_order = ["X1 — ISO 9001", "X2 — IATF 16949",
                  "X3 — Engineering Lifecycle", "Y — Konsistensi Mutu"]
    ave_vals = [0.624, 0.587, 0.671, 0.612]
    cr_vals  = [0.891, 0.857, 0.908, 0.884]
    ca_vals  = [0.852, 0.801, 0.876, 0.841]

    def stat_bars(vals, threshold, label, color):
        fig = go.Figure()
        bar_colors = [color if v >= threshold else "#ff3366" for v in vals]
        fig.add_trace(go.Bar(
            x=vars_order, y=vals,
            marker=dict(color=bar_colors, opacity=0.85),
            text=[f"{v:.3f}" for v in vals], textposition="outside"
        ))
        fig.add_hline(y=threshold, line_dash="dash", line_color="#ffd700",
                      annotation_text=f"Threshold {threshold}",
                      annotation_font_color="#ffd700")
        lay = plotly_layout()
        lay.update(height=300, yaxis=dict(**lay["yaxis"], range=[0, max(vals)*1.2]),
                   title=label)
        fig.update_layout(**lay)
        return fig

    with tab1:
        st.info("AVE > 0.5 = Convergent Validity terpenuhi ✓")
        st.plotly_chart(stat_bars(ave_vals, 0.5, "Average Variance Extracted (AVE)", "#00d4ff"),
                        use_container_width=True)
    with tab2:
        st.info("CR > 0.7 = Composite Reliability terpenuhi ✓")
        st.plotly_chart(stat_bars(cr_vals, 0.7, "Composite Reliability (CR)", "#00ff88"),
                        use_container_width=True)
    with tab3:
        st.info("Cronbach Alpha > 0.7 = Reliabilitas terpenuhi ✓")
        st.plotly_chart(stat_bars(ca_vals, 0.7, "Cronbach Alpha (CA)", "#ffd700"),
                        use_container_width=True)

    st.markdown("---")

    # ── Kesimpulan Narasi ──────────────────────────────────
    st.markdown("#### 📝 Kesimpulan Penelitian")

    kesimpulan = [
        ("1", "#00ff88",
         "Engineering Lifecycle adalah faktor DOMINAN (β=0.532)",
         "Dari ketiga variabel independen, Engineering Lifecycle (X3) terbukti "
         "memiliki pengaruh terbesar dan signifikan terhadap konsistensi mutu produksi "
         "MAUNG MV3 (β=0.532, t=6.124, p<0.001). Ini berarti penguatan change control, "
         "design control, dan traceability memberikan dampak terbesar pada peningkatan "
         "konsistensi mutu kendaraan taktis PT Pindad."),
        ("2", "#00d4ff",
         "ISO 9001 berpengaruh signifikan positif (β=0.318)",
         "Implementasi ISO 9001 berkontribusi nyata terhadap konsistensi mutu (H1 diterima). "
         "Audit internal yang sistematis dan pengendalian dokumen terbukti mengurangi "
         "variasi defect antar batch produksi."),
        ("3", "#0066ff",
         "IATF 16949 berpengaruh signifikan positif (β=0.217)",
         "Standar IATF 16949 yang berfokus pada industri otomotif berpengaruh positif "
         "terhadap konsistensi mutu (H2 diterima). Meskipun koefisiennya terkecil, "
         "defect prevention dan supplier quality management tetap berkontribusi signifikan."),
        ("4", "#ffd700",
         "Model PLS-SEM menjelaskan 72.9% variasi konsistensi mutu (R²=0.729)",
         "Ketiga variabel bersama-sama mampu menjelaskan 72.9% variasi konsistensi mutu "
         "produksi MAUNG MV3. Nilai ini tergolong kuat dalam penelitian manajemen kualitas, "
         "mengindikasikan model yang dibangun relevan dan dapat diandalkan untuk "
         "pengambilan keputusan strategis."),
        ("5", "#a78bfa",
         "Rekomendasi: Prioritaskan penguatan Engineering Lifecycle Change Control",
         "Bukti dari MoM Batch 1-9 menunjukkan bahwa recurring issues (selang wiper 8 batch, "
         "tuas engine hood 6 batch) terjadi karena corrective action tidak diintegrasikan ke "
         "dalam sistem engineering change control. Rekomendasi: implementasi ECO (Engineering "
         "Change Order) yang terdigitalisasi dan terintegrasi dengan sistem MAUNG Platform."),
    ]

    for num, color, title, text in kesimpulan:
        st.markdown(
            f'<div style="padding:1rem 1.25rem;background:#111827;'
            f'border:1px solid {color}22;border-radius:10px;margin-bottom:.75rem;'
            f'display:flex;gap:1rem;">'
            f'<div style="min-width:32px;height:32px;border-radius:50%;'
            f'background:{color}22;border:2px solid {color};display:flex;'
            f'align-items:center;justify-content:center;font-family:Rajdhani;'
            f'font-weight:700;color:{color};font-size:1rem;flex-shrink:0;">{num}</div>'
            f'<div>'
            f'<div style="font-family:Rajdhani;font-size:.95rem;font-weight:700;'
            f'color:{color};margin-bottom:.35rem;">{title}</div>'
            f'<div style="font-size:.83rem;color:#c5d5e8;line-height:1.65;">{text}</div>'
            f'</div></div>',
            unsafe_allow_html=True
        )

    render_footer()
