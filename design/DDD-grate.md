# DDD-grate: metered grate (layer 2) and orifice artworks, PRISM-15 Rev A

Detailed design definition, lane `grate`, 2026-10-15. Parent: `docs/cooling/03-architecture.md` (architecture of record, 2.2 / 3.2 / 4.1-4.3 / 5.1-5.3). Verifier inputs honoured: `appendix/verify/verify-manufacturing.md` (#6, #7, #9-#11, #18, required changes 3, 7), `appendix/verify/verify-hydraulics.md` (section 3 segment balance, required changes 2, 3, 9). Scripts in this folder: `grate_cell.py` (geometry, jet, velocities, stresses, limits; `grate_cell.out`), `grate_artwork.py` (graded artworks, CSV/DXF; `grate_artwork.out`, `grate_artwork_params.json`), `grate_outlet_row.py` (segment balance with the row lumped per line; `grate_outlet_row.out`), `grate_cq_check.py` (CadQuery validity/mass check; `grate_cq_check.json`). Model terms are ±25 % until E2; dimensions are drawing values.

**Conventions.** X along the fins (across the lines), Y along the lines, Z up from the die face; origin at the fin-field centre (`cad/prism_cad.py`). Fin tips and base rim at z = 2.80; grate z = 2.80-4.50. Lines at x = -54 + 7.7143 k, k = 0..14; k odd = inlet (7), k even = outlet (8; k = 0, 14 are the edge outlets at x = ±54.000). PG25 at 45-50 C: 1005 kg/m3, 1.25 mPa s. Flow basis 18 LPM unless stated; rated 15 LPM; 150 % rated = 22.5 LPM.

## 1. Function and requirements carried by the grate

| # | Requirement | Value | Source |
|---|---|---|---|
| G1 | Meter every inlet line through graded orifices so that per-orifice flow is uniform along the plenum | ±3 % at 18 LPM, every flow 9-36 LPM | architecture 4.3; task |
| G2 | Meter pressure drop at 18 LPM | 2.30 kPa (Cd 0.72, mean 1.54 m/s); check ≤ 2.3 | architecture 4.2 |
| G3 | Meter velocity | ≤ 2.0 m/s mean at 150 % rated (22.5 LPM) | architecture 4.1 |
| G4 | Jets land on the grate lip, never on fins or base; fin-top velocity | ≤ 0.5 m/s at 18 LPM | architecture 3.2, E2 |
| G5 | Outlet orifice row | 0.5 kPa at each line's nominal 18 LPM flow | architecture 4.3 |
| G6 | Lands brazed to fin tips, continuous across the field | bond fraction ≥ 0.70 of fin-tip length | architecture 5.2; verify-manufacturing #11 |
| G7 | Filler kept 0.3 mm from window edges, none in any orifice | 0.3 mm mask + capillary break | architecture 3.2; verify-manufacturing #10 |
| G8 | Grate carries the plenum-leg pull into the fin ties at design burst | ≤ 40 MPa (post-braze OFE) | architecture 5.2 |
| G9 | Per-SKU change limited to the orifice artwork | laser-pierced sheet, ~US$2-4 | architecture 2.3 |
| G10 | Thickness, outline, mass | 1.70 mm; inside the cap skirt; ≈ 0.21 kg | architecture 2.2, 5.1 |
| G11 | Segment-level max/min (E2) | ≤ 1.15 at 18 LPM, ≤ 1.20 at 27 LPM | architecture 4.3 |

## 2. Construction decision: two laminations brazed in the one cycle

The architecture's section (web on top, lip below it facing the web, window below the lip) is an undercut: the lip is wider than the window beneath it and faces up. A single 1.7 mm plate can only form it with a T-slot (keyseat) cutter working through the 1.2 mm window, or by abandoning the lip (the draft's jets-on-fins geometry, rejected). The grate is therefore two laminations, both OFE C10100, stacked and brazed in the single vacuum cycle with the rest of the plate.

| Option | How the recess is made | Verdict |
|---|---|---|
| A. Single 1.70 mm plate, T-slot undercut from the fin side | 2.7 mm dia x 0.8 mm keyseat cutter on a ≤ 1.1 mm neck, 7 x 109 mm per plate; orifices laser-pierced into a closed cavity | Rejected: cutter deflection and life in gummy OFE, chips and laser dross trapped in a closed cavity (> 50 µm particles downstream of every filter), no gang option, ~US$8-15 |
| B. Single plate, recess coined | 0.8 mm deep in 1.3 mm = 62 % of thickness; limit for closed-die coining of annealed OFE 30-40 % | Rejected (cracking, displaced-metal doming, no undercut anyway) |
| **C. Two laminations: land plate 1.30 mm (windows, recess pockets from its top face, grooves) + meter web 0.40 mm (orifices)** | pockets slot-milled (prototype CNC, volume 7-spindle head or photochemical half-etch); windows pierced/laser; web laser-pierced (die at volume) | **Chosen**: every feature is a plain face operation; the web is the only per-SKU part (G9); one added internal interface that can only bypass, not leak |

Consequences of C (see Deviations D2): one more braze interface of 2 x ~5.9 mm of land per pitch between the recess (post-meter pressure) and the outlet window; a 25 µm unbonded gap over the full field would bypass ~0.03 LPM (0.15 % of flow, `grate_cell.py` basis: h3 dp / 12 µ L), invisible and harmless. Mass 201 g (CadQuery, `grate_cq_check.json`) against the architecture's 210 g (pockets and holes now counted).

```
 cross-section through an inlet line (x across the line, z up; mm)       through an outlet line
 z 4.50 ──────────────── web 0.40 ──┐o┌───── o = orifice 0.50 wide at x = ±1.00     ─────┐ ┌─────  outlet hole 1.00 (edge 0.40)
 z 4.10 ═══ web/land braze ═══╗     │ │     ╔═══ (filler from |x| ≥ 1.65)             ═══╗ │ │ ╔═══ (filler from |x| ≥ 0.90)
        land plate 1.30       ║  recess 2.70 wide, 0.80 deep (stand-off H)             ║ │ │ ║
 z 3.30                       ╚═══╦═══ lip 0.75 ═══╦═══╝  jets land here               ║ │ │ ║
        floor 0.50               ║ window 1.20 ║                                       ║ │ │ ║  window 1.20 through 1.30
 z 2.80 ═══ tie braze ═══════════╩═════╤═╤═════╩════ fin tips (filler from |x| ≥ 0.90)  ═══╩═╤═╤═╩═══ tie braze
        fins 2.0, kerf 0.30 ───────────┘ └──────────────────────────────────────────────────┘ └──
```

