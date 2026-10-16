# DDD-mfg: manufacturing package (BOM, routing, braze fixture, inspection, GD&T, cost, suppliers, FAI), PRISM-15 Rev A

> Detailed design definition, lane `mfg`, 2026-10-15. Parent: `docs/cooling/03-architecture.md` (sections 2.2, 5.1-5.5). Binding interfaces: `DDD-core.md` / `params-core.json`, `DDD-grate.md` / `params-grate.json`, `DDD-plenum.md` / `plenum_sep_data.json`, `DDD-mech.md` / `params-mech.json`; cap, bosses and guard provisional from `cad/params.json` (cap lane pending). Derivations: `design/mfg_cost.py` -> `mfg_cost.out`; BOM `design/bom.csv`; parameters `design/params-mfg.json`. Cost basis `appendix/verify/ctl/cost_mass_height.out` (C1 PKG-A lean, P50 US$162) plus the architecture's Rev A additions (US$2.5). Dimensions mm; convention X along the fins, Y along the lines, Z up from the die face (datum A), origin at the fin-field centre.

## 0. Summary

| Item | Value | Basis |
|---|---|---|
| Parts per plate | 11 copper parts (CORE, GRT-L, GRT-W, PLN-C, 2 PLN-F, SEP, CAP, BOSS-IN, BOSS-OUT, 2 TAP on -T SKUs), 4 BAg-8 preforms, 2 alumina pins, GUARD, 2 STUB; hardware kit 8 x (CSS-15P, SPR-60, SLV-P, WSH-8, e-clip); LF-15P frame; BP-15P backplate stays with the board | section 1, `bom.csv` |
| Braze | one vacuum cycle, 795 ± 5 C, ≤ 1e-5 mbar, BAg-8 (route A baseline; B/C per E1); fixture pressure **0.08 MPa (0.06-0.10)** on the stack, 60 plates per load (30-80) | section 3; deviation D-F1 |
| Furnaces | 1.4-1.6 per 100k/yr (60-52 plates per load, 5.5 h cycle, 85 % availability, 93.5 % yield) | `mfg_cost.out` §2; architecture 1.6 |
| Factory cost P50 | **US$165.2 at 100k/yr** (P10/P90 156/175); **US$388 at 10k/yr** (361/427) | `mfg_cost.out` §3; architecture 165 (155-175) and 370-430 |
| Mass | plate + stubs + springs 1,250 g; + backplate 1,337 g; FRU with LF-15P 1,422 g | `bom.csv`; deviation D-F3 |
| External seams | 1 perimeter lap (skirt foot to core land) + 2 bosses + 2 tap stubs (-T only) | architecture 5.1 |
| Critical characteristics (CC) | 14, each with a 100 % or lot gauge and an owning station (section 4); CpK ≥ 1.33 on He leak (log rate) and on 18 LPM dP | section 4 |

## 1. Bill of materials and material specifications

Full BOM with masses, process and supplier class in `bom.csv` (25 lines). Masses: lane values where they exist, CadQuery `cad/out/assembly_report.json` for the cap and bosses.

| PN | Qty | Description | Material specification | Finished mass g | Process class |
|---|---:|---|---|---:|---|
| CORE | 1 | base + 360 skived fins + rim + skirt land + 8 ears + 2 tap bosses | C10100 OFE (ASTM B152, O ≤ 5 ppm, ≥ 101 % IACS), plate 4.3 mm (4.2-4.5), H02, grain ≤ 0.050 mm; mill cert lot-traced | 282 | mill, skive, wax, gang-saw, plane, deburr, post-braze fly-cut |
| GRT-L | 1 | land plate 1.30: 15 windows, 7 recess pockets, 56 capillary grooves, D1/D2 | C10100 strip 1.30 ± 0.02 (after skim), H02 | 149 | slot mill (7-spindle at volume) / closed-slot punch / laser scribe / skim |
| GRT-W | 1 | meter web 0.40, artwork ART-TTV-15-A (378 inlet, 378 outlet holes) | C10100 precision strip 0.40 ± 0.010, O60 or H01 | 52 | fibre-laser pierce, electropolish 3-5 µm, 100 % backlit vision |
| PLN-C | 1 | square-wave corrugation, 16 walls, 15 channels 6.914 x 5.00, H 5.80, 32 end tabs, 14 top windows, 8 outlet slots, bleeds | C10100 strip 0.80 ± 0.03, O60 (EN 1652 precision) | 139 | progressive pierce + sequential corrugating fold (Build A: wire-EDM from 5.8 plate) |
| PLN-F | 2 | comb end frame 2.50 x 5.78 x 120.70, 16 slots 0.90 x 1.00 | C10100 bar, H04 | 2 x 14.9 | gang-saw slots, skim, chamfer |
| SEP | 1 | separator 1.80, 14 inlet + 32 outlet windows 5 x 10, pin holes | C10100 strip 1.80 ± 0.03 | 174 | stamp/laser, flatten to 0.03 |
| CAP | 1 | drawn skirted cap 1.0: lid at z 12.10-13.10, 2 inlet + 4 outlet arches 12 x 8 internal, 2 cross-domes, 2 port pockets Ø26, skirt to z 1.50, 2 tap notches | C10100 sheet 1.00 ± 0.03, O60 (anneal between draws) | 260 | 3-station deep draw + trim + pierce (Build A: hydroform on soft tools) |
| BOSS-IN / BOSS-OUT | 1 + 1 | port boss bore 20.0 H9 / OD 26, z 20.1-30.0; inlet boss carries the guard seat Ø18.1 | C10100 bar Ø28 | 2 x 19.2 | CNC turn, brazed in the single cycle |
| TAP | 2 | dP-tap tube stub 1.6 x 0.3 x 6.0 in the core boss counterbore (-T SKUs only) | C12200 DHP tube | 0.2 | cut, deburr, brazed in the cycle |
| PIN-AL2 | 2 | locating pin Ø2.00 x 5.5, stays in the assembly (core/grate/separator/pins see D-F2) | 99.6 % alumina, ground h6 | 0.2 | purchased |
| PF-1 | 1 | BAg-8 preform ladder, fin-tip/rim joint: 15 cut-outs 1.80 x 108.6 + perimeter | BAg-8 (AWS A5.8, 72Ag-28Cu) foil 12-15 µm or perforated 25 µm | 2.0 | photo-etched or laser-cut; vision at placement |
| PF-2 | 1 | BAg-8 sheet, GRT-W/GRT-L joint: 7 cut-outs 3.30 x 109.6, 8 cut-outs 1.80 x 108.6 | BAg-8 foil 12-15 µm | 1.2 | same |
| PF-3 | 1 | BAg-8 sheet, PLN-C feet + PLN-F to web: 7 + 8 cut-outs per DDD-plenum 6 | BAg-8 foil 25 µm; 50 µm frame strips | 0.9 | same |
| PF-4 | 1 | BAg-8 sheet, top flats/flanges/frames to SEP, SEP to cap lands, skirt foot ring, boss rings | BAg-8 foil 25 µm; rings 0.5 mm wire | 1.6 | same |
| GUARD | 1 | 50 µm absolute square-weave 316L inside-out radial diffuser, Ø18 x 8, ≥ 25 cm2 | 316L mesh 325 x 2300 dutch-twill equivalent on a 1.0 frame | 10 | form, resistance-weld, press-fit after fly-cut |
| STUB | 2 | port stub 20 ID x 1.0 x 30, UQD08 adapter seat | 316L tube | 2 x 15.8 | turn; press + O-ring or post-braze TIG to the boss (cap lane) |
| CSS-15P / SPR-60 / SLV-P / WSH-8 / ECL-3.2 | 8 each | captive spring screw set | 17-4PH H900 / 302 SS / 303 SS / 301 SS / spring steel | 79 | purchased to `DDD-mech` 3.1 |
| LF-15P | 1 | product load frame, hook tabs | 301 SS 1/2 hard 2.00, passivated | 85 | stamp, form |
| BP-15P + 8 STD-8 | 1 | backplate with standoffs (board side) | 301 SS 0.8 + 17-4PH | 88 | stamp, press-fit |
| FLT-33 | 1 | tray filter cartridge kit, 33 µm absolute, ≥ 150 cm2 (ships with the plate, not in the plate cost) | 316L / PP | - | purchased |

