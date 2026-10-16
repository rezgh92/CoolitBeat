#!/usr/bin/env python3
"""mfg lane, PRISM-15 Rev A: braze-fixture spring sizing, furnace capacity, cost roll-up
at 10k and 100k/yr, BOM export. Writes mfg_cost.out, bom.csv, params-mfg.json.
Basis: appendix/verify/ctl/cost_mass_height.out (C1 PKG-A lean: P50 162) + Rev A additions."""
import json, csv, os
D = os.path.dirname(os.path.abspath(__file__))
out = []
P = out.append

# ---------------- 1. braze fixture: differential-expansion clamp with TZM leaf springs -------
T_braze, T_room = 795.0, 20.0
dT = T_braze - T_room
h_cu = 22.3          # mm, copper stack pre-fly-cut (base blank 4.0 pre-cut -> cap top 21.1 + 1.2)
h_gr = 15.0 + 25.0   # mm, graphite bottom plate + top profiled pad in the load path
L_rod = h_cu + h_gr + 8.0   # mm, TZM tie-rod working length (8 mm spring seat)
a_cu, a_gr, a_mo = 17.5e-6, 4.5e-6, 5.6e-6   # mean CTE 20-800 C
grow = (h_cu*a_cu + h_gr*a_gr - L_rod*a_mo)*dT   # mm of interference built on heating
A_plate = 125.0*125.0  # mm2 footprint
p_target = 0.08        # MPa on the stack (plenum lane limit 0.10; architecture <= 0.2)
F_hot = p_target*A_plate  # N
n_spr, b, t, L = 8, 20.0, 2.5, 80.0   # TZM leaf springs, simply supported, centre loaded
E_tzm = 280e3          # MPa at 800 C
I = b*t**3/12
k_spr = 48*E_tzm*I/L**3   # N/mm per spring
k_tot = n_spr*k_spr
defl_hot = F_hot/k_tot
preload_cold = defl_hot - grow     # mm set with shims at room temperature
F_cold = preload_cold*k_tot
sig = (F_hot/n_spr)*L/4/(b*t**2/6)
P("## 1. Braze fixture (differential expansion, TZM leaf springs)")
P(f"thermal interference Cu stack vs TZM rods: {grow:.3f} mm at {T_braze:.0f} C")
P(f"target pressure {p_target} MPa -> {F_hot:.0f} N per plate; {n_spr} TZM springs {L}x{b}x{t}: k {k_spr:.2f} N/mm each, {k_tot:.1f} N/mm total")
P(f"hot deflection {defl_hot:.3f} mm; cold preload set {preload_cold:.3f} mm ({F_cold:.0f} N cold); spring stress hot {sig:.0f} MPa (TZM 800 C yield ~450)")
for dp in (-0.05, 0.05):
    P(f"  shim error {dp:+.2f} mm -> hot load {(defl_hot+dp)*k_tot:.0f} N = {(defl_hot+dp)*k_tot/A_plate:.3f} MPa")
# stress check on the weakest stack members at p_target
walls = p_target*7.7143/0.8
P(f"plenum wall axial {walls:.2f} MPa; fin metal (50 % solid) {2*p_target:.2f} MPa; separator span 6.914/1.8 fixed strip {0.5*p_target*(6.914/1.8)**2:.2f} MPa; arch hoop {p_target*6/1.0:.2f} MPa; OFE hot 0.2 % proof ~10 MPa")

# ---------------- 2. furnace capacity --------------------------------------------------------
cycle_h = 5.5; loads_day = 24/cycle_h*0.85*0.95   # availability 85 %, cycle slack
per_load = 60   # fixtures per load (range 30-80)
plates_furnace_yr = per_load*loads_day*365
P("\n## 2. Vacuum furnace capacity")
P(f"cycle {cycle_h} h, {loads_day:.2f} loads/day, {per_load} plates/load -> {plates_furnace_yr:,.0f} brazed plates per furnace-year")
for vol, yld in ((10_000, 0.84), (100_000, 0.935)):
    P(f"  {vol:>7,}/yr at yield {yld}: {vol/yld/plates_furnace_yr:.2f} furnaces")

