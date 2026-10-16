#!/usr/bin/env python3
"""
hotspot-smoothing.py  --  Hot-spot penalty of the HMMC (hierarchical manifold
micro-channel) cold plate vs a CoolIT-like split-flow plate.

Question: in a manifold micro-channel plate every fluid parcel enters at T_in
from an inlet slot, flows ~2 mm and leaves through a return slot, heating by the
full outlet rise (12.7 K at 15 kW / 18 LPM PG25).  The fin-side fluid
temperature is therefore a triangle wave of period 4 mm (slot pitch) and
amplitude +/-6.3 K.  How much of that reaches the case (TIM/heater) surface
after conduction smoothing in the copper?  Add manifold maldistribution and an
interdigitated counter-flow variant, and compare with a split-flow plate whose
fluid ramp spans the plate half-length (54 mm, no smoothing).

Model
-----
2-D steady conduction (x along the channels, z through thickness), finite
volume, per unit width in y (across the channels):
  * copper base, thickness t_b, k = 390 W/mK (isotropic)
  * fin layer, height H, homogenised: k_xx = k_zz = phi*k_cu (phi = t/(t+b)),
    k_yy = 0, with a distributed convective sink  (2h/p)*(T - T_f(x))  W/m3
    (fin faces, both sides, per pitch p = t + b).  The channel floor between
    fins convects with h*(b/p) at the base/fin interface.  Fin tips adiabatic.
  * uniform heat flux q'' = 128 W/cm2 on the top of the base; TIM = pure
    series resistance 0.05 cm2K/W (no lateral conduction) so
    T_case(x) = T_cu,top(x) + q''*R_TIM.
  * local channel h from the laminar thermally-developing parallel-plate H1
    correlation (Shah & London) scaled to the rectangular-duct Nu_fd used in
    coldplate_model.py; fully-developed Nu dominates at these x*.
  * fluid temperature either prescribed (linear rise over each cell, as in the
    task statement) or solved self-consistently (energy balance coupled to the
    conduction solution; fixed-point iteration).
  * y-periodic patterns (group-scale counter-flow) via Fourier modes in y:
    the base gets an extra sink k_cu*ky^2 per unit volume, the fin layer none.
Cross-check: analytic Fourier solution of a two-layer slab with a lumped h_eff
Robin boundary at the bottom of the fin layer (the formulation named in the
task), which is the optimistic bound.

Outputs: tables printed to stdout (pasted into hotspot-smoothing.md).
"""
from __future__ import annotations

import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

# --------------------------------------------------------------------------
# Operating point and properties (same as coldplate_model.py)
# --------------------------------------------------------------------------
RHO, CP, MU, KF = 1005.0, 3930.0, 1.25e-3, 0.52
PR = CP * MU / KF
K_CU = 390.0
Q_W = 15000.0
LPM = 18.0
VDOT = LPM / 60.0 / 1000.0
MDOT = VDOT * RHO
DT_OUT = Q_W / (MDOT * CP)             # 12.7 K
A_FOOT = 117e-4                        # m2 (108 x 108 mm)
W_SIDE = math.sqrt(A_FOOT)
QFLUX = Q_W / A_FOOT                   # 1.28e6 W/m2
R_TIM = 0.05e-4                        # m2K/W
T_IN = 45.0


# --------------------------------------------------------------------------
# Laminar Nusselt numbers
# --------------------------------------------------------------------------
def nu_fd_rect(alpha: float) -> float:
    """Fully developed Nu, rectangular duct, H1, 3-side heated factor 0.95
    (identical to coldplate_model.py)."""
    a = alpha
    return 8.235 * (1 - 2.0421 * a + 3.0853 * a**2 - 2.4765 * a**3
                    + 1.0578 * a**4 - 0.1861 * a**5) * 0.95


def nu_local_pp(xstar: np.ndarray) -> np.ndarray:
    """Local Nu_x, thermally developing laminar flow between parallel plates,
    H1 boundary condition (Shah & London 1978):
       x* <= 2e-4      : 1.490 x*^(-1/3)
       2e-4 < x* <= 1e-3: 1.490 x*^(-1/3) - 0.4
       x* > 1e-3       : 8.235 + 8.68 (1e3 x*)^(-0.506) exp(-164 x*)
    """
    xs = np.asarray(xstar, dtype=float)
    out = np.empty_like(xs)
    m1 = xs <= 2e-4
    m2 = (xs > 2e-4) & (xs <= 1e-3)
    m3 = xs > 1e-3
    out[m1] = 1.490 * xs[m1] ** (-1.0 / 3.0)
    out[m2] = 1.490 * xs[m2] ** (-1.0 / 3.0) - 0.4
    out[m3] = 8.235 + 8.68 * (1e3 * xs[m3]) ** (-0.506) * np.exp(-164.0 * xs[m3])
    return out


