#!/usr/bin/env python3
"""
Advanced-manufacturing lens: does additive / advanced manufacturing earn a place in the cold-plate
architecture that has to beat the CoolIT 15 kW plate?

Built on the project scoping model (docs/cooling/model/coldplate_model.py, corrections of
SYNTHESIS-physics.md already in it). This script adds, without changing the model:
  * separate fin conductivity (printed copper is not wrought copper),
  * multi-layer bases (Cu-diamond, CVD-diamond inserts, vapor-chamber base) with interface resistances,
  * Nusselt and friction multipliers (TPMS mixing, offset-strip restarts, L-PBF roughness),
  * a fin-conduction ceiling for h_eff at a fixed (fouling-limited) channel gap,
  * a micro-pin-fin estimate,
  * the 350 W/cm2 reticle-die fit of SYNTHESIS-physics (dT = 33 + 3500/h_eff + 350 (R_TIM - 0.05)),
    re-based for base material,
  * Monte Carlo bands with the SYNTHESIS perturbation scheme,
  * a cost model for each route at 10k and 100k plates/yr (basis: manufacturing-cost.md, gap-cost-volume,
    proposal-hmmc-elite.md line items; KB-M/KB-L, to be confirmed by RFQ).
Run: python3 am_run.py > am_run.out
"""
from __future__ import annotations

import math
import sys
from dataclasses import replace

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
from coldplate_model import ColdPlate, PG25, TIM, K_CU, coolit_like, hmmc  # noqa: E402

A0 = 117.0           # cm2 calibrated TTV footprint
Q0 = 15000.0         # W
LK0 = 1.2            # LPM/kW
SCREEN_KPA_18 = 0.4  # integrated 50 um absolute screen, clean, at 18 LPM (scaled with flow^2)

K_ECAM = 370.0       # W/mK electrodeposited Cu (assumed ~95 % of wrought; PCB plated Cu 1.7-1.9 uOhm.cm) [KB-L]
K_LPBF = 340.0       # W/mK green-laser L-PBF pure Cu as-built, realistic production value (best lab 95-100 % IACS)
K_BJ = 328.0         # W/mK binder-jet Cu at 2.7 % porosity (Virginia Tech 2019)
K_CUDIA = 600.0      # W/mK Cu-diamond (powder-met / cold spray demonstrators 600-700)
K_CVD = 1500.0       # W/mK thermal-grade CVD diamond
K_CUW = 190.0        # W/mK CuW (W80-85)
K_CUMO = 220.0       # W/mK Mo-Cu


def ev(cp: ColdPlate, Q=Q0, lk=LK0, fluid=PG25, T_in=45.0, *, k_fin=None, base_layers=None, R_int=0.0,
       nu_mult=1.0, f_mult=1.0, area_frac=1.0, tim_R=None, tim_sc=None, pert=None):
    """Re-implementation of ColdPlate.evaluate with extension hooks. With defaults it reproduces the model.
    base_layers: list of (t_mm, k) replacing (base_mm, k_solid); R_int: extra series interface cm2K/W.
    pert: Monte Carlo multipliers h, tim, base, cal, hs_flow, hs_tim, dp."""
    p = dict(h=1.0, tim=1.0, base=1.0, cal=1.0, hs_flow=1.0, hs_tim=1.0, dp=1.0)
    if pert:
        p.update(pert)
    A = cp.footprint_cm2 * 1e-4
    q = Q / A
    flow_lpm = lk * Q / 1000.0
    Vdot = flow_lpm / 60000.0
    mdot = Vdot * fluid.rho
    dT_out = Q / (mdot * fluid.cp)
    b, H, L, t = cp.gap_mm * 1e-3, cp.fin_h_mm * 1e-3, cp.flow_len_mm * 1e-3, cp.fin_t_mm * 1e-3
    pitch = t + b
    W = math.sqrt(A)
    alpha = min(b, H) / max(b, H)
    Dh = 2 * b * H / (b + H)
    Nu_fd = 8.235 * (1 - 2.0421 * alpha + 3.0853 * alpha**2 - 2.4765 * alpha**3
                     + 1.0578 * alpha**4 - 0.1861 * alpha**5) * 0.95
    fRe = 24 * (1 - 1.3553 * alpha + 1.9467 * alpha**2 - 1.7012 * alpha**3 + 0.9564 * alpha**4 - 0.2537 * alpha**5)
    n_paths = (W / pitch) * cp.n_parallel_paths
    u = Vdot / (n_paths * b * H)
    Re = fluid.rho * u * Dh / fluid.mu
    x_star = L / (Dh * Re * fluid.Pr)
    Nu = Nu_fd + 0.024 * x_star**-1.14 / (1 + 0.0358 * fluid.Pr**0.17 * x_star**-0.64)
    h = Nu * fluid.k / Dh * nu_mult * p["h"]
    kf = k_fin if k_fin else cp.k_solid
    m = math.sqrt(2 * h / (kf * t))
    eta = math.tanh(m * H) / (m * H)
    h_eff = h * (area_frac * 2 * H * eta + b) / pitch
    NTU = h_eff * A / (mdot * fluid.cp)
    cal_frac = (1 / (1 - math.exp(-NTU)) - 1 / NTU) if cp.isothermal_cell else 0.5
    R_tim_nom, scatter = TIM[cp.tim]
    if tim_R is not None:
        R_tim_nom = tim_R
    if tim_sc is not None:
        scatter = tim_sc
    dT_cal = cal_frac * dT_out * p["cal"]
    dT_tim = q * R_tim_nom * 1e-4 * p["tim"]
    if base_layers is None:
        base_layers = [(cp.base_mm, cp.k_solid)]
    R_base = sum(tm * 1e-3 / k for tm, k in base_layers) + R_int * 1e-4
    dT_base = q * R_base * p["base"]
    dT_conv = q / h_eff
    dT_avg = dT_cal + dT_tim + dT_base + dT_conv
    hotspot = cp.hotspot_flow_K * p["hs_flow"] + scatter * (q / 1.28e6) * p["hs_tim"]
    dT_max = dT_avg + hotspot
    # hydraulics (as model) + screen
    dp_ch = 2 * fRe * fluid.mu * u * L / Dh**2 * f_mult
    dp_K = cp.K_channel * 0.5 * fluid.rho * u**2
    if cp.slot_w_mm > 0 and cp.n_parallel_paths > 1:
        u_slot = Vdot / ((cp.n_parallel_paths / 2) * W * cp.slot_w_mm * 1e-3)
    else:
        u_slot = 0.0
    dp_slot = cp.K_slot * 0.5 * fluid.rho * u_slot**2
    u_header = cp.header_u_m_s * flow_lpm / 18.0
    dp_header = cp.K_header * 0.5 * fluid.rho * u_header**2
    u_port = Vdot / (math.pi / 4 * (cp.port_bore_mm * 1e-3) ** 2)
    dp_port = cp.K_port * 0.5 * fluid.rho * u_port**2
    # orifice comb sized so the branch (channel + comb) is ~2.2 kPa at 18 LPM; if the channel already exceeds it, none
    orif18 = cp.orifice_dp_kPa_18
    dp_orif = orif18 * 1e3 * (flow_lpm / 18.0) ** 2
    dp_screen = SCREEN_KPA_18 * 1e3 * (flow_lpm / 18.0) ** 2 if cp.isothermal_cell else 0.0
    dp_total = (dp_ch + dp_K + dp_slot + dp_header + dp_port + dp_orif + dp_screen) * p["dp"]
    pump = dp_total * Vdot
    flux_terms = dT_tim + dT_base + dT_conv
    allowed = 85.0 - T_in - dT_cal - hotspot
    Qcap = Q * allowed / flux_terms
    return dict(name=cp.name, q=q / 1e4, flow=flow_lpm, u=u, Re=Re, x_star=x_star, Nu=Nu, h=h, eta=eta, h_eff=h_eff,
                NTU=NTU, cal=dT_cal, tim=dT_tim, base=dT_base, conv=dT_conv, avg=dT_avg, hs=hotspot, max=dT_max,
                R=dT_avg / (q / 1e4), dp_ch=dp_ch / 1e3, dp=dp_total / 1e3, pump=pump, Qcap=Qcap / 1e3,
                Tmax=T_in + dT_max)


