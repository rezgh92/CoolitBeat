#!/usr/bin/env python3
"""
d2d_run.py - numbers for the direct-to-die / chip-co-design proposal (key: direct-to-die).

Uses (1) the project scoping model docs/cooling/model/coldplate_model.py (v2, Darcy + isothermal caloric
corrections already applied) for the deterministic budgets and dP, and (2) the physics-synthesis evaluator
(appendix/physics/SYNTHESIS-physics.py) for Monte Carlo bands, so the numbers line up with the sibling
proposals.  Adds: liquid-metal direct-to-die face (Ni 5 um electrolytic), CuMo-faced lid-core,
junction-to-inlet stacks at 350 W/cm2 (lidded vs lidless vs lid-core vs in-die), BLT/warpage penalty,
GPU-class (2-4 kW) junction table, and equal-performance flows.

Run: python3 d2d_run.py > d2d_run.out
"""
import math
import sys
from dataclasses import replace

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../physics')))

import coldplate_model as cm  # noqa: E402
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "synth", __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../physics/SYNTHESIS-physics.py')))
synth = importlib.util.module_from_spec(spec)
sys.modules['synth'] = synth
spec.loader.exec_module(synth)

# ---------------------------------------------------------------- interface library (cm2K/W, scatter K @128)
R_NI5 = 5e-6 / 80 * 1e4          # electrolytic sulfamate Ni 5 um, k ~80 W/mK -> 0.000625 cm2K/W
cm.TIM["D2D LM + Ni5"] = (0.015 + R_NI5, 0.6)
cm.TIM["D2D PCM"] = (0.055, 1.5)
cm.TIM["In TIM1 (lid-core)"] = (0.025, 0.6)   # 150-200 um In + Ni/Au metallisation, Cu face
cm.TIM["LM EOL"] = (0.030, 0.6)

A0 = 117.0
Q, LK = 15000.0, 1.2
SCREEN_KPA_18 = 0.4              # integrated 50 um absolute pleated screen, clean, 18 LPM (scales ~V^1.5; use V^2)
K_CUMO = 170.0                   # Mo70Cu30 / CMC face, through-plane, W/mK
CUMO_T = 1.0                     # mm
CU_EQ_BASE = CUMO_T * cm.K_CU / K_CUMO   # Cu-equivalent thickness of a 1.0 mm CuMo face


def plate_rows():
    rows = [
        ("CoolIT-like skived split-flow, paste (calibrated)", cm.coolit_like(A0)),
        ("Engine R, flat Cu face, PCM  [Tier 1]", cm.hmmc(A0, core="R", tim="PCM pad")),
        ("Engine R, flat Ni face, LM on lid  [Tier 2]", cm.hmmc(A0, core="R", tim="liquid metal")),
        ("Engine R, pedestal 0.8 mm, LM + Ni5 on die  [Tier 3A]", cm.hmmc(A0, core="R", tim="D2D LM + Ni5", base_mm=0.8)),
        ("Engine R, pedestal 0.8 mm, PCM on die  [3A fallback]", cm.hmmc(A0, core="R", tim="D2D PCM", base_mm=0.8)),
        ("Engine R, pedestal 0.8 mm, LM EOL 0.030  [3A end-of-life]", cm.hmmc(A0, core="R", tim="LM EOL", base_mm=0.8)),
        ("Engine P (0.10 mm), pedestal 0.8, LM + Ni5  [3A-P, <=33 um loops]", cm.hmmc(A0, core="P", tim="D2D LM + Ni5", base_mm=0.8)),
        ("Lid-core R, Cu face 0.8 mm, In TIM1 0.025  [Tier 3B]", cm.hmmc(A0, core="R", tim="In TIM1 (lid-core)", base_mm=0.8)),
        ("Lid-core P, Cu face 0.8 mm, In TIM1 0.025  [3B-P]", cm.hmmc(A0, core="P", tim="In TIM1 (lid-core)", base_mm=0.8)),
        ("(illustrative) lid-core R, CuMo 1.0 mm face, In 0.015", cm.hmmc(A0, core="R", tim="liquid metal", base_mm=CU_EQ_BASE)),
    ]
    return rows


