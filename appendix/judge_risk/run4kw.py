import sys, math
sys.path.insert(0,'/home/user/Rez/docs/cooling/model')
import coldplate_model as cm
from dataclasses import replace
def rf(footprint, *, gap=0.15, fin=0.15, H=2.0, base=1.0, tim="PCM pad", hs=1.5, name=None, orif=2.4):
    side = math.sqrt(footprint) * 10
    n_slots = max(1, int(round(side / 8.0)))
    return cm.ColdPlate(name=name or "RF", footprint_cm2=footprint, fin_t_mm=fin, gap_mm=gap, fin_h_mm=H, flow_len_mm=4.0,
        base_mm=base, tim=tim, isothermal_cell=True, hotspot_flow_K=hs, n_parallel_paths=2 * n_slots, slot_w_mm=3.0,
        K_channel=3.0, K_slot=1.5, header_u_m_s=0.8, K_header=1.0, port_bore_mm=16.0, K_port=2.3, orifice_dp_kPa_18=orif)
for lk in (1.2, 1.5):
  for v in (cm.coolit_like(25.0), rf(25.0, tim="paste 0.07", name="RF paste"), rf(25.0, tim="PCM pad", name="RF PCM"), rf(25.0, tim="liquid metal", name="RF LM")):
    r = v.evaluate(4000, lk)
    print(f"{lk} LPM/kW {v.name[:30]:30s} avg {r['dT_avg']:.1f} max {r['dT_max']:.1f} Rmax {r['dT_max']/4000:.4f} C/W cal {r['dT_cal']:.1f} tim {r['dT_tim']:.1f} base {r['dT_base']:.1f} conv {r['dT_conv']:.1f} NTU {r['NTU']:.2f} dP {r['dp_total_kPa']:.1f}")
# effect of h_eff -15% on 15 kW headline
v = rf(117.0, tim="PCM pad")
r = v.evaluate(15000,1.2)
print('headline', r['dT_avg'], r['dT_max'], r['NTU'], r['h_eff'])
