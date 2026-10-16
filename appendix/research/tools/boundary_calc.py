# What could an OCP "~4,000 W" single-phase cold-plate boundary mean? Scenario calcs.
# PG25 at ~50 C: rho 1010 kg/m3, cp 3930 J/kgK, mu ~1.3 mPa.s, k ~0.475 W/mK
rho, cp = 1010.0, 3930.0
def caloric(Q, lpm):
    m = lpm/60/1000*rho
    return Q/(m*cp)
print("A. Caloric rise at fixed LPM/kW (independent of Q):")
for lpk in (0.75,1.0,1.2,1.5):
    print(f"  {lpk} LPM/kW -> dT_bulk = {caloric(1000, lpk):.1f} K")
print()
print("B. Unit-resistance x area x dT budget: Q_max = A * dT / R''")
for Rpp in (0.10,0.15,0.20,0.25,0.30):
    for A in (16,25,33,50,80,117):
        for dT in (30,35):
            Q = A*dT/Rpp
            if abs(Q-4000) < 700:
                print(f"  R''={Rpp} cm2K/W, A={A} cm2, dT={dT} K -> Q={Q:.0f} W (flux {Q/A:.0f} W/cm2)")
print()
print("C. Per-package absolute R needed for 4 kW at dT=35 K:", 35/4000*1000, "mK/W  (CoolIT 4 kW: <9 mK/W max-case, 1.5 LPM/kW)")
print("   CoolIT 15 kW avg basis:", 34.4/15000*1000, "mK/W; max-case:", 44.2/15000*1000, "mK/W")
print()
print("D. Flow/QD view: 4 kW at 1.5 LPM/kW = 6 LPM per plate; 15 kW at 1.2 = 18 LPM.")
import math
for d_in in (0.25,0.375,0.5):
    d = d_in*0.0254*0.8  # approx bore ~80% of nominal
    A = math.pi*d*d/4
    for lpm in (6,18):
        v = lpm/60/1000/A
        print(f"  nominal {d_in} in (bore ~{d*1000:.1f} mm): {lpm} LPM -> {v:.2f} m/s")
print()
print("E. Reticle-limited die: 2 x 800 mm2 dies = 16 cm2; HBM adds ~8 x 1.2 cm2. Package lid ~ 60-80 cm2")
for Rpp in (0.10,0.15,0.20):
    print(f"  R''={Rpp}: 2-die bare 16 cm2 at 35 K -> {16*35/Rpp:.0f} W; lid 60 cm2 (spreading-limited, eff ~50%) -> {30*35/Rpp:.0f} W")
