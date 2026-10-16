# Gap fill: CoolIT 15 kW TTV footprint, heater map and thermocouple placement

Date: 2026-10-13. Scope: the CoolIT "Tech Brief: 15kW Coldplate" (June 2026) and what can be established about (a) the coldplate footprint and heated area, (b) the four-heater layout and power split, (c) which TC sits where, and (d) how the TCs are mounted.

Tags used: [Brief] = text of the tech brief; [Photo] = measurement on the three photographs embedded in the brief PDF; [D] = derived/calculated; [Sib] = taken from a sibling report (URL reused, not re-verified here); [KB] = general engineering knowledge of standard hardware, no URL.

## 0. Bottom line

1. **No public text source discloses the footprint, heater dimensions, power split or TC map.** The brief itself does not, and the sibling sweep (coolit-briefs-numbers.md, coolit-products.md) found no press, LinkedIn, Computex or patent source that does. **This task could run zero web searches**: the turn's shared WebSearch budget was already exhausted when this agent started (every call returned "budget used up"), and WebFetch/curl are blocked. The search list in Section 8 is therefore a to-do, not a done list.
2. **What is new here is a photogrammetric read of the brief's own photographs** (the only primary evidence). Three independent scale references (standard 12.7 mm worm-drive hose-clamp bands at both ends of the plate, the hose-barb size needed to pass 18 LPM, and the spring-screw heads) converge on a **coldplate body of about 140-145 mm square (range 120-165 mm), with a 24-25 mm wide centre manifold bar and eight mounting ears**. This is a much larger plate than any sibling assumed for the *heated* area.
3. **Heated area**: with four ceramic heaters inside a ~120-130 mm fin cavity and ceramic-heater flux limits of ~150-200 W/cm2 (the 4 kW TTV ran 160-200 W/cm2), the best estimate is **~100-145 cm2 (central ~120 cm2), i.e. ~105-150 W/cm2 (central ~125 W/cm2)**. Of the three calibrations in circulation, the **117 cm2 / 128 W/cm2** model calibration is the most consistent; **~100 cm2** is a plausible lower bound; the **61-79 cm2 / 190-250 W/cm2** estimate in coolit-briefs-numbers.md is the least consistent (it would require a 140 mm plate to overhang an 80 mm heater array by 30 mm per side, and ceramic heaters at 190-250 W/cm2 over 15 kW).
4. **TC placement**: the TCs are in the TTV, not the plate. The same TTV (with its eight TCs) was used for all three plates [Brief]; no TC leads are visible at the plate/TTV interface in either photo [Photo]. The only visible wiring is an 8-way lever terminal block on a PCB at the TTV's side fed by eight thick white high-temperature single leads, which is what four heaters x two power leads look like, not eight thermocouple pairs (16 terminals, colour-coded duplex wire). The TC leads therefore exit through the TTV body, consistent with TCs embedded in the heater stack from below/side and reaching the contact face ("directly at the heater surface" [Brief]). "Case" in the brief = heater top face under the paste, which is the same reference plane as an Intel/OCP-style groove-in-lid Tcase, but bead depth and ceramic material are unknown (0.5-4 K possible offset, Section 6).
5. **Heater map / TC5**: unresolved. The TC table itself gives two usable clues: (i) TC5 sits 12.0-12.4 K above the coolest positions (TC1, TC7), which equals the full split-flow per-pass fluid rise at 18 LPM (12.8 K PG25 / 12.1 K water) [D], so TC5 being an **outlet-edge position (far from the centre bar)** on an ordinary-flux heater explains the hot spot without any HBM/GPU power-split argument; (ii) grouping TCs as (1,2),(3,4),(5,6),(7,8) gives pair means 32.0 / 36.8 / 37.9 / 30.9 K, i.e. two "warm" heaters and two "cool" heaters, consistent with either an unequal power split or manifold maldistribution along the bar. The zoned-feed design rationale should therefore be stated as "removes the outlet-edge caloric/convective gradient" (robust) rather than "fixes the HBM zone" (unproven).

## 1. What the brief says (text only)

