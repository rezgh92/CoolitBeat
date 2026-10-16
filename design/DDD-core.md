# DDD-core: base and skived-fin core (layer 1), PRISM-15 Rev A

> Detailed design definition, lane `core`, 2026-10-15. Parent: `docs/cooling/03-architecture.md` (architecture of record, sections 2.2, 3.1-3.2, 5.1-5.3). Derivations: `design/core_geom.py` -> `core_geom.out`; parameters: `design/params-core.json`. Verification inputs honoured: `appendix/verify/verify-manufacturing.md` (#2, #3, #4, #7, #13, #14, required changes 5-7) and `appendix/verify/verify-hydraulics.md` (§3 layout, §8 items 1, 8, 9). Modelled numbers ±25 % until tested; dimensions are drawing values.

## 1. Scope, conventions, datums

| Item | Definition |
|---|---|
| Part | One-piece OFE copper base + skived fin field + rim + skirt land + 8 ears + 2 dP-tap bosses. Fins and kerfs are machined before braze; the die face is finished after braze |
| Axes | X along the fins; Y across the fins (lines, kerfs and windows run along Y); Z up from the die face. Origin at the fin-field centre on the die face (same convention as `cad/prism_cad.py`) |
| Datum A | Die face (z = 0, final, after the post-braze fly-cut). Flatness 0.020 over the 108 x 108 fin-field projection, 0.050 over 125 x 125 |
| Datum B | Body edge x = -62.5 (milled), perpendicular to A within 0.05 |
| Datum C | Body edge y = -62.5 (milled), perpendicular to A and B within 0.05 |
| Pre-braze datum A' | Back face of the machined blank (becomes the die face after 1.20 mm is removed). Pocket depth, fin root and tip planes are held to A' |
| Pre-braze locating | Two Ø2.0 H7 pin holes in the rim top (diagonal), used by the braze fixture and by the grate, plenum and separator (their lanes carry matching holes) |
| General tolerance | ISO 2768-f for untoleranced linear dimensions, ISO 2768-K for geometry; surface ISO 1302. Every functional dimension is toleranced explicitly below |
| Fixed by the architecture | 0.8 mm base (1.0 fallback), fins 0.15/0.15 x 2.0, 360 fins, 15 lines at 7.7143 mm, kerfs 0.30 mm, body 125 x 125, land 1.8 mm, flatness ≤ 20 µm, Ra ≤ 0.8 µm, MAWP/proof/burst 1.03/1.55/3.1 MPa |

**Z-stack of the core (final, mm):** die face 0 | base top (fin root) 0.80 (+0.10/-0) | kerf floor 0.85-0.90 | fin tips and rim top 2.80 | land and ear top 1.50 | tap-boss top 2.80. Pre-braze the same features sit 1.20 higher above A'.

## 2. Material and blank

| Item | Specification | Basis |
|---|---|---|
| Alloy | C10100 (OFE, 99.99 Cu, O ≤ 5 ppm) per ASTM B152; C10200 (OF) accepted as alternate for the same drawing | architecture 5.1 (all-OFE); hydrogen embrittlement test ASTM B577 required for route C (N2/H2 belt) |
| Form, temper | Rolled plate, raw 4.3 mm (4.2-4.5 accepted), temper H02 (half-hard); H01 alternate. The skiving house fixes the temper on the E1 skive trial (fin-root cracking vs tearing); post-braze the whole part is annealed, design allowable 40 MPa | verify-mfg #1/#2; skived fin is cold-worked (sy 250-300 MPa) until braze |
| Raw blank size | 141 x 141 x 4.3 when the ears are machined from the blank (0.76 kg); 127 x 127 (0.62 kg) if ears are deleted on an SKU | `core_geom.out` §6 |
| Machined blank | Both faces milled: thickness 4.00 ± 0.02 (rim top to A'), flatness 0.02 each face, parallel 0.02 | sets the pocket floor and rim top from one datum |
| Grain size | ≤ 0.050 mm (ASTM E112) at the skive | fin-root integrity at 0.15 mm thickness; E1 metallography confirms |
| Certification | Mill cert with O content, conductivity ≥ 101 % IACS, grain size; lot-traceable to the plate serial | |
| Cleanliness at receipt | Free of rolled-in scale; no lubricant residue after the pre-skive alkaline clean | braze wetting |

**Skive volume balance** (`core_geom.out` §2): the skive consumes h·t/p = 1.00 mm of blank depth, so a 1.00 mm deep pocket brings the fin tips to the rim top (4.00 above A'); the base under the fins is 2.00 mm during the skive (verify-mfg floor 1.5-2.0), and the post-braze fly-cut removes 1.20 mm to reach 0.80.

## 3. Outline, rim, land, ears, bosses: dimension table

All dimensions mm, final (post fly-cut) unless marked pre-braze. Positions to datums B/C unless stated.

| # | Feature | Nominal | Tolerance | Note |
|---|---|---|---|---|
| 3.1 | Body outline | 125.0 x 125.0 | ± 0.10; corners R 2.0 | milled; B and C are the -x and -y faces |
| 3.2 | Skirt land, outer ring | width 1.80, top z = 1.50 | width ± 0.05, z ± 0.05, flatness 0.03 around the ring | receives the cap skirt foot: the only external perimeter seam. Ra ≤ 1.6 |
| 3.3 | Rim outer wall (lap face) | 121.40 x 121.40 | ± 0.05, perpendicular to A 0.03 | vertical lap face for the drawn skirt (height 1.30: z 1.50 to 2.80); outer top edge chamfer 0.3 x 45° as drawing lead-in; Ra ≤ 1.6 |
| 3.4 | Rim top (grate braze land) | z = 2.80 (= fin tip plane); width 6.35 (x sides), 6.55 (y sides) | coplanar with the fin tips 0.02 (planed in the same pass) | internal joint to the grate margin; filler masked 0.3 from the pocket edge and 0.2 from the outer chamfer -> 5.85 wetted |
| 3.5 | Skive pocket | 108.70 (x) x 108.30 (y), floor at fin root | ± 0.05 position to B/C; ± 0.03 size; corner R 0.5; floor flatness 0.02 (pre-skive) | x: 108.0 fin length + 2 x 0.35 edge channel; y: 360 x 0.30 + 2 x 0.15 |
| 3.6 | Pocket depth (pre-braze) | 1.00 from the rim top (3.00 above A') | ± 0.02 | sets fin-root plane |
| 3.7 | Mounting ears (8) | 12.0 wide x 7.0 protrusion, top z = 1.50, R 2.0 | ± 0.1 | 2 per side, centred at ± 40.0 along each side |
| 3.8 | Ear holes (8) | Ø 3.40 (M3 clearance) | +0.10/-0; position Ø 0.10 to B/C | centres 3.5 outboard of the body edge: (± 40, ± 66.0) and (± 66.0, ± 40). SKU option Ø 4.50 for M4 |
| 3.9 | dP-tap bosses (2) | 8.0 wide x 7.0 protrusion, top z = 2.80 | ± 0.1 | on the -y side at x = 0.000 (inlet line k = 7) and x = +15.429 (outlet line k = 9); clear of the ears at ± 40 |
| 3.10 | Tap holes (2, -T SKUs only) | Ø 1.00 along y from the boss tip (y = -69.5) to the pocket wall (y = -54.15), at z = 1.40 | Ø +0.05/-0; z ± 0.05; length 15.35 | EDM or gun-drilled before skiving; counterbore Ø 1.65 +0.05/-0 x 4.0 deep at the tip for a Cu 1.6 x 0.3 tube stub brazed in the same cycle |
| 3.11 | Locating pin holes (2) | Ø 2.00 H7 x 1.5 deep in the rim top at (+57.5, +57.5) and (-57.5, -57.5) | position Ø 0.03 to B/C | alumina pins 2.0 x 5.5 stay in the assembly; floor 1.3 mm above the die face |
| 3.12 | Border (body edge to fin field) | 8.50 | - | = 0.35 edge channel + 6.35/6.55 rim + 1.80 land |
| 3.13 | Edge radii, die face | 0.5 x 45° chamfer on the die-face perimeter | - | TIM pad protection |

Mass 0.282 kg finished (base 0.112, rim 0.053, fins 0.101, land step 0.006, ears 0.008, bosses 0.003); copper buy 0.76 kg (`core_geom.out` §6).

## 4. Fin field

| # | Feature | Nominal | Tolerance | Basis |
|---|---|---|---|---|
| 4.1 | Fin count, orientation | 360 fins running along X | - | 108 / 0.30 |
| 4.2 | Fin pitch | 0.300 | ± 0.005 per fin; cumulative ± 0.03 over 108 (fin 1 to fin 360) | skiving machine servo feed; CTX-class limit: centre distance ≥ 0.16 mm |
| 4.3 | Fin thickness | 0.150 | ± 0.020 at mid-height; taper tip/root ≤ 0.02 | CTX-class limit ≥ 0.08 mm; E1 trial sets Cpk ≥ 1.33 |
| 4.4 | Gap | 0.150 | result of 4.2 and 4.3: 0.13-0.17 | fouling and h_eff basis (architecture 3.1): gap ≥ 3x the 50 µm guard |
| 4.5 | Fin length | 108.00 (x = ± 54.00) | ± 0.05 after the edge trim (saw, §5) | skived 108.3 wall-to-wall, trimmed to 108.0 |
| 4.6 | Fin height (planed) | 2.00 above the fin root | ± 0.02; as-skived 2.10 ± 0.05 before planing | h/gap 13.3 (skiving range 10-25) |
| 4.7 | Fin-tip plane | z = 2.80; flatness ≤ 0.020 over the field (routes A, C); ≤ 0.010 process target (route B, 8-10 µm Ag) | coplanar with the rim top 0.02 | verify-mfg #9, required change 7 |
| 4.8 | Fin centres (y) | y_i = -53.850 + 0.300 i, i = 0..359 | per 4.2 | first/last gap to the pocket wall = 0.15 (a normal channel against the rim) |
| 4.9 | Fin lean | tip offset ≤ 0.05 from the root (≤ 1.4°) | - | skived curl; the tie braze straightens nothing |
| 4.10 | Fin root | skive fillet R 0.03-0.08, no cracks (E1 metallography, 10 fins per trial plate) | - | |
| 4.11 | Surface | as-skived, Ra ≤ 2.0 on the fin flanks; no smeared burr ≥ 15 µm at the tips after planing | - | |

**Skiving process specification** (prototype and volume are the same process; houses to qualify: two of Wieland/Kingka/Winshare/Nakamura class, no public data at this pitch found; CTX publishes Cu fin ≥ 0.08 mm, centre distance ≥ 0.16 mm, height 1-180 mm, so 0.15/0.30/2.0 is inside a current machine envelope):

| Parameter | Value | Note |
|---|---|---|
| Blade | 108.3 wide (pocket width minus 2 x 0.2 clearance), carbide, edge radius ≤ 5 µm, rake and clearance per the house's Cu recipe | fin length is set by the blade, not by the pocket |
| Stroke | 360 strokes at 0.300 feed per stroke, uncut chip 0.05-0.08 mm, cutting depth 1.00 below the pocket floor progressing to the fin-root plane | force 6.5-15.6 kN per stroke (`core_geom.out` §2) |
| Direction | strokes advance in +y from the pocket wall at y = -54.15; the last fin is formed at y = +53.85 with 0.15 to the far wall | blade protrusion from the holder must exceed the 1.0 mm pocket depth by ≥ 1.5 mm (house check) |
| Lubricant | water-miscible, chlorine-free; removed by alkaline clean + DI rinse within 4 h | braze wetting; ISO 16232 cleanliness later |
| In-process checks | pitch and thickness by vision on fins 1, 90, 180, 270, 360 (every plate); tip height by laser line (every plate); root cracks by section (one plate per lot) | Cpk ≥ 1.33 on thickness and pitch |
| Fallback B (if pocket skiving fails trials) | skive on a flat 4.0 blank without the pocket (fins 1.0 proud of the rim face) and braze a 1.0 mm OFE frame ring on the rim in the same cycle (+1 internal seam, +0.02 kg, +US$1-2) | E1 factor "pocket vs frame" |

## 5. Kerfs and edge channels

| # | Feature | Nominal | Tolerance | Basis |
|---|---|---|---|---|
| 5.1 | Interior kerfs | 13, at x_k = -54.000 + 7.7143 k, k = 1..13 (± 46.286 ... 0.000) | position ± 0.05 to B (pocket-referenced); width 0.30 +0.05/-0 | lines 1-13; k odd = inlet (7), k even = outlet (6) |
| 5.2 | Kerf depth | 1.925 from the planed tip plane | ± 0.025 -> floor 0.05-0.10 above the fin root (z 0.85-0.90) | architecture 5.1 stub; verify-mfg required change 5. Never into the base: hinge ≥ 0.80 |
| 5.3 | Kerf full-depth zone | |y| ≤ 48.1 (D 20 saw); arc ramp to zero depth at |y| = 54.0 | saw never touches the rim (y = ± 54.15) | verify-mfg #4: run-out 5.9 mm; thermal cost +0.014 K average (`core_geom.out` §3) |
| 5.4 | Edge channels (lines k = 0, 14) | x = ± 54.00 to ± 54.35 (0.35 wide), full fin height 2.0, floor = fin root (pocket floor) | width +0.10/-0 | half-line-flow outlets; formed by the two outer saw blades trimming the fin ends against the pocket wall |
| 5.5 | Kerf walls | fin end faces square to the base ± 0.03; burr ≤ 15 µm; no slivers | - | 10,080 cut sites per plate |
| 5.6 | Chip entrapment | ISO 16232 flush after de-waxing: no particle > 50 µm, ≤ 5 particles 25-50 µm per plate | - | 5.3 step 7 of the architecture; limit frozen at E1 |

**Kerf velocities** (18 LPM, 2.571 LPM per interior line): window 0.33 m/s; kerf top ≤ 1.3 m/s falling to zero at the floor (mean 0.66); edge channel 0.28 m/s; fin-gap bulk 0.198 m/s. The kerf is a distribution duct, not the fin entry; the ≤ 0.5 m/s fin-top cap is the single-cell CFD check of architecture 3.2, unchanged.

**Gang-saw process specification** (baseline; wire-EDM is excluded because a straight wire would slot the y-side rims under the skirt land):

| Parameter | Value | Basis |
|---|---|---|
| Support fill | water-soluble thermoplastic mounting wax (Aquabond 55/85 class, Tm 60-90 °C), vacuum-impregnated at 80-100 °C into the fin gaps, levelled flush with the tips | verify-mfg required change 5 (potted saw); fins backed against the 1.3-2.1 N tooth force |
| Blades | 15 micro-grain carbide slitting saws Ø 20 x 0.28 ± 0.005 x Ø 5 bore, 40 teeth, 8-10° rake, tooth run-out ≤ 0.01, on one arbor with ground spacers giving 7.7143 ± 0.003 pitch; the two outer blades sit at x = ± 54.175 (trim + edge channel) | 0.3 mm HSS/carbide saws are catalogue items at 63-80 mm; the 20 mm size is a standard slitting-saw diameter (run-out 5.9 vs 7.6 mm at D 32) |
| Cutting | Vc 150-250 m/min (2,400-4,000 rpm), fz 0.003-0.005 mm/tooth, vf 290-800 mm/min, single full-depth pass per kerf, conventional (up) cut, flood coolant compatible with the wax | tooth force 1.3-2.1 N < 1.4-5 N fin lateral capacity even unpotted |
| Depth control | arbor height set to the planed tip plane by touch probe on the rim top; depth 1.925 ± 0.025 | §4.7 coplanarity makes the rim a valid reference |
| De-wax and clean | 70-90 °C DI water + ultrasonic 10 min, two baths; alkaline clean; DI rinse; dry N2; residue check by water-break and FTIR swab (one per lot) | |
| Deburr | ultrasonic + 3-5 µm controlled electropolish (phosphoric) or 2 % citric/peroxide bright dip; burr ≤ 15 µm measured by optical profilometer on 3 kerfs x 5 fins per lot (sectioned coupon from a sacrificial plate per 500) | verify-mfg #3: bright dip alone removes 2-5 µm, so the burr limit is measured, not assumed |
| Prototype option | sinker-EDM the 30 ramp ends to full depth with a 0.28 Cu-W blade electrode (E1 factor: ramp vs full-depth) | |
| Sequence | skive -> wax -> gang-saw kerfs and edge trims -> plane tips and rim top (wax still in) -> de-wax -> clean -> deburr -> inspect -> braze | planing after sawing removes the exit burrs at the tips |

