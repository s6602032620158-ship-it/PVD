import math
import pandas as pd
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(
    page_title="PVD Design Calculator", page_icon="🏗️", layout="wide"
)

st.title("🏗️ PVD Consolidation & Settlement Calculator")
st.caption("แอปพลิเคชันคำนวณการอัดตัวคายน้ำของดินด้วย PVD (AI-Assisted Prototype)")

st.sidebar.header("⚙️ พารามิเตอร์การออกแบบ")

# ส่วนรับข้อมูลผ่าน Sidebar
S = st.sidebar.slider("ระยะห่าง PVD : S (m)", 0.5, 2.0, 1.0, 0.1)
pattern = st.sidebar.radio("รูปแบบการจัดวาง", ["square", "triangular"])
t_days = st.sidebar.number_input("ระยะเวลา (วัน)", value=90, step=10)
H_clay = st.sidebar.number_input(
    "ความหนาชั้นดินเหนียว : H (m)", value=30.0, step=1.0
)

# ปุ่มกดคำนวณ
if st.button("🚀 คำนวณผลลัพธ์"):
    # 1. คำนวณ dw และ de
    a, b = 0.5, 10.0  # cm
    dw = (a + b) / 2.0
    de_m = 1.13 * S if pattern == "square" else 1.05 * S
    de_cm = de_m * 100.0

    # 2. Spacing Factor & Consolidation
    n = de_cm / dw
    Fn = ((n**2) / (n**2 - 1)) * math.log(n) - ((3 * n**2 - 1) / (4 * n**2))

    cv = 20.0  # cm^2/day
    Cr = 7.0 * cv
    Tr = (Cr * t_days) / (de_cm**2)
    Ur = 1.0 - math.exp((-8.0 * Tr) / Fn)

    Hdr_cm = (H_clay / 2.0) * 100.0
    Tv = (cv * t_days) / (Hdr_cm**2)
    Uv = math.sqrt(4.0 * Tv) / math.pi
    Uav = 1.0 - (1.0 - Ur) * (1.0 - Uv)

    # 3. Settlement
    Cc, e0, sigma0, delta_sigma = 0.29, 1.10, 40.0, 80.0
    S_final = H_clay * (Cc / (1.0 + e0)) * math.log10((sigma0 + delta_sigma) / sigma0)
    St = Uav * S_final

    # --- แสดงผลลัพธ์ผ่าน Metric Cards ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Consolidation (Uav)", f"{Uav*100:.2f} %")
    col2.metric("การทรุดตัวรวมสูงสุด (S final)", f"{S_final*100:.2f} cm")
    col3.metric(f"การทรุดตัว ณ {t_days} วัน (St)", f"{St*100:.2f} cm")

    st.markdown("---")

    # สรุปเกณฑ์ผ่าน/ไม่ผ่าน
    if Uav >= 0.90:
        st.success("✅ **ผ่านเกณฑ์มาตรฐาน:** การอัดตัวคายน้ำมากกว่า 90%")
    else:
        st.error(
            "❌ **ไม่ผ่านเกณฑ์:** การอัดตัวคายน้ำน้อยกว่า 90% (แนะนำให้ลดระยะห่าง S)"
        )
