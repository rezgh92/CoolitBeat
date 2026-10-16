#!/usr/bin/env python3
"""Jet-impingement vs manifold-microchannel scoping for the jet-hybrid lens.
PG25 at ~50 C film. 117 cm2 footprint, 18 and 36 LPM. Fouling-tolerant orifices d >= 0.3 mm.
Correlations: Martin (1977) ARN (turbulent, Re>=2000, 0.004<=Ar<=0.04, 2<=H/D<=12), extrapolated
below Re 2000 as an OPTIMISTIC bound; laminar stagnation model Nu0 = 0.8 Re^0.5 Pr^0.4 with r^-0.8
decay beyond 0.75 d (Liu-Lienhard / Elison-Webb class) as the CONSERVATIVE bound; Womac-type two-zone
(stagnation radius 1.9 d, Nu_stag = 0.785 Re^0.5 Pr^0.4; wall-jet zone Nu_L = 0.344 Re_L^0.8 Pr^0.4
on jet velocity) as a MID estimate. Constants from memory, +/-30 %."""
import math
rho, mu, cp, k = 1005.0, 1.25e-3, 3930.0, 0.52
nu = mu/rho; Pr = cp*mu/k
A = 117e-4
def j_of(lpm): return lpm/60/1000/A

def martin_arn(Re, Ar, HD):
    sa = math.sqrt(Ar)
    K = (1 + (HD/(0.6/sa))**6)**(-0.05)
    G = 2*sa*(1-2.2*sa)/(1+0.2*(HD-6)*sa)
    return Pr**0.42*K*G*Re**(2/3)

def h_laminar_avg(Re, d, S, C=0.8, n=0.8):
    Nu0 = C*Re**0.5*Pr**0.4
    h0 = Nu0*k/d
    R = S/math.sqrt(math.pi); r0 = 0.75*d
    if R <= r0: return h0, h0
    integ = r0**2 + 2*r0**n*(R**(2-n)-r0**(2-n))/(2-n)
    return h0, h0*integ/R**2

def h_womac_avg(Re, d, S, Vj):
    # two-zone: stagnation disc radius 1.9 d, remainder wall jet with L* = R - 1.9 d
    R = S/math.sqrt(math.pi); rs = min(1.9*d, R)
    h_stag = 0.785*Re**0.5*Pr**0.4*k/d
    Lw = max(R - rs, 1e-6)
    ReL = Vj*Lw/nu
    h_wall = 0.344*ReL**0.8*Pr**0.4*k/Lw
    f = (rs/R)**2
    return f*h_stag + (1-f)*h_wall

def dp_jet(Vj, Cd=0.72, Kextra=1.0):
    return 0.5*rho*Vj**2*(1/Cd**2 + Kextra)

HMMC_R = dict(h_eff=127e3, dp=5.3e3, pump=1.6)  # model, design H, 0.15/0.10x2.0
HMMC_P = dict(h_eff=187e3, dp=5.4e3)

print(f"PG25: nu={nu:.3e} m2/s, Pr={Pr:.1f}; j at 18 LPM = {j_of(18)*100:.2f} cm/s, at 36 LPM = {j_of(36)*100:.2f} cm/s\n")
print("## A. Bare-surface jet arrays (distributed return), 117 cm2")
print("| LPM | d mm | Ar | pitch mm | Vj m/s | Re_d | h lam-avg | h Womac | h Martin(extrap) | dP kPa (orifice+return) | +3 kPa plumbing | pump W |")
print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
rows=[]
for lpm in (18,36):
    j=j_of(lpm)
    for d in (0.3e-3, 0.45e-3, 0.5e-3):
        for Ar in (0.004, 0.007, 0.01, 0.02, 0.04):
            Vj=j/Ar; Re=Vj*d/nu; S=d*math.sqrt(math.pi/4/Ar)
            h0,hl=h_laminar_avg(Re,d,S); hw=h_womac_avg(Re,d,S,Vj)
            hm=martin_arn(Re,Ar,2.0)*k/d
            dp=dp_jet(Vj); dpt=dp+3e3; pump=dpt*lpm/60/1000
            flag = "" if Re>=2000 else "*"
            print(f"| {lpm} | {d*1e3:.2f} | {Ar:.3f} | {S*1e3:.2f} | {Vj:.2f} | {Re:.0f}{flag} | {hl/1e3:.0f} | {hw/1e3:.0f} | {hm/1e3:.0f} | {dp/1e3:.1f} | {dpt/1e3:.1f} | {pump:.1f} |")
print("(* = below Martin validity, Martin value is an extrapolated optimistic bound)")
print(f"\nHMMC-R reference: h_eff {HMMC_R['h_eff']/1e3:.0f} kW/m2K at {HMMC_R['dp']/1e3:.1f} kPa, {HMMC_R['pump']:.1f} W (18 LPM); HMMC-P {HMMC_P['h_eff']/1e3:.0f} kW/m2K at {HMMC_P['dp']/1e3:.1f} kPa")

