# Reconstruction arithmetic for gap-coolit-dp-flow-curves-and-claim-baselines.md
import math
rho=1010.0; cp=3930.0; mu=1.45e-3   # PG25 ~45-50 C
def mdot(lpm): return lpm/60/1000*rho
print("=== A. Image-scale hypotheses (im-002 top view: plate 387 x 360 px, bar 60 px, barb ridge 32 px, hole span 320 px; im-000: hose OD 61-69 px, clamp band ~24 px, TB pitch 30.6 px true, screw head ~45 px; im-000/im-002 scale ratio 1.43) ===")
hyps=[("A: TB pitch 5.08 mm",5.08/21.4),("B: TB pitch 7.62 mm / 3/8in hose / 5-6 mm band",7.62/21.4),("C: 8 mm band / 1/2in hose / TB 10.16",8.0/24*1.43),("D: 12.7 mm band / 3/4in hose",12.7/24*1.43)]
for name,s in hyps:
    print(f"{name:48s} scale {s:.3f} mm/px(im-002): plate {387*s:5.0f} x {360*s:5.0f} mm = {387*s*360*s/100:5.0f} cm2 | bar {60*s:4.1f} mm | barb OD {32*s:4.1f} mm | half-flow-length {(387-60)/2*s:4.0f} mm | hose OD {65/1.43*s:4.1f} mm | screw head {45/1.43*s:4.1f} mm | clamp band {24/1.43*s:4.1f} mm")
print()
print("=== B. Implied heated area / heat flux for the 15 kW plate under unit-R hypotheses (max-case basis 0.00295 K/W; avg 0.00229) ===")
for Rpp in [0.18,0.20,0.225,0.25,0.30]:
    print(f"R''max={Rpp:.3f} cm2K/W -> A={Rpp/0.00295:5.0f} cm2 ({math.sqrt(Rpp/0.00295)*10:4.0f} mm sq) q''={15000/(Rpp/0.00295):4.0f} W/cm2 | if avg basis: A={Rpp/0.00229:5.0f} cm2 q''={15000/(Rpp/0.00229):4.0f} W/cm2")
print()
print("=== C. 4 kW plate R vs flow reconstruction (max-case; heater 25 cm2 vs 20 cm2; R(6.06)=9.0 mK/W anchor) ===")
# model: R = R_fixed(TIM+base) + R_conv(Q) + f_cal/(m cp); f_cal = fraction of outlet rise seen by max-case TC (0.8 split-flow near exit)
for A,label in [(25,"25 cm2 (50x50 heater)"),(20,"20 cm2")]:
    for fcal in [0.8,1.0]:
        for Rconv6 in [2.5,3.5]:   # mK/W at 6.06 LPM
            cal6=fcal*1e3/(mdot(6.06)*cp); Rfix=9.0-cal6-Rconv6
            out=[]
            for q in [4.28,5.17,6.06,7.0,8.0]:
                cal=fcal*1e3/(mdot(q)*cp); Rc=Rconv6*(6.06/q)**0.4; R=Rfix+Rc+cal
                out.append(f"{q:4.2f}LPM:{R:5.2f}")
            slope=((Rfix+Rconv6*(6.06/4.28)**0.4+fcal*1e3/(mdot(4.28)*cp))-9.0)/(4.28-6.06)
            print(f" {label:22s} fcal={fcal} Rconv@6.06={Rconv6} -> Rfix(TIM+base)={Rfix:4.2f} mK/W ({Rfix*A/1e3:.3f} cm2K/W) | "+" ".join(out)+f" | slope {slope:5.2f} mK/W per LPM; caloric share of 4.28->6.06 change {100*fcal*(1e3/(mdot(4.28)*cp)-1e3/(mdot(6.06)*cp))/((Rfix+Rconv6*(6.06/4.28)**0.4+fcal*1e3/(mdot(4.28)*cp))-9.0):3.0f} %")
print()
print("=== D. 4 kW loop decomposition: 8 psi = 55.2 kPa at 6.06 LPM (assumed) ===")
def dp_cv_kpa(lpm,cv,sg=1.02): return sg*(lpm/3.785/cv)**2*6.895
for qd,cv in [("UQD04-class pair, Cv~1.2",1.2),("UQD04-class pair, Cv~1.8",1.8),("UQD06-class pair, Cv~3.0",3.0)]:
    for hose in [3.0,8.0]:
        two=2*dp_cv_kpa(6.06,cv)
        print(f" {qd:26s} x2 = {two:5.1f} kPa + hoses/fittings {hose:3.0f} kPa -> plate-only {55.2-two-hose:5.1f} kPa ({(55.2-two-hose)/6.895:4.1f} psi) at 6.06 LPM; at 4.28 LPM (n=1.3) {(55.2-two-hose)*(4.28/6.06)**1.3:5.1f} kPa")
print()
print("=== E. 15 kW plate-only dP scenarios at 18 LPM (laminar skived core scaling from the 4 kW plate-only estimate) ===")
# core dP ~ u * L / Dh^2 ; u per channel ~ Q/(N*H*gap) ; N ~ plate length / pitch ; L = half-width
# scale factor from 4 kW (50 mm plate, L=~20 mm, Q=6.06) to 15 kW (plate W, L=(W-bar)/2, Q=18) at same fins:
for W,bar in [(108,17),(138,21),(185,29)]:
    L15=(W-bar)/2; N15=W; L4=20.0; N4=50.0
    fac=(18/6.06)*(N4/N15)*(L15/L4)
    for p4 in [20,30,45]:
        print(f" plate {W} mm (bar {bar}, half-length {L15:.0f} mm): core scale factor {fac:4.2f} x 4 kW plate-only {p4} kPa -> {p4*fac:5.0f} kPa core (same fin pitch, laminar)")
print(" (finer fins or taller fins change this by (pitch ratio)^2 / (height ratio); a 2-slot (double split) feed halves L and halves the factor)")
print()
print("=== F. Port losses at 18 LPM for the barbed TTV ports seen in the photo (K~1.5 per port incl. entry/exit, 2 ports) ===")
for name,d in [("3/8in barb bore 7 mm",7e-3),("1/2in barb bore 9.5 mm",9.5e-3),("5/8in barb bore 12.5 mm",12.5e-3)]:
    v=(18/60/1000)/(math.pi*d*d/4); print(f" {name:24s} v={v:4.1f} m/s, 2 ports x K1.5 = {2*1.5*0.5*rho*v*v/1e3:5.1f} kPa")
print()
print("=== G. Thermal-only falsifiability of 'equal dT at lower LPM/kW' (no CoolIT dP needed) ===")
for lpmkw in [1.2,1.0,0.9,0.75]:
    q=lpmkw*15; dTo=15000/(mdot(q)*cp)
    print(f" {lpmkw:4.2f} LPM/kW ({q:4.1f} LPM): outlet rise {dTo:5.2f} K, mean-fluid rise {dTo/2:5.2f} K -> extra vs 1.2 LPM/kW: outlet +{dTo-12.55:4.2f} K, mean +{(dTo-12.55)/2:4.2f} K; our (TIM+base+conv) must be <= CoolIT's minus {(dTo-12.55)/2:4.2f} K (avg basis) / {(dTo-12.55)*0.8:4.2f} K (max-case near exit)")
print()
print("=== H. Hydraulic power at 18 LPM for scenario plate dPs ===")
for dp in [15,25,35,45,60,90]:
    print(f" {dp:3d} kPa: {dp*1e3*18/60/1000:5.1f} W hydraulic, {dp*1e3*18/60/1000/0.35:5.1f} W electric at 35 % pump eff")
