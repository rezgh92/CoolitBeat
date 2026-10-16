#!/usr/bin/env python3
"""Part A: AI-benchmark numbers for the PE-first family (shared HMMC-R cartridge core).
Uses the project scoping model unmodified (imported)."""
import sys, math
from dataclasses import replace
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
from coldplate_model import ColdPlate, hmmc, coolit_like, TIM, PG25, WATER50, K_CU, K_AL

Q, LK, A0 = 15000.0, 1.2, 117.0
SCREEN_KPA_18 = 0.4   # integrated 50 um abs screen, clean, at 18 LPM (fouling-filtration.md)

def row(r, extra_dp=0.0, flow_scale=1.0):
    dp = r['dp_total_kPa'] + extra_dp * flow_scale**2
    pump = dp * 1e3 * r['flow_lpm'] / 60000
    return (f"| {r['name']:<50} | {r['dT_cal']:4.1f} | {r['dT_tim']:4.1f} | {r['dT_base']:4.1f} | {r['dT_conv']:4.1f} | "
            f"**{r['dT_avg']:4.1f}** | {r['dT_max']:4.1f} | {r['R_unit_cm2K_W']:.3f} | {dp:4.1f} | {pump:4.1f} | {r['Q_cap_kW']:4.1f} | {r['T_case_max']:4.1f} |")

H = "| design | cal | TIM | base | conv | avg dT | max dT | R'' | dP kPa (incl. screen) | pump W | Qcap kW | Tcase,max C |\n|---|---|---|---|---|---|---|---|---|---|---|---|"
print("## A1. 15 kW / 18 LPM / 45 C / 117 cm2")
print(H)
designs = [
    (coolit_like(A0), 0.0),
    (hmmc(A0, core="R", tim="paste 0.07", name="PX-R same paste"), SCREEN_KPA_18),
    (hmmc(A0, core="R", tim="PCM pad", name="PX-R Tier 1 PCM"), SCREEN_KPA_18),
    (hmmc(A0, core="R", tim="liquid metal", name="PX-R Tier 2 LM"), SCREEN_KPA_18),
    (hmmc(A0, core="P", tim="PCM pad", name="PX-P PCM (<=33um loops)"), SCREEN_KPA_18),
    (hmmc(A0, core="P", tim="liquid metal", name="PX-P LM (<=33um loops)"), SCREEN_KPA_18),
    (hmmc(A0, core="R", tim="direct-to-die", base_mm=0.8, name="PX-R Tier 3 D2D"), SCREEN_KPA_18),
    (hmmc(A0, core="R", tim="PCM pad", name="PX-R aluminium body+core (ref)", k_solid=K_AL), SCREEN_KPA_18),
]
for d, s in designs:
    print(row(d.evaluate(Q, LK), s))

r = hmmc(A0, core="R", tim="PCM pad").evaluate(Q, LK)
print(f"\nT1 detail: h {r['h']/1e3:.1f} kW/m2K, eta {r['eta']:.2f}, h_eff {r['h_eff']/1e3:.0f}, NTU {r['NTU']:.2f}, u_ch {r['u_ch']:.3f} m/s Re {r['Re']:.0f}, "
      f"u_port {r['u_port']:.2f}; dP ch {r['dp_ch_kPa']:.2f} K {r['dp_K_kPa']:.2f} hdr {r['dp_header_kPa']:.2f} orif {r['dp_orif_kPa']:.2f} port {r['dp_port_kPa']:.2f} + screen {SCREEN_KPA_18}")

# 20 mm ports
p20 = replace(hmmc(A0, core="R", tim="PCM pad", name="PX-R T1, 20 mm ports"), port_bore_mm=20.0)
print(row(p20.evaluate(Q, LK), SCREEN_KPA_18))

