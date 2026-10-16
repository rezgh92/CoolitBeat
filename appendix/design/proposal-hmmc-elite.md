# HMMC-E: hierarchical manifold micro-channel cold plate, elite architecture (key: hmmc-elite)

Architecture proposal, 2026-10-13. Benchmark: CoolIT 15 kW Split-Flow plate (June 2026): 15 kW, 18 LPM PG25 (1.2 LPM/kW), 45 C inlet, avg case-to-inlet 34.4 K, max 44.2 K, paste TIM, pressure drop undisclosed (our reconstruction ~22-25 kPa, band 17-42). All our numbers are from the project scoping model (`coldplate_model.py`, corrected per `SYNTHESIS-physics.md`) run with this geometry (`design/hmmc_elite_run.py`, `hmmc_elite_geom.py`); treat each term as +/-25 %.

## 1. Concept in one page

HMMC-E is a tied-sandwich, all-OFE-copper, single-phase plate in which coolant reaches every 4 mm of fin through a two-level manifold instead of running 54 mm along the fins. The core is a skived fin field (0.10 mm fins, 0.15 mm gaps, 2.0 mm tall, on a 1.0 mm base); above it an etched tie-grate, an etched plenum layer and an etched orifice-comb feed 28 slots (14 inlet, 14 outlet, 4 mm apart) that are pockets in a machined manifold block; two shallow "bow-tie" header troughs cross the slots at the plate centre and are fed from both ends through in-plane perimeter loops, so the ports exit horizontally and the plate is 21 mm tall (18 mm low-profile). The whole stack is diffusion-bonded in one vacuum cycle: no braze, no weld, no polymer, no dissimilar metal.

Why it beats the benchmark (15 kW, 18 LPM, 45 C, 117 cm2, model):

| metric | CoolIT 15 kW | HMMC-E/R same paste | HMMC-E/R PCM pad (Tier 1) | HMMC-E/R liquid metal (Tier 2) |
|---|---|---|---|---|
| avg case-to-inlet | 34.4 K | 30.0 K | **28.0 K** | 22.9 K |
| max case-to-inlet | 44.2 K | 35.0 K | **31.1 K** | 25.0 K |
| plate dP at 18 LPM | undisclosed (~22-25 est.) | 6.0 kPa | **6.0 kPa** | 6.0 kPa |
| hydraulic pump power | ~7 W est. | 1.8 W | 1.8 W | 1.8 W |
| Q at Tcase,max <= 85 C | ~13 kW | 18.4 kW | **21.6 kW** | 29.7 kW |

The five decisive differentiators:

