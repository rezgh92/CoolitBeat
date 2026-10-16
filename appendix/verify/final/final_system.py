"""System-level, sustainability, landed-cost, statistics, reliability, budget and probability numbers for the final architecture.
Inputs are taken from the verifier scripts (named per line); assumptions are labelled. Run: python3 final_system.py > final_system.out"""
import math
import numpy as np
from scipy import stats
P = print
PLATES_100MW = 100e6/15e3
P("## 1. Hydraulic stack, CDU to plate (18 LPM per 15 kW package; reference rack = 18 trays x 1 package = 324 LPM, 270 kW; 4 racks ~ 1.08 MW)")
plate = {"Rev A (PKG-A + outlet row)": (7.6, 6.0, 10.0), "CoolIT-like reconstruction": (22.0, 17.0, 42.0)}
stub_barb = 3.0                     # stubs + 1/2-in barbs, both plates (verify/loop_rack.py basis, approx)
uqd_pair = (14.0, 24.0)             # vendor Cv 3.65-4.75 (verify-hydraulics)
hose = (3.0, 6.0)                   # 1 m 1/2-in hose pair + fittings (loop_rack.py)
tray_P = (40 + 1.7, 49 + 1.7); tray_C = (56, 79)   # verify-hydraulics tray loop single UQD08; PKG-A adds ~1.7 kPa over the draft plate
P(f"tray loop (single UQD08): Rev A {tray_P[0]:.0f}-{tray_P[1]:.0f} kPa vs CoolIT-like {tray_C[0]}-{tray_C[1]} kPa; dual UQD08: Rev A ~17-20 kPa")
for rc in (80, 124, 180):
    s = [100*(1-(tray_P[i]+rc)/(tray_C[i]+rc)) for i in (0, 1)]
    P(f"rack + CDU {rc} kPa: loop head Rev A {tray_P[0]+rc:.0f}-{tray_P[1]+rc:.0f} vs {tray_C[0]+rc}-{tray_C[1]+rc} kPa -> saving {s[0]:.0f}-{s[1]:.0f} %")
# head-limited CDU: H_avail = a (N/Nr)^2 + b_branch  -> N/Nr = sqrt((H-b)/a); assumption H 250 kPa, a 100 kPa at reference N
H, a = 250.0, 100.0
for lab, b in (("Rev A", np.mean(tray_P)+20), ("CoolIT-like", np.mean(tray_C)+20)):
    P(f"head-limited CDU (assumed 250 kPa available, 100 kPa CDU+piping at reference flow, 20 kPa rack manifold+hoses): {lab} N/Nref = {math.sqrt((H-b)/a):.3f}")
P(f"-> racks per head-limited CDU: +{100*(math.sqrt((H-np.mean(tray_P)-20)/a)/math.sqrt((H-np.mean(tray_C)-20)/a)-1):.0f} % for homogeneous Rev A racks (assumption-driven)")
dW = (22.0-7.6)*0.3          # W hydraulic per plate at 18 LPM (0.3 L/s)
P(f"pump power saved per plate {dW:.1f} W hydraulic, {dW/0.5:.1f} W electrical at 50 % wire-to-water; per 100 MW: {PLATES_100MW*dW/0.5/1e3:.0f} kW -> US${PLATES_100MW*dW/0.5/1e3*8760*0.08/1e3:.0f}k/yr at US$0.08/kWh")
P(f"CDU capex credit when head-limited (research base US$9-25 per plate): US${PLATES_100MW*9/1e3:.0f}-{PLATES_100MW*25/1e3:.0f}k per 100 MW, one-time")
P("mixed racks: Rev A branches need 20-50 kPa keyed orifices (verify-hydraulics rack.py): system saving = 0")
mu = {17: 2.7, 25: 2.1, 45: 1.25}   # PG25 viscosity mPa.s (table values, +/-10 %)
for T, m in mu.items():
    P(f"start-up {T} C: Rev A plate dP at 18 LPM ~{6.05 + 1.55*m/1.25:.1f} kPa (inertial 6.05 + viscous 1.55 x mu ratio); CoolIT-like ~{6.0 + 16.0*m/1.25:.0f} kPa (16 kPa viscous assumed)")

P("\n## 2. Return temperature and heat reuse (15 kW, max-case limit 85 C, return cap 65 C)")
rho, cp = 1005, 3930
for lpmkw in (0.75, 1.0, 1.2):
    dT = 1000/(lpmkw/60000*rho*cp)
    for lab, tin in (("CoolIT paste", 40.8), ("CoolIT PCM", 44.7), ("Rev A paste", 46.3), ("Rev A PCM", 50.2)):
        pass
    P(f"{lpmkw} LPM/kW (rise {dT:.1f} K): return CoolIT paste {min(40.8,65-dT)+dT:.1f} / PCM {min(44.7,65-dT)+dT:.1f} C; Rev A paste {min(46.3,65-dT)+dT:.1f} / PCM {min(50.2,65-dT)+dT:.1f} C (thermal limit, P50)")
