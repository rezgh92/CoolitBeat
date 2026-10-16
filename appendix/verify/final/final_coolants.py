"""Coolant sensitivity for Rev A (PKG-A) at 15 kW / 18 LPM, 45 C inlet, paste, plus P90 of (max - avg). Property values are
table approximations at ~50 C film (+/-5-10 %); PG25 uses k 0.49 as in final_thermal.py."""
import sys, math, numpy as np
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../ctl')))
from harness import ev, cm, TIMS
F = {"PG25 (k 0.49)": cm.Fluid('PG25', 1005.0, 3930.0, 1.25e-3, 0.49),
     "PG30": cm.Fluid('PG30', 1020.0, 3850.0, 1.55e-3, 0.46),
     "EG25": cm.Fluid('EG25', 1030.0, 3700.0, 1.10e-3, 0.50),
     "water": cm.WATER50,
     "PG25 at 20 C film (start-up)": cm.Fluid('PG25c', 1020.0, 3880.0, 2.6e-3, 0.46)}
for lab, fl in F.items():
    e = ev(A=117.0, lpm=18.0, tim="paste", fluid=fl, L=7.7, base=0.8)
    print(f"- {lab}: avg {e['avg']:.1f} K, max {e['max']:.1f} K (caloric {e['cal']:.1f}, conv {e['conv']:.1f}, pen {e['pen']:+.2f}); channel dP {e['dp_ch']:.2f} kPa")
e = ev(A=117.0, lpm=18.0, tim="paste", fluid=F["PG25 (k 0.49)"], L=7.7, base=0.8)
rng = np.random.default_rng(7); n = 40000; R, sc = TIMS["paste"]; s_t = math.log(0.10/R)/1.2816
hf = np.exp(rng.normal(0, 0.125, n)); tf = np.exp(rng.normal(0, s_t, n)); bf = np.exp(rng.normal(0, 0.05, n)); cf = np.exp(rng.normal(0, 0.025, n))
fh = np.exp(rng.normal(0, 0.2, n)); ts = np.exp(rng.normal(0, 0.2, n)); rp = np.exp(rng.normal(0, 0.3, n))
spread = 1.5*fh + sc*e["q"]/128*ts + e["pkpk"]/2*rp
print(f"max - avg (paste, 117 cm2): P50 {np.percentile(spread,50):.1f} K, P90 {np.percentile(spread,90):.1f} K; CoolIT measured 9.8 K")