def orifice_for(cp: ColdPlate, f_mult=1.0, target=2.2):
    """Re-size the comb so channel + comb = 2.2 kPa at 18 LPM (uniformity rule of SYNTHESIS)."""
    r = ev(replace(cp, orifice_dp_kPa_18=0.0), Q0, LK0, f_mult=f_mult)
    return replace(cp, orifice_dp_kPa_18=max(0.0, target - r["dp_ch"]))


def heff_ceiling(b_mm, k, h):
    """Max h_eff of straight plate fins at gap b (infinite height, optimal thickness): (sqrt(2hkt)+hb)/(b+t)."""
    b = b_mm * 1e-3
    best = (0, 0)
    for t in np.linspace(0.02e-3, 0.6e-3, 600):
        v = (math.sqrt(2 * h * k * t) + h * b) / (b + t)
        if v > best[0]:
            best = (v, t)
    return best


def pin_heff(d_mm, gap_mm, H_mm, u_ch, k=K_CU, fluid=PG25):
    """Staggered micro-pin array under a manifold: Zukauskas-type low-Re bank Nu_d = 0.8 Re^0.4 Pr^0.36
    (Re_d 1-40), u_max = u_ch * pitch/gap; pin efficiency with adiabatic tip."""
    d, s, H = d_mm * 1e-3, (d_mm + gap_mm) * 1e-3, H_mm * 1e-3
    umax = u_ch * s / (gap_mm * 1e-3)
    Re = fluid.rho * umax * d / fluid.mu
    Nu = 0.8 * Re**0.4 * fluid.Pr**0.36
    h = Nu * fluid.k / d
    m = math.sqrt(4 * h / (k * d))
    eta = math.tanh(m * H) / (m * H)
    n = 1 / s**2
    ratio = n * math.pi * d * H * eta + (1 - n * math.pi * d**2 / 4)
    return h, eta, h * ratio


def die_dT(h_eff_kW, tim_R, base_mm=1.0, k_base=K_CU, R_int=0.0, q_die=350.0):
    """SYNTHESIS reticle-die hot-cell fit (case-to-inlet, zoned, 1 mm Cu base, 350 W/cm2), re-based for base."""
    d_base = q_die * 10 * (base_mm / k_base - 1.0 / K_CU) + q_die * R_int
    return 33.0 + 3500.0 / h_eff_kW + (tim_R - 0.05) * 350.0 + d_base


