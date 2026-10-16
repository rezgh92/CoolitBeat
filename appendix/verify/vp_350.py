import sys
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model'))); sys.path.insert(0, '../arch')
from prism_model import prism
from vp_cell import solve, oneD
for H in (2.0, 2.5):
    p = prism(A=34.3, grade="R", tim="PCM25", L=5.0, H=H); r = p.evaluate(12000, 1.2)
    h = r['h']; o = oneD(q=3.5e6, dTout=12.9, h=h, H=H)
    s = solve(L=5.0, H=H, dx=0.025, q=3.5e6, dTout=12.9, h=h)
    print(f"350 W/cm2, L5, H{H}: h {h/1e3:.1f}, 1-D heff {o['heff']/1e3:.0f} core {o['core']:.2f} (cal {o['cal']:.2f} conv {o['conv']:.2f} base {o['base']:.2f}); 2-D {s['case']:.2f} -> pen {s['case']-o['core']:+.2f} ({(s['case']/o['core']-1)*100:+.1f} %), pk-pk {s['pkpk']:.2f}", flush=True)
