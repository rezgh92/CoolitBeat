"""Audit: CoolIT-like plate with LM TIM, two ways: (1) the doc's subtraction rule used for 'CoolIT re-tested on PCM';
(2) the patched CoolIT-like reconstruction used in final_thermal.py section 4. Also exact PCM avg for rounding."""
import sys
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../ctl')))
from harness import ev, TIMS, cm
PG = cm.Fluid('PG25 k0.49', 1005.0, 3930.0, 1.25e-3, 0.49)
q = 15000/117.0
tim = {k: q*v[0] for k, v in TIMS.items()}
sc = {k: v[1] for k, v in TIMS.items()}
for t in ("PCM25", "LM"):
    a = 34.4 - (tim["paste"] - tim[t]); m = 44.2 - (tim["paste"] - tim[t]) - (sc["paste"] - sc[t])
    print(f"rule: CoolIT re-tested on {t}: {a:.2f} / {m:.2f}")
def coolit(A, t="paste 0.07"):
    p = cm.coolit_like(A); p.tim = t; p.hotspot_flow_K = 0.0; return p
lo, hi = 60.0, 300.0
for _ in range(60):
    mid = 0.5*(lo+hi)
    if coolit(mid).evaluate(15000, 1.2, fluid=PG)["dT_avg"] > 34.4: lo = mid
    else: hi = mid
A = 0.5*(lo+hi)
print("cm.TIM keys:", list(cm.TIM.keys()))
for t, s in (("paste 0.07", 3.5), ("PCM pad", 1.5), ("LM", 0.6)):
    try:
        c = coolit(A, t).evaluate(15000, 1.2, fluid=PG)
        print(f"model CoolIT-like {t}: avg {c['dT_avg']:.2f} max {c['dT_avg']+0.5*c['dT_out']+s*c['q_W_cm2']/128:.2f}")
    except Exception as e:
        print(t, "err", e)
e = ev(A=117.0, tim="PCM25", L=7.7, base=0.8, fluid=PG)
print(f"Rev A PCM25 exact avg {e['avg']:.4f} max {e['max']:.4f}")
