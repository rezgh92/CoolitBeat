#!/usr/bin/env python3
"""cap_stress.py - PRISM-15 Rev A drawn cap (lane cap): geometry, draw feasibility, pressure stresses,
seam and boss joints, guard hydraulics, mass. Writes cap_stress.out and cap_stress_data.json.
Convention: X along the fins, Y along the lines, Z up from the die face (mm, MPa, N)."""
import json, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent
P_PROOF, P_BURST, P_MAWP = 1.55, 3.10, 1.03      # MPa (architecture 5.2)
SY, E = 40.0, 117e3                               # post-braze annealed OFE allowable, modulus
RHO_CU, RHO_SS, RHO_PG = 8.94e-3, 7.95e-3, 1005.0  # g/mm3, g/mm3, kg/m3 (PG25 45 C)
Q18 = 18.0 / 60000.0                              # m3/s at 18 LPM
out, D = [], {}
def log(s=""): out.append(s); print(s)

# ---------------- 1. geometry of record (this lane) ----------------
t = 1.0                        # sheet
lid_z0, lid_z1 = 12.10, 13.10
h_i = 7.7                      # arch / dome internal height -> crown external z = lid_z1 + h_i + t = 20.8
w_i, r_i = 10.0, 3.5           # arch internal width (y) and internal crown corner radius
pitch = 14.0
inlet_y, outlet_y = [-21.0, -7.0], [7.0, 21.0, 35.0, 49.0]
x_in_ext, x_out_ext = 51.0, 57.0          # arch external half-lengths (mech: <= 52 / <= 58.8)
dome_in = dict(cx=0.0, cy=-20.0, xi=35.0, yi=35.0)      # internal plan; y -37.5..-2.5
dome_out = dict(cx=0.0, cy=21.0, xi=35.0, yi=38.0)      # internal plan; y 2..40 (arches 1-3), spine to arch 4
spine = dict(w_i=10.0, y0=40.0, y1=54.0)
boss = dict(od=26.0, bore=20.0, pocket_d=26.10, pocket_depth=1.0, z0=19.8, z1=29.5)
skirt = dict(inner=121.50, outer=123.40, foot_z=1.5, lap_top_z=2.8, rim_outer=121.40)
crown_z = lid_z0 + h_i + t   # cavity rises from the separator top (lid_z0)
D["crown_z"] = crown_z
log(f"1. Stack: lid {lid_z0}-{lid_z1}, arch internal {w_i} x {h_i} r{r_i}, crown external z {crown_z:.2f} "
    f"(architecture 20.8 recovered with the 1.8 separator by h_i 7.7 instead of 8.0)")
A_arch = w_i * h_i - 2 * (1 - math.pi / 4) * r_i ** 2
A_in, A_out = 2 * A_arch, 4 * A_arch
u_in, u_out = Q18 / 2 / (A_in * 1e-6), Q18 / 2 / (A_out * 1e-6)
log(f"   arch area {A_arch:.1f} mm2 (architecture 80.5); header per half: inlet {A_in:.0f} (161) -> {u_in:.2f} m/s, "
    f"outlet {A_out:.0f} (322) -> {u_out:.2f} m/s; at 22.5 LPM inlet {u_in*22.5/18:.2f} m/s (cap 1.5)")
