#!/usr/bin/env python3
"""Part B2: automotive core sweep, chosen variants with metering comb, base-thickness optima, data-centre
loss-density capability, 2x flow and cold-start bounds. Same models as pe_run.py."""
import sys, math
from dataclasses import replace
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
from coldplate_model import ColdPlate, Fluid, PG25, K_CU, K_AL
import pe_fourier as F
from pe_common import WEG65, WEG25, WEGm40, PAO65, A_MOD, FLOW, N_SW, P_SW, cartridge, ev


print("## C1. Automotive core sweep (Cu, WEG 50/50 65 C, 10 L/min, 84 cm2), PE-DS stack 2.0 mm base, sinter")
print("| gap | fin | H | L | H/t | h_eff kW/m2K | eta | Rth mean K/W | vs pin-fin 0.100 |")
print("|---|---|---|---|---|---|---|---|---|")
best = []
for gap in (0.30, 0.40, 0.50):
    for fin in (0.25, 0.30, 0.40):
        for H in (3.0, 4.0, 5.0, 6.0):
            if H/fin > 20: continue
            for L in (3.0, 4.0, 5.0):
                r = ev(cartridge("s", gap, fin, H, L, 2.0), WEG65)
                R = F.die_temps(F.module_stack(2.0e-3, "sinter"), r['h_eff'])['Rth_mean']
                best.append((R, gap, fin, H, L, r['h_eff'], r['eta']))
best.sort()
for gap_sel in (0.30, 0.40, 0.50):
    for R, gap, fin, H, L, he, eta in [b for b in best if b[1] == gap_sel][:3]:
        print(f"| {gap} | {fin} | {H} | {L} | {H/fin:.0f} | {he/1e3:.0f} | {eta:.2f} | {R:.4f} | {100*(R/0.100-1):+.0f} % |")

# chosen automotive core: 0.40 gap / 0.30 fin / 5.0 mm / L 4 mm (H/t 17), base 2.0 mm, comb 1.5 kPa @10 L/min
COMB10 = 1.5  # kPa at 10 L/min
comb18 = COMB10*(18/10)**2
cA = cartridge("PE-A core 0.40/0.30x5, L4", 0.40, 0.30, 5.0, 4.0, 2.0, orifice_kPa=comb18, hdr_u=0.4)
cDC = cartridge("PE-DS-R core 0.15/0.10x2, L4", 0.15, 0.10, 2.0, 4.0, 1.0, orifice_kPa=comb18, hdr_u=0.4)
cAl = cartridge("PE-Al core 0.50/0.50x5, L4 (Al)", 0.50, 0.50, 5.0, 4.0, 2.0, k=K_AL, orifice_kPa=comb18, hdr_u=0.4)
print("\n## C2. Chosen cores with metering comb (1.5 kPa at 10 L/min), header 0.4 m/s, 14 mm ports")
print("| core | fluid / flow | h_eff | cal frac | dP ch | dP comb | dP hdr | dP ports | dP total kPa | branch/header-head ratio |")
print("|---|---|---|---|---|---|---|---|---|---|")
for cp in (cA, cDC, cAl):
    for fl, fw in ((WEG65, 10.0), (WEG65, 20.0), (WEG25, 10.0), (WEGm40, 10.0), (WEGm40, 5.0)):
        r = ev(cp, fl, flow=fw)
        head = 0.5*fl.rho*(0.4*fw/18*18/10)**2  # header velocity 0.4 m/s at 10 L/min, scaled
        branch = (r['dp_ch_kPa']+r['dp_K_kPa']+r['dp_slot_kPa']+r['dp_orif_kPa'])*1e3
        print(f"| {cp.name} | {fl.name} {fw:.0f} L/min | {r['h_eff']/1e3:.0f} | {r['cal_frac']:.2f} | {r['dp_ch_kPa']:.2f} | {r['dp_orif_kPa']:.2f} | {r['dp_header_kPa']:.2f} | {r['dp_port_kPa']:.2f} | {r['dp_total_kPa']:.1f} | {branch/head:.0f} |")
