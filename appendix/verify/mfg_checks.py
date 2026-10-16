"""Independent manufacturing / mechanical checks of PRISM-15 (verify lane: manufacturing).
Closed-form only (strip, plate, beam-on-elastic-foundation, capillary). +/-25-30 %."""
import numpy as np
E, nu, rho = 117e3, 0.34, 8.94e-3          # MPa, -, g/mm3
D = lambda t: E*t**3/(12*(1-nu**2))         # N.mm
p_d, p_s, p_pr, p_mawp = 3.1, 4.5, 1.55, 1.03
SY = (35, 40, 50)

print("== 1. Skiving volume balance (h*t = p*d) ==")
h, t, p = 2.0, 0.15, 0.30
d = h*t/p
print(f"depth of cut consumed d = {d:.2f} mm; 2.5 mm blank -> base during/after skive {2.5-d:.2f} mm "
      f"(CrossComb note: skiving needs >= 1.5-2 mm base during cut)")
print(f"fin tips stand {h-d:.1f} mm above the original blank face -> a frame flush with the tips needs a "
      f"{2.5-d+h:.1f} mm frame or a pre-pocketed field")
# skiving force: uncut chip = p*sin(theta)*... take kc 1500 N/mm2, uncut chip 0.05-0.08 mm over 108 mm
for uc in (0.05, 0.08):
    print(f"  skive stroke force at uncut chip {uc} mm x 108 mm, kc 1.2-1.8 GPa: {1.2e3*uc*108/1e3:.1f}-{1.8e3*uc*108/1e3:.1f} kN")

print("\n== 2. Kerf gang saw: run-out vs 8.5 mm border; tooth force vs fin lateral capacity ==")
for Dsaw in (20, 32, 50, 63):
    R = Dsaw/2; dk = 2.0
    print(f"  saw D {Dsaw} mm: arc run-out beyond full-depth point = {np.sqrt(2*R*dk-dk**2):.1f} mm (border 8.5 mm)")
# fin wall out-of-plane plastic capacity (cold-worked skived fin, sy 250-300 MPa), load at mid-height
for sy in (250, 300):
    for weff in (1.0, 2.0, 3.0):
        Mp = sy*weff*t**2/4
        print(f"  fin wall sy {sy}, effective width {weff} mm: lateral collapse load at 1 mm height = {Mp/1.0:.2f} N")
for fz in (0.005, 0.01, 0.02):
    print(f"  tooth force kc 1.5 GPa x fz {fz} x 0.3 kerf = {1500*fz*0.3:.2f} N (plus ploughing ~1-2 N on a dull edge)")
print(f"  burr/chip sites per plate: 18 kerfs x 360 fins x 2 faces = {18*360*2}")

print("\n== 3. Stamping ==")
tau = 200.0  # MPa, half-hard OFE shear (annealed ~150)
for name, tsheet, w, L, n, web in (("plenum lam 4.5 mm", 4.5, 4.5, 108, 18, 1.5),
                                    ("plenum lam 1.5 mm (x6)", 1.5, 4.5, 108, 18, 1.5),
                                    ("floor grate 1.0 mm", 1.0, 1.2, 108, 18, 4.8),
                                    ("meter 0.4 mm (per hole)", 0.4, 0.5, 0.9, 486, 1.1),
                                    ("separator 1.5 mm", 1.5, 4.5, 14, 18, 7.5)):
    F = n*2*(w+L)*tsheet*tau/1e3  # kN
    punch_stress = 2*(w+L)*tsheet*tau/(w*L)
    print(f"  {name}: d/t {w/tsheet:.2f}; web/t {web/tsheet:.2f} (conv. >= 1-2, fineblank ~0.6); "
          f"total shear force {F/9.81:.0f} t; punch stress {punch_stress:.0f} MPa")

