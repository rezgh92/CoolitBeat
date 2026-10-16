#!/usr/bin/env python3
"""
System-platform (LoopCore) scoping run.

Thermal core = HMMC robust core (0.15 gap / 0.10 fin / 2.0 mm, 4 mm flow length, 1.0 mm tied base),
design-H manifold, but with the platform's interface choices:
  * dual-end ports (2 in / 2 out, 12 mm bore each = 17 mm equivalent single bore),
  * permanent 50 um absolute pleated screen captive in each inlet stub (2 x >= 12 cm2),
  * Tray Fluid Module (TFM): couplings + 50 um service cartridge + thermowells + metering/balancing orifice.
Then: tray-loop budgets, rack manifold uniformity (dividing/combining network), GPU-class plates,
facility-level value for a 100 MW IT site.

Imports the project scoping model unchanged (Darcy-corrected v2).
Run: python3 -I sysplat_run.py
"""
import math
import sys
from dataclasses import replace

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
from coldplate_model import ColdPlate, hmmc, coolit_like, TIM, PG25  # noqa: E402

Q15 = 15000.0
A0 = 117.0
RHO, CP, MU = PG25.rho, PG25.cp, PG25.mu


def lpm_to_m3s(lpm):
    return lpm / 60000.0


# ---------------------------------------------------------------------------
# 1. Plate definitions
# ---------------------------------------------------------------------------
def loopcore15(tim="PCM pad", core="R"):
    p = hmmc(A0, core=core, tim=tim, name=f"LoopCore-15/{core}")
    # dual 16 mm ports (one inlet + one outlet at each end of the centreline headers) -> 22.6 mm equivalent bore;
    # keeps port velocity <= 1.5 m/s up to 36 LPM (2.4 LPM/kW at 15 kW)
    return replace(p, port_bore_mm=16.0 * math.sqrt(2.0))


def screen_kpa(flow_lpm, rated_lpm=18.0, dp_rated=0.30):
    """Two captive 50 um abs pleated screens (>= 12 cm2 each), clean; ~Q^1.5 (transitional)."""
    return dp_rated * (flow_lpm / rated_lpm) ** 1.5


def plate_eval(p, Q, lk, Tin=45.0):
    r = p.evaluate(Q, lk, T_in=Tin)
    r = dict(r)
    if p.name.startswith("LoopCore"):
        r["dp_screen_kPa"] = screen_kpa(r["flow_lpm"], 18.0 * Q / Q15 if Q != Q15 else 18.0)
        r["dp_total_kPa"] += r["dp_screen_kPa"]
        r["pump_W"] = r["dp_total_kPa"] * 1e3 * lpm_to_m3s(r["flow_lpm"])
    return r


def row(r, label=None):
    return (f"| {label or r['name']} | {r['dT_cal']:.1f} | {r['dT_tim']:.1f} | {r['dT_base']:.1f} | {r['dT_conv']:.1f} | "
            f"**{r['dT_avg']:.1f}** | **{r['dT_max']:.1f}** | {r['R_unit_cm2K_W']:.3f} | {r['dp_total_kPa']:.1f} | "
            f"{r['pump_W']:.1f} | {r['Q_cap_kW']:.1f} | {r['T_case_max']:.1f} |")


HDR = ("| design | caloric | TIM | base | conv | avg dT K | max dT K | R'' cm2K/W | plate dP kPa | pump W | Qcap kW | Tcase,max C |\n"
       "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")


def solve_lk(fun, target, lo=0.3, hi=3.0):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if fun(mid) > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# 2. Couplings / tray loop
# ---------------------------------------------------------------------------
def cv_pair_kpa(flow_lpm, cv, n_parallel=1, sg=1.01):
    """Mated supply+return pair(s): dp per coupling = SG (gpm/Cv)^2 psi; pair = 2x; n_parallel pairs share flow."""
    gpm = flow_lpm / 3.785 / n_parallel
    return 2 * sg * (gpm / cv) ** 2 * 6.895


