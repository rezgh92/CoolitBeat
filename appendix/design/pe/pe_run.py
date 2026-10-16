#!/usr/bin/env python3
"""Part B: power-electronics quantification for the HMMC-PE family.
- h_eff and dP of candidate cartridge cores from the project scoping model (coldplate_model.py, imported
  unmodified) with WEG 50/50, PAO and PG25 property sets;
- per-switch Rth(j-f) from the multilayer Fourier spreading model (pe_fourier.py), pin-fin baseline calibrated
  to Infineon FS01MR12A8MA2B (HybridPACK Drive G2 CoolSiC, Rth(j-f) 0.103 K/W typ, 10 L/min 50/50 WEG, 60 C);
- module-level Tj, die-to-die spread, current headroom and SiC-area saving; cold-start and dielectric checks;
- data-centre (PG25) power-module and discrete cases.
"""
import sys, math
from dataclasses import replace
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
from coldplate_model import ColdPlate, Fluid, PG25, WATER50, K_CU, K_AL
import pe_fourier as F

WEG65 = Fluid("WEG 50/50 @ 65C", 1045.0, 3550.0, 1.40e-3, 0.405)
WEG25 = Fluid("WEG 50/50 @ 25C", 1070.0, 3300.0, 3.6e-3, 0.38)
WEGm40 = Fluid("WEG 50/50 @ -40C", 1095.0, 3050.0, 80e-3, 0.35)
PAO65 = Fluid("PAO-2 @ 65C", 775.0, 2300.0, 2.4e-3, 0.14)

A_MOD = 84.0        # cm2 wetted footprint of a HybridPACK-Drive-class six-pack (assumed 120 x 70 mm)
FLOW = 10.0         # L/min, automotive datasheet reference
N_SW, P_SW = 6, 1000.0   # six switches at 1 kW each (peak) -> 6 kW module loss

def cartridge(name, gap, fin, H, L, base, k=K_CU, A=A_MOD, slot_w=4.0, port=14.0, orifice_kPa=0.0, hdr_u=0.5):
    side = math.sqrt(A)*10
    n_slots = max(1, int(round(side/(2*L))))
    return ColdPlate(name=name, footprint_cm2=A, fin_t_mm=fin, gap_mm=gap, fin_h_mm=H, flow_len_mm=L, base_mm=base,
                     k_solid=k, tim="direct-to-die", isothermal_cell=True, hotspot_flow_K=0.0,
                     n_parallel_paths=2*n_slots, slot_w_mm=slot_w, K_channel=3.0, K_slot=1.5,
                     header_u_m_s=hdr_u, K_header=1.0, port_bore_mm=port, K_port=2.3, orifice_dp_kPa_18=orifice_kPa)

def ev(cp, fluid, flow=FLOW, Q=N_SW*P_SW):
    return cp.evaluate(Q, flow/(Q/1000.0), fluid=fluid, T_in=65.0)

