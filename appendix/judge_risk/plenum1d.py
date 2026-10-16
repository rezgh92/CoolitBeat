import numpy as np
rho, mu = 1005.0, 1.25e-3
W, Hp = 3.0e-3, 9.0e-3; A = W*Hp; Dh = 2*A/(2*(W+Hp)); fRe = 69.0
Lp = 108e-3; n = 360; dy = Lp/n; y = (np.arange(n)+0.5)*dy - Lp/2
Q = 18.0/14/60000.0
q0 = Q/n                      # per y-cell (two 4 mm segments in parallel)
def run(y_in=-14e-3, y_out=+14e-3, dp0=2480.0, fvisc=0.11, th_i=1.0, th_o=2.0):
    R1 = fvisc*dp0/q0; R2 = (1-fvisc)*dp0/q0**2
    q = np.full(n, q0)
    i_in = np.argmin(abs(y-y_in)); i_out = np.argmin(abs(y-y_out))
    for it in range(500):
        # inlet plenum axial flow (positive = +y) at cell faces, fed at i_in
        cum = np.cumsum(q)
        F_in = np.zeros(n+1)   # flow across face j (between cell j-1 and j), +y direction
        for j in range(n+1):
            if j <= i_in: F_in[j] = -cum[j-1] if j>0 else 0.0  # flows toward -y from window
            else: F_in[j] = Q - cum[j-1]
        # outlet plenum: collects q, drains at i_out; flow toward window
        F_out = np.zeros(n+1)
        for j in range(n+1):
            if j <= i_out: F_out[j] = cum[j-1] if j>0 else 0.0   # +y toward window
            else: F_out[j] = -(Q - cum[j-1])                    # -y toward window
        u_in = F_in/A; u_out = F_out/A
        # pressure: march from window cell outwards. dp/dy = -f/Dh*rho*u|u|/2 - th*rho*d(u^2)/dy/2*2? use momentum form
        def march(u, i0, th):
            p = np.zeros(n); p[i0] = 0.0
            for j in range(i0+1, n):   # +y side, face j between j-1 and j
                uf = u[j]; ua = u[j-1] if j-1>=0 else uf; ub = u[j+1]
                fr = fRe*mu/(Dh**2)*2*uf  # Darcy laminar: dp/dy = fD/Dh*rho u^2/2 = (fRe_D mu/(2 Dh^2))... use fRe_D=4*fRe_F? fRe here Darcy-ish
                fr = (fRe*mu/(2*Dh**2))*uf
                mom = th*rho*(ub**2 - ua**2)/2.0/ (2*dy) * dy
                p[j] = p[j-1] - fr*dy - th*rho*(u[j+1]**2-u[j]**2)/2.0
            for j in range(i0-1, -1, -1):
                uf = u[j+1]
                fr = (fRe*mu/(2*Dh**2))*uf
                p[j] = p[j+1] + fr*dy + th*rho*(u[j+1]**2-u[j]**2)/2.0
            return p
        p_in = march(u_in, i_in, th_i)
        p_out = march(u_out, i_out, th_o)
        # choose offset P so that sum q = Q
        def qs(P):
            dp = P + p_in - p_out
            dp = np.maximum(dp, 1e-6)
            return (-R1 + np.sqrt(R1**2 + 4*R2*dp))/(2*R2)
        lo, hi = 0.0, 20000.0
        for _ in range(80):
            mid = 0.5*(lo+hi)
            if qs(mid).sum() > Q: hi = mid
            else: lo = mid
        qn = qs(0.5*(lo+hi))
        if np.max(abs(qn-q))/q0 < 1e-8: break
        q = 0.7*q + 0.3*qn
    r = q/q0
    return r.max()/r.min(), r.max(), r.min(), 0.5*(lo+hi)
for lab, yi, yo in (("proposal offset -14/+14", -14e-3, 14e-3), ("true centre-fed CC 0/0", 0.0, 0.0), ("Z end-fed", -53e-3, 53e-3), ("U end-fed", -53e-3, -53e-3)):
    for th_i, th_o in ((1.0, 2.0), (0.6, 1.5)):
        mm, mx, mn, P = run(yi, yo, th_i=th_i, th_o=th_o)
        print(f"{lab:26s} theta_i {th_i} theta_o {th_o}: along-plenum max/min {mm:.3f} (max {mx:.3f}, min {mn:.3f}), branch-plus-plenum dp {P:.0f} Pa")
