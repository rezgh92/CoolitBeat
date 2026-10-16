"""Final-architecture thermal numbers (Rev A = PKG-A family), chief-architect final revision 2026-10-14.
Method = verify-physics / close-the-losses harness (cell2d absolute 2-D core with PRISM's own penalty, 1-D TIM,
hot spot = 1.5 K flow + TIM scatter scaled by flux + ripple crest), with ONE change: PG25 conductivity 0.49 W/mK
instead of 0.52 (verify-physics: 0.52 is ~5 % high). The CoolIT-like reconstruction is patched for the flow sweep:
split-flow ramp hot spot = 0.5*dT_out (not a fixed 6.3 K) and recalibrated footprint at k = 0.49.
Run: python3 final_thermal.py > final_thermal.out"""
import sys, math
import numpy as np
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../ctl')))
from harness import ev, TIMS, cm
PG = cm.Fluid('PG25 k0.49', 1005.0, 3930.0, 1.25e-3, 0.49)
WATER = cm.WATER50
B = {  # builds
    "PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)": dict(L=7.7, base=0.8),
    "PKG-A fallback base 1.0": dict(L=7.7, base=1.0),
    "PKG-B R+ (0.12/0.12x1.8, L6, base 0.8)": dict(t=0.12, gap=0.12, H=1.8, L=6.0, base=0.8),
    "P-grade (0.10/0.10x1.5, L5, base 0.8)": dict(t=0.10, gap=0.10, H=1.5, L=5.0, base=0.8),
    "P-grade L6": dict(t=0.10, gap=0.10, H=1.5, L=6.0, base=0.8),
    "Draft core corrected (L6, base 1.0)": dict(L=6.0, base=1.0),
}
def E(A=117.0, Q=15000.0, lpm=18.0, tim="paste", **kw):
    return ev(A=A, Q=Q, lpm=lpm, tim=tim, fluid=PG, **kw)
def qcap(kw, tim, A=117.0, Tmax=40.0):
    lo, hi = 5e3, 45e3
    for _ in range(22):
        mid = 0.5 * (lo + hi); e = E(A=A, Q=mid, lpm=1.2 * mid / 1000, tim=tim, **kw)
        lo, hi = (mid, hi) if e["max"] < Tmax else (lo, mid)
    return lo / 1e3
