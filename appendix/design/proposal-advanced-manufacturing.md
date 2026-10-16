# AM-Gated HMMC: a digital-laminate manifold micro-channel cold plate that uses additive manufacturing only where it earns its place (key: advanced-manufacturing)

Architecture proposal, 2026-10-13. Benchmark: CoolIT 15 kW Split-Flow plate (18 LPM PG25, 45 C; 34.4 K average / 44.2 K maximum case-to-inlet; paste; dP undisclosed, reconstructed 24.6 kPa, band 17-42). Numbers come from the project scoping model (`coldplate_model.py`, corrected per `SYNTHESIS-physics.md`), extended in `design/am/am_run.py`, `am_extra.py` and `am_xseg.py` (outputs `am_run.out`, `am_extra.out`, `am_points.out`, `am_xseg.out`). Terms are +/-25 %; P10-P90 bands are a 20k-sample Monte Carlo; costs are KB-M/KB-L estimates for RFQ.

## 1. Concept in one page

**Verdict.** Additive manufacturing does **not** belong in the volume thermal core. The reason is physical, not commercial:

1. **Fouling, not resolution, sets the channel.** A 10-year drop-in plate needs 0.15 mm gaps or more behind a 50 um absolute screen. ECAM's 30-50 um features cannot be deployed.
2. **At 0.15 mm, copper fins are near their ceiling.** No straight copper fin geometry can exceed **h_eff 138 kW/m2K**. Skiving already reaches **127 (92 %)**. The best printed-fin variant gains **0.3 K**. Pins and offset strips lose 0.9-2.0 K.
3. **Coarse printing loses outright.** L-PBF needs channels of at least 0.4 mm, gives Ra 10-20 um and k of about 340 W/mK; binder jet reaches only 93-97 % density. L-PBF fin, L-PBF gyroid and binder-jet cores land at **40.2-62.6 K**, worse than CoolIT. A vapor-chamber base costs **+9 K**.

Advanced manufacturing earns three places:

- **in design:** topology-optimised manifold trees, rendered as a *digital laminate* of etched and laser-cut copper sheets;
- **in development:** printed manifolds give TTV data in month 3 and 1-3-week design iterations, versus 10-12 weeks for bonded prototypes;
- **in two gated product slots:**
  - **(X)** a CTE-matched die module for 350 W/cm2 and >30 kW: ECAM copper fin strips on Cu-diamond under a MoCu cap, with soldered indium TIM1;
  - **(S)** L-PBF copper manifold shells for non-planar SKUs below about 2k/yr.

**What we ship.** An all-OFE-copper hierarchical manifold micro-channel (HMMC) plate: a skived fin field (0.10 mm fins, 0.15 mm gaps, 2.0 mm tall, 1.0 mm base) under a 9-11-sheet laminate (tie grate bonded to 50 % of every fin tip, 1.5 mm plenum, power-map comb, 28 slots each cut into four 27 mm centre-fed segments, 2-level tree, cover), diffusion-bonded in one vacuum cycle. Nothing in the bill of materials is printed.

| 15 kW, 18 LPM, 45 C, 117 cm2 | CoolIT | ours, same paste | **Tier 1 PCM (design of record)** | Tier 2 liquid metal | X module, LM, <= 33 um loops |
|---|---|---|---|---|---|
| avg case-to-inlet | 34.4 K | 30.0 K | **28.0 K (25.7-31.4)** | 22.9 K | 19.8 K |
| max case-to-inlet | 44.2 K | 35.0 K | **31.1 K (28.7-34.5)** | 25.0 K | 21.9 K |
| plate dP incl. screen | n/d (est. 24.6) | 5.7 kPa | **5.7 kPa (4.5-7.2)** | 5.7 kPa | 6.1 kPa |
| pump power | ~7.4 W | 1.7 W | **1.7 W** | 1.7 W | 1.8 W |
| Q at Tcase,max <= 85 C | ~12.7 kW | 18.4 kW | **21.6 kW** | 29.7 kW | 38.2 kW |

**Five decisive differentiators.**

1. **4 mm flow length with a power-map comb.** Convection falls from 12.6 to 10.1 K, the flow-driven hot spot from 8.8 to 1.5 K, and dP from about 24.6 to 5.7 kPa.
2. **Digital-laminate manifold.** We get AM-style freedom from PCB-industry capacity, with no powder.
   - Four-segment centre-fed slots give an **18 mm** core height (target 17-19 mm), versus 21 mm for a 2.5-D CNC block and about 30 mm for design H.
   - A new power map is a new comb artwork in 2 weeks.
3. **Tied sandwich.** There is zero pressure bow and the face is flat to 15-25 um, so PCM and liquid metal hold their datasheet values.
4. **Printed development loop.** Printed manifolds on skived cores give calibrated TTV data before any bond tooling exists.
5. **Gated X module.** At 350 W/cm2 the die top runs at **82 C**, versus 90-93 C for conventional soldered lids on the same fins. That equals bare-die liquid metal, with a soldered, field-proven TIM1.

**Honest framing.** With CoolIT's paste we win by 4.4 K (average) and 9.2 K (maximum). **AM itself adds 0-0.3 K at the TTV point**; its value is height, development speed and the 350 W/cm2 slot.

## 2. Thermal core

### 2.1 Geometry of record