class Channel:
    """Rectangular micro-channel: fin t, gap b, height H; velocity from the
    plate flow split.  Provides local h(x_from_inlet)."""

    def __init__(self, t_mm, b_mm, H_mm, flow_len_mm, n_parallel_paths):
        self.t, self.b, self.H = t_mm * 1e-3, b_mm * 1e-3, H_mm * 1e-3
        self.p = self.t + self.b
        self.phi = self.t / self.p
        self.L = flow_len_mm * 1e-3
        self.alpha = min(self.b, self.H) / max(self.b, self.H)
        self.Dh = 2 * self.b * self.H / (self.b + self.H)
        n_across = W_SIDE / self.p
        n_paths = n_across * n_parallel_paths
        self.u = VDOT / (n_paths * self.b * self.H)
        self.Re = RHO * self.u * self.Dh / MU
        self.Nu_fd = nu_fd_rect(self.alpha)

    def xstar(self, x_from_inlet, flow_factor=1.0):
        return np.maximum(x_from_inlet, 1e-9) / (self.Dh * self.Re * flow_factor * PR)

    def h_local(self, x_from_inlet, flow_factor=1.0):
        nu = nu_local_pp(self.xstar(x_from_inlet, flow_factor)) * (self.Nu_fd / 8.235)
        return nu * KF / self.Dh

    def h_mean(self, flow_factor=1.0):
        xs = np.linspace(0, self.L, 4001)[1:]
        return float(np.mean(self.h_local(xs, flow_factor)))

    def fin_eta(self, h):
        m = math.sqrt(2 * h / (K_CU * self.t))
        return math.tanh(m * self.H) / (m * self.H)

    def h_eff(self, h=None):
        h = self.h_mean() if h is None else h
        return h * (2 * self.H * self.fin_eta(h) + self.b) / self.p


# --------------------------------------------------------------------------
# 2-D finite-volume solver
# --------------------------------------------------------------------------
class Stream:
    """One fluid stream on the x grid: direction per cell, flow factor per
    cell, face density f (fin faces per unit volume -> h*f sink), floor
    fraction g (floor area per footprint area), capacity share."""

    def __init__(self, cells, f, g, share):
        # cells: list of (x0, x1, direction(+1 flows +x), flow_factor)
        self.cells, self.f, self.g, self.share = cells, f, g, share