print("# HMMC-PE power-electronics quantification\n")
print("## B1. Candidate cartridge cores, 84 cm2 module footprint, 10 L/min, 6 kW (scoping model)\n")
print("| core | gap/fin/H mm | L mm | fluid | u_ch m/s | Re | h kW/m2K | eta | h_eff kW/m2K | NTU | cal frac | dP ch | dP K+slot | dP hdr | dP orif | dP port | dP total kPa |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
cores = {
    "A-coarse 0.50/0.40x4 Cu": cartridge("A-coarse", 0.50, 0.40, 4.0, 5.0, 1.5),
    "A 0.40/0.30x3 Cu": cartridge("A", 0.40, 0.30, 3.0, 5.0, 1.5),
    "A-fine 0.30/0.25x2.5 Cu": cartridge("A-fine", 0.30, 0.25, 2.5, 4.0, 1.5),
    "DC-R 0.15/0.10x2 Cu (PG25 core)": cartridge("DC-R", 0.15, 0.10, 2.0, 4.0, 1.0),
    "Al 0.50/0.50x4 (skived 6063)": cartridge("Al", 0.50, 0.50, 4.0, 5.0, 2.0, k=K_AL),
}
H_EFF = {}
for nm, cp in cores.items():
    for fl in (WEG65,):
        r = ev(cp, fl)
        H_EFF[nm] = r
        print(f"| {nm} | {cp.gap_mm}/{cp.fin_t_mm}x{cp.fin_h_mm} | {cp.flow_len_mm} | {fl.name} | {r['u_ch']:.3f} | {r['Re']:.0f} | {r['h']/1e3:.1f} | {r['eta']:.2f} | "
              f"{r['h_eff']/1e3:.0f} | {r['NTU']:.2f} | {r['cal_frac']:.2f} | {r['dp_ch_kPa']:.2f} | {r['dp_K_kPa']+r['dp_slot_kPa']:.2f} | {r['dp_header_kPa']:.2f} | {r['dp_orif_kPa']:.2f} | {r['dp_port_kPa']:.2f} | {r['dp_total_kPa']:.2f} |")

# Branch/header uniformity check for core A: branch dP (channel+turn+slot+orifice) vs header dynamic head
rA = H_EFF["A 0.40/0.30x3 Cu"]
head = 0.5*WEG65.rho*0.5**2
branch = (rA['dp_ch_kPa']+rA['dp_K_kPa']+rA['dp_slot_kPa'])*1e3
print(f"\nCore A uniformity: branch {branch:.0f} Pa vs header head {head:.0f} Pa at 0.5 m/s -> ratio {branch/head:.1f} (rule >= 6; add comb if < 6)")
cpA_comb = replace(cores["A 0.40/0.30x3 Cu"], orifice_dp_kPa_18=0.0)

# ---------------------------------------------------------------- B2 calibration
print("\n## B2. Pin-fin baseline calibration (per switch, 8 x 4.5 mm SiC dies = 1.62 cm2 on a 14 cm2 cell)\n")
target = 0.100   # 0.103 K/W datasheet minus ~0.003 K/W caloric allowance (single-switch characterisation)
L_pf = F.module_stack(3.0e-3, "solder")
h_pf, r_pf = F.calibrate_h(target, L_pf)
print(f"Calibrated pin-fin h_eff (base-referenced) = {h_pf/1e3:.1f} kW/m2K -> Rth mean {r_pf['Rth_mean']:.4f}, max {r_pf['Rth_max']:.4f} K/W; "
      f"die-referenced R'' = {r_pf['Rth_mean']*r_pf['A_die_cm2']:.3f} cm2K/W")
# Zukauskas cross-check
d, ST, SL, Hp = 2.0e-3, 3.0e-3, 2.6e-3, 8.0e-3
u_f = FLOW/60000/(0.12*Hp); u_max = u_f*ST/(ST-d)
Re_d = WEG65.rho*u_max*d/WEG65.mu; Pr = WEG65.Pr
Nu = 0.35*(ST/SL)**0.2*Re_d**0.6*Pr**0.36
hp = Nu*WEG65.k/d; mfin = math.sqrt(4*hp/(K_CU*d)); eta = math.tanh(mfin*Hp)/(mfin*Hp)
dens = 1/(ST*SL); Alat = math.pi*d*Hp*dens; Abase = 1-dens*math.pi*(d/2)**2
heff_z = hp*(eta*Alat+Abase)
print(f"Zukauskas cross-check (2 mm pins, 3.0 x 2.6 mm staggered, 8 mm tall, 120 mm frontal width, no bypass): Re_d {Re_d:.0f}, h {hp/1e3:.1f}, eta {eta:.2f}, "
      f"h_eff {heff_z/1e3:.0f} kW/m2K; with 30-50 % tip bypass ~{0.5*heff_z/1e3:.0f}-{0.7*heff_z/1e3:.0f} kW/m2K -> calibration is plausible")
for t_b in (2.0e-3, 4.0e-3):
    hh, rr = F.calibrate_h(target, F.module_stack(t_b, "solder"))
    print(f"  sensitivity: pin-fin base {t_b*1e3:.0f} mm -> calibrated h_eff {hh/1e3:.1f} kW/m2K")

# ---------------------------------------------------------------- B3 variants
print("\n## B3. Per-switch Rth(j-f) to LOCAL fluid, 10 L/min WEG 65 C (Fourier spreading model)\n")
print("| variant | stack | h_eff kW/m2K | Rth mean K/W | Rth max K/W | die-ref R'' cm2K/W | vs pin-fin |")
print("|---|---|---|---|---|---|---|")
hA = H_EFF["A 0.40/0.30x3 Cu"]['h_eff']; hAc = H_EFF["A-coarse 0.50/0.40x4 Cu"]['h_eff']; hAf = H_EFF["A-fine 0.30/0.25x2.5 Cu"]['h_eff']
hDC = H_EFF["DC-R 0.15/0.10x2 Cu (PG25 core)"]['h_eff']; hAl = H_EFF["Al 0.50/0.50x4 (skived 6063)"]['h_eff']
variants = [
    ("Pin-fin baseline (HPD G2 class)", "3.0 mm Cu base, SnAg 0.10", h_pf, F.module_stack(3.0e-3, "solder")),
    ("ShowerPower-class flat base (KB-L band, h 12)", "3.0 mm Cu base, solder", 12e3, F.module_stack(3.0e-3, "solder")),
    ("ShowerPower-3D-class (KB-L band, h 30)", "3.0 mm Cu base, solder", 30e3, F.module_stack(3.0e-3, "solder")),
    ("PE-A1 drop-in cartridge, core A", "1.5 mm Cu base, solder", hA, F.module_stack(1.5e-3, "solder")),
    ("PE-A1 coarse core (0.5 mm gaps)", "1.5 mm Cu base, solder", hAc, F.module_stack(1.5e-3, "solder")),
    ("PE-A2 cartridge, sintered", "1.5 mm Cu base, Ag sinter", hA, F.module_stack(1.5e-3, "sinter")),
    ("PE-DS direct-substrate (fins on 1.0 mm base sintered to AMB)", "1.0 mm Cu base, Ag sinter", hA, F.module_stack(1.0e-3, "sinter")),
    ("PE-DS fine core (filtered loop)", "1.0 mm, sinter", hAf, F.module_stack(1.0e-3, "sinter")),
    ("PE-DS with DC-R core (PG25-class filtration)", "1.0 mm, sinter", hDC, F.module_stack(1.0e-3, "sinter")),
    ("PE-Al cartridge (Al 6063 core, DBA-class)", "2.0 mm Al base, sinter", hAl, F.module_stack(2.0e-3, "sinter", base_k=K_AL)),
]
RES = {}
base_R = None
for nm, st, h, L in variants:
    r = F.die_temps(L, h)
    if base_R is None:
        base_R = r['Rth_mean']
    RES[nm] = (h, L, r)
    print(f"| {nm} | {st} | {h/1e3:.0f} | {r['Rth_mean']:.4f} | {r['Rth_max']:.4f} | {r['Rth_mean']*r['A_die_cm2']:.3f} | {100*(r['Rth_mean']/base_R-1):+.0f} % |")

# Double-sided (approximate parallel combination of bottom path and top path through a 1 mm Cu spacer)
R_spacer = 0.04e-3/F.K_AG + 1.0e-3/F.K_CU + 0.04e-3/F.K_AG
for nm, h, Lb in (("PE-DSC double-sided, core A both sides", hA, F.module_stack(1.0e-3, "sinter")),
                  ("PE-DSC double-sided, DC-R core both sides", hDC, F.module_stack(1.0e-3, "sinter")),
                  ("DSC with pin-fin-class h on both sides (today's DSC reference)", h_pf, F.module_stack(3.0e-3, "solder"))):
    rb = F.die_temps(Lb, h); rt = F.die_temps(Lb, h, extra_R_die=R_spacer - 0.0)
    # top path: die top -> spacer (1-D) -> AMB -> attach -> base -> h (R_DIE counted once: subtract it from top path)
    Rt = rt['Rth_mean'] - F.R_DIE/ (rt['A_die_cm2']*1e-4)
    Rb = rb['Rth_mean']
    Rd = 1/(1/Rb + 1/Rt) + 0.0
    RES[nm] = (h, Lb, dict(Rth_mean=Rd, Rth_max=Rd*rb['Rth_max']/rb['Rth_mean'], A_die_cm2=rb['A_die_cm2']))
    print(f"| {nm} | 2 x (1.0 mm base, sinter) + 1 mm Cu spacer | {h/1e3:.0f} | {Rd:.4f} | {Rd*rb['Rth_max']/rb['Rth_mean']:.4f} | {Rd*rb['A_die_cm2']:.3f} | {100*(Rd/base_R-1):+.0f} % |")
print("\nPublished anchors: Infineon FS01MR12A8MA2B 0.103 typ / 0.113 max K/W per switch (10 L/min, 60 C); NREL WEG jet impingement ~0.15 cm2K/W "
      "(die-ref.); EPFL manifold-microchannel SiC module 9.85 mm2K/W = 0.099 cm2K/W (water, 2.16 L/min, lab).")

# Base-thickness optimum for core A with sinter
print("\nBase thickness sweep (core A h_eff, sinter attach): " + ", ".join(
    f"{tb:.1f} mm {F.die_temps(F.module_stack(tb*1e-3, 'sinter'), hA)['Rth_mean']:.4f}" for tb in (0.5, 0.8, 1.0, 1.5, 2.0, 3.0)))
print("Base thickness sweep (pin-fin h_eff, solder): " + ", ".join(
    f"{tb:.1f} mm {F.die_temps(F.module_stack(tb*1e-3, 'solder'), h_pf)['Rth_mean']:.4f}" for tb in (1.0, 2.0, 3.0, 4.0, 5.0)))

# Die-area sensitivity of the relative gain
print("\nDie-area sensitivity (recalibrate pin-fin h each time; relative gain of PE-DS core A):")
for ds in (0.75, 1.0, 1.25):
    hh, rr = F.calibrate_h(target, F.module_stack(3.0e-3, "solder"), die_scale=ds)
    rd = F.die_temps(F.module_stack(1.0e-3, "sinter"), hA, die_scale=ds)
    print(f"  SiC {1.62*ds:.2f} cm2/switch: pin-fin h {hh/1e3:.1f} kW/m2K; PE-DS Rth {rd['Rth_mean']:.4f} -> {100*(rd['Rth_mean']/rr['Rth_mean']-1):+.0f} %")

# ---------------------------------------------------------------- B4 module level
print("\n## B4. Module level, 6 x 1 kW, 10 L/min WEG 65 C inlet: hottest-switch Tj, spread, headroom\n")
mdot = FLOW/60000*WEG65.rho; dTout = N_SW*P_SW/(mdot*WEG65.cp)
print(f"Coolant outlet rise {dTout:.1f} K")
print("| variant | flow routing | caloric at hottest switch K | Tj,max C | die-to-die / switch-to-switch spread K | +current at equal Tj,max | SiC area at equal Tj,max |")
print("|---|---|---|---|---|---|---|")
calA = H_EFF["A 0.40/0.30x3 Cu"]['cal_frac']
def tj(nm, cal_hot, cal_cold, label):
    h, L, r = RES[nm]
    Tmax = 65 + cal_hot + P_SW*r['Rth_max']
    spread = (cal_hot - cal_cold) + P_SW*(r['Rth_max'] - r['Rth_mean'])*2
    return Tmax, spread
rows = [("Pin-fin baseline (HPD G2 class)", 5/6*dTout, 1/6*dTout, "series along 3 phases"),
        ("Pin-fin baseline (HPD G2 class)", 0.5*dTout, 0.5*dTout, "transverse (parallel phases)"),
        ("PE-A1 drop-in cartridge, core A", calA*dTout, calA*dTout, "manifold, every cell fresh"),
        ("PE-A2 cartridge, sintered", calA*dTout, calA*dTout, "manifold"),
        ("PE-DS direct-substrate (fins on 1.0 mm base sintered to AMB)", calA*dTout, calA*dTout, "manifold"),
        ("PE-DSC double-sided, core A both sides", calA*dTout, calA*dTout, "manifold, 2 sides in parallel"),
        ("PE-Al cartridge (Al 6063 core, DBA-class)", H_EFF["Al 0.50/0.50x4 (skived 6063)"]['cal_frac']*dTout, H_EFF["Al 0.50/0.50x4 (skived 6063)"]['cal_frac']*dTout, "manifold")]
T_ref = 65 + 5/6*dTout + P_SW*RES["Pin-fin baseline (HPD G2 class)"][2]['Rth_max']
dT_ref = T_ref - 65 - 5/6*dTout   # die-rise budget of the reference hottest switch
for nm, ch, cc, lab in rows:
    h, L, r = RES[nm]
    Tmax = 65 + ch + P_SW*r['Rth_max']
    spread = (ch - cc) + P_SW*(r['Rth_max'] - r['Rth_mean'])
    # current headroom at equal Tj,max (caloric scales with P too: solve P*(Rmax + cal_frac/(mdot cp)*N) = T_ref-65)
    calc_per_W = ch/P_SW
    P_eq = (T_ref - 65)/(r['Rth_max'] + calc_per_W)
    I_gain = math.sqrt(P_eq/P_SW) - 1
    # SiC area at equal Tj,max: P ~ 1/s (conduction, constant current), Rth(s) from spreading model
    lo, hi = 0.3, 1.5
    for _ in range(40):
        s = 0.5*(lo+hi)
        if nm.startswith("PE-DSC"):
            rb = F.die_temps(L, h, die_scale=s); rt = F.die_temps(L, h, die_scale=s, extra_R_die=R_spacer)
            Rt = rt['Rth_mean'] - F.R_DIE/(rt['A_die_cm2']*1e-4); Rm = 1/(1/rb['Rth_mean']+1/Rt)*rb['Rth_max']/rb['Rth_mean']
        else:
            Rm = F.die_temps(L, h, die_scale=s)['Rth_max']
        T = 65 + ch/s + P_SW/s*Rm
        lo, hi = (s, hi) if T > T_ref else (lo, s)
    print(f"| {nm} | {lab} | {ch:.1f} | {Tmax:.1f} | {spread:.1f} | {100*I_gain:+.0f} % | {100*(s-1):+.0f} % |")

# ---------------------------------------------------------------- B5 hydraulics incl. cold start
print("\n## B5. Hydraulics: dP at 10 L/min (model; inertial terms not Re-corrected at -40 C, see note)\n")
print("| core | 65 C | 25 C | -40 C (10 L/min) | -40 C (5 L/min) |")
print("|---|---|---|---|---|")
for nm in ("A 0.40/0.30x3 Cu", "A-coarse 0.50/0.40x4 Cu", "A-fine 0.30/0.25x2.5 Cu"):
    cp = cores[nm]
    vals = [ev(cp, WEG65)['dp_total_kPa'], ev(cp, WEG25)['dp_total_kPa'], ev(cp, WEGm40)['dp_total_kPa'], ev(cp, WEGm40, flow=5.0)['dp_total_kPa']]
    print(f"| {nm} | " + " | ".join(f"{v:.1f}" for v in vals) + " |")
# pin-fin scaling: 7.6 kPa at 65 C incl. reference cooler; pins ~1.3 kPa with Eu = 0.35 + 50/Re
def pin_dp(fl, flow):
    u = flow/60000/(0.12*Hp)*ST/(ST-d); Re = fl.rho*u*d/fl.mu; Eu = 0.35 + 50/Re
    return 23*Eu*0.5*fl.rho*u**2/1e3, Re
p65, re65 = pin_dp(WEG65, 10); p25, _ = pin_dp(WEG25, 10); pm40, rem40 = pin_dp(WEGm40, 10); pm40h, _ = pin_dp(WEGm40, 5)
housing65 = 7.6 - p65
print(f"| pin-fin field only (Eu = 0.35 + 50/Re, 23 rows) | {p65:.1f} (Re {re65:.0f}) | {p25:.1f} | {pm40:.1f} (Re {rem40:.0f}) | {pm40h:.1f} |")
print(f"| pin-fin module + reference cooler (datasheet 7.6 kPa at 65 C; housing {housing65:.1f} kPa held inertial) | 7.6 | {housing65+p25:.1f} | {housing65+pm40:.1f} (x2-3 housing if laminar) | {housing65/4+pm40h:.1f} |")

# ---------------------------------------------------------------- B6 dielectric
print("\n## B6. Dielectric (PAO-2, 65 C) vs WEG 50/50 in core A (10 L/min and at equal caloric rise)\n")
for fl, flow in ((WEG65, 10.0), (PAO65, 10.0), (PAO65, 10.0*WEG65.rho*WEG65.cp/(PAO65.rho*PAO65.cp))):
    r = ev(cores["A 0.40/0.30x3 Cu"], fl, flow=flow)
    rr = F.die_temps(F.module_stack(1.0e-3, "sinter"), r['h_eff'])
    print(f"- {fl.name} at {flow:.1f} L/min: h_eff {r['h_eff']/1e3:.0f} kW/m2K, Rth(j-f) PE-DS {rr['Rth_mean']:.4f} K/W, dT_out {r['dT_out']:.1f} K, dP {r['dp_total_kPa']:.1f} kPa")
# pin-fin in PAO (Zukauskas ratio)
ratio = (PAO65.k/WEG65.k)*((PAO65.Pr/WEG65.Pr)**0.36)*(((PAO65.rho/PAO65.mu)/(WEG65.rho/WEG65.mu))**0.6)
rp = F.die_temps(F.module_stack(3.0e-3, "solder"), h_pf*ratio)
print(f"- pin-fin in PAO at 10 L/min: h ratio {ratio:.2f} -> h_eff {h_pf*ratio/1e3:.1f} kW/m2K, Rth {rp['Rth_mean']:.4f} K/W")

# ---------------------------------------------------------------- B7 data-centre power (PG25, 45 C)
print("\n## B7. Data-centre 800 VDC power stage on a PG25 plate (45 C inlet): plate vs TIM\n")
# baseplate-less SiC module (Si3N4 AMB) through a TIM onto the plate base
def dc_case(h, tim_R, base=2.0e-3, P=400.0):
    L = [(base, K_CU), (tim_R*1e-4*1.0, 1.0)] + [(0.30e-3, K_CU), (0.32e-3, F.K_SN), (0.30e-3, K_CU)]
    return F.die_temps(L, h, P_switch=P)
dcR = cartridge("DC-R", 0.15, 0.10, 2.0, 4.0, 1.0, A=60.0, port=12.0)
dcD = cartridge("DC-D", 0.25, 0.20, 3.0, 6.0, 1.0, A=60.0, port=12.0)
rR = dcR.evaluate(2400.0, 1.2, fluid=PG25); rD = dcD.evaluate(2400.0, 1.2, fluid=PG25)
print(f"PE-DC cores at 2.4 kW / 2.9 L/min PG25 over 60 cm2: DC-R h_eff {rR['h_eff']/1e3:.0f} kW/m2K dP {rR['dp_total_kPa']:.2f} kPa; "
      f"DC-D (0.25/0.20x3, 6 mm) h_eff {rD['h_eff']/1e3:.0f} kW/m2K dP {rD['dp_total_kPa']:.2f} kPa")
print("| plate (h_eff) | TIM | R'' TIM cm2K/W | Tj - T_in per 400 W switch K (local) |")
print("|---|---|---|---|")
for pl, h in (("tube-in-plate / machined channel (6 kW/m2K)", 6e3), ("skived split-flow plate (40)", 40e3), ("PE-DC-D derated core", rD['h_eff']), ("PE-DC-R core", rR['h_eff'])):
    for tn, tr in (("gap pad", 0.50), ("grease", 0.15), ("PCM", 0.08), ("Ag sinter (direct substrate)", 0.003)):
        r = dc_case(h, tr)
        print(f"| {pl} | {tn} | {tr} | {r['T_mean']:.1f} |")
