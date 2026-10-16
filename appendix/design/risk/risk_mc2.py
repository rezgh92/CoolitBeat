#!/usr/bin/env python3
"""Extra Monte Carlo cases for risk-first-12mo: controlled-BLT paste, joint decisive-win probability,
hard-mode 100 cm2, and the effect of each fallback. Reuses risk_run definitions without re-running it."""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import synth_physics as sp

Q, LK = 15e3, 1.2
INERT = 2.75 + 2.0 + 0.4

def rfd(name, gap, fin, H, base, tim_R, lo, hi, lab, sc, hs=1.5):
    d = sp.Design(name, gap*1e-3, fin*1e-3, H*1e-3, 4e-3, base*1e-3, "hmmc", tim_R, lo, hi, lab, sc, hs, 0.0, 0.0)
    r = sp.evaluate(d, Q, LK); d.dp_visc_kPa = 0.10 + r["dp_ch_kPa"]; d.dp_inert_kPa = INERT
    return d

def mc(d, n=20000, seed=11, s_tim_override=None):
    rng = np.random.default_rng(seed)
    s_tim = s_tim_override if s_tim_override is not None else min(0.45, math.log(d.tim_hi/d.tim_R)/1.2816)
    tim = np.exp(rng.normal(0, s_tim, n)); hf = np.exp(rng.normal(0, 0.125, n)); bf = np.exp(rng.normal(0, 0.05, n))
    cf = np.exp(rng.normal(0, 0.025, n)); fh = np.exp(rng.normal(0, 0.2, n)); ts = np.exp(rng.normal(0, 0.2, n))
    dv = np.exp(rng.normal(0, 0.125, n)); di = np.exp(rng.normal(0, 0.225, n))
    a = np.empty(n); m = np.empty(n); dp = np.empty(n)
    for i in range(n):
        r = sp.evaluate(d, Q, LK, dict(h=hf[i], tim=tim[i], base=bf[i], cal=cf[i], flow_hs=fh[i], tim_sc=ts[i], dp_visc=dv[i], dp_inert=di[i]))
        a[i], m[i], dp[i] = r["dT_avg"], r["dT_max"], r["dp_kPa"]
    return a, m, dp

cases = [
    ("RF-15 paste 0.07, uncontrolled BLT (sigma 0.45)", rfd("p", .15, .15, 2, 1, .07, .04, .17, "paste", 3.5), None),
    ("RF-15 paste 0.06, controlled + measured BLT (sigma 0.20)", rfd("p", .15, .15, 2, 1, .06, .045, .075, "paste", 2.5), 0.20),
    ("RF-15 PCM 0.055", rfd("c", .15, .15, 2, 1, .055, .04, .08, "PCM", 1.5), None),
    ("RF-15 PCM, conservative flow +/-20 % (hs 2.3)", rfd("c", .15, .15, 2, 1, .055, .04, .08, "PCM", 1.5, hs=2.3), None),
    ("F1 base 1.5 mm, PCM", rfd("f1", .15, .15, 2, 1.5, .055, .04, .08, "PCM", 1.5), None),
    ("F1 base 1.5 mm, paste 0.07", rfd("f1p", .15, .15, 2, 1.5, .07, .04, .17, "paste", 3.5), None),
]
print("| case | avg P10/P50/P90 | max P10/P50/P90 | P(avg<34.4) | P(max<44.2) | P(both) | P(avg<=31 & max<=35.4) | P(dP<=10) |")
print("|---|---|---|---:|---:|---:|---:|---:|")
for lab, d, s in cases:
    a, m, dp = mc(d, s_tim_override=s)
    pa = np.percentile(a, [10, 50, 90]); pm = np.percentile(m, [10, 50, 90])
    print(f"| {lab} | {pa[0]:.1f}/{pa[1]:.1f}/{pa[2]:.1f} | {pm[0]:.1f}/{pm[1]:.1f}/{pm[2]:.1f} | {np.mean(a<34.4):.2f} | "
          f"{np.mean(m<44.2):.2f} | {np.mean((a<34.4)&(m<44.2)):.2f} | {np.mean((a<=31.0)&(m<=35.4)):.2f} | {np.mean(dp<=10):.3f} |")

# hard mode 100 cm2
sp.A_FP = 100e-4; sp.SIDE = math.sqrt(sp.A_FP)
print("\nHard-mode 100 cm2:")
for lab, d, s in cases[:3]:
    a, m, dp = mc(d, s_tim_override=s)
    print(f"- {lab}: avg P50 {np.median(a):.1f} (P90 {np.percentile(a,90):.1f}), max P50 {np.median(m):.1f} (P90 {np.percentile(m,90):.1f}); "
          f"P(avg<34.4) {np.mean(a<34.4):.2f}, P(max<44.2) {np.mean(m<44.2):.2f}")
