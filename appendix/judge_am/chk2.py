import sys
sys.path.insert(0, "docs/cooling/appendix/design/am")
sys.path.insert(0, "/home/user/Rez/docs/cooling/model")
import am_run as A
from coldplate_model import hmmc, coolit_like
for area in (100, 117, 130, 145):
    for tim in ("paste 0.07","PCM pad","liquid metal"):
        r = A.ev(hmmc(area, core="R", tim=tim))
        print(area, tim, "avg %.1f max %.1f" % (r['avg'], r['max']))
# GPU-class: Rubin and 4 kW point
for (Q, area, lk) in ((2300,60,1.0),(2300,60,1.2),(3600,80,1.0),(4000,25,1.5)):
    for tim in ("PCM pad","liquid metal"):
        r = A.ev(hmmc(area, core="R", tim=tim), Q=Q, lk=lk)
        print(Q, area, lk, tim, "avg %.1f max %.1f cal %.1f conv %.1f dp %.2f NTU %.2f" % (r['avg'], r['max'], r['cal'], r['conv'], r['dp'], r['NTU']))
    c = A.ev(coolit_like(area), Q=Q, lk=lk)
    print("   coolit-like avg %.1f max %.1f" % (c['avg'], c['max']))
