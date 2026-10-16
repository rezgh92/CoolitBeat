# DDD-plenum: folded plenum (layer 3) and separator (layer 4), PRISM-15 Rev A

Detailed design definition, lane `plenum`, 2026-10-15. Parent: `docs/cooling/03-architecture.md` (architecture of record: 2.2 stack, 3.2 clearances, 3.5 bleeds, 4.1-4.3 hydraulics, 5.1-5.3 construction and load paths). Verifier inputs honoured: `appendix/verify/verify-manufacturing.md` (#5 and required change 1: stamped laminations refuted, folded plenum adopted; #8 fixture load; #18 wall/rib crossings; #19 internal joints are bypass-only), `appendix/verify/verify-hydraulics.md` (section 3: header clash at ±14 mm, segment balance, bleed 1.1 mm for 4 %; required changes 1, 2, 10). Sibling lane honoured: `design/DDD-grate.md` and `design/params-grate.json` (line positions, leg keep-out, slot over the outlet row, 0.30 mm filler mask, window-feed sensitivity). Scripts in this folder: `plenum_sep.py` (geometry, flat pattern, multi-window plenum solver with the as-drawn TTV artwork, bleed, final_segbal network, separator plate model, joints, hot-fixture stress, 316L, mass, cost; `plenum_sep.out`, `plenum_sep_data.json`) and `plenum_cq_check.py` (CadQuery validity, mass, foot-on-land check; `plenum_cq_check.json`). Model terms are ±25 % until E1/E2; dimensions are drawing values.

**Conventions** (`cad/prism_cad.py`, DDD-grate). X along the fins (across the lines), Y along the lines, Z up from the die face, origin at the fin-field centre. Lines at x_k = -54 + 7.7143 k, k = 0..14; k odd = inlet (7), k even = outlet (8; k = 0, 14 edge outlets at ±54.000). Grate top (meter web GRT-W) at z = 4.50. Plenum z 4.50-10.30; separator z 10.30-12.10 (1.80, section 7); cap flat on z 12.10. PG25 at 45-50 C: 1005 kg/m3, 1.25 mPa s. Flow basis 18 LPM; rated 15 LPM; 150 % rated 22.5 LPM.

## 1. Function and requirements carried by the plenum and separator

| # | Requirement | Value | Source |
|---|---|---|---|
| P1 | 15 channels at the line pitch, 7 inlet and 8 outlet, inside 6.9 x 5.0 mm; inlet channels floored by the grate web (orifices exposed, no sheet over them) | pitch 7.7143; inside 6.914 x 5.00 | architecture 2.2, 3.2, 4.1 |
| P2 | Along-plenum uniformity with the graded artwork | per-orifice max/min ≤ 1.06 at 9-36 LPM (architecture 1.061 on the lumped model) | architecture 4.3; `ctl/plenum_graded_pkgA.out` |
| P3 | Channel velocity | ≤ 0.62 m/s half-flow mean; copper band ≤ 0.9 m/s (CDA, return > 60 C) | architecture 4.1, 7.3 |
| P4 | Separator window velocity and loss | ≤ 0.6 m/s; ≤ 0.46 kPa in series at 18 LPM | architecture 4.2; task |
| P5 | Dead-end bleed from every inlet dead end into the neighbouring outlet | 1.1 mm hole = 4 % of plenum flow (architecture); see D2 | architecture 3.5; verify-hydraulics |
| P6 | Walls land on grate lands only; no wall, foot or filler over any window or orifice | registration stack ≤ ±0.10 | task; DDD-grate section 4 keep-out |
| P7 | Tie load path: separator → walls → grate at design burst | wall ≤ 40 MPa membrane (29.9); joints carry p x pitch | architecture 5.2; `ctl/pkgA_dp_stress.out` |
| P8 | Separator spans the outlet channels under the cap lands at proof without yield, at design burst without rupture | proof 1.55, burst 3.1 MPa, allowable 40 MPa | architecture 5.2 |
| P9 | Every plenum and separator joint is internal: a missed joint bypasses, never leaks | 0 external seams added | architecture 5.1 |
| P10 | Filler masked 0.30 from every window/slot edge; none reaches an orifice | masks + capillary hierarchy | architecture 5.1; DDG-grate section 7 |
| P11 | One braze cycle, routes A / B / C; fixture load survivable at 790 C | ≤ 0.10 MPa on the stack (section 9) | architecture 5.1; verify-manufacturing #8 |
| P12 | Height, mass, cost | plenum 5.8 mm / 0.19 kg / US$4.4; separator 1.5 mm / 0.19 kg (architecture); result: 5.8 / 0.165 kg / US$4.6-5.8 and 1.8 / 0.208 kg / US$5-6 | architecture 5.1, 5.4; D1 |
| P13 | Fin-field dP taps (qualification and R+/P plates) | tap into one inlet and one outlet channel | architecture 7.3 |

## 2. Construction decisions

### 2.1 Fold type

| Option | Walls | Channel floors / ceilings | Verdict |
|---|---|---|---|
| **A. Single-wall square-wave corrugation (one 0.8 mm sheet, 16 walls, 7 top flats, 8 bottom flats, 2 outward top flanges)** | 0.80 single, at mid-pitch | inlet: floor = grate web, ceiling = top flat (window to the separator); outlet: floor = bottom flat (slot over the outlet row), ceiling = separator | **Chosen.** Gives exactly 6.914 x 5.00 for both channel types at H 5.80 = 5.0 + 0.8 (architecture 2.2); every wall is attached top and bottom through a face joint (bend into a flat), no edge joints; one part |
| B. Hairpin corrugation (double 1.6 mm walls, all channels open to the grate) | 2 x 0.8 back-to-back | floor = grate for all 15 channels | Rejected: channels 6.11 wide (-12 % section, +13 % velocity, artwork re-run); the hairpin stands on the grate on a line contact (two 1.4 mm radii) with no face joint; 2x sheet in the walls (+45 g) |
| C. Eight separate U-channels, wall tops brazed edge-on to the separator | 0.80 | inlet ceilings = separator | Rejected: 16 edge joints 0.8 wide carrying 23.9 N/mm at burst (29.9 MPa on a fillet-fed edge joint), 8 loose parts to register, no inlet-side top flat to spread the cap-land load (section 9) |
| D. Machined from a 5.8 mm plate (alternate-face gang slotting) | 0.80 | as A, sharp corners | Rejected for volume (0.8 mm walls deflect under slotting; ~US$8-15); **wire-EDM from solid is the Build-A fallback** if the fold tool slips (identical envelope, r 0.15 corners, ~3 h/plate) |

### 2.2 Section through the stack (x across the lines, z up; mm)

```
 z 12.10 ───────────────────────────────── SEPARATOR 1.80 (window 5.0 x 10.0 under each arch) ───────────────────────────
 z 10.30 ══╦═══════════ J2: top flat 5.714 bonded ═══════════╦══   (Ro 1.4 arcs)   ══════════ outlet channel ceiling = separator
          ║ ╭──────────── top flat (tflat k, inlet k odd) ────────────╮ ║
          ║ │   INLET CHANNEL 6.914 x 5.00, floor = grate web (orifices) │ ║   OUTLET CHANNEL 6.914 x 5.00 (z 5.30-10.30)
   wall   ║ │   wall 0.80 straight z 5.90-8.90, bleed Ø0.6/1.1 at z 7.40  │ ║
 z  5.30  ║ ╰──╮                                                  ╭──╯ ║ ╔═══════ bottom flat (bflat k, outlet k even) ═══════╗
 z  4.50 ═╩════╧══ (Ro 1.4 foot arcs; fluid-filled fillet void) ══╧════╩═╩═ J1: contact |x-x_out| 0.9..2.857, slot 1.80 over the row ═╩═
          GRATE WEB GRT-W 0.40  o   o   o  (orifices at x_in ± 1.0)      ║   outlet holes at x_out ± 0.5   ║
```

The wall centrelines sit at mid-pitch, x = x_k ± 3.857 (wall faces 3.457 and 4.257 from every line). The foot of every wall is a bend into a bottom flat lying on the grate land between the outlet row and the next inlet channel; the top of every wall is a bend into a top flat lying under the separator. Both are face joints (J1, J2). The fluid-filled fillet void outside each foot arc (0.55 mm2, on the inlet side) and outside each top arc (on the outlet side) are inside the channels and need no filler.

### 2.3 End frames and registration

The 15 channel ends are closed by two **comb end frames** (OFE bars 2.5 x 5.78 x 120.7 with 16 sawn slots 0.90 x 1.00 deep that receive 1.0 mm tabs on every wall end). The comb fixes the wall pitch at both ends (±0.03), makes the corrugation plus frames a self-fixturing sub-assembly (laser-tacked at the four flange corners) and gives face joints to the grate and the separator. Integral folded end tabs were rejected: a tab folded from a top flat is 5.7 wide between the bend radii and leaves 0.6 x 5 mm corner gaps (≈ 10 % of a line's orifice area) that cannot be closed by filler. Bleed holes are pierced in the wall flat pattern (section 3), not machined into the frames: same function, zero cost, ±0.02 position.

## 3. Folded corrugation PLN-C

### 3.1 Material and formed geometry

| Feature | Dimension (mm) | Tolerance | Basis / note |
|---|---|---|---|
| Material | OFE C10100 strip, soft (R220 / O60), grain ≤ 0.035 | EN 1652 / ASTM B152 | Aurubis Cu-OFE datasheet: soft temper 90° bend ratio 0 (both directions); braze cycle re-anneals |
| Thickness t | 0.80 | ±0.03 (EN 1652 ≤ 350 wide is ±0.04; order precision) | channel width follows 1:1 |
| Channel pitch | 7.7143 | ±0.05 per channel, ±0.10 cumulative over 16 walls (frames trim the ends) | lines ±0.03 (grate) |
| Inside channel width | 6.914 | ±0.06 (pitch + 2 x t/2) | architecture 6.9 |
| Height H (grate top to separator) | 5.80 | ±0.03 | 5.0 channel + 0.8 sheet; frames 5.78 -0.02/-0.05 |
| Inside bend radius r_i | 0.60 (0.75 t) | ±0.10 | datasheet allows 0; 0.6 keeps outer-fibre strain 40 % (< elongation 45-55 %) and tooling noses durable |
| Outside bend radius R_o | 1.40 | derived | sets contact widths below |
| Straight wall | 3.00 (z 5.90-8.90) | derived | bleed hole and tabs live here |
| Flat between tangents (top and bottom) | 5.714 | derived | = pitch + t - 2 R_o |
| Wall centrelines | x = -57.857 + 7.7143 j, j = 0..15 | ±0.10 to the grate datums | mid-pitch |
| Wall faces from every line | 3.457 / 4.257 | - | grate keep-out 3.06-4.66 (DDG-grate) contains it |
| Bottom-flat contact on the grate | |x - x_out| ≤ 2.857, both sides of the 1.80 slot | - | bonded strip 1.657 per side after the 0.30 mask |
| Top-flat contact under the separator | |x - x_in| ≤ 2.857 (5.714 wide) | - | minus the two 5.0 x 10.0 windows |
| Outer flanges (2) | 1.50 flat, outward at the top; free edge at x = ±60.357 | ±0.10 | laps under the separator; overall width 120.71 inside the 122.6 grate / 123.0 skirt |
| Channel length (flats, y) | ±57.00 (114.0) | ±0.10 | 3 mm dead end beyond the field (±54); grate recess ends at ±54.5, web solid beyond |
| Wall tabs | 32 x (0.8 x 1.00 long x 3.00 tall), y 57.0-58.0 | L ±0.05 | into the frame comb slots; root relief r 0.3 |
| Perpendicularity of walls | ≤ 0.5° (0.05 over the height) | - | springback compensated in tooling (soft Cu ~1-2°) |
| Flatness of flats | ≤ 0.03 over 114 | - | braze gap ≤ 0.05 with 25 µm foil |
| Twist / camber of the part | ≤ 0.10 over 114 / 120.7 | - | frames pull it true |
| Surface | Ra ≤ 0.8 as rolled; no lubricant residue (vapour degrease + ISO 16232 clean) | - | braze lands on both faces |
| Burr (pierced features) | ≤ 0.015, on the non-braze side where possible | - | windows: burr toward the channel; slots: burr toward the channel |
| Mass | 135 g (CadQuery with tabs), analytic 132 g | - | `plenum_cq_check.json`, `plenum_sep.out` §1 |

### 3.2 Pierced features (in the flat blank, before folding)

| Feature | Qty | Dimension (mm) | Position | Tolerance | Purpose |
|---|---|---|---|---|---|
| Top-flat windows | 14 (2 per inlet flat) | 5.00 x 10.00, r 1.0 | flat centre (x_in), y = -21.0 and -7.0 | size ±0.05, pos ±0.05 | feed from the separator inlet windows under cap arches I1, I2 (section 7) |
| Bottom-flat slots | 8 (1 per outlet flat) | 1.80 x 110.0, ends r 0.9 | flat centre (x_out), y = 0 | w ±0.05, pos ±0.05 | opens the outlet row (holes at x_out ± 0.5); ≥ 1.60 required by DDG-grate; 2.0 mm bridges at y ±55..57 keep the flat in one piece |
| Bleed holes | 14 | Ø0.60 (TTV artwork) / Ø1.10 (zoned artworks); range 0.6-1.1 | wall straight region, z 7.40; walls j = 2, 4, .. 14 at y = +55.5; walls j = 1, 3, .. 13 at y = -55.5 | Ø ±0.03, pos ±0.05 | each inlet dead end bleeds into its +x (north end) or -x (south end) outlet neighbour; D2, O3 |
| dP-tap hole (option, qualification and R+/P plates) | 1 | Ø2.00 | top flat k = 7 (x = 0), y = -53.0 | ±0.05 | under the separator tap at (0, -53); blank on production plates |
| Tab root reliefs | 64 | r 0.30 notches | wall ends at y ±57 | - | prevents tearing at the fold ends |
| ID / lot mark | 1 | laser, 2 mm text | +x flange, y -56 | - | traceability |

### 3.3 Flat pattern (K-factor 0.35, soft copper; verify on a 3-bend coupon, section 3.5)

Developed coordinate s runs from the -x flange free edge; y as assembled. Developed width **180.95** (= 2 x 1.50 flanges + 16 x 3.00 walls + 15 x 5.714 flats + 32 x 1.382 bend allowances); blank 180.95 x 116.0 with the wall tabs forming the 116 extent (flats and bends end at y ±57.0). Bend allowance per 90° fold BA = (π/2)(r_i + K t) = 1.382 (±0.05 with K 0.31-0.39). Full coordinates: `params-plenum.json` → `flat_pattern`.

| Element (s order) | s start | s end | Element | s start | s end |
|---|---|---|---|---|---|
| flange - | 0.000 | 1.500 | bflat0 (outlet k0, x -54.000) | 7.265 | 12.979 |
| bend, wall0 (x -57.857), bend | 1.500 / 2.882 / 5.882 | 2.882 / 5.882 / 7.265 | tflat1 (inlet k1, x -46.286) | 18.743 | 24.458 |
| wall1 | 14.361 | 17.361 | bflat2 (x -38.571) | 30.222 | 35.937 |
| wall2 | 25.840 | 28.840 | tflat3 (x -30.857) | 41.701 | 47.416 |
| wall3 | 37.319 | 40.319 | bflat4 (x -23.143) | 53.180 | 58.894 |
| wall4 | 48.798 | 51.798 | tflat5 (x -15.429) | 64.659 | 70.373 |
| wall5 | 60.277 | 63.277 | bflat6 (x -7.714) | 76.138 | 81.852 |
| wall6 | 71.756 | 74.756 | tflat7 (x 0.000) | 87.617 | 93.331 |
| wall7 | 83.235 | 86.235 | bflat8 (x +7.714) | 99.096 | 104.810 |
| wall8 | 94.713 | 97.713 | tflat9 (x +15.429) | 110.575 | 116.289 |
| wall9 | 106.192 | 109.192 | bflat10 (x +23.143) | 122.053 | 127.768 |
| wall10 | 117.671 | 120.671 | tflat11 (x +30.857) | 133.532 | 139.247 |
| wall11 | 129.150 | 132.150 | bflat12 (x +38.571) | 145.011 | 150.726 |
| wall12 | 140.629 | 143.629 | tflat13 (x +46.286) | 156.490 | 162.204 |
| wall13 | 152.108 | 155.108 | bflat14 (x +54.000) | 167.969 | 173.683 |
| wall14 | 163.587 | 166.587 | wall15 (x +57.857) | 175.066 | 178.066 |
| flange + | 179.448 | 180.948 | every element pair is separated by one 1.382 bend | | |

Each wall is preceded and followed by a 1.382 bend; fold lines are the tangent pairs listed in `plenum_sep.out` §1. Fold directions alternate: walls j even fold down from a top element to a bottom flat, j odd fold up. Feature positions in the blank: window centres at s = tflat centre (21.601, 44.558, 67.516, 90.474, 113.432, 136.390, 159.347), y -21 / -7; slot centres at s = bflat centre (10.122, 33.080, 56.037, 78.995, 101.953, 124.911, 147.868, 170.826); bleed holes at the wall centres s = (15.861, 27.340, 38.819, 50.298, 61.777, 73.256, 84.735, 96.213, 107.692, 119.171, 130.650, 142.129, 153.608, 165.087) for walls 1..14 at y = -55.5 (odd j) / +55.5 (even j).

### 3.4 Process route

| Step | Prototype / Build A (12 plates) | Volume (100k/yr) | Control |
|---|---|---|---|
| Blank + pierce | laser-cut blank with all features (0.05 kerf, ±0.02) | progressive strip die: pierce windows, slots, bleeds, tabs, reliefs; blank | 100 % vision of slot width and bleed Ø |
| Fold | 3-channel soft-tool coupons for E1 (bend radius, K, springback); Build A on the production-intent sequential folding tool if ready by M3, else **wire-EDM from a 5.8 mm OFE plate** (same envelope, r 0.15 corners) | **sequential corrugating (fin-folding) machine**: two 90° wipe folds per index, 0.6 mm punch nose, strip fed along x, 32 folds per part, ~40 s; the class of machine used for transformer fin walls (1-1.5 mm steel, 3 fins/min at 100-400 mm height) and folded heat-exchanger fins (US 5,694,803, US 6,195,874) | pitch ±0.05, height 5.80 ±0.03 (gauge), perpendicularity ≤ 0.5° |
| Frames | wire-EDM or mill from 2.5 x 6 OFE bar, slots by 0.9 slitting saw | bar stock, gang-sawn slots (16 in one pass), skim to 5.78 | slot pitch ±0.03 |
| Sub-assembly | press frames onto the tabs; 4 laser tacks at the flange corners | same, automated | height 5.80 ±0.03 over the frames |
| Clean | vapour degrease, ISO 16232 flush, no particle > 50 µm | same | gravimetry on samples |
| Filler | route A preform ladders; B / C selective strip plating before folding (section 6) | same | XRF per band |

### 3.5 Process limits used

| Rule | Value | Source / note |
|---|---|---|
| Minimum inside bend radius, soft C10100 | 0 t (datasheet); design 0.75 t | Aurubis PNA 203 Cu-OFE: soft temper bend ratio 0 at 90° and 180°, GW and BW |
| Outer-fibre strain at r_i 0.6 | t / (2 r_i + t) = 40 % | ≤ 45-55 % elongation of soft OFE; orange peel limited by grain ≤ 0.035 |
| K-factor | 0.35 (soft copper), range 0.31-0.39 | PCB-industry soft-copper value / SolidWorks soft-copper allowance; **3-bend coupon fixes it before the die is cut** (developed width shifts ±1.3 mm over 32 bends at ±0.04 K) |
| Springback, soft Cu, r/t 0.75 | 1-2°, compensated by over-bend | tooling |
| Strip thickness tolerance | EN 1652: ±0.04 for 0.5 < t ≤ 0.8, width ≤ 350 | ordered as precision ±0.03 |
| Pierced feature limits in 0.8 Cu | d ≥ 1.0 t conventional, web ≥ 1.5-2 t; here Ø0.6 bleed = 0.75 t → laser or fine-blank punch; 1.8 slot = 2.25 t ok | Mate / Xometry rules (verify-manufacturing) |
| Fixture pressure on the stack at 790 C | ≤ 0.10 MPa (bend-corner bending 7 MPa, flats 2.6 MPa, walls 1.0 MPa vs OFE hot 0.2 % proof ~10 MPa, estimate) | section 9; verify-manufacturing #8 "0.2 MPa" is too high for a folded plenum |

## 4. End frames PLN-F (2 off)

| Feature | Dimension (mm) | Tolerance | Note |
|---|---|---|---|
| Material | OFE C10100 bar, H04 (anneals in braze) | - | |
| Section (y x z) | 2.50 x 5.78 | ±0.02 / -0.02..-0.05 relative to the corrugation 5.80 | frames sit 0.02-0.05 below the flats so the separator rests on the 7 top flats and 2 flanges; frame joints take the thicker gap (bypass-only) |
| Length (x) | 120.70 | ±0.10 | = flange edge to flange edge |
| Position | inner face at y = ±57.00; outer face ±59.50 | ±0.05 | 0.5 beyond the grate recess ends (±54.5) as required by DDG-grate; inside the 122.6 outline by 1.8 |
| Comb slots | 16 x (0.90 +0.05/-0 wide x 1.00 ±0.05 deep, full height) at x = -57.857 + 7.7143 j | pitch ±0.03 | receive the wall tabs; 0.05 clearance per side filled by fillet |
| Chamfer | 0.3 x 45° on the four long edges | - | filler entry |
| Faces | Ra ≤ 0.8, flat 0.02 | - | braze lands to grate web (bottom) and separator (top) |
| Mass | 14.9 g each (CadQuery 29.7 for two) | - | |

The frame separates the inlet-channel ends (pre-meter) from the stack-edge cavity (outlet-side pressure) and the inlet from the outlet ends across each wall tab: both are internal, bypass-only joints (section 6).

## 5. Registration on the grate and tolerance stack

The plenum sub-assembly has no datum holes (a Ø3 pin hole cannot fit a 2.5 mm frame at y 57 without breaking out). It is located in the braze fixture by two hardened stops referenced to the fixture's D1/D2 pins: the -x flange free edge (x = -60.357) and the -y frame outer face (y = -59.50), both ±0.05.

| Check | Nominal margin (mm) | Worst-case stack | Result |
|---|---|---|---|
| Wall inner face (3.457 from the inlet line) vs inlet orifice outer edge (1.25) and recess wall (1.35) | 2.11 | fold pitch ±0.10 + fixture ±0.05 + line ±0.03 = ±0.18 | no wall or foot ever reaches the recess (P6 met with 1.9 mm to spare) |
| Bottom-flat contact inner edge (0.90 from the outlet line) vs outlet hole edge (0.50) | 0.40 | ±0.10 + ±0.05 + ±0.02 + slot ±0.05 = ±0.22 | +0.18 worst case; filler starts 0.30 further out (1.20) → +0.48 |
| Slot (1.80) over the row (holes 1.00 wide): slot edge 0.90 vs hole edge 0.50 | 0.40 | ±0.22 | +0.18; the DDG-grate minimum of 1.60 would give +0.08 → 1.80 chosen |
| Edge outlet slot (centred x ±54.0) vs edge row slots (0.40 wide at ±53.70) | inner 0.40 / outer 1.00 | ±0.22 | +0.18 |
| Top-flat window (5.0 x 10.0) vs separator window (5.0 x 10.0) | 0 (equal) | ±0.10 + ±0.05 + sep ±0.05 = ±0.20 | ≤ 0.20 step at 0.43 m/s: no hydraulic effect; filler mask 0.30 from both edges |
| Wall tab in comb slot | 0.05 per side | tab ±0.02, slot +0.05 | always enters; fillet fills |
| Height: 7 top flats + 2 flanges vs 2 frames | flats 5.80 ±0.03, frames 5.78 -0.02/-0.05 | 0-0.10 gap at the frames | frame gaps ≤ 0.10 filled by 50 µm preform strips (bypass-only joints) |
| Separator window vs cap arch footprint (12 wide) | 1.0 each side in y | sep ±0.05 + cap ±0.3 (drawn) | ≥ 0.6: cap land never over a window |

The grate lane's leg keep-out (|x - x_line| 3.06-3.86 "every line", i.e. a 1.6 mm band at mid-pitch) contains the 0.8 mm wall; `plenum_cq_check.py` confirms that no meter-web hole lies within 0.30 of any bottom-flat contact strip (0 violations over 756 holes).

## 6. Braze joints, filler routes and leak class

All joints below are inside the cap skirt: none adds an external seam (architecture: 1 perimeter lap + 2 bosses).

| Joint | Faces | Bonded area per plate | Structural role | Leak class and worst-case bypass (25 µm unbonded gap, h3 dp / 12 µ L) |
|---|---|---|---|---|
| J1 bottom flats → grate web (GRT-W top) | 8 flats x 2 strips 1.657 x 114 + bends' tangent lines | 3,020 mm2 | **structural**: carries each wall's p x pitch (23.9 N/mm at 3.1 MPa) into the grate land, which sits on tied fins (0.3 pitch) directly below | bypass-only: inlet channel → outlet row across the land, ≤ 0.005 LPM per flat (0.03 % of flow) |
| J2 top flats → separator underside | 7 x 5.714 x 114 - 14 windows (5.6 x 10.6 with mask) | 3,730 mm2 | **structural**: transfers the separator/cap pull into the walls; backs the separator over the inlet channels (composite 2.6 mm) | bypass-only: inlet window → outlet channel across the flat, 0.01 % of flow per flat |
| J3 flanges → separator | 2 x 1.50 x 114 | 342 mm2 | ties the outer walls | bypass-only: edge outlet channel → stack-edge cavity |
| J4 frames → grate web and → separator | 2 x 2.5 x 120.7, both faces | 1,207 mm2 | closes 15 channel ends; compression under fixture load | bypass-only: inlet ends → stack-edge cavity → outlet; 50 µm preform strips because the frame gap is 0-0.10 |
| J5 wall tabs in comb slots | 32 tabs x 3.0 x 1.0, fillets both faces | 190 mm2 | pitch registration only | bypass-only: inlet ↔ outlet at the channel ends through 0.05 clearances, ≤ 0.02 % |
| J6 separator top → cap lands (cap lane) | lands between arches and around the headers | cap lane | **structural**: arch feet pull (p x 12 per arch) enters the separator here | bypass-only between headers: 6 mm land at y -1..+3, 0.05 % per 25 µm gap |
| J7 separator tap bores → cap tap stubs (option) | 2 x Ø1.5 | - | sealing of the tap path | a missed seal mis-reads the tap (reads header pressure), no leak |

**Filler by route** (one vacuum cycle with the fin ties; architecture routes A / B / C; the grate's own interfaces are in DDG-grate section 7):

| Route | J1 (grate side) | J2 / J3 / J4 (separator side) | Masks and capillary breaks | Filler per plate (plenum joints) |
|---|---|---|---|---|
| A BAg-8 preforms, **25 µm** (flat face joints, not tip joints: gap-fill to 0.05 wanted) | PF-3 sheet 120.7 x 119: 7 cut-outs 9.70 x 114 over the inlet channels (floor stays bare, no filler within 1.65 of a recess), 8 cut-outs 2.40 x 110 over the slots (0.30 mask), strips 2.5 wide under the frames | PF-4 sheet: 8 cut-outs 9.70 x 114 over the outlet channels, 14 cut-outs 5.60 x 10.60 around the top-flat windows, flange and frame strips; frames get 50 µm strips | the 0.30 mask is a starve zone; the capillary hierarchy (joint 10-40 µm: 45-180 kPa) keeps filler in the joint; the slot edges have no groove (the GRT-W web is flat) so **the 0.30 mask plus the 2.4 cut-out is the control**; E1 sections check no filler within 0.15 of a slot edge | 3,625 + 4,675 mm2 x 25 µm = 0.21 cm3 ≈ **2.1 g BAg-8** (1.5 g Ag ≈ US$3.1 at US$65/oz) |
| B Ag 8-10 µm electroplate | selective **strip plating of the flat blank before folding**: bands on the bottom-flat underside (2 x 1.96 wide per bflat, from the slot mask to the tangent), top-flat upper side (5.714 minus window masks), flange upper side; frames plated all over | same bands | plating resist = the same mask pattern; bends unplated (no cracking of Ag at 40 % strain); nothing plated faces an orifice | 8,300 mm2 x 9 µm = 75 mm3 ≈ **0.78 g Ag** (US$1.6) |
| C Cu-Sn TLP (~3 µm Sn, belt furnace, E1-gated) | same bands, Sn | same | same | 0.18 g Sn |

Filler volume control: at 25 µm the bottom strips hold 0.04 mm3 per mm of length against a 0.55 mm2 fillet void outside each foot arc; the void stays ~90 % empty, which is intended (it is inside the inlet channel, pre-meter, and carries no load).
