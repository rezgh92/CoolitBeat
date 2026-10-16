import time
from vp_cell import solve, oneD
q=1.282e6; dT=12.66
for lab, kw in (("CoolIT 0.2/0.2x4, tb2, h10.2k, end-face outlet", dict(t=0.2, g=0.2, H=4.0, tb=2.0, h=10.2e3)),
                ("CoolIT 0.2/0.2x4, tb2, h10.2k, z-mixed", dict(t=0.2, g=0.2, H=4.0, tb=2.0, h=10.2e3, zmix=True)),
                ("CoolIT-alt 0.15/0.15x3, tb2", dict(t=0.15, g=0.15, H=3.0, tb=2.0, h=12.5e3)),
                ("CoolIT-alt 0.2/0.2x3, tb1.5", dict(t=0.2, g=0.2, H=3.0, tb=1.5, h=10.6e3)),
                ("CoolIT-alt 0.1/0.2x4, tb2", dict(t=0.1, g=0.2, H=4.0, tb=2.0, h=10.2e3)),):
    o = oneD(q=q, dTout=dT, h=kw['h'], t=kw['t'], g=kw['g'], H=kw['H'], tb=kw['tb'], linear=True)
    t0=time.time()
    r = solve(L=54.0, dx=0.1, dz=0.1, q=q, dTout=dT, win_in=2.5, win_out=0.0, kerf_in=0.0, kerf_out=0.0, end_outlet=True, **kw)
    print(f"{lab}: 2-D {r['case']:.2f} vs 1-D linear {o['core']:.2f} -> pen {r['case']-o['core']:+.2f} ({(r['case']/o['core']-1)*100:+.1f} %), eta {o['eta']:.2f}, pkpk {r['pkpk']:.1f}, eclose {r['eclose']:.4f} [{time.time()-t0:.0f}s]", flush=True)
