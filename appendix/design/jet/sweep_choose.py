import math
from jet_hybrid_model import SlotJetFin, j_of, plate_eval, rho
head = 0.5*rho*0.86**2   # L1 trough head at 18 LPM (HMMC-elite design H), 372 Pa
print("branch rule: (nozzle+channel) >= 6 x 372 Pa = 2.23 kPa\n")
print("| core | b/t/H | w_n | P_r | Vj | h_eff | ref | gain | branch kPa | ratio | plate dP | avg PCM | max PCM | avg LM |")
for name,b,t in (("R",0.15e-3,0.10e-3),("P",0.10e-3,0.10e-3),("X",0.30e-3,0.20e-3),("X25",0.30e-3,0.25e-3)):
    Hs = {"R":(1.5e-3,2.0e-3,2.5e-3),"P":(1.2e-3,1.5e-3),"X":(3.0e-3,4.0e-3),"X25":(3.0e-3,4.0e-3)}[name]
    wns = {"R":(0.20e-3,0.25e-3),"P":(0.15e-3,0.20e-3),"X":(0.30e-3,),"X25":(0.30e-3,)}[name]
    for H in Hs:
        for w in wns:
            for P in (6e-3,8e-3,10e-3,12e-3):
                c = SlotJetFin(name,b,t,H,w,P).cell(j_of(18))
                br = c['dp_noz']+c['dp_ch']
                core = SlotJetFin(name,b,t,H,w,P)
                r = plate_eval(core, tim="PCM pad", screen_kPa=0.4 if name in("R","P") else 0.1, hotspot_flow=1.5)
                rl = plate_eval(core, tim="liquid metal", screen_kPa=0.4 if name in("R","P") else 0.1, hotspot_flow=1.5)
                ok = "OK" if br/head>=6 else "--"
                print(f"| {name} | {b*1e3:.2f}/{t*1e3:.2f}/{H*1e3:.1f} | {w*1e3:.2f} | {P*1e3:.0f} | {c['Vj']:.2f} | {c['h_eff']/1e3:.0f} | {c['h_eff_ref']/1e3:.0f} | {c['gain']:.2f} | {br/1e3:.2f} | {br/head:.1f} {ok} | {r['dp']/1e3:.1f} | {r['avg']:.1f} | {r['max']:.1f} | {rl['avg']:.1f} |")
