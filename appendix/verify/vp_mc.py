"""Corrected benchmark budgets + Monte Carlo. 1-D terms from the project scoping model (verified analytically);
2-D term = PRISM's OWN absolute z-unmixed penalty from vp_cell (not net of CoolIT's), since CoolIT is represented
by its measurement (34.4 / 44.2) or by a footprint drawn independently of the model calibration."""
import sys, math, numpy as np
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model'))); sys.path.insert(0, '../arch')
import coldplate_model as cm
from prism_model import prism, TIMS
PEN = {"R6": lambda q: 0.069 + 0.0245*(q/128.2-1), "P4": lambda q: 0.073 + 0.02*(q/128.2-1), "R4": lambda q: 0.121}
RIP = {"R6": 1.85, "P4": 1.26, "R4": 0.85}
GEO = {"R6": (6.0, "R"), "P4": (4.0, "P"), "R4": (4.0, "R")}
def ev(geo, tim, A=117.0, Q=15000.0, lk=1.2, base=1.0, pen=True, frac_override=None):
    L, gr = GEO[geo]; r = prism(A=A, grade=gr, tim=tim, base=base, L=L).evaluate(Q, lk); q = r['q_W_cm2']
    core = r['dT_cal']+r['dT_conv']+r['dT_base']; f = (frac_override if frac_override is not None else PEN[geo](q)) if pen else 0.0
    avg = r['dT_avg'] + f*core; mx = avg + r['hotspot'] + RIP[geo]*q/128.2
    return dict(avg=avg, max=mx, r=r, core=core, f=f, q=q)
print("## Deterministic, 117 cm2 TTV, full own 2-D penalty (draft value in brackets)")
draft = {("R6","paste"):(30.4,37.2), ("R6","PCM25"):(28.4,33.3), ("R6","PCMpkg"):(30.4,35.2), ("R6","LM"):(23.3,27.3), ("P4","paste"):(27.4,33.6), ("P4","PCM25"):(25.4,29.7), ("P4","LM"):(20.3,23.6)}
for (g,t),(da,dm) in draft.items():
    e = ev(g,t); qc = None
    lo, hi = 3e3, 80e3
    for _ in range(60):
        mid = 0.5*(lo+hi); ee = ev(g,t,Q=mid); lo, hi = (mid,hi) if ee['max'] < 40 else (lo,mid)
    print(f"{g} {t}: avg {e['avg']:.1f} [{da}] max {e['max']:.1f} [{dm}] (2-D +{e['f']*e['core']:.2f} K); Qcap {lo/1e3:.1f} kW; inlet for 85 C case {min(85-e['max'], 65-e['r']['dT_out']):.1f} C")
print("\n## Footprint sensitivity, full penalty")
for A in (100.0, 120.0, 145.0):
    s = [f"{g} {t} {ev(g,t,A=A)['avg']:.1f}/{ev(g,t,A=A)['max']:.1f}" for g,t in (("R6","paste"),("R6","PCM25"),("P4","paste"))]
    print(f"A {A:.0f}: " + "; ".join(s) + f" | CoolIT-PCM est {34.4-0.015*15000/A:.1f}")
print("\n## 2-D-consistent recalibration of the CoolIT reconstruction footprint (its penalty 5.5 % end-face / 6.9 % top-window)")
for fc in (0.055, 0.069):
    lo, hi = 80.0, 200.0
    for _ in range(60):
        mid = 0.5*(lo+hi); c = cm.coolit_like(mid).evaluate(15000, 1.2)
        v = c['dT_avg'] + fc*(c['dT_cal']+c['dT_conv']+c['dT_base'])
        lo, hi = (mid, hi) if v > 34.4 else (lo, mid)
    A2 = lo; e = ev("R6","paste",A=A2); e2 = ev("R6","PCM25",A=A2)
    print(f"CoolIT pen {fc*100:.1f} %: footprint {A2:.0f} cm2 -> PRISM-15 at that footprint, full penalty: paste {e['avg']:.1f}/{e['max']:.1f}, PCM {e2['avg']:.1f}/{e2['max']:.1f}")
