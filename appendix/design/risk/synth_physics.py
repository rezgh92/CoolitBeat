#!/usr/bin/env python3
"""
SYNTHESIS-physics.py - consolidated, corrected numbers for the HMMC cold plate vs a CoolIT-like
skived split-flow plate at 15 kW / 18 LPM PG25 / 45 C inlet, with uncertainty bands, Q capacity at
T_case,max <= 85 C and pumping power.  Chief-engineer reconciliation of the seven sibling reports.

Corrections relative to docs/cooling/model/coldplate_model.py (all traced to a sibling report):
 1. Darcy friction  dp = 2 f.Re mu u L / Dh^2  (model had f.Re mu u L / (2 Dh^2): 4x low)   [hydraulic-detail,
    manifold-maldistribution]
 2. Isothermal-cell caloric term for manifold plates  dT_cal = dT_out [1/(1-e^-NTU) - 1/NTU]  instead of
    0.5 dT_out (+1.3-1.6 K)   [hotspot-smoothing]
 3. Hot spot = flow-driven long-wave maldistribution + TIM/assembly scatter (measured-equivalent, max of 8 TCs)
    [hotspot-smoothing, tim-and-direct-to-die]
 4. Channel gap floor 0.15 mm (10-year SKU behind a 50 um absolute plate screen); 0.10 mm only with <= 33 um
    absolute loop filtration; 0.05-0.075 mm not deployable   [fouling-filtration]
 5. Manifold of record = design H (P = 8 mm / 4 mm flow length, centre-fed + centre-collected, 3.5 x 8 mm slots,
    10x15 / 14x20 mm headers, 16 mm ports): 5.0 kPa at 18 LPM, global max/min 1.10.  When channel friction falls
    below ~2 kPa (wider gaps) the branch resistance is restored with a >= 0.4 mm orifice comb at the slot top
    [manifold-maldistribution sec. 3.6, fouling rule 8]
 6. Base 1.0 mm as-bonded / 0.8 mm finished, tied sandwich (fins brazed to manifold webs)  [base-stress-stiffness]
 7. CoolIT-like dP re-based on the corrected network: 21.8 kPa at 18 LPM (17-42 kPa band)  [hydraulic-detail]

Run: python3 SYNTHESIS-physics.py
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace

import numpy as np
from scipy.optimize import brentq

# ------------------------------------------------------------------ fluid / solids
RHO, CP, MU, KF = 1005.0, 3930.0, 1.25e-3, 0.52      # PG25 ~50 C
PR = CP * MU / KF
K_CU = 390.0
T_IN = 45.0
T_CASE_LIMIT = 85.0
A_FP = 117e-4                                        # m2, 108 x 108 mm calibrated footprint
SIDE = math.sqrt(A_FP)                               # m


@dataclass
class Design:
    name: str
    gap: float          # m
    fin_t: float        # m
    fin_h: float        # m
    L: float            # m, channel flow length (inlet slot -> return slot; split-flow: half plate)
    base: float         # m
    kind: str           # 'hmmc' | 'split'
    tim_R: float        # cm2K/W nominal
    tim_lo: float
    tim_hi: float
    tim_label: str
    tim_scatter_K: float    # max-of-8-TC TIM/assembly scatter at 128 W/cm2, measured-equivalent
    flow_hs_K: float        # flow-driven (long-wave maldistribution) hot spot, K
    dp_visc_kPa: float      # linear-in-flow part of plate dP at 18 LPM
    dp_inert_kPa: float     # quadratic-in-flow part of plate dP at 18 LPM
    dp_note: str = ""
    deployable: str = "yes"

    @property
    def n_paths(self) -> int:
        n_across = SIDE / (self.gap + self.fin_t)
        if self.kind == "split":
            return int(n_across * 2)
        n_slots = max(1, round(SIDE / (2 * self.L)))
        return int(n_across * 2 * n_slots)


def nusselt(alpha: float, x_star: float) -> float:
    """Shah & London H1 rectangular duct, 3-side heating factor 0.95, Stephan-type entrance term
    (same correlation as coldplate_model.py so that only the corrections differ)."""
    nu_fd = 8.235 * (1 - 2.0421 * alpha + 3.0853 * alpha**2 - 2.4765 * alpha**3
                     + 1.0578 * alpha**4 - 0.1861 * alpha**5) * 0.95
    return nu_fd + 0.024 * x_star**-1.14 / (1 + 0.0358 * PR**0.17 * x_star**-0.64)


def f_re_fanning(alpha: float) -> float:
    return 24 * (1 - 1.3553 * alpha + 1.9467 * alpha**2 - 1.7012 * alpha**3
                 + 0.9564 * alpha**4 - 0.2537 * alpha**5)


def evaluate(d: Design, Q: float, lpm_per_kw: float, pert: dict | None = None) -> dict:
    """Series network with the corrections 1-3 applied.  pert = multipliers for Monte Carlo."""
    p = {k: 1.0 for k in ("h", "tim", "base", "cal", "flow_hs", "tim_sc", "dp_visc", "dp_inert")}
    if pert:
        p.update(pert)
    q = Q / A_FP
    flow_lpm = lpm_per_kw * Q / 1000
    Vdot = flow_lpm / 60000
    mdot = Vdot * RHO
    dT_out = Q / (mdot * CP)

    b, H, t, L = d.gap, d.fin_h, d.fin_t, d.L
    pitch = b + t
    alpha = min(b, H) / max(b, H)
    Dh = 2 * b * H / (b + H)
    u = Vdot / (d.n_paths * b * H)
    Re = RHO * u * Dh / MU
    x_star = L / (Dh * Re * PR)
    h = nusselt(alpha, x_star) * KF / Dh * p["h"]
    m = math.sqrt(2 * h / (K_CU * t))
    eta = math.tanh(m * H) / (m * H)
    h_eff = h * (2 * H * eta + b) / pitch
    NTU = h_eff * A_FP / (mdot * CP)

    # 1. caloric term
    if d.kind == "hmmc":
        cal_frac = 1 / (1 - math.exp(-NTU)) - 1 / NTU        # isothermal cell (hotspot-smoothing)
    else:
        cal_frac = 0.5                                        # long single pass, linear ramp
    dT_cal = cal_frac * dT_out * p["cal"]
    dT_tim = q * d.tim_R * 1e-4 * p["tim"]
    dT_base = q * d.base * p["base"] / K_CU
    dT_conv = q / h_eff
    dT_avg = dT_cal + dT_tim + dT_base + dT_conv
    hs_flow = d.flow_hs_K * p["flow_hs"]
    hs_tim = d.tim_scatter_K * (q / 1.28e6) * p["tim_sc"]   # scales with flux
    dT_max = dT_avg + hs_flow + hs_tim

    # 2. hydraulics: plate port-to-port, viscous ~V, inertial ~V^2, referenced to 18 LPM
    s = flow_lpm / 18.0
    dp_kPa = d.dp_visc_kPa * s * p["dp_visc"] + d.dp_inert_kPa * s**2 * p["dp_inert"]
    # channel friction check (Darcy form) - reported for information
    dp_ch_Pa = 2 * f_re_fanning(alpha) * MU * u * L / Dh**2
    pump_W = dp_kPa * 1e3 * Vdot

    return dict(q=q / 1e4, flow_lpm=flow_lpm, dT_out=dT_out, u=u, Re=Re, h=h, eta=eta, h_eff=h_eff, NTU=NTU,
                cal_frac=cal_frac, dT_cal=dT_cal, dT_tim=dT_tim, dT_base=dT_base, dT_conv=dT_conv,
                dT_avg=dT_avg, hs_flow=hs_flow, hs_tim=hs_tim, dT_max=dT_max,
                T_case_avg=T_IN + dT_avg, T_case_max=T_IN + dT_max,
                R_unit=dT_avg / (q / 1e4), R_KW=dT_avg / Q,
                dp_kPa=dp_kPa, dp_ch_kPa=dp_ch_Pa / 1e3, pump_W=pump_W)


def q_capacity(d: Design, lpm_per_kw: float, pert: dict | None = None, basis: str = "max") -> float:
    """Largest Q (kW) with T_case,max <= 85 C at constant LPM/kW (flow scales with Q)."""
    key = "T_case_max" if basis == "max" else "T_case_avg"

    def g(Qw):
        return evaluate(d, Qw, lpm_per_kw, pert)[key] - T_CASE_LIMIT

    try:
        return brentq(g, 500.0, 200e3) / 1e3
    except ValueError:
        return float("nan")


# ------------------------------------------------------------------ designs of record
# Hot-spot inputs (K at 128 W/cm2):
#   CoolIT measured 9.8 K = 8.8 K systematic flow/exit + ~1 K; we keep the measured decomposition:
#   flow-driven 6.3 K (model 5.7 perfect .. 8.4 at +/-20 %), TIM scatter 3.5 K (max-of-8 TC, paste, 50-100 um bow)
#   HMMC flow-driven: 0.25 K perfect, 1.3 K at +/-10 %, 2.3 K at +/-20 % long-wave  -> nominal 1.5 K (+/-10 % verified)
#   TIM scatter scaled by bow sensitivity at 50 um (grease 18 K : PCM 7.5 K : LM 3.2 K) -> 3.5 / 1.5 / 0.6 K
COOLIT = Design("CoolIT-like skived split-flow 0.2/0.2x4, 2 mm base, paste 0.07", 0.2e-3, 0.2e-3, 4.0e-3,
                54e-3, 2.0e-3, "split", 0.07, 0.04, 0.17, "paste", 3.5, 6.3,
                # corrected network at 18 LPM: fd friction 14.5 + Hagenbach 0.2 (visc) ; turns/plenums/ports 7.1 (inert)
                dp_visc_kPa=14.7, dp_inert_kPa=7.1, dp_note="hydraulic-detail: 21.8 kPa, band 17-42 kPa")

# HMMC manifold of record = design H budget at 18 LPM (manifold-maldistribution sec. 7):
#   viscous: L3 channel friction (geometry dependent) + L2 slot friction ~0.1
#   inertial: ports 2.5, tees 0.24+0.13, L1 net 0.11, L2 momentum 0.16, L3 turns 0.06  ~ 2.75 kPa  (fit: 0.125 V + 0.00849 V^2)
#   branch target >= 2.2 kPa for global max/min <= 1.10 -> orifice comb adds (2.2 - dp_ch) as an inertial term
HMMC_INERT_BASE = 2.75     # kPa at 18 LPM, manifold + ports, design H
HMMC_VISC_BASE = 0.10      # kPa, slot friction etc.
BRANCH_TARGET = 2.2        # kPa at 18 LPM


def hmmc(name, gap_mm, fin_mm, H_mm, L_mm, base_mm, tim_R, tim_lo, tim_hi, tim_label, tim_sc, flow_hs=1.5,
         deployable="yes"):
    d = Design(name, gap_mm * 1e-3, fin_mm * 1e-3, H_mm * 1e-3, L_mm * 1e-3, base_mm * 1e-3, "hmmc",
               tim_R, tim_lo, tim_hi, tim_label, tim_sc, flow_hs, 0.0, 0.0, deployable=deployable)
    r = evaluate(d, 15e3, 1.2)
    dp_ch = r["dp_ch_kPa"]
    orifice = max(0.0, BRANCH_TARGET - dp_ch)
    d.dp_visc_kPa = HMMC_VISC_BASE + dp_ch
    d.dp_inert_kPa = HMMC_INERT_BASE + orifice
    d.dp_note = f"design-H manifold; channel {dp_ch:.2f} kPa + orifice comb {orifice:.2f} kPa"
    return d


DESIGNS = [
    COOLIT,
    hmmc("HMMC-R robust 0.15/0.10x2.0, L4, base 1.0, paste 0.07 (same TIM as benchmark)",
         0.15, 0.10, 2.0, 4.0, 1.0, 0.07, 0.04, 0.17, "paste", 3.5),
    hmmc("HMMC-R robust, PCM 0.055  [Tier 1 drop-in]", 0.15, 0.10, 2.0, 4.0, 1.0, 0.055, 0.04, 0.08, "PCM", 1.5),
    hmmc("HMMC-R robust, liquid metal 0.015  [Tier 2 OEM]", 0.15, 0.10, 2.0, 4.0, 1.0, 0.015, 0.005, 0.03, "LM", 0.6),
    hmmc("HMMC-P performance 0.10/0.10x1.5, L4, PCM 0.055  (<= 33 um abs filtration)",
         0.10, 0.10, 1.5, 4.0, 1.0, 0.055, 0.04, 0.08, "PCM", 1.5, deployable="25 um loops only"),
    hmmc("HMMC-P performance, liquid metal 0.015", 0.10, 0.10, 1.5, 4.0, 1.0, 0.015, 0.005, 0.03, "LM", 0.6,
         deployable="25 um loops only"),
    hmmc("(ref, not deployable) HMMC-fine 0.075x1.0, L4, LM 0.015", 0.075, 0.075, 1.0, 4.0, 1.0, 0.015, 0.005,
         0.03, "LM", 0.6, deployable="no (W/d <= 3)"),
    hmmc("HMMC-R robust, D2D LM 0.015, base 0.8 (case = die top)  [Tier 3]", 0.15, 0.10, 2.0, 4.0, 0.8, 0.015,
         0.005, 0.03, "D2D LM", 0.6),
]


def monte_carlo(d: Design, Q=15e3, lpm_kw=1.2, n=20000, seed=1):
    """Lognormal / uniform perturbations with the per-report uncertainty statements."""
    rng = np.random.default_rng(seed)
    out = {k: np.empty(n) for k in ("dT_avg", "dT_max", "dp_kPa", "pump_W", "Qcap")}
    # TIM: lognormal about nominal with P90 at the report's upper value, capped at sigma 0.45 (the 0.17 paste tail is
    # a warped-lid outlier already excluded by the 34.4 K calibration); h_eff +/-25 % (1 sigma 12.5 %);
    # base +/-10 % (finish machining); caloric +/-5 %; hot-spot terms +/-40 %; dP viscous +/-25 %, inertial +/-45 %
    s_tim = min(0.45, math.log(d.tim_hi / d.tim_R) / 1.2816)
    tim = np.exp(rng.normal(0, s_tim, n))
    hf = np.exp(rng.normal(0, 0.125, n))
    bf = np.exp(rng.normal(0, 0.05, n))
    cf = np.exp(rng.normal(0, 0.025, n))
    fh = np.exp(rng.normal(0, 0.2, n))
    ts = np.exp(rng.normal(0, 0.2, n))
    dv = np.exp(rng.normal(0, 0.125, n))
    di = np.exp(rng.normal(0, 0.225, n))
    for i in range(n):
        pert = dict(h=hf[i], tim=tim[i], base=bf[i], cal=cf[i], flow_hs=fh[i], tim_sc=ts[i], dp_visc=dv[i],
                    dp_inert=di[i])
        r = evaluate(d, Q, lpm_kw, pert)
        out["dT_avg"][i] = r["dT_avg"]
        out["dT_max"][i] = r["dT_max"]
        out["dp_kPa"][i] = r["dp_kPa"]
        out["pump_W"][i] = r["pump_W"]
        out["Qcap"][i] = np.nan
    # Q-cap bands on a 2000-sample subset (brentq per sample)
    idx = rng.choice(n, 2000, replace=False)
    for i in idx:
        pert = dict(h=hf[i], tim=tim[i], base=bf[i], cal=cf[i], flow_hs=fh[i], tim_sc=ts[i], dp_visc=dv[i],
                    dp_inert=di[i])
        out["Qcap"][i] = q_capacity(d, lpm_kw, pert)
    return {k: (np.nanpercentile(v, 10), np.nanpercentile(v, 50), np.nanpercentile(v, 90)) for k, v in out.items()}


def equal_pump_power_point(d: Design, Q=15e3, target_W=None) -> dict:
    """Flow at which the plate uses the same hydraulic pumping power as the CoolIT-like plate at 18 LPM."""
    if target_W is None:
        target_W = evaluate(COOLIT, Q, 1.2)["pump_W"]

    def g(lk):
        return evaluate(d, Q, lk)["pump_W"] - target_W

    lk = brentq(g, 0.2, 6.0)
    return evaluate(d, Q, lk) | {"lpm_per_kw": lk}


def die_max_dT(h_eff_kWm2K: float, tim_R: float) -> float:
    """Reticle-die hot-cell case dT at 350 W/cm2 (heat-proportional zoning H-Z2, 1 mm base), fitted to the
    nonuniform-heatmap sweep: 68/57/51/47/43 K at h_eff 100/150/200/250/350 with paste 0.05 ->
    dT = 33 + 3500/h ; TIM term re-based linearly at 350 W/cm2."""
    return 33.0 + 3500.0 / h_eff_kWm2K + (tim_R - 0.05) * 350.0


def main():
    Q, lk = 15e3, 1.2
    print("# SYNTHESIS: corrected consolidated numbers, 15 kW / 18 LPM PG25 / 45 C inlet, 117 cm2 (128 W/cm2)\n")
    base = evaluate(COOLIT, Q, lk)
    print(f"dT_out = {base['dT_out']:.2f} K; CoolIT measured avg 34.4 / max 44.2 K\n")

    print("## 1. Deterministic budget (nominal inputs)")
    print("| design | h_eff kW/m2K | NTU | cal frac | caloric | TIM | base | conv | **avg dT** | hs flow | hs TIM | **max dT** | "
          "R'' cm2K/W | R mK/W | dP kPa | pump W | Qcap(max<=85C) kW | Qcap(avg<=85C) kW |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    results = {}
    for d in DESIGNS:
        r = evaluate(d, Q, lk)
        qc = q_capacity(d, lk)
        qca = q_capacity(d, lk, basis="avg")
        results[d.name] = (r, qc, qca)
        print(f"| {d.name} | {r['h_eff']/1e3:.0f} | {r['NTU']:.2f} | {r['cal_frac']:.3f} | {r['dT_cal']:.1f} | {r['dT_tim']:.1f} | "
              f"{r['dT_base']:.1f} | {r['dT_conv']:.1f} | **{r['dT_avg']:.1f}** | {r['hs_flow']:.1f} | {r['hs_tim']:.1f} | "
              f"**{r['dT_max']:.1f}** | {r['R_unit']:.3f} | {r['R_KW']*1e3:.2f} | {r['dp_kPa']:.1f} | {r['pump_W']:.2f} | "
              f"{qc:.1f} | {qca:.1f} |")
    print()
    for d in DESIGNS:
        r = results[d.name][0]
        print(f"- {d.name}: u_ch {r['u']:.3f} m/s, Re {r['Re']:.0f}, h {r['h']/1e3:.1f} kW/m2K, eta {r['eta']:.2f}, "
              f"n_paths {d.n_paths}, dp_ch {r['dp_ch_kPa']:.2f} kPa; {d.dp_note}; deployable: {d.deployable}")
    print()

    print("## 2. Monte Carlo bands (P10 / P50 / P90), 20k samples (Q-cap on 2k)")
    print("| design | avg dT K | max dT K | dP kPa | pump W | Qcap kW |")
    print("|---|---|---|---|---|---|")
    mc = {}
    for d in DESIGNS:
        b = monte_carlo(d)
        mc[d.name] = b
        f = lambda t, n=1: f"{t[0]:.{n}f} / {t[1]:.{n}f} / {t[2]:.{n}f}"
        print(f"| {d.name} | {f(b['dT_avg'])} | {f(b['dT_max'])} | {f(b['dp_kPa'])} | {f(b['pump_W'],2)} | {f(b['Qcap'])} |")
    print()

    print("## 3. Equal-pumping-power operating point (CoolIT-like hydraulic pump power at 18 LPM)")
    print(f"CoolIT-like: {base['pump_W']:.2f} W at 18 LPM, {base['dp_kPa']:.1f} kPa")
    print("| design | LPM/kW | LPM | dP kPa | caloric K | avg dT K | max dT K |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for d in DESIGNS[1:6]:
        e = equal_pump_power_point(d)
        print(f"| {d.name} | {e['lpm_per_kw']:.2f} | {e['flow_lpm']:.1f} | {e['dp_kPa']:.1f} | {e['dT_cal']:.1f} | "
              f"{e['dT_avg']:.1f} | {e['dT_max']:.1f} |")
    print()

    print("## 4. Flow sensitivity (avg / max dT K, dP kPa) - CoolIT-like vs HMMC-R PCM vs HMMC-R LM")
    print("| LPM/kW | LPM | CoolIT-like | HMMC-R PCM | HMMC-R LM |")
    print("|---:|---:|---|---|---|")
    for l in (0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5):
        row = []
        for d in (COOLIT, DESIGNS[2], DESIGNS[3]):
            r = evaluate(d, Q, l)
            row.append(f"{r['dT_avg']:.1f} / {r['dT_max']:.1f} / {r['dp_kPa']:.1f}")
        print(f"| {l:.1f} | {l*15:.0f} | " + " | ".join(row) + " |")
    print()

    print("## 5. Real-package check: reticle die at 350 W/cm2 (H-Z2 zoning, 1 mm base), case dT at hottest die cell")
    print("fit to nonuniform-heatmap sweep: dT_die,max = 33 + 3500/h_eff[kW/m2K] + (R_TIM - 0.05) x 350")
    print("| core | h_eff | paste 0.05 | PCM 0.055 | LM 0.015 | T_case,max with LM (45 C in) |")
    print("|---|---:|---:|---:|---:|---:|")
    for label, d in (("HMMC-R 0.15/0.10x2.0", DESIGNS[2]), ("HMMC-P 0.10/0.10x1.5", DESIGNS[4]),
                     ("HMMC-fine 0.075x1.0 (ref)", DESIGNS[6])):
        he = evaluate(d, Q, lk)["h_eff"] / 1e3
        print(f"| {label} | {he:.0f} | {die_max_dT(he,0.05):.1f} | {die_max_dT(he,0.055):.1f} | {die_max_dT(he,0.015):.1f} | "
              f"{45+die_max_dT(he,0.015):.1f} C |")
    print("CoolIT-like C-x-U (from report): 88.6 K paste, Tcase 134 C; junction adds ~ +17 K (lidded) at 350 W/cm2.")
    print("Direct-to-die removes lid + TIM1 (0.064 + 0.015 cm2K/W = 28 K at 350 W/cm2 at the junction level).")
    print()

    print("## 6. Required manifold branch resistance and orifice sizing (18 LPM, 14 inlet slots)")
    for d in DESIGNS[2:5:2]:
        r = evaluate(d, Q, lk)
        orif = max(0, BRANCH_TARGET - r["dp_ch_kPa"])
        q_slot = 18 / 14 / 60000      # m3/s per slot (half of 28 slot pairs -> 14 inlet slots)
        # orifice comb: 0.5 mm holes, K = 2.8 on hole velocity
        u_o = math.sqrt(2 * orif * 1e3 / (RHO * 2.8)) if orif > 0 else 0
        A_o = q_slot / u_o if u_o > 0 else float("inf")
        n_holes = A_o / (math.pi * (0.25e-3) ** 2)
        print(f"- {d.name.split(',')[0]}: channel {r['dp_ch_kPa']:.2f} kPa -> orifice {orif:.2f} kPa; hole velocity "
              f"{u_o:.2f} m/s, {n_holes:.0f} x 0.5 mm holes per 108 mm slot (pitch {108/max(n_holes,1):.1f} mm)")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
