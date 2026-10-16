#!/usr/bin/env python3
"""
hydraulic-detail.py  --  Independent pressure-drop check: HMMC core vs skived split-flow plate.

Operating point: 15 kW on 108 x 108 mm (117 cm2), PG25 @ ~50 C, 18 LPM nominal (6-36 LPM swept).

Method (component loss network, laminar correlations where Re < ~2000):
  * Fully developed laminar rectangular-duct friction: Fanning f*Re(alpha) from Shah & London (1978)
        dP_fd = 4 f (L/Dh) rho u^2/2 = 2 fRe mu u L / Dh^2   (reduces to Hagen-Poiseuille 32 mu u L/D^2 for fRe=16)
  * Developing-flow (Hagenbach) increment:  dP_dev = K(x+) rho u^2/2,  K(x+) -> K(inf) for x+ = L/(Dh Re) > ~0.05,
        K(inf)(alpha) polynomial fit of Shah & London Table (Steinke & Kandlikar 2006):
        0.6796 + 1.2197a + 3.3089a^2 - 9.5921a^3 + 8.9089a^4 - 2.9959a^5  (0.68 plates ... 1.53 square)
  * Sudden contraction: K_c = 0.5 (1 - sigma) on downstream (higher) velocity, sigma = A_small/A_large
  * Sudden expansion (Borda-Carnot): K_e = (1 - sigma)^2 on upstream (higher) velocity
  * 90-degree sharp turn: K_t = 1.0-1.3 on the higher of the two velocities (1.2 baseline)
  * Dividing / combining manifold channels (laminar): friction = 1/2 of uniform-flow value (flow decays linearly),
    plus entrance K=0.5 (inlet) / exit K=1.0 (outlet) on the entry velocity.
  * Level-1 headers: K=1.5 on header velocity (inlet) and 1.5 (outlet); ports/UQD: 3 kPa @ 18 LPM, quadratic.
Thermal terms are taken unchanged from docs/cooling/model/coldplate_model.py (same series network) so that only
the hydraulics differ; the model's own dp numbers are NOT used (its channel-friction term is 4x low, see check()).
"""
import sys, math
import numpy as np
from scipy.optimize import brentq
from dataclasses import replace

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
import coldplate_model as cpm

RHO, MU, CP, KF = 1005.0, 1.25e-3, 3930.0, 0.52      # PG25 @ ~50 C
Q_W = 15000.0
SIDE = 0.108                                          # m
A_FP = SIDE ** 2                                      # 0.01166 m2 (117 cm2)
LPM = 1.0 / 60.0 / 1000.0                             # m3/s per LPM

def fRe_rect(alpha):
    """Fanning f*Re, rectangular duct, alpha = short/long side (Shah & London)."""
    a = alpha
    return 24 * (1 - 1.3553*a + 1.9467*a**2 - 1.7012*a**3 + 0.9564*a**4 - 0.2537*a**5)

def Kinf_rect(alpha):
    a = alpha
    return 0.6796 + 1.2197*a + 3.3089*a**2 - 9.5921*a**3 + 8.9089*a**4 - 2.9959*a**5

def Kx(alpha, xplus):
    """Hagenbach K(x+) approaching K(inf); simple blend adequate for x+ > 0.02 (our cases are all > 0.3)."""
    Ki = Kinf_rect(alpha)
    return Ki * (1 - math.exp(-xplus / 0.02)) if xplus < 0.2 else Ki

def dyn(u):
    return 0.5 * RHO * u * u

def duct(u, b, H, L, Kinf_override=None):
    """Laminar rectangular duct: returns (dP_fd, dP_dev, Re, Dh, alpha, x+)."""
    Dh = 2 * b * H / (b + H)
    alpha = min(b, H) / max(b, H)
    Re = RHO * u * Dh / MU
    xplus = L / (Dh * Re)
    dp_fd = 2 * fRe_rect(alpha) * MU * u * L / Dh**2
    K = Kinf_override if Kinf_override is not None else Kx(alpha, xplus)
    return dp_fd, K * dyn(u), Re, Dh, alpha, xplus

