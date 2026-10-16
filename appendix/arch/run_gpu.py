import sys, math
sys.path.insert(0,__import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
import coldplate_model as cm
from cell2d import run
from prism_model import prism
K3=(0.3/0.15)**2/0.5
print("| lid case | CoolIT-like 1-D avg/max | CoolIT 2-D core | PRISM L | PRISM 2-D core | PRISM equiv avg (PCM pkg 0.07 / paste) | PRISM equiv max (PCM pkg) |")
for Q, A in ((1400.0, 45.0), (3600.0, 80.0)):
    lk = 1.0
    c = cm.coolit_like(A).evaluate(Q, lk); q = Q/(A*1e-4); dTout = c['dT_out']; half = math.sqrt(A)*10/2
    rc = run(hi=2.5, ho=1.0, ko=1.0, L=half, H=4.0, tb=2.0, d=0.1, q=q, dTout=dTout, h=c['h'], t=0.2, gap=0.2, h_floor_out=8e3, Kkerf_mult=50)
    for L in (4.0, 8.0, 12.0):
        n_slots = max(1, int(round(math.sqrt(A)*10/(2*L))))
        p = cm.ColdPlate(name="P", footprint_cm2=A, fin_t_mm=0.15, gap_mm=0.15, fin_h_mm=2.0, flow_len_mm=L, base_mm=1.0, tim="paste 0.07",
                         isothermal_cell=True, hotspot_flow_K=1.5, n_parallel_paths=2*n_slots, slot_w_mm=3.0)
        r = p.evaluate(Q, lk)
        r2 = run(hi=0.6, ho=0.6, ki=0.15, ko=0.15, L=L, H=2.0, tb=1.0, d=0.05 if L>6 else 0.025, q=q, dTout=dTout, h=r['h'], Kkerf_mult=K3)
        # differential method: PRISM equivalent = CoolIT 1-D (calibrated) - CoolIT 2-D core + PRISM 2-D core, with own TIM
        ccore1 = c['dT_cal']+c['dT_conv']+c['dT_base']
        eq_core = ccore1 + (r2['case'] - rc['case'])
        avg_pcm = eq_core + q*0.07e-4; avg_paste = eq_core + q*0.07e-4
        mx = avg_pcm + 1.5 + 1.5*q/1.28e6 + r2['pkpk']/2
        print(f"| {Q/1e3:.1f} kW / {A:.0f} cm2 ({q/1e4:.0f} W/cm2) | {c['dT_avg']:.1f}/{c['dT_max']:.1f} | {rc['case']:.2f} | {L:.0f} | {r2['case']:.2f} | {avg_pcm:.1f} / {avg_paste:.1f} | {mx:.1f} (pk-pk {r2['pkpk']:.1f}) |", flush=True)
