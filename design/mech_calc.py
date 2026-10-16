#!/usr/bin/env python3
"""DDD-mech calculations: retention force budget, spring-screw design, load-frame checks, clamp and thermal bow,
expansion slip, shock loads, mass budget, PRISM-G envelope. Writes mech_calc.out and mech_calc_data.json.
Axes per cad/prism_cad.py: X along fins, Y along lines, Z up from the die face; origin at the fin-field centre."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = []
def pr(*a): s = " ".join(str(x) for x in a); OUT.append(s); print(s, flush=True)
core = json.load(open(os.path.join(HERE, "params-core.json"))); pln = json.load(open(os.path.join(HERE, "plenum_sep_data.json")))
PSI = 6894.757e-6                      # MPa per psi
E_CU, NU, A_CU = 117e3, 0.34, 17.0e-6  # annealed OFE: E MPa, alpha /K
D = {}
# ======================= 1. RETENTION FORCE BUDGET =======================
pr("## 1. Retention force budget (8 screws)")
cases = [("TTV-A, 4 x 54 x 54 AlN, PCM 25 psi", 25, 4 * 54 * 54), ("TTV-100 hard mode, 4 x 50 x 50, PCM 25 psi", 25, 100 * 100),
         ("lidded 100 cm2 package, PCM/paste 4 psi", 4, 1e4), ("lidded 100 cm2 package, 12 psi", 12, 1e4),
         ("lidded 100 cm2, 60 N kit", None, 1e4), ("lidded 100 cm2, 110 N kit", None, 1e4),
         ("bare-die Rubin 16.6 cm2 die block, 60 N kit", None, 1660), ("bare-die 4-die 33 cm2, 60 N kit", None, 3300)]
D["force_budget"] = []
for name, psi, area in cases:
    F = psi * PSI * area if psi else (480.0 if "60 N" in name else 880.0)
    p = F / area
    pr(f"{name:52s} area {area / 100:6.1f} cm2  F {F:7.0f} N  per screw {F / 8:6.1f} N  p {p:.3f} MPa = {p / PSI:5.1f} psi")
    D["force_budget"].append(dict(case=name, area_cm2=area / 100, F_N=round(F), per_screw_N=round(F / 8, 1), p_MPa=round(p, 3), psi=round(p / PSI, 1)))
F_TTV = 25 * PSI * 4 * 54 * 54; F_TTV100 = 25 * PSI * 1e4
# ======================= 2. EARS CANNOT CARRY THE SPRINGS =======================
pr("\n## 2. Ear bending if a screw loaded the ear directly (1.5 mm annealed Cu tab, hole 3.5 outboard of the body edge)")
b, t, arm = core["ears"]["w"], core["ears"]["z_top"], core["ears"]["hole_offset_from_body_edge"]
for F in (40, 60, 110, 251):
    s = 6 * F * arm / (b * t * t); pr(f"F {F:4d} N: bending stress {s:6.1f} MPa (allowable 40 MPa post-braze OFE) -> {'OK' if s <= 40 else 'FAIL'}")
D["ear_stress_MPa_per_N"] = round(6 * arm / (b * t * t), 4)
# ======================= 3. SPRINGS =======================
pr("\n## 3. Springs")
G_SS = 71700.0   # 302 SS wire, MPa
def coil(d, Dm, Na, F):
    C = Dm / d; Kw = (4 * C - 1) / (4 * C - 4) + 0.615 / C; k = G_SS * d**4 / (8 * Dm**3 * Na)
    tau = Kw * 8 * F * Dm / (math.pi * d**3); x = F / k; Ls = (Na + 2) * d
    return dict(d=d, Dm=Dm, OD=round(Dm + d, 2), Na=Na, k=round(k, 2), x_at_F=round(x, 2), tau_MPa=round(tau), solid=round(Ls, 1), C=round(C, 2))
springs = {"SPR-60": coil(1.30, 6.50, 8.6, 60.0), "SPR-110": coil(1.60, 6.40, 11.0, 110.0)}
L2 = 22.0
for n, s in springs.items():
    s["L2_installed"] = L2; s["L0_free"] = round(L2 + s["x_at_F"], 1); s["F_at_L2"] = round(s["k"] * s["x_at_F"], 1)
    s["uts_1p6_ref"] = 1700; s["tau_over_uts"] = round(s["tau_MPa"] / 1700, 2); s["solid_margin"] = round(L2 - s["solid"], 1)
    s["F_tol_rate10pct_N"] = round(0.10 * s["F_at_L2"], 1); s["F_tol_L0_0p5mm_N"] = round(0.5 * s["k"], 1); s["F_tol_stack_0p3mm_N"] = round(0.3 * s["k"], 1)
    pr(f"{n}: 302 SS d {s['d']} Dm {s['Dm']} (OD {s['OD']}), Na {s['Na']}, C {s['C']}, k {s['k']} N/mm, F {s['F_at_L2']} N at x {s['x_at_F']} (L0 {s['L0_free']} -> L2 {L2}),"
       f" solid {s['solid']} (margin {s['solid_margin']}), tau {s['tau_MPa']} MPa ({s['tau_over_uts']} UTS); F tol: rate +-10% {s['F_tol_rate10pct_N']}, L0 +-0.5 {s['F_tol_L0_0p5mm_N']}, stack +-0.3 {s['F_tol_stack_0p3mm_N']} N")
# TTV die spring ISO 10243 heavy duty 12.5 x 6.3 x 32: rate scaled 1/L from the catalogue 89 mm value (Accu TJH12.5-89: 12.36 N/mm)
k_die = 12.36 * 89 / 32; x_die = F_TTV / 8 / k_die; x100 = F_TTV100 / 8 / k_die
die = dict(std="ISO 10243 heavy duty (red) 12.5 OD x 6.3 bore x 32 L0, Cr-Si rect. wire", k_est=round(k_die, 1), k_basis="12.36 N/mm at L0 89 scaled 89/32; vendor sheet +-10 %",
           F_per_screw_TTV=round(F_TTV / 8, 1), x_TTV=round(x_die, 2), pct_L0_TTV=round(100 * x_die / 32, 1), F_per_screw_TTV100=round(F_TTV100 / 8, 1), x_TTV100=round(x100, 2),
           limit_pct_L0="25 % (2e6 cycles) / 30 % static", L2_TTV=round(32 - x_die, 2), mass_g_est=round(math.pi / 4 * (12.5**2 - 6.3**2) * 32 * 0.45 * 7.85e-3, 1))
springs["DIE-TTV"] = die
pr(f"DIE-TTV: {die['std']}: k ~{die['k_est']} N/mm ({die['k_basis']}); TTV-A {die['F_per_screw_TTV']} N at {die['x_TTV']} mm ({die['pct_L0_TTV']} % L0, limit {die['limit_pct_L0']}); "
   f"TTV-100 {die['F_per_screw_TTV100']} N at {die['x_TTV100']} mm; installed length TTV-A {die['L2_TTV']}")
# ======================= 4. SCREW STACK AND STRESS =======================
pr("\n## 4. Captive shoulder screw CSS-15 (M3 x 0.5 thread, dia 4.00 h8 shoulder) and height stacks")
z_cap = 13.10; frame_T = dict(lands_z=z_cap, body_top=29.10, pocket_floor=19.10, pocket_d=13.2, material="6061-T6 (T1) / 17-4PH H1025 (T2 LM)")
frame_P = dict(lands_z=z_cap, lug_top=15.10, t=2.0, material="301 1/2H stainless, formed")
z_stop_T = -2.15; z_stop_P = -2.30; g_T = 0.15; g_P = 0.40
Ls_T = frame_T["pocket_floor"] + die["L2_TTV"] - z_stop_T; Ls_P = frame_P["lug_top"] + 1.0 + L2 - z_stop_P
pr(f"TTV kit: pocket floor z {frame_T['pocket_floor']} + die spring {die['L2_TTV']} -> head underside z {frame_T['pocket_floor'] + die['L2_TTV']:.2f}; shoulder bottoms at z {z_stop_T} -> shoulder length Ls_T {Ls_T:.2f}")
pr(f"product kit: lug top z {frame_P['lug_top']} + washer 1.0 + coil {L2} -> head underside z {frame_P['lug_top'] + 1.0 + L2:.2f}; shoulder bottoms at z {z_stop_P} -> Ls_P {Ls_P:.2f}")
As = 5.03; T_stop = 0.40; Fp = T_stop * 1e3 / (0.2 * 3.0)   # N.m -> N.mm, K 0.2 (lubricated SS)
for lab, Fs in (("TTV", F_TTV / 8), ("110 N kit", 110.0)):
    Ft = Fp + Fs; pr(f"{lab}: stop torque {T_stop} N.m -> preload {Fp:.0f} N; + spring {Fs:.0f} -> {Ft:.0f} N on As {As} mm2 = {Ft / As:.0f} MPa (A2-70 proof 450: {100 * Ft / As / 450:.0f} %; 17-4PH H900 yield 1170: {100 * Ft / As / 1170:.0f} %)")
I_sh = math.pi * 4.0**4 / 64; Pcr = math.pi**2 * 200e3 * I_sh / Ls_T**2
pr(f"shoulder dia 4.00, L {Ls_T:.1f}: Euler (pinned) {Pcr:.0f} N vs {Fp:.0f} N preload; compressive {Fp / (math.pi * 4):.0f} MPa")
D["screw"] = dict(thread="M3x0.5-6g, 6.0 long", shoulder_d=4.0, shoulder_fit="h8", Ls_TTV=round(Ls_T, 2), Ls_product=round(Ls_P, 2), head="dia 7.0 x 3.0, hex socket 2.5",
                  stop_torque_Nm=T_stop, stop_preload_N=round(Fp), tension_TTV_N=round(Fp + F_TTV / 8), stress_TTV_MPa=round((Fp + F_TTV / 8) / As), euler_N=round(Pcr), z_stop_TTV=z_stop_T, z_stop_product=z_stop_P, ear_gap_TTV=g_T, ear_gap_product=g_P)
# ======================= 5. LOAD FRAME STIFFNESS =======================
pr("\n## 5. Load-frame checks")
Fl = F_TTV / 8; L_span, a = 115.0, 17.5
for lab, E, bw, h in (("LF-15T Al 6061 x-member 20 x 16", 69e3, 20.0, 15.5), ("LF-15T 17-4PH same", 200e3, 20.0, 15.5), ("flat 4 mm plate member 11 wide (rejected)", 200e3, 11.0, 4.0)):
    I = bw * h**3 / 12; dmid = Fl * a * (3 * L_span**2 - 4 * a**2) / (24 * E * I)
    pr(f"{lab}: I {I:.0f} mm4, two {Fl:.0f} N lugs at 17.5 from the supports on a {L_span} span: mid deflection {dmid * 1e3:.0f} um -> lug force change {dmid * k_die:.1f} N")
I_lug = 20 * 15.5**3 / 12; s_lug = Fl * 8 * 7.75 / I_lug
pr(f"lug bending (spring axis 8 mm outboard of the land centre): {s_lug:.1f} MPa (6061-T6 yield 240)")
for lab, F, w, L in (("TTV land 2.5 x 120 (one band)", F_TTV / 2, 2.5, 120), ("product land, 110 N kit", 440.0, 2.5, 120)):
    pr(f"{lab}: bearing on the 1.0 mm cap over separator/end frame {F / (w * L):.2f} MPa (annealed Cu 40)")
# product frame x-member (formed 2.0 mm 301, 12 wide x 10 tall U)
I_u = 2 * (2.0 * 10**3 / 12) + 12 * 2.0 * 5.0**2; d_u = 110 * a * (3 * L_span**2 - 4 * a**2) / (24 * 193e3 * I_u)
pr(f"LF-15P x-member (2.0 mm 301 U 12 x 10): I {I_u:.0f} mm4, mid deflection at 2 x 110 N {d_u * 1e3:.0f} um")
D["frame"] = dict(TTV=frame_T, product=frame_P, lug_stress_MPa=round(s_lug, 1), land_bearing_TTV_MPa=round(F_TTV / 2 / (2.5 * 120), 2))
# ======================= 6. SANDWICH STIFFNESS, CLAMP BOW, THERMAL BOW =======================
pr("\n## 6. Plate sandwich: EI, clamp bow, thermal bow (bending about x, span in y between the +-y bands)")
W = 125.0
# layers: (name, z0, z1, width_eff, T_C)  base face 67 C (PCM benchmark: Tcase 74 - 7.1), fluid mean 51 C
layers = [("base", 0.0, 0.85, 125.0, 65.7), ("fins 50 %", 0.85, 2.80, 54.0, 58.0), ("rim+land ring eq.", 0.85, 2.80, 2 * 6.45, 56.0),
          ("grate 1.70", 2.80, 4.50, 122.6, 51.5), ("plenum flats+walls eq.", 4.50, 10.30, 0.8 * 16 + 15 * 5.714 * 0.8 / 5.8, 51.0),
          ("separator 1.80", 10.30, 12.10, 122.6, 51.0), ("cap top 1.0", 12.10, 13.10, 123.0, 51.0)]
EA = sum(E_CU * (z1 - z0) * w for _, z0, z1, w, _ in layers); zna = sum(E_CU * (z1 - z0) * w * (z0 + z1) / 2 for _, z0, z1, w, _ in layers) / EA
EI = sum(E_CU * (w * (z1 - z0)**3 / 12 + w * (z1 - z0) * ((z0 + z1) / 2 - zna)**2) for _, z0, z1, w, _ in layers)
pr(f"neutral axis z {zna:.2f}; EI {EI:.3e} N.mm2 (full 125 width); per width {EI / W:.3e}; across-fin shear knock-down 0.83 applied to deflections")
res = {}
for lab, F in (("TTV 2.0 kN", F_TTV), ("TTV-100 1.72 kN", F_TTV100), ("product 480 N", 480.0), ("product 880 N", 880.0)):
    Lb = 116.0; q = F / Lb; d2 = 5 * q * Lb**4 / (384 * EI) / 0.83
    Dp = EI / W / (1 - NU**2); d4 = 0.00406 * (F / (116 * 117)) * 116**4 / Dp / 0.83
    res[lab] = (d2 * 1e3, d4 * 1e3); pr(f"{lab}: 2-side bearing (y = +-58) concave bow {d2 * 1e3:5.1f} um; 4-side bearing would give {d4 * 1e3:4.1f} um")
D["clamp_bow_um"] = {k: dict(two_side=round(v[0], 1), four_side=round(v[1], 1)) for k, v in res.items()}
def thermal_bow(scale=1.0, Tref=20.0):
    # laminate: N = sum EA(e0 + k z - a dT) = 0, M = sum EA z (e0 + k z - a dT) + k sum EI_own = 0
    S0 = S1 = S2 = R0 = R1 = 0.0
    for _, z0, z1, w, T in layers:
        A = (z1 - z0) * w; z = (z0 + z1) / 2; dT = Tref + scale * (T - Tref) - Tref; eps = A_CU * (T - Tref) * scale
        S0 += E_CU * A; S1 += E_CU * A * z; S2 += E_CU * (A * z * z + w * (z1 - z0)**3 / 12); R0 += E_CU * A * eps; R1 += E_CU * A * z * eps
    det = S0 * S2 - S1 * S1; kap = (S0 * R1 - S1 * R0) / det
    return kap
kap = abs(thermal_bow()); bow108 = kap * 108**2 / 8   # sign: hot base -> die face convex (centre proud); magnitude reported
pr(f"thermal bow, PCM benchmark (base 65.7 C, grate 51.5, upper stack 51 C): curvature {kap * 1e3:.4f} 1/m, die face convex (centre proud) {bow108 * 1e3:.1f} um over 108 mm, {kap * 54**2 / 8 * 1e3:.1f} um over a 54 mm tile")
kap85 = thermal_bow(scale=(85 - 9 - 20) / (67 - 20) * 1.0 * (67 - 20) / (65.7 - 20) * (65.7 - 20) / (67 - 20)) if False else None
# Tcase 85 C case: base-to-stack difference scales with (Tbase - Tfluid): PCM 14.7 K -> paste at Tcase,max 85 (base face 76) ~ 24 K
kap_hot = kap * (76 - 51) / (65.7 - 51); pr(f"at Tcase 85 C (base face ~76 C, paste): {kap_hot * 108**2 / 8 * 1e3:.1f} um convex over 108 mm")
D["thermal_bow_um"] = dict(benchmark_PCM_108=round(bow108 * 1e3, 1), tile_54=round(kap * 54**2 / 8 * 1e3, 1), Tcase85_108=round(kap_hot * 108**2 / 8 * 1e3, 1), sign="die face convex, corners lift")
net_T = bow108 * 1e3 - res["TTV 2.0 kN"][0]; net_P = bow108 * 1e3 - res["product 480 N"][0]
pr(f"net at the 15 kW TTV point, 2-side bearing: thermal convex {bow108 * 1e3:.1f} - clamp concave {res['TTV 2.0 kN'][0]:.1f} = {net_T:+.1f} um in y (+ convex; x keeps the full thermal bow); product 480 N: {net_P:+.1f} um")
D["net_bow_um"] = dict(TTV_y=round(net_T, 1), product480_y=round(net_P, 1), x_thermal_only=round(bow108 * 1e3, 1))
# ======================= 7. IN-PLANE EXPANSION SLIP =======================
pr("\n## 7. Differential in-plane expansion over 108 mm, 20 -> 85 C (65 K), copper 17.0 ppm/K")
alph = {"AlN tile TTV": 4.5, "Si bare die": 2.6, "Cu-block TTV-100": 17.0, "organic substrate (CoWoS-L eff.)": 12.0, "Cu lid on package": 17.0, "6061 carrier": 23.6, "17-4PH frame": 10.8}
D["expansion"] = {}
for n, a2 in alph.items():
    slip = (A_CU * 1e6 - a2) * 65 * 108e-3; half = slip / 2; strain25 = abs(half) / 25
    pr(f"{n:34s} alpha {a2:5.1f}: free slip {slip:+6.1f} um edge-to-edge, {half:+5.1f} um per side; TIM shear strain at 25 um BLT {strain25:.2f}")
    D["expansion"][n] = dict(alpha_ppm=a2, slip_um=round(slip, 1), half_um=round(half, 1), strain_25um=round(strain25, 2))
# ======================= 8. SHOCK AND VIBRATION LOADS =======================
pr("\n## 8. Shock loads (FRU = plate 1.24 + frame LF-15P 0.085 kg)")
m_fru = 1.325
for g in (0.5, 10, 30, 50):
    Fz = m_fru * 9.81 * g; pr(f"{g:4.1f} g: inertial {Fz:6.0f} N; vs clamp 480 N {'lift-off' if Fz > 480 else 'held'} (60 N kit), vs 880 N {'lift-off' if Fz > 880 else 'held'} (110 N kit); lateral: friction mu 0.2 x 480 = 96 N -> {'slides to the shoulder stops' if Fz > 96 else 'held'}; ear bearing {Fz / 8 / (1.5 * 4):.1f} MPa")
D["shock"] = dict(m_fru_kg=m_fru, F_50g_N=round(m_fru * 9.81 * 50), F_30g_N=round(m_fru * 9.81 * 30), ear_bearing_50g_MPa=round(m_fru * 9.81 * 50 / 8 / 6, 1))
# ======================= 9. MASS BUDGET =======================
pr("\n## 9. Mass budget (g)")
scr = math.pi / 4 * 4.0**2 * Ls_P * 7.9e-3 + 1.0 + 0.3; spr60 = math.pi * 6.5 * 10.6 * math.pi / 4 * 1.3**2 * 7.9e-3; slv = math.pi / 4 * (5.5**2 - 4.1**2) * 21.2 * 7.9e-3   # product lift-off stop sleeve dia 5.5/4.1 (die-spring guide sleeve 6.2/4.1 is TTV only)
bp = 0.8 * (118 * 118 - math.pi / 4 * 60**2) * 7.9e-3; stdoff = 8 * math.pi / 4 * (8.0**2 - 4.2**2) * 7.6 * 7.9e-3
mass = {"core (params-core)": core["mass_kg"] * 1000, "grate GRT-L + GRT-W": 201.0, "plenum PLN-C + 2 PLN-F": pln["mass_g"]["corrugation"] + pln["mass_g"]["frames"], "separator 1.80 Cu": pln["mass_g"]["separator"],
        "cap (allocation to the cap lane, arch 5.1)": 250.0, "stubs 2 x 316L 20 ID x 1.0 x 30": 2 * math.pi * 21 * 1.0 * 30 * 7.95e-3, "guard screen + diffuser": 10.0,
        "8 x CSS-15P screws": 8 * scr, "8 x SPR-60 springs": 8 * spr60, "8 x SLV sleeves + washers + e-clips": 8 * (slv + 0.5 + 0.2), "backplate 0.8 mm 301 118 sq, dia 60 hole": bp, "8 x standoffs STD-8": stdoff}
tot = sum(mass.values())
for k, v in mass.items(): pr(f"{k:48s} {v:7.1f}")
pr(f"{'TOTAL (architecture boundary: plate + stubs + springs + backplate, no load frame)':48s} {tot:7.1f}  (target 1240; SKU limit 1400)")
m_frameP = 85.0; pr(f"with product frame LF-15P {m_frameP:.0f} g: {tot + m_frameP:.0f} g; with 316L 0.6 mm separator (-{pln['mass_g']['separator'] - 68:.0f} g): {tot - (pln['mass_g']['separator'] - 68):.0f} g")
D["mass_g"] = {k: round(v, 1) for k, v in mass.items()}; D["mass_g"]["total_no_frame"] = round(tot, 1); D["mass_g"]["frame_LF15P"] = m_frameP; D["mass_g"]["total_with_frame"] = round(tot + m_frameP, 1)
# ======================= 10. PRISM-G ENVELOPE =======================
pr("\n## 10. PRISM-G envelope (field 110 x 120, lines along y)")
fx, fy = 110.0, 120.0; body = (fx + 17.0, fy + 17.0); sc = body[0] * body[1] / (125 * 125)
mG = dict(core=core["mass_kg"] * 1000 * sc, grate=201 * sc, plenum=(pln["mass_g"]["corrugation"] + pln["mass_g"]["frames"]) * sc, separator=pln["mass_g"]["separator"] * sc, cap=250 * sc * 0.85)
pr(f"body {body[0]} x {body[1]}; outline scale {sc:.3f}; plate-only mass Cu {sum(mG.values()):.0f} g; with 316L separator {sum(mG.values()) - mG['separator'] + 68 * sc:.0f} g (limit 900)")
D["prism_g"] = dict(body=body, mass_plate_cu_g=round(sum(mG.values())), mass_316L_sep_g=round(sum(mG.values()) - mG["separator"] + 68 * sc), ears=[[-40, -72], [40, -72], [-40, 72], [40, 72], [-68, -45], [-68, 45], [68, -45], [68, 45]],
                    height_at_bar=19.1, ports="2 x dia 10 horizontal 316L stubs, +y end, axis z 12.0, OD 12", frame_lands="y = +-(62.5..65.5) over the end frames")
json.dump(D, open(os.path.join(HERE, "mech_calc_data.json"), "w"), indent=1); open(os.path.join(HERE, "mech_calc.out"), "w").write("\n".join(OUT) + "\n")
