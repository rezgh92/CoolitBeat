"""DDD-core: derived numbers for the PRISM-15 Rev A base + skived-fin core (layer 1).
Closed-form only; every output line is cited in DDD-core.md. Writes core_geom.out and params-core.json.
Coordinates: X along the fins, Y across the fins (lines/kerfs run along Y), Z up from the die face (datum A).
Run: python3 core_geom.py
"""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RHO = 8.94e-3            # g/mm3 OFE Cu
E, NU = 117e3, 0.34      # MPa
SY_ANN = 40.0            # MPa post-braze design allowable (architecture 5.2)
P_MAWP, P_PROOF, P_BURST, P_SAMPLE = 1.03, 1.55, 3.1, 4.5
RHO_F, MU_F = 1005.0, 1.25e-3   # PG25 45 C
LPM = 1 / 60000.0
out = []
def P(s=""): out.append(s); print(s)

# ---------------- 1. fixed architecture inputs ----------------
FIELD = 108.0; PITCH_LINE = FIELD / 14          # 7.7143 mm
FIN_T, FIN_GAP, FIN_H = 0.15, 0.15, 2.0; FIN_PITCH = FIN_T + FIN_GAP
N_FIN = int(round(FIELD / FIN_PITCH))           # 360
BASE_T, BASE_T_FALLBACK = 0.8, 1.0
KERF_W = 0.30; STUB = (0.05, 0.10)              # kerf floor above fin root (architecture 5.1)
BODY = 125.0; LAND_W = 1.8; LAND_Z = 1.5
# derived outline
RIM_OUT = BODY - 2 * LAND_W                      # 121.4 rim outer (skirt lap face)
POCKET_X, POCKET_Y = 108.7, 108.3                # skive pocket (x: blade + edge channel; y: 360 fins + 2 x 0.15)
EDGE_CH = (POCKET_X - FIELD) / 2                 # 0.35 edge outlet channel
RIM_W_X = RIM_OUT / 2 - POCKET_X / 2; RIM_W_Y = RIM_OUT / 2 - POCKET_Y / 2
XLINE = [-FIELD / 2 + PITCH_LINE * k for k in range(15)]
KERF_X = XLINE[1:14]                             # 13 interior kerfs; edge lines are the edge channels
INLET_K = [k for k in range(15) if k % 2 == 1]; OUTLET_K = [k for k in range(15) if k % 2 == 0]
SEG_INT = PITCH_LINE - KERF_W; SEG_EDGE = FIELD / 2 - (abs(XLINE[13]) + KERF_W / 2)
P("## 1. Layout")
P(f"lines x (mm): {', '.join(f'{x:+.3f}' for x in XLINE)}")
P(f"interior kerfs (13): x = {KERF_X[0]:+.3f} .. {KERF_X[-1]:+.3f} at {PITCH_LINE:.4f} pitch, w {KERF_W} +0.05/-0")
P(f"edge channels: x = +/-{FIELD/2:.2f} .. +/-{POCKET_X/2:.2f} ({EDGE_CH:.2f} wide, +0.10/-0), outlets (half line flow)")
P(f"fins: {N_FIN} x {FIN_T} mm at {FIN_PITCH} pitch, length {FIELD} (x = +/-54.0), height {FIN_H}; "
  f"centres y = {-FIELD/2 + FIN_PITCH/2:+.3f} .. {FIELD/2 - FIN_PITCH/2:+.3f}")
P(f"segment clear lengths: interior {SEG_INT:.3f} mm (x14 per gap incl. edges: edge {SEG_EDGE:.3f}); cell L = pitch {PITCH_LINE:.3f}")
P(f"outline: body {BODY} sq; rim outer {RIM_OUT:.1f} sq (lap face); land {LAND_W} wide at z {LAND_Z}; "
  f"pocket {POCKET_X} x {POCKET_Y}; rim top width x {RIM_W_X:.2f} / y {RIM_W_Y:.2f}; border {(BODY-FIELD)/2:.2f}")

