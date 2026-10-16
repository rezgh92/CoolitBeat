"""Independent 2-D (x-z) conjugate cell model for verification (written from scratch, not derived from cell2d.py).
Fin layer = Hele-Shaw gaps between plate fins (fins are x-z plates stacked in y at pitch p). Two-temperature
volume-averaged model: solid fraction (1-phi) with k_cu (in-plane x-z conduction of the fin plates), fluid
fraction phi with k_f, interphase h*a, a = 2/p. Kerf columns = open fluid (phi=1), permeability w^2/12.
Base below: solid copper, uniform flux q at the bottom (die side). Pressure: div(K grad p)=0.
Options: outlet as top window (manifold cell) or as vertical end face (split-flow channel end).
Returns case (base-bottom) mean, pk-pk, energy closure, and decomposition."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla

def solve(L=6.0, H=2.0, tb=1.0, dx=0.03, dz=None, q=1.282e6, dTout=12.66, h=13.3e3, t=0.15, g=0.15,
          win_in=0.6, win_out=0.6, kerf_in=0.15, kerf_out=0.15, w_kerf=0.3, end_outlet=False,
          kcu=390.0, kf=0.52, cp=3930.0, h_floor_kerf=12e3, zmix=False, mu=1.25e-3, Kkerf_ratio=None, layers=None):
    dz = dz or dx
    if layers is None: layers = [(tb, kcu, kcu)]
    zrows = []
    for (th, kxl, kzl) in layers:
        n = max(2, int(round(th/dz)))
        zrows += [(th/n*1e-3, kxl, kzl)]*n
    tb = sum(l[0] for l in layers)
    nx = int(round(L/dx)); nzf = int(round(H/dz)); nzb = len(zrows)
    DX, DZ = L/nx*1e-3, H/nzf*1e-3; DZb = tb/nzb*1e-3
    xc = (np.arange(nx)+0.5)*L/nx
    p_ = (t+g)*1e-3; phi = g/(t+g); a = 2.0/p_
    kerf = (xc < kerf_in) | (xc > L-kerf_out)
    Kfin = phi*(g*1e-3)**2/12.0
    Kk = (w_kerf*1e-3)**2/12.0 if Kkerf_ratio is None else Kkerf_ratio*Kfin
    K = np.where(kerf, Kk, Kfin)                     # per column
    # ---------------- pressure (fin layer only), unknowns p[k,i] k=0 bottom .. nzf-1 top
    N = nx*nzf; I = lambda i, k: k*nx+i
    rows, cols, vals = [], [], []; b = np.zeros(N); D = np.zeros(N)
    def add(pi, pj, c):
        rows.append(pi); cols.append(pj); vals.append(-c); D[pi] += c
    topBC = np.full(nx, np.nan)
    topBC[xc < win_in] = 1.0
    if not end_outlet: topBC[xc > L-win_out] = 0.0
    for k in range(nzf):
        for i in range(nx):
            pi = I(i, k)
            if i+1 < nx:
                c = 2*K[i]*K[i+1]/(K[i]+K[i+1])*DZ/DX; add(pi, I(i+1, k), c); add(I(i+1, k), pi, c)
            if k+1 < nzf:
                c = K[i]*DX/DZ; add(pi, I(i, k+1), c); add(I(i, k+1), pi, c)
            if k == nzf-1 and not np.isnan(topBC[i]):
                c = 2*K[i]*DX/DZ; D[pi] += c; b[pi] += c*topBC[i]
            if end_outlet and i == nx-1:
                c = 2*K[i]*DZ/DX; D[pi] += c  # p=0 at x=L face
    A = sp.csr_matrix((vals+list(D), (rows+list(range(N)), cols+list(range(N)))), shape=(N, N))
    P = spla.spsolve(A, b).reshape(nzf, nx)
    # face flows (per unit depth, up to factor 1/mu), positive +x / +z
    Kf = 2*K[:-1]*K[1:]/(K[:-1]+K[1:])
    Fx = -(P[:, 1:]-P[:, :-1])/DX*Kf[None, :]*DZ             # (nzf, nx-1)
    Fz = -(P[1:, :]-P[:-1, :])/DZ*K[None, :]*DX             # (nzf-1, nx)
    Ftop = np.zeros(nx); m = ~np.isnan(topBC)
    Ftop[m] = -(topBC[m]-P[-1, m])/(DZ/2)*K[m]*DX            # >0 = leaving through top
    Fend = np.zeros(nzf)
    if end_outlet: Fend = -(0.0-P[:, -1])/(DX/2)*K[-1]*DZ     # >0 leaving at x=L
    Qin = -Ftop[Ftop < 0].sum()
    mdot = q*L*1e-3/(cp*dTout)                                # kg/s per m depth
    s = mdot/Qin; Fx *= s; Fz *= s; Ftop *= s; Fend *= s
    # mass check
    mres = np.zeros((nzf, nx))
    mres[:, :-1] += Fx; mres[:, 1:] -= Fx; mres[:-1, :] += Fz; mres[1:, :] -= Fz
    mres[-1, :] += Ftop; mres[:, -1] += Fend
    massclose = np.abs(mres).max()/mdot
    # ---------------- energy: base solid (nzb rows), fin solid (nzf rows, non-kerf), fluid (nzf rows)
    nb = nx*nzb; nfs = nx*nzf; nfl = nx*nzf; NT = nb+nfs+nfl
    B = lambda i, k: k*nx+i; S = lambda i, k: nb+k*nx+i; F = lambda i, k: nb+nfs+k*nx+i
    M = sp.lil_matrix((NT, NT)); r = np.zeros(NT)
    def cond(pi, pj, c):
        M[pi, pi] += c; M[pi, pj] -= c; M[pj, pj] += c; M[pj, pi] -= c
    ks = kcu*(1-phi); kfl = kf*phi
    for k in range(nzb):
        dzk, kxk, kzk = zrows[k]
        for i in range(nx):
            if i+1 < nx: cond(B(i, k), B(i+1, k), kxk*dzk/DX)
            if k+1 < nzb:
                dz2, kx2, kz2 = zrows[k+1]
                cond(B(i, k), B(i, k+1), DX/((dzk/2)/kzk+(dz2/2)/kz2))
            if k == 0: r[B(i, k)] += q*DX
    for i in range(nx):
        # base top row <-> fin solid bottom row (non-kerf), half-cell resistances in series
        if not kerf[i]:
            R = (zrows[-1][0]/2)/(zrows[-1][2]*DX)+(DZ/2)/(ks*DX); cond(B(i, nzb-1), S(i, 0), 1/R)
            hfl = h*phi
        else:
            hfl = h_floor_kerf
        R = (zrows[-1][0]/2)/(zrows[-1][2]*DX)+1/(hfl*DX); cond(B(i, nzb-1), F(i, 0), 1/R)
    for k in range(nzf):
        for i in range(nx):
            if kerf[i]:
                M[S(i, k), S(i, k)] = 1.0; continue
            if i+1 < nx and not kerf[i+1]: cond(S(i, k), S(i+1, k), ks*DZ/DX)
            if k+1 < nzf: cond(S(i, k), S(i, k+1), ks*DX/DZ)
            cond(S(i, k), F(i, k), h*a*DX*DZ)
    for k in range(nzf):
        for i in range(nx):
            phic = 1.0 if kerf[i] else phi
            if i+1 < nx:
                phin = 1.0 if kerf[i+1] else phi
                cond(F(i, k), F(i+1, k), kf*min(phic, phin)*DZ/DX)
            if k+1 < nzf:
                cond(F(i, k), F(i, k+1), (1e6 if zmix else kf*phic)*DX/DZ)
    # advection (upwind), energy carried = cp*F*T
    for k in range(nzf):
        for i in range(nx-1):
            f = Fx[k, i]*cp; up, dn = (F(i, k), F(i+1, k)) if f > 0 else (F(i+1, k), F(i, k)); f = abs(f)
            M[up, up] += f; M[dn, up] -= f
    for k in range(nzf-1):
        for i in range(nx):
            f = Fz[k, i]*cp; up, dn = (F(i, k), F(i, k+1)) if f > 0 else (F(i, k+1), F(i, k)); f = abs(f)
            M[up, up] += f; M[dn, up] -= f
    for i in range(nx):
        if Ftop[i] > 0: M[F(i, nzf-1), F(i, nzf-1)] += Ftop[i]*cp
    for k in range(nzf):
        if Fend[k] > 0: M[F(nx-1, k), F(nx-1, k)] += Fend[k]*cp
    T = spla.spsolve(M.tocsr(), r)
    Tb = T[:nb].reshape(nzb, nx); Tfl = T[nb+nfs:].reshape(nzf, nx)
    out_flow = Ftop[Ftop > 0].sum()+Fend[Fend > 0].sum()
    Hout = (Ftop[Ftop > 0]*Tfl[-1][Ftop > 0]).sum()+(Fend[Fend > 0]*Tfl[:, -1][Fend > 0]).sum()
    Tout = Hout/out_flow
    eclose = Hout*cp/(q*L*1e-3)
    case = Tb[0]
    return dict(Tb=Tb, zrows=zrows, case=case.mean(), pkpk=case.max()-case.min(), cmax=case.max(), Tout=Tout, eclose=eclose,
                massclose=massclose, nx=nx, nzf=nzf)

def oneD(q=1.282e6, dTout=12.66, h=13.3e3, t=0.15, g=0.15, H=2.0, tb=1.0, kcu=390.0, linear=False):
    p_ = (t+g)*1e-3; mH = np.sqrt(2*h/(kcu*t*1e-3))*H*1e-3; eta = np.tanh(mH)/mH
    heff = h*(2*H*1e-3*eta+g*1e-3)/p_
    NTU = heff*dTout/q
    cal = 0.5*dTout if linear else dTout*(1/(1-np.exp(-NTU))-1/NTU)
    return dict(cal=cal, conv=q/heff, base=q*tb*1e-3/kcu, core=cal+q/heff+q*tb*1e-3/kcu, heff=heff, NTU=NTU, eta=eta)
