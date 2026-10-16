#!/usr/bin/env python3
"""
nonuniform-heatmap.py  --  2-D (x-y) non-uniform heat-map check for the 15 kW-class cold plate.

Package (future 15 kW-class AI accelerator, 108 x 108 mm cold-plate footprint = calibrated 117 cm2):
  * 4 reticle dies 26 x 33 mm (2x2 block, 1 mm gaps) at 350 W/cm2  -> 4 x 3.0 kW = 12.0 kW
  * 16 HBM stacks 11 x 12 mm (2 cols x 4 rows each side)   at  40 W/cm2  -> 16 x 53 W = 0.85 kW
  * HBM top surface 0.4 mm below die top (non-planar)
Flow: 1.2 LPM/kW of actual power, PG25, 45 C inlet.

Thermal model:
  3-D steady conduction in the Cu base (thickness t) solved spectrally (2-D cosine series = the
  Lee/Yovanovich/Muzychka multi-source spreading solution, adiabatic edges) with
      z=0 (die side):  -k dT/dz = q''(x,y)                 (heat through the TIM, no lateral spreading in TIM)
      z=t (fin side):  -k dT/dz = h_eff(x,y) [T - T_f(x,y)]  (fin array lumped into h_eff from the 1-D model)
  Spatially varying h_eff handled by fixed-point iteration around a reference h0.
  Local fluid temperature T_f from an energy balance on the fin-side flux:
      HMMC       : every 2 mm segment gets fresh inlet fluid -> T_f = T_in + 0.5 q''_bot/(rho cp V''_local)
      split-flow : fluid heats along the path from the centre feed outward, per transverse strip.
  T_case = T_base,top + q'' R''_TIM(local).   Tj estimates: GPU +q'' R''_jc, HBM + P_stack R_jc.
"""
import sys, math
import numpy as np
from scipy.fft import dctn, idctn

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
import coldplate_model as cm

RHO, CP, K_CU = 1005.0, 3930.0, 390.0
T_IN = 45.0
A_PLATE_CM2 = 117.0
LX = LY = 0.108
DX = 0.5e-3
N = int(round(LX / DX))
xc = (np.arange(N) + 0.5) * DX - LX / 2
X, Y = np.meshgrid(xc, xc, indexing="ij")          # X along axis 0, Y along axis 1

# ---------------------------------------------------------------- package geometry (m)
DIE_W, DIE_H = 26e-3, 33e-3
DIES = [((sx * 13.5e-3), (sy * 17.0e-3)) for sx in (-1, 1) for sy in (-1, 1)]       # centres
HBM_W, HBM_H = 11e-3, 12e-3
HBMS = [((sx * cx), cy) for sx in (-1, 1) for cx in (34e-3, 46e-3) for cy in (-19.5e-3, -6.5e-3, 6.5e-3, 19.5e-3)]

def rect(cx, cy, w, h):
    return (np.abs(X - cx) <= w / 2) & (np.abs(Y - cy) <= h / 2)

DIE_MASK = np.zeros((N, N), bool)
for c in DIES: DIE_MASK |= rect(*c, DIE_W, DIE_H)
HBM_MASK = np.zeros((N, N), bool)
for c in HBMS: HBM_MASK |= rect(*c, HBM_W, HBM_H)
DIE_ZONE = (np.abs(X) <= 26.5e-3) & (np.abs(Y) <= 33.5e-3)                        # die block incl. gaps
HBM_ZONE = (np.abs(X) >= 28.5e-3) & (np.abs(X) <= 51.5e-3) & (np.abs(Y) <= 25.5e-3)
UNH_ZONE = ~(DIE_ZONE | HBM_ZONE)
A_cell = DX * DX
frac = lambda m: m.sum() / m.size

# ---------------------------------------------------------------- spectral slab solver
m = np.arange(N)
LAM = np.pi * m / LX
BETA = np.sqrt(LAM[:, None] ** 2 + LAM[None, :] ** 2)

