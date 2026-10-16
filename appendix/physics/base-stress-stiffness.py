#!/usr/bin/env python3
"""
base-stress-stiffness.py
Mechanical feasibility of a thin (0.8-1.0 mm) OFHC copper base under a
hierarchical manifold micro-channel (HMMC) stack, compared with a plain
2 mm base + 4 mm skived fins (CoolIT-like reconstruction).

All closed-form (Roark / Timoshenko) plate & sandwich estimates. Scoping
accuracy +/-20 % on stiffness, +/-30 % on corner-supported bow, +/-50 % on
thermal bow. Not FEA.
"""
import numpy as np

# ---------------------------------------------------------------- materials
E   = 117e9        # Pa, OFHC Cu
nu  = 0.34
G   = E / (2 * (1 + nu))
CTE = 16.5e-6      # 1/K  (Si 2.6, organic substrate ~12-17)
RHO = 8940.0       # kg/m3
MAT = {            # yield / UTS / fatigue strength (1e8 cycles, R=-1)  [Pa]
    "OFHC annealed (post-braze / post-diffusion-bond)": (70e6, 220e6, 70e6),
    "OFHC half-hard (only if joints made cold)":        (250e6, 300e6, 100e6),
}
BRAZE_SHEAR_LO, BRAZE_SHEAR_HI = 100e6, 200e6     # BCuP / BAg on Cu, lap shear
BRAZE_TENS_BUTT = 200e6                           # butt tensile, fails in annealed Cu
DIFF_BOND_TENS  = 180e6                           # Cu-Cu diffusion bond, ~parent (annealed)

# ---------------------------------------------------------------- loads
P_OP    = 0.30e6   # Pa, max operating (envelope 0.1-0.3 MPa gauge)
P_PROOF = 2 * P_OP
P_BURST = 1.5e6    # Pa, 3x of a 0.5 MPa envelope -> upper end of OCP/Nvidia-type asks
F_MOUNT = np.array([130.0, 300.0, 450.0])   # N (30-100 lbf)
A_PLATE = 0.108    # m, bolt-to-bolt span / heated footprint 108x108 mm
DIE     = {"50 mm die": 0.050, "108 mm TTV": 0.108}
FLAT_SPEC = (25e-6, 50e-6)                  # m, allowed bow over die

# ---------------------------------------------------------------- geometry
# HMMC stack (bottom -> top)
T_BASE   = 1.0e-3
T_FIN    = 0.10e-3; GAP = 0.10e-3; PITCH = T_FIN + GAP; H_FIN = 1.0e-3
T_MAN    = 1.75e-3     # etched manifold layer (1.5-2.0)
F_MAN    = 0.60        # solid fraction of manifold layer carrying membrane stress
T_COVER  = 2.5e-3      # 2-3 mm
SLOT_W   = 0.30e-3; SLOT_PITCH = 2.0e-3            # one slot (inlet or return) every 2 mm
F_BOND_FIN = 1 - SLOT_W / SLOT_PITCH               # fin-tip area bonded to manifold webs
F_BOND_MAN = 0.50                                  # manifold-to-cover bonded fraction (headers)
LAND_W   = 4.0e-3      # perimeter seal land: base span unsupported by fins
HEADER_W = 6.0e-3      # 2nd-level header width spanned by cover
# CoolIT-like skived (untied fin tips)
T_BASE_S = 2.0e-3; T_FIN_S = 0.2e-3; GAP_S = 0.2e-3; H_FIN_S = 4.0e-3; T_COVER_S = 3.0e-3

def Dplate(t, Eeff=E):
    return Eeff * t**3 / (12 * (1 - nu**2))

def strip_fixed(p, b, t):
    """fixed-edge strip, width b, thickness t, uniform p  (Roark)."""
    sig = p * b**2 / (2 * t**2)           # 6*M/t^2 with M = p b^2 / 12
    w   = p * b**4 / (384 * Dplate(t))
    return sig, w

