"""DDD-plenum: folded 0.8 mm OFE plenum (layer 3) and 1.5 mm separator (layer 4), PRISM-15 Rev A.
1 geometry, flat pattern, mass | 2 hydraulics: multi-window 1-D plenum solver (physics of ctl/plenum_graded.py and
design/grate_artwork.py) run with the as-drawn TTV artwork, window velocities/dp, bleed bypass, final_segbal network
with the as-designed window areas | 3 structure: wall tension, separator under the cap-land band loads (Fourier x FD
Kirchhoff strip), joint peel, hot-fixture bend stress, 316L option | 4 cost. Output: plenum_sep.out.
Conventions: X along fins (across lines), Y along lines, Z up from the die face (cad/prism_cad.py, DDD-grate)."""
import csv, json, math, os
import numpy as np
from scipy.optimize import fsolve
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = []
def pr(*a): s = " ".join(str(x) for x in a); OUT.append(s); print(s, flush=True)
rho, mu = 1005.0, 1.25e-3; LPM = 1 / 60000; RHO_CU, RHO_SS = 8.94e-3, 7.95e-3
# ======================= 1. GEOMETRY AND FLAT PATTERN =======================
FIELD, NL = 108.0, 15; P = FIELD / 14; XL = [-54.0 + P * k for k in range(NL)]
T, RI, KF, H, ZG = 0.80, 0.60, 0.35, 5.80, 4.50          # sheet, inside bend radius, K-factor, height, grate top z
RO = RI + T; W_CH = P - T; FLAT = P + T - 2 * RO; WALL = H - 2 * RO; BA = math.pi / 2 * (RI + KF * T)
FLANGE, L_CH, TAB, FR_T, FR_H = 1.50, 114.0, 1.0, 2.5, 5.78
XW = [-54.0 - P / 2 + P * j for j in range(16)]            # wall centrelines
Y_WIN_IN, Y_WIN_OUT = [-21.0, -7.0], [9.0, 23.0, 37.0, 51.0]
WIN_X, WIN_Y, WIN_R = 5.0, 10.0, 1.0; SLOT_W, SLOT_L, SLOT_R = 1.80, 110.0, 0.9; BLEED_D, Y_BLEED, Z_BLEED = 1.10, 55.5, 7.40
pr("## 1. Geometry (mm)")
pr(f"pitch {P:.4f}; inside channel width {W_CH:.3f}; flat between tangents {FLAT:.3f}; straight wall {WALL:.2f} (z {ZG + RO:.2f}-{ZG + H - RO:.2f});"
   f" Ri {RI} Ro {RO}; bend allowance (90 deg, K {KF}) {BA:.3f}")
pr(f"inlet channel z {ZG:.2f}-{ZG + H - T:.2f} (floor = grate web), outlet channel z {ZG + T:.2f}-{ZG + H:.2f} (ceiling = separator): both {H - T:.2f} tall")
pr(f"wall faces at |x - x_line| {P / 2 - T / 2:.3f}..{P / 2 + T / 2:.3f}; bottom-flat contact on the grate |x - x_out| <= {P / 2 + T / 2 - RO:.3f};"
   f" bonded strip per side of the {SLOT_W} slot: {P / 2 + T / 2 - RO - SLOT_W / 2 - 0.30:.3f} (0.30 mask)")
pr(f"top-flat contact under the separator |x - x_in| <= {P / 2 + T / 2 - RO:.3f} ({FLAT:.3f} wide); outer walls at x = +/-{abs(XW[0]):.3f}; flange free edge x = +/-{abs(XW[0]) + T / 2 + FLANGE + (RO - T):.3f}")
# developed pattern: s from the -x flange free edge
segs = [("flange-", FLANGE)]
for j in range(16):
    segs += [("bend", BA), (f"wall{j}", WALL), ("bend", BA)]
    segs.append(("flange+", FLANGE) if j == 15 else ((f"bflat{j}", FLAT) if j % 2 == 0 else (f"tflat{j}", FLAT)))
s0 = {}; s = 0.0; folds = []
for name, L in segs:
    s0[name if name != "bend" else f"bend@{s:.3f}"] = s
    if name == "bend": folds.append((round(s, 3), round(s + BA, 3)))
    s += L
