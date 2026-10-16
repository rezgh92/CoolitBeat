#!/usr/bin/env python3
"""Scoping-model run for the CrossComb (conventional-cost) architecture.
Imports the project model unchanged; only geometry/loss inputs differ."""
import sys, math
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
from coldplate_model import ColdPlate, hmmc, coolit_like, TIM, PG25, WATER50
from dataclasses import replace

Q, A0 = 15000.0, 117.0

def crosscomb(footprint_cm2, *, tim="PCM pad", hotspot=2.0, port_mm=16.0, core="R", base_mm=1.0, screen_kPa=0.4, name="CrossComb"):
    """CrossComb: skived 0.10/0.15x2.0 mm core (R) or 0.10/0.10x1.5 (P), gang-slit comb with 3.0 mm slots at 8 mm pitch
    (4 mm flow length), stamped selector floor with per-slot metering slits (~2.5 kPa at 18 LPM), end-fed headers
    at <=0.75 m/s, horizontal ports. Integrated 50 um absolute inlet screen (~0.4 kPa clean at 18 LPM, quadratic)."""
    cores = {"R": dict(gap_mm=0.15, fin_t_mm=0.10, fin_h_mm=2.0, orifice=2.5),
             "P": dict(gap_mm=0.10, fin_t_mm=0.10, fin_h_mm=1.5, orifice=2.0)}[core]
    side = math.sqrt(footprint_cm2) * 10
    n_slots = max(1, int(round(side / 8.0)))
    return ColdPlate(name=f"{name}-{core} ({footprint_cm2:.0f} cm2, {tim})", footprint_cm2=footprint_cm2,
        fin_t_mm=cores["fin_t_mm"], gap_mm=cores["gap_mm"], fin_h_mm=cores["fin_h_mm"], flow_len_mm=4.0,
        base_mm=base_mm, tim=tim, isothermal_cell=True, hotspot_flow_K=hotspot,
        n_parallel_paths=2 * n_slots, slot_w_mm=3.0, K_channel=3.0, K_slot=1.5,
        header_u_m_s=0.86, K_header=1.5, port_bore_mm=port_mm, K_port=2.3,
        orifice_dp_kPa_18=cores["orifice"] + screen_kPa)

def row(r, extra=""):
    print(f"| {r['name']:<46} | {r['flow_lpm']:5.1f} | {r['dT_cal']:4.1f} | {r['dT_tim']:4.1f} | {r['dT_base']:4.1f} | {r['dT_conv']:4.1f} | "
          f"**{r['dT_avg']:4.1f}** | {r['dT_max']:4.1f} | {r['T_case_max']:5.1f} | {r['R_unit_cm2K_W']:5.3f} | {r['dp_total_kPa']:5.1f} | "
          f"{r['pump_W']:4.1f} | {r['Q_cap_kW']:4.1f} |{extra}")