def mc(cp, n=20000, seed=7, tim_hi=None, Qcap_n=1500, **kw):
    rng = np.random.default_rng(seed)
    R_nom = kw.get("tim_R") if kw.get("tim_R") is not None else TIM[cp.tim][0]
    hi = tim_hi if tim_hi else R_nom * 1.5
    s_tim = min(0.45, math.log(hi / R_nom) / 1.2816)
    draws = dict(h=np.exp(rng.normal(0, 0.125, n)), tim=np.exp(rng.normal(0, s_tim, n)),
                 base=np.exp(rng.normal(0, 0.05, n)), cal=np.exp(rng.normal(0, 0.025, n)),
                 hs_flow=np.exp(rng.normal(0, 0.2, n)), hs_tim=np.exp(rng.normal(0, 0.2, n)),
                 dp=np.exp(rng.normal(0, 0.18, n)))
    avg, mx, dp, qc = np.empty(n), np.empty(n), np.empty(n), []
    for i in range(n):
        pert = {k: v[i] for k, v in draws.items()}
        r = ev(cp, pert=pert, **kw)
        avg[i], mx[i], dp[i] = r["avg"], r["max"], r["dp"]
        if i < Qcap_n:
            def g(Qw):
                return ev(cp, Q=Qw, pert=pert, **kw)["Tmax"] - 85.0
            qc.append(brentq(g, 500, 300e3) / 1e3)
    pct = lambda a: tuple(np.percentile(a, [10, 50, 90]))
    return dict(avg=pct(avg), max=pct(mx), dp=pct(dp), Qcap=pct(np.array(qc)))


def row(label, r, extra=""):
    return (f"| {label} | {r['h_eff']/1e3:.0f} | {r['cal']:.1f} | {r['tim']:.1f} | {r['base']:.1f} | {r['conv']:.1f} | "
            f"**{r['avg']:.1f}** | {r['max']:.1f} | {r['R']:.3f} | {r['dp']:.1f} | {r['pump']:.1f} | {r['Qcap']:.1f} | {extra} |")


HDR = ("| variant | h_eff kW/m2K | caloric | TIM | base | conv | avg dT K | max dT K | R'' cm2K/W | dP kPa (incl. screen) "
       "| pump W | Q cap kW | note |\n|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")