# heat pump lifting reuse heat to 80 C supply; Carnot fraction 0.5; source = return - 3 K approach
def cop(src_C, sink_C=80.0, f=0.5):
    Th, Tc = sink_C+273.15+3, src_C+273.15-3; return f*Th/(Th-Tc)
for lab, ret in (("CoolIT PCM 1.2 LPM/kW", 57.2), ("Rev A PCM 1.2 LPM/kW", 62.7)):
    P(f"{lab}: return {ret} C -> heat-pump COP to 80 C ~{cop(ret):.1f}")
reuse = 20.0  # MW of DC heat reused (EnEfG ERF 20 % for 100 MW)
w1 = reuse/(cop(57.2)-1); w2 = reuse/(cop(62.7)-1)
P(f"20 MW reused (ERF 20 % of 100 MW): heat-pump electricity {w1:.1f} vs {w2:.1f} MW -> {w1-w2:.1f} MW less; at 6,000 h/yr and US$0.10/kWh: US${(w1-w2)*6000*100/1e6:.2f} M/yr (contingent on loop-wide supply temperature)")
# WUE illustration: dry cooler approach 8 K; adiabatic needed when ambient > supply - 8
for site, h_lo, h_hi in (("hot-dry (Phoenix-class)", 800, 200), ("temperate (Frankfurt-class)", 5, 0), ("hot-humid (Singapore-class)", 0, 0)):
    saved = h_lo - h_hi
    P(f"{site}: adiabatic hours at 45 C supply ~{h_lo}, at +5.5 K ~{h_hi} (illustrative climate assumption) -> ~{saved} h removed; water at 0.4-0.8 L/kWh-rejected x 100 MW: {saved*100e3*0.4/1e6:.0f}-{saved*100e3*0.8/1e6:.0f} thousand m3/yr")
# embodied carbon
cu_buy, ag_g = 1.43, 5.0
for lab, cu, ag in (("Rev A PKG-A (vacuum braze, BAg)", 1.43, 5.0), ("Rev A C2 (Cu-Sn TLP)", 1.43, 0.0), ("incumbent like-sized (est.)", 2.0, 2.5)):
    co2 = cu*4.5 + ag*1e-3*200 + 3.0*0.4   # Cu mill product ~4-5 kgCO2e/kg; Ag ~150-250 kgCO2e/kg; ~3 kWh process at 0.4
    P(f"{lab}: cradle-to-gate ~{co2:.1f} kgCO2e (Cu {cu} kg buy, Ag {ag} g; screening factors, ISO 14067 study needed)")
P(f"pump-energy saving {dW/0.5*8.76:.0f} kWh/yr per plate -> {dW/0.5*8.76*0.4:.0f} kgCO2e/yr at 0.4 kg/kWh (homogeneous racks only)")

P("\n## 3. Landed cost per plate at a US data centre (PKG-A US$162 factory cost at 100k in Asia; C2 US$141)")
for base in (162.0, 141.0):
    for site, f, frt in (("TW", 1.0, 4), ("VN", 0.97, 5), ("MX", 1.08, 3), ("US", 1.30, 1)):
        fc = base*f + (6 if site == "US" else 0)  # US: COMEX copper premium on ~1.4 kg buy (~US$4-8)
        cv = 1.3*fc
        tar = [0.0, 0.25*cv, 0.50*cv] if site != "US" else [0.0, 0.0, 0.0]
        P(f"base {base:.0f} | {site}: factory {fc:.0f} + freight {frt} + Sec.232 exposure 0 / 25 % / 50 % of customs value ({cv:.0f}) = " + " / ".join(f"{fc+frt+t:.0f}" for t in tar))

P("\n## 4. Statistics of the head-to-head")
ci = np.array([32.5, 35.2, 35.6]); sdC = ci.std(ddof=1); seC = sdC/math.sqrt(3)
for alpha in (0.05,):
    tcrit = stats.t.ppf(1-alpha, 2)
    P(f"Welch vs CoolIT's 3 published plates (SD {sdC:.2f} K): even with infinite PRISM plates the one-sided alpha {alpha} margin needed is > {tcrit*seC:.2f} K (dof -> 2)")
for margin in (3.4, 2.6):
    for sd in (1.0, 1.7):
        for n in range(2, 20):
            nc = margin/(sd/math.sqrt(n)); tc = stats.t.ppf(0.95, n-1)
            pw = 1-stats.nct.cdf(tc, n-1, nc)
            if pw >= 0.8: break
        P(f"one-sample test vs the published 34.4 K (fixed reference), margin {margin} K, plate SD {sd} K: n = {n} plates for power 0.8 at one-sided alpha 0.05")
for margin, sd in ((3.4, 1.0), (3.4, 1.7)):
    for n in (3, 5, 8):
        se = math.sqrt(sdC**2/3 + sd**2/n); v1, v2 = sdC**2/3, sd**2/n; dof = (v1+v2)**2/(v1**2/2 + v2**2/(n-1))
        P(f"Welch, margin {margin}, SD {sd}, n {n}: t {margin/se:.2f}, dof {dof:.1f}, one-sided p {1-stats.t.cdf(margin/se, dof):.3f}")