print("\n== 4. Braze filler budget and capillarity ==")
gam, rhoL = 0.95, 9.8e-3*1e-3  # N/m ; not used
for g in (0.010, 0.020, 0.040, 0.150, 0.300):
    print(f"  capillary pressure 2*gamma/gap, gap {g*1e3:.0f} um: {2*0.95/(g*1e-3)/1e3:.1f} kPa")
land_frac = 4.2/6  # masked 0.3 mm each side of 1.2 mm windows
print(f"  bonded fraction after 0.3 mm masking: land {4.8/6:.2f} -> filler-covered {land_frac:.2f} of fin length")
for route, film in (("A 25 um foil", 25e-3), ("B 5 um Ag -> ~7 um liquid", 7e-3)):
    per_fin = film*p          # mm2 of liquid per fin per mm of bonded length
    bondline = 0.15*0.010     # 10 um x tip width
    fillet = 2*(1-np.pi/4)*0.04**2
    excess = per_fin - bondline - fillet
    print(f"  route {route}: liquid/fin {per_fin*1e3:.2f}e-3 mm2/mm; bond line {bondline*1e3:.2f}e-3; "
          f"fillets r40um {fillet*1e3:.2f}e-3; excess {excess*1e3:+.2f}e-3 -> gap-top fill {max(excess,0)/0.15*1e3:.0f} um; "
          f"max tip gap it can close ~{per_fin/0.15*1e3:.0f} um")
print("  tip-plane tolerance +/-20 um -> local gaps up to 40 um under a stiff land (1.0 mm grate is stiff at 0.3 mm scale)")
# fixture load
A = 125*125
F1 = 0.2*A/1e3
print(f"  fixture load 0.2 MPa x 125^2 = {F1:.1f} kN/plate (= {F1*1e3/9.81:.0f} kg dead weight); "
      f"30-80 plates -> {30*F1:.0f}-{80*F1:.0f} kN per furnace load")
print(f"  tip contact stress at 0.2 MPa (tips 50 % x 70 % bonded zone) = {0.2/(0.5*0.7):.2f} MPa")
# flattening pressure for a bowed 1.5 mm base (SS plate) and a stamped land strip
for bow in (0.05, 0.1, 0.2):
    pfl = bow*D(1.5)/(0.00406*108**4)
    print(f"  pressure to flatten a {bow*1e3:.0f} um bow in the 1.5 mm skived base over 108 mm: {pfl*1e3:.1f} kPa")
# furnace count
for per in (30, 80):
    for lpd in (2.0, 3.0):
        f = 100e3/(per*lpd*365*0.85)
        print(f"  {per}/load, {lpd} loads/day, 85 % availability: furnaces per 100k/yr = {f:.1f}")

print("\n== 5. Post-braze fly-cut on a tied fin foundation ==")
kf = E*0.5/2.0      # N/mm3 foundation modulus of 2 mm fins, 50 % solid
for tb in (1.0, 1.5):
    w = 1/(8*np.sqrt(D(tb)*kf))
    lam = (D(tb)/kf)**0.25
    print(f"  base {tb} mm: foundation k {kf:.0f} N/mm3, char. length {lam:.2f} mm, point compliance {w*1e6:.2f} um/kN -> "
          f"50 N thrust gives {50*w*1e3:.3f} um")
print("  over a free 0.3 mm kerf the base span is 0.3 mm: negligible; over an unbonded patch only the fins' "
      "compression matters (fins still attached to base), so deflection stays sub-um")
# thickness stack: skive base var, braze bow, cut, gauge
comps = {"skived base thickness": 0.05, "as-brazed bow of inner plane (clamped flat on chuck)": 0.05,
         "fly-cut plane": 0.01, "gauge / reference": 0.02}
