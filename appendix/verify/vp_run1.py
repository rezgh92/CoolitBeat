import time
from vp_cell import solve, oneD
o = oneD(); print("1-D iso:", {k: round(float(v),3) for k,v in o.items()})
for L, dx in ((6.0, 0.05), (6.0, 0.03), (6.0, 0.02), (4.0, 0.025), (8.0, 0.04)):
    t0=time.time(); r = solve(L=L, dx=dx)
    print(f"PRISM window1.2+kerf0.3 L={L} dx={dx}: case {r['case']:.3f} pkpk {r['pkpk']:.2f} pen {r['case']-o['core']:+.3f} ({(r['case']/o['core']-1)*100:+.1f} %) eclose {r['eclose']:.4f} mass {r['massclose']:.1e} [{time.time()-t0:.0f}s]", flush=True)
