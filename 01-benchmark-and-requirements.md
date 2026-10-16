# SYNTHESIS: CoolIT 15 kW benchmark, competitive state of the art, and target requirements

> **Status.** Evidence base for the architecture, consolidated 14 Oct 2026 from 22 research reports in `appendix/research/`. Its benchmark facts, requirements and competitor data stand. Its target scorecard (section 9) predates the design panel and verification round: the architecture of record in `03-architecture.md` supersedes those targets.

Chief-of-staff consolidation for the lead thermal architect, 2026-10-14. Inputs: the CoolIT 15 kW tech brief (June 2026), the 12 angle reports and 10 gap reports in `appendix/research/`, `appendix/physics/SYNTHESIS-physics.md` and the corrected scoping model `docs/cooling/model/model_output.md` (+ `coldplate_model.py`). Four WebSearch calls were made this session to resolve contradictions (Section 10, rows C9 and C13).

**How to read the citations.** `[Sn]` is a public source; the URL is in the Source list at the end. Bracketed letters are internal analysis, and every number tagged that way is an **estimate** whose reasoning is in the named file: `[M]` model_output.md / coldplate_model.py; `[P]` SYNTHESIS-physics.md; `[G-TTV]` footprint/heater-map, `[G-DP]` dP and claim baselines, `[G-HYD]` hydraulic reconciliation and UQD losses, `[G-OCP]` OCP documents, `[G-RUB]` Rubin envelope, `[G-COMP]` competitor datasheets, `[G-TIM]` TIM2, `[G-FOUL]` fouling vs filtration, `[G-FTO]` Split-Flow FTO, `[G-COST]` cost/volume (all `gap-*.md`); `[A-...]` angle reports. `[KB]` means background knowledge that no agent could verify. When reports disagree, the later gap reports and `[P]` win over the angle reports, and Section 10 records each case.

**Operating point used throughout:** 15 kW, 18 LPM PG25 (1.2 LPM/kW), 45 C inlet [S1].

---

## 1. The CoolIT 15 kW benchmark

### 1.1 What CoolIT disclosed [S1, S2]

| Item | Value |
|---|---|
| Load / test vehicle | 15 kW; 4 ceramic heaters "simulating GPU and HBM zones"; 3 plates x 8 thermocouples "directly at the heater surface"; one TTV reused for all three plates |
| Coolant / flow / inlet | "standard water-glycol" (mix not stated); 1.2 LPM/kW = 18 LPM; 45 C |
| Case-to-inlet dT | average 34.4 K (plate means 32.5 / 35.2 / 35.6); 24 readings 26.8-44.2 K; "average Tcase ~80 C" |
| Per-position means (TC1-8) | 31.3 / 32.7 / 36.0 / 37.6 / **43.2** / 32.6 / 30.8 / 31.0 K |
| Architecture | patented Split-Flow; "industry-leading internal geometries"; "proven mass-manufacturing"; standard thermal paste; design and CFD done in late 2025 |
| Roadmap | lower R and dP; direct-to-die and micro-channel lids; 100 % heat capture; >1 MW racks |
| Market framing | DLC technology-cooling-system spend >US$5 B (2025), >US$11 B (2026), CoolIT's own sizing; ">10x today's top GPUs"; "nearly 4x" the 4 kW plate |
| PDF author | Benjamin Sutton, the same person who is primary author of the OCP cold-plate test spec [G-TTV, S17] |

The 4 kW predecessor (March 2025): Tr < 0.009 K/W from maximum case to inlet, TIM included; 50 x 50 mm; 4.28-6.06 LPM (6.06 LPM = 1.5 LPM/kW); heat capture 93.4-97.3 %, measured without insulation; 8 psi (55 kPa) for the full loop including fittings and QDs; heat flux "shy of 200 W/cm2" [S3, S4, S5].

### 1.2 Derived numbers

| Quantity | Value | Basis |
|---|---|---|
| R case-to-inlet | **2.29 mK/W** average; 2.17 / 2.35 / 2.37 per plate; 2.95 worst TC; 1.79 best | 34.4/15,000 etc. [S1] |
| Caloric rise, 18 LPM PG25 | **12.6 K** to outlet (57.6 C), 6.3 K to mean fluid; water 12.1 K | m = 0.303 kg/s, cp 3,930 J/kg-K [S70] |
| Caloric share | 18 % of the average to the mean fluid, 37 % to the outlet | estimate |
| R case-to-mean-fluid / case-to-outlet | 1.87 / 1.45 mK/W | estimate |
| Heated footprint | **~120 cm2 (100-145)**; plate body ~143 mm square (120-165 mm), 24-25 mm centre bar, 8 mounting ears | photogrammetry of the brief's photos against clamp, barb and screw references [G-TTV]; model calibration 117 cm2 (108 mm square) kept for continuity [M] |
| Mean heat flux | ~125 W/cm2 (105-150) | estimate [G-TTV] |
| Unit resistance R'' | **0.275 cm2-K/W average (0.23-0.33); 0.355 worst TC (0.30-0.42)**; model 0.269 | estimate [G-TTV, M] |
| Model budget (117 cm2, paste 0.07) | caloric 6.3 + TIM 9.0 + base 6.6 + convection 12.6 = **34.5 K**; hot-spot excess 9.8 K = 6.3 K intrinsic ramp along 54 mm flow paths + ~3.5 K paste/bow scatter | estimate [M, P] |
| TIM share | **6-9 K (18-26 %)** at 0.05-0.07 cm2-K/W; 12.5 K if 0.10 | estimate [G-TTV, M] |
| Uniformity | max-minus-mean per plate 9.0 / 9.0 / 8.4 K; spread of position means 12.4 K; TC5 hottest on all 3 plates; plate-to-plate 10.1 K at TC8 (= a 24-47 um bond-line difference) | [S1]; [G-TIM] |
| Hottest case | 89.2 C; Tcase,max reaches 85 C at ~41 C inlet | estimate |
| Q capacity at Tcase,max <= 85 C, 1.2 LPM/kW | **~13 kW** (12.7-12.9; P10-P90 10-15) | estimate [M, P] |
| Hydraulic power at 18 LPM | 6.5-7.4 W (reconstruction), 10.5 W (working value), 18 W at 60 kPa | estimate |

**Pressure-drop window (undisclosed).** Every corrected reconstruction has the same ~15 kPa core (channel plus turns); the differences are all in the port allowance [G-HYD].

| Boundary / scenario | dP at 18 LPM | Source |
|---|---|---|
| Core, 0.2/0.2 x 4 mm skived, 54 mm half-length | 15 kPa | [G-HYD] |
| Port-to-port, same geometry | 19.5-24.6 kPa (3 kPa flat port vs 12 mm bore) | [G-HYD, M] |
| Fin-pitch window (0.25 to 0.15 mm gaps) | 17-45 kPa | [G-HYD] |
| **Programme working value** | **35 kPa, window 20-60, tail to 140** | [G-DP] |
| CoolIT TTV as photographed | barbed hoses and worm clamps, no UQDs; two barbs alone cost 9-92 kPa depending on bore | [G-DP] |
| Tray loop (UQD08 pair, 12 mm stubs, 1 m of 1/2-in hose) | 64-90 kPa | [G-HYD] |
| Retired | 8.6-9 kPa (v1 model with the Fanning-for-Darcy bug) | [G-HYD] |

### 1.3 What is undisclosed and our best estimates

| Unknown | Best estimate | Key assumption |
|---|---|---|
| Plate dP (any boundary) | 35 kPa port-to-port (20-60) | fins opened to a budget, single split; scaling dP proportional to P from the 4 kW plate [G-DP] |
| Footprint, heater map | 2 x 2 heaters, ~120 cm2 | 12.7 mm clamp bands and 1/2-in barbs (4 m/s, not 10 m/s) [G-TTV] |
| Power split / TC5 cause | the outlet-edge caloric position effect is enough to explain it (TC5 sits 12.0-12.4 K above TC1/TC7, which equals the per-pass rise); the HBM-zone explanation is unproven | [G-TTV] |
| TIM | grease, 0.05-0.07 cm2-K/W, 20-50 um bond line | bond line inferred from the TC8 scatter [G-TIM] |
| Meaning of "case" | heater face under the paste; TCs embedded in the TTV; bead-depth bias +0.5 K (AlN) to +5 K (alumina) | [G-TTV] |
| Coolant | PG25 | it gives 12.6 K rather than 12.1 K for water [S20] |
| Fin geometry / route | skived Cu, ~0.2 mm gaps, ~4 mm tall, 2 mm base; probably FSW unibody (OMNI) | [M]; DCF factory tour [S9] |
| Heat capture, R(flow), reliability, cost, height | none disclosed; the plate is ~10-13 mm thick with the bar ~12-15 mm proud | [S1]; [G-TTV] |