DEV = s
pr(f"developed width {DEV:.2f} x blank length {L_CH + 2 * TAB:.1f} (flats/bends y +/-{L_CH / 2}; wall tabs to y +/-{L_CH / 2 + TAB})")
flat_cent = {k: s0[k] + FLAT / 2 for k in s0 if k.startswith(("bflat", "tflat"))}
wall_cent = {k: s0[k] + WALL / 2 for k in s0 if k.startswith("wall")}
pr("fold lines (tangent pairs, s): " + ", ".join(f"{a}-{b}" for a, b in folds))
pr("flat centres (s): " + ", ".join(f"{k} {v:.3f}" for k, v in flat_cent.items()))
feat = {"top_flat_windows": [], "bottom_flat_slots": [], "bleed_holes": [], "tabs": []}
for k, sc in flat_cent.items():
    j = int(k[5:])
    if k.startswith("tflat"):
        for y in Y_WIN_IN: feat["top_flat_windows"].append(dict(flat=k, line_x=round(XL[j], 4), s=round(sc, 3), y=y, w=WIN_X, h=WIN_Y, r=WIN_R))
    else: feat["bottom_flat_slots"].append(dict(flat=k, line_x=round(XL[j], 4), s=round(sc, 3), y=0.0, w=SLOT_W, l=SLOT_L, r=SLOT_R))
for k, sc in wall_cent.items():
    j = int(k[4:])
    if 1 <= j <= 14: feat["bleed_holes"].append(dict(wall=k, wall_x=round(XW[j], 4), s=round(sc, 3), y=(Y_BLEED if j % 2 == 0 else -Y_BLEED), d=BLEED_D, z=Z_BLEED))
    feat["tabs"] += [dict(wall=k, s_from=round(s0[k], 3), s_to=round(s0[k] + WALL, 3), y_from=L_CH / 2, y_to=L_CH / 2 + TAB), dict(wall=k, s_from=round(s0[k], 3), s_to=round(s0[k] + WALL, 3), y_from=-L_CH / 2 - TAB, y_to=-L_CH / 2)]
