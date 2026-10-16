#!/usr/bin/env python3
"""3-D finite-volume conduction model of one SiC switch position (quarter-symmetric unit cell)
for comparing coolers: pin-fin baseplate (calibrated to Infineon HybridPACK Drive G2 CoolSiC
FS01MR12A8MA2B Rth(j-f) = 0.103 K/W typ at 10 L/min 50/50 WEG, 60 C) vs HMMC-derived cartridges.
Bottom (and optional top) wetted faces carry an effective HTC h_eff referenced to the projected
face area, against the LOCAL fluid temperature; caloric rise is added separately.
"""
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

K_CU, K_AL, K_SIC, K_SN, K_AG, K_SOLDER, K_GEL, K_MOLD, K_ALN = 390., 200., 300., 90., 150., 50., 0.2, 0.9, 170.

# unit cell: one switch = 8 dies of 4.5x4.5 mm (1.62 cm2 SiC) on a 40 x 35 mm cell (14 cm2); quarter modelled
CELL_X, CELL_Y = 20.0, 17.5          # quarter, mm
SUB_X, SUB_Y = 18.0, 15.5            # substrate edge in quarter (2 mm margin)
DIE = 4.5

def masks(dx, die_scale=1.0):
    nx, ny = int(round(CELL_X/dx)), int(round(CELL_Y/dx))
    xc = (np.arange(nx)+0.5)*dx; yc = (np.arange(ny)+0.5)*dx
    X, Y = np.meshgrid(xc, yc, indexing="ij")
    d = DIE*np.sqrt(die_scale)
    die = np.zeros_like(X, bool)
    for cx in (3.25, 9.75):          # die centres fixed (pitch 6.5 x 7 mm), die size scales
        for cy in (3.25,):
            die |= (np.abs(X-cx) < d/2 - 1e-9) & (np.abs(Y-cy) < d/2 - 1e-9)
    sub = (X <= SUB_X) & (Y <= SUB_Y)
    full = np.ones_like(X, bool)
    return nx, ny, die, sub, full

def build_stack(kind, t_base=3.0, attach="solder", base_k=K_CU, sub_ceramic=("Si3N4", 0.32, K_SN), dsc=False):
    """Layers bottom->top: (name, thickness mm, k_in, mask_name, k_out)."""
    cer = sub_ceramic
    att = ("solder", 0.10, K_SOLDER) if attach == "solder" else ("Ag sinter", 0.04, K_AG)
    L = [("base", t_base, base_k, "full", base_k),
         (att[0], att[1], att[2], "sub", K_GEL),
         ("AMB Cu bottom", 0.30, K_CU, "sub", K_GEL),
         (cer[0], cer[1], cer[2], "sub", K_GEL),
         ("AMB Cu top", 0.30, K_CU, "sub", K_GEL),
         ("die attach Ag", 0.04, K_AG, "die", K_GEL),
         ("SiC die", 0.18, K_SIC, "die", K_GEL)]
    src_layer = len(L)-1
    if dsc:   # top-side path: sinter, Cu spacer (die area), sinter, AMB, sinter, top cooler base
        L += [("top sinter", 0.04, K_AG, "die", K_MOLD),
              ("Cu spacer", 1.0, K_CU, "die", K_MOLD),
              ("spacer sinter", 0.04, K_AG, "die", K_MOLD),
              ("AMB Cu top2", 0.30, K_CU, "sub", K_MOLD),
              (cer[0]+" top", cer[1], cer[2], "sub", K_MOLD),
              ("AMB Cu bot2", 0.30, K_CU, "sub", K_MOLD),
              ("top attach Ag", 0.04, K_AG, "sub", K_MOLD),
              ("top base", t_base, base_k, "full", base_k)]
    return L, src_layer

