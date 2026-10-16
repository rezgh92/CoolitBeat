#!/usr/bin/env python3
"""HMMC-elite scoping run on the project model (unmodified import)."""
import sys, math
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
from dataclasses import replace
from coldplate_model import ColdPlate, hmmc, coolit_like, TIM, PG25, WATER50, K_CU

A0 = 117.0
Q = 15000.0

def elite(footprint, core="R", tim="PCM pad", base=1.0, fin_h=None, orifice=None, name=None, flow_len=4.0, port=16.0, hot=1.5):
    """HMMC-E: design-H manifold re-packaged (bow-tie troughs, in-plane loops, 3.3 mm slots), same core families."""
    cores = {"R": dict(gap_mm=0.15, fin_t_mm=0.10, fin_h_mm=2.0, orifice=2.2),
             "P": dict(gap_mm=0.10, fin_t_mm=0.10, fin_h_mm=1.5, orifice=1.6)}[core]
    side = math.sqrt(footprint) * 10
    n_slots = max(1, int(round(side / (2 * flow_len))))
    return ColdPlate(
        name=name or f"HMMC-E/{core} ({footprint:.0f} cm2, {tim})",
        footprint_cm2=footprint, fin_t_mm=cores["fin_t_mm"], gap_mm=cores["gap_mm"],
        fin_h_mm=fin_h or cores["fin_h_mm"], flow_len_mm=flow_len, base_mm=base, k_solid=K_CU,
        tim=tim, isothermal_cell=True, hotspot_flow_K=hot,
        n_parallel_paths=2 * n_slots, slot_w_mm=3.3, K_channel=3.0, K_slot=1.5,
        header_u_m_s=0.9, K_header=1.5,       # bow-tie troughs + perimeter loop + tees
        port_bore_mm=port, K_port=2.3,
        orifice_dp_kPa_18=orifice if orifice is not None else cores["orifice"],
        notes="HMMC-E elite stack")

SCREEN_KPA_18 = 0.4   # integrated 50 um absolute pleated screen, >= 12 cm2, clean

def row(r, screen=True):
    dp = r["dp_total_kPa"] + (SCREEN_KPA_18 * (r["flow_lpm"] / 18.0) ** 2 if screen else 0)
    pump = dp * 1e3 * r["flow_lpm"] / 60e3
    return (f"| {r['name']:<46} | {r['q_W_cm2']:5.0f} | {r['dT_cal']:5.1f} | {r['dT_tim']:5.1f} | {r['dT_base']:4.1f} | "
            f"{r['dT_conv']:5.1f} | **{r['dT_avg']:5.1f}** | {r['dT_max']:5.1f} | {r['R_unit_cm2K_W']:.3f} | "
            f"{dp:5.1f} | {pump:4.1f} | {r['Q_cap_kW']:5.1f} | {r['T_case_max']:5.1f} |")

