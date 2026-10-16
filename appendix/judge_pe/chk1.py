import sys, math
sys.path.insert(0, "/home/user/Rez/docs/cooling/model")
sys.path.insert(0, "docs/cooling/appendix/design/pe")
from coldplate_model import coolit_like, hmmc, PG25
import pe_fourier as F
from pe_common import WEG65, cartridge, ev
# skived split-flow plate on a power shelf footprint
for A,Q in ((60,2400),(117,15000)):
    r = coolit_like(A).evaluate(Q, 1.2)
    print(A, Q, "coolit-like h_eff kW/m2K", round(r['h_eff']/1e3,1), "u", round(r['u_ch'],3), "Re", round(r['Re']), "dP", round(r['dp_total_kPa'],2))
# direct-substrate sinter on a CoolIT-class skived fin field (h_eff from above) in PG25 at 45 C, Tj 150
r = coolit_like(60).evaluate(2400, 1.2)
L = F.module_stack(1.0e-3, "sinter")
for h in (40e3, r['h_eff'], 124e3):
    R = F.die_temps(L, h)['Rth_max']
    # caloric full 9.7 K as in proposal
    q = (150-45-9.7)/R
    print("h", round(h/1e3), "Rth_max", round(R,4), "loss kW", round(q/1e3,2))
# skived plate + PCM 0.08 module-scale at h CoolIT-like
L2 = F.module_stack(3.0e-3, (0.08e-4*1.0, 1.0))  # placeholder
