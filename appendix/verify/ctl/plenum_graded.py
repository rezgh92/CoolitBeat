"""Graded-meter compensation: the along-plenum profile is momentum-driven (scales with u^2) and the meter is inertial
(scales with u^2), so orifice areas graded along y can cancel the profile at every flow. Same physics as
arch/plenum_prism.run, but with a per-branch inertial coefficient R2_i (orifice area A_i -> R2_i ~ 1/A_i^2)."""
import numpy as np
rho, mu = 1005.0, 1.25e-3
def run(W, Hp, Q, dp0, fvisc, r2scale=None, y_in=-14e-3, y_out=14e-3, th_i=1.0, th_o=2.0, n=432):
    A=W*Hp; Dh=2*A/(2*(W+Hp)); fRe=69.0 if Hp/W>2.5 else 62.0
    Lp=108e-3; dy=Lp/n; y=(np.arange(n)+0.5)*dy-Lp/2; q0=Q/n
    R1=fvisc*dp0/q0; R2=(1-fvisc)*dp0/q0**2*(np.ones(n) if r2scale is None else r2scale)
    q=np.full(n,q0); i_in=np.argmin(abs(y-y_in)); i_out=np.argmin(abs(y-y_out))
    for it in range(1500):
        cum=np.cumsum(q); F_in=np.zeros(n+1); F_out=np.zeros(n+1)
        for j in range(n+1):
            F_in[j]= (-cum[j-1] if j>0 else 0.0) if j<=i_in else Q-cum[j-1]
            F_out[j]=(cum[j-1] if j>0 else 0.0) if j<=i_out else -(Q-cum[j-1])
        u_in=F_in/A; u_out=F_out/A
        def march(u,i0,th):
            p=np.zeros(n)
            for j in range(i0+1,n):
                fr=(fRe*mu/(2*Dh**2))*u[j]; p[j]=p[j-1]-fr*dy-th*rho*(u[j+1]**2-u[j]**2)/2.0
            for j in range(i0-1,-1,-1):
                fr=(fRe*mu/(2*Dh**2))*u[j+1]; p[j]=p[j+1]+fr*dy+th*rho*(u[j+1]**2-u[j]**2)/2.0
            return p
        p_in=march(u_in,i_in,th_i); p_out=march(u_out,i_out,th_o)
        def qs(P):
            dp=np.maximum(P+p_in-p_out,1e-6); return (-R1+np.sqrt(R1**2+4*R2*dp))/(2*R2)
        lo,hi=0.0,60000.0
        for _ in range(80):
            mid=0.5*(lo+hi)
            if qs(mid).sum()>Q: hi=mid
            else: lo=mid
        qn=qs(0.5*(lo+hi))
        if np.max(abs(qn-q))/q0<1e-10: break
        q=0.7*q+0.3*qn
    return q/q0
# design the grading at 18 LPM for the shallow layout, then test at 9, 18, 27, 36 LPM; orifice sizes quantised to 5 punch sizes
for lab, n, W, Hp, met, fin in (("9 in, 5.4 x 5.0, meter 2.3, L6", 9, 5.4, 5.0, 2.30, 0.65), ("7 in, 7.1 x 4.0, meter 2.3, L7.7", 7, 7.1, 4.0, 2.30, 1.07)):
    def prof(lpm, sc):
        s=lpm/18.0; inert=(met+0.08)*s*s; visc=fin*s; dp0=(inert+visc)*1e3
        return run(W*1e-3, Hp*1e-3, lpm/n/60000.0, dp0, visc/(inert+visc), r2scale=sc)
    sc=np.ones(432)
    base=prof(18, None)
    for k in range(6):
        r=prof(18, sc); sc=sc*r**1.6   # over-fed branch -> smaller orifice -> larger R2
        sc=sc/np.mean(sc)
    # quantise R2 scale to 5 discrete orifice sizes, per 2 mm orifice pitch (54 orifices along 108 mm)
    blk=sc.reshape(54,8).mean(1); levels=np.quantile(blk,[0.1,0.3,0.5,0.7,0.9])
    q5=np.array([levels[np.argmin(abs(levels-b))] for b in blk]); scq=np.repeat(q5,8)
    areas = 1/np.sqrt(levels)
    out=[]
    for lpm in (9,18,27,36):
        r0=prof(lpm,None); r1=prof(lpm,scq); 
        out.append(f"{lpm} LPM: ungraded {r0.max()/r0.min():.3f}, graded {r1.max()/r1.min():.3f}")
    print(f"{lab}: " + "; ".join(out) + f"; orifice area span {areas.max()/areas.min():.2f}x (5 sizes: {', '.join(f'{a/areas.mean():.3f}' for a in areas)})", flush=True)
