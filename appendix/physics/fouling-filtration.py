#!/usr/bin/env python3
"""
fouling-filtration.py  --  Fouling / clogging / filtration check for fine micro-channel
cold plates (HMMC candidate) in today's data-centre DLC loops.

Operating point (CoolIT 15 kW brief): 15 kW, 18 LPM PG25, 45 C inlet, 117 cm2 footprint,
128 W/cm2.  Fluid PG25 @ 50 C: rho 1005, cp 3930, mu 1.25e-3, k 0.52.  Cu k = 390.

Sections
  A  particle classes, Stokes settling, entry Stokes number, shear-removal vs adhesion
  B  channel-width / filter-rating regime table (bridging, sieving)
  C  inlet-screen pressure drop (Brundrett-type screen correlation cross-checked with Ergun)
     vs screen area and clog state; area needed for < 2 kPa
  D  uniform fouling-layer sensitivity vs channel width (dP ratio, dT penalty)
  E  10 % blocked channels: global hydraulics + local hot spot (1-D strip, 2-D disc)
  F  fouling-tolerant HMMC variants vs CoolIT-like, through the project 1-D model
  G  self-flushing header bleed sizing; screen pore-count capacity vs channel inlets

All literature numbers are 'working assumptions' (web search budget was exhausted in this
run, so nothing here was re-verified online) and are tagged with a confidence level.
"""
from __future__ import annotations
import math, sys
import numpy as np
from scipy.special import k0, k1

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
import coldplate_model as cm  # project scoping model

# ----------------------------------------------------------------------------- fluid / point
rho, cp, mu, kf = 1005.0, 3930.0, 1.25e-3, 0.52
k_cu = 390.0
g = 9.81
Q = 15000.0
LPM = 18.0
Vdot = LPM / 60 / 1000            # m3/s
A_fp = 117e-4                     # m2
side = math.sqrt(A_fp)            # m
q = Q / A_fp                      # W/m2  (128 W/cm2)

print("=" * 100)
print("A. PARTICLE CLASSES, SETTLING, ENTRY IMPACTION, SHEAR REMOVAL")
print("=" * 100)
# (name, density kg/m3, typical size range um, source/notes, confidence)
particles = [
    ("Cu oxide flakes (Cu2O/CuO)",        6000, (1, 50),    "corrosion / galvanic Cu; colloid 0.1-10 um, flakes to 50 um", "med"),
    ("Al(OH)3 / Al oxide (mixed-metal)",   2400, (1, 100),   "Al components in Cu loop; gelatinous, sticky",                "med"),
    ("Brazing residue / flux / Cu chips",  3000, (10, 500),  "manufacturing; removed by factory flush, residual <1 mg/plate","med"),
    ("Ni plating debris / flakes",         8900, (1, 200),   "bath particulate 1-50 um, peel flakes 50-200 um",             "med"),
    ("EPDM / elastomer shedding",          1100, (10, 300),  "hoses, UQD seals; soft, deformable, passes nominal filters", "high"),
    ("PTFE tape / thread sealant",         2200, (100, 2000),"installation debris; classic strainer catch",               "high"),
    ("Glycol inhibitor precipitate",       2000, (1, 20),    "silicate/phosphate gels if hard make-up water; azole-Cu",     "med"),
    ("Biofilm flocs",                      1050, (20, 1000), "sloughed biofilm; sticky, low density, deformable",           "med"),
    ("CaCO3 / silica scale",               2700, (1, 10),    "hard make-up water; deposits rather than transports",          "high"),
]

def v_stokes(d, rho_p):
    return (rho_p - rho) * g * d**2 / (18 * mu)

print("\nStokes settling velocity (mm/s) and settling parameter")
print("| particle | rho | d=10um | d=25um | d=50um | d=100um |")
print("|---|---:|---:|---:|---:|---:|")
for name, rp, rng, src, conf in particles:
    row = [f"{v_stokes(d*1e-6, rp)*1e3:.3f}" for d in (10, 25, 50, 100)]
    print(f"| {name} | {rp} | " + " | ".join(row) + " |")