# ---------------- 2. blank and skive volume balance ----------------
P("\n## 2. Blank, pocket and skive volume balance")
d_consumed = FIN_H * FIN_T / FIN_PITCH          # 1.0 mm of blank depth becomes fin
BASE_SKIVE = 2.0                                 # base under the fins during the skive (pre-braze)
BLANK = BASE_SKIVE + d_consumed + (FIN_H - d_consumed)   # rim top coplanar with fin tips -> 4.0
POCKET_D = BLANK - BASE_SKIVE - d_consumed       # 1.0 pocket depth before the skive
FLYCUT = BASE_SKIVE - BASE_T
P(f"skive consumes d = h*t/p = {d_consumed:.2f} mm; pocket depth {POCKET_D:.2f}; base during skive {BASE_SKIVE:.2f} "
  f"(verify-mfg floor 1.5-2.0); machined blank {BLANK:.2f} (raw plate 4.2-4.5); post-braze fly-cut removes {FLYCUT:.2f} mm")
for uc in (0.05, 0.08):
    P(f"  skive stroke force, uncut chip {uc} x {POCKET_X-0.4:.1f} mm, kc 1.2-1.8 GPa: "
      f"{1.2e3*uc*(POCKET_X-0.4)/1e3:.1f}-{1.8e3*uc*(POCKET_X-0.4)/1e3:.1f} kN")
P(f"  aspect ratio h/gap = {FIN_H/FIN_GAP:.1f} (skiving range 10-25); h/t = {FIN_H/FIN_T:.1f}")
P(f"  CTX-class machine limits (web): Cu fin >= 0.08 mm, fin centre distance >= 0.16 mm, height 1-180 mm -> 0.15/0.30/2.0 inside")

# ---------------- 3. kerfing by gang saw ----------------
P("\n## 3. Kerf gang saw")
BLADE_T, BLADE_D, Z_TEETH = 0.28, 20.0, 40
KERF_DEPTH = FIN_H - 0.5 * sum(STUB)             # 1.925 from the tip plane
for D in (16.0, 20.0, 25.0, 32.0):
    R = D / 2; run = math.sqrt(2 * R * KERF_DEPTH - KERF_DEPTH ** 2)
    P(f"  saw D {D:.0f}: arc run-out beyond full-depth point {run:.2f} mm (field edge to rim wall: {POCKET_Y/2-FIELD/2:.2f}; "
      f"full-depth zone |y| <= {FIELD/2-run:.1f})")
R = BLADE_D / 2; run20 = math.sqrt(2 * R * KERF_DEPTH - KERF_DEPTH ** 2)
ys = np.linspace(FIELD / 2 - run20, FIELD / 2, 200)
depth = KERF_DEPTH - (R - np.sqrt(np.maximum(R ** 2 - (ys - (FIELD / 2 - run20)) ** 2, 0)))
frac_ramp = 2 * run20 / FIELD; mean_depth_ramp = depth.mean() / KERF_DEPTH
P(f"  D 20 ramp zones: 2 x {run20:.2f} mm = {frac_ramp*100:.1f} % of field length; mean kerf depth in ramp {mean_depth_ramp*100:.0f} %")
P(f"  thermal cost of ramps: kerf credit 0.4 K (arch 3.2) x (1-{mean_depth_ramp:.2f}) x {frac_ramp:.3f} = "
  f"+{0.4*(1-mean_depth_ramp)*frac_ramp:.3f} K average; local <= +0.4 K in the last ~2 mm (also rim-cooled)")
for vc in (150, 250):
    n = vc * 1e3 / (math.pi * BLADE_D)
    for fz in (0.003, 0.005):
        P(f"  Vc {vc} m/min -> n {n:.0f} rpm; fz {fz} -> vf {n*Z_TEETH*fz:.0f} mm/min; tooth force kc1.5GPa x fz x {BLADE_T} = "
          f"{1500*fz*BLADE_T:.2f} N (fin lateral capacity 1.4-5 N cold-worked; wax-potted fins are backed)")
