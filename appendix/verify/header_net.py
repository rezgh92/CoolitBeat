"""Slot-to-slot and segment-level distribution for PRISM-15 (line-lumped network).
Inlet header (192 mm2) mid-fed, outlet header (224 mm2) mid-collected; windows at 12 mm pitch.
Each inlet line: inlet window + meter (inertial) -> kerf node -> left/right fin segments (viscous) -> outlet plenums -> outlet window -> outlet header.
Key point tested: the meter fixes the LINE flow, but the LEFT/RIGHT split of each line is set only by the fin segment (0.67 kPa)
against the pressure difference between the two neighbouring outlet plenums."""
import numpy as np
from scipy.optimize import fsolve
rho = 1005.0; LPM = 1/60000
A_h_in, A_h_out = 192e-6, 224e-6
A_w = 4.5e-3*14e-3; K_wi, K_wo = 1.6, 1.6
A_port = np.pi/4*0.02**2
def build(layout):
    if layout == 18:   # I O I O ... O : inlets -51..45, outlets -45..51
        xin = -51 + 12*np.arange(9); xout = -45 + 12*np.arange(9)
    else:              # 19 lines O I O ... O : outlets -54..54 (10), inlets -48..48 (9)
        xin = -48 + 12*np.arange(9); xout = -54 + 12*np.arange(10)
    # connectivity: inlet k -> outlets at xin-6 and xin+6 if they exist
    segs = []
    for k, x in enumerate(xin):
        for xo in (x-6, x+6):
            j = np.where(np.isclose(xout, xo))[0]
            if len(j): segs.append((k, j[0]))
    return xin, xout, segs
def header_in(Q, ip, kd, s_jet, u_port):
    n = len(Q); P = np.zeros(n)
    P[ip] = s_jet*0.5*rho*u_port**2
    for side in (-1, +1):
        idx = list(range(ip+side, -1 if side < 0 else n, side))
        F = sum(Q[i] for i in idx); Pst = 0.0
        for i in idx:
            ua = F/A_h_in; F -= Q[i]; ub = F/A_h_in
            P[i] = Pst + 0.5*kd*0.5*rho*(ua**2-ub**2)
            Pst += kd*0.5*rho*(ua**2-ub**2) - 0.02*(12e-3/9.6e-3)*0.5*rho*ua**2
    return P
def header_out(Qo, ip, kc, s_out, u_port):
    n = len(Qo); P = np.zeros(n)
    P[ip] = -s_out*0.5*rho*u_port**2
    for side in (-1, +1):
        idx = list(range(ip+side, -1 if side < 0 else n, side))
        # march from the junction outward: going outward the header flow decreases; static RISES outward (falls toward port)
        F = sum(Qo[i] for i in idx); Pst = 0.0
        for i in idx:
            ua = F/A_h_out; F -= Qo[i]; ub = F/A_h_out
            P[i] = Pst + 0.5*kc*0.5*rho*(ua**2-ub**2)
            Pst += kc*0.5*rho*(ua**2-ub**2) + 0.02*(12e-3/10.8e-3)*0.5*rho*ua**2
    return P
