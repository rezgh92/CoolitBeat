"""Independent hydraulic re-derivation for PRISM-15 (verify-hydraulics).
PG25 ~45-50 C: rho 1012 (use 1005 to match draft too), mu 1.25e-3 (range 1.1-1.45)."""
import math, numpy as np
rho, mu = 1005.0, 1.25e-3
LPM = 1/60000
def head(u): return 0.5*rho*u*u
Q18 = 18*LPM
print("=== 1. Velocities at 18 LPM ===")
A_port20 = math.pi/4*0.020**2; A_port16 = math.pi/4*0.016**2
u20 = Q18/A_port20; u16 = Q18/A_port16
print(f"port 20 mm u={u20:.3f} m/s head={head(u20):.0f} Pa; 16 mm u={u16:.3f} head={head(u16):.0f}")
# header: 192 mm2 per direction carries 9 LPM (draft) -- check asymmetric layout
print(f"inlet header 192 mm2 @9 LPM u={9*LPM/192e-6:.3f}; outlet 224 mm2 @9 LPM u={9*LPM/224e-6:.3f}")
print(f"(if 2x(12x8) meant per-half 96 mm2: u={9*LPM/96e-6:.2f} m/s)")
# 18 plenums alternating: centres -51..51 step 6 -> inlets at -51,-39,...,45
cent = -51 + 6*np.arange(18); inl = cent[0::2]; outl = cent[1::2]
print("inlet plenum centres", inl, "outlet", outl)
print(f"mid-fed at x=0: left windows {np.sum(inl<0)}, right {np.sum(inl>0)} -> {18*np.sum(inl<0)/9:.0f}/{18*np.sum(inl>0)/9:.0f} LPM split; symmetric only if port at x={inl[4]:.0f}")
# segments: 18 lines alternating I O ... -> 17 interior intervals
print(f"segments per gap row with 18 lines: 17 (draft uses 18 -> 6480); fin field edges: inlet at -51 and outlet at +51 each face a 3 mm dead-end strip")
print(f"dead-end strip area 2*3*108 = {2*3*108/100:.1f} cm2 = {2*3*108/11664*100:.1f} % of 108x108 heated area")
# separator window
Asw = 4.5e-3*14e-3; usw = 2*LPM/Asw; print(f"separator window 63 mm2 @2 LPM u={usw:.3f} head={head(usw):.0f} Pa")
Apl = 4.5e-3*9e-3; upl = 2*LPM*(68/108)/Apl; Dh_pl = 2*4.5*9/(13.5)*1e-3
print(f"plenum long half u={upl:.3f} head={head(upl):.0f} Pa Re={rho*upl*Dh_pl/mu:.0f} (36 LPM Re {2*rho*upl*Dh_pl/mu:.0f})")
# meter orifice
A_rect = 0.5e-3*0.9e-3; A_obl = 0.5e-3*0.4e-3 + math.pi*0.25e-3**2
for lab, A1 in (("rectangle 0.45 mm2", A_rect), ("oblong/stadium 0.396 mm2", A_obl)):
    u = Q18/(486*A1)
    P = (2*0.4e-3 + math.pi*0.5e-3) if 'obl' in lab else 2*(0.5e-3+0.9e-3)
    Dh = 4*A1/P; Re = rho*u*Dh/mu
    for Cd in (0.61, 0.72, 0.80):
        print(f"meter {lab}: u={u:.3f} m/s Re={Re:.0f} t/Dh={0.4e-3/Dh:.2f} Cd {Cd}: dp={head(u)/Cd**2/1e3:.2f} kPa")
# fin channels
g, H = 0.15e-3, 2.0e-3
for nseg, Lch in ((6480, 5.7e-3), (6120, 5.7e-3), (6480, 6.0e-3)):
    u = Q18/nseg/(g*H); a = g/H
    fRe = 96*(1-1.3553*a+1.9467*a**2-1.7012*a**3+0.9564*a**4-0.2537*a**5)
    Dh = 2*g*H/(g+H); Re = rho*u*Dh/mu
    dpf = fRe*mu*u*Lch/(2*Dh**2); dph = 0.67*head(u)
    tau = 6*mu*u/g
    print(f"fins nseg {nseg} L {Lch*1e3:.1f}: u={u:.4f} Re={Re:.1f} fRe_D={fRe:.1f} dp={dpf:.0f}+{dph:.0f} Pa, wall shear {tau:.1f} Pa")
