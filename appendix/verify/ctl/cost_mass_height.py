"""Cost, mass and height of the gap-closing packages on the SAME basis as verify/cost_market_check.py
(Sep-2026 Cu and Ag, Monte Carlo triangular inputs, 100k/yr per SKU, mature yield + overhead).
C0 = PRISM-15 as drafted (verifier-corrected). C1 = PKG-A lean drop-in. C2 = C1 + silver-free Cu-Sn TLP (route C) in a
continuous atmosphere belt furnace (E1-gated). C3 = PKG-B (R+ 0.12 mm core, L6). Incumbent = like-sized CoolIT-15 class."""
import numpy as np
rng = np.random.default_rng(7); N = 200_000
tri = lambda lo, mid, hi: rng.triangular(lo, mid, hi, N)
pct = lambda x: np.percentile(x, [10, 50, 90])
RHO = 8.94
lme = tri(14.4, 14.6, 15.0); ofe = tri(2.5, 4.0, 7.0); scrapf = tri(0.80, 0.88, 0.95); ag = tri(60, 65, 72)
def copper(parts):
    buy = sum(b for b, f in parts.values()); fin = sum(f for b, f in parts.values())
    bk = buy * tri(0.92, 1.0, 1.10)
    return bk * (lme + ofe) - (bk - fin) * lme * scrapf, buy, fin
strip = 13.5 * 13.0  # cm2 of strip per 125 mm stamped part
# ---- part lists (buy kg, finished kg) ----
P0 = {"base+fins": (13.5 * 14.0 * 0.27 * RHO / 1000, 0.27), "grate 1.0": (strip * 0.10 * RHO / 1000, 0.11),
      "meter 0.4": (strip * 0.04 * RHO / 1000, 0.05), "2 laminations 4.5": (strip * 0.90 * RHO / 1000, 0.55),
      "separator 1.5": (strip * 0.15 * RHO / 1000, 0.21), "bar (forged)": (0.41 / 0.70, 0.41)}
P1 = {"base+fins (0.8 base)": (13.5 * 14.0 * 0.27 * RHO / 1000, 0.25), "metered grate 1.7": (strip * 0.17 * RHO / 1000, 0.21),
      "folded plenum 0.8 + end frame": (0.137 * 1.08 + 0.047 * 1.6, 0.18), "separator 1.5": (strip * 0.15 * RHO / 1000, 0.20),
      "arched cap 1.0 + 2 bosses": (strip * 0.10 * 1.15 * RHO / 1000 + 0.07, 0.18)}
def filler_routeAB(land):
    bag8_g = land * 25e-4 * 10.0; routeA = bag8_g * 0.72 / 31.1035 * ag + tri(2, 4, 8) + 1.0
    routeB = land * 5e-4 * 10.49 / 31.1035 * ag * tri(1.2, 1.6, 2.5) + tri(3, 6, 12) + 1.0
    return 0.5 * routeA + 0.5 * routeB
def braze_vac(per_load, cycle_h, assy_min):
    furn = (100_000 / per_load) * cycle_h / 7000
    return (furn * tri(0.8e6, 1.4e6, 2.2e6) * 0.21 / 100_000 + (tri(600, 900, 1300) * 0.11 + tri(20, 40, 80)) / per_load
            + tri(2, 5, 10) + assy_min * tri(0.5, 0.8, 1.2)), furn
common = dict(flycut=tri(4, 5, 8), stubs=tri(6, 8, 11), hw=tri(10, 14, 18), test=tri(7, 10, 14))
res = {}
# C0 (verifier-corrected draft)
cu0, b0, f0 = copper(P0)
br0, fu0 = braze_vac(tri(30, 50, 80), tri(6, 8, 11), tri(4, 7, 12))
d0 = dict(copper=cu0, skive=tri(14, 20, 28), kerf=tri(2, 3, 6), stampings=tri(4, 6, 9), plenum=tri(4, 7, 12), header=tri(10, 14, 20),
          filler=filler_routeAB(tri(330, 410, 480)), braze=br0, dies=tri(0.4e6, 0.65e6, 1.0e6) / 3e5, **common)