def D_stack(layers):
    """layers: list of (t, fx, fy) = thickness, membrane fraction along-fin (x), across-fin (y).
    Returns (Dx, Dy, total thickness, zbar) with full composite action."""
    z0 = 0.0; items = []
    for t, fx, fy in layers:
        items.append((t, fx, fy, z0 + t / 2)); z0 += t
    out = []
    for idx in (1, 2):
        A = sum(t * l[idx] for l in items for t in [l[0]])
        zbar = sum(t * l[idx] * l[3] for l in items for t in [l[0]]) / A
        I = sum(l[idx] * (t**3 / 12 + t * (l[3] - zbar)**2) for l in items for t in [l[0]])
        out.append(E * I / (1 - nu**2))
    return out[0], out[1], z0

def sec_props(layers, idx):
    """neutral axis, I (per unit width) and extreme-fibre distances for stress."""
    z0 = 0.0; items = []
    for l in layers:
        items.append((l[0], l[idx], z0 + l[0] / 2)); z0 += l[0]
    A = sum(t * f for t, f, _ in items)
    zbar = sum(t * f * z for t, f, z in items) / A
    I = sum(f * (t**3 / 12 + t * (z - zbar)**2) for t, f, z in items)
    return zbar, I, z0

print("=" * 78)
print("1. LOCAL BASE BENDING BETWEEN FINS / OVER UNSUPPORTED SPANS at p_burst = %.1f MPa" % (P_BURST / 1e6))
print("=" * 78)
print("%-34s %8s %8s %10s %12s %8s" % ("span", "t_base", "sigma", "w_max", "SF vs yield", "SF UTS"))
sy, su, sf = MAT["OFHC annealed (post-braze / post-diffusion-bond)"]
for label, b in (("fin gap 0.10 mm", GAP), ("slot width 0.30 mm (fins continuous)", SLOT_W),
                 ("perimeter land 4 mm", LAND_W), ("plenum over base 6 mm (avoid)", 6e-3),
                 ("plenum over base 10 mm (avoid)", 10e-3)):
    for t in (0.5e-3, 0.8e-3, 1.0e-3):
        sig, w = strip_fixed(P_BURST, b, t)
        print("%-34s %6.1f mm %7.3f MPa %9.3g um %10.0f %8.0f" % (label, t * 1e3, sig / 1e6, w * 1e6, sy / sig, su / sig))
    print()

print("=" * 78)
print("2. FINS AS TENSION TIES (brazed / diffusion-bonded both faces)")
print("=" * 78)
for label, p in (("operating", P_OP), ("proof", P_PROOF), ("burst", P_BURST)):
    s_fin  = p * PITCH / T_FIN                       # fin body
    s_bond = p * PITCH / (T_FIN * F_BOND_FIN)         # fin-tip bond (85 % of tip area bonded)
    s_man  = p / F_BOND_MAN                           # manifold-cover bond
    print("%-10s %5.2f MPa: fin tie %5.2f MPa | tip-bond %5.2f MPa | manifold/cover bond %5.2f MPa"
          % (label, p / 1e6, s_fin / 1e6, s_bond / 1e6, s_man / 1e6))
s_bond_burst = P_BURST * PITCH / (T_FIN * F_BOND_FIN)
print("\nSafety factors at burst (%.1f MPa) on the tip bond (%.2f MPa):" % (P_BURST / 1e6, s_bond_burst / 1e6))
for name, (y, u, f) in MAT.items():
    print("  %-52s SF_yield %5.1f  SF_UTS %5.1f" % (name, y / s_bond_burst, u / s_bond_burst))
print("  %-52s SF %5.1f .. %5.1f" % ("brazed lap-shear 100-200 MPa", BRAZE_SHEAR_LO / s_bond_burst, BRAZE_SHEAR_HI / s_bond_burst))
print("  %-52s SF %5.1f" % ("diffusion bond ~180 MPa", DIFF_BOND_TENS / s_bond_burst))
# with stress concentration and partial bonding
for kt, fb in ((2.5, 0.85), (2.5, 0.30)):
    s = P_BURST * PITCH / (T_FIN * fb) * kt
    print("  Kt=%.1f at fin root, bonded fraction %.0f%% -> %.1f MPa, SF_yield(annealed) %.1f" % (kt, fb * 100, s / 1e6, sy / s))

