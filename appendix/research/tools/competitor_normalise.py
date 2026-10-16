# Normalisation of the competitor plate data points already on disk to common bases.
# PG25 at ~45-50 C: rho 1010 kg/m3, cp 3930 J/kgK (sibling metrics_calc.py). Water: 990, 4180.
import math
def caloric(P, lpm, fluid="PG25"):
    rho,cp = (1010,3930) if fluid=="PG25" else (990,4180)
    m = lpm/60/1000*rho
    return P/(m*cp)
print("=== A. Vendor / independent points: dT, caloric split, R_case-mean-fluid, R'' at assumed heated area ===")
pts = [
 # name, P W, R K/W (case-to-inlet unless noted), flow LPM, fluid, dP kPa, assumed heated area cm2 (die), note
 ("ToneCooling GB300 plate (V,S)",1067,0.0130,1.7,"PG25",12.06,16.0,"B300 2 reticle dies ~16 cm2; if Rjf on silicon add nothing (already incl. TIM1)"),
 ("ToneCooling at 0.0133",1067,0.0133,1.7,"PG25",12.06,16.0,""),
 ("FiberMall GB200 target (S) at 1.2 kW",1200,0.030,1.8,"PG25",20.0,16.0,"<0.03, <20 kPa; 1.8 LPM assumed per GPU plate"),
 ("FiberMall if 1.8 LPM were per 2.7 kW superchip",2700,0.030,1.8,"PG25",20.0,16.0,"implausible: dT 81 K"),
 ("OCP OAI 1 kW OAM (I)",1000,0.0155,3.5,"PG25",float('nan'),8.0,"2-5 LPM 'high flow'; PCM TIM; OAM die ~8 cm2 assumed"),
 ("JetCool H100 SmartPlate (V)",700,0.021,3.2,"PG25",float('nan'),8.1,"Rjf? vs air 0.122; H100 die 8.1 cm2"),
 ("JetCool RTX PRO 6000 @0.6 LPM (datasheet, Rjf)",600,0.058,0.6,"PG25",float('nan'),7.5,"GB202 ~750 mm2"),
 ("JetCool RTX PRO 6000 @0.9 LPM (datasheet, Rjf, interp)",600,0.048,0.9,"PG25",float('nan'),7.5,""),
 ("JetCool RTX PRO 6000 @1.8 LPM (datasheet, Rjf)",600,0.040,1.8,"PG25",float('nan'),7.5,""),
 ("Wakefield on-chip plate (V)",700,0.0267,1.6,"PG25",float('nan'),8.1,"700 W, 1.6 LPM"),
 ("Iceotope KUL SINK (V)",1000,0.039,7.0,"PG25",float('nan'),8.0,"precision immersion, not a plate"),
 ("ORNL Cu diamond pin-fin (I)",1000,0.0069,3.0,"water",9.0,56.25,"75x75 mm plate, 17.8 W/cm2 -> heater = full 56 cm2"),
 ("CoolIT 4 kW (V)",4000,0.009,6.06,"PG25",55.0,25.0,"max-case incl. TIM; 55 kPa is full loop incl. QDs; 50x50 mm heater favoured"),
 ("CoolIT 15 kW avg (V)",15000,0.00229,18.0,"PG25",float('nan'),100.0,"area inferred 76-117 cm2; 100 used"),
 ("CoolIT 15 kW worst TC (V)",15000,0.00295,18.0,"PG25",float('nan'),100.0,""),
 ("Boyd HybridKIT DSC power module (V)",float('nan'),0.026,10.0,"WEG50",12.5,float('nan'),"Rth basis unknown; not a GPU plate"),
]
print(f"{'point':58s} {'P W':>6s} {'LPM':>5s} {'LPM/kW':>6s} {'dT K':>6s} {'cal K':>6s} {'R_cmf mK/W':>10s} {'A cm2':>6s} {'q W/cm2':>8s} {'R'' c-in':>8s} {'R'' c-mf':>8s} {'dP kPa':>6s}")
for n,P,R,lpm,fl,dp,A,note in pts:
    if math.isnan(P):
        print(f"{n:58s} {'n/a':>6s} {lpm:5.1f} {'':>6s} {'':>6s} {'':>6s} {'':>10s} {'':>6s} {'':>8s} {'':>8s} {'':>8s} {dp:6.1f}  {note}")
        continue
    dT = R*P
    cal = caloric(P,lpm,"PG25" if fl=="PG25" else "water")
    Rcmf = (dT-cal/2)/P
    q = P/A
    print(f"{n:58s} {P:6.0f} {lpm:5.2f} {lpm/P*1000:6.2f} {dT:6.1f} {cal:6.1f} {Rcmf*1e3:10.2f} {A:6.1f} {q:8.0f} {R*A:8.3f} {Rcmf*A:8.3f} {dp:6.1f}  {note}")

