"""Robust version: unknowns N_k (kerf node per inlet line), Ppo_j (outlet plenum), C (inlet-port static offset)."""
import numpy as np
from scipy.optimize import fsolve
from header_net import build, header_in, header_out, rho, LPM, A_h_in, A_h_out, A_w, A_port
def solve(lpm=18, layout=19, kd=1.0, kc=2.0, s_jet=0.0, s_out=0.0, meter_kPa=1.88, seg_kPa=0.67, K_wi=1.6, K_wo=1.6,
          out_meter_kPa=0.0, A_out_scale=1.0):
    xin, xout, segs = build(layout); nin, nout = len(xin), len(xout)
    Qt = lpm*LPM; s = lpm/18; Ql0 = Qt/9; qs0 = Qt/18
    a_m = meter_kPa*1e3/(18*LPM/9)**2; a_wi = K_wi*0.5*rho/A_w**2; a_wo = K_wo*0.5*rho/A_w**2
    a_om = out_meter_kPa*1e3/(18*LPM/18)**2         # optional outlet-side orifice per segment (inertial)
    r_s = seg_kPa*1e3/(18*LPM/18)                   # viscous segment resistance (fixed geometry)
    u_port = Qt/A_port
    ip_in = int(np.argmin(abs(xin-(-3 if layout == 18 else 0)))); ip_out = int(np.argmin(abs(xout-(3 if layout == 18 else 0))))
    import header_net as hn
    hn.A_h_out = A_h_out*A_out_scale
    def segflow(dp):
        # dp = r_s q + a_om q^2
        dp = np.maximum(dp, -1e9)
        if a_om == 0: return dp/r_s
        sgn = np.sign(dp); d = abs(dp); return sgn*(-r_s + np.sqrt(r_s**2 + 4*a_om*d))/(2*a_om)
    def state(z):
        N = z[:nin]; Ppo = z[nin:nin+nout]; C = z[-1]
        q = np.array([segflow(N[k]-Ppo[j]) for k, j in segs])
        Q = np.zeros(nin); Qo = np.zeros(nout)
        for (k, j), qq in zip(segs, q): Q[k] += qq; Qo[j] += qq
        return N, Ppo, C, q, Q, Qo
    def resid(z):
        N, Ppo, C, q, Q, Qo = state(z)
        Phi = header_in(Q, ip_in, kd, s_jet, u_port) + C
        Pho = hn.header_out(Qo, ip_out, kc, s_out, u_port)
        r1 = (Phi - N - (a_m + a_wi)*Q*np.abs(Q))/(1e3*s*s)
        r2 = (Ppo - Pho - a_wo*Qo*np.abs(Qo))/(1e3*s*s)
        r3 = [(Q.sum()-Qt)/Qt]
        return np.concatenate([r1, r2, r3])
    z0 = np.concatenate([np.full(nin, seg_kPa*1e3*s), np.zeros(nout), [(meter_kPa+0.3)*1e3*s*s + seg_kPa*1e3*s]])
    z, info, ier, msg = fsolve(resid, z0, full_output=True, xtol=1e-13, maxfev=50000)
    N, Ppo, C, q, Q, Qo = state(z)
    rl = Q/Ql0; rs = q/qs0
    return dict(line_mm=rl.max()/rl.min(), seg_mm=rs.max()/rs.min(), seg_min=rs.min(), seg_max=rs.max(), ok=ier == 1,
                res=np.max(abs(resid(z))), line=rl, seg=rs, dPo=Ppo.max()-Ppo.min())
if __name__ == "__main__":
    print("| layout | LPM | kd/kc | jet s_in | s_out | line max/min | segment max/min | seg min/max | outlet-plenum spread Pa | ok |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for layout in (19, 18):
        for lpm in (15, 18, 27, 36):
            for kd, kc, sj, so in ((1.0, 2.0, 0.0, 0.0), (0.6, 2.6, 0.0, 0.0), (1.3, 1.5, 0.0, 0.0), (1.0, 2.0, 1.0, 0.0), (1.0, 2.0, 1.0, 0.5)):
                if layout == 18 and (kd, kc, sj, so) != (1.0, 2.0, 0.0, 0.0): continue
                if lpm in (15, 27) and (kd, kc, sj, so) != (1.0, 2.0, 0.0, 0.0): continue
                r = solve(lpm, layout, kd, kc, sj, so)
                print(f"| {layout} | {lpm} | {kd}/{kc} | {sj} | {so} | {r['line_mm']:.3f} | {r['seg_mm']:.3f} | {r['seg_min']:.3f}/{r['seg_max']:.3f} | {r['dPo']:.0f} | {r['ok']} |")
    print("\nFixes at 18 LPM (19 lines, kd/kc 1/2, jet 1.0 at inlet port unless diffused):")
    for lab, kw in (("baseline (open outlet slots)", {}), ("guard cylinder diffuses port jet (s_in 0)", dict(s_jet=0.0)),
                    ("outlet header area x2", dict(A_out_scale=2.0)), ("outlet-side orifice row 0.5 kPa per segment", dict(out_meter_kPa=0.5)),
                    ("outlet-side orifice row 1.0 kPa", dict(out_meter_kPa=1.0)), ("meter 1.2 kPa + outlet orifices 0.6 kPa", dict(meter_kPa=1.2, out_meter_kPa=0.6))):
        args = dict(s_jet=1.0); args.update(kw)
        r = solve(18, 19, **args)
        print(f"  {lab}: line {r['line_mm']:.3f}, segment {r['seg_mm']:.3f} (min {r['seg_min']:.3f}), ok {r['ok']}")
    r = solve(18, 19); print("\n19-line nominal segment ratios:", np.round(r['seg'], 3))
