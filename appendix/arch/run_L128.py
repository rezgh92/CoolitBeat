import sys, math
sys.path.insert(0,__import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
import coldplate_model as cm
from cell2d import run
from prism_model import prism
K3=(0.3/0.15)**2/0.5
for L in (4.0, 5.0, 6.0, 8.0):
    p = prism(L=L, tim="paste"); r = p.evaluate(15000, 1.2)
    r2 = run(hi=0.6, ho=0.6, ki=0.15, ko=0.15, L=L, h=r['h'], d=0.025 if L<=5 else 0.04, Kkerf_mult=K3)
    corr = r2['case'] - 1.069*r2['ref']
    print(f"L={L:.0f}: h {r['h']/1e3:.1f} heff {r['h_eff']/1e3:.0f} NTU {r['NTU']:.2f}; 1-D cal+conv+base {r2['ref']:.2f}; 2-D {r2['case']:.2f} "
          f"(differential vs CoolIT {corr:+.2f}); pk-pk {r2['pkpk']:.2f}; avg paste {r2['case']-0.069*r2['ref']+r['dT_tim']:.2f} "
          f"max paste {r2['case']-0.069*r2['ref']+r['dT_tim']+1.5+3.5+r2['pkpk']/2:.2f}; ch dP {r['dp_ch_kPa']:.2f}", flush=True)