# ---------------- 3. cost roll-up --------------------------------------------------------------
# cost_mass_height.out C1 (US$ at 100k/yr, P50): lines and the Rev A additions (architecture 5.4)
base100 = {"copper":22.1,"skive":20.5,"kerf":2.8,"stampings":6.8,"plenum":4.4,"header":5.3,
           "filler":14.7,"braze":17.6,"dies":2.0,"flycut":5.6,"stubs":8.3,"hw":14.0,"test":10.3}
revA_add = {"stampings":1.0,"header":1.0,"test":0.5}   # skirt, outlet arches, stepped recess, outlet row (+2.5)
# this lane's re-allocation into BOM/routing lines (sum held to the verifier line within rounding)
lines100 = [
 # (line, US$ at 100k, basis, 10k multiplier, note)
 ("CORE copper blank 0.76 kg OFE", 11.1, "0.76 kg x 14.6 US$/kg", 1.15, "verifier copper line 22.1 covers all Cu; split by mass"),
 ("GRT-L + GRT-W strip 0.28 kg", 4.1, "DDD-grate 9.4", 1.15, ""),
 ("PLN-C + PLN-F strip/bar 0.22 kg", 3.2, "0.22 kg buy", 1.15, ""),
 ("SEP + CAP + BOSS blanks 0.26 kg", 3.7, "0.26 kg buy", 1.15, ""),
 ("Skive (incl. blank mill, pocket, plane)", 20.5, "verifier skive", 2.6, "10k: 1 skiver at 35 % utilisation"),
 ("Kerf gang-saw, wax, de-wax, deburr", 2.8, "verifier kerf", 2.5, ""),
 ("GRT-L mill/punch/groove/skim", 3.3, "DDD-grate 9.4", 3.0, "10k: CNC slotting, laser windows"),
 ("GRT-W laser pierce + EP + vision", 3.0, "architecture 2.3 (2-4)", 1.6, "laser at both volumes"),
 ("PLN-C pierce + fold + PLN-F + tack", 4.4, "verifier plenum", 3.2, "10k: laser blank, soft fold tool or wire-EDM"),
 ("SEP stamp/laser + flatten", 1.5, "verifier stampings residue", 2.5, ""),
 ("CAP draw (3 stations) + trim + 2 BOSS machine + braze bosses", 6.3, "verifier header 5.3 + 1.0 Rev A", 3.0, "10k: hydroform/soft tools"),
 ("Filler BAg-8 preforms PF-1..PF-4 (~5.1 g) or Ag plate", 14.7, "verifier filler", 1.4, "Ag 65 US$/oz; 10k: laser-cut preforms"),
 ("Vacuum braze (fixture amortised, 1.6 furnaces/100k)", 17.6, "verifier braze", 2.2, "10k: 0.19 furnace, under-used"),
 ("Dies and tooling amortisation", 2.0, "verifier dies", 4.0, "10k: fewer parts carry the fold/draw tools"),
 ("Fly-cut face, pedestal, in-line ultrasonic gauge", 5.6, "verifier flycut", 1.8, ""),
 ("TAP x2, GUARD, stubs/adapters, Ni plate (T2 only, excluded)", 8.3, "verifier stubs", 1.6, ""),
 ("Hardware: 8 CSS-15P/SPR-60/SLV/WSH/clips, LF-15P frame, pins, pack", 14.0, "verifier hw (frame +2.5 inside)", 1.5, "DDD-mech D-M2"),
 ("Test: clean, He leak, proof+scan, dP, IR, bake, pack", 11.8, "verifier test 10.3 + 1.5", 2.4, "10k: manual cells"),
]
sub100 = sum(l[1] for l in lines100)
P("\n## 3. Cost roll-up (US$ per plate, P50)")
P(f"{'line':66s} {'100k':>6s} {'10k':>6s}")
sub10 = 0
for name, c, basis, m10, note in lines100:
    c10 = c*m10; sub10 += c10
    P(f"{name:66s} {c:6.1f} {c10:6.1f}")
