# Benchmark-protocol arithmetic for the CoolIT 15 kW comparison (PG25 vs water)
import statistics as st
P=15000.0
# Property sets (approximate, 25 wt% PG in water; Dow DOWFROST LC-25 class). KB values, +/-3 %.
props={
 "PG25 @25C":dict(rho=1021.0,cp=3880.0,k=0.455,mu=2.6e-3),
 "PG25 @45C":dict(rho=1010.0,cp=3930.0,k=0.475,mu=1.45e-3),
 "PG25 @51C(mean)":dict(rho=1007.0,cp=3940.0,k=0.478,mu=1.30e-3),
 "water @25C":dict(rho=997.0,cp=4180.0,k=0.607,mu=0.89e-3),
 "water @45C":dict(rho=990.0,cp=4180.0,k=0.637,mu=0.596e-3),
}
print("=== Fluid properties and Prandtl ===")
for n,p in props.items():
    Pr=p["mu"]*p["cp"]/p["k"]
    print(f"{n:16s} rho={p['rho']:.0f} kg/m3 cp={p['cp']:.0f} J/kgK k={p['k']:.3f} W/mK mu={p['mu']*1e3:.2f} mPa.s Pr={Pr:.1f}")
print()
print("=== Caloric rise at 15 kW ===")
for lpmkw in [0.75,1.0,1.2,1.5,2.0]:
    Q=lpmkw*15/60/1000  # m3/s
    for n in ["PG25 @45C","water @45C"]:
        p=props[n]; m=Q*p["rho"]; mcp=m*p["cp"]; dT=P/mcp
        print(f"{lpmkw:4.2f} LPM/kW = {lpmkw*15:5.1f} LPM | {n:11s} mdot={m:.4f} kg/s  m*cp={mcp:.0f} W/K  R_cal=1/(m cp)={1/mcp*1e3:.3f} mK/W  dT_out={dT:.2f} K  T_out={45+dT:.1f} C  T_mean={45+dT/2:.1f} C")
print()
Q=18/60/1000; p=props["PG25 @45C"]; m=Q*p["rho"]; dT=P/(m*p["cp"])
print(f"Benchmark point: 18 LPM PG25, mdot={m:.3f} kg/s, dT_bulk={dT:.2f} K, outlet={45+dT:.1f} C, mean fluid={45+dT/2:.1f} C")
print(f"Share of 34.4 K: inlet-to-outlet {dT/34.4*100:.0f} %, inlet-to-mean {dT/2/34.4*100:.0f} %")
print(f"R_case-inlet avg={34.4/P*1e3:.3f} mK/W; R_case-mean-fluid={(34.4-dT/2)/P*1e3:.3f} mK/W; R_case-outlet (LMTD-free floor)={(34.4-dT)/P*1e3:.3f} mK/W")
print()
print("=== Viscosity ratio effects (laminar: h ~ independent of mu for fixed geometry/flow; dP ~ mu) ===")
print(f"PG25 45C/25C viscosity ratio = {props['PG25 @45C']['mu']/props['PG25 @25C']['mu']:.2f}  -> laminar dP at 25 C inlet is ~{props['PG25 @25C']['mu']/props['PG25 @45C']['mu']:.1f}x that at 45 C")
print(f"PG25/water at 45 C viscosity ratio = {props['PG25 @45C']['mu']/props['water @45C']['mu']:.2f}; k ratio = {props['PG25 @45C']['k']/props['water @45C']['k']:.2f}; rho*cp ratio = {props['PG25 @45C']['rho']*props['PG25 @45C']['cp']/(props['water @45C']['rho']*props['water @45C']['cp']):.3f}")
print()
print("=== Pumping power and COP at 18 LPM (3.0e-4 m3/s) ===")
for dp in [10e3,20e3,35e3,55e3,100e3,150e3,200e3]:
    Ph=dp*Q
    print(f"dP={dp/1e3:5.0f} kPa ({dp/6894.76:5.1f} psi): hydraulic={Ph:6.1f} W  COP_hyd={P/Ph:8.0f}  elec@35%eff={Ph/0.35:6.1f} W  COP_elec={P/(Ph/0.35):7.0f}  frac of load={Ph/0.35/P*100:.2f} %")
