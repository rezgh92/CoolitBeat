"""Spend part of PRISM's dP margin to cut plenum depth (height, mass). Along-plenum max/min from the draft's own
1-D plenum model (arch/plenum_prism.run, imported without its __main__), offset feed +/-14 mm, momentum coefficients
(1,2) and (0.6,1.5). Branch = meter + fins + window/kerf; inertial part scales with flow^2."""
import sys, types, numpy as np
src = open(__import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../arch/plenum_prism.py'))).read().split('print("| case')[0]
mod = types.ModuleType("pp"); exec(src, mod.__dict__); run = mod.run
cases = [
 # label, n_inlet_plenums, W mm, Hp mm, meter kPa @18, fins kPa @18
 ("draft: 9 in, 4.5 x 9.0 (1.5 mm Cu walls), meter 1.82, L6", 9, 4.5, 9.0, 1.82, 0.65),
 ("9 in, 4.5 x 6.0, meter 1.82, L6", 9, 4.5, 6.0, 1.82, 0.65),
 ("9 in, 5.4 x 6.0 (0.6 mm folded walls), meter 2.3, L6", 9, 5.4, 6.0, 2.30, 0.65),
 ("9 in, 5.4 x 5.0, meter 2.3, L6", 9, 5.4, 5.0, 2.30, 0.65),
 ("7 in, 7.1 x 5.0 (0.6 mm walls), meter 2.3, L7.7", 7, 7.1, 5.0, 2.30, 1.07),
 ("7 in, 7.1 x 4.0, meter 2.3, L7.7", 7, 7.1, 4.0, 2.30, 1.07),
 ("7 in, 6.2 x 5.0 (1.5 mm walls), meter 2.3, L7.7", 7, 6.2, 5.0, 2.30, 1.07),
]
print("| layout | u long half @18 LPM m/s | branch kPa @18 | max/min 18 / 27 / 36 LPM (th 1/2) | (th 0.6/1.5) |")
print("|---|---|---|---|---|")
for lab, n, W, Hp, met, fin in cases:
    out1 = []; out2 = []
    for lpm in (18, 27, 36):
        s = lpm / 18.0
        inert = (met + 0.08) * s * s; visc = fin * s; dp0 = (inert + visc) * 1e3; fv = visc / (inert + visc)
        Q = lpm / n / 60000.0
        out1.append(run(W=W*1e-3, Hp=Hp*1e-3, Q=Q, dp0=dp0, fvisc=fv)); out2.append(run(W=W*1e-3, Hp=Hp*1e-3, Q=Q, dp0=dp0, fvisc=fv, th_i=0.6, th_o=1.5))
    u = (18 / n / 60000.0) * (54 + 14) / 108 / (W * Hp * 1e-6)
    print(f"| {lab} | {u:.2f} | {met + 0.08 + fin:.2f} | {' / '.join(f'{x:.3f}' for x in out1)} | {' / '.join(f'{x:.3f}' for x in out2)} |", flush=True)
