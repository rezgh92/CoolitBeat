"""DDD-grate: single-cell geometry, jet-landing margins, fin-top velocity, orifice hydraulics, bond fraction, grate
stresses, process limits and mass for the PRISM-15 Rev A metered grate (two laminations: 1.30 mm land plate + 0.40 mm
meter web). Every number in DDD-grate.md sections 3-9 that is not a drawing choice comes from here (grate_cell.out).
Conventions: X along the fins (across the lines), Y along the lines, Z up from the die face (cad/prism_cad.py).
Fluid PG25 at 45-50 C: rho 1005 kg/m3, mu 1.25 mPa s (verify-hydraulics). Run: python3 grate_cell.py"""
import math, os
rho, mu = 1005.0, 1.25e-3
LPM = 1 / 60000
out = []
P = lambda s="": out.append(s)

# ---------------- fixed by the architecture (03-architecture.md 2.2, 3.2, 4.1, 5.1) ----------------
T_GRATE, T_WEB = 1.70, 0.40            # mm
PITCH = 108 / 14                        # 7.7143 mm line pitch, 15 lines
WIN = 1.20                              # window width through the land to the kerf
KERF = 0.30; FIN_T = 0.15; GAP = 0.15; FIN_H = 2.0
ORIF_W, ORIF_L = 0.50, 1.05             # inlet orifice width (x) and as-drawn mean length (y); r 0.10 corners
N_ORIF, ORIF_PITCH = 54, 2.0
U_MEAN = 1.54; CD = 0.72; DP_METER = 0.5 * rho * U_MEAN**2 / CD**2 / 1e3   # 2.30 kPa
MASK = 0.30                              # filler mask from window / recess edges
# ---------------- set in this document ----------------
RECESS_W, RECESS_D = 2.70, 0.80          # upper recess in the land plate top face (mm), floor 0.50
LIP = (RECESS_W - WIN) / 2               # 0.75
X_OFF = 1.00                             # orifice centre offset from the line centre
T_LAND = T_GRATE - T_WEB                 # 1.30
T_FLOOR = T_LAND - RECESS_D              # 0.50
GROOVE_W, GROOVE_D = 0.15, 0.08          # capillary-break scribe inside the mask zone
TOL_ORIF, TOL_LAND, TOL_REG = 0.02, 0.03, 0.03    # orifice position, pocket/window position, lamination registration

P("# grate_cell.py output (DDD-grate)")
P(f"grate {T_GRATE} = web {T_WEB} + land plate {T_LAND:.2f}; recess {RECESS_W} x {RECESS_D} deep -> floor {T_FLOOR:.2f}; lip {LIP:.2f}; window {WIN}")

