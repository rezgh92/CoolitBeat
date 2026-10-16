"""Segment-level flow balance for the Rev A (PKG-A) line layout: 15 lines at 7.7 mm (7 inlets, 8 outlets incl. edge outlets),
mid-fed arched headers (161 mm2 per header half each side), graded inlet meter 2.3 kPa per line, fin segment 1.07 kPa (viscous),
optional outlet-side orifice row in the metered grate. Same network method as verify/header_net2-4.py (hydraulics verifier)."""
import numpy as np
from scipy.optimize import fsolve
rho = 1005.0; LPM = 1/60000
PITCH = 7.7e-3
xin = (-46.2 + 15.4*np.arange(7))*1e-3; xout = (-53.9 + 15.4*np.arange(8))*1e-3
segs = []
for k, x in enumerate(xin):
    for xo in (x - PITCH, x + PITCH):
        j = np.where(np.isclose(xout, xo))[0]
        if len(j): segs.append((k, j[0]))
NSEG = len(segs)
def hdr(Q, ip, A, k, sign, s_jet, u_port):
    n = len(Q); P = np.zeros(n); P[ip] = sign*s_jet*0.5*rho*u_port**2
    for side in (-1, 1):
        idx = list(range(ip+side, -1 if side < 0 else n, side)); F = sum(Q[i] for i in idx); Pst = 0.0
        for i in idx:
            ua = F/A; F -= Q[i]; ub = F/A
            P[i] = Pst + 0.5*k*0.5*rho*(ua**2-ub**2)
            Pst += k*0.5*rho*(ua**2-ub**2) + sign*(-1)*0.02*(15.4e-3/9e-3)*0.5*rho*ua**2
    return P
def hdr_out(Qo, ip, A, kc):
    n = len(Qo); P = np.zeros(n)
    for side in (-1, 1):
        idx = list(range(ip+side, -1 if side < 0 else n, side)); F = sum(Qo[i] for i in idx); Pst = 0.0
        for i in idx:
            ua = F/A; F -= Qo[i]; ub = F/A
            P[i] = Pst + 0.5*kc*0.5*rho*(ua**2-ub**2)
            Pst += kc*0.5*rho*(ua**2-ub**2) + 0.02*(15.4e-3/9e-3)*0.5*rho*ua**2
    return P
def run(lpm=18, A_out_scale=1.0, out_meter=0.0, meter=2.3, seg=1.07, s_jet=0.0, kd=1.0, kc=2.0, edge_half=True, A_w=6.9e-3*14e-3):
    nin, nout = len(xin), len(xout); Qt = lpm*LPM; s = lpm/18; Ql0 = Qt/nin; qs0 = Qt/NSEG
    A_hi = 161e-6; A_ho = 161e-6*A_out_scale; u_port = Qt/(np.pi/4*0.02**2)
    a_m = meter*1e3/(18*LPM/nin)**2; a_wi = 1.6*0.5*rho/A_w**2
    Aw = np.full(nout, A_w)
    if edge_half: Aw[0] = Aw[-1] = A_w/2
    a_wo = 1.6*0.5*rho/Aw**2; r_s = seg*1e3/(18*LPM/NSEG); a_om = out_meter*1e3/(18*LPM/NSEG)**2
    ip_in = 3; ip_out = 4   # inlet port over the centre inlet window; outlet port between windows
    def segflow(dp):
        if a_om == 0: return dp/r_s
        return np.sign(dp)*(-r_s+np.sqrt(r_s**2+4*a_om*abs(dp)))/(2*a_om)
    def state(z):
        N = z[:nin]; P = z[nin:nin+nout]; C = z[-1]
        q = np.array([segflow(N[k]-P[j]) for k, j in segs]); Q = np.zeros(nin); Qo = np.zeros(nout)
        for (k, j), qq in zip(segs, q): Q[k] += qq; Qo[j] += qq
        return N, P, C, q, Q, Qo
    def res(z):
        N, P, C, q, Q, Qo = state(z)
        Phi = hdr(Q, ip_in, A_hi, kd, +1, s_jet, u_port) + C
        Pho = hdr_out(Qo, ip_out, A_ho, kc)  # combining header: static rises outward from the port (as verify/header_net.header_out)
        return np.concatenate([(Phi-N-(a_m+a_wi)*Q*abs(Q))/(1e3*s*s), (P-Pho-a_wo*Qo*abs(Qo))/(1e3*s*s), [(Q.sum()-Qt)/Qt]])
    z0 = np.concatenate([np.full(nin, seg*1e3*s), np.zeros(nout), [(meter+0.3)*1e3*s*s+seg*1e3*s]])
    z, info, ier, msg = fsolve(res, z0, full_output=True, xtol=1e-13, maxfev=50000)
    N, P, C, q, Q, Qo = state(z); rs = q/qs0; rl = Q/Ql0
    return rl.max()/rl.min(), rs.max()/rs.min(), rs.min(), ier == 1
print(f"Rev A layout: {len(xin)} inlet lines, {len(xout)} outlet lines, {NSEG} segments per fin gap ({NSEG*360} in the field)")
for lab, kw in (("PKG-A as closed (open outlet windows, port jet diffused)", {}),
                ("PKG-A, port jet undiffused", dict(s_jet=1.0)),
                ("+ outlet-side orifice row 0.5 kPa", dict(out_meter=0.5)),
                ("+ outlet-side orifice row 0.5 kPa, port jet undiffused", dict(out_meter=0.5, s_jet=1.0)),
                ("+ outlet header area x2 (no orifice)", dict(A_out_scale=2.0)),
                ("+ outlet orifice 1.0 kPa", dict(out_meter=1.0))):
    for lpm in (18, 36):
        r = run(lpm, **kw); print(f"- {lab}, {lpm} LPM: line max/min {r[0]:.3f}, segment max/min {r[1]:.3f} (min {r[2]:.3f}), converged {r[3]}")
print("Combined fixes:")
for lab, kw in (("outlet header x2 + outlet orifice 0.5 kPa", dict(A_out_scale=2.0, out_meter=0.5)),
                ("outlet header x2 + outlet orifice 0.5 kPa, port jet undiffused", dict(A_out_scale=2.0, out_meter=0.5, s_jet=1.0)),
                ("outlet header x2, port jet undiffused", dict(A_out_scale=2.0, s_jet=1.0))):
    for lpm in (9, 18, 36):
        r = run(lpm, **kw); print(f"- {lab}, {lpm} LPM: line max/min {r[0]:.3f}, segment max/min {r[1]:.3f} (min {r[2]:.3f}), converged {r[3]}")