## 3. Land plate GRT-L (lower lamination)

Material OFE C10100, H02 strip for machining (anneals in the braze), 1.30 ± 0.02 after a both-faces skim. All positions to datum A (field centre: pin hole D1) / B (pin slot D2); features run the full line length in Y.

| Feature | Qty | Dimension (mm) | Tolerance | Basis / note |
|---|---|---|---|---|
| Thickness | - | 1.30 | ±0.02 | 1.70 - 0.40 web; sets floor and lip height |
| Outline | 1 | 122.6 x 122.6, corners R2.0 | ±0.10 | body 125 - 2 x skirt 1.0 - 2 x 0.2 clearance (cap lane to confirm) |
| Datum D1 | 1 | Ø3.00 H7 at (-57.0, -57.0) | pos ±0.02 | round + slot 2-pin scheme shared by the stack |
| Datum D2 | 1 | slot 3.00 x 3.40 at (+57.0, +57.0), long axis along the diagonal | ±0.02 | takes thermal/registration growth |
| Interior windows | 13 | 1.20 x 108.0 through, ends R0.6, centred on x_line (k = 1..13) | w +0.05/-0; pos ±0.03; L ±0.10 | architecture 1.2 mm window; 0.33 m/s mean face velocity |
| Edge windows | 2 | 0.60 x 108.0 through, x from ±53.40 to ±54.00 (centre ±53.70) | w +0.05/-0; pos ±0.03 | half-area edge outlets (architecture 4.3, segbal) |
| Recess pockets (inlet lines) | 7 | 2.70 wide x 0.80 deep x 109.0 long (y ±54.5), ends R1.35, from the TOP face, centred on x_line (k odd) | w +0.05/-0; depth ±0.03; pos ±0.03 | section 5: lip 0.75, stand-off 0.80, floor 0.50 |
| Floor under pocket | 7 | 0.50 (= 1.30 - 0.80) | ±0.04 (stack) | window depth; 7.5 MPa cantilever (section 8) |
| Lip | 14 | 0.75 wide (x 0.60-1.35 from the line), flat, Ra ≤ 1.6 | derived | jet landing zone, must be burr-free |
| Capillary-break grooves, underside | 28 | 0.15 wide x 0.08 deep along every window edge at |x - x_line| = 0.775 (edge windows: at x = ±53.225), y ±54.3 | w ±0.03, d ±0.02 | inside the 0.3 mask zone; stops filler creep (section 7) |
| Capillary-break grooves, top face | 14 + 14 | at inlet lines |x - x_line| = 1.525 (outside the pocket); at outlet lines 0.775 | same | web/land joint |
| Flatness, both faces | - | 0.020 over the field, 0.030 overall | - | architecture 5.3 "grate flatness ±20 µm"; tie plane |
| Land face Ra | - | ≤ 0.8 (fly-cut or lapped) | - | tie wetting |
| Burr | - | ≤ 0.015 on both faces; pocket/window edges brushed | - | verify-manufacturing #6 |
| Mass | - | 149 g | - | `grate_cq_check.json` (analytic 145, `grate_cell.out` §8) |

Lands: 14 interior strips 6.51 wide (7.714 - 1.20) x full length, two rim lands, all continuous in Y and joined across the field by the solid ends (y beyond ±54.5): the land plate is one piece. Windows and pockets are closed-ended; nothing opens to the stack-edge cavity (which would short the post-meter recess to the outlet side).

Process sequence (prototype → volume): (1) blank 1.30 strip, pierce D1/D2; (2) pockets: CNC slot mill 2.7 mm 2-flute carbide, 2 passes of 0.4, ~1.0 min/plate (volume: 7-spindle slotting head in one pass, or photochemical half-etch ±0.05 as the alternative); (3) windows: laser (prototype) or one-hit closed-slot punch from the FIN side so roll-over sits on the land face edge and the burr on the lip/top face, then brush; (4) grooves: laser scribe (0.15 x 0.08, ~15 s/plate) both faces; (5) stress relieve 300 C / 1 h; (6) both-faces skim to 1.30 ± 0.02 and flatness 0.020 (the skim also removes the window burr); (7) clean to ISO 16232, no particle > 50 µm; (8) route-B/C plating with the mask (section 7) if not route A.

## 4. Meter web GRT-W (upper lamination, the per-SKU artwork part)

Material OFE C10100, O60 or H01 precision strip 0.40 ± 0.010; outline and datums identical to GRT-L (122.6 x 122.6; D1 Ø3.00 H7; D2 slot). Holes are rounded rectangles (w across the line, h along the line).

| Feature | Qty (TTV) | Dimension (mm) | Tolerance | Basis |
|---|---|---|---|---|
| Thickness t | - | 0.40 | ±0.010 | architecture "0.4 mm web"; t/Dh 0.60 |
| Inlet orifices | 378 (7 x 54) | w 0.50, h per size step (0.99 / 1.01 / 1.06 / 1.09 / 1.12), r 0.10; centre at x_line ± 1.00, alternating sides along the line; y = -53 + 2 j | w ±0.010, h ±0.010 (area ±2 %), pos ±0.020 | section 10; architecture 0.5 x 1.0 nominal |
| Outlet holes, interior lines | 324 (6 x 54) | w 1.00, h 1.12, r 0.15 at x_line, y = -53 + 2 j | ±0.015, pos ±0.02 | 0.504 kPa at 2.571 LPM (section 6) |
| Outlet slots, edge lines | 54 (2 x 27) | w 0.40, h 2.78, r 0.10 at x = ±53.70, y = -52 + 4 j | ±0.015, pos ±0.02 | 0.501 kPa at 1.286 LPM; fits the 0.60 edge window with 0.10 margins |
| Hole edge condition | - | laser entry on the plenum (top) face; entry rounding ≤ 0.03; exit dross ≤ 0.015 then electropolish 3-5 µm; taper ≤ 1° (≤ 0.007/side) | - | fixes the Cd direction (verify-hydraulics change 3); jet defined by the sharp exit edge |
| Minimum web between holes | - | 0.88 along inlet and interior outlet rows; 1.22 edge rows | - | web/t 2.2 / 3.05 ≥ 2 (die rule) |
| Keep-out | - | no hole within 0.30 of any plenum-leg footprint (legs at |x - x_line| = 3.06-3.86) or of D1/D2 | - | braze land for the folded plenum |
| Flatness | - | 0.05 free, conforms under fixture load | - | thin sheet |
| Fiducials | 2 | Ø1.00 at (-57.0, +57.0) and (+57.0, -57.0) | ±0.02 | backlit vision reference |
| Marking | 1 | artwork ID + lot, laser, outside the field at (0, -59) | - | ART-TTV-15-A |
| Mass | - | 52 g | - | `grate_cq_check.json` 51.5 g (756 holes) |

