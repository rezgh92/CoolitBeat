"""Independent cost / value / GTM check of PRISM (ARCHITECTURE-draft.md 5.6, 6.7, 7, 10.4).
Written by the cost-market adversarial reviewer, 2026-10-14. Not derived from prism_cost.py.
All inputs are explicit (low, mid, high). Prices: LME Cu cash 14.4-14.7 k$/t (Cochilco 1 Sep 2026,
Westmetall 8 Sep 2026); silver spot ~US$65/oz (early Sep 2026 reports, 64.8-66.4)."""
import numpy as np
rng = np.random.default_rng(7)
N = 200_000
def tri(lo, mid, hi, n=N): return rng.triangular(lo, mid, hi, n)
def pct(x): return np.percentile(x, [10, 50, 90])
RHO = 8.94  # g/cm3 Cu

# ---------------- A. copper mass balance by part (PRISM-15, 125 x 125 mm) ----------------
# blank/strip footprint for stamped parts: 125 mm part on ~135 mm strip at ~130 mm pitch
strip_cm2 = 13.5 * 13.0
parts = {  # name: (buy kg, finished kg)
  "base+fins (2.5-3.0 mm blank, clamp allowance)": ((13.5*14.0)*0.27*RHO/1000, 0.27),
  "floor grate 1.0 mm":   (strip_cm2*0.10*RHO/1000, 0.11),
  "meter sheet 0.4 mm":   (strip_cm2*0.04*RHO/1000, 0.05),
  "2 plenum laminations 4.5 mm": (strip_cm2*0.90*RHO/1000, 0.55),
  "separator 1.5 mm":     (strip_cm2*0.15*RHO/1000, 0.21),
  "header bar (forging, 30-40 % flash+machining)": (0.41/0.70, 0.41),
}
buy = sum(v[0] for v in parts.values()); fin = sum(v[1] for v in parts.values())
print("A. Copper mass balance")
for k, (b, f) in parts.items(): print(f"   {k:48s} buy {b:5.2f} kg  finished {f:4.2f} kg")
print(f"   TOTAL buy {buy:.2f} kg, finished {fin:.2f} kg, scrap {buy-fin:.2f} kg  (draft: 2.5 buy / 0.85 scrap)")
lme = tri(14.4, 14.6, 15.0) # $/kg; Sep-2026 cash; COMEX ~6.65 $/lb on 21 Sep
ofe_prem = tri(2.5, 4.0, 7.0)  # $/kg OFE C10100 strip/plate/forging-bar fabrication premium (KB-M)
scrap_frac = tri(0.80, 0.88, 0.95) # clean OFE process scrap vs LME
buy_kg = tri(buy*0.92, buy, buy*1.10)
scrap_kg = buy_kg - fin
cu = buy_kg*(lme+ofe_prem) - scrap_kg*lme*scrap_frac
print("   copper line P10/50/90 $:", np.round(pct(cu), 1), " (draft 35 at 100k)")

# ---------------- B. braze filler at Sep-2026 silver ----------------
ag_oz = tri(60, 65, 72)  # $/troy oz
land_cm2 = tri(330, 410, 480)  # 6 interfaces: fin tips/grate ~120, grate/meter ~110, 4 plenum-wall interfaces ~45 each
# Route A: 25 um BAg-8 preforms (72 % Ag), density 10.0
bag8_g = land_cm2*25e-4*10.0
agA = bag8_g*0.72/31.1035*ag_oz
fabA = tri(2, 4, 8)      # foil rolling premium + laser/stamp cutting 6 preforms + skeleton loss
routeA = agA + fabA + 1.0  # + clean
# Route B: 5 um electroplated Ag on one face of each joint, masked
agB = land_cm2*5e-4*10.49/31.1035*ag_oz
overplate = tri(1.2, 1.6, 2.5)   # plating is never perfectly selective; slot walls / edges
maskB = tri(3, 6, 12)            # photoresist or mechanical masking of 5 parts + plating line cost
routeB = agB*overplate + maskB + 1.0
print("\nB. Filler (draft: 5 at 100k, 'Ag plate / BAg-8 preforms + clean')")
print("   BAg-8 per plate g P50:", round(np.median(bag8_g),1), "; Ag content $ P50:", round(np.median(agA),1))
print("   route A preforms $ P10/50/90:", np.round(pct(routeA),1))
print("   route B plated  $ P10/50/90:", np.round(pct(routeB),1))

