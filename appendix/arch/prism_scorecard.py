import sys, math, numpy as np
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
import coldplate_model as cm
from prism_model import prism, TIMS
RHO, CP = 1005.0, 3930.0
# geometry-dependent 2-D differential (fraction of cal+conv+base) and ripple crest (K at 128 W/cm2) from cell2d runs
G = {"R4": (4.0, "R", 0.052, 0.85), "R5": (5.0, "R", 0.0215, 1.35), "R6": (6.0, "R", 0.000, 1.85),
     "R8": (8.0, "R", -0.028, 2.74), "P4": (4.0, "P", 0.004, 1.23)}
out = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s); out.append(s)

def ev(geo, tim, A=117.0, Q=15000.0, lk=1.2, base=1.0, hs=1.5, Tin=45.0, H=None):
    L, gr, c2d, rip = G[geo]
    p = prism(A=A, grade=gr, tim=tim, base=base, L=L, hs=hs, H=H)
    r = p.evaluate(Q, lk); q = r["q_W_cm2"]
    core = r["dT_cal"] + r["dT_conv"] + r["dT_base"]
    avg = r["dT_avg"] + c2d * core
    mx = avg + r["hotspot"] + rip * q / 128
    return dict(r=r, avg=avg, max=mx, q=q, dTout=r["dT_out"], core=core * (1 + c2d), Rpp=avg / q)

def qcap(geo, tim, base=1.0, A=117.0):
    lo, hi = 3e3, 80e3
    for _ in range(60):
        mid = 0.5 * (lo + hi); e = ev(geo, tim, A=A, Q=mid, base=base)
        lo, hi = (mid, hi) if e["max"] < 40 else (lo, mid)
    return lo / 1000