P(f"  kerf width = blade {BLADE_T} + side clearance/runout 0.02-0.06 -> 0.30-0.34 (spec 0.30 +0.05/-0)")
P(f"  kerf depth {KERF_DEPTH:.3f} +/-0.025 from the planed tip plane -> floor {STUB[0]:.2f}-{STUB[1]:.2f} above the fin root; never into the base")
P(f"  burr/chip sites: 13 kerfs x {N_FIN} x 2 + 2 trims x {N_FIN} = {13*N_FIN*2 + 2*N_FIN}")
# kerf hydraulics
q_line_in = 18.0 / 7 * LPM                       # m3/s per inlet line (2.571 LPM)
q_line_out_int = 18.0 / 7 * LPM; q_line_edge = 0.5 * q_line_out_int
A_kerf = KERF_W * 1e-3 * FIELD * 1e-3; A_edge = EDGE_CH * 1e-3 * FIELD * 1e-3
P(f"  kerf as a vertical duct (half the line flow descends ~half-depth): mean v {0.5*q_line_in/A_kerf:.2f} m/s interior; "
  f"edge channel {0.5*q_line_edge/A_edge:.2f} m/s (cap: fin entry <= 0.5 m/s)")
v_gap = (18.0 * LPM) / (N_FIN * FIN_GAP * 1e-3 * FIN_H * 1e-3 * 14)   # 14 segments per gap in parallel, all flow
P(f"  fin gap bulk velocity 18 LPM / (360 gaps x 14 segments x 0.15 x 2.0): {v_gap:.3f} m/s (architecture 0.20)")

# ---------------- 4. tip planing, fly-cut and tolerance stack ----------------
P("\n## 4. Tip plane, die face and tolerance stack")
kf = E * (FIN_T / FIN_PITCH) / FIN_H              # N/mm3 foundation modulus of tied fins
Dp = lambda t: E * t ** 3 / (12 * (1 - NU ** 2))
for tb in (BASE_T, BASE_T_FALLBACK):
    w = 1 / (8 * math.sqrt(Dp(tb) * kf)); lam = (Dp(tb) / kf) ** 0.25
    P(f"  fly-cut on tied fins, base {tb}: foundation k {kf:.0f} N/mm3, char. length {lam:.2f} mm, 50 N thrust -> {50*w*1e3:.2f} um")
comps_open = {"skived root plane": 0.05, "as-brazed bow (clamped)": 0.05, "fly-cut": 0.01, "gauge": 0.02}
comps_mapped = {"UT map of root plane (9 pts)": 0.02, "residual bow between pts": 0.015, "fly-cut": 0.01, "gauge": 0.01}
for lab, c in (("open-loop", comps_open), ("per-plate UT-mapped final pass", comps_mapped)):
    rss = math.sqrt(sum(v ** 2 for v in c.values())); wc = sum(c.values())
    P(f"  base thickness, {lab}: RSS +/-{rss:.3f}, worst +/-{wc:.3f} (spec 0.80 +0.10/-0 -> target 0.85 +/-0.05)")
P(f"  machining layer 30 um at 100 MPa residual: bow 14 um over 108 mm (verify-mfg) -> diamond finish pass <= 10 um deep: ~5 um")
P(f"  tip plane: planed along the fins with the rim top in the same pass -> coplanar by construction; spec <= 0.020 (route A/C), <= 0.010 target (route B)")

# ---------------- 5. stresses on core features ----------------
P("\n## 5. Stresses (allowable 40 MPa post-braze, architecture 5.2)")
for f in (0.70, 0.56):
    s = P_BURST * FIN_PITCH / (FIN_T * f)
    P(f"  fin tie at 3.1 MPa, bonded fraction {f:.2f}: {s:.1f} MPa ({2.5*s:.0f} local Kt 2.5); at 4.5 MPa {P_SAMPLE*FIN_PITCH/(FIN_T*f):.1f}")