HDR = ("| design | q'' W/cm2 | caloric | TIM | base | conv | **avg dT K** | max dT K | R'' cm2K/W | dP kPa (incl. screen) | pump W | Q cap kW | Tcase,max C |\n"
       "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

print("# HMMC-E scoping run, 15 kW / 18 LPM PG25 / 45 C / 117 cm2\n")
print(HDR)
rows = [
    coolit_like(A0),
    elite(A0, "R", "paste 0.07", name="HMMC-E/R, same paste (like-for-like)"),
    elite(A0, "R", "PCM pad", name="HMMC-E/R Tier 1 PCM pad"),
    elite(A0, "R", "liquid metal", name="HMMC-E/R Tier 2 liquid metal (Ni face)"),
    elite(A0, "R", "direct-to-die", base=0.8, name="HMMC-E/R Tier 3 direct-to-die (ref.)"),
    elite(A0, "P", "PCM pad", name="HMMC-E/P PCM pad (<=33 um loops)"),
    elite(A0, "P", "liquid metal", name="HMMC-E/P liquid metal (<=33 um loops)"),
    elite(A0, "R", "PCM pad", fin_h=1.5, orifice=3.2, name="HMMC-E/R low-profile 18 mm (1.5 mm fins, 3.2 kPa comb)"),
    elite(A0, "R", "PCM pad", fin_h=1.5, orifice=1.6, name="HMMC-E/R LP15 (15.6 mm, 1.6 kPa comb)"),
]
res = {}
for v in rows:
    r = v.evaluate(Q, 1.2); res[v.name] = r
    print(row(r, screen=(v is not rows[0])))

r1 = res["HMMC-E/R Tier 1 PCM pad"]
print(f"\nTier-1 detail: NTU {r1['NTU']:.2f}, cal_frac {r1['cal_frac']:.2f}, h {r1['h']/1e3:.1f} kW/m2K, eta {r1['eta']:.2f}, "
      f"h_eff {r1['h_eff']/1e3:.0f} kW/m2K, u_ch {r1['u_ch']:.3f} m/s (Re {r1['Re']:.0f}), u_slot {r1['u_slot']:.2f} m/s, u_port {r1['u_port']:.2f} m/s")
print(f"dP split: channel {r1['dp_ch_kPa']:.2f} + turns {r1['dp_K_kPa']:.2f} + slot {r1['dp_slot_kPa']:.2f} + header {r1['dp_header_kPa']:.2f} "
      f"+ comb {r1['dp_orif_kPa']:.2f} + ports {r1['dp_port_kPa']:.2f} + screen {SCREEN_KPA_18:.2f} = {r1['dp_total_kPa']+SCREEN_KPA_18:.1f} kPa")

print("\n## Flow sweep (HMMC-E/R PCM and LM vs CoolIT-like), 15 kW, 117 cm2")
print("| LPM/kW | LPM | CoolIT avg/max K | dP kPa | pump W | E/R-PCM avg/max | dP (16 mm ports) | dP (20 mm ports) | pump W | E/R-LM avg/max | E/P-LM avg/max |")
print("|---:|---:|---|---:|---:|---|---:|---:|---:|---|---|")
for lk in (0.6, 0.75, 0.9, 1.0, 1.2, 1.5, 2.0, 2.4):
    a = coolit_like(A0).evaluate(Q, lk)
    b = elite(A0, "R", "PCM pad").evaluate(Q, lk)
    b20 = elite(A0, "R", "PCM pad", port=20.0).evaluate(Q, lk)
    c = elite(A0, "R", "liquid metal").evaluate(Q, lk)
    d = elite(A0, "P", "liquid metal").evaluate(Q, lk)
    sc = SCREEN_KPA_18 * (b["flow_lpm"] / 18) ** 2
    dpb = b["dp_total_kPa"] + sc; dpb20 = b20["dp_total_kPa"] + sc
    print(f"| {lk:.2f} | {b['flow_lpm']:.1f} | {a['dT_avg']:.1f} / {a['dT_max']:.1f} | {a['dp_total_kPa']:.1f} | {a['pump_W']:.1f} | "
          f"{b['dT_avg']:.1f} / {b['dT_max']:.1f} | {dpb:.1f} | {dpb20:.1f} | {dpb*1e3*b['flow_lpm']/60e3:.1f} | "
          f"{c['dT_avg']:.1f} / {c['dT_max']:.1f} | {d['dT_avg']:.1f} / {d['dT_max']:.1f} |")

# equal pumping power / equal dT crossovers
def find_flow(target_fn, lo=0.3, hi=3.0, up=True):
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if target_fn(mid) > 0: hi = mid if up else hi
        if target_fn(mid) > 0 and not up: lo = mid
        if target_fn(mid) <= 0 and up: lo = mid
        if target_fn(mid) <= 0 and not up: hi = mid
    return 0.5 * (lo + hi)
ref = coolit_like(A0).evaluate(Q, 1.2)
pw_ref = ref["pump_W"]
def pump_at(lk):
    r = elite(A0, "R", "PCM pad").evaluate(Q, lk); sc = SCREEN_KPA_18 * (r["flow_lpm"] / 18) ** 2
    return (r["dp_total_kPa"] + sc) * 1e3 * r["flow_lpm"] / 60e3
lk_eq = find_flow(lambda lk: pump_at(lk) - pw_ref)
req = elite(A0, "R", "PCM pad").evaluate(Q, lk_eq); reqlm = elite(A0, "R", "liquid metal").evaluate(Q, lk_eq)
print(f"\nEqual pumping power to the CoolIT-like plate ({pw_ref:.1f} W at 18 LPM): HMMC-E/R runs {req['flow_lpm']:.1f} LPM ({lk_eq:.2f} LPM/kW): "
      f"PCM {req['dT_avg']:.1f}/{req['dT_max']:.1f} K, LM {reqlm['dT_avg']:.1f}/{reqlm['dT_max']:.1f} K")
def dt_at(lk, tim="PCM pad"):
    return elite(A0, "R", tim).evaluate(Q, lk)["dT_avg"] - 34.4
lk_dt = find_flow(lambda lk: -dt_at(lk), 0.3, 2.0)
r_dt = elite(A0, "R", "PCM pad").evaluate(Q, lk_dt)
print(f"Equal average dT (34.4 K): HMMC-E/R PCM needs {r_dt['flow_lpm']:.1f} LPM ({lk_dt:.2f} LPM/kW), dP {r_dt['dp_total_kPa']+SCREEN_KPA_18*(r_dt['flow_lpm']/18)**2:.1f} kPa, pump {r_dt['pump_W']:.2f} W")
lk_dt2 = find_flow(lambda lk: -(elite(A0, "R", "paste 0.07").evaluate(Q, lk)["dT_avg"] - 34.4), 0.3, 2.0)
print(f"Equal average dT with the SAME paste: {lk_dt2*15:.1f} LPM ({lk_dt2:.2f} LPM/kW)")
# max-dT equivalence (44.2 K)
lk_mx = find_flow(lambda lk: -(elite(A0, "R", "paste 0.07").evaluate(Q, lk)["dT_max"] - 44.2), 0.3, 2.0)
print(f"Equal MAX dT (44.2 K) with the same paste: {lk_mx*15:.1f} LPM ({lk_mx:.2f} LPM/kW)")

print("\n## 2x flow (36 LPM, 2.4 LPM/kW) and inlet 50 C (W+)")
for v in (elite(A0, "R", "PCM pad"), elite(A0, "R", "liquid metal"), elite(A0, "R", "PCM pad", port=20.0, name="HMMC-E/R PCM, 20 mm ports")):
    r = v.evaluate(Q, 2.4); sc = SCREEN_KPA_18 * 4
    print(f"- {v.name}: avg {r['dT_avg']:.1f} K, max {r['dT_max']:.1f} K, dP {r['dp_total_kPa']+sc:.1f} kPa, pump {(r['dp_total_kPa']+sc)*1e3*36/60e3:.1f} W, u_port {r['u_port']:.2f} m/s, u_slot {r['u_slot']:.2f} m/s")
r50 = elite(A0, "R", "PCM pad").evaluate(Q, 1.2, T_in=50.0)
print(f"- 50 C inlet, 18 LPM, E/R PCM: Tcase,max {r50['T_case_max']:.1f} C, Q cap {r50['Q_cap_kW']:.1f} kW")
rw = elite(A0, "R", "PCM pad").evaluate(Q, 1.2, fluid=WATER50)
print(f"- DI water, 18 LPM, E/R PCM: avg {rw['dT_avg']:.1f} / max {rw['dT_max']:.1f} K, dP {rw['dp_total_kPa']+SCREEN_KPA_18:.1f} kPa")

print("\n## GPU-class plates (1.2 LPM/kW unless stated)")
print(HDR)
for Qk, A, lk, label in ((2.3, 60, 1.0, "Rubin-class 2.3 kW, 60 cm2 lidded, 1.0 LPM/kW"), (2.3, 60, 1.2, "Rubin-class 2.3 kW, 60 cm2, 1.2"),
                         (3.6, 80, 1.0, "Rubin-Ultra-class 3.6 kW, 80 cm2, 1.0"), (4.0, 25, 1.5, "CoolIT-4kW TTV 4 kW, 25 cm2 (160 W/cm2), 1.5")):
    for v in (coolit_like(A), elite(A, "R", "PCM pad"), elite(A, "R", "liquid metal"), elite(A, "P", "liquid metal")):
        v = replace(v, name=f"{label}: {v.name.split('(')[0].strip()}")
        r = v.evaluate(Qk * 1e3, lk); print(row(r, screen=("CoolIT" not in v.name)))
    print("|  |  |  |  |  |  |  |  |  |  |  |  |  |")

print("\n## Real 2027-28 package (4 x 26x33 mm dies at 350 W/cm2 + 16 HBM, 12.85 kW, 15.4 LPM), hottest-die case-to-inlet, zoned")
print("fit from nonuniform-heatmap: dT = 33 + 3500/h_eff + 350 (R_TIM - 0.05); h_eff from the model core at the die-zone flow")
for core in ("R", "P"):
    v = elite(A0, core, "PCM pad"); r = v.evaluate(12850.0, 1.2)
    he = r["h_eff"] / 1e3
    for tim, Rt in (("paste 0.07", 0.07), ("PCM 0.055", 0.055), ("liquid metal 0.015", 0.015), ("direct-to-die LM (lid+TIM1 removed, ~ -28 K at junction)", 0.015)):
        dt = 33 + 3500 / he + 350 * (Rt - 0.05)
        print(f"- core {core}, h_eff {he:.0f} kW/m2K, {tim}: hot-die dT {dt:.1f} K -> Tcase {45+dt:.0f} C")