def solve(layers, src_layer, h_bot, h_top=None, P_switch=1000.0, dx=0.5, dz_max=0.25, die_scale=1.0, P_density_scale=None):
    nx, ny, die, sub, full = masks(dx, die_scale)
    M = {"die": die, "sub": sub, "full": full}
    # vertical discretisation
    zk = []   # list of (dz, kmap, layer_index)
    for li, (nm, t, kin, mk, kout) in enumerate(layers):
        n = max(1, int(np.ceil(t/dz_max)))
        kmap = np.where(M[mk], kin, kout)
        for _ in range(n):
            zk.append((t/n, kmap, li))
    nz = len(zk)
    N = nx*ny*nz
    idx = np.arange(N).reshape(nz, nx, ny)
    dxm = dx*1e-3
    rows, cols, vals = [], [], []
    diag = np.zeros(N); rhs = np.zeros(N)
    A_cell = dxm*dxm
    for kz, (dz, kmap, li) in enumerate(zk):
        dzm = dz*1e-3
        # x-direction
        kh = 2*kmap[:-1, :]*kmap[1:, :]/(kmap[:-1, :]+kmap[1:, :])
        g = kh*dzm*dxm/dxm
        a = idx[kz, :-1, :].ravel(); b = idx[kz, 1:, :].ravel(); gv = g.ravel()
        rows += [a, b]; cols += [b, a]; vals += [-gv, -gv]
        np.add.at(diag, a, gv); np.add.at(diag, b, gv)
        # y-direction
        kh = 2*kmap[:, :-1]*kmap[:, 1:]/(kmap[:, :-1]+kmap[:, 1:])
        g = kh*dzm*dxm/dxm
        a = idx[kz, :, :-1].ravel(); b = idx[kz, :, 1:].ravel(); gv = g.ravel()
        rows += [a, b]; cols += [b, a]; vals += [-gv, -gv]
        np.add.at(diag, a, gv); np.add.at(diag, b, gv)
        # z-direction to next
        if kz < nz-1:
            dz2, kmap2, _ = zk[kz+1]
            R = (dzm/2)/(kmap*A_cell) + (dz2*1e-3/2)/(kmap2*A_cell)
            gv = (1/R).ravel()
            a = idx[kz].ravel(); b = idx[kz+1].ravel()
            rows += [a, b]; cols += [b, a]; vals += [-gv, -gv]
            np.add.at(diag, a, gv); np.add.at(diag, b, gv)
    # bottom BC
    dz0, k0, _ = zk[0]
    gb = 1/((dz0*1e-3/2)/(k0*A_cell) + 1/(h_bot*A_cell))
    np.add.at(diag, idx[0].ravel(), gb.ravel())
    if h_top is not None:
        dzt, kt, _ = zk[-1]
        gt = 1/((dzt*1e-3/2)/(kt*A_cell) + 1/(h_top*A_cell))
        np.add.at(diag, idx[-1].ravel(), gt.ravel())
    # heat source: top sub-layer of the die layer, die cells; quarter gets P/4
    ktop = max(i for i, z in enumerate(zk) if z[2] == src_layer)
    src = die.ravel()
    q_cells = idx[ktop].ravel()[src]
    rhs[q_cells] = (P_switch/4)/src.sum()
    Aop = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N)) + sp.diags(diag)
    Aop = Aop.tocsr()
    # Jacobi-scaled CG with incomplete-LU preconditioner
    try:
        ilu = spla.spilu(Aop.tocsc(), drop_tol=1e-4, fill_factor=8)
        Mpre = spla.LinearOperator(Aop.shape, ilu.solve)
    except Exception:
        Mpre = sp.diags(1/Aop.diagonal())
    T, info = spla.cg(Aop, rhs, rtol=1e-10, maxiter=4000, M=Mpre)
    if info != 0:
        T = spla.spsolve(Aop.tocsc(), rhs)
    T3 = T.reshape(nz, nx, ny)
    Tj = T3[ktop][die]
    # heat split for DSC
    q_bot = float((gb.ravel()*T3[0].ravel()).sum())*4
    return dict(Tj_mean=Tj.mean(), Tj_max=Tj.max(), Rth_mean=Tj.mean()/P_switch, Rth_max=Tj.max()/P_switch,
                frac_bottom=q_bot/P_switch, N=N, die_area_cm2=4*die.sum()*dx*dx/100)

def calibrate(target, layers, src, lo=2e3, hi=5e5, **kw):
    for _ in range(40):
        mid = np.sqrt(lo*hi)
        r = solve(layers, src, mid, **kw)
        lo, hi = (mid, hi) if r["Rth_mean"] > target else (lo, mid)
    return mid, r
