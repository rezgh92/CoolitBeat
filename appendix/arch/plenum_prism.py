"""Along-plenum (L2) uniformity for PRISM, adapted from judge_risk/plenum1d.py.
Plenum W x Hp, length 108 mm, fed (inlet) at y_in and drained (outlet plenum) at y_out; branch = slit+window+kerf+channel
with viscous fraction fvisc. Returns along-plenum max/min."""
import numpy as np
rho, mu = 1005.0, 1.25e-3
def run(W=3.0e-3, Hp=7.0e-3, Q=18.0/14/60000.0, y_in=-14e-3, y_out=14e-3, dp0=900.0, fvisc=0.5, th_i=1.0, th_o=2.0, n=360):
    A=W*Hp; Dh=2*A/(2*(W+Hp)); fRe=69.0 if Hp/W>2.5 else 62.0
    Lp=108e-3; dy=Lp/n; y=(np.arange(n)+0.5)*dy-Lp/2; q0=Q/n
    R1=fvisc*dp0/q0; R2=(1-fvisc)*dp0/q0**2
    q=np.full(n,q0); i_in=np.argmin(abs(y-y_in)); i_out=np.argmin(abs(y-y_out))
    for it in range(800):
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
        lo,hi=0.0,40000.0
        for _ in range(80):
            mid=0.5*(lo+hi)
            if qs(mid).sum()>Q: hi=mid
            else: lo=mid
        qn=qs(0.5*(lo+hi))
        if np.max(abs(qn-q))/q0<1e-9: break
        q=0.7*q+0.3*qn
    r=q/q0; return r.max()/r.min()
print("| case | flow | branch dp Pa | visc frac | plenum | max/min (th 1/2) | max/min (th 0.6/1.5) |")
print("|---|---|---:|---:|---|---:|---:|")
for lab,Hp,yi,yo in (("offset feed +/-14 mm",7e-3,-14e-3,14e-3),("offset feed, plenum 9 mm",9e-3,-14e-3,14e-3),("true centre feed",7e-3,0,0)):
    for lpm,dp0,fv in ((18,900,0.5),(27,900*(0.5*1.5+0.5*1.5**2),0.5/(0.5+0.5*1.5)),(36,900*(0.5*2+0.5*4),0.5*2/(0.5*2+0.5*4))):
        Q=lpm/14/60000.0
        a=run(Hp=Hp,Q=Q,y_in=yi,y_out=yo,dp0=dp0,fvisc=fv); b=run(Hp=Hp,Q=Q,y_in=yi,y_out=yo,dp0=dp0,fvisc=fv,th_i=0.6,th_o=1.5)
        print(f"| {lab} | {lpm} LPM | {dp0:.0f} | {fv:.2f} | 3 x {Hp*1e3:.0f} mm | {a:.3f} | {b:.3f} |",flush=True)