p_burst_fin  = su * T_FIN / PITCH * F_BOND_FIN
p_burst_bond = BRAZE_SHEAR_LO * T_FIN / PITCH * F_BOND_FIN
p_burst_land_y = 2 * sy * T_BASE**2 / LAND_W**2
p_burst_land_u = 2 * su * T_BASE**2 / LAND_W**2
p_burst_hdr_y  = 2 * sy * T_COVER**2 / HEADER_W**2
print("\nBurst-pressure ladder for the tied HMMC sandwich (1.0 mm base):")
print("  fin fracture (UTS annealed)          : %6.1f MPa" % (p_burst_fin / 1e6))
print("  fin-tip braze, 100 MPa shear         : %6.1f MPa" % (p_burst_bond / 1e6))
print("  cover over 6 mm header, yield / UTS  : %6.1f / %6.1f MPa" % (p_burst_hdr_y / 1e6, p_burst_hdr_y * su / sy / 1e6))
print("  4 mm perimeter land, yield / UTS     : %6.1f / %6.1f MPa   <-- governs" % (p_burst_land_y / 1e6, p_burst_land_u / 1e6))
print("  -> SF on 1.5 MPa burst (yield-based) : %6.1f" % (p_burst_land_y / P_BURST))
# perimeter seam shear, tied vs untied
perim = 4 * A_PLATE; seam = 3e-3
F_untied = P_BURST * A_PLATE**2
F_tied   = P_BURST * perim * LAND_W
print("  perimeter seam (3 mm braze) shear at burst: untied cavity %.1f MPa  |  tied sandwich %.1f MPa"
      % (F_untied / (perim * seam) / 1e6, F_tied / (perim * seam) / 1e6))

print("\n" + "=" * 78)
print("3. EFFECTIVE BENDING STIFFNESS D (N.m per m width)")
print("=" * 78)
hmmc = [(T_BASE, 1.0, 1.0), (H_FIN, T_FIN / PITCH, 0.0), (T_MAN, F_MAN, F_MAN), (T_COVER, 1.0, 1.0)]
skived_base = [(T_BASE_S, 1.0, 1.0), (H_FIN_S, T_FIN_S / (T_FIN_S + GAP_S), 0.0)]   # fin tips free
Dx_h, Dy_h, h_h = D_stack(hmmc)
Dx_s, Dy_s, h_s = D_stack(skived_base)
D_cov_s = Dplate(T_COVER_S)
D_2mm = Dplate(2e-3); D_1mm = Dplate(1e-3)
# sandwich core shear stiffness across fins (fins bend as fixed-fixed plates between faces)
G_core_across = E * T_FIN**3 / (H_FIN**2 * PITCH)
G_core_along  = G * T_FIN / PITCH
rows = [
    ("plain 1.0 mm plate", D_1mm, D_1mm, 1.0),
    ("plain 2.0 mm plate", D_2mm, D_2mm, 2.0),
    ("skived: 2 mm base + 4 mm free-tip fins (base alone)", Dx_s, Dy_s, h_s * 1e3),
    ("skived cover 3 mm (separate, perimeter-joined)", D_cov_s, D_cov_s, 3.0),
    ("skived base + cover acting in parallel (mounting load)", Dx_s + D_cov_s, Dy_s + D_cov_s, 9.0),
    ("HMMC tied sandwich 1+1+1.75+2.5 mm", Dx_h, Dy_h, h_h * 1e3),
]
print("%-58s %10s %10s %8s %9s" % ("construction", "D_along", "D_across", "h mm", "t_equiv"))
for name, dx, dy, h in rows:
    teq = (np.sqrt(dx * dy) * 12 * (1 - nu**2) / E) ** (1 / 3) * 1e3
    print("%-58s %10.0f %10.0f %8.2f %7.2f mm" % (name, dx, dy, h, teq))
print("\ncore shear modulus of 0.1/0.1x1.0 mm fin layer: along fins %.1f GPa, across fins %.2f GPa"
      % (G_core_along / 1e9, G_core_across / 1e9))
# shear deflection fraction, across-fin direction, SS strip, uniform load
z_upper = T_BASE + H_FIN + (T_MAN * F_MAN * (T_MAN / 2) + T_COVER * (T_MAN + T_COVER / 2)) / (T_MAN * F_MAN + T_COVER)
d_core = z_upper - T_BASE / 2                              # distance between face centroids (base | manifold+cover)
shear_rig = G_core_across * d_core**2 / H_FIN              # sandwich shear rigidity per unit width; fin layer is the only compliant core
ratio = (A_PLATE**2 / (8 * shear_rig)) / (5 * A_PLATE**4 / (384 * Dy_h))
print("across-fin shear deflection / bending deflection (SS strip, uniform load): %.2f -> stiffness knock-down 1/(1+r) = %.2f"
      % (ratio, 1 / (1 + ratio)))