dp_header = 0.5 * RHO_PG * (u_in ** 2 - 0.93 ** 2) * 1.0 / 1000  # K~1 on the changed inlet velocity head
D.update(A_arch=A_arch, u_in=u_in, u_out=u_out, dp_header_delta_kpa=dp_header)
log(f"   header dP change vs architecture (K 1.0 on the inlet velocity head): +{dp_header:.2f} kPa")
# valley between arches: external land, fluid-side land, effective braze land
r_v = 0.5                                  # outer valley radius (0.5 t, re-struck)
land_ext = pitch - (w_i + 2 * t)
flat_fluid = pitch - w_i - 2 * t - 2 * r_v
wet_half = math.sqrt(2 * (r_v + t) * 0.10)  # arc where the gap to the separator is <= 0.10 (braze-fillable)
land_eff = flat_fluid + 2 * wet_half
D.update(valley_land_ext=land_ext, valley_flat_fluid=flat_fluid, valley_land_eff=land_eff)
log(f"   valley: external land {land_ext:.1f}, fluid-side flat {flat_fluid:.1f}, effective braze land {land_eff:.2f} mm")
# window margin: separator windows requested 5.0 x 8.0 (IR-C1), plenum top-flat windows stay 5 x 10
win_len = 8.0
margin = (w_i - win_len) / 2
stack = 0.05 + 0.15 + 0.05       # sep position, cap arch position (die), window size
log(f"   window margin {margin:.2f} each side vs position stack {stack:.2f}: min clear {margin-stack:.2f} (>= 0.5 wanted)")
D.update(window_margin=margin, window_min_clear=margin - stack)

# ---------------- 2. pressure stresses (closed forms, clamped strips/plates) ----------------
def strip_clamped(p, L, t=1.0): return p * L ** 2 / (2 * t ** 2)      # 6M/t^2 with M = pL^2/12
def report(name, s_burst):
    sf = SY / (s_burst / 2)   # SF at proof against yield (proof = burst/2)
    log(f"   {name:60s} {s_burst:6.1f} MPa at 3.1  |  SF at proof {sf:4.2f}  {'ok' if s_burst <= SY else 'FLAG'}")
    return dict(s_burst=round(s_burst, 1), sf_proof=round(sf, 2))
log("2. Stresses at design burst 3.1 MPa (allowable 40 = SF 2 on yield at proof 1.55)")
S = {}
straight_wall = h_i - r_i
S["arch_top_flat"] = report(f"arch top flat {w_i-2*r_i:.1f} span", strip_clamped(P_BURST, w_i - 2 * r_i))
S["arch_wall"] = report(f"arch side wall {straight_wall:.1f} straight", strip_clamped(P_BURST, straight_wall))
S["arch_crown_hoop"] = report(f"arch crown corner hoop r_i {r_i} (pr/t)", P_BURST * r_i / t)
S["arch_end_hoop_thinned"] = report("arch end dome r_i 5 at 0.70 wall (30 % draw thinning)", P_BURST * 5.0 / 0.70)
S["dome_wall"] = report("dome side wall (same section)", strip_clamped(P_BURST, straight_wall))
S["dome_plan_corner"] = report("dome plan-corner cylinder r_i 6 hoop", P_BURST * 6.0 / t)
# dome top: flat 28 x 31 with the stiff boss ring; ligaments carry the ring load as clamped strips
F_ring = P_BURST * math.pi / 4 * boss["od"] ** 2
lig = (dome_out["yi"] + 2 * t - 2 * (r_i + t) - boss["od"]) / 2      # 2.5 on the outlet dome (y)
line = F_ring / (math.pi * boss["od"])
S["dome_ligament_bend"] = report(f"dome top ligament {lig:.1f} carrying the boss ring (line load {line:.1f} N/mm)",
                                 6 * (line * lig / 8) / t ** 2)
S["dome_ligament_shear"] = report("dome top shear at the boss ring", F_ring / (math.pi * boss["od"] * t))
# dome walls carry the whole dome top load down to the separator except at the arch openings
for key, dm, n_open in (("in", dome_in, 4), ("out", dome_out, 6)):
    per_full = 2 * (dm["xi"] + dm["yi"]); per = per_full - n_open * w_i
    F = P_BURST * dm["xi"] * dm["yi"]
    S[f"dome_{key}_wall_tension"] = report(f"dome {key} wall membrane, dome foot only ({per:.0f} mm, no arch-wall share)", F / (per * t))
    S[f"dome_{key}_wall_tension_T"] = report(f"dome {key} wall membrane with the arch walls as T-stiffeners ({per_full:.0f} mm)", F / (per_full * t))
