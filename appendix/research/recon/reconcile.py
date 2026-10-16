#!/usr/bin/env python3
"""Reconcile the three internal hydraulic reconstructions and size the loop (UQD/hose/barb) losses.
Run from anywhere:  python3 -I reconcile.py
"""
import sys, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coldplate_model_v2 as v2

RHO, MU, CP = 1005.0, 1.25e-3, 3930.0      # PG25 ~50 C (model values)
LPM = 1 / 60 / 1000

print("=" * 100)
print("A. Darcy / Fanning identity check")
print("=" * 100)
# Hagen-Poiseuille: dp = 32 mu u L / D^2 ; Fanning fRe = 16 (circular), Darcy fRe = 64
mu, u, L, D = 1.25e-3, 0.5, 0.05, 0.4e-3
hp = 32 * mu * u * L / D**2
fan_correct = 2 * 16 * mu * u * L / D**2          # 2 (fRe)_F mu u L / Dh^2
darcy_correct = 64 * mu * u * L / (2 * D**2)      # (fRe)_D mu u L / (2 Dh^2)
v1_form = 16 * mu * u * L / (2 * D**2)            # v1 model: (fRe)_F mu u L / (2 Dh^2)
print(f"Hagen-Poiseuille {hp:.1f} Pa | 2*fRe_F*mu*u*L/Dh^2 {fan_correct:.1f} | fRe_D*mu*u*L/(2Dh^2) {darcy_correct:.1f} | v1 formula {v1_form:.1f} -> v1/true = {v1_form/hp:.2f}")
# Shah & London polynomial at alpha=1 and alpha->0
poly = lambda a: (1 - 1.3553*a + 1.9467*a**2 - 1.7012*a**3 + 0.9564*a**4 - 0.2537*a**5)
print(f"24*poly(1) = {24*poly(1):.2f} (square duct Fanning fRe = 14.23 -> Darcy 56.9) ; 24*poly(0) = {24*poly(0):.1f} (parallel plates Fanning 24 -> Darcy 96)")
print(f"Shah&London alpha=0.05 (0.2 x 4 mm): Fanning fRe = {24*poly(0.05):.2f}, Darcy {96*poly(0.05):.1f}")
print()

print("=" * 100)
print("B. The CoolIT-like 0.2/0.2 x 4 mm, 54 mm split-flow reconstruction at 18 LPM: v1, v1+fix, hydraulic-detail, v2")
print("=" * 100)
Q, lk = 15000.0, 1.2
r2 = v2.coolit_like(117).evaluate(Q, lk)
# v1 (git 3a14c9f, read at session start): dp_ch = fRe mu u L/(2 Dh^2) [= v2/4]; K_channel 2.0 on u_ch; manifold K 2.0 on 1.2 m/s; ports flat 3.0 kPa
v1_ch = r2['dp_ch_kPa'] / 4; v1_K = r2['dp_K_kPa']; v1_man = 2.0 * 0.5 * RHO * 1.2**2 / 1e3; v1_port = 3.0
v1_total = v1_ch + v1_K + v1_man + v1_port
print(f"v1 (bug):      channel {v1_ch:.2f} + K_channel {v1_K:.2f} + manifold {v1_man:.2f} + ports(flat) {v1_port:.2f} = {v1_total:.2f} kPa   <- the '8.6 / ~9 kPa' quoted downstream")
fix_total = 4 * v1_ch + v1_K + v1_man + v1_port
print(f"v1 + 4x fix:   channel {4*v1_ch:.2f} + K_channel {v1_K:.2f} + manifold {v1_man:.2f} + ports(flat) {v1_port:.2f} = {fix_total:.2f} kPa   <- the '19 kPa' of manifold-maldistribution.md")
print(f"hydraulic-detail.md: channel fd+Hagenbach 14.71 + entry/exit 0.67 + plenums 3.41 + ports(flat) 3.00 = 21.78 kPa  <- the '22 kPa'")
print(f"v2 (on disk):  channel {r2['dp_ch_kPa']:.2f} + K_channel {r2['dp_K_kPa']:.2f} + header {r2['dp_header_kPa']:.2f} + ports(12 mm bore, K 2.3: u={r2['u_port']:.2f} m/s) {r2['dp_port_kPa']:.2f} = {r2['dp_total_kPa']:.2f} kPa  <- the '24.6 kPa' now in model_output.md")
print(f"   channel u = {r2['u_ch']:.3f} m/s, Re = {r2['Re']:.0f}; core-only (channel + K) = {r2['dp_ch_kPa']+r2['dp_K_kPa']:.1f} kPa in all three corrected versions")
print()
print("Pitch sensitivity of the skived core (v2 model, 117 cm2, 18 LPM): gap/fin/H -> channel term, total")
for g, t, H in [(0.25, 0.25, 4.0), (0.2, 0.2, 4.0), (0.15, 0.15, 3.0), (0.15, 0.10, 2.0), (0.10, 0.10, 2.0), (0.10, 0.15, 2.0)]:
    from dataclasses import replace
    p = replace(v2.coolit_like(117), gap_mm=g, fin_t_mm=t, fin_h_mm=H)
    r = p.evaluate(Q, lk)
    print(f"  {g:.2f}/{t:.2f} x {H:.1f} mm: u {r['u_ch']:.2f} m/s, channel {r['dp_ch_kPa']:5.1f} kPa, total {r['dp_total_kPa']:5.1f} kPa, avg dT {r['dT_avg']:.1f} K")
