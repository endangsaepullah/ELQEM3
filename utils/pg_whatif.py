import streamlit as st
import plotly.graph_objects as go
import numpy as np
from utils.styles import section_header, plotly_layout, render_footer


# Koefisien jalur PLS-SEM dari hasil penelitian
COEF = {"X1": 0.318, "X2": 0.217, "X3": 0.532}
R2   = 0.729
INTERCEPT = 100 * (1 - sum(COEF.values()))  # baseline

# Nilai aktual dari evaluasi platform (rata-rata)
BASELINE = {"X1": 74.2, "X2": 71.8, "X3": 68.5}


def predict_y(x1, x2, x3):
    raw = COEF["X1"]*x1 + COEF["X2"]*x2 + COEF["X3"]*x3
    # Normalize ke skala 0-100
    base = COEF["X1"]*BASELINE["X1"] + COEF["X2"]*BASELINE["X2"] + COEF["X3"]*BASELINE["X3"]
    y = 70 + (raw - base) * (30 / (sum(COEF.values()) * 100 * 0.3))
    return round(min(100, max(0, y)), 2)


def show():
    section_header(
        "Simulasi What-If",
        "Prediksi Konsistensi Mutu Berbasis Model PLS-SEM",
        "🔮"
    )

    # ── Info model ─────────────────────────────────────────
    st.markdown("""
    <div style="padding:.85rem 1.25rem;background:rgba(0,212,255,0.07);
                border:1px solid rgba(0,212,255,0.2);border-radius:8px;
                font-size:.85rem;color:#c5d5e8;line-height:1.65;margin-bottom:1.25rem;">
        <b style="color:#00d4ff;">Model PLS-SEM Tervalidasi</b> —
        Simulasi menggunakan koefisien jalur dari hasil penelitian:
        <b style="color:#00d4ff;">X1 (ISO 9001) β=0.318</b> +
        <b style="color:#0066ff;">X2 (IATF 16949) β=0.217</b> +
        <b style="color:#00ff88;">X3 (Engineering Lifecycle) β=0.532</b> →
        <b style="color:#ffd700;">Y (Konsistensi Mutu)</b> | R²=0.729
    </div>
    """, unsafe_allow_html=True)

    # ── Sliders ────────────────────────────────────────────
    st.markdown("#### 🎛️ Atur Skenario Simulasi")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="padding:.6rem .85rem;background:#111827;border:1px solid rgba(0,212,255,.2);
                    border-left:4px solid #00d4ff;border-radius:8px;margin-bottom:.5rem;">
        <div style="font-family:Rajdhani;color:#00d4ff;font-weight:700;font-size:.9rem;">
        📊 ISO 9001 (X1)</div>
        <div style="font-size:.7rem;color:#7a9bb5;">Process Documentation, Control,<br>
        Internal Audit, Corrective Action</div></div>
        """, unsafe_allow_html=True)
        x1 = st.slider("Skor ISO 9001", 0, 100, int(BASELINE["X1"]),
                        key="x1", help="β=0.318")
        st.markdown(
            f'<div style="text-align:center;font-family:Rajdhani;font-size:2rem;'
            f'font-weight:700;color:#00d4ff;">{x1}</div>', unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="padding:.6rem .85rem;background:#111827;border:1px solid rgba(0,102,255,.2);
                    border-left:4px solid #0066ff;border-radius:8px;margin-bottom:.5rem;">
        <div style="font-family:Rajdhani;color:#0066ff;font-weight:700;font-size:.9rem;">
        🏭 IATF 16949 (X2)</div>
        <div style="font-size:.7rem;color:#7a9bb5;">Risk-Based Thinking, Defect Prevention,<br>
        Supplier Quality, Improvement</div></div>
        """, unsafe_allow_html=True)
        x2 = st.slider("Skor IATF 16949", 0, 100, int(BASELINE["X2"]),
                        key="x2", help="β=0.217")
        st.markdown(
            f'<div style="text-align:center;font-family:Rajdhani;font-size:2rem;'
            f'font-weight:700;color:#0066ff;">{x2}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="padding:.6rem .85rem;background:#111827;border:1px solid rgba(0,255,136,.2);
                    border-left:4px solid #00ff88;border-radius:8px;margin-bottom:.5rem;">
        <div style="font-family:Rajdhani;color:#00ff88;font-weight:700;font-size:.9rem;">
        ⚙️ Engineering Lifecycle (X3) ⭐</div>
        <div style="font-size:.7rem;color:#7a9bb5;">Design Control, Change Control,<br>
        Verification, Traceability</div></div>
        """, unsafe_allow_html=True)
        x3 = st.slider("Skor Engineering Lifecycle", 0, 100, int(BASELINE["X3"]),
                        key="x3", help="β=0.532 — DOMINAN")
        st.markdown(
            f'<div style="text-align:center;font-family:Rajdhani;font-size:2rem;'
            f'font-weight:700;color:#00ff88;">{x3}</div>', unsafe_allow_html=True)

    # ── Hasil prediksi ─────────────────────────────────────
    y_pred    = predict_y(x1, x2, x3)
    y_base    = predict_y(BASELINE["X1"], BASELINE["X2"], BASELINE["X3"])
    delta     = round(y_pred - y_base, 2)
    delta_str = f"+{delta}" if delta >= 0 else str(delta)

    y_color = "#00ff88" if y_pred >= 80 else ("#ffd700" if y_pred >= 70 else
              "#ff6b35" if y_pred >= 60 else "#ff3366")
    y_label = ("Sangat Baik" if y_pred >= 80 else "Baik" if y_pred >= 70 else
               "Cukup" if y_pred >= 60 else "Perlu Perbaikan")

    st.markdown("---")
    st.markdown("#### 📊 Hasil Prediksi")

    rc1, rc2, rc3, rc4 = st.columns(4)
    rc1.metric("Y — Konsistensi Mutu", f"{y_pred}", delta_str)
    rc2.metric("Baseline Aktual", f"{y_base}")
    rc3.metric("Kontribusi X3 (Lifecycle)", f"{round(COEF['X3']*x3, 1)}")
    rc4.metric("R² Model", "0.729")

    st.markdown(
        f'<div style="padding:1.25rem;text-align:center;margin:1rem 0;'
        f'background:linear-gradient(135deg,{y_color}11,{y_color}22);'
        f'border:2px solid {y_color}44;border-radius:12px;">'
        f'<div style="font-size:.75rem;color:#7a9bb5;letter-spacing:2px;'
        f'text-transform:uppercase;">Prediksi Konsistensi Mutu (Y)</div>'
        f'<div style="font-family:Rajdhani;font-size:4rem;font-weight:700;'
        f'color:{y_color};line-height:1.1;">{y_pred}</div>'
        f'<div style="font-size:1rem;color:{y_color};font-weight:600;">{y_label}</div>'
        f'<div style="font-size:.8rem;color:#7a9bb5;margin-top:.35rem;">'
        f'Perubahan dari baseline: <b style="color:{y_color};">{delta_str}</b></div>'
        f'</div>', unsafe_allow_html=True)

    # ── Waterfall kontribusi ────────────────────────────────
    st.markdown("#### 🏗️ Dekomposisi Kontribusi Setiap Variabel")
    col_wf, col_sens = st.columns(2)

    with col_wf:
        contrib_x1 = round(COEF["X1"] * x1, 2)
        contrib_x2 = round(COEF["X2"] * x2, 2)
        contrib_x3 = round(COEF["X3"] * x3, 2)

        fig_wf = go.Figure(go.Bar(
            x=["ISO 9001 (X1)", "IATF 16949 (X2)", "Eng. Lifecycle (X3)", "Total Y"],
            y=[contrib_x1, contrib_x2, contrib_x3, y_pred],
            marker=dict(color=["#00d4ff","#0066ff","#00ff88","#ffd700"], opacity=0.85),
            text=[f"β×s={contrib_x1}", f"β×s={contrib_x2}", f"β×s={contrib_x3}", f"Y={y_pred}"],
            textposition="outside"
        ))
        lay = plotly_layout()
        lay.update(height=320, title="Kontribusi Setiap Variabel ke Y")
        fig_wf.update_layout(**lay)
        st.plotly_chart(fig_wf, use_container_width=True)

    with col_sens:
        # Sensitivity analysis — variasikan X3 saja
        x3_range = list(range(40, 101, 5))
        y_range  = [predict_y(x1, x2, v) for v in x3_range]

        fig_s = go.Figure()
        fig_s.add_trace(go.Scatter(
            x=x3_range, y=y_range,
            mode="lines+markers",
            line=dict(color="#00ff88", width=2.5),
            marker=dict(size=7),
            name="Y vs X3",
            fill="tozeroy", fillcolor="rgba(0,255,136,0.05)"
        ))
        fig_s.add_vline(x=x3, line_color="#ffd700", line_dash="dash",
                        annotation_text=f"X3={x3}", annotation_font_color="#ffd700")
        fig_s.add_hline(y=75, line_color="#00d4ff", line_dash="dot",
                        annotation_text="Target 75", annotation_font_color="#00d4ff")
        lay2 = plotly_layout()
        lay2.update(height=320, title="Sensitivitas Y terhadap X3 (Engineering Lifecycle)")
        fig_s.update_layout(**lay2)
        st.plotly_chart(fig_s, use_container_width=True)

    # ── Skenario Komparasi ─────────────────────────────────
    st.markdown("---")
    st.markdown("#### 🔄 Komparasi Skenario")

    scenarios = {
        "Kondisi Aktual": (BASELINE["X1"], BASELINE["X2"], BASELINE["X3"]),
        "X3 Naik +10":   (BASELINE["X1"], BASELINE["X2"], min(100, BASELINE["X3"]+10)),
        "X3 Naik +20":   (BASELINE["X1"], BASELINE["X2"], min(100, BASELINE["X3"]+20)),
        "Semua Naik +10": (min(100,BASELINE["X1"]+10), min(100,BASELINE["X2"]+10), min(100,BASELINE["X3"]+10)),
        "Skenario Anda":  (x1, x2, x3),
    }
    s_names = list(scenarios.keys())
    s_y     = [predict_y(*v) for v in scenarios.values()]
    s_color = ["#7a9bb5","#0066ff","#00d4ff","#ffd700","#00ff88"]

    fig_comp = go.Figure(go.Bar(
        x=s_names, y=s_y,
        marker=dict(color=s_color, opacity=0.85),
        text=[f"{v:.1f}" for v in s_y], textposition="outside"
    ))
    fig_comp.add_hline(y=75, line_dash="dash", line_color="#ff6b35",
                       annotation_text="Target 75", annotation_font_color="#ff6b35")
    lay3 = plotly_layout()
    lay3.update(height=320, title="Perbandingan Skenario")
    fig_comp.update_layout(**lay3)
    st.plotly_chart(fig_comp, use_container_width=True)

    # ── Implikasi manajerial ───────────────────────────────
    st.markdown("---")
    st.markdown("#### 💡 Implikasi Manajerial")

    x3_needed = BASELINE["X3"]
    while predict_y(x1, x2, x3_needed) < 75 and x3_needed < 100:
        x3_needed += 1
    gap_x3 = max(0, round(x3_needed - BASELINE["X3"], 1))

    col_i1, col_i2 = st.columns(2)
    with col_i1:
        st.markdown(f"""
        <div style="padding:1rem 1.25rem;background:#111827;border:1px solid rgba(0,255,136,.2);
                    border-left:4px solid #00ff88;border-radius:8px;">
        <div style="font-family:Rajdhani;color:#00ff88;font-weight:700;margin-bottom:.4rem;">
        ⚙️ Rekomendasi Utama — Engineering Lifecycle</div>
        <div style="font-size:.84rem;color:#c5d5e8;line-height:1.65;">
        Dengan nilai β=<b style="color:#00ff88;">0.532</b> (dominan), peningkatan
        <b>{gap_x3} poin</b> pada skor Engineering Lifecycle sudah cukup membawa
        konsistensi mutu ke target ≥75.<br><br>
        Fokus pada: <b>Change Control</b>, <b>Design Change Communication</b>,
        dan <b>Traceability</b> sebagai sub-variabel dengan gap terbesar.</div></div>
        """, unsafe_allow_html=True)
    with col_i2:
        pct_x3 = round(COEF["X3"] / sum(COEF.values()) * 100, 1)
        st.markdown(f"""
        <div style="padding:1rem 1.25rem;background:#111827;border:1px solid rgba(255,215,0,.2);
                    border-left:4px solid #ffd700;border-radius:8px;">
        <div style="font-family:Rajdhani;color:#ffd700;font-weight:700;margin-bottom:.4rem;">
        📊 Distribusi Pengaruh</div>
        <div style="font-size:.84rem;color:#c5d5e8;line-height:1.65;">
        <b style="color:#00ff88;">Engineering Lifecycle (X3)</b> berkontribusi
        <b style="color:#00ff88;">{pct_x3}%</b> dari total pengaruh.<br>
        ISO 9001 (X1): {round(COEF['X1']/sum(COEF.values())*100,1)}% &nbsp;|&nbsp;
        IATF 16949 (X2): {round(COEF['X2']/sum(COEF.values())*100,1)}%<br><br>
        <b>Konsekuensi strategis:</b> Investasi pada Engineering Lifecycle
        memberikan ROI terbesar untuk peningkatan konsistensi mutu produksi MAUNG MV3.</div></div>
        """, unsafe_allow_html=True)

    render_footer()