# ---------------- 1. jet landing ----------------
q_or = 18 * LPM / (7 * N_ORIF)                       # m3/s per orifice at 18 LPM
A_or = ORIF_W * ORIF_L - (4 - math.pi) * 0.1**2      # mm2
u_or = q_or / (A_or * 1e-6)
u_vc = u_or / 0.62                                   # vena-contracta velocity if the jet does not reattach (Cc 0.62)
H = RECESS_D                                         # stand-off from the web underside to the lip
spread = 0.10 * H                                    # planar-jet mixing-layer growth ~0.1 x per side (near field, x/w < 3)
jet_in = X_OFF - ORIF_W / 2 - spread                 # inner edge of the jet at the lip
jet_out = X_OFF + ORIF_W / 2 + spread
m_in = jet_in - WIN / 2                              # clearance to the window edge
m_out = RECESS_W / 2 - (X_OFF + ORIF_W / 2)          # orifice outer edge to the recess wall (must stay >= 0: no blocked area)
rss = math.sqrt(TOL_ORIF**2 + TOL_LAND**2 + TOL_REG**2); worst = TOL_ORIF + TOL_LAND + TOL_REG
P("\n## 1. Jet landing on the lip (18 LPM)")
P(f"orifice {ORIF_W} x {ORIF_L} r0.10 = {A_or:.4f} mm2; mean exit u {u_or:.2f} m/s; vena contracta (Cc 0.62) {u_vc:.2f} m/s; stagnation 0.5 rho u^2 {0.5 * rho * u_or**2 / 1e3:.2f}-{0.5 * rho * u_vc**2 / 1e3:.2f} kPa")
P(f"stand-off H {H:.2f} mm = {H / ORIF_W:.1f} orifice widths (potential core 4-6 w: jet core intact at the lip); spread {spread:.3f} mm per side")
P(f"jet footprint on the lip x = {jet_in:.3f} .. {jet_out:.3f} (lip x = {WIN / 2:.2f} .. {RECESS_W / 2:.2f})")
P(f"inner margin jet edge -> window edge {m_in:.3f} mm; outer margin orifice edge -> recess wall {m_out:.3f} mm")
P(f"position stack (orifice +/-{TOL_ORIF}, pocket/window +/-{TOL_LAND}, registration +/-{TOL_REG}): RSS +/-{rss:.3f}, worst +/-{worst:.3f}")
P(f"margins at RSS: inner {m_in - rss:.3f}, outer {m_out - rss:.3f}; at worst case: inner {m_in - worst:.3f}, outer {m_out - worst:.3f}")
for rw, lip_alt in ((2.50, 0.65), (2.60, 0.70), (2.70, 0.75), (2.80, 0.80)):
    xo = rw / 2 - ORIF_W / 2 - 0.10                  # keep 0.10 outer margin
    mi = xo - ORIF_W / 2 - spread - WIN / 2
    P(f"  recess {rw:.2f} / lip {lip_alt:.2f}: orifice centre {xo:.3f}, inner margin nominal {mi:.3f}, at RSS {mi - rss:.3f}")
tau = 0.04 * 0.5 * rho * u_vc**2
P(f"lip wall shear (impinging slot jet, Cf ~0.03-0.05 on the vena-contracta velocity): ~{0.03 * 0.5 * rho * u_vc**2:.0f}-{0.05 * 0.5 * rho * u_vc**2:.0f} Pa at 18 LPM, x{(22.5 / 18)**2:.2f} at 22.5 LPM (copper, PG25, <= 50 um particles: erosion check is E4)")

# ---------------- 2. window entry and fin-top velocity ----------------
P("\n## 2. Window entry and fin-top velocity")
u_win = (18 * LPM / 7) / (WIN * 108e-6)              # mean through the window face
P(f"mean velocity through the 1.2 x 108 window face: {u_win:.3f} m/s at 18 LPM, {u_win * 22.5 / 18:.3f} at 22.5 LPM (cap 0.5)")
P("entry-sheet model: all of an orifice's flow crosses the window edge through a section H x pitch (lip-side wall jet), then decays ~20 % over the 0.5 mm floor before the fin tops")
P("| H mm | floor mm | entry sheet u 18 LPM | fin-top est. 18 LPM | fin-top est. 22.5 LPM | inner jet margin (nominal) |")
P("|---|---|---|---|---|---|")
for Hh in (0.60, 0.70, 0.80, 0.90, 1.00):
    ue = q_or / (Hh * ORIF_PITCH * 1e-6)
    mi = X_OFF - ORIF_W / 2 - 0.10 * Hh - WIN / 2
    P(f"| {Hh:.2f} | {T_LAND - Hh:.2f} | {ue:.2f} | {0.8 * ue:.2f} | {0.8 * ue * 22.5 / 18:.2f} | {mi:.3f} |")
kerf_share = (KERF * 108) / (WIN * 108)
P(f"kerf fraction of the window face {kerf_share:.2f}; fin-tip stubs under the window {(WIN - KERF) / 2:.2f} mm each side (open, unbonded)")
P("the estimate is +/-30 %: H is fixed by the E2 single-cell CFD and water-table PIV (pass: fin-top <= 0.5 m/s at 18 LPM); H range 0.7-0.9 mm, floor 0.4-0.6")

