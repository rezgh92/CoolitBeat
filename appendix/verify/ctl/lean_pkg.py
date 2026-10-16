"""Scorecard of the gap-closing packages, own 2-D penalty throughout (verify-physics method), vs CoolIT measured.
PKG-0 = PRISM-15 as drafted (R 0.15/0.15x2.0, L6, base 1.0). PKG-A = drop-in lean (R core, base 0.8, L 7.7).
PKG-B = R+ grade (0.12/0.12x1.8, L6, base 0.8; tray filter <= 40 um abs)."""
import numpy as np, math
from harness import ev, TIMS
PK = {"PKG-0 draft R6 b1.0": dict(), "PKG-A R L7.7 b0.8": dict(L=7.7, base=0.8),
      "PKG-B R+ g0.12 L6 b0.8": dict(t=0.12, gap=0.12, H=1.8, base=0.8)}
def qcap(kw, tim, A=117.0, Tmax=40.0):
    lo, hi = 5e3, 40e3
    for _ in range(22):
        mid = 0.5 * (lo + hi); e = ev(A=A, Q=mid, lpm=1.2 * mid / 1000, tim=tim, **kw)
        lo, hi = (mid, hi) if e["max"] < Tmax else (lo, mid)
    return lo / 1e3
print("| package | A | TIM | avg | max | max-avg | vs CoolIT avg / max | Qcap kW (85 C case, 1.2 LPM/kW) | T_in allowed C |")
print("|---|---|---|---|---|---|---|---|---|")
for lab, kw in PK.items():
    for A in (117.0, 100.0):
        for tim in ("paste", "PCM25"):
            e = ev(A=A, tim=tim, **kw)
            qc = qcap(kw, tim, A) if A == 117.0 else float('nan')
            tin = min(85 - e["max"], 65 - e["dTout"])
            print(f"| {lab} | {A:.0f} | {tim} | {e['avg']:.2f} | {e['max']:.2f} | {e['max']-e['avg']:.1f} | {(e['avg']/34.4-1)*100:+.1f} % / {(e['max']/44.2-1)*100:+.1f} % | {qc:.1f} | {tin:.1f} |", flush=True)
# Monte Carlo (draft's distributions, own penalty N(pen, 0.01 core))
rng = np.random.default_rng(11); n = 20000
print("\n| package | A | TIM | avg P10/P50/P90 | max P10/P50/P90 | P(avg<34.4) | P(max<44.2) |")
print("|---|---|---|---|---|---|---|")
for lab, kw in PK.items():
    for A in (117.0, 100.0):
        for tim in ("paste", "PCM25"):
            e = ev(A=A, tim=tim, **kw)
            R, sc = TIMS[tim]; Rhi = {"paste": 0.10, "PCM25": 0.075}[tim]
            s_t = math.log(Rhi / R) / 1.2816
            hf = np.exp(rng.normal(0, 0.125, n)); tf = np.exp(rng.normal(0, s_t, n)); bf = np.exp(rng.normal(0, 0.05, n))
            cf = np.exp(rng.normal(0, 0.025, n)); fh = np.exp(rng.normal(0, 0.2, n)); ts = np.exp(rng.normal(0, 0.2, n)); rp = np.exp(rng.normal(0, 0.3, n))
            core1 = e["cal"] * cf + e["conv"] / hf + e["base"] * bf
            pen = rng.normal(e["pen"], 0.01 * e["core1d"], n)
            avg = core1 + pen + e["tim"] * tf
            mx = avg + 1.5 * fh + sc * e["q"] / 128 * ts + e["pkpk"] / 2 * rp
            pc = lambda x: "/".join(f"{np.percentile(x,p):.1f}" for p in (10, 50, 90))
            print(f"| {lab} | {A:.0f} | {tim} | {pc(avg)} | {pc(mx)} | {np.mean(avg<34.4):.2f} | {np.mean(mx<44.2):.2f} |", flush=True)
