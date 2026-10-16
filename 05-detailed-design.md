# PRISM-15 Rev A: detailed design definition (synthesis)

This document is the entry point to the design-definition layer that sits between the architecture of record (`03-architecture.md`) and the CAD (`cad/`). It records which lanes are complete, which parameter values the CAD baseline uses where lanes disagree, every deviation from the architecture, and the open items with the test that closes each. The dimensioned definition itself lives in the lane documents listed in section 1; the single source of truth for geometry is `design/params.json`. The design report (`report/PRISM-15-RevA-design-report.md`, PDF alongside) presents the same content for a reader who was not in the room.

Status on 16 October 2026: design definition complete for every layer (core, grate, plenum and separator, cap, mounting, manufacturing, predicted datasheet, innovation register); the CAD assembly of fourteen parts is regenerated from the lane values and checked for interference. No hardware exists.

## 1. Lane map

| Lane | Document | Scripts and data | Status | What it fixed |
|---|---|---|---|---|
| Core | `design/DDD-core.md` | `core_geom.py` → `core_geom.out`, `params-core.json` | complete | blank, fin field 0.15/0.15/2.0 at 0.30 pitch, 15 kerfs, pocket, rim 121.4, land z 1.5, ears, tap bosses, 2.0 mm pins, die-face flatness and form rule, base 0.85 (0.80–0.90, 1.0 fallback) |
| Grate | `design/DDD-grate.md` | `grate_cell.py`, `grate_artwork.py`, `grate_outlet_row.py`, `grate_cq_check.py`; `artwork_prism15_ttv.csv/.dxf`, `artwork_prism_g_example.csv/.dxf`, `params-grate.json` | complete | two laminations (1.30 land plate + 0.40 web), windows 1.2 / 0.6 edge, recess 2.7 × 0.8, lip 0.75, 378 graded inlet orifices in five steps, 378 outlet-row holes, capillary-break grooves, meter 2.31 kPa, ±2.2 % per-orifice uniformity, segment 1.092 |
| Plenum and separator | `design/DDD-plenum.md` | `plenum_sep.py` → `plenum_sep.out`, `plenum_sep_data.json`, `plenum_cq_check.py` | complete | folded 0.80 mm corrugation, 15 channels 6.914 × 5.00, bends r 0.6/1.4, developed blank 180.95 × 116.0, ceiling windows, bottom-flat slots, 14 bleed holes, end frames 2.5 × 5.78 × 120.7, separator 1.80 with 14 + 32 windows, 0.46 kPa |
| Mounting and integration | `design/DDD-mech.md` | `mech_calc.py` → `mech_calc.out`, `mech_calc_data.json`, `params-mech.json` | complete | load frame LF-15P/LF-15T, 8 × dia-4 captive screws with SPR-60/110 and DIE-TTV kits, retention budget, bow and die-face form rule, TTV family and thermocouple layout, HBM pedestal, PRISM-G envelope, mass budget, shock and vibration envelope |
| Manufacturing | `design/DDD-mfg.md` | `mfg_cost.py` → `mfg_cost.out`, `params-mfg.json`, `bom.csv` | complete | 25-line BOM, routing ops 110–760, braze fixture FIX-15 at 0.08 MPa, 16 critical characteristics, GD&T per part, cost 165.2 / 388, supplier classes A1–G, FAI F1–F12 |
| Predicted datasheet | `design/DDD-perf.md` | `perf_datasheet.py` → `perf_datasheet.out`, `params-perf.json` | complete | benchmark re-run on the 0.85 mm base (31.1 / 38.8 K paste, 29.2 / 34.9 K pad), OCP flow sweep, three-boundary dP table, inlet and coolant cases, margins, measurement order |
| Cap, bosses, guard, seam | `design/DDD-cap.md` | `cap_stress.py` → `cap_stress.out`, `cap_stress_data.json`, `params-cap.json` | complete | arches 10 × 7.7 internal at 14 pitch (external 12 × 8.7), crown r 3.5/4.5, inlet ends ±51 / outlet ±57; cross domes 35 × 35 at y −20 and 35 × 38 at y +21 with a spine to arch 4; bosses OD 26 / bore 20 at (0, −20) and (0, +21), z 19.8–29.5, pilot in a d26.1 pocket; skirt 121.5 / 123.4 lapped 1.3 mm on the rim with one BAg-8 ring; GUARD-C cup d30 × 5 under the inlet dome (GUARD-A alternative); height 20.8 at the bar; cap 279 g; draw sequence arches first |
| Innovation register | `design/DDD-innovation.md` | `params-innovation.json` | complete | ten element cards with mechanism, quantified benefit, closest prior art, novelty confidence under the FTO caveat and proving test; non-claims; stretch items |

## 2. Controlled stack and the values the CAD baseline uses