| item | value | consequence |
|---|---|---|
| fins (R core) | skived OFE C10100, t 0.10, gap 0.15, H 2.0 mm, along x | h 13.2 kW/m2K, eta 0.56, h_eff 127 (92 % of the 138 ceiling) |
| base | 1.0 mm as bonded, >= 0.8 mm finished under the die; 1.5-2 mm at the land | 3.3 K at 128 W/cm2 |
| flow length / slot pitch | 4 / 8 mm (die zone of real packages 5 / 10 mm) | u 0.083 m/s, Re 19, x* 0.08, friction 0.23 kPa |
| P core (filtration-gated) | 0.10 / 0.10 x 1.5 mm | h_eff 187 (90 % of the 207 ceiling); needs <= 33 um absolute loop filtration |

### 2.2 Flow path and zoning

The coolant path is:

1. port and 50 um absolute screen;
2. perimeter loops in the ear bosses;
3. four inlet branches (10 x 7.5 mm) interleaved with four outlet branches (15 x 7.5 mm), each fed from both ends at <= 0.5 m/s;
4. etched window, then a slot segment (3.3 x 2.0 x 27 mm, centre-fed);
5. comb (0.5 mm holes, 1.2 m/s), plenum and grate;
6. 4 mm of fin each way, then back up the mirror path.

Zoning is purely comb artwork. For the 2027-28 package (4 x 26 x 33 mm dies at 350 W/cm2 plus 16 HBM):

- the die block (34 cm2) gets about 90 % of the flow;
- HBM gets 6-8 %;
- the margin gets 2 %.

HBM is never downstream of a die. A stepped copper pedestal, machined after bonding (+/-0.05 mm), reaches the HBM plane. Un-zoned, the plate loses 15 K at the hot die.

### 2.3 Interface strategy by tier

| tier | package | interface | R'' cm2K/W | retention |
|---|---|---|---|---|
| 1 drop-in, serviceable | lidded | PCM pad (PTM7950 class) on lapped bare Cu | 0.055 | 20-30 psi |
| 2 OEM co-design | lidded, Ni lid | Ga-In LM, dam, 20-30 um BLT, 3-5 um Ni on the face only | 0.015 | 10-20 psi |
| 3A chip co-design (conventional) | bare die | LM on a 0.8 mm Cu pedestal | 0.015 | <= 0.3 MPa on die |
| **3X X module (gated)** | micro-channel lid soldered to dies | indium TIM1, 79-88 um | 0.011 | reflow 157 C |

Grease is never used on lids of 100 mm or more: its bow and ageing tails produced CoolIT's 10 K plate-to-plate spread.

The indium bond line scales with CTE mismatch (`am_extra.out` section 4):

- a copper lid needs about 259 um (0.032 cm2K/W, 11.2 K at 350 W/cm2);
- a 7 ppm/K lid needs 79-88 um (0.011-0.012, 3.9-4.3 K).

### 2.4 What each advanced process buys, with its penalties

**Fin-conduction ceiling.** Maximum h_eff for straight plate fins at a fixed gap, any thickness and height (`am_run.out` section 1):

| gap | Cu 390 W/mK | ECAM Cu 370 | L-PBF Cu 340 | skiving achieves |
|---|---:|---:|---:|---|
| 0.10 mm | 207 kW/m2K | 202 | 194 | 187 (P core) |
| 0.15 mm (drop-in floor) | 138 | 134 | 129 | 127; 135 at H 3 mm |
| 0.40 mm (L-PBF limit) | 53 | 52 | 50 | - |

**Route screen.** At 15 kW / 128 W/cm2, and at the 350 W/cm2 reticle die (hottest die, LM):

| route | avg / max dT at TTV | delta | 350 W/cm2 die | adder at 100k/yr | verdict |
|---|---|---|---|---|---|
| skived R core + digital laminate | 28.0 / 31.1 K (PCM) | ref. | 48.3 K (93 C) | ref. | **volume baseline** |
| ECAM fins at 0.15 mm, same geometry / near-ceiling 0.12 x 3.0 mm | 28.2 / 31.2 ; 27.7 / 30.7 | +0.2 / -0.3 K | 47.2 K | +13 to +63 | second source only |
| ECAM offset strips (1 mm) / micro-pins d 0.15 (eta 0.41) | 28.9 / 31.9 ; ~30.1 | +0.9 / +2.0 K | - | +13 to +63 | rejected |
| L-PBF Cu fins 0.40/0.25 x 3 (Ra 10-20 um, k 340) | 48.9 / 51.9 | +20.9 K | - | +279 (manifold alone) | rejected |
| L-PBF gyroid (Nu x1.8, f x3.9): in manifold / monolith split-flow | 40.8 / 43.8 ; 40.2 / 48.0 at 16.7 kPa | +12-13 K | - | +60 to +310 | rejected |
| binder-jet Cu 0.50/0.40 x 3, k 328 | 62.6 / 65.6 | +34.6 K | - | parity | rejected |
| 1 mm Cu-diamond base (k 600) under the R core | 21.8 / 23.9 (LM) | -1.1 K | 46.2 K | +117 to +277 | only inside X |
| CVD diamond 0.5 mm insert + braze 0.005 | 22.3 / 24.4 (LM) | -0.6 K | 37.9 vs 39.4 K (P core) | +300 to +1,000 | only <= 2 cm2 hot spots |
| vapor-chamber base (0.08 cm2K/W) | 31.9 / 34.0 (LM) | **+9.0 K** | 63.8 K (109 C) | +10 to +25 | rejected |
| **X: segmented ECAM 0.10 strips on Cu-diamond, MoCu cap** | 19.8 / 21.9 (LM) | -0.4 K vs P core | 38.5 K (84 C); soldered lid 37.1 K (82 C) | +117 to +277 | **gated Tier 3X / >30 kW** |