print("\n## B. Equal pumping power / equal dP solutions, 18 LPM, d = 0.45 mm, bare surface")
for target in (5.3e3, 24.6e3, 50e3):
    Vj=math.sqrt(2*(target-3e3 if target>3e3 else target)/(rho*(1/0.72**2+1)))
    j=j_of(18); Ar=j/Vj; d=0.45e-3; Re=Vj*d/nu; S=d*math.sqrt(math.pi/4/Ar)
    h0,hl=h_laminar_avg(Re,d,S); hw=h_womac_avg(Re,d,S,Vj); hm=martin_arn(Re,min(max(Ar,0.004),0.04),2.0)*k/d
    print(f"- plate dP {target/1e3:.1f} kPa ({target*0.3/1e3:.1f} W): Vj {Vj:.2f} m/s, Ar {Ar:.4f}, pitch {S*1e3:.1f} mm, Re {Re:.0f}: h_avg laminar {hl/1e3:.0f} / Womac {hw/1e3:.0f} / Martin-extrap {hm/1e3:.0f} kW/m2K vs HMMC-R 127 at 5.3 kPa")

print("\n## C. Die-zone (3x local flux density, 2.5x at 2x flow) jet landing field vs fins")
for lpm,zone in ((18,3.0),(36,3.0)):
    j=j_of(lpm)*zone; d=0.45e-3
    for Ar in (0.015,0.028):
        Vj=j/Ar; Re=Vj*d/nu; S=d*math.sqrt(math.pi/4/Ar)
        h0,hl=h_laminar_avg(Re,d,S); hw=h_womac_avg(Re,d,S,Vj); hm=martin_arn(Re,Ar,2.0)*k/d
        # short pin field around pads: pins 0.2 mm dia, 0.4 mm pitch, 0.6 mm tall; wall-jet h ~ 0.6 Re^0.5 Pr^0.37 on 0.5 Vj
        u=0.5*Vj; Rep=u*0.2e-3/nu; hp=0.6*Rep**0.5*Pr**0.37*k/0.2e-3
        m=math.sqrt(4*hp/(390*0.2e-3)); eta=math.tanh(m*0.6e-3)/(m*0.6e-3)
        AR=1+math.pi*0.2e-3*0.6e-3*eta/(0.4e-3**2)
        hpin=hp*AR
        # pad fraction ~ (1.9d)^2 pi / S^2
        fpad=min(1.0, math.pi*(1.9*d)**2/S**2)
        hhyb=fpad*0.785*Re**0.5*Pr**0.4*k/d + (1-fpad)*hpin
        dp=dp_jet(Vj)
        print(f"- {lpm} LPM, zone {zone}x, Ar {Ar}: Vj {Vj:.2f} m/s, Re {Re:.0f}, pitch {S*1e3:.2f} mm; bare h_avg lam/Womac/Martin {hl/1e3:.0f}/{hw/1e3:.0f}/{hm/1e3:.0f}; pin field h_wall {hp/1e3:.0f} x AR {AR:.2f} = {hpin/1e3:.0f}; hybrid pad+pins {hhyb/1e3:.0f} kW/m2K; jet dP {dp/1e3:.1f} kPa  | fins: HMMC-R 127-129 / HMMC-P 187-206 at +0.7 kPa zoning")

print("\n## D. Fin-tip metering comb (JetFin) sizing per 108 mm slot, 0.667 LPM/slot at 18 LPM")
q=0.667/60/1000
for dpm in (2.0e3,2.5e3,3.0e3):
    Vj=math.sqrt(2*dpm/(rho*(1/0.70**2+1))); Aor=q/Vj
    n05=Aor/(math.pi/4*0.5e-3**2); n045=Aor/(math.pi/4*0.45e-3**2)
    Re=Vj*0.5e-3/nu
    print(f"- metering {dpm/1e3:.1f} kPa: Vj {Vj:.2f} m/s (Re_0.5mm {Re:.0f}), orifice area {Aor*1e6:.1f} mm2 -> {n05:.0f} x 0.5 mm holes ({108/n05:.2f} mm pitch) or {n045:.0f} x 0.45 mm; at 36 LPM dP x4 = {4*dpm/1e3:.0f} kPa")
# header dynamic head check
for uh in (1.0,1.5):
    print(f"  header u {uh} m/s: dynamic head {0.5*rho*uh**2/1e3:.2f} kPa; branch/head ratio at 2.5 kPa comb + 0.2 kPa channel = {2.7e3/(0.5*rho*uh**2):.1f} (need >= 6)")

print("\n## E. Jet-fed channel: what fraction of channels sees an impinging entry?")
for pitch_mm,hole in ((2.6,0.5),(1.2,0.5),(5.2,0.5)):
    print(f"- holes {hole} mm at {pitch_mm} mm pitch along the row: {hole/pitch_mm*100:.0f} % of channels under a hole; rest fed by 0.3 mm gallery at ~{0.0256*8/(3.5e-3*1000)*1:.2f} m/s-equivalent slot descent")

print("\n## F. Extended-fouling SKU (0.3 mm gaps, 0.2 mm fins, 4 mm tall) estimate")
for H in (3e-3,4e-3):
    b=0.3e-3;t=0.2e-3;p=b+t
    # channel h from model-like laminar Nu ~ 6.5 (3-side) * k/Dh with entrance factor ~1.3
    Dh=2*b*H/(b+H); h=6.5*1.3*k/Dh
    m=math.sqrt(2*h/(390*t)); eta=math.tanh(m*H)/(m*H); AR=(2*H*eta+b)/p
    print(f"- H {H*1e3:.0f} mm: h {h/1e3:.1f} kW/m2K, eta {eta:.2f}, AR {AR:.1f}, h_eff {h*AR/1e3:.0f} kW/m2K -> conv {128e4/(h*AR):.1f} K at 128 W/cm2; with +15 % jet entry {128e4/(1.15*h*AR):.1f} K")
