import numpy as np, header_net2 as h2
from scipy.optimize import fsolve
import header_net as hn
# variant: per-outlet window area (edge outlets half area) and outlet header area scale
def run(lpm=18, edge_half=True, A_out_scale=1.0, K_wo=1.6, s_jet=0.0, kd=1.0, kc=2.0, out_meter=0.0):
    xin, xout, segs = hn.build(19); nin, nout = 9, 10
    rho=hn.rho; LPM=hn.LPM; Qt=lpm*LPM; s=lpm/18; Ql0=Qt/9; qs0=Qt/18
    a_m=1.88e3/(18*LPM/9)**2; a_wi=1.6*0.5*rho/hn.A_w**2
    Aw=np.full(nout,hn.A_w); 
    if edge_half: Aw[0]=Aw[-1]=hn.A_w/2
    a_wo=K_wo*0.5*rho/Aw**2; r_s=0.67e3/(18*LPM/18); a_om=out_meter*1e3/(18*LPM/18)**2
    hn.A_h_out=224e-6*A_out_scale; u_port=Qt/hn.A_port
    def segflow(dp):
        if a_om==0: return dp/r_s
        return np.sign(dp)*(-r_s+np.sqrt(r_s**2+4*a_om*abs(dp)))/(2*a_om)
    def state(z):
        N=z[:nin]; P=z[nin:nin+nout]; C=z[-1]
        q=np.array([segflow(N[k]-P[j]) for k,j in segs]); Q=np.zeros(nin); Qo=np.zeros(nout)
        for (k,j),qq in zip(segs,q): Q[k]+=qq; Qo[j]+=qq
        return N,P,C,q,Q,Qo
    def res(z):
        N,P,C,q,Q,Qo=state(z)
        Phi=hn.header_in(Q,4,kd,s_jet,u_port)+C; Pho=hn.header_out(Qo,5,kc,0.0,u_port)
        return np.concatenate([(Phi-N-(a_m+a_wi)*Q*abs(Q))/(1e3*s*s),(P-Pho-a_wo*Qo*abs(Qo))/(1e3*s*s),[(Q.sum()-Qt)/Qt]])
    z0=np.concatenate([np.full(nin,670*s),np.zeros(nout),[2200*s*s+670*s]])
    z,info,ier,msg=fsolve(res,z0,full_output=True,xtol=1e-13,maxfev=50000)
    N,P,C,q,Q,Qo=state(z); rs=q/qs0; rl=Q/Ql0
    return rl.max()/rl.min(), rs.max()/rs.min(), rs.min(), ier==1, np.round(rs,3)
for lab,kw in (("edge outlets full window (as 19-line base)",dict(edge_half=False)),("edge outlet windows half area",{}),
               ("+ outlet header x2",dict(A_out_scale=2.0)),("+ outlet window K 0.8",dict(K_wo=0.8)),
               ("+ outlet orifice 0.5 kPa",dict(out_meter=0.5)),("+ outlet orifice 1.0 kPa",dict(out_meter=1.0))):
    for lpm in (18,36):
        r=run(lpm,**kw); print(f"{lab}, {lpm} LPM: line {r[0]:.3f} seg {r[1]:.3f} min {r[2]:.3f} ok {r[3]}")
print(run(18)[4])