# ----------------------------------------------------------------------------------------------
def hmmc_dp(lpm, b=0.10e-3, t=0.10e-3, H=1.0e-3, L=2.0e-3, w_s=0.30e-3, t_s=0.5e-3,
            w_m=1.2e-3, d_m=4.0e-3, K_turn=1.2, Kinf_override=None, port_kPa18=3.0,
            K_h=1.5, u_h=1.2, both_ends=True):
    """Hierarchical manifold micro-channel plate. Channels along x (108 mm), inlet/outlet slots run along y,
    alternating with pitch L (inlet-to-outlet). Level-2 manifold channels (w_m x d_m) sit above the slots and
    are fed from their ends by level-1 headers."""
    V = lpm * LPM
    p = b + t
    n_ch = SIDE / p                        # channels across the plate
    n_in = SIDE / (2 * L)                  # inlet slots (each feeds two directions)
    n_paths = n_ch * 2 * n_in              # parallel channel segments
    q_seg = V / n_paths                    # flow per channel segment
    u_c = q_seg / (b * H)                  # channel velocity
    u_s = V / (n_in * w_s * SIDE)          # slot (nozzle) velocity
    u_w = q_seg / (0.5 * w_s * b)          # velocity through the half-window (slot half-width x gap)
    q_m = V / n_in                         # flow per level-2 channel
    u_m = (q_m / 2 if both_ends else q_m) / (w_m * d_m)
    L_m = SIDE / 2 if both_ends else SIDE
    out = {}
    # ports + level-1 headers
    out["port"] = port_kPa18 * 1e3 * (lpm / 18.0) ** 2
    out["L1 header in"] = K_h * dyn(u_h * lpm / 18.0)
    out["L1 header out"] = K_h * dyn(u_h * lpm / 18.0)
    # level-2 manifold channels (dividing / combining)
    fd_m, dev_m, Re_m, Dh_m, al_m, _ = duct(u_m, w_m, d_m, L_m)
    out["L2 manifold in (entr+fric)"] = 0.5 * dyn(u_m) + 0.5 * fd_m
    out["L2 manifold out (fric+exit)"] = 0.5 * fd_m + 1.0 * dyn(u_m)
    # inlet nozzle (slot): contraction from manifold channel, slot friction (parallel plates) + developing
    sig_s = w_s / w_m
    fd_s, dev_s, Re_s, _, _, _ = duct(u_s, w_s, SIDE, t_s)
    out["nozzle in (contr+slot fric)"] = 0.5 * (1 - sig_s) * dyn(u_s) + fd_s + dev_s
    # slot -> channel: contraction into fin gaps (open fraction b/p), 90 deg turn, expansion to channel velocity
    A_w, A_c = 0.5 * w_s * b, b * H
    out["entry: window contr."] = 0.5 * (1 - b / p) * dyn(u_w)
    out["entry: 90deg turn"] = K_turn * dyn(u_w)
    out["entry: expansion"] = (1 - A_w / A_c) ** 2 * dyn(u_w) if A_w < A_c else 0.0
    # channel
    fd_c, dev_c, Re_c, Dh_c, al_c, xp_c = duct(u_c, b, H, L, Kinf_override)
    out["channel fd friction"] = fd_c
    out["channel Hagenbach"] = dev_c
    # channel -> outlet slot: contraction + 90 deg turn
    out["exit: contr. to window"] = 0.5 * (1 - A_w / A_c) * dyn(u_w) if A_w < A_c else 0.0
    out["exit: 90deg turn"] = K_turn * dyn(u_w)
    # outlet nozzle: slot friction + expansion into manifold channel
    out["nozzle out (fric+exp)"] = fd_s + dev_s + (1 - sig_s) ** 2 * dyn(u_s)
    core_keys = [k for k in out if k.startswith(("nozzle", "entry", "channel", "exit"))]
    core = sum(out[k] for k in core_keys)
    total = sum(out.values())
    header_var = max(0.5 * fd_m, 0.5 * dyn(u_m))   # pressure variation along L2 (friction vs momentum, opposite sign)
    return dict(parts=out, core=core, total=total, u_c=u_c, u_s=u_s, u_w=u_w, u_m=u_m, Re_c=Re_c, Re_m=Re_m,
                Re_s=Re_s, Dh_c=Dh_c, xplus=xp_c, Kinf=Kinf_rect(al_c), n_paths=n_paths, header_var=header_var,
                lin_frac=(fd_c + 2 * fd_s + fd_m) / total)