**Where diamond does matter: the sub-die hot spot.** For a 2 x 2 mm patch at +650 W/cm2 on a 350 W/cm2 die (axisymmetric finite volume), copper gives a 27.7 K peak excess; Cu-diamond is 5.3 K lower, CVD diamond 11.9 K lower and CuW 14.6 K higher. That justifies diamond in the die module and laser/RF niches, not in the 117 cm2 plate.

Printed-copper conductivity is a weak lever: going from 390 to 300 W/mK costs only +0.9 K.

## 3. Hydraulic architecture

| level | element (18 LPM) | section | velocity | rule |
|---|---|---|---|---|
| L0 | 16 mm horizontal ports in 21 mm ear bosses (20 mm option) | 201 mm2 | 1.49 m/s | <= 1.5 m/s Cu |
| L1a | perimeter loops 10 x 15 inlet / 10 x 22 mm outlet | 150 / 220 mm2 | 1.0 / 0.68 m/s | headers <= 1.0 |
| L1b | 4 + 4 interleaved branches (10 / 15 x 7.5 mm), both-end fed | 75 / 113 mm2 | 0.50 / 0.33 m/s, head 126 Pa | branch/head 17 >= 6 |
| L2 | 112 slot segments 3.3 x 2.0 mm, centre-fed | 6.6 mm2 per half | <= 0.5 m/s | >= 15x slot head |
| L3 | comb, about 1,300 holes of 0.5 mm | - | 1.2 m/s | 2.0 kPa, inertial |
| L3' | plenum 1.5 mm + 50 %-open grate | - | 0.12 m/s | <= 0.5 m/s |
| L4 | 0.15 mm gaps x 4 mm, 12,100 parallel segments | - | 0.083 m/s | 0.23 kPa |

Each stage is more than twice the width of the next (16 > 10 > 3.3 > 0.5 > 0.15 mm), so nothing sieves upstream of the channels.

**dP budget** (port-to-port, PG25, 45 C; MC P10-P90 4.5-7.2 kPa at 18 LPM):

| flow | channel + turns | tree | comb | ports | screen | **total** | pump |
|---|---:|---:|---:|---:|---:|---:|---:|
| 18 LPM, 16 mm ports | 0.24 | 0.50 | 2.00 | 2.57 | 0.40 | **5.7 kPa** | 1.7 W |
| 18 LPM, 20 mm ports | 0.24 | 0.50 | 2.00 | 1.05 | 0.40 | 4.2 kPa | 1.3 W |
| 36 LPM, 16 mm ports | 0.5 | 2.0 | 8.0 | 10.3 | 1.6 | **22.4 kPa** | 13.4 W |
| 36 LPM, 20 mm ports | 0.5 | 2.0 | 8.0 | 4.2 | 1.6 | 16.3 kPa | 9.8 W |

**Ratings.** At 36 LPM, 16 mm ports reach 2.98 m/s (above the copper erosion limit), so 2x needs 20 mm bores (1.91 m/s) or 316L stubs. LP15 (15 mm core) uses a 5 mm tree (0.75 m/s) and a 3.0 kPa comb: 6.5 kPa at 18 LPM, 25.6 kPa at 36 LPM.

**Uniformity.** The branch is 90 % inertial, so uniformity does not degrade with flow. Target max/min <= 1.10 (1.5 K hot spot; 2.5 K at +/-20 %), unverified until experiment 1.

**Couplings.** A UQD08 pair costs about 25 kPa at 18 LPM, four times the plate. Specify UQD12-class or 3/4 in lines (about 5 kPa) at 15 kW; UQD08 suits Rubin-class plates (plate 0.3 kPa).

**Filtration and fouling.**

- Gap >= 3x the absolute rating of the last filter.
- Integrated 50 um absolute pleated 316L screen, >= 12 cm2, alarm at +2 kPa.
- 5 % slot-end bleed through 0.6 mm orifices (+0.4 K).
- The P core and X module need <= 33 um absolute loop filtration.

**AM contamination rules.** No L-PBF or binder-jet wetted part upstream of a fin core: 15-45 um satellites bridge 0.10-0.15 mm gaps, and as-built channels are Ra 3-50 um. Printed rig manifolds are chemically polished, flushed to ISO 16232 and followed by a 25 um filter. ECAM parts are rinsed, checked by ion chromatography (< 1 ug/cm2) and annealed.

## 4. Mechanical and construction

**Stack-up, digital-laminate (DL) chassis, 15 kW class, 18 mm core:**

| # | layer | t mm | process | function |
|---|---|---:|---|---|
| 0 | base + fins | 1.0 + 2.0 | skived OFE Cu | fin field; pedestal machined after bonding |
| 1 | tie grate | 0.5 | photo-etched | bonds 50 % of each fin tip |
| 2-3 | plenum | 1.5 | 2 etched sheets | spreads jets over 432 gaps per slot |
| 4 | comb | 0.4 | etched | metering and zoning artwork |
| 5-6 | slot segments | 2.0 | 2 etched sheets | 112 centre-fed segments |
| 7 | window sheet | 0.6 | etched | segment feeds/returns |
| 8 | feed tree | 7.5 | waterjet/CNC through-cut plate or 3 laser-cut sheets | interleaved branches, 8 mm posts, ear loops |
| 9 | cover | 2.0 | Cu plate | closes the tree |