# ---------------- 3. orifice hydraulics ----------------
P("\n## 3. Orifice hydraulics")
Dh = 4 * A_or / (2 * (ORIF_W + ORIF_L))
Re = rho * u_or * Dh * 1e-3 / mu
P(f"Dh {Dh:.3f} mm; t/Dh {T_WEB / Dh:.2f} (thick-orifice regime); Re {Re:.0f} at 18 LPM, {Re * 9 / 18:.0f} at 9 LPM, {Re * 36 / 18:.0f} at 36 LPM")
P("| Cd | meter dp 18 LPM kPa | plate dp 18 LPM kPa (7.6 at Cd 0.72) | note |")
P("|---|---|---|---|")
for cd, note in ((0.61, "sharp thin plate, no reattachment"), (0.65, "verify-hydraulics low"), (0.72, "design, coupon-gated"), (0.80, "rounded entry / reattached")):
    dpm = 0.5 * rho * U_MEAN**2 / cd**2 / 1e3
    P(f"| {cd:.2f} | {dpm:.2f} | {7.6 - DP_METER + dpm:.2f} | {note} |")
P(f"meter dp is {DP_METER / 7.6 * 100:.0f} % of plate dp; a +/-10 % Cd error moves plate dp by {DP_METER * (1 / 0.9**2 - 1):.2f} / {DP_METER * (1 / 1.1**2 - 1):.2f} kPa")
P(f"velocity cap 2.0 m/s (mean) reached at {2.0 / U_MEAN * 18:.1f} LPM; smallest-step orifices run 6 % above the mean (grate_artwork.out)")

# ---------------- 4. outlet row ----------------
P("\n## 4. Outlet orifice row (0.5 kPa at the line's nominal 18 LPM flow)")
u_row = CD * math.sqrt(2 * 500 / rho)
for lab, Ql, n, w, h, r in (("interior line", 18 * LPM / 7, 54, 1.00, 1.12, 0.15), ("edge line", 18 * LPM / 14, 27, 0.40, 2.78, 0.10)):
    A = w * h - (4 - math.pi) * r * r
    u = Ql / (n * A * 1e-6); dp = 0.5 * rho * u**2 / CD**2 / 1e3
    P(f"{lab}: {Ql / LPM:.3f} LPM, {n} holes {w} x {h} r{r} = {A:.4f} mm2 each ({n * A:.1f} mm2); u {u:.3f} m/s; dp {dp:.3f} kPa at 18 LPM, {dp * 4:.2f} at 36 LPM (Cd {CD}; row u target {u_row:.3f})")
P("segment balance with the row lumped per outlet line: grate_outlet_row.out (1.092 at 18 LPM, 1.122 at 27, 1.148 at 36; E2 pass <= 1.15 / 1.20)")

# ---------------- 5. bond fraction and filler ----------------
P("\n## 5. Land pattern, bond fraction, filler")
unb = WIN + 2 * MASK
bond_pitch = (PITCH - unb) / PITCH; bond_tip = (PITCH - unb) / (PITCH - KERF)
P(f"unbonded per line: window {WIN} + 2 x mask {MASK} = {unb:.2f} mm; bonded land per pitch {PITCH - unb:.3f} mm")
P(f"bond fraction: {bond_pitch:.3f} of the pitch, {bond_tip:.3f} of the fin-tip length between kerfs (target >= 0.70; E1 gate: every land strip >= 70 % bonded over any 10 mm -> {0.7 * bond_pitch:.2f} effective)")
P(f"capillary-break groove {GROOVE_W} x {GROOVE_D} at x = +/-{WIN / 2 + 0.10 + GROOVE_W / 2:.3f} (inside the mask zone {WIN / 2:.2f}-{WIN / 2 + MASK:.2f}); bonded width unchanged")
sig = 0.90   # N/m, Ag-Cu eutectic on Cu
for g in (10e-6, 25e-6, 40e-6, GAP * 1e-3, KERF * 1e-3):
    P(f"  capillary pressure 2 sigma / h at h {g * 1e6:.0f} um: {2 * sig / g / 1e3:.1f} kPa")