P("\n## 5. Reliability demonstration and mechanical loads")
for R, C in ((0.90, 0.90), (0.95, 0.90), (0.90, 0.95), (0.99, 0.90)):
    P(f"zero-failure success run R{int(R*100)}/C{int(C*100)}: n = {math.ceil(math.log(1-C)/math.log(R))}")
for lab, m in (("Rev A PKG-A plate", 1.17), ("+ load frame 0.3-0.6 kg", 1.62), ("draft PRISM", 1.74), ("CoolIT est.", 1.4)):
    P(f"{lab} {m} kg: inertial load at 30 g / 50 g = {m*9.81*30:.0f} / {m*9.81*50:.0f} N")

P("\n## 6. 12-month budget (US$ M), verifier-completed")
lines = {"Labour 14.5 FTE (draft)": (3.30, 3.30), "Added FTE: BD/customer eng 1.5, SQE Asia 1, compliance 0.5, cost eng 0.5": (0.60, 0.80),
         "PG25 rig, upgraded 25 -> 40 kW": (0.60, 0.70), "TTVs incl. 100 cm2 + 25 cm2 + high-flux Cu-neck TTV-D": (0.38, 0.45),
         "Flow, printed-manifold, fouling rigs": (0.23, 0.23), "IR flow-screen station": (0.20, 0.20), "Confocal pressure scan, He leak, D5470": (0.30, 0.60),
         "Prototypes and coupons": (0.35, 0.35), "Build-B dies (moved forward from M12-18)": (0.25, 0.60), "CFD/FEA licences, CT services": (0.10, 0.25),
         "Lab fit-out": (0.10, 0.30), "Reliability incl. chemistry matrix, shock/vib/orientation": (0.38, 0.50), "Independent lab": (0.15, 0.15),
         "IP: FTO charts + opinions, provisionals": (0.25, 0.35), "Compliance: CBP ruling, 62368-1 support, PFAS BOM": (0.05, 0.10), "E0 incumbent plates and couplings": (0.04, 0.06)}
lo = sum(v[0] for v in lines.values()); hi = sum(v[1] for v in lines.values())
for k, v in lines.items(): P(f"- {k}: {v[0]:.2f}-{v[1]:.2f}")
P(f"subtotal {lo:.2f}-{hi:.2f}; with 15-20 % contingency {lo*1.15:.1f}-{hi*1.20:.1f}")

P("\n## 7. Programme probabilities (model x programme factors; programme factors are judgement)")
pj, pr = 0.80, 0.90   # join route qualified by G1 (<= 3-month slip incl. fallbacks); rig/TTV repeatability by M6
for lab, pm in (("decisive PCM (<= 31 / <= 36 K) at M12", 0.60), ("paste avg win at 117 cm2", 0.81), ("paste max win", 0.90),
                ("PCM avg+max win and dP", 0.95), ("paste avg win at 100 cm2 (R-grade)", 0.44), ("paste avg win at 100 cm2 (R+ PKG-B)", 0.69)):
    P(f"- {lab}: model {pm:.2f} x join {pj} x rig {pr} = {pm*pj*pr:.2f}")

P("\n## 8. Facility value vs premium per 100 MW (15 kW class)")
for lab, prem in (("PKG-A vacuum braze", 162-126), ("C2 belt TLP", 141-126)):
    price_prem = prem/0.7*PLATES_100MW/1e6
    for hk, k in (("P50 +5.5 K", 5.5), ("P90 +0.6-1.8 K (use 1.2)", 1.2)):
        P(f"{lab}: price premium US${price_prem:.2f} M; value at {hk}: US${0.54*k:.1f}-{1.09*k:.1f} M -> {0.54*k/price_prem:.0f}-{1.09*k/price_prem:.0f}x")
P("GPU class (37,500 plates per 100 MW): lean PRISM-G US$129-148 vs incumbent ~US$110: premium US$19-38 -> price premium US$1.0-2.0 M; value at 1-3 K (max only) US$0.5-3.3 M -> 0.3-3x: not a value case")

P("\n## 9. P&L sketch per plate (planning assumptions)")
for lab, vol, asp, cost in (("Hyperscaler ramp 10k/yr (CM, laser/CNC parts)", 10e3, 600, 400), ("Hyperscaler 100k/yr, PKG-A", 100e3, 330, 162), ("Hyperscaler 100k/yr, C2", 100e3, 330, 141)):
    cm_margin = 0.12*cost    # CM margin on top of factory cost
    war = 0.03*asp; gp = asp - cost - cm_margin - war
    P(f"{lab}: ASP {asp}, factory {cost}, CM margin {cm_margin:.0f}, warranty reserve 3 % {war:.0f} -> our gross profit {gp:.0f}/plate = US${gp*vol/1e6:.1f} M/yr ({gp/asp*100:.0f} %)")
opex = 5.0
P(f"opex after qualification ~US${opex} M/yr (engineering, BD, quality, insurance US$0.3-0.6 M, IP reserve) -> break-even ~{opex*1e6/150/1e3:.0f}k plates/yr at ~US$150 gross profit")
