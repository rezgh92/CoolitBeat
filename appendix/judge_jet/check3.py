import sys, math
sys.path.insert(0, 'docs/cooling/appendix/design/jet')
import jet_hybrid_model as J
from coldplate_model import TIM, K_CU
rho, cp = J.rho, J.cp
A=117e-4; Q=15000; q=Q/A
def plate(h, tim, lpm=18, base=1.0e-3, hs_flow=1.5):
    mcp = lpm/60e3*rho*cp; dTo = Q/mcp; NTU = h*A/mcp
    cal = dTo*(1/(1-math.exp(-NTU))-1/NTU)
    R, sc = TIM[tim]
    t = q*R*1e-4; b = q*base/K_CU; c = q/h
    avg = cal+t+b+c; mx = avg + hs_flow + sc*(q/1.28e6)
    Qcap = Q*(85-45-cal-(hs_flow+sc))/(t+b+c)/1e3
    return avg, mx, cal, Qcap
print("TIM table", TIM)
for lab, h in (("JH-R model",146.5e3),("JH-R corr",141.7e3),("JH-R strict",137.4e3),("HMMC-R",127.2e3),("JH-X model",87.9e3),("JH-X corr",80.2e3),("JH-X strict",73.9e3)):
    for tim in ("paste 0.07","PCM pad","liquid metal"):
        a,m,cal,qc = plate(h,tim)
        print(f"{lab:12s} {tim:12s}: avg {a:.1f} max {m:.1f} (cal {cal:.1f}) Qcap {qc:.1f}")
# nozzle dP sensitivity: Cd-based orifice loss on 0.22x0.15 opening at Vj
c = J.JH_R.cell(J.j_of(18))
for Cd in (0.6,0.65,0.7,0.75):
    dp = 0.5*rho*c['Vj']**2/Cd**2 + 0.5*rho*0.5*c['V_slot']**2
    print(f"Cd {Cd}: nozzle dP {dp/1e3:.2f} kPa (model {c['dp_noz']/1e3:.2f}); plate ~{(dp + c['dp_ch']+c['dp_ret'] + 2570+610+400)/1e3:.1f} kPa")
