import statistics as st
P=15000.0
cp={"Coldplate 1":[26.8,29.9,31.5,34.6,41.5,29.0,29.0,37.7],
    "Coldplate 2":[34.7,33.5,37.6,39.3,44.2,33.6,30.8,27.6],
    "Coldplate 3":[32.3,34.7,39.0,39.0,44.0,35.2,32.6,27.7]}
allv=[v for l in cp.values() for v in l]
print("n=",len(allv),"mean=%.2f sd=%.2f min=%.1f max=%.1f"%(st.mean(allv),st.stdev(allv),min(allv),max(allv)))
for k,l in cp.items():
    print(k,"avg=%.2f max=%.1f min=%.1f spread=%.1f R_avg=%.5f R_max=%.5f"%(st.mean(l),max(l),min(l),max(l)-min(l),st.mean(l)/P,max(l)/P))
pos=[st.mean([cp[k][i] for k in cp]) for i in range(8)]
print("per-position avg:",[round(x,1) for x in pos], "spread=%.1f"%(max(pos)-min(pos)))
for i in range(8):
    vals=[cp[k][i] for k in cp]; print(" TC%d plate-to-plate spread=%.1f"%(i+1,max(vals)-min(vals)))
print("R avg=%.5f K/W, R max=%.5f, R min=%.5f"%(34.4/P,44.2/P,26.8/P))
# caloric
Q=18.0/60/1000 # m3/s
for name,rho,c in [("PG25",1010,3940),("water",990,4180)]:
    m=Q*rho; dT=P/(m*c); print(name,"mdot=%.4f kg/s dT=%.2f K outlet=%.1f mean=%.1f"%(m,dT,45+dT,45+dT/2))
# 4kW
for q in [4.28,6.0,6.06]:
    m=q/60*0.995; print("4kW @%.2f LPM water dT=%.2f K"%(q,4000/(m*4180)))
print("4kW Tr<0.009 -> dT<%.1f K"%(0.009*4000))
# unit resistance scenarios 15kW
for A in [50,61,64,79,81,100,150]:
    print("A=%d cm2: q=%.0f W/cm2, R''avg=%.3f, R''max=%.3f cm2K/W"%(A,P/A,0.00229*A,0.00295*A))
print("4kW: 200 W/cm2 -> A=%.1f cm2, R''=%.3f cm2K/W"%(4000/200,0.009*20))
print("implied A from 4kW R'' 0.18: avg %.0f cm2 (%.0f mm sq), max %.0f cm2 (%.0f mm sq)"%(0.18/0.00229,(0.18/0.00229)**0.5*10,0.18/0.00295,(0.18/0.00295)**0.5*10))
# pumping power
for dp in [30e3,55.2e3,100e3,150e3]:
    print("15kW: dP=%.0f kPa hydraulic=%.1f W (%.3f%%), at 30%% pump eff=%.0f W"%(dp/1e3,dp*Q,100*dp*Q/P,dp*Q/0.3))
print("4kW: 55.2 kPa @6LPM hydraulic=%.1f W (%.3f%%)"%(55.2e3*1e-4,100*55.2e3*1e-4/4000))
# TIM share
for Rtim in [0.05,0.1,0.2]:
    for A in [61,80,100]:
        print("TIM R''=%.2f cm2K/W, A=%d: dT_TIM=%.1f K (%.0f%% of 34.4)"%(Rtim,A,Rtim*P/A,100*Rtim*P/A/34.4))
print("case-to-mean-fluid R=%.5f K/W"%((34.4-6.3)/P))
print("10x claim: 15/1.4=%.1f ; 4x: 15/4=%.2f"%(15/1.4,15/4))
print("ORNL R''=%.3f cm2K/W (75mm sq)"%(0.0069*56.25))
print("GB300 vendor 0.013 K/W x ~ (B300 ~ 2x8.5cm2=17? ) skip")