hdr = ("| design | LPM | cal | TIM | base | conv | **avg dT K** | max dT K | Tcase,max C | R'' cm2K/W | dP kPa | pump W | Q cap kW |\n"
       "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

print("## A. 15 kW / 18 LPM PG25 / 45 C / 117 cm2 (128 W/cm2)")
print(hdr)
row(coolit_like(A0).evaluate(Q, 1.2))
for hs, lab in ((3.0, "conservative +/-20%"), (2.0, "nominal +/-10%"), (1.3, "stretch, verified +/-5%")):
    row(crosscomb(A0, tim="paste 0.07", hotspot=hs, name=f"CrossComb paste [{lab}]").evaluate(Q, 1.2))
for hs, lab in ((3.0, "conservative"), (2.0, "nominal"), (1.3, "stretch")):
    row(crosscomb(A0, tim="PCM pad", hotspot=hs, name=f"CrossComb PCM T1 [{lab}]").evaluate(Q, 1.2))
for hs, lab in ((3.0, "conservative"), (2.0, "nominal"), (1.3, "stretch")):
    row(crosscomb(A0, tim="liquid metal", hotspot=hs, name=f"CrossComb LM T2 [{lab}]").evaluate(Q, 1.2))
row(crosscomb(A0, tim="PCM pad", hotspot=2.0, core="P", name="CrossComb-P PCM (<=25um loops)").evaluate(Q, 1.2))
row(crosscomb(A0, tim="liquid metal", hotspot=2.0, core="P", name="CrossComb-P LM (<=25um loops)").evaluate(Q, 1.2))
row(crosscomb(A0, tim="PCM pad", hotspot=2.0, port_mm=13.0, name="CrossComb PCM, 13 mm (1/2 in) ports").evaluate(Q, 1.2))
row(crosscomb(A0, tim="PCM pad", hotspot=2.0, base_mm=0.8, name="CrossComb PCM, 0.8 mm base").evaluate(Q, 1.2))
row(crosscomb(A0, tim="PCM pad", hotspot=2.0, base_mm=1.2, name="CrossComb PCM, 1.2 mm base").evaluate(Q, 1.2))
row(crosscomb(A0, tim="PCM pad", hotspot=2.0, name="CrossComb PCM water").evaluate(Q, 1.2, fluid=WATER50))

r = crosscomb(A0, tim="PCM pad", hotspot=2.0).evaluate(Q, 1.2)
print(f"\nNominal detail: NTU {r['NTU']:.2f}, cal_frac {r['cal_frac']:.2f}, h {r['h']/1e3:.1f} kW/m2K, eta {r['eta']:.2f}, h_eff {r['h_eff']/1e3:.0f} kW/m2K,"
      f" u_ch {r['u_ch']:.3f} m/s Re {r['Re']:.0f}, u_slot {r['u_slot']:.2f} m/s, u_port {r['u_port']:.2f} m/s;"
      f" dP: channel {r['dp_ch_kPa']:.2f} + turns {r['dp_K_kPa']:.2f} + slot {r['dp_slot_kPa']:.2f} + header {r['dp_header_kPa']:.2f}"
      f" + slit+screen {r['dp_orif_kPa']:.2f} + ports {r['dp_port_kPa']:.2f} = {r['dp_total_kPa']:.1f} kPa")

print("\n## B. Flow sweep (117 cm2, 15 kW): CoolIT-like paste vs CrossComb PCM (nominal) vs CrossComb LM")
print("| LPM/kW | LPM | CoolIT avg | max | dP | pump W | CC-PCM avg | max | dP | pump W | CC-LM avg | max |")
print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
for lk in (0.5, 0.6, 0.75, 0.9, 1.0, 1.2, 1.5, 2.0, 2.4, 3.0):
    a = coolit_like(A0).evaluate(Q, lk)
    b = crosscomb(A0, tim="PCM pad", hotspot=2.0).evaluate(Q, lk)
    c = crosscomb(A0, tim="liquid metal", hotspot=2.0).evaluate(Q, lk)
    print(f"| {lk:.2f} | {a['flow_lpm']:.1f} | {a['dT_avg']:.1f} | {a['dT_max']:.1f} | {a['dp_total_kPa']:.1f} | {a['pump_W']:.1f} | "
          f"{b['dT_avg']:.1f} | {b['dT_max']:.1f} | {b['dp_total_kPa']:.1f} | {b['pump_W']:.1f} | {c['dT_avg']:.1f} | {c['dT_max']:.1f} |")

# flow at which CrossComb PCM / paste reproduces CoolIT 34.4 K avg
for tim in ("PCM pad", "paste 0.07"):
    lo, hi = 0.2, 1.2
    for _ in range(50):
        mid = 0.5*(lo+hi)
        if crosscomb(A0, tim=tim, hotspot=2.0).evaluate(Q, mid)['dT_avg'] > 34.4: lo = mid
        else: hi = mid
    rr = crosscomb(A0, tim=tim, hotspot=2.0).evaluate(Q, 0.5*(lo+hi))
    print(f"Flow-equivalence ({tim}): {0.5*(lo+hi):.2f} LPM/kW = {rr['flow_lpm']:.1f} LPM gives 34.4 K avg (max {rr['dT_max']:.1f}), dP {rr['dp_total_kPa']:.1f} kPa, pump {rr['pump_W']:.2f} W")
# equal pumping power to CoolIT-like at 18 LPM
target = coolit_like(A0).evaluate(Q, 1.2)['pump_W']
lo, hi = 1.2, 4.0
for _ in range(50):
    mid = 0.5*(lo+hi)
    if crosscomb(A0, tim="PCM pad", hotspot=2.0).evaluate(Q, mid)['pump_W'] < target: lo = mid
    else: hi = mid
rr = crosscomb(A0, tim="PCM pad", hotspot=2.0).evaluate(Q, 0.5*(lo+hi))
print(f"Equal pump power ({target:.1f} W): CrossComb PCM at {rr['flow_lpm']:.1f} LPM ({0.5*(lo+hi):.2f} LPM/kW): avg {rr['dT_avg']:.1f} / max {rr['dT_max']:.1f} K, dP {rr['dp_total_kPa']:.1f} kPa")

print("\n## C. Other loads/footprints at 1.2 LPM/kW (uniform TTV): CoolIT-like paste vs CrossComb PCM vs CrossComb LM")
print(hdr)
for Qk, A in ((1.0, 36), (1.4, 45), (2.3, 60), (3.6, 80), (3.6, 117), (15, 117), (20, 117), (25, 117), (30, 150), (50, 250)):
    row(coolit_like(A).evaluate(Qk*1e3, 1.2))
    row(crosscomb(A, tim="PCM pad", hotspot=2.0).evaluate(Qk*1e3, 1.2))
    row(crosscomb(A, tim="liquid metal", hotspot=2.0).evaluate(Qk*1e3, 1.2))
print("\nGPU-class at 2.0 LPM/kW (CrossComb has the dP headroom):")
print(hdr)
for Qk, A in ((1.4, 45), (2.3, 60), (3.6, 80)):
    row(coolit_like(A).evaluate(Qk*1e3, 1.2))
    row(crosscomb(A, tim="PCM pad", hotspot=2.0).evaluate(Qk*1e3, 2.0))

print("\n## D. Die-zone estimate, Rubin-class 2-die package (16.6 cm2 logic at 117 W/cm2 = 1.95 kW; 2.3 kW total at 1.0 LPM/kW = 2.3 LPM)")
print("Zoned CrossComb: die zone gets 85 % of flow (1.96 LPM). CoolIT-like split-flow: die zone sees the fresh centre fluid but at ")
print("area-proportional flow (16.6/60 of 2.3 LPM = 0.64 LPM) and a long ramp; both evaluated on the 16.6 cm2 die footprint.")
print(hdr)
die_A, die_Q = 16.6, 1950.0
cc = replace(crosscomb(die_A, tim="PCM pad", hotspot=2.0), name="CrossComb zoned die zone, PCM")
r = cc.evaluate(die_Q, 1.96/1.95); row(r)
cc = replace(crosscomb(die_A, tim="liquid metal", hotspot=2.0), name="CrossComb zoned die zone, LM")
r = cc.evaluate(die_Q, 1.96/1.95); row(r)
cp = replace(coolit_like(die_A), name="CoolIT-like die zone (area-share flow), paste")
r = cp.evaluate(die_Q, 0.64/1.95); row(r)
cp = replace(coolit_like(die_A), name="CoolIT-like die zone (all 2.3 LPM over dies), paste")
r = cp.evaluate(die_Q, 2.3/1.95); row(r)

print("\n## E. 2027-28 stress package: hottest die cell, fit dT = 33 + 3500/h_eff + 350 (R_TIM - 0.05) [nonuniform-heatmap]")
for core, heff in (("R robust 0.15 mm", 127), ("P performance 0.10 mm", 187)):
    for tim, Rt in (("paste 0.05", 0.05), ("PCM 0.055", 0.055), ("LM 0.015", 0.015)):
        dT = 33 + 3500/heff + 350*(Rt-0.05)
        print(f"  {core:<24} {tim:<10}: hot-die case dT {dT:5.1f} K -> T_case {45+dT:5.1f} C")
print("  CoolIT-like split-flow (report): 88.6 K paste -> 134 C; ~76 K LM -> ~121 C")
# Rubin-Ultra realistic: die-average ~120 W/cm2 with 300-350 W/cm2 patches: scale flux terms
for core, heff in (("R robust", 127), ("P perf", 187)):
    for tim, Rt in (("PCM", 0.055), ("LM", 0.015)):
        flux_terms = (3500/heff + 350*(Rt-0.05) + 350*0.05 + 9.0)  # conv + TIM + base at 350 (base 1 mm = 9 K at 350)
        # at 350: 33 = caloric 6.7 + base 9 + ... hmm; reconstruct: dT = cal(6.7) + base + conv + TIM
        cal = 6.7
        conv350 = 3500/heff; base350 = 9.0; tim350 = 350*Rt
        for qf in (120, 200):
            dT = cal + (conv350 + base350 + tim350)*qf/350
            print(f"  Rubin-class die-average {qf} W/cm2, {core} {tim}: hot-die dT ~{dT:4.1f} K -> {45+dT:4.1f} C")

print("\n## F. 2x flow (36 LPM) dP and velocities")
r = crosscomb(A0, tim="PCM pad", hotspot=2.0).evaluate(Q, 2.4)
print(f"CrossComb at 36 LPM: dP {r['dp_total_kPa']:.1f} kPa (ch {r['dp_ch_kPa']:.2f}, header {r['dp_header_kPa']:.2f}, slit+screen {r['dp_orif_kPa']:.2f}, ports {r['dp_port_kPa']:.2f}), u_port {r['u_port']:.2f} m/s, u_slot {r['u_slot']:.2f}, u_ch {r['u_ch']:.3f}, pump {r['pump_W']:.1f} W, avg {r['dT_avg']:.1f}/max {r['dT_max']:.1f}")
r = coolit_like(A0).evaluate(Q, 2.4)
print(f"CoolIT-like at 36 LPM: dP {r['dp_total_kPa']:.1f} kPa, pump {r['pump_W']:.1f} W, avg {r['dT_avg']:.1f}/max {r['dT_max']:.1f}")

print("\n## G. Geometry/hydraulic sanity (hand calc)")
n_in = 13; q_slot = 18/60/1000/n_in; half = q_slot/2
for depth in (8, 10, 12, 15):
    A = 3.0e-3*depth*1e-3; u = half/A; dyn = 0.5*1005*u**2
    branch = 230 + 30  # Pa: channel + turns at 18 LPM (model)
    print(f"  slot 3.0 x {depth} mm: entry u {u:.2f} m/s, dyn head {dyn:.0f} Pa, branch/dyn = {branch/dyn:.1f}")
for w_slit in (1.2, 1.5, 2.0):
    A = w_slit*12e-6*1e-3*1e3  # mm2 -> m2
    A = w_slit*12/1e6; u = q_slot/A; dp = 1.5*0.5*1005*u**2
    print(f"  selector slit {w_slit} x 12 mm: u {u:.2f} m/s, dp {dp/1e3:.2f} kPa at 18 LPM")
for hw, hh in ((20, 10), (15, 10), (25, 12)):
    A = hw*hh/1e6; u = 18/60/1000/A; dyn = 0.5*1005*u**2
    print(f"  end-fed header {hw}x{hh} mm: u {u:.2f} m/s, dyn head {dyn:.0f} Pa (branch ~2.8 kPa -> ratio {2800/dyn:.0f})")
# tie stress
for burst in (1.5, 2.0):
    fin_sigma = burst*0.25/0.10; f_bond = 1.0/4.0; bond = fin_sigma/f_bond
    print(f"  burst {burst} MPa: fin tensile {fin_sigma:.1f} MPa, bond-line nominal {bond:.0f} MPa (25 % bonded), Kt2.5 local {bond*2.5*f_bond:.0f} MPa in fin tip")
# base ripple (Fourier lumped) for 8 mm period, 3 mm Cu, h_eff 127e3
for Lp, t in ((4e-3, 2e-3), (8e-3, 3e-3), (12e-3, 3e-3)):
    k2 = 2*math.pi/Lp; att = 1/(math.cosh(k2*t) + (390*k2/127e3)*math.sinh(k2*t))
    print(f"  period {Lp*1e3:.0f} mm, Cu {t*1e3:.0f} mm: Fourier attenuation {att:.3f} -> {12.7*att:.2f} K pk-pk (FV ~2x) ")
# copper mass
for lab, dims in (("15kW-class 125x125", (125,125)), ("GPU-class 110x120", (110,120))):
    w,l = dims; fa = (w-17)*(l-17)
    base = w*l*2.8/1000; comb_blank = w*l*10/1000; comb_net = comb_blank - fa*10*0.75/1000; floor = w*l*2/1000
    cover = (w*l*5 + 50*l*9)/1000
    blank = base+comb_blank+floor+cover; net = base*0.75 + comb_net + floor + cover
    print(f"  {lab}: blank {blank*8.96/1000:.2f} kg, finished ~{net*8.96/1000:.2f} kg (base {base*8.96/1000:.2f}, comb net {comb_net*8.96/1000:.2f}, floor {floor*8.96/1000:.2f}, cover {cover*8.96/1000:.2f})")
