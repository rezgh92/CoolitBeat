#!/usr/bin/env python3
"""
risk_run.py - numbers for the risk-first-12mo proposal ("R12 / RiskFirst plate").

Geometry of record (risk-first subset of HMMC):
  core   : skived OFE Cu, gap 0.15 mm, fin 0.15 mm (pitch 0.30), H 2.0 mm  -> "RF-15"
           same-lot hedge variant gap 0.15 / fin 0.10 / H 2.0 (physics core of record) -> "RF-10"
  base   : 1.0 mm finished (0.8 min under die), tied sandwich via vacuum-brazed lands (89 % of fin-tip length bonded)
  flow   : 4 mm flow length (inlet slit -> outlet slit), 14 inlet + 14 outlet slits at 8 mm inlet pitch
  meter  : 0.30 mm continuous inlet window slit (distributed meter, ~1.6 kPa) + 0.60 mm outlet slit (~0.4 kPa)
  L2     : 3.0 x 9 mm plenums (1.0 mm walls), fed near mid-length (CC, +/-14 mm offset); L1 headers 20x10 / 24x12 mm
  ports  : 2 x 16 mm bore, centre top; integrated 50 um absolute screen (0.4 kPa clean)

Two models are used, both unchanged from the project:
  (1) docs/cooling/model/coldplate_model.py  (deterministic, term budget)
  (2) appendix/physics/SYNTHESIS-physics.py (same physics + Monte Carlo bands, Q capacity)
Run: python3 risk_run.py > risk_run.out
"""
from __future__ import annotations

import importlib.util
import math
import os
import sys
from dataclasses import replace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import coldplate_model as cm  # noqa: E402  (copy of docs/cooling/model/coldplate_model.py)

import synth_physics as sp  # noqa: E402  (copy of appendix/physics/SYNTHESIS-physics.py)

Q, LK = 15000.0, 1.2
A0 = 117.0

# ------------------------------------------------------------------------------------------------
# (1) project scoping model
# ------------------------------------------------------------------------------------------------
WINDOW_KPA = 2.0    # inlet 0.30 mm slit (~1.6) + outlet 0.60 mm slit (~0.4) at 18 LPM, inertial
SCREEN_KPA = 0.4    # 50 um abs pleated screen, >= 10 cm2, clean (fouling-filtration sec. 3)


def rf(footprint, *, gap=0.15, fin=0.15, H=2.0, base=1.0, tim="PCM pad", hs=1.5, name=None):
    side = math.sqrt(footprint) * 10
    n_slots = max(1, int(round(side / 8.0)))
    return cm.ColdPlate(
        name=name or f"RF gap{gap}/fin{fin}x{H} base{base} ({tim})",
        footprint_cm2=footprint, fin_t_mm=fin, gap_mm=gap, fin_h_mm=H, flow_len_mm=4.0,
        base_mm=base, tim=tim, isothermal_cell=True, hotspot_flow_K=hs,
        n_parallel_paths=2 * n_slots, slot_w_mm=3.0, K_channel=3.0, K_slot=1.5,
        header_u_m_s=0.8, K_header=1.0, port_bore_mm=16.0, K_port=2.3,
        orifice_dp_kPa_18=WINDOW_KPA + SCREEN_KPA)


def row(r):
    return (f"| {r['name']:<58} | {r['q_W_cm2']:4.0f} | {r['dT_cal']:4.1f} | {r['dT_tim']:4.1f} | {r['dT_base']:4.1f} | "
            f"{r['dT_conv']:4.1f} | **{r['dT_avg']:4.1f}** | {r['dT_max']:4.1f} | {r['R_unit_cm2K_W']:.3f} | "
            f"{r['h_eff']/1e3:4.0f} | {r['dp_total_kPa']:4.1f} | {r['pump_W']:4.1f} | {r['Q_cap_kW']:4.1f} |")