print()
print("=== B. Flow-normalisation of the ToneCooling and FiberMall points to 1.2 and 1.0 LPM/kW ===")
print("Model: R_case-inlet(Q) = R_fixed + R_conv(Q) + 0.5/(m cp); R_conv ~ Q^-0.3 (laminar developing / skived band, exponent 0.2-0.4);")
print("dP ~ Q^1.3 (laminar core + quadratic manifold, sibling exponent band 1.3-1.75). R_fixed = TIM + base spreading, taken as 40 % of (R - caloric/2) at the quoted point.")
def normalise(P,R,lpm,dp,target_lpmkw,n_conv=0.3,n_dp=1.3,fixed_frac=0.4):
    cal = caloric(P,lpm)
    Rrest = R - 0.5*cal/P
    Rfix = fixed_frac*Rrest; Rconv = (1-fixed_frac)*Rrest
    lpm2 = target_lpmkw*P/1000
    cal2 = caloric(P,lpm2)
    R2 = Rfix + Rconv*(lpm2/lpm)**(-n_conv) + 0.5*cal2/P
    dp2 = dp*(lpm2/lpm)**n_dp if not math.isnan(dp) else float('nan')
    return lpm2,R2,R2*P,dp2
for n,P,R,lpm,dp in [("ToneCooling 0.013 @1.7 LPM, 12.06 kPa",1067,0.013,1.7,12.06),("FiberMall <0.03 @1.8 LPM, <20 kPa (1.2 kW)",1200,0.030,1.8,20.0),("CoolIT 4 kW <0.009 @6.06 LPM, 55 kPa loop",4000,0.009,6.06,55.0)]:
    for t in [1.5,1.2,1.0,0.75]:
        for nd in [1.3,1.75]:
            lpm2,R2,dT2,dp2 = normalise(P,R,lpm,dp,t,n_dp=nd)
            print(f"{n:48s} -> {t:4.2f} LPM/kW = {lpm2:5.2f} LPM : R={R2*1e3:6.2f} mK/W dT={dT2:5.1f} K  dP={dp2:5.1f} kPa (n_dp={nd})")
    print()

print("=== C. Pumping power / hydraulic COP at the quoted points ===")
for n,P,lpm,dp in [("ToneCooling",1067,1.7,12.06),("FiberMall target",1200,1.8,20.0),("CoolIT 4 kW loop",4000,6.06,55.0),("ORNL pin-fin",1000,3.0,9.0),("Mikros 1 kW/cm2 claim (flow unstated, assume 1 LPM)",1000,1.0,20.7)]:
    Q = lpm/60/1000; Ph = dp*1e3*Q
    print(f"{n:52s} P={P:5.0f} W  Q={lpm:4.2f} LPM dP={dp:5.1f} kPa -> hydraulic {Ph:6.3f} W, COP_hyd {P/Ph:8.0f}, elec@35% {Ph/0.35:5.2f} W = {Ph/0.35/P*100:.3f} % of load")

print()
print("=== D. Scaling the ToneCooling-class unit resistance to the 15 kW TTV (if a Group-A skived plate were simply enlarged) ===")
for Rpp in [0.14,0.18,0.21,0.225]:
    for A in [76,100,117]:
        cal = caloric(15000,18.0)
        dT = Rpp*15000/A + cal/2   # R'' here is case-to-mean-fluid basis
        print(f"R''_c-mf={Rpp:5.3f} cm2K/W, A={A:3d} cm2: q''={15000/A:4.0f} W/cm2, dT_case-inlet avg = {dT:5.1f} K (benchmark 34.4)")

print()
print("=== E. JetCool RTX PRO 6000 datasheet curve: strip caloric, fit exponent ===")
for lpm,R in [(0.6,0.058),(1.8,0.040)]:
    cal = caloric(600,lpm); print(f"  {lpm} LPM: Rjf={R:.3f}, caloric/2 = {cal/2/600*1e3:.2f} mK/W, R_j-mean-fluid = {(R-cal/2/600)*1e3:.1f} mK/W")
r1 = 0.058-caloric(600,0.6)/2/600; r2 = 0.040-caloric(600,1.8)/2/600
print(f"  exponent of R_j-mf vs flow = {math.log(r2/r1)/math.log(3):.2f} (includes fixed die+TIM1 share, so convective exponent is steeper)")
