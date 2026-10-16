# Envelope arithmetic for the NVIDIA/Rubin plate-envelope gap report (PG25 and water)
rho_pg, cp_pg = 1.02, 3.90   # kg/L, kJ/kg-K (PG25 ~50 C)
rho_w,  cp_w  = 0.99, 4.18
def rise(lpm_per_kw, rho, cp):
    m = lpm_per_kw*rho/60.0      # kg/s per kW
    return 1.0/(m*cp)            # K per kW -> K
print("Specific flow -> coolant rise (K): PG25 / water")
for f in [0.6, 0.75, 0.87, 1.0, 1.2, 1.5, 2.0]:
    print(f"  {f:4.2f} LPM/kW : {rise(f,rho_pg,cp_pg):5.1f} / {rise(f,rho_w,cp_w):5.1f}")
print()
print("Flow (LPM) needed for a fixed rise, PG25:")
for dT in [7.5, 10, 12, 15, 20]:
    f = 60.0/(rho_pg*cp_pg*dT)
    print(f"  dT={dT:4.1f} K -> {f:4.2f} LPM/kW")
print()
print("Per-package flow at specific flow (LPM):")
for name,P in [("B200 GB200",1.2),("B300 GB300",1.4),("Rubin MaxQ",1.8),("Rubin MaxP",2.3),("Rubin Ultra (analyst)",3.6),("MI455X (sec.)",2.3),("Maia 200",0.75),("CoolIT TTV",15.0)]:
    print(f"  {name:22s} {P:4.1f} kW : 0.75->{0.75*P:5.2f}  1.0->{1.0*P:5.2f}  1.2->{1.2*P:5.2f}  1.5->{1.5*P:5.2f}")
print()
print("Rack flow (LPM) for NVL72-class racks:")
for name,kW,cap in [("GB200 NVL72 120 kW",120,0.85),("GB200 NVL72 132 kW",132,0.85),("GB300 NVL72 ~140 kW",140,0.90),("VR NVL72 Max-P ~230 kW",230,1.0),("Kyber ~600 kW",600,1.0)]:
    for f in [0.75,1.0,1.2]:
        print(f"  {name:24s} capture {cap:.2f}  {f:4.2f} LPM/kW -> {kW*cap*f:6.0f} LPM")
print()
print("Pumping power per rack at rack dP (hydraulic, W): Q[LPM]*dP[kPa]/60")
for Q in [130,150,230,600]:
    for dp in [124,276,552]:
        print(f"  Q={Q:4d} LPM dP={dp:3d} kPa -> {Q*dp/60:6.0f} W")
print()
print("Die-average flux estimates (W/cm2): (TDP - HBM)/logic area")
cases=[("B200 1.2 kW, 2 x ~800 mm2, 8xHBM3e @30W",1200,8*30,16.0),
       ("B300 1.4 kW, same",1400,8*32,16.0),
       ("Rubin 2.3 kW, 2 x ~830 mm2, 8xHBM4 @45W",2300,8*45,16.6),
       ("Rubin 1.8 kW",1800,8*40,16.6),
       ("Rubin Ultra 3.6 kW, 4 x ~830 mm2, 16xHBM4e @45W",3600,16*45,33.2),
       ("MI455X 2.3 kW, 8 XCD ~ 8x1.4 cm2 stacked, 12xHBM4 @45W",2300,12*45,11.2),
       ("Maia 200 0.75 kW, ~800 mm2, 6xHBM3e @30W",750,6*30,8.0),
       ("CoolIT TTV 15 kW over ~117 cm2 (model)",15000,0,117.0)]
for n,P,hbm,A in cases:
    print(f"  {n:58s} -> {(P-hbm)/A:6.0f} W/cm2 (HBM share {hbm/P*100:3.0f} %)")
print()
print("Tj - T(die top) for bulk Si, k=1.2 W/cm-K at ~85 C:")
for t_um in [500,650,775]:
    for q in [75,120,200,350]:
        print(f"  t={t_um} um q''={q} W/cm2 -> {q*t_um*1e-4/1.2:4.1f} K")
print()
print("Budget at 45 C inlet: Tj limit 85/90 C minus Si drop at 120 W/cm2 (650 um):")
dsi = 120*650e-4/1.2
for tj in [85,90,95]:
    print(f"  Tj={tj} -> die-top-to-inlet budget {tj-45-dsi:4.1f} K (CoolIT avg 34.4, max 44.2)")