s_strip = P_BURST * (FIN_GAP) ** 2 / (2 * BASE_T ** 2)
P(f"  base strip between fins (0.15 span, 0.8 base) at 3.1 MPa: {s_strip:.3f} MPa")
for span, lab in ((KERF_W, "interior kerf"), (EDGE_CH, "edge channel"), (1.2 + 2 * 0.3, "window + masking (fins continuous below)")):
    P(f"  base over {lab} {span:.2f} mm span, 0.8 base: {P_BURST*span**2/(2*BASE_T**2):.2f} MPa")
hinge = BASE_T; L_def = PITCH_LINE - KERF_W      # unbonded land strip spans kerf to kerf
for tb in (0.80, 0.75, 0.70):
    P(f"  defect case (one unbonded land strip, span {L_def:.2f}), hinge {tb:.2f}: proof {6*P_PROOF*L_def**2/12/tb**2:.0f}-"
      f"{6*P_PROOF*L_def**2/8/tb**2:.0f} MPa; collapse {16*(SY_ANN*tb**2/4)/L_def**2:.2f} MPa (E1 gate on per-strip detection)")
P(f"  -> kerf stub >= {STUB[0]:.2f} mm guarantees hinge >= base: no kerf overshoot into the 0.8 mm base")
# rim / land / ears
F_clamp = (300.0, 1000.0, 2000.0)
for F in F_clamp:
    per = F / 8; a_ear = 12.0 * (LAND_Z); M = per * 3.5; Z = 12.0 * LAND_Z ** 2 / 6
    P(f"  clamp {F:.0f} N via load frame on the stack; if 1/8 reached an ear as a cantilever at the hole (3.5 mm arm): {M/Z:.0f} MPa "
      f"-> ears locate only; frame bears on the cap flats")
shock = 1.27 * 50 * 9.81
P(f"  shock 50 g x 1.27 kg = {shock:.0f} N; in-plane on 8 ears {shock/8/(12*LAND_Z):.1f} MPa; z-lift over clamp (300 N min) "
  f"{(shock-300)/8:.0f} N per ear at <= 2 mm stop arm: {(shock-300)/8*2/(12*LAND_Z**2/6):.0f} MPa (<= 40)")
P(f"  lap seam load: cavity pressure is carried by the tied stack, skirt hoop sees end-frame leakage only -> seam is a leak barrier (verify-mfg SF 4.5-6.5)")
P(f"  rim top braze land (grate margin): x {RIM_W_X:.2f} / y {RIM_W_Y:.2f} wide, filler masked 0.3 from the pocket edge -> {RIM_W_X-0.3-0.2:.2f} wetted")

# ---------------- 6. mass, copper buy, thermal consequences ----------------
P("\n## 6. Mass, copper, thermal consequences")
EAR_W, EAR_L, EAR_N = 12.0, 7.0, 8
BOSS_W, BOSS_L, BOSS_Z, BOSS_N = 8.0, 7.0, 2.8, 2
v_base = BODY ** 2 * BASE_T
v_rim = (RIM_OUT ** 2 - POCKET_X * POCKET_Y) * FIN_H
v_land = (BODY ** 2 - RIM_OUT ** 2) * (LAND_Z - BASE_T)
v_fins = N_FIN * FIN_T * FIELD * FIN_H * (1 - 13 * KERF_W / FIELD * (KERF_DEPTH / FIN_H))
v_ears = EAR_N * EAR_W * EAR_L * LAND_Z - EAR_N * math.pi / 4 * 3.4 ** 2 * LAND_Z
v_boss = BOSS_N * BOSS_W * BOSS_L * BOSS_Z
v_pins = -2 * math.pi / 4 * 2.0 ** 2 * 1.5
vols = dict(base=v_base, rim=v_rim, land_step=v_land, fins=v_fins, ears=v_ears, tap_bosses=v_boss, pin_holes=v_pins)
m_tot = sum(vols.values()) * RHO / 1e3
for k, v in vols.items(): P(f"  {k}: {v*RHO/1e3:.3f} kg")
P(f"  core finished mass {m_tot:.3f} kg (architecture base+fins line 0.251; plate 1.24 -> {1.24 - 0.251 + m_tot:.2f} kg, limit 1.4)")
raw = (BODY + 2 * EAR_L + 2) * (BODY + 2 * EAR_L + 2) * 4.3 * RHO / 1e3
raw_sq = (BODY + 2) ** 2 * 4.3 * RHO / 1e3
P(f"  copper buy: {BODY+2*EAR_L+2:.0f} sq x 4.3 raw = {raw:.2f} kg (ears in the blank); {BODY+2:.0f} sq = {raw_sq:.2f} kg if ears are not needed; "
  f"architecture line 0.456 kg -> +{raw-0.456:.2f} kg buy, ~+US${(raw-0.456)*(14.6+4.0) - (raw-0.456)*14.6*0.88:.1f}/plate net of scrap")
