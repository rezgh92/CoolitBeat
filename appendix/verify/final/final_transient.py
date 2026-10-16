"""Transient Tcase response to AI power excursions: Rev A (PKG-A: 0.8 mm base, 0.15/0.15x2.0 fins, L7.7) vs a CoolIT-like
split-flow plate (2.0 mm base, 0.2/0.2x4 mm fins). 1-D (z) finite-volume network per unit area, implicit Euler:
 source -> [TTV: 0.635 mm AlN heater | lidded: 3 mm Cu lid, heat input at die side] -> TIM (paste 0.07, no C) -> Cu base ->
 fin layer as an effective medium (k_z = phi k_Cu, C = phi rho c_Cu + (1-phi) rho c_fluid, volumetric h a_v to the fluid) -> fluid.
Fluid mean temperature = caloric term, first-order lag with the channel transit time. h is taken from the scoping/cell2d
harness and adjusted so the steady 1-D network reproduces each plate's steady conv (+ PRISM's own 2-D penalty) at 15 kW.
Case = heater face (TTV) or lid top (lidded). Pulses of 1.5x on top of a 1.0x steady state (128 W/cm2 baseline)."""
import sys, math
import numpy as np
from scipy.linalg import lu_factor, lu_solve
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../ctl')))
from harness import ev, cm
PG = cm.Fluid('PG25 k0.49', 1005.0, 3930.0, 1.25e-3, 0.49)
KCU, RCCU = 390.0, 8930*385.0; RCF = 1005*3930.0; RCALN = 3260*740.0
q0 = 15000/117e-4
def conv_1d(h, t, g, H):
    m = math.sqrt(2*h/(KCU*t)); eta = math.tanh(m*H)/(m*H); return q0/(h*(2*H*eta+g)/(t+g))
def solve_h(target, t, g, H):
    lo, hi = 1e3, 2e5
    for _ in range(80):
        mid = 0.5*(lo+hi)
        if conv_1d(mid, t, g, H) > target: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
def build(plate, config):
    t, g, H, tb, h, cal, tau = plate["t"], plate["g"], plate["H"], plate["tb"], plate["h"], plate["cal"], plate["tau"]
    nodes = []  # (dz, k, C, hv, is_source)
    if config == "TTV":
        nodes.append(dict(dz=0.635e-3, k=170.0, C=RCALN, hv=0.0, src=True, lumped=True))
    else:
        for i in range(12): nodes.append(dict(dz=3e-3/12, k=KCU, C=RCCU, hv=0.0, src=(i == 0), lumped=False))
    case_idx = len(nodes)-1  # last source-side node = case surface (TIM side)
    nb = 12
    for i in range(nb): nodes.append(dict(dz=tb/nb, k=KCU, C=RCCU, hv=0.0, src=False, lumped=False))
    nodes[-1]["hv_floor"] = h*g/(t+g)
    phi = t/(t+g); nf = 20
    for i in range(nf): nodes.append(dict(dz=H/nf, k=phi*KCU, C=phi*RCCU+(1-phi)*RCF, hv=h*2/(t+g), src=False, lumped=False))
    n = len(nodes); Rtim = 0.07e-4
    # conductances between node centres
    G = np.zeros(n-1)
    for i in range(n-1):
        a, b = nodes[i], nodes[i+1]
        r = (0.0 if a.get("lumped") else a["dz"]/2/a["k"]) + b["dz"]/2/b["k"]
        if i == case_idx: r += Rtim
        G[i] = 1/r
    Cv = np.array([nd["dz"]*nd["C"] for nd in nodes])
    Hs = np.array([nd["dz"]*nd["hv"] + nd.get("hv_floor", 0.0) for nd in nodes])
    src = np.array([1.0 if nd["src"] else 0.0 for nd in nodes])
    K = np.zeros((n, n))
    for i in range(n-1):
        K[i, i] += G[i]; K[i+1, i+1] += G[i]; K[i, i+1] -= G[i]; K[i+1, i] -= G[i]
    K += np.diag(Hs)
    # case temperature: for TTV the lumped heater node; for the lid, the top face of the lid = node centre + half-cell (approx node value)
    return dict(K=K, Cv=Cv, Hs=Hs, src=src, case=case_idx, n=n, cal=cal, tau=tau)