Open area (TTV): inlet 195.1 mm2 (mean orifice 0.5162 mm2; 1.538 m/s at 18 LPM), outlet 416.2 mm2; 756 holes. Artwork files: `artwork_prism15_ttv.csv` (columns line_id, line_x_mm, orifice_index, x_mm, y_mm, w_mm, h_mm, type, then r_mm, area_mm2, size_step, lip_side, zone, q_rel_18lpm, u_18lpm_m_s, lamination) and `artwork_prism15_ttv.dxf` (R2010, mm; layers WEB_ORIFICE_INLET, WEB_ORIFICE_OUTLET for GRT-W; LAND_RECESS_TOP, LAND_WINDOW_THRU, LAND_GROOVE_BOTH_FACES for GRT-L; OUTLINE_BOTH, DATUM_BOTH; MASK_NO_FILLER for the preform/plating masks; REF).

Process: laser pierce (single-mode fibre, 0.5-1 kW, N2 assist, kerf 0.03-0.05, position ±0.01-0.02 on a linear-scale flatbed), ~0.1 s per hole, ~1.3 min per plate (US$2-4 at 100k/yr, architecture 2.3); electropolish; 100 % backlit vision of every hole area (±1 %) and position; volume option after artwork freeze: perforating die, 5 inlet punch sizes + 2 outlet punch sizes, d/t 1.25 / 2.5 / 1.0, clearance 4-6 % t per side, punch entry from the plenum face, shaved burr ≤ 0.015; die-made holes re-qualify Cd (roll-over differs from laser entry).

## 5. Stepped recess: jet landing and fin-top velocity

Jet physics (`grate_cell.out` §1-2): orifice exit mean 1.54 m/s (vena contracta 2.48 m/s if the jet does not reattach in the 0.4 web, Cc 0.62); stand-off H = 0.80 = 1.6 orifice widths, inside the potential core (4-6 w), so the jet arrives at the lip at exit velocity with a mixing-layer growth of ~0.1 H per side (0.08 mm). Stagnation pressure on the lip 1.2-3.1 kPa; lip shear ~90-150 Pa at 18 LPM (x1.56 at 22.5 LPM): copper, PG25, ≤ 50 µm particles, erosion checked in E4 at 1x / 1.5x / 2x.

| Quantity | Value (mm) | Note |
|---|---|---|
| Window half-width | 0.60 | fixed |
| Lip | 0.60-1.35 (0.75 wide) | recess 2.70 |
| Orifice | 0.75-1.25 (centre 1.00, w 0.50) | alternating ±x along the line |
| Jet footprint at the lip | 0.670-1.330 | 0.08 spread per side |
| Inner margin (jet edge → window edge) | 0.070 nominal; 0.023 at RSS; -0.010 worst case | position stack: orifice ±0.02, pocket/window ±0.03, lamination registration ±0.03 → RSS ±0.047, worst ±0.08 |
| Outer margin (orifice edge → recess wall) | 0.100 nominal; 0.053 RSS; 0.020 worst | ≥ 0 always: no orifice area is ever masked by the wall (flow error would be 1:1 with area) |

Why not the architecture's 2.5 / 0.65: with the orifice centred on a 0.65 lip the spread jet reaches 0.03 past the window edge nominally and 0.08 at RSS, so ~10-15 % of the jet would drop straight down the window onto the fin tips at ~1.5 m/s. The alternatives (`grate_cell.out` §1): recess 2.60 / lip 0.70 gives +0.020 nominal, -0.027 at RSS; 2.70 / 0.75 gives +0.070 / +0.023; 2.80 / 0.80 gives +0.120 / +0.073. 2.70 / 0.75 is the smallest recess with a positive RSS margin; it is recorded as Deviation D1 (nil thermal or hydraulic effect: window, meter and kerf are unchanged). If the E2 CFD shows the jet has no tolerance to spill, the fallback is 2.80 / 0.80 with the orifice at ±1.05 (land to the leg face 1.66 mm, still 14 MPa).

Fin-top velocity. The mean through the 1.2 x 108 window face is 0.331 m/s at 18 LPM and 0.413 at 22.5 LPM. Locally, each orifice's flow crosses the window edge as a wall-jet sheet of height H over the 2 mm pitch and decays ~20 % through the 0.5 mm floor:

| H (mm) | floor (mm) | entry sheet u, 18 LPM | fin-top estimate, 18 LPM | 22.5 LPM | inner jet margin |
|---|---|---|---|---|---|
| 0.60 | 0.70 | 0.66 | 0.53 | 0.66 | 0.090 |
| 0.70 | 0.60 | 0.57 | 0.45 | 0.57 | 0.080 |
| **0.80** | **0.50** | **0.50** | **0.40** | **0.50** | **0.070** |
| 0.90 | 0.40 | 0.44 | 0.35 | 0.44 | 0.060 |
| 1.00 | 0.30 | 0.40 | 0.32 | 0.40 | 0.050 |

Nominal H = 0.80 meets G4 at 18 LPM with 20 % margin on a ±30 % estimate; the range is 0.70-0.90 (floor 0.60-0.40) and the value is fixed by the E2 single-cell CFD and water-table PIV (pass: fin-top ≤ 0.5 m/s at 18 LPM, jet footprint wholly on the lip). Deeper recesses trade floor thickness (cantilever 7.5 MPa at 0.50, 11.7 MPa at 0.40) and inner margin. Below the window: 0.45 mm of unbonded fin-tip stubs each side of the 0.30 kerf (kerf = 25 % of the window face), so the entry is part kerf (full height) and part fin-top, as the 2-D cell model assumes (`appendix/arch/cell2d.py`).