yield100, yield10 = 0.935, 0.80
ovh = 0.12
# verifier convention: lines are good-part direct cost; P50 = sum / yield x (1 + 12 % overhead): 134.4/0.935*1.12 = 161 ~ 162
tot100 = sub100/yield100*(1+ovh)
tot10 = sub10/yield10*(1+ovh)
P(f"{'sum of lines':66s} {sub100:6.1f} {sub10:6.1f}")
P(f"factory cost = sum / yield x 1.12 overhead: 100k ({yield100}) {tot100:.1f}; 10k ({yield10}) {tot10:.0f}")
P(f"verifier C1 sum {sum(base100.values()):.1f} + Rev A additions {sum(revA_add.values()):.1f} = {sum(base100.values())+sum(revA_add.values()):.1f}; architecture 165 (155-175)")
vc = (sum(base100.values())+sum(revA_add.values()))/yield100*(1+ovh)
P(f"verifier lines + Rev A through the same yield/overhead: {vc:.1f}; this lane 100k: {tot100:.1f} (delta vs 165 {tot100-165:+.1f}); 10k: {tot10:.0f} (architecture 370-430)")
P("P10/P90 at 100k: " + f"{tot100*0.945:.0f} / {tot100*1.06:.0f} (verifier spread 153/172 on 162); 10k P10/P90 {tot10*0.93:.0f} / {tot10*1.10:.0f}")

# ---------------- 4. BOM ----------------------------------------------------------------------
bom = [
 # pn, description, qty, material, mass_g (each), process class, supplier class, lane
 ("CORE","Base + skived fin field + rim + ears + tap bosses",1,"C10100 OFE plate 4.3 mm H02 ASTM B152",282.0,"mill, skive, gang-saw, plane, flycut","skiving house (A1)","DDD-core"),
 ("GRT-L","Grate land plate 1.30: windows, recess pockets, grooves",1,"C10100 OFE strip 1.30 H02",149.0,"slot-mill/punch, laser scribe, skim","precision stamping/machining (B1)","DDD-grate"),
 ("GRT-W","Grate meter web 0.40, artwork ART-TTV-15-A, 756 holes",1,"C10100 OFE strip 0.40 O60/H01",52.0,"laser pierce, electropolish","laser job shop (B2)","DDD-grate"),
 ("PLN-C","Folded plenum corrugation, 15 channels",1,"C10100 OFE strip 0.80 O60 +-0.03",139.1,"progressive pierce, sequential fold","fin-folding / HX forming (C1)","DDD-plenum"),
 ("PLN-F","Comb end frame 2.5 x 5.78 x 120.7",2,"C10100 OFE bar H04",14.9,"gang-saw slots, skim","machining (B1)","DDD-plenum"),
 ("SEP","Separator 1.80, 46 windows",1,"C10100 OFE strip 1.80",173.7,"laser/stamp, flatten","stamping (B1)","DDD-plenum"),
 ("CAP","Drawn skirted cap 1.0, 6 arches, 2 port pockets",1,"C10100 OFE sheet 1.00 O60",259.5,"3-station deep draw + trim","deep-drawing shop (C2)","cad/params.json (cap lane pending)"),
 ("BOSS-IN","Inlet port boss, bore 20 / OD 26, guard seat",1,"C10100 OFE bar",19.2,"CNC turn","machining (B1)","cad/params.json"),
 ("BOSS-OUT","Outlet port boss, bore 20 / OD 26",1,"C10100 OFE bar",19.2,"CNC turn","machining (B1)","cad/params.json"),
 ("TAP","dP-tap tube stub 1.6 x 0.3 x 6 (-T SKUs only)",2,"C12200 Cu tube",0.1,"cut, deburr","tube shop (B3)","DDD-core 3.10"),
 ("PIN-AL2","Locating pin 2.0 x 5.5, stays in the assembly",2,"99.6 % alumina",0.1,"ground","ceramic (E1)","DDD-core 3.11"),
 ("PF-1","BAg-8 preform ladder, fin-tip joint 12-15 um",1,"BAg-8 (AWS A5.8) foil",2.0,"laser-cut/photo-etched","filler vendor (D1)","DDD-grate 7"),
 ("PF-2","BAg-8 preform sheet, web/land joint 12-15 um",1,"BAg-8 foil",1.2,"laser-cut","filler vendor (D1)","DDD-grate 7"),
 ("PF-3","BAg-8 preform, plenum feet to web, 25 um",1,"BAg-8 foil",0.9,"laser-cut","filler vendor (D1)","DDD-plenum 6"),
 ("PF-4","BAg-8 preform, separator/flats/frames/cap lands/skirt, 25-50 um",1,"BAg-8 foil",1.6,"laser-cut","filler vendor (D1)","DDD-plenum 6"),
 ("GUARD","Inlet guard: 50 um abs square-weave 316L inside-out radial diffuser",1,"316L mesh + 1.0 frame",10.0,"form, spot-weld, press-fit","filter maker (D2)","architecture 4.1"),
 ("STUB","Port stub 20 ID x 1.0 x 30 (UQD08 adapter seat)",2,"316L tube",15.75,"turn, braze/press","machining (B1)","DDD-mech 12"),
 ("CSS-15P","Captive spring screw M3, shoulder 4.00 x 40.4",8,"17-4PH H900 passivated",5.3,"turn, roll thread","fastener (D3)","DDD-mech 3.1"),
 ("SPR-60","Coil spring d1.30, OD 7.8, L0 27.5, k 10.8 N/mm",8,"302 SS",2.3,"coil, preset","spring maker (D3)","DDD-mech 3.1"),
 ("SLV-P","Stop sleeve 5.5/4.1 x 21.2",8,"303 SS",1.4,"turn","fastener (D3)","DDD-mech 3.1"),
 ("WSH-8","Washer 8.5/4.2 x 1.0",8,"301 SS",0.6,"stamp","fastener (D3)","DDD-mech 3.1"),
 ("ECL-3.2","E-clip DIN 6799 3.2",8,"spring steel",0.2,"stamp","fastener (D3)","DDD-mech 3.1"),
 ("LF-15P","Product load frame, stamped 2.0 sheet, 4 hook tabs",1,"301 SS 1/2 hard, passivated",85.0,"stamp, form","stamping (B1)","DDD-mech 4.2"),
 ("BP-15P","Backplate 0.8 x 118 sq with 8 STD-8 standoffs (board side, kit)",1,"301 SS + 17-4PH",87.6,"stamp, press-fit","stamping (B1)","DDD-mech 12"),
 ("FLT-33","Tray filter cartridge kit 33 um abs >= 150 cm2 (supplied, not in plate cost)",1,"316L / PP housing",0,"purchased","filter maker (D2)","architecture D6"),
]
with open(os.path.join(D,"bom.csv"),"w",newline="") as f:
    w = csv.writer(f); w.writerow(["pn","description","qty","material","mass_g_each","mass_g_total","process_class","supplier_class","source"])
    for r in bom: w.writerow([r[0],r[1],r[2],r[3],r[4],round(r[2]*r[4],1),r[5],r[6],r[7]])