| Item | Value | Source |
|---|---|---|
| Heat load | 15 kW TDP from **four ceramic heaters** "simulating GPU and HBM zones" | [Brief] p.3 |
| TCs | eight, "placed directly at the heater surface, measuring case temperatures across the device footprint" | [Brief] p.3 |
| Samples | three coldplates, one TTV | [Brief] p.3-4 |
| Flow / inlet | 1.2 LPM/kW (= 18 LPM), 45 C inlet, water-glycol | [Brief] p.3 |
| Result | average dT 34.4 K; per-TC means 31.3 / 32.7 / 36.0 / 37.6 / 43.2 / 32.6 / 30.8 / 31.0 K | [Brief] p.4 |
| Footprint, heater size, per-heater power, TC map, TC method, dP | **not stated** | [Brief] |
| PDF author | Benjamin Sutton (CoolIT), file created 1 June 2026 08:10 UTC, Word 365 | PDF metadata |

The PDF author name is useful for the LinkedIn search in Section 8.

## 2. The photographs (primary evidence)

The PDF embeds three JPEGs (extracted to `docs/cooling/appendix/pdf/img/`, gridded crops alongside):

- **im-000** (p.1, 1053x902): coldplate mounted on the TTV, three-quarter view. Square copper plate; a raised centre bar (manifold) runs across the full plate with a hose barb at each end; black hose with worm-drive clamps at both ends; **eight spring-loaded Torx captive screws, four per side**, on ears at the corners and at ~1/3-2/3 positions; a square stainless/aluminium TTV top plate (chamfered corners, four Phillips screws) about 1.15-1.2x the copper plate; a black carrier block beneath it; on one side a red PCB carrying a **green 8-position orange-lever pluggable terminal block**.
- **im-001** (p.3, 821x785): same assembly, other side. **Eight thick white high-temperature single leads**, printed labels, enter the terminal block one per position. No other wiring visible.
- **im-002** (p.4, 538x587; shown rotated on the page): the bare coldplate, near-orthographic top view: square body, centre bar with a ridged barb at each end, eight mounting ears/holes.

What is *not* visible: the heater faces, the TIM joint, any TC lead at the plate edge, any fin geometry.

## 3. Photogrammetry: scale of the coldplate

Method: pixel extents by colour thresholding (copper vs background; grey metal for barbs) plus gridded crops; ratios taken within one image only; absolute scale from standard hardware whose size is fixed by convention [KB].

### 3.1 Ratios measured (dimensionless, [Photo])

| Feature | Measurement | Value |
|---|---|---|
| Plate width across the bar, im-002 | 377 px (far edge) to 396 px (near edge); mean 386 px | perspective +5 % far-to-near |
| Plate length along the bar, im-002 | 358 px (y 122-480) | foreshortened by camera tilt; plate is square to within ~10 % |
| Centre bar width, im-002 | 66 px (x 236-302) | **bar / plate = 0.171** |
| Barb ridge OD, im-002 | 33 px (far) / 36 px (near) | **barb / plate = 0.088-0.091**; barb bore/OD ~0.78 |
| Ear-hole spacing (1st to 4th hole), im-002 | 325 px of 358 px | holes at 0 / 0.31 / 0.62 / 0.91 of the side |
| Hose-clamp band width, im-000 | 40 px (far clamp), 48 px (near clamp) | band / hex-screw-head = 1.5-1.6 (standard-band clamp, not mini) |
| Bar width, im-000 | 77 px (far end), 93 px (near end) | same object as im-002 bar |
| Hose OD, im-000 | 60 px (far), 67 px (near) | hose / clamp band = 1.4-1.5 |
| Spring-screw head, im-000 | 43 px; plate side ~497 px (from ear spacing) | head / plate = 0.087 |
| Terminal-block pitch, im-000 | 24.6 px (8 levers, dimple to dimple); plate side ~507 px | pitch / plate = 0.049 |

### 3.2 Absolute scale by reference object