## 6. Grate hydraulics

### 6.1 Meter (inlet orifices)

| Item | Value | Basis |
|---|---|---|
| Total inlet open area, as drawn | 195.1 mm2 (target 194.8 = 18 LPM / 1.54 m/s) | `grate_artwork.out` |
| Mean orifice area / length | 0.5162 mm2 / 1.05 (w 0.50, r 0.10) | A = w h - (4 - π) r2 |
| Mean velocity 15 / 18 / 22.5 / 23.4 / 27 / 36 LPM | 1.28 / 1.54 / 1.93 / 2.00 / 2.31 / 3.08 m/s | G3 met: 2.0 m/s mean at 23.4 LPM (architecture rating 19.5 kW) |
| Largest single-orifice velocity (step 5 at y = +15, most-fed position) | 1.64 m/s at 18 LPM; 2.05 at 22.5; 2.13 at 23.4 | 6 % above the mean; the cap is a mean-velocity rule |
| Meter dp at 18 LPM, flow-weighted | 2.309 kPa (min 2.00, max 2.61 per orifice) | check ≤ 2.3: met within rounding |
| Dh / t/Dh / Re | 0.666 mm / 0.60 / 823 at 18 LPM (412 at 9, 1647 at 36) | thick-orifice regime; Cd depends on entry edge and direction |
| Cd band and plate dp at 18 LPM | 0.61: 3.20 / 8.5; 0.65: 2.82 / 8.1; **0.72: 2.30 / 7.6**; 0.80: 1.86 / 7.2 kPa | `grate_cell.out` §3; ±10 % Cd = +0.54 / -0.40 kPa plate |

Cd is gated by the E2 coupon test (Re 300-1700, both flow directions, laser-entry up and down, 5 sizes). If the coupon Cd differs from 0.72 the along-plenum grading stays valid (sensitivity 1.044-1.055, section 10) and the programme decides between holding 2.3 kPa (scale all areas by 0.72/Cd, re-pierce) and accepting the dp shift.

### 6.2 Outlet orifice row (G5)

| Line type | Flow at 18 LPM | Holes | Area | Velocity | dp 18 / 36 LPM |
|---|---|---|---|---|---|
| Interior outlet (6) | 2.571 LPM | 54 x (1.00 x 1.12 r0.15) = 1.1007 mm2 each | 59.4 mm2 | 0.721 m/s | 0.504 / 2.02 kPa |
| Edge outlet (2) | 1.286 LPM | 27 x (0.40 x 2.78 r0.10) at 4 mm = 1.1034 mm2 each | 29.8 mm2 | 0.719 m/s | 0.501 / 2.01 kPa |

Row velocity u = Cd sqrt(2 dp/ρ) = 0.718 m/s. The row sits in the web directly over the 1.2 mm window (edge: 0.6 mm window), hole edges 0.10 inside the window edges. The row is one lumped element per outlet line (the left and right segments have already merged in the kerf), which is how `grate_outlet_row.py` models it; `final_segbal.py` placed it per segment.

### 6.3 Segment and line balance with the row as built

| Case (`grate_outlet_row.out`, Rev A network, header x2, edge windows half area) | 9 LPM | 18 LPM | 27 LPM | 36 LPM |
|---|---|---|---|---|
| architecture convention: row 0.5 kPa per segment (`final_segbal.out`) | 1.045 | 1.061 | 1.070 | 1.076 |
| no outlet row | 1.060 | 1.100 | 1.137 | 1.172 |
| **row 0.5 kPa lumped per line, 54 / 27 holes (design)** | 1.057 | **1.092** | **1.122** | 1.148 |
| edge rows with 54 holes (0.125 kPa at the edge) | 1.147 | 1.241 | 1.312 | 1.367 |
| row 0.75 kPa per line | 1.056 | 1.090 | 1.117 | 1.140 |
| row 1.0 kPa per line (R2 fallback artwork) | 1.055 | 1.088 | 1.114 | 1.135 |
| design, port jet undiffused | 1.085 | 1.116 | 1.138 | 1.158 |
| design, outlet header not doubled | 1.159 | 1.287 | 1.418 | 1.546 |

Segment max/min 1.092 at 18 LPM and 1.122 at 27 LPM pass E2 (≤ 1.15 / ≤ 1.20); line max/min 1.035. The architecture's 1.061 was the per-segment convention (Deviation D5, a corrected prediction, not a design change). The edge rows must carry their full 0.5 kPa (27 holes, not 54), otherwise the edge segments over-draw (1.24). Raising the row to 1.0 kPa buys only 0.004 at 18 LPM for +0.5 kPa plate dp, so 0.5 kPa stands; the R2 fallback artwork (row 1.0 kPa: h 0.79 instead of 1.12) is pre-computed.

### 6.4 Velocity hierarchy through the grate at 18 LPM

| Station | Velocity | Cap / note |
|---|---|---|
| Inlet channel floor (web, plenum side) | ≤ 0.62 m/s half-channel | plenum lane |
| Orifice | 1.54 mean (1.44-1.64) | ≤ 2.0 at 22.5 LPM (mean 1.93) |
| Jet at the lip | 1.5-2.5 (reattached to vena contracta) | lands on the lip, never on fins |
| Window face | 0.33 mean; entry sheet 0.50; fin-top ≤ 0.40 est. | ≤ 0.5 (E2 CFD) |
| Kerf (0.30 x 2.0 under the window) | ~0.5-0.7 if ~half the line flow descends | verify-hydraulics "kerf share"; E2 |
| Fin gaps | 0.20 | architecture |
| Outlet window face | 0.33 | - |
| Outlet row | 0.72 | 0.5 kPa |

Passage hierarchy preserved: window 1.2 > orifice 0.5 > kerf 0.3 > gap 0.15 (nothing sieves upstream of the fins). Fin-field dp taps are cap/separator features (inlet header to outlet header), not grate features.

## 7. Land pattern, bond fraction, filler masking and capillary breaks (G6, G7)

