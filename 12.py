import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIG & SAFE CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="GEO-PVD Pro | Enterprise",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Prompt:wght@400;600;700&display=swap');

    html, body, .stApp {
        font-family: 'Plus Jakarta Sans', 'Prompt', sans-serif;
    }

    /* Top Brand Navigation Bar */
    .brand-navbar {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 41, 59, 0.8) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.25rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    .brand-title {
        font-size: 1.6rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 50%, #C084FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    .brand-badge {
        background: rgba(168, 85, 247, 0.2);
        border: 1px solid rgba(168, 85, 247, 0.5);
        color: #F1F5F9;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
    }

    /* Custom Alert Banners */
    .alert-pass {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #34D399;
        color: #34D399;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }
    .alert-fail {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid #F87171;
        color: #F87171;
        padding: 1rem 1.25rem;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    .info-box {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
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
        <div>
            <span class="brand-title">💎 GEO-PVD STUDIO</span>
            <span class="brand-badge" style="margin-left: 10px;">ENTERPRISE v4.4</span>
        </div>
        <div style="color: #94A3B8; font-size: 0.85rem; font-weight: 600;">
            Geotechnical Soil Consolidation Suite
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.title("🎛️ Control Panel")

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


# 1. Vector SVG: PVD Cross Section Plan
def render_pvd_svg(pattern, S_m, de_m):
    p_text = (
        "Square Grid Layout (de = 1.13S)"
        if pattern == "square"
        else "Triangular Grid Layout (de = 1.05S)"
    )

    svg = f"""
    <svg viewBox="0 0 460 250" width="100%" height="240" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius:12px; border:1px solid rgba(255,255,255,0.1);">
        <defs>
            <radialGradient id="zoneGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#38BDF8;stop-opacity:0.3" />
                <stop offset="100%" style="stop-color:#0F172A;stop-opacity:0" />
            </radialGradient>
            <linearGradient id="pvdGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#38BDF8" />
                <stop offset="100%" style="stop-color:#8B5CF6" />
            </linearGradient>
            <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#38BDF8"/>
            </marker>
        </defs>

        <rect x="15" y="15" width="430" height="220" rx="10" fill="none" stroke="#334155" stroke-dasharray="6 6"/>
        <text x="30" y="40" font-size="12" fill="#F8FAFC" font-weight="700">{p_text}</text>
        <text x="430" y="40" font-size="12" fill="#38BDF8" font-weight="700" text-anchor="end">de = {de_m:.2f} m</text>
        
        <circle cx="230" cy="140" r="70" fill="url(#zoneGlow)" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="4 4"/>
        
        <rect x="130" y="132" width="16" height="16" rx="3" fill="#1E293B" stroke="#64748B" stroke-width="1.5"/>
        <rect x="314" y="132" width="16" height="16" rx="3" fill="#1E293B" stroke="#64748B" stroke-width="1.5"/>
        
        <rect x="222" y="132" width="16" height="16" rx="3" fill="url(#pvdGrad)"/>
        <text x="230" y="168" font-size="11" fill="#F8FAFC" font-weight="700" text-anchor="middle">Center PVD</text>
        
        <line x1="238" y1="140" x2="308" y2="140" stroke="#38BDF8" stroke-width="1.8" marker-end="url(#arrow)"/>
        <rect x="250" y="120" width="55" height="16" rx="4" fill="#020617"/>
        <text x="277" y="132" font-size="10" fill="#38BDF8" font-weight="700" text-anchor="middle">S = {S_m:.2f} m</text>
    </svg>
    """
    return svg


# 2. Vector SVG: Subsurface Clay Layer & PVD Insertion Profile
def render_subsurface_svg(H_m, delta_sig):
    svg = f"""
    <svg viewBox="0 0 460 250" width="100%" height="240" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius:12px; border:1px solid rgba(255,255,255,0.1);">
        <defs>
            <linearGradient id="embankGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#F59E0B;stop-opacity:0.8" />
                <stop offset="100%" style="stop-color:#D97706;stop-opacity:0.9" />
            </linearGradient>
            <linearGradient id="sandGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#FDE047;stop-opacity:0.6" />
                <stop offset="100%" style="stop-color:#CA8A04;stop-opacity:0.6" />
            </linearGradient>
            <linearGradient id="clayGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#1E293B" />
                <stop offset="100%" style="stop-color:#0F172A" />
            </linearGradient>
        </defs>

        <!-- Surcharge / Embankment Fill -->
        <polygon points="50,55 110,25 350,25 410,55" fill="url(#embankGrad)"/>
        <text x="230" y="42" font-size="11" fill="#FFFFFF" font-weight="800" text-anchor="middle">Surcharge Load Δσ = {delta_sig:.0f} kN/m²</text>

        <!-- Sand Blanket / Drainage Layer -->
        <rect x="30" y="55" width="400" height="18" fill="url(#sandGrad)" stroke="#EAB308" stroke-width="0.8"/>
        <text x="230" y="68" font-size="10" fill="#FEF08A" font-weight="700" text-anchor="middle">Sand Drainage Blanket</text>

        <!-- Clay Layer -->
        <rect x="30" y="73" width="400" height="145" fill="url(#clayGrad)" stroke="#334155" stroke-width="1"/>
        <text x="50" y="100" font-size="11" fill="#94A3B8" font-weight="700">Soft Clay Layer</text>
        <text x="50" y="115" font-size="10" fill="#38BDF8" font-weight="700">H = {H_m:.1f} m</text>

        <!-- Vertical PVD Drains Installed -->
        <line x1="120" y1="55" x2="120" y2="210" stroke="#38BDF8" stroke-width="3.5" stroke-dasharray="8 3"/>
        <line x1="190" y1="55" x2="190" y2="210" stroke="#38BDF8" stroke-width="3.5" stroke-dasharray="8 3"/>
        <line x1="260" y1="55" x2="260" y2="210" stroke="#38BDF8" stroke-width="3.5" stroke-dasharray="8 3"/>
        <line x1="330" y1="55" x2="330" y2="210" stroke="#38BDF8" stroke-width="3.5" stroke-dasharray="8 3"/>
        <line x1="400" y1="55" x2="400" y2="210" stroke="#38BDF8" stroke-width="3.5" stroke-dasharray="8 3"/>

        <!-- Flow Direction Arrows -->
        <text x="260" y="145" font-size="12" fill="#38BDF8" font-weight="800" text-anchor="middle">💧 Radial Flow to PVDs</text>

        <!-- Impermeable Base -->
        <rect x="30" y="218" width="400" height="15" fill="#1E293B"/>
        <text x="230" y="230" font-size="10" fill="#64748B" font-weight="600" text-anchor="middle">Firm Stratum / Impermeable Base</text>
    </svg>
    """
    return svg


# ==========================================
# 5. MAIN DASHBOARD LAYOUT
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
        # 5.1 Native Streamlit Metrics
        u_percent = results["Uav"] * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            with st.container(border=True):
                st.metric(
                    label="⚡ Average Consolidation (Uav)",
                    value=f"{u_percent:.2f}%",
                    delta="Degree of Consolidation",
                )
        with col2:
            with st.container(border=True):
                st.metric(
                    label="🎯 Ultimate Settlement (S_final)",
                    value=f"{results['S_final']*100:.1f} cm",
                    delta="Primary Settlement",
                )
        with col3:
            with st.container(border=True):
                st.metric(
                    label=f"⏳ Settlement at Day {t_days} (St)",
                    value=f"{results['St']*100:.1f} cm",
                    delta=f"{u_percent:.1f}% Completed",
                )

        # 5.2 Status Banner
        if u_percent >= 90:
            st.markdown(
                f"""
                <div class="alert-pass">
                    🎉 <b>DESIGN PASSED:</b> การอัดตัวคายน้ำทำได้ถึง <b>{u_percent:.2f}%</b> ซึ่งสูงกว่าเกณฑ์มาตรฐานวิศวกรรม (≥ 90%)
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="alert-fail">
                    🚨 <b>DESIGN WARNING:</b> การอัดตัวคายน้ำทำได้เพียง <b>{u_percent:.2f}%</b> (ต่ำกว่าเกณฑ์ 90%) แนะนำให้ลดระยะห่าง S
                </div>
            """,
                unsafe_allow_html=True,
            )

        # 5.3 Engineering Schematics (100% Native SVG - Always Loads!)
        st.subheader("🖼️ Engineering Schematics & Subsurface Model")
        img_col1, img_col2 = st.columns(2)

        with img_col1:
            st.markdown(
                """
                <div class="info-box">
                    <div style="font-weight:700; color:#F8FAFC;">📱 Dynamic Cross-Section Diagram</div>
                    <div style="font-size:0.8rem; color:#94A3B8;">ผังแสดงระยะห่าง PVD และรัศมีอิทธิพล (Zone of Influence)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
            svg_plan = render_pvd_svg(pattern, S, results["de_m"])
            st.markdown(svg_plan, unsafe_allow_html=True)

        with img_col2:
            st.markdown(
                """
                <div class="info-box">
                    <div style="font-weight:700; color:#F8FAFC;">🏞️ Subsurface Profile Diagram</div>
                    <div style="font-size:0.8rem; color:#94A3B8;">แบบจำลองชั้นดินเหนียวอ่อนและการติดตั้ง PVD</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
            svg_profile = render_subsurface_svg(H_clay, delta_sigma)
            st.markdown(svg_profile, unsafe_allow_html=True)

        # 5.4 Intermediate Metrics Grid
        with st.expander(
            "📐 ตัวแปรคำนวณระหว่างทางเพิ่มเติม (Intermediate Parameters)"
        ):
            m1, m2, m3 = st.columns(3)
            m1.metric("Equivalent Dia. (dw)", f"{results['dw']:.2f} cm")
            m2.metric("Influence Dia. (de)", f"{results['de_m']:.2f} m")
            m3.metric("Spacing Factor (n)", f"{results['n']:.2f}")

            m4, m5, m6 = st.columns(3)
            m4.metric("Drain Factor F(n)", f"{results['Fn']:.3f}")
            m5.metric("Radial Consolidation (Ur)", f"{results['Ur']*100:.1f}%")
            m6.metric(
                "Vertical Consolidation (Uv)", f"{results['Uv']*100:.1f}%"
            )

        # 5.5 Analytics Charts
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
            font=dict(size=12, color="#94A3B8"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.6)",
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified",
            xaxis=dict(
                showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)", title="Time (Days)"
            ),
            yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.05)"),
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
                    fillcolor="rgba(56, 189, 248, 0.1)",
                    line=dict(color="#38BDF8", width=3),
                )
            )
            fig1.add_hline(
                y=90,
                line_dash="dash",
                line_color="#34D399",
                line_width=2,
                annotation_text="90% Target",
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
                    fillcolor="rgba(244, 63, 94, 0.1)",
                    line=dict(color="#F43F5E", width=3),
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