HDR = ("| design | W/cm2 | cal | TIM | base | conv | avg dT | max dT | R'' | h_eff | dP kPa | pump W | Qcap kW |\n"
       "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

print("# risk-first-12mo: model runs\n")
print("## A. Project scoping model, 15 kW / 18 LPM PG25 / 45 C / 117 cm2\n")
print(HDR)
rows = [
    cm.coolit_like(A0),
    rf(A0, tim="paste 0.07", name="RF-15 like-for-like, paste 0.07"),
    rf(A0, tim="paste thin-BLT", name="RF-15 named paste at 25 um BLT, 0.05"),
    rf(A0, tim="PCM pad", name="RF-15 PCM pad (OCP-reference TIM) [Tier 1]"),
    rf(A0, tim="liquid metal", name="RF-15 liquid metal on Ni [Tier 2, stretch]"),
    rf(A0, fin=0.10, tim="paste 0.07", name="RF-10 (fin 0.10) paste 0.07"),
    rf(A0, fin=0.10, tim="PCM pad", name="RF-10 (fin 0.10) PCM"),
    rf(A0, base=1.5, tim="paste 0.07", name="Fallback F1: base 1.5 mm, paste"),
    rf(A0, base=1.5, tim="PCM pad", name="Fallback F1: base 1.5 mm, PCM"),
    rf(A0, base=2.0, tim="paste 0.07", hs=2.3, name="Fallback F2: base 2.0, +/-20% flow, paste"),
    rf(A0, base=2.0, tim="PCM pad", hs=2.3, name="Fallback F2: base 2.0, +/-20% flow, PCM"),
    rf(A0, H=3.0, tim="PCM pad", name="Upside U1: fin height 3.0 mm, PCM"),
]
res = {}
for v in rows:
    r = v.evaluate(Q, LK)
    res[v.name] = r
    print(row(r))
r1 = rf(A0, tim="PCM pad").evaluate(Q, LK)
print(f"\nRF-15 PCM detail: NTU {r1['NTU']:.2f}, cal frac {r1['cal_frac']:.2f}, h {r1['h']/1e3:.1f} kW/m2K, eta {r1['eta']:.2f}, "
      f"h_eff {r1['h_eff']/1e3:.0f}, channel u {r1['u_ch']:.3f} m/s Re {r1['Re']:.0f}, port u {r1['u_port']:.2f} m/s; "
      f"dP: ch {r1['dp_ch_kPa']:.2f} + turns {r1['dp_K_kPa']:.2f} + slot {r1['dp_slot_kPa']:.2f} + header {r1['dp_header_kPa']:.2f} "
      f"+ window+screen {r1['dp_orif_kPa']:.2f} + ports {r1['dp_port_kPa']:.2f} = {r1['dp_total_kPa']:.2f} kPa")

# window-slit check (hand calc, documented in proposal)
rho = 1005.0
q_slot = 18.0 / 14 / 60000             # m3/s per inlet slit
n_ch = 108.0 / 0.30                    # channels across 108 mm (RF-15)
a_win = n_ch * 2 * 0.15e-3 * 0.15e-3   # per inlet slit: gap x half-slit x 2 directions
u_win = q_slot / a_win
a_slit = 0.30e-3 * 0.108
u_slit = q_slot / a_slit
dp_in = 2.0 * 0.5 * rho * u_win**2
a_win_o = n_ch * 2 * 0.15e-3 * 0.30e-3
u_win_o = q_slot / a_win_o
dp_out = 2.0 * 0.5 * rho * u_win_o**2
u_plen = (q_slot * 68.0 / 108.0) / (3.0e-3 * 9e-3)   # long half of an offset-fed plenum
dyn_plen = 0.5 * rho * u_plen**2
u_hdr = (18.0 / 2 / 60000) / (20e-3 * 10e-3)
dyn_hdr = 0.5 * rho * u_hdr**2
branch = dp_in + dp_out + r1["dp_ch_kPa"] * 1e3
print(f"\nWindow check: per inlet slit {q_slot*6e4:.3f} LPM; slit u {u_slit:.2f} m/s; fin-gap entry u {u_win:.2f} m/s -> "
      f"{dp_in/1e3:.2f} kPa (K=2); outlet {u_win_o:.2f} m/s -> {dp_out/1e3:.2f} kPa; branch {branch/1e3:.2f} kPa. "
      f"Plenum 3.0x9 offset-fed (long half) u {u_plen:.2f} m/s dyn {dyn_plen:.0f} Pa -> ratio {branch/dyn_plen:.0f} (rule >= 15). "
      f"L1 inlet header 20x10 mm mid-fed u {u_hdr:.2f} m/s dyn {dyn_hdr:.0f} Pa -> ratio {branch/dyn_hdr:.1f} (rule >= 6).")
# tie stress
for gap, fin in ((0.15, 0.15), (0.15, 0.10)):
    pitch = gap + fin
    f_bond = (8 - 0.30 - 0.60) / 8
    for p in (0.69, 2.0, 4.5):
        s = p * pitch / (fin * f_bond)
        print(f"Tie stress gap {gap}/fin {fin}, bonded {f_bond:.2f}, p {p} MPa: nominal {s:.1f} MPa, Kt2.5 {2.5*s:.1f} MPa (annealed yield 70)")

edge = replace(cm.coolit_like(A0), name="Edge-fed skived reference (rig proxy)", n_parallel_paths=1, flow_len_mm=108.0, hotspot_flow_K=9.5)
re_ = edge.evaluate(Q, LK)
print(f"Edge-fed single-pass skived reference 0.2/0.2x4, 2 mm base, paste (rig proxy, no central slot): avg {re_['dT_avg']:.1f} K, "
      f"max ~{re_['dT_max']:.1f} K (hot-spot assumed 9.5 K), dP {re_['dp_total_kPa']:.0f} kPa")

print("\n## B. Flow sweep (117 cm2, 15 kW): CoolIT-like paste vs RF-15 paste / PCM / LM\n")
print("| LPM/kW | LPM | CoolIT avg/max | dP | RF-15 paste avg/max | RF-15 PCM avg/max | RF-15 LM avg/max | RF dP kPa | RF pump W |")
print("|---:|---:|---|---:|---|---|---|---:|---:|")
for lk in (0.6, 0.75, 1.0, 1.2, 1.5, 2.0, 2.4):
    a = cm.coolit_like(A0).evaluate(Q, lk)
    b = rf(A0, tim="paste 0.07").evaluate(Q, lk)
    c = rf(A0, tim="PCM pad").evaluate(Q, lk)
    d = rf(A0, tim="liquid metal").evaluate(Q, lk)
    print(f"| {lk:.2f} | {a['flow_lpm']:.1f} | {a['dT_avg']:.1f} / {a['dT_max']:.1f} | {a['dp_total_kPa']:.1f} | "
          f"{b['dT_avg']:.1f} / {b['dT_max']:.1f} | {c['dT_avg']:.1f} / {c['dT_max']:.1f} | {d['dT_avg']:.1f} / {d['dT_max']:.1f} | "
          f"{c['dp_total_kPa']:.1f} | {c['pump_W']:.2f} |")

# flow to match CoolIT 34.4 avg
from scipy.optimize import brentq  # noqa: E402
for tim in ("paste 0.07", "PCM pad", "liquid metal"):
    lk = brentq(lambda x: rf(A0, tim=tim).evaluate(Q, x)["dT_avg"] - 34.4, 0.2, 3.0)
    lkm = brentq(lambda x: rf(A0, tim=tim).evaluate(Q, x)["dT_max"] - 44.2, 0.1, 3.0)
    print(f"Flow to match 34.4 K avg with {tim}: {lk:.2f} LPM/kW = {lk*15:.1f} LPM; to match 44.2 K max: {lkm:.2f} LPM/kW = {lkm*15:.1f} LPM")

print("\n## C. Hard-mode footprint 100 cm2 (150 W/cm2) and soft 145 cm2, 15 kW 18 LPM\n")
print(HDR)
for A in (100.0, 145.0):
    for v in (cm.coolit_like(A), rf(A, tim="paste 0.07", name=f"RF-15 paste ({A:.0f} cm2)"),
              rf(A, tim="PCM pad", name=f"RF-15 PCM ({A:.0f} cm2)")):
        print(row(v.evaluate(Q, LK)))

print("\n## D. GPU-class plates (uniform TTV, 1.2 LPM/kW) - where it does NOT win on average\n")
print(HDR)
for Qk, A in ((1.4, 45), (2.3, 60), (3.6, 80)):
    for v in (cm.coolit_like(A), rf(A, tim="PCM pad", name=f"RF-15 PCM {Qk} kW {A} cm2"),
              rf(A, tim="liquid metal", name=f"RF-15 LM {Qk} kW {A} cm2")):
        print(row(v.evaluate(Qk * 1e3, LK)))

print("\n## D2. Die-zone (zoned) indicative 1-D: die area only, die-zone flow = 88 % of package flow at 1.2 LPM/kW\n")
print(HDR)
for label, Qpkg, frac_die, A_die in (("B300-class 1.4 kW, 2 dies 16 cm2", 1400, 0.90, 16.0),
                                      ("Rubin-class 2.3 kW, 2 dies 16.6 cm2", 2300, 0.90, 16.6),
                                      ("Rubin-Ultra-class 3.6 kW, 4 dies 33 cm2", 3600, 0.93, 33.0)):
    Qd = Qpkg * frac_die
    lpm_zone = 0.88 * 1.2 * Qpkg / 1000
    lk_zone = lpm_zone / (Qd / 1000)
    for v in (replace(cm.coolit_like(A_die), name=f"CoolIT-like {label}"),
              rf(A_die, tim="PCM pad", name=f"RF-15 PCM {label}"),
              rf(A_die, tim="liquid metal", name=f"RF-15 LM {label}")):
        r = v.evaluate(Qd, lk_zone)
        print(row(r))

# ------------------------------------------------------------------------------------------------
# (2) physics synthesis model with Monte Carlo bands and win probabilities
# ------------------------------------------------------------------------------------------------
print("\n## E. Physics-synthesis model + Monte Carlo (20k), RF geometry with window metering\n")
INERT = 2.75 + WINDOW_KPA + SCREEN_KPA   # design-H ports+manifold, window meter, screen


def rfd(name, gap, fin, H, base, tim_R, lo, hi, lab, sc, hs=1.5):
    d = sp.Design(name, gap * 1e-3, fin * 1e-3, H * 1e-3, 4e-3, base * 1e-3, "hmmc", tim_R, lo, hi, lab, sc, hs,
                  0.0, 0.0)
    r = sp.evaluate(d, Q, LK)
    d.dp_visc_kPa = 0.10 + r["dp_ch_kPa"]
    d.dp_inert_kPa = INERT
    return d


DES = [
    sp.COOLIT,
    rfd("RF-15 paste 0.07 (like-for-like)", 0.15, 0.15, 2.0, 1.0, 0.07, 0.04, 0.17, "paste", 3.5),
    rfd("RF-15 PCM 0.055 (Tier 1)", 0.15, 0.15, 2.0, 1.0, 0.055, 0.04, 0.08, "PCM", 1.5),
    rfd("RF-15 LM 0.015 (Tier 2)", 0.15, 0.15, 2.0, 1.0, 0.015, 0.005, 0.03, "LM", 0.6),
    rfd("RF-10 PCM 0.055", 0.15, 0.10, 2.0, 1.0, 0.055, 0.04, 0.08, "PCM", 1.5),
    rfd("F2 fallback base 2.0, +/-20 %, paste", 0.15, 0.15, 2.0, 2.0, 0.07, 0.04, 0.17, "paste", 3.5, hs=2.3),
    rfd("F2 fallback base 2.0, +/-20 %, PCM", 0.15, 0.15, 2.0, 2.0, 0.055, 0.04, 0.08, "PCM", 1.5, hs=2.3),
]

print("| design | avg dT P10/P50/P90 | max dT P10/P50/P90 | dP kPa P50 (P90) | pump W | Qcap kW P10/P50/P90 | "
      "P(avg<34.4) | P(max<44.2) | P(avg<=31.0) | P(max<=35.4) |")
print("|---|---|---|---|---|---|---:|---:|---:|---:|")


def mc_full(d, n=20000, seed=7):
    rng = np.random.default_rng(seed)
    s_tim = min(0.45, math.log(d.tim_hi / d.tim_R) / 1.2816)
    tim = np.exp(rng.normal(0, s_tim, n))
    hf = np.exp(rng.normal(0, 0.125, n))
    bf = np.exp(rng.normal(0, 0.05, n))
    cf = np.exp(rng.normal(0, 0.025, n))
    fh = np.exp(rng.normal(0, 0.2, n))
    ts = np.exp(rng.normal(0, 0.2, n))
    dv = np.exp(rng.normal(0, 0.125, n))
    di = np.exp(rng.normal(0, 0.225, n))
    avg = np.empty(n); mx = np.empty(n); dp = np.empty(n); pw = np.empty(n)
    for i in range(n):
        pert = dict(h=hf[i], tim=tim[i], base=bf[i], cal=cf[i], flow_hs=fh[i], tim_sc=ts[i], dp_visc=dv[i],
                    dp_inert=di[i])
        r = sp.evaluate(d, Q, LK, pert)
        avg[i], mx[i], dp[i], pw[i] = r["dT_avg"], r["dT_max"], r["dp_kPa"], r["pump_W"]
    idx = rng.choice(n, 1500, replace=False)
    qc = []
    for i in idx:
        pert = dict(h=hf[i], tim=tim[i], base=bf[i], cal=cf[i], flow_hs=fh[i], tim_sc=ts[i], dp_visc=dv[i],
                    dp_inert=di[i])
        qc.append(sp.q_capacity(d, LK, pert))
    qc = np.array(qc)
    return avg, mx, dp, pw, qc


for d in DES:
    avg, mx, dp, pw, qc = mc_full(d)
    p = lambda a: np.percentile(a, [10, 50, 90])  # noqa: E731
    pa, pm, pd, pq = p(avg), p(mx), p(dp), np.nanpercentile(qc, [10, 50, 90])
    nom = sp.evaluate(d, Q, LK)
    print(f"| {d.name} (nominal {nom['dT_avg']:.1f}/{nom['dT_max']:.1f}) | {pa[0]:.1f}/{pa[1]:.1f}/{pa[2]:.1f} | "
          f"{pm[0]:.1f}/{pm[1]:.1f}/{pm[2]:.1f} | {pd[1]:.1f} ({pd[2]:.1f}) | {np.median(pw):.2f} | "
          f"{pq[0]:.1f}/{pq[1]:.1f}/{pq[2]:.1f} | {np.mean(avg<34.4):.3f} | {np.mean(mx<44.2):.3f} | "
          f"{np.mean(avg<=31.0):.3f} | {np.mean(mx<=35.4):.3f} |")

print("\nNominal term budgets (physics model):")
for d in DES:
    r = sp.evaluate(d, Q, LK)
    print(f"- {d.name}: cal {r['dT_cal']:.1f} + TIM {r['dT_tim']:.1f} + base {r['dT_base']:.1f} + conv {r['dT_conv']:.1f} "
          f"= {r['dT_avg']:.1f} K; hs flow {r['hs_flow']:.1f} + TIM {r['hs_tim']:.1f} -> max {r['dT_max']:.1f}; "
          f"h_eff {r['h_eff']/1e3:.0f} kW/m2K, NTU {r['NTU']:.2f}; dP {r['dp_kPa']:.1f} kPa, pump {r['pump_W']:.2f} W; "
          f"Qcap {sp.q_capacity(d, LK):.1f} kW; R {r['R_KW']*1e3:.2f} mK/W, R'' {r['R_unit']:.3f}")

print("\n2x flow (36 LPM, 2.4 LPM/kW) and equal pumping power:")
for d in DES[:4]:
    r2 = sp.evaluate(d, Q, 2.4)
    print(f"- {d.name}: 36 LPM avg {r2['dT_avg']:.1f} max {r2['dT_max']:.1f} dP {r2['dp_kPa']:.1f} kPa pump {r2['pump_W']:.1f} W")
for d in DES[1:4]:
    e = sp.equal_pump_power_point(d, Q)
    print(f"- equal pump power ({sp.evaluate(sp.COOLIT, Q, 1.2)['pump_W']:.1f} W) {d.name}: {e['lpm_per_kw']:.2f} LPM/kW "
          f"({e['flow_lpm']:.1f} LPM), dP {e['dp_kPa']:.1f} kPa, avg {e['dT_avg']:.1f} max {e['dT_max']:.1f}")

print("\nInlet headroom (inlet T at which Tcase,max = 85 C, 15 kW, 18 LPM):")
for d in DES[:4]:
    r = sp.evaluate(d, Q, LK)
    print(f"- {d.name}: {85 - r['dT_max']:.1f} C")

print("\n## F. Real 2027-28 package stress case (4 x 26x33 mm dies at 350 W/cm2 + 16 HBM, zoned), hottest die cell")
for lab, gap, fin, H in (("RF-15 robust", 0.15, 0.15, 2.0), ("RF-10", 0.15, 0.10, 2.0),
                         ("performance core 0.10/0.10x1.5 (die zone only, <= 33 um loops)", 0.10, 0.10, 1.5)):
    d = rfd(lab, gap, fin, H, 1.0, 0.055, 0.04, 0.08, "PCM", 1.5)
    h = sp.evaluate(d, Q, LK)["h_eff"] / 1e3
    out = [f"{tim}: {sp.die_max_dT(h, R):.1f} K ({45 + sp.die_max_dT(h, R):.0f} C)" for tim, R in
           (("paste 0.05", 0.05), ("PCM 0.055", 0.055), ("LM 0.015", 0.015))]
    print(f"- {lab} (h_eff {h:.0f}): " + "; ".join(out))
print("- CoolIT-like split-flow (report): 88.6 K paste 0.07 (134 C), ~76 K LM (121 C)")

# hard-mode MC: footprint 100 cm2
print("\n## G. Hard-mode 100 cm2 footprint, physics model, nominal")
sp.A_FP = 100e-4
sp.SIDE = math.sqrt(sp.A_FP)
for d in DES[:4]:
    r = sp.evaluate(d, Q, LK)
    print(f"- {d.name} at 100 cm2: avg {r['dT_avg']:.1f} max {r['dT_max']:.1f}")
sp.A_FP = 117e-4
sp.SIDE = math.sqrt(sp.A_FP)