# ---------------- C. braze furnace: load, cycle, cost ----------------
print("\nC. Vacuum braze (draft: 16 $/plate at 100k, 30-80 per load, ~1.5 furnaces per 100k/yr)")
per_load = tri(30, 50, 80)
cycle_h = tri(6, 8, 11)     # pump-down + slow ramp of a dense fixtured load to 790 C + hold + gas cool
avail_h = 7000
furn_capex = tri(0.8e6, 1.4e6, 2.2e6)  # large Mo/graphite hot-zone vacuum furnace, installed
crf = 0.16   # capital recovery 10 yr at ~10 %
maint = 0.05 # of capex per yr
energy_load = tri(600, 900, 1300)*0.11  # kWh per load x $/kWh
gas_load = tri(20, 40, 80)
fixt_per_plate_cycle = tri(2, 5, 10)    # TZM/graphite differential-expansion fixture, $300-1000, 100-200 cycles + stop-off
assy_min = tri(4, 7, 12)                # stack 6 layers + preforms, pins, fixture, vision check, per plate
lab_rate = tri(0.5, 0.8, 1.2)           # $/min burdened (TW/VN/MX)
loads_yr = 100_000/per_load
furnaces = loads_yr*cycle_h/avail_h
furn_cost_yr = furnaces*furn_capex*(crf+maint)
braze = furn_cost_yr/100_000 + (energy_load+gas_load)/per_load + fixt_per_plate_cycle + assy_min*lab_rate
print("   furnaces per 100k/yr P10/50/90:", np.round(pct(furnaces),1))
print("   braze + stack-up $/plate P10/50/90:", np.round(pct(braze),1))
print("   clamp per plate at 0.05-0.2 MPa on ~78 cm2 of land: %.1f-%.1f kN" % (0.05*7800/1000, 0.2*7800/1000))

# ---------------- D. other lines (bottom-up ranges, 100k/yr per SKU) ----------------
skive = tri(14, 20, 28); kerf = tri(2, 3, 6)
stamp3 = tri(4, 6, 9)        # grate + 486-orifice meter + separator incl. die amortisation
lamin2 = tri(4, 7, 12)       # 2 x 4.5 mm closed-slot laminations: 300 t / fine-blank, flatten/lap for braze gap
bar = tri(10, 14, 20); flycut = tri(4, 5, 8); stubs = tri(6, 8, 11); hw = tri(10, 14, 18)
test = tri(7, 10, 14)
dies_per_sku = tri(0.4e6, 0.65e6, 1.0e6)  # 5 stamping dies + forging die
die_amort = dies_per_sku/(3*100_000)
filler = 0.5*routeA + 0.5*routeB
direct = cu + skive + kerf + stamp3 + lamin2 + bar + filler + braze + flycut + stubs + hw + test + die_amort
# yield: non-reworkable 6-layer single braze; reject value ~ all value-add before test
y_mature = tri(0.88, 0.93, 0.97)
ovh = tri(0.08, 0.12, 0.16)  # factory overhead/indirects not in burdened rates
fc100 = direct/y_mature*(1+ovh)
print("\nD. PRISM-15 factory cost at 100k/yr per SKU, P10/50/90 $:", np.round(pct(fc100),0), " (draft 160; judges' rule 18-25 % yield/ovh)")
# ramp year (first 1-2 years run at ~10-30k/yr per SKU with laser-cut/CNC parts and lower yield)
direct10 = cu*1.08 + tri(30,40,50) + 6 + tri(20,26,34) + tri(24,32,42) + tri(25,32,40) + filler*1.15 + braze*1.4 + 8 + 14 + 20 + tri(12,16,22)
y_ramp = tri(0.75, 0.85, 0.92)
fc10 = direct10/y_ramp*(1+tri(0.10,0.15,0.20))
print("   at 10k/yr (laser-cut/CNC parts, ramp yield) P10/50/90 $:", np.round(pct(fc10),0), " (draft ~300)")