def solve_slab(q_top, Tf_eff, t, h0, k=K_CU):
    """Top-surface and bottom-surface temperature of a slab with top flux q_top and
    bottom Robin BC with uniform h0 and fluid field Tf_eff. All fields (N,N)."""
    Q = dctn(q_top, type=2, norm="ortho")
    F = dctn(Tf_eff, type=2, norm="ortho")
    b = BETA.copy(); b[0, 0] = 1.0
    sh, ch = np.sinh(b * t), np.cosh(b * t)
    B = -Q / (k * b)
    A = (h0 * F - B * (k * b * ch + h0 * sh)) / (k * b * sh + h0 * ch)
    Tbot = A * ch + B * sh
    A[0, 0] = F[0, 0] + Q[0, 0] / h0 + Q[0, 0] * t / k
    Tbot[0, 0] = A[0, 0] - Q[0, 0] * t / k
    return idctn(A, type=2, norm="ortho"), idctn(Tbot, type=2, norm="ortho")

# ---------------------------------------------------------------- fluid / bottom-flux operators
# Bottom BC written as q_bot = M(u), u = T_bot - T_in, with M a LINEAR operator:
#   HMMC : q_bot = h_loc u,  h_loc = 1/(1/h_eff + 0.5/(rho cp V''_local))   (segment-mean fluid rise in series)
#   split: marching along each strip from the centre feed: T_f,i = T_in + ds (S_{i-1} + 0.5 q_i)/(m' cp),
#          q_i = h_i (u_i - (T_f,i - T_in)), solved cell by cell (lower-triangular, exact).
# The slab is then solved as  u - S_f(u - M(u)/h0) = S_q(q_top)  with GMRES, S_q/S_f the spectral slab maps.
from scipy.sparse.linalg import LinearOperator, gmres

def M_hmmc(u, h, Vpp):
    hloc = 1.0 / (1.0 / h + 0.5 / (RHO * CP * Vpp))
    q = hloc * u
    Tf = T_IN + 0.5 * q / (RHO * CP * Vpp)
    return q, Tf

def M_split(u, h, mprime, axis):
    """Flow along `axis`, outward from the centre line; mprime (N,) per transverse strip."""
    uu = u if axis == 1 else u.T
    hh = h if axis == 1 else h.T
    half = N // 2
    q = np.empty_like(uu); Tf = np.empty_like(uu)
    c = DX / (mprime * CP)                                      # K per (W/m2) of picked-up flux, (N,)
    for sgn, idx in ((1, range(half, N)), (-1, range(half - 1, -1, -1))):
        S = np.zeros(N)
        for i in idx:
            qi = hh[:, i] * (uu[:, i] - c * S) / (1 + 0.5 * hh[:, i] * c)
            q[:, i] = qi; Tf[:, i] = T_IN + c * (S + 0.5 * qi)
            S = S + qi
    return (q, Tf) if axis == 1 else (q.T, Tf.T)

def solve_coupled(q_top, Mfun, h0, t):
    """Solve slab + fluid coupling exactly (linear). Returns Ttop, Tbot, q_bot, Tf, gmres info."""
    zero = np.zeros((N, N))
    b = solve_slab(q_top, zero, t, h0)[1].ravel()
    def matvec(v):
        u = v.reshape(N, N)
        q, _ = Mfun(u)
        return (u - solve_slab(zero, u - q / h0, t, h0)[1]).ravel()
    A = LinearOperator((N * N, N * N), matvec=matvec, dtype=float)
    u, info = gmres(A, b, rtol=1e-9, restart=60, maxiter=400)
    u = u.reshape(N, N)
    q_bot, Tf = Mfun(u)
    Ttop, Tbot = solve_slab(q_top, T_IN + u - q_bot / h0, t, h0)
    return Ttop, Tbot, q_bot, Tf, info

