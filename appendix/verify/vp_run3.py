from vp_cell import solve, oneD
q=1.28e6; dT=12.66
o = oneD(q=q, dTout=dT, h=10.2e3, t=0.2, g=0.2, H=4.0, tb=2.0, linear=True)
r = solve(L=54.0, dx=0.1, dz=0.1, q=q, dTout=dT, win_in=2.5, win_out=1.0, kerf_in=0.0, kerf_out=1.0, w_kerf=0.2/0.2**0.5*0+0.2*(50*0.5)**0.5, t=0.2, g=0.2, H=4.0, tb=2.0, h=10.2e3, h_floor_kerf=10e3, Kkerf_ratio=50)
print(f"CoolIT with draft's top-window outlet repr: 2-D {r['case']:.2f} vs 1-D {o['core']:.2f} -> {r['case']-o['core']:+.2f} ({(r['case']/o['core']-1)*100:+.1f}%), pkpk {r['pkpk']:.1f}")