def main():
    print("# Advanced-manufacturing lens: scoping runs (15 kW, 18 LPM PG25, 45 C, 117 cm2 unless stated)\n")
    # ---------------------------------------------------------------- 0. validation
    m_ref = hmmc(A0, core="R", tim="PCM pad").evaluate(Q0, LK0)
    e_ref = ev(replace(hmmc(A0, core="R", tim="PCM pad")), Q0, LK0)
    print("## 0. Validation against the project model")
    print(f"model HMMC-R PCM: avg {m_ref['dT_avg']:.2f} max {m_ref['dT_max']:.2f} dP {m_ref['dp_total_kPa']:.2f} kPa; "
          f"this script: avg {e_ref['avg']:.2f} max {e_ref['max']:.2f} dP {e_ref['dp']:.2f} kPa "
          f"(= model + {SCREEN_KPA_18} kPa clean screen)\n")

    # ---------------------------------------------------------------- 1. fin-conduction ceiling
    print("## 1. Fin-conduction ceiling at a fixed channel gap (straight plate fins, any process, infinite height)")
    print("| gap mm | h (4 mm cell) kW/m2K | ceiling h_eff Cu 390 | opt. fin t mm | ceiling ECAM 370 | ceiling L-PBF 340 | "
          "ceiling Cu-diamond fins 600 (not makeable) | achieved by skived core |")
    print("|---:|---:|---:|---:|---:|---:|---:|---|")
    ach = {0.10: "187 (P core 0.10/0.10x1.5)", 0.15: "127 (R core 0.15/0.10x2.0); 135 at H 3 mm",
           0.20: "87-98", 0.40: "-", 0.45: "-"}
    for g in (0.10, 0.15, 0.20, 0.40):
        cp = replace(hmmc(A0, core="R"), gap_mm=g, fin_t_mm=0.10, fin_h_mm=2.0)
        h = ev(cp)["h"]
        c390, t390 = heff_ceiling(g, 390, h)
        c370, _ = heff_ceiling(g, 370, h)
        c340, _ = heff_ceiling(g, 340, h)
        c600, _ = heff_ceiling(g, 600, h)
        print(f"| {g:.2f} | {h/1e3:.1f} | {c390/1e3:.0f} | {t390*1e3:.2f} | {c370/1e3:.0f} | {c340/1e3:.0f} | {c600/1e3:.0f} | "
              f"{ach.get(g, '-')} |")
    print("\nReading: at the 0.15 mm fouling floor no copper plate-fin geometry exceeds ~138 kW/m2K; the skived R core is "
          "at 92 % of it (98 % at 3 mm fins). Resolution buys nothing once the gap is fixed by filtration.\n")

    # ---------------------------------------------------------------- 2. variants at the TTV point
    print("## 2. Variants at the benchmark point")
    print(HDR)
    cool = ev(coolit_like(A0))
    print(row("CoolIT-like skived split-flow, paste (calibrated reconstruction)", cool, "measured 34.4 / 44.2"))
    R_pcm = hmmc(A0, core="R", tim="PCM pad")
    R_lm = hmmc(A0, core="R", tim="liquid metal")
    P_lm = hmmc(A0, core="P", tim="liquid metal")
    P_pcm = hmmc(A0, core="P", tim="PCM pad")
    out = {}
    out["R_pcm"] = ev(R_pcm)
    out["R_paste"] = ev(hmmc(A0, core="R", tim="paste 0.07"))
    out["R_lm"] = ev(R_lm)
    out["P_pcm"] = ev(P_pcm)
    out["P_lm"] = ev(P_lm)
    print(row("A. Chassis, skived R core 0.15/0.10x2.0, same paste", out["R_paste"], "like-for-like"))
    print(row("A. Chassis, skived R core, PCM [Tier 1, design of record]", out["R_pcm"], "50 um abs screen"))
    print(row("A. Chassis, skived R core, liquid metal [Tier 2]", out["R_lm"], ""))
    print(row("A. Chassis, skived P core 0.10/0.10x1.5, PCM", out["P_pcm"], "<= 33 um abs loops"))
    print(row("A. Chassis, skived P core, liquid metal", out["P_lm"], "<= 33 um abs loops"))
    # ECAM variants (fins only differ; manifold identical)
    e1 = ev(R_pcm, k_fin=K_ECAM)
    print(row("B1. ECAM fins, same 0.15/0.10x2.0, k 370, PCM", e1, "parity check"))
    e2c = orifice_for(replace(R_pcm, fin_t_mm=0.12, fin_h_mm=3.0))
    e2 = ev(e2c, k_fin=K_ECAM)
    print(row("B2. ECAM fins 0.15/0.12x3.0 (near ceiling), PCM", e2, "+1 mm height"))
    # offset strip: restart every 1 mm -> evaluate Nu at L = 1 mm, area loss 15 %
    st = replace(R_pcm, flow_len_mm=1.0)
    r_st = ev(st, k_fin=K_ECAM)
    nu_ratio = r_st["Nu"] / ev(R_pcm, k_fin=K_ECAM)["Nu"]
    e3 = ev(R_pcm, k_fin=K_ECAM, nu_mult=nu_ratio, area_frac=0.85, f_mult=1.6)
    print(row(f"B3. ECAM offset-strip fins, 1 mm strips (Nu x{nu_ratio:.2f}, area x0.85), PCM", e3, "x* 0.08 -> 0.02"))
    hp, etap, heffp = pin_heff(0.15, 0.15, 2.0, out["R_pcm"]["u"])
    print(f"| B4. ECAM staggered micro-pins d 0.15 / gap 0.15 / H 2.0 (correlation estimate) | {heffp/1e3:.0f} | - | - | - | "
          f"{q_conv(heffp):.1f} | ~{out['R_pcm']['avg'] - out['R_pcm']['conv'] + q_conv(heffp):.1f} | - | - | - | - | - | "
          f"h {hp/1e3:.1f} kW/m2K, eta {etap:.2f}: pins lose to plates |")
    eP = ev(P_lm, k_fin=K_ECAM)
    print(row("B5. ECAM fins 0.10/0.10x1.5 (P geometry), k 370, LM", eP, "<= 33 um abs loops"))
    # L-PBF
    l1c = orifice_for(replace(R_pcm, gap_mm=0.40, fin_t_mm=0.25, fin_h_mm=3.0), f_mult=1.3)
    l1 = ev(l1c, k_fin=K_LPBF, f_mult=1.3)
    print(row("C1. L-PBF Cu straight fins at process limit 0.40/0.25x3.0, Ra 10-20 um, PCM", l1, "fouling-immune"))
    l2c = orifice_for(replace(R_pcm, gap_mm=0.45, fin_t_mm=0.25, fin_h_mm=3.0), f_mult=3.9)
    l2 = ev(l2c, k_fin=K_LPBF, nu_mult=1.8, f_mult=3.9)
    print(row("C2. L-PBF Cu gyroid-equivalent (0.45 pore / 0.25 wall, Nu x1.8, f x3.9), PCM", l2, "TPMS literature mult."))
    l3c = orifice_for(replace(R_pcm, gap_mm=0.45, fin_t_mm=0.25, fin_h_mm=3.0, flow_len_mm=0.5 * 108,
                              n_parallel_paths=2, isothermal_cell=False, hotspot_flow_K=6.3), f_mult=3.9)
    l3 = ev(replace(l3c, orifice_dp_kPa_18=0.0), k_fin=K_LPBF, nu_mult=1.8, f_mult=3.9)
    print(row("C3. L-PBF gyroid monolith, split-flow 54 mm (no manifold), PCM", l3, "what 'print the whole plate' gives"))
    b1c = orifice_for(replace(R_pcm, gap_mm=0.50, fin_t_mm=0.40, fin_h_mm=3.0))
    b1 = ev(b1c, k_fin=K_BJ, base_layers=[(1.0, K_BJ)])
    print(row("C4. Binder-jet Cu fins+base 0.50/0.40x3.0, k 328, PCM", b1, "porosity -> leak risk"))
    # Bases
    d1 = ev(R_lm, base_layers=[(1.0, K_CUDIA)])
    print(row("D1. R core + 1.0 mm Cu-diamond base (k 600), LM", d1, "vs A Tier 2"))
    d2 = ev(R_lm, base_layers=[(0.5, K_CVD), (0.5, K_CU)], R_int=0.005)
    print(row("D2. R core + 0.5 mm CVD diamond insert + 0.5 mm Cu, braze 0.005, LM", d2, "full-field (cost-prohibitive)"))
    d3 = ev(R_lm, base_layers=[(0.6, K_CU)], R_int=0.08)
    print(row("D3. Vapor-chamber base (evaporator+condenser 0.08 cm2K/W, 0.6 mm walls), LM", d3, "rejected"))
    x1 = ev(P_lm, k_fin=K_ECAM, base_layers=[(0.03, K_CU), (1.0, K_CUDIA), (0.03, K_CU)])
    print(row("X. ECAM 0.10/0.10x1.5 fins on 1.0 mm Cu-diamond (30 um Cu skins), LM", x1, "<= 33 um loops; Tier 3 / >30 kW"))
    x2 = ev(R_lm, k_fin=K_ECAM, base_layers=[(0.03, K_CU), (1.0, K_CUDIA), (0.03, K_CU)])
    print(row("X-R. ECAM 0.15/0.10x2.0 fins on Cu-diamond, LM", x2, "drop-in filtration"))
    print()

    # ---------------------------------------------------------------- 3. other operating points
    print("## 3. Other operating points, design of record (A, R core, PCM) and Tier 2")
    print("| case | flow LPM | avg dT | max dT | dP kPa incl. screen | pump W |")
    print("|---|---:|---:|---:|---:|---:|")
    for lk, lab in ((0.75, "0.75 LPM/kW (Nvidia 45/65 C envelope)"), (1.0, "1.0 LPM/kW"), (1.2, "1.2 LPM/kW benchmark"),
                    (2.4, "2x flow, 36 LPM")):
        r = ev(R_pcm, lk=lk)
        r2 = ev(R_lm, lk=lk)
        print(f"| {lab} PCM / LM | {r['flow']:.1f} | {r['avg']:.1f} / {r2['avg']:.1f} | {r['max']:.1f} / {r2['max']:.1f} | "
              f"{r['dp']:.1f} | {r['pump']:.1f} |")
    r20 = ev(replace(R_pcm, port_bore_mm=20.0), lk=2.4)
    print(f"| 2x flow with 20 mm ports | 36.0 | {r20['avg']:.1f} | {r20['max']:.1f} | {r20['dp']:.1f} | {r20['pump']:.1f} |")
    target = cool["pump"]
    lk_eq = brentq(lambda lk: ev(R_pcm, lk=lk)["pump"] - target, 0.5, 5)
    req = ev(R_pcm, lk=lk_eq)
    req2 = ev(R_lm, lk=lk_eq)
    print(f"| equal pump power to CoolIT-like ({target:.1f} W) | {req['flow']:.1f} | {req['avg']:.1f} / {req2['avg']:.1f} | "
          f"{req['max']:.1f} / {req2['max']:.1f} | {req['dp']:.1f} | {req['pump']:.1f} |")
    lk_par = brentq(lambda lk: ev(R_pcm, lk=lk)["avg"] - 34.4, 0.3, 3)
    rpar = ev(R_pcm, lk=lk_par)
    print(f"| flow to match CoolIT 34.4 K avg (PCM) | {rpar['flow']:.1f} | {rpar['avg']:.1f} | {rpar['max']:.1f} | "
          f"{rpar['dp']:.1f} | {rpar['pump']:.2f} |")
    r50 = ev(R_pcm, T_in=50.0)
    print(f"\nAt 50 C inlet, 15 kW, PCM: Tcase,max {r50['Tmax']:.1f} C\n")

    # ---------------------------------------------------------------- 4. Monte Carlo
    print("## 4. Monte Carlo P10 / P50 / P90 (20k samples; Q cap on 1.5k)")
    print("| variant | avg dT K | max dT K | dP kPa | Q cap kW |")
    print("|---|---|---|---|---|")
    cases = [("A Tier 1 R core PCM", R_pcm, dict(), 0.08), ("A Tier 2 R core LM", R_lm, dict(), 0.03),
             ("A P core LM (<= 33 um)", P_lm, dict(), 0.03),
             ("X ECAM P-fins on Cu-diamond LM", P_lm, dict(k_fin=K_ECAM, base_layers=[(0.03, K_CU), (1.0, K_CUDIA),
                                                                                      (0.03, K_CU)]), 0.03)]
    mcres = {}
    for lab, cp, kw, hi in cases:
        res = mc(cp, tim_hi=hi, **kw)
        mcres[lab] = res
        f = lambda t: f"{t[0]:.1f} / {t[1]:.1f} / {t[2]:.1f}"
        print(f"| {lab} | {f(res['avg'])} | {f(res['max'])} | {f(res['dp'])} | {f(res['Qcap'])} |")
    print()

    # ---------------------------------------------------------------- 5. real package 350 W/cm2
    print("## 5. Real 2027-28 package: 4 reticle dies 26x33 mm at 350 W/cm2 + 16 HBM, zoned, hottest-die case-to-inlet")
    print("| die-zone core / base | h_eff | PCM 0.055 | LM 0.015 | Tcase,max LM at 45 C | indium-soldered micro-channel lid, die top (In R'' by lid CTE) |")
    print("|---|---:|---:|---:|---:|---:|")
    rows5 = [("CoolIT-like split-flow (heat-map run, not the fit)", None),
             ("A: skived R core, 1 mm Cu", (out["R_pcm"]["h_eff"] / 1e3, 1.0, K_CU)),
             ("A: skived P core, 1 mm Cu (<= 33 um)", (out["P_pcm"]["h_eff"] / 1e3, 1.0, K_CU)),
             ("ECAM 0.15 fins near ceiling (B2), 1 mm Cu", (e2["h_eff"] / 1e3, 1.0, K_CU)),
             ("X-R: ECAM 0.15 fins on 1 mm Cu-diamond", (x2["h_eff"] / 1e3, 1.06, None)),
             ("X: ECAM 0.10 fins on 1 mm Cu-diamond (<= 33 um)", (x1["h_eff"] / 1e3, 1.06, None)),
             ("P core on 1 mm CuW (CTE-matched, conventional)", (out["P_pcm"]["h_eff"] / 1e3, 1.0, K_CUW)),
             ("P core on 1 mm MoCu (CTE-matched, conventional)", (out["P_pcm"]["h_eff"] / 1e3, 1.0, K_CUMO)),
             ("P core + 0.5 mm CVD diamond insert + 0.5 mm Cu (braze 0.005)", (out["P_pcm"]["h_eff"] / 1e3, None, "cvd")),
             ("Vapor-chamber base (0.08 cm2K/W), P core", (out["P_pcm"]["h_eff"] / 1e3, None, "vc"))]
    pkg = {}
    for lab, spec in rows5:
        if spec is None:
            print(f"| {lab} | 101 | 88.6 (paste 0.05) | ~76 | ~121 C | - |")
            continue
        h, tb, kb = spec
        def dd(R):
            if kb == "cvd":
                return die_dT(h, R, 0.5, K_CVD) + 350 * 10 * (0.5 / K_CU) + 350 * 0.005
            if kb == "vc":
                return die_dT(h, R, 0.6, K_CU, R_int=0.08)
            if kb is None:  # Cu-diamond with two 30 um Cu skins
                return die_dT(h, R, 1.0, K_CUDIA) + 350 * 10 * (0.06 / K_CU)
            return die_dT(h, R, tb, kb)
        matched = (kb is None) or (kb in (K_CUW, K_CUMO))
        R_in = 0.011 if kb is None else (0.012 if matched else 0.032)
        a, b, c = dd(0.055), dd(0.015), dd(R_in)
        pkg[lab] = (a, b, c)
        print(f"| {lab} | {h:.0f} | {a:.1f} | {b:.1f} | {45 + b:.0f} C | {c:.1f} ({45 + c:.0f} C), In {R_in} |")
    d2d = die_dT(out["P_pcm"]["h_eff"] / 1e3, 0.015, 0.8, K_CU)
    d2dR = die_dT(out["R_pcm"]["h_eff"] / 1e3, 0.015, 0.8, K_CU)
    print(f"| Reference: bare-die LM on 0.8 mm Cu pedestal (sibling Tier 3A), R / P core | 127 / 187 | - | {d2dR:.1f} / {d2d:.1f} (die top) | {45+d2dR:.0f} / {45+d2d:.0f} C | - |")
    xs = ev(replace(P_lm, flow_len_mm=2.0), k_fin=K_ECAM)["Nu"] / ev(P_lm, k_fin=K_ECAM)["Nu"]
    xseg = ev(P_lm, k_fin=K_ECAM, base_layers=[(0.03, K_CU), (1.0, K_CUDIA), (0.03, K_CU)], nu_mult=xs, area_frac=2/2.2)
    cseg = die_dT(xseg["h_eff"] / 1e3, 0.011, 1.0, K_CUDIA) + 350 * 10 * (0.06 / K_CU)
    print(f"| X as built: segmented 2 mm ECAM strips on Cu-diamond, CuMo cap (<= 33 um) | {xseg['h_eff']/1e3:.0f} | - | - | - | {cseg:.1f} ({45+cseg:.0f} C), In 0.011 |")
    print("\nNotes: fit valid for 1 mm bases and h_eff 100-350 kW/m2K; base re-based 1-D (die 26x33 mm >> spreading "
          "length 1.8-4 mm, so lateral spreading credit is negligible). CVD/VC rows include their interfaces.\n")

    # sub-die hot spot: spreading benefit of a high-k base for a 2x2 mm 1000 W/cm2 patch (axisymmetric FD)
    print("## 6. Sub-die hot spot (r = 1.13 mm patch, +650 W/cm2 over the 350 W/cm2 die field), base 1 mm, "
          "h_eff 187 kW/m2K, LM TIM 0.015, peak excess above the uniform field (axisymmetric finite volume)")
    print("| base | peak excess K | vs Cu |")
    print("|---|---:|---:|")
    cu_ex = None
    for lab, k in (("Cu 390", 390), ("Cu-diamond 600", 600), ("CVD diamond 1500", 1500), ("CuW 190", 190)):
        ex = hotspot_excess(k, 1.0e-3, 187e3, 0.015e-4, 1.13e-3, 650e4)
        cu_ex = ex if cu_ex is None else cu_ex
        print(f"| {lab} | {ex:.1f} | {ex - cu_ex:+.1f} |")
    print()

    # ---------------------------------------------------------------- 7. GPU-class plates
    print("## 7. GPU-class plates (lidded, model), chassis R core vs CoolIT-like")
    print("| case | CoolIT-like avg/max | R PCM avg/max | R LM avg/max | X (ECAM P on CuDia) LM avg/max | dP CoolIT-like / R |")
    print("|---|---|---|---|---|---|")
    for lab, Qk, A, lk in (("Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW", 2.3, 60, 1.0), ("Rubin 2.3 kW, 60 cm2, 1.2 LPM/kW", 2.3, 60, 1.2),
                           ("Rubin Ultra 3.6 kW, 80 cm2, 1.0 LPM/kW", 3.6, 80, 1.0),
                           ("CoolIT 4 kW point, 25 cm2, 1.5 LPM/kW", 4.0, 25, 1.5)):
        c = ev(coolit_like(A), Q=Qk * 1e3, lk=lk)
        a = ev(hmmc(A, core="R", tim="PCM pad"), Q=Qk * 1e3, lk=lk)
        b = ev(hmmc(A, core="R", tim="liquid metal"), Q=Qk * 1e3, lk=lk)
        x = ev(hmmc(A, core="P", tim="liquid metal"), Q=Qk * 1e3, lk=lk, k_fin=K_ECAM,
               base_layers=[(0.03, K_CU), (1.0, K_CUDIA), (0.03, K_CU)])
        print(f"| {lab} | {c['avg']:.1f} / {c['max']:.1f} | {a['avg']:.1f} / {a['max']:.1f} | {b['avg']:.1f} / {b['max']:.1f} | "
              f"{x['avg']:.1f} / {x['max']:.1f} | {c['dp']:.1f} / {a['dp']:.1f} |")
    print()

    # ---------------------------------------------------------------- 8. wafer-scale / >30 kW
    print("## 8. >30 kW and wafer-scale (1.2 LPM/kW)")
    print("| case | design | avg dT | max dT | dP kPa | Q cap kW |")
    print("|---|---|---:|---:|---:|---:|")
    for lab, Qk, A in (("30 kW, 150 cm2 (200 W/cm2)", 30, 150), ("25 kW on 117 cm2 (214 W/cm2)", 25, 117),
                       ("Wafer-scale 20 kW, 460 cm2 (43 W/cm2)", 20, 460)):
        for dl, cp, kw in (("A R core PCM", hmmc(A, core="R", tim="PCM pad"), {}),
                           ("A R core LM", hmmc(A, core="R", tim="liquid metal"), {}),
                           ("X ECAM P on CuDia LM", hmmc(A, core="P", tim="liquid metal"),
                            dict(k_fin=K_ECAM, base_layers=[(0.03, K_CU), (1.0, K_CUDIA), (0.03, K_CU)]))):
            r = ev(cp, Q=Qk * 1e3, **kw)
            print(f"| {lab} | {dl} | {r['avg']:.1f} | {r['max']:.1f} | {r['dp']:.1f} | {r['Qcap']:.1f} |")
    print("(wafer-scale dP assumes the manifold is tiled with 4 port pairs; the single-port number is not meaningful)\n")

    # ---------------------------------------------------------------- 9. cost model
    print("## 9. Unit factory cost by route, US$ per plate (KB-M/KB-L, RFQ needed)")
    cost_rows()

    # ---------------------------------------------------------------- 10. power electronics
    print("\n## 10. Power-electronics check: SiC module baseplate area 30-80 W/cm2, 50/50 WEG at 65 C, 10 LPM per module")
    WEG = replace(PG25, name="WEG50 @65C", rho=1045.0, cp=3500.0, mu=1.6e-3, k=0.42)
    for lab, cp in (("forged pin-fin class (coarse 1.0/1.0 x 6 mm, 40 mm path)",
                     replace(coolit_like(60), gap_mm=1.0, fin_t_mm=1.0, fin_h_mm=6.0, base_mm=3.0, tim="direct-to-die",
                             hotspot_flow_K=2.0)),
                    ("chassis de-rated 0.40/0.30 x 3 mm, 4 mm cells, Cu",
                     orifice_for(replace(hmmc(60, core="R", tim="direct-to-die"), gap_mm=0.40, fin_t_mm=0.30, fin_h_mm=3.0,
                                         base_mm=3.0))),
                    ("L-PBF AlSi10Mg conformal 0.5/0.5 x 4 mm, 4 mm cells (k 150)",
                     orifice_for(replace(hmmc(60, core="R", tim="direct-to-die"), gap_mm=0.5, fin_t_mm=0.5, fin_h_mm=4.0,
                                         base_mm=3.0, k_solid=150.0)))):
        r = ev(cp, Q=3000.0, lk=10 / 3.0, fluid=WEG, T_in=65.0)
        print(f"- {lab}: plate R'' {r['R'] - 0.0:.3f} cm2K/W (incl. caloric), conv {r['conv']:.1f} K, base {r['base']:.1f} K, "
              f"avg dT {r['avg']:.1f} K at {r['q']:.0f} W/cm2, dP {r['dp']:.1f} kPa")