| z (mm) | Layer | Controlled value | Source | CAD value | Status |
|---|---|---|---|---|---|
| 0 | die face, datum A | flatness 0.020 over the field, concave 0–10 µm, Ra 0.8 | core, mech 7.3 | – | agreed |
| 0–0.85 | base | 0.85 ± 0.05, min 0.80, fallback 1.0 | core | 0.85 | gated on E1 |
| 0.85–2.80 | fins | 360 × 0.15 / 0.15 / 1.95 effective; tips at 2.80 | core | as controlled | agreed |
| – | kerfs | 15 at x = −54 + 7.7143 k, 0.30 wide | core, grate | as controlled | agreed |
| 2.80–4.10 | land plate | 1.30; windows 1.20 / 0.60; recess 2.70 × 0.80; lip 0.75 | grate | as controlled | agreed; H and lip to E2 |
| 4.10–4.50 | meter web | 0.40; artwork ART-TTV-15-A | grate | 756 holes from the CSV | agreed |
| 4.50–10.30 | plenum | 0.80 sheet, 15 channels 6.914 × 5.00, walls at line ± 3.857 | plenum | as controlled | agreed |
| 10.30–12.10 | separator | 1.80; inlet windows y −21 / −7; outlet windows y +7 / +21 / +35 / +49 | plenum (thickness), mech IR-M3 (positions) | as controlled | agreed; 316L 0.6 option open |
| 12.10–13.10 | cap lid | 1.0 drawn; lands flat at |y| 56.5–59.7 (IR-M2), z 13.10 ± 0.10 | cap, mech | as controlled | agreed |
| 12.10–20.80 | arches and domes | 2 inlet at y −21 / −7 (x ±51), 4 outlet at +7 / +21 / +35 / +49 (x ±57); 10 × 7.7 internal, crown r 3.5 / 4.5; domes 35 × 35 and 35 × 38 + spine | cap | as controlled | agreed; dome walls to E1 FEA (O-C1) |
| 19.80–29.5 | bosses | 20 bore, 26 OD, pilot d25.95 × 1.0 in d26.1 pockets at (0, −20) and (0, +21); stub seat d23 H8 | cap | as controlled | agreed |
| 14.1–19.1 | guard | GUARD-C cup d30 × 5.0, 50 µm absolute 316L, 17.4 cm², under the inlet dome; GUARD-A 25 cm² stub housing as the alternative | cap | shell model | **open, O-C3** |
| – | outline | body 125; rim lap face 121.4; skirt 121.5 / 123.4; grate, web and separator 121.0 ± 0.08 | core, cap IR-C2 | 121.0 | closed (grate drawing to update) |
| – | datum pins | 2.0 H7 at (±57.5, ±57.5) | core | 2.0 at ±57.5 | **open, G1** (grate wrote 3.0 at ±57) |
| – | ear holes | 3.4 (core) / 4.5 +0.10/−0 (mech IR-M1) | – | 3.4 | **open, G1**; recommendation 4.5 |
| – | height | 20.8 at the arch crowns, 29.5 at the bosses | cap | 20.8 / 29.5 | agreed |
| – | mass | 1,240 budget, 1,400 limit; 1,307 on the architecture boundary with the cap lane's 279 g cap (about 1,262 with the CAD cap mass of 234 g); up to 1,392 with the frame | mech, cap, CAD | plate solids 1,151 | **open, G1** (316L separator −106 g) |

## 3. Reconciliation decisions taken for the baseline

1. **Outline 121.0 mm** for the land plate, web and separator (core lane recommendation), so the stack fits inside the 121.4 mm skirt with 0.2 mm radial clearance; −1.6 g against the grate lane's 122.6; no process change. The grate lane's drawings are to be updated at G1.
2. **Pins 2.0 mm H7 alumina at (±57.5, ±57.5)**, one round, one slotted at 45°, per the core lane; the grate lane's 3.0 mm at ±57 is withdrawn because 3.0 mm pins at ±57 fall on the 121.0 outline's corner radius.
3. **Separator 1.8 mm copper** for Rev A (plenum lane; separator span stress 22.8 MPa at design burst). The 0.6 mm 316L option (−106 g) is held for the mass decision at G1 together with a 0.9 mm cap sheet (−26 g).
4. **Outlet windows at y +7 / +21 / +35 / +49** (mechanical lane request IR-M3) so the last outlet arch ends at y ≤ 55.5 and both cap lands are equal; `params.json` and the CAD already carry these; `plenum_sep.py` is to be re-run (expected change in per-orifice max/min below 0.005).
5. **Fixture pressure 0.08 MPa** (manufacturing lane D-F1) replaces the architecture's ≤ 0.2 MPa; the E1 matrix tests 0.04 / 0.08 / 0.12.
6. **Test order** per the manufacturing lane (He leak dry → IR screen → fly-cut → flush → proof and scan → dP → bake).
7. **Ear holes 4.5 mm** recommended (mechanical lane IR-M1); the CAD still shows 3.4 and is changed by one parameter at G1.
8. **Cap per the cap lane:** 10 × 7.7 arches, 35 mm domes with the outlet spine, bosses at y −20 / +21, skirt 121.5 / 123.4, d26.1 pockets, guard cup under the inlet dome. The provisional 12 × 8 arches could not be drawn at the 14 mm pitch (zero valley land).
9. **Separator windows 5 × 8** (cap IR-C1); plenum top-flat windows stay 5 × 10; `plenum_sep.py` to be re-run (expected change below 0.005 in per-orifice max/min).
10. **Guard variant open** (O-C3): GUARD-C in the plate for the test vehicles and Build A; GUARD-A on the stub if the first customer's interface control document prefers a serviceable element.