D_h_eff = np.sqrt(Dx_h * Dy_h / (1 + ratio))
D_s_eff = np.sqrt(Dx_s * Dy_s)
print("effective isotropic D used below: HMMC %.0f N.m | skived base alone %.0f N.m | skived base+cover %.0f N.m | plain 2 mm %.0f N.m"
      % (D_h_eff, D_s_eff, D_s_eff + D_cov_s, D_2mm))
print("stiffness ratio HMMC sandwich / plain 2 mm base = %.0f x ; / skived base alone = %.0f x ; / skived base+cover = %.1f x"
      % (D_h_eff / D_2mm, D_h_eff / D_s_eff, D_h_eff / (D_s_eff + D_cov_s)))

print("\n" + "=" * 78)
print("4. GLOBAL BOW UNDER INTERNAL PRESSURE (untied base = clamped square plate over wetted cavity)")
print("=" * 78)
# clamped square plate: w = 0.00126 p a^4 / D ; edge moment M = 0.0513 p a^2 ; sigma = 6M/t^2 (homogeneous)
def clamped_square(p, a, D):
    return 0.00126 * p * a**4 / D, 0.0513 * p * a**2
for label, p in (("operating 0.3 MPa", P_OP), ("burst 1.5 MPa", P_BURST)):
    print(label)
    for name, D, t, layers in (("plain 1.0 mm base", D_1mm, 1e-3, None), ("plain 2.0 mm base", D_2mm, 2e-3, None),
                               ("skived 2 mm base + 4 mm free fins", D_s_eff, None, skived_base),
                               ("skived 3 mm cover", D_cov_s, 3e-3, None)):
        w, M = clamped_square(p, A_PLATE, D)
        if layers is None:
            sig = 6 * M / t**2
        else:   # ribbed section, along-fin direction, stress at base outer fibre
            zbar, I, h = sec_props(layers, 1)
            sig = M * zbar / I
        print("  %-36s bow %8.3f mm  edge stress %7.0f MPa  (yield 70)" % (name, w * 1e3, sig / 1e6))
    print("  %-36s bow %8.3f um  (self-equilibrated: ties carry p; only 4 mm land strip bends)" % ("HMMC tied sandwich", 0.0))
# required untied base thickness vs support pitch
print("\nUntied base: max unsupported square span s for sigma = 0.308 p s^2/t^2 <= allowable at burst 1.5 MPa")
for t in (1e-3, 2e-3, 3e-3):
    s_y = t * np.sqrt(sy / (0.308 * P_BURST)); s_u = t * np.sqrt(su / (0.308 * P_BURST))
    print("  t = %.0f mm: s <= %5.1f mm (yield, annealed) | %5.1f mm (UTS, rupture)" % (t * 1e3, s_y * 1e3, s_u * 1e3))
for a in (0.06, 0.108):
    t_y = a * np.sqrt(0.308 * P_BURST / sy); t_u = a * np.sqrt(0.308 * P_BURST / su)
    print("  unsupported cavity %3.0f mm: needs t >= %4.1f mm (yield) / %4.1f mm (UTS)" % (a * 1e3, t_y * 1e3, t_u * 1e3))

print("\n" + "=" * 78)
print("5. BOW UNDER MOUNTING LOAD (plate between bolts, die reaction at centre)")
print("=" * 78)
# SS-edge square plate, central concentrated load: w = 0.0116 P a^2 / D (Timoshenko, nu=0.3)  -> lower bound
# corner-supported: x ~6 (ratio of uniform-load coefficients 0.025/0.00406) -> upper bound, +/-30 %
C_SS, C_CORNER = 0.0116, 0.0116 * 6.1
print("%-44s" % "construction", " ".join("%8.0f N" % F for F in F_MOUNT))
for name, D in (("plain 2 mm base alone", D_2mm), ("skived base+cover (parallel)", D_s_eff + D_cov_s), ("HMMC tied sandwich", D_h_eff)):
    w_ss = C_SS * F_MOUNT * A_PLATE**2 / D
    w_c  = C_CORNER * F_MOUNT * A_PLATE**2 / D
    print("%-44s" % (name + " [SS edges]"), " ".join("%7.1f um" % (w * 1e6) for w in w_ss))
    print("%-44s" % (name + " [corner bolts]"), " ".join("%7.1f um" % (w * 1e6) for w in w_c))
