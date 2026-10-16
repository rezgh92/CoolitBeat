import sys, math
sys.path.insert(0, "/home/user/Rez/docs/cooling/model")
import coldplate_model as cm
from dataclasses import replace
A0=117.0; Q=15000; LK=1.2
cm.TIM["D2D LM + Ni5"]=(0.015+0.000625,0.6)
cl=cm.coolit_like(A0)
for tim in ["paste 0.07","PCM pad","D2D LM + Ni5"]:
    r=replace(cl,tim=tim).evaluate(Q,LK)
    print(f"CoolIT-like {tim}: avg {r['dT_avg']:.1f} max {r['dT_max']:.1f}")
# CoolIT-like with LM direct + 0.8mm? no, keep 2mm
# 3A at 30.8 kW Qcap: flow, port velocity, dp
p=cm.hmmc(A0,core="R",tim="D2D LM + Ni5",base_mm=0.8)
r=p.evaluate(30800,1.2); print("3A at 30.8kW:",round(r['flow_lpm'],1),"LPM u_port",round(r['u_port'],2),"dp",round(r['dp_total_kPa'],1),"max",round(r['dT_max'],1))
# Fixed 18 LPM capacity
for Qw in (15000,20000,25000,30000):
    r=p.evaluate(Qw,18/(Qw/1000)); print(Qw, "fixed 18 LPM: avg",round(r['dT_avg'],1),"max",round(r['dT_max'],1),"Tmax",round(r['T_case_max'],1))
# 4 kW CoolIT point: CoolIT measured <36 K max incl TIM at 6 LPM on 25 cm2
for lab,pp in [("CoolIT-like",cm.coolit_like(25)),("T1",cm.hmmc(25,core="R",tim="PCM pad")),("3A",cm.hmmc(25,core="R",tim="D2D LM + Ni5",base_mm=0.8))]:
    r=pp.evaluate(4000,1.5); print("4kW",lab,round(r['dT_avg'],1),round(r['dT_max'],1), "flow",r['flow_lpm'])
# caloric under die with isothermal NTU
heff=127e3; q=350e4; dTloc=2*6.7
mcp=q/dTloc; NTU=heff/mcp; cf=1/(1-math.exp(-NTU))-1/NTU
print("die NTU",round(NTU,3),"cal_frac",round(cf,3),"cal",round(cf*dTloc,2))
# LM 30um penalty consistency
print("LM 30um R''", 30e-6/22*1e4+0.004)
# 3A at 350 with 45um BLT and Si 775um
for blt,rsi in [(30,0.05),(45,0.065)]:
    rlm=blt*1e-6/22*1e4+0.004+0.000625
    die=7.3+350*(rlm+0.8e-3/390*1e4+1e4/127e3); print("BLT",blt,"Si",rsi,"Tj-in",round(die+350*rsi,1))
