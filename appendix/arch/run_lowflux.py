import sys, math
sys.path.insert(0,__import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
import coldplate_model as cm
from cell2d import run
# GPU-class uniform lid: 2.3 kW on 60 cm2 at 1.0 LPM/kW (Rubin-class convention used by the proposals)
Q, A, lk = 2300.0, 60.0, 1.0
c = cm.coolit_like(A).evaluate(Q, lk)
print(f"CoolIT-like 1-D (scoping model): avg {c['dT_avg']:.1f} max {c['dT_max']:.1f}; cal {c['dT_cal']:.1f} tim {c['dT_tim']:.1f} base {c['dT_base']:.1f} conv {c['dT_conv']:.1f}; h {c['h']/1e3:.1f} heff {c['h_eff']/1e3:.0f}; dTout {c['dT_out']:.1f}")
q = Q/(A*1e-4); dTout = c['dT_out']; half = math.sqrt(A)*10/2
rc = run(hi=2.5, ho=1.0, ko=1.0, L=half, H=4.0, tb=2.0, d=0.1, q=q, dTout=dTout, h=c['h'], t=0.2, gap=0.2, h_floor_out=8e3, Kkerf_mult=50)
lin = 0.5*dTout + q/rc['heff1d'] + q*2e-3/390
print(f"CoolIT-like 2-D cal+conv+base {rc['case']:.2f} vs 1-D linear {lin:.2f} -> 2-D total avg incl paste {rc['case']+c['dT_tim']:.1f}")
for L in (4.0, 8.0, 12.0, 16.0):
    n_slots = max(1, int(round(math.sqrt(A)*10/(2*L))))
    p = cm.ColdPlate(name="PRISM-R", footprint_cm2=A, fin_t_mm=0.15, gap_mm=0.15, fin_h_mm=2.0, flow_len_mm=L, base_mm=1.0,
                     tim="PCM pad", isothermal_cell=True, hotspot_flow_K=1.5, n_parallel_paths=2*n_slots, slot_w_mm=3.0)
    r = p.evaluate(Q, lk)
    K3 = (0.3/0.15)**2/0.5
    r2 = run(hi=0.6, ho=0.6, ki=0.15, ko=0.15, L=L, H=2.0, tb=1.0, d=0.05 if L>6 else 0.025, q=q, dTout=dTout, h=r['h'], t=0.15, gap=0.15, Kkerf_mult=K3)
    print(f"PRISM-R L={L:.0f} mm: 1-D iso cal+conv+base {r['dT_cal']+r['dT_conv']+r['dT_base']:.2f} (NTU {r['NTU']:.1f}, cal {r['dT_cal']:.1f}); "
          f"2-D {r2['case']:.2f}; avg with PCM 0.055 {r2['case']+r['dT_tim']:.1f}, with paste {r2['case']+q*0.07e-4:.1f}; ch dP {r['dp_ch_kPa']:.2f} kPa; case pk-pk {r2['pkpk']:.2f}", flush=True)
