# Derived-number checks for gap-cost-volume-and-market-anchors.md (2026-10-13)
# All inputs are tagged in the report; this file only guarantees the arithmetic.

# 1. Canonical factory-cost model, bare GB-class skived/welded Cu plate (100 x 120 mm), US$ per plate
# element: (10k low, 10k high, 100k low, 100k high, 1M low, 1M high)
cost = {
 "OFHC Cu stock 1.5-2.2 kg @ US$10-12/kg, net of 50-70% swarf credit": (14,22, 12,19, 11,17),
 "Skived fin core (2-5 min/plate, machine US$150-400k)":              (25,40, 15,28, 11,20),
 "Cover + ports (CNC at 10k/100k, stamped+CNC finish at 1M)":          (30,50, 12,25, 6,12),
 "Join (vacuum braze / green-laser / FSW)":                            (8,15, 4,9, 2.5,6),
 "Electroless Ni-P 8-12 um on wetted path + contact face":            (6,12, 4,7, 2.5,5),
 "Leaf spring, bracket, screws, O-rings":                              (14,22, 9,16, 6,11),
 "Hose stubs / fittings (UQDs excluded)":                              (10,18, 6,12, 4,8),
 "100% He leak + proof pressure + flow/dP test":                       (6,10, 3,6, 2,4),
 "Yield loss, scrap, overhead, logistics":                             (8,16, 5,11, 3,7),
}
tot = [0]*6
for v in cost.values():
    for i in range(6): tot[i]+=v[i]
print("Factory cost bare plate low/high: 10k %.0f-%.0f | 100k %.0f-%.0f | 1M %.0f-%.0f" % tuple(tot))
print("Mid-points: 10k %.0f | 100k %.0f | 1M %.0f" % ((tot[0]+tot[1])/2,(tot[2]+tot[3])/2,(tot[4]+tot[5])/2))

# 2. Morgan Stanley BOM consistency (A: TechRadar / igor'sLAB)
tray=2260; plate=300; sw_plate=200; rack=49860
print("18 compute trays x US$2,260 =", 18*tray, "; residual for 9 switch trays + rack manifold/QDs =", rack-18*tray)
print("per compute tray: 6 plates x US$300 =", 6*plate, "; residual for VR plates/hoses/QDs/tray manifold =", tray-6*plate)
print("switch plates 18 x US$200 =", 18*sw_plate, "; residual for manifolds/QDs/hoses at rack level =", rack-18*tray-18*sw_plate)
print("plate share of rack cooling BOM = %.0f %%" % (100*(108*plate+18*sw_plate)/rack))

# 3. What the US$300 'plate' line can contain if it is a plate ASSEMBLY (plate + 2 UQD halves + hoses)
for uqd in (15,25,40):
    for hose in (8,15):
        asm = uqd*2+hose
        print("UQD US$%d x2 + hoses US$%d = US$%d of the US$300 -> bare-plate price <= US$%d" % (uqd,hose,asm,300-asm))

# 4. Gross-margin cross-check: AVC company GM ~17-20% (KB-M), plate SKU GM assumed 25-40%
for gm in (0.25,0.30,0.40,0.55):
    print("ASP 300, SKU GM %.0f%% -> supplier cost US$%.0f ; ASP 400 -> US$%.0f" % (gm*100, 300*(1-gm), 400*(1-gm)))

# 5. Rack volumes -> plates
plates_per_rack = {"GB300 NVL72 (108 CPU/GPU + 18 switch)":126, "VR NVL144 (incl. NIC/VR plates, est.)":150}
for yr,(lo,hi) in {"2025":(25e3,35e3),"2026":(35e3,80e3),"2027":(60e3,120e3)}.items():
    print(yr, "racks %.0fk-%.0fk -> plates %.1f-%.1f M (126/rack) ; %.1f-%.1f M (150/rack)" % (lo/1e3,hi/1e3,lo*126/1e6,hi*126/1e6,lo*150/1e6,hi*150/1e6))
# GPU-based cross-check: Blackwell+Rubin GPUs 2026 8-12 M, NVL share 60-75 %
for g in (8e6,12e6):
    for s in (0.6,0.75):
        print("2026 GPUs %.0f M, NVL share %.0f%% -> %.0fk NVL72-equivalent racks" % (g/1e6,s*100,g*s/72/1e3))
# Revenue-based cross-check: NVL rack ASP US$3.0-3.5 M; NVL-based revenue 2026 US$150-250 B
for rev in (150e9,250e9):
    for asp in (3.0e6,3.5e6):
        print("revenue US$%.0f B / rack US$%.1f M -> %.0fk racks" % (rev/1e9,asp/1e6,rev/asp/1e3))

