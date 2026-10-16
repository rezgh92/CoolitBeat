#!/usr/bin/env python3
"""Supplementary checks for the advanced-manufacturing proposal:
1. ECAM copper conductivity sensitivity (R core and P core).
2. Segmented (strip) ECAM fins needed on a CTE-matched base: thermal penalty.
3. Bimetal bow / mismatch for Cu-diamond (7 ppm/K) joined to copper (17 ppm/K) features.
4. Indium TIM1 bond-line needed vs lid CTE (shear-strain argument) and its thermal value at 350 W/cm2.
5. Printed-manifold development loop vs bonded prototype loop (calendar).
Run: python3 am_extra.py > am_extra.out
"""
import math
import sys
from dataclasses import replace

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
import am_run as A  # noqa: E402
from coldplate_model import hmmc  # noqa: E402

print("## 1. ECAM Cu conductivity sensitivity (117 cm2, 15 kW, 18 LPM)")
print("| k_fin W/mK | R core PCM avg / max | P core LM avg / max |")
print("|---:|---|---|")
for k in (390, 370, 350, 330, 300):
    r = A.ev(hmmc(117, core="R", tim="PCM pad"), k_fin=k)
    p = A.ev(hmmc(117, core="P", tim="liquid metal"), k_fin=k)
    print(f"| {k} | {r['avg']:.2f} / {r['max']:.2f} | {p['avg']:.2f} / {p['max']:.2f} |")

print("\n## 2. Segmented ECAM fins on Cu-diamond (P geometry, LM): strips of length Ls with 0.2 mm breaks")
base = [(0.03, 390), (1.0, A.K_CUDIA), (0.03, 390)]
P = hmmc(117, core="P", tim="liquid metal")
r0 = A.ev(P, k_fin=A.K_ECAM, base_layers=base)
print(f"continuous fins: avg {r0['avg']:.2f} max {r0['max']:.2f} K, h_eff {r0['h_eff']/1e3:.0f}")
for Ls in (1.0, 2.0, 4.0):
    nu_ratio = A.ev(replace(P, flow_len_mm=min(Ls, 4.0)), k_fin=A.K_ECAM)["Nu"] / A.ev(P, k_fin=A.K_ECAM)["Nu"]
    af = Ls / (Ls + 0.2)
    r = A.ev(P, k_fin=A.K_ECAM, base_layers=base, nu_mult=nu_ratio, area_frac=af, f_mult=1.3)
    print(f"strips {Ls:.0f} mm: Nu x{nu_ratio:.2f}, area x{af:.2f} -> avg {r['avg']:.2f} max {r['max']:.2f} K "
          f"(delta {r['avg'] - r0['avg']:+.2f} K), h_eff {r['h_eff']/1e3:.0f}")
# at 350 W/cm2
for Ls in (2.0,):
    nu_ratio = A.ev(replace(P, flow_len_mm=Ls), k_fin=A.K_ECAM)["Nu"] / A.ev(P, k_fin=A.K_ECAM)["Nu"]
    r = A.ev(P, k_fin=A.K_ECAM, base_layers=base, nu_mult=nu_ratio, area_frac=Ls / (Ls + 0.2))
    d_cont = A.die_dT(r0["h_eff"] / 1e3, 0.008, 1.0, A.K_CUDIA) + 3500 * 0.06 / 390
    d_seg = A.die_dT(r["h_eff"] / 1e3, 0.008, 1.0, A.K_CUDIA) + 3500 * 0.06 / 390
    print(f"350 W/cm2 soldered lid, 2 mm strips: die-top dT {d_seg:.1f} K vs continuous {d_cont:.1f} K")


def bimetal_bow(E1, t1, a1, E2, t2, a2, dT, L):
    """Timoshenko bimetal: curvature kappa, mid-span bow over length L (m)."""
    m = t1 / t2
    n = E1 / E2
    h = t1 + t2
    kappa = 6 * (a2 - a1) * dT * (1 + m) ** 2 / (h * (3 * (1 + m) ** 2 + (1 + m * n) * (m ** 2 + 1 / (m * n))))
    return kappa, kappa * L ** 2 / 8


print("\n## 3. CTE mismatch: Cu-diamond (E ~300 GPa, 7 ppm/K) with copper (E 120 GPa, 17 ppm/K)")
print("| configuration | dT from stress-free K | free mismatch over 30 mm half-span um | bow over 60 mm um |")
print("|---|---:|---:|---:|")
cases = [
    ("1.0 mm Cu-diamond insert diffusion-bonded into Cu frame (stress-free at 900 C), at 20 C", 880, None),
    ("same, Ag-sinter / Cu-Sn TLP rim joint (stress-free at 250 C), at 20 C", 230, None),
    ("continuous ECAM Cu fins (0.75 mm equivalent along fins) on 1.0 mm Cu-diamond, -40 C storage", 65, (0.75,)),
    ("same, +40 K in operation", 40, (0.75,)),
    ("printed Cu manifold walls (1.3 mm equivalent) on 1.0 mm Cu-diamond, -40 C storage", 65, (1.3,)),
]
for lab, dT, cu in cases:
    mism = 10e-6 * dT * 30e-3 * 1e6
    if cu is None:
        print(f"| {lab} | {dT} | {mism:.0f} | (rim yields; not a bimetal) |")
    else:
        k, bow = bimetal_bow(300e9, 1.0e-3, 7e-6, 120e9, cu[0] * 1e-3, 17e-6, dT, 60e-3)
        print(f"| {lab} | {dT} | {mism:.0f} | {bow*1e6:.0f} |")
print("Segmented fins (<= 2 mm strips) and segmented grate carry no long-range stress: bow -> ~0 (strip-level only);"
      " the cap must be CTE-matched (Mo70Cu30 7-8 ppm/K or CuW).")

print("\n## 4. Indium TIM1 bond line vs lid CTE (shear strain gamma = d_alpha * dT * DNP / BLT <= gamma_allow)")
DNP = 45e-3        # m, distance to neutral point for a ~4-die 60 x 70 mm lid footprint corner
dT_cyc = 100.0     # K, reflow-to-cold / power-cycle envelope
for lab, a_lid in (("Cu lid 17 ppm/K", 17e-6), ("CuW / MoCu 7-8 ppm/K", 7.5e-6), ("Cu-diamond 7 ppm/K", 7e-6)):
    da = a_lid - 2.6e-6
    for g_allow in (0.25,):
        blt = da * dT_cyc * DNP / g_allow
        R = blt / 86.0 * 1e4 + 0.002   # cm2K/W, k_In 86 W/mK + 2 interfaces 0.001 each
        print(f"- {lab}: min BLT {blt*1e6:.0f} um at gamma_allow {g_allow}, R'' {R:.4f} cm2K/W, "
              f"{R*350:.1f} K at 350 W/cm2")

print("\n## 5. Development loop calendar (weeks to a tested manifold variant)")
for lab, w in (("clear SLA manifold on water table (uniformity, theta_c)", "1-2"),
               ("L-PBF Cu manifold block + skived core, bolted with metal C-seal, TTV-A", "2-3"),
               ("etched-laminate + diffusion-bond prototype", "8-12"),
               ("2.5-D CNC block + diffusion bond prototype", "10-12")):
    print(f"- {lab}: {w} weeks")
