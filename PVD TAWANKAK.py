import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="PVD Design Calculator Pro",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS เพื่อตกแต่ง UI ให้ทันสมัย สวยงาม
st.markdown(
    """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Kanit', sans-serif;
    }

    /* Gradient Banner Header */
    .header-banner {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        margin-bottom: 2rem;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
        color: #FFFFFF;
    }
    .header-subtitle {
        font-size: 1.0rem;
        color: #B2FEFA;
        opacity: 0.9;
    }

    /* Custom Metric Cards */
    .metric-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #0072FF;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    }
    .metric-card-title {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 400;
    }
    .metric-card-value {
        font-size: 1.8rem;
        font-weight: 600;
        color: #1E293B;
        margin-top: 0.3rem;
    }

    /* Badge Customization */
    .status-badge-pass {
        background-color: #E6F4EA;
        color: #137333;
        border: 1px solid #CEEAD6;
        padding: 1rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.05rem;
    }
    .status-badge-fail {
        background-color: #FCE8E6;
        color: #C5221F;
        border: 1px solid #FAD2CF;
        padding: 1rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.05rem;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
    }
    
    /* Expander Container Style */
    div[data-testid="stExpander"] {
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        background-color: #FFFFFF;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. HEADER BANNER
# ==========================================
st.markdown(
    """
    <div class="header-banner">
        <div class="header-title">🏗️ PVD Consolidation & Settlement Calculator</div>
        <div class="header-subtitle">ระบบวิเคราะห์การอัดตัวคายน้ำและการทรุดตัวของดินด้วยวิธี PVD (Barron & Carillo Theory)</div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. SIDEBAR - INPUT MODULE
# ==========================================
st.sidebar.markdown(
    "### ⚙️ พารามิเตอร์การออกแบบ", help="กำหนดค่าตัวแปรปฐพีวิศวกรรม"
)

# 3.1 PVD & Geometric Parameters
with st.sidebar.expander("📍 1. ข้อมูล PVD และรูปแบบ", expanded=True):
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
        format_func=lambda x: "🔲 สี่เหลี่ยม (Square)"
        if x == "square"
        else "🔺 สามเหลี่ยม (Triangular)",
    )
    b = st.number_input("ความกว้าง PVD : b (cm)", value=10.0, step=0.5)
    a = st.number_input("ความหนา PVD : a (cm)", value=0.5, step=0.1)

# 3.2 Soil Properties & Drainage
with st.sidebar.expander("🧱 2. คุณสมบัติดินและการระบายน้ำ", expanded=True):
    cv = st.number_input("ค่า Cv (cm²/day)", value=20.0, step=1.0)
    kr_kv = st.number_input("อัตราส่วน kr/kv", value=7.0, step=0.5)
    H_clay = st.number_input(
        "ความหนาชั้นดินเหนียว : H (m)", min_value=0.1, value=30.0, step=1.0
    )
    drainage_type = st.selectbox(
        "รูปแบบการระบายน้ำ",
        ["Double Drainage (2 ทาง)", "Single Drainage (ทางเดียว)"],
    )
    t_days = st.slider("ระยะเวลาที่พิจารณา : t (วัน)", 10, 365, 90, 5)

# 3.3 Settlement Parameters
with st.sidebar.expander("📊 3. พารามิเตอร์การทรุดตัว", expanded=False):
    Cc = st.number_input("Compression Index (Cc)", value=0.29, step=0.01)
    e0 = st.number_input("Initial Void Ratio (e0)", value=1.10, step=0.05)
    sigma0 = st.number_input(
        "Effective Stress เดิม : σ'0 (kN/m²)", value=40.0, step=5.0
    )
    delta_sigma = st.number_input(
        "น้ำหนักบรรทุกเพิ่ม : Δσ (kN/m²)", value=80.0, step=5.0
    )