print("Note: at -40 C the comb holes (0.6 mm, Re ~10) and ports (Re ~200) are laminar; bound the inertial terms x3: "
      "PE-A at -40 C, 10 L/min <= ~" + f"{3*(ev(cA, WEGm40)['dp_total_kPa']-ev(cA, WEGm40)['dp_ch_kPa'])+ev(cA, WEGm40)['dp_ch_kPa']:.0f} kPa")

hA = ev(cA, WEG65)['h_eff']; hDC = ev(cDC, WEG65)['h_eff']; hAl = ev(cAl, WEG65)['h_eff']
calA = ev(cA, WEG65)['cal_frac']; calDC = ev(cDC, WEG65)['cal_frac']
h_pf, _ = F.calibrate_h(0.100, F.module_stack(3.0e-3, "solder"))
print(f"\nh_eff: PE-A {hA/1e3:.0f}, PE-DS-R {hDC/1e3:.0f}, PE-Al {hAl/1e3:.0f}, pin-fin calibrated {h_pf/1e3:.1f} kW/m2K")

print("\n## C3. Base thickness optimum")
for nm, h, att in (("PE-A (sinter)", hA, "sinter"), ("PE-A (solder)", hA, "solder"), ("PE-DS-R (sinter)", hDC, "sinter")):
    print(f"- {nm}: " + ", ".join(f"{tb} mm {F.die_temps(F.module_stack(tb*1e-3, att), h)['Rth_mean']:.4f}" for tb in (0.5, 0.8, 1.0, 1.5, 2.0, 3.0)))

print("\n## C4. Final per-switch table, 10 L/min WEG 65 C (local fluid), and module level 6 x 1 kW")
mdot = FLOW/60000*WEG65.rho; dTout = N_SW*P_SW/(mdot*WEG65.cp)
R_spacer = 0.04e-3/F.K_AG + 1.0e-3/F.K_CU + 0.04e-3/F.K_AG
def dsc(L, h, s=1.0):
    rb = F.die_temps(L, h, die_scale=s); rt = F.die_temps(L, h, die_scale=s, extra_R_die=R_spacer)
    Rt = rt['Rth_mean'] - F.R_DIE/(rt['A_die_cm2']*1e-4)
    Rm = 1/(1/rb['Rth_mean']+1/Rt); return Rm, Rm*rb['Rth_max']/rb['Rth_mean']
V = [  # name, stack, h, dsc?, caloric at hottest switch (fraction of dTout), dP at 10 L/min (kPa), note
    ("Pin-fin HPD G2 class, series flow", F.module_stack(3.0e-3, "solder"), h_pf, False, 5/6, 7.6, "datasheet-calibrated"),
    ("Pin-fin, transverse (parallel phases)", F.module_stack(3.0e-3, "solder"), h_pf, False, 0.5, 7.6, ""),
    ("ShowerPower-3D class (estimate)", F.module_stack(3.0e-3, "solder"), 30e3, False, 0.5, 5.0, "KB-L band"),
    ("PE-A1 cartridge, solder (drop-in)", F.module_stack(2.0e-3, "solder"), hA, False, calA, ev(cA, WEG65)['dp_total_kPa'], ""),
    ("PE-A2 cartridge, Ag sinter", F.module_stack(2.0e-3, "sinter"), hA, False, calA, ev(cA, WEG65)['dp_total_kPa'], ""),
    ("PE-DS-R direct substrate, 0.15 mm core (filtered loop)", F.module_stack(1.0e-3, "sinter"), hDC, False, calDC, ev(cDC, WEG65)['dp_total_kPa'], "needs <=50 um abs screen"),
    ("DSC, pin-fin-class h both sides (today's DSC)", F.module_stack(1.0e-3, "sinter"), h_pf, True, 0.5, 2*6.0, "reference"),
    ("PE-DSC, PE-A core both sides", F.module_stack(1.0e-3, "sinter"), hA, True, calA, ev(cA, WEG65, flow=5.0)['dp_total_kPa'], "flow split 5+5"),
    ("PE-DSC-R, 0.15 mm core both sides", F.module_stack(1.0e-3, "sinter"), hDC, True, calDC, ev(cDC, WEG65, flow=5.0)['dp_total_kPa'], "flow split 5+5"),
    ("PE-Al cartridge (Al core on DBA)", F.module_stack(2.0e-3, "sinter", base_k=K_AL), hAl, False, ev(cAl, WEG65)['cal_frac'], ev(cAl, WEG65)['dp_total_kPa'], ""),
]
print("| variant | h_eff | Rth mean K/W | Rth max | vs pin-fin | dP kPa @10 L/min | Tj,max C (65 C in, 6x1 kW) | +I at equal Tj | SiC area at equal Tj |")
print("|---|---|---|---|---|---|---|---|---|")
ref = None
for nm, L, h, isd, cf, dp, note in V:
    if isd:
        Rm, Rx = dsc(L, h)
    else:
        r = F.die_temps(L, h); Rm, Rx = r['Rth_mean'], r['Rth_max']
    cal = cf*dTout
    Tmax = 65 + cal + P_SW*Rx
    if ref is None:
        ref = (Rm, Tmax)
    P_eq = (ref[1]-65)/(Rx + cal/P_SW); Ig = math.sqrt(P_eq/P_SW)-1
    lo, hi = 0.2, 1.6
    for _ in range(40):
        s = 0.5*(lo+hi)
        if isd:
            _, Rxs = dsc(L, h, s)
        else:
            Rxs = F.die_temps(L, h, die_scale=s)['Rth_max']
        T = 65 + cal/s + P_SW/s*Rxs
        lo, hi = (s, hi) if T > ref[1] else (lo, s)
    print(f"| {nm} | {h/1e3:.0f} | {Rm:.4f} | {Rx:.4f} | {100*(Rm/ref[0]-1):+.0f} % | {dp:.1f} | {Tmax:.1f} | {100*Ig:+.0f} % | {100*(s-1):+.0f} % |")

