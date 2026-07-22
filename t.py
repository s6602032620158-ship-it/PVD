import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIG & ADVANCED CSS (Glassmorphism)
# ==========================================
st.set_page_config(
    page_title="PVD Engineering Suite Pro",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS ตกแต่งระดับพรีเมียม
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Prompt', sans-serif !important;
    }

    /* Main Background */
    .stApp {
        background-color: #F8FAFC;
    }

    /* Header Banner with Soft Glow */
    .hero-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E1B4B 50%, #312E81 100%);
        padding: 2.2rem 2.5rem;
        border-radius: 20px;
        color: white;
        box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.3);
        margin-bottom: 2rem;
        position: relative;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #FFFFFF 0%, #A5B4FC 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.3rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #C7D2FE;
        font-weight: 300;
    }

    /* Modern Glass Cards */
    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 1.4rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.03);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.08);
        border-color: #C7D2FE;
    }

    .card-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        margin-bottom: 0.8rem;
    }
    .card-title {
        font-size: 0.85rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .card-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #0F172A;
        margin-top: 0.2rem;
    }

    /* Status Pill Badge */
    .status-pill-pass {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 1px solid #A7F3D0;
        color: #065F46;
        padding: 1rem 1.2rem;
        border-radius: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .status-pill-fail {
        background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%);
        border: 1px solid #FCA5A5;
        color: #991B1B;
        padding: 1rem 1.2rem;
        border-radius: 14px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Progress Bar */
    .progress-container {
        width: 100%;
        background-color: #E2E8F0;
        border-radius: 10px;
        height: 10px;
        margin-top: 10px;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease-in-out;
    }

    /* Sidebar Clean styling */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. HERO HEADER BANNER
# ==========================================
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-title">⚡ PVD Consolidation Analytics</div>
        <div class="hero-subtitle">ระบบจำลองการอัดตัวคายน้ำและการทรุดตัวของชั้นดินเหนียวด้วยวิธี Prefabricated Vertical Drain</div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown(
    "### 🛠️ พารามิเตอร์การออกแบบ", help="กำหนดค่าทางปฐพีวิศวกรรม"
)

with st.sidebar.expander("📌 1. PVD & Geometry", expanded=True):
    S = st.number_input(
        "ระยะห่าง PVD : S (m)",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1,
    )
    pattern = st.selectbox(
        "รูปแบบการจัดวาง",
        ["square", "triangular"],
        format_func=lambda x: "🔲 Square Grid"
        if x == "square"
        else "🔺 Triangular Grid",
    )
    b = st.number_input("ความกว้าง PVD : b (cm)", value=10.0, step=0.5)
    a = st.number_input("ความหนา PVD : a (cm)", value=0.5, step=0.1)

with st.sidebar.expander("🧱 2. Soil Properties", expanded=True):
    cv = st.number_input("ค่า Cv (cm²/day)", value=20.0, step=1.0)
    kr_kv = st.number_input("อัตราส่วน kr/kv", value=7.0, step=0.5)
    H_clay = st.number_input(
        "ความหนาดินเหนียว : H (m)", min_value=0.1, value=30.0, step=1.0
    )
    drainage_type = st.selectbox(
        "เงื่อนไขการระบายน้ำ",
        ["Double Drainage (2 ทาง)", "Single Drainage (ทางเดียว)"],
    )
    t_days = st.slider("ระยะเวลาพิจารณา : t (วัน)", 10, 365, 90, 5)

with st.sidebar.expander("📈 3. Settlement Parameters", expanded=False):
    Cc = st.number_input("Compression Index (Cc)", value=0.29, step=0.01)
    e0 = st.number_input("Initial Void Ratio (e0)", value=1.10, step=0.05)
    sigma0 = st.number_input("Effective Stress เดิม (kN/m²)", value=40.0, step=5.0)
    delta_sigma = st.number_input(
        "น้ำหนักบรรทุกเพิ่ม Δσ (kN/m²)", value=80.0, step=5.0
    )


# ==========================================
# 4. CALCULATION ENGINE
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
        return None, "ระยะห่าง PVD (S) เล็กเกินไปเมื่อเทียบกับขนาดแผ่น PVD"

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


# ==========================================
# 5. MAIN DASHBOARD DISPLAY
# ==========================================
if S <= 0 or H_clay <= 0 or sigma0 <= 0:
    st.error("⚠️ ข้อผิดพลาด: ค่าพารามิเตอร์ S, H, และ σ'0 ต้องมากกว่า 0")
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
        st.error(f"⚠️ ข้อผิดพลาดทางคณิตศาสตร์: {err_msg}")
    else:
        # 5.1 Glassmorphic Metric Cards
        c1, c2, c3 = st.columns(3)

        u_percent = results["Uav"] * 100
        progress_color = "#10B981" if u_percent >= 90 else "#EF4444"

        with c1:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="card-icon-box" style="background-color: #EEF2FF; color: #4F46E5;">💧</div>
                    <div class="card-title">Average Consolidation (Uav)</div>
                    <div class="card-value" style="color: #4F46E5;">{u_percent:.2f}%</div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {min(u_percent, 100)}%; background-color: {progress_color};"></div>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="card-icon-box" style="background-color: #F0FDF4; color: #16A34A;">🎯</div>
                    <div class="card-title">Ultimate Settlement (S final)</div>
                    <div class="card-value" style="color: #16A34A;">{results['S_final']*100:.2f} <span style="font-size:1.1rem; font-weight:400; color:#64748B;">cm</span></div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="glass-card">
                    <div class="card-icon-box" style="background-color: #FFF7ED; color: #EA580C;">⏱️</div>
                    <div class="card-title">Settlement at {t_days} Days (St)</div>
                    <div class="card-value" style="color: #EA580C;">{results['St']*100:.2f} <span style="font-size:1.1rem; font-weight:400; color:#64748B;">cm</span></div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.2 Status Banner
        if results["Uav"] >= 0.90:
            st.markdown(
                f"""
                <div class="status-pill-pass">
                    <span style="font-size: 1.4rem;">🎉</span>
                    <div><b>ผ่านเกณฑ์มาตรฐานออกแบบ:</b> การอัดตัวคายน้ำทำได้ถึง <b>{u_percent:.2f}%</b> (เป้าหมาย ≥ 90%)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="status-pill-fail">
                    <span style="font-size: 1.4rem;">⚠️</span>
                    <div><b>ไม่ผ่านเกณฑ์มาตรฐาน:</b> การอัดตัวคายน้ำทำได้เพียง <b>{u_percent:.2f}%</b> (เป้าหมาย ≥ 90%) — แนะนำให้ลดระยะห่าง S</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.3 Detailed Parameters Expander
        with st.expander(
            "📐 ตัวแปรที่คำนวณได้ระหว่างทาง (Intermediate Parameters)"
        ):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric(
                    "Equivalent Dia. (dw)", f"{results['dw']:.2f} cm"
                )
                st.metric("Influence Dia. (de)", f"{results['de_m']:.2f} m")
            with col_b:
                st.metric("Spacing Factor (n)", f"{results['n']:.2f}")
                st.metric("Drain Factor F(n)", f"{results['Fn']:.4f}")
            with col_c:
                st.metric(
                    "Radial Consol. (Ur)", f"{results['Ur']*100:.2f} %"
                )
                st.metric(
                    "Vertical Consol. (Uv)", f"{results['Uv']*100:.2f} %"
                )

        st.markdown("---")

        # ==========================================
        # 6. HIGH-END PLOTLY CHARTS (Gradient Area)
        # ==========================================
        st.subheader("📊 กราฟวิเคราะห์แนวโน้มตามเวลา")

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
            ["💧 Consolidation Progress (%)", "📉 Settlement History (cm)"]
        )

        chart_layout = dict(
            font=dict(family="Prompt, sans-serif", size=13),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#FFFFFF",
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified",
            xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
            yaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
        )

        # Chart 1: Consolidation Rate Area Chart
        with tab1:
            fig1 = go.Figure()
            fig1.add_trace(
                go.Scatter(
                    x=days_array,
                    y=u_av_list,
                    mode="lines",
                    name="Uav (%)",
                    fill="tozeroy",
                    fillcolor="rgba(79, 70, 229, 0.1)",  # Indigo Gradient Fill
                    line=dict(color="#4F46E5", width=3),
                    hovertemplate="เวลา %{x} วัน: <b>%{y:.2f}%</b>",
                )
            )
            fig1.add_hline(
                y=90,
                line_dash="dash",
                line_color="#10B981",
                line_width=2,
                annotation_text="Target 90%",
            )
            fig1.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="#EF4444",
                line_width=2,
                annotation_text=f"Day {t_days}",
            )
            fig1.update_layout(
                **chart_layout,
                title="<b>ความก้าวหน้าการอัดตัวคายน้ำ (Consolidation Rate vs Time)</b>",
                yaxis_range=[0, 105],
            )
            st.plotly_chart(fig1, use_container_width=True)

        # Chart 2: Settlement Area Chart
        with tab2:
            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=days_array,
                    y=st_list,
                    mode="lines",
                    name="Settlement (cm)",
                    fill="tozeroy",
                    fillcolor="rgba(234, 88, 12, 0.1)",  # Orange Gradient Fill
                    line=dict(color="#EA580C", width=3),
                    hovertemplate="เวลา %{x} วัน: <b>%{y:.2f} cm</b>",
                )
            )
            fig2.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="#EF4444",
                line_width=2,
                annotation_text=f"Day {t_days}",
            )
            fig2.update_layout(
                **chart_layout,
                title="<b>ระยะการทรุดตัวของชั้นดินตามเวลา (Settlement vs Time)</b>",
                yaxis_autorange="reversed",  # ทรุดลงล่าง
            )
            st.plotly_chart(fig2, use_container_width=True)