# residence times: HMMC channel (L 2 mm, u ~0.5 m/s) vs header (u 1 m/s, L ~ 54 mm) vs rack manifold (u 0.5 m/s, 2 m)
# settling distance = v_s * t_res ; compare with channel height (1 mm) or header depth (3 mm)
print("\nSettling distance during transit (um) for a 50 um Cu-oxide particle:")
vs50 = v_stokes(50e-6, 6000)
for label, u, L, depth in [("HMMC channel (L=2 mm, u=0.5 m/s, H=1 mm)", 0.5, 2e-3, 1e-3),
                           ("inlet slot / header (L=54 mm, u=1 m/s, depth 3 mm)", 1.0, 54e-3, 3e-3),
                           ("slot dead-end (u->0.05 m/s over last 5 mm)", 0.05, 5e-3, 3e-3),
                           ("rack manifold (L=2 m, u=0.5 m/s, D=25 mm)", 0.5, 2.0, 25e-3)]:
    t = L / u
    print(f"  {label:<55s} t_res={t*1e3:7.1f} ms  settles {vs50*t*1e6:7.1f} um  ({vs50*t/depth*100:5.1f} % of depth)")

# Stokes number at channel entry (90-degree turn from slot into channel of width W)
print("\nEntry Stokes number St = rho_p d^2 u / (18 mu W)  (St > ~0.3-1 -> inertial impaction on fin tips)")
print("| d (um) | rho_p | W=0.05 | W=0.075 | W=0.1 | W=0.15 | W=0.2 mm |")
print("|---:|---:|---:|---:|---:|---:|---:|")
u_ch = 0.5
for d in (10, 25, 50, 100):
    for rp in (1100, 6000):
        row = [f"{rp*(d*1e-6)**2*u_ch/(18*mu*W*1e-3):.2f}" for W in (0.05, 0.075, 0.1, 0.15, 0.2)]
        print(f"| {d} | {rp} | " + " | ".join(row) + " |")

def channel_hydraulics(b, H, u):
    alpha = min(b, H) / max(b, H)
    Dh = 2 * b * H / (b + H)
    fRe = 24 * (1 - 1.3553 * alpha + 1.9467 * alpha**2 - 1.7012 * alpha**3 + 0.9564 * alpha**4 - 0.2537 * alpha**5)
    dpdx = fRe * mu * u / (2 * Dh**2)
    tau_w = dpdx * Dh / 4
    return Dh, fRe, dpdx, tau_w

# wall shear in a channel and drag on an attached particle vs adhesion.
# Channel velocity comes from the project model (HMMC: ~29 000 parallel 2 mm segments -> u ~ 0.1 m/s;
# CoolIT-like split-flow 0.2x4 mm: u ~ 0.7 m/s).
def model_u(gap, fin, H, L=2.0, hmmc=True):
    if hmmc:
        return cm.hmmc_design(117.0, fin_t_mm=fin, gap_mm=gap, fin_h_mm=H, flow_len_mm=L).evaluate(Q, 1.2)["u_ch"]
    return cm.coolit_like(117.0).evaluate(Q, 1.2)["u_ch"]

