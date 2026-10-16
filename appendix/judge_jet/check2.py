import sys, math
sys.path.insert(0, 'docs/cooling/appendix/design/jet')
sys.path.insert(0, '.')
import jet_hybrid_model as J
from check1 import cell_corrected
from coldplate_model import K_CU
rho, cp = J.rho, J.cp
j_die = 3.0*J.j_of(15.4)
print("j_die cm/s", j_die*100)
# die zone flows/caloric
Qdie = 4*26*33e-2*350  # W  (26x33 mm = 8.58 cm2)
lpm_die = 0.91*15.4
mcp = lpm_die/60e3*rho*cp
Adie = 4*8.58e-4
dTout = Qdie/mcp
print(f"Qdie {Qdie:.0f} W, die flow {lpm_die:.1f} LPM, dT_out die zone {dTout:.1f} K, A {Adie*1e4:.1f} cm2")
def cal_iso(h):
    NTU = h*Adie/mcp
    return dTout*(1/(1-math.exp(-NTU)) - 1/NTU), NTU
for h in (127e3, 133e3, 158e3, 172e3):
    c, n = cal_iso(h); print(f"  h {h/1e3:.0f}: NTU {n:.2f} caloric(iso, zone mean) {c:.2f} K")
for name, core, P_r, w_n in (("JH-R 6mm", J.JH_R, 6e-3, 0.42e-3), ("JH-R 4mm", J.JH_R, 4e-3, 0.28e-3), ("JH-P 6mm", J.JH_P, 6e-3, 0.51e-3), ("JH-X 6mm", J.JH_X, 6e-3, 0.47e-3)):
    dz = J.SlotJetFin(name, core.b, core.t, core.H, w_n, P_r, w_r=0.8e-3, base=core.base)
    r = cell_corrected(dz, j_die, delta_turn=0.5e-3, verbose=True)
    for lab, h in (("model", r['model']), ("corr", r['corr']), ("strict", r['strict']), ("ref", r['ref'])):
        # caloric adjusted relative to 6.7 at h=127
        dcal = cal_iso(h)[0] - cal_iso(127e3)[0]
        lm = J.hot_die_dT(h, 0.015) ; lm_c = lm + dcal
        lm08 = J.hot_die_dT(h, 0.015, base=0.8e-3) + dcal
        print(f"    {lab:6s} h {h/1e3:6.1f}: LM T_case {45+lm:.1f} C (with caloric shift {dcal:+.2f}: {45+lm_c:.1f} C; 0.8 mm base {45+lm08:.1f} C)")
# gallery velocity in die zone
print()
Q_die_m3 = lpm_die/60e3
for pitch, gw, gh in ((6e-3, 2.3e-3, 7.0e-3), (4e-3, 1.3e-3, 7.0e-3)):
    ngal = round(66e-3/pitch)
    q_half = Q_die_m3/ngal/2
    u = q_half/(gw*gh)
    head = 0.5*rho*u**2
    print(f"die pitch {pitch*1e3:.0f} mm: {ngal} inlet galleries {gw*1e3:.1f}x{gh*1e3:.1f} mm, half-gallery u {u:.2f} m/s, head {head:.0f} Pa, branch 2110 Pa -> ratio {2110/head:.1f} (rule >= 15 slot-entry)")
