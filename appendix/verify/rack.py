"""Rack manifold: N trays on dividing supply + combining return headers, U (same-end) or Z (opposite-end).
Static march: dividing p rises kd*rho/2*(u_up^2-u_dn^2) - friction; combining p falls kc*rho/2*(u_dn^2-u_up^2) + friction."""
import numpy as np, math
from scipy.optimize import brentq
rho, mu = 1005.0, 1.25e-3; LPM = 1/60000
def fD(u, D):
    Re = max(rho*abs(u)*D/mu, 1.0)
    return 64/Re if Re < 2300 else 0.25/math.log10(5.74/Re**0.9 + 1.5e-6/(3.7*D))**2
def headers(q, D, pitch, kd, kc, config):
    A = math.pi/4*D*D; n = len(q)
    ps = np.zeros(n); pr = np.zeros(n)
    F = q.sum(); p = 0.0
    for i in range(n):                       # supply fed at i=0
        ua = F/A; F -= q[i]; ub = F/A
        ps[i] = p + 0.5*kd*0.5*rho*(ua**2-ub**2)
        p += kd*0.5*rho*(ua**2-ub**2) - fD(ub, D)*pitch/D*0.5*rho*ub**2
    order = range(n) if config == 'U' else range(n-1, -1, -1)   # return exit at i=0 (U) or i=n-1 (Z)
    order = list(order); F = q.sum(); p = 0.0
    for i in order:                          # march from exit outward; static rises outward
        ua = F/A; F -= q[i]; ub = F/A
        pr[i] = p + 0.5*kc*0.5*rho*(ua**2-ub**2)
        p += kc*0.5*rho*(ua**2-ub**2) + fD(ub, D)*pitch/D*0.5*rho*ub**2
    return ps, pr
def solve(branches, D=0.063, pitch=0.089, kd=1.0, kc=2.0, config='U', Qtot=None, dP=None):
    """branches: list of (a [kPa/LPM^2], b [kPa/LPM]) per tray. Either fixed total flow (CDU flow-limited) or fixed header dP."""
    n = len(branches); a = np.array([x[0] for x in branches]); b = np.array([x[1] for x in branches])
    def qfrom(d):  # d kPa per branch -> LPM
        d = np.maximum(d, 1e-9); return np.where(a > 0, (-b + np.sqrt(b*b + 4*a*d))/(2*a + 1e-30), d/b)
    q = np.full(n, (Qtot or 18*n)/n)*LPM
    for it in range(500):
        ps, pr = headers(q, D, pitch, kd, kc, config)
        dev = (ps - pr)/1e3
        if Qtot is not None:
            C = brentq(lambda C: qfrom(C + dev).sum() - Qtot, -200, 2000)
        else:
            C = dP
        qn = qfrom(C + dev)*LPM
        if np.max(abs(qn - q))/q.mean() < 1e-10: break
        q = 0.5*q + 0.5*qn
    return q/LPM, C
def branch(kpa18, visc_frac):           # branch through 18 LPM with given viscous fraction
    return (kpa18*(1-visc_frac)/18**2, kpa18*visc_frac/18)
if __name__ == "__main__":
    print("=== Homogeneous rack, 18 trays x 18 LPM (324 LPM), max/min tray flow ===")
    print("| branch | 50 mm U | 50 mm Z | 63 mm U | 63 mm Z |")
    for lab, k, vf in (("PRISM dual UQD08 ~17 kPa", 17.0, 0.08), ("PRISM single UQD08 ~45 kPa", 45.0, 0.04),
                       ("PRISM dual + 10 kPa orifice ~27 kPa", 27.0, 0.05), ("CoolIT-like single UQD08 ~65 kPa", 65.0, 0.24)):
        row = []
        for D in (0.050, 0.063):
            for cfg in ('U', 'Z'):
                q, C = solve([branch(k, vf)]*18, D=D, config=cfg, Qtot=324.0)
                row.append(f"{q.max()/q.min():.3f}")
        print(f"| {lab} | " + " | ".join(row) + " |")
    print(f"63 mm header velocity at 324 LPM: {324*LPM/(math.pi/4*0.063**2):.2f} m/s; 50 mm: {324*LPM/(math.pi/4*0.05**2):.2f} m/s")
    print("\n=== Mixed rack: 9 CoolIT-like trays (65 kPa) + 9 PRISM trays, CDU flow-limited at 324 LPM, 63 mm U ===")
    for lab, k, vf in (("PRISM dual UQD08 17 kPa, no orifice", 17.0, 0.08), ("PRISM single UQD08 45 kPa, no orifice", 45.0, 0.04),
                       ("PRISM dual + keyed orifice to 65 kPa", 65.0, 0.02)):
        br = [branch(65.0, 0.24), branch(k, vf)]*9
        q, C = solve(br, Qtot=324.0)
        qc = q[0::2]; qp = q[1::2]
        print(f"  {lab}: incumbent trays {qc.mean():.1f} LPM ({qc.mean()/18-1:+.0%}), PRISM trays {qp.mean():.1f} LPM ({qp.mean()/18-1:+.0%}); header dP {C:.0f} kPa")
    print("\n=== Temperature drift: same mixed rack (PRISM single UQD08), PG25 viscosity at 25 C = 1.7x the 45 C value ===")
    for T, f in (("45 C", 1.0), ("25 C start-up", 1.7)):
        br = [(65*0.76/324, 65*0.24/18*f), (45*0.96/324, 45*0.04/18*f)]*9
        q, C = solve(br, Qtot=324.0); print(f"  {T}: incumbent {q[0::2].mean():.1f} LPM, PRISM {q[1::2].mean():.1f} LPM")
    print("\n=== Fixed-dP header (pump at fixed head), branch flow response to -20 % header dP ===")
    for lab, vf in (("82 % inertial plate alone", 0.18), ("CoolIT-like plate alone (68 % viscous)", 0.68)):
        a, b = 0.82 if vf == 0.18 else 0.32, vf
        f = lambda d: (-b + math.sqrt(b*b + 4*a*d))/(2*a)
        print(f"  {lab}: flow ratio at 0.8 x dP = {f(0.8)/f(1.0):.3f}")