print("\n## A2. Flow sweep (PX-R T1 PCM vs CoolIT-like)")
print("| LPM/kW | LPM | CoolIT avg/max | dP | PX-R T1 avg/max | dP incl screen | pump W | PX-R T2 LM avg/max |")
print("|---|---|---|---|---|---|---|---|")
for lk in (0.6, 0.72, 0.8, 1.0, 1.2, 1.5, 2.0, 2.4):
    a = coolit_like(A0).evaluate(Q, lk); b = hmmc(A0, core="R", tim="PCM pad").evaluate(Q, lk); c = hmmc(A0, core="R", tim="liquid metal").evaluate(Q, lk)
    s = (lk/1.2)**2
    dpb = b['dp_total_kPa'] + SCREEN_KPA_18*s
    print(f"| {lk} | {a['flow_lpm']:.1f} | {a['dT_avg']:.1f}/{a['dT_max']:.1f} | {a['dp_total_kPa']:.1f} | {b['dT_avg']:.1f}/{b['dT_max']:.1f} | {dpb:.1f} | {dpb*b['flow_lpm']/60:.2f} | {c['dT_avg']:.1f}/{c['dT_max']:.1f} |")

# equal pumping power to CoolIT-like at 18 LPM
a = coolit_like(A0).evaluate(Q, 1.2); target = a['pump_W']
lo, hi = 1.2, 4.0
for _ in range(50):
    mid = 0.5*(lo+hi); b = hmmc(A0, core="R", tim="PCM pad").evaluate(Q, mid)
    pw = (b['dp_total_kPa'] + SCREEN_KPA_18*(mid/1.2)**2) * b['flow_lpm']/60
    lo, hi = (mid, hi) if pw < target else (lo, mid)
b = hmmc(A0, core="R", tim="PCM pad").evaluate(Q, mid); c = hmmc(A0, core="R", tim="liquid metal").evaluate(Q, mid)
print(f"\nEqual pump power {target:.1f} W: {mid:.2f} LPM/kW ({b['flow_lpm']:.1f} LPM): T1 {b['dT_avg']:.1f}/{b['dT_max']:.1f}, T2 {c['dT_avg']:.1f}/{c['dT_max']:.1f}")
# flow to match CoolIT avg
lo, hi = 0.3, 1.2
for _ in range(50):
    mid = 0.5*(lo+hi); b = hmmc(A0, core="R", tim="PCM pad").evaluate(Q, mid)
    lo, hi = (mid, hi) if b['dT_avg'] > 34.4 else (lo, mid)
b = hmmc(A0, core="R", tim="PCM pad").evaluate(Q, mid)
print(f"Flow to match 34.4 K avg (T1): {mid:.2f} LPM/kW = {b['flow_lpm']:.1f} LPM, dP {b['dp_total_kPa']+SCREEN_KPA_18*(mid/1.2)**2:.1f} kPa, pump {(b['dp_total_kPa']+SCREEN_KPA_18*(mid/1.2)**2)*b['flow_lpm']/60:.2f} W")

print("\n## A3. GPU-class plates (lidded, 1.2 and 1.0 LPM/kW)")
print("| case | CoolIT-like avg/max, dP | PX-R T1 avg/max, dP | PX-R T2 avg/max |")
print("|---|---|---|---|")
for (Qk, A, lk, lab) in ((2.3, 60, 1.0, "Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW"), (2.3, 60, 1.2, "Rubin 2.3 kW, 60 cm2, 1.2"),
                          (3.6, 80, 1.0, "Rubin Ultra-class 3.6 kW, 80 cm2, 1.0"), (4.0, 25, 1.5, "CoolIT 4 kW point, 25 cm2, 1.5")):
    a = coolit_like(A).evaluate(Qk*1e3, lk); b = hmmc(A, core="R", tim="PCM pad").evaluate(Qk*1e3, lk); c = hmmc(A, core="R", tim="liquid metal").evaluate(Qk*1e3, lk)
    print(f"| {lab} | {a['dT_avg']:.1f}/{a['dT_max']:.1f}, {a['dp_total_kPa']:.1f} | {b['dT_avg']:.1f}/{b['dT_max']:.1f}, {b['dp_total_kPa']:.1f} | {c['dT_avg']:.1f}/{c['dT_max']:.1f} |")

print("\n## A4. Real 2027-28 package fit (SYNTHESIS-physics): dT = 33 + 3500/h_eff[kW/m2K] + 350 (R_TIM - 0.05)")
for lab, he in (("CoolIT-like", 101), ("PX-R", 127), ("PX-P", 187)):
    for tl, rt in (("PCM", 0.055), ("LM", 0.015)):
        dT = 33 + 3500/he + 350*(rt-0.05)
        print(f"- {lab} {tl}: hottest-die case-to-inlet {dT:.1f} K, Tcase {45+dT:.0f} C")