| Item | Value | Basis |
|---|---|---|
| Unbonded width per line (window 1.20 + 2 x 0.30 mask) | 1.80 mm (edge: 0.60 + 0.30 inboard) | architecture 3.2 |
| Bonded land per 7.714 pitch | 5.914 mm, continuous in Y over 108 mm and across the field between windows | section 3 |
| Bond fraction | **0.767 of the pitch; 0.798 of the fin-tip length between kerfs (7.414)** ≥ 0.70 | `grate_cell.out` §5; verify #11 gave 0.70 at the draft's 6 mm pitch |
| E1 gate as applied to this grate | every land strip ≥ 70 % wetted over any 10 mm in Y (0.54 effective of pitch) | architecture E1 |
| Tie load path | plenum leg at |x - x_line| 3.06-3.86 stands on the full-thickness land; ties within ±3 mm of the leg carry its pull | section 8 |

**Filler routes on the two grate interfaces** (both in the one vacuum cycle; the architecture's routes A/B/C):

| Route | Tip joint (GRT-L underside ↔ fin tips and base rim) | Web joint (GRT-W ↔ GRT-L top) | Masks |
|---|---|---|---|
| A BAg-8 preform | 12-15 µm foil ladder: 15 cut-outs 1.80 wide (edge 0.90) x 108.6 long on the window lines; perimeter ring to the rim | 12-15 µm foil sheet: 7 cut-outs 3.30 x 109.6 (recess + 2 x 0.30) and 8 cut-outs 1.80 x 108.6 (outlet windows); clearance 0.3 at D1/D2 | cut-outs = MASK_NO_FILLER layer in the DXF |
| B Ag plating | 8-10 µm on the GRT-L underside, masked (tape/resist) on 1.80-wide strips over the windows | 8-10 µm on the GRT-L top face, masked 3.30 over pockets, 1.80 over outlet windows; GRT-W bare | plating only on GRT-L (the web stays a flat bare sheet: nothing plated near an orifice) |
| C Cu-Sn TLP (C2) | ~3 µm Sn on GRT-L underside, same mask | ~3 µm Sn on GRT-L top, same mask | belt furnace N2/H2; E1-gated |

Filler needed per plate for the two grate interfaces (route A, 13 µm): tips 58 mm3 + web/land 142 mm3 ≈ 2.0 g BAg-8 (`grate_cell.out` §5). The 0.3 mm mask is a starve zone, not a barrier: the joint gap (10-40 µm, capillary pressure 45-180 kPa) always out-pulls the 0.15 gap (12 kPa) and the 0.30 kerf (6 kPa), so filler that reaches the mask edge creeps along the joint toward the window. The capillary-break grooves (0.15 x 0.08, laser-scribed, section 3) sit inside the mask zone at 0.10 from the window (recess) edge: a 150 µm gap has 1/6-1/18 of the joint's capillary pull, so the front stops at the groove. Orifices are ≥ 0.40 mm from the nearest filler (inlet: recess wall 1.35 + 0.30 = 1.65 vs orifice edge 1.25; outlet: 0.90 vs 0.50), meeting the ≥ 0.35 rule. E1 verifies by sectioning (no filler within 0.15 of a window edge, none in a groove's inboard side) and by 100 % backlit vision of orifice areas before and after braze (±1 %).

## 8. Structural checks (post-braze OFE, design allowable 40 MPa, design burst 3.1 MPa)

The grate is wetted on both faces: under proof and burst it carries no net pressure. Its loads are (a) the meter dp across the web in flow, (b) the plenum-leg pull (the cap/separator pressure load passing down the 0.8 mm legs) reacted by the fin ties, and (c) the fin-tie tension from the base pressure.

| Load path | Stress at 3.1 MPa | Allowable | Basis |
|---|---|---|---|
| Web over the 2.70 recess, 0.40 t, under meter dp 9.2 kPa (36 LPM) | 0.21 MPa | 40 | fixed-edge strip, `grate_cell.out` §6 |
| Plenum leg 0.8 mm at 7.714 pitch | 29.9 MPa | 40 | `pkgA_dp_stress.out` 29.8 |
| Land strip, outlet side: 2.46 mm from the window edge to the leg face, tie pull 3.1 MPa, t 1.70 (bonded laminations) | 25.8 MPa | 40 | cantilever moment 12.4 N mm/mm; `pkgA_dp_stress` 28.6 at a 3.25 arm |
| Land strip, inlet side: 1.71 mm from the recess wall to the leg face, t 1.70 | 13.8 MPa | 40 | same method |
| Recess floor cantilever, 0.75 lip at t 0.50, tied from x 0.90 | 7.5 MPa | 40 | M 0.31 N mm/mm |
| Tie stress per leg pitch, f 0.70 | 11.6 MPa mean | 40 (local 22-28 per verify) | verify-manufacturing #15 basis 8.9 / 22 |
| Web/land interface shear under the leg pull | 24 N/mm over ≥ 2 x 2 mm of bonded land | BAg-8 shear ≥ 100 MPa, Cu-Sn TLP ≥ 40 | 6 MPa |

The outlet-side land strip (25.8 MPa) is the governing grate member and is why the laminations must be bonded over the land (an unbonded web adds nothing; the 1.30 land plate alone gives 44 MPa). The governing plate defect (one unbonded land strip spanning kerf to kerf, 7.41 mm) belongs to the base/E1 lane and is unchanged by this design (`pkgA_dp_stress.out`: 67-99 MPa at proof at 0.8 mm base, detectable bulge 2.2 µm).

## 9. Manufacturing route, process limits, inspection and cost

### 9.1 Process-limit checks for OFE C10100 (`grate_cell.out` §7)