A_rr = lambda w, h, r: w * h - (4 - math.pi) * r * r
area = DEV * L_CH + 32 * WALL * TAB - 14 * A_rr(WIN_X, WIN_Y, WIN_R) - 8 * A_rr(SLOT_W, SLOT_L, SLOT_R) - 14 * math.pi / 4 * BLEED_D**2 - math.pi / 4 * 2.0**2
m_corr = area * T * RHO_CU; FR_L = 2 * (abs(XW[0]) + T / 2 + FLANGE + RO - T)
m_frame = (FR_T * FR_H * FR_L - 16 * 0.9 * 1.0 * FR_H) * RHO_CU
pr(f"mass: corrugation {m_corr:.1f} g (sheet {area:.0f} mm2), 2 end frames {2 * m_frame:.1f} g ({FR_T} x {FR_H} x {FR_L:.2f}, 16 comb slots each), plenum total {m_corr + 2 * m_frame:.1f} g (architecture 190 g)")
SEP_T, SEP_OUT = 1.50, 122.6
n_win = dict(inlet=14, outlet_int=24, outlet_edge=8)
a_win = n_win["inlet"] * A_rr(WIN_X, WIN_Y, WIN_R) + n_win["outlet_int"] * A_rr(WIN_X, WIN_Y, WIN_R) + n_win["outlet_edge"] * A_rr(WIN_X, 5.0, WIN_R)
m_sep = (SEP_OUT**2 - (4 - math.pi) * 4 - a_win - math.pi / 4 * 9 - 3 * 3.4) * SEP_T * RHO_CU
pr(f"separator {SEP_T} mm OFE {SEP_OUT} sq: {m_sep:.1f} g (46 windows {a_win:.0f} mm2; architecture 190 g); 0.6 / 0.8 / 1.0 mm 316L: {m_sep / SEP_T / RHO_CU * RHO_SS * 0.6:.0f} / {m_sep / SEP_T / RHO_CU * RHO_SS * 0.8:.0f} / {m_sep / SEP_T / RHO_CU * RHO_SS * 1.0:.0f} g")
# ======================= 2. HYDRAULICS =======================
rows = [r for r in csv.DictReader(open(os.path.join(HERE, "artwork_prism15_ttv.csv"))) if r["line_id"] == "I4" and r["type"] == "inlet"]
A_or = np.array([float(r["area_mm2"]) for r in sorted(rows, key=lambda r: float(r["y_mm"]))]); A_mean = A_or.mean()
sc_meter = np.repeat((A_mean / A_or)**2, 8)                       # meter R2 scale per 0.25 mm cell (54 orifices x 8 cells)
CD = 0.72; DP_MET = 0.5 * rho * 1.54**2 / CD**2 / 1e3; DP_ROW, DP_FIN, DP_MISC = 0.50, 1.07, 0.08; KW = 1.6
W_PL, H_PL = W_CH * 1e-3, (H - T) * 1e-3
def plenum(lpm, win_in, win_out, A_in, A_out, scale=None, n=432, th_i=1.0, th_o=2.0, Lp=FIELD * 1e-3, Lch=L_CH * 1e-3):
    """1-D inlet/outlet channel pair, channels y +/-Lch/2, orifice cells over y +/-Lp/2. win_*: list of (y_c, half_len) m;
    A_*: window area m2 per window. Window split solved from channel pressure (K 1.6 on the window velocity)."""
    A = W_PL * H_PL; Dh = 2 * A / (2 * (W_PL + H_PL)); fRe = 62.0; Q = lpm / 7 / 60000.0
    nc = int(round(n * Lch / Lp)); dy = Lch / nc; y = (np.arange(nc) + 0.5) * dy - Lch / 2; ye = np.arange(nc + 1) * dy - Lch / 2
    act = abs(y) <= Lp / 2 + 1e-9; q0 = Q / act.sum(); s = lpm / 18
    inert = (DP_MET * (np.ones(nc) if scale is None else np.interp(y, np.linspace(-Lp / 2, Lp / 2, n), scale)) + DP_ROW + DP_MISC) * 1e3 * s * s
    R2 = np.where(act, inert / q0**2, 1e30); R1 = np.full(nc, DP_FIN * 1e3 * s / q0)
    def wmask(w):
        m = np.zeros((len(w), nc))
        for i, (yc, hl) in enumerate(w): m[i] = (abs(y - yc) <= hl); m[i] /= m[i].sum()
        return m
    Mi, Mo = wmask(win_in), wmask(win_out); fi = np.full(len(win_in), 1 / len(win_in)); fo = np.full(len(win_out), 1 / len(win_out))
    wm_i = (Mi.sum(0) > 0).astype(float); wm_o = (Mo.sum(0) > 0).astype(float)
    q = np.where(act, q0, 0.0); fric = fRe * mu / (2 * Dh**2)
    def pressure(u, th, wm):   # u on cell edges (signed, + toward +y); p on cells from y = -L/2 (dead end, p = 0);
        um = 0.5 * (u[1:] + u[:-1])   # no momentum recovery inside window cells (wm), as plenum_graded.py skips the feed cell
        inc = fric * um * dy + th * rho * (u[1:]**2 - u[:-1]**2) / 2 * (1 - wm); inc[0] = 0.0
        return -np.cumsum(inc)
    for it in range(2000):
        src_in = (fi @ Mi) * Q; src_out = (fo @ Mo) * Q
        F_in = np.concatenate([[0.0], np.cumsum(src_in - q)]); F_out = np.concatenate([[0.0], np.cumsum(q - src_out)])
        u_in, u_out = F_in / A, F_out / A; p_in = pressure(u_in, th_i, wm_i); p_out = pressure(u_out, th_o, wm_o)
        def qs(C):
            dp = np.maximum(C + p_in - p_out, 1e-6); return (-R1 + np.sqrt(R1**2 + 4 * R2 * dp)) / (2 * R2)
        lo, hi = -1e5, 1e6
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if qs(mid).sum() > Q: hi = mid
            else: lo = mid
        qn = qs(0.5 * (lo + hi)); C = 0.5 * (lo + hi)
        pw_in = Mi @ p_in; pw_out = Mo @ p_out      # channel pressure at the windows
        def split(pw, Aw, sign):
            def tot(Ph): return sum(Aw * math.sqrt(max(sign * (Ph - pw[i]), 0.0) * 2 / (KW * rho)) for i in range(len(pw)))
            lo, hi = (pw.max(), pw.max() + 1e5) if sign > 0 else (pw.min() - 1e5, pw.min())
            for _ in range(100):
                mid = 0.5 * (lo + hi)
                if (tot(mid) > Q) == (sign > 0): hi = mid
                else: lo = mid
            Ph = 0.5 * (lo + hi); f = np.array([Aw * math.sqrt(max(sign * (Ph - pw[i]), 0.0) * 2 / (KW * rho)) for i in range(len(pw))]); return f / f.sum(), Ph
        fi_n, Ph_in = split(pw_in, A_in, +1); fo_n, Ph_out = split(pw_out, A_out, -1)
        conv = np.max(abs(qn - q)) / q0 < 1e-8 and np.max(abs(fi_n - fi)) < 1e-7 and np.max(abs(fo_n - fo)) < 1e-7
        q = 0.7 * q + 0.3 * qn; fi = 0.85 * fi + 0.15 * fi_n; fo = 0.85 * fo + 0.15 * fo_n
        if conv: break
    r = q[act] / q0; ro = r.reshape(54, 8).mean(1)
    bleed_dp = (C + p_in - p_out)[[0, -1]]                       # branch dp at the two dead ends (Pa)
    return dict(cell=r.max() / r.min(), orif=ro.max() / ro.min(), ro=ro, u_in=u_in, u_out=u_out, ye=ye, fi=fi, fo=fo, Q=Q,
                dp_win_in=Ph_in - pw_in, dp_win_out=pw_out - Ph_out, bleed_dp=bleed_dp, it=it, conv=conv)
