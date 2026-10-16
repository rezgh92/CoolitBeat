# CoolIT Systems public cold-plate performance claims: every number, derived metrics, and what was not disclosed

Prepared 2026-10-13 for the benchmark-definition step of the "beat the CoolIT 15 kW coldplate" program.
Method: ~40 web searches (standard + extended). Direct fetch of CoolIT PDFs (4 kW tech brief, Split-Flow brief, skived brief) was blocked by the container network policy, so brief contents are reconstructed from search-index excerpts and press reprints; the 15 kW brief was read in full from the supplied PDF text. Vendor claims are labelled (V); independent/peer-reviewed/standards data are labelled (I). All derived values are ours and marked (D).

---

## 1. Executive summary

- CoolIT's 15 kW demonstration (announced 1 June 2026, Computex) discloses only: 15 kW TDP on a 4-heater ceramic TTV, 3 plates x 8 thermocouples, water-glycol at 1.2 LPM/kW (= 18 LPM), 45 C inlet, average case-to-inlet dT 34.4 C (26.8-44.2 C), average Tcase ~80 C, Split-Flow architecture, "standard thermal paste". It does **not** disclose pressure drop, footprint, heater/die area, fin geometry, coolant mix, flow per plate vs. per zone, outlet temperature, TIM type/impedance, or heat-capture fraction.
- Derived (D): average case-to-inlet resistance **0.00229 K/W** (per-plate 0.00217-0.00237; worst TC 0.00295; best 0.00179). Fluid caloric rise at 18 LPM is **~12.6 K (PG25) / ~12.1 K (water)**, so outlet ~57.5 C and mean fluid ~51 C; case-to-mean-fluid resistance ~0.00187 K/W. Hot-spot spread within one plate is **14.7-16.6 K**; the same TC position (TC5) is hottest on all three plates (41.5/44.2/44.0 C), and plate-to-plate spread at a fixed TC reaches **10.1 K (TC8)**, which points to TIM/mounting variability rather than flow design.
- The 4 kW plate (13 March 2025) is the only CoolIT plate with a published resistance: **Tr < 0.009 C/W, max-case-to-inlet, TIM included**, 50 x 50 mm footprint, 4.28-6.06 LPM, 93.4 % heat capture at 4.28 LPM and ~97.3 % at 6.06 LPM, **8 psi (55 kPa) full-loop dP incl. fittings and QDs**, ~200 W/cm2 (Tom's Hardware). Implied unit resistance **~0.18 cm2-K/W** including TIM (D, assumes ~20 cm2 heater).
- If the 15 kW plate's unit resistance is similar to the 4 kW plate ("same architectural foundation"), the heater array is ~60-80 cm2 (roughly 78-89 mm square) and the mean heat flux ~190-250 W/cm2 (D). This is an inference, not a disclosed value.
- A TIM bound (D): at those heat fluxes, every 0.05 cm2-K/W of paste impedance costs ~9-12 K of the 34.4 K budget. Standard paste is therefore likely the single largest resistance in the CoolIT stack after the fluid rise; this is the cheapest lever for a competitor to pull.
- CoolIT's own "industry standard" flow figure moved from **1.5 LPM/kW (March 2025, "semiconductor industry recommended")** to **1.2 LPM/kW (June 2026, "industry standard flow rate for AI systems")**. Independent references: OCP CDU methodology and CoolIT's own CHx1000 CDU use 1.5 LPM/kW; an Electronics Cooling (June 2025) article calls 1.2 LPM/kW at 45 C "a common industry standard that many CDUs can meet"; OCP OAI guideline recommends 7.5-12 C coolant rise (1.2 LPM/kW with PG25 gives ~12.6 K, i.e., at/above the top of that window).
- The "2-2.5 kW single-phase limit" CoolIT argues against is traceable to IDTechEx ("struggles at ~1.5 kW, 2.0 kW upper limit") and to CoolIT's own 2025 framing ("1,500-2,000 W"); no source states 2.5 kW as a single-phase limit (2.5 kW appears only as a Wiwynn two-phase cold-plate capability). An OCP white paper (Oct 2026) refers to a single-phase physics boundary "roughly 4,000 W" (fragment only).

---

## 2. Timeline of CoolIT cold-plate claims

| Date | Item | Headline numbers | Source |
|---|---|---|---|
| Feb 2021 | Skived Coldplate Technical Brief (RX3) | <= 0.03 C/W "or lower" for Ice Lake-class CPUs, flow rate not stated; fins+base one piece; centre of fin array removed for Split-Flow (V) | coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf ; datacenterknowledge.com/cooling/skived-coldplates-technical-brief |
| May 2024 | Split-Flow Technology Tech Brief (3 pp.) | Qualitative only: "halves the coolant's distance across the microchannels", lower flow impedance, lower case-to-fluid resistance; no dP or R numbers in the retrievable text (V) | coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf ; scribd.com/document/1025620831 |
| 9 May 2024 | OMNI All-Metal Coldplates launch | ">1,500 W TDP", ">300 W/cm2", "up to 60 % lower thermal resistance vs standard microchannel coldplates"; single-metal unibody, no braze, "aerospace-grade metallic sealing"; no test conditions (V) | storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled ; coolitsystems.com/omni/ |
| Dec 2024 | CHx1000 CDU | 1,000 kW at 1.5 LPM/kW, 3 C approach (V) | hpcwire.com/2024/12/10/ai-performance-reliability-serviceability-with-coolits-chx1000-cdu/ |
| 13 Mar 2025 | 4000 W coldplate PR + Tech Brief R2 (14 Mar 2025) | Tr < 0.009 C/W (max case to inlet, incl. TIM); 8 psi full loop incl. QDs; 97 %+ capture at 6 LPM (= 1.5 LPM/kW); 50 x 50 mm; 4.28-6.06 LPM; "Split-Flow 30 % better thermal and flow performance" (V) | prnewswire.com/news-releases/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership-302401512.html ; coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf |
| 2025 | Tom's Hardware state-of-play | CoolIT 4 kW Split-Flow plate "heat flux shy of 200 W/cm2"; next-gen plates from Accelsius and CoolIT "up to 300 W/cm2" (press, citing vendors) | tomshardware.com/pc-components/cooling/the-data-center-cooling-state-of-play-2025-... |
| Jun 2025 | Manufacturing | production scaled "25X in 18 months"; Starfield plant 112,000 sq ft; ~150,000 sq ft mfg+R&D; 6 MW thermal test rig (V) | hpcwire.com/2025/06/25/coolit-systems-scales-north-american-manufacturing-to-cool-ais-next-wave/ ; datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale |
| 19-20 Mar 2026 | Ecolab to acquire CoolIT | US$4.75 B; ~US$550 M NTM sales; 29x NTM adj. EBITDA; closed ~2 Jul 2026; YTD sales +100 % | businesswire.com/news/home/20260319353197/en/ ; s204.q4cdn.com/.../Ecolab-Closes-CoolIT-Acquisition-... |
| 1 Jun 2026 | 15 kW coldplate PR + Tech Brief | see Section 3 (V) | prnewswire.com/news-releases/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-roadmap-far-beyond-2030-302787344.html ; coolitsystems.com/resources/news/15kw-coldplate/ |
| 28 Jul 2026 | Blog "Behind the world's most advanced AI coldplates" | 150+ liquid-cooling patents; six generations of supercomputers; co-design silicon-to-rack (V) | coolitsystems.com/resources/news/coolit-behind-the-worlds-most-advanced-ai-coldplates/ |

---

## 3. The 15 kW coldplate (June 2026): disclosed numbers and derived metrics

### 3.1 Disclosed (from the tech brief and PR)

| Quantity | Value | Note |
|---|---|---|
| TDP on TTV | 15,000 W | 4 ceramic heaters "simulating GPU and HBM zones" |
| Plates tested | 3 | 8 thermocouples each, "directly at the heater surface" |
| Coolant | "standard water-glycol" | mix ratio not stated (PG25 assumed below) |
| Flow | 1.2 LPM/kW => 18 LPM | "industry standard flow rate for AI systems" |
| Inlet temperature | 45 C | "warm-water" environments; ASHRAE W45 |
| Average case-to-inlet dT | 34.4 C | per-plate 32.5 / 35.2 / 35.6 C |
| Range of 24 readings | 26.8-44.2 C | sd 5.04 K (D) |
| Average Tcase | ~80 C | 45 + 34.4 = 79.4 C |
| Architecture | Split-Flow, "industry-leading internal geometries, proven mass-manufacturing techniques, standard thermal paste" | design + CFD in late 2025 |
| Scaling claims | "nearly 4x" the 4 kW plate (3.75x); ">10x today's top-end AI GPUs" (15/1.4 kW GB300 = 10.7x) | |
| Roadmap | further R and dP reduction; direct-to-die and micro-channel lids; 100 % heat capture; >1 MW racks | no numbers |
| TDP chart | processor TDP trajectory plotted to ~8,000 W by 2028; 750 W air-cooling threshold | CoolIT projection |

Press coverage found (all repeat the PR; none adds footprint, dP or heater size): PR Newswire / Yahoo Finance (1 Jun 2026), HPCwire (4 Jun 2026), StorageReview, Data Center Dynamics (EN/ES; adds Rubin TDP "up to 2,300 W" and the Ecolab/KKR ownership history), Electronics360 (Computex 2026; adds IDTechEx 1.5/2.0 kW limit framing), letsdatascience, datacenternews.ca, whtop, Data Center Richness (Substack). Not found: Tom's Hardware, The Register, The Next Platform, ServeTheHome coverage of the 15 kW plate (domain-restricted search returned only 4 kW coverage).

### 3.2 Per-thermocouple analysis of CoolIT's table (D)

| Position | CP1 | CP2 | CP3 | Avg | Plate-to-plate spread |
|---|---|---|---|---|---|
| dT1 | 26.8 | 34.7 | 32.3 | 31.3 | 7.9 |
| dT2 | 29.9 | 33.5 | 34.7 | 32.7 | 4.8 |
| dT3 | 31.5 | 37.6 | 39.0 | 36.0 | 7.5 |
| dT4 | 34.6 | 39.3 | 39.0 | 37.6 | 4.7 |
| dT5 | 41.5 | 44.2 | 44.0 | 43.2 | 2.7 |
| dT6 | 29.0 | 33.6 | 35.2 | 32.6 | 6.2 |
| dT7 | 29.0 | 30.8 | 32.6 | 30.8 | 3.6 |
| dT8 | 37.7 | 27.6 | 27.7 | 31.0 | 10.1 |
| Avg | 32.5 | 35.2 | 35.6 | 34.4 | |
| In-plate max-min | 14.7 | 16.6 | 16.3 | 12.4 (of averages) | |

Observations: TC5 is the hottest location on every plate (consistent, so it is a design/flow-path hot spot, probably the zone farthest downstream or the highest-flux heater); TC8 on CP1 (37.7 C) vs CP2/CP3 (27.6/27.7 C) is a 10 K outlier that can only be TIM/clamping/flatness variability; CP1 is 3 K better on average than CP2/3. For a benchmark, use CoolIT's **average 34.4 K** as the headline and **worst-TC 44.2 K** as the hot-spot figure.

### 3.3 Derived thermal metrics (D)

| Metric | Value | Basis |
|---|---|---|
| R_case-inlet, average | 0.00229 K/W | 34.4/15,000 |
| R_case-inlet, per plate | 0.00217 / 0.00234 / 0.00237 K/W | |
| R_case-inlet, worst TC | 0.00295 K/W | 44.2/15,000 |
| R_case-inlet, best TC | 0.00179 K/W | 26.8/15,000 |
| Fluid caloric rise, PG25 | 12.6 K | 18 LPM, rho ~1.01 kg/L, cp 3.94 kJ/kg-K (Dow DOWFROST LC-25 at 50 C) |
| Fluid caloric rise, water | 12.1 K | rho 0.99, cp 4.18 |
| Outlet / mean fluid | ~57.5 C / ~51.3 C | |
| R_case-to-mean-fluid | ~0.00187 K/W | (34.4 - 6.3)/15,000 |
| 4 kW plate for comparison | < 0.009 K/W (max case) at 1.5 LPM/kW | 3.1x higher absolute R than the 15 kW average, as expected for 3.75x the power on a larger area |

Unit (area-normalised) resistance and heat flux cannot be computed exactly because the heater area is undisclosed. Scenario table:

| Assumed heated area | Mean heat flux | R'' avg (cm2-K/W) | R'' worst-TC (cm2-K/W) |
|---|---|---|---|
| 50 cm2 (71 mm sq) | 300 W/cm2 | 0.114 | 0.147 |
| 64 cm2 (80 mm sq) | 234 W/cm2 | 0.147 | 0.189 |
| 81 cm2 (90 mm sq) | 185 W/cm2 | 0.185 | 0.239 |
| 100 cm2 (100 mm sq) | 150 W/cm2 | 0.229 | 0.295 |
| 150 cm2 | 100 W/cm2 | 0.343 | 0.443 |

Cross-check: the 4 kW plate at ~200 W/cm2 implies ~20 cm2 heated area and R'' ~0.18 cm2-K/W (max-case, TIM included, 1.5 LPM/kW). If the 15 kW plate shares that unit performance, its heated area is ~61 cm2 (worst-TC basis) to ~79 cm2 (average basis), i.e., roughly 78-89 mm square, with mean heat flux ~190-250 W/cm2. That is consistent with Tom's Hardware's "shy of 200 W/cm2" (4 kW) and "up to 300 W/cm2" next-gen statements. Treat as an inference.

### 3.4 TIM share bound (D)

At heat flux q'' the TIM temperature drop is q'' x R''_TIM. Shin-Etsu X23-7921-5 grease is 5.0 mm2-K/W (0.05 cm2-K/W) at 25 um bond line / 20 psi; X23-8117 is 6.1 mm2-K/W; Honeywell PTM7950 phase-change is 0.04-0.08 C-cm2/W. Large AI packages with lid warpage usually run thicker bond lines than 25 um.

| TIM R'' | Heated area 61 cm2 | 80 cm2 | 100 cm2 |
|---|---|---|---|
| 0.05 cm2-K/W | 12.3 K (36 % of 34.4) | 9.4 K (27 %) | 7.5 K (22 %) |
| 0.10 cm2-K/W | 24.6 K (71 %) | 18.8 K (55 %) | 15.0 K (44 %) |

Since total case-to-inlet dT is only 34.4 K and ~6 K of that is fluid rise to mean, the paste CoolIT used must be <= ~0.1 cm2-K/W effective (or the heated area is >= 100 cm2). Either way, the TIM is plausibly 20-50 % of the stack. Replacing paste with a <= 0.02 cm2-K/W interface (sintered/liquid metal/direct-to-die) is worth 5-15 K at these fluxes before any fin redesign.

### 3.5 Pressure drop and pumping power (not disclosed; scenarios, D)

The only CoolIT dP datum is 8 psi = 55.2 kPa for the 4 kW plate's full loop (fittings + QDs) at presumably 6 LPM, i.e., hydraulic power 5.5 W (0.14 % of 4 kW). For 15 kW at 18 LPM (3.0e-4 m3/s):

| Plate/loop dP | Hydraulic power | % of 15 kW | Electrical at 30 % pump eff. |
|---|---|---|---|
| 30 kPa | 9 W | 0.06 % | 30 W |
| 55 kPa | 17 W | 0.11 % | 55 W |
| 100 kPa | 30 W | 0.20 % | 100 W |
| 150 kPa | 45 W | 0.30 % | 150 W |

Reference budgets: OCP cold-plate test spec runs dP at 45 +/- 2 C at six flow rates from 25 % to 150 % of rated flow; the Electronics Cooling (Jun 2025) worked example budgets ~18 psi (124 kPa) for a whole rack at 1.2 LPM/kW; the OCP CDU methodology lists >= 40 psi TCS head at 1.5 LPM/kW; vendor GB200/GB300 plates quote < 20 kPa at 1.8 LPM, 35 kPa at 2.5 LPM, 12 kPa at 1.7 LPM.

---

## 4. The 4 kW coldplate (March 2025): all numbers

| Quantity | Value | Source |
|---|---|---|
| Rated TDP | 4,000 W ("more than double the previously accepted 1,500-2,000 W limit") | CoolIT PR 13 Mar 2025 |
| Footprint | 50 x 50 mm ("slightly smaller than a Blackwell GPU") | DCD; tech brief R2 |
| Thermal resistance | Tr < 0.009 C/W, **max case temperature to fluid inlet, includes TIM** | tech brief R2 (14 Mar 2025) |
| Implied dT at 4 kW | < 36 K (D) | |
| Flow range tested | 4.28-6.06 LPM | tech brief R2 |
| Heat capture | 93.4 % at 4.28 LPM (TTV ~4,006 W); 94.1 % at 4.34 LPM; "97 %+" / 97.3 % at 6.06 LPM; tested **without** convection barrier or insulation | tech brief Table 1; PR |
| Flow basis | 6 LPM = "1.5 LPM/kW, the semiconductor industry's recommended flow rate for high-wattage chips" | PR |
| Full-loop dP | 8 psi (55.2 kPa) incl. fittings and QDs | PR; StorageReview |
| Heat flux | "shy of 200 W/cm2" | Tom's Hardware 2025 state-of-play |
| Coolant | "water or water-glycol"; inlet temperature **not stated** in retrievable text | |
| Fluid rise (D) | 9.5 K at 6.06 LPM, 13.5 K at 4.28 LPM (water) | |
| Unit R'' (D) | ~0.18 cm2-K/W incl. TIM (assuming ~20 cm2 heater from 200 W/cm2) | |
| Hydraulic power (D) | 5.5 W full loop at 6 LPM | |
| Built/tested | in-house at Liquid Lab Innovation Center (CNC + skiving); TTV also built in-house | tech brief |
| Press | PR Newswire, StorageReview, DCD, Tom's Hardware, TweakTown, KitGuru, ServeTheHome, HPCwire (sponsored, 31 Mar 2025), insideHPC, SDxCentral, Converge Digest, AIwire (14 Mar 2025), HostingJournalist | |

Comparator (I): OCP OAI guideline reports case-to-inlet 0.015-0.016 C/W "at high flow rates" for a 1 kW OAM with PG25/DI water, 2-5 LPM, phase-change TIM. CoolIT's 4 kW plate at 0.009 C/W on ~4x the power is a large step; the 15 kW plate's 0.0023 C/W is another ~4x.

---

## 5. OMNI, Split-Flow, skived: what the briefs actually quantify

| Claim | Number | Conditions disclosed? | Independent check |
|---|---|---|---|
| OMNI thermal load | > 1,500 W TDP | no | - |
| OMNI heat flux | > 300 W/cm2 | no (hot-spot size, flow, inlet undisclosed) | Tom's Hardware repeats "up to 300 W/cm2" for next-gen CoolIT/Accelsius |
| OMNI vs standard microchannel | "up to 60 % lower thermal resistance" | baseline undefined | none found |
| Split-Flow vs standard | "30 % better thermal and flow performance" / "up to 30 % better coolant flow and heat capture" | no | Kisitu & Ortega (Villanova, InterPACK 2021, NSF PAR 10341820): geometrically identical split-flow and parallel-flow plates have **similar thermal resistance; split-flow has significantly lower pressure drop** (shorter path, half the per-channel flow, thermally developing flow). So the dP claim is better supported than the R claim. |
| Split-Flow patents | US 8,746,330 B2; US 9,603,284; US 12,495,513 "Fluid heat exchanger configured to provide a split flow" | | |
| OMNI construction | single-metal unibody, no braze, metallic seal, "eliminates differential CTE" | | relevant to reliability claims |
| Skived RX3 | <= 0.03 C/W (Ice Lake), "depending on flow rate" | flow not stated | - |
| Supermicro/CoolIT reference CPU plate | 63.0 x 63.0 x 15.68 mm | (older design, not 15 kW) | newegg Supermicro_CoolIT_Whitepaper.pdf |
| CHx1000 CDU | 1,000 kW at 1.5 LPM/kW; 3 C approach | | |

---

## 6. CoolIT's framing statements cross-checked

| CoolIT statement | Where | Independent status |
|---|---|---|
| "1.2 LPM/kW is the industry standard flow rate for AI systems" (2026) | 15 kW brief | Electronics Cooling (Jun 2025): "a common industry standard that many CDUs available today can meet is 1.2 LPM/kW for 45 C inlet"; vendor/trade sources also quote 1.25-2.0 LPM/kW with 1.5 typical; OCP CDU methodology recommends 1.5 LPM/kW; CoolIT CHx1000 rated at 1.5 LPM/kW. No OCP/ASHRAE/NVIDIA document codifies 1.2. |
| "1.5 LPM/kW is the semiconductor industry's recommended flow rate" (2025) | 4 kW PR | OCP OAI guideline: 1-2 LPM per OAM, ~1.5 LPM/kW giving ~10 C rise, recommended 7.5-12 C rise. |
| 45 C inlet / W45 | both briefs | ASHRAE Thermal Guidelines 5th ed. (2021) classes W17/W27/W32/W40/W45/W+; W45 = 45 C supply allowable. NVIDIA GB200 NVL72 (QCT whitepaper; DCD quoting Ian Buck): max inlet 45 C, max return 65 C, up to ~130 LPM/rack. |
| "widely claimed limits of 2 to 2.5 kW" (2026) / "1,500-2,000 W" (2025) | briefs | IDTechEx: single-phase "begins to struggle ~1,500 W, 2,000 W upper limit"; two-phase large-scale from 2027. No source states 2.5 kW as a single-phase limit. Wiwynn two-phase plate: 2.5 kW from a die at 125 W/cm2, 45 C boiling point. ZutaCore two-phase: 2,800 W/chip. OCP "Thermal Boundaries in AI Infrastructure" (Oct 2026): single-phase cold plate boundary "roughly 4,000 W" (fragment; basis unclear). |
| "750 W = forced-air limit; mainstream GPUs exceeded it in 2024" | 15 kW brief | consistent with B200 ~1,000-1,200 W, GB300 1.4 kW (TweakTown GTC 2025). |
| ">10x today's top-end AI GPUs" | 15 kW PR | GB300 1.4 kW -> 10.7x. Analyst (Ming-Chi Kuo via CTEE/CLS): Vera Rubin VR200 NVL72 Max Q ~1.8 kW / Max P ~2.3 kW per GPU, 190/230 kW rack, micro-channel cold plate + gold-plated lid; micro-channel lid for 2.3 kW not before 2H 2027. DCD: Rubin "up to 2,300 W". AMD MI455X (Helios): ">2 kW" per GPU (secondary). Rubin Ultra/Kyber: ~600 kW rack (2027). |
| DLC TCS market: > US$5 B (2025), > US$11 B (2026) | 15 kW brief | CoolIT's own market sizing; no independent check. |

---

## 7. Independent and third-party comparators (for calibrating "beat in every aspect")

| Source | Device / test | Numbers |
|---|---|---|
| OCP OAI Liquid Cooling Guidelines (Mar 2023) (I) | 1 kW OAM, PG25, 2-5 LPM, phase-change TIM | case-to-inlet 0.015-0.016 C/W at high flow; DI water better; 1-2 LPM per OAM; 7.5-12 C rise target |
| ORNL / IJHMT 2025 (I) | 75 x 75 mm Cu diamond pin-fin plate, 1 kW (17.8 W/cm2), water, 3 LPM | chip-to-coolant incl. TIM 6.9 K/kW (Cu), 9.0 K/kW (CuW); dP 9.0 kPa; 15 % lower R than straight microchannel; pins H 4 mm, S 0.5 mm, 1 x 4 mm |
| ToneCooling GB300 kit (V) | GPU plate 1,067 W, 1.7 LPM | measured 0.0130-0.0133 C/W; dP 12.06 kPa; design target < 40 kPa at 3 LPM |
| ToneCooling/others GB200 (V) | 2,700 W superchip plate | 1.8 LPM, < 20 kPa; alt. 35 kPa at 2.5 LPM; target <= 0.03 C/W base-to-coolant |
| JetCool SmartPlate RTX PRO 6000 (V) | 600 W, PG25 40 C, 0.6-1.8 LPM | junction-to-fluid 0.040-0.058 C/W |
| Wakefield on-chip plate (V) | 700 W, 1.6 LPM | 0.0267 C/W |
| TSMC direct-to-silicon on CoWoS (ECTC 2025) (I) | 3.3x-reticle test package | > 2.6 kW sustained, dT < 63 C (fluid-to-junction basis unclear) |
| Wiwynn two-phase (V) | die-level | 2.5 kW at 125 W/cm2, 45 C saturation |
| Parallel two-phase GPU plates (ScienceDirect 2026) (I) | R245fa, 8 plates | 2,300 W/chip (~300 W/cm2), total R order 1e-3 C/W |
| Kisitu & Ortega 2021 (I) | split-flow vs parallel microchannel | similar R, lower dP; optimum channel aspect ratio ~12 |
| Electronics Cooling Jun 2025 (I-ish, trade) | DLC design guidance | 1.2 LPM/kW at 45 C "common standard CDUs meet"; 96 LPM for 80 kW rack; ~18 psi rack budget |
| OCP Cold Plate Test Spec v1.0.0 (Aug/Sep 2026) (I) | method only | dP test at 45 +/- 2 C, >= 6 flow points 25-150 % of rated; R = (Tcase - Tinlet)/P at multiple flows with recommended TIM; burst > 20 bar example; He leak <= 1e-5 mbar-L/s; cycling 10-65 C and -40/+70 C |

Note on units: CoolIT publishes absolute C/W; OCP's new test spec also uses absolute case-to-inlet R. For cross-footprint comparison our program should report both absolute R (K/W) and unit R'' (cm2-K/W) at a stated heater area, plus dP at a stated LPM/kW and 45 C.

---

## 8. What CoolIT did NOT disclose (15 kW brief)

1. Pressure drop (plate or loop) at 18 LPM; pumping power. (The 4 kW plate's 8 psi is the only dP ever published.)
2. Coldplate footprint and the TTV heated area / die-emulation dimensions; hence heat flux and unit resistance are unknown (inference: ~60-80 cm2, ~190-250 W/cm2).
3. Heater layout and power split among the four heaters (GPU vs HBM zones), and which TC sits on which zone; which zone TC5 (hottest) represents.
4. Fin/channel geometry (fin pitch, height, thickness), manufacturing route for this plate (skived vs machined vs other), material (copper assumed), and whether it is a single Split-Flow plate or a multi-zone/manifolded plate.
5. TIM identity and impedance; bond-line thickness; clamping load; TIM share of the 34.4 K.
6. Coolant glycol fraction; outlet temperature; measured heat-capture fraction; whether thermocouple readings are steady-state averages.
7. Whether 1.2 LPM/kW was applied per plate (18 LPM through one plate) or per zone/channel group.
8. Any variation study (flow sweep, inlet sweep) and the R vs flow curve; only one operating point is given.
9. Reliability data: burst/proof pressure, cycling, corrosion/erosion at the implied channel velocities, long-term TIM pump-out at 15 kW thermal cycling.
10. Cost, mass, height (1U/2U fit), and manufacturing yield for the 15 kW design.
11. Why the three plates differ by up to 10 K at the same TC (assembly variability is not discussed).
12. Independent validation: none exists for any CoolIT plate; all data are CoolIT Liquid Lab measurements.

---

## 9. Benchmark card to carry into design (proposed numbers to beat)

| Metric | CoolIT 15 kW value | Basis | Our "beat" threshold suggestion |
|---|---|---|---|
| Power | 15 kW single plate | disclosed | >= 20-30 kW demonstrated, 15 kW at margin |
| Flow | 1.2 LPM/kW (18 LPM), 45 C inlet, water-glycol | disclosed | <= 1.0 LPM/kW at 45 C for same Tcase (i.e., lower pumping energy and CDU sizing) |
| Avg case-to-inlet dT | 34.4 K | disclosed | <= 25 K (R <= 0.00167 K/W) |
| Worst-TC dT | 44.2 K | disclosed | <= 30 K and in-plate spread <= 6 K (CoolIT: 14.7-16.6 K) |
| Unit R'' incl. TIM | ~0.14-0.19 cm2-K/W (inferred) | D | <= 0.08-0.10 cm2-K/W via low-impedance TIM + enhanced convection |
| Plate dP | undisclosed; 4 kW loop 55 kPa | 4 kW datum | publish plate dP <= 35 kPa at 1.0-1.2 LPM/kW with QD-inclusive loop <= 70 kPa |
| Hydraulic power | ~10-30 W (scenario) | D | <= 10 W at 15 kW (<= 0.07 %) |
| Plate-to-plate repeatability | up to 10 K at a TC | disclosed table | <= 3 K |
| Heat capture | 15 kW: n/a; 4 kW: 93-97 % | | >= 98 % with barrier |
| TIM | "standard thermal paste" | disclosed | <= 0.02 cm2-K/W interface or TIM-less (direct-to-die) option |
| Manufacturing | skiving/CNC, unibody OMNI | | conventional (skived/brazed/FSW/stamped-fin) with stated cost per kW |

---

## 10. Gaps / unknowns

- The 4 kW tech brief's second page (R vs flow chart, inlet temperature, TTV heater size, dP vs flow) could not be read; the 93.4 % / 94.1 % / 97.3 % capture rows and the 4.28-6.06 LPM range come from index excerpts; 97.3 % at 6.06 LPM is reported by secondary summaries and not seen verbatim.
- The 15 kW TTV heated area, heater layout and footprint were not reported by any outlet or image caption found; the 60-80 cm2 / 190-250 W/cm2 estimate is inference from the 4 kW plate's unit performance.
- No 15 kW pressure drop exists anywhere public; the pumping-power table is scenario-based.
- "Standard water-glycol" fraction is not stated; PG25 assumed for the 12.6 K caloric rise (water gives 12.1 K).
- Split-Flow brief (May 2024) charts were not retrievable; the brief appears to be qualitative in its text, and the "30 %" figure comes from the NVIDIA partner page and the 4 kW PR rather than the brief.
- OMNI's ">300 W/cm2" has no public test condition; the "60 % lower R" baseline is undefined.
- Tom's Hardware's "shy of 200 W/cm2" for the 4 kW plate is press paraphrase; CoolIT has not published a heat-flux number for that plate directly.
- The OCP "Thermal Boundaries in AI Infrastructure" (Oct 2026) "~4,000 W" single-phase boundary was seen only as a fragment; Section 8.2 and Appendix B should be read directly.
- Vera Rubin per-GPU TDPs (1.8/2.3 kW) are analyst figures (Kuo) and DCD paraphrase, not NVIDIA-published.
- No independent third-party measurement of any CoolIT plate was found.
- Whether CoolIT's 8 thermocouples are embedded in the heater (as stated, "directly at the heater surface") or on the TIM side matters for comparing to OCP's "case" definition; not clarified.

---

## Sources

CoolIT primary
- 15 kW PR (1 Jun 2026): https://www.coolitsystems.com/resources/news/15kw_press_release/ ; https://www.prnewswire.com/news-releases/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-roadmap-far-beyond-2030-302787344.html
- 15 kW Tech Brief page: https://www.coolitsystems.com/resources/news/15kw-coldplate/ (PDF text supplied locally)
- 4000 W PR (13 Mar 2025): https://www.coolitsystems.com/resources/news/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership/ ; https://www.prnewswire.com/news-releases/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership-302401512.html
- 4000 W Technical Brief R2 (14 Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- 4000 W sponsored article (HPCwire, 31 Mar 2025): https://www.hpcwire.com/2025/03/31/coolit-systems-4000w-breakthroughredefining-single-phase-dlc-for-ultra-high-wattage-ai-processors/
- Split-Flow Tech Brief (May 2024): https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf ; https://www.scribd.com/document/1025620831/Split-Flow-Technology-CoolIT-Tech-Brief
- Skived Coldplate Technical Brief (Feb 2021): https://coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf ; https://www.datacenterknowledge.com/cooling/skived-coldplates-technical-brief
- OMNI page / launch: https://www.coolitsystems.com/omni/ ; https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled
- Coldplate technology page: https://www.coolitsystems.com/coldplate-technology/ ; NVIDIA co-innovation page: https://www.coolitsystems.com/capabilities/co-innovation/nvidia/
- Blog 28 Jul 2026: https://www.coolitsystems.com/resources/news/coolit-behind-the-worlds-most-advanced-ai-coldplates/
- CHx1000 CDU: https://www.hpcwire.com/2024/12/10/ai-performance-reliability-serviceability-with-coolits-chx1000-cdu/
- Manufacturing: https://www.hpcwire.com/2025/06/25/coolit-systems-scales-north-american-manufacturing-to-cool-ais-next-wave/ ; https://www.datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale
- Ecolab acquisition: https://www.businesswire.com/news/home/20260319353197/en/ ; https://www.coolitsystems.com/resources/news/ecolab-to-acquire-coolit-systems/ ; https://pulse2.com/why-ecolab-is-buying-coolit-systems-for-4-75-billion/
- Patents: https://patents.google.com/patent/US8746330B2/en ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9603284 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12495513
- Supermicro/CoolIT whitepaper (63 mm reference plate): https://promotions.newegg.com/b2b/nepro/20-2658/images/Supermicro_CoolIT_Whitepaper.pdf

15 kW press coverage
- https://www.hpcwire.com/off-the-wire/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-roadmap-far-beyond-2030/
- https://www.storagereview.com/news/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-beyond-2030
- https://www.datacenterdynamics.com/en/news/coolit-designs-15kw-coldplate-to-future-proof-liquid-cooling-for-gpus/
- https://electronics360.globalspec.com/article/23837/computex-2026-coolit-pushes-single-phase-dlc-to-15-kw
- https://datacenternews.ca/story/coolit-unveils-first-15kw-coldplate-for-ai-cooling
- https://datacenterrichness.substack.com/p/coolit-unveils-coldplate-for-extreme
- https://letsdatascience.com/news/coolit-systems-demonstrates-15kw-coldplate-for-gpu-cooling-291c89c7
- https://finance.yahoo.com/sectors/technology/articles/coolit-systems-demonstrates-15kw-coldplate-225800443.html

4 kW press coverage
- https://www.storagereview.com/news/coolit-unveils-4000w-cold-plate-setting-new-standard-for-single-phase-direct-liquid-cooling
- https://datacenterdynamics.com/en/news/coolit-details-liquid-cooling-coldplate-able-to-cool-4000w-chips
- https://www.tomshardware.com/pc-components/liquid-cooling/coolit-unleashes-4kw-single-phase-dlc-cold-plate-seemingly-timed-for-nvidia-blackwell-ultra-chips
- https://www.tomshardware.com/pc-components/cooling/the-data-center-cooling-state-of-play-2025-liquid-cooling-is-on-the-rise-thermal-density-demands-skyrocket-in-ai-data-centers-and-tsmc-leads-with-direct-to-silicon-solutions
- https://www.servethehome.com/coolit-shows-off-a-4kw-coldplate-for-liquid-cooling/
- https://www.kitguru.net/components/cooling/joao-silva/coolit-unveils-new-coldplate-capable-of-cooling-4000w-of-heat/
- https://www.tweaktown.com/news/103966/coolit-unveils-4kw-single-phase-dlc-cold-plate-ready-for-nvidia-gb300-blackwell-ultra-ai-gpus/index.html
- https://insidehpc.com/2025/03/coolit-announces-4000w-liquid-cooling-coldplate/ ; https://www.sdxcentral.com/news/coolit-systems-introduces-4000w-coldplate-for-liquid-cooling/ ; https://convergedigest.com/coolit-unveils-4000w-coldplate-advancing-single-phase-liquid-cooling/ ; https://aiwire.net/2025/03/14/coolit-advances-single-phase-direct-liquid-cooling-technology-with-4000w-coldplate
- https://www.scientific-computing.com/article/coldplate-innovation-raising-bar-thermal-ceiling

Standards, independent and comparator data
- OCP OAI System Liquid Cooling Guidelines (Mar 2023): https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/
- OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (2026): https://www.opencompute.org/documents/ocp-cold-plate-test-specification-v1-0-0-pdf-1/
- OCP Cold Plate Development and Qualification white paper: https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/
- OCP L-L CDU Test Methodology (1.5 LPM/kW, 40 psi): https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf
- OCP Thermal Boundaries in AI Infrastructure (Oct 2026): https://www.opencompute.org/documents/white-paper-thermal-boundaries-in-ai-infrastructure/
- OCP PG25 base spec: https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/
- ASHRAE 5th ed. liquid classes: https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/ ; https://www.thegreengrid.org/resources/glossary/W
- Electronics Cooling, "Direct Liquid Cooling for High-Compute Servers" (Jun 2025): https://www.electronics-cooling.com/2025/06/direct-liquid-cooling-for-high-compute-servers/
- Kisitu & Ortega split-flow models (InterPACK 2021): https://par.nsf.gov/biblio/10341820 ; https://www.researchgate.net/publication/356363419
- ORNL Cu/CuW diamond pin-fin plates (IJHMT 2025): https://www.sciencedirect.com/science/article/pii/S0017931025014152 ; https://www.electronics-cooling.com/2026/04/high-performance-copper-tungsten-cold-plates-for-direct-to-chip-single-phase-liquid-cooling/
- IDTechEx two-phase article: https://www.idtechex.com/de/research-article/two-phase-liquid-cooling-the-future-of-high-end-gpus/33862
- Wiwynn two-phase 2.5 kW: https://www.wiwynn.com/whitepapers/innovative-two-phase-cold-plate-solutions-for-future-high-power-ai-chips
- ZutaCore 2,800 W: https://www.storagereview.com/news/zutacore-targets-high-density-blackwell-pcie-servers-with-waterless-two-phase-cooling
- TSMC direct-to-silicon (ECTC 2025): https://semiwiki.com/semiconductor-manufacturers/tsmc/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/
- Two-phase parallel GPU plates 2,300 W: https://www.sciencedirect.com/science/article/abs/pii/S1359431126009294
- NVIDIA GB200 NVL72 45/65 C, 130 LPM (QCT): https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf ; DCD: https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus
- Vera Rubin TDP (Kuo): https://www.ctee.com.tw/news/20260107701081-430704 ; https://www.cls.cn/detail/2250526 ; GB300 1.4 kW: https://www.tweaktown.com/news/103938/
- AMD Helios / MI455X: https://introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026 ; https://wccftech.com/amd-helios-ai-rack-mi455x-6th-gen-epyc-challenging-nvidia/amp/
- Vendor GB200/GB300 cold-plate data: https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ ; https://tonecooling.com/gb200-liquid-cooling-kit/ ; https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm
- JetCool RTX PRO 6000 SmartPlate datasheet: https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
- Wakefield on-chip cold plate: https://www.mouser.in/new/wakefield/wakefield-thermal-on-chip-liquid-cold-plates/
- TIM data: Shin-Etsu X23-7921-5 https://cdn.microsi.com/wp-content/uploads/2019/07/X23-7921-5-TDS-July-2019-.pdf ; X23-8117 https://www.microsi.com/applications-solutions/thermal-interface-material/tim-2/thermal-grease-X23-8117/ ; PTM7950 https://www.caplinq.com/ptm7950-most-thermally-conductive-phase-change-pad-with-very-low-thermal-impedance-that-works-in-vertical-applications-ptm7950.html
- PG25 properties (Dow DOWFROST LC 25): https://www.chempoint.com/en-ca/products/dow/dowfrost-glycol-thermal-fluids/dowfrost-propylene-glycol-thermal-fluids/dowfrost-lc-25
