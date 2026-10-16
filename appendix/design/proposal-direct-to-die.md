# DieDirect-3 (DD3): one bonded manifold-microchannel engine, three die-side faces (key: direct-to-die)

Architecture proposal, chip co-design tier, 2026-10-14. Benchmark: CoolIT 15 kW Split-Flow plate (June 2026): 15 kW on 4 ceramic heaters, 18 LPM PG25 (1.2 LPM/kW), 45 C inlet, average case-to-inlet 34.4 K, maximum 44.2 K, paste TIM, pressure drop undisclosed (our reconstruction ~25 kPa, band 17-42). Every number below comes from the project scoping model `coldplate_model.py` v2 and the physics-synthesis evaluator. Both are run by `design/d2d_run.py` (output `design/d2d_run.out`). Treat each term as +/-25 %. Tags: [M] model, [P] physics reports, [S] sourced (URLs at the end), [KB] engineering memory to verify.

---

## 1. Concept in one page

**What it is.** DD3 is a single-phase, all-OFE-copper, diffusion-bonded hierarchical manifold micro-channel (HMMC) engine. It has 0.10 mm skived fins with 0.15 mm gaps, 2.0 mm tall, on a 1.0 mm tied base. Flow runs 4 mm between centre-fed and centre-collected slots on an 8 mm pitch. An etched orifice comb meters the flow and zones it to the device heat map, and a 50 um absolute screen is built in. Only the die-side face differs between tiers, and it is set by machining and plating after the bond:

| face (machined after bond) | package | interface that sets Tj | tier |
|---|---|---|---|
| flat lapped bare Cu | lidded (B300/MI355X/Rubin flat lid) | PCM pad on lid | 1, drop-in |
| flat + 5 um electrolytic Ni + dam groove | lidded, Ni/Au lid | Ga-In liquid metal (LM) on lid | 2, OEM |
| **stepped pedestal + Ni (or W) + dam + moat, kinematic float** | **bare die / removable-lid / lidless CoWoS-L** | **LM on the die backside, which becomes the TIM1** | **3A, chip co-design (lead product of this proposal)** |
| Cu lid-core face, Ni/Au, separable manifold cap | micro-channel lid (MCL) inside the package | indium TIM1 soldered by the OSAT | 3B, lid component |
| manifold cap only | Si micro-cooler (TSMC IMC-Si) / in-die channels (Corintis) | none (fluid in silicon) | 4, end-state |

**Why it beats CoolIT.** On CoolIT's own TTV (15 kW, 18 LPM, 45 C, 117 cm2) Tier 3A gives 22.3 K average and 24.4 K maximum [M] (CoolIT: 34.4 / 44.2 K). Plate dP is 5.7 kPa including the screen (CoolIT: ~25 kPa estimated). Pumping power is 1.7 W (CoolIT: ~7.4 W). It holds T_case,max <= 85 C up to 30.8 kW (CoolIT: ~12.7 kW). The decisive gain shows up only on real silicon. At a 350 W/cm2 reticle die, junction-to-inlet is 64 K, against 86 K for the best lidded path on the same engine and 139 K for a CoolIT-like lidded paste plate. That raises the die flux allowed at Tj <= 105 C (45 C inlet) from 129 to 323 W/cm2 [M].

**Decisive differentiators**

1. **It removes the lid and TIM1, and uses LM for what remains.** Junction-to-inlet R'' (excluding caloric) at 350 W/cm2 is 0.165 cm2K/W, against 0.225 (lidded, LM), 0.259 (lidded, PCM) and 0.357 (CoolIT-like, lidded paste). That is 21-33 K at the junction compared with the best lidded options.
2. **One engine, one furnace, one wetted-side qualification.** Tiers 1, 2 and 3A share the same bonded sandwich and differ only in about 30 minutes of post-bond finishing. Tier 3B reuses the fin, grate, plenum and comb layers. The company sells one product line, not three.
3. **Package-aware mechanics.** A load-limited kinematic float delivers 0.04-0.10 MPa on the dies, and stiffener hard stops take shock loads. The pedestal crown is matched to the measured hot-state warpage. HBM pedestal fingers are cut per package SKU. Together these hold the LM bond line at 30 +/- 15 um across a 100-150 mm CoWoS-L.
4. **Gallium containment is designed as a subsystem, not a recipe.** A single LM field covers the molded interposer top. Containment is an FKM dam, a Ni or W barrier, a capture moat and conformally coated passives. Plates ship factory pre-wetted, so the interface is a part number rather than a field process.
5. **It is built for the in-silicon end-state.** The manifold cap (headers, metering comb, screen, ports) is a separable layer. It becomes the fluid-delivery layer for silicon micro-coolers and in-die channels.

---

## 2. Thermal core

**Engine geometry (robust "R" core, 15 kW TTV-class field 108 x 108 mm):**

| item | value | consequence [M/P] |
|---|---|---|
| fins | skived OFE C10100, t 0.10, gap 0.15, H 2.0 mm | h 13.2 kW/m2K, eta 0.56, h_eff 127 kW/m2K |
| flow length / slot pitch | 4 mm / 8 mm (die zone of real packages 5 mm / 10 mm) | channel velocity 0.083 m/s, Re 19, 12,100 parallel segments; NTU 1.25, isothermal caloric 0.60 x 12.66 = 7.6 K |
| base | 1.0 mm as-bonded, tied sandwich; **pedestal finished at 0.8 mm under the dies** (0.55-1.0 mm range set by the HBM step) | base term 2.6 K at 128 W/cm2; 7.2 K at 350 W/cm2 |
| performance "P" core (option) | gap 0.10, fin 0.10, H 1.5 mm, h_eff 187 kW/m2K | only behind <= 33 um absolute loop filtration [P] |
| channel floor | 0.15 mm behind an integrated 50 um absolute screen | 10-year deployable [P] |

**Flow path.** Port (16 mm), then the screen, then the centre-fed L1 header and centre-fed L2 slots. Flow passes the orifice comb (0.5 mm holes, 1.2 m/s, 2.0 kPa), the lower plenum and the tie grate, runs 4 mm through the fins in both directions, rises into the outlet slot and leaves by the outlet header and port. Every parcel of fluid wets only 4 mm of fin, all at inlet temperature.