print()
print("=== Uncertainty budget on R = (Tcase-Tin)/P (type B, k=1) ===")
import math
for dT_meas,uTC,uTin,uP_rel,uQ_rel in [(34.4,0.5,0.3,0.005,0.01),(34.4,0.2,0.1,0.003,0.005),(25.0,0.2,0.1,0.003,0.005)]:
    u_dT=math.sqrt(uTC**2+uTin**2); uR_rel=math.sqrt((u_dT/dT_meas)**2+uP_rel**2)
    print(f"dT={dT_meas} K, u(Tc)={uTC} K, u(Tin)={uTin} K, u(P)={uP_rel*100:.1f} %: u(dT)={u_dT:.2f} K, u(R)/R={uR_rel*100:.2f} %  (k=2: {2*uR_rel*100:.1f} %)")
print()
print("=== CoolIT table statistics ===")
cp={"CP1":[26.8,29.9,31.5,34.6,41.5,29.0,29.0,37.7],"CP2":[34.7,33.5,37.6,39.3,44.2,33.6,30.8,27.6],"CP3":[32.3,34.7,39.0,39.0,44.0,35.2,32.6,27.7]}
allv=[v for l in cp.values() for v in l]
print(f"n=24 mean={st.mean(allv):.2f} sd={st.stdev(allv):.2f} min={min(allv)} max={max(allv)} ; 95% of population ~ mean+/-2sd = {st.mean(allv)-2*st.stdev(allv):.1f}..{st.mean(allv)+2*st.stdev(allv):.1f}")
for k,l in cp.items():
    print(f"{k}: mean={st.mean(l):.2f} max={max(l)} spread={max(l)-min(l):.1f} max-minus-mean={max(l)-st.mean(l):.1f} sd={st.stdev(l):.2f} CoV={st.stdev(l)/st.mean(l)*100:.1f}%")
pos=[st.mean([cp[k][i] for k in cp]) for i in range(8)]
print("position means:",[round(x,1) for x in pos],"spread=%.1f"%(max(pos)-min(pos)))
print("plate means sd=%.2f K (plate-to-plate repeatability, n=3)"%st.stdev([st.mean(l) for l in cp.values()]))
print()
print("=== Unit resistance scenarios for 15 kW (area undisclosed) ===")
for A in [60,80,100,117,150]:
    print(f"A={A:3d} cm2 ({math.sqrt(A)*10:.0f} mm sq): q''={P/A:5.0f} W/cm2  R''avg={34.4/P*A:.3f}  R''max={44.2/P*A:.3f} cm2K/W ; 4 kW plate (25 cm2, 160 W/cm2): R''max<={0.009*4000/160:.3f}")
print()
print("=== Thermal-paste share at 0.05 / 0.10 cm2K/W ===")
for A in [80,117,150]:
    for Rt in [0.03,0.05,0.10]:
        print(f"A={A} cm2 TIM R''={Rt}: dT_TIM={Rt*P/A:5.1f} K ({Rt*P/A/34.4*100:4.0f} % of 34.4 K)")
print()
print("=== Transient: thermal time constant of the plate+fluid (order of magnitude) ===")
# copper plate 120x120x8 mm, fluid hold-up 10 mL
mcu=8960*0.12*0.12*0.008; Ccu=mcu*385; Cfl=1e-5*1007*3940
UA=P/(34.4-dT/2)
print(f"Cu mass={mcu:.2f} kg, C_cu={Ccu:.0f} J/K, C_fluid={Cfl:.0f} J/K, UA (case-to-mean-fluid)={UA:.0f} W/K, tau~{(Ccu+Cfl)/UA:.1f} s ; fluid residence time ~{1e-5/Q*1e3:.0f} ms")
