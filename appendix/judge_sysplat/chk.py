import sys, math
from dataclasses import replace
sys.path.insert(0, "/home/user/Rez/docs/cooling/model")
from coldplate_model import ColdPlate, hmmc, coolit_like, TIM, PG25
print("PG25", PG25)
def lc(A, tim, core="R"):
    return replace(hmmc(A, core=core, tim=tim), port_bore_mm=16*math.sqrt(2))
# footprint sensitivity at 15 kW 1.2 LPM/kW
for A in (100, 117, 120, 145):
    c = coolit_like(A).evaluate(15000, 1.2)
    for tim in ("paste 0.07","PCM pad","liquid metal"):
        r = lc(A, tim).evaluate(15000, 1.2)
        print(f"A={A} {tim:12s} avg {r['dT_avg']:.1f} max {r['dT_max']:.1f} | CoolIT-like avg {c['dT_avg']:.1f} max {c['dT_max']:.1f}")
# 4 kW point
for A in (20, 25):
    for tim in ("paste 0.07","paste thin-BLT","PCM pad","liquid metal"):
        p = hmmc(A, core="R", tim=tim)
        flow = 6.0
        p = replace(p, port_bore_mm=8.0*math.sqrt(2), orifice_dp_kPa_18=2.0*(18.0/flow)**2, header_u_m_s=1.0*18.0/flow)
        r = p.evaluate(4000, 1.5)
        print(f"4kW A={A} {tim:14s} avg {r['dT_avg']:.1f} max {r['dT_max']:.1f} R''max {r['dT_max']*A/4000:.3f} dP {r['dp_total_kPa']:.1f}")
    c = coolit_like(A).evaluate(4000,1.5); print(f"  coolit-like A={A}: avg {c['dT_avg']:.1f} max {c['dT_max']:.1f}  (measured <36 K max)")
