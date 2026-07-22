เห็นภาพแล้วครับ! สาเหตุที่ตัวอักษร **`arrow_down` ลอยซ้อนทับหัวข้อ** ในหน้า Sidebar เกิดจากตัวคำสั่ง CSS นี้ครับ:

```css
* {
    font-family: 'Plus Jakarta Sans', 'Prompt', sans-serif !important;
}

```

คำสั่ง `*` พร้อม `!important` ไป **บังคับเปลี่ยนฟอนต์ของไอคอนลูกศร Streamlit** (Material Icons) ให้กลายเป็นฟอนต์ตัวหนังสือทั่วไป ผลคือระบบไม่สามารถวาดรูป "ลูกศรชี้ลง" ได้ จึงแสดงผลเป็นข้อความตัวหนังสือคำว่า `arrow_down` แล้ววิ่งไปทับซ้อนกับชื่อหัวข้อ `1. PVD & Grid Layout` ตามที่เห็นในรูปครับ

---

### 🛠️ วิธีแก้ไขง่ายนิดเดียว

ปรับ CSS โดย**ยกเว้นไม่ให้เปลี่ยนฟอนต์ของไอคอน Streamlit** และปรับตกแต่งหัวข้อ Expander ใน Dark Mode ให้เนียนกริบ ไร้แถบสีขาวโผล่มากวนสายตาครับ

นำโค้ด `app.py` ฉบับแก้ไขปัญหานี้ไปวางทับได้เลยครับ:

```python
import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ==========================================
# 1. PAGE CONFIG & FIX CSS (No Icon Overlap)
# ==========================================
st.set_page_config(
    page_title="GEO-PVD Pro | Enterprise Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Prompt:wght@300;400;500;600;700&display=swap');
    
    /* Apply Font without breaking Streamlit Icons */
    html, body, p, h1, h2, h3, h4, h5, h6, label, div[data-testid="stMarkdownContainer"] {
        font-family: 'Plus Jakarta Sans', 'Prompt', sans-serif !important;
    }

    /* Preserve Icon Font for Expander Arrows */
    [data-testid="stExpanderToggleIcon"], i, .material-symbols-outlined {
        font-family: 'Material Symbols Outlined', 'Material Icons', sans-serif !important;
    }

    /* Main App Background */
    .stApp {
        background: #07090E;
        color: #F8FAFC;
    }

    /* Fix Sidebar Expander Dark Styling */
    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        margin-bottom: 0.8rem !important;
        overflow: hidden;
    }
    
    div[data-testid="stExpander"] summary {
        background-color: rgba(30, 41, 59, 0.5) !important;
        color: #F8FAFC !important;
        border-radius: 12px !important;
    }

    div[data-testid="stExpander"] summary:hover {
        background-color: rgba(51, 65, 85, 0.8) !important;
        color: #38BDF8 !important;
    }

    /* Top Brand Navigation Header */
    .brand-navbar {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.2rem 2.2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 0 50px rgba(99, 102, 241, 0.15);
    }
    .brand-title {
        font-size: 1.7rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #38BDF8 50%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .brand-badge {
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 100%);
        color: white;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.8px;
        box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);
    }

    /* Cyber-Luxe Stat Cards */
    .stat-card {
        background: rgba(18, 24, 38, 0.6);
        border-radius: 20px;
        padding: 1.6rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stat-card:hover {
        transform: translateY(-4px);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 20px 40px -15px rgba(56, 189, 248, 0.2);
    }
    .stat-label {
        font-size: 0.8rem;
        color: #94A3B8;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .stat-value {
        font-size: 2.3rem;
        font-weight: 800;
        margin: 0.4rem 0;
        letter-spacing: -0.5px;
    }
    .stat-sub {
        font-size: 0.825rem;
        color: #64748B;
    }
    .glow-bar-cyan { background: linear-gradient(90deg, #38BDF8, #6366F1); height: 3px; width: 100%; position: absolute; top:0; left:0; }
    .glow-bar-emerald { background: linear-gradient(90deg, #34D399, #10B981); height: 3px; width: 100%; position: absolute; top:0; left:0; }
    .glow-bar-pink { background: linear-gradient(90deg, #EC4899, #F43F5E); height: 3px; width: 100%; position: absolute; top:0; left:0; }

    .content-box {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        margin-bottom: 1.5rem;
    }

    .alert-pass {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(52, 211, 153, 0.3);
        color: #34D399;
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.15);
    }
    .alert-fail {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(248, 113, 113, 0.3);
        color: #F87171;
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        font-weight: 600;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.15);
    }

    section[data-testid="stSidebar"] {
        background-color: #0B0F17;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
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
            <span>⚡ GEO-PVD <span style="font-weight:300; opacity:0.8;">STUDIO</span></span>
            <span class="brand-badge">PRO v3.5</span>
        </div>
        <div style="color: #64748B; font-size: 0.85rem; font-weight: 500;">
            Advanced Geotechnical Consolidation Engine
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
st.sidebar.markdown("### 🎛️ Engineering Controls")

with st.sidebar.expander("📌 1. PVD & Grid Layout", expanded=True):
    S = st.number_input(
        "Spacing : S (m)", min_value=0.1, max_value=5.0, value=1.0, step=0.1
    )
    pattern = st.selectbox(
        "Grid Pattern",
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
        "Square Grid (de = 1.13S)"
        if pattern == "square"
        else "Triangular Grid (de = 1.05S)"
    )

    svg = f"""
    <svg viewBox="0 0 440 280" width="100%" height="250" xmlns="http://www.w3.org/2000/svg" style="background:#0F172A; border-radius:16px;">
        <defs>
            <radialGradient id="zoneGlow" cx="50%" cy="50%" r="50%">
                <stop offset="0%" style="stop-color:#38BDF8;stop-opacity:0.2" />
                <stop offset="100%" style="stop-color:#0F172A;stop-opacity:0" />
            </radialGradient>
            
            <linearGradient id="pvdCore" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#38BDF8" />
                <stop offset="100%" style="stop-color:#8B5CF6" />
            </linearGradient>

            <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#38BDF8"/>
            </marker>
        </defs>
        
        <rect x="15" y="15" width="410" height="250" rx="14" fill="none" stroke="#334155" stroke-dasharray="6 6" stroke-width="1.5"/>
        <text x="30" y="42" font-size="13" fill="#F8FAFC" font-weight="700" letter-spacing="0.5">{p_text}</text>
        <text x="410" y="42" font-size="12" fill="#38BDF8" font-weight="600" text-anchor="end">de = {de_m:.2f} m</text>
        
        <circle cx="220" cy="155" r="80" fill="url(#zoneGlow)" stroke="#38BDF8" stroke-width="2" stroke-dasharray="6 4"/>
        <text x="220" y="66" font-size="11" fill="#94A3B8" font-weight="500" text-anchor="middle">Zone of Influence Radius</text>
        
        <rect x="110" y="148" width="14" height="14" rx="3" fill="#334155" opacity="0.8"/>
        <rect x="316" y="148" width="14" height="14" rx="3" fill="#334155" opacity="0.8"/>
        <rect x="213" y="68" width="14" height="14" rx="3" fill="#334155" opacity="0.8"/>
        <rect x="213" y="228" width="14" height="14" rx="3" fill="#334155" opacity="0.8"/>
        
        <rect x="213" y="148" width="14" height="14" rx="3" fill="url(#pvdCore)"/>
        <text x="220" y="182" font-size="11" fill="#F8FAFC" font-weight="600" text-anchor="middle">Center PVD</text>
        
        <line x1="227" y1="155" x2="310" y2="155" stroke="#38BDF8" stroke-width="1.5" marker-end="url(#arrow)"/>
        <rect x="245" y="132" width="55" height="18" rx="4" fill="#0F172A" stroke="#334155"/>
        <text x="272.5" y="145" font-size="11" fill="#38BDF8" font-weight="700" text-anchor="middle">S = {S_m:.2f} m</text>
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
                <div class="stat-card">
                    <div class="glow-bar-cyan"></div>
                    <div class="stat-label">Average Consolidation</div>
                    <div class="stat-value" style="color: #38BDF8;">{u_percent:.2f}%</div>
                    <div class="stat-sub">Degree of Consolidation (Uav)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="glow-bar-emerald"></div>
                    <div class="stat-label">Ultimate Settlement</div>
                    <div class="stat-value" style="color: #34D399;">{results['S_final']*100:.1f} <span style="font-size:1rem; font-weight:500;">cm</span></div>
                    <div class="stat-sub">Total primary consolidation (S_final)</div>
                </div>
            """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="stat-card">
                    <div class="glow-bar-pink"></div>
                    <div class="stat-label">Settlement at Day {t_days}</div>
                    <div class="stat-value" style="color: #F43F5E;">{results['St']*100:.1f} <span style="font-size:1rem; font-weight:500;">cm</span></div>
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

        st.markdown("<br>", unsafe_allow_html=True)

        # 5.3 VISUAL DIAGRAMS SECTION
        st.subheader("🖼️ Engineering Schematics & Soil Profile")
        img_col1, img_col2 = st.columns(2)

        with img_col1:
            st.markdown(
                """
                <div class="content-box">
                    <div style="font-weight:700; color:#F8FAFC; margin-bottom:0.2rem;">📱 Dynamic Cross-Section Diagram</div>
                    <div style="font-size:0.825rem; color:#64748B; margin-bottom:0.8rem;">ผังแสดงระยะห่าง PVD และรัศมีอิทธิพล (Zone of Influence)</div>
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
                    <div style="font-size:0.825rem; color:#64748B; margin-bottom:0.8rem;">แบบจำลองชั้นดินเหนียวอ่อนและการติดตั้ง PVD</div>
                </div>
            """,
                unsafe_allow_html=True,
            )
            st.image(
                "https://images.unsplash.com/photo-1581094184920-7a72da566411?auto=format&fit=crop&w=800&q=80",
                caption="Soil Consolidation & PVD Drainage Mechanism",
                use_container_width=True,
            )

        # 5.4 Intermediate Calculations Expander
        with st.expander(
            "📐 ตัวแปรคำนวณระหว่างทางเพิ่มเติม (Intermediate Parameters)"
        ):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Equivalent Dia. (dw)", f"{results['dw']:.2f} cm")
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

        # 5.5 Advanced Cyberpunk Analytics Charts
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
            plot_bgcolor="#0F172A",
            margin=dict(l=20, r=20, t=30, b=20),
            hovermode="x unified",
            xaxis=dict(
                showgrid=True,
                gridcolor="#1E293B",
                title="Time (Days)",
                color="#94A3B8",
            ),
            yaxis=dict(showgrid=True, gridcolor="#1E293B", color="#94A3B8"),
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
                    fillcolor="rgba(56, 189, 248, 0.1)",
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
                    fill="tozeroy",
                    fillcolor="rgba(244, 63, 94, 0.1)",
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

```