# curvature over a 50 mm die: w_die ~ w_total * (L_die/a)^2 for a parabolic-ish dome
print("\nbow across a 50 mm die ~ (50/108)^2 = %.2f of the full-span bow; spec 25-50 um" % ((0.05 / 0.108) ** 2))
print("Pressure-vs-mount competition: p_op x 117 cm2 = %.0f N  (%.0fx a 300 N mount load); at burst %.0f N"
      % (P_OP * A_PLATE**2, P_OP * A_PLATE**2 / 300, P_BURST * A_PLATE**2))
print("Mean TIM pressure from 300 N over 50 mm die = %.3f MPa; untied base pushes with p_op = %.1f MPa -> crowning dominates"
      % (300 / 0.05**2 / 1e6, P_OP / 1e6))

print("\n" + "=" * 78)
print("6. THERMAL BOW (hot base constrained by cooler fins/manifold/cover; Timoshenko bimetal, n=1)")
print("=" * 78)
def bimetal_curv(t_hot, t_cold, dT):
    m = t_hot / t_cold
    return 6 * CTE * dT * (1 + m) ** 2 / ((t_hot + t_cold) * (3 * (1 + m) ** 2 + (1 + m) * (m**2 + 1 / m)))
# base mean temperature above the rest: q t/(2k) + conv-side wall superheat share
q = 15e3 / A_PLATE**2
# wall superheat (conv term) and fin efficiency from coldplate_model.py: HMMC 8.1 K / eta 0.76 ; skived 12.6 K / eta 0.48
theta_h, eta_h = 8.1, 0.76
theta_s, eta_s = 12.6, 0.48
stack_h = (H_FIN * 0.5 * eta_h * theta_h + T_MAN * F_MAN * 0.5 + T_COVER * 0.0) / (H_FIN * 0.5 + T_MAN * F_MAN + T_COVER)
dT_h = q * T_BASE / (2 * 390) + theta_h - stack_h
dT_s = q * T_BASE_S / (2 * 390) + theta_s - eta_s * theta_s
for name, t_hot, t_cold, dT in (("HMMC: 1 mm base vs 5.25 mm bonded stack", T_BASE, h_h - T_BASE, dT_h),
                                ("skived: 2 mm base vs 4 mm fins (50 % solid, as 2 mm)", T_BASE_S, 2.0e-3, dT_s)):
    k = bimetal_curv(t_hot, t_cold, dT)
    print("%-52s dT_base-rest %4.1f K  curvature %.4f 1/m  bow over 50 mm %5.1f um | over 108 mm %5.1f um"
          % (name, dT, k, k * 0.05**2 / 8 * 1e6, k * 0.108**2 / 8 * 1e6))
# in-plane constraint stress in the base
for name, dT, frac in (("HMMC 1 mm base", dT_h, 1 - T_BASE / h_h), ("skived 2 mm base", dT_s, 0.5)):
    s = E * CTE * dT / (1 - nu) * frac
    print("%-20s constrained in-plane thermal stress ~ %5.1f MPa (cycles 0 -> this; fatigue amp %4.1f MPa vs 70 MPa endurance)" % (name, s / 1e6, s / 2e6))
# CTE mismatch to package
for name, L, cte_p in (("Si die 50 mm (D2D)", 0.05, 2.6e-6), ("organic substrate 108 mm", 0.108, 14e-6)):
    for dT in (40.0, 60.0):
        print("  Cu vs %-26s dT %2.0f K: relative shear displacement at edge %5.1f um" % (name, dT, (CTE - cte_p) * dT * L / 2 * 1e6))