def q_conv(heff):
    return Q0 / (A0 * 1e-4) / heff


def hotspot_excess(k, t, h_eff, R_tim, a, dq, Rdom=12e-3, nr=240, nz=20):
    """Axisymmetric finite-volume: base disc radius Rdom, thickness t, conductivity k; heat dq over r<a on the top face
    through a TIM R_tim (series, per area, applied as a contact layer); bottom face h_eff to 0. Returns peak top-surface
    temperature excess at r = 0 (die-side surface, i.e. above the TIM) relative to far field (superposition)."""
    from scipy.sparse import lil_matrix
    from scipy.sparse.linalg import spsolve
    dr, dz = Rdom / nr, t / nz
    N = nr * nz
    Amat = lil_matrix((N, N))
    rhs = np.zeros(N)
    idx = lambda i, j: j * nr + i
    for j in range(nz):
        for i in range(nr):
            rc = (i + 0.5) * dr
            rw, re = i * dr, (i + 1) * dr
            vol = rc * dr * dz
            p = idx(i, j)
            diag = 0.0
            if i > 0:
                c = k * rw * dz / dr
                Amat[p, idx(i - 1, j)] -= c
                diag += c
            if i < nr - 1:
                c = k * re * dz / dr
                Amat[p, idx(i + 1, j)] -= c
                diag += c
            if j > 0:
                c = k * rc * dr / dz
                Amat[p, idx(i, j - 1)] -= c
                diag += c
            else:  # bottom: convective h_eff through half cell
                c = rc * dr / (dz / (2 * k) + 1 / h_eff)
                diag += c
            if j < nz - 1:
                c = k * rc * dr / dz
                Amat[p, idx(i, j + 1)] -= c
                diag += c
            else:  # top: heat input
                if rc < a:
                    rhs[p] += dq * rc * dr
            Amat[p, p] = diag
    T = spsolve(Amat.tocsr(), rhs)
    T_top0 = T[idx(0, nz - 1)] + dq * (dz / 2) / k
    return T_top0 + dq * R_tim