print("\n## C5. Data-centre 800 VDC / SST power stage in the PG25 TCS loop (45 C in, Tj limit 150 C):"
      " loss a 1.62 cm2 switch can carry")
cDCdc = cartridge("DC-R", 0.15, 0.10, 2.0, 4.0, 1.0, A=60.0, port=12.0)
cDDdc = cartridge("DC-D", 0.25, 0.20, 3.0, 6.0, 1.0, A=60.0, port=12.0)
rR = cDCdc.evaluate(2400.0, 1.2, fluid=PG25); rD = cDDdc.evaluate(2400.0, 1.2, fluid=PG25)
cal_dc = rR['cal_frac']*rR['dT_out']
print(f"PG25 1.2 L/min/kW: DC-R h_eff {rR['h_eff']/1e3:.0f}, DC-D h_eff {rD['h_eff']/1e3:.0f} kW/m2K; caloric {cal_dc:.1f} K; dP DC-R {rR['dp_total_kPa']:.2f} kPa (no comb)")
def dc_R(h, tim_R, base=2.0e-3):
    L = [(base, K_CU)] + ([(tim_R*1e-4, 1.0)] if tim_R else []) + [(0.30e-3, K_CU), (0.32e-3, F.K_SN), (0.30e-3, K_CU)]
    return F.die_temps(L, h)['Rth_max']
print("| assembly | Rth max K/W | max loss per switch at Tj 150 C, kW | W/cm2 of SiC |")
print("|---|---|---|---|")
for nm, h, tr, b in (("air-era practice: tube plate h 6k + gap pad 0.5", 6e3, 0.5, 3e-3),
                     ("skived plate h 40k + gap pad 0.5", 40e3, 0.5, 2e-3),
                     ("skived plate h 40k + PCM 0.08", 40e3, 0.08, 2e-3),
                     ("pin-fin baseplate (h 22k), solder, as automotive", 22.3e3, None, 3e-3),
                     ("PE-DC-D plate + PCM 0.08", rD['h_eff'], 0.08, 2e-3),
                     ("PE-DS-R direct substrate (sinter), 1.0 mm base", rR['h_eff'], None, 1e-3)):
    if tr is None:
        Rx = F.die_temps(F.module_stack(b, "solder" if "pin-fin" in nm else "sinter"), h)['Rth_max']
    else:
        Rx = dc_R(h, tr, b)
    Pmax = (150-45-cal_dc)/Rx
    print(f"| {nm} | {Rx:.4f} | {Pmax/1e3:.2f} | {Pmax/1.62:.0f} |")
