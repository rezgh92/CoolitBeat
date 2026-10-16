from vp_cell import solve, oneD
for q, dT, lab in ((3.5e6, 12.9, "350 W/cm2"), (2.0e6, 12.7, "200 W/cm2"), (1.282e6, 12.66, "128 W/cm2")):
    o = oneD(q=q, dTout=dT, h=14.0e3)
    s = []
    for L in (4.0, 5.0, 6.0, 8.0):
        r = solve(L=L, dx=0.025 if L <= 5 else 0.04, dz=0.025, q=q, dTout=dT, h=14.0e3)
        s.append(f"L{L:.0f}: avg {r['case']:.2f} crest {r['case']+r['pkpk']/2:.2f}")
    print(lab, "| 1-D", round(o['core'],2), "|", "; ".join(s), flush=True)
