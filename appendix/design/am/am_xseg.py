#!/usr/bin/env python3
"""X module as built: segmented 2 mm ECAM strips (0.2 mm breaks) on 1 mm Cu-diamond with 30 um Cu skins, P geometry, LM.
Recomputes every X number used in the proposal (TTV, MC, Q cap, real package, GPU-class, >15 kW)."""
import sys
from dataclasses import replace
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
import am_run as A
from coldplate_model import hmmc

BASE = [(0.03, 390.0), (1.0, A.K_CUDIA), (0.03, 390.0)]
def xkw(cp):
    nu = A.ev(replace(cp, flow_len_mm=2.0), k_fin=A.K_ECAM)["Nu"] / A.ev(cp, k_fin=A.K_ECAM)["Nu"]
    return dict(k_fin=A.K_ECAM, base_layers=BASE, nu_mult=nu, area_frac=2 / 2.2, f_mult=1.3)

P = hmmc(117, core="P", tim="liquid metal")
kw = xkw(P)
r = A.ev(P, **kw)
print(f"TTV X segmented: h_eff {r['h_eff']/1e3:.0f} cal {r['cal']:.1f} tim {r['tim']:.1f} base {r['base']:.1f} conv {r['conv']:.1f} "
      f"avg {r['avg']:.1f} max {r['max']:.1f} R'' {r['R']:.3f} dP {r['dp']:.1f} pump {r['pump']:.1f} Qcap {r['Qcap']:.1f} Tmax {r['Tmax']:.1f}")
m = A.mc(P, tim_hi=0.03, **kw)
f = lambda t: f"{t[0]:.1f} / {t[1]:.1f} / {t[2]:.1f}"
print(f"MC X segmented: avg {f(m['avg'])} max {f(m['max'])} dP {f(m['dp'])} Qcap {f(m['Qcap'])}")
h = r["h_eff"] / 1e3
for lab, R in (("PCM", 0.055), ("LM", 0.015), ("In lid 0.011", 0.011)):
    d = A.die_dT(h, R, 1.0, A.K_CUDIA) + 3500 * 0.06 / 390
    print(f"350 W/cm2 X segmented {lab}: {d:.1f} K -> {45 + d:.1f} C")
for lab, Qk, Ar, lk in (("Rubin 2.3 kW 60 cm2 1.0", 2.3, 60, 1.0), ("Rubin 2.3 kW 60 cm2 1.2", 2.3, 60, 1.2),
                        ("Rubin Ultra 3.6 kW 80 cm2 1.0", 3.6, 80, 1.0), ("4 kW 25 cm2 1.5", 4.0, 25, 1.5),
                        ("25 kW 117 cm2", 25, 117, 1.2), ("30 kW 150 cm2", 30, 150, 1.2), ("wafer 20 kW 460 cm2", 20, 460, 1.2)):
    cp = hmmc(Ar, core="P", tim="liquid metal")
    rr = A.ev(cp, Q=Qk * 1e3, lk=lk, **xkw(cp))
    print(f"{lab}: X seg avg {rr['avg']:.1f} max {rr['max']:.1f} dP {rr['dp']:.1f} Qcap {rr['Qcap']:.1f}")
