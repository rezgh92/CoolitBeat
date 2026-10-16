# DDD-cap: drawn skirted cap, port bosses, guard and the one external seam, PRISM-15 Rev A

Detailed design definition, lane `cap`, 2026-10-16. Parent: `docs/cooling/03-architecture.md` (2.2 stack, 4.1 headers and guard, 5.1 parts and seams, 5.2 pressure, 5.6 height). Binding siblings: `DDD-core.md` / `params-core.json` (rim lap face 121.40, land 1.8 at z 1.5, tap bosses), `DDD-grate.md` / `params-grate.json`, `DDD-plenum.md` / `plenum_sep_data.json` (separator z 10.30-12.10, windows 5 x 10 at y -21/-7 and +7/+21/+35/+49, flanges x +-60.36, frames y 57-59.5), `DDD-mech.md` / `params-mech.json` (IR-M2, IR-M3, IR-M4, IR-M6), `DDD-mfg.md` / `bom.csv` (one vacuum braze, 0.08 MPa, BAg-8). Provisional geometry corrected: `cad/params.json` keys `cap`, `bosses`, `guard`. Script `cap_stress.py` -> `cap_stress.out`, `cap_stress_data.json`; parameters `params-cap.json`. Convention X along the fins, Y along the lines, Z up from the die face (datum A), origin at the fin-field centre. Dimensions mm; closed-form stresses +-25 % until E1 FEA.

## 0. Result in brief

| Item | Provisional (cad/params v0) | This lane | Why |
|---|---|---|---|
| Arch internal section | 12 x 8 box, pitch 14 | **10.0 x 7.7, crown r_i 3.5**, pitch 14 (external 12 x 8.7) | at 14 mm pitch a 1.0 sheet can only form a valley if the external land is >= 2 mm: internal width <= 10 (section 2); 7.7 recovers 20.8 at the bar (section 8) |
| Arch ends | 118 long (|x| 59) | inlet **|x| <= 51.0**, outlet **|x| <= 57.0** external | mech IR-M2 (52 / 58.8); windows covered with >= 1.05 margin |
| Cross domes | 30 x 26 at (0,-14); 30 x 54 at (0,+28) | **inlet 35 x 35 internal at (0,-20); outlet 35 x 38 at (0,+21) + spine 10 wide to arch 4** | a d26 boss needs a 28 mm flat top; a 35 x 52 flat top cannot carry 1.55 MPa in 1.0 Cu |
| Port bosses | (0,-14), (0,+28), z 20.1-30.0 | **(0,-20), (0,+21), z 19.8-29.5**, OD 26 / bore 20, pocket d26.1 x 1.0 | follows the domes; inside the mech keep-in |
| Skirt | outline 125, inner 123 | **inner 121.50 +-0.03, outer 123.4 +-0.15**, foot z 1.5, lap 1.3 on the rim 121.40 | braze gap 0.05 nominal (mech IR-M4) |
| Grate / separator outline | 121.0 (CAD) vs 122.6 (grate lane) | **121.0 +-0.08** (IR-C2) | 0.25 clearance inside the skirt (>= 0.18 min) |
| Separator windows | 5 x 10 | **5 x 8 (IR-C1)**; plenum top-flat windows stay 5 x 10 | 1.0 window margin under a 10 mm arch |
| Guard | d18 x 8 shell in the boss | **GUARD-C cup d30 x 5 under the inlet dome**, pre-braze, 17.4 cm2, 0.40 kPa | 25 cm2 does not fit a d20 bore or a 7.7 mm dome (D-C3); GUARD-A alternative in a stub housing |
| Height at the bar | 21.1 | **20.8** (bosses to 29.5) | architecture and the <= 21 mm G1 requirement met |
| Mass | 259.5 (CAD) | **279 g** cap + 38 g bosses + 6 g guard | D-C4 (+29 g on the 250 allocation) |

## 1. Requirements honoured