# ---------------- E. incumbent baselines ----------------
gb = tri(95, 110, 130)           # GB-class 100x120 skived split-flow, copper-corrected (research canonical + Cu)
coolit15 = gb + tri(8, 14, 22)   # 125-130 mm square, 1.2-1.6 kg, 1/2-3/4 in barbs: more Cu, bigger skive field
print("\nE. Incumbent: GB-class $", np.round(pct(gb),0), "; CoolIT-15-class $", np.round(pct(coolit15),0))
prem_gb = fc100/gb - 1; prem_c15 = fc100/coolit15 - 1
print("   PRISM-15 premium vs GB-class plate (draft's +45 %):", np.round(100*pct(prem_gb),0), "%")
print("   PRISM-15 premium vs a like-sized CoolIT-15-class plate:", np.round(100*pct(prem_c15),0), "%")
print("   absolute premium vs CoolIT-15-class $:", np.round(pct(fc100-coolit15),0))

# ---------------- F. PRISM-G (GPU class, 110 x 120 mm, 0.85 kg) ----------------
cuG = cu*0.85/1.60*1.05
fcG = (cuG + skive*0.9 + kerf + stamp3*0.85 + tri(3,5,8) + bar*0.8 + filler*0.8 + braze*0.85 + flycut + stubs*0.9 + hw + test + die_amort)/y_mature*(1+ovh)
print("\nF. PRISM-G at 100k/yr $:", np.round(pct(fcG),0), " (draft ~120 vs incumbent 105-110)")
print("   PRISM-G premium vs GB-class $:", np.round(pct(fcG-gb),0))

# ---------------- G. $ per kW of Tcase-limited capacity (draft capacities) ----------------
cap = {"PRISM PCM":19.4, "PRISM paste":16.6, "CoolIT-like PCM":14.8, "CoolIT-like paste":12.9}
print("\nG. $/kW at 100k (P50 costs): PRISM PCM %.1f, PRISM paste %.1f, CoolIT-15 PCM %.1f, CoolIT-15 paste %.1f" % (
  np.median(fc100)/19.4, np.median(fc100)/16.6, np.median(coolit15)/14.8, np.median(coolit15)/12.9))
print("   draft (CoolIT-like at 112): 8.2 / 9.6 / 7.6 / 8.7")

# ---------------- H. facility value of inlet headroom ----------------
print("\nH. Dry-cooler sensitivity to +1 K supply (fixed design ambient)")
def lmtd(a, b): return (a-b)/np.log(a/b) if abs(a-b) > 1e-9 else a
for appr in (6, 8, 10, 12, 15):
    for R, dTair in ((10, 10), (10, 15), (12, 8)):
        hot = appr + R - dTair; cold = appr
        if hot <= 0: continue
        L0 = lmtd(hot, cold); L1 = lmtd(hot+1, cold+1)
        print(f"   approach {appr:2d} K, fluid range {R} K, air rise {dTair:2d} K: UA saving per K {100*(1-L0/L1):4.1f} %;"
              f" fixed-unit capacity gain per K {100/(appr+R):4.1f} %")
# value per K per 100 MW, with only the UA-proportional share of installed cost scaling
dc_cost = tri(60, 120, 200)    # $/kW-thermal installed (unverified; no public price found)
ua_share = tri(0.55, 0.65, 0.8)
dua = tri(0.07, 0.095, 0.12)   # UA saving per K at 8-12 K approach (LMTD table above)
val_perK = 100_000*dc_cost*ua_share*dua/1e6
print("   value per K per 100 MW IT, US$M P10/50/90:", np.round(pct(val_perK), 2), " (draft 0.8-2.0)")
# headroom like-for-like (from the draft's own scorecard): CoolIT paste max 44.2 -> Tin 40.8; CoolIT PCM max 40.3 -> 44.7
pairs = {"PCM vs CoolIT paste (draft '+11')": 51.7-40.8, "PCM vs CoolIT-PCM (like-for-like)": 51.7-44.7,
         "paste vs paste": 47.8-40.8, "paste P90 vs paste": (85-42.0)-40.8, "PCM P90 vs CoolIT-PCM": (85-36.9)-44.7}
for k, v in pairs.items(): print(f"   headroom {k}: {v:+.1f} K")
# 15 kW class
plates15 = 100e3/15
prem15 = (fc100-coolit15)/(1-0.30)  # price premium at 30 % GM
for lab, dK in (("P50 like-for-like 7.0 K", 7.0), ("P90 like-for-like 2.2-3.4 K", tri(2.2, 2.8, 3.4))):
    ratio = val_perK*dK/(plates15*prem15/1e6)
    print(f"   15 kW class, {lab}: value/premium P10/50/90", np.round(pct(ratio), 1), " (draft 15-60x)")