def tray_loop(flow, plate_dp, coupling, orifice_rated_kpa=0.0, rated=18.0, fittings="15mm", hose="5/8"):
    s = flow / rated
    if coupling == "UQD08x1":
        qd = (cv_pair_kpa(flow, 4.0), cv_pair_kpa(flow, 3.0))
    elif coupling == "UQD08x2":
        qd = (cv_pair_kpa(flow, 4.0, 2), cv_pair_kpa(flow, 3.0, 2))
    elif coupling == "3/4in":
        qd = (cv_pair_kpa(flow, 10.0), cv_pair_kpa(flow, 6.0))
    elif coupling == "UQD06x1":
        qd = (cv_pair_kpa(flow, 2.0), cv_pair_kpa(flow, 1.3))
    elif coupling == "UQD04x1":
        qd = (cv_pair_kpa(flow, 0.8), cv_pair_kpa(flow, 0.5))
    else:
        raise ValueError(coupling)
    hose_kpa_per_m = {"1/2": 5.6, "5/8": 1.9, "3/4": 0.8, "3/8": 22.0}[hose] * s ** 1.75
    hose_dp = 1.0 * hose_kpa_per_m  # 1 m total (supply + return)
    fit = {"9.5mm": 36.0, "12mm": 14.0, "15mm": 4.2}[fittings] * s ** 2
    tfm_internal = (0.5 + 0.3) * s ** 1.6  # 50 um cartridge (clean) + thermowells/taps
    orif = orifice_rated_kpa * s ** 2
    lo = qd[0] + hose_dp + fit + tfm_internal + orif + plate_dp
    hi = qd[1] + hose_dp + fit + tfm_internal + orif + plate_dp
    return lo, hi, dict(qd=qd, hose=hose_dp, fit=fit, tfm=tfm_internal, orif=orif, plate=plate_dp)


# ---------------------------------------------------------------------------
# 3. Rack manifold network (dividing supply, combining return), N branches
# ---------------------------------------------------------------------------
def rack_network(N, Q_total_lpm, D_mm, pitch_m, k_branch_kpa_at_rated, rated_lpm, layout="U",
                 theta_d=1.0, theta_c=2.0, iters=400):
    """Branch dp = k*(q/rated)^2. Returns branch flows (LPM). Branch 0 is nearest the inlet of the supply header.
    U: supply in at branch-0 end, return out at branch-0 end (direct return).
    Z: supply in at branch-0 end, return out at the far end (reverse return)."""
    A = math.pi / 4 * (D_mm / 1000) ** 2
    Dh = D_mm / 1000
    q = [Q_total_lpm / N] * N

    def seg_friction(u, L):
        if u <= 0:
            return 0.0
        Re = RHO * u * Dh / MU
        f = 64 / Re if Re < 2300 else 0.316 / Re ** 0.25
        return f * L / Dh * 0.5 * RHO * u * u

    for _ in range(iters):
        # supply header pressures (relative), marching from inlet
        Ps = [0.0] * N
        flow_in = Q_total_lpm
        P = 0.0
        for i in range(N):
            if i > 0:
                u1 = lpm_to_m3s(flow_in) / A
                u2 = lpm_to_m3s(flow_in - 0) / A
                P += -seg_friction(u1, pitch_m)
            Ps[i] = P
            u_before = lpm_to_m3s(flow_in) / A
            flow_in -= q[i]
            u_after = lpm_to_m3s(max(flow_in, 0)) / A
            P += theta_d * 0.5 * RHO * (u_before ** 2 - u_after ** 2)  # static regain at takeoff
        # return header pressures
        Pr = [0.0] * N
        if layout == "U":  # exit at branch-0 end: accumulate from far end toward 0
            flow = 0.0
            P = 0.0
            order = list(range(N - 1, -1, -1))
        else:  # Z: exit at far end, accumulate from 0 toward N-1
            flow = 0.0
            P = 0.0
            order = list(range(N))
        tmp = {}
        for j, i in enumerate(order):
            if j > 0:
                u = lpm_to_m3s(flow) / A
                P -= seg_friction(u, pitch_m)
            u_b = lpm_to_m3s(flow) / A
            flow += q[i]
            u_a = lpm_to_m3s(flow) / A
            P -= theta_c * 0.5 * RHO * (u_a ** 2 - u_b ** 2)
            tmp[i] = P
        # reference so that return pressures are relative to the exit; shift does not matter for differences
        Pr = [tmp[i] for i in range(N)]
        dP = [Ps[i] - Pr[i] for i in range(N)]
        # branch flows from dp = k (q/rated)^2 with a common offset c so that sum q = Q_total
        k = k_branch_kpa_at_rated * 1e3

        def total(c):
            return sum(rated_lpm * math.sqrt(max(d + c, 1e-9) / k) for d in dP)
        lo, hi = -min(dP) + 1e-6, -min(dP) + 50 * k
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if total(mid) > Q_total_lpm:
                hi = mid
            else:
                lo = mid
        c = 0.5 * (lo + hi)
        q_new = [rated_lpm * math.sqrt(max(d + c, 1e-9) / k) for d in dP]
        q = [0.7 * a + 0.3 * b for a, b in zip(q, q_new)]
    hdr_var_kpa = (max(dP) - min(dP)) / 1e3
    return q, hdr_var_kpa