def simulate(net, pulse, mult=1.5, dt=2e-4, tend=None):
    K, Cv, Hs, src = net["K"], net["Cv"], net["Hs"], net["src"]
    Tf0 = net["cal"]  # fluid mean rise at 1.0x
    T = np.linalg.solve(K, src*q0 + Hs*Tf0)  # steady at 1.0x
    T1 = T[net["case"]]
    Tss15 = np.linalg.solve(K, src*q0*mult + Hs*Tf0*mult)[net["case"]]
    tend = tend or pulse
    A = np.diag(Cv/dt) + K; lu = lu_factor(A); Tf = Tf0; tt = 0.0; peak = T1
    while tt < tend - 1e-12:
        P = mult if tt < pulse else 1.0
        Tf += dt/(net["tau"]+dt)*(Tf0*P - Tf)
        T = lu_solve(lu, Cv/dt*T + src*q0*P + Hs*Tf); tt += dt
        peak = max(peak, T[net["case"]])
    return T1, peak, Tss15
plates = {}
e = ev(A=117.0, lpm=18.0, tim="paste", fluid=PG, L=7.7, base=0.8)
hP = solve_h(e["conv"] + e["pen"], 0.15e-3, 0.15e-3, 2.0e-3)
plates["Rev A (PKG-A, 0.8 mm base)"] = dict(t=0.15e-3, g=0.15e-3, H=2.0e-3, tb=0.8e-3, h=hP, cal=e["cal"], tau=7.7e-3/max(e["u"], 1e-3))
p = cm.coolit_like(119.3); r = p.evaluate(15000, 1.2, fluid=PG)
q119 = 15000/119.3e-4; conv117 = r["dT_conv"]*q0/q119
hC = solve_h(conv117, 0.2e-3, 0.2e-3, 4.0e-3)
plates["CoolIT-like (2.0 mm base)"] = dict(t=0.2e-3, g=0.2e-3, H=4.0e-3, tb=2.0e-3, h=hC, cal=r["dT_cal"], tau=0.5*math.sqrt(119.3)*10e-3/r["u_ch"])
for k, v in plates.items():
    print(f"{k}: h {v['h']/1e3:.1f} kW/m2K, caloric {v['cal']:.2f} K, fluid lag {v['tau']*1e3:.0f} ms, base+fin Cu-equivalent {v['tb']*1e3 + v['H']*1e3*v['t']/(v['t']+v['g']):.2f} mm, near-die base heat capacity {RCCU*v['tb']/1e4:.2f} J/K/cm2")
print("\nPulse 1.0x -> 1.5x (128 -> 192 W/cm2) for the stated duration, paste TIM both; values are Tcase - Tin (K), same uniform-flux 1-D basis")
print("| config | plate | 1.0x steady | 10 ms peak | 100 ms peak | 1 s peak | 10 s peak | 1.5x steady | excursion at 10 ms / 100 ms / 1 s / 10 s |")
print("|---|---|---|---|---|---|---|---|---|")
for config in ("TTV", "lid"):
    for k, v in plates.items():
        net = build(v, config); res = []
        for pulse, dt in ((0.01, 2e-5), (0.1, 1e-4), (1.0, 5e-4), (10.0, 2e-3)):
            T1, pk, Tss = simulate(net, pulse, dt=dt); res.append(pk)
        print(f"| {config} | {k} | {T1:.1f} | {res[0]:.1f} | {res[1]:.1f} | {res[2]:.1f} | {res[3]:.1f} | {Tss:.1f} | " + " / ".join(f"{x-T1:.1f}" for x in res) + " |", flush=True)
print("\nNote: steady values are 1-D network values with paste (no hot-spot terms); compare with the scorecard averages (PKG-A 31.0 K, CoolIT 34.4 K).")