| ID | Requirement | Design value | Source |
|---|---|---|---|
| C1 | 1.0 mm OFE drawn cap, lid flat on z 12.10, skirt drawn to the core land (one external perimeter seam) | sheet 1.00 +-0.03 O60; lid 12.10-13.10; foot on the land at z 1.5 | architecture 2.2, 5.1; core land |
| C2 | Inlet 2 arches, outlet 4 arches at 2x area, mid-fed | 2 x 71.7 = 143 mm2 and 4 x 71.7 = 287 mm2 per half (ratio 2.0) | architecture 4.1; D-C1 |
| C3 | Arch ends inlet |x| <= 52, outlet |x| <= 58.8; lands |y| 56.5-59.7 at z 13.10; no feature at |y| >= 56 | 51.0 / 57.0; lands 3.2 wide, flat 0.05, coplanar 0.08; outlet system ends at y 55 external | mech IR-M2, IR-M3 |
| C4 | Wall >= 2 mm between arches | external land 2.0, fluid-side flat 1.0 + fillable radii = 2.1 effective braze land | task; plenum J6 |
| C5 | Proof 1.55 MPa with SF >= 2 on 40 MPa yield (= <= 40 MPa at 3.1) | all closed-form cases <= 38 MPa except two bounded cases flagged to E1 (section 4) | architecture 5.2 |
| C6 | Braze gap 0.03-0.08 at the lap, BAg-8 ring, one cycle | 0.05 nominal; 0.01-0.09 worst case; 0.5 wire ring 0.98 g | mfg 3 |
| C7 | Port bosses 20 bore at the port centres, UQD08 / barb interface, 316L stubs pressed after fly-cut | section 5 | mfg 420/720; architecture 4.1 |
| C8 | Guard 50 um square weave 316L, inside-out radial diffuser, >= 25 cm2, <= 0.3 kPa clean | 17.4 cm2 / 0.40 kPa in the plate (D-C3); 25 cm2 / 0.2 kPa in GUARD-A | architecture 4.1, 7.2 |
| C9 | Height 20.8 at the bar | 20.8 (arch internal 7.7) | architecture 5.6; traceability <= 21 |
| C10 | Everything inside the skirt with 0.2 clearance | 121.0 outline, 0.25 nominal | mech IR-M4 |

## 2. Why the arches are 10 x 7.7 and the domes 35 wide

