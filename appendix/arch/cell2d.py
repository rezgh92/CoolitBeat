"""2-D (x-z) Darcy/Hele-Shaw + two-equation conjugate model of one manifold half-cell, generalised from
judge_hmmc/heleshaw.py (model A) to allow full-height KERFS in the fin field under the inlet and outlet
openings. Half-cell: x=0 inlet-opening centre .. x=L outlet-opening centre (mm). Openings in the floor
(top boundary of the fin layer): inlet [0,hi], outlet [L-ho, L]. Kerfs (no fins, open fluid): [0,ki] and [L-ko,L].
Base below (tb mm Cu) heated uniformly with q (W/m2). Fluid enters at T=0. Returns case-average dT."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla

def run(hi, ho, ki=0.0, ko=0.0, L=4.0, H=2.0, tb=1.0, d=0.025, q=1.28e6, dTout=12.66, h=13.2e3,
        t=0.15, gap=0.15, kcu=390., kf=0.52, cp=3930., h_floor_in=15e3, h_floor_out=8e3, kfz_mult=1.0,
        Kkerf_mult=200.0, verbose=False):
    nx=int(round(L/d)); nzf=int(round(H/d)); nzb=int(round(tb/d)); dx=d*1e-3
    xs=(np.arange(nx)+0.5)*d
    pitch=(t+gap)*1e-3; phi=gap*1e-3/pitch; ks=kcu*(1-phi); a=2/pitch
    kerf=np.array([(x<=ki) or (x>=L-ko) for x in xs])
    Kx=np.where(kerf, Kkerf_mult, 1.0)               # relative permeability per column
    N=nx*nzf; idx=lambda i,k: k*nx+i
    top=[1.0 if x<=hi else (0.0 if x>=L-ho else None) for x in xs]
    rows=[];cols=[];vals=[]; b=np.zeros(N); diag=np.zeros(N)
    for k in range(nzf):
        for i in range(nx):
            p=idx(i,k)
            for di,dk in ((1,0),(-1,0),(0,1),(0,-1)):
                ii,kk=i+di,k+dk
                if 0<=ii<nx and 0<=kk<nzf:
                    c=2*Kx[i]*Kx[ii]/(Kx[i]+Kx[ii]); rows.append(p); cols.append(idx(ii,kk)); vals.append(-c); diag[p]+=c
                elif kk==nzf and top[i] is not None:
                    c=2*Kx[i]; diag[p]+=c; b[p]+=c*top[i]
    A=sp.csr_matrix((vals+list(diag),(rows+list(range(N)),cols+list(range(N)))),shape=(N,N))
    P=spla.spsolve(A,b).reshape(nzf,nx)
    Kf=2*Kx[1:]*Kx[:-1]/(Kx[1:]+Kx[:-1])
    Fx=-(P[:,1:]-P[:,:-1])*Kf[None,:]
    Fz=-(P[1:,:]-P[:-1,:])*Kx[None,:]
    Ftop=np.zeros(nx)
    for i in range(nx):
        if top[i] is not None: Ftop[i]=-(top[i]-P[-1,i])*2*Kx[i]
    Qin=-Ftop[Ftop<0].sum()
    mdot=q*L*1e-3/(cp*dTout); s=mdot/Qin
    Fx*=s; Fz*=s; Ftop*=s
    # lower-half flow fraction at mid-cell
    im=nx//2; col=Fx[:,im]; frac_low=col[:nzf//2].sum()/col.sum()
    nzs=nzb+nzf; Ns=nx*nzs; NT=Ns+N
    sidx=lambda i,k: k*nx+i; fidx=lambda i,k: Ns+k*nx+i
    M=sp.lil_matrix((NT,NT)); r=np.zeros(NT); vol=dx*dx
    phic=np.where(kerf,1.0,phi)
    for k in range(nzs):
        for i in range(nx):
            if k>=nzb and kerf[i]: continue      # no solid in kerf columns of fin layer
            p=sidx(i,k); kh_here=kcu if k<nzb else ks
            for di,dk in ((1,0),(-1,0),(0,1),(0,-1)):
                ii,kk=i+di,k+dk
                if 0<=ii<nx and 0<=kk<nzs:
                    if kk>=nzb and kerf[ii]: continue
                    k2=kcu if kk<nzb else ks
                    kh=2*kh_here*k2/(kh_here+k2); M[p,p]+=kh; M[p,sidx(ii,kk)]-=kh
            if k==0: r[p]+=q*dx
            if k>=nzb:
                G=h*a*vol; M[p,p]+=G; M[p,fidx(i,k-nzb)]-=G
            if k==nzb-1:
                hfl = (h_floor_in if xs[i]<L/2 else h_floor_out) if kerf[i] else h*phi
                G=hfl*dx; M[p,p]+=G; M[p,fidx(i,0)]-=G
    for i in range(nx):
        if kerf[i]:
            for k in range(nzb,nzs): M[sidx(i,k),sidx(i,k)]=1.0   # dummy solid nodes
    for k in range(nzf):
        for i in range(nx):
            p=fidx(i,k)
            if not kerf[i]:
                G=h*a*vol; M[p,p]+=G; M[p,sidx(i,k+nzb)]-=G
            if k==0:
                hfl=(h_floor_in if xs[i]<L/2 else h_floor_out) if kerf[i] else h*phi
                G2=hfl*dx; M[p,p]+=G2; M[p,sidx(i,nzb-1)]-=G2
            for di,dk in ((1,0),(-1,0),(0,1),(0,-1)):
                ii,kk=i+di,k+dk
                if 0<=ii<nx and 0<=kk<nzf:
                    kk_=kf*min(phic[i],phic[ii])*(kfz_mult if dk!=0 else 1.0)
                    M[p,p]+=kk_; M[p,fidx(ii,kk)]-=kk_
            if i<nx-1:
                F=Fx[k,i]*cp
                if F>0: M[p,p]+=F; M[fidx(i+1,k),p]-=F
                else: M[fidx(i+1,k),fidx(i+1,k)]+=-F; M[p,fidx(i+1,k)]-=-F
            if k<nzf-1:
                F=Fz[k,i]*cp
                if F>0: M[p,p]+=F; M[fidx(i,k+1),p]-=F
                else: M[fidx(i,k+1),fidx(i,k+1)]+=-F; M[p,fidx(i,k+1)]-=-F
            if k==nzf-1 and top[i] is not None and Ftop[i]>0: M[p,p]+=Ftop[i]*cp
    T=spla.spsolve(M.tocsr(),r)
    Ts=T[:Ns].reshape(nzs,nx); Tf=T[Ns:].reshape(nzf,nx)
    Tout=(Ftop[Ftop>0]*Tf[-1][Ftop>0]).sum()/Ftop[Ftop>0].sum()
    case=Ts[0].mean(); pk=Ts[0].max()-Ts[0].min()
    # 1-D reference (no kerf, isothermal cell, z-mixed)
    m=np.sqrt(2*h/(kcu*t*1e-3)); eta=np.tanh(m*H*1e-3)/(m*H*1e-3)
    heff=h*(eta*2*H*1e-3+gap*1e-3)/pitch; NTU=heff*L*1e-3/(mdot*cp)
    ref=dTout*(1/(1-np.exp(-NTU))-1/NTU)+q/heff+q*tb*1e-3/kcu
    return dict(case=case, ref=ref, pen=case-ref, pkpk=pk, Tout=Tout, frac_low=frac_low, heff1d=heff)

if __name__=="__main__":
    import sys
    # validation vs model A (no kerf): PSM slit RF-15 -> A gave 24.78 / ref 21.43
    r=run(0.15,0.30); print("validation PSM slit no kerf:", {k:round(v,2) for k,v in r.items()})