print()

print("=" * 100)
print("C. HMMC variants at 18 LPM: v1 (6.2), hydraulic-detail (8.3-8.6), manifold design H (5.0), v2 HMMC-R (5.3)")
print("=" * 100)
from dataclasses import replace
side = math.sqrt(117) * 10; n_slots = int(round(side / 4.0))
h1p = v2.ColdPlate(name="v1 HMMC emul", footprint_cm2=117, fin_t_mm=0.1, gap_mm=0.1, fin_h_mm=1.0, flow_len_mm=2.0, base_mm=1.0,
                   tim="paste thin-BLT", isothermal_cell=False, n_parallel_paths=2 * n_slots, slot_w_mm=0.3, K_channel=3.0, K_slot=1.5,
                   header_u_m_s=1.0, K_header=4.0, port_bore_mm=1000.0, K_port=0.0)
h1 = h1p.evaluate(Q, lk)
h1_total = h1['dp_ch_kPa'] / 4 + h1['dp_K_kPa'] + h1['dp_slot_kPa'] + h1['dp_header_kPa'] + 4.0
print(f"v1 HMMC 0.1/0.1x1.0, L=2 mm, 0.3 mm slots: channel {h1['dp_ch_kPa']/4:.2f} (bug; true {h1['dp_ch_kPa']:.2f}) + K {h1['dp_K_kPa']:.2f} + slot {h1['dp_slot_kPa']:.2f} + manifold {h1['dp_header_kPa']:.2f} + ports(flat) 4.00 = {h1_total:.2f} kPa (bug-free {h1_total + 0.75*h1['dp_ch_kPa']:.2f})")
for core in ["R", "P", "F"]:
    h2 = v2.hmmc(117, core=core).evaluate(Q, lk)
    print(f"v2 HMMC-{core} (design H, L=4 mm, 3.5 mm slots, 16 mm ports): channel {h2['dp_ch_kPa']:.2f} + K {h2['dp_K_kPa']:.2f} + slot {h2['dp_slot_kPa']:.2f} + header {h2['dp_header_kPa']:.2f} + orifice {h2['dp_orif_kPa']:.2f} + ports(u={h2['u_port']:.2f} m/s) {h2['dp_port_kPa']:.2f} = {h2['dp_total_kPa']:.2f} kPa ; u_ch {h2['u_ch']:.3f} m/s")
print("hydraulic-detail HMMC 0.1x1.0 L2: ports 3.00 + L1 2.17 + L2 1.81 + nozzles 0.13 + entry 0.51 + channel 0.33 + exit 0.38 = 8.35 kPa (0.2 mm slot/8 mm L2 variant 8.6)")
print("manifold-maldistribution design H: ports 2.53 + L1 net -0.19 + tees 0.24 + L2 net 0.11 + L3 friction 2.22 + L3 turns 0.06 = 4.99 kPa (no UQD)")
print()
print("Flow-length sensitivity of the channel friction term (v2 HMMC-R, 18 LPM):")
for Lf in [2.0, 3.0, 4.0, 6.0]:
    side = math.sqrt(117) * 10
    n_slots = max(1, int(round(side / (2 * Lf))))
    p = replace(v2.hmmc(117), flow_len_mm=Lf, n_parallel_paths=2 * n_slots)
    r = p.evaluate(Q, lk)
    print(f"  L = {Lf:.0f} mm ({n_slots} inlet slots): channel {r['dp_ch_kPa']:.2f} kPa, total {r['dp_total_kPa']:.2f} kPa, conv {r['dT_conv']:.1f} K, avg dT {r['dT_avg']:.1f} K")
print()

