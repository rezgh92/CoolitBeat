"""End-fed segmented-fin (impingement-trench) variant of the slot-jet cell: fins are cross-cut under every nozzle slot
(trench width w_t), so the slot jet impinges on a bare base strip and enters the channel ENDS of the two adjacent fin
segments; the return slot sits over the middle of each segment (inlet at the ends, outlet between the ends = the reverse
of a split-flow cell). Compares h_eff with the continuous-fin slot-jet cell of record."""
import math
from jet_hybrid_model import SlotJetFin, channel_h, descent_h, stag_h_plane, j_of, plate_eval, rho, K_CU, JH_R, A_FP, Q0, cp
def trench_cell(b,t,H,w_n,P_r,w_t,j,c_turn=0.5,C=0.6,w_r=1.0e-3):
    p=b+t; phi=b/p
    qline=j*P_r; V_slot=qline/w_n
    Vj=V_slot                       # jet enters the open trench: no fin blockage
    u_ch=qline/(2*H*phi)
    Lc=P_r/2
    xt=w_t/2
    x1=min(xt+c_turn*H, Lc-w_r/2-0.2e-3)
    h_st=stag_h_plane(Vj,w_n,C)
    V_ent=0.5*(Vj*w_n/(2*H)/phi+u_ch)*2   # turning flow entering the channel ends (approx 2x u_ch)
    h_ent=descent_h(b,H,max(V_ent,u_ch))   # entrance-region fin walls
    L2=max(Lc-w_r/2-x1,0.2e-3)
    h_ch,_,_=channel_h(b,H,u_ch,L2)
    # fins exist only for x > xt
    f_fin_len=(Lc-xt)/Lc
    f1=(x1-xt)/(Lc-xt)
    h_fin=f1*h_ent+(1-f1)*h_ch
    m=math.sqrt(2*h_fin/(K_CU*t)); eta=math.tanh(m*H)/(m*H)
    h_floor_fin=f1*0.6*h_st+(1-f1)*h_ch
    h_eff_fin=(h_fin*2*H*eta+h_floor_fin*b)/p
    h_eff=f_fin_len*h_eff_fin+(1-f_fin_len)*h_st
    dp_noz=0.5*rho*(0.5*V_slot**2+1.0*Vj**2)+0.5*rho*(Vj*w_n/(2*H*phi))**2*0.5
    return dict(h_eff=h_eff,Vj=Vj,u_ch=u_ch,h_st=h_st,h_ent=h_ent,h_ch=h_ch,eta=eta,dp_noz=dp_noz,f_fin_len=f_fin_len)
j=j_of(18)
print("| variant | w_n mm | w_t mm | P_r mm | Vj m/s | h_st | h_ent | h_ch | h_eff kW/m2K | nozzle dP kPa |")
print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
c=JH_R.cell(j)
print(f"| continuous fins (record) | 0.22 | - | 8 | {c['Vj']:.2f} | {c['h_st']/1e3:.0f} | {c['h_desc']/1e3:.0f} | {c['h_ch']/1e3:.1f} | {c['h_eff']/1e3:.0f} | {c['dp_noz']/1e3:.2f} |")
for w_n,w_t in ((0.22e-3,0.40e-3),(0.18e-3,0.40e-3),(0.15e-3,0.35e-3),(0.18e-3,0.50e-3)):
    r=trench_cell(0.15e-3,0.10e-3,2.0e-3,w_n,8e-3,w_t,j)
    print(f"| trench (end-fed segments) | {w_n*1e3:.2f} | {w_t*1e3:.2f} | 8 | {r['Vj']:.2f} | {r['h_st']/1e3:.0f} | {r['h_ent']/1e3:.0f} | {r['h_ch']/1e3:.1f} | {r['h_eff']/1e3:.0f} | {r['dp_noz']/1e3:.2f} |")
# die zone
jd=3.0*j_of(15.4)
r=trench_cell(0.15e-3,0.10e-3,2.0e-3,0.18e-3,4e-3,0.40e-3,jd)
c=SlotJetFin("d",0.15e-3,0.10e-3,2.0e-3,0.28e-3,4e-3,w_r=0.8e-3).cell(jd)
print(f"\ndie zone (j {jd*100:.1f} cm/s, P_r 4 mm): continuous-fin w_n 0.28 h_eff {c['h_eff']/1e3:.0f} (noz {c['dp_noz']/1e3:.2f} kPa); trench w_n 0.18/w_t 0.40 h_eff {r['h_eff']/1e3:.0f} (noz {r['dp_noz']/1e3:.2f} kPa, Vj {r['Vj']:.2f})")