y0 = tri(0.88, 0.93, 0.97); ov = tri(0.08, 0.12, 0.16)
res["C0 draft (verifier basis)"] = (d0, y0, b0, f0, fu0)
# C1 lean drop-in: merged metered grate, folded plenum, arched drawn cap, 15 lines instead of 19, lighter/thinner stack
cu1, b1, f1 = copper(P1)
br1, fu1 = braze_vac(tri(30, 50, 80) * 1.3, tri(6, 8, 11) * 0.9, tri(3, 5.5, 9))
d1 = dict(copper=cu1, skive=tri(14, 20, 28), kerf=tri(2, 3, 6) * 15 / 19, stampings=tri(4.5, 6.5, 9.5), plenum=tri(2.5, 4, 7),
          header=tri(3, 5, 8), filler=filler_routeAB(tri(330, 410, 480) * 0.68), braze=br1, dies=tri(0.35e6, 0.55e6, 0.9e6) / 3e5, **common)
y1 = tri(0.89, 0.94, 0.97)
res["C1 PKG-A lean drop-in"] = (d1, y1, b1, f1, fu1)
# C2 = C1 + route C (masked electroplated Sn, Cu-Sn TLP, no silver) in a continuous N2/H2 belt furnace
d2 = dict(d1); d2["filler"] = tri(2, 4, 7); d2["braze"] = tri(5, 8, 13)
res["C2 PKG-A + silver-free belt braze (E1-gated)"] = (d2, tri(0.87, 0.93, 0.96), b1, f1, None)
# C3 = PKG-B: R+ 0.12/0.12 x 1.8 core (+25 % skive strokes), L6 -> 19 lines
d3 = dict(d1); d3["skive"] = tri(14, 20, 28) * 1.22; d3["kerf"] = tri(2, 3, 6); d3["stampings"] = tri(4.5, 7, 10)
res["C3 PKG-B R+ core"] = (d3, y1, b1, f1, fu1)
gb = tri(95, 110, 130); inc = gb + tri(8, 14, 22)
print("| line (US$ at 100k/yr, P50) | " + " | ".join(res) + " |"); print("|---" * (len(res) + 1) + "|")
for k in d0:
    print(f"| {k} | " + " | ".join(f"{np.median(v[0][k]):.1f}" for v in res.values()) + " |")
tot = {}
for lab, (d, y, b, f, fu) in res.items():
    tot[lab] = sum(d.values()) / y * (1 + ov)
print("| **factory cost P10/P50/P90** | " + " | ".join("/".join(f"{x:.0f}" for x in pct(t)) for t in tot.values()) + " |")
print("| copper buy / finished kg | " + " | ".join(f"{v[2]:.2f} / {v[3]:.2f}" for v in res.values()) + " |")
print("| vacuum furnaces per 100k/yr (P50) | " + " | ".join(f"{np.median(v[4]):.1f}" if v[4] is not None else "belt" for v in res.values()) + " |")
print(f"\nIncumbent like-sized CoolIT-15 class P10/50/90: {'/'.join(f'{x:.0f}' for x in pct(inc))}")
for lab, t in tot.items():
    pr = t / inc - 1
    print(f"{lab}: premium vs like-sized incumbent P10/50/90 {'/'.join(f'{x*100:+.0f}%' for x in pct(pr))}; P(cost <= incumbent) {np.mean(t <= inc):.2f}")
# $/kW of Tcase-limited capacity (85 C case, 45 C inlet, 1.2 LPM/kW): own-penalty capacities from lean_pkg.out
cap = {"C0 draft (verifier basis)": (15.8, 18.5), "C1 PKG-A lean drop-in": (15.9, 18.8),
       "C2 PKG-A + silver-free belt braze (E1-gated)": (15.9, 18.8), "C3 PKG-B R+ core": (17.5, None)}
print("\nUS$ per kW of capacity (P50 cost / capacity): CoolIT-15 paste %.2f, PCM %.2f" % (np.median(inc) / 12.9, np.median(inc) / 14.8))
for lab, (cp, cc) in cap.items():
    s = f"{lab}: paste {np.median(tot[lab]) / cp:.2f} ({(np.median(tot[lab]) / cp) / (np.median(inc) / 12.9) - 1:+.0%})"
    if cc: s += f"; PCM {np.median(tot[lab]) / cc:.2f} ({(np.median(tot[lab]) / cc) / (np.median(inc) / 14.8) - 1:+.0%})"
    print(s)