print("=" * 100)
print("D. Loop losses outside the plate at 15 kW: quick disconnects (Cv law), hose friction, barbs")
print("=" * 100)
SG = RHO / 1000.0
def dp_cv_kpa(lpm, cv):
    """Single mated coupling, dp[psi] = SG (gpm/Cv)^2."""
    return SG * (lpm / 3.785 / cv) ** 2 * 6.895
print(f"Cv law (SG {SG:.2f}): dp per mated coupling = SG*(Q[gpm]/Cv)^2 psi; a plate loop has TWO couplings (supply + return).")
cvs = [("UQD02 (1/8 in) Cv 0.2-0.3", 0.2, 0.3), ("UQD04 (1/4 in) Cv 0.5-0.8", 0.5, 0.8), ("UQD06 (3/8 in) Cv 1.3-2.0", 1.3, 2.0),
       ("UQD08 (1/2 in) Cv 3.0-4.0", 3.0, 4.0), ("UQDB08 blind-mate Cv 2.5-4.0", 2.5, 4.0), ("3/4 in / 'UQD12-class' Cv 6-10", 6.0, 10.0)]
flows = [6.0, 9.0, 11.25, 15.0, 18.0, 24.0, 36.0]
print("| coupling (Cv range, memory-based) | " + " | ".join(f"{q:g} LPM" for q in flows) + " |  (kPa for the PAIR = 2 couplings; hi-lo)")
for name, lo, hi in cvs:
    cells = []
    for q in flows:
        a, b = 2 * dp_cv_kpa(q, hi), 2 * dp_cv_kpa(q, lo)
        cells.append(f"{a:.0f}-{b:.0f}")
    print(f"| {name} | " + " | ".join(cells) + " |")
print()
print("Cross-check of the Cv ranges against a loss coefficient on the nominal flow bore (K per coupling = dp / (rho u^2/2)):")
for name, d_mm, cv in [("UQD04 1/4 in, bore ~5 mm", 5.0, 0.65), ("UQD06 3/8 in, bore ~8 mm", 8.0, 1.6), ("UQD08 1/2 in, bore ~10 mm", 10.0, 3.5), ("3/4 in, bore ~16 mm", 16.0, 8.0)]:
    A = math.pi / 4 * (d_mm * 1e-3) ** 2
    u = 18 * LPM / A
    dp1 = dp_cv_kpa(18, cv)
    K = dp1 * 1e3 / (0.5 * RHO * u * u)
    print(f"  {name}: u = {u:.1f} m/s at 18 LPM, dyn head {0.5*RHO*u*u/1e3:.1f} kPa, Cv {cv} -> {dp1:.1f} kPa per coupling -> K = {K:.1f} (valved QDs typically K 1-4 on bore)")
print()
print("Hose friction (smooth, Blasius turbulent / laminar 64/Re) per metre of hose, PG25 at 50 C:")
print("| hose ID | " + " | ".join(f"{q:g} LPM" for q in flows) + " |  (kPa/m ; velocity m/s at 18 LPM)")
for name, d_mm in [("1/4 in (6.4 mm)", 6.35), ("3/8 in (9.5 mm)", 9.5), ("1/2 in (12.7 mm)", 12.7), ("5/8 in (15.9 mm)", 15.9), ("3/4 in (19 mm)", 19.0)]:
    A = math.pi / 4 * (d_mm * 1e-3) ** 2
    cells = []
    for q in flows:
        u = q * LPM / A
        Re = RHO * u * d_mm * 1e-3 / MU
        f = 64 / Re if Re < 2300 else 0.316 * Re ** -0.25
        cells.append(f"{f / (d_mm*1e-3) * 0.5 * RHO * u * u / 1e3:.1f}")
    u18 = 18 * LPM / A
    print(f"| {name} | " + " | ".join(cells) + f" |  (u18 = {u18:.1f} m/s, Re18 = {RHO*u18*d_mm*1e-3/MU:.0f})")
print()
print("Barb / fitting losses (K = 1.0 per barb on the barb BORE velocity; bore is 2-3 mm under the hose ID):")
for name, bore in [("3/8 in barb, 7 mm bore", 7.0), ("1/2 in barb, 9.5 mm bore", 9.5), ("1/2 in full-bore stub, 12 mm", 12.0), ("5/8-3/4 in, 15 mm bore", 15.0)]:
    A = math.pi / 4 * (bore * 1e-3) ** 2
    out = []
    for q in [11.25, 15.0, 18.0]:
        u = q * LPM / A
        out.append(f"{q:g} LPM: {0.5*RHO*u*u/1e3:.1f} kPa each, x4 = {4*0.5*RHO*u*u/1e3:.0f}")
    print(f"  {name}: " + " | ".join(out))
