"""DDD-grate: outlet-orifice-row sizing check.
final_segbal.py placed the 0.5 kPa outlet orifice PER SEGMENT (between the kerf node of each inlet line and the outlet
plenum). Physically the row sits in the grate web over the outlet window, where the left and right segments have already
merged in the kerf, so it is one lumped element per OUTLET LINE carrying the sum of both segments. This script re-runs
the Rev A network (same method, geometry and K values as final_segbal.py: 15 lines at 7.7 mm, mid-fed arched headers,
inlet meter 2.3 kPa, fin segment 1.07 kPa viscous, outlet header x2, half-area edge windows) with the row lumped per line,
and sizes it: dp_row = 0.5 kPa at the line's nominal 18 LPM flow (2.571 LPM interior, 1.286 LPM edge with half the holes)."""
import numpy as np
from scipy.optimize import fsolve
rho = 1005.0; LPM = 1/60000; PITCH = 108/14*1e-3
xin = (-54 + 108/14*(1 + 2*np.arange(7)))*1e-3; xout = (-54 + 108/14*(2*np.arange(8)))*1e-3
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
def run(lpm=18, A_out_scale=2.0, row_kpa=0.5, row_mode="line", meter=2.3, seg=1.07, s_jet=0.0, kd=1.0, kc=2.0,
        edge_half=True, A_w=6.9e-3*14e-3, edge_row_half=True):
    nin, nout = len(xin), len(xout); Qt = lpm*LPM; s = lpm/18; Ql0 = Qt/nin; qs0 = Qt/NSEG
    A_hi = 161e-6; A_ho = 161e-6*A_out_scale; u_port = Qt/(np.pi/4*0.02**2)
    a_m = meter*1e3/(18*LPM/nin)**2; a_wi = 1.6*0.5*rho/A_w**2
    Aw = np.full(nout, A_w)
    if edge_half: Aw[0] = Aw[-1] = A_w/2
    a_wo = 1.6*0.5*rho/Aw**2; r_s = seg*1e3/(18*LPM/NSEG)
    # outlet row: per-segment (final_segbal convention) or lumped per outlet line (physical)
    a_om = row_kpa*1e3/(18*LPM/NSEG)**2 if row_mode == "segment" else 0.0
    nsegs_per_out = np.array([sum(1 for k, j in segs if j == jj) for jj in range(nout)])   # 1 at edges, 2 interior
    Qo_nom = qs0*nsegs_per_out
    if row_mode == "line":
        # row area per line scaled by hole count: interior 54 holes, edge 27 (edge_row_half) or 54
        n_holes = np.where(nsegs_per_out == 2, 54, 27 if edge_row_half else 54)
        A_row_int = None
        a_row = row_kpa*1e3/(18*LPM/NSEG*2)**2 * (54/n_holes)**2     # dp = a_row Qo^2 ; interior gives 0.5 kPa at 2.571 LPM
    else:
        a_row = np.zeros(nout)
    ip_in = 3; ip_out = 4
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
        Pho = hdr_out(Qo, ip_out, A_ho, kc)
        return np.concatenate([(Phi-N-(a_m+a_wi)*Q*abs(Q))/(1e3*s*s), (P-Pho-(a_wo+a_row)*Qo*abs(Qo))/(1e3*s*s), [(Q.sum()-Qt)/Qt]])
    z0 = np.concatenate([np.full(nin, seg*1e3*s), np.zeros(nout), [(meter+0.3)*1e3*s*s+seg*1e3*s]])
    z, info, ier, msg = fsolve(res, z0, full_output=True, xtol=1e-13, maxfev=50000)
    N, P, C, q, Q, Qo = state(z); rs = q/qs0; rl = Q/Ql0
    dp_row = a_row*Qo**2/1e3 if row_mode == "line" else np.full(nout, np.nan)
    return dict(line=rl.max()/rl.min(), seg=rs.max()/rs.min(), segmin=rs.min(), ok=ier == 1, dp_row=dp_row, Qo=Qo/LPM)
print(f"Rev A layout: {len(xin)} inlet, {len(xout)} outlet lines, {NSEG} segments per gap; pitch {PITCH*1e3:.4f} mm")
print("\n| case | LPM | line max/min | segment max/min | segment min | row dp interior / edge (kPa) |")
print("|---|---|---|---|---|---|")
cases = (("final_segbal convention: row 0.5 kPa PER SEGMENT, header x2", dict(row_mode="segment", row_kpa=0.5)),
         ("no outlet row, header x2", dict(row_mode="line", row_kpa=0.0)),
         ("LUMPED row 0.5 kPa per line (54 / 27 holes), header x2  <- design", dict(row_mode="line", row_kpa=0.5)),
         ("LUMPED row 0.5 kPa per line, edge rows 54 holes (0.125 kPa at edge)", dict(row_mode="line", row_kpa=0.5, edge_row_half=False)),
         ("LUMPED row 0.75 kPa per line, header x2", dict(row_mode="line", row_kpa=0.75)),
         ("LUMPED row 1.0 kPa per line, header x2 (R2 fallback artwork)", dict(row_mode="line", row_kpa=1.0)),
         ("LUMPED row 0.5 kPa, header x2, port jet undiffused", dict(row_mode="line", row_kpa=0.5, s_jet=1.0)),
         ("LUMPED row 0.5 kPa, header x1 (outlet header not doubled)", dict(row_mode="line", row_kpa=0.5, A_out_scale=1.0)))
for lab, kw in cases:
    for lpm in (9, 18, 27, 36):
        r = run(lpm, **kw)
        dpr = f"{r['dp_row'][4]:.2f} / {r['dp_row'][0]:.2f}" if not np.isnan(r['dp_row'][0]) else "-"
        print(f"| {lab} | {lpm} | {r['line']:.3f} | {r['seg']:.3f} | {r['segmin']:.3f} | {dpr} |")
r = run(18, row_mode="line", row_kpa=0.5)
print("\nOutlet-line flows at 18 LPM (LPM), edge to edge:", np.round(r['Qo'], 3))
