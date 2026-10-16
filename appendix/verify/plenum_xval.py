import plenum_check as pc, numpy as np
LPM=1/60000
for (W,Hp) in ((3e-3,7e-3),(3e-3,9e-3),(4.5e-3,9e-3)):
    pc.W, pc.Hp = W, Hp; pc.A = W*Hp; pc.Dh = 2*pc.A/(2*(W+Hp))
    for yi,yo,win,lab in ((-14e-3,14e-3,0.0,'offset point'),(0,0,0.0,'centre point')):
        r = pc.solve(18/14*LPM, 900., 0.5, 1.0, 2.0, yi, yo, win)
        print(f"{W*1e3:.1f}x{Hp*1e3:.0f} mm, 18/14 LPM, 900 Pa, fv .5, {lab}: max/min {r[0]:.3f}")
    r = pc.solve(2*LPM, 900., 0.3, 1.0, 2.0, -14e-3, 14e-3, 0.0); print(f"   same plenum at 2 LPM / 900 Pa branch, offset point: {r[0]:.3f}")