| Reference assumed | Basis [KB] | Plate body L |
|---|---|---|
| Worm-drive clamp band = 12.7 mm (SAE J1508 type F "standard" band; 8 mm mini bands have hex/band ~1.1, ours is 1.5-1.6) | bar = 24.4 mm (far) / 24.6 mm (near); L = bar/0.171 | **143 / 144 mm** |
| Hose barb: 1/2 in (ridge OD ~14.5 mm) / 12 mm metric (~13.5) / 3/8 in (~11) / 5/16 in (~8.5) | L = OD/0.09 | 161 / 150 / 122 / 94 mm |
| Hose OD from band: 1.45 x 12.7 = 18-19 mm | matches a 1/2 in ID hose with ~3 mm wall; a 5/16-3/8 in hose would be 12-16 mm | supports 1/2 in barb class |
| Spring-screw head: M6 pan 12 mm / M5 10 mm / M4 8 mm | L = head/0.087 | 139 / 116 / 92 mm |
| Terminal-block pitch 7.5 / 7.62 mm (lever-type, 24-32 A class) vs 5.0 / 5.08 mm (17.5 A class) | L = pitch/0.049, +4 % depth correction | 161-163 / 107-109 mm |

Hydraulic discriminator [D]: 18 LPM through a 5/16 in barb bore (~6 mm) is 10.6 m/s (59 kPa dynamic head per fitting), through 3/8 in (~7.3 mm) 7.2 m/s (27 kPa), through 1/2 in (~9.8 mm) 4.0 m/s (8 kPa). A demonstration rig would not be plumbed at 10 m/s; 4 m/s is normal. The heater-lead discriminator points the same way: if the 8-way block carries four 3.75 kW heaters (15.6 A each at 240 V), a 7.5 mm-pitch 24-32 A block fits, a 5 mm-pitch 17.5 A block is marginal.

**Consensus: two internally consistent scenarios exist, and the hydraulics and current ratings favour the large one.**

| Scenario | Clamp | Barb | Hose | Screw | Block pitch | Plate body |
|---|---|---|---|---|---|---|
| Large (favoured) | 12.7 mm band | 12-14.5 mm (1/2 in class) | 1/2 in ID | M6 | 7.5 mm | **140-150 mm** (clamp 143-144; barb 150-161; screw 139; block 161) |
| Small (disfavoured) | 8 mm mini band | 8.5 mm (5/16 in) | 5/16-3/8 in | M4 | 5.08 mm | 90-110 mm |

Adopted: **plate body 143 mm +/- 15 mm (120-165 mm) square**, centre bar 24-25 mm wide, barb ~13 mm OD, hose ~19 mm OD, TTV top plate ~165-175 mm square, copper plate height ~10-13 mm with the bar ~12-15 mm proud of the cover [Photo, D]. Confidence: medium on the large/small choice, low-medium on the +/-15 mm.

## 4. Heated area and heat flux (inference)

Constraints [D]:
- The four heaters sit inside the fin cavity; with 8 ears on the perimeter and a 24 mm bar, the cavity of a 143 mm plate is plausibly 115-130 mm square (130-170 cm2). The heater array cannot exceed this and would normally nearly fill it ("across the device footprint" [Brief]).
- Ceramic heater flux: commercial AlN thick-film heaters are rated to ~155 W/cm2 continuous (1,000 W/in2 class) [KB]; CoolIT's own 4 kW TTV ran a 50 x 50 mm plate at 160 W/cm2 (if 25 cm2 heated) to "shy of 200 W/cm2" (Tom's Hardware paraphrase) [Sib]. So the 15 kW array needs >= 75-100 cm2 and more plausibly 100-150 cm2.
- Demonstration logic: a plate sized 140 mm to cool an 80 mm heater array would be an odd choice; CoolIT's 4 kW plate was sized to its heater ("slightly smaller than a Blackwell GPU") [Sib].

| Candidate array | A (cm2) | q'' (W/cm2) | R''avg = 34.4/15000 x A | R''TC5 (43.2 K) | R''max (44.2 K) | Paste drop at 0.05 / 0.10 cm2K/W |
|---|---|---|---|---|---|---|
| 4 x 40x40 mm (sibling low case) | 64 | 234 | 0.147 | 0.184 | 0.189 | 11.7 / 23.4 K |
| 4 x 45x45 | 81 | 185 | 0.186 | 0.233 | 0.239 | 9.3 / 18.5 K |
| 4 x 50x50 | 100 | 150 | 0.229 | 0.288 | 0.295 | 7.5 / 15.0 K |
| 108 mm square (model calibration) | 117 | 128 | 0.268 | 0.337 | 0.345 | 6.4 / 12.8 K |
| 4 x 55x55 | 121 | 124 | 0.277 | 0.348 | 0.357 | 6.2 / 12.4 K |
| 4 x 60x60 | 144 | 104 | 0.330 | 0.415 | 0.424 | 5.2 / 10.4 K |
| 125 mm square (cavity-filling) | 156 | 96 | 0.358 | 0.449 | 0.460 | 4.8 / 9.6 K |

