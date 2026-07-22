import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PVD Design Calculator",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🏗️ PVD Consolidation & Settlement Calculator")
st.caption("ระบบวิเคราะห์การอัดตัวคายน้ำและการทรุดตัวของดินด้วยวิธี PVD (Barron & Carillo Theory)")
st.markdown("---")

# ==========================================
# 2. SIDEBAR - INPUT MODULE
# ==========================================
st.sidebar.header("⚙️ พารามิเตอร์การออกแบบ (Inputs)")

# 2.1 PVD & Geometric Parameters
st.sidebar.subheader("1. ข้อมูล PVD และ รูปแบบ")
S = st.sidebar.number_input(
    "ระยะห่าง PVD : S (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1
)
pattern = st.sidebar.selectbox("รูปแบบการจัดวาง (Pattern)", ["square", "triangular"])
b = st.sidebar.number_input("ความกว้าง PVD : b (cm)", value=10.0, step=0.5)
a = st.sidebar.number_input("ความหนา PVD : a (cm)", value=0.5, step=0.1)

# 2.2 Soil Properties & Drainage
st.sidebar.subheader("2. คุณสมบัติดินและการระบายน้ำ")
cv = st.sidebar.number_input("ค่า Cv (cm²/day)", value=20.0, step=1.0)
kr_kv = st.sidebar.number_input("อัตราส่วน kr/kv", value=7.0, step=0.5)
H_clay = st.sidebar.number_input(
    "ความหนาชั้นดินเหนียว : H (m)", min_value=0.1, value=30.0, step=1.0
)
drainage_type = st.sidebar.selectbox(
    "รูปแบบการระบายน้ำ",
    ["Double Drainage (2 ทาง)", "Single Drainage (ทางเดียว)"],
)
t_days = st.sidebar.slider("ระยะเวลาที่พิจารณา : t (วัน)", 10, 365, 90, 5)

# 2.3 Settlement Parameters
st.sidebar.subheader("3. พารามิเตอร์การทรุดตัว")
Cc = st.sidebar.number_input("Compression Index (Cc)", value=0.29, step=0.01)
e0 = st.sidebar.number_input("Initial Void Ratio (e0)", value=1.10, step=0.05)
sigma0 = st.sidebar.number_input(
    "Effective Stress เดิม : σ'0 (kN/m²)", value=40.0, step=5.0
)
delta_sigma = st.sidebar.number_input(
    "น้ำหนักบรรทุกเพิ่ม : Δσ (kN/m²)", value=80.0, step=5.0
)


# ==========================================
# 3. CALCULATION ENGINE FUNCTION
# ==========================================
def calculate_pvd(S, pattern, a, b, cv, kr_kv, H_clay, drainage_type, t, Cc, e0, sigma0, delta_sigma):
    # 1. Equivalent & Influence Diameter
    dw = (a + b) / 2.0  # cm
    de_m = 1.13 * S if pattern == "square" else 1.05 * S
    de_cm = de_m * 100.0  # cm

    # Safety check for spacing factor
    n = de_cm / dw
    if n <= 1:
        return None, "ระยะห่าง PVD (S) เล็กเกินไปเมื่อเทียบกับขนาดแผ่น PVD"

    # 2. Spacing Factor F(n) & Barron's Radial Consolidation
    Fn = ((n**2) / (n**2 - 1)) * math.log(n) - ((3 * n**2 - 1) / (4 * n**2))
    Cr = kr_kv * cv
    Tr = (Cr * t) / (de_cm**2)
    Ur = 1.0 - math.exp((-8.0 * Tr) / Fn)

    # 3. Terzaghi's Vertical Consolidation
    Hdr_cm = (
        (H_clay / 2.0) * 100.0
        if "Double" in drainage_type
        else H_clay * 100.0
    )
    Tv = (cv * t) / (Hdr_cm**2)

    # Approximation for Uv
    if Tv <= 0.282:
        Uv = math.sqrt(4.0 * Tv) / math.pi
    else:
        Uv = 1.0 - (8.0 / (math.pi**2)) * math.exp(-((math.pi**2) / 4.0) * Tv)

    # 4. Combined Consolidation (Carillo's Formula)
    Uav = 1.0 - (1.0 - Ur) * (1.0 - Uv)

    # 5. Settlement Calculation
    S_final = H_clay * (Cc / (1.0 + e0)) * math.log10((sigma0 + delta_sigma) / sigma0)
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
# 4. MAIN APPLICATION & DISPLAY LOGIC
# ==========================================