# GPU class: draft table 3.3 maxima improvement 1.7-2.4 K at nominal; P90 may be ~0
platesG = 100e3*0.75/2.0
premG = (fcG-gb)/(1-0.30)
for lab, dK in (("nominal 1.7-2.4 K", tri(1.7, 2.0, 2.4)), ("draft +2-3 K", tri(2, 2.5, 3))):
    ratio = val_perK*dK/(platesG*premG/1e6)
    print(f"   GPU class {lab}: value/premium P10/50/90", np.round(pct(ratio), 2), " (draft 1.5-6x)")
print("   GPU-class plates per 100 MW: %.0f; price premium per 100 MW US$M P50 %.2f" % (platesG, np.median(platesG*premG/1e6)))

# ---------------- I. Group-A margin arithmetic ----------------
print("\nI. Margin arithmetic")
for asp in (230, 330):
    for gm in (0.18, 0.30, 0.33):
        gp = asp*gm
        print(f"   bare ASP ${asp}, GM {gm:.0%}: gross profit ${gp:.0f}; a +$50 cost premium consumes {50/gp:.0%} of it")
print("   AVC reported GM: 2Q25 24.4 %, 1Q26 29.8 %, 2Q26 32.6 % (draft assumes 17-20 %)")

# ---------------- J. budget ----------------
print("\nJ. Budget")
lab = 3.3e6/14.5
print(f"   labour per FTE-year implied: ${lab/1e3:.0f}k")
items = {"labour":3.3, "rig":0.45, "TTVs":0.3, "rigs2":0.23, "IR station":0.2, "protos":0.35, "reliab":0.25, "lab":0.15, "IP":0.25}
s = sum(items.values()); print(f"   sum before contingency {s:.2f}, +20 % = {s*1.2:.2f} (draft 6.6)")
missing = {"Build-B stamping/forging dies (draft moves tooling to M12-18 but Build B uses stamped parts at M6-9)": (0.25, 0.6),
           "confocal pressurised-flatness scanner + He leak detector + D5470 TIM tester": (0.3, 0.6),
           "CFD/FEA licences, CT/sectioning services": (0.1, 0.25),
           "lab fit-out with 25 kW heat rejection, PG25 handling": (0.1, 0.3),
           "BD / key-account + customer co-design travel, OCP membership": (0.15, 0.35)}
lo = sum(v[0] for v in missing.values()); hi = sum(v[1] for v in missing.values())
for k, v in missing.items(): print(f"   missing: {k}: US${v[0]}-{v[1]} M")
print(f"   missing total US${lo:.2f}-{hi:.2f} M vs contingency 1.1 M -> realistic 12-month {s+lo:.1f}-{s+hi+1.1:.1f} M with contingency kept")
# CM scale-up capex per 100k/yr (not in the draft)
capex = {"vacuum furnaces": (np.median(furnaces)*0.8, np.median(furnaces)*2.2), "skiving + tip planing": (0.4, 1.2),
         "test line (IR, confocal, He, dP, flush, dry)": (1.0, 1.6), "dies per SKU": (0.4, 1.0), "fixtures (2x WIP of 50/load)": (0.1, 0.3)}
print("   CM capex per 100k/yr capacity US$M:", {k: (round(v[0],1), round(v[1],1)) for k, v in capex.items()},
      " total %.1f-%.1f" % (sum(v[0] for v in capex.values()), sum(v[1] for v in capex.values())))

# ---------------- K. floor scenario (every disputed line at its most favourable value) ----------------
floor_direct = 35 + 22 + 3 + 5 + 4 + 12 + 13.0 + 17.7 + 5 + 8 + 14 + 9 + 1.3
print("\nK. Floor scenario: direct %.0f, at 95 %% yield and 10 %% overhead -> $%.0f (draft 160)" % (floor_direct, floor_direct/0.95*1.10))
# GPU-class TCO with the draft's own PRISM-G cost (120 vs 107.5)
premG_d = (120-107.5)/(1-0.30)
r = val_perK*tri(1.7, 2.0, 2.4)/(platesG*premG_d/1e6)
print("   GPU class with the draft's own US$120 PRISM-G: value/premium P10/50/90", np.round(pct(r),1))
# PRISM-G on the draft's own unit rates (non-Cu lines x0.9, Cu ~19)
print("   PRISM-G on the draft's own rates: $%.0f-%.0f" % ((19+103*0.88)*1.15, (19+103*0.95)*1.15))