foil = 0.013; solid = FIN_T / (FIN_T + GAP)
P(f"route A foil {foil * 1e3:.0f} um over the land: liquid per mm2 of land {foil * 1e3:.1f} um; tip plane +/-10 um needs ~{10 / solid:.0f} um equivalent -> 12-15 um foil (verify-manufacturing #9)")
P(f"filler volume per plate (both grate interfaces, route A 13 um): tips {13e-3 * (PITCH - unb) / PITCH * 108 * 108 * solid:.0f} mm3, web/land {13e-3 * (122.6**2 - 7 * (RECESS_W + 2 * MASK) * 109 - 8 * (WIN + 2 * MASK) * 108):.0f} mm3 -> ~{(13e-3 * (PITCH - unb) / PITCH * 108 * 108 * solid + 13e-3 * (122.6**2 - 7 * (RECESS_W + 2 * MASK) * 109 - 8 * (WIN + 2 * MASK) * 108)) * 0.0100:.1f} g BAg-8 (10.0 g/cm3)")

# ---------------- 6. stresses (post-braze OFE, design allowable 40 MPa, 3.1 MPa design burst) ----------------
P("\n## 6. Grate stresses")
p_b = 3.1
dp36 = DP_METER * 4 / 1e3                             # MPa, meter dp at 36 LPM
P(f"web over the recess (2.7 span, 0.4 t) under meter dp {dp36 * 1e3:.1f} kPa at 36 LPM, fixed-edge plate: {0.5 * dp36 * (RECESS_W / T_WEB)**2:.2f} MPa; under proof/burst the web is wet both sides (0 net)")
leg_x = PITCH / 2 - 6.9 / 2                           # plenum leg inner face from the line centre: 0.4 mm... (leg 0.8 wide, channel 6.9)
P(f"plenum leg (0.8 wide) stands {PITCH / 2 - 0.4 - 0.4:.2f}-{PITCH / 2 - 0.4 + 0.4:.2f} mm from each line centre, on the full-thickness land; leg tension {p_b * PITCH / 0.8:.1f} MPa (pkgA_dp_stress)")
arm_o = (PITCH / 2 - 0.4) - WIN / 2                   # land strip from the outlet window edge to the leg centre
M_o = p_b * (arm_o - 0.4) * ((arm_o - 0.4) / 2 + 0.4)
P(f"outlet side: land strip {arm_o - 0.4:.2f} mm from the window edge to the leg face, tie pull {p_b:.1f} MPa -> moment {M_o:.1f} N mm/mm, sigma {6 * M_o / T_GRATE**2:.1f} MPa at t {T_GRATE} (allowable 40; pkgA 28.6 at a 3.25 mm arm)")
arm_i = (PITCH / 2 - 0.4) - RECESS_W / 2
M_i = p_b * (arm_i - 0.4) * ((arm_i - 0.4) / 2 + 0.4)
P(f"inlet side: full-thickness land {arm_i - 0.4:.2f} mm from the recess wall to the leg face -> {6 * M_i / T_GRATE**2:.1f} MPa; recess floor cantilever {LIP:.2f} mm at t {T_FLOOR:.2f}, tied from x {WIN / 2 + MASK:.2f}: M {p_b * (LIP - MASK) * ((LIP - MASK) / 2):.2f} -> {6 * p_b * (LIP - MASK) * ((LIP - MASK) / 2) / T_FLOOR**2:.1f} MPa")
tie = p_b * PITCH / ((PITCH - unb) * solid * 0.70)
P(f"tie stress per leg pitch at f 0.70: {tie:.1f} MPa mean (verify-manufacturing 8.9 mean / 22 local on the fin-root basis)")
P(f"governing defect unchanged: one unbonded land strip spans kerf to kerf ({PITCH - KERF:.2f} mm), base lane / E1 (pkgA_dp_stress: 67-99 MPa at proof, 0.8 mm base)")