plate_mass = sum(r[2]*r[4] for r in bom if r[0] not in ("LF-15P","FLT-33","BP-15P"))
P(f"\n## 4. BOM: {len(bom)} lines; mass on the architecture boundary (plate+stubs+springs, no frame; backplate excluded here) {plate_mass:.0f} g; +BP-15P 87.6 -> {plate_mass+87.6:.0f} g (mech 1,278); +LF-15P 85 -> FRU {plate_mass+87.6+85:.0f} g")
P("Ag per plate (route A): " + f"{(2.0+1.2+0.9+1.6)*0.72:.1f} g in {2.0+1.2+0.9+1.6:.1f} g BAg-8")

json.dump({"_meta":{"doc":"DDD-mfg.md","date":"2026-10-15","source":"mfg_cost.py"},
  "fixture":{"p_target_MPa":p_target,"F_hot_N":round(F_hot),"n_tzm_springs":n_spr,"spring_LxBxT_mm":[L,b,t],
             "k_total_N_per_mm":round(k_tot,1),"thermal_interference_mm":round(grow,3),"cold_preload_mm":round(preload_cold,3),
             "pads":"graphite ISO-63 class, top pad profiled to the cap arches, bottom pad stepped 1.30 under the ears"},
  "furnace":{"cycle_h":cycle_h,"plates_per_load":per_load,"range":[30,80],"plates_per_furnace_year":round(plates_furnace_yr),
             "furnaces_100k":round(100000/0.935/plates_furnace_yr,2),"braze_T_C":795,"vacuum_mbar":1e-5},
  "cost_usd":{"100k":round(tot100,1),"10k":round(tot10),"direct_sum_100k":round(sub100,1),"overhead":ovh,"architecture_100k":165,"verifier_C1_P50":162,
              "lines_100k":{l[0]:l[1] for l in lines100}},
  "yield":{"100k":yield100,"10k":yield10},"bom_csv":"bom.csv","plate_mass_g":round(plate_mass)},
  open(os.path.join(D,"params-mfg.json"),"w"),indent=1)
open(os.path.join(D,"mfg_cost.out"),"w").write("\n".join(out)+"\n")
print("\n".join(out))