**Joining.** One-shot vacuum diffusion bond of OFE C10100/C10200 (850-950 C, 5-10 MPa, 1-4 h, no H2): printed-circuit heat-exchanger practice, and what Alloy Enterprises markets as "Stack Forging" for AI copper DLC. No filler, no dissimilar metal; strength designed to annealed OFHC (yield 70 MPa). Fallback: the 2.5-D CNC block (21 mm). Acceptance: 100 % He <= 1e-5 mbar L/s (target 1e-6), C-scan tip bond >= 50 %, first-article CT.

**Base thickness logic.** Tied fin tips leave the base with negligible pressure stress; finishing, erosion and skive tolerance set 1.0 mm (0.8 mm minimum under the die). Each extra mm costs +9 K at 350 W/cm2.

**Pressure.** MAWP 1.0 MPa, proof 1.5, design burst >= 3.0 (above OCP's > 20 bar example), qualification burst >= 4.5 MPa; tie stress at burst 15 MPa (SF 4.7); land <= 4 mm unsupported (SF 5.8); vacuum-stable to -0.9 bar(g).

**Flatness and mounting.** Lapped to <= 15 um over the die and <= 25 um over 100 mm (Ra <= 0.4 um); springs bear within 10 mm of the die edge; 20-30 psi (PCM) or 10-20 psi (LM).

**Envelope and mass.**

| variant | body | height | mass |
|---|---|---|---|
| 15 kW class | 148 x 152 mm | 18 mm core (17-19); 21 mm port bosses | ~1.8 kg |
| 2.5-D fallback | 148 x 152 mm | 21 mm | 2.3 kg |
| Rubin class | 110 x 120 mm | 14-16 mm | ~0.9 kg |

These figures are CFD-gated targets.

**X module construction** (`am_extra.out` sections 2-3). Cu-diamond (7 ppm/K) cannot simply be joined to copper (17 ppm/K); every obvious approach blows the 15-25 um flatness budget:

- diffusion-bonded into a Cu frame: 264 um of mismatch over 30 mm;
- Ag-sinter rim: 69 um;
- continuous ECAM fins: 215 um of bow at -40 C (133 um in operation);
- printed Cu walls: 189 um.

The module is therefore CTE-matched throughout:

1. 1.0 mm Cu-diamond base (k 550-600 W/mK, 30 um Cu skins) as the substrate.
2. ECAM prints room-temperature copper **strips** (0.10/0.10 x 1.5 mm, 2 mm long, 0.2 mm breaks). These carry no long-range stress and cost +0.4 K at TTV and +1.3 K at 350 W/cm2.
3. Mo70Cu30 cap, joined at <= 300 C (Ag sinter or Cu-Sn TLP) through a segmented printed grate.
4. Indium solder to the dies.

The X module is a lid supplied with the package. It is never a plate SKU.

## 5. Manufacturing route at volume

**Process chain** (all conventional; capacity in TW/VN/MX/EU):

1. Skive (108 mm wide, 2-5 min); CNC-thin the base.
2. Photo-etch 0.4-0.75 mm OFE sheets (phototools US$0.5-3k; +/-25 um).
3. Waterjet the tree plate; lap the cover.
4. Clean, deoxidise, stack on dowels (+/-0.05 mm).
5. Diffusion bond (50-200 plates per 8-12 h cycle).
6. Lap the face, machine the pedestal, Ni for Tier 2.
7. Screen, ISO 16232 flush, 100 % He and dP signature (5.7 +/-0.6 kPa).

**Unit factory cost** (basis: `manufacturing-cost.md`, `gap-cost-volume-and-market-anchors.md`, `proposal-hmmc-elite.md` line items; KB-M):

| line item | 10k/yr | 100k/yr |
|---|---:|---:|
| OFE Cu incl. swarf | 26 | 24 |
| skived core | 40 | 24 |
| laminate set incl. tree plate (2.5-D route: laminates + CNC block 116 / 50) | 105-125 | 45-60 |
| cover, stubs | 14 | 6 |
| diffusion bond | 55 | 32 |
| screen, plugs | 15 | 8 |
| lapping, inspection | 12 | 6 |
| load frame | 20 | 14 |
| He leak + flow test | 8 | 5 |
| **15 kW class incl. 12 % yield/overhead** | **~US$343 (+/-10)** | **~US$189 (+/-10)** |
| Rubin class (110 x 120 mm) | ~US$240 | ~US$134 |

A GB200-class skived plate costs about US$170 / US$105 to make. Our plate adds US$30-85 and stays under the US$300-400 Group-A ASP.

**Advanced routes: cost and throughput** (`am_run.out` section 9, `am_points.out`):

| route | 10k/yr | 100k/yr | time / part | tools per 100k/yr | note |
|---|---:|---:|---|---|---|
| ECAM full fin field (12 cm3) | 159 | 37-87 (vs US$24 skived) | 0.6-2.4 h at an assumed 5-20 cm3/h | 10-40 | rate and price unpublished |
| X module (Cu-diamond 40 cm2 + 4 cm3 ECAM + MoCu cap) | 253-573 | +117-277 | 0.27-0.8 h | 1-2 at a realistic 10k/yr | Cu-diamond US$2-12/cm2 [KB-L] |
| L-PBF Cu manifold (~105 cm3) | ~700 | ~324 (+279) | 2.1-7 h | **35-117 machines (US$35-175 M)** | vs 2-3 bond furnaces (US$3-6 M) |
| binder-jet Cu manifold + sinter/HIP | 60-120 | 30-60 | - | - | 15-20 % shrink, 93-97 % dense |
| CVD diamond 34 cm2 x 0.5 mm | 340-1,700 | 300-1,000 | - | - | US$10/cm2 to US$1/mm3 |
| dev: L-PBF test manifold / clear SLA | 600-1,200 / 80-200 | - | 3-7 days | - | development only |

**Lead time.**

- Printed test articles: 2-3 weeks.
- First bonded plates: 8-12 weeks.
- 100k/yr capacity: 9-12 months, gated by furnaces.

**Yield risks, ranked.**

1. Unbonded tip or rim (sheets flat to < 10 um; C-scan; He).
2. Registration.
3. Pre-bond fin damage.
4. Thin-sheet warpage.
5. X only: strip-root adhesion and Cu-skin delamination.

## 6. Predicted performance vs benchmark

### 6.1 Benchmark point (15 kW, 18 LPM PG25, 45 C, 117 cm2, 128 W/cm2)

| design | cal | TIM | base | conv | avg dT | max dT | R'' | dP kPa | pump W | Q cap kW | Tcase,max |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---|---:|
| CoolIT-like reconstruction | 6.3 | 9.0 | 6.6 | 12.6 | 34.5 | 44.3 | 0.269 | 24.6 | 7.4 | 12.7 | 89 C |
| DL R, same paste | 7.6 | 9.0 | 3.3 | 10.1 | 30.0 | 35.0 | 0.234 | 5.7 | 1.7 | 18.4 | 80 C |
| **DL R, PCM (Tier 1)** | 7.6 | 7.1 | 3.3 | 10.1 | **28.0 (25.7-31.4)** | **31.1 (28.7-34.5)** | 0.219 | **5.7 (4.5-7.2)** | 1.7 | **21.6 (18.3-24.3)** | **76 C** |
| DL R, LM (Tier 2) | 7.6 | 1.9 | 3.3 | 10.1 | 22.9 (21.7-24.8) | 25.0 (23.8-27.0) | 0.179 | 5.7 | 1.7 | 29.7 (26.8-32.9) | 70 C |
| DL P, LM (<= 33 um) | 8.2 | 1.9 | 3.3 | 6.8 | 20.2 (19.2-21.9) | 22.3 | 0.158 | 5.8 | 1.7 | 37.0 | 67 C |
| X module (segmented strips), LM | 8.0 | 1.9 | 2.3 | 7.5 | 19.8 (18.7-21.4) | 21.9 (20.8-23.6) | 0.154 | 6.1 | 1.8 | 38.2 (33.8-43.1) | 67 C |

### 6.2 Other operating points (Tier 1 PCM / Tier 2 LM)

| condition | flow | avg dT | max dT | dP | pump |
|---|---:|---|---|---:|---:|
| 0.75 LPM/kW (Nvidia 45/65 C) | 11.2 LPM | 33.8 / 28.7 K | 36.8 / 30.8 K | 2.3 kPa | 0.4 W |
| 2x flow | 36.0 | 23.6 / 18.5 | 26.7 / 20.6 | 22.4 (16.3 w/ 20 mm) | 13.4 |
| equal pump power (7.4 W) | 29.4 | 24.6 / 19.5 | 27.6 / 21.6 | 15.0 | 7.4 |
| CoolIT's 34.4 K average reached at | 10.9 / 8.4 | 34.4 | 37.4 / 36.5 | 2.1 / 1.3 | 0.39 / 0.18 |
| 50 C inlet | 18 | - | Tcase,max 81.1 C | 5.7 | 1.7 |

### 6.3 Real 2027-28 package (4 x 26 x 33 mm dies at 350 W/cm2 + 16 HBM, zoned; hottest-die case-to-inlet)

| construction | PCM | LM | Tcase,max LM | soldered micro-channel lid, die top |
|---|---:|---:|---:|---|
| CoolIT-like split-flow (heat-map run) | 88.6 K (paste) | ~76 K | ~121 C | - |
| DL R core, Cu | 62.3 | 48.3 | 93 C | 54.2 K (99 C), In 0.032 |
| DL P core, Cu (<= 33 um) | 53.4 | 39.4 | 84 C | 45.4 K (90 C), Cu lid + thick In |
| P core on CuW / MoCu (conventional CTE-matched) | 62.9 / 60.4 | 48.9 / 46.4 | 94 / 91 C | 47.8 / 45.3 K (93 / 90 C) |
| bare-die LM on 0.8 mm pedestal, R / P (Tier 3A) | - | 46.5 / 37.6 | 92 / 83 C | - |
| **X module (segmented strips, Cu-diamond)** | 52.5 | 38.5 | 84 C | **37.1 K (82 C)**, In 0.011 |

HBM on the stepped pedestal: Tj 84-91 C, versus 105 C on the split-flow plate. On-die 2-3x hot spots add 5-15 K to every path; Cu-diamond recovers 5.3 K of that, CVD diamond 11.9 K.

### 6.4 GPU-class and beyond-15 kW plates (avg / max dT)

| case | CoolIT-like | DL R, PCM | DL R, LM | X, LM | dP CoolIT-like / DL |
|---|---|---|---|---|---|
| Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW | 16.1 / 23.5 K | 18.4 / 20.3 | 16.9 / 18.5 | 16.5 / 18.2 | 2.0 / 0.1 kPa |
| Rubin 2.3 kW, 60 cm2, 1.2 LPM/kW | 14.8 / 22.2 | 16.0 / 17.9 | 14.4 / 16.1 | 14.0 / 15.7 | 2.5 / 0.2 |
| Rubin Ultra 3.6 kW, 80 cm2, 1.0 LPM/kW | 17.6 / 25.1 | 19.1 / 21.1 | 17.3 / 19.0 | 16.7 / 18.4 | 3.3 / 0.3 |
| CoolIT 4 kW point, 25 cm2, 1.5 LPM/kW | 40.0 / 50.7 (recon.; measured max < 36) | 31.0 / 34.4 | 24.6 / 26.8 | 20.0 / 22.3 | 6.2 / 1.0 |
| 25 kW on 117 cm2 | - | 40.9 / 44.9 | 32.3 / 34.8 | 26.7 / 29.2 | - / 15.6 |
| 30 kW on 150 cm2 (Q cap) | - | 38.8 / 42.6 (27.5 kW) | 30.8 / 33.2 (38.7 kW) | 25.6 / 28.0 (49.8 kW) | - / 22.3 |
| wafer-scale 20 kW, 460 cm2, tiled ports | - | 16.5 / 18.5 | 14.8 / 16.5 | 14.2 / 15.9 (not needed) | - / 9.8 |

### 6.5 Where it does not win

1. **Low-flux GPU lids (38-45 W/cm2):** the Tier 1 *average* is 1.2-2.3 K worse than split-flow (isothermal caloric penalty); we win the maximum by 3-4 K, uniformity and dP.
2. **AM at the benchmark point** contributes nothing measurable (ECAM -0.3 to +0.9 K; Cu-diamond -1.1 K for more than US$100).
3. **R core at 350 W/cm2** misses 85 C even with LM (93 C); 82-84 C needs the P core or X, both with 33 um loops.
4. **X only ties bare-die LM** (82 C soldered vs 83 C) and, as a plate with LM, ties the P core (84 C); its case is a soldered TIM1.
5. **dP** is compared against a reconstruction.
6. **18 mm / 1.8 kg are targets**; on the fallback (21 mm, 2.3 kg) we are probably no better than the benchmark.

## 7. Product family and applications

| product | core / process | interface | what changes |
|---|---|---|---|
| DL-15 (15-30 kW, Rubin Ultra/Kyber class) | R (P option) | PCM / LM | UQD12-class couplings; 20 mm ports above 25 kW |
| DL-GPU (1.8-3.6 kW) | R | PCM / LM | 110 x 120 x 14-16 mm, 12 mm bores, UQD08 |
| DL-CPU / NVSwitch / NIC | R, 1.5 mm fins | PCM | 60-80 x 80 mm, 12 mm high |
| **X module (gated)** | ECAM strips on Cu-diamond, MoCu cap | indium TIM1 | lid partner; 350 W/cm2 dies, > 30 kW |
| wafer-scale / multi-chip (43 W/cm2, 460 cm2) | R core; **L-PBF Cu manifold shell (S)** below 2k/yr | per-tile pads | tiled manifold, 4 port pairs; the one place L-PBF fits |
| 800 VDC shelves, SST, DC-DC | de-rated chassis 0.40/0.30 x 3 mm | pad / baseplate | 20.9 K vs 41.7 K pin-fin at 50 W/cm2 |
| SiC traction / chargers (Al loops) | licensed forged/MIM Cu insert or brazed Al laminate | baseplate | no bare Cu in Al loops; AQG 324 |
| aerospace / eVTOL / motorsport inverters | **L-PBF AlSi10Mg conformal cooler-housing (S)** | baseplate | 34.6 K vs 41.7 K pin-fin; AM niche (integration, mass) |
| laser diodes, RF GaN, CPO | P core + **CVD diamond insert <= 2 cm2** | AuSn / In | -11.9 K on a 2 x 2 mm hot spot |

## 8. Reliability, qualification and drop-in compatibility

**Drop-in checklist.**

- OCP PG25 with bare OFE Cu, 316L and EPDM; no Al, Zn, non-DZR brass, NBR or silicone.
- Inlet 17-50 C, spec point 45 C (ASHRAE W45, 65 C return), with full performance at Nvidia's 0.75-1.0 LPM/kW.
- MAWP 1.0 / proof 1.5 / burst >= 3.0 MPa; He <= 1e-5 mbar L/s on 100 % of units.
- <= 1.5 m/s; MGX/OAM/ORv3 envelopes; CpK >= 1.33 on dP and leak.

**Leak-before-break.** Ductile annealed copper with no brittle filler and burst/MAWP >= 3 means a crack leaks before it can rupture. At 5.7 kPa the plate runs in negative-pressure loops.

**Test plan** (OCP Cold Plate Test Spec v1.0.0 plus additions): TTV-A parity (117 cm2, 8 mirrored + 4 extra TCs, 0.5-1.5 LPM/kW, 25-50 C, three TIMs with D5470) and TTV-B (350 W/cm2 + HBM); dP at >= 6 points over 25-150 % of flow; burst and 10,000 pressure cycles; 1,000 cycles at 10-65 C, 50 at -40/+70 C and 1,000 power cycles (R drift <= 5 %, dP <= 10 %); 1,000-3,000 h PG25 soak at 65 C; fouling rig; ISTA 3E; independent-lab repeat.

**AM-specific qualification** (X, S, development parts):

- allowables for printed/electrodeposited Cu, including self-annealing;
- conductivity and strip-root shear;
- X flatness drift <= 5 um after 1,000 cycles at -40/+125 C;
- 100 % CT of S shells;
- particle shedding and ion-chromatography residue.

New-process qualification at Nvidia or a hyperscaler takes 12-24 months, which is why Tier 1/2 contain nothing printed.

**Service life.** 10 years, with screen checks keyed to the dP signature. PCM is field-replaceable. LM is handled by trained service or a sealed FRU. X lasts the life of the package.

## 9. IP posture

**Expired foundations we build on:** Tuckerman-Pease; Harpole/TRW US 5,088,005; Valenzuela/Creare normal-flow laminates; Heatric diffusion-bonded etched heat exchangers; IBM distributed feed; Cooligy multi-level manifolds (verify each); cold spray US 5,302,414; basic Cu-diamond composites; early L-PBF.

**Avoid or licence:** Fabric8 ECAM process patents (buy as a service); UIUC/Fabric8 "copper tree" designs; Corintis heat-map topologies; Alloy Enterprises support-removal specifics (we use through-etched features); Diabatix outputs (or our own adjoint CFD); CoolIT central-slot family (US 8,746,330 / 9,603,284 / 12,495,513, about 2028, verify); JetCool/Flex jets; Mikros/Jabil laminate improvements (FTO needed); WO2019043269A1 cold-spray Cu-diamond.

**Claim** (provisionals before disclosure):

1. Laminate HMMC with segmented, centre-fed/centre-collected slots fed by an interleaved in-laminate tree, stack <= 19 mm.
2. CTE-matched micro-channel lid: Cu-diamond base, segmented electrodeposited Cu strips <= 2 mm, CTE-matched cap joined at <= 300 C, indium BLT <= 100 um.
3. Power-map comb as a replaceable artwork layer, with a dP signature for screen health.
4. Stepped HBM pedestal in a bonded sandwich, with comb zoning.

FTO on about 12 families: US$50-110k, 8-14 weeks.

## 10. Risks, experiments and roadmap

| risk | likelihood / impact | mitigation |
|---|---|---|
| segmented-feed uniformity worse than 1.10 | medium / +1 K | experiment 1; 3.0 kPa comb; 2.5-D fallback |
| 10-20-layer bond yield | medium / cost, leaks | PCHE heritage, flat sheets, C-scan, He; CNC tree fallback |
| ECAM single source, unpublished rate, price, R | high / X only | X gated; Tier 3A LM or MoCu lid fallback |
| Cu-diamond CTE, joining, price | high / X only | strips, MoCu cap, <= 300 C joint; month-9 gate |
| printed-part contamination | medium / life | no printed wetted parts upstream of cores |
| benchmark reconstruction | certain / claim band | publish band; parity TTV; publish our dP curve |

**Five experiments that retire the most risk:**

1. **Clear-SLA water table + CFD of the segmented-feed laminate** (weeks 1-4): momentum coefficients, uniformity at 18 and 36 LPM, 17-19 mm stack.
2. **Printed-manifold TTV-A article** (L-PBF Cu manifold bolted to a skived R core with a metal C-seal, weeks 4-12): parity data with PCM and LM at month 3, calibrating every model term before bond tooling.
3. **Laminate bond coupons** (10-20 layers, months 3-5): burst >= 4.5 MPa, tip bond >= 50 %, He <= 1e-6, 1,000 cycles.
4. **X coupon and quote** (40 x 40 mm, months 3-9): conductivity, shear, residue, bow over -40/+125 C, and a 10k/100k price. Gate: >= 7 K better than a Cu lid with indium (model 8.3 K), bow <= 15 um, <= US$300 at 100k.
5. **Fouling rig** (months 1-6): 0.15/0.10 mm cores behind 50/33/25 um screens, ISO 4406-dosed PG25, 1,000 h, ECAM surface versus skived.

**Roadmap (months):**

| months | work |
|---|---|
| 0-1 | Topology-optimise the tree; render it as artwork; FTO and provisionals; order prints and ECAM coupons |
| 1-3 | Experiments 1, 2, 5; first TTV data at month 3 |
| 3-6 | Bond coupons; first bonded DL plates (15 kW and Rubin class) at month 6 |
| 6-9 | OCP-format TTV-A and TTV-B on bonded plates; **X gate at month 9** |
| 9-15 | Qualification matrix; hyperscaler/ASIC samples; LP15; Tier 1/2 qualified by month 15; independent-lab repeat; PPAP; second bond source |
| 15-18 | Customer qualification; 100k/yr capacity; if X is a go, X lid prototypes with a lid partner; first S-shell wafer-scale unit |

## 11. Scorecard vs CoolIT 15 kW

Conditions: 15 kW, 18 LPM PG25, 45 C, 117 cm2. Columns:

- **conservative** = Tier 1 (R, PCM) at the Monte Carlo P90;
- **nominal** = median/deterministic value;
- **stretch** = Tier 2 LM, with the X module (33 um loops) in brackets.

| metric | CoolIT 15 kW | conservative | nominal | stretch |
|---|---|---|---|---|
| average case-to-inlet dT | 34.4 K | <= 31.4 K (-9 %) | 28.0 K (-19 %) | 22.9 K (-33 %) [19.8 K, -42 %] |
| maximum case-to-inlet dT | 44.2 K | <= 34.5 K (-22 %) | 31.1 K (-30 %) | 25.0 K (-43 %) [21.9 K, -50 %] |
| Tcase,max at 15 kW | 89.2 C | <= 79.5 C | 76.1 C | 70.0 C [66.9 C] |
| same-paste avg / max | 34.4 / 44.2 K (reconstruction P90 41.5 / 51.8) | <= 36.9 / 42.1 K (P90) | 30.0 / 35.0 K | 26.5 / 31.5 K at equal pump power |
| R'' (avg, incl. TIM) | 0.269 cm2K/W | <= 0.245 | 0.219 | 0.179 [0.154] |
| flow-driven hot spot | 8.8 K (9.8 total) | <= 2.5 K | 1.5 K | 0.7 K |
| plate dP, 18 LPM, incl. screen | n/d (est. 24.6, 17-42) | <= 7.2 kPa | 5.7 kPa | 4.2 kPa (20 mm ports) |
| plate dP, 36 LPM | - | <= 26 kPa | 22.4 kPa | 16.3 kPa |
| pump power, 18 LPM | ~7.4 W | <= 2.2 W | 1.7 W | 1.3 W |
| Q cap, Tcase,max <= 85 C, 1.2 LPM/kW | ~12.7 kW | >= 18.3 kW | 21.6 kW | 29.7 kW [38.2 kW] |
| 350 W/cm2 reticle die, Tcase,max (zoned) | ~121 C (LM), ~134 C (paste) | 107 C (PCM) | 93 C (LM) | 84 C (P core, LM) [82 C soldered X lid, die top] |
| flow to match 34.4 K average | 18 LPM | <= 12 LPM | 10.9 LPM (0.39 W) | 8.4 LPM (LM, 0.18 W) |
| core height, 15 kW class | n/d | <= 21 mm | 18 mm (17-19) | 15 mm (LP15) |
| factory cost, 100k/yr | n/d (GB200 skived ~US$105; ASP 300-400) | <= US$200 | ~US$189 (Rubin ~US$134) | X +US$117-277 |
| service life vs skived | 1.0x | >= 0.6x | 1.0x | 1.2x behind 25 um |
| printed content, volume BOM | 0 | 0 | 0 | X only (month-9 gate) |
| first TTV data / qualified | - | 4 / 18 months | 3 / 15-18 months | 3 / 15 months |

**Sources (web, this session):**

- Fabric8/UIUC ECAM plate: https://www.metal-am.com/copper-am-cold-plate-improves-ai-data-centre-cooling/
- Fabric8 Hot Chips 2023: https://www.hc2023.hotchips.org/assets/program/conference/day2/FPGAs%20Cooling/Fabric8Labs%20-%202023%20Hot%20Chips%20-%20ECAM%20for%20Cooling%20High%20Performance%20ICs%20(2023.08.29).pdf
- Fabric8 capacity round: https://www.metal-am.com/?p=113419 ; https://evertiq.com/news/2025-11-18-fabric8labs-secures-50m-to-expand-us-manufacturing-capacity
- ECAM 0.1 mm features: https://blogs.sw.siemens.com/simcenter/the-cool-factor-additive-manufacturing-is-redefining-cold-plate-design/
- Green-laser L-PBF Cu: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8269709/
- Binder-jet Cu 327.9 W/mK: https://vtechworks.lib.vt.edu/items/04c6137a-008a-4c2f-932e-c22700ca002b
- Cu-diamond 600-700 W/mK, CTE 7-8: https://www.scientific.net/AMR.59.169 ; https://www.knowledgetransferireland.com/Benefits_to_Business/Licensing-Opportunities/Copper-Diamond-Composite-Heat-Spreaders-Using-Cold-Spray.pdf
- CVD diamond cost: https://www.circuitnet.com/news/uploads/2/IMAPS2015_E6_Paper_TObeloer_2.10.2015__3__1.pdf ; https://www.electronics-cooling.com/2016/04/application-of-diamond-heat-spreaders-for-the-thermal-management-of-gan-devices/
- Vapor-chamber evaporator resistance: https://docs.lib.purdue.edu/coolingpubs/354 ; https://www.1-act.com/?p=7619
- L-PBF channel roughness: https://iris.polito.it/bitstream/11583/2952372/3/Manuscript%2020200224_Rev2.pdf ; https://www.patsnap.com/resources/blog/articles/electrochemical-polishing-for-am-heat-exchanger-channels/
- Alloy Enterprises Stack Forging: https://techcrunch.com/2025/11/05/this-startups-metal-stacks-could-help-solve-ais-massive-heat-problem/ ; https://www.3dnatives.com/en/alloy-enterprises-releases-copper-direct-liquid-cooling-for-ai-data-centers-160620254/
- Diabatix/GKN GPU case: https://www.gknpm.com/media/qtcdp40x/gknpm_diabatix_case_study_web.pdf ; GB200 generative design: https://www.alphaxiv.org/abs/2604.10941
- Internal: `research/manufacturing-cost.md`, `research/physics-options.md`, `research/gap-cost-volume-and-market-anchors.md`, `research/power-electronics.md`, `physics/SYNTHESIS-physics.md`, `design/proposal-hmmc-elite.md`, `design/proposal-direct-to-die.md`.
