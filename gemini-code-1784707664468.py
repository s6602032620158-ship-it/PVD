import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & ULTRA-MODERN CSS
# ==========================================
st.set_page_config(
    page_title="GEO-PVD Pro | Geotechnical Engineering Suite",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=Prompt:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', 'Prompt', sans-serif !important;
    }

    .stApp {
        background: #F1F5F9;
    }

    /* Top Navigation / Brand Header */
    .brand-navbar {
        background: #090D16;
        border-bottom: 1px solid #1E293B;
        padding: 1.2rem 2rem;
        border-radius: 16px;
        margin-bottom: 1.8rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2);
    }
    .brand-title {
        font-size: 1.6rem;
        font-weight: 700;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-badge {
        background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Professional Top-Tier Stat Card */
    .stat-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .stat-label {
        font-size: 0.825rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stat-value {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0F172A;
        margin: 0.4rem 0;
    }
    .stat-sub {
        font-size: 0.8rem;
        color: #94A3B8;
    }
    .stat-accent {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
    }

    /* Diagram Section Box */
    .diagram-box {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }

    /* Custom Status Badges */
    .alert-pass {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        color: #166534;
        padding: 1.2rem;
        border-radius: 14px;
        font-weight: 600;
    }
    .alert-fail {
        background: #FEF2F2;
        border: 1px solid #FECACA;
        color: #991B1B;
        padding: 1.2rem;
        border-radius: 14px;
        font-weight: 600;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. BRAND HEADER NAVBAR
# ==========================================
st.markdown(
    """
    <div class="brand-navbar">
        <div class="brand-title">
            <span>🏗️ GEO-PVD <span style="color:#3B82F6;">STUDIO</span></span>
            <span class="brand-badge">ENTERPRISE v3.0</span>
        </div>
        <div style="color: #94A3B8; font-size: 0.85rem;">
            Advanced Ground Improvement & Settlement Simulator
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("### 🎛️ Control Panel")

with st.sidebar.expander("📍 1. PVD & Grid Configuration", expanded=True):
    S = st.number_input(
        "Spacing : S (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1
    )
    pattern = st.selectbox(
        "Pattern",
        ["square", "triangular"],
        format_func=lambda x: "🔲 Square Grid"
        if x == "square"
        else "🔺 Triangular Grid",
    )
    b = st.number_input("PVD Width : b (cm)", value=10.0, step=0.5)
    a = st.number_input("PVD Thickness : a (cm)", value=0.5, step=0.1)

with st.sidebar.expander("🧱 2. Soil & Drainage Profile", expanded=True):
    cv = st.number_input("Cv (cm²/day)", value=20.0, step=1.0)
    kr_kv = st.number_input("Ratio kr/kv", value=7.0, step=0.5)
    H_clay = st.number_input(
        "Clay Thickness : H (m)", min_value=0.1, value=30.0, step=1.0
    )
    drainage_type = st.selectbox(
        "Drainage Path",
        ["Double Drainage (2-Way)", "Single Drainage (1-Way)"],
    )
    t_days = st.slider("Target Time : t (Days)", 10, 365, 90, 5)

with st.sidebar.expander("📊 3. Soil Compressibility", expanded=False):
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


# ฟังก์ชันสร้าง Dynamic SVG Diagram แสดงผังหน้าตัด PVD ตามค่าจริง
def render_pvd_svg(pattern, S_m, de_m):
    p_text = "Square Grid" if pattern == "square" else "Triangular Grid"
    svg = f"""
    <svg viewBox="0 0 400 240" width="100%" height="220" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="clayGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#F59E0B;stop-opacity:0.1" />
                <stop offset="100%" style="stop-color:#D97706;stop-opacity:0.25" />
            </linearGradient>
            <linearGradient id="pvdGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style="stop-color:#2563EB;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#1D4ED8;stop-opacity:1" />
            </linearGradient>
        </defs>
        
        <!-- Background Soil Zone -->
        <rect x="10" y="10" width="380" height="220" rx="12" fill="url(#clayGrad)" stroke="#F59E0B" stroke-dasharray="4 4" stroke-width="1.5"/>
        
        <!-- Influence Zone Circle (de) -->
        <circle cx="200" cy="120" r="75" fill="none" stroke="#2563EB" stroke-width="2" stroke-dasharray="6 6"/>
        <text x="200" y="38" font-size="12" fill="#2563EB" font-weight="600" text-anchor="middle">Zone of Influence (de = {de_m:.2f} m)</text>
        
        <!-- PVD Points Grid -->
        <rect x="194" y="114" width="12" height="12" rx="2" fill="url(#pvdGrad)"/>
        <text x="200" y="142" font-size="11" fill="#1E293B" font-weight="600" text-anchor="middle">Center PVD</text>
        
        <!-- Neighbor PVDs -->
        <rect x="94" y="114" width="12" height="12" rx="2" fill="url(#pvdGrad)" opacity="0.6"/>
        <rect x="294" y="114" width="12" height="12" rx="2" fill="url(#pvdGrad)" opacity="0.6"/>
        <rect x="194" y="34" width="12" height="12" rx="2" fill="url(#pvdGrad)" opacity="0.6"/>
        <rect x="194" y="194" width="12" height="12" rx="2" fill="url(#pvdGrad)" opacity="0.6"/>
        
        <!-- Dimension Line for S -->
        <line x1="200" y1="120" x2="300" y2="120" stroke="#0F172A" stroke-width="1.5" marker-end="url(#arrow)"/>
        <text x="250" y="112" font-size="11" fill="#0F172A" font-weight="700" text-anchor="middle">S = {S_m:.2f} m</text>
        
        <text x="25" y="35" font-size="12" fill="#78350F" font-weight="700">{p_text}</text>
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
        accent_col = "#10B981" if u_percent >= 90 else "#EF4444"

        with c1:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-accent" style="background: #2563EB;"></div>
                    <div class="stat-label">Average Consolidation</div>
                    <div class="stat-value" style="color: #2563EB;">{u_percent:.2f}%</div>
                    <div class="stat-sub">Degree of Consolidation (Uav)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-accent" style="background: #059669;"></div>
                    <div class="stat-label">Ultimate Settlement</div>
                    <div class="stat-value" style="color: #059669;">{results['S_final']*100:.1f} <span style="font-size:1rem; font-weight:500;">cm</span></div>
                    <div class="stat-sub">Total primary consolidation (S_final)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="stat-accent" style="background: #D97706;"></div>
                    <div class="stat-label">Settlement at Day {t_days}</div>
                    <div class="stat-value" style="color: #D97706;">{results['St']*100:.1f} <span style="font-size:1rem; font-weight:500;">cm</span></div>
                    <div class="stat-sub">Current predicted settlement (St)</div>
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
                    🎉 <b>DESIGN PASSED:</b> ค่าการอัดตัวคายน้ำทำได้ถึง <b>{u_percent:.2f}%</b> ซึ่งผ่านเกณฑ์มาตรฐานขั้นต่ำ (≥ 90%) ที่กำหนดไว้
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="alert-fail">
                    🚨 <b>DESIGN WARNING:</b> ค่าการอัดตัวคายน้ำทำได้เพียง <b>{u_percent:.2f}%</b> (ต่ำกว่าเกณฑ์ 90%) แนะนำให้ลดระยะห่าง S หรือเพิ่มเวลาเร่งดิน
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.3 VISUAL DIAGRAMS SECTION (ภาพประกอบและผังวิศวกรรม)
        st.subheader("🖼️ Engineering Schematics & Cross Section")
        img_col1, img_col2 = st.columns(2)

        with img_col1:
            st.markdown(
                """
                <div class="diagram-box">
                    <div style="font-weight:700; color:#0F172A; margin-bottom:0.5rem;">📱 Dynamic Cross-Section Diagram</div>
                    <div style="font-size:0.825rem; color:#64748B; margin-bottom:1rem;">ผังการจัดวาง PVD และ รัศมีอิทธิพล (Zone of Influence) ที่คำนวณตามจริง</div>
            """,
                unsafe_allow_html=True,
            )
            # Render Dynamic SVG Diagram
            svg_code = render_pvd_svg(pattern, S, results["de_m"])
            st.markdown(svg_code, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with img_col2:
            st.markdown(
                """
                <div class="diagram-box">
                    <div style="font-weight:700; color:#0F172A; margin-bottom:0.5rem;">🏞️ Soil & PVD Profile Illustration</div>
                    <div style="font-size:0.825rem; color:#64748B; margin-bottom:1rem;">ภาพจำลองโครงสร้างชั้นดินเหนียวอ่อนและการไหลคายน้ำของน้ำใต้ดิน</div>
            """,
                unsafe_allow_html=True,
            )
            # High-Quality Soil Profile Illustration (Unsplash Engineering Photo)
            st.image(
                "https://images.unsplash.com/photo-1581094184920-7a72da566411?auto=format&fit=crop&w=800&q=80",
                caption="Soil Consolidation & PVD Drainage Mechanism",
                use_container_width=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        # 5.4 Advanced Interactive Analytics Charts
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
            font=dict(family="Plus Jakarta Sans, sans-serif", size=13),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9", title="Time (Days)"),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        )

        with tab1:
            fig1 = go.Figure()
            fig1.add_trace(
                go.Scatter(
                    x=days_array,
                    y=u_av_list,
                    mode="lines",
                    name="Uav (%)",
                    fill="tozeroy",
                    fillcolor="rgba(37, 99, 235, 0.08)",
                    line=dict(color="#2563EB", width=3.5),
                )
            )
            fig1.add_hline(
                y=90,
                line_dash="dash",
                line_color="#059669",
                line_width=2,
                annotation_text="90% Target",
            )
            fig1.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="#DC2626",
                line_width=2,
                annotation_text=f"Selected {t_days} Days",
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
                    fill="tozeroy",
                    fillcolor="rgba(217, 119, 6, 0.08)",
                    line=dict(color="#D97706", width=3.5),
                )
            )
            fig2.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="#DC2626",
                line_width=2,
                annotation_text=f"Selected {t_days} Days",
            )
            fig2.update_layout(
                **chart_layout,
                yaxis_title="Settlement St (cm)",
                yaxis_autorange="reversed",
            )
            st.plotly_chart(fig2, use_container_width=True)