## 4. Deviations from the architecture of record (consolidated)

| ID | Lane | Architecture | Design | Consequence |
|---|---|---|---|---|
| D-C1 | core | base 0.80 | 0.85 nominal (0.80–0.90), 1.0 fallback | +0.14 K average; ultrasonic gauge tolerance |
| D-G2 | grate | one grate plate | two laminations, land 1.30 + web 0.40 | +US$1.2; recess can face the web; orifices off the braze plane |
| D-G5 | grate | segment max/min 1.061 | 1.092 lumped-row at 18 LPM | weakest segment +0.41 K inside the 1.5 K allowance |
| D-P1 | plenum | separator 1.5 | 1.80 | +0.3 mm height (21.1), +35 g |
| D-M1 | mech | mass 1.24 kg | 1.278 kg on the same boundary | +38 g; within the 1.4 kg limit |
| D-M2 | mech | no load frame on packages | LF-15P mandatory | +85 g, +US$2–3 |
| D-M3 | mech | PRISM-G ≤ 0.9 kg | 1.03–1.15 kg | limit to be restated (~1.05 with 316L separator) |
| D-M4 | mech | bow measured | closed-form 22.6 µm concave vs 18.7 convex thermal | E1 FEA and heated scan remain |
| D-M5 | mech | HBM step ±0.05 | 0–0.40 signed ±0.05 | +0.7 K per 0.25 mm raised root |
| D-F1 | mfg | braze at ≤ 0.2 MPa | 0.08 MPa differential-expansion fixture | tip closure relies on the tip-plane tolerance and the foil |
| D-F3 | mfg | 1.24 kg | 1.337 kg | cap and separator options recover it |
| D-F4 | mfg | test order 5.3 | He → IR → fly-cut → flush → proof → dP → bake | none on content |
| D-F5 | mfg | grate US$6.8 | 10.4 | inside the Rev A allowance; P50 165.2 |
| D-F7 | mfg | bosses "brazed" | BAg-8 rings in cap pockets in the one cycle; stubs pressed after the fly-cut | one furnace cycle kept |
| D-C1 | cap | arches 12 × 8 semicircular, 80.5 mm² | 10 × 7.7 r 3.5, 71.7 mm² | inlet header 1.05 m/s, +0.11 kPa; plate dP about 7.8 kPa with D-C3 |
| D-C2 | cap | – | skirt wall 44.5 MPa at working pressure if the stack-edge cavity is wetted | secondary boundary behind two internal joints; E1 FEA |
| D-C3 | cap | guard ≥ 25 cm², 0.30 kPa booked | GUARD-C 17.4 cm², 0.40 kPa clean | fouling life 0.70×; GUARD-A restores 25 cm² outside the braze boundary |
| D-C4 | cap | cap + bosses 250 g | cap 279 g (CAD solid 233.6 g, O-C7) | plate 1,262–1,307 g on the architecture boundary |
| D-C5 | cap | bosses at (0, −14) / (0, +28) | (0, −20) / (0, +21) | a d26 boss needs a 28 mm flat dome top |
| D-P1 (perf) | perf | 31.0 / 38.7 K paste | 31.1 / 38.8 K | datasheet uses the as-designed value |
| D-P2 (perf) | perf | segment 1.061 | 1.092 | nil on the published maximum |

## 5. Open items and the test that closes each