# skirt wall as a secondary boundary if the stack-edge cavity is wetted (two internal joints must both fail)
S["skirt_wall_MAWP"] = report("skirt wall 9.3 free span if cavity wetted, at MAWP (secondary)", strip_clamped(P_MAWP, lid_z0 - 2.8))
# arch walls as beams where the inter-arch valley is unbrazed (spine crossing 12 mm)
L_int, w_up = spine["w_i"] + 2 * t, P_BURST * w_i
I_wall = t * h_i ** 3 / 12
S["valley_interrupt_beam"] = report(f"arch walls as beams over the {L_int:.0f} mm spine crossing",
                                    (w_up * L_int ** 2 / 12) * (h_i / 2) / I_wall)
D["stress"] = S
log("   dome walls: bound by the two cases above; E1 FEA decides (O-C1)")
log("   tie ribs: none needed; every flat panel is <= 3.0 mm span or carried by the brazed boss ring (E1 FEA on the domes)")

# ---------------- 3. seams and joints ----------------
log("3. External seams")
gap_nom = (skirt["inner"] - skirt["rim_outer"]) / 2
gap_min = (skirt["inner"] - 0.05 - skirt["rim_outer"] - 0.05) / 2
gap_max = (skirt["inner"] + 0.05 - skirt["rim_outer"] + 0.05) / 2
lap_h = skirt["lap_top_z"] - skirt["foot_z"]
per = 4 * skirt["rim_outer"] - (8 - 2 * math.pi) * 2.0
A_lap = per * lap_h
F_lap = P_BURST * per * ((skirt["inner"] - 120.71) / 2)   # lid strip outboard of the plenum flange tie
tau_lap = F_lap / A_lap
log(f"   lap: radial gap {gap_nom:.3f} nominal ({gap_min:.3f}-{gap_max:.3f} with +-0.05 on both faces); lap {lap_h:.1f} tall, "
    f"{A_lap:.0f} mm2; shear {tau_lap:.2f} MPa at 3.1 (BAg-8 shear >= 150: SF {150/tau_lap:.0f})")
A_fill = per * (gap_nom * lap_h + 0.045 + 0.08)       # gap + inner chamfer fillet + outer 0.4 fillet
ring_len = 4 * skirt["outer"] + 2 * (2 * 1.4)
v_ring = math.pi / 4 * 0.5 ** 2 * ring_len
log(f"   BAg-8 ring 0.5 wire x {ring_len:.0f} mm = {v_ring:.0f} mm3 ({v_ring*10.0/1000:.2f} g) vs need {A_fill:.0f} mm3")
A_face = math.pi / 4 * (boss["od"] ** 2 - boss["bore"] ** 2)
F_boss = P_BURST * math.pi / 4 * boss["bore"] ** 2 + 200.0     # pressure on the bore + 200 N hose side load
log(f"   boss joint: face {A_face:.0f} mm2 + pocket wall {math.pi*boss['od']*boss['pocket_depth']:.0f} mm2; "
    f"load {F_boss:.0f} N -> {F_boss/A_face:.1f} MPa; ring 0.6 wire d26.5 = {math.pi/4*0.36*math.pi*26.5:.0f} mm3 "
    f"vs need {A_face*0.04 + math.pi*26*1.0*0.05 + 10:.0f} mm3")
D.update(lap_gap=[gap_min, gap_nom, gap_max], lap_shear=tau_lap, ring_g=v_ring * 10.0 / 1000, boss_face_MPa=F_boss / A_face)

# ---------------- 4. draw feasibility ----------------
log("4. Draw feasibility (annealed OFE 1.0, n ~0.45, elongation >= 45 %, LDR ~2.1)")
sec_len = w_i + 2 * t + 2 * (h_i + t) - 2 * (2 - math.pi / 2) * (r_i + t)
stretch = sec_len / pitch - 1
log(f"   arch section developed {sec_len:.1f} mm per {pitch} pitch: {stretch*100:.0f} % if stretched in place -> NOT formable without feed;"
    f" station 1 forms the arches centre-outward with free blank feed from the y edges ({6*(sec_len-pitch):.0f} mm total draw-in)")