# ---------------------------------------------------------------- configuration runner
def run(cfg, q_die, q_hbm, verbose=False, lpm=None):
    q_top = np.where(DIE_MASK, q_die, 0.0) + np.where(HBM_MASK, q_hbm, 0.0)
    Q_tot = q_top.sum() * A_cell
    Vdot = (1.2 * Q_tot / 1000 if lpm is None else lpm) / 60 / 1000   # m3/s, default 1.2 LPM/kW
    Vpp_avg = Vdot / (A_PLATE_CM2 * 1e-4)
    t = cfg["t_base"]
    if cfg["kind"] == "hmmc":
        fmap = cfg["f_map"]; Vpp = Vpp_avg * fmap
        h = cfg["heff_fn"](fmap)
        Mfun = lambda u: M_hmmc(u, h, Vpp)
        h0 = float(np.mean(1.0 / (1.0 / h + 0.5 / (RHO * CP * Vpp))))
    else:
        fprof = cfg["f_profile"]
        mprime = RHO * Vdot / (2 * LX) * fprof
        h = np.asarray(cfg["heff_fn"](np.broadcast_to(fprof[:, None] if cfg["axis"] == 1 else fprof[None, :], (N, N))))
        Mfun = lambda u: M_split(u, h, mprime, cfg["axis"])
        h0 = float(np.mean(h))
    Ttop, Tbot, q_bot, Tf, info = solve_coupled(q_top, Mfun, h0, t)
    ebal = q_bot.sum() * A_cell / Q_tot
    Rt = np.where(DIE_MASK, cfg["R_tim_die"], 0.0) + np.where(HBM_MASK, cfg["R_tim_hbm"], 0.0)
    Tcase = Ttop + q_top * Rt
    d = dict(Q_kW=Q_tot / 1e3, lpm=Vdot * 6e4, info=info, ebal=ebal, h0=h0,
             h_die=float(np.mean(h[DIE_MASK])),
             die_max=Tcase[DIE_MASK].max() - T_IN, die_avg=Tcase[DIE_MASK].mean() - T_IN,
             die_min=Tcase[DIE_MASK].min() - T_IN,
             hbm_max=Tcase[HBM_MASK].max() - T_IN, hbm_avg=Tcase[HBM_MASK].mean() - T_IN,
             hbm_basetop_max=Ttop[HBM_MASK].max() - T_IN, hbm_basetop_avg=Ttop[HBM_MASK].mean() - T_IN,
             die_basetop_max=Ttop[DIE_MASK].max() - T_IN,
             Tf_die_avg=Tf[DIE_MASK].mean() - T_IN, Tf_die_max=Tf[DIE_MASK].max() - T_IN,
             Tf_hbm_avg=Tf[HBM_MASK].mean() - T_IN, Tf_hbm_max=Tf[HBM_MASK].max() - T_IN,
             Tcase=Tcase, Ttop=Ttop, Tf=Tf, q_bot=q_bot)
    if verbose or info != 0 or abs(ebal - 1) > 0.01:
        print(f"   [solver] gmres info={info}, energy balance q_bot/q_top = {ebal:.4f}")
    return d

# ---------------------------------------------------------------- h_eff functions from the 1-D model
Q_REF = 12850.0
def heff_from_model(plate_fn, fvals):
    f = np.atleast_1d(np.asarray(fvals, float))
    uniq = np.unique(np.round(f, 4))
    table = {}
    for u in uniq:
        r = plate_fn().evaluate(Q_REF, 1.2 * max(u, 1e-3))
        table[u] = r["h"] * r["area_ratio"]
    out = np.vectorize(lambda v: table[np.round(v, 4)])(f)
    return out.reshape(np.shape(fvals)) if np.ndim(fvals) else float(out.ravel()[0])

HMMC = lambda: cm.hmmc_design(A_PLATE_CM2)
HMMC_FINE = lambda: cm.hmmc_design(A_PLATE_CM2, fin_t_mm=0.075, gap_mm=0.075, fin_h_mm=0.8)
COOLIT = lambda: cm.coolit_like(A_PLATE_CM2)

def zone_map(fd, fh, fu):
    return np.where(DIE_ZONE, fd, np.where(HBM_ZONE, fh, fu))

def profile_y(fd, fh, fm):                      # transverse = x for flow along y
    return np.where(np.abs(xc) <= 26.5e-3, fd, np.where(np.abs(xc) <= 51.5e-3, fh, fm))

def profile_x(fin, fout):                       # transverse = y for flow along x
    return np.where(np.abs(xc) <= 33.5e-3, fin, fout)