**Adopted benchmark basis: A_heated = 120 cm2 (+25/-20 cm2), q'' = 125 W/cm2 (105-150), R''avg = 0.275 cm2K/W (0.23-0.33), R''max = 0.355 cm2K/W (0.30-0.42), paste share at 0.05 cm2K/W about 6 K (18 %) of the 34.4 K.** This makes the benchmark's area-specific performance *worse* than the 4 kW plate's <= 0.225 cm2K/W max-basis figure [Sib], confirming test-metrics.md's reading that 15 kW is an area-and-flow scaling demonstration, not a lower unit resistance. It also lowers the modelled magnitude of the TIM lever (6 K rather than 9-12 K) and raises the share attributable to convection plus caloric rise.

## 5. Heater layout, power split and TC map: hypotheses tested against the table

Nothing in the brief or photos shows the heater faces. What the TC statistics support [D]:

1. **Caloric match.** Per split-flow half (7.5 kW at 9 LPM) the fluid rises 12.8 K (PG25) / 12.1 K (water). TC5 is 12.0 K above TC1 and 12.4 K above TC7 (and above the coolest position). A TC at the end of the fin pass (plate outer edge, farthest from the centre bar) on a heater of ordinary flux reproduces TC5's +8.8 K over the grand mean once the usual entrance-region enhancement near the bar is added (the sibling hotspot-smoothing model gets 5.7-8.4 K max-minus-mean from this mechanism alone). **No HBM/GPU power-split assumption is required to explain TC5.**
2. **Pair structure.** Treating TCs as two per heater in numbering order, pair means are (1,2) 32.0 K, (3,4) 36.8 K, (5,6) 37.9 K, (7,8) 30.9 K. Pair (3,4) is uniformly warm (+1.6, +3.2 K), pair (5,6) has one extreme and one normal reading (+8.8, -1.8 K), pairs (1,2) and (7,8) are uniformly cool. This is consistent with (a) two higher-power "GPU" heaters and two lower-power "HBM" heaters, or (b) equal heaters with the (3,4)/(5,6) side of the centre bar starved by manifold maldistribution along the bar (inlet at one end, outlet at the other). Mirror groupings ((1,5),(2,6),(3,7),(4,8): differences -12.0, +0.1, +5.2, +6.6 K) show no symmetric structure, so the TCs are probably not numbered as mirrored pairs across the bar.
3. **Plate 1 tilt.** Coldplate 1 reads 2.6-6.8 K *cooler* than plates 2/3 at TC1-TC7 but **10.1 K hotter at TC8**. A monotonic bond-line tilt (thin at one end, thick at the other) does this if TC1 and TC8 are at opposite ends of the array, so sequential numbering from one end to the other is the more likely scheme. Position x plate residual sd is 2.5 K with the single 8.6 K outlier at (TC8, plate 1) [D].
4. **Candidate heater maps** (all unproven): (A) 2 x 2 equal ceramic heaters, ~55 x 55 mm each, two on each side of the bar, flow outward from the bar to the plate edges, hottest points at the four outer edges; (B) two large "GPU" heaters flanking the bar plus two "HBM" strips at the outer edges, which would put the HBM zones at the end of the fin pass (the worst place, and the zone with the lowest Tj limit in a real package); (C) two GPU heaters on one side, two HBM heaters on the other. Under (A) and (C) the TC5 excess is a position effect; under (B) it is a position *and* zone effect. The uniformity KPI should therefore be defined as max-minus-power-weighted-mean *and* edge-minus-centre, so it is meaningful under any of the three.

## 6. Thermocouple mounting and the meaning of "case"

Evidence [Brief, Photo]:
- "placed directly at the heater surface" and "case temperatures" [Brief]; same TTV reused for all three plates.
- No TC leads emerge at the plate/TTV interface, plate edge or under the spring screws in either photo; the eight visible leads are heater-class white high-temperature wire into a single-row 8-way lever block (one lead per clamp). Eight TCs would need 16 terminals and would normally be colour-coded duplex wire. Conclusion: TC leads exit through the TTV body (base or far side), i.e. the beads are embedded in the heater stack and reach the contact face from below/side (drilled holes or grooves in the ceramic or in a thin metal spreader on it), or are the integral TCs some AlN heater vendors offer (bead ~0.5-1 mm below the face) [KB].