| Feature | d or w | t | d/t | web | web/t | Laser | Perforating die |
|---|---|---|---|---|---|---|---|
| Inlet orifice 0.50 x 0.99-1.12 | 0.50 | 0.40 | 1.25 | 0.88 | 2.2 | ok | ok |
| Outlet hole 1.00 x 1.12 | 1.00 | 0.40 | 2.5 | 0.88 | 2.2 | ok | ok |
| Edge outlet slot 0.40 x 2.78 | 0.40 | 0.40 | 1.0 | 1.22 | 3.05 | ok | ok (limit) |
| Window 1.20 through the 0.50 floor | 1.20 | 0.50 | 2.4 | 3.81 | 7.6 | ok | ok |
| Window 1.20 through 1.30 (outlet lines) | 1.20 | 1.30 | 0.92 | 3.81 | 2.9 | ok | fine-blank or guided punch (verify #6) |
| Recess pocket 2.70 x 0.80 in 1.30 | - | 1.30 | 62 % depth | - | - | n/a | coining limit 30-40 % → milled |

Rules used: conventional piercing d ≥ 1.0 t and web ≥ 1.5-2 t (Mate / Xometry, cited in verify-manufacturing); fine-blank d ≥ 0.6 t; punch clearance 4-6 % t per side for annealed Cu; burr ≤ 10 % t, shaved ≤ 0.015; roll-over 10-20 % t on the punch-entry face. Laser (fibre, 0.4 Cu): minimum feature 0.10, kerf 0.03-0.05, taper ≤ 1°, HAZ ≤ 0.03, dross ≤ 0.02 removed by 3-5 µm electropolish, position ±0.01-0.02. Coining (closed die, annealed OFE): ≤ 30-40 % of thickness at 300-600 MPa; used only if the 0.08 grooves are not laser-scribed.

### 9.2 Route summary

| Step | Prototype / Build A (12 plates) | Volume (100k/yr) | Control |
|---|---|---|---|
| GRT-L pockets | CNC slot mill, 2 passes | 7-spindle slotting head (1 pass) or photochemical half-etch | depth ±0.03, width +0.05/-0, Ra 1.6 |
| GRT-L windows | laser | closed-slot punch from the fin face, brush | w +0.05/-0, burr ≤ 0.015 after skim |
| GRT-L grooves | laser scribe | laser scribe | 0.15 x 0.08 ±0.02 |
| GRT-L flatten/skim | fly-cut both faces | fly-cut both faces | 0.020 flatness, 1.30 ±0.02 |
| GRT-W holes | laser, entry from the plenum face | laser; perforating die after artwork freeze (re-qualify Cd) | 100 % backlit vision ±1 % area, ±0.02 position |
| Deburr | electropolish 3-5 µm | electropolish | no dross ≥ 0.015 |
| Filler | preform ladders (route A) | plating on GRT-L (B) or Sn (C2) | XRF per strip, preform vision |
| Stack | pins D1/D2, fixture pads | same | registration ±0.03 |
| Clean | ISO 16232, no particle > 50 µm | same | flush gravimetry |

### 9.3 Inspection (grate-specific additions to architecture 5.3)

1. GRT-W: 100 % backlit vision of all 756 holes (area ±1 %, position ±0.02, no dross), per-SKU artwork checksum; sample Cd coupons per laser lot.
2. GRT-L: pocket depth and floor thickness by touch probe on 7 x 3 points; flatness map both faces (0.020); window width gauge; groove depth by profilometer on samples; lip Ra.
3. After braze (per lot): CT for filler presence under every land strip and absence in grooves/orifices; sections on E1 coupons; dp at three flows (CpK ≥ 1.33) which also screens a mis-sized artwork (±2 % area = ±4 % meter dp = ±1.2 % plate dp).
4. Dye/IR water table (E2) per segment: ≤ 1.15 at 18 LPM.

### 9.4 Cost (basis `cost_mass_height.out`: grate line US$6.8 at 100k/yr)

| Line | US$/plate at 100k/yr | Note |
|---|---|---|
| OFE strip 1.30 + 0.40, 122.6 sq, 197 g finished (~280 g buy) | 4.1 | Cu US$14.6/kg |
| Pockets (multi-spindle) + windows (punch) + grooves + skim | 2.5-3.5 | ~1.5 min machine time |
| Web laser piercing + electropolish + vision | 2-4 | architecture 2.3 |
| Second preform / plating mask (vs a single plate) | +0.5-1.0 | Deviation D2 |
| **Total grate** | **~9-13** | vs 6.8 + part of the US$2.5 "Rev A additions" (stepped recess, outlet row) |

The grate is 6-8 % of the US$165 plate; the two-lamination route adds about US$1 against the architecture's line, well inside its ±20 % band and inside the Rev A additions allowance.

## 10. TTV artwork ART-TTV-15-A (15 kW benchmark plate)

Method (`grate_artwork.py`, physics of `appendix/verify/ctl/plenum_graded.py` PKG-A run): 1-D centre-fed inlet channel (6.9 x 5.0, window at y = -14) and outlet channel (window at y = +14), 432 cells of 0.25 mm per line; branch = fin segment 1.07 kPa viscous + meter 2.30 + row 0.50 + misc 0.08 kPa inertial; dividing/combining momentum coefficients 1.0 / 2.0. Orifice areas graded continuously, quantised to 5 sizes (Lloyd), re-solved with the as-drawn (0.01 mm rounded) lengths.

| Step | Length h (mm) | Area (mm2) | Relative area | Count (7 lines) | Share |
|---|---|---|---|---|---|
| 1 | 1.12 | 0.5514 | 1.069 | 84 | 22.2 % |
| 2 | 1.09 | 0.5364 | 1.039 | 56 | 14.8 % |
| 3 | 1.06 | 0.5214 | 1.011 | 56 | 14.8 % |
| 4 | 1.01 | 0.4964 | 0.964 | 98 | 25.9 % |
| 5 | 0.99 | 0.4864 | 0.939 | 84 | 22.2 % |

Span 1.134x in area (architecture ~1.16x; Deviation D3). Sequence along every inlet line, y = -53 → +53 (1 = largest): `1 1 1 1 1 1 1 1 1 1 2 1 1 2 2 2 2 2 2 2 3 3 3 3 3 3 3 3 4 4 4 5 5 5 5 5 5 5 5 5 4 5 4 5 4 5 4 4 4 4 4 4 4 4`. Large orifices sit at the far dead end of the outlet channel (y -53), small ones just past the outlet window (y +15 .. +33) where the combining-manifold pressure is lowest. Sides alternate +x / -x (odd / even index) so both lips receive 27 jets per line.

| Flow (LPM) | Ungraded max/min (cell) | Graded (cell) | Graded per orifice | Per-orifice min / max |
|---|---|---|---|---|
| 9 | 1.114 | 1.048 | 1.044 | 0.983 / 1.027 |
| 18 | 1.120 | 1.048 | **1.044 (±2.2 %)** | 0.983 / 1.026 |
| 22.5 | 1.121 | 1.050 | 1.044 | 0.983 / 1.026 |
| 27 | 1.122 | 1.052 | 1.046 | 0.981 / 1.026 |
| 36 | 1.123 | 1.053 | 1.047 | 0.980 / 1.026 |

G1 met (±2.2 % ≤ ±3 %) at every flow, because both the profile and the meter scale with u2. Sensitivity (per-orifice max/min at 18 / 36 LPM): Cd 0.80 1.055 / 1.055; Cd 0.65 1.044 / 1.043; no outlet row 1.056 / 1.057; windows at ±16 1.047 / 1.047; at ±12 1.050 / 1.048; feed spread over two arches (y -26..-2) 1.058 / 1.060; ungraded 1.118 / 1.122. The artwork is robust to a ±2 mm window move and to a distributed feed; it must be re-run if the separator windows move > 2 mm or the channel section changes.

Totals: 378 inlet orifices, 195.1 mm2; 324 + 54 outlet holes, 416.2 mm2; 756 holes. Meter dp 2.31 kPa at 18 LPM (G2); mean 1.54 m/s, max orifice 1.64 m/s at 18 LPM, mean 1.93 / max 2.05 m/s at 22.5 LPM (G3 met on the mean). Files: `artwork_prism15_ttv.csv`, `artwork_prism15_ttv.dxf`, `grate_artwork_params.json`.

## 11. PRISM-G zoned example artwork ART-G-EX-A

Package: 4 dies 26 x 33 mm at 350 W/cm2 (12,012 W) + 16 HBM 11 x 12 mm at 40 W/cm2 (845 W) = 12,857 W on a 110 (x) x 120 (y) field; dies at (±15, ±18.5), HBM columns at x = ±35.5 and ±48.5, y = ±7, ±21. Zoning by heat (architecture 3.5) with the flux-graded line pitch (3.3): die block ≥ 250 W/cm2 → L 5.5 mm (line pitch 5.5), HBM and margin → L 11 mm. Lines (17): outlets at 0, ±11, ±22, ±33, ±55 (edge); inlets at ±5.5, ±16.5, ±27.5, ±44. Zones are the package footprints dilated by the lid spreading (dies +3 mm, HBM +2 mm); margin positions carry no orifice and are fed by the plenum-end bleeds only. Same web, land-plate and recess design; only the artwork and the line positions change (the PRISM-G land plate and plenum are their own parts, 124.6 x 134.6 outline assumed).

| Inlet line | x (mm) | Zone (L) | Flow at 18 LPM | Open area (mm2) | Orifice velocity | Plenum half-channel u (4.7 x 5.0) |
|---|---|---|---|---|---|---|
| I1 / I8 | ±44.0 | HBM (11) | 0.53 LPM | 4.8 | 1.73-1.82 m/s | 0.09 m/s |
| I2 / I7 | ±27.5 | die (5.5) | 2.44 | 26.5 | 1.54 | 0.87 |
| I3-I6 | ±16.5, ±5.5 | die (5.5) | 3.02 | 31.9 | 1.54-1.58 | 1.07 |

| Result | Value | Note |
|---|---|---|
| Flow share | **die zone 94.3 %** (≥ 85 % required), HBM 5.7 %, margin 0 % + bleeds | real heat share 93.4 / 6.6 % |
| Flow per area | die 0.338 LPM/cm2 (2.5x field mean); HBM 0.041 (0.30x; architecture 0.3-0.5x) | dilated footprints 50.2 / 25.5 cm2 |
| Fin segments | die u 0.31 m/s, 1.18 kPa (L 5.5); HBM 0.076 m/s, 0.58 kPa (L 11) | TTV: 0.20 m/s, 1.07 kPa |
| Branch dp | 4.06 kPa (die meter 2.30 + fin 1.18 + row 0.50 + misc 0.08) | TTV 3.95 |
| Meter dp at 18 LPM | die-zone orifices **2.30 kPa** at 1.54 m/s (check ≤ 2.3 met); HBM orifices 2.90 kPa | common plenum: HBM orifices must take the dp the die fins do not |
| Max orifice velocity | **1.73 m/s** (HBM, 0.5 x 0.5 sites) at 18 LPM; 2.21 at 23 LPM (150 % of the package's 15.4 LPM rating) | exceeds the 2.0 cap at 150 % rated: use L 8 in the HBM zone or the -HF die meter (1.3 m/s) for a product artwork |
| Open area | 190.1 mm2 inlet (360 orifices: 320 die 2 x (0.5 x 0.85-1.05) per position, 40 HBM 0.5 x 0.50 dithered); 480 outlet holes | 840 holes |
| Outlet rows (0.5 kPa each) | O at 0 / ±11: 60 x (1.0 x 1.19); ±22: 1.0 x 1.07; ±33: 1.0 x 0.59; edge ±55: 30 x (0.4 x 0.53) | web ≥ 0.81 |
| Plenum note | die lines run 1.07 m/s half-channel at 4.7 x 5.0: PRISM-G plenum should be 7 mm deep (0.76 m/s) | plenum lane |

Files: `artwork_prism_g_example.csv` (same columns; zone = die / hbm / outlet), `artwork_prism_g_example.dxf` (package footprints on layer REF). The example demonstrates the zoning method; a product artwork needs the PRISM-G plenum (end-fed, 10 mm horizontal ports) profile re-run and the die-zone L confirmed against the 2-D cell model at 350 W/cm2 (architecture 6.4: ~98 C with LM).

## 12. Interfaces to the other lanes

| Lane | What this design needs / gives | Value |
|---|---|---|
| Base + fins | fin-tip plane at z 2.80 flush with the rim top, ±10 µm after diamond planing; rim ≥ 122.6 square available for the GRT-L perimeter land; pins D1 Ø3.00 h6 at (-57, -57) and D2 at (+57, +57) in the rim; kerfs 0.30 centred on x_line ±0.03; an end gap ≥ 0.3 at x = ±54.0 (fin ends free of the pocket wall) so the edge segments exit full-height (if confirmed the edge windows may widen to 0.90, x 53.4-54.3) | section 3 |
| Folded plenum | legs 0.8 wide land on the web at |x - x_line| = 3.06-3.86 (every line); outlet-channel flats over outlet lines need a slot ≥ 1.60 wide over the row (holes at ±0.50) with filler masked 0.30 from the slot; end frames clear the recess ends (y ±54.5) by ≥ 0.5; bleed holes 1.1 mm are plenum features | section 4 keep-out |
| Separator / cap | inlet windows centred at y = -14 ±2, outlet at +14 ±2 (artwork re-run if moved further or if the channel section changes); outline 122.6 inside the skirt with 0.2 clearance; fin-field dp taps in the headers | section 10 sensitivity |
| Braze / E1 | preform ladders or GRT-L plating per section 7; grooves as capillary breaks; fixture load ≤ 0.6 MPa on the tips; registration ±0.03 on D1/D2; E1 coupon sections for filler run-out and web/land bond | sections 7-9 |
| Test / E2 | single-cell CFD + PIV fixes H (0.70-0.90) and lip (0.70-0.80); coupon Cd(Re) both directions; water-table segment max/min ≤ 1.15 | section 5-6 |
| CAD | `params-grate.json`: lamination thicknesses, outline, datums, window/recess/groove geometry, hole lists via the CSVs, mass | this folder |

## 13. Deviations from the architecture of record

| # | Architecture | This design | Reason | Consequence |
|---|---|---|---|---|
| D1 | stepped recess 2.5 wide, lip 0.65, orifice centred on the lip (±0.925) | recess 2.70, lip 0.75, orifice centre ±1.00; range 2.6-2.8 fixed by E2 | jet spread + position stack (RSS ±0.047) leave no margin at 2.5 / 0.65: 10-15 % of each jet would spill down the window at ~1.5 m/s | thermal 0 K, hydraulic 0 (window, meter, kerf unchanged); full-thickness land to the leg 1.71 mm (13.8 MPa); cost 0 |
| D2 | "1.7 mm OFE; stepped recess gang-milled from the fin side; orifices pierced through the 0.4 mm web" (one part) | two laminations 1.30 + 0.40 brazed in the same cycle | the lip faces the web: an undercut that no face operation on one plate can make | one more internal interface (bypass-only, ≤ 0.15 % of flow at a 25 µm gap); +US$0.5-1.0; mass 201 g vs 210 g; web is the only per-SKU part (improves G9) |
| D3 | 5 sizes spanning 1.16x in area | 5 sizes spanning 1.134x (lengths 0.99-1.12) | re-solved with as-drawn rounded lengths and the 0.5 kPa row | per-orifice ±2.2 % at every flow (target ±3 %) |
| D4 | outlet row unspecified at the edge lines | 27 slots 0.40 x 2.78 at 4 mm pitch in the 0.60 edge window | a 1.0 mm hole cannot sit in a 0.6 mm window; full 0.5 kPa needed at the edge (54 holes would give 1.24 segment max/min) | 0.501 kPa, identical to interior |
| D5 | segment max/min 1.061 at 18 LPM (row applied per segment) | 1.092 at 18 LPM, 1.122 at 27, 1.148 at 36 with the row lumped per line as built | physical placement of the row | still passes E2 (≤ 1.15 / 1.20); flow hot-spot term 1.5 K unchanged |
| D6 | orifice "0.5 x 1.0 nominal" | mean length 1.05 (0.99-1.12) with r 0.10 | holds the fixed 1.54 m/s / 2.30 kPa with rounded corners | none |
| D7 (example) | PRISM-G on the 15-line family | 17 lines, pitch 5.5 over the die block, 11 elsewhere | with uniform 7.86 mm lines the die cells' fin dp (3.6 kPa at 2.5x flow) forces HBM orifices to 2.3 m/s | follows architecture 3.3; PRISM-G plenum 7 mm deep |

## 14. Open items and the tests that close them

| # | Item | Nominal (range) | Closed by | When |
|---|---|---|---|---|
| O1 | Recess depth H and lip width | 0.80 (0.70-0.90); 0.75 (0.70-0.80) | E2 single-cell CFD + water-table PIV: fin-top ≤ 0.5 m/s at 18 LPM, jet footprint on the lip | M2 (before G1) |
| O2 | Cd(Re), direction, laser vs die entry | 0.72 (0.65-0.80) | E2 coupons, Re 300-1700; decide hold-2.3-kPa (re-scale areas) vs accept dp | M2 |
| O3 | Separator window positions / feed spread | y ±14 (±2) | cap/separator lane freeze; artwork re-run (`grate_artwork.py`, 60 s) | G1 |
| O4 | Edge window width | 0.60 (0.60-0.90) | base lane confirms the end gap at x ±54.0 | G1 |
| O5 | Lamination registration | ±0.03 (tighten to ±0.02 if O1 shows no spill tolerance) | E1 coupon CT/sections | M3 |
| O6 | Capillary-break effectiveness, orifice cleanliness | no filler within 0.15 of a window edge; area change ≤ 1 % | E1 sections + backlit vision before/after braze | M3 |
| O7 | Web/land bypass | ≤ 0.2 % of flow | E2 dye test on a Build A plate | M4 |
| O8 | Lip erosion at 2.2-2.5 m/s jets | none measurable | E4 at 1x / 1.5x / 2x, 1,000 h | M10 |
| O9 | Perforating-die transition | after artwork freeze | Build B dies; Cd re-qualification | M6-9 |
| O10 | PRISM-G product artwork | example only | end-fed plenum profile, L 8 or -HF meter in the HBM zone, 7 mm plenum | PRISM-G programme |

## 15. Files

| File | Content |
|---|---|
| `DDD-grate.md` | this document |
| `params-grate.json` | parameter block for the CAD and assembly lanes |
| `grate_cell.py` / `.out` | jet landing, velocities, Cd band, rows, bond fraction, filler, stresses, limits, mass |
| `grate_artwork.py` / `grate_artwork.out` / `grate_artwork_params.json` | graded TTV artwork and PRISM-G example (plenum solver of `appendix/verify/ctl/plenum_graded.py`) |
| `artwork_prism15_ttv.csv` / `.dxf` | 756-hole TTV artwork, both laminations (DXF layers) |
| `artwork_prism_g_example.csv` / `.dxf` | 840-hole zoned example |
| `grate_outlet_row.py` / `.out` | Rev A network with the outlet row lumped per line |
| `grate_cq_check.py` / `.json` | CadQuery validity, volume and mass of GRT-L and GRT-W |