Copper buy per plate 1.52 kg (CORE 0.76, grate 0.28, plenum 0.22, SEP + CAP + bosses 0.26) against the verifier's 1.43 kg; finished copper 1.09 kg. Silver 4.1 g per plate (route A, 5.7 g BAg-8); route B 8-10 µm plating ≈ 2.3 g Ag; route C2 0.5 g Sn.

**Material controls common to all copper parts:** oxygen ≤ 5 ppm (hydrogen embrittlement, ASTM B577 on route C); no S, P or Pb bearing lubricants (braze wetting); vapour degrease + alkaline clean + DI rinse ≤ 4 h before stacking; parts handled in nitrile gloves, stored in N2 cabinets ≤ 72 h before braze; grain ≤ 0.035 mm on PLN-C and CAP strip (orange peel at 40 % bend strain).

## 2. Routing / process sheet (in order; cycle time per plate at 100k/yr; station owning each tolerance)

Stations are numbered by stream: 1xx core, 2xx grate, 3xx plenum/separator, 4xx cap/bosses, 5xx filler and stack, 6xx braze, 7xx post-braze, 8xx test and pack. Cycle times are machine minutes per plate at the volume process (prototype values in brackets where different). "Owns" lists the characteristics whose tolerance is created at that station and gauged there.

