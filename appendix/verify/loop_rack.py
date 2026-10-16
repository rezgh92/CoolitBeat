import sys, math, numpy as np, io, contextlib
rho = 1005.0; SG = 1.02; LPM = 1/60000
def plate_prism(l, port=20.0):
    s = l/18; up = 18*LPM/(math.pi/4*(port*1e-3)**2)
    i = 3.5*0.5*rho*up**2/1e3 + 0.80+0.46+0.10+1.82+0.06; v = 1.02
    return i*s*s + v*s
def plate_coolit(l, base=22.0):        # 15.4 viscous-ish core of 21.8 (hydraulic-detail): channel 14.7 visc, rest inertial
    s = l/18; f = base/21.8
    return f*(14.71*s*1.05**(s-1) + (0.67+3.41+3.0)*s*s)
def uqd_pair(l, cv):                   # two mated couplings (supply+return)
    gpm = l/3.785; return 2*SG*(gpm/cv)**2*6.895
def hose(l, m=1.0): return 5.6*m*(l/18)**1.75
def stubs(l, n=4, kpa18=3.5): return n*kpa18*(l/18)**2
print("=== UQD08 pair dP (two mated couplings) ===")
for cv, src in ((3.65, "FITOK UQD08 socket->plug"), (3.76, "FITOK alt sheet"), (4.75, "CPC Everis 'max'"), (5.32, "Danfoss (unconfirmed)"), (3.0, "research low"), (4.0, "research high")):
    print(f"  Cv {cv} ({src}): 9 LPM {uqd_pair(9,cv):.1f} | 15 {uqd_pair(15,cv):.1f} | 18 {uqd_pair(18,cv):.1f} | 36 {uqd_pair(36,cv):.1f} kPa")
print(f"  UQD08 10 mm bore velocity: 18 LPM {18*LPM/(math.pi/4*0.01**2):.2f} m/s; 36 LPM {36*LPM/(math.pi/4*0.01**2):.2f}; vendors' 5 m/s reference = 23.6 LPM")
print("\n=== Tray loops at 18 LPM (1 m 1/2-in hose, 4 x 12 mm stubs) ===")
for cv in (3.65, 4.75):
    p = plate_prism(18); c = plate_coolit(18)
    lp = p + uqd_pair(18, cv) + hose(18) + stubs(18); lc = c + uqd_pair(18, cv) + hose(18) + stubs(18)
    dual = plate_prism(18) + 0.5 + uqd_pair(9, cv) + hose(9) + stubs(9)   # +0.5 kPa for 4 x 13 mm horizontal bores
    print(f"  Cv {cv}: PRISM single UQD08 {lp:.1f} kPa | CoolIT-like (22) {lc:.1f}; (35 kPa plate) {lc-c+35:.1f} | PRISM dual UQD08 {dual:.1f} kPa")
print("\n=== Port-bore boundary: plate dP at 18 LPM with the same bore on both plates (K 3.5 on bore) ===")
for d in (20, 16, 12):
    u = 18*LPM/(math.pi/4*(d*1e-3)**2); pt = 3.5*0.5*rho*u*u/1e3
    pr = plate_prism(18) - 1.60 + pt; co = 21.8 - 3.0 + pt
    print(f"  {d} mm: PRISM {pr:.1f} vs CoolIT-like {co:.1f} kPa -> {100*(1-pr/co):.0f} % lower, ratio {co/pr:.1f}x")
print(f"  core only (no ports): PRISM {plate_prism(18)-1.60:.1f} vs CoolIT-like {21.8-3.0:.1f}")
# ---- equal pumping power at plate vs loop boundary
def solve_flow(f, target):
    lo, hi = 1.0, 80.0
    for _ in range(80):
        m = 0.5*(lo+hi); lo, hi = (m, hi) if f(m)*m/60 < target else (lo, m)
    return lo
print("\n=== Equal pumping power ===")
for cbase in (17.0, 22.0, 35.0):
    W = plate_coolit(18, cbase)*18/60
    q_plate = solve_flow(plate_prism, W)
    for cv in (3.65, 4.75):
        Wl = (plate_coolit(18, cbase) + uqd_pair(18, cv) + hose(18) + stubs(18))*18/60
        q_loop = solve_flow(lambda l: plate_prism(l) + uqd_pair(l, cv) + hose(l) + stubs(l), Wl)
        print(f"  CoolIT plate {cbase} kPa: plate-only {W:.1f} W -> PRISM {q_plate:.1f} LPM | loop (single UQD08 Cv {cv}) {Wl:.1f} W -> PRISM {q_loop:.1f} LPM")
# ---- thermal at those flows via the draft's own thermal model (hydraulic lane: flows recomputed, thermal model reused)
sys.path.insert(0, '../arch')
with contextlib.redirect_stdout(io.StringIO()):
    from prism_scorecard import ev
print("\n=== Draft thermal model at corrected flows (PCM25 / paste) ===")
for l in (11.1, 11.4, 18.0, 19.5, 20.5, 28.5, 36.0):
    a = ev("R6", "PCM25", lk=l/15); b = ev("R6", "paste", lk=l/15)
    print(f"  {l:5.1f} LPM: PCM {a['avg']:.1f}/{a['max']:.1f}  paste {b['avg']:.1f}/{b['max']:.1f}  outlet {45+a['dTout']:.1f} C")
# flow floor for 65 C return at 45 C inlet
rc = 1005*3930; print(f"  min flow for 65 C return (rho cp {rc/1e6:.2f} MJ/m3K): {15000/(rc*20)/LPM:.2f} LPM; with PG25 rho 1015 cp 3950: {15000/(1015*3950*20)/LPM:.2f} LPM")
# ---- velocity caps at Q-capacity points (1.2 LPM/kW)
print("\n=== Velocities at the draft's Q-capacity points (1.2 LPM/kW), rated 15 LPM so cap applies at 22.5 LPM ===")
for lab, kw in (("PCM 19.4 kW", 19.4), ("paste 16.6", 16.6), ("LM 26.4", 26.4), ("P+PCM 23.3", 23.3), ("P+LM 34.1", 34.1), ("25 kW on 117 cm2", 25), ("30 kW", 30)):
    l = 1.2*kw; up = l*LPM/(math.pi/4*0.02**2); um = l*LPM/(486*0.45e-6); umo = l*LPM/(486*0.396e-6)
    print(f"  {lab}: {l:.1f} LPM port20 {up:.2f} m/s (cap 1.5) meter {um:.2f}/{umo:.2f} m/s rect/oblong (cap 2.0) {'VIOLATES' if up>1.5 or um>2.0 else 'ok'}")
print(f"  port-20 cap reached at {1.5*math.pi/4*0.02**2/LPM:.1f} LPM = {1.5*math.pi/4*0.02**2/LPM/1.2:.1f} kW; meter cap (rect) at {2.0*486*0.45e-6/LPM:.1f} LPM = {2.0*486*0.45e-6/LPM/1.2:.1f} kW; (oblong) {2.0*486*0.396e-6/LPM/1.2:.1f} kW")
