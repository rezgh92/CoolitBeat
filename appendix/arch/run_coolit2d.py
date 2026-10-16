import numpy as np
from cell2d import run
# CoolIT-like split-flow half-cell: centre slot (half-width 2.5 mm) at x=0, fin-field end at x=54 (full-height exit modelled as 1 mm open end)
def coolit(d=0.1, slot_half=2.5, kfz=1.0):
    r = run(hi=slot_half, ho=1.0, ki=0.0, ko=1.0, L=54.0, H=4.0, tb=2.0, d=d, q=1.28e6, dTout=12.66, h=10.2e3,
            t=0.2, gap=0.2, h_floor_out=10e3, Kkerf_mult=(1.0/0.2)**2/0.5, kfz_mult=kfz)
    # proper 1-D reference for a long channel (linear ramp): 0.5 dTout + q/heff + q tb/k
    ref = 0.5*12.66 + 1.28e6/r['heff1d'] + 1.28e6*2e-3/390
    return r, ref
for lab, kw in (("CoolIT-like long channel, unmixed", {}), ("CoolIT-like, z-mixed", dict(kfz=1e4))):
    r, ref = coolit(**kw)
    print(f"{lab}: 2-D case avg {r['case']:.2f} K vs 1-D linear-ramp ref {ref:.2f} K -> {r['case']-ref:+.2f} K; pk-pk {r['pkpk']:.2f}; h_eff1d {r['heff1d']/1e3:.0f}")
# realistic kerf permeability for our cell: K ratio = (w/b)^2 / phi
for w in (0.3, 0.5):
    for q, dT, L in ((1.28e6, 12.66, 4.0), (3.5e6, 12.9, 4.0), (3.5e6, 12.9, 5.0)):
        r = run(hi=0.15, ho=max(0.15, w/2), ki=w/2, ko=w/2, L=L, q=q, dTout=dT, Kkerf_mult=(w/0.15)**2/0.5)
        r0 = run(hi=0.15, ho=0.30, L=L, q=q, dTout=dT)
        print(f"kerf {w} mm, q {q/1e4:.0f} W/cm2, L {L}: kerfed {r['case']:.2f} vs no-kerf {r0['case']:.2f} (1-D {r['ref']:.2f})", flush=True)
