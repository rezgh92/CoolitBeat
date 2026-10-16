import sys
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../ctl')))
from harness import ev, cm
PG = cm.Fluid('PG25 k0.49', 1005.0, 3930.0, 1.25e-3, 0.49)
e = ev(A=117.0, tim="paste", L=7.7, base=0.8, fluid=PG)
print({k: round(v, 4) for k, v in e.items()})
print("wall shear Pa (6 mu u / gap):", 6*1.25e-3*e['u']/0.15e-3)
for g in (0.146, 0.14, 0.13):
    r = (0.15/g)**3; print(f"gap {g}: fin dP x{r:.3f}; plate dP +{(r-1)*e['dp_ch']/7.59*100:.1f} %")
