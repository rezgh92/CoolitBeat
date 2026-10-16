"""Independent along-plenum (L2) model for PRISM-15 actual geometry.
Inlet plenum 4.5 x 9 mm x 108 mm, fed through a 14 mm window centred at y_in; outlet plenum same, drained at y_out.
54 orifice branches at 2 mm pitch; branch dp = a q^2 + b q, with dp(q0) = dp0, inertial fraction fi.
Dividing: static rises kd*rho/2*(u_up^2-u_dn^2) minus friction; combining: static falls kc*rho/2*(...) plus friction.
Feed/drain distributed uniformly over the window span (or point). Optional jet stagnation bonus under the inlet window."""
import numpy as np
rho, mu = 1005.0, 1.25e-3
LPM = 1/60000
W, Hp, L, n = 4.5e-3, 9e-3, 108e-3, 54
A = W*Hp; Dh = 2*A/(2*(W+Hp)); dy = L/n
y = (np.arange(n)+0.5)*dy - L/2
def fric_grad(u):
    Re = rho*abs(u)*Dh/mu + 1e-9
    f = np.where(Re < 2300, 62.2/Re, 0.316*Re**-0.25)   # Darcy; 62.2 laminar for aspect 0.5
    return f/Dh*0.5*rho*u*np.abs(u)
def axial(q, ysrc, win, sign):
    """axial flow at cell faces (n+1) for a plenum with source(+)/sink distributed over window; q branch outflows (+ for inlet)"""
    Qt = q.sum()
    src = np.zeros(n)
    if win > 0:
        m = np.abs(y-ysrc) <= win/2 + 1e-12; src[m] = Qt/m.sum()
    else:
        src[np.argmin(abs(y-ysrc))] = Qt
    # face flow F[j] = flow crossing face j (between cell j-1 and j) in +y direction; F[0]=F[n]=0
    F = np.zeros(n+1); F[1:] = np.cumsum(src - q)
    return F
def pressures(F, k, kind):
    """march static pressure cell-to-cell; F face flows (+y). kind 'div' or 'comb'"""
    u_face = F/A
    uc = 0.5*(u_face[:-1]+u_face[1:])           # cell-centre axial velocity
    p = np.zeros(n)
    for j in range(1, n):
        uf = u_face[j]                          # face between j-1 and j
        fr = fric_grad(np.array([uf]))[0]*dy    # pressure drop in +y direction if uf>0
        du2 = uc[j]**2 - uc[j-1]**2
        if kind == 'div':   # static change = -kd*rho/2*du2 (rise when speed falls)
            p[j] = p[j-1] - fr - k*rho/2*du2
        else:               # combining: static falls by kc*rho/2 when speed rises along flow
            p[j] = p[j-1] - fr - k*rho/2*du2
    return p
def solve(Qpl=2*LPM, dp0=2550., fi=0.737, kd=1.0, kc=2.0, y_in=-14e-3, y_out=14e-3, win=14e-3, jet=0.0):
    q0 = Qpl/n; a = fi*dp0/q0**2; b = (1-fi)*dp0/q0
    q = np.full(n, q0)
    for it in range(3000):
        Fi = axial(q, y_in, win, +1); Fo = axial(-q, y_out, win, -1)   # outlet: branches are sources, window sink
        pi_ = pressures(Fi, kd, 'div'); po_ = pressures(Fo, kc, 'comb')
        if jet > 0:   # stagnation bonus under inlet window: fraction 'jet' of window dynamic head
            usw = Qpl/(W*win); m = np.abs(y-y_in) <= win/2; bonus = np.zeros(n); bonus[m] = jet*0.5*rho*usw**2
            pi_ = pi_ + bonus
        d = pi_ - po_
        def qs(C):
            dp = np.maximum(C + d, 1e-6); return (-b + np.sqrt(b*b + 4*a*dp))/(2*a)
        lo, hi = -2e4, 4e4
        for _ in range(100):
            mid = 0.5*(lo+hi)
            if qs(mid).sum() > Qpl: hi = mid
            else: lo = mid
        qn = qs(0.5*(lo+hi))
        if np.max(abs(qn-q))/q0 < 1e-10: break
        q = 0.6*q + 0.4*qn
    r = q/q0
    return r.max()/r.min(), r.min(), r.max(), it
if __name__ == "__main__":
    print("| case | LPM | branch dp0 Pa | fi | kd/kc | max/min | min | max |")
    print("|---|---|---|---|---|---|---|---|")
    for lab, yi, yo, win, jet in (("offset +/-14 mm, 14 mm window", -14e-3, 14e-3, 14e-3, 0.0),
                                  ("offset +/-14 mm, point feed", -14e-3, 14e-3, 0.0, 0.0),
                                  ("offset +/-14, window + full jet stagnation", -14e-3, 14e-3, 14e-3, 1.0),
                                  ("centre fed and drained (y=0 both)", 0.0, 0.0, 14e-3, 0.0)):
        for lpm in (15, 18, 27, 36):
            s = lpm/18; Qpl = lpm/9*LPM
            inert = 1.88*s*s; visc = 0.67*s; dp0 = (inert+visc)*1e3; fi = inert/(inert+visc)
            for kd, kc in ((1.0, 2.0), (0.6, 1.5), (1.3, 2.6), (2.0, 2.0)):
                if lpm not in (18, 36) and (kd, kc) != (1.0, 2.0): continue
                mm, mn, mx, it = solve(Qpl, dp0, fi, kd, kc, yi, yo, win, jet)
                print(f"| {lab} | {lpm} | {dp0:.0f} | {fi:.2f} | {kd}/{kc} | {mm:.3f} | {mn:.3f} | {mx:.3f} |")
    # sensitivity: weaker meter (draft lesson 0.9 kPa branch) on the PRISM plenum
    print("\nmeter-strength sensitivity at 18 LPM, offset feed, kd/kc 1/2:")
    for dp0, fi in ((900, 0.3), (1500, 0.55), (2550, 0.737), (3300, 0.8)):
        print(f"  branch {dp0} Pa: max/min {solve(2*LPM, dp0, fi)[0]:.3f}")
    # draft's plenum_prism parameters replicated in my solver (3x7 mm, 18/14 LPM, 900 Pa, fv 0.5)