pr("\n## 2. Hydraulics (18 LPM unless stated; PG25 1005 kg/m3, 1.25 mPa s)")
win_in = [(yc * 1e-3, WIN_Y / 2 * 1e-3) for yc in Y_WIN_IN]; win_out = [(yc * 1e-3, WIN_Y / 2 * 1e-3) for yc in Y_WIN_OUT]
A_wi, A_wo = A_rr(WIN_X, WIN_Y, WIN_R) * 1e-6, A_rr(WIN_X, WIN_Y, WIN_R) * 1e-6
ref = plenum(18, [(-14e-3, 0.125e-3)], [(14e-3, 0.125e-3)], 96.6e-6, 96.6e-6, sc_meter)
pr(f"solver check, point feed -14/+14 as the architecture model: per-orifice max/min {ref['orif']:.3f} (grate lane 1.044), cell {ref['cell']:.3f}, long-half peak u {abs(ref['u_in']).max():.3f} m/s (plenum_height.py 0.78)")
res = {}
for lpm in (9, 18, 22.5, 27, 36):
    r = plenum(lpm, win_in, win_out, A_wi, A_wo, sc_meter); res[lpm] = r
    pr(f"as-designed windows, {lpm} LPM: per-orifice max/min {r['orif']:.3f} (cell {r['cell']:.3f}); inlet window split {np.round(r['fi'], 3).tolist()}, outlet split {np.round(r['fo'], 3).tolist()}; conv {r['conv']} ({r['it']} it)")
