import sys
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model'))); sys.path.insert(0, '../arch')
from prism_model import prism
from vp_cell import solve, oneD
p = prism(A=34.3, grade="P", tim="PCM25", L=4.0); r = p.evaluate(12000, 1.2); h = r['h']
o = oneD(q=3.5e6, dTout=12.9, h=h, H=1.5, t=0.10, g=0.10)
s = solve(L=4.0, H=1.5, t=0.10, g=0.10, dx=0.025, q=3.5e6, dTout=12.9, h=h)
print(f"P-grade 350 W/cm2 L4: h {h/1e3:.1f} heff {o['heff']/1e3:.0f} core {o['core']:.2f}; 2-D {s['case']:.2f} pen {s['case']-o['core']:+.2f} ({(s['case']/o['core']-1)*100:+.1f} %)")
o = oneD(q=1.282e6, dTout=12.66, h=h, H=1.5, t=0.10, g=0.10)
s = solve(L=4.0, H=1.5, t=0.10, g=0.10, dx=0.025, q=1.282e6, dTout=12.66, h=h)
print(f"P-grade 128 W/cm2 L4: core {o['core']:.2f}; 2-D {s['case']:.2f} pen {s['case']-o['core']:+.2f} ({(s['case']/o['core']-1)*100:+.1f} %), pk-pk {s['pkpk']:.2f}")
# kerf / window sensitivities at the PRISM-15 point
o = oneD()
for lab, kw in (("baseline K_kerf=w^2/12 (ratio 8)", {}), ("kerf ratio 4", dict(Kkerf_ratio=4)), ("kerf ratio 16", dict(Kkerf_ratio=16)),
                ("kerf floor h 6k", dict(h_floor_kerf=6e3)), ("no kerf (kerf filled)", dict(kerf_in=0.0, kerf_out=0.0)),
                ("inlet kerf filled only", dict(kerf_in=0.0)), ("k_fluid 0.49, h scaled", dict(kf=0.49, h=13.3e3*0.49/0.52))):
    s = solve(L=6.0, dx=0.03, **kw)
    print(f"PRISM-15 L6 {lab}: 2-D {s['case']:.2f} (pen vs 1-D {s['case']-o['core']:+.2f}), pk-pk {s['pkpk']:.2f}", flush=True)