print()

print("=" * 100)
print("E. Tray-loop budgets for ONE 15 kW plate (plate + 2 x 0.5 m hose + 4 barbs/stubs + QD pair), kPa")
print("=" * 100)
def hose_kpa(q, d_mm, Lm):
    A = math.pi / 4 * (d_mm * 1e-3) ** 2; u = q * LPM / A; Re = RHO * u * d_mm * 1e-3 / MU
    f = 64 / Re if Re < 2300 else 0.316 * Re ** -0.25
    return f / (d_mm * 1e-3) * 0.5 * RHO * u * u / 1e3 * Lm
def barb_kpa(q, bore_mm, n=4, K=1.0):
    A = math.pi / 4 * (bore_mm * 1e-3) ** 2; u = q * LPM / A
    return n * K * 0.5 * RHO * u * u / 1e3
plates = {"HMMC design H (5.3 model, claim 10)": (5.3, 10.0), "skived split-flow recon (24.6 model, window 17-42)": (24.6, 35.0)}
loops = [("3/8 in hose + 7 mm barbs + UQD06 pair (Cv 1.3-2.0)", 9.5, 7.0, 1.3, 2.0),
         ("1/2 in hose + 9.5 mm barbs + UQD08 pair (Cv 3-4)", 12.7, 9.5, 3.0, 4.0),
         ("1/2 in hose + 12 mm stubs + UQD08 pair (Cv 3-4)", 12.7, 12.0, 3.0, 4.0),
         ("1/2 in hose + 12 mm stubs + DUAL UQD08 pairs (half flow each)", 12.7, 12.0, 6.0, 8.0),
         ("3/4 in hose + 15 mm stubs + 3/4-in class pair (Cv 6-10)", 19.0, 15.0, 6.0, 10.0)]
for q, lkw in [(18.0, 1.2), (15.0, 1.0), (11.25, 0.75)]:
    print(f"\n-- {q:g} LPM ({lkw} LPM/kW) --")
    print("| loop | hose 1 m | barbs x4 | QD pair | plate (model / claim) | TOTAL (model-lo .. claim-hi) | <=100 | <=70 | <=50 | <=30 |")
    for lname, hd, bb, cvlo, cvhi in loops:
        hs = hose_kpa(q, hd, 1.0); br = barb_kpa(q, bb)
        qd_lo, qd_hi = 2 * dp_cv_kpa(q, cvhi), 2 * dp_cv_kpa(q, cvlo)
        if "DUAL" in lname:   # dual ports: half the flow per coupling and per barb set; hose shared
            qd_lo, qd_hi = 2 * dp_cv_kpa(q / 2, 4.0), 2 * dp_cv_kpa(q / 2, 3.0)
            br = barb_kpa(q / 2, bb)
        for pname, (pm, pc) in plates.items():
            scale = (q / 18.0) ** (1.3 if "skived" in pname else 1.8)
            lo = hs + br + qd_lo + pm * scale; hi = hs + br + qd_hi + pc * scale
            flags = " | ".join("yes" if hi <= lim else ("marginal" if lo <= lim else "no") for lim in (100, 70, 50, 30))
            print(f"| {lname} + {pname.split(' (')[0]} | {hs:.0f} | {br:.0f} | {qd_lo:.0f}-{qd_hi:.0f} | {pm*scale:.0f} / {pc*scale:.0f} | **{lo:.0f}..{hi:.0f}** | {flags} |")
print()
print("Hydraulic power of the QD pair alone at 18 LPM: UQD08 (25 kPa) = %.1f W ; UQD06 (75 kPa) = %.1f W ; vs plate HMMC 5 kPa = %.1f W" % (25e3*18*LPM, 75e3*18*LPM, 5e3*18*LPM))
print()
print("=" * 100)
print("F. What flow per QD pair do today's trays see? (secondary/KB; GB200 NVL72 ~120-132 kW rack, ~130 LPM, 18 compute + 9 switch trays)")
print("=" * 100)
for rack_lpm in [120, 130, 150]:
    per_ct = rack_lpm * 0.88 / 18    # ~88 % of flow to compute trays (KB assumption)
    print(f"  rack {rack_lpm} LPM -> ~{per_ct:.1f} LPM per compute tray through ONE QD pair; a single 15 kW plate at 1.2 LPM/kW is {18/per_ct:.1f}x that flow -> {(18/per_ct)**2:.0f}x the QD dP for the same coupling size")