The six separator windows sit at a 14 mm pitch (y -21, -7, +7, +21, +35, +49) and each arch is a drawn channel whose two walls must come back to the lid and be brazed to the separator in the valley between neighbours (the arch foot pull, p x width, has no other path). A valley drawn from 1.0 sheet is two walls plus two outer radii of >= 0.5 t plus a flat: external land >= 2 x 1.0 + 2 x 0.5 = 3.0 for a 1.0 fluid-side flat, i.e. **internal width <= 14 - 3 - 1 = 10.0**. The provisional 12 x 8 had zero external land (walls touching) and cannot be formed. With 10.0 internal, the window under it must be <= 8 long to keep the 1.0 margin the plenum lane assumed (sep +-0.05, cap arch position +-0.15, window +-0.05 = 0.25 stack): IR-C1 shortens the **separator** windows to 5 x 8 (velocity 0.54 m/s, series dP 0.29-0.44 kPa against the plenum lane's 0.46 limit); the plenum top-flat windows stay 5 x 10 and the 1 mm step is on the downstream side of a 0.43 m/s flow.

Section: internal 10.0 wide, 7.7 high from the separator top, crown corners r_i 3.5 (external 4.5), top flat 3.0, straight wall 4.2. Area 71.7 mm2 (architecture semicircular 12 x 8: 80.5). Inlet header per half 143 mm2 -> 1.05 m/s at 18 LPM (1.31 at 22.5, below the 1.5 cap); outlet 287 mm2 -> 0.52 m/s. Header dP +0.11 kPa at K 1 on the inlet velocity head (D-C1).

Cross domes. A d26 boss needs a flat >= 28 under it; a dome with r_e 4.5 top corners therefore needs >= 37 external = 35 internal in both directions. In y the inlet arches occupy -26..-2 internal: the inlet dome spans **-37.5..-2.5 internal** (centre -20, 11.5 mm of still water beyond arch 1 at -y, over solid separator); its +y wall at -1.5 external leaves the 2.0 wall to the outlet system (external +1). The outlet dome spans **+2..+40 internal** (arches 1-3; centre +21, top flat 28 x 31); arch 4 (44..54) joins through a **spine** 10 wide internal at |x| <= 5 crossing the 41..43 valley, carrying 4.5 LPM at 1.0 m/s. Where an arch enters a dome the inter-arch valley is interrupted over the dome width (35) and over the spine (12): the arch walls act as beams there (section 4). Both domes: plan corners r_i 6 / r_e 7; top flat 28 (x). Domes and arches are one cavity system per header; nothing is above z 20.8 except the two bosses.

## 3. Geometry of record

| Feature | Value | Tol | Basis |
|---|---|---|---|
| Sheet | C10100 OFE 1.00, O60, grain <= 0.035 | +-0.03 | mfg 46; draw-quality |
| Lid | z 12.10 (underside on the separator) to 13.10 | 13.10 +-0.10 | plenum stack |
| Lid lands (load frame) | |y| 56.5-59.7, x -60..+60, z 13.10, flat 0.05, coplanar 0.08; no feature at |y| >= 56.0; marking flat at (-45,-45) | +-0.10 | mech IR-M2, IR-M6 |
| Skirt inner | 121.50 square, corners r_i 1.0 (restruck), inner face |x|,|y| 60.75 | +-0.03 (punch-sized) | lap gap 0.05 on the rim 121.40 +-0.05 |
| Skirt outer | 123.4 (wall 0.95-1.0 at the foot after restrike) | +-0.15 | mech IR-M4; mfg D-F2; land exposed 0.8 outboard |
| Skirt foot | z 1.50 on the core land (1.8 wide); squareness to A 0.10 | +-0.05 | core land_z |
| Lap | inner face on the rim outer wall z 1.5-2.8 (1.3 tall); rim chamfer 0.3 at z 2.8 is the inner filler reservoir | - | core rim |
| Tap notches | 2, on -y at x 0 and 15.429, 8.4 wide, z 1.4-2.9; edges brazed to the boss | +-0.1 | core tap bosses 8 wide to z 2.8 |
| Arches (6) | internal 10.0 (y) x 7.7, r_i 3.5; external 12.0 x 8.7; crown z 20.80 | 10.0 +-0.15; 7.7 +-0.15; position +-0.15; crown +-0.15 | section 2 |
| Arch y centres | -21, -7 (inlet); 7, 21, 35, 49 (outlet) | +-0.15 | separator windows; mech IR-M3 |
| Arch ends | vertical, plan r_i 5 / r_e 6; inlet internal |x| 50.0 / external 51.0; outlet 56.0 / 57.0 | +-0.2 | windows end at 48.79 / 54.95 |
| Valleys (5) | external land 2.0, outer radius 0.5, fluid flat 1.0; J6 braze land 2.1 effective | - | section 2 |
| Inlet/outlet wall | y -1..+1 external (2.0) | - | mech +y land = -y land |
| Inlet dome | internal 35 (x) x 35 (y -37.5..-2.5), plan r_i 6; same section as the arches; top flat 28 x 28 | +-0.2 | section 2 |
| Outlet dome | internal 35 x 38 (y 2..40); top flat 28 x 31 | +-0.2 | section 2 |
| Spine | internal 10 (x) x 7.7, y 40..54, at x 0 | +-0.15 | joins arch 4 |
| Port pockets | d26.10 +0.05/0 x 1.0 deep in the dome tops, floor z 19.8, through hole d20.0; centres (0,-20.0) and (0,+21.0) | position d0.10 to B/C | boss pilot |
| Grate / web / separator outline | 121.0 square r 2.0 | +-0.08 | IR-C2: 0.25 to the skirt |
| Clearances inside the skirt | separator 0.25, plenum flange 0.40, frames 1.25, grate 0.25 | min 0.18 | stack tolerances |

## 4. Pressure design (cap_stress.out section 2; 3.1 MPa, allowable 40 = SF 2 at proof)

| Case | Model | MPa at 3.1 | SF at proof | Verdict |
|---|---|---:|---:|---|
| Arch top flat 3.0 | clamped strip pL2/2t2 | 14.0 | 5.7 | ok |
| Arch / dome side wall 4.2 straight | clamped strip | 27.3 | 2.9 | ok |
| Arch crown corner r_i 3.5 | hoop pr/t | 10.8 | 7.4 | ok |
| Arch end half-dome r 5 at 0.70 wall (30 % draw thinning) | hoop | 22.1 | 3.6 | ok |
| Dome plan corner r_i 6 | hoop | 18.6 | 4.3 | ok |
| Dome top ligament 2.5 carrying the boss ring (20 N/mm) | clamped strip, line load | 37.8 | 2.1 | ok, E1 FEA |
| Dome top shear at the boss ring | F / (pi d t) | 20.1 | 4.0 | ok |
| Inlet dome walls, membrane, foot only (100 mm) / with arch walls as T-stiffeners (140) | F / (per x t) | 38.0 / 27.1 | 2.1 / 3.0 | ok |
| Outlet dome walls, foot only (86 mm) / with arch walls (146) | same | 47.9 / 28.2 | 1.7 / 2.8 | **bounded; O-C1** |
| Arch walls as beams across the 12 mm spine crossing (35 N/mm uplift) | fixed beam, I = t h3/12 | 37.6 | 2.1 | ok |
| Arch walls as beams across the 35 mm dome crossing | - | n/a: inside the dome the cavity is the dome; the dome walls carry | - | section 2 |
| Skirt wall 9.3 free span, cavity wetted, MAWP | clamped strip | 44.5 (at 1.03) | 1.8 | **D-C2** |
| Lap seam shear | lid strip outboard of the plenum flange tie x p / lap area | 0.94 | > 100 | ok |
| Boss face joint | pressure on the bore + 200 N side load / 217 mm2 | 5.4 | > 25 | ok |

Tie ribs are not needed: no flat panel spans more than 3.0 mm except the dome tops, which are carried by the brazed boss ring (a 3 x 9.7 Cu ring is rigid against the 1.0 sheet). The two flagged cases are bounds, not failures: the outlet dome's uplift is shared between its own foot and the six arch walls that run into it (the arch walls are brazed in the valleys within 2 mm of the openings); the skirt sees pressure only if the lid/separator perimeter band (J6, 1.7-4 mm wide, continuous) and the plenum flange joint J3 both fail, and then it is a ductile secondary wall at 1.1x yield, leak-before-break, not a tie. E1 adds the two domes and the skirt to the FEA list (O-C1, O-C2). Fixture load 0.08 MPa (mfg): arch crown bearing 0.48 MPa, dome top 0.08 MPa on the boss face: no hot-creep issue (OFE hot 0.2 % proof about 10 MPa).

## 5. Seams, bosses and stubs

**Perimeter lap (the one external seam).** Skirt inner 121.50 +-0.03 against the rim 121.40 +-0.05: radial gap 0.050 nominal, 0.01-0.09 worst case (the AWS range for BAg-8 is 0.025-0.125; vacuum brazing of clean Cu fills 0-0.10). Lap 1.3 tall x 485 perimeter = 627 mm2. **Ring:** BAg-8 (72Ag-28Cu) 0.5 mm wire, one closed ring of 499 mm laid in the outer corner between the skirt foot and the land, detouring the two tap notches; 98 mm3 = 0.98 g against 92 mm3 needed (gap 32, inner chamfer fillet 22, outer fillet 0.4 leg 38). The filler climbs the lap by capillarity (0.05 gap: 90 kPa head for a 1.3 mm rise), fills the 0.3 rim chamfer inside and leaves a 0.4 outer fillet on the land. Stop-off (BN) on the body vertical edge below z 1.5 and on the ear roots; none on the land. Inspection: continuous outer fillet visually at station 620; He leak 100 % (station 7xx); the fillet must not reach the ears (0.8 land exposed). Load: 0.94 MPa shear at 3.1 MPa; SF > 100 on BAg-8 shear (150-200).

**Port bosses (BOSS-IN, BOSS-OUT).** OFE bar d28: OD 26.0 h9, bore 20.0 H9, height 9.7 (z 19.8-29.5), pilot d25.95 x 1.0 into the cap pocket d26.10 (radial gap 0.05-0.10), 0.5 x 45 deg chamfer at the pilot top as the ring seat. **Ring:** BAg-8 0.6 wire, d26.5 closed ring (24 mm3) in the chamfer corner; the filler runs down the pilot wall and across the 217 mm2 face to the d20 through-hole edge, where it stops at the hole edge (no groove needed; the bore edge of the pocket is sharp). Bosses are located by the pocket (concentric d0.05) and held down by the fixture top pad. Upper 8.0 of the bore is a **stub seat** counterbore d23.0 H8 with a face O-ring groove 1.3 x 0.75 at d20.3-21.6 in its floor.

**Stubs (STUB, 316L, 2).** 20.0 ID x 23.0 OD (+0.03/+0.06) x 30 long; pressed into the seat after the fly-cut (station 720) against an EPDM-70 face O-ring (ID 20 x 1.0, 25 % squeeze), then the 0.5 mm boss lip is rolled into a 0.3 deep groove on the stub (retention independent of the Cu press fit, which yields and creeps). Top 12 mm per the ICD: UQD08 male adapter (brazed to the stub before pressing) or 3/4 in barb. Pressure load on a stub 974 N at 3.1 MPa; rolled lip shear area 36 mm2 -> 27 MPa on 316L. Mech keep-in met: bosses at (0,-20) and (0,+21) inside |x| <= 50, -40 <= y <= 50; flange d26; 41 mm apart (UQD08 body d30 fits). Height to the stub top z 59.5 (stub) or per the adapter.

## 6. Guard

Architecture: 50 um absolute square weave 316L, inside-out radial diffuser in the inlet boss, >= 25 cm2, 0.1-0.2 kPa clean (0.30 booked). A d20 bore cannot hold 25 cm2 (a plain d18 x 8 sleeve is 4.5 cm2 and leaves no exit annulus), so the element goes **under the inlet dome** as a cup:

| Item | Value |
|---|---|
| Mesh | 316L square weave 270 x 270, wire 0.041, opening 0.053 (50 um absolute), 36 % open, ISO 16889 certified |
| Shape | inverted cup d30 x 5.0 tall, corrugated bottom 2.5 deep (7 corrugations along x), 0.5 mm 316L rim ring and collar; mesh resistance-welded to the frame |
| Position | centred (0,-20) under the inlet boss; top at z 19.1, bottom at 14.1 on four 2.0 feet; 2.5 mm to the dome walls |
| Retention | collar d19.6 x 3.0 rises through the cap's d20 pocket hole; three 0.3 mm hook tabs snap above the cap top wall inside the boss bore; the boss is placed over it; installed at station 520 before the cap goes on (316L survives the 795 C cycle; no filler within 10 mm) |
| Area | 17.4 cm2 (sides 4.7 + corrugated bottom 12.7) |
| Hydraulics | face 0.17 m/s, through-pore 0.48 m/s, mesh 0.17 kPa; exit under the cup 0.95 m/s, 0.23 kPa after diffusion -> **0.40 kPa clean** (0.30 booked); 3x-clean alarm at 1.2 kPa |
| Fouling life | scales with area: 0.70x the architecture's figures (behind the 33 um cartridge still years; without it 45 d at 1e-4/mL) |

Deviation D-C3. **GUARD-A** (recommended for the ICD discussion, O-C3): a pleated 50 um element 25 cm2 in a d34 x 40 316L housing on the inlet stub above the boss, serviceable with the tray drained, 0.15-0.2 kPa, +12 mm at the port only, the plate itself unchanged (the dome then stays empty).

## 7. Draw feasibility (cap_stress.out section 4)

| Step | Operation | Formability figure | Note |
|---|---|---|---|
| Blank | 188 x 233 x 1.0 O60, 393 g | - | feed margins: 20 per side in x, 8 per side plus 69 draw-in in y |
| Station 1 | arches, domes and spine formed in the flat blank, centre pair first (y -7 / +7), then outward pair by pair, blank free to feed from the +-y edges; arch ends fed from the +-x margin | developed arch section 25.5 per 14 pitch = 82 % if stretched in place (impossible); with free feed each arch is a channel draw at ratio 1.8; arch ends are half-cups d12 x 8.7 at equivalent ratio 1.97 (LDR 2.1 for annealed OFE); local thinning <= 30 % accepted (hoop 22 MPa at 3.1) | this is the reason the arches are drawn before the skirt (IR-C4 to mfg, which had the skirt first) |
| Anneal | 450 C / 30 min N2 | hardness <= 55 HV | mfg 415 |
| Station 2 | skirt box draw 125 sq x 11.6 deep, corners r_i 3.0, 2 % blank-holder draw-in | equivalent cylindrical ratio 1.15; the corrugated field is stiff in x and bends in y only at the flats (|y| > 38.5 and the 2 mm valleys), so the lid shape holds | hydroform at Build A |
| Station 3 | restrike: skirt corners to r_i 1.0 (mech IR-M2), valleys to r 0.5, lid lands flat 0.05 / coplanar 0.08, pockets d26.1 x 1.0; trim to 123.4 and foot z 1.5; pierce 2 x d20 and the 2 tap notches | springback about 1 deg at r/t 3.5-4.5: dies over-bend 1.5 deg; land flatness set by the restrike pad | wall 0.92-1.0 at crowns and skirt foot; 0.70 min at arch ends |
| Inspection | CMM skirt inner 121.50 +-0.03 at 8 points, land z 13.10 +-0.10, arch position +-0.15, crown z 20.80 +-0.15, pocket d and position, wall by ultrasonic at 6 arch ends | - | GD&T per mfg table (CAP row), with these values |

## 8. Height check

Stack: separator top 12.10 + lid 1.0 + arch internal 7.7 + crown 1.0 = **20.80 at the bar**; bosses to 29.5; stubs to 59.5 or per adapter. The provisional 8.0 internal gave 21.1, over the <= 21 mm G1 requirement (architecture 13.4) because the plenum lane's 1.8 separator added 0.3. Recovering 20.8 costs 4 % header area (74.7 -> 71.7 mm2) and 0.02 m/s: accepted. Alternative (not taken): keep 8.0 (21.1) and re-baseline the requirement to <= 21.5.

## 9. Mass and cost

| Item | g | Basis |
|---|---:|---|
| Cap (lid 140, skirt 56, arches 51, domes 32) | 279 | sheet area x 1.0 x 8.94 |
| Bosses 2 x 19 | 38 | d26/d20 x 9.7 |
| Guard GUARD-C | 6 | mesh + 0.5 frame |
| Stubs 2 x 16 (316L) | 32 | mech / BOM |
| Cap-lane total | 355 | BOM had 259.5 + 38.4 + 10 + 31.5 = 339 |
| Plate on the architecture boundary | 1,307 | mech 1,278 + 29 (D-C4); limit 1,400; 316L separator option -106 |

Cost: unchanged against the mfg lane's US$6.3 (draw + bosses + rings) except the arches-first sequence, which uses the same three stations; the pre-braze guard removes the station-720 press of the guard and adds a 10 s placement at 520; the stub seat counterbore and roll adds ~US$0.3. Lane cost US$6.6, BAg-8 for the two seams 1.0 + 0.5 g (within the 5.7 g plate total).

## 10. Interface requests, deviations, open items

| ID | To | Request / statement |
|---|---|---|
| IR-C1 | plenum | separator windows **5.0 x 8.0** at the same centres; plenum top-flat windows unchanged; re-run `plenum_sep.py` (expected per-orifice max/min change < 0.005; window dP 0.29-0.44 kPa) |
| IR-C2 | grate, plenum, CAD | GRT-L, GRT-W, SEP outline **121.0 +-0.08**, not 122.6 (grate lane) nor "cap lane to confirm" |
| IR-C3 | mech | bosses at (0,-20) / (0,+21), top z 29.5, d26; lands |y| 56.5-59.7 confirmed; arches end 51.0 / 57.0; nothing at |y| >= 56; frame window and LF-15P unchanged |
| IR-C4 | mfg | station order arches -> anneal -> skirt -> restrike; guard placed at station 520 before the cap; stub seat d23 H8 with face O-ring and rolled lip; fixture top pad to this profile (crowns 20.8, domes 37 x 37 / 37 x 40, pockets) |
| IR-C5 | mfg / BOM | CAP 279 g, blank 188 x 233 (393 g buy); GUARD-C 6 g; STUB 20/23 x 30 |
| D-C1 | architecture 4.1 | arches 10 x 7.7 r 3.5 (71.7 mm2) instead of 12 x 8 semicircular (80.5): inlet header 1.05 m/s, +0.11 kPa; plate dP 7.6 -> about 7.8 kPa with D-C3 |
| D-C2 | architecture 5.2 | skirt wall 44.5 MPa at MAWP if the stack-edge cavity is wetted; secondary boundary behind two internal joints |
| D-C3 | architecture 4.1, 7.2 | guard 17.4 cm2 / 0.40 kPa in the plate; GUARD-A alternative restores 25 cm2 / 0.2 kPa outside the braze boundary |
| D-C4 | mech 12 | cap 279 g against 250: plate 1,307 g (target 1,240, limit 1,400) |
| D-C5 | architecture / CAD | bosses moved to y -20 / +21 |
| O-C1 | E1 FEA | outlet dome walls and top ligaments with the boss ring (bounds 28-48 MPa at 3.1); inlet dome 27-38 |
| O-C2 | E1 FEA, E0 | skirt wall with a wetted cavity; lap seam fillet continuity on the first 5 plates by section |
| O-C3 | ICD / E4 | GUARD-C vs GUARD-A decision with the first customer ICD; E4 fouling dose on the chosen element |
| O-C4 | Build A | draw trial on soft tools: arch-end thinning map (target >= 0.70), valley r 0.5 restrike, land flatness 0.05 |
| O-C5 | CAD | regenerate `cad/parts/cap.py` from `params-cap.json` (arches 10 x 7.7 r 3.5, domes, spine, pockets, skirt 121.5/123.4) and re-run the interference check |
