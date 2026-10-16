#!/usr/bin/env python3
"""Fast multilayer spreading model (double Fourier cosine series, adiabatic cell walls, uniform h_eff on the
wetted face) for one SiC switch cell. Exact for full-extent layers; die + die-attach added as 1-D over die area.
Cross-checked against the 3-D finite-volume model (pe_stack.py, 0.5 mm grid, with a 2 mm substrate margin)."""
import numpy as np

K_CU, K_AL, K_SIC, K_SN, K_AG, K_SOLDER, K_ALN, K_AL2O3 = 390., 200., 300., 90., 150., 50., 170., 24.

CELL_A, CELL_B = 40.0e-3, 35.0e-3            # one switch cell, m (14 cm2)
DIE_CENTRES_X = (-9.75, -3.25, 3.25, 9.75)   # mm from cell centre (6.5 mm pitch)
DIE_CENTRES_Y = (-3.25, 3.25)                # mm (6.5 mm pitch)
DIE = 4.5                                    # mm (8 dies -> 1.62 cm2 SiC per switch)
R_DIE = 0.18e-3 / K_SIC + 0.04e-3 / K_AG     # SiC die + Ag die attach, m2K/W (1-D over die area)


def patches(die_scale=1.0):
    d = DIE * np.sqrt(die_scale) * 1e-3
    P = []
    for cx in DIE_CENTRES_X:
        for cy in DIE_CENTRES_Y:
            x0 = CELL_A / 2 + cx * 1e-3
            y0 = CELL_B / 2 + cy * 1e-3
            P.append((x0 - d / 2, x0 + d / 2, y0 - d / 2, y0 + d / 2))
    return P


def Z_stack(beta, layers, h):
    """Surface impedance T/q (m2K/W) at the top of 'layers' (bottom->top list of (t m, k)) over h at the bottom."""
    Z = np.full_like(beta, 1.0 / h, dtype=float)
    for t, k in layers:
        with np.errstate(divide="ignore", invalid="ignore"):
            th = np.tanh(beta * t)
            Zn = (Z + th / (k * beta)) / (1 + k * beta * Z * th)
        Z = np.where(beta == 0, Z + t / k, Zn)
    return Z


def _Ix(x1, x2, l):
    safe = np.where(l == 0, 1.0, l)
    return np.where(l == 0, x2 - x1, (np.sin(l * x2) - np.sin(l * x1)) / safe)


def die_temps(layers, h, P_switch=1000.0, die_scale=1.0, M=240, Nn=210, extra_R_die=0.0):
    """Mean temperature rise above the LOCAL fluid temperature of each die (heat spread uniformly over the dies,
    entering the top of 'layers' over the die footprints)."""
    P = patches(die_scale)
    A_die = sum((x2 - x1) * (y2 - y1) for x1, x2, y1, y2 in P)
    q0 = P_switch / A_die
    m = np.arange(M)
    n = np.arange(Nn)
    lam = m * np.pi / CELL_A
    dl = n * np.pi / CELL_B
    LAM, DL = np.meshgrid(lam, dl, indexing="ij")
    beta = np.sqrt(LAM ** 2 + DL ** 2)
    Z = Z_stack(beta, layers, h)
    em = np.where(m == 0, 1.0, 2.0)
    en = np.where(n == 0, 1.0, 2.0)
    qmn = np.zeros_like(beta)
    for x1, x2, y1, y2 in P:
        qmn += np.outer(em * _Ix(x1, x2, lam), en * _Ix(y1, y2, dl)) * q0 / (CELL_A * CELL_B)
    Tmn = Z * qmn
    T = []
    for x1, x2, y1, y2 in P:
        avg = np.outer(_Ix(x1, x2, lam) / (x2 - x1), _Ix(y1, y2, dl) / (y2 - y1))
        T.append(float((Tmn * avg).sum()) + q0 * (R_DIE + extra_R_die))
    T = np.array(T)
    return dict(T_mean=T.mean(), T_max=T.max(), Rth_mean=T.mean() / P_switch, Rth_max=T.max() / P_switch,
                A_die_cm2=A_die * 1e4, q_die=q0 / 1e4)


def module_stack(t_base=3.0e-3, attach="solder", base_k=K_CU, ceramic=(0.32e-3, K_SN), cu=0.30e-3):
    if attach == "solder":
        att = (0.10e-3, K_SOLDER)
    elif attach == "sinter":
        att = (0.04e-3, K_AG)
    else:
        att = attach
    L = []
    if t_base > 0:
        L.append((t_base, base_k))
    if att is not None:
        L.append(att)
    L += [(cu, K_CU), ceramic, (cu, K_CU)]
    return L      # bottom -> top (top = AMB top copper under the dies)


def calibrate_h(target, layers, lo=1e3, hi=1e6, **kw):
    for _ in range(60):
        mid = np.sqrt(lo * hi)
        r = die_temps(layers, mid, **kw)
        lo, hi = (mid, hi) if r["Rth_mean"] > target else (lo, mid)
    return mid, r


if __name__ == "__main__":
    import time
    t = time.time()
    r = die_temps(module_stack(), 25000.0)
    print("Fourier, pin-fin stack, h=25k:", {k: round(v, 5) for k, v in r.items()}, round(time.time() - t, 2), "s")
    for M in (120, 240, 400):
        print(M, round(die_temps(module_stack(), 25000.0, M=M, Nn=int(M * 0.875))["Rth_mean"], 5))