r = res[18]; A = W_PL * H_PL
iu = np.argmax(abs(r["u_in"])); io = np.argmax(abs(r["u_out"]))
pr(f"inlet channel |u| max {abs(r['u_in'][iu]):.3f} m/s at y {r['ye'][iu] * 1e3:+.1f} (cap 0.62 = half flow / section; CDA band 0.9); outlet channel |u| max {abs(r['u_out'][io]):.3f} m/s at y {r['ye'][io] * 1e3:+.1f}")
for lpm in (22.5, 36): pr(f"  {lpm} LPM: inlet |u| max {abs(res[lpm]['u_in']).max():.2f}, outlet {abs(res[lpm]['u_out']).max():.2f} m/s")
uw_in = r["fi"] * r["Q"] / A_wi; uw_out = r["fo"] * r["Q"] / A_wo
pr(f"separator windows 18 LPM: inlet {WIN_X} x {WIN_Y} r{WIN_R} ({A_wi * 1e6:.1f} mm2) u {np.round(uw_in, 3).tolist()} m/s, dp {np.round(r['dp_win_in'] / 1e3, 3).tolist()} kPa;"
    f" outlet u {np.round(uw_out, 3).tolist()} m/s, dp {np.round(r['dp_win_out'] / 1e3, 3).tolist()} kPa; cap 0.6 m/s; edge outlet 4 x {WIN_X} x 5.0 at half flow: same u")
pr(f"window dp in series (flow-weighted) {np.dot(r['fi'], r['dp_win_in']) / 1e3 + np.dot(r['fo'], r['dp_win_out']) / 1e3:.3f} kPa (architecture budget 0.46; K 1.6 convention of final_segbal.py)")
Ab = math.pi / 4 * (BLEED_D * 1e-3)**2
for d in (1.10, 0.80, 0.60):
    Ab = math.pi / 4 * (d * 1e-3)**2; qb = [0.62 * Ab * math.sqrt(2 * dp / rho) for dp in r["bleed_dp"]]
    tot = 7 * sum(qb) / (18 * LPM) * 100
    pr(f"bleed d {d:.2f} (Cd 0.62): branch dp at the dead ends {r['bleed_dp'][0] / 1e3:.2f} / {r['bleed_dp'][1] / 1e3:.2f} kPa -> {qb[0] * 6e4:.3f} / {qb[1] * 6e4:.3f} LPM per hole"
       f" = {qb[0] / (r['Q']) * 100:.1f} / {qb[1] / r['Q'] * 100:.1f} % of the line; 14 holes {tot:.1f} % of 18 LPM; caloric term 7.5 K x bypass/(1-bypass) = +{7.5 * tot / (100 - tot):.2f} K on the average")
# ---- final_segbal.py network (same method, kd/kc/K, 15 lines, mid-fed headers) with the as-designed window areas ----
PITCH = 7.7e-3; xin = (-46.2 + 15.4 * np.arange(7)) * 1e-3; xout = (-53.9 + 15.4 * np.arange(8)) * 1e-3
segs2 = [(k, j[0]) for k, x in enumerate(xin) for xo in (x - PITCH, x + PITCH) for j in [np.where(np.isclose(xout, xo))[0]] if len(j)]
NSEG = len(segs2)
def hdr(Q, ip, A, k, sign, s_jet, u_port):
    n = len(Q); Pp = np.zeros(n); Pp[ip] = sign * s_jet * 0.5 * rho * u_port**2
    for side in (-1, 1):
        idx = list(range(ip + side, -1 if side < 0 else n, side)); F = sum(Q[i] for i in idx); Pst = 0.0
        for i in idx:
            ua = F / A; F -= Q[i]; ub = F / A; Pp[i] = Pst + 0.5 * k * 0.5 * rho * (ua**2 - ub**2)
            Pst += k * 0.5 * rho * (ua**2 - ub**2) + sign * (-1) * 0.02 * (15.4e-3 / 9e-3) * 0.5 * rho * ua**2
    return Pp
def hdr_out(Qo, ip, A, kc):
    n = len(Qo); Pp = np.zeros(n)
    for side in (-1, 1):
        idx = list(range(ip + side, -1 if side < 0 else n, side)); F = sum(Qo[i] for i in idx); Pst = 0.0
        for i in idx:
            ua = F / A; F -= Qo[i]; ub = F / A; Pp[i] = Pst + 0.5 * kc * 0.5 * rho * (ua**2 - ub**2)
            Pst += kc * 0.5 * rho * (ua**2 - ub**2) + 0.02 * (15.4e-3 / 9e-3) * 0.5 * rho * ua**2
    return Pp