| ID | Item | Nominal (range) | Closes at |
|---|---|---|---|
| O-G1 | recess depth and lip width: fin-top ≤ 0.5 m/s, jet footprint on the lip | 0.80 (0.70–0.90); 0.75 (0.70–0.80) | E2 CFD and PIV, M2 |
| O-G2 | orifice Cd vs Re, direction, laser vs die edge | 0.72 (0.65–0.80) | E2 coupons, M2 |
| O-G4 | edge window width | 0.60 (0.60–0.90) | G1 |
| O-G5 | lamination registration | ±0.03 (±0.02) | E1 CT, M3 |
| O-G6 | capillary-break effectiveness; orifice area change through braze ≤ 1 % | – | E1 sections and vision, M3 |
| O-G7 | web-to-land bypass ≤ 0.2 % | – | E2 dye on Build A, M4 |
| O-G8 | lip erosion at 2.2–2.5 m/s, 1,000 h | – | E4, M10 |
| O-G9 | perforating-die transition | – | M6–9 after artwork freeze |
| O-F1 | fixture pressure vs tie-bond fraction and plenum corner set | 0.08 (0.04–0.12) | E1, M3 |
| O-F2 | 25 µm perforated vs 12–15 µm foil at the tips | – | E1, M3 |
| O-F3, O-C4 | cap draw trial on soft tools: arch-end thinning ≥ 0.70, valley r 0.5 restrike, land flatness 0.05, skirt inner 121.50 ± 0.03 | – | Build A, M3–4 |
| O-C1 | outlet dome walls and top ligaments with the boss ring | 28–48 MPa bound at 3.1 MPa | E1 FEA, M2 |
| O-C2 | skirt wall with a wetted cavity; lap-seam fillet continuity by section | – | E1 FEA, E0 |
| O-C3 | GUARD-C vs GUARD-A; fouling dose on the chosen element | 17.4 vs 25 cm² | first customer ICD, E4 |
| O-C6 | arch ends vs the outermost separator windows: 1.3 % (inlet, x ±46.3) and 4.0 % (edge outlet, x ±53.7) of window area under the arch end wall; lengthen the arches about 1 mm within the mechanical limits or trim the windows | – | cap and plenum lanes, G1 |
| O-C7 | cap mass basis: lane 279 g (developed area, lid counted twice under the arches and domes) vs CAD 233.6 g; BOM to the CAD figure once the lane confirms | – | G1 |
| O-F4 | pin reconciliation (section 3); the outline is closed at 121.0 by cap IR-C2 | 2.0 | G1 |
| O-F5 | He-leak Cpk method on Build B | – | M12–18 |
| O-F6 | dP Cpk: bypass contribution; limits ±10 % or ±8 % | – | M4 |
| O-F7 | flush recipe; chip CT | – | M4 |
| O-F10 | second sources; CBP ruling | – | M6 |
| O-M1 | DIE-TTV spring rate; 2,011 ± 40 N | 34 N/mm ± 10 % | E3 rig build |
| O-M2 | clamp and thermal bow FEA; heated pressurised flatness scan; bearing choice | – | E1 M2, E3 M4 |
| O-M3 | shock and vibration levels from ORv3, OCP white paper, GR-63 | – | M5 |
| O-M4 | 2.8 mm ears as a frame-less option for liquid-metal SKUs | – | G1 cost review |
| O-M7 | thermocouple layout vs a purchased CoolIT vehicle and OCP §5.2 | – | E0, M1 |
| O-M8 | PRISM-G port box and 1U stack | – | PRISM-G start |
| O-P1 | PG25 property table from the vendor | ±10 % on viscosity | M1 |

## 6. Experiments mapped to open items

| Experiment | Closes | Pass criterion |
|---|---|---|
| E0 purchased incumbent plates, rig repeatability | O-M7, perf CoolIT-like columns | ≤ 1 K on the 8-TC maximum |
| E1 tie-braze matrix, fixture commissioning, Build A CT, FEA | O-F1, O-F2, O-G5, O-G6, O-M2 (FEA), O-C1, O-C2, base 0.85 gate | every land strip ≥ 70 % bonded; per-strip bulge detected at 0.85; burst ≥ 4.5 MPa |
| E2 water table and single-cell CFD, orifice coupons | O-G1, O-G2, O-G7, O-F6 | segment max/min ≤ 1.15 at 18 LPM; fin-top ≤ 0.5 m/s |
| E3 test-vehicle commissioning | O-M1, O-M2 (scan) | heat capture ≥ 98 %; re-mount ≤ 1 K |
| E4 dose fouling and erosion | O-G8 | fin-field dP ≤ +10 %; no measurable erosion |
| G1 gate record | O-F4, O-G4, O-M4, mass option (316L separator), ear hole, guard variant if the ICD is in hand | – |

## 7. Files

| Path | Content |
|---|---|
| `design/params.json` | the CAD parameter file (section 2 values) |
| `design/DDD-*.md` and their scripts | lane definitions, calculations, outputs |
| `design/artwork_*.csv/.dxf` | orifice artworks |
| `design/bom.csv` | bill of materials |
| `cad/` | parametric CAD, outputs, drawings, renders, `cad/README.md` |
| `report/PRISM-15-RevA-design-report.md`, `.pdf` | the design report |
| `03-architecture.md` | architecture of record |