print("\nWall shear and hydrodynamic drag on a wall-attached particle (O'Neill: F = 1.7*6*pi*mu*a*gamma*a) vs adhesion")
print("(JKR adhesion 1.5*pi*W_A*a with W_A,eff = 1.5e-3 J/m2 for rough particles in water; smooth would be ~30x higher)")
print("| geometry | W (mm) | H (mm) | u (m/s) | tau_w (Pa) | gamma (1/s) | F_drag 10um (nN) | F_drag 50um (nN) | F_adh 10um (nN) | F_adh 50um (nN) |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
W_A_eff = 1.5e-3
geos = [("HMMC", 0.05, 0.05, 0.6, True), ("HMMC", 0.075, 0.075, 0.8, True), ("HMMC", 0.1, 0.1, 1.0, True),
        ("HMMC", 0.15, 0.1, 1.5, True), ("HMMC", 0.15, 0.1, 2.0, True), ("HMMC", 0.2, 0.15, 2.5, True),
        ("CoolIT-like split-flow", 0.2, 0.2, 4.0, False)]
u_by_geom = {}
for name, W, fin, H, hm in geos:
    u = model_u(W, fin, H, hmmc=hm)
    u_by_geom[(W, H)] = u
    Dh, fRe, dpdx, tau = channel_hydraulics(W*1e-3, H*1e-3, u)
    gam = tau / mu
    row = []
    for d in (10e-6, 50e-6):
        a = d / 2
        Fd = 1.7009 * 6 * math.pi * mu * a * (gam * a)
        Fa = 1.5 * math.pi * W_A_eff * a
        row += [Fd * 1e9, Fa * 1e9]
    print(f"| {name} | {W} | {H} | {u:.2f} | {tau:.1f} | {gam:.0f} | {row[0]:.1f} | {row[2]:.1f} | {row[1]:.1f} | {row[3]:.1f} |")

print("\nEntry Stokes number at the model velocities (slot -> channel 90-degree turn), 50 um Cu oxide / 50 um EPDM:")
for name, W, fin, H, hm in geos:
    u = u_by_geom[(W, H)]
    st_cu = 6000 * (50e-6)**2 * u / (18 * mu * W * 1e-3)
    st_ep = 1100 * (50e-6)**2 * u / (18 * mu * W * 1e-3)
    print(f"  {name:<24s} W={W} u={u:.2f} m/s: St(50um Cu-ox)={st_cu:.2f}, St(50um EPDM)={st_ep:.2f}")

print("\n" + "=" * 100)
print("B. CHANNEL WIDTH vs FILTER RATING: W/d regimes")
print("=" * 100)
# Filter cases: (label, absolute pass size um, confidence/notes)
filters = [
    ("25 um absolute (pleated, beta>=200)", 25,  "emerging spec for microchannel GPU plates (unverified: recalled for GB200-class guidance)"),
    ("50 um absolute mesh strainer",       50,  "rigid particles only; fibres/soft particles pass"),
    ("50 um nominal (typical CDU/rack)",   90,  "nominal ~85-95 % @50 um -> absolute ~1.5-2x => ~75-100 um"),
    ("100 um nominal / Y-strainer",        180, "coarse facility-side or legacy"),
]
widths = [0.05, 0.075, 0.1, 0.15, 0.2, 0.3]
def regime(r):
    if r < 1:   return "SIEVE (immediate)"
    if r < 3:   return "BRIDGING (fast)"
    if r < 7:   return "deposition clog (slow)"
    return "safe (dilute)"
print("\nW/d_abs and regime (W = channel width; d_abs = largest particle the upstream filter passes)")
print("| filter | d_abs um | " + " | ".join(f"W={w}" for w in widths) + " |")
print("|---|---:|" + "---:|" * len(widths))
for lab, d, note in filters:
    cells = []
    for w in widths:
        r = w * 1e3 / d
        cells.append(f"{r:.1f} {regime(r)}")
    print(f"| {lab} | {d} | " + " | ".join(cells) + " |")
print("Min channel width by the W >= 3 d_abs rule:")
for lab, d, note in filters:
    print(f"  {lab:<40s}: W_min = {3*d/1e3:.3f} mm   ({note})")

L_flow = 2.0e-3
n_slots = int(round(side / (2 * L_flow)))        # 27 inlet slots
n_paths = 2 * n_slots                             # 54 channel segments along the flow direction
# Successive-deposition clogging (Wyss et al. 2006, PRE 74 061402; Dressaire & Sauret 2017 review):
# a channel of width W clogs after N* ~ C (W/d)^4 particles of size d have passed (sticky particles, W/d ~ 2.5-6).
# Particle budget: ISO-4406-like cumulative distribution N(>d) = c14 (d/14um)^-2.2 per mL, truncated at the
# absolute pass size d_abs of the upstream filter.  Only particles with d > W/6 can take part (W/d < 6).
# Representative participating size d_rep = max(W/6, 14 um)... use the count-weighted size ~ W/5.
print("\nTime-to-clog by successive deposition (C = 30; c14 = count/mL of particles > 14 um; slope -2.2)")
print("Loop cleanliness labels: 'very clean' c14=0.1/mL (ISO ~ -/-/4), 'typical' 1/mL (ISO ~ -/-/7), 'dirty' 10/mL (ISO ~ -/-/11)")
print("| W (mm) | inlets | q/ch mL/min | d_abs um | d_min=W/6 um | N(>d_min)/mL @c14=1 | N* | years to clog @c14 = 0.1 / 1 / 10 |")
print("|---:|---:|---:|---:|---:|---:|---:|---|")
C_wyss = 30.0
def n_gt(d_um, c14, d_abs):
    if d_um >= d_abs:
        return 0.0
    return c14 * ((d_um / 14.0) ** -2.2 - (d_abs / 14.0) ** -2.2)
for W in (0.05, 0.075, 0.1, 0.15, 0.2, 0.3):
    pitch = (W + min(W, 0.15)) * 1e-3
    n_inlets = (side / pitch) * n_paths
    q_ch = Vdot / n_inlets
    for d_abs in (25, 50, 90):
        d_min = max(W * 1e3 / 6.0, 4.0)
        d_rep = max(W * 1e3 / 5.0, 5.0)
        Nstar = C_wyss * (W * 1e3 / d_rep) ** 4
        cells = []
        for c14 in (0.1, 1.0, 10.0):
            n = n_gt(d_min, c14, d_abs)
            if n <= 0:
                cells.append("none (W>6 d_abs)")
            else:
                rate = q_ch * 1e6 * 60 * 525960 * n   # particles per year
                cells.append(f"{Nstar / rate:.1f}")
        print(f"| {W} | {n_inlets:.0f} | {q_ch*6e7:.3f} | {d_abs} | {d_min:.1f} | {n_gt(d_min, 1.0, d_abs):.3f} | {Nstar:.0f} | " + " / ".join(cells) + " |")
print("Note: N* law validated for W/d 2.5-6 with sticky monodisperse particles; C is uncertain by 10x either way, so")
print("treat 'years' as order-of-magnitude.  'none' means no particle in the loop is large enough to trigger the mechanism.")

# Field calibration: the industry runs 0.2 mm skived channels behind 50 um nominal (~90 um abs) filters for
# ~10 years, so set the reference life of (W=0.2, d_abs=90) to 10 y and express every other case relative to it.
# Relative life = [q_ch * N(>W/6, d_abs)]_ref / [q_ch * N(>W/6, d_abs)]_case  (C and c14 cancel).
print("\nDeposition-clogging life RELATIVE to a field-proven 0.2 mm skived channel on a 50 um nominal loop (= 10 y reference)")
print("| W (mm) | loop/plate filter 90 um abs (50 nominal) | 50 um abs | 33 um abs | 25 um abs |")
print("|---:|---:|---:|---:|---:|")
def rate(W, d_abs):
    pitch = (W + min(W, 0.15)) * 1e-3
    n_inlets = (side / pitch) * n_paths
    q_ch = Vdot / n_inlets
    return q_ch * n_gt(max(W * 1e3 / 6.0, 4.0), 1.0, d_abs)
ref = rate(0.2, 90)
for W in (0.05, 0.075, 0.1, 0.15, 0.2, 0.3):
    cells = []
    for d_abs in (90, 50, 33, 25):
        r = rate(W, d_abs)
        cells.append("no mechanism" if r <= 0 else f"{ref/r:.2f}x ({10*ref/r:.0f} y)")
    print(f"| {W} | " + " | ".join(cells) + " |")

print("\n" + "=" * 100)
print("C. INLET SCREEN PRESSURE DROP")
print("=" * 100)
# plain-weave mesh definitions: (label, opening um, wire um)
meshes = [("25 um", 25, 25), ("50 um", 50, 36), ("100 um", 100, 65)]

def screen_dp_brundrett(u_s, d_w, beta, frac_open=1.0):
    """Brundrett-type square-mesh screen loss coefficient on approach velocity:
    K = (7.125/Re + 0.88/ln(Re+1.25) + 0.055 log10 Re) (1-beta)/beta^2,  Re = rho u_s d_w / (mu beta).
    frac_open < 1 models clogged pores (effective open area reduced)."""
    b = beta * frac_open
    Re = rho * u_s * d_w / (mu * b)
    K = (7.125 / Re + 0.88 / math.log(Re + 1.25) + 0.055 * math.log10(Re)) * (1 - b) / b**2
    return K * 0.5 * rho * u_s**2, Re, K

def screen_dp_ergun(u_s, d_w, p, frac_open=1.0):
    """Ergun on the mesh as a thin packed bed: eps = 1 - pi d_w/(4 p), L = 2 d_w, d_eq = 1.5 d_w.
    Clogging: reduce eps by the same fraction of blocked void."""
    eps = 1 - math.pi * d_w / (4 * p)
    eps = eps * frac_open
    L = 2 * d_w
    dp_ = 1.5 * d_w
    dpdx = 150 * mu * (1 - eps)**2 * u_s / (eps**3 * dp_**2) + 1.75 * rho * (1 - eps) * u_s**2 / (eps**3 * dp_)
    return dpdx * L, eps

print("\nClean-screen dP at 18 LPM vs screen area (Brundrett-type / Ergun cross-check)")
print("| mesh | open area | area cm2 | u_s m/s | Re_d | K | dP Brundrett kPa | dP Ergun kPa |")
print("|---|---:|---:|---:|---:|---:|---:|---:|")
areas = [1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 117.0]
for lab, op, dw in meshes:
    p = (op + dw) * 1e-6
    beta = (op / (op + dw))**2
    for A in areas:
        u_s = Vdot / (A * 1e-4)
        dpb, Re, K = screen_dp_brundrett(u_s, dw * 1e-6, beta)
        dpe, eps = screen_dp_ergun(u_s, dw * 1e-6, p)
        print(f"| {lab} | {beta:.2f} | {A:.0f} | {u_s:.3f} | {Re:.1f} | {K:.1f} | {dpb/1e3:.3f} | {dpe/1e3:.3f} |")

print("\nMinimum screen area for dP < 2 kPa (clean) and < 2 kPa at 50 % pores blocked (Brundrett-type, conservative = max of the two models)")
for lab, op, dw in meshes:
    p = (op + dw) * 1e-6
    beta = (op / (op + dw))**2
    for frac in (1.0, 0.5, 0.2):
        A = 0.3
        while True:
            u_s = Vdot / (A * 1e-4)
            dpb, _, _ = screen_dp_brundrett(u_s, dw * 1e-6, beta, frac)
            dpe, _ = screen_dp_ergun(u_s, dw * 1e-6, p, frac)
            if max(dpb, dpe) < 2000:
                break
            A *= 1.05
        print(f"  {lab} mesh, open fraction {frac:.1f}: A_min = {A:6.1f} cm2 (u_s = {Vdot/(A*1e-4):.3f} m/s)")

print("\nClog progression for a 25 um full-plate screen (117 cm2) and a 5 cm2 port cartridge (50 um):")
for lab, op, dw, A in [("25 um", 25, 25, 117.0), ("25 um", 25, 25, 10.0), ("50 um", 50, 36, 5.0)]:
    p = (op + dw) * 1e-6
    beta = (op / (op + dw))**2
    u_s = Vdot / (A * 1e-4)
    row = []
    for frac in (1.0, 0.8, 0.5, 0.2, 0.1):
        dpb, _, _ = screen_dp_brundrett(u_s, dw * 1e-6, beta, frac)
        dpe, _ = screen_dp_ergun(u_s, dw * 1e-6, p, frac)
        row.append(f"{max(dpb, dpe)/1e3:.2f}")
    n_pores = A * 1e-4 / p**2
    print(f"  {lab} @ {A:.0f} cm2: pores = {n_pores:.2e}; dP kPa at open fraction 1/0.8/0.5/0.2/0.1 = " + " / ".join(row))

print("\nScreen loading timeline: days to 50 % pore blockage (1 particle > rating = 1 blocked pore; conservative)")
print("| screen | pores | capacity (50 %) | c(>rating) = 1e-4/mL | 1e-3/mL | 1e-2/mL | 1e-1/mL |")
print("|---|---:|---:|---:|---:|---:|---:|")
for lab, op, dw, A in [("25 um @117 cm2", 25, 25, 117.0), ("25 um @10 cm2", 25, 25, 10.0), ("50 um @117 cm2", 50, 36, 117.0), ("50 um @5 cm2", 50, 36, 5.0)]:
    p = (op + dw) * 1e-6
    n_pores = A * 1e-4 / p**2
    cap = 0.5 * n_pores
    cells = []
    for c in (1e-4, 1e-3, 1e-2, 1e-1):
        per_day = c * Vdot * 1e6 * 86400
        cells.append(f"{cap/per_day:.0f}")
    print(f"| {lab} | {n_pores:.1e} | {cap:.1e} | " + " | ".join(cells) + " |")
print("(for reference: an ISO-like loop with c14 = 1/mL has c(>25 um) ~ 0.28/mL and c(>50 um) ~ 0.06/mL BEFORE the loop filter;")
print(" steady-state after a 50 um nominal filter with ~1 loop turnover/min is generation-limited and typically 10-1000x lower)")

print("\n" + "=" * 100)
print("D. UNIFORM FOULING LAYER SENSITIVITY vs CHANNEL WIDTH (HMMC geometry, fixed flow)")
print("=" * 100)
# Use the project model for each width, then compute the fouled state by shrinking b and H by delta (both walls),
# adding a fouling conduction resistance on the wetted area, keeping total flow fixed.
def hmmc_eval(gap, fin, H, delta=0.0, k_foul=0.6, L=2.0, tim=0.05, lpm_kw=1.2):
    base = cm.hmmc_design(117.0, fin_t_mm=fin, gap_mm=gap, fin_h_mm=H, flow_len_mm=L, tim_R=tim)
    r0 = base.evaluate(Q, lpm_kw)
    if delta == 0:
        return r0, 0.0, 1.0
    b_f = gap - 2 * delta * 1e3
    H_f = H - delta * 1e3
    if b_f <= 0.005:
        return None, None, None
    fouled = cm.replace(base, gap_mm=b_f, fin_h_mm=H_f)
    r1 = fouled.evaluate(Q, lpm_kw)
    # fouling conduction resistance per unit footprint: delta/(k_f * wetted area ratio)
    R_f = delta / (k_foul * r1["area_ratio"])
    dT_f = q * R_f
    dT_avg = r1["dT_avg"] + dT_f
    return r1, dT_avg - r0["dT_avg"], r1["dp_total_kPa"] / r0["dp_total_kPa"]

print("| gap/fin/H (mm) | clean avg dT K | clean dP kPa | delta=5um: ddT K, dP x | delta=10um | delta=20um | delta=30um |")
print("|---|---:|---:|---:|---:|---:|---:|")
geoms = [(0.05, 0.05, 0.6), (0.075, 0.075, 0.8), (0.1, 0.1, 1.0), (0.15, 0.1, 1.5), (0.15, 0.15, 2.0), (0.2, 0.15, 2.0), (0.2, 0.2, 4.0)]
for gap, fin, H in geoms:
    r0, _, _ = hmmc_eval(gap, fin, H)
    cells = []
    for dl in (5e-6, 10e-6, 20e-6, 30e-6):
        r1, ddT, ratio = hmmc_eval(gap, fin, H, dl)
        cells.append("blocked" if r1 is None else f"+{ddT:.1f} K, x{ratio:.2f}")
    print(f"| {gap}/{fin}/{H} | {r0['dT_avg']:.1f} | {r0['dp_total_kPa']:.1f} | " + " | ".join(cells) + " |")
print("(dP ratio is at fixed 18 LPM; the HMMC channel term is a minority of plate dP, so ratios understate the channel-only effect)")
print("Channel-only laminar dP ratio (b/(b-2 delta))^3 for parallel-plate-like channels:")
for gap in (0.05, 0.075, 0.1, 0.15, 0.2):
    print(f"  b={gap} mm: " + ", ".join(f"d={dl}um x{(gap/(gap-2*dl*1e-3))**3:.2f}" for dl in (5, 10, 20) if gap - 2*dl*1e-3 > 0))

print("\n" + "=" * 100)
print("E. 10 % OF CHANNELS BLOCKED: GLOBAL HYDRAULICS AND LOCAL HOT SPOT")
print("=" * 100)
r_h = cm.hmmc_design(117.0).evaluate(Q, 1.2)
r_c = cm.coolit_like(117.0).evaluate(Q, 1.2)
print(f"HMMC baseline: avg dT {r_h['dT_avg']:.1f} K, conv {r_h['dT_conv']:.1f} K, dP {r_h['dp_total_kPa']:.1f} kPa (channel term {r_h['dp_ch_kPa']+r_h['dp_K_kPa']:.1f} kPa)")
# global: 10 % blocked -> remaining channels carry 1/0.9 flow (fixed-flow CDU) ; laminar channel dP x1.11, K-term x1.23
f_open = 0.9
dp_ch_new = (r_h['dp_ch_kPa'] / f_open) + r_h['dp_K_kPa'] / f_open**2
dp_new = dp_ch_new + r_h['dp_slot_kPa'] + r_h['dp_man_kPa'] + 4.0
print(f"  fixed flow: plate dP {r_h['dp_total_kPa']:.2f} -> {dp_new:.2f} kPa (+{(dp_new/r_h['dp_total_kPa']-1)*100:.0f} %)")
# fixed-dP branch with plate 6 kPa out of 50 kPa branch: flow reduction
for branch in (30.0, 50.0, 100.0):
    R_frac = r_h['dp_total_kPa'] / branch
    flow_ratio = 1 / (1 - R_frac + R_frac * dp_new / r_h['dp_total_kPa'])   # laminar-ish
    print(f"  fixed branch dP {branch:.0f} kPa (plate {R_frac*100:.0f} % of branch): plate flow -> {flow_ratio*100:.1f} %")

# flow-distribution robustness: channel+slot dP vs manifold dynamic head
dyn_head = 0.5 * rho * 1.0**2
ch_term = (r_h['dp_ch_kPa'] + r_h['dp_K_kPa'] + r_h['dp_slot_kPa']) * 1e3
print(f"  distribution check: channel+slot dP = {ch_term:.0f} Pa vs header dynamic head 0.5 rho u^2 = {dyn_head:.0f} Pa "
      f"(ratio {ch_term/dyn_head:.2f}; >= 3-5 wanted for even distribution -> add per-slot metering orifices ~1-2 kPa)")

# local hot spot: base spreading model. h_eff on footprint from conv term
h_eff = q / r_h['dT_conv']
t_b = 1.0e-3
m = math.sqrt(h_eff / (k_cu * t_b))
print(f"\nBase-spreading model: h_eff = {h_eff/1e3:.0f} kW/m2K on footprint, base 1 mm Cu, m = {m:.0f} 1/m (1/m = {1/m*1e3:.2f} mm)")
print("Excess hot-spot temperature above the unblocked case temperature:")
print("| blocked region | strip half-width a (mm) | 1-D strip dT_excess K | 2-D disc dT_excess K |")
print("|---|---:|---:|---:|")
cases = [("one channel (0.1 mm gap)", 0.1e-3), ("3 channels (0.6 mm)", 0.3e-3), ("one slot segment (2 mm)", 1.0e-3),
         ("cluster 4 mm", 2.0e-3), ("cluster 10 mm", 5.0e-3), ("10 % of plate as a strip (10.8 mm)", 5.4e-3),
         ("10 % of plate as a disc (r=6.1 mm)", 6.1e-3)]
for lab, a in cases:
    strip = q * a / (k_cu * t_b * m) + q * a**2 / (2 * k_cu * t_b)
    disc = q * a**2 / (4 * k_cu * t_b) + q * a / (k_cu * t_b * m) * k0(m * a) / k1(m * a)
    print(f"| {lab} | {a*1e3:.2f} | {strip:.1f} | {disc:.1f} |")
# with thicker base (2 mm, CoolIT-like) for comparison
t_b2 = 2.0e-3
h_eff2 = q / r_c['dT_conv']
m2 = math.sqrt(h_eff2 / (k_cu * t_b2))
a = 5.4e-3
strip2 = q * a / (k_cu * t_b2 * m2) + q * a**2 / (2 * k_cu * t_b2)
print(f"  (CoolIT-like, 2 mm base, h_eff {h_eff2/1e3:.0f} kW/m2K: 10.8 mm strip excess = {strip2:.1f} K)")
# random single-channel blockage: 10 % of channels individually -> each adds ~0.5 K locally, nothing globally
a1 = 0.1e-3
print(f"  10 % random single-channel blockages: local +{q*a1/(k_cu*t_b*m)+q*a1**2/(2*k_cu*t_b):.2f} K each; "
      f"global h_eff x0.9 -> conv dT {r_h['dT_conv']:.1f} -> {r_h['dT_conv']/0.9:.1f} K (+{r_h['dT_conv']/0.9-r_h['dT_conv']:.1f} K avg)")

print("\n" + "=" * 100)
print("F. FOULING-TOLERANT HMMC VARIANTS vs CoolIT-like (project model, 15 kW, 18 LPM, paste 0.05 unless noted)")
print("=" * 100)
print(cm.HEADER)
print(cm.fmt_row(cm.coolit_like(117.0).evaluate(Q, 1.2)))
variants = [
    ("HMMC 0.1/0.1x1.0 (baseline)", dict(fin_t_mm=0.1, gap_mm=0.1, fin_h_mm=1.0)),
    ("HMMC 0.1/0.1x1.5", dict(fin_t_mm=0.1, gap_mm=0.1, fin_h_mm=1.5)),
    ("HMMC gap0.15/fin0.1x1.5", dict(fin_t_mm=0.1, gap_mm=0.15, fin_h_mm=1.5)),
    ("HMMC gap0.15/fin0.1x2.0", dict(fin_t_mm=0.1, gap_mm=0.15, fin_h_mm=2.0)),
    ("HMMC gap0.15/fin0.15x2.0", dict(fin_t_mm=0.15, gap_mm=0.15, fin_h_mm=2.0)),
    ("HMMC gap0.15/fin0.12x2.5", dict(fin_t_mm=0.12, gap_mm=0.15, fin_h_mm=2.5)),
    ("HMMC gap0.2/fin0.15x2.5", dict(fin_t_mm=0.15, gap_mm=0.2, fin_h_mm=2.5)),
    ("HMMC gap0.2/fin0.2x3.0", dict(fin_t_mm=0.2, gap_mm=0.2, fin_h_mm=3.0)),
    ("HMMC gap0.15/fin0.1x2.0, L=3 mm", dict(fin_t_mm=0.1, gap_mm=0.15, fin_h_mm=2.0, flow_len_mm=3.0)),
    ("HMMC gap0.15/fin0.1x2.0, 5 % bleed (17.1 LPM eff.)", dict(fin_t_mm=0.1, gap_mm=0.15, fin_h_mm=2.0, _lpm=1.14)),
    ("HMMC gap0.15/fin0.1x2.0, liquid metal TIM", dict(fin_t_mm=0.1, gap_mm=0.15, fin_h_mm=2.0, tim_R=0.015, tim_label="liquid metal")),
]
for lab, kw in variants:
    lpm = kw.pop("_lpm", 1.2)
    d = cm.hmmc_design(117.0, name=lab, **kw)
    print(cm.fmt_row(d.evaluate(Q, lpm)))

print("\n" + "=" * 100)
print("G. SELF-FLUSHING HEADER BLEED AND SCREEN CAPACITY")
print("=" * 100)
dp_plate = r_h['dp_total_kPa'] * 1e3 - 4000 - r_h['dp_man_kPa'] * 1e3  # slot-to-outlet dP available across the bleed orifice
dp_plate = max(dp_plate, 1500.0)
bleed_frac = 0.05
q_bleed = bleed_frac * Vdot / n_slots
K_or = 1.5
u_or = math.sqrt(2 * dp_plate / (K_or * rho))
A_or = q_bleed / u_or
print(f"Inlet slots: {n_slots}; slot-to-outlet dP available for the bleed: {dp_plate/1e3:.1f} kPa; "
      f"5 % bleed -> {q_bleed*6e7:.3f} mL/min... = {q_bleed*6e4:.3f} L/min per slot; orifice u = {u_or:.2f} m/s, A = {A_or*1e6:.3f} mm2 "
      f"(square {math.sqrt(A_or)*1e3:.2f} mm): passes {math.sqrt(A_or)*1e3/0.1:.0f}x a 100 um particle")
# velocity at the slot dead-end with bleed: carries settled particles if u > ~10x v_settle(100um Cu oxide)
slot_w, slot_d = 0.3e-3, 3.0e-3
u_end = q_bleed / (slot_w * slot_d)
print(f"  slot end velocity with bleed = {u_end:.2f} m/s vs v_settle(100 um Cu oxide) = {v_stokes(100e-6, 6000)*1e3:.1f} mm/s -> ratio {u_end/v_stokes(100e-6,6000):.0f}")
# screen capacity vs channel inlet count
for W in (0.1, 0.15):
    pitch = (W + 0.1) * 1e-3
    n_inlets = (side / pitch) * n_paths
    for lab, op, dw, A in [("25 um", 25, 25, 117.0), ("25 um", 25, 25, 10.0), ("50 um", 50, 36, 5.0)]:
        p = (op + dw) * 1e-6
        n_pores = A * 1e-4 / p**2
        print(f"  W={W} mm: channel inlets {n_inlets:.0f}; {lab} screen @ {A:.0f} cm2 has {n_pores:.2e} pores = {n_pores/n_inlets:.0f}x the inlet count")
# allowable oversize-particle arrival for 10 % channel blockage in 10 years
for W in (0.1, 0.15):
    pitch = (W + 0.1) * 1e-3
    n_inlets = (side / pitch) * n_paths
    n_allow = 0.1 * n_inlets
    print(f"  W={W} mm: 10 % blockage = {n_allow:.0f} oversize particles per plate in 10 y = {n_allow/3652.5:.2f} per plate-day "
          f"= {n_allow/3652.5/ (Vdot*86400*1e3):.2e} per litre of coolant delivered (unscreened)")
print("\nDone.")