# 4.1 Input Validation Check (NFR-01)
if S <= 0 or H_clay <= 0 or sigma0 <= 0:
    st.error("⚠️ ข้อผิดพลาด: ค่าพารามิเตอร์ S, H, และ σ'0 ต้องมากกว่า 0")
else:
    # Run Calculation
    results, err_msg = calculate_pvd(
        S, pattern, a, b, cv, kr_kv, H_clay, drainage_type, t_days, Cc, e0, sigma0, delta_sigma
    )

    if err_msg:
        st.error(f"⚠️ ข้อผิดพลาดทางคณิตศาสตร์: {err_msg}")
    else:
        # 4.2 KPI Metric Dashboard (FR-09)
        col1, col2, col3 = st.columns(3)
        col1.metric("การอัดตัวคายน้ำรวม (Uav)", f"{results['Uav']*100:.2f} %")
        col2.metric("การทรุดตัวสูงสุด (S_final)", f"{results['S_final']*100:.2f} cm")
        col3.metric(
            f"การทรุดตัว ณ วันที่ {t_days} (St)", f"{results['St']*100:.2f} cm"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # 4.3 Criteria Evaluation Alert (FR-10)
        if results["Uav"] >= 0.90:
            st.success(
                f"✅ **ผ่านเกณฑ์มาตรฐาน:** อัตราการอัดตัวคายน้ำเท่ากับ {results['Uav']*100:.2f}% (≥ 90%)"
            )
        else:
            st.error(
                f"❌ **ไม่ผ่านเกณฑ์มาตรฐาน:** อัตราการอัดตัวคายน้ำเท่ากับ {results['Uav']*100:.2f}% (< 90%) แนะนำให้ลดระยะห่าง S"
            )

        # 4.4 Detailed Calculation Expansion
        with st.expander("🔍 ดูรายละเอียดตัวแปรการคำนวณ (Intermediate Values)"):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"- **dw (Equivalent Dia.):** {results['dw']:.2f} cm")
                st.write(f"- **de (Influence Dia.):** {results['de_m']:.2f} m")
                st.write(f"- **n (Spacing Factor):** {results['n']:.2f}")
                st.write(f"- **F(n):** {results['Fn']:.4f}")
            with c2:
                st.write(f"- **Ur (Radial Consol.):** {results['Ur']*100:.2f} %")
                st.write(f"- **Uv (Vertical Consol.):** {results['Uv']*100:.2f} %")
                st.write(
                    f"- **Uav (Combined):** {results['Uav']*100:.2f} %"
                )

        st.markdown("---")

        # ==========================================
        # 5. VISUALIZATION MODULE (Interactive Charts)
        # ==========================================
        st.subheader("📈 กราฟแสดงแนวโน้มตามช่วงเวลา (Time-History Curves)")

        # Generate Time Series Data (1 to 365 Days)
        days_array = np.arange(1, 366)
        u_av_list = []
        st_list = []

        for d in days_array:
            res, _ = calculate_pvd(
                S, pattern, a, b, cv, kr_kv, H_clay, drainage_type, d, Cc, e0, sigma0, delta_sigma
            )
            u_av_list.append(res["Uav"] * 100)
            st_list.append(res["St"] * 100)

        tab1, tab2 = st.tabs(
            ["📊 Consolidation Rate (% Degree)", "📉 Settlement vs Time (cm)"]
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
                    line=dict(color="#1f77b4", width=3),
                )
            )
            fig1.add_hline(
                y=90,
                line_dash="dash",
                line_color="green",
                annotation_text="Target 90%",
            )
            fig1.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="red",
                annotation_text=f"Selected Day ({t_days})",
            )
            fig1.update_layout(
                title="อัตราการอัดตัวคายน้ำตามเวลา (Consolidation Rate vs Time)",
                xaxis_title="เวลา (วัน)",
                yaxis_title="เปอร์เซ็นต์การอัดตัวคายน้ำ Uav (%)",
                yaxis_range=[0, 105],
                hovermode="x unified",
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
                    line=dict(color="#ff7f0e", width=3),
                )
            )
            fig2.add_vline(
                x=t_days,
                line_dash="dot",
                line_color="red",
                annotation_text=f"Selected Day ({t_days})",
            )
            fig2.update_layout(
                title="ระยะการทรุดตัวตามเวลา (Settlement vs Time)",
                xaxis_title="เวลา (วัน)",
                yaxis_title="การทรุดตัว (cm)",
                yaxis_autorange="reversed",  # กลับแกน Y ให้เห็นภาพการจมลง
                hovermode="x unified",
            )
            st.plotly_chart(fig2, use_container_width=True)