rss = np.sqrt(sum(v**2 for v in comps.values())); wc = sum(comps.values())
print(f"  thickness tolerance: RSS +/-{rss:.3f} mm, worst case +/-{wc:.2f} mm vs claimed +/-0.10")
# machining residual stress bow
for layer, s in ((0.03, 100), (0.01, 100)):
    Dsand = 2.12e6   # N.mm (base-stress report, 2119 N.m)
    M = layer*s*7.0
    kappa = M/Dsand
    print(f"  cold-worked layer {layer*1e3:.0f} um at {s} MPa: bow over 108 mm {kappa*108**2/8*1e3:.1f} um, over 50 mm die {kappa*50**2/8*1e3:.1f} um")

print("\n== 6. Section 5.2 stresses re-derived ==")
for f in (0.80, 0.70, 0.56):
    s = p_d*p/(t*f)
    print(f"  fin tie, bonded fraction {f:.2f}: {s:.1f} MPa at 3.1 MPa ({2.5*s:.0f} local Kt2.5); at 4.5 MPa {p_s*p/(t*f):.1f} ({2.5*p_s*p/(t*f):.0f})")
print(f"  plenum wall tension 4p: {4*p_d:.1f} / {4*p_s:.1f} MPa")
print(f"  separator 1.5 mm over 4.5 mm (fixed strip): {p_d*4.5**2/(2*1.5**2):.1f} / {p_s*4.5**2/(2*1.5**2):.1f} MPa")
for tw in (3.5, 2.5):
    for b in (12, 14):
        s3 = p_d*b**2/(2*tw**2); s4 = p_s*b**2/(2*tw**2); spr = p_pr*b**2/(2*tw**2)
        pcs = [4*sy*tw**2/b**2 for sy in SY]
        print(f"  header top wall t {tw} over {b} mm: proof {spr:.0f}, design {s3:.0f}, sample {s4:.0f} MPa; "
              f"plastic collapse {pcs[0]:.1f}-{pcs[2]:.1f} MPa")
print("  stack-up check: header 8 mm + top wall 3.5 mm = 11.5 mm > 10.5 mm bar  -> wall is 2.5 mm as drawn")
# grate cantilever (missing load path)
for tt, lab in ((1.0, "grate alone"), (1.4, "grate+meter bonded")):
    M = 2.25*1.1    # per unit p: load 2.25p at ~1.1 mm arm
    Z = tt**2/6
    print(f"  floor-grate cantilever ({lab}, 1.65 mm from wall): {M/Z*p_d:.0f} / {M/Z*p_s:.0f} MPa; collapse "
          f"{sy_c:=0}" if False else f"  floor-grate cantilever ({lab}, 1.65 mm from wall): {M/Z*p_d:.0f} / {M/Z*p_s:.0f} MPa; "
          f"plastic collapse p = {40*tt**2/4/M:.1f} MPa (sy 40)")
# crossing joint between plenum walls (run y) and header ribs/walls (run x) under the bar
trib = 6*13
for Aeff in (3.0, 7.5, 12.0):
    print(f"  wall/rib crossing under bar: tributary {trib} mm2 -> {trib*p_d:.0f} N at 3.1 MPa; over {Aeff} mm2: "
          f"{trib*p_d/Aeff:.0f} / {trib*p_s/Aeff:.0f} MPa")
print(f"  perimeter land 1.8 mm over 4 mm: {p_d*16/(2*1.8**2):.1f} MPa")
# unbonded patch
for sy in SY:
    a_sq = 1.0*np.sqrt(sy/(0.3078*p_pr))
    a_strip = 1.0*np.sqrt(2*sy/p_pr)
    print(f"  unbonded patch, 1.0 mm base, yield at proof 1.55 MPa, sy {sy}: square {a_sq:.1f} mm, long strip across fins {a_strip:.1f} mm")
for a in (7, 9, 12, 15, 20):
    w = 0.00126*p_pr*a**4/D(1.0)*1e3
    print(f"  bulge at 1.55 MPa, clamped square patch {a} mm: {w:.1f} um (2 MPa: {w*2/1.55:.1f} um)")