R_PASTE_CI, R_PASTE_H = 0.07e-4, 0.05e-4        # m2K/W (0.07 / 0.05 cm2K/W)
# HBM interface options for a 0.4 mm step + 0.05 mm nominal BLT:
K_PASTE, K_PAD = 4.0, 5.0
R_HBM = {
    "paste 0.45 mm":   0.45e-3 / K_PASTE + 0.03e-4,                 # bulk + contact
    "pad 5 W/mK":      0.45e-3 / K_PAD + 0.15e-4,                   # pads: ~0.1-0.2 cm2K/W contact
    "Cu pedestal+paste": 0.10e-3 / K_PAD * 0 + 0.10e-3 / K_PASTE + 0.03e-4,   # 0.1 mm BLT paste (tolerance margin)
    "pedestal+indium": 0.10e-3 / 80.0 + 0.05e-4,                    # 0.1 mm In pad, two contacts
}
R_JC_GPU = 0.05e-4        # m2K/W, lidless 0.6 mm Si
R_JC_HBM = 0.30           # K/W per stack (+-50 %)

def mk(kind, plate_fn, t_base, R_die, fmap=None, axis=None, prof=None):
    fn = lambda f: heff_from_model(plate_fn, f)
    return dict(kind=kind, t_base=t_base, heff_fn=fn, f_map=fmap, axis=axis, f_profile=prof,
                R_tim_die=R_die, R_tim_hbm=R_HBM["Cu pedestal+paste"])

# fraction of plate area per zone
a_d, a_h, a_u = frac(DIE_ZONE), frac(HBM_ZONE), frac(UNH_ZONE)

CONFIGS = {
  "C-x-U  CoolIT-like, flow x (across die then HBM), uniform":
      mk("split", COOLIT, 2e-3, R_PASTE_CI, axis=0, prof=profile_x(1.0, 1.0)),
  "C-y-U  CoolIT-like, flow y (along HBM columns), uniform":
      mk("split", COOLIT, 2e-3, R_PASTE_CI, axis=1, prof=profile_y(1.0, 1.0, 1.0)),
  "C-y-Z  CoolIT-like, flow y, zoned channels 1.75/0.3/0.1":
      mk("split", COOLIT, 2e-3, R_PASTE_CI, axis=1, prof=profile_y(1.75, 0.30, 0.10)),
  "H-U    HMMC 0.1 mm, base 1 mm, uniform flow":
      mk("hmmc", HMMC, 1e-3, R_PASTE_H, fmap=zone_map(1.0, 1.0, 1.0)),
  "H-Z1   HMMC, 2x flow/area over die block":
      mk("hmmc", HMMC, 1e-3, R_PASTE_H, fmap=zone_map(1.53, 0.767, 0.767)),
  "H-Z2   HMMC, heat-proportional 3-zone 3.0/0.32/0.04":
      mk("hmmc", HMMC, 1e-3, R_PASTE_H, fmap=zone_map(3.0, 0.32, 0.04)),
  "H-Z3   HMMC, 3-zone 2.9/0.5/0.04 (more HBM flow)":
      mk("hmmc", HMMC, 1e-3, R_PASTE_H, fmap=zone_map(2.9, 0.5, 0.04)),
  "H-Z2f  HMMC-fine 0.075 mm, 3-zone":
      mk("hmmc", HMMC_FINE, 1e-3, R_PASTE_H, fmap=zone_map(3.0, 0.32, 0.04)),
  "H-Z2-LM HMMC 3-zone, liquid-metal die TIM 0.015":
      mk("hmmc", HMMC, 1e-3, 0.015e-4, fmap=zone_map(3.0, 0.32, 0.04)),
  "H-Z2f-LM HMMC-fine 3-zone, liquid-metal die TIM":
      mk("hmmc", HMMC_FINE, 1e-3, 0.015e-4, fmap=zone_map(3.0, 0.32, 0.04)),
}