P(f"  fin length 108.0 = field: 0 K; fin count 360 = architecture: 0 K; kerf ramps +{0.4*(1-mean_depth_ramp)*frac_ramp:.2f} K avg; "
  f"kerf stub 0.05-0.10: ~0 K (cell2d kerf-floor h credit is small, arch 3.2)")
P(f"  base 0.8 vs 1.0 fallback: 31.0/38.7 -> 31.7/39.2 K paste (final_thermal.out), +0.7 K")
P(f"  transient near-die heat capacity: 0.8 base {0.8e-3*8940*385/1e4*1e4/1e4:.2f} J/K/cm2 base alone (+ fins); architecture 0.28 J/K/cm2 with fins")

# ---------------- 7. params JSON ----------------
params = {
  "_meta": {"doc": "DDD-core.md", "units": "mm", "axes": "X along fins, Y across fins (lines run along Y), Z up from die face (datum A)",
            "origin": "fin-field centre on the die face", "date": "2026-10-15", "source": "core_geom.py"},
  "material": {"alloy": "C10100 OFE (C10200 OF alternate), ASTM B152 plate", "temper_blank": "H02 (H01 alternate, fixed by skiving trial E1)",
               "post_braze_allowable_MPa": 40, "density_g_cm3": 8.94},
  "body": {"x": BODY, "y": BODY, "corner_r": 2.0, "tol": 0.1},
  "base_t": {"nom": 0.85, "min": 0.80, "max": 0.90, "fallback": 1.0, "note": "final, after post-braze fly-cut; 0.8 gated on E1 per-strip detection"},
  "blank": {"raw_t": 4.3, "raw_t_range": [4.2, 4.5], "machined_t": BLANK, "pocket_depth": POCKET_D, "base_during_skive": BASE_SKIVE, "flycut_removal": FLYCUT},
  "pocket": {"x": POCKET_X, "y": POCKET_Y, "corner_r": 0.5, "tol": 0.05, "wall_z_top": BASE_T + FIN_H},
  "fin_field": {"x": FIELD, "y": FIELD, "x_extent": [-FIELD/2, FIELD/2]},
  "fin_pitch": FIN_PITCH, "fin_pitch_tol": 0.005, "fin_t": FIN_T, "fin_t_tol": 0.02, "fin_gap": FIN_GAP, "fin_h": FIN_H, "fin_h_tol": 0.02,
  "n_fins": N_FIN, "fin_y_centres": [round(-FIELD/2 + FIN_PITCH/2 + i*FIN_PITCH, 3) for i in range(N_FIN)],
  "fin_tip_z": BASE_T + FIN_H, "tip_plane_flatness": 0.020, "tip_plane_flatness_routeB": 0.010,
  "line_pitch": round(PITCH_LINE, 4), "n_lines": 15, "line_x": [round(x, 4) for x in XLINE], "inlet_k": INLET_K, "outlet_k": OUTLET_K,
  "kerf_w": KERF_W, "kerf_w_tol": [0.0, 0.05], "kerf_x": [round(x, 4) for x in KERF_X], "kerf_x_tol": 0.05,
  "kerf_depth_from_tip": round(KERF_DEPTH, 3), "kerf_depth_tol": 0.025, "kerf_stub_above_root": list(STUB),
  "kerf_full_depth_y": round(FIELD/2 - run20, 1), "kerf_ramp_runout": round(run20, 2), "saw": {"d": BLADE_D, "t": BLADE_T, "teeth": Z_TEETH, "bore": 5.0},
  "edge_channel": {"x_inner": FIELD/2, "x_outer": POCKET_X/2, "w": round(EDGE_CH, 2), "w_tol": [0.0, 0.10], "role": "edge outlet line k=0,14, half line flow"},
  "segment_len": {"interior": round(SEG_INT, 3), "edge": round(SEG_EDGE, 3), "cell_L": round(PITCH_LINE, 3)},
  "rim": {"outer": RIM_OUT, "outer_tol": 0.05, "top_z": BASE_T + FIN_H, "width_x": round(RIM_W_X, 2), "width_y": round(RIM_W_Y, 2),
          "top_chamfer_outer": 0.3, "braze_mask_from_pocket": 0.3, "grate_outline_recommended": 121.0},
  "land_w": LAND_W, "land_z": LAND_Z, "land_z_tol": 0.05, "land_role": "cap-skirt lap seam (only external perimeter seam)",
  "ears": {"n": EAR_N, "w": EAR_W, "protrusion": EAR_L, "z_top": LAND_Z, "corner_r": 2.0, "hole_d": 3.4, "hole_d_tol": [0.0, 0.10],
           "hole_offset_from_body_edge": 3.5, "alt_hole_d_M4": 4.5,
           "positions": [[-40.0, -66.0], [40.0, -66.0], [-40.0, 66.0], [40.0, 66.0], [-66.0, -40.0], [-66.0, 40.0], [66.0, -40.0], [66.0, 40.0]]},
  "tap_bosses": {"n": BOSS_N, "w": BOSS_W, "protrusion": BOSS_L, "z_top": BOSS_Z, "side": "-y",
                 "x_centres": [0.0, round(XLINE[9], 3)], "hole_d": 1.0, "hole_z": 1.4, "hole_len": round(BOSS_L + (BODY/2 - POCKET_Y/2), 2),
                 "stub_counterbore": [1.65, 4.0], "stub_tube": "Cu 1.6 OD x 0.3 wall, brazed in the same cycle", "reads": "inlet kerf k=7 vs outlet kerf k=9 (fin-field dP)",
                 "drilled_on": "-T SKUs (R+, P, pilot, qualification)"},
  "pin_holes": {"d": 2.0, "fit": "H7", "depth": 1.5, "positions": [[57.5, 57.5], [-57.5, -57.5]], "pin": "alumina 2.0 x 5.5"},
  "die_face": {"flatness_fin_field": 0.020, "ra_um": 0.8, "parallel_to_ear_plane": 0.03},
  "datums": {"A": "die face (z=0)", "B": "body edge x=-62.5", "C": "body edge y=-62.5"},
  "hbm_pedestal_variant": {"pedestal_base_t": [0.8, 0.9], "field_base_t_min": 0.8, "step": [0.0, 0.20], "step_tol": 0.02, "edge": "die outline + 0.5, R0.2"},
  "mass_kg": round(m_tot, 3), "copper_buy_kg": round(raw, 2)}
with open(os.path.join(HERE, "params-core.json"), "w") as f: json.dump(params, f, indent=1)
with open(os.path.join(HERE, "core_geom.out"), "w") as f: f.write("\n".join(out) + "\n")
print("\nwrote params-core.json and core_geom.out")