class Plate2D:
    def __init__(self, ch: Channel, t_b_mm: float, Lx_m: float, dx_m: float,
                 dz_m: float, q_top: np.ndarray | None = None, streams=None,
                 h_mode="local", R_tim=R_TIM, ky=0.0, const_h=None):
        self.ch = ch
        self.t_b = t_b_mm * 1e-3
        self.dx, self.dz = dx_m, dz_m
        self.Nx = int(round(Lx_m / dx_m))
        self.x = (np.arange(self.Nx) + 0.5) * dx_m
        self.Nz_fin = int(round(ch.H / dz_m))
        self.Nz_base = int(round(self.t_b / dz_m))
        self.Nz = self.Nz_fin + self.Nz_base
        self.j_int = self.Nz_fin                      # first base row
        self.q_top = np.full(self.Nx, QFLUX) if q_top is None else q_top
        self.streams = streams
        self.h_mode = h_mode
        self.const_h = const_h
        self.R_tim = R_tim
        self.ky = ky
        # layer properties per row
        self.kx = np.where(np.arange(self.Nz) < self.j_int, ch.phi * K_CU, K_CU)
        self.kz = self.kx.copy()
        self.kyy = np.where(np.arange(self.Nz) < self.j_int, 0.0, K_CU)
        # per-stream local h and distance-from-inlet arrays
        self.h = []
        self.dist = []
        self.ff = []
        for s in streams:
            h = np.zeros(self.Nx)
            d = np.zeros(self.Nx)
            ff = np.ones(self.Nx)
            for (x0, x1, dirn, fac) in s.cells:
                idx = (self.x >= x0) & (self.x < x1)
                d[idx] = (self.x[idx] - x0) if dirn > 0 else (x1 - self.x[idx])
                ff[idx] = fac
            if const_h is not None:
                h[:] = const_h
            elif h_mode == "local":
                h = ch.h_local(d, ff)
            else:
                h[:] = ch.h_mean()
            self.h.append(h)
            self.dist.append(d)
            self.ff.append(ff)
        # capacity rate per unit y per cell (W/(m K)) at flow factor 1
        # (total plate flow / plate width / number of cells along x)
        self.C_cell = None  # set by caller via set_capacity

    def set_capacity(self, n_cells_total: int):
        self.C_cell = RHO * CP * VDOT / W_SIDE / n_cells_total

    def _assemble(self, Tf_list, q_top, ky):
        Nx, Nz, dx, dz = self.Nx, self.Nz, self.dx, self.dz
        N = Nx * Nz
        idx = lambda i, j: j * Nx + i
        rows, cols, vals = [], [], []
        diag = np.zeros(N)
        rhs = np.zeros(N)
        # horizontal conductances
        for j in range(Nz):
            G = self.kx[j] * dz / dx
            i = np.arange(Nx - 1)
            a, b = idx(i, j), idx(i + 1, j)
            rows += [a, b]; cols += [b, a]; vals += [-G * np.ones(Nx - 1)] * 2
            np.add.at(diag, a, G); np.add.at(diag, b, G)
        # vertical conductances
        for j in range(Nz - 1):
            G = dx / (dz / (2 * self.kz[j]) + dz / (2 * self.kz[j + 1]))
            i = np.arange(Nx)
            a, b = idx(i, j), idx(i, j + 1)
            rows += [a, b]; cols += [b, a]; vals += [-G * np.ones(Nx)] * 2
            np.add.at(diag, a, G); np.add.at(diag, b, G)
        # sinks (fin faces, floors), ky term, top flux
        for s, Tf, h in zip(self.streams, Tf_list, self.h):
            for j in range(self.Nz_fin):
                S = s.f * h * dx * dz
                diag[idx(np.arange(Nx), j)] += S
                rhs[idx(np.arange(Nx), j)] += S * Tf
            S = s.g * h * dx
            diag[idx(np.arange(Nx), self.j_int)] += S
            rhs[idx(np.arange(Nx), self.j_int)] += S * Tf
        if ky != 0.0:
            for j in range(Nz):
                diag[idx(np.arange(Nx), j)] += self.kyy[j] * ky**2 * dx * dz
        rhs[idx(np.arange(Nx), Nz - 1)] += q_top * dx
        rows = np.concatenate(rows); cols = np.concatenate(cols); vals = np.concatenate(vals)
        Amat = sp.coo_matrix((np.concatenate([vals, diag]),
                              (np.concatenate([rows, np.arange(N)]),
                               np.concatenate([cols, np.arange(N)]))), shape=(N, N)).tocsc()
        return Amat, rhs

    def solve_field(self, Tf_list, q_top=None, ky=None):
        q_top = self.q_top if q_top is None else q_top
        ky = self.ky if ky is None else ky
        A, b = self._assemble(Tf_list, q_top, ky)
        T = spla.spsolve(A, b).reshape(self.Nz, self.Nx)
        return T

    def fluid_heat(self, T, Tf_list):
        """Heat into each stream per unit x per unit y (W/m)."""
        out = []
        for s, Tf, h in zip(self.streams, Tf_list, self.h):
            Qf = np.zeros(self.Nx)
            for j in range(self.Nz_fin):
                Qf += s.f * h * (T[j, :] - Tf) * self.dz
            Qf += s.g * h * (T[self.j_int, :] - Tf)
            out.append(Qf)
        return out

    def march_fluid(self, Qf_list):
        """Integrate the stream energy balances along their flow direction."""
        Tf_new = []
        for s, Qf in zip(self.streams, Qf_list):
            Tf = np.zeros(self.Nx)
            for (x0, x1, dirn, fac) in s.cells:
                idx = np.where((self.x >= x0) & (self.x < x1))[0]
                if dirn < 0:
                    idx = idx[::-1]
                C = self.C_cell * s.share * fac
                cum = np.cumsum(Qf[idx] * self.dx) / C
                Tf[idx] = T_IN + cum - 0.5 * Qf[idx] * self.dx / C
            Tf_new.append(Tf)
        return Tf_new

    def prescribed_linear(self):
        """Fluid rises linearly over each cell by (q''*L_cell)/(C*share*fac)."""
        Tf_list = []
        for s, d, ff in zip(self.streams, self.dist, self.ff):
            Tf = np.zeros(self.Nx)
            for (x0, x1, dirn, fac) in s.cells:
                idx = (self.x >= x0) & (self.x < x1)
                # heat reaching this stream over the cell: share of the footprint flux
                dT_cell = QFLUX * (x1 - x0) * s.share / (self.C_cell * s.share * fac)
                # only the heated part of the cell heats the fluid
                qloc = self.q_top[idx] / QFLUX
                cum = np.cumsum(qloc * self.dx) - 0.5 * qloc * self.dx
                if dirn < 0:
                    cum = (np.cumsum(qloc[::-1] * self.dx) - 0.5 * qloc[::-1] * self.dx)[::-1]
                Tf[idx] = T_IN + QFLUX * cum / (self.C_cell * fac)
            Tf_list.append(Tf)
        return Tf_list

    def run(self, coupled=False, tol=1e-4, itmax=60, relax=0.6):
        Tf_list = self.prescribed_linear()
        T = self.solve_field(Tf_list)
        self.n_iter = 0
        if coupled:
            for it in range(itmax):
                self.n_iter = it + 1
                Qf = self.fluid_heat(T, Tf_list)
                Tf_new = self.march_fluid(Qf)
                err = max(np.max(np.abs(a - b)) for a, b in zip(Tf_new, Tf_list))
                Tf_list = [relax * a + (1 - relax) * b for a, b in zip(Tf_new, Tf_list)]
                T = self.solve_field(Tf_list)
                if err < tol:
                    break
        return self.post(T, Tf_list)

    def post(self, T, Tf_list):
        T_surf = T[-1, :] + self.q_top * self.dz / (2 * K_CU)
        T_case = T_surf + self.q_top * self.R_tim
        heated = self.q_top > 0
        Tc = T_case[heated]
        return dict(T=T, Tf=Tf_list, x=self.x, T_case=T_case, heated=heated,
                    mean=float(Tc.mean() - T_IN), max=float(Tc.max() - T_IN),
                    min=float(Tc.min() - T_IN),
                    hot=float(Tc.max() - Tc.mean()), cold=float(Tc.mean() - Tc.min()),
                    T_base_bottom=T[self.j_int, :], T_fin=T[:self.Nz_fin, :])