Implications [D]:
- Reference plane: the heater face under the paste is the same plane as an Intel/OCP-style groove-in-lid Tcase, so CoolIT's 34.4 K is *comparable in kind* to an OCP v1.0.0 case-to-inlet number, with the caveat that the heater face material and flatness differ from a nickel-plated copper lid.
- Bead-depth offset: at 125 W/cm2 a bead 0.5 mm below the face reads hotter than the face by 0.4 K in AlN (k ~170 W/mK) but by ~2.5 K in alumina (k ~25 W/mK); at 1 mm depth 0.7 K / 5 K. If CoolIT's beads are sub-surface in alumina, the true face-to-inlet dT could be 2-5 K lower than 34.4 K; if flush-mounted in grooves or in AlN, within ~0.5 K. The ceramic material is therefore the single most valuable unknown for comparability.
- Groove perturbation: a flush bead in a groove under paste locally thickens the TIM; this is common to Intel's method and OCP's recommended practice and does not bias the comparison.
- Equal-weight average: CoolIT's 34.4 K is an unweighted mean over positions; if two heaters carry more power, the power-weighted mean is higher (pairs (3,4)/(5,6) average 37.4 K vs 31.5 K for the others).

## 7. What this changes for the benchmark and the design case

| Quantity | Previous spread across reports | Adopt now | Confidence |
|---|---|---|---|
| Coldplate body | not estimated | ~143 mm square (120-165), bar 24-25 mm, 8 ears | medium |
| Heated area | 61-79 / ~100 / 117 cm2 | **120 cm2 (100-145)**; keep 117 cm2 calibration | medium-low |
| Mean heat flux | 128-250 W/cm2 | **125 W/cm2 (105-150)** | medium-low |
| R''avg incl. paste | 0.15-0.27 cm2K/W | **0.275 (0.23-0.33)** | medium-low |
| R''max (44.2 K) | 0.19-0.35 | **0.355 (0.30-0.42)** | medium-low |
| Paste share (0.05 cm2K/W) | 9-12 K | **~6 K (18 %)**; 12 K if 0.10 | medium-low |
| TC5 hot spot cause | HBM zone vs outlet edge | **outlet-edge/caloric position effect suffices**; zone effect possible, unproven | medium |
| "Case" reference | ambiguous | heater face under paste, TCs in TTV; possible +0.5 to +5 K bead-depth bias depending on ceramic | medium |
| Per-heater split | unknown | unknown; data hint at 2 warm + 2 cool heaters | low |

Design consequences: (1) the convection + caloric terms, not the paste, are the larger share at ~125 W/cm2, which strengthens the case for the manifold-microchannel / zoned-feed lever and slightly weakens the "TIM alone wins" story; (2) the competitor plate should be benchmarked on a 2 x 2 ceramic TTV of ~120 cm2 at 15 kW *and* on a die-realistic TTV, as test-metrics.md already proposes, with TTV-A's heater array set to ~110 x 110 mm rather than 108 x 108 mm only if the follow-up searches confirm a larger plate; (3) a 143 mm plate body implies CoolIT's "15 kW" plate is a Rubin-Ultra-class package footprint, not a Blackwell one, so application messaging should target 4-reticle-class packages.

## 8. Follow-up searches (not run; budget exhausted) and what each would settle

