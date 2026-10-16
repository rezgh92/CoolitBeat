import sys, math
sys.path.insert(0, "/home/user/Rez/docs/cooling/model")
sys.path.insert(0, "docs/cooling/appendix/design")
from coldplate_model import PG25
import importlib.util
spec = importlib.util.spec_from_file_location("cc", "docs/cooling/appendix/design/crosscomb_model_run.py")
# avoid executing printing: re-define crosscomb locally
from coldplate_model import ColdPlate
def crosscomb(A, tim="PCM pad", hotspot=2.0, port_mm=16.0, orifice=2.5, screen=0.4):
    side = math.sqrt(A)*10; n_slots = max(1,int(round(side/8.0)))
    return ColdPlate(name="cc", footprint_cm2=A, fin_t_mm=0.10, gap_mm=0.15, fin_h_mm=2.0, flow_len_mm=4.0,
        base_mm=1.0, tim=tim, isothermal_cell=True, hotspot_flow_K=hotspot, n_parallel_paths=2*n_slots,
        slot_w_mm=3.0, K_channel=3.0, K_slot=1.5, header_u_m_s=0.86, K_header=1.5, port_bore_mm=port_mm,
        K_port=2.3, orifice_dp_kPa_18=orifice+screen)
rho=1005
Q=18/60/1000
# slit losses inlet (13 slots) and outlet (14 slots), 1.2x12 mm
A_s=1.2*12e-6
for n,lab in ((13,"inlet"),(14,"outlet")):
    u=Q/n/A_s; dyn=0.5*rho*u**2
    print(lab, "slit u %.2f m/s dyn %.0f Pa; K1.5 -> %.2f kPa; K2.0 -> %.2f kPa"%(u,dyn,1.5*dyn/1e3,2.0*dyn/1e3))
# along-slot ratio with off-centre feed
q_slot=Q/13; A_slot=3e-3*10e-3
for off in (0,7.5,14):
    frac=(54+off)/108; u=q_slot*frac/A_slot; dyn=0.5*rho*u**2
    print("feed offset %4.1f mm: long branch %.0f%%, u %.2f, dyn %.0f Pa, ratio (0.27 kPa branch) %.1f"%(off,frac*100,u,dyn,270/dyn))
# jet from slit: plane-jet centreline at 10 mm, 1.2 mm slit, potential core ~6 b
u0=Q/13/A_s; b=1.2
for x in (6,8.3,10):
    uc=u0 if x<=6*b else u0*math.sqrt(6*b/x)
    print("jet x=%.1f mm uc %.2f m/s dyn %.0f Pa"%(x,uc,0.5*rho*uc**2))
# fin-tip tie stress
for p in (0.69,1.03,1.5,2.0,4.5):
    bond=p*4*0.25/(1.0*0.1); print("p %.2f MPa: bond/fin-tip nominal %.1f MPa, local Kt2.5 %.1f MPa, SF yield70 %.2f, SF UTS220(nom) %.1f"%(p,bond,2.5*bond,70/(2.5*bond),220/bond))
# base ripple, 8 mm period
for teff in (1.0,1.8,3.0):
    k=2*math.pi/8e-3; t=teff*1e-3
    att=1/(math.cosh(k*t)+(390*k/127e3)*math.sinh(k*t)); print("t_eff %.1f mm att %.3f -> %.2f K pk-pk (Fourier)"%(teff,att,12.66*att))
# gang slit run-out
for D in (45,63,80):
    R=D/2; d=10.5
    half_top=math.sqrt(R**2-(R-d)**2); half_bot=math.sqrt(R**2-(R-0.5)**2)
    T=108-2*half_bot
    print("saw D %d: traverse %.1f for 108 mm bottom opening -> top opening %.1f mm (outline 125)"%(D,T,T+2*half_top))
# corrected performance
for hs,lab in ((2.0,"proposal nominal"),(3.0,"+/-20% along-slot (report map) + ripple"),(3.5,"+/-25-30%")):
    r=crosscomb(117,hotspot=hs,orifice=3.6).evaluate(15000,1.2)
    print(lab, "avg %.1f max %.1f dP %.1f"%(r['dT_avg'],r['dT_max'],r['dp_total_kPa']))
# PCM at 50 um BLT 0.079
TIM_ALT=0.079
r=crosscomb(117,hotspot=3.0,orifice=3.6).evaluate(15000,1.2)
print("PCM 0.079 BLT50: avg %.1f max approx %.1f"%(r['dT_avg']+128*(0.079-0.055)*1e0, r['dT_max']+128*(0.079-0.055)))
# clamp force
for psi in (20,30):
    print("%d psi on 117 cm2 = %.0f N, on 100 cm2 = %.0f N"%(psi, psi*6895*117e-4, psi*6895*100e-4))
# 36 LPM along-slot ratio
print("along-slot ratio at 36 LPM (centre assumption): %.1f"%(540/(0.5*rho*(2*q_slot/2/A_slot)**2)))