def cost_rows():
    # 15 kW-class body 148 x 152 mm; Rubin-class 110 x 120 mm. Chassis line items follow proposal-hmmc-elite / manufacturing-cost.
    chassis = {
        "OFE Cu incl. swarf": (26, 24), "skived fin core": (40, 24), "3 etched laminates (grate, plenum, comb)": (36, 16),
        "CNC manifold block": (80, 34), "cover + stubs": (14, 6), "vacuum diffusion bond": (55, 32),
        "screen, plugs, taps": (15, 8), "lapping, inspection": (12, 6), "load frame, screws": (20, 14), "He leak + flow test": (8, 5)}
    sub = [sum(v[0] for v in chassis.values()), sum(v[1] for v in chassis.values())]
    tot = [round(s * 1.12) for s in sub]
    print("| line item | 10k/yr | 100k/yr |\n|---|---:|---:|")
    for k_, v in chassis.items():
        print(f"| {k_} | {v[0]} | {v[1]} |")
    print(f"| **A. chassis, skived core, factory cost incl. 12 % yield/overhead** | **{tot[0]}** | **{tot[1]}** |")
    print(f"| Rubin-class (110 x 120 mm) chassis | {round(tot[0]*0.70)} | {round(tot[1]*0.71)} |")
    # ECAM throughput model: deposit volume / rate x hourly cost + prep/rinse/inspect
    def ecam(vol_cm3, rate, hourly, fixed):
        return vol_cm3 / rate * hourly + fixed
    full_fin_10k = ecam(12.0, 5.0, 60.0, 15.0)
    full_fin_100k_lo, full_fin_100k_hi = ecam(12.0, 20.0, 45.0, 10.0), ecam(12.0, 8.0, 50.0, 12.0)
    print("\n| route (replaces) | 10k/yr | 100k/yr | adder vs chassis at 100k | basis |\n|---|---:|---:|---:|---|")
    print(f"| B. ECAM full fin field 108x108 mm, 12 cm3 (replaces skived core 40/24) | {full_fin_10k:.0f} | "
          f"{full_fin_100k_lo:.0f}-{full_fin_100k_hi:.0f} | +{full_fin_100k_lo-24:.0f} to +{full_fin_100k_hi-24:.0f} | "
          "5 cm3/h & US$60/h today; 8-20 cm3/h & US$45-50/h at maturity (assumed; Fabric8 publishes none) |")
    die_10k = ecam(4.0, 5.0, 60.0, 15.0)
    die_100k = ecam(4.0, 15.0, 45.0, 10.0)
    cudia_10k = (4 * 40, 12 * 40)
    cudia_100k = (2 * 40, 6 * 40)
    skin_10k, skin_100k = 30, 15
    print(f"| X. die-zone core: Cu-diamond 1 mm x 40 cm2 + ECAM 0.10 fins 4 cm3 + Cu skins/rim weld | "
          f"{cudia_10k[0]+die_10k+skin_10k:.0f}-{cudia_10k[1]+die_10k+skin_10k:.0f} | "
          f"{cudia_100k[0]+die_100k+skin_100k:.0f}-{cudia_100k[1]+die_100k+skin_100k:.0f} | "
          f"+{cudia_100k[0]+die_100k+skin_100k:.0f} to +{cudia_100k[1]+die_100k+skin_100k:.0f} | "
          "Cu-diamond US$4-12/cm2 (10k), 2-6 (100k) [KB-L, no published price] |")
    lp10 = 105 / 15 * 75 + 95 + 80
    lp100 = 105 / 50 * 90 + 85 + 50
    print(f"| C. L-PBF Cu manifold block ~105 cm3 incl. supports (replaces CNC block + 2 laminates, 104/45) | {lp10:.0f} | "
          f"{lp100:.0f} | +{lp100-45:.0f} | 15 cm3/h single-laser at US$75/h; 50 cm3/h multi-laser at US$90/h; powder US$90-100/kg |")
    print("| C'. Binder-jet Cu manifold block + sinter + HIP + machining | 60-120 | 30-60 | -15 to +15 | parity at best; "
          "15-20 % shrink, 93-97 % dense |")
    print("| C''. L-PBF Cu complete plate (fins >= 0.4 mm) | 400-900 | 250-500 | +60 to +310 vs chassis total | "
          "manufacturing-cost.md |")
    print("| D. CVD diamond insert 34 cm2 x 0.5 mm (metallised, brazed) | 340-1700 | 300-1000 | +300 to +1000 | "
          "US$10/cm2 film to US$1/mm3 (Element Six 2015) |")
    print("| D'. Vapor-chamber base (rejected thermally) | 60-90 | 25-40 | +10 to +25 | air-cooling VC industry |")
    print("| Dev tooling: L-PBF Cu manifold test block / clear SLA manifold | 600-1200 / 80-200 each | - | - | 3-7 days |")


if __name__ == "__main__":
    main()