def hdr():
    return ("| design | caloric | TIM | base | conv | avg dT | max dT | R'' cm2K/W | dP plate kPa | dP +screen | pump W | Q cap kW | Tcase,max C |\n"
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")


def row(label, r, screen=True):
    scr = SCREEN_KPA_18 * (r["flow_lpm"] / 18.0) ** 2 if screen else 0.0
    dpt = r["dp_total_kPa"] + scr
    pump = dpt * 1e3 * r["flow_lpm"] / 60000
    return (f"| {label} | {r['dT_cal']:.1f} | {r['dT_tim']:.1f} | {r['dT_base']:.1f} | {r['dT_conv']:.1f} | "
            f"**{r['dT_avg']:.1f}** | **{r['dT_max']:.1f}** | {r['R_unit_cm2K_W']:.3f} | {r['dp_total_kPa']:.1f} | "
            f"{dpt:.1f} | {pump:.2f} | {r['Q_cap_kW']:.1f} | {r['T_case_max']:.1f} |")


def solve_flow_for(plate, key, target, lo=0.2, hi=3.0):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if plate.evaluate(Q, mid)[key] > target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    print("# d2d_run: direct-to-die / chip-co-design tier numbers\n")
    r0 = cm.coolit_like(A0).evaluate(Q, LK)
    print(f"Operating point: 15 kW, 18 LPM PG25, 45 C inlet, {A0:.0f} cm2 ({r0['q_W_cm2']:.0f} W/cm2), dT_out {r0['dT_out']:.2f} K")
    print(f"Ni 5 um electrolytic barrier R'' = {R_NI5:.5f} cm2K/W; CuMo 1.0 mm face = {CU_EQ_BASE:.2f} mm Cu-equivalent\n")

    # ------------------------------------------------------------- 1. TTV budget (project model)
    print("## 1. 15 kW TTV, project scoping model (coldplate_model.py v2)\n")
    print(hdr())
    for label, p in plate_rows():
        r = p.evaluate(Q, LK)
        print(row(label, r, screen=(not label.startswith("CoolIT"))))
    rT = cm.hmmc(A0, core="R", tim="D2D LM + Ni5", base_mm=0.8).evaluate(Q, LK)
    print(f"\n3A detail: NTU {rT['NTU']:.2f}, cal frac {rT['cal_frac']:.3f}, h {rT['h']/1e3:.1f} kW/m2K, eta {rT['eta']:.2f}, "
          f"h_eff {rT['h_eff']/1e3:.0f} kW/m2K, u_ch {rT['u_ch']:.3f} m/s, Re {rT['Re']:.0f}, u_slot {rT['u_slot']:.2f}, u_port {rT['u_port']:.2f} m/s")
    print(f"dP split (model): channel {rT['dp_ch_kPa']:.2f} + turns {rT['dp_K_kPa']:.2f} + slot {rT['dp_slot_kPa']:.2f} + header "
          f"{rT['dp_header_kPa']:.2f} + orifice {rT['dp_orif_kPa']:.2f} + ports {rT['dp_port_kPa']:.2f} = {rT['dp_total_kPa']:.2f} kPa (+ screen {SCREEN_KPA_18})\n")

    # 2x flow and 20 mm ports
    print("### 1b. 2x flow (36 LPM, 2.4 LPM/kW) and 20 mm ports\n")
    print(hdr())
    p3a = cm.hmmc(A0, core="R", tim="D2D LM + Ni5", base_mm=0.8)
    print(row("3A at 36 LPM, 16 mm ports", p3a.evaluate(Q, 2.4)))
    print(row("3A at 18 LPM, 20 mm ports", replace(p3a, port_bore_mm=20.0).evaluate(Q, 1.2)))
    print(row("3A at 36 LPM, 20 mm ports", replace(p3a, port_bore_mm=20.0).evaluate(Q, 2.4)))
    print(row("CoolIT-like at 36 LPM", cm.coolit_like(A0).evaluate(Q, 2.4), screen=False))
    print()

    # equal performance
    print("### 1c. Flow at which 3A reproduces CoolIT's measured 34.4 K avg / 44.2 K max\n")
    for label, p in (("3A LM", p3a), ("3A PCM fallback", cm.hmmc(A0, core="R", tim="D2D PCM", base_mm=0.8))):
        lk_avg = solve_flow_for(p, "dT_avg", 34.4)
        lk_max = solve_flow_for(p, "dT_max", 44.2)
        ra = p.evaluate(Q, lk_avg)
        rm = p.evaluate(Q, lk_max)
        print(f"- {label}: avg 34.4 K at {lk_avg:.2f} LPM/kW ({ra['flow_lpm']:.1f} LPM, {ra['dp_total_kPa']:.2f} kPa, "
              f"{ra['pump_W']:.2f} W); max 44.2 K at {lk_max:.2f} LPM/kW ({rm['flow_lpm']:.1f} LPM, {rm['dp_total_kPa']:.2f} kPa)")
    print()

    # flow sweep
    print("### 1d. Flow sweep, 3A LM (avg / max dT K, plate dP kPa incl. screen)\n")
    print("| LPM/kW | LPM | CoolIT-like avg / max / dP | 3A LM avg / max / dP | 3A-P LM avg / max / dP |")
    print("|---:|---:|---|---|---|")
    pP = cm.hmmc(A0, core="P", tim="D2D LM + Ni5", base_mm=0.8)
    for lk in (0.6, 0.75, 1.0, 1.2, 1.5, 2.0, 2.4):
        a = cm.coolit_like(A0).evaluate(Q, lk)
        b = p3a.evaluate(Q, lk)
        c = pP.evaluate(Q, lk)
        s = SCREEN_KPA_18 * (lk / 1.2) ** 2
        print(f"| {lk:.2f} | {a['flow_lpm']:.1f} | {a['dT_avg']:.1f} / {a['dT_max']:.1f} / {a['dp_total_kPa']:.1f} | "
              f"{b['dT_avg']:.1f} / {b['dT_max']:.1f} / {b['dp_total_kPa']+s:.1f} | {c['dT_avg']:.1f} / {c['dT_max']:.1f} / {c['dp_total_kPa']+s:.1f} |")
    print()

    # ------------------------------------------------------------- 2. Monte Carlo (synthesis evaluator)
    print("## 2. Monte Carlo bands (synthesis evaluator, 20k samples; P10 / P50 / P90)\n")
    D = synth.hmmc
    designs = [
        synth.COOLIT,
        D("Tier 1 PCM, engine R", 0.15, 0.10, 2.0, 4.0, 1.0, 0.055, 0.04, 0.08, "PCM", 1.5),
        D("Tier 2 LM on lid, engine R", 0.15, 0.10, 2.0, 4.0, 1.0, 0.015, 0.005, 0.03, "LM", 0.6),
        D("Tier 3A D2D LM+Ni, engine R, base 0.8", 0.15, 0.10, 2.0, 4.0, 0.8, 0.0156, 0.005, 0.03, "LM", 0.6),
        D("Tier 3A D2D PCM fallback, base 0.8", 0.15, 0.10, 2.0, 4.0, 0.8, 0.055, 0.04, 0.08, "PCM", 1.5),
        D("Tier 3A-P D2D LM+Ni, engine P, base 0.8", 0.10, 0.10, 1.5, 4.0, 0.8, 0.0156, 0.005, 0.03, "LM", 0.6,
          deployable="<=33 um loops"),
        D("Tier 3B Cu lid-core, In TIM1 0.025, face 0.8", 0.15, 0.10, 2.0, 4.0, 0.8, 0.025, 0.015, 0.035,
          "In", 0.6),
    ]
    print("| design | avg dT | max dT | dP plate kPa | pump W | Q cap kW (Tcase,max<=85 C) |")
    print("|---|---|---|---|---|---|")
    mc = {}
    for d in designs:
        b = synth.monte_carlo(d, n=20000, seed=7)
        mc[d.name] = b
        f = lambda t: f"{t[0]:.1f} / {t[1]:.1f} / {t[2]:.1f}"
        print(f"| {d.name} | {f(b['dT_avg'])} | {f(b['dT_max'])} | {f(b['dp_kPa'])} | "
              f"{b['pump_W'][0]:.2f} / {b['pump_W'][1]:.2f} / {b['pump_W'][2]:.2f} | {f(b['Qcap'])} |")
    print("\n(dP excludes the integrated screen: add 0.4 kPa clean / 1.2 kPa at the 3x alarm.)\n")
    print("Deterministic synthesis values:")
    for d in designs:
        r = synth.evaluate(d, Q, LK)
        print(f"- {d.name}: avg {r['dT_avg']:.2f}, max {r['dT_max']:.2f}, dP {r['dp_kPa']:.2f} kPa, pump {r['pump_W']:.2f} W, "
              f"Qcap {synth.q_capacity(d, LK):.1f} kW, h_eff {r['h_eff']/1e3:.0f} kW/m2K")
    print()

    # ------------------------------------------------------------- 3. junction-to-inlet at 350 W/cm2
    print("## 3. Reticle die at 350 W/cm2 (4 x 26 x 33 mm + 16 HBM, 12.85 kW, 15.4 LPM, heat-proportional zoning)\n")
    q = 350.0  # W/cm2
    R_SI = 0.050      # 0.6 mm Si at ~120 W/mK (0.065 for 775 um)
    R_TIM1_IN = 0.015
    R_LID = 2.5e-3 / 390 * 1e4      # 0.064, 1-D
    S_LID = 0.85      # lid-top flux / die flux (2.5 mm lateral spreading at the 53 x 67 mm die-block edge)
    S_LIDMID = 0.92   # mean flux through the lid thickness
    CAL_ZONED = 6.7   # K, hottest die cell, H-Z2 zoning (nonuniform-heatmap)
    heff = {"R": 127.0e3, "P": 187.0e3}

    def plate_side(core, base_mm, k_base=390.0):
        return base_mm * 1e-3 / k_base * 1e4 + 1e4 / heff[core]

    paths = []
    # CoolIT-like split-flow lidded paste: case from heat-map report (88.6 K at paste 0.05) +7 K for paste 0.07
    case_c = 88.6 + (0.07 - 0.05) * q
    paths.append(("CoolIT-like split-flow on lid, paste 0.07 (case from 3-D heat-map)", case_c, None,
                  case_c + q * (S_LIDMID * R_LID + R_TIM1_IN + R_SI)))
    for core in ("R", "P"):
        for lab, rt in (("PCM 0.055", 0.055), ("LM 0.015", 0.015)):
            case = CAL_ZONED + S_LID * q * (rt + plate_side(core, 1.0))
            tj = case + q * (S_LIDMID * R_LID + R_TIM1_IN + R_SI)
            paths.append((f"Engine {core}, lidded, TIM2 {lab}, base 1.0  [Tier {'1' if rt > 0.03 else '2'}]", case, None, tj))
        die = CAL_ZONED + q * (0.015 + R_NI5 + plate_side(core, 0.8))
        paths.append((f"Engine {core}, direct-to-die pedestal, LM + Ni5, base 0.8  [Tier 3A]", None, die, die + q * R_SI))
        die_p = CAL_ZONED + q * (0.055 + plate_side(core, 0.8))
        paths.append((f"Engine {core}, direct-to-die pedestal, PCM 0.055  [3A fallback]", None, die_p, die_p + q * R_SI))
        die_b = CAL_ZONED + q * (0.025 + plate_side(core, 0.8))
        paths.append((f"Engine {core} Cu lid-core, In TIM1 0.025 (170 um), face 0.8  [Tier 3B]", None, die_b, die_b + q * R_SI))
        die_b2 = CAL_ZONED + q * (0.015 + plate_side(core, CUMO_T, K_CUMO))
        paths.append((f"Engine {core} lid-core, CuMo 1.0 mm face, In 0.015 (illustrative low-CTE)", None, die_b2, die_b2 + q * R_SI))
    # in-die microfluidics (Corintis / Microsoft) - junction-to-fluid 0.02 (0.01-0.05)
    for lab, rj in (("0.02 nominal", 0.02), ("0.05 pessimistic", 0.05)):
        paths.append((f"In-die microfluidics, j-to-fluid {lab}", None, None, CAL_ZONED + q * rj))
    print("| path | lid-top case dT K | die-top dT K | **Tj-to-inlet K** | Tj at 45 C inlet | inlet for Tj = 105 C | R''j-in cm2K/W (excl. caloric) | max die flux at Tj<=105 C, 45 C in (W/cm2) |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|")
    tj_ref = None
    for lab, case, die, tj in paths:
        if tj_ref is None:
            tj_ref = tj
        rjin = (tj - CAL_ZONED) / q if "CoolIT" not in lab else (tj - 13.9) / q
        cal = 13.9 if "CoolIT" in lab else CAL_ZONED
        qmax = q * (60.0 - cal) / (tj - cal)
        print(f"| {lab} | {case if case is None else round(case, 1)} | {die if die is None else round(die, 1)} | **{tj:.1f}** | "
              f"{45 + tj:.0f} | {105 - tj:.0f} | {rjin:.3f} | {qmax:.0f} |")
    print("\nNotes: lidded stacks get a lateral-spreading credit (lid-top flux 0.85x die flux, lid mean 0.92x); the "
          "die-top and junction values are 1-D at the die centre; Si 0.6 mm = 0.050 cm2K/W (775 um: +5 K); on-die "
          "2-3x hot spots add 5-15 K for every path except in-die (nonuniform-heatmap caveat).\n")

    # HBM
    print("### 3b. HBM (40 W/cm2) by interface over the pedestal (base-top dT under HBM max 18.7 K for H-Z2)\n")
    for lab, rh in (("paste 0.45 mm gap fill (1.16)", 1.16), ("Cu pedestal + 0.1 mm PCM putty (0.28)", 0.28),
                    ("pedestal + LM 50-100 um single-field (0.04)", 0.04), ("pedestal + indium (0.06)", 0.06)):
        hbm_case = 18.7 + 40 * rh
        print(f"- {lab}: HBM case dT {hbm_case:.1f} K, Tj HBM ~{45 + hbm_case + 53 * 0.3:.0f} C (53 W/stack x 0.3 K/W)")
    print()

    # BLT / warpage penalty at 350 W/cm2
    print("### 3c. Bond-line penalty at 350 W/cm2 (die-top dT added by the interface)\n")
    print("| BLT um | LM (k 22, Rc 0.004) K | PCM (k 8.5, Rc 0.02) K | paste (k 3.5, Rc 0.012) K |")
    print("|---:|---:|---:|---:|")
    for blt in (15, 30, 50, 80):
        lm = q * (blt * 1e-6 / 22 * 1e4 + 0.004)
        pcm = q * (blt * 1e-6 / 8.5 * 1e4 + 0.02)
        pas = q * (blt * 1e-6 / 3.5 * 1e4 + 0.012)
        print(f"| {blt} | {lm:.1f} | {pcm:.1f} | {pas:.1f} |")
    print()

    # ------------------------------------------------------------- 4. GPU-class
    print("## 4. GPU-class plates (2-4 kW), plate-level model and die-level junction\n")
    print("### 4a. Plate-level, project model on the plate footprint (lidded framing as in sibling proposals)\n")
    print(hdr())
    for Qk, A, lk, name in ((2.3, 60, 1.0, "Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW"),
                            (3.6, 80, 1.0, "Rubin Ultra 3.6 kW, 80 cm2, 1.0 LPM/kW"),
                            (4.0, 25, 1.5, "CoolIT 4 kW TTV point, 25 cm2, 1.5 LPM/kW")):
        for lab, p in (("CoolIT-like", cm.coolit_like(A)),
                       ("T1 PCM", cm.hmmc(A, core="R", tim="PCM pad")),
                       ("T3A LM pedestal", cm.hmmc(A, core="R", tim="D2D LM + Ni5", base_mm=0.8))):
            r = p.evaluate(Qk * 1e3, lk)
            print(row(f"{name}: {lab}", r, screen=(lab != "CoolIT-like")))
    print()

    print("### 4b. Die-level junction-to-inlet (die-zone sub-plate, heat-proportional zoning)\n")
    print("Die-zone sub-plate: footprint = logic area, Q = package - HBM, flow = 88 % of package flow; "
          "CoolIT-like: unzoned split-flow, hottest-die caloric 1.1 x dT_out (heat-map ratio 13.9/12.66).\n")
    print("| device / flux | path | caloric | Tj-to-inlet at die avg K | Tj-to-inlet at 300 W/cm2 patch K | Tj avg / patch at 45 C |")
    print("|---|---|---:|---:|---:|---|")
    for Qk, A_logic, n_hbm, w_hbm, lk, dev in ((2.3, 16.6, 8, 45, 1.0, "Rubin 2.3 kW"),
                                               (3.6, 33.0, 16, 45, 1.0, "Rubin Ultra 3.6 kW")):
        Qd = Qk * 1e3 - n_hbm * w_hbm
        qd = Qd / A_logic
        flow = lk * Qk
        dT_out_pkg = Qk * 1e3 / (flow / 60000 * cm.PG25.rho * cm.PG25.cp)
        sub = cm.hmmc(A_logic, core="R", tim="D2D LM + Ni5", base_mm=0.8)
        rs = sub.evaluate(Qd, 0.88 * flow / (Qd / 1e3))
        cal_z = rs["dT_cal"]
        cal_c = 1.1 * dT_out_pkg
        for path, cal, stack in (
            ("CoolIT-like lidded paste", cal_c, lambda qq: qq * (R_SI + R_TIM1_IN + S_LIDMID * R_LID + S_LID * (0.07 + 2.0e-3 / 390 * 1e4 + 1e4 / 101e3))),
            ("T1 lidded PCM (engine R)", cal_z, lambda qq: qq * (R_SI + R_TIM1_IN + S_LIDMID * R_LID + S_LID * (0.055 + plate_side("R", 1.0)))),
            ("T2 lidded LM (engine R)", cal_z, lambda qq: qq * (R_SI + R_TIM1_IN + S_LIDMID * R_LID + S_LID * (0.015 + plate_side("R", 1.0)))),
            ("T3A D2D LM (engine R)", cal_z, lambda qq: qq * (R_SI + 0.015 + R_NI5 + plate_side("R", 0.8))),
            ("T3B Cu lid-core In 0.025 (engine R)", cal_z, lambda qq: qq * (R_SI + 0.025 + plate_side("R", 0.8))),
        ):
            ta = cal + stack(qd)
            tp = cal + stack(300.0)
            print(f"| {dev}, {qd:.0f} W/cm2 die avg | {path} | {cal:.1f} | {ta:.1f} | {tp:.1f} | {45+ta:.0f} / {45+tp:.0f} C |")
    print()

    # ------------------------------------------------------------- 5. Rubin-Ultra-class D2D plate hydraulics
    print("## 5. Rubin-Ultra-class D2D plate (fin field ~80 x 95 mm = 76 cm2, 3.6 kW)\n")
    pr = cm.hmmc(76.0, core="R", tim="D2D LM + Ni5", base_mm=0.8)
    pr = replace(pr, port_bore_mm=10.0, header_u_m_s=0.5 * 18 / 4.3, orifice_dp_kPa_18=1.5 * (18 / 4.3) ** 2)
    for lk in (1.0, 1.2, 2.4):
        r = pr.evaluate(3600.0, lk)
        print(f"- {lk} LPM/kW ({r['flow_lpm']:.1f} LPM): dP plate {r['dp_total_kPa']:.2f} kPa (+screen {0.15*(r['flow_lpm']/4.3)**2:.2f}) (10 mm bores, comb 1.5 kPa at 4.3 LPM), u_port {r['u_port']:.2f} m/s, "
              f"case-to-inlet avg on 76 cm2 uniform {r['dT_avg']:.1f} K")
    print("  (at 3-4 LPM the comb must be re-sized to keep branch dP >= 6x header head: hole count scaled to flow,"
          " target 1.5-2 kPa branch -> ~3 kPa plate)\n")


if __name__ == "__main__":
    main()
