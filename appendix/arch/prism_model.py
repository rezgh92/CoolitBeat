"""PRISM consolidated architecture: scorecard numbers.
Thermal: project scoping model (coldplate_model.py, unchanged) + three corrections derived this session:
  c2d   : 2-D Hele-Shaw / z-unmixed differential vs the calibrated CoolIT reconstruction (cell2d.py):
          R-grade (recessed-meter window 1.2/1.2 + 0.3 mm kerfs): +5.2 % of (cal+conv+base); P-grade +0.4 %;
          PSM slit without kerf: +8.2 % (for reference).
  ripple: case sawtooth crest = pk-pk/2 from cell2d (R 1.70 K, P 2.46 K at 128 W/cm2), scaled with flux, added to max.
  TIM   : TTV headline PCM at 25 psi 0.055 (P90 0.075); real-package Tier 1 PCM at module retention 0.07.
Hydraulics: element-by-element budget (this file), not the scoping model's lumped dP."""
import sys, math, numpy as np
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
import coldplate_model as cm
from dataclasses import replace
Q0, LK0, A0 = 15000.0, 1.2, 117.0
RHO, CP = 1005.0, 3930.0
TIMS = {"paste": (0.070, 0.10, 3.5), "paste_thin": (0.050, 0.07, 3.5), "PCM25": (0.055, 0.075, 1.5),
        "PCMpkg": (0.070, 0.09, 1.5), "LM": (0.015, 0.030, 0.6), "D2D": (0.015, 0.030, 0.6)}
cm.TIM.update({k: (v[0], v[2]) for k, v in TIMS.items()})

def prism(A=A0, grade="R", tim="PCM25", base=1.0, L=4.0, H=None, hs=1.5):
    g = dict(R=dict(gap=0.15, fin=0.15, H=2.0), P=dict(gap=0.10, fin=0.10, H=1.5))[grade]
    H = H or g["H"]; side = math.sqrt(A) * 10; n_slots = max(1, int(round(side / (2 * L))))
    return cm.ColdPlate(name=f"PRISM-{grade} {tim}", footprint_cm2=A, fin_t_mm=g["fin"], gap_mm=g["gap"], fin_h_mm=H,
                        flow_len_mm=L, base_mm=base, tim=tim, isothermal_cell=True, hotspot_flow_K=hs,
                        n_parallel_paths=2 * n_slots, slot_w_mm=3.0)

C2D = {"R": 0.052, "P": 0.004}; RIP = {"R": 1.70 / 2, "P": 2.46 / 2}

def evalp(p, Q=Q0, lk=LK0, grade="R", T_in=45.0):
    r = p.evaluate(Q, lk); q128 = r["q_W_cm2"] / 128.0
    core = r["dT_cal"] + r["dT_conv"] + r["dT_base"]
    corr = C2D[grade] * core
    avg = r["dT_avg"] + corr
    mx = avg + r["hotspot"] + RIP[grade] * q128
    return dict(r=r, avg=avg, max=mx, corr=corr, dTout=r["dT_out"], Rpp=avg / r["q_W_cm2"], q=r["q_W_cm2"],
                Tcmax=T_in + mx, Tout=T_in + r["dT_out"])

# ---------------- hydraulics: PRISM-15 Rev A element budget at 18 LPM (kPa), (viscous, inertial) parts
def dp_budget(port_mm=16.0, Kport=3.0):
    V = 18 / 60000; up = V / (math.pi / 4 * (port_mm * 1e-3) ** 2)
    el = {
        f"ports 2 x {port_mm:.0f} mm, K {Kport} (u {up:.2f} m/s)": (0.0, Kport * 0.5 * RHO * up ** 2 / 1e3),
        "guard screen 50 um abs (clean)": (0.30, 0.0),
        "headers (inlet 2x12x8 mm 0.78 m/s, outlet 2x14x8 mm 0.67 m/s), mid-fed tees K 1.5": (0.0, (1.5 * 0.5 * RHO * 0.78 ** 2 + 1.5 * 0.5 * RHO * 0.67 ** 2) / 1e3),
        "separator windows 3 x 10 mm, in + out, K 2": (0.0, 2 * 2 * 0.5 * RHO * 0.357 ** 2 / 1e3),
        "plenums 3 x 9 mm (friction + combining momentum)": (0.05, 0.10),
        "meter orifices 0.40 x 0.73 mm @ 2 mm (1.35 m/s, Cd 0.72)": (0.0, (1 / 0.72 ** 2) * 0.5 * RHO * 1.35 ** 2 / 1e3),
        "window cavity + kerf turn + outlet window": (0.02, 0.06),
        "fin channels 0.15 x 2.0 x ~3.7 mm": (0.28, 0.0),
    }
    return el

