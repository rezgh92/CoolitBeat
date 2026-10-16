#!/usr/bin/env python3
"""Part B3: no-manifold straight skived-fin coolers (is the manifold needed?), Al pin-fin baseline, transient mass."""
import sys, math
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
from coldplate_model import ColdPlate, PG25, K_CU, K_AL
import pe_fourier as F
from pe_common import WEG65, WEGm40, A_MOD, FLOW, N_SW, P_SW, cartridge, ev

side = math.sqrt(A_MOD)*10
print("## D1. Straight single-pass skived-fin cooler (no manifold), 84 cm2, 10 L/min WEG 65 C")
print("| core | flow length mm | u m/s | Re | h_eff kW/m2K | channel+K dP kPa (65 C) | at -40 C | hottest-switch caloric (series) K |")
print("|---|---|---|---|---|---|---|---|")
mdot = FLOW/60000*WEG65.rho; dTout = N_SW*P_SW/(mdot*WEG65.cp)
for gap, fin, H in ((0.40, 0.30, 5.0), (0.15, 0.10, 2.0)):
    cp = ColdPlate(name="straight", footprint_cm2=A_MOD, fin_t_mm=fin, gap_mm=gap, fin_h_mm=H, flow_len_mm=side, base_mm=2.0,
                   tim="direct-to-die", isothermal_cell=False, hotspot_flow_K=0.0, n_parallel_paths=1, K_channel=2.0,
                   header_u_m_s=0.5, K_header=2.0, port_bore_mm=14.0, K_port=2.3)
    r = ev(cp, WEG65); rc = ev(cp, WEGm40)
    print(f"| {gap}/{fin}x{H} straight | {side:.0f} | {r['u_ch']:.2f} | {r['Re']:.0f} | {r['h_eff']/1e3:.0f} | {r['dp_ch_kPa']+r['dp_K_kPa']:.1f} (total {r['dp_total_kPa']:.1f}) | {rc['dp_ch_kPa']+rc['dp_K_kPa']:.0f} | {5/6*dTout:.1f} |")

print("\n## D2. Aluminium baselines (same stack, Al base 3 mm k 200; Al pin-fin h = 0.9 x Cu calibrated)")
h_pf, _ = F.calibrate_h(0.100, F.module_stack(3.0e-3, "solder"))
for nm, L, h in (("Al pin-fin baseplate on DBA (sinter)", F.module_stack(3.0e-3, "sinter", base_k=K_AL), 0.9*h_pf),
                 ("PE-Al cartridge 0.50/0.50x5 on DBA (sinter)", F.module_stack(2.0e-3, "sinter", base_k=K_AL), ev(cartridge("al", 0.5, 0.5, 5.0, 4.0, 2.0, k=K_AL), WEG65)['h_eff']),
                 ("PE-Al cartridge 0.40/0.40x5 (Al, filtered)", F.module_stack(2.0e-3, "sinter", base_k=K_AL), ev(cartridge("al", 0.4, 0.4, 5.0, 4.0, 2.0, k=K_AL), WEG65)['h_eff'])):
    r = F.die_temps(L, h)
    print(f"- {nm}: h_eff {h/1e3:.0f} kW/m2K, Rth {r['Rth_mean']:.4f} K/W")

print("\n## D3. Thermal mass per 14 cm2 switch cell (mm-equivalent Cu below the substrate)")
pin = 3.0 + (math.pi*(1.0)**2/(3.0*2.6))*8.0
cart = 2.0 + 0.30/0.70*5.0
print(f"pin-fin 3 mm base + 2 mm pins (3.0x2.6 pitch, 8 mm): {pin:.1f} mm-eq ({pin*14*0.1*3.45:.0f} J/K); "
      f"PE-A cartridge 2.0 mm + 0.30/0.40x5 fins: {cart:.1f} mm-eq ({cart*14*0.1*3.45:.0f} J/K); PE-DS-R 1.0 + 0.10/0.25x2: {1.0+0.4*2.0:.1f} mm-eq")