| Op | Station | Process | Cycle min | Owns (tolerance) | Source |
|---|---|---|---:|---|---|
| 110 | Blank mill (twin-spindle VMC) | 141 x 141 x 4.3 blank: both faces to 4.00 ± 0.02, flat 0.02, parallel 0.02; pocket 108.70 x 108.30 x 1.00 ± 0.02; outline 125 ± 0.10, ears, lap face 121.40 ± 0.05, land z 1.50 ± 0.05, tap bosses, pin holes Ø2.0 H7, EDM tap holes (-T) | 3.0 (6) | pocket size/position ± 0.05/0.03; pre-braze datum A'; rim/land heights; pin positions Ø0.03 | core 3 |
| 115 | Alkaline clean | spray clean, DI rinse, dry | 0.5 | water-break free | core 2 |
| 120 | **Skive** (CTX-class machine, 108.3 carbide blade) | 360 strokes, 0.300 feed, fins 2.10 ± 0.05 as-skived | 5.0 | fin pitch 0.300 ± 0.005 (cum. ± 0.03); thickness 0.150 ± 0.020; lean ≤ 0.05; root fillet | core 4 |
| 125 | Wax impregnate (batch 20) | Aquabond-class wax, vacuum 80-100 C, level flush | 1.5 | - | core 5 |
| 130 | **Gang-saw kerfs** (15-blade arbor Ø20 x 0.28) | 15 kerfs + 2 edge trims, one pass, depth 1.925 ± 0.025 from the tip plane | 1.5 | kerf position ± 0.05; width 0.30 +0.05/-0; depth/floor stub 0.05-0.10; edge channel 0.35 +0.10/-0 | core 5 |
| 135 | **Diamond plane** (fly-cut along X) | tips and rim top to z 2.80 (4.00 above A'), one pass, wax in | 1.0 | tip plane flatness ≤ 0.020 (route B ≤ 0.010); tip-to-rim coplanar 0.02; fin height 2.00 ± 0.02 | core 4.6-4.7 |
| 140 | De-wax + clean (batch) | 70-90 C DI ultrasonic x 2, alkaline, DI, N2 dry; FTIR swab per lot | 1.0 | residue (water-break, FTIR) | core 5 |
| 145 | Deburr (batch) | ultrasonic + 3-5 µm electropolish; optical profilometer 3 kerfs x 5 fins per lot | 0.5 | burr ≤ 15 µm; no slivers | core 5 |
| 150 | Core inspection | vision fins 1/90/180/270/360; laser-line tip map; CMM pocket/pins | 1.0 (CC-1..3 gauged) | - | section 4 |
| 210 | GRT-L blank + pierce | 1.30 strip, outline 122.6 (see D-F2), D1 Ø3.00 H7, D2 slot | 0.2 | outline ± 0.10; D1/D2 ± 0.02 | grate 3 |
| 215 | GRT-L pockets (7-spindle slotting head; CNC at Build A) | 7 recesses 2.70 x 0.80 x 109, one pass | 1.0 (1.5) | recess width +0.05/-0; depth ± 0.03; floor 0.50 ± 0.04; lip Ra ≤ 1.6 | grate 3 |
| 220 | GRT-L windows (closed-slot punch from the fin face; laser at Build A) | 13 x 1.20 x 108, 2 x 0.60 x 108 | 0.3 (2.0) | window width +0.05/-0; position ± 0.03 | grate 3 |
| 225 | Laser scribe grooves | 56 capillary-break grooves 0.15 x 0.08, both faces | 0.3 | groove w ± 0.03, d ± 0.02 | grate 3, 7 |
| 230 | Stress relieve 300 C / 1 h (batch) + both-face skim | fly-cut both faces to 1.30 ± 0.02 | 0.8 | flatness 0.020 field / 0.030 overall; Ra ≤ 0.8; burr ≤ 0.015 | grate 3 |
| 240 | **GRT-W laser pierce** (single-mode fibre, N2, flatbed) | 756 holes, entry from the plenum face; ID mark | 1.3 | hole w/h ± 0.010 (area ± 2 %); position ± 0.020; taper ≤ 1° | grate 4 |
| 245 | Electropolish + 100 % backlit vision | 3-5 µm; every hole area ± 1 %, position; artwork checksum | 0.6 | dross ≤ 0.015; Cd direction (entry rounding ≤ 0.03) | grate 4, 9.3 |
| 310 | PLN-C progressive pierce + blank (laser at Build A) | windows 5 x 10, slots 1.80, bleeds Ø0.6/1.1, tabs, reliefs; developed width 180.95 ± 0.05 | 0.2 (3.0) | feature position ± 0.02; slot width; bleed Ø | plenum 3.2-3.3 |
| 315 | Selective strip plating (routes B/C only) | Ag 8-10 µm bands on the flat blank | 0.5 | Ag thickness by XRF per band | plenum 6 |
| 320 | **Sequential corrugating fold** (32 folds; wire-EDM from 5.8 plate at Build A) | two 90° wipe folds per index, 0.6 punch nose, over-bend 1-2° | 0.7 (180) | pitch 7.7143 ± 0.05; H 5.80 ± 0.03; wall perpendicular ≤ 0.5°; r_i 0.60 | plenum 3.1, 3.5 |
| 325 | PLN-F frames | bar, gang-saw 16 slots 0.90 x 1.00, skim to 5.78 -0.02/-0.05, chamfer | 0.6 | slot pitch ± 0.03; height; Ra 0.8 | plenum 4 |
| 330 | Plenum sub-assembly | press frames on tabs, 4 laser tacks, height gauge | 0.7 | sub-assembly H 5.80 ± 0.03 over the frames; tab engagement | plenum 2.3 |
| 340 | SEP stamp (laser at Build A) + flatten | 1.80 strip, 46 windows, pins, outline; roller flatten | 0.4 (2.0) | window position ± 0.05; flatness 0.03; burr ≤ 0.02 toward the cap side | plenum/sep data |
| 345 | Clean (plenum, SEP, GRT-L, GRT-W; batch) | vapour degrease, alkaline, DI, N2; ISO 16232 sample | 0.5 | no particle > 50 µm | all lanes |
| 410 | **CAP deep draw**, 3 stations + inter-draw anneal (batch 450 C / 30 min, N2) | station 1 skirt box draw to 125 x 125 x 12.8; station 2 arches 12 x 8 and cross-domes; station 3 port pockets Ø26 and lid flatten; trim + pierce port holes and tap notches | 0.5 (4, hydroform) | skirt outer 123.4 ± 0.15 (D-F2), lid z 13.10 ± 0.10 and land flatness 0.05 (IR-M2), arch height 8.0 ± 0.15, pocket Ø ± 0.05, skirt foot square 0.1 | cad/params cap; mech IR-M2 |
| 415 | Cap anneal + clean | 450 C N2 soft anneal, degrease | 0.3 | hardness ≤ 55 HV (draw-quality for the lap seam) | - |
| 420 | BOSS-IN / BOSS-OUT CNC turn | bore 20.0 H9, OD 26 h9, pilot step into the port pocket 0.05 clearance, guard seat Ø18.1 H8 x 8 (inlet), stub seat; TAP stubs cut | 1.0 each (2.0) | bore, pilot concentricity Ø0.05, seat Ø | cad/params bosses |
| 510 | Preform cut (photo-etch or laser, vendor) | PF-1..PF-4, boss rings | vendor | cut-out position ± 0.05 (vision at 520) | grate 7, plenum 6 |
| 520 | **Stack build** (robot at volume, manual at Build A) | core on the fixture base → PF-1 → GRT-L → PF-2 → GRT-W → PF-3 → PLN-C+F → PF-4 → SEP → CAP (skirt over the rim lap face) → boss rings, bosses, TAP stubs; alumina pins through D1/D2; stop-off painted (section 3); preform-presence vision | 1.5 (4) | registration ± 0.03 (pins); preform presence 100 %; XRF Ag/Sn per strip (routes B/C) | section 3 |
| 530 | Fixture close | top pad set, TZM springs shimmed to the cold preload 0.09 mm (502 N), load cell check on 1 in 20 | 0.5 | cold preload ± 0.02 mm | section 3 |
| 610 | **Vacuum braze** | 60 fixtures per load; pump to ≤ 1e-5 mbar; 10 K/min to 500 C, hold 20 min (outgas), 10 K/min to 760 C, 5 K/min to 795 ± 5 C, hold 6 min (thermocouples on 3 witness fixtures), furnace cool to 700 C, N2 2 bar gas quench to 100 C; cycle 5.5 h | 5.5 furnace-min equivalent | joint formation; tie bond fraction ≥ 0.70 (CT per lot); no fillet in grooves/orifices (E1 sections) | architecture 5.1; section 3 |
| 620 | Unfixture, visual, witness coupons | remove pads; check skirt seam fillet, boss fillets; peel coupon per load | 0.7 | - | section 4 |
| 630 | **Dry He leak** (chamber, accumulation; part evacuated to 1 mbar then He at 1 bar(g)) | before any wet step; ≤ 1e-6 mbar·L/s | 3.0 (3 chambers) | **CC-11 leak**, CpK ≥ 1.33 on log10 rate | architecture 5.3 |
| 640 | **IR flow screen**, coated as-brazed face | high-emissivity paint on the base, 18 LPM 45 C water with a 10 K step, IR camera 5-10 mm resolution; blow-dry + vacuum dry 60 C | 2.0 | gross maldistribution (blocked line) | architecture 5.3 step 6; verify-mfg 9 |
| 710 | **Post-braze fly-cut** (diamond, MQL, 8,000 rpm, 50 N thrust) + pedestal | remove 1.20 to base 0.85 (0.80-0.90); HBM pedestal on T3 SKUs; in-line ultrasonic thickness at 9 points (10 MHz, ± 0.01); interferometer flatness | 2.0 | **CC-8 base thickness 0.85 ± 0.05; CC-9 flatness ≤ 0.020 / 0.050, form concave 0-10 µm; Ra ≤ 0.8** | core 1; mech 7.3 |
| 715 | Ni plate face (Tier 2 only; masked to the die face) | 3-5 µm electrolytic Ni after an acid activate | 1.0 (T2) | thickness by XRF | architecture 2.3 |
| 720 | Guard / stub fit | press GUARD into the inlet boss seat (0.02-0.05 interference), STUB x 2 press + O-ring (or TIG) per cap lane; -T tap tubes leak-checked | 1.0 | guard orientation (inside-out), seat | architecture 4.1 |
| 730 | **ISO 16232 flush** | pulsed 25 LPM DI + 0.1 % surfactant, forward 2 min / reverse 2 min; final DI; membrane 5 µm; gravimetry + particle count per plate, chip-entrapment CT on 1 in 500 | 5.0 (4 parallel: 1.25) | **CC-12 cleanliness: no particle > 50 µm, ≤ 5 of 25-50 µm** | architecture 5.3 step 7 |
| 740 | **Proof + pressurised flatness scan** | 1.55 MPa water, 2 min; confocal map of the die face at 0 and 1.55 MPa (1 µm, 0.5 mm grid over 108 x 108); lot over-proof 2.5-3.1 MPa on 1 in 200 with before/after zero-pressure map | 3.0 | **CC-13 proof; per-strip bulge ≥ 2.2 µm reject (E1-gated at 0.8 base), patch ≥ 13 mm** | architecture 5.2-5.3 |
| 750 | **3-point dP** (same wet rig) | 9, 18, 27 LPM PG25-equivalent (water with viscosity correction) at 45 C; port-to-port with fixed stubs | 2.0 | **CC-14 dP at 18 LPM 7.6 kPa ± 10 %, CpK ≥ 1.33; 9/27 ratio check (orifice area)** | architecture 4.2 |
| 760 | Vacuum bake | 80 C, ≤ 1 mbar, until outlet dew point ≤ -40 C (≈ 45 min, batch 40) | 1.1 | dew point 100 % | architecture 5.3 step 8 |
| 770 | Hardware kit + final | 8 screw sets into LF-15P (frame kitted, not mounted), serial laser mark at (-45, -45) on the cap, TIM-face cover | 1.5 | kit completeness (scale check) | mech 3, 10 |
| 780 | N2 fill, cap ports, pack | port caps with O-rings, N2 purge, ESD/vapour bag with indicator, tray | 0.5 | - | architecture 5.3 |

Total machine time ≈ 50 min per plate at volume (≈ 230 min at Build A). Takt at 100k/yr on 2 shifts: 1.5 plates/min; critical resources skive (5 min: 2-3 machines), furnace (1.4-1.6), fly-cut (2 min: 1-2), flush (4 stations), proof/dP (2 rigs).

**Sequence note.** The He leak (630) is placed directly after braze and before every wet step, as architecture 5.3 requires (water masks leaks); the IR screen (640) precedes the fly-cut because the cut removes the coating. The task list's order (flush → He → proof → dP → IR) is therefore re-ordered to 630 He → 640 IR → 710 fly-cut → 730 flush → 740 proof/scan → 750 dP (deviation D-F4; no change in content).

## 3. Braze fixture concept (FIX-15)

**Principle.** A differential-expansion clamp: the copper stack (22.3 mm pre-fly-cut) grows more on heating than the TZM tie rods that hold the graphite platens together, and eight TZM leaf springs convert that interference (0.137 mm at 795 C, `mfg_cost.out` §1) plus a cold shim preload into a load that is insensitive to shim error. Dead weight is rejected: 0.08 MPa is 1.25 kN = 128 kg per plate (7.7 t per 60-plate load).

| Element | Specification | Basis |
|---|---|---|
| Base platen | ISO-63 class isostatic graphite 180 x 180 x 15, top face ground flat 0.01; central 108 x 108 raised pad 0.02 high under the fin field, outer step 1.30 lower under the ears/land (so the rim top and the die-face region bear, the ears float); two alumina locating pins D1/D2 engage from below; 0.2 mm Grafoil sheet between graphite and the core back face (A'); BN stop-off painted on every graphite face that sees copper | verify-mfg 8 ("stepped pads"); core 1 (A' datum) |
| Top pad | graphite 180 x 180 x 25, underside machined to the cap outer profile with 0.10 clearance at 20 C (arch crowns r 7, pockets, cross-domes) so that at 795 C (Cu +0.9 mm over 125, graphite +0.4) the pad touches the arch crowns and the lid lands together; load enters the stack over ≥ 60 % of the footprint | section 3 stress table |
| Tie rods | 4 x TZM Ø8 at the platen corners, M8 TZM nuts, working length 55 mm; alumina washers insulate the rods from the graphite (no carburisation at the thread) | `mfg_cost.py` |
| Springs | 8 x TZM leaf 80 x 20 x 2.5 (two per rod, simply supported on graphite saddles, centre-loaded by the nut washer): k 684 N/mm each, 5.47 kN/mm total; hot deflection 0.229 mm = 1,250 N; cold preload shim 0.09 mm (502 N cold); spring stress 150 MPa (TZM yield at 800 C ≈ 450); shim error ± 0.05 mm gives 0.062-0.098 MPa | `mfg_cost.out` §1 |
| Pressure budget at 0.08 MPa | plenum wall axial 0.77 MPa, bend corners ~5.6 MPa (plenum lane 7 MPa at 0.10); fin metal 0.16 MPa (≤ 0.6 creep limit); separator span 0.59 MPa; arch hoop 0.48 MPa; all ≤ OFE hot 0.2 % proof ≈ 10 MPa | plenum 3.5; grate 12; verify-mfg 8 |
| Stop-off placement | BN (water-based, no binder residue above 400 C) brushed on: graphite faces; the 0.30 mm mask bands outside the capillary-break grooves are **not** painted (the groove is the control); the skirt foot outer edge below z 1.5 and the lap face chamfer (fillet stays on the inside); boss OD above the port-pocket flange; alumina pins (plain, unpainted, do not wet). No stop-off within 2 mm of any orifice, window or kerf (particle source) | grate 7; architecture 5.3 |
| Thermocouple witnesses | 3 fixtures per load carry type-K TCs in a dummy core: load uniformity ± 5 K at 795 C | AMS 2750 class 2 practice |
| Capacity | fixture 180 x 180 x 95 tall, 9.5 kg; 60 per load (3 x 4 per shelf, 5 shelves) in a 900 x 600 x 600 hot zone; 30-80 per load across furnace sizes; fixture life ≥ 300 cycles (graphite re-dressed at 100) | architecture 5.1 (30-80) |
| Route C2 (belt furnace) | same graphite platens and springs, no tie-rod thread exposure to H2 (TZM nuts hydrogen-safe); belt load 0.08 MPa identical | architecture 5.4 |

The top pad bears on the cap; the cap load path is lid lands → separator → plenum top flats and walls → bottom flats → grate → fin tips. The architecture's 0.2 MPa (3.1 kN) is reduced to 0.08 MPa because the folded plenum limits the stack to ≤ 0.10 MPa (plenum lane 3.5) and because the parts that need flattening (1.30 land plate at 20 µm bow, 0.40 web) need < 10 kPa (verify-mfg 8: 7 kPa flattens a 100 µm bow in 1.5 mm); the fin-tip closure relies on the ± 10-20 µm tip plane plus the 12-15 µm foil, not on pressure (deviation D-F1).

## 4. Inspection plan: critical characteristics, gauges, sampling

| CC | Characteristic | Limit | Gauge (resolution) | Sample | Owner op | Reaction |
|---|---|---|---|---|---|---|
| CC-1 | Fin thickness / pitch | 0.150 ± 0.020 / 0.300 ± 0.005 | telecentric vision on fins 1, 90, 180, 270, 360 (1 µm); X-bar/R | 100 % plates, 5 fins | 120 | CpK ≥ 1.33; blade change on trend |
| CC-2 | Fin-tip plane + rim coplanarity | flatness ≤ 0.020 (≤ 0.010 route B); coplanar 0.02 | laser-line scanner 0.5 mm grid (1 µm) | 100 % | 135 | re-plane once; scrap |
| CC-3 | Kerf position, width, depth | ± 0.05 / 0.30 +0.05/-0 / floor stub 0.05-0.10 | optical CMM top view (2 µm); depth by white-light section on 3 kerfs | 100 % position; depth 1 in 10 | 130 | arbor spacer / height re-set |
| CC-4 | Kerf burr, chips | burr ≤ 15 µm; no particle > 50 µm | optical profilometer 3 x 5 sites; flush gravimetry | 1 per lot sectioned (per 500); gravimetry per plate at 730 | 145 | re-polish lot |
| CC-5 | GRT-L pocket depth / floor / flatness | 0.80 ± 0.03 / 0.50 ± 0.04 / 0.020 | touch probe 7 x 3 points (1 µm); flatness interferometer | 100 % | 215, 230 | re-skim |
| CC-6 | GRT-W hole area and position | area ± 1 % of artwork, position ± 0.020 | backlit vision every hole (0.5 µm/px), checksum | 100 % (756 holes) | 245 | scrap web (US$3) |
| CC-7 | Plenum height / pitch | 5.80 ± 0.03 / 7.7143 ± 0.05 | gauge block + dial (2 µm); vision on 16 walls | 100 % | 320, 330 | re-set fold tool |
| CC-8 | Base thickness after fly-cut | 0.85 ± 0.05 (fallback 1.0) | in-line 10 MHz ultrasonic 9 points (10 µm) | 100 % | 710 | adaptive cut depth; scrap < 0.80 |
| CC-9 | Die-face flatness / form / Ra | ≤ 0.020 field, 0.050 body; concave 0-10 µm; Ra ≤ 0.8 | Fizeau interferometer (0.1 µm); profilometer | 100 % flatness; Ra 1 in 20 | 710 | re-cut once |
| CC-10 | Registration of the stack | ± 0.03 on D1/D2 | CT of 1 in 200 plates; alumina pin fit | lot | 520 | fixture pin wear |
| CC-11 | **He leak, dry** | ≤ 1e-6 mbar·L/s; CpK ≥ 1.33 on log10(rate) vs -6 | He mass-spectrometer, accumulation chamber (1e-9) | 100 % | 630 | scrap; seam section |
| CC-12 | Cleanliness | ISO 16232: no particle > 50 µm, ≤ 5 of 25-50 µm | 5 µm membrane, automated particle count + gravimetry | 100 % | 730 | re-flush once; CT on chip sites per 500 |
| CC-13 | Proof + pressurised flatness | 1.55 MPa, 2 min; bulge map: no strip ≥ 2.2 µm, no patch ≥ 13 mm; over-proof 2.5-3.1 MPa set ≤ 2 µm | confocal 1 µm, 0.5 mm grid | 100 %; over-proof 1 in 200 | 740 | scrap; CT |
| CC-14 | **dP at 18 LPM** (and 9, 27) | 7.6 kPa ± 10 %; ratio 27/9 = 7.4 ± 0.4; CpK ≥ 1.33 | Coriolis flow (0.2 %), differential transducer (0.1 % FS 25 kPa), 45 C bath | 100 % | 750 | sort: artwork or bypass |
| CC-15 | IR flow screen | no cold line (5-10 mm feature) | 640 x 512 LWIR, 30 mK | 100 % | 640 | CT, scrap |
| CC-16 | Dew point / N2 pack | ≤ -40 C outlet | chilled-mirror | 100 % | 760 | re-bake |
| Lot | Braze quality | tie bond ≥ 0.70 per land strip over any 10 mm; no filler within 0.15 of a window edge; no filler in grooves/orifices | CT 20 µm voxel of 1 in 200; sections on 1 in 1000 and every E1 coupon; peel coupon per load | lot | 610 | hold lot |
| Lot | Burst sample | ≥ 4.5 MPa | hydraulic burst 1 in 2000 | lot | 740 | hold lot |

CpK on CC-11: the distribution of log10(leak) on good plates is centred near -9 (chamber floor); CpK ≥ 1.33 requires sigma ≤ 0.75 decades against the -6 limit, achieved by a 1e-9 floor and a 300 s accumulation. CpK on CC-14: 7.6 ± 0.76 kPa limits; sigma ≤ 0.19 kPa (2.5 %), of which artwork area ± 1 % gives ± 0.03 kPa, bath temperature ± 0.5 K gives ± 0.05 kPa, flow ± 0.2 % gives ± 0.03 kPa: the budget leaves 0.17 kPa for braze bypass and burr variation.

## 5. GD&T summary per part (ISO 1101; general ISO 2768-fK)

| Part | Datum A | Datum B | Datum C | Flatness | Profile | Position | Other |
|---|---|---|---|---|---|---|---|
| CORE | die face (final); A' back face pre-braze | -x body edge | -y body edge | A 0.020 over 108 sq, 0.050 over 125; tip plane 0.020 to A' | pocket walls 0.05 to A'BC; lap face 121.40 profile 0.05 ⊥ A 0.03 | kerfs Ø0.05 to B; pin holes Ø0.03 to BC; ear holes Ø0.10 | tip/rim coplanar 0.02; land z 1.50 ± 0.05 parallel 0.03 |
| GRT-L | underside (land face) | D1 hole Ø3.00 H7 | D2 slot | 0.020 field / 0.030 both faces; parallel 0.03 | recess walls/floor profile 0.05; windows profile 0.05 | windows and recesses ± 0.03 to BC (Ø0.06) | thickness 1.30 ± 0.02; grooves ± 0.03 |
| GRT-W | underside | D1 | D2 | 0.05 free | hole profile 0.02 (w/h ± 0.010) | holes Ø0.04 to BC; fiducials ± 0.02 | thickness 0.40 ± 0.010; marking |
| PLN-C | bottom-flat plane | -x wall outer face (wall 0) | frame seat face y -57.0 | bottom flats coplanar 0.05; top flats 0.05 | wall profile 0.10 to A; windows/slots profile 0.05 | wall pitch ± 0.05 to B; bleeds ± 0.02 | H 5.80 ± 0.03; wall ⊥ ≤ 0.5° |
| PLN-F | bottom face | slot 1 | inner face | 0.02 both faces; parallel 0.02 | - | slots ± 0.03 (16) | 2.50 ± 0.02 x 5.78 -0.02/-0.05 x 120.70 ± 0.10 |
| SEP | underside | pin hole | pin slot | 0.03; parallel 0.03 | windows profile 0.10 | windows ± 0.05 (Ø0.10) to BC | 1.80 ± 0.03; burr ≤ 0.02 up |
| CAP | lid underside (seats on SEP) | skirt inner face -x | skirt inner face -y | lid lands flat 0.05, coplanar 0.08 (IR-M2); land z 13.10 ± 0.10 | outer surface profile 0.3 (draw); skirt inner profile 0.10 to A; arches internal 12 x 8 ± 0.15 | port pockets Ø0.10 to BC; tap notches ± 0.1 | skirt foot ⊥ A 0.10; wall 1.0 ± 0.08 after draw |
| BOSS-IN/OUT | bottom pilot face | bore 20.0 H9 | - | 0.02 | - | bore ∥ A Ø0.05 over 10; guard seat concentric Ø0.05 | OD 26 h9; z0-z1 20.1-30.0 ± 0.1 |
| LF-15P | lug plane | window -x edge | window -y edge | lands coplanar 0.05 | hook tabs profile 0.2 | lug holes Ø0.10 | per `DDD-mech` 4.2 |
| Assembly (brazed) | die face | -x body edge | -y body edge | A 0.020 / 0.050 | cap top profile 0.3 to ABC; height at the bar 21.1 ± 0.2 | bosses Ø0.2 to ABC; ear holes Ø0.10 | skirt seam fillet continuous; mass 1,250 ± 40 g |

## 6. Cost roll-up (US$ per plate, P50; `mfg_cost.out` §3)

Verifier convention honoured: lines are direct cost of good parts; factory cost = sum / yield x 1.12 overhead (verifier C1: 134.4 / 0.935 x 1.12 = 161 ≈ 162). Yield 93.5 % at 100k/yr, 80 % at the 10k/yr ramp (architecture 75-92 %).

| Line | 100k/yr | 10k/yr | 10k basis |
|---|---:|---:|---|
| Copper: CORE blank 0.76 kg; grate 0.28; plenum 0.22; SEP/CAP/BOSS 0.26 (1.52 kg at US$14.6/kg) | 22.1 | 25.5 | +15 % small-lot strip |
| Skive incl. blank mill, pocket, plane | 20.5 | 53.3 | 1 skiver at 35 % utilisation |
| Kerf: wax, gang-saw, de-wax, deburr | 2.8 | 7.0 | manual batches |
| GRT-L mill/punch/groove/skim | 3.3 | 9.9 | CNC slotting, laser windows |
| GRT-W laser + EP + vision | 3.0 | 4.8 | laser at both volumes |
| PLN-C pierce + fold + PLN-F + tack | 4.4 | 14.1 | laser blank, soft fold tool |
| SEP stamp/laser + flatten | 1.5 | 3.8 | laser |
| CAP draw + trim; 2 BOSS; boss braze rings | 6.3 | 18.9 | hydroform, soft tools |
| Filler: 5.7 g BAg-8 preforms (4.1 g Ag at US$65/oz = 8.6) + cutting | 14.7 | 20.6 | laser-cut preforms |
| Vacuum braze (fixture amortised, 1.4-1.6 furnaces) | 17.6 | 38.7 | 0.15 furnace, under-used |
| Dies and tooling amortisation | 2.0 | 8.0 | fold/draw tools over 20k parts |
| Fly-cut + pedestal + in-line gauge | 5.6 | 10.1 | - |
| TAP x 2, GUARD, STUB x 2, adapters (Ni plate T2 excluded) | 8.3 | 13.3 | - |
| Hardware: 8 screw sets, LF-15P (+2.5), pins, pack | 14.0 | 21.0 | - |
| Test: clean/flush, He, proof + scan, dP, IR, bake | 11.8 | 28.3 | manual cells |
| **Direct sum** | **137.9** | **277.1** | |
| **Factory cost P50 (/yield x 1.12)** | **165.2** | **388** | |
| P10 / P90 | 156 / 175 | 361 / 427 | verifier spread ± 6 % at 100k; -7/+10 % at 10k |

Cross-check: verifier C1 lines 134.4 + Rev A additions 2.5 (stampings +1.0, header +1.0, test +0.5) = 136.9 → 164.0; this lane 165.2 (+0.2 against the architecture's 165, +1.2 against the verifier basis because the grate's two laminations add ~US$1, DDD-grate 9.4). The 10k/yr value 388 sits inside the architecture's 370-430. Route C2 (Cu-Sn belt, E1-gated): filler 14.7 → 4.3, braze 17.6 → 8.5 → direct 118.3 → **US$142** (architecture 144). Capex at the CM per 100k/yr line: 1.6 vacuum furnaces US$2.4-3.2 M, 2-3 skivers 1.2-2.1 M, fold tool + progressive die 0.35 M, draw dies 0.25 M, fly-cut cell 0.4 M, test cell (He, confocal, dP, IR, flush, bake) 1.0-1.6 M: US$5.6-8.0 M, inside the architecture's 3.7-9 M.

## 7. Supplier and process classes

| Class | Scope | Qualification requirement | Candidates (type) | Dual source |
|---|---|---|---|---|
| A1 skiving house | CORE ops 110-150 | CTX-class machine, 0.15/0.30 x 2.0 Cu demonstrated on the E1 trial (Cpk ≥ 1.33 on CC-1), in-house wax/saw/plane or accepts our cell | Wieland / Kingka / Winshare / Nakamura class | 2 houses, M12 and M18 |
| B1 precision stamping and machining | GRT-L, PLN-F, SEP, BOSS, LF-15P, BP-15P | ± 0.02 on 1.3-1.8 Cu strip; 7-spindle slotting or photo-etch; IATF-style QMS | Asian/Mexican precision-stamping tier 2 | 2 |
| B2 laser job shop | GRT-W (per-SKU artwork), Build A blanks | single-mode fibre, ± 0.01-0.02, backlit vision 100 % | regional | 2 |
| C1 fin-folding / HX forming | PLN-C | sequential corrugating machine, 0.8 soft Cu, pitch ± 0.05; fold-tool build 8-14 weeks | transformer-fin and folded-fin HX makers | 2 (one holds the wire-EDM fallback) |
| C2 deep drawing | CAP | 3-station transfer draw, inter-draw anneal, 1.0 OFE; hydroform for Build A | automotive/HX draw shops | 2 |
| D1 filler | PF-1..PF-4, boss rings; Ag plating (B); Sn (C2) | AWS A5.8 BAg-8 foil 12-50 µm, photo-etched; Ag indexed to LBMA, 6-12 month hedge | Lucas-Milhaupt / Prince & Izant / Wesgo class | 2 |
| D2 filtration | GUARD, FLT-33 | 50 / 33 µm absolute square weave, ISO 16889 certified | Pall / Bopp / Haver class | 2 |
| D3 fasteners and springs | CSS-15P, SPR-60/110, SLV, WSH, e-clips | 17-4PH H900, 302 preset springs ± 10 % rate | PEM / Southco / Lee Spring class | 2 |
| E1 ceramics and graphite | PIN-AL2, FIX-15 platens, TZM rods and springs | ISO-63 isostatic graphite, TZM per ASTM B386 | Toyo Tanso / SGL / Plansee class | 2 |
| F braze house / CM | ops 520-640, 710-780 (the assembly site) | vacuum furnace ≤ 1e-5 mbar, AMS 2750 class 2 uniformity, Cu braze experience, IATF-style QMS, non-Group-A, outside Taiwan (architecture D5); belt-furnace capable for C2 at one of the two | Vietnam / Mexico CM | 2 (M12, M18) |
| G test equipment | He leak, confocal scanner, dP rig, IR station, flush, bake | our specification, our ownership (US$1-1.6 M per line) | Pfeiffer/Inficon, Keyence/Zygo, FLIR class | - |

## 8. First-article qualification sequence (FAI, AS9102-style, gated to the architecture's E1/E2/G1)

| Step | What | Quantity | Acceptance | When |
|---|---|---|---|---|
| F1 | Material receipt: mill certs (O ≤ 5 ppm, IACS, grain), strip thickness map, ASTM B577 on route-C lots | every lot | per section 1 | M1 |
| F2 | Core process trial: skive 6 blanks (3 H02, 3 H01), pot + saw + plane 4, section 2 (root cracks, burr), tip map | 6 | CC-1..4 met; Cpk estimate ≥ 1.33 on 5 fins x 6 plates | M1-2 (E1 factor) |
| F3 | Grate and plenum coupons: 3 GRT-L/GRT-W coupon pairs 30 x 30; 3-bend fold coupon (K-factor, r_i 0.6, springback) | 3 + 3 | recess/lip ± 0.03; K 0.31-0.39 fixed | M1-2 |
| F4 | Braze coupons (E1): 60 x 60 stacks core/grate/plenum/sep with routes A, B, C; fixture pressure 0.04 / 0.08 / 0.12 MPa; tip plane ± 10 / ± 20 µm; potted vs unpotted saw; ramp vs EDM kerf ends | 24 coupons | tie bond ≥ 0.70 per strip (CT + sections); no filler within 0.15 of a window; grooves empty on the inboard side; per-strip bulge detection demonstrated (0.8 base gate) | M2-3 (E1) |
| F5 | FIX-15 commissioning: 3 fixtures, load cells at 20 C and witness TCs at 795 C; spring set measured | 3 | 1,250 ± 250 N hot; uniformity ± 5 K | M2 |
| F6 | Build A, 12 full plates (laser/CNC/hydroform/wire-EDM parts, route A): full routing with 100 % CC data | 12 | CC-8..16 on all; 2 plates to CT + sections, 1 burst ≥ 4.5 MPa, 1 over-proof 3.1 MPa, 8 to E2 water table and E3 thermal | M3-4 |
| F7 | Dimensional FAI report: ballooned drawings per section 5, CMM on 3 plates of each part, GD&T per datum scheme | 3 per part | all characteristics in tolerance; deviations dispositioned | M4 |
| F8 | E2 hydraulic: dP 7.6 ± 10 % at 18 LPM, segment max/min ≤ 1.15 (dye/IR), Cd(Re) both directions on orifice coupons | 8 plates | pass per architecture 4.3 | M4 |
| F9 | G1 freeze: artwork, recess H/lip, base 0.8 vs 1.0, route A vs C2; release production tooling (fold tool, draw dies, slotting head, perforating die after artwork freeze) | - | gate record | M3-5 |
| F10 | Build B pilot, 300-500 plates on production-intent tooling at the CM: capability study (30-plate CpK on CC-1, 8, 9, 11, 14), PPAP-style package (control plan = section 4, PFMEA, MSA on every CC gauge with GR&R ≤ 10 %) | 300-500 | CpK ≥ 1.33 on CC-11 and CC-14; yield ≥ 75 % | M12-18 |
| F11 | Second-source FAI (skive, braze) repeating F2, F4, F6 at the second houses | 12 | match first-source within gauge R&R | M18 |
| F12 | Reliability/compat samples drawn from Build B (pressure cycling, thermal cycling, 1,000 h erosion at 2x flow, coolant compatibility) | per architecture 10.1 | - | M12-24 |

## 9. Deviations from the architecture of record

| ID | Architecture | This lane | Reason | Consequence |
|---|---|---|---|---|
| D-F1 | vacuum braze at ≤ 0.2 MPa | 0.08 MPa (0.06-0.10) on the stack through a differential-expansion fixture with TZM leaf springs | the folded plenum limits the stack to ≤ 0.10 MPa (plenum lane 3.5); flattening needs < 10 kPa; the ≤ 0.2 MPa was a draft limit, not a requirement | tip closure relies on the ± 10-20 µm tip plane and 12-15 µm foil (verify-mfg 7, 9); fixture is lighter (9.5 kg) and cheaper; E1 factor 0.04/0.08/0.12 MPa decides |
| D-F2 | one outline per layer implied | the stack outline conflict stands: GRT-L/GRT-W/SEP 122.6 (grate lane), PLN-F flange 120.7, core lap face 121.4 (skirt inner 121.4 → cap outer 123.4), CAD 121.0; pins Ø2.0 at ± 57.5 (core) vs Ø3.0 at ± 57 (grate) | not this lane's call (mech IR-M4) | the routing carries the grate-lane 122.6 and the core-lane pins; if the skirt inner is 121.4 the grate/separator outline must drop to 121.0 (-1.6 g, no process change). Must close at G1 |
| D-F3 | mass 1.24 kg (plate + stubs + springs + backplate) | 1.337 kg on that boundary (+97 g, 8 %); FRU 1.422 kg | CAD cap 260 g + bosses 38 g against the architecture's 250 g for cap and bosses; mech's hardware 80 g; 1.8 separator | over the 1.4 kg SKU limit only with the frame (1.422); the 316L separator option (-106 g) or a 0.9 mm cap sheet (-26 g) recovers it; cap lane to decide |
| D-F4 | test order 5.3: He → proof → over-proof → dP → IR → fly-cut/flush → bake | 630 He → 640 IR → 710 fly-cut → 730 flush → 740 proof/scan → 750 dP → 760 bake | IR must precede the fly-cut (coating), He must precede any wet step; proof and dP share one wet rig after the flush so that chips are out before the scan | none on content; the task-list order (flush before He) is not followed |
| D-F5 | grate line US$6.8 | grate lines 3.3 + 3.0 + strip 4.1 = 10.4 | two-lamination grate (DDD-grate D2) | +US$1.2 inside the Rev A allowance; P50 165.2 vs 165 |
| D-F6 | furnaces 1.6 per 100k/yr | 1.4 at 60 per load (1.6 at 52) | 5.5 h cycle with gas quench | capex 2.4-3.2 M either way |
| D-F7 | bosses "brazed" (route unstated) | bosses brazed in the single vacuum cycle with 0.5 mm BAg-8 rings in the cap port pockets; STUBs pressed with O-rings after the fly-cut (TIG option) | keeps one furnace cycle and 1 + 2 external seams | cap-lane confirmation of the pocket/pilot fit |

## 10. Open items and the tests that close them

| ID | Item | Closes at |
|---|---|---|
| O-F1 | Fixture pressure 0.04 / 0.08 / 0.12 MPa vs tie bond fraction and plenum corner set (E1 F4) | M3 |
| O-F2 | Perforated 25 µm vs 12-15 µm PF-1 foil: tip gap fill vs filler run-out into kerfs (sections) | M3 |
| O-F3 | Cap draw: 3-station feasibility of the arches + cross-domes + skirt in 1.0 OFE (draw ratio, inter-draw anneal count); hydroform for Build A; the cap lane's drawing | M2 (cap lane) |
| O-F4 | Outline and pin reconciliation (D-F2) | G1 |
| O-F5 | He-leak CpK method: log-rate distribution on Build B; chamber floor 1e-9 confirmed | M12-18 |
| O-F6 | dP CpK: bypass contribution (web/land, J1) measured by dye on Build A; limits ± 10 % confirmed or tightened to ± 8 % | M4 |
| O-F7 | Flush recipe: 4 min forward/reverse at 25 LPM clears 10,080 kerf sites; chip CT on 3 Build A plates | M4 |
| O-F8 | Belt-furnace (C2) fixture variant: TZM in N2/H2 at 795 C, graphite life | E1 route C |
| O-F9 | Perforating-die transition for GRT-W: Cd re-qualification, d/t 1.0 edge slots | M6-9 after artwork freeze |
| O-F10 | Second-source list and the CBP ruling on the build site (architecture D5) | M6 |

## 11. Files

| File | Content |
|---|---|
| `design/DDD-mfg.md` | this document |
| `design/bom.csv` | 25-line BOM: pn, description, qty, material, mass, process class, supplier class, source lane |
| `design/mfg_cost.py` → `mfg_cost.out` | fixture spring sizing, furnace capacity, cost roll-up 10k/100k, BOM export |
| `design/params-mfg.json` | fixture, furnace, cost and yield parameters |
| `appendix/verify/ctl/cost_mass_height.out` | verifier cost basis (C1 162 / C2 141) |