# ---------------------------------------------------------------------------
def main():
    out = []
    P = out.append
    P("# LoopCore system-platform scoping run (project model v2, PG25, 45 C inlet)\n")

    # ---- 1. benchmark point
    P("## 1. 15 kW / 18 LPM / 45 C / 117 cm2\n")
    P(HDR)
    rows = [
        ("CoolIT-like reconstruction (calibration, paste)", coolit_like(A0)),
        ("LoopCore-15/R same paste 0.07 (like-for-like)", loopcore15("paste 0.07")),
        ("LoopCore-15/R PCM pad (Tier 1 drop-in)", loopcore15("PCM pad")),
        ("LoopCore-15/R liquid metal (Tier 2 OEM)", loopcore15("liquid metal")),
        ("LoopCore-15/P PCM (<=33 um loops)", loopcore15("PCM pad", "P")),
        ("LoopCore-15/P liquid metal (<=33 um loops)", loopcore15("liquid metal", "P")),
        ("LoopCore-15/R direct-to-die, 0.8 mm base (Tier 3)", replace(loopcore15("direct-to-die"), base_mm=0.8)),
    ]
    res = {}
    for lab, p in rows:
        r = plate_eval(p, Q15, 1.2)
        res[lab] = r
        P(row(r, lab))
    t1 = res["LoopCore-15/R PCM pad (Tier 1 drop-in)"]
    P(f"\nTier 1 dP split (kPa): channel {t1['dp_ch_kPa']:.2f} + turns {t1['dp_K_kPa']:.2f} + header {t1['dp_header_kPa']:.2f} "
      f"+ orifice comb {t1['dp_orif_kPa']:.2f} + dual 16 mm ports {t1['dp_port_kPa']:.2f} + screens {t1['dp_screen_kPa']:.2f} "
      f"= {t1['dp_total_kPa']:.2f} kPa; port velocity {t1['u_port']:.2f} m/s; channel u {t1['u_ch']:.3f} m/s Re {t1['Re']:.0f}; "
      f"h_eff {t1['h_eff']/1e3:.0f} kW/m2K; NTU {t1['NTU']:.2f}\n")

    # ---- 2. flow sweep
    P("## 2. Flow sweep (avg / max dT K, plate dP kPa, hydraulic W)\n")
    P("| LPM/kW | LPM | CoolIT-like | LoopCore T1 PCM | LoopCore T2 LM | T1 outlet C |")
    P("|---:|---:|---|---|---|---:|")
    for lk in (0.6, 0.75, 0.8, 1.0, 1.2, 1.5, 2.0, 2.4):
        a = plate_eval(coolit_like(A0), Q15, lk)
        b = plate_eval(loopcore15("PCM pad"), Q15, lk)
        c = plate_eval(loopcore15("liquid metal"), Q15, lk)
        P(f"| {lk:.2f} | {a['flow_lpm']:.1f} | {a['dT_avg']:.1f} / {a['dT_max']:.1f} / {a['dp_total_kPa']:.1f} / {a['pump_W']:.1f} | "
          f"{b['dT_avg']:.1f} / {b['dT_max']:.1f} / {b['dp_total_kPa']:.1f} / {b['pump_W']:.1f} | "
          f"{c['dT_avg']:.1f} / {c['dT_max']:.1f} / {c['dp_total_kPa']:.1f} | {45 + b['dT_out']:.1f} |")
    # 2x flow with 16 mm dual ports
    p2 = loopcore15("PCM pad")
    r2 = plate_eval(p2, Q15, 2.4)
    P(f"\n2x flow (36 LPM) with dual 16 mm ports: T1 {r2['dT_avg']:.1f} / {r2['dT_max']:.1f} K, plate dP {r2['dp_total_kPa']:.1f} kPa, "
      f"hydraulic {r2['pump_W']:.1f} W")
    r2b = plate_eval(replace(loopcore15("PCM pad"), port_bore_mm=12.0 * math.sqrt(2)), Q15, 2.4)
    P(f"2x flow (36 LPM) with dual 12 mm ports: plate dP {r2b['dp_total_kPa']:.1f} kPa\n")

    # flow equivalence
    f_avg = solve_lk(lambda lk: plate_eval(loopcore15("PCM pad"), Q15, lk)["dT_avg"], 34.4)
    f_max = solve_lk(lambda lk: plate_eval(loopcore15("PCM pad"), Q15, lk)["dT_max"], 44.2)
    f_avg2 = solve_lk(lambda lk: plate_eval(loopcore15("liquid metal"), Q15, lk)["dT_avg"], 34.4, lo=0.2)
    f_max2 = solve_lk(lambda lk: plate_eval(loopcore15("liquid metal"), Q15, lk)["dT_max"], 44.2, lo=0.15)
    f_avgp = solve_lk(lambda lk: plate_eval(loopcore15("paste 0.07"), Q15, lk)["dT_avg"], 34.4)
    P(f"Flow equivalence (LPM/kW at which LoopCore matches CoolIT 34.4 K avg / 44.2 K max): "
      f"T1 PCM {f_avg:.2f} / {f_max:.2f}; T2 LM {f_avg2:.2f} / {f_max2:.2f}; same paste avg {f_avgp:.2f}")
    for lab, lk in (("T1 at avg-equivalence", f_avg),):
        r = plate_eval(loopcore15("PCM pad"), Q15, lk)
        P(f"  {lab}: {r['flow_lpm']:.1f} LPM, plate dP {r['dp_total_kPa']:.2f} kPa, {r['pump_W']:.2f} W, outlet rise {r['dT_out']:.1f} K")
    # equal pumping power to CoolIT-like at 18 LPM
    pw_ref = plate_eval(coolit_like(A0), Q15, 1.2)["pump_W"]
    lk_eq = solve_lk(lambda lk: -plate_eval(loopcore15("PCM pad"), Q15, lk)["pump_W"], -pw_ref)
    re = plate_eval(loopcore15("PCM pad"), Q15, lk_eq)
    rel = plate_eval(loopcore15("liquid metal"), Q15, lk_eq)
    P(f"Equal hydraulic power to CoolIT-like ({pw_ref:.1f} W): {re['flow_lpm']:.1f} LPM ({lk_eq:.2f} LPM/kW), "
      f"dP {re['dp_total_kPa']:.1f} kPa, T1 {re['dT_avg']:.1f} / {re['dT_max']:.1f} K, T2 {rel['dT_avg']:.1f} / {rel['dT_max']:.1f} K\n")

    # ---- 3. inlet headroom at 15 kW
    P("## 3. Warm-water headroom at 15 kW, 1.2 LPM/kW\n")
    P("| design | max dT K | inlet for Tcase,max = 85 C | avg dT K | inlet for Tcase,avg = 80 C (CoolIT convention) |")
    P("|---|---:|---:|---:|---:|")
    for lab in ("CoolIT-like reconstruction (calibration, paste)", "LoopCore-15/R same paste 0.07 (like-for-like)",
                "LoopCore-15/R PCM pad (Tier 1 drop-in)", "LoopCore-15/R liquid metal (Tier 2 OEM)"):
        r = res[lab]
        P(f"| {lab} | {r['dT_max']:.1f} | {85 - r['dT_max']:.1f} C | {r['dT_avg']:.1f} | {80 - r['dT_avg']:.1f} C |")
    P("Measured CoolIT: max 44.2 K -> 40.8 C; avg 34.4 K -> 45.6 C. Conservative Tier 1 (P90 max 34.5-35 K) -> 50 C.\n")

    # ---- 4. tray loops
    P("## 4. Tray-loop budgets for one 15 kW plate (kPa; low-high from coupling Cv band)\n")
    P("| configuration | 18 LPM | 15 LPM (1.0/kW) | 11.25 LPM (0.75/kW) | 36 LPM (2x) |")
    P("|---|---|---|---|---|")
    cases = [
        ("CoolIT-like + 1x UQD08, 12 mm stubs, 1/2-in hose", "cool", "UQD08x1", 0.0, "12mm", "1/2"),
        ("CoolIT-like + 2x UQD08, 15 mm fittings, 5/8-in hose", "cool", "UQD08x2", 0.0, "15mm", "5/8"),
        ("LoopCore + 1x UQD08, 12 mm stubs, 1/2-in hose", "lc", "UQD08x1", 0.0, "12mm", "1/2"),
        ("LoopCore + 2x UQD08 (dual-end ports), no orifice", "lc", "UQD08x2", 0.0, "15mm", "5/8"),
        ("LoopCore + 2x UQD08 + TFM orifice 10 kPa (recommended)", "lc", "UQD08x2", 10.0, "15mm", "5/8"),
        ("LoopCore + 3/4-in class pair + TFM orifice 10 kPa", "lc", "3/4in", 10.0, "15mm", "3/4"),
    ]
    loop_res = {}
    for lab, kind, cpl, orf, fit, hose in cases:
        cells = []
        for lk in (1.2, 1.0, 0.75, 2.4):
            flow = 15.0 * lk
            if kind == "cool":
                pdp = plate_eval(coolit_like(A0), Q15, lk)["dp_total_kPa"]
            else:
                pdp = plate_eval(loopcore15("PCM pad") if lk < 2 else p2, Q15, lk)["dp_total_kPa"]
            lo, hi, parts = tray_loop(flow, pdp, cpl, orf, fittings=fit, hose=hose)
            cells.append(f"{lo:.0f}-{hi:.0f}")
            loop_res[(lab, lk)] = (lo, hi, parts)
        P(f"| {lab} | " + " | ".join(cells) + " |")
    lo, hi, parts = loop_res[("LoopCore + 2x UQD08 + TFM orifice 10 kPa (recommended)", 1.2)]
    P(f"\nRecommended loop at 18 LPM, parts (kPa): couplings {parts['qd'][0]:.1f}-{parts['qd'][1]:.1f}, hose {parts['hose']:.1f}, "
      f"fittings {parts['fit']:.1f}, TFM cartridge+wells {parts['tfm']:.1f}, orifice {parts['orif']:.1f}, plate {parts['plate']:.1f}\n")

    P(f"Catalogue Cv check, UQD08 pair at 18 LPM: Cv 4.75 (CPC max) {cv_pair_kpa(18,4.75):.1f} kPa; Cv 3.7 (FITOK) {cv_pair_kpa(18,3.7):.1f} kPa; "
      f"dual pairs at 9 LPM each: {cv_pair_kpa(18,4.75,2):.1f}-{cv_pair_kpa(18,3.7,2):.1f} kPa\n")
    # ---- 5. rack network uniformity
    P("## 5. Rack manifold uniformity: 18 trays x 15 kW, 324 LPM at 1.2 LPM/kW, 2U pitch, theta_d 1 / theta_c 2\n")
    P("| branch (rated dP at 18 LPM) | header ID | layout | header dP variation kPa | tray flow max/min | worst tray flow % | T1 max-dT penalty at worst tray K |")
    P("|---|---:|---|---:|---:|---:|---:|")
    base_max = plate_eval(loopcore15("PCM pad"), Q15, 1.2)["dT_max"]
    def mid(lab):
        lo, hi, _ = loop_res[(lab, 1.2)]
        return 0.5 * (lo + hi)
    branch_cases = [(f"CoolIT-like + 1x UQD08 ({mid(cases[0][0]):.0f} kPa)", mid(cases[0][0])),
                    (f"LoopCore + 1x UQD08 ({mid(cases[2][0]):.0f} kPa)", mid(cases[2][0])),
                    (f"LoopCore + 2x UQD08, no orifice ({mid(cases[3][0]):.0f} kPa)", mid(cases[3][0])),
                    (f"LoopCore + 2x UQD08 + 10 kPa orifice ({mid(cases[4][0]):.0f} kPa)", mid(cases[4][0]))]
    for lab, k in branch_cases:
        for D in (50.0, 63.0):
            for lay in ("U", "Z"):
                q, var = rack_network(18, 324.0, D, 0.0889, k, 18.0, layout=lay)
                mx, mn = max(q), min(q)
                worst_lk = mn / 15.0
                pen = plate_eval(loopcore15("PCM pad"), Q15, worst_lk)["dT_max"] - base_max
                P(f"| {lab} | {D:.0f} mm | {lay} | {var:.1f} | {mx/mn:.3f} | {100*mn/18:.1f} % | {pen:+.2f} |")
    P("")

    # ---- 6. mixed rack: GPU branches + low-dP power-shelf branches without/with equal-dP rule
    P("## 6. Mixed loads on one manifold (equal-dP rule)\n")
    # GPU branch rated 31 kPa at 18 LPM; power-shelf plate branch: 2 kW at 0.6 LPM/kW = 1.2 LPM rated, intrinsic 4 kPa
    # Without rule: it sees the same header dP (31 kPa) -> flow = 1.2*sqrt(31/4)
    gb = mid(cases[4][0])
    q_ps = 1.2 * math.sqrt(gb / 4.0)
    P(f"Power-shelf branch (2 kW, rated 1.2 LPM, intrinsic 4 kPa at rated) on a header set for {gb:.0f} kPa GPU branches: "
      f"draws {q_ps:.1f} LPM ({q_ps/1.2:.1f}x rated) unless its TFM orifice adds {gb-4:.0f} kPa at rated flow. "
      f"With 10 power branches per rack that is {10*(q_ps-1.2):.0f} LPM stolen from {324:.0f} LPM of GPU flow "
      f"({100*10*(q_ps-1.2)/324:.0f} %).\n")

    # ---- 7. GPU-class plates (GPU-sized ports and comb: 2 kPa comb at rated flow, 8 mm dual ports, 1 m/s headers)
    P("## 7. GPU-class plates (lidded, uniform heat over the lid footprint)\n")
    P("| case | flow LPM | CoolIT-like paste avg/max | LoopCore T1 PCM avg/max | LoopCore T2 LM avg/max | plate dP CoolIT-like / LoopCore kPa |")
    P("|---|---:|---|---|---|---|")
    gcases = [("B300 1.4 kW, 45 cm2, 1.0 LPM/kW", 1400, 45, 1.0), ("Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW", 2300, 60, 1.0),
              ("Rubin 2.3 kW, 60 cm2, 1.2 LPM/kW", 2300, 60, 1.2), ("Rubin Ultra 3.6 kW, 80 cm2, 1.0 LPM/kW", 3600, 80, 1.0),
              ("CoolIT 4 kW point, 25 cm2, 1.5 LPM/kW", 4000, 25, 1.5)]
    gres = {}
    for lab, Q, A, lk in gcases:
        flow = Q / 1000 * lk
        def gp(tim):
            p = hmmc(A, core="R", tim=tim, name="LoopCore-G")
            return replace(p, port_bore_mm=8.0 * math.sqrt(2), orifice_dp_kPa_18=2.0 * (18.0 / flow) ** 2,
                           header_u_m_s=1.0 * 18.0 / flow)
        a = coolit_like(A).evaluate(Q, lk)
        b = gp("PCM pad").evaluate(Q, lk)
        c = gp("liquid metal").evaluate(Q, lk)
        gres[lab] = (a, b, c)
        P(f"| {lab} | {flow:.1f} | {a['dT_avg']:.1f} / {a['dT_max']:.1f} | {b['dT_avg']:.1f} / {b['dT_max']:.1f} | "
          f"{c['dT_avg']:.1f} / {c['dT_max']:.1f} | {a['dp_total_kPa']:.1f} / {b['dp_total_kPa']:.1f} |")
    # die-zone crude estimate, Rubin 2.3 kW: dies 16.6 cm2 carry 1.94 kW
    P("\nDie-zone estimate, Rubin 2.3 kW (2 dies, 16.6 cm2, 1.94 kW; split-flow passes ~65 % of 2.3 LPM over the dies, "
      "16-20 mm path; LoopCore zoned comb sends 88 %):")
    for lk_tot in (1.0, 1.2):
        f_tot = 2.3 * lk_tot
        a = coolit_like(16.6).evaluate(1940, 0.65 * f_tot / 1.94)
        def gz(tim):
            flow = 0.88 * f_tot
            p = hmmc(16.6, core="R", tim=tim, name="LoopCore-G zone")
            return replace(p, port_bore_mm=8.0 * math.sqrt(2), orifice_dp_kPa_18=2.0 * (18.0 / flow) ** 2,
                           header_u_m_s=1.0 * 18.0 / flow).evaluate(1940, flow / 1.94)
        b, c = gz("PCM pad"), gz("liquid metal")
        P(f"- {lk_tot:.1f} LPM/kW: CoolIT-like paste {a['dT_avg']:.1f} / {a['dT_max']:.1f} K; LoopCore PCM {b['dT_avg']:.1f} / "
          f"{b['dT_max']:.1f} K; LoopCore LM {c['dT_avg']:.1f} / {c['dT_max']:.1f} K (die-zone case-to-inlet, no lateral spreading credit)")
    P("")

    # ---- 8. real package (synthesis fit)
    P("## 8. Real 2027-28 package, hottest die cell (4 x 26 x 33 mm at 350 W/cm2 + 16 HBM, zoned), synthesis fit\n")
    for lab, he in (("robust core R", 127), ("performance core P (die zone only, 25 um loops)", 187)):
        for tl, R in (("PCM", 0.055), ("LM", 0.015)):
            d = 33 + 3500 / he + (R - 0.05) * 350
            P(f"- {lab}, {tl}: {d:.1f} K -> Tcase,max {45 + d:.1f} C")
    P("- CoolIT-like split-flow (paste 0.05, flow over dies then HBM): 88.6 K -> 134 C; with LM ~76 K -> ~121 C\n")

    # ---- 9. facility value, 100 MW IT
    P("## 9. Facility-level value, 100 MW IT liquid-captured\n")
    MW = 100.0
    cdu_lpm = 2400.0  # CHx2000-class secondary flow
    def tcs(lk, tray_mid_kpa):
        Qlpm = MW * 1000 * lk
        # fixed TCS network outside the tray (CDU HX+filter 70 kPa, row piping 50, rack manifold 20) at 1.2 LPM/kW
        ext = (70 + 50 + 20) * (lk / 1.2) ** 2
        dp = ext + tray_mid_kpa
        hyd = lpm_to_m3s(Qlpm) * dp * 1e3 / 1e3   # kW
        return Qlpm, dp, hyd, hyd / 0.6
    # GPU-class realistic: tray loop mid values at 1.2 LPM/kW, scaled
    mA, mB, mR = mid(cases[0][0]), mid(cases[2][0]), mid(cases[4][0])
    scen = [
        (f"A benchmark: CoolIT-like, 1x UQD08, 1.2 LPM/kW (tray {mA:.0f} kPa)", 1.2, mA),
        (f"B LoopCore, 1x UQD08, same 1.2 LPM/kW (tray {mB:.0f})", 1.2, mB),
        ("C LoopCore, 1x UQD08, 1.0 LPM/kW (design point)", 1.0, mB * (1.0 / 1.2) ** 2),
        ("D LoopCore, 1x UQD08, 0.75 LPM/kW (65 C return floor)", 0.75, mB * (0.75 / 1.2) ** 2),
        (f"E LoopCore, 2x UQD08 + metering, 1.0 LPM/kW (tray {mR*(1/1.2)**2:.0f})", 1.0, mR * (1.0 / 1.2) ** 2),
    ]
    P("| scenario | TCS flow LPM | CDUs (2,400 LPM, flow-limited, N) | TCS dP kPa | hydraulic kW | pump electric kW (60 %) | energy GWh/yr | PUE delta vs A |")
    P("|---|---:|---:|---:|---:|---:|---:|---:|")
    base = None
    for lab, lk, tray in scen:
        Qlpm, dp, hyd, el = tcs(lk, tray)
        n = math.ceil(Qlpm / cdu_lpm)
        e = el * 8760 / 1e6   # GWh/yr (kW*h/1e6)
        if base is None:
            base = el
        P(f"| {lab} | {Qlpm:,.0f} | {n} | {dp:.0f} | {hyd:.0f} | {el:.0f} | {e:.2f} | {(el-base)/(MW*1000):+.4f} |")
    P("")
    # supply temperature value
    P("Supply-temperature value (estimates per gap-cost report: US$0.8-2.0 M capex per K per 100 MW of dry cooler, "
      "US$0.16-0.32 M/yr per K trim-chiller energy in hot climates):")
    for lab, dK in (("GPU-class lidded (Rubin 2.3 kW, max dT gain, T1 PCM)", None), ("15 kW-class conservative (P90)", 9.2),
                    ("15 kW-class nominal T1", 13.1), ("15 kW-class T2 LM", 19.2)):
        if dK is None:
            a, b, c = gres["Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW"]
            dK = a["dT_max"] - b["dT_max"]
        cap_lo, cap_hi = 0.8 * dK, 2.0 * dK
        en_lo, en_hi = 0.16 * dK, 0.32 * dK
        P(f"- {lab}: +{dK:.1f} K supply at equal Tcase,max -> US${cap_lo:.1f}-{cap_hi:.1f} M capex + US${en_lo:.2f}-{en_hi:.2f} M/yr (hot climate) per 100 MW")

    # ---- 10. GPU-class tray loop (VR NVL144-like: 4 x 2.3 kW GPU + 2 x 0.5 kW CPU, 1.0 LPM/kW)
    P("\n## 10. GPU-class tray loop (4 x 2.3 kW GPU + 2 x 0.5 kW CPU = 10.2 kW, 1.0 LPM/kW = 10.2 LPM)\n")
    fg = 2.3
    p = hmmc(60, core="R", tim="PCM pad", name="LoopCore-G")
    p = replace(p, port_bore_mm=8.0 * math.sqrt(2), orifice_dp_kPa_18=2.0 * (18.0 / fg) ** 2, header_u_m_s=18.0 / fg)
    pdp = p.evaluate(2300, 1.0)["dp_total_kPa"]
    svc = (cv_pair_kpa(fg, 0.8), cv_pair_kpa(fg, 0.5))      # per-plate UQD04-class service pair
    svc6 = (cv_pair_kpa(fg, 2.0), cv_pair_kpa(fg, 1.3))     # per-plate UQD06-class
    hose = 0.4 * 22.0 * (fg / 18.0) ** 1.75                 # 0.4 m of 3/8-in hose
    br_lo, br_hi = pdp + svc[0] + hose, pdp + svc[1] + hose
    br6_lo, br6_hi = pdp + svc6[0] + hose, pdp + svc6[1] + hose
    ft = 10.2
    tray_qd = (cv_pair_kpa(ft, 4.0), cv_pair_kpa(ft, 3.0))
    orif = 10.0
    tfm = 0.8 * (ft / 18) ** 1.6
    P(f"- GPU plate (LoopCore-G, 60 cm2, 2.3 LPM): {pdp:.1f} kPa port-to-port")
    P(f"- per-plate branch with UQD04-class service pair: {br_lo:.0f}-{br_hi:.0f} kPa; with UQD06-class: {br6_lo:.0f}-{br6_hi:.0f} kPa")
    P(f"- tray UQDB08 pair at {ft} LPM: {tray_qd[0]:.1f}-{tray_qd[1]:.1f} kPa; TFM orifice {orif:.0f} kPa; cartridge+wells {tfm:.1f} kPa")
    P(f"- tray total (UQD04 service pairs): {br_lo + tray_qd[0] + orif + tfm:.0f}-{br_hi + tray_qd[1] + orif + tfm:.0f} kPa; "
      f"(UQD06 service pairs): {br6_lo + tray_qd[0] + orif + tfm:.0f}-{br6_hi + tray_qd[1] + orif + tfm:.0f} kPa")
    vend = 12.0 * (fg / 1.7) ** 1.5
    P(f"- reference: vendor GB300-class skived plate 12 kPa at 1.7 LPM -> ~{vend:.0f} kPa at 2.3 LPM (flow^1.5), no service coupling; "
      f"tray total {vend + hose + tray_qd[0] + tfm:.0f}-{vend + hose + tray_qd[1] + tfm:.0f} kPa without metering")

    # ---- 11. low-profile and P90 flows
    P("\n## 11. Variants\n")
    lp = replace(loopcore15("PCM pad"), fin_h_mm=1.5, orifice_dp_kPa_18=3.2)
    r = plate_eval(lp, Q15, 1.2)
    P(f"- LP18 (fins 1.5 mm, comb 3.2 kPa): {r['dT_avg']:.1f} / {r['dT_max']:.1f} K, plate dP {r['dp_total_kPa']:.1f} kPa, Qcap {r['Q_cap_kW']:.1f} kW")
    d16 = replace(loopcore15("PCM pad"), port_bore_mm=12.0 * math.sqrt(2))
    r = plate_eval(d16, Q15, 1.2)
    P(f"- dual 12 mm ports at 18 LPM: plate dP {r['dp_total_kPa']:.1f} kPa, hydraulic {r['pump_W']:.2f} W")
    for lk in (0.75, 1.0):
        r = plate_eval(loopcore15("PCM pad"), Q15, lk)
        P(f"- T1 at {lk} LPM/kW: {r['dT_avg']:.1f} / {r['dT_max']:.1f} K; +3.4 K P90 penalty -> {r['dT_avg']+3.4:.1f} / {r['dT_max']+3.4:.1f} K")
    r = plate_eval(loopcore15("liquid metal"), Q15, 0.75)
    P(f"- T2 at 0.75 LPM/kW: {r['dT_avg']:.1f} / {r['dT_max']:.1f} K")
    r = plate_eval(loopcore15("PCM pad"), Q15, 1.0, Tin=50.0)
    P(f"- T1 at 1.0 LPM/kW, 50 C inlet: Tcase,max {r['T_case_max']:.1f} C")
    P("\nDone.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
