import sys
sys.path.insert(0, "docs/cooling/appendix/design/am")
sys.path.insert(0, "/home/user/Rez/docs/cooling/model")
import am_run as A
from coldplate_model import hmmc, coolit_like, PG25, TIM
from dataclasses import replace
print("PG25", PG25)
print("TIM", TIM)
for area in (100, 117, 145):
    r = A.ev(hmmc(area, core="R", tim="PCM pad"))
    c = A.ev(coolit_like(area))
    print(area, "R PCM avg %.1f max %.1f dp %.2f | coolit-like avg %.1f max %.1f" % (r['avg'], r['max'], r['dp'], c['avg'], c['max']))
r = A.ev(hmmc(117, core="R", tim="PCM pad"))
for k in ('u','Re','Nu','h','eta','h_eff','NTU','cal','tim','base','conv','avg','hs','max','dp','Qcap'):
    print(k, r[k])
# Qcap with hotspot flow scaling with Q
cp = hmmc(117, core="R", tim="PCM pad")
from scipy.optimize import brentq
def g(Q): return A.ev(cp, Q=Q)['Tmax']-85
print("Qcap self-consistent (hs flow const, scatter scales)", brentq(g, 5e3, 60e3)/1e3)
# scale flow hotspot too
def g2(Q):
    r = A.ev(cp, Q=Q); 
    return r['Tmax'] + cp.hotspot_flow_K*(Q/15000-1) - 85
print("Qcap if flow hotspot scales with Q", brentq(g2, 5e3, 60e3)/1e3)
print(cp)