d_end, h_end = w_i + 2 * t, h_i + t
D0 = math.sqrt(d_end ** 2 + 4 * d_end * h_end)
log(f"   arch end (half cup d {d_end:.0f} x {h_end:.1f} deep): equivalent cup ratio {D0/d_end:.2f} (limit ~2.1); feed from the x blank margin;"
    f" thinning <= 30 % accepted (hoop at 0.70 wall {P_BURST*5/0.7:.0f} MPa)")
d_eq = 2 * math.sqrt(125 ** 2 / math.pi)
D0b = math.sqrt(d_eq ** 2 + 4 * d_eq * (lid_z1 - skirt["foot_z"]))
log(f"   skirt box draw: equivalent ratio {D0b/d_eq:.2f}; corners drawn at r_i 3 then re-struck to r_i 1.0 (mech IR-M2)")
blank = (125 + 2 * (lid_z1 - skirt["foot_z"]) + 2 * 20, 125 + 2 * (lid_z1 - skirt["foot_z"]) + 6 * (sec_len - pitch) + 2 * 8)
log(f"   blank {blank[0]:.0f} x {blank[1]:.0f} x 1.0 = {blank[0]*blank[1]*RHO_CU:.0f} g buy; springback at r/t 3.5-4.5 about 1 deg -> die over-bend 1.5 deg")
D.update(stretch_in_place=stretch, end_cup_ratio=D0 / d_end, blank=blank, blank_g=blank[0] * blank[1] * RHO_CU)

# ---------------- 5. guard (in-dome cup) ----------------
log("5. Guard: 316L 50 um abs square weave cup under the inlet dome (installed before braze)")
cup_d, cup_h, pleat_f = 30.0, 5.0, 1.8
A_mesh = math.pi * cup_d * cup_h + math.pi / 4 * cup_d ** 2 * pleat_f
u_face = Q18 / (A_mesh * 1e-6)
eps = 0.36
dp_mesh = 1.5 * 0.5 * RHO_PG * (u_face / eps) ** 2 / 1000
gap_under = 2.0
u_exit = 0.6 * Q18 / (math.pi * cup_d * gap_under * 1e-6)
dp_exit = 0.5 * 0.5 * RHO_PG * u_exit ** 2 / 1000
log(f"   area {A_mesh/100:.1f} cm2 (25 wanted): face {u_face:.2f} m/s, mesh dP {dp_mesh:.2f} kPa, under-cup exit {u_exit:.2f} m/s "
    f"{dp_exit:.2f} kPa -> guard {dp_mesh+dp_exit:.2f} kPa (0.30 booked)")
D.update(guard_area_cm2=A_mesh / 100, guard_dp_kpa=dp_mesh + dp_exit)

# ---------------- 6. mass ----------------
lid_A = 125 ** 2 - 4 * (1 - math.pi / 4) * 4
skirt_A = (4 * 123.4) * (lid_z0 - skirt["foot_z"] + 0.5)
arch_extra = sum(2 * x * (sec_len - pitch) for x in [x_in_ext] * 2 + [x_out_ext] * 4)
dome_extra = 2 * (2 * (35 + 36.5) * (h_i + t))
m_cap = (lid_A + skirt_A + arch_extra + dome_extra) * t * RHO_CU
m_boss = 2 * math.pi / 4 * (boss["od"] ** 2 - boss["bore"] ** 2) * (boss["z1"] - boss["z0"]) * RHO_CU
log(f"6. Mass: cap {m_cap:.0f} g (CAD provisional 259.5), bosses {m_boss:.0f} g (2), guard ~6 g; mech allocation 250")
D.update(mass_cap_g=m_cap, mass_bosses_g=m_boss)
(HERE / "cap_stress.out").write_text("\n".join(out) + "\n")
(HERE / "cap_stress_data.json").write_text(json.dumps(D, indent=1))
