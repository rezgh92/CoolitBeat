import numpy as np
from scipy import stats
# 1. CoolIT 3-plate scatter vs PRISM like-for-like margin
ci = np.array([32.5,35.2,35.6]); tc5=np.array([41.5,44.2,44.0])
tc = np.array([[26.8,34.7,32.3],[29.9,33.5,34.7],[31.5,37.6,39.0],[34.6,39.3,39.0],[41.5,44.2,44.0],[29.0,33.6,35.2],[29.0,30.8,32.6],[37.7,27.6,27.7]])
print("CoolIT plate avgs", ci, "mean %.2f sd %.2f"%(ci.mean(), ci.std(ddof=1)))
print("CoolIT per-plate max", tc.max(axis=0), "mean of plate maxima %.2f"%tc.max(axis=0).mean())
for name, mu in [("PRISM paste corrected",31.8),("PRISM paste draft",30.4),("PKG-A paste",30.6),("PRISM PCM corrected",29.9)]:
    for sd in (1.0,1.7):
        se=np.sqrt(ci.var(ddof=1)/3+sd**2/3); d=ci.mean()-mu
        # Welch dof
        v1=ci.var(ddof=1)/3; v2=sd**2/3; dof=(v1+v2)**2/(v1**2/2+v2**2/2)
        p=2*(1-stats.t.cdf(d/se,dof))
        print(f"{name:24s} sd={sd}: diff {d:.2f} K, t={d/se:.2f}, dof {dof:.1f}, p={p:.3f}, margin vs best CoolIT plate {ci.min()-mu:+.2f} K")
# 2. Heat reuse: outlet temperature at headroom inlet
cp=3930; rho=1020
for lpmkw in (0.75,1.0,1.2):
    dT=1000/(lpmkw/60000*rho*cp)
    print(f"{lpmkw} LPM/kW: coolant rise {dT:.1f} K; CoolIT inlet 40.8 -> out {40.8+dT:.1f}; CoolIT PCM 44.7 -> {44.7+dT:.1f}; PRISM PCM corr 50.2 -> {min(50.2,65-dT)+dT:.1f}; paste corr 46.3 -> {min(46.3,65-dT)+dT:.1f}")
# 3. Guard blinding without tray cartridge (fouling-filtration: 5 cm2 50um port cartridge 13 d at 1e-4/mL to 50% blocked)
for A in (25,):
    for c in (1e-4,1e-3,1e-2):
        print(f"guard {A} cm2 at {c:g}/mL: ~{13*A/5*1e-4/c:.0f} days to 50% blockage")
# 4. Loop-level share of plate dP saving (hydraulics verifier: tray loop single UQD08 40-49 vs 56-79 kPa)
for rack_cdu in (80,124,180):
    p=np.array([40,49]); c=np.array([56,79])
    print(f"rack+CDU {rack_cdu} kPa: total PRISM {p+rack_cdu} vs CoolIT {c+rack_cdu} -> saving {100*(1-(p+rack_cdu)/(c+rack_cdu))}%")
# pump energy value per 100 MW
plates=6700; dW=6.5-1.8
print("pump power saving per 100 MW (plate-only, hydraulic): %.1f kW; at pump eff 0.5: %.1f kW; $/yr at 0.08 $/kWh: %.0f k"%(plates*dW/1e3, plates*dW/0.5/1e3, plates*dW/0.5*8760*0.08/1e6))
# 5. Incumbent + LM vs PRISM
print("CoolIT-like + LM (synthesis lever 1): avg %.1f max %.1f ; PRISM PCM corrected 29.9/34.8 ; PRISM LM corrected 24.8/28.7"%(34.5-7.1,44.3-9.0))
# 6. Transient: near-die heat capacity per area, Cu
rhoc=8930*385
for t in (1.0,2.0):
    print(f"Cu base {t} mm: heat capacity {rhoc*t*1e-3/1e4:.2f} J/(K cm2); diffusion time {(t*1e-3)**2/1.1e-4*1e3:.0f} ms")
# 7. Tariff exposure per plate (Section 232: 50% full value if 'almost entirely Cu', 25% derivative)
for cost in (160,209,162):
    print(f"factory cost {cost}: customs value ~ transfer price 1.3x -> tariff 25% {0.25*1.3*cost:.0f}, 50% {0.5*1.3*cost:.0f} $/plate")
# 8. Shock load: plate mass on package
for m in (1.74,1.17,0.85):
    print(f"mass {m} kg at 30 g / 50 g: {m*9.81*30:.0f} / {m*9.81*50:.0f} N")
# 9. TTV capacity vs claims
print("TTV-A limit 18 kW; Q capacity claims 19.4 (PCM), 26.4 (LM), 23.3 (P+PCM), 34.1 (P+LM); TTV-100 at 15 kW: %.0f W/cm2 = %.0f%% of 155 rating"%(15000/100,15000/100/155*100))
# 10. 350 W/cm2 heater
print("350 W/cm2 die on AlN heater rated 155 W/cm2: %.1fx rating"%(350/155))
# 11. R'' comparisons core
print("PRISM core conv+base R'' = %.3f cm2K/W; with caloric %.3f; with PCM TIM total %.3f"%((10.5+3.3)/128,(10.5+3.3+7.6)/128,(10.5+3.3+7.6+7.1)/128))
