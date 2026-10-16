"""Judge check: 2-D (x-z) Hele-Shaw flow + conjugate fin in one 4 mm manifold cell.
Top-fed from a slit at x=0 (half width a_in), drained by a slit at x=L (half width a_out).
Compares heat removed vs the 1-D model (uniform flow over fin height, isothermal cell, 1-D fin eta).
"""
import numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spl, sys
rho, cp, mu, kf = 1005.0, 3930.0, 1.25e-3, 0.52
kcu = 390.0

def run(H=2.0e-3, L=4.0e-3, b=0.15e-3, t=0.15e-3, a_in=0.15e-3, a_out=0.30e-3, h=13.3e3, Qseg=2.98e-8, d=0.025e-3):
    nx, nz = int(round(L/d)), int(round(H/d))
    dx, dz = L/nx, H/nz
    xc = (np.arange(nx)+0.5)*dx
    N = nx*nz
    idx = lambda i,k: k*nx+i  # k=0 bottom (base), k=nz-1 top (floor/tip)
    # ---- pressure (Hele-Shaw, perm K=b^2/12mu), unit conductance in x,z
    A = sps.lil_matrix((N,N)); rhs = np.zeros(N)
    inlet = xc < a_in; outlet = xc > L-a_out
    q_in_per_len = Qseg/(b*a_in)   # velocity (m/s) normal through window
    Kp = b**2/(12*mu)
    for k in range(nz):
        for i in range(nx):
            n = idx(i,k); diag = 0.0
            for (ii,kk,ds,dl) in ((i-1,k,dz,dx),(i+1,k,dz,dx),(i,k-1,dx,dz),(i,k+1,dx,dz)):
                if 0<=ii<nx and 0<=kk<nz:
                    c = Kp*ds/dl; A[n,idx(ii,kk)] -= c; diag += c
            if k==nz-1 and inlet[i]:
                rhs[n] += q_in_per_len*dx          # inflow (velocity*length per unit gap)
            if k==nz-1 and outlet[i]:
                c = Kp*dx/(dz/2); diag += c          # p=0 at outlet window
            A[n,n] = diag
    p = spl.spsolve(A.tocsr(), rhs).reshape(nz,nx)
    # face velocities
    ux = np.zeros((nz,nx+1)); uz = np.zeros((nz+1,nx))
    ux[:,1:-1] = -Kp*(p[:,1:]-p[:,:-1])/dx
    uz[1:-1,:] = -Kp*(p[1:,:]-p[:-1,:])/dz
    uz[-1,inlet] = -q_in_per_len   # downward into domain at top
    uz[-1,outlet] = Kp*p[-1,outlet]/(dz/2)  # upward out
    # flow fraction through lower half (horizontal flux at mid-x)
    im = nx//2
    flux = ux[:,im]*dz
    frac_low = flux[:nz//2].sum()/flux.sum()
    u_base = ux[0,im]; u_mean = flux.sum()/H
    # ---- conjugate: fluid T_f(x,z) gap-averaged; fin T_w(x,z); base T_b=1, T_in=0
    Tw = np.full((nz,nx),0.5); Tb = 1.0
    hb2 = 2*h
    for it in range(200):
        # fluid: upwind FV, b*rho*cp*div(u T) = 2h(Tw-Tf) + floor
        Af = sps.lil_matrix((N,N)); rf = np.zeros(N)
        for k in range(nz):
            for i in range(nx):
                n = idx(i,k); diag = 0.0
                # outflow faces
                # east
                fe = ux[k,i+1]*dz; fw = ux[k,i]*dz; fn = uz[k+1,i]*dx; fs = uz[k,i]*dx
                # out-fluxes contribute diag, in-fluxes from neighbors
                for f, nb, sign in ((fe,(i+1,k),1),(fw,(i-1,k),-1),(fn,(i,k+1),1),(fs,(i,k-1),-1)):
                    out = f*sign  # positive = leaving cell
                    if out>0: diag += out*b*rho*cp
                    else:
                        ii,kk = nb
                        if 0<=ii<nx and 0<=kk<nz:
                            Af[n,idx(ii,kk)] -= (-out)*b*rho*cp
                        else:
                            rf[n] += (-out)*b*rho*cp*0.0  # inflow at T_in=0
                cc = hb2*dx*dz
                diag += cc; rf[n] += cc*Tw[k,i]
                if k==0:
                    cfl = h*b*dx; diag += cfl; rf[n] += cfl*Tb
                Af[n,n] = diag
        Tf = spl.spsolve(Af.tocsr(), rf).reshape(nz,nx)
        # fin: k t lap Tw = 2h (Tw - Tf); root Tw=Tb at z=0 (ghost below), tip adiabatic, sides adiabatic
        Aw = sps.lil_matrix((N,N)); rw = np.zeros(N)
        for k in range(nz):
            for i in range(nx):
                n = idx(i,k); diag=0.0
                for (ii,kk,ds,dl) in ((i-1,k,dz,dx),(i+1,k,dz,dx),(i,k-1,dx,dz),(i,k+1,dx,dz)):
                    if 0<=ii<nx and 0<=kk<nz:
                        c = kcu*t*ds/dl; Aw[n,idx(ii,kk)] -= c; diag += c
                    elif kk==-1:
                        c = kcu*t*ds/(dl/2); diag += c; rw[n] += c*Tb
                cc = hb2*dx*dz; diag += cc; rw[n] += cc*Tf[k,i]
                Aw[n,n] = diag
        Tw_new = spl.spsolve(Aw.tocsr(), rw).reshape(nz,nx)
        if np.max(abs(Tw_new-Tw))<1e-6: Tw=Tw_new; break
        Tw = 0.5*Tw+0.5*Tw_new
    # heat removed: fluid enthalpy out
    Tout = (Tf[-1,outlet]*(-uz[-1,outlet]*-1)*dx).sum()/((uz[-1,outlet])*dx).sum()
    Qheat = rho*cp*Qseg*Tout   # per unit (Tb-Tin)
    # 1-D reference
    m = np.sqrt(2*h/(kcu*t)); eta = np.tanh(m*H)/(m*H)
    hA = h*(b+2*eta*H)*L
    NTU = hA/(rho*cp*Qseg)
    Q1 = rho*cp*Qseg*(1-np.exp(-NTU))
    # effective NTU of 2-D
    NTU2 = -np.log(1-Tout)
    return dict(frac_low=frac_low, u_base_over_mean=u_base/u_mean, Tout2=Tout, Tout1=1-np.exp(-NTU), NTU1=NTU, NTU2=NTU2,
                heat_ratio=Qheat/Q1, eta=eta)

if __name__=="__main__":
    for H in (2.0e-3, 3.0e-3):
        r = run(H=H, d=0.05e-3 if H>2.5e-3 else 0.04e-3)
        print(f"H={H*1e3:.1f} mm: flow in lower half {r['frac_low']:.2f}, u(base)/u(mean) at mid-cell {r['u_base_over_mean']:.2f}, "
              f"NTU 1-D {r['NTU1']:.2f} vs 2-D {r['NTU2']:.2f}, heat ratio 2-D/1-D {r['heat_ratio']:.3f}, eta {r['eta']:.2f}")