Run with WebSearch mode "extended" where marked:
1. `"CoolIT" "15kW" coldplate Computex 2026 booth` and `site:servethehome.com CoolIT 15kW`, `site:tomshardware.com CoolIT 15 kW cold plate 2026` (booth photos with a hand or a ruler in frame settle the scale).
2. `site:linkedin.com "Benjamin Sutton" CoolIT 15kW` (PDF author) and `site:linkedin.com CoolIT "15kW" "thermal test vehicle"` (extended).
3. `"CoolIT" "thermal test vehicle" ceramic heater "W/cm2" 2026` and `CoolIT Liquid Lab TTV "four heaters" HBM GPU` (extended).
4. `"CoolIT" 15 kW coldplate "mm" OR "cm2" footprint` (extended); `CoolIT 15kW coldplate pressure drop kPa`.
5. `CoolIT 4000W coldplate tech brief TTV heater size thermocouple groove` (the 4 kW brief R2 page 2 was never readable by the siblings; it likely shows the same TTV construction and TC method).
6. Google Patents: assignee "CoolIT Systems" 2025-2026, terms "thermal test vehicle", "plurality of heaters", "split flow" "manifold" (a 2025-26 filing may contain the heater layout drawing).
7. `OCP "Single-Phase Direct-to-Chip Cold Plate Test Specification" v1.0.0 thermocouple "case" groove` (exact Tcase definition; primary author is CoolIT per the siblings).
8. Watlow Ultramic / AlN heater max W/cm2 datasheet (bounds the heater area from the flux side).

## Sources

Primary:
- CoolIT Systems, "Tech Brief: 15kW Coldplate", June 2026 (PDF author Benjamin Sutton, created 2026-06-01). Local copy: `docs/cooling/appendix/pdf/brief.pdf`; extracted photos and gridded crops in `docs/cooling/appendix/pdf/img/` (im-000/001/002, grid-*, crop*-*.png); measurement scripts in `.../pdf/tools/`. Publisher site: https://www.coolitsystems.com/coldplate-technology/ (not fetched).

Reused from sibling reports (URLs as recorded there; not re-verified in this task):
- CoolIT 4 kW coldplate PR (13 Mar 2025): https://www.prnewswire.com/news-releases/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership-302401512.html
- CoolIT 4 kW Technical Brief R2 (14 Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- Tom's Hardware, data-center cooling state of play 2025 ("shy of 200 W/cm2"): https://www.tomshardware.com/pc-components/cooling/the-data-center-cooling-state-of-play-2025-liquid-cooling-is-on-the-rise-thermal-density-demands-skyrocket-in-ai-data-centers-and-tsmc-leads-with-direct-to-silicon-solutions
- Tom's Hardware, 4 kW plate: https://www.tomshardware.com/pc-components/liquid-cooling/coolit-unleashes-4kw-single-phase-dlc-cold-plate-seemingly-timed-for-nvidia-blackwell-ultra-chips
- OCP L-L CDU test methodology r1: https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/

General hardware references used for scale [KB, no URL]: SAE J1508 worm-drive clamp band widths (12.7 mm standard, 8 mm mini); hose-barb ridge diameters by nominal size; PCB lever terminal-block pitches (3.5 / 5.0 / 5.08 / 7.5 / 7.62 mm) and current classes; metric pan/button-head screw head diameters; AlN thick-film ceramic heater continuous flux ratings (~155 W/cm2 class); thermal conductivity of AlN (~170 W/mK) and alumina (~25 W/mK).

## Gaps / unknowns

1. **No web search was possible in this task** (shared per-turn budget exhausted before the first call; WebFetch/curl blocked). Section 8 lists what to run. All footprint numbers are photogrammetric inferences from three small JPEGs, not disclosed values.
2. The large-vs-small scale scenario rests on identifying the hose clamps as standard 12.7 mm-band types and the barbs as 1/2 in class; if CoolIT used mini clamps and 5/16 in barbs at 10 m/s, the plate is ~90-110 mm and the heated area ~60-80 cm2. Judged unlikely (hydraulics, lead current), not excluded.
3. Heater dimensions, per-heater power, ceramic material (AlN vs alumina), heater face finish/flatness, and whether a metal spreader sits between heaters and paste: all unknown.
4. TC map (which TC on which heater, centre vs edge), TC type, bead depth, groove vs integral, extrapolation to the face: all unknown; only the lead-routing inference (TCs in the TTV) is evidence-based.
5. Whether the 8-way block is heater power (favoured) or a common-return TC scheme: not confirmed.
6. Flow topology inside the bar (inlet distribution slot vs outlet collection) is assumed from CoolIT's Split-Flow description; the outlet return path (edge collectors back to the bar's second barb) is inferred, not seen.
7. Plate 1's TC8 outlier is attributed to bond-line tilt; a damaged or mis-seated TC8 bead on that run cannot be excluded.
8. The OCP v1.0.0 Tcase definition text was not retrieved by any report; comparability is argued from the physical reference plane, not the spec wording.