def skived_dp(lpm, b=0.20e-3, t=0.20e-3, H=4.0e-3, L=54e-3, w_in=8e-3, d_in=12e-3, w_out=6e-3, d_out=12e-3,
              K_turn=1.2, Kinf_override=None, port_kPa18=3.0):
    """Skived split-flow plate: central inlet plenum (w_in x d_in) running along y, fed at mid-length (two halves),
    flow turns into channels along +/-x, 54 mm to the edge, turns up into two edge outlet plenums."""
    V = lpm * LPM
    p = b + t
    n_ch = SIDE / p
    q_seg = V / (2 * n_ch)                 # two half-length paths per channel
    u_c = q_seg / (b * H)
    u_pin = (V / 2) / (w_in * d_in)        # inlet plenum, each half carries V/2
    u_pout = (V / 2) / (w_out * d_out)
    u_win = q_seg / (0.5 * w_in * b)       # velocity through half-window under the inlet plenum
    u_wout = q_seg / (w_out * b)
    out = {}
    out["port"] = port_kPa18 * 1e3 * (lpm / 18.0) ** 2
    out["inlet plenum (K=1.0)"] = 1.0 * dyn(u_pin)
    A_win, A_c = 0.5 * w_in * b, b * H
    hi = max(u_win, u_c)
    out["entry: window contr."] = 0.5 * (1 - b / p) * dyn(u_win)
    out["entry: 90deg turn"] = K_turn * dyn(hi)
    out["entry: expansion"] = (1 - A_win / A_c) ** 2 * dyn(u_win) if A_win < A_c else 0.0
    fd_c, dev_c, Re_c, Dh_c, al_c, xp_c = duct(u_c, b, H, L, Kinf_override)
    out["channel fd friction"] = fd_c
    out["channel Hagenbach"] = dev_c
    out["exit: 90deg turn"] = K_turn * dyn(max(u_wout, u_c))
    out["exit: expansion"] = (1 - A_c / (w_out * b)) ** 2 * dyn(u_c) if A_c < w_out * b else 0.0
    out["outlet plenum (K=1.0)"] = 1.0 * dyn(u_pout)
    core_keys = [k for k in out if k.startswith(("entry", "channel", "exit"))]
    core = sum(out[k] for k in core_keys)
    return dict(parts=out, core=core, total=sum(out.values()), u_c=u_c, Re_c=Re_c, Dh_c=Dh_c, xplus=xp_c,
                Kinf=Kinf_rect(al_c), lin_frac=fd_c / sum(out.values()))

# ----------------------------------------------------------------------------------------------
# Thermal: reuse the series model (same assumptions) -- only flow changes along the curves.
HMMC_T = cpm.hmmc_design(117)                                    # 0.1/0.1 x 1.0 mm, L=2 mm, paste 0.05
HMMC_T_F = cpm.hmmc_design(117, fin_t_mm=0.075, gap_mm=0.075, fin_h_mm=1.0, name="HMMC-075")
HMMC_T_U = cpm.hmmc_design(117, fin_t_mm=0.05, gap_mm=0.05, fin_h_mm=1.0, name="HMMC-050")
COOL_T = cpm.coolit_like(117)                                    # 0.2/0.2 x 4 mm, 54 mm, paste 0.07
FINE_T = replace(COOL_T, name="finer skived 0.1/0.1x2", fin_t_mm=0.1, gap_mm=0.1, fin_h_mm=2.0)

def thermal(plate, lpm):
    return plate.evaluate(Q_W, lpm / 15.0)

PLATES = {
    "CoolIT-like skived 0.2/0.2x4, L54": (COOL_T, lambda q, **kw: skived_dp(q, **kw)),
    "finer skived 0.1/0.1x2, L54":       (FINE_T, lambda q, **kw: skived_dp(q, b=0.1e-3, t=0.1e-3, H=2e-3, **kw)),
    "HMMC 0.10 x 1.0 mm, L2":            (HMMC_T, lambda q, **kw: hmmc_dp(q, **kw)),
    "HMMC 0.075 x 1.0 mm, L2":           (HMMC_T_F, lambda q, **kw: hmmc_dp(q, b=0.075e-3, t=0.075e-3, **kw)),
    "HMMC 0.05 x 1.0 mm, L2":            (HMMC_T_U, lambda q, **kw: hmmc_dp(q, b=0.05e-3, t=0.05e-3, **kw)),
}

def check():
    mu, u, L, D = 1.25e-3, 0.5, 0.05, 0.4e-3
    hp = 32 * mu * u * L / D**2
    mine = 2 * 16 * mu * u * L / D**2
    assert abs(hp - mine) / hp < 1e-9
    r = COOL_T.evaluate(Q_W, 1.2)
    s = skived_dp(18.0)
    print(f"check: Hagen-Poiseuille OK; model dp_ch(CoolIT-like)={r['dp_ch_kPa']:.2f} kPa vs this script "
          f"fd={s['parts']['channel fd friction']/1e3:.2f} kPa (ratio {s['parts']['channel fd friction']/1e3/r['dp_ch_kPa']:.2f} "
          f"-> model channel friction is 4x low)\n")