def segbal(lpm=18, A_out_scale=2.0, out_meter=0.5, meter=2.3, seg=1.07, s_jet=0.0, kd=1.0, kc=2.0, A_wi=96.6e-6, A_wo=96.6e-6, A_wedge=48.3e-6):
    nin, nout = 7, 8; Qt = lpm * LPM; s = lpm / 18; Ql0 = Qt / nin; qs0 = Qt / NSEG; A_hi = 161e-6; A_ho = 161e-6 * A_out_scale; u_port = Qt / (np.pi / 4 * 0.02**2)
    a_m = meter * 1e3 / (18 * LPM / nin)**2; a_wi = 1.6 * 0.5 * rho / A_wi**2; Aw = np.full(nout, A_wo); Aw[0] = Aw[-1] = A_wedge
    a_wo = 1.6 * 0.5 * rho / Aw**2; r_s = seg * 1e3 / (18 * LPM / NSEG); a_om = out_meter * 1e3 / (18 * LPM / NSEG)**2
    def segflow(dp): return dp / r_s if a_om == 0 else np.sign(dp) * (-r_s + np.sqrt(r_s**2 + 4 * a_om * abs(dp))) / (2 * a_om)
    def state(z):
        N = z[:nin]; Pq = z[nin:nin + nout]; C = z[-1]; q = np.array([segflow(N[k] - Pq[j]) for k, j in segs2]); Q = np.zeros(nin); Qo = np.zeros(nout)
        for (k, j), qq in zip(segs2, q): Q[k] += qq; Qo[j] += qq
        return N, Pq, C, q, Q, Qo
    def resid(z):
        N, Pq, C, q, Q, Qo = state(z); Phi = hdr(Q, 3, A_hi, kd, +1, s_jet, u_port) + C; Pho = hdr_out(Qo, 4, A_ho, kc)
        return np.concatenate([(Phi - N - (a_m + a_wi) * Q * abs(Q)) / (1e3 * s * s), (Pq - Pho - a_wo * Qo * abs(Qo)) / (1e3 * s * s), [(Q.sum() - Qt) / Qt]])
    z0 = np.concatenate([np.full(nin, seg * 1e3 * s), np.zeros(nout), [(meter + 0.3) * 1e3 * s * s + seg * 1e3 * s]])
    z, info, ier, msg = fsolve(resid, z0, full_output=True, xtol=1e-13, maxfev=50000); N, Pq, C, q, Q, Qo = state(z)
    rs = q / qs0; rl = Q / Ql0; return rl.max() / rl.min(), rs.max() / rs.min(), ier == 1
for lab, kw in (("final_segbal.py convention (A_w 6.9 x 14 both, edge half)", {}),
                ("as-designed windows: inlet 2 x 50, outlet 4 x 50, edge 4 x 25 mm2", dict(A_wi=2 * A_wi, A_wo=4 * A_wo, A_wedge=2 * A_wo)),
                ("as-designed, port jet undiffused", dict(A_wi=2 * A_wi, A_wo=4 * A_wo, A_wedge=2 * A_wo, s_jet=1.0))):
    pr(f"segbal {lab}: " + "; ".join(f"{lpm} LPM line {a:.3f} / segment {b:.3f}" for lpm in (9, 18, 36) for a, b, ok in [segbal(lpm, **kw)]))