print("\n" + "=" * 78)
print("7. CREEP, FATIGUE, BUCKLING, HANDLING")
print("=" * 78)
Tm = 1358.0
for T in (50.0, 85.0):
    print("  homologous temperature at %3.0f C: %.2f Tm  (creep regime >0.4 Tm = %.0f C)" % (T, (T + 273.15) / Tm, 0.4 * Tm - 273.15))
s_op = P_OP * PITCH / (T_FIN * F_BOND_FIN)
print("  tie stress at operating %.2f MPa, pressure-cycle amplitude %.2f MPa -> fatigue SF %.0f (annealed endurance 70 MPa)" % (s_op / 1e6, s_op / 2e6, 70e6 / (s_op / 2)))
# fin column buckling under mounting compression
P_fin = 0.5 * np.pi**2 * E * T_FIN**2 / (12 * (1 - nu**2) * (0.5 * H_FIN) ** 2)
print("  fin Euler/plate buckling stress (fixed-fixed, 0.1 x 1.0 mm): %.0f MPa  vs mounting compression %.2f MPa -> yield governs, no buckling"
      % (P_fin / 1e6, 450 / A_PLATE**2 / (T_FIN / PITCH) / 1e6))
m_h = RHO * A_PLATE**2 * (T_BASE + H_FIN * 0.5 + T_MAN * F_MAN + T_COVER)
m_s = RHO * A_PLATE**2 * (T_BASE_S + H_FIN_S * 0.5 + T_COVER_S)
print("  mass over the 108 mm footprint: HMMC %.2f kg (%.2f mm thick) | skived %.2f kg (%.1f mm)" % (m_h, h_h * 1e3, m_s, (T_BASE_S + H_FIN_S + T_COVER_S) * 1e3))
print("  base-thickness floor (non-pressure): post-bond flatness machining 0.10-0.20 mm + erosion/corrosion allowance 0.10 mm + etch/skive tolerance 0.05 mm")
print("  -> 0.8 mm finished (1.0 mm as-bonded) is the practical minimum; pressure alone would allow < 0.5 mm.")

# summary table rows for the report
print("\n" + "=" * 78)
print("8. SUMMARY TABLE (markdown)")
print("=" * 78)
sig_gap, w_gap = strip_fixed(P_BURST, GAP, T_BASE)
sig_land, w_land = strip_fixed(P_BURST, LAND_W, T_BASE)
w_s_press, _ = clamped_square(P_OP, A_PLATE, D_s_eff)
w_mount_h = C_CORNER * 300 * A_PLATE**2 / D_h_eff
w_mount_s = C_CORNER * 300 * A_PLATE**2 / (D_s_eff + D_cov_s)
print("| quantity | CoolIT-like skived (2 mm base, free fins) | HMMC tied sandwich (1 mm base) |")
print("|---|---:|---:|")
print("| effective D (N.m) | %.0f (base) / %.0f (+cover) | %.0f |" % (D_s_eff, D_s_eff + D_cov_s, D_h_eff))
print("| local base stress between fins @1.5 MPa | 0.04 MPa (0.2 mm gap, 2 mm) | %.4f MPa |" % (sig_gap / 1e6))
print("| base bow under 0.3 MPa operating (108 mm cavity, untied) | %.2f mm (yields) | 0 (ties) |" % (w_s_press * 1e3))
print("| fin/bond tie stress @1.5 MPa | n/a | %.1f MPa (SF %.0f annealed yield) |" % (s_bond_burst / 1e6, sy / s_bond_burst))
zb_s, I_s, _ = sec_props(skived_base, 1)
sig_s_unit = 0.0513 * A_PLATE**2 * zb_s / I_s          # base outer-fibre stress per Pa of pressure (ribbed, along fins)
sig_c_unit = 0.0513 * A_PLATE**2 * 6 / T_COVER_S**2    # 3 mm cover
print("| governing pressure, untied 108 mm cavity | ribbed base yields %.2f / ruptures %.2f MPa; 3 mm cover yields %.2f / ruptures %.2f MPa | %.1f MPa yield (4 mm land) |"
      % (sy / sig_s_unit / 1e6, su / sig_s_unit / 1e6, sy / sig_c_unit / 1e6, su / sig_c_unit / 1e6, p_burst_land_y / 1e6))
print("| mounting bow, 300 N, corner bolts | %.0f um | %.0f um |" % (w_mount_s * 1e6, w_mount_h * 1e6))
