import math


def calculate_pvd_consolidation(
    S=1.0,  # ระยะห่าง PVD (m)
    pattern="square",  # รูปแบบ: 'square' หรือ 'triangular'
    a=0.5,  # ความหนา PVD (cm) [ทางปฏิบัติใช้ 0.5 cm หรือ 5 mm]
    b=10.0,  # ความกว้าง PVD (cm) [100 mm = 10 cm]
    cv=20.0,  # สปส.การอัดตัวคายน้ำแนวดิ่ง (cm^2/day)
    kr_kv_ratio=7.0,  # อัตราส่วน kr/kv
    t_days=90,  # ระยะเวลา (วัน)
    H_clay_m=30.0,  # ความหนาชั้นดินเหนียว (m)
    drainage_type="double",  # การระบายน้ำ: 'double' (ระบาย 2 ทาง) หรือ 'single'
    Cc=0.29,  # Compression Index
    e0=1.10,  # Void ratio เริ่มต้น
    sigma0_prime=40.0,  # Effective stress เดิม (kN/m^2)
    delta_sigma=80.0,  # น้ำหนักบรรทุกเพิ่ม (kN/m^2)
):

    print("=" * 60)
    print("      การคำนวณ PVD Design & Settlement Analysis")
    print("=" * 60)

    # 1. คำนวณขนาดเส้นผ่านศูนย์กลางเทียบเท่า (dw) และ เส้นผ่านศูนย์กลางอิทธิพล (de)
    dw = (a + b) / 2.0  # วิธี Rixner (cm)
    if pattern == "square":
        de_m = 1.13 * S
    else:  # triangular
        de_m = 1.05 * S

    de_cm = de_m * 100.0  # แปลงเป็น cm

    # 2. คำนวณ Drain Spacing Factor: F(n)
    n = de_cm / dw
    n_sq = n**2
    Fn = (n_sq / (n_sq - 1)) * math.log(n) - ((3 * n_sq - 1) / (4 * n_sq))

    # 3. คำนวณ Degree of Radial Consolidation: Ur (Barron Theory)
    Cr = kr_kv_ratio * cv  # cm^2/day
    Tr = (Cr * t_days) / (de_cm**2)
    Ur = 1.0 - math.exp((-8.0 * Tr) / Fn)

    # 4. คำนวณ Degree of Vertical Consolidation: Uv (Terzaghi Theory)
    if drainage_type == "double":
        Hdr_cm = (H_clay_m / 2.0) * 100.0
    else:
        Hdr_cm = H_clay_m * 100.0

    Tv = (cv * t_days) / (Hdr_cm**2)
    Uv = math.sqrt(4.0 * Tv) / math.pi  # ใช้กรณี Uv <= 60%

    # 5. คำนวณ Degree of Average Consolidation: Uav (Carillo, 1942)
    Uav = 1.0 - (1.0 - Ur) * (1.0 - Uv)

    # 6. คำนวณการทรุดตัวสุดท้าย (S_final) และ การทรุดตัว ณ เวลา t (S_t)
    S_final_m = H_clay_m * (Cc / (1.0 + e0)) * math.log10(
        (sigma0_prime + delta_sigma) / sigma0_prime
    )
    St_m = Uav * S_final_m

    # --- แสดงผลลัพธ์ ---
    print(f"1. ตัวแปรหน้าตัด PVD และ ระยะห่าง:")
    print(f"   - Equivalent Diameter (dw) : {dw:.2f} cm")
    print(f"   - Effective Diameter  (de) : {de_cm:.2f} cm ({de_m:.2f} m)")
    print(f"   - Spacing Factor       (n)  : {n:.2f}")
    print(f"   - Drain Spacing Factor F(n) : {Fn:.4f}")

    print(f"\n2. ผลการคำนวณการคายน้ำ (ที่เวลา {t_days} วัน):")
    print(f"   - Cr                        : {Cr:.2f} cm^2/day")
    print(f"   - Time Factor Radial   (Tr) : {Tr:.4f}")
    print(f"   - Radial Consol.       (Ur) : {Ur*100:.2f} %")
    print(f"   - Vertical Consol.     (Uv) : {Uv*100:.2f} %")
    print(f"   - Average Consol.     (Uav) : {Uav*100:.2f} %")

    print(f"\n3. การประเมินผลการทรุดตัว (Settlement):")
    print(f"   - Ultimate Settlement (S_final) : {S_final_m:.4f} m ({S_final_m*100:.2f} cm)")
    print(f"   - Settlement at t={t_days} days (St)    : {St_m:.4f} m ({St_m*100:.2f} cm)")

    print("-" * 60)
    if Uav >= 0.90:
        print("RESULT: ผ่านเกณฑ์! (Uav >= 90%)")
    else:
        print("RESULT: ไม่ผ่านเกณฑ์! (Uav < 90%) แนะนำให้ลดระยะห่าง S")
    print("=" * 60)


# --- เรียกใช้งานฟังก์ชั่น (อ้างอิงตามตัวอย่างในเอกสาร) ---
calculate_pvd_consolidation(
    S=1.0,  # ระยะห่าง 1.0 ม.
    pattern="square",  # รูปแบบสี่เหลี่ยม
    a=0.5,  # หนา 5 mm = 0.5 cm[cite: 1]
    b=10.0,  # กว้าง 100 mm = 10 cm[cite: 1]
    cv=20.0,  # Cv = 20 cm^2/day[cite: 1]
    kr_kv_ratio=7.0,  # kr/kv = 7[cite: 1]
    t_days=90,  # เวลา 90 วัน[cite: 1]
    H_clay_m=30.0,  # ดินหนา 30 ม.[cite: 1]
)
