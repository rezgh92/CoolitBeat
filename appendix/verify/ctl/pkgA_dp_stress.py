"""PKG-A element dP (same element method and K values as arch/prism_flow.dpL6) and the load paths changed by PKG-A,
on the draft's own convention (post-braze OFE yield design value 40 MPa at the 3.1 MPa design burst)."""
import math
from harness import ev
RHO = 1005.0
def dp(lpm, port=20.0, Kport=3.5, meter=2.30, plen_in=0.21, fins=None):
    s = lpm / 18.0; up = 18 / 60000 / (math.pi / 4 * (port * 1e-3) ** 2)
    hdr_u = 0.93  # 2 arches of ~80 mm2 per header half (161 mm2) at 9 LPM per half
    inert = Kport * 0.5 * RHO * up ** 2 / 1e3 + (1.5 * 0.5 * RHO * hdr_u ** 2 + 1.5 * 0.5 * RHO * 0.67 ** 2) / 1e3 + 0.46 + plen_in + meter + 0.06
    visc = 0.30 + 0.08 + 0.02 + fins
    return inert * s * s + visc * s, inert, visc
f = ev(L=7.7, base=0.8, tim="paste")["dp_ch"]
for lpm in (15, 18, 22.5, 27, 36):
    t, i, v = dp(lpm, fins=f)
    print(f"PKG-A {lpm} LPM: {t:.1f} kPa (inertial {i*(lpm/18)**2:.2f}, viscous {v*lpm/18:.2f}); meter velocity {1.54*lpm/18:.2f} m/s")
print(f"fin channels at L7.7: {f:.2f} kPa (draft L6: 0.65)")
p = 3.1
print("\nLoad paths at design burst 3.1 MPa (allowable 40 MPa, draft convention):")
print(f"- folded plenum wall 0.8 mm at 7.7 mm pitch, tension: {p*7.7/0.8:.1f} MPa (draft 1.5 mm walls at 6 mm: {p*6/1.5:.1f})")
print(f"- separator 1.5 mm over 6.9 mm outlet channels: {0.5*p*(6.9/1.5)**2:.1f} MPa (draft over 4.5 mm: {0.5*p*(4.5/1.5)**2:.1f})")
print(f"- grate cantilever to outlet-window edge, scaled from verify-manufacturing 23 MPa (draft, 1.4 mm bonded, 2.4 mm arm): "
      f"PKG-A 1.7 mm, 3.25 mm arm -> {23*(3.25/1.7)**2/(2.4/1.4)**2:.1f} MPa")
print(f"- arched cap 1.0 mm, r 6 mm, hoop: {p*6/1.0:.1f} MPa; port pocket r 12 mm at 1.5 mm: {p*12/1.5:.1f} MPa")
k = (1/0.8)**2*(7.4/6.3)**2
print(f"- defect case, one unbonded land strip (verify-manufacturing: 31-46 MPa at 1.55 MPa proof, collapse 3.5-5.0 MPa, 1.0 mm base, 6.3 mm span):"
      f" PKG-A 0.8 mm base, 7.4 mm span -> {31*k:.0f}-{46*k:.0f} MPa at proof, collapse {3.5/k:.1f}-{5.0/k:.1f} MPa;"
      f" bulge at proof x{(7.4/6.3)**4/0.8**3:.1f} (0.58 -> {0.58*(7.4/6.3)**4/0.8**3:.1f} um)")