print("## 1. Benchmark point (15 kW, 18 LPM PG25 k0.49, 45 C), absolute, own 2-D penalty")
print("| build | A cm2 | TIM | cal | TIM K | base | conv | pen | avg | max | max-avg | vs 34.4/44.2 | T_in allowed C |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
rows = [("PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)", A, t) for A in (117.0, 100.0) for t in ("paste", "PCM25", "PCMpkg", "LM")]
rows += [("PKG-A fallback base 1.0", 117.0, t) for t in ("paste", "PCM25")]
rows += [("PKG-B R+ (0.12/0.12x1.8, L6, base 0.8)", A, t) for A in (117.0, 100.0) for t in ("paste", "PCM25", "LM")]
rows += [("P-grade (0.10/0.10x1.5, L5, base 0.8)", 117.0, t) for t in ("paste", "PCM25", "LM")]
rows += [("P-grade L6", 117.0, t) for t in ("paste", "PCM25")]
rows += [("Draft core corrected (L6, base 1.0)", 117.0, t) for t in ("paste", "PCM25", "LM")]
R = {}
for lab, A, tim in rows:
    e = E(A=A, tim=tim, **B[lab]); R[(lab, A, tim)] = e
    tin = min(85 - e["max"], 65 - e["dTout"])
    print(f"| {lab} | {A:.0f} | {tim} | {e['cal']:.2f} | {e['tim']:.2f} | {e['base']:.2f} | {e['conv']:.2f} | {e['pen']:+.2f} | **{e['avg']:.2f}** | **{e['max']:.2f}** | {e['max']-e['avg']:.1f} | {(e['avg']/34.4-1)*100:+.1f} % / {(e['max']/44.2-1)*100:+.1f} % | {tin:.1f} |", flush=True)
print("\nCoolIT re-tested on PCM (measured minus TIM delta 9.0->7.1 K and scatter 3.5->1.5 K): 32.5 / 40.3 K; T_in allowed 44.7 C")
print("R'' (avg/q): PKG-A paste %.3f, PCM %.3f, LM %.3f cm2K/W; CoolIT measured 34.4/128.2 = %.3f (at 117 cm2)" % (
    R[("PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)",117.0,"paste")]["avg"]/128.2, R[("PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)",117.0,"PCM25")]["avg"]/128.2,
    R[("PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)",117.0,"LM")]["avg"]/128.2, 34.4/128.2))

print("\n## 2. Monte Carlo (draft distributions; own penalty N(pen, 0.01 core); optional model-form error lognormal sigma 0.08 on the core)")
print("| build | A | TIM | avg P10/P50/P90 | max P10/P50/P90 | P(avg<34.4) | P(max<44.2) | with model-form: P(avg<34.4) / P(max<44.2) | P(avg<=31 & max<=36) PCM |")
print("|---|---|---|---|---|---|---|---|---|")
rng = np.random.default_rng(2026); n = 40000
for lab, A, tim in [(l, a, t) for (l, a, t) in R if t in ("paste", "PCM25", "LM") and not l.startswith("P-grade L6")]:
    e = R[(lab, A, tim)]; Rt, sc = TIMS[tim]; Rhi = {"paste": 0.10, "PCM25": 0.075, "LM": 0.025}[tim]
    s_t = math.log(Rhi / Rt) / 1.2816
    out = []
    for mf in (0.0, 0.08):
        hf = np.exp(rng.normal(0, 0.125, n)); tf = np.exp(rng.normal(0, s_t, n)); bf = np.exp(rng.normal(0, 0.05, n))
        cf = np.exp(rng.normal(0, 0.025, n)); fh = np.exp(rng.normal(0, 0.2, n)); ts = np.exp(rng.normal(0, 0.2, n)); rp = np.exp(rng.normal(0, 0.3, n))
        core1 = e["cal"] * cf + e["conv"] / hf + e["base"] * bf
        pen = rng.normal(e["pen"], 0.01 * e["core1d"], n)
        core = (core1 + pen) * np.exp(rng.normal(0, mf, n)) if mf else core1 + pen
        avg = core + e["tim"] * tf
        mx = avg + 1.5 * fh + sc * e["q"] / 128 * ts + e["pkpk"] / 2 * rp
        out.append((avg, mx))
    (avg, mx), (avg2, mx2) = out
    pc = lambda x: "/".join(f"{np.percentile(x,p):.1f}" for p in (10, 50, 90))
    dec = f"{np.mean((avg<=31)&(mx<=36)):.2f} / {np.mean((avg2<=31)&(mx2<=36)):.2f}" if tim == "PCM25" else "-"
    print(f"| {lab} | {A:.0f} | {tim} | {pc(avg)} | {pc(mx)} | {np.mean(avg<34.4):.2f} | {np.mean(mx<44.2):.2f} | {np.mean(avg2<34.4):.2f} / {np.mean(mx2<44.2):.2f} | {dec} |", flush=True)

print("\n## 3. Q capacity at Tcase,max <= 85 C (45 C inlet, 1.2 LPM/kW), thermal limit vs velocity-rated limit")
METER_U18 = 1.54  # m/s at 18 LPM, PKG-A meter (ctl/pkgA_dp_stress)
q_meter = 2.0 / METER_U18 * 18 / 1.2; q_port = 1.5 * (math.pi / 4 * 0.02**2) * 60000 / 1.2
print(f"velocity caps: meter 2.0 m/s -> {q_meter:.1f} kW; 20 mm port 1.5 m/s -> {q_port:.1f} kW; TTV-A heater limit 18 kW; single UQD08 pair practical 18 LPM -> 15 kW")
for lab, tim in (("PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)", "paste"), ("PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)", "PCM25"),
                 ("PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)", "PCMpkg"), ("PKG-A R (0.15/0.15x2.0, L7.7, base 0.8)", "LM"),
                 ("PKG-B R+ (0.12/0.12x1.8, L6, base 0.8)", "paste"), ("PKG-B R+ (0.12/0.12x1.8, L6, base 0.8)", "PCM25"),
                 ("P-grade (0.10/0.10x1.5, L5, base 0.8)", "PCM25"), ("P-grade (0.10/0.10x1.5, L5, base 0.8)", "LM")):
    qc = qcap(B[lab], tim)
    print(f"- {lab}, {tim}: thermal {qc:.1f} kW; rated (velocity-capped) {min(qc, q_meter):.1f} kW", flush=True)
cl = cm.coolit_like(117.0)
print("CoolIT measured-basis capacity (draft, flux-scaled terms): ~12.9 kW paste / ~14.8 kW re-tested on PCM")

print("\n## 4. OCP sweep 25-150 % of rated (rated = 1.0 LPM/kW = 15 LPM), 15 kW, 45 C inlet; CoolIT-like patched (ramp 0.5 dT_out, k 0.49)")
def coolit(A, tim="paste 0.07"):
    p = cm.coolit_like(A); p.tim = tim; p.hotspot_flow_K = 0.0; return p
lo, hi = 60.0, 300.0
for _ in range(60):
    mid = 0.5 * (lo + hi)
    if coolit(mid).evaluate(15000, 1.2, fluid=PG)["dT_avg"] > 34.4: lo = mid
    else: hi = mid
Acal = 0.5 * (lo + hi)
print(f"CoolIT-like recalibrated footprint at k 0.49: {Acal:.1f} cm2 (draft 117 at k 0.52)")
def dp_pkgA(lpm, out_orif=0.5):
    s = lpm / 18.0; up = 18 / 60000 / (math.pi / 4 * 0.02**2); rho = 1005.0
    inert = 3.5 * 0.5 * rho * up**2 / 1e3 + (1.5 * 0.5 * rho * 0.93**2 + 1.5 * 0.5 * rho * 0.67**2) / 1e3 + 0.46 + 0.21 + 2.30 + 0.06 + out_orif
    visc = 0.30 + 0.08 + 0.02 + E(L=7.7, base=0.8)["dp_ch"]
    return inert * s * s + visc * s
print("| LPM | LPM/kW | % rated | outlet C @15 kW | P for 65 C outlet kW | PKG-A paste avg/max | PKG-A PCM avg/max | PKG-A R K/kW (paste) | CoolIT-like paste avg/max | CoolIT-like PCM avg/max | PKG-A dP kPa (w/ outlet row) | CoolIT-like dP kPa |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for lpm in (3.75, 7.5, 11.25, 15.0, 18.0, 22.5, 36.0):
    kw = lpm / 15.0
    a = E(lpm=lpm, tim="paste", L=7.7, base=0.8); b = E(lpm=lpm, tim="PCM25", L=7.7, base=0.8)
    c = coolit(Acal).evaluate(15000, kw, fluid=PG); d = coolit(Acal, "PCM pad").evaluate(15000, kw, fluid=PG)
    cmax = c["dT_avg"] + 0.5 * c["dT_out"] + 3.5 * c["q_W_cm2"] / 128; dmax = d["dT_avg"] + 0.5 * d["dT_out"] + 1.5 * d["q_W_cm2"] / 128
    pmax65 = 15.0 * 20.0 / a["dTout"]
    flag = " (!)" if 45 + a["dTout"] > 65 else ""
    print(f"| {lpm:.2f} | {kw:.2f} | {lpm/15*100:.0f} | {45+a['dTout']:.1f}{flag} | {min(pmax65,99):.1f} | {a['avg']:.1f} / {a['max']:.1f} | {b['avg']:.1f} / {b['max']:.1f} | {a['avg']/15:.2f} | {c['dT_avg']:.1f} / {cmax:.1f} | {d['dT_avg']:.1f} / {dmax:.1f} | {dp_pkgA(lpm):.1f} | {c['dp_total_kPa']:.1f} |", flush=True)

print("\n## 5. CoolIT 4 kW point (4 kW, 6.06 LPM, 50x50 mm plate), max-case R C/W, k 0.49; CoolIT < 0.009 (TIM, heater area undisclosed)")
for lab, kw in (("PKG-A core L7.7 b0.8 (drop-in)", dict(L=7.7, base=0.8)), ("PRISM-S4 R+ L5 b0.8", dict(t=0.12, gap=0.12, H=1.8, L=5.0, base=0.8)),
                ("PRISM-S4 P L5 b0.8", dict(t=0.10, gap=0.10, H=1.5, L=5.0, base=0.8))):
    for A in (25.0, 20.0):
        s = []
        for tim in ("paste", "PCM25", "LM"):
            e = E(A=A, Q=4000.0, lpm=6.06, tim=tim, **kw); s.append(f"{tim} {e['max']/4000:.4f}")
        print(f"- {lab}, {A:.0f} cm2: " + "; ".join(s), flush=True)
c4 = cm.coolit_like(25.0); c4.hotspot_flow_K = 0.0
r4 = c4.evaluate(4000, 1.515, fluid=PG); print(f"- CoolIT-like reconstruction at 25 cm2, paste: {(r4['dT_avg']+0.5*r4['dT_out']+3.5*r4['q_W_cm2']/128)/4000:.4f} C/W (vs measured < 0.009)")

print("\n## 6. Higher-power cases (own penalty, k 0.49); flows beyond the standard meter cap need the -HF meter and dual UQD08")
for lab, A, Q, lpm, kw in (("25 kW on 117 cm2, PKG-A", 117.0, 25000.0, 30.0, dict(L=7.7, base=0.8)),
                           ("30 kW on 150 cm2, PKG-A", 150.0, 30000.0, 36.0, dict(L=7.7, base=0.8)),
                           ("25 kW on 117 cm2, P-grade L5", 117.0, 25000.0, 30.0, dict(t=0.10, gap=0.10, H=1.5, L=5.0, base=0.8)),
                           ("20 kW wafer-scale 460 cm2, PKG-A core L7.7", 460.0, 20000.0, 24.0, dict(L=7.7, base=0.8))):
    s = []
    for tim in ("PCM25", "LM"):
        e = E(A=A, Q=Q, lpm=lpm, tim=tim, **kw); s.append(f"{tim} {e['avg']:.1f}/{e['max']:.1f} K (Tcase,max {45+e['max']:.0f} C)")
    print(f"- {lab} at {lpm:.0f} LPM: " + "; ".join(s), flush=True)
