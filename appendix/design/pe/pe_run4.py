#!/usr/bin/env python3
"""Part B4: dielectric check and die-area sensitivity with the CHOSEN cores (C-A 0.40/0.30x5 L4, 2.0 mm base;
C-R 0.15/0.10x2 L4, 1.0 mm base), both with the 1.5 kPa @10 L/min metering comb."""
import sys, math
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
from coldplate_model import K_CU
import pe_fourier as F
from pe_common import WEG65, PAO65, cartridge, ev
comb18 = 1.5*(18/10)**2
cA = cartridge("C-A", 0.40, 0.30, 5.0, 4.0, 2.0, orifice_kPa=comb18, hdr_u=0.4)
cR = cartridge("C-R", 0.15, 0.10, 2.0, 4.0, 1.0, orifice_kPa=comb18, hdr_u=0.4)
h_pf, _ = F.calibrate_h(0.100, F.module_stack(3.0e-3, "solder"))
print("## E1. Dielectric PAO-2 vs WEG 50/50 at 65 C")
for nm, cp, L in (("C-A sinter 2.0 mm", cA, F.module_stack(2.0e-3, "sinter")), ("C-R sinter 1.0 mm", cR, F.module_stack(1.0e-3, "sinter"))):
    for fl, fw in ((WEG65, 10.0), (PAO65, 10.0), (PAO65, 10.0*WEG65.rho*WEG65.cp/(PAO65.rho*PAO65.cp))):
        r = ev(cp, fl, flow=fw); R = F.die_temps(L, r['h_eff'])['Rth_mean']
        print(f"- {nm}, {fl.name} {fw:.1f} L/min: h_eff {r['h_eff']/1e3:.0f} kW/m2K, Rth {R:.4f} K/W, dT_out {r['dT_out']:.1f} K, dP {r['dp_total_kPa']:.1f} kPa")
ratio = (PAO65.k/WEG65.k)*((PAO65.Pr/WEG65.Pr)**0.36)*(((PAO65.rho/PAO65.mu)/(WEG65.rho/WEG65.mu))**0.6)
print(f"- pin-fin, PAO-2 10 L/min: h_eff {ratio*h_pf/1e3:.1f} kW/m2K, Rth {F.die_temps(F.module_stack(3.0e-3,'solder'), ratio*h_pf)['Rth_mean']:.4f} K/W")
print("\n## E2. SiC-area sensitivity of the relative Rth gain (pin-fin h recalibrated to 0.100 K/W each time)")
hA = ev(cA, WEG65)['h_eff']; hR = ev(cR, WEG65)['h_eff']
for ds in (0.75, 1.0, 1.25):
    hh, rr = F.calibrate_h(0.100, F.module_stack(3.0e-3, "solder"), die_scale=ds)
    a1 = F.die_temps(F.module_stack(2.0e-3, "solder"), hA, die_scale=ds)['Rth_mean']
    a2 = F.die_temps(F.module_stack(2.0e-3, "sinter"), hA, die_scale=ds)['Rth_mean']
    r1 = F.die_temps(F.module_stack(1.0e-3, "sinter"), hR, die_scale=ds)['Rth_mean']
    print(f"- SiC {1.62*ds:.2f} cm2/switch: pin-fin h {hh/1e3:.1f}; PE-A1 {100*(a1/0.1-1):+.0f} %, PE-A2 {100*(a2/0.1-1):+.0f} %, PE-DS-R {100*(r1/0.1-1):+.0f} %")