# 6. TCS US$/kW cross-check vs CoolIT US$11 B (2026)
inrack = 49860/140e3  # US$/W
print("in-rack BOM US$/kW IT = %.0f" % (inrack*1e3))
for tcs_per_kw in (550,700,850):
    print("US$11 B / US$%d per kW -> %.1f GW of DLC IT capacity in 2026" % (tcs_per_kw, 11e9/tcs_per_kw/1e6))
print("bottom-up GW: 60k racks x 140 kW = %.1f GW + ASIC 3-5 GW" % (60e3*140e3/1e9))

# 7. CDU per rack and -10 kPa monetisation
cdu_price=(250e3,500e3); racks_per_cdu=(12,14)
for p in cdu_price:
    for r in racks_per_cdu:
        per_rack=p/r
        # one extra rack per CDU from 20-30 kPa saved head (2-3 plates in series x 10 kPa)
        saving_per_rack = per_rack/(r+1)
        print("CDU US$%.0fk / %d racks = US$%.0f per rack; +1 rack/CDU saves US$%.0f per rack = US$%.1f per plate (126)" % (p/1e3,r,per_rack,saving_per_rack,saving_per_rack/126))
# hydraulic power of 10 kPa at 18 LPM
Q=18/60/1000; dP=10e3
print("10 kPa x 18 LPM = %.1f W hydraulic per plate; per 140 kW rack at 1.2 LPM/kW (168 LPM, 2.5 plates series-equiv): %.0f W hydraulic, ~%.0f W electrical (50%% w2w)" % (Q*dP, 168/60/1000*25e3, 2*168/60/1000*25e3))
print("per 100 MW IT: %.0f kW electrical = %.2f GWh/yr = US$%.0fk/yr at US$0.08/kWh" % (2*168/60/1000*25e3/140e3*100e6/1e3, 2*168/60/1000*25e3/140e3*100e6*8760/1e9, 2*168/60/1000*25e3/140e3*100e6*8760/1e9*80e3/1e3))

# 8. +1 K supply temperature value
for approach in (8,10,12):
    print("dry-cooler approach %d K: +1 K supply = +%.0f %% capacity" % (approach, 100/approach))
for capex in (80,200):
    print("dry cooler US$%d/kW thermal: 10%% less area per K on 100 MW = US$%.1f M per K" % (capex, 0.10*capex*100e3/1e6))
# trim chiller energy in a hot climate: 150 h/yr fewer trim hours per K, chiller COP 5, 100 MW
for hrs in (100,200):
    e = 100e6/5*hrs/1e9
    print("hot climate: %d fewer trim-chiller hours per K -> %.1f GWh/yr = US$%.2f M/yr per K (US$0.08/kWh)" % (hrs,e,e*80e3/1e6))
# chip power sensitivity
for s in (0.002,0.005):
    e=100e6*s*8760/1e9
    print("Tj -1 K at %.1f %%/K on 100 MW = %.1f GWh/yr = US$%.2f M/yr" % (s*100,e,e*80e3/1e6))

# 9. 800 VDC power-shelf plates
for rack_kw,eff in ((600,0.975),(600,0.985),(1000,0.975),(1000,0.985)):
    print("rack %d kW at %.1f%% in-rack conversion efficiency -> %.0f kW of conversion heat" % (rack_kw,eff*100,rack_kw*(1-eff)/eff))
for racks in (10e3,30e3):
    for units in (8,20):
        for asp in (50,150):
            print("%.0fk Kyber-class racks x %d power units x US$%d = US$%.0f M/yr, %.2f M plates" % (racks/1e3,units,asp,racks*units*asp/1e6,racks*units/1e6))

# 10. Liquid-metal / indium TIM material cost
ga_price=(400,700)  # US$/kg gallium-alloy class 2025-26 (KB-L)
for p in ga_price:
    print("liquid metal 0.1-0.2 g per package at US$%d/kg = US$%.2f-%.2f material" % (p,0.1e-3*p,0.2e-3*p))
# indium foil over 40 cm2 x 0.15 mm, density 7.31 g/cm3
m=40*0.015*7.31
for p in (300,500):
    print("indium preform %.1f g at US$%d/kg = US$%.1f material" % (m,p,m*p/1e3))

# 11. ECAM core cost from throughput
vol = 10*12*0.2*0.5  # cm3 of copper in a 100x120 mm x 2 mm fin field at 50% solid
for rate in (5,20):   # cm3/h per machine (KB-L)
    hrs = vol/rate
    for machine in (0.5e6,1.0e6):
        amort = machine/5/ (8000/hrs)  # 5-yr, 8,000 h/yr
        print("ECAM fin field %.0f cm3 at %d cm3/h = %.1f h; machine US$%.1f M -> amortisation US$%.0f per plate" % (vol,rate,hrs,machine/1e6,amort))