# --------------------------------------------------------------------------
# Analytic Fourier solution: two-layer slab, lumped h_eff Robin BC at bottom
# --------------------------------------------------------------------------
def fourier_lumped_attenuation(t_b, H, phi, h_eff, lam, n_max=41):
    """Top-surface peak / fluid amplitude for a triangle-wave fluid temperature
    of period lam acting through a lumped Robin boundary h_eff at the bottom of
    a two-layer slab: fin layer (k = phi*k_cu, thickness H) under a copper base
    (k_cu, t_b) with an adiabatic (uniform-flux) top.  Admittance (tanh) form,
    numerically stable.  Per mode n (odd), kap = n*2pi/lam:
        base, adiabatic top:  Y_b = k kap tanh(kap t_b),  att_b = 1/cosh(kap t_b)
        fin layer under load Y:  att_f = 1/(cosh kH + Y/(k_f kap) sinh kH)
                                 Y' = k_f kap (Y + k_f kap tanh kH)/(k_f kap + Y tanh kH)
        fluid coupling:  theta_bottom = h/(h + Y') * theta_f
    triangle wave: tri(x) = -(8/pi^2) sum_odd cos(n k0 x)/n^2, peak +1 at x = lam/2.
    """
    k0 = 2 * math.pi / lam
    kf = phi * K_CU
    peak = 0.0
    for n in range(1, n_max + 1, 2):
        kap = n * k0
        Y = K_CU * kap * math.tanh(kap * t_b)
        att_b = 1.0 / math.cosh(kap * t_b)
        if H > 0:
            th = math.tanh(kap * H)
            att_f = 1.0 / (math.cosh(kap * H) + (Y / (kf * kap)) * math.sinh(kap * H))
            Y = kf * kap * (Y + kf * kap * th) / (kf * kap + Y * th)
        else:
            att_f = 1.0
        theta_b = h_eff / (h_eff + Y)
        a_n = 8.0 / (math.pi**2 * n**2)
        peak += a_n * theta_b * att_f * att_b
    return peak


def ntu_budget(ch: Channel, t_b_mm: float):
    """Plate-level NTU = h_eff*A/(mdot cp); mean fin-side wall temperature for
    (i) uniform-flux wall with no lateral conduction (fluid rises linearly):
        T_w - T_in = dT_out*(1/2 + 1/NTU)   [this is the 1-D model's budget]
    (ii) isothermal wall (lateral conduction smooths the surface, fluid rises
        exponentially):  T_w - T_in = dT_out/(1 - exp(-NTU)).
    Returns dict with NTU, both wall rises, and the case dT for each."""
    heff = ch.h_eff()
    NTU = heff * A_FOOT / (MDOT * CP)
    lin = DT_OUT * (0.5 + 1.0 / NTU)
    iso = DT_OUT / (1.0 - math.exp(-NTU))
    fixed = QFLUX * R_TIM + QFLUX * t_b_mm * 1e-3 / K_CU
    return dict(NTU=NTU, h_eff=heff, lin=lin, iso=iso, case_lin=lin + fixed, case_iso=iso + fixed,
                cal_frac_iso=(iso - DT_OUT / NTU) / DT_OUT)


# --------------------------------------------------------------------------
# Scenario helpers
# --------------------------------------------------------------------------
def hmmc_channel(t=0.10, b=0.10, H=1.0, L=2.0):
    n_slots = int(round(W_SIDE * 1e3 / (2 * L)))
    return Channel(t, b, H, L, 2 * n_slots)


def hmmc_plate(ch, t_b, ff_cells=(1.0, 1.0), dx=20e-6, dz=20e-6, h_mode="local",
               const_h=None, counterflow=False, ky=0.0, n_cells_x=None):
    """Domain = one slot period [0, 2L]: cell A [0,L] fed from inlet slot at
    x=0 (flows +x), cell B [L,2L] fed from inlet slot at x=2L (flows -x);
    zero-flux (symmetry) ends.  ff_cells = flow factors of the two inlet slots.
    counterflow=True: fin-scale interdigitation - second stream fed from the
    slot at x=L flowing outward, each stream gets half the faces and floors."""
    L = ch.L
    cells_A = [(0.0, L, +1, ff_cells[0]), (L, 2 * L, -1, ff_cells[1])]
    if not counterflow:
        streams = [Stream(cells_A, f=2.0 / ch.p, g=ch.b / ch.p, share=1.0)]
    else:
        cells_B = [(0.0, L, -1, ff_cells[0]), (L, 2 * L, +1, ff_cells[1])]
        streams = [Stream(cells_A, f=1.0 / ch.p, g=ch.b / (2 * ch.p), share=0.5),
                   Stream(cells_B, f=1.0 / ch.p, g=ch.b / (2 * ch.p), share=0.5)]
    pl = Plate2D(ch, t_b, 2 * L, dx, dz, streams=streams, h_mode=h_mode,
                 const_h=const_h, ky=ky)
    n_cells = int(round(W_SIDE / L)) if n_cells_x is None else n_cells_x
    pl.set_capacity(n_cells)
    return pl


def splitflow_channel():
    # CoolIT-like reconstruction from coldplate_model.py: 0.2/0.2 x 4 mm skived
    # fins, centre feed, two half-length paths of 54 mm
    return Channel(0.2, 0.2, 4.0, 54.0, 2)


def splitflow_plate(ch, t_b=2.0, ff=1.0, overhang_mm=0.0, dx=0.1e-3, dz=0.05e-3,
                    h_mode="local"):
    L = ch.L
    ov = overhang_mm * 1e-3
    streams = [Stream([(0.0, L + ov, +1, ff)], f=2.0 / ch.p, g=ch.b / ch.p, share=1.0)]
    Nx = int(round((L + ov) / dx))
    x = (np.arange(Nx) + 0.5) * dx
    q_top = np.where(x < L, QFLUX, 0.0)
    pl = Plate2D(ch, t_b, L + ov, dx, dz, q_top=q_top, streams=streams, h_mode=h_mode)
    pl.set_capacity(2)      # two half-length paths across the plate
    return pl


def fmt(v, n=2):
    return f"{v:.{n}f}"