Conclusion: on unit resistance the benchmark sits **mid-band for conventional skived copper** and is worse than CoolIT's own 4 kW plate (<= 0.225 cm2-K/W on a max-case basis). 15 kW demonstrates area and flow scaling, not a better plate [G-COMP, A-test-metrics].

---

## 2. CoolIT: technology, business, IP, likely next moves

| Topic | Facts | Source |
|---|---|---|
| Split-Flow | coolant enters a slot over the middle of the fin field, splits and exits at both ends, halving the flow length. "30 % better" has no stated baseline (most plausibly CoolIT's own edge-fed plate). Independent work finds similar R and much lower dP for split vs parallel flow | [S6, S4, S61]; [G-DP] |
| Skived | fins and base in one piece; RX3 CPU plate <= 0.03 K/W; fin geometry never disclosed | [S7] |
| OMNI (May 2024) | all-metal unibody with no braze; ">1,500 W", ">300 W/cm2", "up to 60 % lower R" (no conditions; the 300 W/cm2 is plausible only as a small hot spot or at low inlet temperature); the 2026 factory tour attributes the joint to friction stir welding | [S8, S9]; [G-DP] |
| 4 kW plate | see 1.1; R''max <= 0.225 cm2-K/W (25 cm2 heater) | [S3, S5]; [G-DP] |
| CDUs | CHx1000 1 MW at 1.5 LPM/kW; CHx2000 2 MW at 1.2 LPM/kW, 53 psi secondary head | [S14, S13] |
| Manufacturing | Calgary Starfield (~200,000 sq ft), plus China and Vietnam; Liquid Lab in Calgary and Taipei; 6 MW test rig; output "25x in 18 months" | [S9, S10] |
| Ownership | KKR + Mubadala (2023) -> **Ecolab, US$4.75 B cash, 29x NTM adj. EBITDA, ~US$550 M NTM sales, ~30 % EBITDA margin**, closed early July 2026 | [S11, S12] |
| Partners | NVIDIA Partner Network (NA2 loop for GB200); Dell since 2017; HPE; Lenovo; claims "4 of top 5 OEMs, 4 of 5 hyperscalers"; **not on the Rubin Group-A plate list** | [S15, S31, S32] |
| Standards | Ben Sutton (CoolIT) is primary author of the OCP Single-Phase D2C Cold Plate Test Spec v1.0.0 (Oct 2026); CoolIT is a collaborator on OCP UQD v2.0.0 | [S17, S18] |
| Field issue | Ecolab attributes recent field cold-plate problems to incomplete flushing, with particulates migrating into plates | [S66] |
| IP | ">120" rising to "150+" patents. Split-Flow: US 8,746,330 (filed 11 Aug 2008), 9,603,284 and 12,495,513 (same title, issued ~Dec 2025, almost certainly a continuation). US expiry **Aug 2028 to ~mid-2031** depending on patent-term adjustment. Compliant-member family US 11,725,886 / 12,188,733; US 12,101,906 (unknown scope); Asetek litigation settled in 2022 | [S16, S62, S63, S65]; [G-FTO] |

**New this session [S64]:** a search snippet of the USPTO gazette entry for CoolIT's US 12,460,878 B2 (issued 4 Nov 2025) shows a priority chain that includes application 13/401,618 as a **continuation-in-part of 12/189,476** (the Split-Flow parent). So the 2008 family branches beyond the three known patents. Any branch that claims 2008 priority still expires 20 years from the earliest non-provisional filing plus its own PTA, but new matter in CIPs is prior art only from its later date. All branches must be charted.

**Likely next moves (estimate):** (1) a micro-channel-lid or direct-to-die bid for Rubin Ultra (stated roadmap; NVIDIA is reported to be seeking lid partners [S35, S88]); (2) publishing dP and R(flow) in the OCP format CoolIT authored once a better plate exists, so it sets the yardstick; (3) bundling Ecolab/Nalco water chemistry and commissioning with CDUs and plates, sold against the flushing and particulate problem; (4) defending the 1.2 LPM/kW / 45 C framing that suits CHx2000; (5) multi-slot or zoned variants as Split-Flow nears expiry, protected by continuations and CIPs; (6) assertion against entrants, which Ecolab can now fund.

---

## 3. Competitive state of the art

`R` is case-to-inlet unless noted; `c-mf` is case-to-mean-fluid. Unit values for vendor points use the stated or assumed area [G-COMP].

| Vendor / device | Architecture | Best R | dP | Flow | Heat flux | Manufacturing | Date | Source |
|---|---|---|---|---|---|---|---|---|
| CoolIT 15 kW | skived Split-Flow, paste | 2.29 mK/W avg; 0.275 cm2-K/W | n/d (est. 35) | 1.2 LPM/kW | ~125 W/cm2 avg (est.) | skived + unibody | Jun 2026 | [S1] |
| CoolIT 4 kW | Split-Flow | < 9 mK/W max-case; <= 0.225 | 55 kPa full loop | 1.5 LPM/kW | ~160 | CNC + skive; OMNI on unit 2 | Mar 2025 | [S3, S4] |
| ToneCooling GB300 plate | skived Cu, Ni | 13.0-13.3 mK/W at 1,067 W; 0.14-0.21 c-mf | 12.06 kPa | 1.7 LPM (1.6/kW) | 43-67 | skived | 2025-26 | [S41] |
| FiberMall GB200 "target" | skived <= 0.5 mm fins | < 30 mK/W (a ceiling, not data) | < 20 kPa | 1.8 LPM per GPU | - | - | 2025 | [S42] |
| ORNL diamond pin-fin | Cu / CuW pins | 6.9 / 9.0 mK/W incl. TIM at 1 kW | 9.0 kPa | 3 LPM water | 18 | machined | Mar 2026 | [S43] |
| JetCool SmartPlate | microjet | Rjf 40-58 mK/W at 600 W; third-party claim -25 % vs microchannel | n/d | 0.6-1.8 LPM | - | drilled jets | 2024-26 | [S44, S45, S46] |
| Frore LiquidJet | metal-wafer jets | "-6-12 C on Rubin" | 1.7 kPa (4x vs 10x claims conflict) | 0.87 LPM/kW claim | 600 W/cm2 hot spot | lithographic | Oct 2025 | [S47] |
| Mikros (Jabil) Normal Flow | laminate MMC | 0.02 cm2-K/W core only | 20.7 kPa at 1 kW/cm2 | n/d | >1,000 | etched + bonded | 2024-25 | [S48, S78] |
| Wiwynn / Fabric8 ECAM | printed Cu, double-sided | "up to 40 %" / "48 % vs skived" | n/d | n/d | >350 | ECAM | 2025-26 | [S49, S80] |
| UIUC / Fabric8 TO plate | topology-optimised | -32 % R at equal flow; -68 % dP at equal R vs pin fins | - | - | GaN array | ECAM | 2026 | [S50] |
| PKU jet-manifold | 3-tier MMC + jets, Si | 0.065 cm2-K/W at 1 kW/cm2 | 0.9 W/cm2 pumping at 3 kW/cm2 | ~0.1 L/min | 3,000 | Si microfab | Sep 2025 | [S51] |
| Bio-inspired Cu MMC | manifold microchannel | 0.088 cm2-K/W | 25.2 kPa | - | 633 | Cu | 2025 | [S52] |
| Wakefield on-chip | plate | 26.7 mK/W at 700 W (~0.18 c-mf) | n/d | 1.6 LPM | - | - | 2025 | [S83] |
| Accelsius NeuCool | pumped two-phase | -9 C Tj vs single-phase on B200; 54 C inlet = 45 C single-phase; 4,500 W TTV | n/d | n/d | - | evaporator + CDU | Jul 2026 | [S53] |
| ZutaCore HyperCool | two-phase dielectric | 2.8 kW certified; "4 kW+" claimed | n/d | 0.3 LPM/kW | - | evaporator + heat-rejection unit | 2024-26 | [S54] |
| Wiwynn two-phase | cold plate | 2.5 kW at 125 W/cm2 | n/d | 45 C saturation | 125 | - | 2025 | [S55] |
| R245fa parallel plates | two-phase | ~1 mK/W total | - | - | ~300 | - | 2026 | [S56] |
| ACT cut sheet | two-phase vs single | 0.080 vs "typical single-phase" 0.150 | - | - | - | - | Nov 2025 | [S57] |
| Microsoft / Corintis | in-die microfluidics | -65 % peak Si rise; "3x" heat removal | - | - | - | die etch | Sep 2025 | [S58, S79] |
| TSMC direct-to-silicon | on CoWoS | >2.6 kW at dT < 63 C | - | - | - | foundry | ECTC 2025 | [S59] |
| Chilldyne (Daikin) | negative pressure | 2 kW rating | < 1 atm available | - | - | - | Nov 2025 | [S60] |
| Iceotope KUL SINK | precision immersion | 39 mK/W at 1 kW | - | 7 LPM/kW | - | pinned Cu | ~2023 | [S84] |

**Anchored conventional-skived band:** 0.14-0.22 cm2-K/W case-to-mean-fluid and 0.18-0.25 case-to-inlet (worst point up to 0.30), TIM included, at 1.2-1.6 LPM/kW. A ToneCooling- or AVC-class plate enlarged to the CoolIT footprint would land within +/- 4 K of 34.4 K. Peer-reviewed manifold-microchannel plates sit at 0.065-0.09 [G-COMP]. **No Group-A supplier publishes any plate-level K/W, LPM or kPa figure** [G-COMP].

**Rubin Group-A context:** for Vera Rubin, NVIDIA centralised cold-plate purchasing with **Jentech (the lid incumbent), AVC, Cooler Master and Delta** at ~US$400 per plate [S31, S32]. AVC held ~40-50 % of GB200/GB300 plates [S33]. A "Group B" (Auras, Nidec, Foxconn...) is press rumour only [G-COST, KB]. CoolIT is absent. A lid maker on a *plate* list signals that lid, TIM2 and plate are being specified as one system [G-TIM].

---

## 4. Target requirements

### 4.1 AI accelerators 2026-2029

| Device | TDP | Logic / HBM | Package | Die-average flux | Status | Source |
|---|---|---|---|---|---|---|
| B200 (GB200) | 1,200 W (superchip 2,700 W; rack 120-140 kW) | 2 reticle dies (~16 cm2) / 8 HBM3e | CoWoS-L; **probably lidded** (Section 10, C9) | ~60-70 W/cm2 | official [KB-H] | rack [S86, S85]; [G-RUB] |
| B300 (GB300) | 1,400 W | same / 8 HBM3e 12-high | "SXM puck"; reported possible lidless HGX variant | ~72 | official | [S36, S75, S89] |
| Rubin (VR200) | 1.8 / 2.3 kW | 2 dies (~16.6 cm2) / 8 HBM4 | ~100 x 100 mm substrate; gold-plated lid + micro-channel plate; micro-channel lid not before 2H 2027 | 89-117 | analyst | [S28, S27]; [G-RUB] |
| Rubin Ultra (Kyber, 600 kW rack) | ~3.6 kW | 4 dies (~33 cm2) / 16 HBM4e | ~120 x 150 mm; micro-channel lid or direct-to-chip rumoured | ~87; 300-400 local hot spots | analyst / NVIDIA rack figure | [S29, S34, S35] |
| MI355X / MI455X | 1.4 / >2 kW | 8 stacked XCDs / 8-12 HBM | lidded lineage | 120-150+ at XCD | official / secondary | [S37]; [KB] |
| Ironwood TPU | ~0.7-0.9 kW (est.) | 2 dies / 8 HBM3e | bare die since TPU v4; chips in series; 80 psi head | 80-110 | derived | [S38, S40] |
| Feynman (2028) | 4-6 kW (extrapolation) | - | candidate for in-package microfluidics | >150 | estimate | [A-chip-roadmap] |

**Requirements derived from these devices** (45 C inlet, 1.0 LPM/kW design point) [G-RUB, P]:

| Parameter | Requirement | Basis |
|---|---|---|
| Temperature budget | Tj ~85 C operating, 87-89 C slowdown, HBM 95 C [KB]; after a 5-8 K silicon drop: **<= 28-30 K average, <= 33-35 K maximum** die-top-to-inlet | [G-RUB] |
| Inlet / return | 45 C max supply, 65 C max return (GB200); Rubin MGX gen-3 "designed for 45 C" | [S25, S87, S27] |
| Flow | **1.0 LPM/kW design** (NVIDIA rack ~1.0, floor 0.75 from 45/65 C); 1.2 is a CDU rating point (CHx2000); curves at 0.6 / 0.75 / 1.0 / 1.2 / 1.5 | [S25, S13, S26]; [G-RUB] |
| Plate dP | <= 25 kPa at 1.0 LPM/kW and <= 35 kPa at 1.2 (15 kW TTV); public plate band 12-40 kPa | [G-RUB, G-HYD] |
| Tray / rack / CDU budget | tray <= 100 kPa with one UQD08 pair and >= 12 mm stubs; rack ~124 kPa (18 psi); CDU head 35-53 psi (CoolIT), >= 40 psi (OCP), 80 psi (Google Deschutes); components to 100 psi | [S26, S13, S21, S39] |
| Footprint | 100 x 100 mm (Rubin, MI455X) to 120 x 150 mm (Rubin Ultra), with per-channel flow length independent of package size | [G-RUB] |
| Non-planar contact | HBM4 stack height up to 775 um, so the HBM-to-logic step is 0 to +/-0.15 mm with either sign [KB]; bare die needs a stepped Cu pedestal plus <= 0.1 mm compliant TIM (gap pads fail above ~15-20 W/cm2) | [G-RUB, P] |
| Mounting | 20 psi on a 100 cm2 lid is 1.38 kN while module retention gives ~0.3-1 kN (4-12 psi), which favours PCM or liquid metal; flatness <= 25 um, Ra <= 0.8 um; warpage 100-300 um | [G-TIM] |
| Coolant | OCP PG25: cp 3.93-3.94 kJ/kg-K, mu ~1.45 mPa-s at 45 C (~2.4x water), laminar in microchannels | [S20, S70]; [A-test-metrics] |

**UQD couplings and their losses** (pair = supply + return, PG25, Cv values not verified, +/- 50 %) [G-HYD]:

| Coupling | Cv per coupling | Pair dP at 15 LPM | **at 18 LPM** | Bore velocity at 18 LPM |
|---|---|---|---|---|
| UQD04 (1/4 in) | 0.5-0.8 | 340-870 kPa | 490-1,250 kPa | 15 m/s |
| UQD06 (3/8 in) | 1.3-2.0 | 54-129 | 78-185 | 6 m/s |
| UQD08 (1/2 in) | 3.0-4.0 | 14-24 | **20-35** | 3.8 m/s |
| UQDB08 blind-mate | 2.5-4.0 | 14-35 | 20-50 | - |
| 3/4-in class (not confirmed in OCP v2.0.0) | 6-10 | 2-6 | 3-9 | 1.5 m/s |

A 15 kW loop needs 1/2-in hardware at minimum. Four 1/2-in barbs at 18 LPM cost ~36 kPa, seven times our plate. A negative-pressure loop of <= 30-50 kPa is infeasible at 18 LPM with one UQD08 pair and needs either dual UQD08 or 1.0 LPM/kW [G-HYD]. CoolIT's TTV avoided UQDs altogether [G-DP].

**Rubin plate envelope (assembled, not published by NVIDIA):** flat ~100 mm Au-finished lid (liquid-metal-ready); 1.8-2.3 kW; ~2-3 LPM per package; plate dP <= 30-40 kPa; ASP ~US$400; Group-A procurement [G-RUB, S28, S31].

### 4.2 Power electronics

| Segment | Load / flux | Coolant / inlet | Required R'' incl. interface | dP | Cost class | Fit | Source |
|---|---|---|---|---|---|---|---|
| 800 VDC in-rack conversion (NVIDIA, Kyber 2027) | 9-15 kW per 600 kW rack, 15-26 kW per MW; SiC/GaN Tj 150-175 C; 5-30 W/cm2 at the package | same PG25 loop, 30-45 C | 0.5-2 (limited by the gap pad) | 20-50 kPa, must not starve GPU plates | US$50-150 per plate; 0.08-0.6 M plates/yr, US$4-90 M/yr | **high: rack-kit SKU** | [S73]; [G-COST, A-power-electronics] |
| CPO switches | 1-2 kW ASIC + optical engines; lasers < 70-80 C, +/- 3 K | PG25 | <= 0.2 | 10-30 kPa | US$150-300 | high | [KB] |
| EV SiC traction | 2-4 kW peak; 300-800 W/cm2 die, 30-100 at baseplate | WEG 50/50, 65 C, 10 LPM, -40 C cold start | 0.4-1.0 today; 0.1-0.2 would save 15-20 % SiC area (US$100-150 per inverter) | 10-30 kPa | cooler content US$20-60; 25-35 M inverters/yr | low: Al loops, AQG 324, module vendor owns the baseplate; license only | [S72]; [KB] |
| SST / MV SiC | 20-40 kW per MW | DI water or WEG, 40-50 C | 0.3-0.8 | 30-100 | US$100-300 | medium (2027-28) | [KB] |
| Laser diodes / RF GaN | 500-1,000+ W/cm2 | DI water / PAO | <= 0.03-0.3 | 50-140 | high margin | niche | [KB] |

Rule: minimum feature >= 0.3-0.5 mm for automotive and charger loops; 0.15 mm only in filtered PG25 or DI water [A-power-electronics].

---

## 5. Standards and qualification checklist (drop-in)

Status: **V** = text captured; **A** = assumed from predecessor documents or practice and to be checked against the PDF (none of the October 2026 OCP PDFs has been read in full) [G-OCP].

| # | Requirement | Target | Status / source |
|---|---|---|---|
| 1 | Thermal metric | R = (Tcase - Tin)/P in K/W at >= 6 flows with the OCP "recommended TIM" (probably a PCM); also report cm2-K/W with heater area | V method [S17]; TIM identity A |
| 2 | dP measurement | 45 +/- 2 C, >= 6 points, 25-150 % of rated flow; declare rated flow = 1.0 LPM/kW (the sweep then covers 18 LPM and 0.75 LPM/kW); publish three boundaries (port-to-port with bore, plate + stubs, plate + named UQD pair) | V [S17]; boundary A |
| 3 | Burst / proof / MAWP | MAWP >= 100 psi (6.9 bar), preferred 150 psi; proof 1.5x; burst >= 3x and > 20 bar (OCP example); our tied sandwich qualifies at >= 45 bar; vacuum to -0.9 bar(g) | burst V [S17]; 100 psi V [S21]; rest A; 45 bar [P] |
| 4 | Leak | He <= 1e-5 mbar-L/s (target 1e-6), 100 % production test | V [S17] |
| 5 | Cycling | 10-65 C operating, -40/+70 C storage (counts not captured; plan 1,000 / 50); >= 10,000 pressure cycles 0-MAWP; >= 1,000 power cycles; drift <= 5 % R, <= 10 % dP | windows V [S17]; counts A |
| 6 | Coolant | OCP PG25; rate performance in PG25 at 45 C and show water as a secondary curve; PG25 Guidelines carry action limits for particle count, pH, conductivity, inhibitor and microbes (values not captured) | V [S19, S20] |
| 7 | Temperature class | ASHRAE W45; characterise at 50 C (W+); outlet <= 65 C | V [S24, S25] |
| 8 | Interfaces | OCP UQD v2.0.0 sizes UQD02-08 and UQDB; 1/2-in-class stubs (12-13 mm bore) for >= 15 kW; EIA, ORv3, MGX/Kyber envelopes | sizes V [S18]; pressure classes A |
| 9 | Wetted materials | Cu (bare or Ni-plated), 316L, peroxide-cured EPDM, PTFE/PPSU/PEEK; no Al, Zn, NBR, silicone; fluxless joints; Ni plating is *practice*, not a requirement | A [G-TIM] |
| 10 | Filtration / passages | fleet runs 50 um *nominal* at the CDU (~90 um absolute) with no in-tray filtration; smallest passage >= 3x absolute rating, so **0.15 mm channels need a plate-integral 50 um absolute screen** (>= 30 cm2, clean 0.2-0.8 kPa, 2-5 kPa budget); hierarchical widths port >= 3 mm > L1 >= 1 > L2 >= 0.3 > channel | KB-M rating [G-FOUL]; Schneider on filter dP [S67] |
| 11 | Velocity | <= 1.5-2.0 m/s in Cu at 150 % rated flow; ports <= 1.5 m/s | A [P] |
| 12 | Mechanical | flatness <= 25 um, Ra <= 0.8 um; load within the package window | A |
| 13 | Cleanliness, compatibility | flushed and particle-counted; 1,000-3,000 h PG25 soak at 65 C, dP drift <= 10 % | A |
| 14 | Particulate challenge (beyond OCP) | 500 h dosed ISO 12103 dust + Cu + EPDM, R drift < 5 %; clustered-blockage test at slot ends | [G-FOUL] |
| 15 | Reporting | OCP v1.0.0 format plus k = 2 uncertainty, 3-plate CpK, power-weighted mean, independent-lab repeat | [A-test-metrics] |
| 16 | Quality / commercial | PPAP-style package, CpK >= 1.33 on leak and dP; route to NVIDIA RVL/ODM qualification (12-18 months to first PO) | [KB]; [A-market] |

---

## 6. Physics levers and manufacturing routes

### 6.1 Levers ranked by mean dT reduction at fixed 18 LPM PG25 (117 cm2, from the CoolIT-like 34.5 / 44.3 K) [M, P]

| Rank | Lever | Mean dT | Max dT | dP effect | Quantitative basis |
|---|---|---|---|---|---|
| 1 | Interface: paste 0.07 -> liquid metal 0.015 cm2-K/W on Ni | **-7.1 K** | -9 K (scatter 3.5 -> 0.6 K) | none | TIM term 9.0 -> 1.9 K; LM physics 0.007-0.03 [G-TIM] |
| 1b | Direct-to-die (lid and TIM removed) | -9 K plate; -28 K at the junction at 350 W/cm2 | - | none | chip co-design [P] |
| 2 | Base 2.0 -> 1.0 mm as a tied sandwich (fin tips bonded to manifold webs) | **-3.3 K** | -3.3 K | 0 | base term 6.6 -> 3.3 K; zero pressure bow; stack 24x stiffer [P] |
| 3 | Finer fins, possible only under a manifold: 0.2/0.2 x 4 -> 0.15/0.10 x 2.0 (robust) / 0.10/0.10 x 1.5 (performance) | **-2.5 / -5.8 K** convection | same | without a manifold 0.10 mm fins cost 128 kPa | h_eff 101 -> 127 / 187 kW/m2K; the 0.10 mm core needs <= 33 um absolute filtration [P, G-HYD] |
| 4 | Interface: paste -> PCM 0.055 | -1.9 K | -4 K incl. scatter | none | PTM7950 0.04-0.08 [S69] |
| 5 | Manifold, 4 mm flow length (design H) | **+1.3 K** (isothermal caloric penalty) | **-3.5 to -6 K**; flow-driven hot spot 6.3 -> 1.5 K | **-75 to -80 %** (22-25 -> 5 kPa) | enables lever 3; removes the streamwise ramp [P] |
| 6 | Zone flow to heat (die >= 85-90 % of flow) | 0 on a uniform TTV | **-15 K** at the hot die of a real package | ~0 | an un-zoned manifold loses 15 K [P] |
| 7 | More flow (1.2 -> 2.0 LPM/kW) | -3.5 K (Tier 1) | -3.6 K | x2.7 dP | a weak lever [M] |
| 8 | Water instead of PG25 | -1.4 K | -1.4 K | -4 % | usually not allowed by spec [M] |
| 9 | Cu-diamond base / local diamond insert | -1.5 K / -2-3 K local | | 0 | cost prohibitive [A-physics] |
| 10 | Topology-optimised or TPMS AM core vs a good manifold | 0 to -3 K | | | gain comes from distribution, not lattice [A-physics] |
| 11 | Counter-flow interdigitation | <= 0.25 K | | | not worth building [P] |
| 12 | Two-phase refrigerant at the Tsat a 45 C loop forces (60 C) | **+6 to +14 K** vs single-phase LM | | | not in the baseline [P] |

**Stacked result:** robust core + PCM = **28.0 / 31.1 K** (Tier 1, P10-P90 26-31 / 29-35); + liquid metal = **22.9 / 25.0 K** (Tier 2); same paste as CoolIT = 30.0 / 35.0 K (-13 % mean, -21 % max); plate dP 5.0-5.3 kPa, pumping 1.5 W [P, M]. Fouling rule: channels narrower than 0.15 mm buy only 2-4 K, so 0.05-0.075 mm channels come off the roadmap [G-FOUL, P].

### 6.2 Manufacturing routes that realise each lever (100k/yr unless stated)

| Lever | Route | Cost (estimate) | Volume readiness | Source |
|---|---|---|---|---|
| Fin core | skived OFE Cu, 0.10-0.15 mm fins (0.06 mm / 0.10 mm pitch demonstrated) | US$15-28 core | proven | [S81]; [G-COST] |
| Manifold laminate | photochemically etched Cu, 1-2 layers 0.2-0.3 mm | +US$5-15 | proven (PCB/EMI industry) | [G-COST] |
| Tied sandwich | vacuum braze or diffusion tack of fin tips to the manifold web (>= 50 % bonded) | +US$4-9 per join (est.) | proven in brazed plates | [A-manufacturing], [P] |
| Perimeter seal | green-laser weld (-US$2 to +3 vs braze) or FSW (+US$4-12) | | proven (EV) | [G-COST] |
| Premium core | etched + diffusion-bonded laminate (Mikros class) | +US$40-80 | 10-100k; furnace-limited | [G-COST] |
| Gen-2 conformal fins | ECAM | +US$50-150 today, +US$20-60 at maturity | single supplier | [G-COST] |
| Interface | contact-face electrolytic Ni 3-5 um +US$1-3; liquid metal +US$3-10; In pre-form +US$5-15 | | consumer LM precedent only at 1-8 cm2 | [G-COST, G-TIM] |
| Prototypes only | Cu L-PBF | +US$300-700 | none | [G-COST] |

**Canonical factory cost** (bare plate, no QDs): ~US$165 / ~100 / ~70 at 10k / 100k / 1M per year (+/- 25 %). Our base design is **~US$110-125 at 100k**, ~US$80 at 1M and ~US$175-185 at 10k [G-COST].

---

## 7. IP: crowded vs open design spaces [A-ip, G-FTO]

| Design space | Status | Verdict |
|---|---|---|
| Parallel microchannels; manifold microchannel (Harpole US 5,088,005); alternating counter-flow (Walpole US 5,099,910); normal-flow laminates (US 5,145,001) | expired | open |
| Cooligy interwoven/multi-level manifolds, hot-spot delivery (US 6,986,382; 7,156,159; 7,000,684; 7,104,312) | expired 2023 | open; also our invalidity shield and the reason we cannot broadly claim "denser fins over hot spots" |
| Single central slot, split flow (CoolIT '330 / '284 / '513 + CIP branches [S64]) | live to Aug 2028 - ~mid-2031 (US); foreign counterparts probably none | **"Use >= 2 slots" is not a safe design-around on its own** ("comprising" plus "an"). Distinguish by interior interdigitated outlets, fins segmented at each outlet slot, manifold in a separate laminate, zones separated by solid ribs; document the mapping to the expired Cooligy/Harpole art now; claim chart US$25-60 k before US sales |
| Compliant member (US 11,725,886 / 12,188,733) | live (priority 2011-13 or 2020-21) | a rigid stepped base is clear; avoid spring-loaded HBM pedestals; IBM TCM pistons (1976) are prior art |
| US 12,101,906 | unknown | highest-priority read |
| Microjet arrays and jet-onto-die lids (JetCool/Flex, Frore, Microsoft, NVIDIA) | crowded, live to 2037-45 | avoid as a core; orifice combs feeding fin roots need a claim review |
| Two-phase dielectric evaporators and fluids (ZutaCore, Accelsius/Bell Labs, fluid makers) | crowded | avoid |
| In-silicon microfluidics (Corintis, Microsoft, TSMC, IBM) | crowded and silicon-gated | not our business |
| Micro-channel lids / bare-die compliance (Intel, NVIDIA, Jentech, TSMC) | emerging thicket | claim review before a bare-die SKU |
| Sensors or valves in the plate (NVIDIA "intelligent" plates); in-plate leak sensing (CoolIT 9,052,252) | live | keep the plate passive |
| Purdue HMMC, IBM Zurich MMC | live only if granted and maintained | check |

**What to file (provisionals before any disclosure):** the skive + etched-laminate + tied-sandwich + weld stack; zone-rib and port layout tied to the power map; the skiving-stroke pitch-modulation process; the stepped bare-die base; the integrated-screen plate with slot-end bleed. The FTO search plus opinion on ~10 families costs US$40-100 k [A-ip].

---

## 8. Market

| Metric | Value | Source |
|---|---|---|
| DLC technology-cooling-system spend | >US$5 B (2025), >US$11 B (2026), vendor figure; bottom-up US$6.5-16 B (2026), US$12-25 B (2027) | [S1]; [A-market] |
| Plates' share of that spend | 25-40 % (~US$2-5 B in 2026) | estimate [A-market] |
| NVL72-equivalent racks, 2026 | 35k / **55k** / 80k (low / base / high) | estimate, three triangulations [G-COST] |
| Plates per rack | 126 (GB300); ~150 (VR NVL144) | estimate from the Morgan Stanley BOM [S30] |
| DLC plates per year | 6.5-16 M (2026, base ~10 M); 11-24 M (2027) | estimate [G-COST] |
| Prices | GB300 CPU/GPU plate ~US$300, NVSwitch ~US$200, Rubin up to ~US$400; rack cooling BOM US$49,860 (GB300) / US$55,710 (VR NVL144); IDTechEx US$300-500 | [S30, S29, S71] |
| What the US$300 contains | probably includes UQD halves and hoses (US$38-95), so the bare plate sells for ~US$200-260 and costs US$100-180; **our US$100 is cost parity, not a 2-3x advantage**; the 45-70 % SKU margins in the angle reports are an upper bound | estimate [G-COST] |
| In-rack BOM per kW / CDU hardware | US$356/kW; US$120-300/kW | estimate [G-COST] |
| Buyers | NVIDIA (envelope, RVL, Rubin purchasing); ODMs (Foxconn, Quanta, Wiwynn, Supermicro); OEMs (Dell, HPE, Lenovo); hyperscalers for their own ASICs | [A-market] |
| M&A | Ecolab-CoolIT US$4.75 B; Flex-JetCool; Jabil-Mikros; Daikin-Chilldyne; Eaton-Boyd (~US$9.5 B, unverified) | [S11, S77, S78, S60]; [KB] |

**How a new entrant wins (ranked):** (1) hyperscaler custom-ASIC programmes, which own the spec, run bare die, allow 80 psi and buy on TCO; (2) license or manufacture through a Group-A house or a Western contract manufacturer, because the route uses the same skive + etch + weld supply base; (3) co-design a micro-channel-lid core with a Jentech-class partner for Rubin Ultra or Feynman; (4) OEM-branded systems; (5) an 800 VDC rack-power kit; (6) a transparency play: full OCP-format data plus an independent lab (ORNL publishes copper plate data [S43]) [A-market, G-COST].

**Value of performance deltas (estimates; no operator has published US$/K or US$/kPa)** [G-COST]:

| Delta | Value per 100 MW IT |
|---|---|
| +1 K of supply temperature (from 1 K of case-to-inlet margin) | +8-12 % dry-cooler capacity = **US$0.8-2.0 M capex**, plus US$0.16-0.32 M/yr trim-chiller energy in hot climates |
| 1 K spent on Tj instead | US$0.14-0.35 M/yr (0.2-0.5 % of chip power per K) |
| 5 K (W45 -> 50 C at the same Tcase) | US$4-10 M capex + US$1-2 M/yr, against ~US$2.2 M of plate premium |
| -10 kPa plate dP | 3 W per 15 kW plate, ~US$70k/yr; or **US$9-25 per plate** of CDU capex if it lets a head-limited CDU carry one more rack |
| 1.2 -> 1.0 LPM/kW at the same Tcase | -17 % LPM, i.e. ~US$30-80/kW of CDU, pump and manifold capex |

---

## 9. "Beat CoolIT" scorecard

Thermal targets follow `[P]`. **Design** is the model median; **commit** is the value we publish and guarantee (Monte Carlo P90). All at 15 kW, PG25, 45 C, on the ~117-120 cm2 parity TTV unless stated.

| # | Metric | CoolIT 15 kW (measured or estimate) | Our target: design / **commit** | Margin | Basis |
|---|---|---|---|---|---|
| 1 | Average dT at 1.2 LPM/kW | 34.4 K (measured) | Tier 1 PCM 28 K / **<= 31 K**; Tier 2 LM 23 K / **<= 25 K** | -10 to -33 % | [P, M] |
| 1b | Same-paste like-for-like | 34.4 K | 30 K / **<= 33 K** | -4.5 K honest claim | [P] |
| 2 | Maximum dT (worst TC) | 44.2 K | Tier 1 31 K / **<= 35 K**; Tier 2 25 K / **<= 27 K** | -21 to -43 % | [P] |
| 2b | At the 1.0 LPM/kW design point (Rubin-class budget <= 28-30 K average / <= 33-35 K maximum) | CoolIT-like 35.8 / 45.6 K (fails) | Tier 1 29.9 / 32.9 K (meets the budget at design value only); Tier 2 **24.8 / 26.9 K** (meets with margin); dP 3.7 kPa | Tier 2 is the Rubin-class product | model run this session [M]; budget [G-RUB] |
| 3 | Uniformity, max - mean | 8.4-9.0 K | 3 K / **<= 4 K** (flow uniformity +/- 20 % verified) | 2x+ | [P] |
| 4 | Plate-to-plate spread at one TC (3 plates) | 10.1 K | **<= 2 K** | 5x | [G-TIM] |
| 5 | Plate dP port-to-port, 18 LPM (16 mm ports, no QD) | undisclosed; reconstruction 22-25 kPa, working 35 (20-60) | 5 kPa / **<= 10 kPa** | 2-7x | [G-HYD, P] |
| 5b | Tray loop with one UQD08 pair + 12 mm stubs | 64-90 kPa (est.) | **<= 65 kPa** (45-65) | meets <= 70 kPa where CoolIT is marginal | [G-HYD] |
| 6 | Hydraulic pumping power, 18 LPM | ~6.5-10.5 W (est.) | 1.5 W / **<= 3 W** | 3-7x | [P] |
| 7 | Flow to match 34.4 K average | 1.2 LPM/kW | Tier 1 0.72 / **<= 0.75 LPM/kW**; Tier 2 0.56 / **<= 0.6** | -38 to -50 % LPM | model run this session (Section 10, C17) |
| 8 | Max TDP at Tcase,max <= 85 C, 1.2 LPM/kW, same footprint | ~13 kW (15 kW runs at 89 C) | Tier 1 21.5 kW / **>= 18 kW**; Tier 2 30 kW / **>= 27 kW**; stated per area: **>= 150 W/cm2** (Tier 1), **>= 225 W/cm2** (Tier 2) | +40-130 % | [P]; phrasing per OCP reading A [G-OCP] |
| 9 | Inlet headroom (Tcase,max = 85 C at 15 kW) | ~41 C | **>= 50 C** (W+) | +9 K | estimate from rows 2 and 8 |
| 10 | Heat flux: reticle die at 350 W/cm2, zoned real package, Tcase,max | ~134 C paste / ~121 C LM (CoolIT-like); OMNI ">300 W/cm2" has no conditions | Tier 1 PCM 107 C; Tier 2 LM **<= 93 C**; performance core **<= 84 C**; direct-to-die ~80 C | -27 to -41 K | [P] (2029+ stress case, C11) |
| 11 | Cost | undisclosed; incumbent bare plate ~US$100 at 100k, assembly ASP US$300-400 | factory **<= US$125** at 100k; ASP <= US$400; at equal ASP, **US$ per kW of Tcase-limited capacity >= 25 % lower** (commit, 18 vs 13 kW; design -40 %) | parity per plate, better per kW | [G-COST]; row 8 |
| 12 | Reliability: pressure | none disclosed | burst **>= 45 bar**, He <= 1e-6 mbar-L/s, 1,000 power cycles <= 5 % R drift, zero pressure bow | > OCP 20-bar example | [P, S17] |
| 12b | Reliability: fouling | ~0.2 mm skived channels on 50 um nominal; field-proven, ~10-year reference; shear self-cleaning | 0.15 mm behind an integrated 50 um absolute screen; **relative life >= 0.6x (honest band 0.6-1.2x)**; published particulate-challenge result | **parity at best, not a win**; claim transparency instead | [G-FOUL, P] |
| 13 | Manufacturability | skive + FSW unibody, in-house, proven | same supply base + 1 etched layer + fin-tip braze; >= 2 sources per process; yield >= 95 %; **plate height ~30 mm is a constraint to resolve** | parity | [G-COST, P] |
| 14 | Application breadth | one TTV demo, lidded, paste; 4 kW and OMNI products | 4 interface SKUs (lidded PCM, lidded LM, stepped bare die, micro-channel-lid core), 100 x 100 to 120 x 150 mm, CPO and 800 VDC derivatives, curves 0.6-1.5 LPM/kW | broader | [G-RUB, A-power-electronics] |
| 15 | Transparency | one flow point, no dP, no TIM identity, vendor-only data | full OCP v1.0.0 report, 6-point dP at 3 boundaries, 3 plates x 3 assemblies, independent-lab repeat | decisive | [G-OCP] |

Claims to avoid [P]: anything that depends on 0.05-0.075 mm channels; any dP that leaves out quick disconnects or ports without saying so; any 350 W/cm2 figure without zoning; "N kW per package" scalability (state W/cm2 at R'', dT and LPM/kW instead).

---

## 10. Contradictions and uncertainties

| # | Contradiction | Resolution (which source supersedes) | Verification needed |
|---|---|---|---|
| C1 | Heated area: 61-79 cm2 (coolit-briefs) vs ~100 (coolit-products) vs 117 (model) | the photogrammetry gap report supersedes: **120 cm2 (100-145)**; 61-79 cm2 would need a 140 mm plate overhanging the heaters by 30 mm a side | booth photos with a scale reference; CoolIT disclosure |
| C2 | The two photogrammetry reports: body 143 mm (120-165) vs 130-185 mm; 8-way block = heater leads vs TCs | the footprint report (dedicated, more references) supersedes; both agree the TCs sit in the TTV | as C1 |
| C3 | 4 kW unit R: 0.18 vs 0.225 cm2-K/W | [G-DP]: "shy of 200 W/cm2" fits 160 W/cm2, so 25 cm2 and **0.225** | page 2 of the 4 kW brief |
| C4 | CoolIT dP: 8.6-9 / 19.5 / 21.8 / 24.6 kPa | 8.6-9 is the v1 friction bug (retired); the rest are the same 15 kPa core with different port allowances [G-HYD]; working value **35 kPa (20-60)** [G-DP] | CoolIT curve; OCP example data |
| C5 | HMMC dP: 6.2 / 8.3-8.6 / 5.0 / 5.3 kPa | different manifold geometries; **design H (5.0-5.3) is the design of record; claim <= 10** [G-HYD, P] | CFD or water-table test of one slot pair |
| C6 | HMMC thermal: 19.8-24 K (physics-options), 26.1 K (fouling gap) vs 28.0 K PCM (synthesis) | the synthesis supersedes: fouling floor 0.15 mm, isothermal caloric (+1.3 K), 4 mm flow length | prototype on the parity TTV |
| C7 | TIM share: 9-12 K (early) vs ~6 K (photogrammetry) vs 9.0 K (model) | **6-9 K**, depending on paste impedance; convection plus caloric dominate at 125 W/cm2 | ASTM D5470 of a named paste at the measured bond line |
| C8 | TC5 cause: HBM zone vs outlet edge | the outlet-edge caloric effect suffices [G-TTV]; consistent with the synthesis split (6.3 intrinsic + 3.5 scatter) | heater map |
| C9 | Package form: lidded (chip-roadmap) vs bare-die + stiffener for A100-B300 (Rubin and TIM gap reports) | **Partly reversed by this session's search:** a market-rumour post says the B300 HGX "may revert to the lidless stiffener design used in Hopper", which implies **B200 is lidded** [S75], and Lenovo's B200 cold-plate procedure uses phase-change pads [S76]. Working view: H100 bare die; **B200 lidded**; B300 uncertain; Rubin gold-plated lid [S28]. The gap reports are superseded on B200 only. This favours Tier 1 flat-lid drop-in as the lead SKU | NVIDIA module photo or design guide; teardown |
| C10 | Design flow: 1.2 (CoolIT) vs 0.75-1.0 | **1.0 LPM/kW design**; 1.2 kept only for the comparison; FiberMall's "0.67 LPM/kW" is a misreading (the figure is per GPU, 1.5 LPM/kW) [G-RUB, G-COMP] | NVIDIA site-planning guide |
| C11 | Real-package stress case: 4 dies at 350 W/cm2 ([P]) vs Rubin Ultra ~87 W/cm2 average with 300-400 W/cm2 local spots | the Rubin gap report: 350 W/cm2 over whole dies is a **2029+ stress case**; keep the synthesis numbers as a stress KPI, not a Rubin Ultra spec | Rubin Ultra power map (NDA) |
| C12 | Cost: "US$90-160 at 100k" vs a 170/105/70 table; 45-70 % margins | labelling error: **US$165 / 100 / 70**; the US$300 line probably includes UQDs, so we are at parity [G-COST] | full Morgan Stanley text; RFQs |
| C13 | Split-Flow expiry "~Aug 2028" vs "Aug 2028 - mid-2031"; ">= 2 slots is a design-around" | the FTO gap supersedes on both; this session also found a CIP branch (US 12,460,878 chain) [S64] | Patent Center continuity, PTA, IPR records; claims of '284, '513, '906 |
| C14 | Two-phase as "second SKU" (physics-options) vs "not in baseline" | the synthesis supersedes: 6-14 K hotter at 60 C Tsat, plus PFAS and refrigerant CDUs | revisit if facility water <= 40 C or PFAS outcome is clear |
| C15 | Laser-welded lid (manufacturing) vs a tied sandwich that needs bonded fin tips (synthesis) | the synthesis supersedes: area bonding (braze or diffusion) of fin tips is required for a 1.0 mm base; laser or FSW stays as the perimeter seal | burst >= 4.5 MPa plus acoustic microscopy of the bond |
| C16 | Scalability ">20-30 kW per plate" vs OCP "~4,000 W" boundary | restate per area (reading A: lidded package at 0.2-0.3 cm2-K/W, 35 K); 15 kW and 4 kW are consistent [G-OCP] | read OCP Thermal Boundaries Section 8.2 / Appendix B (the search found nothing) |
| C17 | Synthesis: "equal average dT at ~7 LPM" vs the model flow sweep | re-run this session: equal **average** needs 10.9 LPM (PCM) / 8.4 LPM (LM); ~7.8 / 6.4 LPM matches the **maximum** basis. The scorecard uses the average-basis values | same as C6 |
| C18 | Rack volumes 30-50k vs 50-80k | **35 / 55 / 80k** band [G-COST] | TrendForce / Morgan Stanley 2026 |
| C19 | Plate height: synthesis ~30 mm vs a CoolIT plate of ~10-13 mm + bar | unresolved packaging risk for 1U MGX trays | tray CAD envelope |

**Top uncertainties, ranked by impact on the scorecard:**
1. **CoolIT's real dP and footprint.** The dP claim rests on reconstruction. Mitigation: state margins against the 20-60 kPa window and the >= 15-20 kPa physics floor for any single-split skived plate; buy 2-3 incumbent plates and test them (< US$10 k, 4-8 weeks) [G-COMP].
2. **Manifold flow uniformity and the tied-sandwich bond.** The 1.5 K hot spot and the 1.0 mm base both depend on them. Cheapest experiments: a slot-pair water table plus a braze coupon C-scan [P].
3. **Fouling life of 0.15 mm channels with no shear self-cleaning.** Run the particulate challenge in Section 5, row 14.
4. **Liquid-metal containment at 100 cm2 over 1,000+ bow cycles.** There is no public data, so Tier 2 is gated on our own cycling tests [G-TIM].
5. **Unread October 2026 OCP PDFs** (case definition, recommended TIM, dP boundary, filtration rating) and **NDA NVIDIA envelope** (package form, load, flatness) [G-OCP, G-RUB].
6. **IP:** the claim text and continuity of '513, '906 and the CIP branches [G-FTO].
7. **Cost:** whether the US$300 includes UQDs, and RFQ-grade numbers for the etched laminate and fin-tip braze [G-COST].

---

## Sources

S1 CoolIT 15 kW Tech Brief (Jun 2026), local `appendix/pdf/brief.txt`: https://www.coolitsystems.com/resources/news/15kw-coldplate/
S2 CoolIT 15 kW press release: https://www.prnewswire.com/news-releases/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-roadmap-far-beyond-2030-302787344.html
S3 CoolIT 4 kW Technical Brief R2: https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
S4 CoolIT 4 kW press release: https://www.prnewswire.com/news-releases/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership-302401512.html
S5 Tom's Hardware, cooling state of play 2025: https://www.tomshardware.com/pc-components/cooling/the-data-center-cooling-state-of-play-2025-liquid-cooling-is-on-the-rise-thermal-density-demands-skyrocket-in-ai-data-centers-and-tsmc-leads-with-direct-to-silicon-solutions
S6 Split-Flow tech brief: https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf
S7 Skived coldplate brief: https://coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf
S8 OMNI launch: https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled
S9 DCF CoolIT factory tour: https://www.datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale
S10 CoolIT manufacturing scale-up: https://www.hpcwire.com/2025/06/25/coolit-systems-scales-north-american-manufacturing-to-cool-ais-next-wave/
S11 Ecolab to acquire CoolIT: https://www.businesswire.com/news/home/20260319353197/en/
S12 Ecolab closes CoolIT: https://itbrief.co.uk/story/ecolab-completes-usd-4-75-billion-coolit-takeover
S13 CoolIT CHx2000: https://www.coolitsystems.com/cdu-product/chx2000/
S14 CoolIT CHx1000: https://www.hpcwire.com/2024/12/10/ai-performance-reliability-serviceability-with-coolits-chx1000-cdu/
S15 CoolIT NVIDIA co-innovation: https://www.coolitsystems.com/capabilities/co-innovation/nvidia/
S16 CoolIT blog, 150+ patents: https://www.coolitsystems.com/resources/news/coolit-behind-the-worlds-most-advanced-ai-coldplates/
S17 OCP Cold Plate Test Spec v1.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
S18 OCP UQD v2.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf
S19 OCP PG25 Guidelines v1.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
S20 OCP PG25 base spec: https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/
S21 OCP L-L CDU methodology: https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
S22 OCP OAI liquid cooling guidelines: https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/
S23 OCP Thermal Boundaries white paper: https://www.opencompute.org/documents/white-paper-thermal-boundaries-in-ai-infrastructure/
S24 ASHRAE 5th-ed. W classes (Upsite): https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/
S25 QCT GB200 NVL72 whitepaper: https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf
S26 Electronics Cooling, Jun 2025: https://www.electronics-cooling.com/2025/06/direct-liquid-cooling-for-high-compute-servers/
S27 TechPowerUp, Vera Rubin NVL144: https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production
S28 Kuo via CTEE (Rubin TDP, gold-plated lid): https://www.ctee.com.tw/news/20260107701081-430704
S29 igor'sLAB NVL72 cooling cost: https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
S30 TechRadar / Morgan Stanley BOM: https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks
S31 TVBS, Rubin Group-A: https://news.tvbs.com.tw/english/3188903
S32 Digitimes, Rubin Group-A: https://www.digitimes.com/news/a20260318PD231.html
S33 TVBS, AVC share: https://news.tvbs.com.tw/english/3179423
S34 DCD, Rubin Ultra 600 kW: https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027
S35 Digitimes, Rubin cooling design: https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html
S36 TweakTown, B300 1.4 kW: https://www.tweaktown.com/news/103938/
S37 Introl, AMD Helios: https://introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026
S38 STH, Ironwood: https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/
S39 DCD, Google Deschutes CDU: https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
S40 Chips and Cheese, Google liquid cooling: https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips
S41 ToneCooling GB300 plate: https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/
S42 FiberMall GB200 plate: https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm
S43 ORNL Cu/CuW pin-fin plates: https://www.sciencedirect.com/science/article/pii/S0017931025014152
S44 JetCool RTX PRO 6000 datasheet: https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
S45 JetCool H100 SmartPlate: https://www.businesswire.com/news/home/20240430522600/en
S46 JetCool third-party testing: https://jetcool.com/post/third-party-testing-data/
S47 Frore LiquidJet: https://www.froresystems.com/media-room/frore-systems-introduces-liquidjet-redefining-coldplates-for-ai-data-centers ; https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/
S48 Mikros Normal Flow: https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/
S49 Wiwynn cold plates: https://www.wiwynn.com/technology/advanced-cooling/cold-plate-liquid-cooling
S50 UIUC / Fabric8Labs: https://mechse.illinois.edu/news/82871
S51 PKU, Nature Electronics 2025: https://www.nature.com/articles/s41928-025-01449-4
S52 Bio-inspired Cu MMC, Energy 2025: https://www.sciencedirect.com/science/article/abs/pii/S0360544225049114
S53 Accelsius benchmark / 4,500 W: https://www.businesswire.com/news/home/20260721991081/en/ ; https://www.datacenterdynamics.com/en/news/accelsius-tests-ability-to-cool-4500-watt-chips
S54 ZutaCore: https://zutacore.com/faq ; https://zutacore.com/solutions
S55 Wiwynn two-phase: https://www.wiwynn.com/whitepapers/innovative-two-phase-cold-plate-solutions-for-future-high-power-ai-chips
S56 R245fa two-phase GPU plates: https://www.sciencedirect.com/science/article/abs/pii/S1359431126009294
S57 ACT two-phase cut sheet: https://www.1-act.com/wp-content/uploads/2025/11/TPCP-CS-01_TwoPhaseColdPlates-DataCenters-CutSheet_V1_2025-11-12_Web.pdf
S58 Microsoft / Corintis: https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/
S59 TSMC direct-to-silicon: https://semiwiki.com/semiconductor-manufacturers/tsmc/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/
S60 Chilldyne / Daikin: https://www.storagereview.com/news/chilldyne-starter-kit-enables-rapid-liquid-cooling-adoption-in-the-data-center ; https://www.daikinapplied.com/news/news/daikin-applied-expands-data-center-offering-with-acquisition-of-chilldyne
S61 Kisitu & Ortega, split-flow: https://par.nsf.gov/biblio/10341820
S62 Split-Flow patents: https://patents.google.com/patent/US8746330B2/en ; https://patents.google.com/patent/US9603284B2/en ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12495513
S63 US 12,188,733 gazette: https://patentsgazette.uspto.gov/week01/OG/html/1530-1/US12188733-20250107.html
S64 US 12,460,878 gazette (search snippet, this session): https://patentsgazette.uspto.gov/week44/OG/html/1540-1/US12460878-20251104.html
S65 Asetek v. CoolIT: https://www.datacenterdynamics.com/en/news/coolit-wins-patent-suit-brought-by-danish-cooling-firm-asetek/
S66 Ecolab Q&A, Electronics360: https://electronics360.globalspec.com/article/24164/q-a-ecolab-bets-on-liquid-cooling-for-ai-data-center-growth
S67 Schneider, filter dP in CDU ratings: https://blog.se.com/datacenter/2025/12/16/account-for-filtering-too-beware-of-how-cdu-rating-capacity-is-specified/
S68 Shin-Etsu X23-7921-5: https://cdn.microsi.com/wp-content/uploads/2019/07/X23-7921-5-TDS-July-2019-.pdf
S69 Honeywell PTM7950: https://www.caplinq.com/ptm7950-most-thermally-conductive-phase-change-pad-with-very-low-thermal-impedance-that-works-in-vertical-applications-ptm7950.html
S70 Dow DOWFROST LC-25: https://www.chempoint.com/en-ca/products/dow/dowfrost-glycol-thermal-fluids/dowfrost-propylene-glycol-thermal-fluids/dowfrost-lc-25
S71 IDTechEx plate ASP (repost): https://onartificialintelligence.com/articles/34213/two-phase-d2c-cooling-in-data-center-thermal-management-cost-analysis
S72 Boyd HybridKIT DSC: https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf
S73 NVIDIA 800 VDC blog: https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/
S74 Uptime, 40 C GPU supply: https://intelligence.uptimeinstitute.com/entity_pdf/node/153594/pdf
S75 B300 lidless rumour (this session): https://wt6191.substack.com/p/recent-market-rumors-nvidia-b300
S76 Lenovo SR780a V3 B200 cold plate (this session): https://pubs.lenovo.com/sr780a-v3/install_front_b200_gpu_cold_plate_module
S77 Flex acquires JetCool: https://investors.flex.com/news/news-details/2024/Flex-Acquires-JetCool-to-Expand-Data-Center-and-Power-Portfolio/
S78 Jabil acquires Mikros: https://www.businesswire.com/news/home/20241003396998/en/Jabil-Acquires-Mikros-Technologies-to-Support-Demand-for-Liquid-Cooling-in-AI-Data-Centers
S79 Corintis US$24 M: https://www.yolegroup.com/industry-news/corintis-raises-24m-to-target-the-next-ai-bottleneck-and-collaborates-with-microsoft-for-chip-cooling-breakthrough/
S80 Fabric8Labs / Wiwynn NexGen: https://www.d2pmagazine.com/2026/08/14/fabric8labs-wiwynn-collaborating-to-develop-nexgen-3d-printed-cold-plates-for-ai-data-centers/
S81 USUSTK skived fins: https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink
S82 UTA, Cu plates in PG25: https://uta-ir.tdl.org/uta-ir/handle/10106/31381
S83 Wakefield on-chip plate: https://www.mouser.in/new/wakefield/wakefield-thermal-on-chip-liquid-cold-plates/
S84 Iceotope 1 kW: https://www.datacenterdynamics.com/en/news/iceotope-achieves-chip-cooling-up-to-and-beyond-1000w
S85 Vertiv GB200 reference: https://investors.vertiv.com/news/news-details/2024/Vertiv-Codevelops-with-NVIDIA-Complete-Power-and-Cooling-Blueprint-for-NVIDIA-GB200-NVL72-Platform/default.aspx
S86 TrendForce GB200 rack: https://www.trendforce.com/presscenter/news/20240730-12232.html
S87 DCD GB200 45/65 C: https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus
S88 Wccftech, Rubin Ultra cooling: https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/
S89 EE News Europe, B300 / SXM puck: https://www.eenewseurope.com/en/nvidia-tapes-out-b300-blackwell-says-report

Internal files: `docs/cooling/model/model_output.md` and `coldplate_model.py`; `appendix/physics/SYNTHESIS-physics.md`; `appendix/research/gap-*.md` and the angle reports; flow-equivalence run `appendix/synth/flow_equiv.py`.
