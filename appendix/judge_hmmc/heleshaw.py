# 2-D (x-z) Hele-Shaw + two-equation conjugate model of one HMMC half-cell (inlet slot centre -> outlet slot centre)
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla
def run(openings_in, openings_out, L=4.0, H=2.0, tb=1.0, d=0.025, q=1.28e6, dTout=12.66,
        h=13.2e3, pitch=0.25e-3, gap=0.15e-3, kcu=390., kf=0.50, rho=1005., cp=3930., mu=1.25e-3, label="", kfz_mult=1.0):
    nx=int(round(L/d)); nzf=int(round(H/d)); nzb=int(round(tb/d)); dx=d*1e-3
    xs=(np.arange(nx)+0.5)*d
    phi=gap/pitch; ks=kcu*(1-phi); a=2/pitch
    # ---- pressure in fin layer: Laplace, Dirichlet at top openings ----
    N=nx*nzf; idx=lambda i,k: k*nx+i   # k=0 bottom row of fin layer, k=nzf-1 top row
    A=sp.lil_matrix((N,N)); b=np.zeros(N)
    def isin(x,ops): return any(lo<=x<=hi for lo,hi in ops)
    top_bc=[]
    for i,x in enumerate(xs):
        top_bc.append(1.0 if isin(x,openings_in) else (0.0 if isin(x,openings_out) else None))
    for k in range(nzf):
        for i in range(nx):
            p=idx(i,k); diag=0
            for di,dk in ((1,0),(-1,0),(0,1),(0,-1)):
                ii,kk=i+di,k+dk
                if 0<=ii<nx and 0<=kk<nzf:
                    A[p,idx(ii,kk)]=-1; diag+=1
                elif kk==nzf and top_bc[i] is not None:
                    diag+=2; b[p]+=2*top_bc[i]
            A[p,p]=diag
    P=spla.spsolve(A.tocsr(),b).reshape(nzf,nx)
    # face fluxes (Darcy, arbitrary scale): horizontal faces between i,i+1; vertical faces between k,k+1; top faces
    Fx=-(P[:,1:]-P[:,:-1])          # per unit (K/mu*dz*...), positive = +x
    Fz=-(P[1:,:]-P[:-1,:])          # positive = +z (up)
    Ftop=np.zeros(nx)
    for i in range(nx):
        if top_bc[i] is not None: Ftop[i]=-(top_bc[i]-P[-1,i])*2   # outflow positive (up)
    Qin=-Ftop[Ftop<0].sum()
    mdot=q*L*1e-3/(cp*dTout)       # kg/s per m depth (y)
    s=mdot/Qin                      # kg/s per unit flux
    Fx*=s; Fz*=s; Ftop*=s
    # bypass metric: fraction of flow under the wall centre passing within the top half of the fin
    iw=np.argmin(abs(xs-0.5*(openings_in[-1][1]+openings_out[0][0])))
    col=Fx[:,min(iw,nx-2)]; top_frac=col[nzf//2:].sum()/col.sum()
    # ---- energy: unknowns Ts (base + fin layer) and Tf (fin layer) ----
    nzs=nzb+nzf; Ns=nx*nzs; Nf=nx*nzf; NT=Ns+Nf
    sidx=lambda i,k: k*nx+i          # k=0 bottom base row
    fidx=lambda i,k: Ns+k*nx+i       # k=0 bottom fin row
    M=sp.lil_matrix((NT,NT)); r=np.zeros(NT)
    vol=dx*dx
    for k in range(nzs):
        for i in range(nx):
            p=sidx(i,k); kk_here=kcu if k<nzb else ks
            for di,dk in ((1,0),(-1,0),(0,1),(0,-1)):
                ii,kk=i+di,k+dk
                if 0<=ii<nx and 0<=kk<nzs:
                    k2=kcu if kk<nzb else ks
                    kh=2*kk_here*k2/(kk_here+k2)
                    M[p,p]+=kh; M[p,sidx(ii,kk)]-=kh
            if k==0: r[p]+=q*dx
            if k>=nzb:
                kf_=k-nzb; G=h*a*vol
                M[p,p]+=G; M[p,fidx(i,kf_)]-=G
            if k==nzb-1:   # channel floor exchange to bottom fluid row
                G=h*phi*dx; M[p,p]+=G; M[p,fidx(i,0)]-=G
    kfe=kf*phi
    for k in range(nzf):
        for i in range(nx):
            p=fidx(i,k); G=h*a*vol
            M[p,p]+=G; M[p,sidx(i,k+nzb)]-=G
            if k==0:
                G2=h*phi*dx; M[p,p]+=G2; M[p,sidx(i,nzb-1)]-=G2
            # conduction in fluid
            for di,dk in ((1,0),(-1,0),(0,1),(0,-1)):
                ii,kk=i+di,k+dk
                if 0<=ii<nx and 0<=kk<nzf:
                    kk_=kfe*(kfz_mult if dk!=0 else 1.0)
                    M[p,p]+=kk_; M[p,fidx(ii,kk)]-=kk_
            # advection (upwind), outflow - inflow
            # east face
            if i<nx-1:
                F=Fx[k,i]*cp
                if F>0: M[p,p]+=F; M[fidx(i+1,k),p]-=F
                else:   M[fidx(i+1,k),fidx(i+1,k)]+=-F; M[p,fidx(i+1,k)]-=-F
            if k<nzf-1:
                F=Fz[k,i]*cp
                if F>0: M[p,p]+=F; M[fidx(i,k+1),p]-=F
                else:   M[fidx(i,k+1),fidx(i,k+1)]+=-F; M[p,fidx(i,k+1)]-=-F
            if k==nzf-1 and top_bc[i] is not None:
                F=Ftop[i]*cp
                if F>0: M[p,p]+=F          # outflow
                else: r[p]+=-F*0.0   # inflow at T_in=0 (no diagonal term)
    T=spla.spsolve(M.tocsr(),r)
    Ts=T[:Ns].reshape(nzs,nx); Tf=T[Ns:].reshape(nzf,nx)
    Tout=(Ftop[Ftop>0]*Tf[-1][Ftop>0]).sum()/Ftop[Ftop>0].sum()
    case=Ts[0].mean()
    # 1-D reference with same inputs
    m=np.sqrt(2*h/(kcu*(pitch-gap))); eta=np.tanh(m*H*1e-3)/(m*H*1e-3)
    heff=h*(eta*2*H*1e-3+gap)/pitch; NTU=heff*L*1e-3/(mdot*cp)
    cal=dTout*(1/(1-np.exp(-NTU))-1/NTU); ref=cal+q/heff+q*tb*1e-3/kcu
    print(f"{label:48s} case avg {case:5.2f} K (pk-pk {Ts[0].max()-Ts[0].min():4.2f})  1-D ref {ref:5.2f} K  -> penalty {case-ref:+5.2f} K;"
          f" Tout check {Tout:5.2f}; top-half flow fraction under land {top_frac:4.2f}")
    return case,ref
if __name__=="__main__" and False:
    # proposal geometry: 3.3 mm slots, 0.7 mm wall, grate bars 0.5 mm @1.0 mm pitch (one under wall)
    run([(0.25,0.75),(1.25,1.65)],[(2.35,2.75),(3.25,3.75)],label="proposal: 3.3/0.7 slots + grate (bars at 0,1,2,3,4)")
    run([(0.0,1.65)],[(2.35,4.0)],label="proposal slots, no grate")
    run([(0.0,0.5)],[(3.5,4.0)],label="classic MMC: 1.0 mm openings, 3.0 mm land")
    run([(0.0,1.0)],[(3.0,4.0)],label="2.0 mm openings, 2.0 mm land")