def main():
    print(f"grid {N}x{N} @ {DX*1e3:.2f} mm; zone area fractions die {a_d:.3f} HBM {a_h:.3f} unheated {a_u:.3f}")
    print(f"die area {DIE_MASK.sum()*A_cell*1e4:.1f} cm2, HBM area {HBM_MASK.sum()*A_cell*1e4:.1f} cm2")
    for nm, c in CONFIGS.items():
        if c["kind"] == "hmmc":
            s = (c["f_map"] * A_cell).sum() / (LX * LY)
        else:
            s = c["f_profile"].mean()
        print(f"  flow-share check {nm[:8]}: sum f*area/A = {s:.3f}")

    # ---------- validation 1: uniform 128 W/cm2 TTV must reproduce the 1-D model
    print("\n## V1: uniform TTV 15 kW / 128 W/cm2 (should match 1-D model: CoolIT-like 34.5 K, HMMC 24.1 K)")
    q_ttv = 15000 / (LX * LY)
    for nm, c in [("CoolIT-like split", CONFIGS["C-x-U  CoolIT-like, flow x (across die then HBM), uniform"]),
                  ("HMMC uniform", CONFIGS["H-U    HMMC 0.1 mm, base 1 mm, uniform flow"])]:
        q_top = np.full((N, N), q_ttv)
        Vdot = 1.2 * 15 / 60 / 1000; Vpp = Vdot / (LX * LY)
        h = np.full((N, N), float(c["heff_fn"](1.0)))
        if c["kind"] == "hmmc":
            Mfun = lambda u: M_hmmc(u, h, np.full((N, N), Vpp)); h0 = float(np.mean(1/(1/h + 0.5/(RHO*CP*Vpp))))
        else:
            Mfun = lambda u: M_split(u, h, np.full(N, RHO * Vdot / (2 * LX)), 0); h0 = float(h.mean())
        Ttop, Tbot, q_bot, Tf, info = solve_coupled(q_top, Mfun, h0, c["t_base"])
        Tc = Ttop + q_top * c["R_tim_die"]
        print(f"  {nm}: avg dT {Tc.mean()-T_IN:.1f} K, max {Tc.max()-T_IN:.1f} K, fluid avg {Tf.mean()-T_IN:.1f} / max {Tf.max()-T_IN:.1f} K  (h_eff {h.mean()/1e3:.0f} kW/m2K, gmres {info})")

    # ---------- validation 2: single 26x33 source, spreading vs Lee et al. (1995)
    print("\n## V2: single die 26x33 mm @ 350 W/cm2, isothermal fluid, spreading check vs Lee/Yovanovich")
    q1 = np.where(rect(0, 0, DIE_W, DIE_H), 3.5e6, 0.0)
    for t in (1e-3, 2e-3, 3e-3):
        for h in (100e3, 200e3):
            Ttop, _ = solve_slab(q1, np.full((N, N), T_IN), t, h)
            src = rect(0, 0, DIE_W, DIE_H)
            Tmax, Tavg = Ttop[src].max() - T_IN, Ttop[src].mean() - T_IN
            # Lee et al.: equivalent circular source / plate
            P = 3.5e6 * DIE_W * DIE_H
            a = math.sqrt(DIE_W * DIE_H / math.pi); b = math.sqrt(LX * LY / math.pi)
            eps, tau, Bi = a / b, t / b, h * b / K_CU
            lam = math.pi + 1 / (eps * math.sqrt(math.pi))
            Phi = (math.tanh(lam * tau) + lam / Bi) / (1 + lam / Bi * math.tanh(lam * tau))
            psi_max = eps * tau / math.sqrt(math.pi) + (1 - eps) * Phi / math.sqrt(math.pi)
            psi_avg = eps * tau / math.sqrt(math.pi) + 0.5 * (1 - eps) ** 1.5 * Phi
            R_max = psi_max / (K_CU * a * math.sqrt(math.pi)) + 1 / (h * math.pi * b * b)
            R_avg = psi_avg / (K_CU * a * math.sqrt(math.pi)) + 1 / (h * math.pi * b * b)
            one_d = 3.5e6 * (t / K_CU + 1 / h)
            print(f"  t={t*1e3:.0f} mm h={h/1e3:.0f}: DCT max {Tmax:.1f} avg {Tavg:.1f} | Lee max {P*R_max:.1f} avg {P*R_avg:.1f} | 1-D no-spreading {one_d:.1f} K")

    # ---------- main configurations, primary package
    print("\n## Primary package: 4 dies @350 W/cm2 + 16 HBM @40 W/cm2, 1.2 LPM/kW, HBM on Cu pedestal (0.1 mm paste)")
    hdr = "| config | Q kW | LPM | h_eff die kW/m2K | Tf die avg/max | die case dT avg / max / min | Tj GPU max (C) | Tf HBM avg/max | HBM case dT avg/max | Tj HBM max (C) |"
    print(hdr); print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    RES = {}
    for nm, c in CONFIGS.items():
        d = run(c, 3.5e6, 0.40e6); RES[nm] = d
        TjG = T_IN + d["die_max"] + 3.5e6 * R_JC_GPU
        TjH = T_IN + d["hbm_max"] + 0.40e6 * HBM_W * HBM_H * R_JC_HBM
        print(f"| {nm} | {d['Q_kW']:.2f} | {d['lpm']:.1f} | {d['h_die']/1e3:.0f} | {d['Tf_die_avg']:.1f}/{d['Tf_die_max']:.1f} | "
              f"{d['die_avg']:.1f} / {d['die_max']:.1f} / {d['die_min']:.1f} | {TjG:.0f} | {d['Tf_hbm_avg']:.1f}/{d['Tf_hbm_max']:.1f} | "
              f"{d['hbm_avg']:.1f}/{d['hbm_max']:.1f} | {TjH:.0f} |")

    # budget decomposition for key configs (at the hottest die point)
    print("\n## Budget at the hottest die cell (K): caloric (Tf-Tin) | base+conv (Ttop-Tf) | TIM")
    for nm in ("C-x-U  CoolIT-like, flow x (across die then HBM), uniform", "H-U    HMMC 0.1 mm, base 1 mm, uniform flow",
               "H-Z2   HMMC, heat-proportional 3-zone 3.0/0.32/0.04", "H-Z2f-LM HMMC-fine 3-zone, liquid-metal die TIM"):
        d = RES[nm]; i = np.unravel_index(np.argmax(np.where(DIE_MASK, d["Tcase"], -1e9)), (N, N))
        cal = d["Tf"][i] - T_IN; bc = d["Ttop"][i] - d["Tf"][i]; tim = d["Tcase"][i] - d["Ttop"][i]
        print(f"  {nm[:8]}: at x={X[i]*1e3:+.1f} y={Y[i]*1e3:+.1f} mm: caloric {cal:.1f} | base+conv {bc:.1f} | TIM {tim:.1f} | total {cal+bc+tim:.1f}")

    # ---------- HBM interface options
    print("\n## HBM case dT (K) and Tj (C) vs interface option (0.4 mm step), HBM 40 W/cm2 (53 W/stack), R_jc,HBM 0.3 K/W")
    print("| config | base-top dT under HBM avg/max | " + " | ".join(R_HBM) + " |")
    print("|---|---:|" + "---:|" * len(R_HBM))
    for nm in ("C-x-U  CoolIT-like, flow x (across die then HBM), uniform", "C-y-Z  CoolIT-like, flow y, zoned channels 1.75/0.3/0.1",
               "H-U    HMMC 0.1 mm, base 1 mm, uniform flow", "H-Z2   HMMC, heat-proportional 3-zone 3.0/0.32/0.04",
               "H-Z3   HMMC, 3-zone 2.9/0.5/0.04 (more HBM flow)"):
        d = RES[nm]; row = f"| {nm[:8]} | {d['hbm_basetop_avg']:.1f}/{d['hbm_basetop_max']:.1f} |"
        for k, R in R_HBM.items():
            dT = d["hbm_basetop_max"] + 0.40e6 * R
            row += f" {dT:.1f} K / Tj {T_IN + dT + 0.40e6*HBM_W*HBM_H*R_JC_HBM:.0f} C |"
        print(row)
    print("R''_HBM options (cm2K/W): " + ", ".join(f"{k}: {v*1e4:.2f}" for k, v in R_HBM.items()))

    # HBM flux sensitivity (H-Z2 and C-x-U), pedestal
    print("\n## HBM flux sensitivity (pedestal + 0.1 mm paste): HBM case dT max / Tj max")
    print("| HBM W/cm2 | W/stack | C-x-U | H-Z2 | H-Z2 with pad 5 W/mK |")
    print("|---:|---:|---:|---:|---:|")
    for qh in (20e4, 40e4, 60e4, 80e4):
        dC = run(CONFIGS["C-x-U  CoolIT-like, flow x (across die then HBM), uniform"], 3.5e6, qh)
        dH = run(CONFIGS["H-Z2   HMMC, heat-proportional 3-zone 3.0/0.32/0.04"], 3.5e6, qh)
        P = qh * HBM_W * HBM_H
        pad = dH["hbm_basetop_max"] + qh * R_HBM["pad 5 W/mK"]
        print(f"| {qh/1e4:.0f} | {P:.0f} | {dC['hbm_max']:.1f} K / {T_IN+dC['hbm_max']+P*R_JC_HBM:.0f} C | "
              f"{dH['hbm_max']:.1f} K / {T_IN+dH['hbm_max']+P*R_JC_HBM:.0f} C | {pad:.1f} K / {T_IN+pad+P*R_JC_HBM:.0f} C |")

    # ---------- die-induced heating of HBM (superposition: HBM-only solve)
    print("\n## Die-to-HBM coupling: HBM base-top dT with dies ON vs OFF (K)")
    for nm in ("C-x-U  CoolIT-like, flow x (across die then HBM), uniform", "C-y-Z  CoolIT-like, flow y, zoned channels 1.75/0.3/0.1",
               "H-Z2   HMMC, heat-proportional 3-zone 3.0/0.32/0.04"):
        c = CONFIGS[nm]; on = RES[nm]
        off = run(c, 0.0, 0.40e6, lpm=on["lpm"])
        print(f"  {nm[:8]}: dies ON {on['hbm_basetop_avg']:.1f}/{on['hbm_basetop_max']:.1f}, OFF {off['hbm_basetop_avg']:.1f}/{off['hbm_basetop_max']:.1f} "
              f"-> die-induced {on['hbm_basetop_avg']-off['hbm_basetop_avg']:.1f} avg / {on['hbm_basetop_max']-off['hbm_basetop_max']:.1f} max; "
              f"fluid under HBM avg {on['Tf_hbm_avg']:.1f} K")

    # ---------- zoning sweep: die-zone flow factor (HBM zone 0.32, remainder to unheated)
    print("\n## HMMC zoning sweep: die-zone flow factor f_d (HBM zone 0.32; unheated takes the remainder)")
    print("| f_d | die share of flow | unheated f_u | Tf die avg | die dT avg | die dT max | HBM dT max | dP est kPa |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|")
    base = CONFIGS["H-Z2   HMMC, heat-proportional 3-zone 3.0/0.32/0.04"]
    r0 = HMMC().evaluate(Q_REF, 1.2)
    for fd in (1.0, 1.5, 2.0, 2.5, 3.0):
        fu = max(0.02, (1 - a_d * fd - a_h * 0.32) / a_u)
        c = dict(base); c["f_map"] = zone_map(fd, 0.32, fu)
        d = run(c, 3.5e6, 0.40e6)
        dp = HMMC().port_dp_kPa + r0["dp_man_kPa"] + fd * r0["dp_ch_kPa"] + fd ** 2 * (r0["dp_K_kPa"] + r0["dp_slot_kPa"])
        print(f"| {fd:.1f} | {a_d*fd:.2f} | {fu:.2f} | {d['Tf_die_avg']:.1f} | {d['die_avg']:.1f} | {d['die_max']:.1f} | {d['hbm_max']:.1f} | {dp:.1f} |")
    rc = COOLIT().evaluate(Q_REF, 1.2)
    print(f"(CoolIT-like dP at same flow, 1-D model estimate: {rc['dp_total_kPa']:.1f} kPa; HMMC uniform {r0['dp_total_kPa']:.1f} kPa)")

    # ---------- base thickness x h_eff table (die zone, H-Z2 fluid field, paste 0.05)
    print("\n## Die case dT (avg / max, K) vs base thickness and h_eff; H-Z2 zoning, paste 0.05 cm2K/W, 350 W/cm2")
    print("| base mm | h=100 | h=150 | h=200 | h=250 | h=350 |")
    print("|---:|---:|---:|---:|---:|---:|")
    for t in (1e-3, 2e-3, 3e-3):
        row = f"| {t*1e3:.0f} |"
        for h in (100e3, 150e3, 200e3, 250e3, 350e3):
            c = dict(base); c["t_base"] = t; c["heff_fn"] = (lambda hh: (lambda f: np.full(np.shape(f), hh) if np.ndim(f) else hh))(h)
            d = run(c, 3.5e6, 0.40e6)
            row += f" {d['die_avg']:.1f} / {d['die_max']:.1f} |"
        print(row)

    # ---------- die flux sweep
    print("\n## Die flux sweep (HBM 40 W/cm2, 1.2 LPM/kW of actual power): die case dT max (K) and GPU Tj max (C)")
    print("| die W/cm2 | kW/die | total kW | C-x-U | H-U | H-Z2 | H-Z2f | H-Z2f-LM |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|")
    keys = ["C-x-U  CoolIT-like, flow x (across die then HBM), uniform", "H-U    HMMC 0.1 mm, base 1 mm, uniform flow",
            "H-Z2   HMMC, heat-proportional 3-zone 3.0/0.32/0.04", "H-Z2f  HMMC-fine 0.075 mm, 3-zone", "H-Z2f-LM HMMC-fine 3-zone, liquid-metal die TIM"]
    for qd in (1.5e6, 2.0e6, 2.5e6, 3.0e6, 3.5e6, 4.0e6):
        row = f"| {qd/1e4:.0f} | {qd*DIE_W*DIE_H/1e3:.2f} | "
        first = True
        for k in keys:
            d = run(CONFIGS[k], qd, 0.40e6)
            if first: row += f"{d['Q_kW']:.1f} |"; first = False
            row += f" {d['die_max']:.1f} / {T_IN + d['die_max'] + qd*R_JC_GPU:.0f} |"
        print(row)

    # ---------- stretch 15 kW case
    print("\n## Stretch 15.0 kW: dies 400 W/cm2 (13.7 kW) + HBM 60 W/cm2 (1.27 kW), 18 LPM")
    for k in keys + ["C-y-Z  CoolIT-like, flow y, zoned channels 1.75/0.3/0.1"]:
        d = run(CONFIGS[k], 4.0e6, 0.60e6)
        P = 0.6e6 * HBM_W * HBM_H
        print(f"  {k[:8]}: Q {d['Q_kW']:.2f} kW, die dT avg {d['die_avg']:.1f} / max {d['die_max']:.1f} K (Tj {T_IN+d['die_max']+4e6*R_JC_GPU:.0f} C); "
              f"HBM dT max {d['hbm_max']:.1f} K (Tj {T_IN+d['hbm_max']+P*R_JC_HBM:.0f} C)")

    # ---------- die temperature non-uniformity (gradient across one die)
    print("\n## Across-die case-temperature spread (max-min over the hottest die), K")
    for nm in CONFIGS:
        d = RES[nm]; best = None
        for c in DIES:
            msk = rect(*c, DIE_W, DIE_H); v = d["Tcase"][msk]
            sp = v.max() - v.min(); sp98 = np.percentile(v, 99) - np.percentile(v, 2)
            if best is None or v.max() > best[0]: best = (v.max(), sp, sp98)
        print(f"  {nm[:8]}: max-min {best[1]:.1f} K, p99-p2 {best[2]:.1f} K")

    # save fields for plotting / later use
    np.savez(__import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'nonuniform-heatmap-fields.npz')),
             x=xc, **{k[:8].strip().replace(' ', '_'): v["Tcase"] for k, v in RES.items()})

if __name__ == "__main__":
    main()
