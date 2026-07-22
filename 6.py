import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIG & CLEAN DARK ENGINE (FIXED)
# ==========================================
st.set_page_config(
    page_title="GEO-PVD Pro | Next-Gen Suite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Prompt:wght@300;400;500;600;700&display=swap');

    /* 1. Safe Global Typography (Do NOT override generic div/span to prevent icon glitches) */
    html, body, .stApp, h1, h2, h3, h4, h5, h6, p, label {
        font-family: 'Plus Jakarta Sans', 'Prompt', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* 2. Preserve Streamlit Native Material Icons */
    [data-testid="stIconMaterial"], 
    [data-testid="stExpanderToggleIcon"],
    .material-symbols-outlined,
    i {
        font-family: 'Material Symbols Outlined', 'Material Icons' !important;
    }

    /* Ambient Background Glow */
    .stApp {
        background-color: #05070A !important;
        background-image: 
            radial-gradient(at 15% 15%, rgba(56, 189, 248, 0.08) 0px, transparent 45%),
            radial-gradient(at 85% 20%, rgba(139, 92, 246, 0.08) 0px, transparent 45%),
            radial-gradient(at 50% 85%, rgba(236, 72, 153, 0.05) 0px, transparent 50%);
        background-attachment: fixed;
        color: #F8FAFC;
    }

    /* Sidebar Clean Layout */
    section[data-testid="stSidebar"] {
        background: rgba(8, 12, 20, 0.85) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }

    /* Expander UI Fix (Clean Flex Layout) */
    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        margin-bottom: 0.8rem !important;
        overflow: hidden;
    }

    /* Custom Input Glowing Borders */
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background-color: rgba(15, 23, 42, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: #F8FAFC !important;
    }
    div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
        border-color: #38BDF8 !important;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.25) !important;
    }

    /* Top Brand Navigation Bar */
    .brand-navbar {
        background: rgba(13, 18, 30, 0.75);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.2rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    }
    .brand-title {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 12px;
        line-height: 1.2;
    }
    .brand-badge {
        background: rgba(168, 85, 247, 0.15);
        border: 1px solid rgba(168, 85, 247, 0.4);
        color: #E2E8F0;
        padding: 0.3rem 0.8rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    /* Glass Metric Cards */
    .glass-card {
        background: rgba(13, 18, 30, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(16px);
    }
    .stat-label {
        font-size: 0.8rem;
        color: #94A3B8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.4rem;
    }
    .stat-value {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 0.3rem 0;
        letter-spacing: -1px;
    }
    .stat-sub {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 500;
    }

    /* Accent Lines */
    .glow-cyan { background: linear-gradient(90deg, #38BDF8, #818CF8); height: 3px; width: 100%; position: absolute; top:0; left:0; }
    .glow-emerald { background: linear-gradient(90deg, #34D399, #059669); height: 3px; width: 100%; position: absolute; top:0; left:0; }
    .glow-pink { background: linear-gradient(90deg, #F43F5E, #FB7185); height: 3px; width: 100%; position: absolute; top:0; left:0; }

    /* Content Box Containers */
    .content-box {
        background: rgba(13, 18, 30, 0.55);
        border-radius: 18px;
        padding: 1.25rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
    }

    /* Status Banners */
    .alert-pass {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(52, 211, 153, 0.3);
        color: #34D399;
        padding: 1rem 1.5rem;
        border-radius: 16px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .alert-fail {
        background: rgba(239, 68, 68, 0.08);
        border: 1px solid rgba(248, 113, 113, 0.3);
        color: #F87171;
        padding: 1rem 1.5rem;
        border-radius: 16px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    /* Metric Grid Cards */
    .metric-grid-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 14px;
        padding: 1rem;
        text-align: center;
    }
    .metric-grid-title { font-size: 0.75rem; color: #94A3B8; font-weight: 600; margin-bottom: 0.2rem; }
    .metric-grid-val { font-size: 1.25rem; color: #F8FAFC; font-weight: 800; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. BRAND NAVIGATION NAVBAR
# ==========================================
st.markdown(
    """
    <div class="brand-navbar">
        <div class="brand-title">
            <span>💎 GEO-PVD <span style="font-weight:300; opacity:0.75;">STUDIO</span></span>
            <span class="brand-badge">PRO v4.2</span>
        </div>
        <div style="color: #64748B; font-size: 0.85rem; font-weight: 600;">
            Geotechnical Soil Consolidation Suite
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("### 🎛️ Control Panel")

with st.sidebar.expander("📌 1. PVD & Grid Layout", expanded=True):
    S = st.number_input(
        "Spacing : S (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1
    )
    pattern = st.selectbox(
        "Grid Pattern",
        ["square", "triangular"],
        format_func=lambda x: "Square Grid"
        if x == "square"
        else "Triangular Grid",
    )
    b = st.number_input("PVD Width : b (cm)", value=10.0, step=0.5)
    a = st.number_input("PVD Thickness : a (cm)", value=0.5, step=0.1)

with st.sidebar.expander("🧱 2. Soil & Drainage Profile", expanded=True):
    cv = st.number_input("Cv (cm²/day)", value=20.0, step=1.0)
    kr_kv = st.number_input("Ratio kr/kv", value=7.0, step=0.5)
    H_clay = st.number_input(
        "Clay Depth : H (m)", min_value=0.1, value=30.0, step=1.0
    )
    drainage_type = st.selectbox(
        "Drainage Path",
        ["Double Drainage (2-Way)", "Single Drainage (1-Way)"],
    )
    t_days = st.slider("Analysis Period : t (Days)", 10, 365, 90, 5)

with st.sidebar.expander("📊 3. Compressibility Index", expanded=False):
    Cc = st.number_input("Cc (Compression Index)", value=0.29, step=0.01)
    e0 = st.number_input("e0 (Initial Void Ratio)", value=1.10, step=0.05)
    sigma0 = st.number_input("Initial Stress : σ'0 (kN/m²)", value=40.0, step=5.0)
    delta_sigma = st.number_input(
        "Surcharge Load : Δσ (kN/m²)", value=80.0, step=5.0
    )


# ==========================================
# 4. ENGINE & HELPER FUNCTIONS
# ==========================================
def calculate_pvd(
    S,
    pattern,
    a,
    b,
    cv,
    kr_kv,
    H_clay,
    drainage_type,
    t,
    Cc,
    e0,
    sigma0,
    delta_sigma,
):
    dw = (a + b) / 2.0
    de_m = 1.13 * S if pattern == "square" else 1.05 * S
    de_cm = de_m * 100.0

    n = de_cm / dw
    if n <= 1:
        return None, "ระยะห่าง PVD เล็กเกินไปเมื่อเทียบกับหน้าตัด"

    Fn = ((n**2) / (n**2 - 1)) * math.log(n) - ((3 * n**2 - 1) / (4 * n**2))
    Cr = kr_kv * cv
    Tr = (Cr * t) / (de_cm**2)
    Ur = 1.0 - math.exp((-8.0 * Tr) / Fn)

    Hdr_cm = (
        (H_clay / 2.0) * 100.0 if "Double" in drainage_type else H_clay * 100.0
    )
    Tv = (cv * t) / (Hdr_cm**2)

    if Tv <= 0.282:
        Uv = math.sqrt(4.0 * Tv) / math.pi
    else:
        Uv = 1.0 - (8.0 / (math.pi**2)) * math.exp(-((math.pi**2) / 4.0) * Tv)

    Uav = 1.0 - (1.0 - Ur) * (1.0 - Uv)
    S_final = H_clay * (Cc / (1.0 + e0)) * math.log10(
        (sigma0 + delta_sigma) / sigma0
    )
    St = Uav * S_final

    return {
        "dw": dw,
        "de_m": de_m,
        "n": n,
        "Fn": Fn,
        "Ur": Ur,
        "Uv": Uv,
        "Uav": Uav,
        "S_final": S_final,
        "St": St,
    }, None


def render_pvd_svg(pattern, S_m, de_m):
    p_text = (
        "Square Grid Layout (de = 1.13S)"
        if pattern == "square"
        else "Triangular Grid Layout (de = 1.05S)"
    )

    svg = f"""
    <svg viewBox="0 0 460 270" width="100%" height="250" xmlns="http://www.w3.org/2000/svg" style="background:#090D16; border-radius:16px; border:1px solid rgba(255,255,255,0.08);">
        <defs>
            <radialGradient id="zoneGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#38BDF8;stop-opacity:0.25" />
                <stop offset="100%" style="stop-color:#090D16;stop-opacity:0" />
            </radialGradient>
            <linearGradient id="pvdGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#38BDF8" />
                <stop offset="100%" style="stop-color:#8B5CF6" />
            </linearGradient>
            <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#38BDF8"/>
            </marker>
        </defs>

        <rect x="15" y="15" width="430" height="240" rx="12" fill="none" stroke="#1E293B" stroke-dasharray="6 6" stroke-width="1.5"/>
        
        <text x="30" y="42" font-size="13" fill="#F8FAFC" font-weight="700">{p_text}</text>
        <text x="430" y="42" font-size="12" fill="#38BDF8" font-weight="700" text-anchor="end">de = {de_m:.2f} m</text>
        
        <circle cx="230" cy="150" r="75" fill="url(#zoneGlow)" stroke="#38BDF8" stroke-width="1.8" stroke-dasharray="5 4"/>
        <text x="230" y="65" font-size="11" fill="#94A3B8" font-weight="600" text-anchor="middle">Zone of Influence</text>
        
        <rect x="125" y="142" width="16" height="16" rx="3" fill="#1E293B" stroke="#475569" stroke-width="1.5"/>
        <rect x="319" y="142" width="16" height="16" rx="3" fill="#1E293B" stroke="#475569" stroke-width="1.5"/>
        
        <rect x="222" y="142" width="16" height="16" rx="3" fill="url(#pvdGrad)"/>
        <text x="230" y="178" font-size="11" fill="#F8FAFC" font-weight="700" text-anchor="middle">Center PVD</text>
        
        <line x1="238" y1="150" x2="313" y2="150" stroke="#38BDF8" stroke-width="1.8" marker-end="url(#arrow)"/>
        <rect x="250" y="128" width="60" height="18" rx="4" fill="#0F172A" stroke="#334155" stroke-width="1"/>
        <text x="280" y="141" font-size="10" fill="#38BDF8" font-weight="800" text-anchor="middle">S = {S_m:.2f} m</text>
    </svg>
    """
    return svg


# ==========================================
# 5. DASHBOARD MAIN CONTENT
# ==========================================
if S <= 0 or H_clay <= 0 or sigma0 <= 0:
    st.error("⚠️ Invalid Parameters: S, H, and σ'0 must be greater than zero.")
else:
    results, err_msg = calculate_pvd(
        S,
        pattern,
        a,
        b,
        cv,
        kr_kv,
        H_clay,
        drainage_type,
        t_days,
        Cc,
        e0,
        sigma0,
        delta_sigma,
    )

    if err_msg:
        st.error(f"⚠️ Calculation Error: {err_msg}")
    else:
        # 5.1 Top Stat Cards Dashboard
        c1, c2, c3 = st.columns(3)
        u_percent = results["Uav"] * 100

        with c1:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="glow-cyan"></div>
                    <div class="stat-label">⚡ Average Consolidation</div>
                    <div class="stat-value" style="color: #38BDF8;">{u_percent:.2f}%</div>
                    <div class="stat-sub">Degree of Consolidation (Uav)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="glow-emerald"></div>
                    <div class="stat-label">🎯 Ultimate Settlement</div>
                    <div class="stat-value" style="color: #34D399;">{results['S_final']*100:.1f} <span style="font-size:1.1rem; font-weight:600;">cm</span></div>
                    <div class="stat-sub">Total primary consolidation (S_final)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="glow-pink"></div>
                    <div class="stat-label">⏳ Current Settlement (Day {t_days})</div>
                    <div class="stat-value" style="color: #F43F5E;">{results['St']*100:.1f} <span style="font-size:1.1rem; font-weight:600;">cm</span></div>
                    <div class="stat-sub">Predicted settlement at time t</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.2 Status Alert Banner
        if u_percent >= 90:
            st.markdown(
                f"""
                <div class="alert-pass">
                    <span>🎉</span> <div><b>DESIGN PASSED:</b> การอัดตัวคายน้ำทำได้ถึง <b>{u_percent:.2f}%</b> ซึ่งสูงกว่าเกณฑ์มาตรฐานวิศวกรรม (≥ 90%)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="alert-fail">
                    <span>🚨</span> <div><b>DESIGN WARNING:</b> การอัดตัวคายน้ำทำได้เพียง <b>{u_percent:.2f}%</b> (ต่ำกว่าเกณฑ์ 90%) แนะนำให้ลดระยะห่าง S</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.3 Visual Diagrams Section
        st.subheader("🖼️ Engineering Schematics & Subsurface Model")
        img_col1, img_col2 = st.columns(2)

        with img_col1:
            st.markdown(
                """
                <div class="content-box">
                    <div style="font-weight:700; color:#F8FAFC; margin-bottom:0.2rem;">📱 Dynamic Cross-Section Diagram</div>
                    <div style="font-size:0.8rem; color:#64748B;">ผังแสดงระยะห่าง PVD และรัศมีอิทธิพล (Zone of Influence)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
            svg_code = render_pvd_svg(pattern, S, results["de_m"])
            st.html(svg_code)

        with img_col2:
            st.markdown(
                """
                <div class="content-box">
                    <div style="font-weight:700; color:#F8FAFC; margin-bottom:0.2rem;">🏞️ Subsurface Profile Diagram</div>
                    <div style="font-size:0.8rem; color:#64748B;">แบบจำลองชั้นดินเหนียวอ่อนและการติดตั้ง PVD</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
            st.image(
                "https://images.unsplash.com/photo-1581094184920-7a72da566411?auto=format&fit=crop&w=800&q=80",
                caption="Soil Consolidation & PVD Drainage Mechanism",
                use_container_width=True,
            )

        # 5.4 Intermediate Calculations Grid
        with st.expander(
            "📐 ตัวแปรคำนวณระหว่างทางเพิ่มเติม (Intermediate Parameters)"
        ):
            m1, m2, m3, m4, m5, m6 = st.columns(6)
            m1.markdown(
                f'<div class="metric-grid-card"><div class="metric-grid-title">Equiv. Dia. (dw)</div><div class="metric-grid-val">{results["dw"]:.2f} cm</div></div>',
                unsafe_allow_html=True,
            )
            m2.markdown(
                f'<div class="metric-grid-card"><div class="metric-grid-title">Influence Dia. (de)</div><div class="metric-grid-val">{results["de_m"]:.2f} m</div></div>',
                unsafe_allow_html=True,
            )
            m3.markdown(
                f'<div class="metric-grid-card"><div class="metric-grid-title">Spacing Factor (n)</div><div class="metric-grid-val">{results["n"]:.2f}</div></div>',
                unsafe_allow_html=True,
            )
            m4.markdown(
                f'<div class="metric-grid-card"><div class="metric-grid-title">Drain Factor F(n)</div><div class="metric-grid-val">{results["Fn"]:.3f}</div></div>',
                unsafe_allow_html=True,
            )
            m5.markdown(
                f'<div class="metric-grid-card"><div class="metric-grid-title">Radial Consol. (Ur)</div><div class="metric-grid-val">{results["Ur"]*100:.1f}%</div></div>',
                unsafe_allow_html=True,
            )
            m6.markdown(
                f'<div class="metric-grid-card"><div class="metric-grid-title">Vertical Consol. (Uv)</div><div class="metric-grid-val">{results["Uv"]*100:.1f}%</div></div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.5 Next-Gen Analytics Charts
        st.subheader("📈 Time-Consolidation Analytics")

        days_array = np.arange(1, 366)
        u_av_list, st_list = [], []

        for d in days_array:
            res, _ = calculate_pvd(
                S,
                pattern,
                a,
                b,
                cv,
                kr_kv,
                H_clay,
                drainage_type,
                d,
                Cc,
                e0,
                sigma0,
                delta_sigma,
            )
            u_av_list.append(res["Uav"] * 100)
            st_list.append(res["St"] * 100)

        tab1, tab2 = st.tabs(
            ["💧 Consolidation Rate Curve", "📉 Settlement Curve"]
        )

        chart_layout = dict(
            font=dict(
                family="Plus Jakarta Sans, Prompt, sans-serif",
                size=12,
                color="#94A3B8",
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(9, 13, 22, 0.6)",
            margin=dict(l=25, r=25, t=30, b=25),
            hovermode="x unified",
            xaxis=dict(
                showgrid=True,
                gridcolor="rgba(255, 255, 255, 0.05)",
                title="Time (Days)",
                color="#94A3B8",
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255, 255, 255, 0.05)",
                color="#94A3B8",
            ),
        )

        with tab1:
            fig1 = go.Figure()
            fig1.add_trace(
                go.Scatter(
                    x=days_array,
                    y=u_av_list,
                    mode="lines",
                    name="Uav (%)",
                    line_shape="spline",
                    fill="tozeroy",
                    fillcolor="rgba(56, 189, 248, 0.08)",
                    line=dict(color="#38BDF8", width=3.5),
                )
            )
            fig1.add_hline(
                y=90,
                line_dash="dash",
                line_color="#34D399",
                line_width=2,
                annotation_text="90% Target",
                annotation_position="bottom right",
            )
            fig1.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="#F43F5E",
                line_width=2,
                annotation_text=f"Day {t_days}",
            )
            fig1.update_layout(
                **chart_layout,
                yaxis_title="Degree of Consolidation Uav (%)",
                yaxis_range=[0, 105],
            )
            st.plotly_chart(fig1, use_container_width=True)

        with tab2:
            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=days_array,
                    y=st_list,
                    mode="lines",
                    name="Settlement (cm)",
                    line_shape="spline",
                    fill="tozeroy",
                    fillcolor="rgba(244, 63, 94, 0.08)",
                    line=dict(color="#F43F5E", width=3.5),
                )
            )
            fig2.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="#38BDF8",
                line_width=2,
                annotation_text=f"Day {t_days}",
            )
            fig2.update_layout(
                **chart_layout,
                yaxis_title="Settlement St (cm)",
                yaxis_autorange="reversed",
            )
            st.plotly_chart(fig2, use_container_width=True)
