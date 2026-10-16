import sys
sys.path.insert(0, "/home/user/Rez/docs/cooling/model")
import coldplate_model as cm
from dataclasses import replace
print(cm.TIM.keys())
A0=117.0; Q=15000; LK=1.2
cm.TIM["D2D LM + Ni5"]=(0.015+0.000625,0.6)
cm.TIM["paste"] = cm.TIM.get("paste", (0.07,3.5))
for lab,p in [("CoolIT-like paste",cm.coolit_like(A0)),
              ("CoolIT-like LM", cm.coolit_like(A0, tim="liquid metal") if 'tim' in cm.coolit_like.__code__.co_varnames else None),
              ("HMMC R paste", cm.hmmc(A0, core="R", tim=[k for k in cm.TIM if 'paste' in k.lower()][0])),
              ("3A", cm.hmmc(A0, core="R", tim="D2D LM + Ni5", base_mm=0.8))]:
    if p is None: print(lab,"n/a"); continue
    r=p.evaluate(Q,LK)
    print(f"{lab}: cal {r['dT_cal']:.2f} tim {r['dT_tim']:.2f} base {r['dT_base']:.2f} conv {r['dT_conv']:.2f} avg {r['dT_avg']:.2f} max {r['dT_max']:.2f} dp {r['dp_total_kPa']:.2f} Qcap {r['Q_cap_kW']:.1f}")