# ======================= 3. STRUCTURE =======================
pr("\n## 3. Structure (post-braze OFE, design allowable 40 MPa; design burst 3.1 MPa, proof 1.55 MPa)")
for p in (1.55, 3.1, 4.5): pr(f"wall tension at {p} MPa: p x pitch / t = {p * P / T:.1f} MPa; pull per wall {p * P:.1f} N/mm")
def plate_band(b, t, E, nu, Lam, wland, qb, N=300, M=60):
    """Kirchhoff strip 0..b (clamped), periodic in y (period Lam), band load qb over |y|<wland/2; returns stresses at y=0 and
    the clamped-edge reaction peak/mean (= wall-pull concentration)."""
    D = E * t**3 / (12 * (1 - nu**2)); h = b / N; x = np.arange(N + 1) * h
    W = {}; sig_e = sig_m = 0.0; V0 = Vm = 0.0
    for m in range(M + 1):
        qm = qb * wland / Lam if m == 0 else 2 * qb / (m * math.pi) * math.sin(m * math.pi * wland / Lam)
        k = 2 * math.pi * m / Lam; n = N - 1; Amat = np.zeros((n, n)); rhs = np.full(n, qm / D)
        for i in range(1, N):
            row = i - 1
            for off, c4 in ((-2, 1), (-1, -4), (0, 6), (1, -4), (2, 1)):
                jj = i + off; c = c4 / h**4
                if 1 <= jj <= N - 1: Amat[row, jj - 1] += c
                elif jj == -1: Amat[row, 0] += c          # ghost: W(-1) = W(1) (clamped)
                elif jj == N + 1: Amat[row, N - 2] += c
            for off, c2 in ((-1, 1), (0, -2), (1, 1)):
                jj = i + off
                if 1 <= jj <= N - 1: Amat[row, jj - 1] += -2 * k * k * c2 / h**2
            Amat[row, row] += k**4
        w = np.zeros(N + 1); w[1:N] = np.linalg.solve(Amat, rhs); W[m] = w
        wxx_e = (8 * w[1] - w[2]) / (2 * h**2); wxx_m = (w[N // 2 + 1] - 2 * w[N // 2] + w[N // 2 - 1]) / h**2   # Taylor with w(0)=w'(0)=0
        sig_e += 6 * D * wxx_e / t**2; sig_m += 6 * D * (wxx_m - nu * k * k * w[N // 2]) / t**2
        wxxx_e = 1.5 * (w[2] - 4 * w[1]) / h**3
        V = -D * wxxx_e
        V0 += V; Vm += V if m == 0 else 0.0
    return abs(sig_e), abs(sig_m), (V0 / Vm if Vm else float("nan"))
E_CU, E_SS, NU = 117e3, 193e3, 0.33
LAM, WLAND = 14.0, 2.0
for p in (1.55, 3.1):
    se, sm, cf = plate_band(W_CH, SEP_T, E_CU, NU, LAM, LAM, p)          # uniform p: calibration vs 0.5 p (b/t)^2
    pr(f"separator {SEP_T} Cu, uniform {p} MPa: edge {se:.1f} / mid {sm:.1f} MPa (closed form {0.5 * p * (W_CH / SEP_T)**2:.1f})")
    qb = p * LAM / WLAND
    for t, E, lab in ((1.5, E_CU, "1.5 Cu"), (1.8, E_CU, "1.8 Cu"), (2.0, E_CU, "2.0 Cu"), (0.6, E_SS, "0.6 316L"), (0.8, E_SS, "0.8 316L"), (1.0, E_SS, "1.0 316L")):
        se, sm, cf = plate_band(W_CH, t, E, 0.3 if E == E_SS else NU, LAM, WLAND, qb)
        pr(f"separator {lab}, cap-land band load (p {p} MPa x {LAM:.0f} pitch on a {WLAND:.0f} mm land = {qb:.1f} N/mm2) over an outlet channel {W_CH:.3f}: edge {se:.0f} / mid {sm:.0f} MPa; wall-pull peak/mean {cf:.2f}")
se, sm, cf = plate_band(W_CH, 1.5, E_CU, NU, LAM, 3.0, 3.1 * LAM / 3.0); pr(f"separator 1.5 Cu, 3 mm lands at 14 pitch, 3.1 MPa: edge {se:.0f} / mid {sm:.0f} MPa")
se, sm, cf = plate_band(W_CH, 1.5, E_CU, NU, 10.0, 2.0, 3.1 * 10 / 2.0); pr(f"separator 1.5 Cu, 2 mm lands at 10 pitch (8 wide arches), 3.1 MPa: edge {se:.0f} / mid {sm:.0f} MPa")
pr(f"over an inlet channel the separator is backed by the bonded 0.8 top flat: composite t 2.3 -> x{(1.5 / 2.3)**2:.2f}")
# joint peel at the wall foot / top (beam on elastic foundation, braze layer 25 um, E 80 GPa)
EI = E_CU * T**3 / 12; kf = 80e3 / 0.025; lam = (4 * EI / kf)**0.25
for p in (1.55, 3.1):
    Fw = p * P; strip = P / 2 + T / 2 - RO - SLOT_W / 2 - 0.30; net_bot = Fw - p * (P / 2 + T / 2 - RO - SLOT_W / 2); net_top = Fw - p * (P / 2 + T / 2 - RO)
    pr(f"joint peel at {p} MPa: foundation length {lam:.2f} mm; foot (bottom flat to grate, bonded strip {strip:.2f}): net uplift {net_bot:.1f} N/mm -> peak ~{2 * net_bot / lam:.0f} MPa, mean {net_bot / strip:.0f};"
       f" top flat to separator: net {net_top:.1f} N/mm -> peak ~{2 * net_top / lam:.0f} MPa (BAg-8 joint tensile > 150; E1 FEA)")
for pf in (0.05, 0.10, 0.20, 0.60):
    M = pf * P / 2 * (P / 4); pr(f"braze fixture {pf} MPa at 790 C: top flat {0.5 * pf * (FLAT / T)**2:.1f} MPa, bend corner {6 * M / T**2:.1f} MPa (OFE hot 0.2 % proof ~10 MPa, est.), wall {pf * P / T:.1f} MPa compression")
dalpha, dT = 1.0e-6, 760; eps = dalpha * dT
pr(f"316L option: CTE mismatch ~{dalpha * 1e6:.1f} ppm/K x {dT} K = {eps * 100:.3f} % -> constrained stress {E_SS * eps:.0f} MPa (yield 170-240 annealed), edge shear-lag on the top-flat joints ~{E_SS * eps * 0.8 / 3:.0f} MPa (0.8 mm over 3 mm),"
   f" as-brazed bow ~{6 * eps * 0.8 / 11.8**2 * (E_SS / E_CU) * 60**2 / 2 * 1e3:.0f} um over the half-width (removed by the fly-cut; +/-50 %)")
# ======================= 4. COST =======================
pr("\n## 4. Cost (US$ at 100k/yr, Cu US$14.6/kg LME + 4 OFE premium, scrap 88 %)")
buy_c = area * 1.10 * T * RHO_CU / 1000; buy_f = 2 * FR_T * FR_H * FR_L * 1.05 * RHO_CU / 1000; buy_s = SEP_OUT**2 * 1.08 * SEP_T * RHO_CU / 1000
cu = lambda b, f: b * 18.6 - (b - f) * 14.6 * 0.88
pr(f"plenum copper: corrugation buy {buy_c:.3f} kg / finished {m_corr / 1000:.3f} -> US${cu(buy_c, m_corr / 1000):.2f}; frames buy {buy_f:.3f} -> US${cu(buy_f, 2 * m_frame / 1000):.2f}; fold+pierce 0.9-1.4; frames saw/skim 0.6-1.0; tack 0.2 -> plenum US$4.6-5.8 (architecture 4.4)")
pr(f"separator copper buy {buy_s:.3f} kg / finished {m_sep / 1000:.3f} -> US${cu(buy_s, m_sep / 1000):.2f}; pierce (compound die) + double-disc grind 1.0-1.5 -> separator US$4.5-5.3 (in the architecture's stampings 6.8 with the grate)")
json.dump(dict(dev_width=round(DEV, 3), folds=folds, flat_centres={k: round(v, 3) for k, v in flat_cent.items()}, wall_centres={k: round(v, 3) for k, v in wall_cent.items()},
               features=feat, mass_g=dict(corrugation=round(m_corr, 1), frames=round(2 * m_frame, 1), separator=round(m_sep, 1)),
               hyd18=dict(orifice_maxmin={str(k): round(v["orif"], 4) for k, v in res.items()}, u_in_max=round(float(abs(r["u_in"]).max()), 3), u_out_max=round(float(abs(r["u_out"]).max()), 3),
                          win_u_in=np.round(uw_in, 3).tolist(), win_u_out=np.round(uw_out, 3).tolist(), bleed_dp_kpa=np.round(r["bleed_dp"] / 1e3, 3).tolist())),
          open(os.path.join(HERE, "plenum_sep_data.json"), "w"), indent=1)
open(os.path.join(HERE, "plenum_sep.out"), "w").write("\n".join(OUT) + "\n")