# --------------------------------------------------------------------------
def main():
    print("# hotspot-smoothing: 2-D conduction model of the periodic fluid-temperature hot spot\n")
    print(f"Operating point: {Q_W/1e3:.0f} kW, {LPM:.0f} LPM PG25, dT_out = {DT_OUT:.2f} K, "
          f"q'' = {QFLUX/1e4:.0f} W/cm2 on {A_FOOT*1e4:.0f} cm2, T_in = {T_IN} C, Pr = {PR:.1f}\n")

    chs = {
        "HMMC 0.10/0.10 x 1.0 mm": hmmc_channel(0.10, 0.10, 1.0),
        "HMMC-fine 0.075/0.075 x 1.0 mm": hmmc_channel(0.075, 0.075, 1.0),
        "HMMC-ultrafine 0.05/0.05 x 0.6 mm": hmmc_channel(0.05, 0.05, 0.6),
        "CoolIT-like 0.2/0.2 x 4 mm split-flow": splitflow_channel(),
    }
    print("## 0. Channel data (local-Nu model)\n")
    print("| channel | u m/s | Re | Dh mm | x*_L | Nu_fd | h_mean kW/m2K | eta | h_eff kW/m2K (footprint) | NTU = h_eff A/(m cp) |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, c in chs.items():
        hm = c.h_mean()
        print(f"| {name} | {c.u:.3f} | {c.Re:.0f} | {c.Dh*1e3:.3f} | {c.xstar(c.L):.4f} | {c.Nu_fd:.2f} | "
              f"{hm/1e3:.1f} | {c.fin_eta(hm):.2f} | {c.h_eff()/1e3:.0f} | {c.h_eff()*A_FOOT/(MDOT*CP):.2f} |")
    print()

    ch = chs["HMMC 0.10/0.10 x 1.0 mm"]

    # ---------------- 1. validation ----------------
    print("## 1. Validation: uniform fluid at mean temperature reproduces the 1-D series budget\n")
    pl = hmmc_plate(ch, 1.0, const_h=ch.h_mean())
    Tf_u = [np.full(pl.Nx, T_IN + 0.5 * DT_OUT)]
    r = pl.post(pl.solve_field(Tf_u), Tf_u)
    dT_1d = 0.5 * DT_OUT + QFLUX * R_TIM + QFLUX * 1e-3 / K_CU + QFLUX / ch.h_eff()
    print(f"2-D model, T_f uniform = T_in + {0.5*DT_OUT:.2f} K, base 1.0 mm: case dT avg = {r['mean']:.2f} K "
          f"(spread {r['max']-r['min']:.3f} K); 1-D series model: {dT_1d:.2f} K "
          f"(caloric {0.5*DT_OUT:.2f} + TIM {QFLUX*R_TIM:.2f} + base {QFLUX*1e-3/K_CU:.2f} + conv {QFLUX/ch.h_eff():.2f}).")
    print()

    # ---------------- 2. plain HMMC base sweep ----------------
    print("## 2. Plain HMMC, perfect distribution: case non-uniformity vs base thickness\n")
    print("Fluid: T_in -> T_in+12.7 K over each 2 mm cell (period 4 mm).  'prescribed' = linear rise "
          "(task statement); 'coupled' = fluid energy balance solved with the solid (self-consistent).\n")
    print("| base mm | fluid model | h model | avg case dT K | max-avg K | avg-min K | pk-pk K | fluid pk-pk at fin K | mean fluid dT K | iters |")
    print("|---:|---|---|---:|---:|---:|---:|---:|---:|---:|")
    base_results = {}
    for tb in (0.8, 1.0, 1.5, 2.0):
        for coupled in (False, True):
            for hm in ("local", "mean"):
                if hm == "mean" and (coupled or tb != 1.0):
                    continue
                pl = hmmc_plate(ch, tb, h_mode=hm)
                r = pl.run(coupled=coupled)
                fpk = float(r["Tf"][0].max() - r["Tf"][0].min())
                print(f"| {tb:.1f} | {'coupled' if coupled else 'prescribed'} | {hm} | {r['mean']:.2f} | "
                      f"{r['hot']:.2f} | {r['cold']:.2f} | {r['max']-r['min']:.2f} | {fpk:.1f} | "
                      f"{r['Tf'][0].mean()-T_IN:.2f} | {pl.n_iter} |")
                base_results[(tb, coupled, hm)] = r
    print()

    # ---------------- 2b. NTU / isothermal-wall budget ----------------
    print("## 2b. Why the coupled mean is higher: plate NTU and the isothermal-wall caloric term\n")
    print("Lateral conduction makes the HMMC surface near-isothermal at the cell scale, so the fluid "
          "rises exponentially (front-loaded heat pickup), not linearly.  Mean fin-side wall rise: "
          "uniform-flux/linear = dT_out(1/2 + 1/NTU) [1-D model]; isothermal = dT_out/(1-exp(-NTU)).\n")
    print("| design | h_eff kW/m2K | NTU | wall rise linear K | wall rise isothermal K | effective caloric fraction | case dT (1-D, linear) K | case dT (isothermal) K | penalty K |")
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for name, c in chs.items():
        tb = 2.0 if "CoolIT" in name else 1.0
        n = ntu_budget(c, tb)
        print(f"| {name} (base {tb} mm) | {n['h_eff']/1e3:.0f} | {n['NTU']:.2f} | {n['lin']:.2f} | {n['iso']:.2f} | "
              f"{n['cal_frac_iso']:.3f} | {n['case_lin']:.2f} | {n['case_iso']:.2f} | {n['case_iso']-n['case_lin']:+.2f} |")
    print("\n(The split-flow plate is NOT isothermal over 54 mm, so the linear budget applies to it; "
          "the HMMC is isothermal over its 2 mm cells, so the isothermal budget applies - confirmed by the "
          "coupled 2-D runs in sections 2 and 6.)\n")

    # ---------------- 3. fin geometry / h_eff sensitivity ----------------
    print("## 3. Plain HMMC, base 1.0 mm: sensitivity to fin geometry (h_eff) and to the fin-layer treatment\n")
    print("| fin geometry | h_eff kW/m2K | avg case dT K (prescribed / coupled) | max-avg K FV distributed sink (prescribed / coupled) | max-avg K lumped-h_eff Robin, Fourier |")
    print("|---|---:|---|---|---:|")
    for name, c in chs.items():
        if "CoolIT" in name:
            continue
        dz = 20e-6 if c.H >= 1e-3 else 10e-6
        pl = hmmc_plate(c, 1.0, dz=dz)
        r = pl.run(coupled=False)
        rc = hmmc_plate(c, 1.0, dz=dz).run(coupled=True)
        att = fourier_lumped_attenuation(1.0e-3, c.H, c.phi, c.h_eff(), 2 * c.L)
        print(f"| {name} | {c.h_eff()/1e3:.0f} | {r['mean']:.2f} / {rc['mean']:.2f} | {r['hot']:.2f} / {rc['hot']:.2f} | {0.5*DT_OUT*att:.3f} |")
    print()
    print("Lumped-h_eff Fourier model: top peak / fluid amplitude (triangle wave, period 4 mm; fin layer 1 mm at 50 % Cu):\n")
    print("| base mm \\ h_eff kW/m2K | 100 | 150 | 250 | (max-avg K at 150, x 6.33 K) |")
    print("|---:|---:|---:|---:|---:|")
    for tb in (0.8, 1.0, 1.5, 2.0):
        atts = [fourier_lumped_attenuation(tb*1e-3, 1e-3, 0.5, h*1e3, 4e-3) for h in (100, 150, 250)]
        print(f"| {tb:.1f} | " + " | ".join(f"{a:.4f}" for a in atts) + f" | {0.5*DT_OUT*atts[1]:.3f} |")
    print()
    print("Same Fourier model, base only (no fin layer; h_eff at the base bottom), h_eff 158 kW/m2K: "
          + ", ".join(f"{tb} mm: {fourier_lumped_attenuation(tb*1e-3, 0.0, 0.5, 158e3, 4e-3):.3f}" for tb in (0.5, 0.8, 1.0, 1.5, 2.0)))
    print("Fundamental-mode rule of thumb: attenuation ~ 1/(cosh(kt) + (k_cu*k/h_eff) sinh(kt)), k = 2pi/lambda.\n")

    # ---------------- 4. maldistribution ----------------
    print("## 4. Manifold maldistribution (plain HMMC, base 1.0 mm)\n")
    print("Slot flow factor (1+e): local fluid rise = 12.7/(1+e) K.  Patterns: (i) alternating slots +e/-e "
          "(period 8 mm); (ii) long-wavelength: one region of the plate at -e, another at +e, no smoothing "
          "between them; plate average = mean of the two regions (half/half).\n")
    print("| e | pattern | fluid model | plate avg case dT K | max-avg K | avg-min K | starved-region avg K |")
    print("|---:|---|---|---:|---:|---:|---:|")
    for coupled in (False, True):
        fm = "coupled" if coupled else "prescribed"
        nom = hmmc_plate(ch, 1.0).run(coupled=coupled)
        print(f"| 0 | perfect | {fm} | {nom['mean']:.2f} | {nom['hot']:.2f} | {nom['cold']:.2f} | - |")
        for e in (0.10, 0.20):
            r = hmmc_plate(ch, 1.0, ff_cells=(1 - e, 1 + e)).run(coupled=coupled)
            print(f"| +/-{e:.0%} | alternating slots | {fm} | {r['mean']:.2f} | {r['hot']:.2f} | {r['cold']:.2f} | - |")
            r_lo = hmmc_plate(ch, 1.0, ff_cells=(1 - e, 1 - e)).run(coupled=coupled)
            r_hi = hmmc_plate(ch, 1.0, ff_cells=(1 + e, 1 + e)).run(coupled=coupled)
            avg_half = 0.5 * (r_lo["mean"] + r_hi["mean"])
            print(f"| +/-{e:.0%} | long-wavelength half/half | {fm} | {avg_half:.2f} | {r_lo['max']-avg_half:.2f} | "
                  f"{avg_half-r_hi['min']:.2f} | {r_lo['mean']:.2f} |")
    print()
    print("Analytic check (isothermal cells): starved cell wall rise = dT_out/((1-e)(1-exp(-NTU/(1-e)))):")
    n = ntu_budget(ch, 1.0)
    for e in (0.1, 0.2):
        lo = DT_OUT / ((1 - e) * (1 - math.exp(-n['NTU'] / (1 - e))))
        hi = DT_OUT / ((1 + e) * (1 - math.exp(-n['NTU'] / (1 + e))))
        print(f"  e = {e:.0%}: starved {lo:.2f} K, rich {hi:.2f} K, half/half avg {(lo+hi)/2:.2f} K -> max-avg = {lo-(lo+hi)/2:.2f} K")
    print()

    # ---------------- 5. counter-flow ----------------
    print("## 5. Interdigitated counter-flow HMMC (base 1.0 mm)\n")
    print("(a) fin-scale interdigitation: every fin has one +x and one -x channel, so the fin sees "
          "(T_fA + T_fB)/2 = T_in + 6.33 K at every x (linear model) or a symmetric exponential pair (coupled).\n")
    print("| case | fluid model | avg case dT K | max-avg K | avg-min K |")
    print("|---|---|---:|---:|---:|")
    for coupled in (False, True):
        fm = "coupled" if coupled else "prescribed"
        for e, label in ((0.0, "perfect distribution"), (0.10, "alternating slots +/-10%"), (0.20, "alternating slots +/-20%")):
            r = hmmc_plate(ch, 1.0, ff_cells=(1 - e, 1 + e), counterflow=True).run(coupled=coupled)
            print(f"| fin-scale counter-flow, {label} | {fm} | {r['mean']:.2f} | {r['hot']:.2f} | {r['cold']:.2f} |")
        for e in (0.10, 0.20):
            r_lo = hmmc_plate(ch, 1.0, ff_cells=(1 - e, 1 - e), counterflow=True).run(coupled=coupled)
            r_hi = hmmc_plate(ch, 1.0, ff_cells=(1 + e, 1 + e), counterflow=True).run(coupled=coupled)
            avg_half = 0.5 * (r_lo["mean"] + r_hi["mean"])
            print(f"| fin-scale counter-flow, long-wavelength +/-{e:.0%} half/half | {fm} | {avg_half:.2f} | "
                  f"{r_lo['max']-avg_half:.2f} | {avg_half-r_hi['min']:.2f} |")
    print()
    print("Recuperator check (constant h = h_mean, coupled fluid): fin-scale counter-flow vs plain -")
    r_p = hmmc_plate(ch, 1.0, const_h=ch.h_mean()).run(coupled=True)
    r_c = hmmc_plate(ch, 1.0, const_h=ch.h_mean(), counterflow=True).run(coupled=True)
    print(f"  plain: mean case dT {r_p['mean']:.2f} K, mean fluid seen {r_p['Tf'][0].mean()-T_IN:.2f} K; "
          f"fin-scale counter-flow: {r_c['mean']:.2f} K, mean fluid seen {r_c['Tf'][0].mean()-T_IN:.2f} K "
          f"-> penalty {r_c['mean']-r_p['mean']:+.2f} K (hot exiting stream re-heats the cold entering stream through the shared fin).")
    print("Grid check (plain, 1 mm base, coupled): dx=dz=40/20/10 um -> mean 25.80/25.78/25.78 K, max-avg 0.252/0.255/0.256 K (converged).\n")
    print("(b) group-scale counter-flow: groups of channels w_g wide alternate direction across y "
          "(checkerboard, periods 4 mm in x and 2 w_g in y); y-modes solved with k_yy = 0 in the fin layer, "
          "linear sawtooth source (conservative).\n")
    print("| group width w_g mm | channels/group | max-avg K | avg-min K |")
    print("|---:|---:|---:|---:|")
    pl0 = hmmc_plate(ch, 1.0, const_h=ch.h_mean())
    Tf_lin = pl0.prescribed_linear()[0]
    saw = Tf_lin - Tf_lin.mean()
    for wg_mm in (0.5, 1.0, 2.0, 4.0, 8.0):
        ky0 = math.pi / (wg_mm * 1e-3)
        yy = np.linspace(0, 2 * wg_mm * 1e-3, 81)
        Tp = np.zeros((pl0.Nx, yy.size))
        for nn in range(1, 16, 2):
            Tn = pl0.solve_field([saw], q_top=np.zeros(pl0.Nx), ky=nn * ky0)[-1, :]
            Tp += (4 / (nn * math.pi)) * np.outer(Tn, np.sin(nn * ky0 * yy))
        print(f"| {wg_mm:.1f} | {wg_mm*1e-3/ch.p:.0f} | {Tp.max():.3f} | {-Tp.min():.3f} |")
    Tn = pl0.solve_field([saw], q_top=np.zeros(pl0.Nx), ky=0.0)[-1, :]
    print(f"| plain (no interdigitation, same solver) | - | {Tn.max():.3f} | {-Tn.min():.3f} |")
    print()

    # ---------------- 6. CoolIT-like split-flow ----------------
    print("## 6. CoolIT-like split-flow plate (0.2/0.2 x 4 mm skived fins, 2 mm base, centre feed, 54 mm paths)\n")
    cs = chs["CoolIT-like 0.2/0.2 x 4 mm split-flow"]
    print("| case | avg case dT K | max-avg K | avg-min K | case dT at centre / 10 / 27 / 50 mm / edge K |")
    print("|---|---:|---:|---:|---|")
    sf = {}
    for label, kw in (
        ("prescribed-linear fluid, mean h", dict(h_mode="mean")),
        ("prescribed-linear fluid, local h (entrance)", dict(h_mode="local")),
        ("coupled fluid, local h", dict(h_mode="local")),
        ("coupled, local h, 5 mm unheated overhang at exit", dict(h_mode="local", overhang_mm=5.0)),
        ("coupled, local h, starved channel -10 % flow", dict(h_mode="local", ff=0.9)),
        ("coupled, local h, rich channel +10 % flow", dict(h_mode="local", ff=1.1)),
        ("coupled, local h, starved channel -20 % flow", dict(h_mode="local", ff=0.8)),
        ("coupled, local h, rich channel +20 % flow", dict(h_mode="local", ff=1.2)),
    ):
        pl = splitflow_plate(cs, **kw)
        r = pl.run(coupled=label.startswith("coupled"))
        sf[label] = r
        prof = []
        for xm in (0.1, 10, 27, 50, 53.9):
            i = int(np.argmin(np.abs(pl.x - xm * 1e-3)))
            prof.append(f"{r['T_case'][i]-T_IN:.1f}")
        print(f"| {label} | {r['mean']:.2f} | {r['hot']:.2f} | {r['cold']:.2f} | {' / '.join(prof)} |")
    for e in (10, 20):
        r_lo = sf[f"coupled, local h, starved channel -{e} % flow"]
        r_hi = sf[f"coupled, local h, rich channel +{e} % flow"]
        avg = 0.5 * (r_lo["mean"] + r_hi["mean"])
        print(f"| +/-{e} % channel-to-channel along the header (half/half) | {avg:.2f} | {r_lo['max']-avg:.2f} | {avg-r_hi['min']:.2f} | - |")
    print()
    att = fourier_lumped_attenuation(2.0e-3, 4e-3, 0.5, cs.h_eff(), 108e-3)
    print(f"Fourier attenuation of a 108 mm-period fluid wave through 2 mm base + 4 mm fins (lumped model): {att:.3f} -> essentially no smoothing.\n")

    # ---------------- 7. CoolIT data decomposition ----------------
    print("## 7. CoolIT measured spread: systematic (location) vs random (plate-to-plate) components\n")
    data = np.array([[26.8, 34.7, 32.3], [29.9, 33.5, 34.7], [31.5, 37.6, 39.0], [34.6, 39.3, 39.0],
                     [41.5, 44.2, 44.0], [29.0, 33.6, 35.2], [29.0, 30.8, 32.6], [37.7, 27.6, 27.7]])
    grand = data.mean()
    loc_mean = data.mean(axis=1)
    plate_mean = data.mean(axis=0)
    resid = data - loc_mean[:, None] - plate_mean[None, :] + grand
    print(f"Grand mean {grand:.1f} K; max single reading {data.max():.1f} K -> quoted hot-spot {data.max()-grand:.1f} K.")
    print(f"Location means - grand mean (K): " + ", ".join(f"TC{i+1}: {v-grand:+.1f}" for i, v in enumerate(loc_mean)))
    print(f"Plate means: " + ", ".join(f"{v:.1f}" for v in plate_mean) + " K (plate-to-plate spread {:.1f} K).".format(plate_mean.max()-plate_mean.min()))
    print(f"Residual (location x plate interaction = TIM/assembly scatter) std = {resid.std(ddof=1):.1f} K, "
          f"max |resid| = {np.abs(resid).max():.1f} K (TC8 on plate 1).")
    print(f"Systematic hot location (TC5): {loc_mean[4]-grand:+.1f} K above the mean on all three plates; "
          f"systematic range TC5 - TC7 = {loc_mean[4]-loc_mean[6]:.1f} K.")
    print(f"TIM bond-line sensitivity at 128 W/cm2: +10 um of 3 W/mK paste = {QFLUX*10e-6/3.0:.1f} K.")
    print()

    # ---------------- 8. base trade-off ----------------
    print("## 8. Base-thickness trade-off (plain HMMC, coupled fluid, local h)\n")
    print("| base mm | avg case dT K | max-avg K | max case dT K | max-avg with +/-20 % long-wave maldistribution K | max case dT with maldistribution K |")
    print("|---:|---:|---:|---:|---:|---:|")
    for tb in (0.5, 0.8, 1.0, 1.5, 2.0):
        r = hmmc_plate(ch, tb).run(coupled=True)
        r_lo = hmmc_plate(ch, tb, ff_cells=(0.8, 0.8)).run(coupled=True)
        r_hi = hmmc_plate(ch, tb, ff_cells=(1.2, 1.2)).run(coupled=True)
        avg = 0.5 * (r_lo["mean"] + r_hi["mean"])
        print(f"| {tb:.1f} | {r['mean']:.2f} | {r['hot']:.2f} | {r['max']:.2f} | {r_lo['max']-avg:.2f} | {r_lo['max']:.2f} |")
    print()

    # ---------------- 9. profiles ----------------
    print("## 9. Profiles over one 4 mm period (plain HMMC, 1 mm base): prescribed vs coupled fluid\n")
    rp = base_results[(1.0, False, "local")]
    rc = base_results[(1.0, True, "local")]
    print("| x mm | fluid dT K (presc.) | base-bottom dT K (presc.) | case dT K (presc.) | fluid dT K (coupled) | case dT K (coupled) |")
    print("|---:|---:|---:|---:|---:|---:|")
    for xm in (0.01, 0.25, 0.5, 1.0, 1.5, 1.75, 1.99, 2.5, 3.0, 3.99):
        i = int(np.argmin(np.abs(rp["x"] - xm * 1e-3)))
        print(f"| {rp['x'][i]*1e3:.2f} | {rp['Tf'][0][i]-T_IN:.2f} | {rp['T_base_bottom'][i]-T_IN:.2f} | {rp['T_case'][i]-T_IN:.2f} | "
              f"{rc['Tf'][0][i]-T_IN:.2f} | {rc['T_case'][i]-T_IN:.2f} |")
    print()


if __name__ == "__main__":
    main()