P("## 1. Benchmark point 15 kW, 18 LPM PG25, 45 C, 117 cm2 -- PRISM-15 (R6 = 12 mm slot pitch)")
P("| case | cal | TIM | base | conv | corr | avg | max | max-avg | R'' | Tcase,max | Qcap (1.2 LPM/kW) | T_in max (85 C case / 65 C return) |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
cases = [("R6 paste 0.07 like-for-like", "R6", "paste", 1.0), ("R6 PCM 25 psi (TTV headline)", "R6", "PCM25", 1.0),
         ("R6 PCM real-package retention 0.07", "R6", "PCMpkg", 1.0), ("R6 LM Tier 2", "R6", "LM", 1.0),
         ("R6 PCM base 0.8 (stretch)", "R6", "PCM25", 0.8), ("R4 paste (PSM-like pitch, kerfed)", "R4", "paste", 1.0),
         ("P4 paste (filtration-gated)", "P4", "paste", 1.0), ("P4 PCM", "P4", "PCM25", 1.0), ("P4 LM", "P4", "LM", 1.0),
         ("R6 D2D LM base 0.8", "R6", "D2D", 0.8)]
R = {}
for lab, geo, tim, base in cases:
    e = ev(geo, tim, base=base); r = e["r"]; qc = qcap(geo, tim, base)
    tin = min(85 - e["max"], 65 - e["dTout"]); R[lab] = e
    P(f"| {lab} | {r['dT_cal']:.1f} | {r['dT_tim']:.1f} | {r['dT_base']:.1f} | {r['dT_conv']:.1f} | {e['core']-r['dT_cal']-r['dT_conv']-r['dT_base']:+.1f} | **{e['avg']:.1f}** | **{e['max']:.1f}** | {e['max']-e['avg']:.1f} | {e['Rpp']:.3f} | {45+e['max']:.1f} | {qc:.1f} | {tin:.1f} ({85-e['max']:.1f} / {65-e['dTout']:.1f}) |")
P("CoolIT measured: 34.4 / 44.2, max-avg 9.8, R'' 0.269 (117 cm2 basis), Tcase,max 89.2, Qcap ~12.9 kW, T_in max 40.8 C")
cP = (34.4 - 0.015 * 128.2, 44.2 - 0.015 * 128.2 - 2.0)
P(f"CoolIT re-tested on PCM (estimate): {cP[0]:.1f} / {cP[1]:.1f}")
P("")
P("## 2. Footprint sensitivity (same 15 kW): our plate tested at CoolIT's possible footprint")
for A in (100.0, 117.0, 120.0, 145.0):
    s = []
    for lab, geo, tim in (("R6 paste", "R6", "paste"), ("R6 PCM", "R6", "PCM25"), ("R6 LM", "R6", "LM"), ("P4 paste", "P4", "paste")):
        e = ev(geo, tim, A=A); s.append(f"{lab} {e['avg']:.1f}/{e['max']:.1f}")
    qa = 15000 / A
    P(f"A {A:.0f} cm2 ({qa:.0f} W/cm2): " + "; ".join(s) + f" | CoolIT 34.4/44.2, CoolIT-PCM {34.4-0.015*qa:.1f}/{44.2-0.015*qa-2*qa/128:.1f}")
P("")
P("## 3. Monte Carlo (20k): as-published comparison at our 117 cm2 TTV, and footprint-fair at CoolIT's A ~ tri(100,120,145)")
rng = np.random.default_rng(7); n = 20000
def mc(geo, tim, base=1.0):
    L, gr, c2d0, rip0 = G[geo]
    nom = ev(geo, tim, base=base); r = nom["r"]
    Rt, Rhi, sc = TIMS[tim]
    s_t = min(0.45, math.log(Rhi / Rt) / 1.2816)
    hf = np.exp(rng.normal(0, 0.125, n)); tf = np.exp(rng.normal(0, s_t, n)); bf = np.exp(rng.normal(0, 0.05, n))
    cf = np.exp(rng.normal(0, 0.025, n)); fh = np.exp(rng.normal(0, 0.2, n)); ts = np.exp(rng.normal(0, 0.2, n))
    rp = np.exp(rng.normal(0, 0.3, n)); c2d = np.clip(rng.normal(c2d0 + 0.005, 0.02, n), c2d0 - 0.03, c2d0 + 0.06)
    AC = rng.triangular(100, 120, 145, n)
    res = {}
    for basis, A in (("pub", np.full(n, 117.0)), ("fair", AC)):
        k = 117.0 / A                                   # flux ratio
        NTU = r["NTU"] * hf * (A / 117.0)
        cal = r["dT_out"] * (1 / (1 - np.exp(-NTU)) - 1 / NTU) * cf
        conv = r["dT_conv"] / hf * k; base_ = r["dT_base"] * bf * k; tim_ = r["dT_tim"] * tf * k
        core = cal + conv + base_
        avg = core * (1 + c2d) + tim_
        mx = avg + 1.5 * fh + sc * ts * k + rip0 * rp * k
        res[basis] = (avg, mx)
    # CoolIT with same TIM: CoolIT's paste actual R'' ~ U(0.05,0.07); PCM-equivalent gain = (Rp - Rt)*q_C
    qC = 15000 / AC; Rp = rng.uniform(0.05, 0.07, n)
    return res, qC, Rp
P("| case | avg P10/P50/P90 | max P10/P50/P90 | P(avg<34.4) pub / fair | P(max<44.2) pub / fair | P(beat same-TIM CoolIT: avg / max), fair |")
P("|---|---|---|---|---|---|")
for lab, geo, tim in (("R6 paste", "R6", "paste"), ("R6 PCM 25 psi", "R6", "PCM25"), ("R6 PCM pkg 0.07", "R6", "PCMpkg"), ("R6 LM", "R6", "LM"), ("P4 paste", "P4", "paste"), ("P4 PCM", "P4", "PCM25")):
    res, qC, Rp = mc(geo, tim)
    (a, m), (af, mf) = res["pub"], res["fair"]
    Rt = TIMS[tim][0]
    # same-TIM CoolIT: if our TIM is paste -> CoolIT as measured; if PCM -> CoolIT minus (Rp-0.055) qC and scatter 3.5->1.5; if LM -> minus (Rp-0.015) qC, scatter 3.5->0.6
    if tim.startswith("paste"): ca, cmx = 34.4 + 0 * qC, 44.2 + 0 * qC
    elif tim.startswith("PCM"): ca = 34.4 - (Rp - Rt) * qC; cmx = 44.2 - (Rp - Rt) * qC - 2.0 * qC / 128
    else: ca = 34.4 - (Rp - Rt) * qC; cmx = 44.2 - (Rp - Rt) * qC - 2.9 * qC / 128
    pc = lambda x: f"{np.percentile(x,10):.1f}/{np.percentile(x,50):.1f}/{np.percentile(x,90):.1f}"
    P(f"| {lab} | {pc(a)} | {pc(m)} | {np.mean(a<34.4):.2f} / {np.mean(af<34.4):.2f} | {np.mean(m<44.2):.2f} / {np.mean(mf<44.2):.2f} | {np.mean(af<ca):.2f} / {np.mean(mf<cmx):.2f} |")
P("")
P("## 4. CoolIT 4 kW point (25 cm2, 4 kW, 6 LPM = 1.5 LPM/kW); CoolIT spec < 0.009 C/W max-case incl TIM")
for lab, geo, tim, base in (("R4 PCM", "R4", "PCM25", 1.0), ("R4 paste", "R4", "paste", 1.0), ("R4 LM", "R4", "LM", 1.0), ("R4 PCM base 0.8", "R4", "PCM25", 0.8), ("R6 PCM", "R6", "PCM25", 1.0), ("P4 PCM", "P4", "PCM25", 1.0), ("P4 paste", "P4", "paste", 1.0)):
    e = ev(geo, tim, A=25.0, Q=4000.0, lk=1.5, base=base)
    P(f"{lab}: avg {e['avg']:.1f} max {e['max']:.1f} -> {e['max']/4000:.4f} C/W")
c4 = cm.coolit_like(25.0).evaluate(4000, 1.5); P(f"(CoolIT-like reconstruction at 25 cm2: {c4['dT_max']/4000:.4f} C/W -- overpredicts the real <0.009)")
P("")
P("## 5. 25-30 kW and wafer-scale (PCM / LM), 1.2 LPM/kW")
for Qk, A, geo in ((25, 117, "R6"), (30, 150, "R6"), (20, 460, "R8")):
    s = []
    for tim in ("PCM25", "LM"):
        e = ev(geo, tim, A=A, Q=Qk * 1e3); s.append(f"{tim}: {e['avg']:.1f}/{e['max']:.1f} (Tcase,max {45+e['max']:.0f} C)")
    P(f"{Qk} kW on {A} cm2 ({geo}): " + "; ".join(s))
P("")
P("## 6. Real 2027-28 package, 4 dies 26x33 mm at 350 W/cm2 + 16 HBM, zoned, hottest die cell (fit 33 + 3500/h_eff + 350(R-0.05)) + 2-D diff")
for lab, geo, H in (("R die-zone L5, H2.0", "R5", 2.0), ("R die-zone L5, H2.5", "R5", 2.5), ("P die-zone L4", "P4", None)):
    e = ev(geo, "PCM25", A=34.3, Q=12000, lk=1.2, H=H); heff = e["r"]["h_eff"] / 1e3
    diff = {"R5": 1.6, "P4": 0.2}[geo]
    s = [f"{t}: {33 + 3500/heff + 350*(Rt-0.05) + diff:.1f} K ({45+33+3500/heff+350*(Rt-0.05)+diff:.0f} C)" for t, Rt in (("paste 0.05", 0.05), ("PCM 0.055", 0.055), ("LM 0.015", 0.015))]
    P(f"{lab} (h_eff {heff:.0f}): " + "; ".join(s))
P("CoolIT-like split-flow: 88.6 K paste (134 C), ~76 K LM (121 C). Direct-to-die removes lid + TIM1 ~28 K at the junction.")
with open("prism_scorecard.out", "w") as f: f.write("\n".join(out) + "\n")