# ---------------- 7. process limits ----------------
P("\n## 7. Process-limit checks (OFE C10100, annealed after braze; piercing in H01/H02 strip)")
P("| feature | d or w | t | d/t | web between | web/t | laser | perforating die |")
P("|---|---|---|---|---|---|---|---|")
rows = (("inlet orifice 0.5 x 1.05", ORIF_W, T_WEB, ORIF_PITCH - 1.12), ("outlet hole 1.0 x 1.12", 1.00, T_WEB, ORIF_PITCH - 1.12),
        ("edge outlet 0.4 x 2.78", 0.40, T_WEB, 4.0 - 2.78), ("window 1.2 in the 0.5 floor", WIN, T_FLOOR, PITCH - WIN - RECESS_W),
        ("window 1.2 in 1.3 (outlet)", WIN, T_LAND, PITCH - WIN - RECESS_W))
for lab, d, t, web in rows:
    P(f"| {lab} | {d:.2f} | {t:.2f} | {d / t:.2f} | {web:.2f} | {web / t:.2f} | {'ok' if d >= 0.10 else 'no'} | {'ok' if d / t >= 1.0 and web / t >= 1.5 else ('fine-blank' if d / t >= 0.6 and web / t >= 1.0 else 'no')} |")
P("rules: conventional piercing d >= 1.0 t, web >= 1.5-2 t (Mate / Xometry, verify-manufacturing); fine-blank d >= 0.6 t; punch clearance 4-6 % t per side for annealed Cu;")
P("burr <= 10 % t (shaved <= 0.015 mm); rollover 10-20 % t on the punch-entry side; laser: min feature 0.10 mm, kerf 0.03-0.05, taper <= 1 deg (<= 0.007/side over 0.4), HAZ <= 0.03, dross <= 0.02 (electropolish 3-5 um), position +/-0.01-0.02")
P("coining (closed die, annealed OFE): depth <= 30-40 % t at 300-600 MPa; the 0.8 deep recess is 62 % of 1.3 mm -> milled, not coined (coining only for the 0.08 grooves if not laser-scribed)")
P(f"gang/multi-spindle slot milling: 7 pockets x 109 mm, 2.7 mm 2-flute carbide, 2 passes of 0.4 -> {7 * 109 * 2 / 1500:.1f} min at 1.5 m/min; laser piercing 756 holes x ~0.1 s -> ~{756 * 0.1 / 60:.1f} min")

# ---------------- 8. mass ----------------
P("\n## 8. Mass (OFE 8.94 g/cm3)")
OUT_ = 122.6
V_land = OUT_**2 * T_LAND - 7 * RECESS_W * RECESS_D * 109 - (13 * WIN * 108 * T_FLOOR * 0 + 6 * WIN * 108 * T_LAND + 7 * WIN * 108 * T_FLOOR + 2 * 0.6 * 108 * T_LAND) - 2 * math.pi / 4 * 3.0**2 * T_LAND
V_web = OUT_**2 * T_WEB - 378 * A_or * T_WEB - 324 * (1.0 * 1.12 - (4 - math.pi) * 0.15**2) * T_WEB - 54 * (0.4 * 2.78 - (4 - math.pi) * 0.1**2) * T_WEB
P(f"land plate {V_land * 8.94e-3:.0f} g; meter web {V_web * 8.94e-3:.0f} g; grate total {(V_land + V_web) * 8.94e-3:.0f} g (architecture 0.21 kg)")
txt = "\n".join(out)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "grate_cell.out"), "w").write(txt + "\n")
print(txt)