def dp_at(el, lpm):
    s = lpm / 18.0
    return sum(v * s + i * s * s for v, i in el.values())

if __name__ == "__main__":
    out = []
    P = lambda *a: (print(*a), out.append(" ".join(str(x) for x in a)))
    coo = cm.coolit_like(A0).evaluate(Q0, LK0)
    P("## A. Benchmark point, 15 kW / 18 LPM PG25 / 45 C / 117 cm2")
    P(f"CoolIT-like calibration: avg {coo['dT_avg']:.1f} max {coo['dT_max']:.1f} (measured 34.4 / 44.2); q {coo['q_W_cm2']:.0f} W/cm2; dTout {coo['dT_out']:.2f}")
    qC = coo['q_W_cm2']
    cpcm_avg = 34.4 - (0.070 - 0.055) * qC; cpcm_max = 44.2 - (0.070 - 0.055) * qC - 2.0 * qC / 128
    P(f"CoolIT re-tested with PCM (same TIM as ours, estimate): avg {cpcm_avg:.1f} max {cpcm_max:.1f}")
    rows = [("R paste 0.07 (like-for-like)", "R", "paste", 1.0), ("R named paste 0.05", "R", "paste_thin", 1.0),
            ("R PCM 25 psi (TTV headline)", "R", "PCM25", 1.0), ("R PCM at module retention 0.07", "R", "PCMpkg", 1.0),
            ("R LM (Tier 2)", "R", "LM", 1.0), ("R PCM, base 0.8", "R", "PCM25", 0.8), ("R paste, base 0.8", "R", "paste", 0.8),
            ("P paste", "P", "paste", 1.0), ("P PCM", "P", "PCM25", 1.0), ("P LM", "P", "LM", 1.0),
            ("R D2D LM base 0.8 (case=die top)", "R", "D2D", 0.8)]
    P("| design | cal | TIM | base | conv | 2-D corr | avg | max | R'' | Tcase,max | Qcap@1.2 LPM/kW | Qcap@18 LPM | inlet headroom |")
    P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    res = {}
    for lab, g, t, b in rows:
        p = prism(grade=g, tim=t, base=b); e = evalp(p, grade=g); r = e["r"]
        core = r["dT_cal"] + r["dT_conv"] + r["dT_base"]
        # Q cap at constant 1.2 LPM/kW: caloric & flow-hs constant; flux terms (TIM, base, conv, corr on conv+base, scatter, ripple) scale with Q
        flux = r["dT_tim"] + (r["dT_base"] + r["dT_conv"]) * (1 + C2D[g]) + (r["hotspot"] - 1.5) + RIP[g] * e["q"] / 128
        const = r["dT_cal"] * (1 + C2D[g]) + 1.5
        qcap = 15 * (40 - const) / flux
        # Q cap at fixed 18 LPM
        lo, hi = 5e3, 60e3
        for _ in range(60):
            mid = 0.5 * (lo + hi); ee = evalp(prism(grade=g, tim=t, base=b), Q=mid, lk=18.0 / (mid / 1000), grade=g)
            lo, hi = (mid, hi) if ee["max"] < 40 else (lo, mid)
        qcap18 = lo / 1000
        Tin = min(85 - e["max"], 65 - e["dTout"])
        res[lab] = e
        P(f"| {lab} | {r['dT_cal']:.1f} | {r['dT_tim']:.1f} | {r['dT_base']:.1f} | {r['dT_conv']:.1f} | {e['corr']:+.1f} | **{e['avg']:.1f}** | **{e['max']:.1f}** | {e['Rpp']:.3f} | {e['Tcmax']:.1f} | {qcap:.1f} | {qcap18:.1f} | {Tin:.1f} C (thermal {85-e['max']:.1f}) |")
    P(f"CoolIT Tcase,max 85 C inlet: {85-44.2:.1f} C; Qcap ~12.9 kW (synthesis)")
    P("")
    P("## B. Hard mode: everything at 100 cm2 (150 W/cm2) vs CoolIT measured; and footprint 145 cm2")
    for A in (100.0, 145.0):
        for lab, g, t, b in (("R paste", "R", "paste", 1.0), ("R PCM", "R", "PCM25", 1.0), ("R LM", "R", "LM", 1.0), ("P paste", "P", "paste", 1.0)):
            e = evalp(prism(A=A, grade=g, tim=t, base=b), grade=g)
            qa = 15000 / A; cP = 34.4 - (0.070 - 0.055) * qa
            P(f"A {A:.0f} cm2 {lab}: avg {e['avg']:.1f} max {e['max']:.1f} | CoolIT measured 34.4/44.2, CoolIT-with-PCM est {cP:.1f}/{44.2-(0.015*qa)-2*qa/128:.1f}")
    P("")
    P("## C. Hydraulics (PRISM-15 Rev A), element budget")
    for port in (16.0, 20.0):
        el = dp_budget(port_mm=port)
        tot18 = dp_at(el, 18); tot36 = dp_at(el, 36); tot15 = dp_at(el, 15); tot27 = dp_at(el, 27)
        if port == 16.0:
            for k, (v, i) in el.items(): P(f"  - {k}: {v + i:.2f} kPa")
        P(f"ports {port:.0f} mm: 15 LPM {tot15:.1f} | 18 LPM {tot18:.1f} kPa ({tot18*0.3:.2f} W) | 27 LPM {tot27:.1f} | 36 LPM {tot36:.1f} kPa ({tot36*0.6:.1f} W)")
    el = dp_budget(); inert = sum(i for v, i in el.values()); visc = sum(v for v, i in el.values())
    branch = 1.46 + 0.28 + 0.08  # meter + channels + window/kerf
    P(f"inertial fraction of plate dP {inert/(inert+visc):.2f}; branch (meter+channel+window) ~{branch:.2f} kPa, inertial frac {(1.46+0.06)/branch:.2f}")
    P(f"plenum long-half head (3x9, 0.50 m/s) {0.5*RHO*0.50**2:.0f} Pa -> along-slot ratio {branch*1e3/(0.5*RHO*0.5**2):.1f}; header head {0.5*RHO*0.78**2:.0f} Pa -> slot-to-slot ratio {(branch+0.26)*1e3/(0.5*RHO*0.78**2):.1f}")
    # equal pump power vs CoolIT-like 6.5 W
    lo, hi = 18.0, 60.0
    for _ in range(60):
        mid = 0.5 * (lo + hi); w = dp_at(el, mid) * 1e3 * mid / 60000
        lo, hi = (mid, hi) if w < 6.54 else (lo, mid)
    P(f"equal pumping power (6.5 W): {lo:.1f} LPM ({lo/15:.2f} LPM/kW), dP {dp_at(el, lo):.1f} kPa")
    for lab, g, t in (("R PCM", "R", "PCM25"), ("R paste", "R", "paste"), ("R LM", "R", "LM")):
        e = evalp(prism(grade=g, tim=t), lk=lo / 15, grade=g); P(f"   {lab} at equal pump power: {e['avg']:.1f} / {e['max']:.1f}")
    P("")
    P("## D. Flow sweep and flow-to-match (R grade)")
    for lab, t in (("PCM", "PCM25"), ("paste", "paste"), ("LM", "LM")):
        s = []
        for lk in (0.6, 0.75, 1.0, 1.2, 1.5, 2.0, 2.4):
            e = evalp(prism(tim=t), lk=lk); s.append(f"{lk}: {e['avg']:.1f}/{e['max']:.1f} (out {e['Tout']:.0f} C, dP {dp_at(el, lk*15):.1f})")
        P(f"{lab}: " + "; ".join(s))
        for target, key in ((34.4, "avg"), (44.2, "max")):
            lo, hi = 0.2, 1.2
            for _ in range(60):
                mid = 0.5 * (lo + hi); e = evalp(prism(tim=t), lk=mid)
                lo, hi = (lo, mid) if e[key] < target else (mid, hi)
            e = evalp(prism(tim=t), lk=hi)
            P(f"   flow to match CoolIT {key} {target}: {hi:.2f} LPM/kW ({hi*15:.1f} LPM), outlet {e['Tout']:.1f} C, dP {dp_at(el, hi*15):.1f} kPa")
    with open("prism_model.out", "w") as f: f.write("\n".join(out) + "\n")
