# TIM2 interface arithmetic for the gap report (units: cm2-K/W, um, W/mK, W/cm2, K)
import math
def Rpp(blt_um, k, Rc=0.0):      # cm2-K/W ; BLT/k in m2K/W *1e4
    return blt_um*1e-6/k*1e4 + Rc
fluxes=[67,128,200,300]
print("1. R'' and dT = q''*R'' for candidate interfaces (Rc = two contact resistances, cm2-K/W)")
cases=[("grease k3.5, 25um, Rc.012",25,3.5,0.012),("grease k3.5, 50um",50,3.5,0.012),("grease k3.5, 100um (warped)",100,3.5,0.012),
       ("X23-7921-5 k6, 25um (TDS 0.050)",25,6.0,0.008),("X23-7921-5 k6, 50um",50,6.0,0.008),("X23-7921-5 k6, 100um",100,6.0,0.008),
       ("PTM7950 k8.5, 25um, Rc.02",25,8.5,0.02),("PTM7950 k8.5, 50um",50,8.5,0.02),
       ("Galinstan k16.5, 25um, Rc.004",25,16.5,0.004),("EGaIn k26, 25um",25,26,0.004),("Conductonaut-class k73, 25um",25,73,0.004),("LM k26, 50um",50,26,0.004),
       ("Indium solder k86, 100um, Rc.005",100,86,0.005),("Indium solder k86, 200um",200,86,0.005),
       ("Indium foil HeatSpring 200um, Rc.04 (2 dry faces)",200,86,0.04),
       ("Graphite pad k(z)=20, 150um, Rc.03",150,20,0.03)]
for n,b,k,rc in cases:
    r=Rpp(b,k,rc); print(f"  {n:48s} R''={r:.3f}  dT@{fluxes[0]}={fluxes[0]*r:5.1f}  @128={128*r:5.1f}  @200={200*r:5.1f}  @300={300*r:5.1f} K")
print("\n2. CoolIT TC8 plate-to-plate spread 10.1 K (37.7 vs 27.6 K) expressed as BLT difference at 128 W/cm2:")
dR=10.1/128
for k in (3.0,3.5,6.0,8.5): print(f"  k={k}: dR''={dR:.3f} cm2-K/W -> dBLT={dR*1e-4*k*1e6:5.1f} um")
print("\n3. Ni plating on the contact face / inside channels: R''=t/k")
for name,k in (("electroless Ni-P high-P k5",5),("electroless Ni-P mid-P k10",10),("electrolytic (sulfamate/bright) Ni k80",80)):
    print("  "+name+": "+", ".join(f"{t}um={t*1e-6/k*1e4:.4f} cm2K/W ({300*t*1e-6/k*1e4:.1f} K @300)" for t in (3,5,10,15)))
print("  channel-gap loss: 2 x t on a 100 um gap:", ", ".join(f"{t}um -> {2*t} % " for t in (3,5,10)))
print("\n4. Clamp load: pressure x area")
for A,label in ((16,"B300 die pair 16 cm2"),(33,"Rubin Ultra 4-die 33 cm2"),(100,"Rubin lid ~100 cm2"),(117,"CoolIT TTV 117 cm2")):
    print(f"  {label}: "+", ".join(f"{p} psi={p*6895*A*1e-4:.0f} N" for p in (10,20,30,50)))
print("\n5. Liquid metal mass and cost at 25 um BLT: ", ", ".join(f"{A} cm2 -> {A*25e-4*6.4:.2f} g" for A in (16,33,100)), "(rho 6.4 g/cm3)")
print("\n6. CTE shear per 55 K cycle (10-65 C), Cu plate (16.5 ppm) vs Si die (2.6 ppm), half-length L/2:")
for L in (40,60,108): print(f"  L={L} mm: {(16.5-2.6)*1e-6*55*L/2*1e3:.1f} um -> shear strain at 25 um BLT = {(16.5-2.6)*1e-6*55*L/2*1e3/25:.2f}")
print("\n7. Paste at 300 W/cm2 cannot fit a 35 K budget: paste 0.05-0.10 -> ", 300*0.05, "-", 300*0.10, "K of TIM alone; LM 0.015 ->", 300*0.015, "K")