# ==========================================
# 4. CALCULATION ENGINE FUNCTION
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
# 5. MAIN APPLICATION LOGIC
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
        # 5.1 Custom Metric Cards Dashboard
        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color: #0072FF;">
                    <div class="metric-card-title">💧 อัตราการอัดตัวคายน้ำรวม (Uav)</div>
                    <div class="metric-card-value" style="color: #0072FF;">{results['Uav']*100:.2f} %</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color: #8E2DE2;">
                    <div class="metric-card-title">📏 การทรุดตัวรวมสูงสุด (S_final)</div>
                    <div class="metric-card-value" style="color: #8E2DE2;">{results['S_final']*100:.2f} cm</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card" style="border-left-color: #FF8008;">
                    <div class="metric-card-title">⏱️ การทรุดตัว ณ วันที่ {t_days} (St)</div>
                    <div class="metric-card-value" style="color: #FF8008;">{results['St']*100:.2f} cm</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.2 Criteria Badge Alert
        if results["Uav"] >= 0.90:
            st.markdown(
                f"""
                <div class="status-badge-pass">
                    ✅ <b>ผ่านเกณฑ์มาตรฐาน:</b> อัตราการอัดตัวคายน้ำเท่ากับ <b>{results['Uav']*100:.2f}%</b> (≥ 90%)
                </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="status-badge-fail">
                    ❌ <b>ไม่ผ่านเกณฑ์มาตรฐาน:</b> อัตราการอัดตัวคายน้ำเท่ากับ <b>{results['Uav']*100:.2f}%</b> (< 90%) แนะนำให้ลดระยะห่าง S
                </div>
            """,
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.3 Intermediate Calculation Table
        with st.expander(
            "🔍 ดูรายละเอียดค่าตัวแปรการคำนวณเพิ่มเติม (Intermediate Values)"
        ):
            ic1, ic2 = st.columns(2)
            with ic1:
                st.markdown(f"• **Equivalent Dia. ($d_w$):** `{results['dw']:.2f} cm`")
                st.markdown(
                    f"• **Influence Dia. ($d_e$):** `{results['de_m']:.2f} m`"
                )
                st.markdown(f"• **Spacing Factor ($n$):** `{results['n']:.2f}`")
                st.markdown(f"• **Drain Factor $F(n)$:** `{results['Fn']:.4f}`")
            with ic2:
                st.markdown(
                    f"• **Radial Consolidation ($U_r$):** `{results['Ur']*100:.2f} %`"
                )
                st.markdown(
                    f"• **Vertical Consolidation ($U_v$):** `{results['Uv']*100:.2f} %`"
                )
                st.markdown(
                    f"• **Combined Consolidation ($U_{{av}}$):** `{results['Uav']*100:.2f} %`"
                )

        st.markdown("---")

        # ==========================================
        # 6. VISUALIZATION MODULE (Plotly Charts)
        # ==========================================
        st.subheader("📈 กราฟแสดงแนวโน้มตามช่วงเวลา (Time-History Curves)")

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
            ["📊 Consolidation Rate (% Degree)", "📉 Settlement vs Time (cm)"]
        )

        # Config กราฟธีมมินิมอล & มีสีสัน
        layout_common = dict(
            font=dict(family="Kanit, sans-serif", size=13),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#F8FAFC",
            margin=dict(l=40, r=40, t=50, b=40),
            hovermode="x unified",
        )

        # Chart 1: Consolidation Rate Graph
        with tab1:
            fig1 = go.Figure()
            fig1.add_trace(
                go.Scatter(
                    x=days_array,
                    y=u_av_list,
                    mode="lines",
                    name="Uav (%)",
                    line=dict(color="#0072FF", width=3.5),
                    hovertemplate="เวลา %{x} วัน: <b>%{y:.2f}%</b>",
                )
            )
            fig1.add_hline(
                y=90,
                line_dash="dash",
                line_color="#10B981",
                annotation_text="เกณฑ์เป้าหมาย 90%",
                annotation_position="bottom right",
            )
            fig1.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="#EF4444",
                annotation_text=f"วันที่เลือก ({t_days} วัน)",
            )
            fig1.update_layout(
                **layout_common,
                title="<b>อัตราการอัดตัวคายน้ำตามเวลา (Consolidation Rate vs Time)</b>",
                xaxis_title="เวลา (วัน)",
                yaxis_title="เปอร์เซ็นต์การอัดตัวคายน้ำ Uav (%)",
                yaxis_range=[0, 105],
            )
            st.plotly_chart(fig1, use_container_width=True)

        # Chart 2: Settlement Graph
        with tab2:
            fig2 = go.Figure()
            fig2.add_trace(
                go.Scatter(
                    x=days_array,
                    y=st_list,
                    mode="lines",
                    name="Settlement (cm)",
                    line=dict(color="#FF8008", width=3.5),
                    hovertemplate="เวลา %{x} วัน: <b>%{y:.2f} cm</b>",
                )
            )
            fig2.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="#EF4444",
                annotation_text=f"วันที่เลือก ({t_days} วัน)",
            )
            fig2.update_layout(
                **layout_common,
                title="<b>ระยะการทรุดตัวตามเวลา (Settlement vs Time)</b>",
                xaxis_title="เวลา (วัน)",
                yaxis_title="การทรุดตัว (cm)",
                yaxis_autorange="reversed",
            )
            st.plotly_chart(fig2, use_container_width=True)
