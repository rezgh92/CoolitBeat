import sys, math
sys.path.insert(0,__import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
import coldplate_model as cm
from prism_scorecard import ev
RHO=1005.0
def dpL6(lpm, port=20.0, Kport=3.5):
    s=lpm/18.0; up=18/60000/(math.pi/4*(port*1e-3)**2)
    inert = Kport*0.5*RHO*up**2/1e3 + 0.80 + 0.46 + 0.10 + 1.82 + 0.06
    visc = 0.30 + 0.05 + 0.02 + 0.65
    return inert*s*s + visc*s, inert, visc
for port in (16.0, 20.0):
    t,i,v = dpL6(18, port); print(f"PRISM-15 R6, {port:.0f} mm ports: 15 LPM {dpL6(15,port)[0]:.1f} | 18 LPM {t:.1f} kPa (inertial {i:.2f}, viscous {v:.2f}) | 27 LPM {dpL6(27,port)[0]:.1f} | 36 LPM {dpL6(36,port)[0]:.1f} kPa")
for tim in ("PCM25","paste","LM"):
    s=[]
    for lk in (0.6,0.75,1.0,1.2,1.5,2.0,2.4):
        e=ev("R6",tim,lk=lk); s.append(f"{lk}: {e['avg']:.1f}/{e['max']:.1f} (out {45+e['dTout']:.0f} C, {dpL6(lk*15)[0]:.1f} kPa)")
    print(f"R6 {tim}: "+"; ".join(s))
    for target,key in ((34.4,"avg"),(44.2,"max")):
        lo,hi=0.2,1.2
        for _ in range(60):
            mid=0.5*(lo+hi); e=ev("R6",tim,lk=mid); lo,hi=(lo,mid) if e[key]<target else (mid,hi)
        e=ev("R6",tim,lk=hi); print(f"   match CoolIT {key} {target}: {hi:.2f} LPM/kW ({hi*15:.1f} LPM), outlet {45+e['dTout']:.1f} C, {dpL6(hi*15)[0]:.1f} kPa, {dpL6(hi*15)[0]*hi*15/60:.2f} W")
lo,hi=18.0,60.0
for _ in range(60):
    mid=0.5*(lo+hi); w=dpL6(mid)[0]*mid/60
    lo,hi=(mid,hi) if w<6.54 else (lo,mid)
print(f"equal pumping power 6.5 W: {lo:.1f} LPM ({lo/15:.2f} LPM/kW), {dpL6(lo)[0]:.1f} kPa")
for tim in ("PCM25","paste","LM"):
    e=ev("R6",tim,lk=lo/15); print(f"   R6 {tim}: {e['avg']:.1f}/{e['max']:.1f}")
c=cm.coolit_like(117).evaluate(15000,2.4); print(f"CoolIT-like at 36 LPM: {c['dT_avg']:.1f}/{c['dT_max']:.1f}")