def solve(lpm=18, layout=18, kd=1.0, kc=2.0, s_jet=0.0, s_out=0.0, meter_kPa=1.88, seg_kPa=0.67, ip_in=None, ip_out=None):
    xin, xout, segs = build(layout)
    nin, nout = len(xin), len(xout)
    Qt = lpm*LPM; Ql0 = Qt/9; qs0 = Qt/18             # nominal line flow, nominal segment flow (18 segments)
    a_m = meter_kPa*1e3/Ql0**2; a_wi = K_wi*0.5*rho/A_w**2; a_wo = K_wo*0.5*rho/A_w**2
    r_s = seg_kPa*1e3/qs0                             # viscous segment
    u_port = Qt/A_port
    ip_in = int(np.argmin(abs(xin-(-3 if layout == 18 else 0)))) if ip_in is None else ip_in
    ip_out = int(np.argmin(abs(xout-(3 if layout == 18 else 0)))) if ip_out is None else ip_out
    def unpack(z): return z[:nin], z[nin]
    def flows(z):
        N, C = unpack(z)
        # first guess line flows from the inlet side using current header estimate (fixed-point inside residual)
        Q = np.full(nin, Ql0)
        for _ in range(30):
            Phi = header_in(Q, ip_in, kd, s_jet, u_port) + C
            dp = np.maximum(Phi - N, 1.0)
            Q = np.sqrt(dp/(a_m + a_wi))
        return Q, Phi
    def resid(z):
        N, C = unpack(z)
        Q, Phi = flows(z)
        # outlet side: need outlet plenum pressures; iterate on segment flows
        qseg = np.array([Q[k]/sum(1 for kk, _ in segs if kk == k) for k, j in segs])
        for _ in range(60):
            Qo = np.zeros(nout)
            for (k, j), q in zip(segs, qseg): Qo[j] += q
            Pho = header_out(Qo, ip_out, kc, s_out, u_port)
            Ppo = Pho + a_wo*Qo**2
            qnew = np.array([(N[k] - Ppo[j])/r_s for k, j in segs])
            qseg = 0.5*qseg + 0.5*qnew
        res = np.zeros(nin+1)
        for k in range(nin):
            res[k] = (Q[k] - sum(q for (kk, j), q in zip(segs, qseg) if kk == k))/Ql0
        res[nin] = (Q.sum() - Qt)/Qt
        return res
    z0 = np.concatenate([np.full(nin, 0.9e3*(lpm/18)**2), [3.0e3*(lpm/18)**2]])
    z = fsolve(resid, z0, xtol=1e-12, maxfev=20000)
    N, C = unpack(z); Q, Phi = flows(z)
    qseg = np.array([Q[k]/sum(1 for kk, _ in segs if kk == k) for k, j in segs])
    for _ in range(200):
        Qo = np.zeros(nout)
        for (k, j), q in zip(segs, qseg): Qo[j] += q
        Pho = header_out(Qo, ip_out, kc, s_out, u_port); Ppo = Pho + a_wo*Qo**2
        qseg = 0.5*qseg + 0.5*np.array([(N[k] - Ppo[j])/r_s for k, j in segs])
    rl = Q/Ql0; rs = qseg/qs0
    return dict(line=rl, seg=rs, line_mm=rl.max()/rl.min(), seg_mm=rs.max()/rs.min(), seg_min=rs.min(), seg_max=rs.max(),
                res=np.max(abs(resid(z))), xin=xin, segs=segs)
if __name__ == "__main__":
    print("| layout | LPM | kd/kc | port jet s_in | s_out | line max/min | segment max/min | seg min | seg max | resid |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for layout in (18, 19):
        for lpm in (18, 36):
            for kd, kc, sj, so in ((1.0, 2.0, 0.0, 0.0), (0.6, 2.6, 0.0, 0.0), (1.0, 2.0, 1.0, 0.0), (1.0, 2.0, 1.0, 0.5), (1.0, 2.0, 0.0, -0.5)):
                r = solve(lpm, layout, kd, kc, sj, so)
                print(f"| {layout} lines | {lpm} | {kd}/{kc} | {sj} | {so} | {r['line_mm']:.3f} | {r['seg_mm']:.3f} | {r['seg_min']:.3f} | {r['seg_max']:.3f} | {r['res']:.1e} |")
    r = solve(18, 18); print("\n18-line nominal: line ratios", np.round(r['line'], 3)); print("segment ratios", np.round(r['seg'], 3))
    r = solve(18, 19); print("19-line nominal: line ratios", np.round(r['line'], 3)); print("segment ratios", np.round(r['seg'], 3))
    print("\nmeter strength at 18 LPM (19 lines, kd/kc 1/2, no jet): meter kPa -> line, segment max/min")
    for m in (0.6, 1.2, 1.88, 2.5):
        r = solve(18, 19, meter_kPa=m); print(f"  {m}: {r['line_mm']:.3f} {r['seg_mm']:.3f}")