1. **4 mm flow length, fresh fluid everywhere.** Convection falls from 12.6 to 10.1 K, the 54 mm caloric ramp (CoolIT's +8.8 K systematic hot spot) becomes a 0.3 K ripple, and the channel friction term is 0.23 kPa instead of ~15 kPa. The plate is 86 % inertial; dP is set by ports and metering, not fins.
2. **Orifice-comb metering with a power-map-programmed hole density.** 0.5 mm etched holes (92 per uniform slot, 1.2 m/s, 2.2 kPa) make every branch inertial and identical, so flow uniformity is 1.10 max/min and does not degrade with flow; the same etched layer zones the flow (die block 92 %, HBM 6 %) by hole count alone, so one plate family serves any package by changing one artwork.
3. **Tied sandwich with 50 % fin-tip bond and a 1.0 mm base.** Pressure bow is zero, the stack is 24x stiffer than a 2 mm skived base, mount+thermal bow over a 50 mm die is 4-25+6 um (vs 13-77+19), the base term halves (6.6 -> 3.3 K), and burst is governed by the perimeter land, not the base.
4. **In-plane header routing.** Both-end-fed bow-tie troughs plus perimeter loops cut the design-H stack from ~30 mm to 21 mm with horizontal 16 mm ports, keeping all velocities <= 1.5 m/s and the slot-to-slot criterion (branch dP >= 6x header head) satisfied.
5. **Deployability engineered in, not assumed.** 0.15 mm gaps behind an integrated 50 um absolute screen with a dP signature give a 10-year drop-in SKU; a 0.10 mm core is a filtration-gated performance SKU; every datum will be published in OCP Cold Plate Test Spec v1.0.0 format with the dP curve CoolIT withholds.

Honest framing: with CoolIT's own paste the mean gain is 13 % (30.0 vs 34.4 K) and the max gain 21 %; the interface (PCM, then liquid metal) is where the margin becomes 19-33 % mean and 30-43 % max. The tied sandwich is what lets a pad or liquid metal hold its datasheet value (uniform bond line), so the interface claim is legitimately part of the architecture.

## 2. Thermal core

**Geometry (robust core, HMMC-E/R, 117 cm2 reference field, 108 x 108 mm):**

| item | value | note |
|---|---|---|
| fins | skived OFE Cu C10100, t 0.10 mm, gap 0.15 mm (pitch 0.25), H 2.0 mm, along x | eta 0.56, h 13.2 kW/m2K, h_eff 127 kW/m2K |
| base | 1.0 mm as-bonded, 0.8 mm minimum finished under the die; 1.5-2.0 mm under the perimeter land | base term 3.3 K at 128 W/cm2 |
| flow length / slot pitch | 4 mm / 8 mm inlet-to-inlet (die zone of real packages: 5 mm / 10 mm) | sawtooth at case < 0.5 K |
| channel state | u 0.083 m/s, Re 19, 12,100 parallel 4 mm segments | laminar, no self-cleaning (hence screen) |
| caloric | isothermal cell, NTU 1.25, 0.60 x 12.7 K = 7.6 K | +1.3 K vs linear ramp, accepted |

**Performance core (HMMC-E/P):** gap 0.10, fin 0.10, H 1.5 mm, h_eff 187 kW/m2K, convection 6.8 K; identical manifold with a 1.6 kPa comb. Only for loops with <= 33 um absolute filtration (section 3).

**Flow path:** port -> integrated screen -> inlet trough (centre of plate, both ends) -> window in block floor -> feed slot (3.3 x 6.5 mm, centre-fed) -> comb (0.5 mm holes) -> lower plenum (1.5 mm) -> tie-grate openings -> down the fin gaps, 4 mm along the fins in both directions -> up through the grate into the outlet slot (3.3 x 8.4 mm) -> outlet trough -> port. Every fluid parcel wets 4 mm of fin at inlet temperature.

**Zoning for GPU/HBM (real package, 4 reticle dies 26 x 33 mm + 16 HBM):** the comb hole density follows the heat map at 4 mm (x) by 1 mm (y) resolution. For the 2027-28 package at 350 W/cm2: die block 34 cm2 gets 92 % of flow (1182 holes, 11.4 holes per cm of slot, 3 staggered rows), HBM columns 21 cm2 get 6 % (78 holes, one row at 8 mm pitch), unheated margin 2 % (28 holes, anti-stagnation). Die-zone slots are widened to 4.3 mm at 10 mm pitch (5 mm flow length) so the slot-entry head (249 Pa) stays below branch dP/13 at 2.4 LPM per slot; channel velocity there is 0.25 m/s (Re 57), friction 1.1 kPa. Across-die case gradient 6-8 K (split-flow: 22-30 K). HBM is never downstream of a die.

**HBM pedestal:** the base is machined (after bonding) as a stepped Cu pedestal reaching the HBM plane within +/-0.05 mm (step 0 to 0.4 mm as a test variable; lidded packages are flat), flatness 0.02 mm, 0.5 mm clearance to the die edge, with 0.05-0.10 mm compliant TIM (paste <= 0.3 cm2K/W or indium 0.06). No gap-filler pads above 15 W/cm2. Model: HBM Tj 84-91 C at 40 W/cm2 (split-flow plate: 105 C).

**Interface strategy by tier (same core):**

| tier | package | interface | plate face | R'' cm2K/W | retention |
|---|---|---|---|---|---|
| 1 drop-in, serviceable | lidded (B300, MI355X, Rubin flat lid) | phase-change pad PTM7950-class | bare lapped Cu, <= 25 um over 100 mm | 0.055 | 20-30 psi |
| 2 OEM co-design | lidded, Ni/Au lid | Ga-In liquid metal, dam, 20-30 um BLT | 3-5 um electrolytic sulfamate Ni on the contact face only, no Au, masked | 0.015 | 10-20 psi |
| 3 chip co-design | bare die / microchannel-lid socket | stepped pedestal on die through liquid metal | Ni on face; CuW/CuMo variant only if soldered | 0.015 (lid + TIM1 removed) | <= 0.3 MPa on die |

Grease is never specified on 100+ mm lids: its bow/ageing tails produced CoolIT's 10 K plate-to-plate spread. Ni plating is used only where liquid metal is used; the wetted path is bare OFE copper.

## 3. Hydraulic architecture

**Manifold levels (18 LPM reference):**

| level | element | section | velocity | rule |
|---|---|---|---|---|
| L0 | ports, 16 mm bore (20 mm option), horizontal, in the ears | 201 mm2 | 1.49 m/s (0.95 at 20 mm) | <= 1.5 m/s |
| L1a | inlet trough, 29 x 6 mm, crossing the slots at y = 54 mm, fed at both ends with Q/2 | 175 mm2 | 0.86 m/s, head 372 Pa | branch dP / head = 6.5 >= 6 |
| L1a | outlet trough, 43 x 6 mm, side by side with the inlet trough, 3 mm wall, drained at both ends | 260 mm2 | 0.57 m/s | 1.5x inlet area |
| L1b | perimeter loops in the ears (inlet along one x-edge, outlet along the other), carrying Q/2 to the far trough end | 150 / 225 mm2 (10 x 15, 10 x 22.5 mm) | 1.0 / 0.67 m/s | both ports on one plate edge |
| L2 | 14 inlet feed slots 3.3 x 6.5 mm, 0.7 mm walls, centre-fed through 3.3 x 29 mm windows | 21.4 mm2 per half-slot | 0.50 m/s, head 125 Pa | branch / head = 19 >= 15 |
| L2 | 14 outlet slots 3.3 x 8.4 mm, windows 3.3 x 43 mm | | 0.12 m/s | |
| L3 | comb: 92 x 0.5 mm holes per slot (1288 total, 14 mL/min each) | 18.1 mm2 per slot | 1.19 m/s | 2.2 kPa, inertial |
| L3 | plenum 1.5 mm + grate (50 % open) | 178 mm2 per slot | 0.12 m/s descent | <= 0.5 m/s |
| L4 | fin gaps, 4 mm | | 0.083 m/s | 0.23 kPa |

Hierarchical passage widths: port 16 > loop 10 > trough 6 > slot 3.3 > comb 0.5 > plenum/grate 0.5 > channel 0.15 mm; each stage > 2x the next, so nothing sieves before the channels. Each inlet slot dead-end (at the plate edges) has a 0.6 mm bleed into the neighbouring outlet slot (5 % of slot flow, +0.4 K) so dense particles cannot settle under the die. Reverse flow is tolerated (symmetric geometry; the comb meters in either direction).

**dP budget, port-to-port, PG25 at 45 C (model, +/-25 %):**

| flow | channel | turns | troughs+loops+tees | comb | ports | screen (clean) | total | pump W |
|---|---|---|---|---|---|---|---|---|
| 18 LPM (1.2 LPM/kW) | 0.23 | 0.01 | 0.61 | 2.20 | 2.57 | 0.40 | **6.0 kPa** | 1.8 |
| 36 LPM (2.4 LPM/kW), 16 mm ports | 0.5 | 0.05 | 2.4 | 8.8 | 10.3 | 1.6 | **23.6 kPa** | 14.2 |
| 36 LPM, 20 mm ports | 0.5 | 0.05 | 2.4 | 8.8 | 4.2 | 1.6 | 17.6 kPa | 10.5 |

Claim <= 8 kPa at 18 LPM and <= 25 kPa at 36 LPM until CFD/test. Flow uniformity: slot-to-slot 1.06-1.15 (momentum-coefficient uncertainty), along-slot 1.05-1.09, global target <= 1.10 at 18 LPM; because the branch is inertial (2.2 of 2.4 kPa), the ratio to the header head is flow-independent, so uniformity holds to 36 LPM. Flow-driven hot-spot term 1.5 K nominal (+/-10 %), 2.5 K conservative (+/-20 %).

**Couplings:** at 18 LPM a UQD08 pair costs ~25 kPa (Cv estimate +/-50 %), four times the plate; a UQD06 pair ~100 kPa. Specify UQD12-class (3/4 in) or 3/4 in barb / hard line for the 15 kW-class product (~5 kPa per pair) and UQD08 minimum for Rubin-class plates (2-4 LPM, where it is 1-2 kPa). Negative-pressure (Chilldyne-class) compatibility follows from 6 kPa.

**Filtration and fouling strategy:** channel gap >= 3x the absolute rating of the last filter. R core (0.15 mm): integrated 50 um absolute pleated 316L screen >= 12 cm2 in the inlet ear (clean 0.3-0.5 kPa, 100x the channel count in pores), serviceable through a threaded plug, with the plate dP as its signature (alarm at +2 kPa = screen at 3x clean); relative life 0.6-1.2x a skived plate behind a 50 um nominal CDU filter, >= 1.0x behind 25 um. P core (0.10 mm): loop filtration <= 33 um absolute mandatory plus a 33 um integrated screen >= 15 cm2; life ~0.6x. 0.05-0.075 mm channels are excluded from the roadmap (W/d <= 3, 1-3 year life). Factory flush to ISO 16232 class, < 0.1 mg residue, capped and shipped dry or PG25-filled.

## 4. Mechanical and construction

**Stack-up (standard, 21.1 mm):**

| # | layer | thickness | process | function |
|---|---|---|---|---|
| 0 | base + fins | 1.0 + 2.0 mm | skived OFE Cu | fin field; pedestal machined after bonding |
| G | tie grate | 0.5 mm | photochemically etched, 0.5 mm bars in y at 1.0 mm pitch | bonds 50 % of every fin tip; defines slot walls |
| P | lower plenum | 1.5 mm | double-sided etched, 28 slots 3.3 x 108 mm, 0.7 mm walls, bleed notches | spreads comb jets to all 432 gaps per slot |
| C | comb | 0.4 mm | etched: hole map over inlet slots, open over outlet slots | metering and zoning |
| B | manifold block | 11.5 mm | CNC OFE Cu: 28 pockets 3.3 x 6.5 mm from below (die zone 4.3 mm at 10 mm pitch); 0.7 mm floor with windows; two troughs 6 mm deep from above with 2.5 mm posts at 8 mm pitch; perimeter loops; port bores; screen cavity | L1/L2 |
| K | cover | 2.5 mm | Cu plate, bonded to block rim and posts | closes troughs; span between posts 5.5 mm |

Low-profile LP18 (17.8 mm): fins 1.5 mm, plenum 1.2, slots 5.0, troughs 5.0 with 3.2 kPa comb; costs +0.9 K and +1.1 kPa. LP15 (15.6 mm): troughs 4.0 (37.5 + 56 mm wide), slots 4.5, cover 2.0; +0.9 K, uniformity relaxes to ~1.12. The honest answer to "15 mm for 1U": 18 mm is free, 15.6 mm costs ~1 K and a uniformity point; below that the comb or the fins must go.

**Joining:** one-shot vacuum diffusion bonding of all six layers (OFE C10100/C10200 only, 850-950 C, 5-10 MPa, 1-4 h, vacuum or argon, never H2 with ETP copper). No filler to wick into 0.15 mm gaps, no CTE mismatch, hermetic, and the furnace anneals the stack, so all strength is designed to annealed OFHC (yield 70 MPa, UTS 220). Fallback: BAg-8 foil vacuum braze of layers 0-G-P-C-B with stop-off on the fin tips, plus green-laser or FSW cover seam. Acceptance: 100 % He leak <= 1e-5 mbar L/s (target 1e-6), C-scan sampling of tip-bond fraction (>= 50 %, reject < 30 %), first-article CT.

**Base thickness logic:** between 0.15 mm gaps the base stress at 3 MPa is 0.015 MPa; the base is irrelevant to pressure once the fins are ties. The floor is set by finish machining (0.1-0.2 mm), erosion allowance (0.1 mm) and skive tolerance (0.05 mm): order 1.0 mm, deliver 0.8 mm minimum under the die. Thinner is strictly better thermally (each mm is +9 K at 350 W/cm2).

**Pressure ratings:** MAWP 1.0 MPa (145 psi), proof 1.5 MPa, design burst >= 3.0 MPa (30 bar, above the OCP > 20 bar example), vacuum-stable to -0.9 bar(g). Tie stress at 3 MPa with 50 % bonded tips = 15 MPa (SF 4.7 on yield, 1.9 with Kt 2.5, 14.7 on UTS); perimeter land <= 4 mm unsupported or stepped to 1.5-2 mm (SF 5.8 at 1.5 MPa); cover between posts SF > 4; pressure-cycle amplitude 0.35 MPa (SF ~200); thermal fatigue amplitude 11 MPa in the base (SF ~6, verified by 1000 power cycles). Qualification burst target >= 4.5 MPa on first articles.

**Flatness and mounting:** finish-lap after bonding to <= 15 um over the die and <= 25 um over 100 mm, Ra <= 0.4 um. Four or eight spring screws on a stiff load frame bearing within 10 mm of the die edge (corner bolting on 150 mm consumes the whole bow budget); retention 10-20 psi (liquid metal) or 20-30 psi (PCM) over the contact area; package gap <= 50 um hot, verified with pressure film at 65 C.

**Envelope and mass:** 15 kW-class body 148 x 152 x 21 mm (fin field 108 x 108), ~2.3 kg; Rubin-class 110 x 120 x 16-18 mm, ~1.1 kg. Ports horizontal on one edge (vertical stubs optional for 2U).

## 5. Manufacturing route at volume

Process chain (all conventional; capacity exists in Taiwan/Vietnam/Mexico/EU):

1. Skiving of the fin field (0.10/0.15 x 2.0 mm, 108 mm wide, 2-5 min; vendors of the USUSTK/Wieland/Nakamura class; blade width caps the field at 100-250 mm). Base thinned to 1.0 mm by the same CNC.
2. Photochemical etching of G, P, C from 0.4-1.5 mm OFE strip (PCB/EMI-shield industry capacity; phototools US$0.5-3k; +/-25 um on 0.5 mm holes = +/-10 % area, acceptable because all holes drift together).
3. CNC of the manifold block: pockets by 3.3 mm slot mill (3 m of slot, ~5 min) or gang slitting saw, troughs and posts by 2.5-axis milling, bores, screen cavity. 0.7 mm pocket walls are supported at the root (aspect 9); 0.5 mm walls rejected for chatter.
4. Cover plate: stamped or sawn Cu, lapped.
5. Clean (alkaline/acid, deoxidise), fixture, vacuum diffusion bond (batches of 50-200 plates per 8-12 h cycle).
6. Finish machining: lap contact face, pedestal step, flatness check; masked electrolytic Ni on the contact face for Tier-2 SKUs.
7. Screen cartridge, plugs, stubs; ISO-cleanliness flush; 100 % He leak, 100 % flow/dP signature (6.0 +/-0.6 kPa at 18 LPM, 45 C), serialised.

| cost element (15 kW-class, 148 x 152 mm) | 10k/yr | 100k/yr |
|---|---|---|
| OFE copper 2.3 kg incl. swarf | 26 | 24 |
| skived core | 40 | 24 |
| three etched laminates | 36 | 16 |
| CNC manifold block | 80 | 34 |
| cover + stubs | 14 | 6 |
| diffusion bond cycle | 55 | 32 |
| screen, plug, taps | 15 | 8 |
| lapping, inspection | 12 | 6 |
| load frame, screws | 20 | 14 |
| He leak + flow test | 8 | 5 |
| **factory cost incl. 12 % yield/overhead** | **~US$345** | **~US$190** |
| Rubin-class plate (110 x 120 mm) | ~US$240 | ~US$135 |

Basis: `manufacturing-cost.md` route costs [KB-M, to be confirmed by RFQ]; a GB200-class skived/welded plate is ~US$170 (10k) / ~US$105 (100k), so HMMC-E adds ~US$30-70 per Rubin-class plate and stays under the ~US$400 Group-A ASP. The diffusion-bond cycle is the single largest adder and the capacity gate: ~2-3 furnaces per 100k/yr (US$3-6 M capex, 9-12 months). Lead time: first bonded prototypes 10-12 weeks (laminates 2 weeks, block 2 weeks, furnace slot 4-6 weeks); 100k/yr capacity 9-12 months. Yield risks, ranked: unbonded tip or rim areas (mitigation: flatness < 10 um per layer, C-scan, 100 % He), braze/bond creep into the comb holes (fallback route only), fin damage in handling before bonding (fixture), comb artwork registration to pockets (+/-0.1 mm, tolerant by design because holes sit in a 3.3 mm wide plenum), block pocket wall chatter (0.7 mm walls).

## 6. Predicted performance vs benchmark

**15 kW / 18 LPM / 45 C / 117 cm2 (model; P10-P90 from the 20k-sample Monte Carlo in `SYNTHESIS-physics.md`):**

| design | caloric | TIM | base | conv | avg dT | max dT | R'' cm2K/W | dP kPa | pump W | Q cap kW | Tcase,max |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CoolIT-like reconstruction (calibrated) | 6.3 | 9.0 | 6.6 | 12.6 | 34.5 | 44.3 | 0.269 | 24.6 | 7.4 | 12.7 | 89 C |
| HMMC-E/R same paste | 7.6 | 9.0 | 3.3 | 10.1 | 30.0 (26-37) | 35.0 (31-42) | 0.234 | 6.0 | 1.8 | 18.4 | 80 C |
| **HMMC-E/R PCM (Tier 1)** | 7.6 | 7.1 | 3.3 | 10.1 | **28.0 (26-31)** | **31.1 (29-35)** | 0.219 | **6.0 (4.7-7.8)** | 1.8 | **21.6** | **76 C** |
| HMMC-E/R liquid metal (Tier 2) | 7.6 | 1.9 | 3.3 | 10.1 | 22.9 (22-25) | 25.0 (24-27) | 0.179 | 6.0 | 1.8 | 29.7 | 70 C |
| HMMC-E/P PCM (<= 33 um loops) | 8.2 | 7.1 | 3.3 | 6.8 | 25.4 | 28.4 | 0.198 | 6.0 | 1.8 | 25.2 | 73 C |
| HMMC-E/P liquid metal | 8.2 | 1.9 | 3.3 | 6.8 | 20.2 (19-22) | 22.3 (21-24) | 0.158 | 6.0 | 1.8 | 37.0 | 67 C |
| HMMC-E/R LP18 low-profile, PCM | 7.5 | 7.1 | 3.3 | 11.1 | 28.9 | 31.9 | 0.226 | 7.1 | 2.1 | 20.6 | 77 C |

Other operating points (E/R PCM unless stated): 2x flow (36 LPM) 23.6 / 26.7 K at 23.6 kPa (17.6 with 20 mm ports); equal pumping power to the benchmark (7.4 W) is reached at 28.9 LPM, giving 24.7 / 27.7 K (liquid metal 19.6 / 21.7); CoolIT's 34.4 K average is reproduced at 10.9 LPM (0.72 LPM/kW, 2.3 kPa, 0.4 W) with PCM and at 12.3 LPM (0.82 LPM/kW) with the same paste; CoolIT's 44.2 K maximum at 9.3 LPM (0.62 LPM/kW) with the same paste; 50 C inlet (W+) at 15 kW: Tcase,max 81 C; DI water: 26.6 / 29.6 K.

**Real 2027-28 package (4 x 26 x 33 mm dies at 350 W/cm2 + 16 HBM at 40 W/cm2 = 12.85 kW, 15.4 LPM, heat-proportional zoning, 1 mm base), hottest-die case-to-inlet (3-D spectral fit):**

| core | h_eff | PCM | liquid metal | Tcase,max with LM | HBM Tj (pedestal) |
|---|---|---|---|---|---|
| CoolIT-like split-flow, flow across die then HBM | 101 | 88.6 K (paste 0.05) | ~76 K | ~121 C | 105 C |
| HMMC-E/R robust | 126 | 62.4 K | 48.4 K | **93 C** | 84-91 C |
| HMMC-E/P performance | 187 | 53.5 K | 39.5 K | **84 C** | 84-91 C |
| HMMC-E/R direct-to-die (Tier 3) | 126 | - | junction-to-inlet 0.14 vs 0.28 cm2K/W | ~80 C at the die top | - |

Un-zoned, the same plate loses 15 K at the hot die; zoning is mandatory and is a comb artwork, not a new plate.

**GPU-class plates (model, lidded, PCM / liquid metal):**

| case | CoolIT-like avg / max | HMMC-E/R PCM | HMMC-E/R LM | dP CoolIT-like / E |
|---|---|---|---|---|
| Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW | 16.1 / 23.5 K | 18.4 / 20.3 K | 16.9 / 18.5 K | 2.0 / 0.2 kPa |
| Rubin 2.3 kW, 60 cm2, 1.2 LPM/kW | 14.8 / 22.2 K | 16.0 / 17.9 K | 14.4 / 16.1 K | 2.5 / 0.2 kPa |
| Rubin Ultra 3.6 kW, 80 cm2, 1.0 LPM/kW | 17.6 / 25.1 K | 19.1 / 21.1 K | 17.3 / 19.0 K | 3.3 / 0.3 kPa |
| CoolIT 4 kW TTV point, 25 cm2, 160 W/cm2, 1.5 LPM/kW | measured < 36 K max | 31.0 / 34.4 K | 24.6 / 26.8 K | n/d / 1.0 kPa |

**Where it does not win, stated plainly:** (i) at 38-45 W/cm2 GPU-class flux the isothermal-cell caloric penalty (12 K at 1.0 LPM/kW) makes the HMMC's *average* dT 1-2 K worse than a split-flow plate with a pad; it wins only on maximum (3-4 K), on uniformity and on dP, and ties with liquid metal; (ii) against CoolIT's 4 kW plate (<= 0.225 cm2K/W max-basis) the robust core with PCM only matches it (0.215 max-basis); liquid metal or the P core is needed to beat it clearly; (iii) at 350 W/cm2 the robust core does not reach 85 C even with liquid metal (93 C) - that product needs the P core (25-33 um loops) or direct-to-die; (iv) the dP win is against a reconstruction, since CoolIT publishes none; (v) 2.3 kg and 21 mm are heavier and about as tall as the benchmark's ~143 mm body with its 12-15 mm centre bar.

## 7. Product family and applications

| product | core | interface | what changes |
|---|---|---|---|
| E15 TTV/Rubin-Ultra-class, 15 kW, 148 x 152 mm | R (P option) | PCM / LM | reference design above; UQD12-class or 3/4 in stubs |
| E-GPU Rubin / MI455X class, 1.8-3.6 kW, 100 x 100 mm lid | R | PCM (Tier 1), LM on Au/Ni lid (Tier 2) | 110 x 120 mm body, 16-18 mm, 10 inlet slots, 12 mm bores, UQD08 |
| E-D2D bare-die (TPU, Maia, Blackwell puck, Rubin Ultra option) | R or P | stepped pedestal + LM + dam | HBM step 0 to +/-0.15 mm as a variant; load-limited contact over HBM |
| E-Lid micro-channel lid core (Rubin Ultra 2H 2027 bid) | P | TIM1 only | the sandwich (layers 0-C) becomes the lid; CuW/CuMo base if soldered |
| E-CPU / NVSwitch / NIC | R, 1.5 mm fins | PCM | 60-80 x 80 mm, 6-8 slots, LP18 stack |
| E-Wafer / multi-chip (Cerebras-class, 43 W/cm2 over 460 cm2) | R, 2.5 mm fins | compliant per-die pads | tiled 4-trough manifold, 30 mm ports; the manifold is what scales, flow length stays 4 mm |
| E-Power: 800 VDC shelves, SST, DC-DC (5-30 W/cm2, Tj 150-175 C) | R de-rated (0.2 mm gaps, 3 mm fins, 12 mm pitch) | gap pad / direct-cooled baseplate jacket | same loop, same chemistry; die-to-die uniformity <= +/-3 K; cost-led |
| E-SiC traction / chargers (WEG 50/50, 65-75 C, aluminium loops) | 0.4-0.5 mm features, forged/MIM Cu baseplate insert, Al jacket | module baseplate | licensing play, AQG 324; not a copper plate business |
| E-Optics: laser diodes, CPO engines, RF GaN (DI water or PAO) | P | Au/Ni, isolated | high margin, low volume; the short flow length pays most in viscous PAO |

## 8. Reliability, qualification and drop-in compatibility

**Drop-in checklist:** OCP PG25 (bare Cu, 316L stubs, peroxide EPDM; no Al, Zn, brass except DZR, NBR or silicone anywhere); 17-50 C inlet, spec point 45 C, published 50 C data; full performance at 0.75-1.0 LPM/kW (NVIDIA's 45/65 C envelope) with curves 0.5-1.5 LPM/kW; plate dP 6 kPa at 1.2 LPM/kW leaves > 90 % of a tray budget for QDs and hoses; MAWP 1.0 MPa / proof 1.5 / burst >= 3.0 MPa and >= 20 bar; He <= 1e-5 (target 1e-6) mbar L/s, 100 % tested; velocities <= 1.5 m/s at 150 % rated flow, no orifice > 1.8 m/s; smallest passage 3x the screen rating; MGX/EIA/ORv3 envelopes with UQD08 (GPU) or UQD12-class (15 kW) at the tray; flatness <= 25 um, Ra <= 0.4 um; PPAP-style controls, CpK >= 1.33 on dP and leak.

**Wetted materials and chemistry:** all-OFE-copper wetted path with no filler; Ni only on the dry contact face of Tier-2 SKUs; biocide-containing inhibited PG25 at pH 8-9.5; copper-ion tripwire < 1-2 ppm in the 1000-3000 h soak. Operators who mandate a Ni-plated wetted path get an ENi option applied to layers before bonding (costs 7 % of the gap and 0.4 K).

**Leak-before-break:** ductile annealed OFE copper, no brittle braze in the pressure boundary, burst/MAWP >= 3, a through-crack in the 2.5 mm cover or 0.8 mm land leaks detectably long before the critical length; the 6 kPa plate also runs in negative-pressure loops where a breach draws air in.

**Test plan (OCP Cold Plate Test Spec v1.0.0 format, plus our additions):** TTV-A parity (2 x 2 ceramic, 117 cm2, 8 mirrored + 4 extra TCs, 15 kW, 0.5-1.5 LPM/kW, 25/35/45/50 C, PG25 and DI, three TIMs with ASTM D5470 at clamp pressure, 3 plates x 3 assemblies, heat capture >= 98 %, k = 2 uncertainty <= 2 % on R); TTV-B realism (4 die heaters with 300-350 W/cm2 patches + 16 HBM heaters, step 0 to 0.4 mm); dP at >= 6 points, 25-150 % of 15 LPM rated, three boundaries (port-to-port, with stubs, with named UQD pair); proof/burst, He leak, 10,000 pressure cycles 0-MAWP, 1000 operating cycles 10-65 C and 50 storage cycles -40/+70 C with R drift <= 5 % and dP drift <= 10 %, 1000 power cycles, 1000-3000 h PG25 soak at 65 C with coupons, fouling test with ISO 4406-dosed PG25 behind the 50 um screen, ISTA 3E shipping, 1000 QD mating cycles; post-cycling D5470 on PCM and liquid metal. Independent repeat of the headline point at a named national or university lab, published.

**Service life:** 10-year plate design life; screen inspection at the tray dP signature; PCM pad field-replaceable; liquid-metal SKU serviced by trained staff or shipped as a sealed plate-plus-module FRU (indium pre-form alternative).

## 9. IP posture

**Build on expired foundations:** Tuckerman-Pease parallel microchannels (1984), Harpole/TRW manifold microchannel US 5,088,005 (1992), Walpole/MIT alternating flow (1992), Valenzuela/Creare normal-flow laminates (1992), IBM cross-hatch distribution (1991), Cooligy hot-spot and multi-level manifold families (2003-06 filings, verify each expiry), TWI friction stir welding; copper diffusion bonding is public process art.

**Avoid:** a single central inlet slot over one fin field (CoolIT US 8,746,330 / 9,603,284 / 12,495,513, expiring ~Aug 2028 if the last is a true continuation - verify, plus CA/CN/TW/EP counterparts); discrete microjet arrays with per-jet returns and jet-onto-die lids (JetCool/Flex, Frore, Microsoft, Nvidia); two-phase dielectric evaporators and fluids; sensors, valves or controllers inside the plate (Nvidia "intelligent cold plate" families) and in-plate leak sensing (CoolIT 9,052,252); CoolIT's compliant-member family (US 11,725,886 / 12,188,733) for the bare-die variant.

**Verify before freeze:** Purdue HMMC (Garimella/Weibel/Drummond 2016-19), IBM Zurich Escher/Michel ultra-thin manifold (2009-11), Corintis heat-map topologies (2022-25), Nvidia hybrid-zone plates (2021-26), Mikros/Jabil laminate families (only if a full-laminate SKU proceeds), Taiwanese utility models at detailed design.

**Claim (US provisionals before any disclosure, then PCT):** (1) the etched orifice comb whose hole density is mapped to the device power map, with a lower plenum and tie grate between comb and fin tips; (2) both-end-fed bow-tie header troughs crossing the slots with in-plane perimeter loops giving horizontal ports and <= 21 mm height; (3) the tied sandwich with >= 50 % fin-tip bond through an etched grate and a <= 1.0 mm base in a one-cycle diffusion-bonded all-copper stack; (4) integrated last-chance screen with the plate dP as its signature and slot-end bleed orifices; (5) the stepped HBM pedestal machined into a bonded sandwich base, combined with zoned comb feeding; (6) the dual-use de-rated power-electronics derivative. Defensive publication for slot pitches, comb counts and loop orderings we do not claim. FTO opinion on ~10 families: US$40-100k, 8-14 weeks, run in US/CN/TW/EP/VN.

## 10. Risks, experiments, roadmap

| risk | likelihood / impact | mitigation |
|---|---|---|
| Flow uniformity assumed (theta_c 1-2.5 spans global 1.06-1.15) | medium / +1 K hot spot | experiment 1; comb is the regulator, not the headers |
| Diffusion-bond yield (unbonded tips, rim voids) | medium / cost, leaks | flatness < 10 um per layer, C-scan, 100 % He, braze+laser fallback |
| Loop cleanliness outside our control; 0.15 mm channels have no self-cleaning | medium / life | screen with dP signature, bleed orifices, fouling test, PG25 Guidelines action limits |
| TIM bond-line scatter now the largest hot-spot term (+/-10 um = +/-4 K with paste) | high / spread | never grease; PCM or LM; flatness 15 um; load frame near the die |
| Liquid-metal handling, Ga attack, cold storage (EGaIn freezes at 15.5 C) | medium / Tier 2 | Ni face, dam, no Al in module, Galinstan where needed, sealed-FRU indium alternative |
| 350 W/cm2 regime out of reach for the R core | certain / segment | P core behind 25-33 um filtration; direct-to-die; micro-channel-lid bid |
| CoolIT's dP, footprint and TC method unknown | certain / claim credibility | state the reconstruction band; publish ours in OCP format; parity TTV |
| Height 21 mm in 1U/MGX | medium / fit | LP18 and LP15 variants, horizontal ports |
| Furnace capacity and single-process dependence | medium / ramp | two bonding houses, braze fallback, 9-12 month capacity plan |
| Cost above US$400 Group-A ASP at low volume | low-medium | US$190 at 100k; sell via hyperscaler ASIC programmes and a Group-A partner |
| IP: Cooligy continuations, Purdue HMMC, Nvidia zone plates | medium | FTO before freeze; narrow, implementation-specific claims |

**Five experiments that retire the most risk:**

1. Water-table / CFD test of one slot pair with comb (clear acrylic, dye, 18 and 36 LPM scaled): pins theta_c and along-slot uniformity; the cheapest experiment in the programme (4 weeks).
2. Bonded coupons (108 x 40 mm): burst to >= 4.5 MPa, acoustic microscopy of tip-bond fraction, 1000 power cycles 10-65 C with He leak before/after (8 weeks).
3. Fouling rig: 0.15 mm and 0.10 mm cores behind 50 / 33 / 25 um absolute screens, PG25 dosed to ISO 4406 classes, 1000 h, dP and local-blockage thermography (12 weeks, started early).
4. TTV-A parity test, 3 plates x 3 assemblies, paste / PCM / liquid metal with D5470, OCP-format report (10 weeks after first plates).
5. TTV-B zoned real-package test with the stepped pedestal: die patches at 350 W/cm2, HBM at 40-60 W/cm2, step 0 / 0.15 / 0.4 mm, PCM and LM on Ni (12 weeks).

**Roadmap (months from go):** M0-2 detailed design, CFD of slot/comb/trough, FTO search, provisionals filed, laminate and block vendors engaged; M2-5 etched laminates, CNC blocks, bond trials, coupons (experiments 1-2), fouling rig running; M5-7 first three bonded 15 kW-class plates and three Rubin-class plates, TTV-A parity data; M7-10 TTV-B, LP18 variant, pressure/thermal cycling, soak start, hyperscaler ASIC sample; M10-14 full OCP qualification matrix, pilot diffusion-bond line, independent-lab repeat, PPAP package, Rubin-Ultra micro-channel-lid proposal with a lid partner; M14-18 customer qualification, second bonding source, 100k/yr capacity committed. Qualified product at M15-18.

## 11. Scorecard vs CoolIT 15 kW

15 kW, 18 LPM PG25, 45 C inlet, 117 cm2. Conservative = Tier-1 (R core, PCM) at the Monte-Carlo P90; nominal = its median; stretch = Tier-2 liquid metal on the R core [P core in brackets].

| metric | CoolIT 15 kW | conservative | nominal | stretch |
|---|---|---|---|---|
| average case-to-inlet dT | 34.4 K | <= 31 K (-10 %) | 28.0 K (-19 %) | 22.9 K (-33 %) [20.2 K] |
| maximum case-to-inlet dT | 44.2 K | <= 35 K (-21 %) | 31.1 K (-30 %) | 25.0 K (-43 %) [22.3 K] |
| Tcase,max at 15 kW | 89 C | <= 80 C | 76 C | 70 C [67 C] |
| same-paste like-for-like avg / max | 34.4 / 44.2 K | <= 34 / 40 K | 30.0 / 35.0 K | 26.5 K at equal pump power |
| unit resistance R'' (avg, incl. TIM) | 0.269 cm2K/W | <= 0.25 | 0.219 | 0.179 [0.158] |
| flow-driven hot spot (max - avg) | 8.8 K systematic (9.8 total) | <= 2.5 K | 1.5 K | 0.7 K |
| plate dP port-to-port at 18 LPM (incl. screen) | undisclosed (est. 22-25, band 17-42) | <= 8 kPa | 6.0 kPa | 4.5 kPa (20 mm ports) |
| plate dP at 36 LPM | - | <= 25 kPa | 23.6 kPa | 17.6 kPa (20 mm ports) |
| hydraulic pump power at 18 LPM | ~7 W est. | <= 3 W | 1.8 W | 1.4 W |
| Q capacity, Tcase,max <= 85 C, 1.2 LPM/kW | ~13 kW | >= 18 kW | 21.6 kW | 29.7 kW [37 kW] |
| flow for CoolIT's 34.4 K average | 18 LPM | <= 13 LPM | 10.9 LPM (0.72 LPM/kW) | 9 LPM |
| inlet for Tcase,max 85 C at 15 kW | ~41 C | >= 48 C | 54 C | 60 C |
| 350 W/cm2 reticle die, Tcase,max (zoned, real package) | ~134 C (paste) | 107 C (PCM) | 93 C (LM) | 84 C [P, LM]; ~80 C direct-to-die |
| HBM Tj at 40 W/cm2 (pedestal) | 105 C | <= 91 C | 88 C | 84 C |
| plate height / mass (15 kW-class) | ~25 mm with bar / ~1.5 kg est. | 21 mm / 2.3 kg | 18 mm (LP18) | 15.6 mm (LP15, +0.9 K) |
| factory cost at 100k/yr (15 kW-class / Rubin-class) | n/d (GB200-class skived ~US$105) | <= US$220 / 160 | US$190 / 135 | US$170 / 120 |
| service life vs skived plate (50 um abs screen) | 1.0x (10 y ref.) | >= 0.6x | 1.0x | 1.2x behind 25 um |
| disclosure | one flow point, no dP | full OCP v1.0.0 report, 6-point dP curve, independent repeat | same | same |

Claims to avoid externally: any figure resting on 0.05-0.075 mm channels; "< 10 % non-uniformity" without tying it to the comb-metered design; any dP that omits the coupling class; any 350 W/cm2 figure without zoning; any "beats the 4 kW plate" claim with PCM alone.
