import sys
sys.path.insert(0, "/home/user/Rez/docs/cooling/model")
sys.path.insert(0, "docs/cooling/appendix/design/pe")
from coldplate_model import K_CU, PG25
import pe_fourier as F
from pe_common import cartridge
cR = cartridge("DC-R", 0.15, 0.10, 2.0, 4.0, 1.0, A=60.0, port=12.0)
rR = cR.evaluate(2400.0, 1.2, fluid=PG25); cal = rR['cal_frac']*rR['dT_out']
print("cal", round(cal,2), "dT_out", round(rR['dT_out'],2), "frac", round(rR['cal_frac'],2))
def dc(h, tr, b):
    L = [(b, K_CU)] + ([(tr*1e-4, 1.0)] if tr else []) + [(0.30e-3, K_CU), (0.32e-3, F.K_SN), (0.30e-3, K_CU)]
    return F.die_temps(L, h)['Rth_max']
for nm,h,tr,b in (("skived h99 + PCM",99e3,0.08,2e-3),("skived h99 + gap pad",99e3,0.5,2e-3),("DC-R h124 + PCM",124e3,0.08,2e-3)):
    R = dc(h,tr,b); print(nm, round(R,4), round((150-45-cal)/R/1e3,2), "kW")
# skived direct substrate sinter, 2 mm base (skived base) with linear caloric (0.5*dT_out) vs isothermal
R = F.die_temps(F.module_stack(2e-3,"sinter"), 99e3)['Rth_max']
print("skived direct-sub sinter 2mm base", round(R,4), "loss@cal", round((150-45-cal)/R/1e3,2), "loss@0.5dTout", round((150-45-0.5*rR['dT_out'])/R/1e3,2))