print("\n## CoolIT 4 kW point (6.06 LPM), max-case R incl TIM; CoolIT < 0.009 C/W")
for A in (25.0, 20.0):
    for g,t in (("R6","PCM25"),("R4","PCM25"),("R6","paste"),("P4","PCM25"),("R6","LM")):
        e0 = ev(g,t,A=A,Q=4000,lk=1.515,pen=False); e = ev(g,t,A=A,Q=4000,lk=1.515)
        # draft's own differential value for comparison
        dd = {"R6":0.0,"R4":0.052,"P4":0.004}[g]; ed = ev(g,t,A=A,Q=4000,lk=1.515,frac_override=dd)
        print(f"A {A:.0f} {g} {t}: draft-method {ed['max']/4000:.4f}; full penalty {e['max']/4000:.4f} C/W")
print("\n## Monte Carlo 20k (draft's input distributions; 2-D term = own penalty N(f,0.01))")
rng = np.random.default_rng(11); n = 20000
def mc(g, t, frac_mode="full"):
    L, gr = GEO[g]; Rt, Rhi, sc = TIMS[t]; s_t = min(0.45, math.log(Rhi/Rt)/1.2816)
    hf = np.exp(rng.normal(0,.125,n)); tf = np.exp(rng.normal(0,s_t,n)); bf = np.exp(rng.normal(0,.05,n)); cf = np.exp(rng.normal(0,.025,n))
    fh = np.exp(rng.normal(0,.2,n)); ts = np.exp(rng.normal(0,.2,n)); rp = np.exp(rng.normal(0,.3,n))
    out = {}
    for basis in ("pub","fair"):
        A = np.full(n,117.0) if basis=="pub" else rng.triangular(100,120,145,n)
        r = prism(A=117.0, grade=gr, tim=t, L=L).evaluate(15000,1.2); k = 117.0/A; q = 128.2*k
        NTU = r['NTU']*hf*(A/117.0); cal = r['dT_out']*(1/(1-np.exp(-NTU))-1/NTU)*cf
        conv = r['dT_conv']/hf*k; base = r['dT_base']*bf*k; tim = r['dT_tim']*tf*k
        f = np.array([PEN[g](qq) for qq in q]) + rng.normal(0,0.01,n)
        avg = (cal+conv+base)*(1+f) + tim
        mx = avg + 1.5*fh + sc*ts*k + RIP[g]*rp*k
        out[basis] = (avg, mx, A)
    return out
for g,t in (("R6","paste"),("R6","PCM25"),("R6","PCMpkg"),("R6","LM"),("P4","paste"),("P4","PCM25")):
    o = mc(g,t); (a,m,_),(af,mf,Af) = o["pub"], o["fair"]
    pc = lambda x: f"{np.percentile(x,10):.1f}/{np.percentile(x,50):.1f}/{np.percentile(x,90):.1f}"
    Rt = TIMS[t][0]
    if t.startswith("paste"): ca, cm_ = 34.4, 44.2
    else:
        Rp = rng.uniform(0.05,0.07,n); qC = 15000/Af; ca = 34.4-(Rp-Rt)*qC; cm_ = 44.2-(Rp-Rt)*qC-(2.0 if t.startswith("PCM") else 2.9)*qC/128
    print(f"{g} {t}: avg {pc(a)} max {pc(m)} | P(avg<34.4) pub {np.mean(a<34.4):.2f} fair {np.mean(af<34.4):.2f} | P(max<44.2) {np.mean(m<44.2):.2f}/{np.mean(mf<44.2):.2f} | same-TIM fair {np.mean(af<ca):.2f}/{np.mean(mf<cm_):.2f} | P(avg<34.4 | A<110) {np.mean(af[Af<110]<34.4):.2f}")