**Zoning (4 x 26 x 33 mm dies + 16 HBM).** Comb hole density follows the heat map. The die block gets 85-90 % of the flow (3x the average flow per area), HBM columns get 0.3-0.5x, and the unheated margin gets about 2 % to prevent stagnation. Fluid under the hottest die rises 6.4-6.7 K. The across-die gradient is 6-8 K (split-flow: 22-30 K). HBM never sits downstream of a die [P]. Un-zoned, the same engine loses 15 K at the hot die, so zoning is mandatory. It costs a comb artwork, not a new plate.

**Pedestal (3A).** After the bond, the base is fly-cut into:

- a die plateau: one plane under all logic dies, crowned to the inverse of the measured hot-state die-top shape, <= 10 um per die after compensation;
- HBM fingers stepped by the per-SKU HBM-to-logic offset Delta (expected 0 +/- 0.15 mm, both signs since HBM4's 775 um stack height [S/KB]; 0.4 mm handled as a stress case), always leaving >= 30 um minimum gap so the plate never bears on HBM;
- a 1.0 x 0.3 mm capture moat and a dam-gasket groove on the interposer perimeter;
- relief of >= 1.5 mm over substrate passives and the stiffener.

**Interface strategy by tier (same engine):**

| tier | interface | R'' cm2K/W | BLT | pressure | plate face |
|---|---|---|---|---|---|
| 1 | PCM (PTM7950 class) on lid | 0.055 | 30 um | 20-30 psi | lapped Cu, <= 25 um / 100 mm |
| 2 | Ga-In LM on Ni/Au lid | 0.015 | 20-30 um | 5-15 psi | electrolytic Ni 3-5 um (0.0006), **no Au** |
| 3A | LM on bare Si die (no Au BSM on the lidless SKU); single field over dies and HBM | 0.0156 incl. Ni at the die; 0.04 over HBM at 50-100 um | 30 +/- 15 um | 0.04-0.10 MPa on dies, 0 on HBM | Ni 5 um, or sputtered W 1 um for 10 y at 95-105 C die-top |
| 3A fallback | PCM on die, putty on HBM (today's bare-die practice) | 0.055 / 0.28 | 30 / 100 um | 20-30 psi | bare Cu |
| 3B | indium TIM1, 150-200 um, OSAT reflow | 0.025 incl. metallisation | 170 um | bonded | Cu lid-core face with Ni/Au |
| 4 | none, fluid in silicon | 0.02-0.05 junction-to-fluid | - | - | manifold cap only |

Why LM at 3A rather than PCM: at 350 W/cm2 each extra 25 um of bond line costs about 4 K with LM, 10 K with PCM and 25 K with paste [M] (section 6.2). Only LM tolerates the residual warpage of a 100+ mm package. Why a copper lid-core at 3B rather than CuMo: a 1.0 mm CuMo face cannot pull down the effective CTE of a 4 mm copper sandwich (modulus-weighted it stays ~14-15 ppm/K), yet it costs +13 K at 350 W/cm2 [M]. The proven route is the Intel/AMD soldered-IHS practice: a copper lid with thick, compliant indium (shear strain about 0.06-0.1 per cycle at 170 um). A low-CTE CuW lid is reserved for spans above ~70 mm, where ORNL measured CuW at +30 % R over copper [S].

**End-state (Tier 4: Microsoft/Corintis, TSMC IMC-Si).** In-die channels reach 0.02-0.05 cm2K/W junction-to-fluid, i.e. 14-24 K at 350 W/cm2 versus 64 K for 3A [M]. Microsoft reports "up to 3x" heat removal and a 65 % lower peak rise on a prototype [S]. No external plate can match this, because the silicon bulk (0.05 cm2K/W, 17.5 K) and the hot-spot spreading stay in the path. TSMC's IMC-Si (a silicon cooler fusion-bonded to the die backside) reported only ~15 % over its lidded-TIM baseline (0.055 vs 0.064 C/W) [S]. A well-executed 3A therefore competes with backside silicon coolers. Channels in or just under the active layer are the real leap. Section 7 covers how DD3 stays relevant.

---

## 3. Hydraulic architecture

**Manifold levels (15 kW class, 18 LPM):**

| level | element | velocity | rule [P] |
|---|---|---|---|
| L0 | 2 ports, 16 mm bore (20 mm option) | 1.49 m/s | <= 1.5 m/s |
| L1 | inlet header 10 x 15, outlet 14 x 20 mm, side by side on the centre line | <= 1.0 m/s | branch dP >= 6x header head |
| L2 | 14 + 14 slots 3.5 x 8 mm, fed and drained at mid-length | <= 0.5 m/s at entry | branch dP >= 15x slot-entry head |
| L3 | etched comb, 0.5 mm holes, about 92 per uniform slot (zoned by count) | 1.2 m/s, 2.0 kPa | inertial, so uniformity holds with flow |
| L4 | 0.15 mm fin gaps, 4 mm | 0.083 m/s | 0.23 kPa |

**dP budget, port to port, PG25 at 45 C [M]:**

| flow | channel | headers/turns | comb | ports | screen (clean) | total | pump |
|---|---:|---:|---:|---:|---:|---:|---:|
| 18 LPM (1.2 LPM/kW) | 0.23 | 0.51 | 2.00 | 2.57 | 0.40 | **5.7 kPa** | 1.7 W |
| 36 LPM (2x), 16 mm ports | 0.5 | 2.0 | 8.0 | 10.3 | 1.6 | **22.4 kPa** | 13.4 W |
| 36 LPM, 20 mm ports | 0.5 | 2.0 | 8.0 | 4.2 | 1.6 | 16.3 kPa | 9.8 W |
| CoolIT-like reconstruction, 18 / 36 LPM | | | | | | 24.6 / 69.3 kPa | 7.4 / 41.6 W |

Monte Carlo P10-P90 of plate dP (without screen) is 3.9-6.6 kPa. Global flow max/min is 1.10 (1.06-1.15 across momentum-coefficient uncertainty), and the flow-driven hot spot is 1.5 K [P]. Claims to quote until CFD and test are done: <= 8 kPa at 18 LPM and <= 25 kPa at 36 LPM.

**Rubin-Ultra-class 3A plate (fin field ~80 x 95 mm, 3.6 kW):** 10 mm bores, 6 x 12 mm headers, comb re-sized to a 1.5 kPa branch. It gives 2.0 kPa at 3.6 LPM (1.0 LPM/kW, 0.12 W), 2.9 kPa at 4.3 LPM and 11 kPa at 2x flow [M]. That leaves essentially the whole tray budget to the couplings.

**Couplings.** A UQD08 pair costs ~25 kPa at 18 LPM, four times the plate, so the 15 kW class specifies UQD12-class or 3/4 in barbs (~5 kPa). Rubin-class flows of 2-4 LPM run UQD08 at 1-2 kPa [P]. Low dP makes the plate compatible with negative-pressure loops (Chilldyne/Daikin class).

**Filtration and fouling.** The governing rule is gap >= 3x the absolute rating of the last filter. The R core sits behind an integrated pleated 316L screen: 50 um absolute, >= 12 cm2, clean 0.4 kPa, alarm at 3x clean dP, serviceable through a plug. Slot dead-ends carry 0.6 mm bleeds, and every passage is > 2x the next stage downstream. The P core needs <= 33 um absolute loop filtration. Chip-co-design customers (Nvidia module, hyperscaler ASIC) control their loops, which is why 3A-P is a realistic option at this tier. The in-die end-state will need <= 10-25 um absolute, and building that competence now is part of the strategy (section 7).

---

## 4. Mechanical and construction

**Stack-up (D2D-15, 15 kW class; D2D-RU, Rubin-Ultra class, in brackets):**

| layer | thickness | process |
|---|---|---|
| pedestal base + fins | 1.0 + 2.0 mm | skived OFE Cu; pedestal fly-cut after bond |
| tie grate | 0.5 mm | etched; bonds >= 50 % of every fin tip |
| lower plenum | 1.5 mm | etched |
| orifice comb | 0.4 mm | etched; heat-map artwork |
| manifold block | 13 mm [8 mm] | CNC OFE Cu: slots, headers, screen cavity |
| cover | 2.5 mm | Cu plate, bonded |
| **total** | **21-25 mm [16-18 mm]** depending on header routing | |

**Joining.** All layers are vacuum diffusion-bonded in one cycle (850-950 C, 5-10 MPa, OFE only, no H2). There is no filler to wick into the 0.15 mm gaps, no dissimilar metal, and the result is hermetic. The fallback is a BAg vacuum braze with a laser-welded cover. Everything is designed to annealed OFHC (yield 70 MPa). For 3B, the block and cover are replaced by a 1.5 mm cover with two port bosses, and the manifold becomes a separate 316L or Cu cap sealed with a captured EPDM O-ring.

**Base-thickness logic.** Because the fin tips are ties (tie stress 2p), pressure does not limit the base: stress between 0.15 mm gaps is 0.015 MPa at 3 MPa, and even 0.5 mm passes [P]. The floor comes from fly-cut stock (0.1-0.2 mm), an erosion allowance (0.1 mm) and the HBM step. Under the dies the base is 0.8 mm, because each 0.1 mm costs 0.9 K at 350 W/cm2. Under HBM it is 0.55-1.0 mm depending on Delta. The perimeter land stays <= 4 mm unsupported or is stepped to 1.5-2 mm.

**Die flatness, warpage and loading (100-150 mm CoWoS-L):**

| issue | magnitude | DD3 answer |
|---|---|---|
| substrate warp over temperature | 100-300 um at corners [S/KB] | plate never references the substrate; it floats on the die plane |
| tilt of the die plane | 20-60 um across the interposer [KB] | kinematic float: 4 shoulder screws with calibrated springs on a stiff load frame, gimballing within +/-0.3 deg |
| die-top bow at operating temperature | 10-40 um second order [KB] | crown machined to the inverse of the hot-state (65-85 C) shadow-moire shape per package SKU (JESD22-B112 method) |
| plate bow | mount 4-25 um, thermal 6 um over 50 mm (tied sandwich, 24x stiffer than a skived 2 mm base) [P] | load frame bears within 10 mm of the die edge |
| residual | +/-15 um | absorbed by a 30 um LM film (window 15-50 um: +/-3 K at 350 W/cm2) |
| die load | 0.04-0.10 MPa (6-15 psi) = 140-340 N over 34 cm2 of logic; die-crack guide ~0.3 MPa | spring preload set by a shoulder stop; this is below today's bare-die PCM practice (20-40 psi) |
| HBM load | 0 (>= 30 um gap, LM or putty fill) | HBM is never a bearing surface |
| shock | 50 g x 1.5 kg = 735 N | 4 hard-stop pads on the stiffener engage at 50 um overtravel; co-design ask: pad height +/-25 um to the die top |

**Pressure ratings.** MAWP 1.0 MPa (145 psi), proof 1.5 MPa, design burst >= 3.0 MPa (above OCP's > 20 bar example), first-article qualification >= 4.5 MPa. Vacuum-stable to -0.9 bar(g). Tie SF at burst is about 20 on yield, the land SF is 5.8, and the thermal-fatigue amplitude in the base is 11 MPa (SF ~6) [P].

**Envelope and mass.** D2D-15: 148 x 152 x 21-25 mm, about 2.3 kg. D2D-RU: about 125 x 155 x 17 mm, about 1.5 kg. Ports are horizontal on one edge. Contact face: Ra <= 0.4 um, plateau <= 10 um per die, die-to-die co-planarity +/-10 um, HBM fingers +/-15 um.

---

## 5. Manufacturing route at volume

**Process chain (all conventional, all available in Taiwan, Vietnam, Mexico and the EU):**

1. Skive the fin field (0.10/0.15 x 2.0 mm; USUSTK/Wieland/Nakamura-class skiving). CNC the base blank to 1.0 mm.
2. Photochemically etch the grate, plenum and comb from OFE strip (PCB/EMI-shield industry; phototools US$0.5-3k; +/-25 um on 0.5 mm holes).
3. CNC the manifold block (slot mills, headers, port bores, screen cavity).
4. Clean, fixture and vacuum diffusion bond, 50-200 plates per 8-12 h cycle.
5. **Face finishing, which is where the tier is set.** Tier 1: lap. Tier 2: lap plus masked electrolytic sulfamate Ni 3-5 um. Tier 3A: vacuum-chuck the plate on a backing fixture so the fins are not crushed, single-point diamond fly-cut the plateau, fingers and crown from a per-SKU CAD map (+/-5 um), mill the moat and dam groove, Ni 5 um (or sputtered W 1 um), porosity test (ferroxyl/SO2). Tier 3B: fly-cut flat, then Ni/Au for solder wetting.
6. Screen cartridge, plugs and stubs; ISO 16232 flush; 100 % He leak <= 1e-5 mbar L/s; 100 % dP signature at 18 LPM (5.3 +/- 0.6 kPa).
7. Tier 3A only: install the FKM dam, stencil a pre-measured 1.5-2.0 g LM charge inside the dam, fit a peelable cap, and map 100 % of the faces optically.

**Unit cost estimate (factory cost, US$; engine basis from `manufacturing-cost.md` route costs and the sibling engine build-up [KB-M]; adders are this proposal's estimates [KB-M/L]; RFQ required):**

| element | D2D-15 10k/yr | 100k/yr | D2D-RU 10k/yr | 100k/yr |
|---|---:|---:|---:|---:|
| bonded engine (Cu, skive, 3 laminates, block, bond, screen, test, 12 % yield/overhead) | 345 | 190 | 255 | 145 |
| pedestal fly-cut + crown, per-SKU map | 18 | 9 | 15 | 8 |
| masked Ni 5 um face (W PVD option +10 / +5) | 8 | 4 | 7 | 3 |
| moat + FKM dam gasket | 5 | 3 | 5 | 2 |
| pre-applied LM charge (Ga-In ~2 g, ~US$2-3 material) + cap + QA | 9 | 5 | 8 | 4 |
| kinematic float + hard stops (increment over a standard frame) | 12 | 7 | 10 | 6 |
| face map, dam leak check, sampled thermal signature | 6 | 3 | 5 | 3 |
| hot-state warpage metrology (amortised per SKU) | 6 | 2 | 6 | 2 |
| **factory cost** | **~410** | **~225** | **~310** | **~175** |
| 3B: Cu lid-core (no block, Ni/Au face) + 316L manifold cap | - | - | ~165 | ~90 |

Against benchmarks: a GB200-class skived plate costs about US$105 at 100k, Rubin plate ASPs are about US$400 [S], and MLCP units are reported at 3-5x conventional solutions [S]. D2D-RU costs about +US$30 over the Tier-1 engine and stays below the Group-A ASP.

**Lead time.** First bonded 3A plates in 12-14 weeks (laminates 2 weeks, block 2 weeks, furnace slot 4-6 weeks, face finishing 2 weeks). The gating item is not the plate: it is lidless package samples, or our TTV-C (section 10). 100k/yr capacity takes 9-12 months, gated by 2-3 bond furnaces (US$3-6 M).

**Yield risks, ranked.**

1. Fin crush or base distortion during fly-cutting of a 0.8 mm base over a fin field. Mitigation: backing fixture, light diamond cuts, crown verified on 100 % of faces.
2. Ni pinholes, which let Ga attack the copper locally. Mitigation: 5 um minimum, porosity test, W option.
3. Unbonded fin tips. Mitigation: flatness < 10 um per layer, C-scan sampling.
4. Dam registration to the interposer edge, which has only 1-2 mm of margin. Mitigation: die-cut tolerance +/-0.1 mm, located on dowels.
5. LM charge mass +/-10 %. Mitigation: gravimetric check.

---

## 6. Predicted performance vs benchmark

### 6.1 CoolIT TTV point: 15 kW, 18 LPM PG25, 45 C, 117 cm2 (128 W/cm2)

On a TTV, "direct-to-die" means LM straight onto the heater top over a 0.8 mm pedestal. Budgets come from the project model; bands are the 20k-sample Monte Carlo P10-P90 [M].

| design | caloric | TIM | base | conv | avg dT K | max dT K | R'' | dP incl. screen kPa | pump W | Q cap kW (Tcase,max <= 85 C) |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---|
| CoolIT-like reconstruction (calibrated) | 6.3 | 9.0 | 6.6 | 12.6 | 34.5 (30.5-41.6) | 44.3 (40.1-51.8) | 0.269 | 24.6 | 7.4 | 12.7 |
| Tier 1, PCM | 7.6 | 7.1 | 3.3 | 10.1 | 28.0 | 31.1 | 0.219 | 5.7 | 1.7 | 21.6 |
| Tier 2, LM on lid | 7.6 | 1.9 | 3.3 | 10.1 | 22.9 | 25.0 | 0.179 | 5.7 | 1.7 | 29.7 |
| **Tier 3A, LM + Ni, 0.8 mm pedestal** | 7.6 | 2.0 | 2.6 | 10.1 | **22.3 (21.1-24.2)** | **24.4 (23.2-26.4)** | **0.174** | **5.7** | **1.7** | **30.8 (27.8-34.5)** |
| 3A, LM end-of-life (0.030) | 7.6 | 3.8 | 2.6 | 10.1 | 24.2 | 26.3 | 0.189 | 5.7 | 1.7 | 27.4 |
| 3A fallback, PCM on die | 7.6 | 7.1 | 2.6 | 10.1 | 27.4 | 30.4 | 0.214 | 5.7 | 1.7 | 22.3 |
| 3A-P (0.10 mm core, <= 33 um loops) | 8.2 | 2.0 | 2.6 | 6.8 | 19.7 (18.6-21.3) | 21.8 (20.7-23.6) | 0.153 | 5.8 | 1.75 | 38.9 (34.6-43.9) |
| Tier 3B, Cu lid-core, In 0.025 | 7.6 | 3.2 | 2.6 | 10.1 | 23.5 | 25.6 | 0.184 | 5.7 | 1.7 | 28.5 |

Other operating points for 3A:

| condition | avg / max dT | dP and pump |
|---|---|---|
| 2x flow (36 LPM) | 17.9 / 20.0 K | 22.4 kPa (16.3 with 20 mm ports) |
| 1.0 LPM/kW | 24.2 / 26.3 K | 4.0 kPa |
| 0.75 LPM/kW (Nvidia 45/65 C envelope) | 28.1 / 30.2 K | 2.3 kPa |
| ~29-30 LPM (equal pumping power to the benchmark, 7.4 W) | ~18.8 / 20.9 K | - |

CoolIT's 34.4 K average is reproduced at 0.55 LPM/kW (8.2 LPM, 1.2 kPa, 0.16 W), i.e. 54 % less flow and 45x less pumping power. Its 44.2 K maximum is reproduced at 0.42 LPM/kW, but the outlet would then reach 81 C, above Nvidia's 65 C return limit. At 50 C inlet, T_case,max at 15 kW is 74 C.

### 6.2 Real 2027-28 package: 4 x 26 x 33 mm dies at 350 W/cm2 + 16 HBM at 40 W/cm2 (12.85 kW, 15.4 LPM, zoned)

Hottest die centre, 1-D, Si 0.6 mm. Lidded stacks receive a lateral-spreading credit of 0.85x on lid-top flux. The CoolIT-like case value comes from the 3-D heat-map run [M/P].

| path (engine R unless noted) | case or die-top dT | **Tj-to-inlet** | Tj at 45 C | R''j-in | max die flux at Tj <= 105 C |
|---|---:|---:|---:|---:|---:|
| CoolIT-like split-flow, lidded, paste | 95.6 (lid) | **139.0 K** | 184 C | 0.357 | 129 W/cm2 |
| Tier 1, lidded, PCM | 54.1 (lid) | 97.5 K | 143 C | 0.259 | 205 |
| Tier 2, lidded, LM | 42.2 (lid) | 85.6 K | 131 C | 0.225 | 236 |
| 3A fallback, PCM on die | 60.7 (die) | 78.2 K | 123 C | 0.204 | 261 |
| Tier 3B, Cu lid-core, In TIM1 | 50.2 (die) | 67.7 K | 113 C | 0.174 | 306 |
| **Tier 3A, LM on die** | **46.9 (die)** | **64.4 K** | **109 C** | **0.165** | **323** |
| Tier 3A-P (0.10 mm core) | 38.1 (die) | **55.6 K** | 101 C | 0.140 | 382 |
| In-die microfluidics (0.02-0.05) | - | 13.7-24.2 K | 59-69 C | 0.02-0.05 | 1,070-2,670 |

HBM, with the H-Z2 fluid field:

| HBM interface | Tj HBM |
|---|---|
| single-field LM over pedestal fingers | 81 C |
| putty fallback | 91 C |
| paste gap-fill over a 0.4 mm step | 126 C (fails) |
| CoolIT-like plate (HBM downstream of the dies) | 105 C |

Bond-line penalty at 350 W/cm2:

| BLT | LM | PCM | paste |
|---:|---:|---:|---:|
| 15 um | 3.8 K | 13.2 K | 19.2 K |
| 30 um | 6.2 K | 19.4 K | 34.2 K |
| 50 um | 9.4 K | 27.6 K | 54.2 K |
| 80 um | 14.1 K | 39.9 K | 84.2 K |

On-die 2-3x hot spots add 5-15 K to every external path. Honest reading: only 3A-P reaches Tj ~100 C at 45 C inlet on this stress case. 3A-R needs 41 C inlet. The analyst Rubin Ultra (3.6 kW, ~87 W/cm2 die-average) is far easier, see 6.3.

### 6.3 GPU-class plates (2-4 kW)

**Die-level junction-to-inlet** (die-zone sub-plate, 88 % of flow, 1.0 LPM/kW, PG25 45 C):

| device | path | Tj-in at die average | Tj-in at a 300 W/cm2 patch |
|---|---|---:|---:|
| Rubin 2.3 kW (117 W/cm2) | CoolIT-like, lidded paste | 53.1 K (98 C) | 110.1 K |
| | Tier 1, lidded PCM | 39.4 K | 87.0 K |
| | Tier 2, lidded LM | 35.5 K | 76.8 K |
| | **Tier 3A** | **28.4 K (73 C)** | **58.6 K (104 C)** |
| | Tier 3B | 29.5 K | 61.4 K |
| Rubin Ultra 3.6 kW (87 W/cm2) | CoolIT-like, lidded paste | 43.9 K | 110.1 K |
| | **Tier 3A** | **23.4 K (68 C)** | **58.5 K** |

**Plate level, lidded framing [M]:**

| case | CoolIT-like avg / max | Tier 1 PCM avg / max | Tier 3A LM avg / max | dP (CoolIT-like / ours) |
|---|---|---|---|---|
| Rubin 2.3 kW, 60 cm2 | 16.1 / 23.5 K | 18.4 / 20.3 K | 16.7 / 18.4 K | 2.0 / 0.1 kPa |
| Rubin Ultra 3.6 kW, 80 cm2 | 17.6 / 25.1 K | 19.1 / 21.1 K | 17.0 / 18.8 K | 3.3 / 0.3 kPa |
| CoolIT 4 kW point, 25 cm2, 1.5 LPM/kW | 40.0 / 50.7 K reconstruction (CoolIT measured < 36 K maximum) | 31.0 / 34.4 K | 23.9 / 26.1 K | 6.2 / 1.0 kPa |

**Where DD3 does not win.**

1. On a ceramic TTV the direct-to-die advantage is invisible: 3A beats Tier 2 by only 0.6 K. The benefit is a junction-level claim that needs real silicon to prove.
2. On large, low-flux lidded footprints (38-45 W/cm2) the isothermal-cell caloric penalty makes the average 0.6-2 K worse than split-flow. DD3 wins only on maximum, dP and uniformity there.
3. In-die microfluidics will beat any external plate by 40-50 K at 350 W/cm2.
4. 3A-R misses Tj <= 105 C at 45 C inlet on the 350 W/cm2 stress case.
5. Height (21-25 mm) and mass (2.3 kg) are probably no better than CoolIT's plate, whose dimensions are undisclosed.
6. LM serviceability is worse than paste.

---

## 7. Product family and applications

| product | core / face | application, what changes |
|---|---|---|
| DD3-T1/T2 lidded GPU (Rubin flat Au lid, MI455X, B300) | R / flat | drop-in channel; PCM, then LM on the Au/Ni lid |
| **DD3-3A bare-die module** (Blackwell-class bare die with stiffener: Lenovo B200 service docs show PCM on the die and putty on surrounding parts [S]; Google TPU bare die since v4 [S]; Jentech's removable-lid Rubin Ultra concept [S]; Maia/Trainium) | R or P / pedestal | per-SKU pedestal map and dam; LM or PCM; sold pre-wetted as a module FRU |
| DD3-3B lid-core for MCL (Rubin Ultra/Feynman; Jentech is co-developing MCL with Nvidia [S]) | P / Cu lid-core | lid-core plus manifold cap supplied to the lid maker or OSAT; indium TIM1 by the OSAT |
| DD3-4 manifold cap for silicon micro-coolers (TSMC IMC-Si, Corintis) | cap only | headers, comb, 10-25 um screen, ports, seal face; standard interface proposed to OCP |
| CPU / NVSwitch / NIC | R, LP 18 mm / flat | lidded parts get Tier 1; bare-die switch ASICs get 3A with PCM |
| wafer-scale / multi-chip (Cerebras-class, 43 W/cm2 over 460 cm2) | R / per-reticle pedestals | tiled engines; per-die LM cells with individual dams; wafer warp handled by per-tile float |
| SiC modules, 800 VDC shelves, EV | de-rated engine (0.2 mm gaps) | **"direct-to-substrate"**: the power-electronics analogue of 3B. The engine face is Ag-sintered (0.005 cm2K/W) to the AMB/DBC copper, deleting baseplate and TIM. WEG 50/50, 65 C inlet, Tj 175 C. Shelves (5-30 W/cm2) use Tier 1. EV is a licensing play |
| RF GaN, laser diodes, co-packaged optics | P / pedestal or CuW face | direct-to-die heritage already exists (CuW flanges); high margin |

**Staying relevant as in-silicon cooling arrives (2028-2030+).** The external plate loses the junction contest but keeps the fluid-delivery problem. In-die channels still need low-dP, heat-map-zoned, uniformly metered flow from 2-4 LPM loops into thousands of 50-100 um passages, plus cleanliness at <= 10-25 um absolute. That is exactly DD3's L0-L3 manifold, comb and screen. DD3 therefore:

1. keeps the manifold cap separable from the 3B generation onward;
2. builds heat-map-to-comb zoning software now (the same asset class as Corintis' topology optimisation);
3. qualifies <= 10-25 um integrated screens and dP-signature monitoring;
4. proposes an OCP "liquid-cooled package interface" (port pitch, seal face, cleanliness class);
5. partners with Corintis or the OSATs rather than competing on in-die channel IP.

The copper engine keeps funding this: single-phase plates are expected to hold most DLC sockets through 2030 [S/KB].

---

## 8. Reliability, qualification and drop-in compatibility

**Drop-in and requirements checklist:**

- OCP PG25 wetted list: bare OFE Cu, 316L, peroxide EPDM; no Al, Zn or brass anywhere in the loop or module.
- Inlet 17-50 C (spec point 45 C).
- Curves published at 0.5-1.5 LPM/kW, with dP at >= 6 points from 25-150 % of rated flow (OCP Cold Plate Test Spec v1.0.0 format, three boundaries including the named UQD).
- He leak <= 1e-5 mbar L/s on 100 % of units.
- Burst >= 3.0 MPa.
- Velocities <= 1.5 m/s.
- Thermal cycling 10-65 C operating and -40/+70 C storage [S].
- Tier 3A is drop-in only on bare-die packages using standard spring retention and the same ports. On lidded parts it falls back to Tier 1/2.

**Liquid-metal-specific reliability:**

| failure mode | design control | qualification |
|---|---|---|
| Cu dissolution (CuGa2) | Ni 5 um electrolytic (k 80; 0.0006 cm2K/W) or W 1 um; no Au anywhere on the plate face | Ni/W consumption by cross-section after 2,000 cycles and 3,000 h at 105 C die-top |
| Au on the die backside | lidless SKU specified without Au BSM (bare Si or Ti/Ni) | wetting and R'' test on the actual die stack |
| migration and pump-out under 20-40 um cyclic gap change | single field inside an FKM dam, capture moat, 30 um BLT | 1,000 power cycles plus 1,000 cycles at 10-65 C on a warped package simulant; dam inspection; R'' drift <= 15 % |
| electrical shorts | conformal coat (parylene/ALD) on passives within 5 mm; dam outside the mold edge | Ga-droplet bias test on a powered daisy-chain substrate |
| freeze/thaw (EGaIn 15.5 C; Galinstan -19 C; Ga expands 3 % on freezing) | Galinstan for shipping and storage | 50 cycles at -40/+70 C storage, then R'' re-measured |
| oxidation | capped pre-wetted FRU, nitrogen-packed | shelf-life test |

**Leak-before-break.** Ductile annealed copper, no brittle braze in the pressure boundary, and burst/MAWP >= 3. A coolant leak at the die-side face is impossible, because the pedestal is the outside of a hermetic sandwich.

**Who owns TIM1, and the qualification path:**

| tier | interface setting Tj | specified by | applied by | qualified / warranted by | our role |
|---|---|---|---|---|---|
| 1 / 2 | OSAT TIM1 plus our TIM2 | silicon vendor (TIM1); Nvidia thermal design guide (TIM2) | OSAT; ODM or us | silicon vendor (package); plate vendor (plate) | plate and interface kit |
| **3A** | **our LM on the die = de facto TIM1** | **module owner** (Nvidia for SXM/puck modules; Google/Microsoft/AWS for their ASICs) | us, factory pre-wetted (preferred), or the ODM at L10 | module owner under its reliability plan (JEDEC-style temperature cycling, power cycling, shock/vibration, HAST); die-warranty indemnity is negotiated | plate, LM recipe, process, data |
| 3B | indium TIM1 | silicon vendor/OSAT | OSAT lid attach | package qualification (JESD22-A104/A103/A110, B112) | lid-core supplier to the lid maker; cap supplier |
| 4 | none | silicon vendor plus Corintis/TSMC | foundry/OSAT | silicon vendor | manifold cap, screen, loop |

Access path:

- **Nvidia:** plate purchasing is centralised for Rubin, with Jentech, AVC, Cooler Master and Delta as Group-A [S]. The realistic route is a manufacturing or licence partnership with a Group-A house (Jentech for 3B), Nvidia thermal-design-guide compliance, then EVT/DVT (9-12 months).
- **First 3A socket:** a hyperscaler ASIC, where the buyer owns both the package and the plate, so TIM1 ownership is clean.

**Test plan:**

1. TTV-A parity on CoolIT's conditions.
2. TTV-B, 350 W/cm2 patches.
3. **TTV-C**: real-silicon thermal test dies with diode sensors, tiled to 26 x 33 mm, 4 per substrate, with HBM dummies and a stiffener on a warping 120 mm substrate. This is the only test that measures the junction claim.
4. dP at three boundaries.
5. Proof, burst, He leak, 10,000 pressure cycles.
6. ASTM D5470 at clamp pressure, at beginning of life and after cycling.
7. Fouling rig behind 50 and 33 um screens.
8. Shock/vibration with die-strain gauges and post-test acoustic microscopy.
9. Independent repeat of the headline point at a university or national lab.

**Service life.** 10-year plate design life. The LM interface has a 5-year inspection interval, with a module-level FRU swap: the plate is pre-wetted and the old plate is refurbished at depot. The screen is serviced on its dP signature.

---

## 9. IP posture

**Expired foundations we build on:** Tuckerman-Pease in-die/under-die microchannels (US 4,450,472, 1984); Harpole/TRW manifold microchannel (US 5,088,005); Walpole/MIT alternating flow; Creare normal-flow laminates; IBM cross-hatch distribution and 1980s TCM direct-contact cooling; Cooligy hot-spot and multi-level manifold families (2003-06 filings, verify each expiry); TWI friction-stir welding; diffusion bonding as public process art [S/KB].

**Avoid:**

- a single central inlet slot over one fin field (CoolIT US 8,746,330 family, ~Aug 2028);
- discrete microjets onto bare die (JetCool SmartLid / Flex, Frore);
- Si fusion-bonded micro-coolers (TSMC IMC-Si) and in-die channel topologies (Corintis, Microsoft);
- microchannel-lid and removable-lid constructions (Jentech, Nvidia, Intel liquid-cooled IHS);
- sensors or valves in the plate (Nvidia "intelligent cold plate");
- CoolIT's compliant-member family (US 11,725,886 / 12,188,733): our float must stay a conventional spring-screw gimbal and be checked against it.

**Claim (US provisionals before disclosure, then PCT):**

1. single-field LM over the whole molded interposer top, with perimeter dam, capture moat and a hard-stop load path through the stiffener;
2. a post-bond-machined stepped pedestal in a tied HMMC sandwich, crowned to hot-state package metrology;
3. one bonded engine whose tier is set by face finishing (process and product-family claim);
4. a factory pre-wetted, capped LM plate as a field-replaceable unit;
5. a separable heat-map-zoned manifold cap with an integrated screen, as a standard interface to silicon micro-coolers;
6. direct-to-substrate sintered engines for SiC modules.

FTO opinion: US$60-120k over 10-14 weeks, covering US, TW, CN, EP and VN.

---

## 10. Risks, experiments and roadmap

| risk | likelihood / impact | mitigation |
|---|---|---|
| LM containment and ageing at 80-100 cm2 under cyclic warpage; no public data exist [P] | high / product-defining | experiment 1; W barrier; PCM fallback costs 14 K at 350 W/cm2 but keeps the product |
| no lidless package access; silicon vendors gatekeep | high / schedule | TTV-C on our own silicon; hyperscaler ASIC first; Jentech partnership for 3B |
| TIM1 ownership and die-warranty liability | medium-high / commercial | pre-wetted FRU as a part number; module-owner qualification; insurance/indemnity cap |
| gallium supply: China's US export ban is suspended only until 27 Nov 2026 and licensing still applies [S] | medium / cost, availability | ~2 g per plate (200 kg/yr at 100k); dual-source non-Chinese Ga (recycled, Japan/Germany); 12-month stock; PCM fallback |
| die crack or bump damage from load or shock | low-medium / severe | 0.04-0.10 MPa preload, stiffener hard stops, strain-gauged shock test |
| warpage larger than assumed | medium / +5-10 K | hot-state metrology per SKU; LM window to 50 um |
| in-die cooling leapfrogs 3A | certain post-2029 / segment | manifold-cap strategy (section 7) |
| fouling of the 0.15 mm core | medium / life | screen, bleeds, dP signature [P] |
| 3B CTE fatigue with a copper lid-core | medium | thick indium; CuW option for > 70 mm spans; JEDEC temperature cycling on coupons |

**Five experiments that retire the most risk:**

1. **LM ageing and containment rig** (14 weeks, start first). 100 mm warped package simulants (Si on an organic substrate with known bow), Ni vs W faces, Galinstan vs EGaIn, 2,000 cycles at 10-65 C, 1,000 power cycles at 95 C die-top, 50 storage cycles at -40/+70 C. Measure R'' drift, migration, and intermetallic thickness by cross-section.
2. **Hot-state warpage metrology** (6 weeks). Shadow moire at 25-125 C on 3 lidless CoWoS-class packages, or on TTV-C. Fix the crown and confirm the float plus crown holds +/-15 um.
3. **TTV-C junction test** (16 weeks). Tiled thermal-test-chip dies, 3A vs Tier 2 vs Tier 1 on the same engine at 117-350 W/cm2. Proves the 21-33 K junction gain.
4. **Load, shock and vibration** (8 weeks). Strain-gauged dies, pressure film, 50 g shock, acoustic microscopy for die and bump damage.
5. **3B lid-core coupons** (12 weeks). Copper lid-core soldered with 150-200 um indium to 26 x 33 mm Si dummies; 1,000 cycles at -40/+125 C; acoustic microscopy for voids and cracks; tie-bond burst.

The engine-level experiments (water-table uniformity, fouling, bond coupons) are shared with the engine programme and not repeated here.

**Roadmap (months from go):**

| months | work |
|---|---|
| M0-3 | Engine design shared with Tier 1/2; pedestal and dam design; provisionals filed; LM rig and warpage metrology started; LOIs with one hyperscaler ASIC team and one lid maker or OSAT |
| M3-6 | First bonded 3A and 3B parts; TTV-C built; shock tests |
| M6-9 | TTV-C junction data; 1,000-cycle LM readout; lid-core coupons |
| M9-12 | Hyperscaler bare-die EVT samples; OCP-format report; independent-lab repeat |
| M12-15 | DVT: 2,000-cycle LM data, module-owner reliability plan, pilot bond line |
| M15-18 | 3A qualified for one hyperscaler ASIC; 3B lid-core sampled to the lid maker for a 2028 (Feynman-class) package |

3B and 4 then follow the silicon calendar (24-30 months to package qualification).

---

## 11. Scorecard vs CoolIT 15 kW

15 kW, 18 LPM PG25, 45 C inlet, 117 cm2. Conservative = Tier 3A at the Monte Carlo P90, which also equals LM end-of-life at R'' 0.030. Nominal = Tier 3A median, 0.15 mm R core. Stretch = Tier 3A-P (0.10 mm core, <= 33 um loops).

| metric | CoolIT 15 kW | conservative | nominal | stretch |
|---|---|---|---|---|
| average case-to-inlet dT | 34.4 K | <= 24.2 K (-30 %) | **22.3 K (-35 %)** | 19.7 K (-43 %) |
| maximum case-to-inlet dT | 44.2 K | <= 26.4 K (-40 %) | **24.4 K (-45 %)** | 21.8 K (-51 %) |
| T_case,max at 15 kW | 89.2 C | <= 71.4 C | 69.4 C | 66.8 C |
| unit resistance R'' (avg) | 0.269 cm2K/W (reconstruction) | <= 0.189 | 0.174 | 0.153 |
| hot spot (max - avg) | 9.8 K | <= 3.0 K | 2.1 K | 1.3 K (flow uniformity verified at 1.06) |
| plate dP at 18 LPM incl. screen | undisclosed (~25 kPa, 17-42) | <= 8 kPa | 5.7 kPa | 4.2 kPa (20 mm ports) |
| plate dP at 36 LPM | ~69 kPa (reconstruction) | <= 25 kPa | 22.4 kPa | 16.3 kPa |
| pumping power at 18 LPM | ~7.4 W | <= 2.4 W | 1.7 W | 1.3 W |
| Q capacity, Tcase,max <= 85 C | ~12.7 kW | >= 27 kW | 30.8 kW | 38.9 kW |
| flow to match 34.4 K average | 18 LPM | <= 10.5 LPM (PCM fallback) | 8.2 LPM (0.55 LPM/kW) | - |
| Tj-to-inlet, 350 W/cm2 reticle die (real package) | 139 K (CoolIT-like lidded paste) | 78 K (3A with PCM) | **64 K** | 56 K |
| max die flux at Tj <= 105 C, 45 C inlet | 129 W/cm2 | 261 W/cm2 | 323 W/cm2 | 382 W/cm2 |
| HBM Tj at 40 W/cm2 | ~105 C | 91 C (putty) | 81 C (LM) | 81 C |
| Rubin 2.3 kW, Tj-to-inlet at die average | 53 K | 39 K (Tier 1) | 28 K | 26 K (P core) |
| factory cost, 100k/yr (Rubin-Ultra class) | ~US$105 skived; ASP ~US$400 | ~US$195 | ~US$175 | ~US$185 (P core) |
| height / mass | undisclosed | 25 mm / 2.4 kg | 21 mm / 2.3 kg | 17 mm (RU) / 1.5 kg; no claimed win |
| serviceability | paste, field | PCM, field | LM pre-wetted FRU, depot | same; worse than paste |

**Sources (web, as retrieved):**

- Kuo via CTEE (Rubin lid / MCL timing): https://www.ctee.com.tw/news/20260107701081-430704
- TechNews, Rubin microchannel lid: https://technews.tw/2025/09/04/nvidia-rubin-gpu-use-microchannel-lid/
- Taiwan News, Jentech removable-lid Rubin Ultra: https://www.taiwannews.com.tw/news/6435018
- Wccftech, Rubin Ultra cooling: https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/
- TVBS, Group-A suppliers: https://news.tvbs.com.tw/english/3188903
- SemiWiki, TSMC IMC-Si on CoWoS (ECTC 2025): https://semiwiki.com/semiconductor-manufacturers/tsmc/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/
- HPCwire, Microsoft/Corintis microfluidics: https://www.hpcwire.com/2025/09/25/microfluidics-offers-3x-better-cooling-than-cold-plates-microsoft-says/
- IEEE Spectrum, Corintis: https://spectrum.ieee.org/microfluidics-cooling-ai-chips-corintis
- Lenovo SR780a V3 B200 cold-plate service (PCM/putty): https://pubs.lenovo.com/sr780a-v3/remove_front_b200_gpu_cold_plate_module
- ServeTheHome, Google TPU bare die: https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/
- Electronics Cooling, ORNL CuW plates: https://www.electronics-cooling.com/2026/04/high-performance-copper-tungsten-cold-plates-for-direct-to-chip-single-phase-liquid-cooling/
- OCP Cold Plate Test Spec v1.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- Fastmarkets, gallium export-ban suspension to 27 Nov 2026: https://fastmarkets.com/insights/china-suspends-export-prohibition-on-superhard-materials-us
- Internal: `physics/SYNTHESIS-physics.md`, `tim-and-direct-to-die.md`, `nonuniform-heatmap.md`, `base-stress-stiffness.md`, `fouling-filtration.md`, `manifold-maldistribution.md`; `research/gap-tim2-…`, `gap-nvidia-rubin-…`, `manufacturing-cost.md`, `ip-landscape.md`, `market-business.md`.