for pb in (3.1, 4.5):
    print(f"  rupture-governed patch (scaled from 22 mm at 1.5 MPa, UTS-based): {22*np.sqrt(1.5/pb):.1f} mm at {pb} MPa")

print("\n== 7. IR flow screen ==")
alpha = 1.1e-4
for tt in (0.1, 0.5, 1.0, 5.0):
    print(f"  lateral diffusion length in Cu after {tt} s: {np.sqrt(alpha*tt)*1e3:.1f} mm")
print("  emissivity of lapped bare Cu ~0.02-0.05 -> needs a removable high-emissivity film/coating on the face")

print("\n== 8. Mass and copper buy ==")
parts = {"base 1.0 mm (125^2)": 125**2*1.0, "fins 50 % x 2 mm x 108^2 less kerfs": 108**2*2.0*0.5*(1-0.3/6),
         "frame 2 mm tall x (125^2-108^2)": (125**2-108**2)*2.0, "grate": (125**2-18*1.2*108)*1.0,
         "meter": (125**2-486*0.40-9*1.2*108)*0.4, "plenum layer": (125**2-18*4.5*108)*9.0,
         "separator": (125**2-18*4.5*14)*1.5}
tot = 0
for k, v in parts.items():
    m = v*rho/1e3; tot += m; print(f"  {k}: {m:.3f} kg")
print(f"  stack without bar: {tot:.2f} kg; + bar 0.41 + stubs/guard ~0.10 = {tot+0.51:.2f} kg (draft 1.75 incl. 'backplate')")
buy = {"base block 130x130x3.5": 130*130*3.5, "2 lam strips 4.5 mm (skeleton 1.25)": 2*130*130*4.5*1.25,
       "grate+meter+sep strips (1.25)": 130*130*2.9*1.25, "bar forging slug": 0.7/rho*1e3}
b = sum(v*rho/1e3 for v in buy.values())
fin = tot+0.41
print(f"  copper buy ~{b:.2f} kg, finished Cu ~{fin:.2f} kg, scrap ~{b-fin:.2f} kg -> copper line "
      f"US${b*18-(b-fin)*11.5:.0f} (draft 35 on 2.5 kg buy)")

print("\n== 9. Critical defect for a KERFED field: one unbonded land strip ==")
# kerfs cut the fin ribs, so an unbonded segment spans kerf-to-kerf: 5.7 + 2 x 0.3 = 6.3 mm, hinges = base at kerfs
L = 6.3
for tb in (1.0, 0.9, 0.85):
    for c, lab in ((12, "pL^2/12"), (8, "pL^2/8 (stiff ribbed middle)")):
        s_pr = 6*p_pr*L**2/c/tb**2; s_d = 6*p_d*L**2/c/tb**2
        print(f"  hinge t {tb} mm, {lab}: proof {s_pr:.0f} MPa, design burst {s_d:.0f} MPa")
    for sy in SY:
        pc = 16*(sy*tb**2/4)/L**2
        if tb == 1.0: print(f"    plastic collapse (fixed-fixed) sy {sy}: {pc:.1f} MPa")
w = p_pr*L**4/(384*D(1.0))*1e3
print(f"  elastic bulge of the strip at proof: {w:.2f} um (flatness scan resolution ~1 um) -> not detectable")
sm = 4.5*L**2/(8*200*1.0)
print(f"  membrane deflection to reach UTS 200 MPa at 4.5 MPa: {sm*1e3:.0f} um -> holds without rupture (burst sample passes)")
# bypass through a missed internal joint (wall between in/out plenums), PG25 45 C
mu = 1.5e-3
for g in (25e-6, 50e-6, 100e-6):
    Q = 0.108*g**3*2500/(12*mu*1.5e-3)*6e4
    print(f"  missed wall joint gap {g*1e6:.0f} um x 108 mm, 2.5 kPa: bypass {Q:.3f} LPM (inlet plenum carries ~2 LPM)")