# CoolIT-like fin shear for comparison
print(f"CoolIT-like 0.2 mm gap 0.69 m/s wall shear {6*mu*0.69/0.2e-3:.1f} Pa; 1.5 m/s in 20 mm Cu tube turbulent: {0.316*(rho*1.5*0.02/mu)**-0.25/8*rho*1.5**2:.1f} Pa")
# orifice wall shear (developed slot + entrance)
uo = Q18/(486*A_obl); print(f"orifice wall shear developed slot {6*mu*uo/0.5e-3:.0f} Pa; entrance (Blasius x=0.2mm, U=uo/0.75) {0.332*rho*(uo/0.75)**2/math.sqrt(rho*(uo/0.75)*0.2e-3/mu):.0f} Pa")
# fin-entry mean vs jet
print(f"window mean entry: 2 LPM over (0.3 + 0.9*0.5)*108 mm2 = {2*LPM/((0.3+0.45)*108e-6):.2f} m/s ; orifice jet exit {uo:.2f}-{uo/0.75:.2f} m/s (vena contracta), travel 1.0 mm = {1.0/0.5:.1f} minor dia (inside potential core)")
# bleeds
for d in (0.6e-3, 1.0e-3, 1.1e-3):
    q = 0.65*math.pi/4*d*d*math.sqrt(2*2550/rho); print(f"dead-end bleed d={d*1e3:.1f} mm @2.55 kPa: {q/(2*LPM)*100:.1f} % of plenum flow")

print("\n=== 2. Element budget, independent K choices (kPa at 18 LPM), low / mid / high ===")
el = {}
# inlet: port bore + dividing bull-tee into header (K on port velocity), outlet: combining bull tee (K on port vel)
el['port bores + stub transitions (K 0.5-1.5 total on port u)'] = (0.5*head(u20), 1.0*head(u20), 1.5*head(u20))
el['inlet dividing bull tee (K 1.0-1.5 on port u)'] = (1.0*head(u20), 1.25*head(u20), 1.5*head(u20))
el['outlet combining bull tee (K 1.5-2.5 on port u)'] = (1.5*head(u20), 2.0*head(u20), 2.5*head(u20))
el['guard screen clean'] = (0.1e3, 0.3e3, 0.6e3)
el['header friction'] = (0.01e3, 0.02e3, 0.04e3)
el['separator windows in+out (K 3-5 total on 0.53 m/s)'] = (3*head(usw), 4*head(usw), 5*head(usw))
el['plenums net'] = (0.05e3, 0.15e3, 0.25e3)
uo_r = Q18/(486*A_rect); uo_o = Q18/(486*A_obl)
el['meter (rect Cd .80 / rect Cd .72 / oblong Cd .65)'] = (head(uo_r)/0.8**2, head(uo_r)/0.72**2, head(uo_o)/0.65**2)
el['window/kerf/outlet window'] = (0.05e3, 0.08e3, 0.15e3)
el['fin channels'] = (0.55e3, 0.63e3, 0.75e3)
lo = sum(v[0] for v in el.values()); mid = sum(v[1] for v in el.values()); hi = sum(v[2] for v in el.values())
for k, v in el.items(): print(f"  {k}: {v[0]/1e3:.2f} / {v[1]/1e3:.2f} / {v[2]/1e3:.2f}")
print(f"  TOTAL 20 mm ports: {lo/1e3:.1f} / {mid/1e3:.1f} / {hi/1e3:.1f} kPa  (draft 5.9, claim <= 7.5)")
d16 = (head(u16)-head(u20))*np.array([3.0, 4.25, 5.5])
print(f"  TOTAL 16 mm ports: {(lo+d16[0])/1e3:.1f} / {(mid+d16[1])/1e3:.1f} / {(hi+d16[2])/1e3:.1f} kPa (draft 8.2, claim <= 10)")
# 12 mm (1/2-in plumbing) ports for boundary comparison
u12 = Q18/(math.pi/4*0.012**2)
print(f"  12 mm bore at 18 LPM u={u12:.2f} m/s head {head(u12):.0f} Pa; draft K3.5 -> {3.5*head(u12)/1e3:.1f} kPa")
# draft script check
inert = 3.5*head(u20)/1e3 + 0.80 + 0.46 + 0.10 + 1.82 + 0.06; visc = 0.30+0.05+0.02+0.65
print(f"draft prism_flow: inertial {inert:.2f} viscous {visc:.2f} total {inert+visc:.2f} frac {inert/(inert+visc):.3f}; table rows sum = {1.6+0.30+0.80+0.56+0.15+1.82+0.08+0.65:.2f}")
def dpd(lpm, port=20.0):
    s = lpm/18; up = Q18/(math.pi/4*(port*1e-3)**2)
    i = 3.5*head(up)/1e3 + 0.80+0.46+0.10+1.82+0.06
    return i*s*s + visc*s
for l in (3.75, 11.1, 11.25, 15, 18, 22.5, 27, 28.5, 36):
    print(f"  draft law {l:5.2f} LPM: {dpd(l):.2f} kPa ({dpd(l)*l/60:.2f} W); 16 mm {dpd(l,16):.2f}")