def breakdown(name, res):
    print(f"### {name}  (18 LPM)")
    print("| component | Pa |\n|---|---:|")
    for k, v in res["parts"].items():
        print(f"| {k} | {v:,.0f} |")
    print(f"| **core (fins+nozzles/turns)** | **{res['core']:,.0f}** |")
    print(f"| **total incl. headers+ports** | **{res['total']:,.0f}** |")
    print()

def main():
    global SIDE, MU
    np.set_printoptions(precision=3)
    print("# hydraulic-detail: independent dP check (PG25 @ 50 C, 108x108 mm, 15 kW)\n")
    check()

    print("## 1. Velocities, Reynolds numbers, developing-flow parameters at 18 LPM")
    print("| plate | u_ch m/s | Re_ch | Dh mm | x+ = L/(Dh Re) | K(inf) | u_slot | u_window | u_L2 man. | Re_L2 | parallel paths |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, (pt, fn) in PLATES.items():
        r = fn(18.0)
        if "HMMC" in name:
            print(f"| {name} | {r['u_c']:.3f} | {r['Re_c']:.1f} | {r['Dh_c']*1e3:.3f} | {r['xplus']:.2f} | {r['Kinf']:.2f} | "
                  f"{r['u_s']:.2f} | {r['u_w']:.2f} | {r['u_m']:.2f} | {r['Re_m']:.0f} | {r['n_paths']:,.0f} |")
        else:
            print(f"| {name} | {r['u_c']:.3f} | {r['Re_c']:.0f} | {r['Dh_c']*1e3:.3f} | {r['xplus']:.2f} | {r['Kinf']:.2f} | - | - | - | - | "
                  f"{2*SIDE/(0.4e-3 if '0.2' in name else 0.2e-3):,.0f} |")
    print()

    print("## 2. Component breakdown at 18 LPM")
    breakdown("CoolIT-like skived 0.2/0.2x4 mm, L=54 mm split-flow", skived_dp(18.0))
    breakdown("finer skived 0.1/0.1x2 mm, L=54 mm split-flow", skived_dp(18.0, b=0.1e-3, t=0.1e-3, H=2e-3))
    breakdown("HMMC 0.10/0.10 x 1.0 mm, L=2 mm, 0.3 mm slots, L2 1.2x4 mm fed both ends", hmmc_dp(18.0))

    print("## 3. dP vs flow (kPa) and hydraulic pumping power (W), 6-36 LPM")
    flows = [6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
    print("| LPM | " + " | ".join(f"{n} core / total / W" for n in PLATES) + " |")
    print("|---:|" + "---:|" * len(PLATES))
    curves = {n: [] for n in PLATES}
    for q in flows:
        row = [f"{q}"]
        for n, (pt, fn) in PLATES.items():
            r = fn(float(q))
            W = r["total"] * q * LPM
            curves[n].append((q, r["core"] / 1e3, r["total"] / 1e3, W))
            row.append(f"{r['core']/1e3:.1f} / {r['total']/1e3:.1f} / {W:.2f}")
        print("| " + " | ".join(row) + " |")
    print()

    print("## 4. Thermal-resistance vs pumping-power Pareto (series thermal model, this script's hydraulics)")
    print("| LPM | " + " | ".join(f"{n}: avg dT / max dT / W_pump" for n in PLATES) + " |")
    print("|---:|" + "---:|" * len(PLATES))
    for q in flows:
        row = [f"{q}"]
        for n, (pt, fn) in PLATES.items():
            th = thermal(pt, float(q)); r = fn(float(q))
            row.append(f"{th['dT_avg']:.1f} / {th['dT_max']:.1f} / {r['total']*q*LPM:.2f}")
        print("| " + " | ".join(row) + " |")
    print()

    # crossovers
    cool_name = "CoolIT-like skived 0.2/0.2x4, L54"
    cool18 = skived_dp(18.0); cool_th18 = thermal(COOL_T, 18.0)
    W_cool = cool18["total"] * 18 * LPM
    print("## 5. Equal-dP, equal-pumping-power and equal-dT crossovers vs the CoolIT-like plate at 18 LPM")
    print(f"CoolIT-like @18 LPM: avg dT {cool_th18['dT_avg']:.1f} K, max {cool_th18['dT_max']:.1f} K, "
          f"core {cool18['core']/1e3:.1f} kPa, total {cool18['total']/1e3:.1f} kPa, W_pump {W_cool:.2f} W\n")
    print("| HMMC variant | basis | HMMC flow LPM | LPM/kW | HMMC dP total kPa | W_pump W | caloric K | conv K | avg dT K | max dT K | gain vs CoolIT-like |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for n, (pt, fn) in PLATES.items():
        if "HMMC" not in n:
            continue
        for basis, g in [("equal total dP", lambda q: fn(q)["total"] - cool18["total"]),
                         ("equal core dP", lambda q: fn(q)["core"] - cool18["core"]),
                         ("equal pump power (total)", lambda q: fn(q)["total"] * q * LPM - W_cool),
                         ("equal avg dT (34.5 K)", lambda q: thermal(pt, q)["dT_avg"] - cool_th18["dT_avg"])]:
            try:
                q = brentq(g, 2.0, 120.0)
            except ValueError:
                print(f"| {n} | {basis} | n/a | | | | | | | | |"); continue
            r = fn(q); th = thermal(pt, q); W = r["total"] * q * LPM
            if "dT" in basis:
                gain = f"{W_cool/W:.0f}x less pump power, {18/q:.1f}x less flow"
            else:
                gain = f"-{cool_th18['dT_avg']-th['dT_avg']:.1f} K avg ({(1-th['dT_avg']/cool_th18['dT_avg'])*100:.0f} %)"
            print(f"| {n} | {basis} | {q:.1f} | {q/15:.2f} | {r['total']/1e3:.1f} | {W:.2f} | {th['dT_cal']:.1f} | "
                  f"{th['dT_conv']:.1f} | {th['dT_avg']:.1f} | {th['dT_max']:.1f} | {gain} |")
    print()

    print("## 6. Sensitivities (HMMC 0.10 x 1.0 mm, 18 LPM): core / total kPa")
    print("| case | core kPa | total kPa | u_window m/s | header var./core |")
    print("|---|---:|---:|---:|---:|")
    cases = [
        ("baseline (w_s 0.3, t_s 0.5, L2 1.2x4, K_turn 1.2, K(inf) fit)", dict()),
        ("K_turn 1.0", dict(K_turn=1.0)), ("K_turn 1.3", dict(K_turn=1.3)),
        ("K(inf) = 1.4 (upper bound)", dict(Kinf_override=1.4)),
        ("slot 0.15 mm", dict(w_s=0.15e-3)), ("slot 0.20 mm", dict(w_s=0.20e-3)), ("slot 0.40 mm", dict(w_s=0.40e-3)),
        ("flow length 3 mm", dict(L=3e-3)), ("flow length 4 mm", dict(L=4e-3)),
        ("fin height 0.6 mm", dict(H=0.6e-3)), ("fin height 1.5 mm", dict(H=1.5e-3)),
        ("gap/fin 0.05 x 1.0", dict(b=0.05e-3, t=0.05e-3)), ("gap/fin 0.05 x 0.6", dict(b=0.05e-3, t=0.05e-3, H=0.6e-3)),
        ("L2 manifold 1.2 x 8 mm (u_m halved)", dict(d_m=8e-3)),
        ("L2 fed one end only", dict(both_ends=False)),
        ("L2 one end only + 1.2x8 mm", dict(both_ends=False, d_m=8e-3)),
        ("slot 0.15 + L2 1.2x8 (uniformity fix)", dict(w_s=0.15e-3, d_m=8e-3)),
        ("no ports (core+manifold only)", dict(port_kPa18=0.0)),
        ("headers K 1.5 -> 3.0 @ 1.2 m/s", dict(K_h=3.0)),
    ]
    for label, kw in cases:
        r = hmmc_dp(18.0, **kw)
        print(f"| {label} | {r['core']/1e3:.2f} | {r['total']/1e3:.2f} | {r['u_w']:.2f} | {r['header_var']/r['core']:.2f} |")
    print()
    print("Skived sensitivities (18 LPM): ", end="")
    for label, kw in [("K_turn 1.0", dict(K_turn=1.0)), ("K_turn 1.3", dict(K_turn=1.3)), ("K(inf)=1.4", dict(Kinf_override=1.4)),
                      ("fins 0.25/0.25x4", dict(b=0.25e-3, t=0.25e-3)), ("fins 0.2/0.2x5", dict(H=5e-3)),
                      ("fins 0.15/0.15x3", dict(b=0.15e-3, t=0.15e-3, H=3e-3))]:
        r = skived_dp(18.0, **kw)
        print(f"{label}: {r['core']/1e3:.1f}/{r['total']/1e3:.1f} kPa; ", end="")
    print("\n")

    print("## 7. Manifold flow-uniformity criterion")
    r = hmmc_dp(18.0)
    print(f"Level-2 channel entry velocity {r['u_m']:.2f} m/s, Re {r['Re_m']:.0f}; pressure variation along it "
          f"~{r['header_var']:.0f} Pa (friction {0.5*duct(r['u_m'],1.2e-3,4e-3,SIDE/2)[0]:.0f} Pa vs momentum "
          f"{0.5*dyn(r['u_m']):.0f} Pa, opposite sign) against a branch (core) dP of {r['core']:.0f} Pa -> ratio "
          f"{r['header_var']/r['core']:.2f}. Rule of thumb: ratio <= 0.1-0.2 for <10 % flow non-uniformity.")
    for kw, lab in [(dict(w_s=0.15e-3), "slot 0.15 mm"), (dict(d_m=8e-3), "L2 1.2x8"), (dict(w_s=0.15e-3, d_m=8e-3), "both")]:
        rr = hmmc_dp(18.0, **kw)
        print(f"  {lab}: core {rr['core']:.0f} Pa, header var {rr['header_var']:.0f} Pa, ratio {rr['header_var']/rr['core']:.2f}, total {rr['total']/1e3:.1f} kPa")
    print()

    print("## 8. Scaling check against published manifold-microchannel devices (same correlations)")
    print("Core-only dP predicted by this network for literature-class geometries (volumetric flux j = V/A_fp):")
    lit = [
        ("Escher-class: 2x2 cm, water-like mu, 1.3 LPM, b=0.05, H=0.3, L=1.0, slot 0.10, t_s 0.3", 0.02, 1.3, 0.05e-3, 0.05e-3, 0.3e-3, 1.0e-3, 0.10e-3, 0.3e-3, 0.55e-3),
        ("Drummond/Weibel-class: 3x3 of 5 mm? -> 1.5x1.5 cm, 0.8 LPM, b=0.03, H=0.3, L=0.5, slot 0.1, t_s 0.3", 0.015, 0.8, 0.03e-3, 0.03e-3, 0.3e-3, 0.5e-3, 0.10e-3, 0.3e-3, 0.55e-3),
        ("Jung/Ohadi-class: 1x1 cm, 0.5 LPM, b=0.075, H=0.5, L=1.0, slot 0.15, t_s 0.5", 0.01, 0.5, 0.075e-3, 0.075e-3, 0.5e-3, 1.0e-3, 0.15e-3, 0.5e-3, 0.55e-3),
        ("this work: 10.8x10.8 cm, 18 LPM PG25, b=0.10, H=1.0, L=2, slot 0.3, t_s 0.5", SIDE, 18.0, 0.1e-3, 0.1e-3, 1.0e-3, 2.0e-3, 0.3e-3, 0.5e-3, MU),
    ]
    print("| case | j cm/s | u_ch m/s | Re_ch | u_window m/s | core dP kPa |\n|---|---:|---:|---:|---:|---:|")
    S0, M0 = SIDE, MU
    for label, side, lpm, b, t, H, L, ws, ts, mu in lit:
        SIDE, MU = side, mu
        rr = hmmc_dp(lpm, b=b, t=t, H=H, L=L, w_s=ws, t_s=ts, w_m=max(4*ws, 0.5e-3), d_m=max(2e-3, side/20), port_kPa18=0.0, K_h=0.0)
        j = lpm * LPM / side**2
        print(f"| {label} | {j*100:.1f} | {rr['u_c']:.2f} | {rr['Re_c']:.0f} | {rr['u_w']:.2f} | {rr['core']/1e3:.1f} |")
    SIDE, MU = S0, M0
    print()
    # Save curves
    import csv
    with open(__import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'hydraulic-detail-curves.csv')), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["plate", "LPM", "core_kPa", "total_kPa", "W_pump", "dT_avg", "dT_max"])
        for n, (pt, fn) in PLATES.items():
            for q, c, tt, W in curves[n]:
                th = thermal(pt, float(q)); w.writerow([n, q, f"{c:.3f}", f"{tt:.3f}", f"{W:.3f}", f"{th['dT_avg']:.2f}", f"{th['dT_max']:.2f}"])

if __name__ == "__main__":
    main()
