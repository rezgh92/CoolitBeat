import numpy as np, scipy.sparse as sps, scipy.sparse.linalg as spl
rho, cp, mu, kf, kcu = 1005.0, 3930.0, 1.25e-3, 0.52, 390.0
def run_uniform(H=2.0e-3, L=4.0e-3, b=0.15e-3, t=0.15e-3, h=13.3e3, Qseg=2.98e-8, d=0.04e-3, mixed=False):
    nx, nz = int(round(L/d)), int(round(H/d)); dx, dz = L/nx, H/nz
    u = Qseg/(b*H)
    Tw = np.full((nz,nx),0.5); Tb=1.0
    for it in range(300):
        # fluid marching in x (upwind), each z layer independent (unmixed) or mixed
        Tf = np.zeros((nz,nx)); Tin = np.zeros(nz)
        for i in range(nx):
            # cell balance: b u dz rho cp (T - Tup) = 2h dx dz (Tw - T) + floor
            a = b*u*dz*rho*cp
            c = 2*h*dx*dz*np.ones(nz); src = c*Tw[:,i]
            c2 = c.copy(); c2[0] += h*b*dx; src = src.copy(); src[0] += h*b*dx*Tb
            if mixed:
                Tm_up = Tin.mean()
                T = (a*nz*Tm_up + src.sum())/(a*nz + c2.sum()); Tf[:,i]=T; Tin=np.full(nz,T)
            else:
                T = (a*Tin + src)/(a + c2); Tf[:,i]=T; Tin=T
        Tout = Tin.mean()
        # fin solve
        N=nx*nz; idx=lambda i,k:k*nx+i
        Aw=sps.lil_matrix((N,N)); rw=np.zeros(N)
        for k in range(nz):
            for i in range(nx):
                n=idx(i,k); diag=0
                for (ii,kk,ds,dl) in ((i-1,k,dz,dx),(i+1,k,dz,dx),(i,k-1,dx,dz),(i,k+1,dx,dz)):
                    if 0<=ii<nx and 0<=kk<nz:
                        cc=kcu*t*ds/dl; Aw[n,idx(ii,kk)]-=cc; diag+=cc
                    elif kk==-1:
                        cc=kcu*t*ds/(dl/2); diag+=cc; rw[n]+=cc*Tb
                cc=2*h*dx*dz; diag+=cc; rw[n]+=cc*Tf[k,i]; Aw[n,n]=diag
        Twn=spl.spsolve(Aw.tocsr(),rw).reshape(nz,nx)
        if np.max(abs(Twn-Tw))<1e-7: break
        Tw=0.5*Tw+0.5*Twn
    m=np.sqrt(2*h/(kcu*t)); eta=np.tanh(m*H)/(m*H)
    NTU=h*(b+2*eta*H)*L/(rho*cp*Qseg)
    return Tout, 1-np.exp(-NTU), -np.log(1-Tout), NTU
for H in (2.0e-3,3.0e-3):
    for mixed in (True, False):
        To2, To1, n2, n1 = run_uniform(H=H, mixed=mixed)
        print(f"H={H*1e3:.0f} mm uniform flow, {'z-mixed' if mixed else 'z-unmixed'}: Tout 2D {To2:.3f} vs 1-D {To1:.3f}, NTU {n2:.2f} vs {n1:.2f}, ratio {To2/To1:.3f}")
