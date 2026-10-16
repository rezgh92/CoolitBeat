"""CoolIT 4 kW point: 4 kW, 6 LPM (1.5 LPM/kW), heater 25 cm2 (50x50 plate) or 20 cm2 ('shy of 200 W/cm2').
(1) PRISM variants with own 2-D penalty; (2) CoolIT-like reconstruction under alternative test conditions,
to find which conditions reproduce CoolIT's measured < 0.009 C/W; (3) PRISM / CoolIT-like ratios at equal conditions."""
import sys, math
from harness import ev, cm, TIMS
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../arch')))
from cell2d import run as cell
Q, LPM = 4000.0, 6.0
W = cm.WATER50
print("## (1) PRISM single-die SKU at 4 kW / 6 LPM, own 2-D penalty, max-case R (C/W); CoolIT < 0.009")
print("| build | A | fluid | TIM | avg | max | R C/W | pen | pk-pk |")
print("|---|---|---|---|---|---|---|---|---|")
builds = [("R L6 b1.0 (drop-in core)", dict()), ("R L5 b0.8", dict(L=5.0, base=0.8)), ("R L6 b0.8", dict(base=0.8)),
          ("R L6 b0.6", dict(base=0.6)),
          ("R+ gap0.12/t0.12 H1.8 L5 b0.8", dict(t=0.12, gap=0.12, H=1.8, L=5.0, base=0.8)),
          ("R+ gap0.12/t0.12 H1.8 L6 b0.8", dict(t=0.12, gap=0.12, H=1.8, L=6.0, base=0.8)),
          ("P 0.10/0.10x1.5 L4 b1.0", dict(t=0.10, gap=0.10, H=1.5, L=4.0)),
          ("P L5 b0.8", dict(t=0.10, gap=0.10, H=1.5, L=5.0, base=0.8)),
          ("P L5 b0.6", dict(t=0.10, gap=0.10, H=1.5, L=5.0, base=0.6))]
res = {}
for lab, kw in builds:
    for A in (25.0, 20.0):
        for fl in (cm.PG25, W):
            for tim in ("paste", "PCM25", "LM"):
                e = ev(A=A, Q=Q, lpm=LPM, tim=tim, fluid=fl, **kw)
                res[(lab, A, fl.name[:5], tim)] = e
                print(f"| {lab} | {A:.0f} | {fl.name[:5]} | {tim} | {e['avg']:.1f} | {e['max']:.1f} | **{e['max']/Q:.4f}** | {e['pen']:+.2f} | {e['pkpk']:.2f} |", flush=True)

print("\n## (2) CoolIT-like reconstruction (0.2/0.2x4, 2 mm base, split-flow, half-length 25 mm) at 4 kW / 6 LPM")
print("Ramp hot spot set to 0.5 dT_out (verify-physics fix); 2-D penalty: own cell2d run with end-face exit")
def coolit(A, fl, tim, pen=True):
    p = cm.coolit_like(A); p.tim = tim
    r = p.evaluate(Q, LPM / 4.0, fluid=fl); q = r["q_W_cm2"] * 1e4
    half = math.sqrt(A) * 10 / 2
    core1 = 0.5 * r["dT_out"] + r["dT_conv"] + r["dT_base"]
    if pen:
        c = cell(hi=2.5, ho=1.0, ki=0.0, ko=1.0, L=half, H=4.0, tb=2.0, d=0.1, q=q, dTout=r["dT_out"], h=r["h"], t=0.2, gap=0.2,
                 h_floor_out=10e3, Kkerf_mult=(1.0 / 0.2) ** 2 / 0.5, kf=fl.k, cp=fl.cp)
        core = c["case"]
    else:
        core = core1
    R, sc = TIMS[tim]
    avg = core + q * R * 1e-4
    mx = avg + 0.5 * r["dT_out"] + sc * q / 1.28e6
    return avg, mx, core, core1
print("| A | fluid | TIM | avg | max | R C/W | 2-D core / 1-D core |")
print("|---|---|---|---|---|---|---|")
for A in (25.0, 20.0):
    for fl in (cm.PG25, W):
        for tim in ("paste", "paste05", "PCM25", "LM"):
            a, m, c2, c1 = coolit(A, fl, tim)
            res[("CoolIT", A, fl.name[:5], tim)] = (a, m)
            print(f"| {A:.0f} | {fl.name[:5]} | {tim} | {a:.1f} | {m:.1f} | **{m/Q:.4f}** | {c2:.1f} / {c1:.1f} |", flush=True)

print("\n## (3) Ratio PRISM / CoolIT-like at identical conditions (max-case R)")
for lab in ("R L6 b1.0 (drop-in core)", "R L6 b0.8", "R+ gap0.12/t0.12 H1.8 L6 b0.8", "P L5 b0.8"):
    s = []
    for A in (25.0, 20.0):
        for fl in ("PG25 ", "water"):
            for tim in ("paste", "PCM25", "LM"):
                pr = res[(lab, A, fl, tim)]["max"]; co = res[("CoolIT", A, fl, tim)][1]
                s.append(f"{A:.0f}/{fl.strip()}/{tim}: {pr/co:.2f}")
    print(f"- {lab}: " + "; ".join(s))
