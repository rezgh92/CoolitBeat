"""Thermal cost of a stricter Split-Flow design-around: inlet window no wider than the kerf
(segment fed only through its end face), using the draft's own cell2d model (h at 18 LPM from draft 3.1 = 13.3 kW/m2K).
Also a 'one-way' (no-split) variant cost is estimated as doubling the per-cell flow length at fixed slot count."""
import sys
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../arch')))
from cell2d import run
K3 = (0.3/0.15)**2/0.5
base = run(hi=0.6, ho=0.6, ki=0.15, ko=0.15, L=6.0, h=13.3e3, d=0.04, Kkerf_mult=K3)
endfed = run(hi=0.15, ho=0.6, ki=0.15, ko=0.15, L=6.0, h=13.3e3, d=0.04, Kkerf_mult=K3)
endfed2 = run(hi=0.16, ho=0.16, ki=0.15, ko=0.15, L=6.0, h=13.3e3, d=0.04, Kkerf_mult=K3)
nokerf = run(hi=0.6, ho=0.6, L=6.0, h=13.3e3, d=0.04)
for lab, r in (("baseline window 1.2 + kerf 0.3", base), ("inlet window = kerf (end-fed)", endfed),
               ("in+out windows = kerf", endfed2), ("no kerf", nokerf)):
    print(f"{lab:32s} 2-D case {r['case']:.2f} K  (delta vs baseline {r['case']-base['case']:+.2f})  pk-pk {r['pkpk']:.2f}")
