from vp_cell import solve, oneD
for A in (100.0, 117.0, 145.0, 25.0):
    q = 15000/(A*1e-4) if A != 25.0 else 4000/(25e-4)
    dT = 12.66 if A != 25.0 else 4000/(6.0/60000*1005*3930)
    o = oneD(q=q, dTout=dT); s = solve(L=6.0, dx=0.03, q=q, dTout=dT)
    s4 = solve(L=4.0, dx=0.025, q=q, dTout=dT)
    print(f"A {A} q {q/1e4:.0f} W/cm2 dTout {dT:.2f}: L6 pen {(s['case']/o['core']-1)*100:+.1f} % ({s['case']-o['core']:+.2f} K) pkpk {s['pkpk']:.2f}; L4 pen {(s4['case']/o['core']-1)*100:+.1f} % pkpk {s4['pkpk']:.2f}", flush=True)
