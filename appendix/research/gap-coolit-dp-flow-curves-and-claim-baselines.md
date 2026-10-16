# Gap fill: CoolIT pressure-drop and flow curves, and the baselines behind the Split-Flow "30 %" and OMNI "300 W/cm2 / 60 %" claims

Prepared 2026-10-13 for the cooling-architecture programme. Angle: the undisclosed pressure drop (dP) of the 15 kW plate, the 4 kW brief's page-2 curves, and the test conditions behind CoolIT's marketing ratios.

## 0. Method and status (read first)

- **No web searches could be run.** All five WebSearch calls issued by this agent were refused: the per-turn budget (200 calls, shared by every agent in this workflow) was already exhausted. One WebFetch of the 4 kW brief PDF failed on DNS (`getaddrinfo ENOTFOUND www.coolitsystems.com`), as the task warned; not retried. The user can send a follow-up message to continue the search, or raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`.
- What was done instead, and what is new in this note:
  1. **The 15 kW brief's three photographs were extracted and measured** (`appendix/pdf/img/im-000..002.png`, crops in `appendix/pdf/crops/`). They show the plate architecture, port type and relative dimensions, none of which the text discloses. This is the only primary CoolIT evidence available offline beyond the brief's text.
  2. The sibling reports (`coolit-briefs-numbers.md`, `coolit-products.md`, `test-metrics.md`, `physics/hydraulic-detail.md`, `physics/manifold-maldistribution.md`, `model_output.md`) were mined for every CoolIT dP/flow datum they had already sourced (~90 searches between them). Those URLs are repeated in Sources, tagged **[Sib]**; they were not re-fetched here.
  3. A first-principles reconstruction (`appendix/research/gap_dp_calc.py`) bounds what the brief withholds. Everything derived is tagged **[D]**; vendor statements **[V]**; independent/peer-reviewed **[I]**; the brief itself **[Brief]**.
- Bottom line: **no public source gives the 15 kW plate's dP, the 4 kW brief's page-2 curves, the Split-Flow "30 %" baseline, or the OMNI test conditions**, and none was found by any of the ~130 searches run across this workflow. The value of this note is (a) new photographic evidence that tightens the dP window, (b) a scaling argument that says what the window must be, and (c) a clean separation of which programme claims need CoolIT's curve and which do not.

## 1. What is actually known (all CoolIT dP / flow data ever published)

| Item | Value | Basis | Source | Confidence |
|---|---|---|---|---|
| 15 kW plate flow | 1.2 LPM/kW = 18 LPM, water-glycol, 45 C inlet | TTV test, 3 plates | [Brief] p.3-4 | high |
| 15 kW plate dP | **not disclosed** (plate or loop) | - | [Brief]; all press reprints [Sib] | high (that it is absent) |
| 15 kW brief's own next step | "further coldplate optimization to reduce thermal resistance **and pressure drop**" | - | [Brief] p.5 | high |
| 4 kW plate dP | **8 psi (55.2 kPa), full loop incl. fittings and QDs**, flow point not stated in excerpts (presumed 6.06 LPM = 1.5 LPM/kW) | TTV loop | PR 13 Mar 2025; StorageReview [Sib] | medium (flow point: low) |
| 4 kW plate R | Tr < 0.009 C/W, max case to inlet, TIM included | TTV | Tech brief R2 14 Mar 2025 [Sib] | high |
| 4 kW flow points | 4.28 - 6.06 LPM; heat capture 93.4 % / 94.1 % / 97.3 % (three rows, "without convection barrier or insulation") | TTV | brief index excerpts [Sib] | medium |
| 4 kW footprint / heater | "50 x 50 mm"; Tom's Hardware: heat flux "shy of 200 W/cm2" | - | PR; Tom's [Sib] | medium; whether 50 x 50 is heater or plate: low |
| Split-Flow claim | "30 % better thermal and flow performance" (4 kW PR); "up to 30 % better coolant flow and heat capture" (NVIDIA partner page); brief text qualitative ("halves the coolant's distance across the microchannels") | no baseline, no conditions | [Sib] | high (wording), none (baseline) |
| OMNI claim | > 1,500 W TDP; > 300 W/cm2; "up to 60 % lower thermal resistance vs standard microchannel coldplates" | no conditions | StorageReview 9 May 2024; coolitsystems.com/omni [Sib] | high (wording), none (conditions) |
| OCP cold-plate test spec v1.0.0 (Oct 2026, CoolIT primary author) | dP at 45 +/- 2 C at >= 6 flow points, 25-150 % of rated flow; R at multiple flows with recommended TIM | spec | [Sib] test-metrics / standards-reliability | medium (full text not retrieved) |
| Independent split-flow physics | Geometrically identical split-flow vs parallel-flow plates: similar R, **significantly lower dP** | model + experiment | Kisitu & Ortega, InterPACK 2021 [I][Sib] | high |

## 2. The 15 kW plate: new evidence from the brief's photographs

The brief contains a cover photo and two set-up photos of the plate on the TTV (p.1, p.3) and a product-style top view (extracted as `im-002.png`). Observations (visual, high confidence unless noted):

1. **Architecture.** Square-ish bare-copper plate with a **single full-length raised central manifold bar**; the **inlet and outlet ports are at opposite ends of the bar**, on the plate centre line. This is the canonical Split-Flow layout: coolant enters the centre of the fin field, splits into two streams that run outward to the two plate edges, and is collected back to the outlet end of the bar. There is **one split**, i.e. a flow length of roughly (plate width minus bar width)/2 per stream. No lid fasteners are visible: the lid is brazed or unibody (OMNI-style), consistent with "proven mass-manufacturing techniques".
2. **Ports are barbed hose fittings with worm-drive hose clamps, not UQDs.** Any dP CoolIT measured on this TTV was therefore plate + barbs + hose, with no quick-disconnect term; the 4 kW "full loop incl. QDs" basis cannot be reused as-is for the 15 kW plate.
3. **Instrumentation.** 8 spring-loaded clamp screws (uniform, calibrated clamping load), one 8-position terminal block on a small PCB (the 8 thermocouples), thermocouple leads routed under the plate (TCs in the heater/TTV face, not in the plate).
4. **Relative dimensions (measured in pixels, `gap_dp_calc.py` section A).** Plate 387 x 360 px (aspect 1.07, so slightly rectangular or slightly perspective), bar width 60 px (15.5 % of plate width), barb ridge OD 32 px (8.3 %), half-flow-length (plate - bar)/2 = 163 px (42 %), hose OD 61-69 px and clamp band ~24 px in the other photo (scale ratio 1.43 between photos).
5. **Absolute scale requires one trusted reference object.** The candidates disagree, which is why the footprint is given as a range:

| Reference assumed | Scale (mm/px) | Plate (mm) | Overall area | Bar width | Barb OD / implied bore | Half flow length | Consistency check |
|---|---|---|---|---|---|---|---|
| TC terminal-block pitch 5.08 mm | 0.237 | 92 x 85 | 79 cm2 | 14 mm | 7.6 mm / ~5 mm | 39 mm | rejected: 18 LPM at ~15 m/s in the port; clamp band would be 4 mm (no such product) |
| TB pitch 7.62 mm, 3/8 in hose, 5-6 mm mini clamp band, M6 screws | 0.356 | **138 x 128** | 177 cm2 | 21 mm | 11.4 mm / ~7 mm | 58 mm | self-consistent but port velocity 7.8 m/s at 18 LPM (ugly, lab-only) |
| 8 mm clamp band, 1/2 in hose, M8-M10 screws, TB pitch 10.16 mm | 0.477 | **184 x 172** | 317 cm2 | 29 mm | 15.3 mm / ~9.5 mm | 78 mm | self-consistent; port velocity 4.2 m/s |
| 12.7 mm band, 3/4 in hose | 0.757 | 293 x 272 | 798 cm2 | 45 mm | 24 mm | 124 mm | rejected: implies 24 mm screw heads and a 13 mm TB pitch |

   **Best estimate: plate footprint 130-185 mm square-ish (170-320 cm2 overall), low confidence (+/-30 %).** The heated (fin) area is smaller than the footprint: the sibling calibration of 76-117 cm2 heated (sections 3 and 5 of `coolit-briefs-numbers.md`; `test-metrics.md` s.2) remains compatible with the 138 mm hypothesis (fins under a ~90-110 mm central zone, lugs and port bar outside it). A 2 x 2 array of four 50 x 50 mm ceramic heaters (3.75 kW each, 150 W/cm2, i.e. four copies of the 4 kW TTV heater) fits "four ceramic heaters", "nearly 4x the 4 kW plate" and "same architectural foundation" neatly, and gives 100 cm2 heated; this is a hypothesis, not a reading [D].

6. **Port-loss consequence [D].** At 18 LPM, two barbed ports with K ~ 1.5 each cost 92 kPa (7 mm bore), 27 kPa (9.5 mm bore) or 9 kPa (12.5 mm bore). Unless the TTV ports are 5/8 in class or larger, CoolIT's own TTV loop dP at 18 LPM was dominated or heavily contaminated by port losses. That is a plausible, non-sinister reason the number was not published, and it means a CoolIT "plate dP" for this plate, if it ever appears, must be read with the port boundary stated.

## 3. Bounding the 15 kW plate's pressure drop [D]

### 3.1 The scaling argument (the most useful new result)

For a single-split Split-Flow plate with laminar skived channels, core dP ~ mu x u x L / Dh^2 with u = Q / (N x H x gap) and N ~ plate length / fin pitch. Holding **LPM/kW, W/cm2 and fin geometry constant** while scaling power P: plate side ~ sqrt(P), N ~ sqrt(P), Q ~ P, so u ~ sqrt(P) and L ~ sqrt(P): **core dP ~ P**. From 4 kW at 1.5 LPM/kW to 15 kW at 1.2 LPM/kW the factor is 3.75 x 0.8 = 3.0; the explicit geometric calculation gives 3.1-3.2 for 108, 138 or 185 mm plates (section E of the script; the factor is insensitive to the absolute plate size because N and L scale together). Two corollaries:

- A 15 kW plate that merely scales the 4 kW plate's fins with one central split would have **3x the 4 kW plate-only dP**. The 4 kW plate-only dP is itself 5-48 kPa at 6.06 LPM (section 3.2), so the scaled core would be 15-145 kPa. The upper half of that range is not deployable (CoolIT's own CDUs offer 35-53 psi secondary head for a whole rack, and the Electronics Cooling worked example budgets ~18 psi per rack [Sib]). 
- Therefore CoolIT either (a) opened the fin geometry (coarser pitch or taller fins) to hold dP within a budget, paying in convective resistance, or (b) subdivided the flow length (multiple feed slots under the lid; the external photo cannot exclude this), or (c) accepted a high dP and did not publish it. The measured unit resistance supports (a) or (c): on a max-case basis the 15 kW plate is 0.22-0.30 cm2-K/W at 76-100 cm2 heated, **no better than the 4 kW plate's <= 0.225** ([Sib] test-metrics s.2; section B of the script), even though the heat flux is lower (150-200 vs ~160-200 W/cm2). The brief's closing bullet that further work is needed "to reduce thermal resistance and pressure drop" reads as an acknowledgement that dP is a live constraint.

### 3.2 The 4 kW plate-only number is the anchor, and it is loose

The only CoolIT dP datum, 8 psi = 55.2 kPa, is "full loop incl. fittings and QDs" [Sib]. Decomposing it at 6.06 LPM (PG25, SG 1.02) with Cv-based coupling losses, dP_pair[psi] = SG (Q[gpm]/Cv)^2:

| Coupling assumption (two mated pairs) | 2 x QD (kPa) | Hoses/fittings (kPa) | **Plate-only at 6.06 LPM** | Plate-only at 4.28 LPM (n = 1.3) |
|---|---|---|---|---|
| 1/4-in or UQD02-class, Cv ~ 0.6 | 100 | - | **impossible** (> 55 kPa): rules out tiny QDs if 8 psi is at 6.06 LPM | - |
| UQD04-class, Cv ~ 1.2 | 25 | 3-8 | **22-27 kPa (3.2-3.9 psi)** | 14-17 kPa |
| UQD04-class, Cv ~ 1.8 | 11 | 3-8 | **36-41 kPa (5.2-6.0 psi)** | 23-26 kPa |
| UQD06-class, Cv ~ 3.0 | 4 | 3-8 | **43-48 kPa (6.3-7.0 psi)** | 28-31 kPa |

Cv values for UQD04/06 pairs are from memory and need verification against the OCP UQD spec and CPC/Staubli datasheets (listed in Gaps). If the 8 psi was instead measured at 4.28 LPM, every plate-only figure above scales up by (6.06/4.28)^1.3-1.75 = 1.57-1.84.

Cross-check from the fin side (same script, laminar Shah-London friction, Darcy basis, i.e. after the 4x correction noted in `physics/hydraulic-detail.md`): a 50 mm plate with 0.2 mm gaps / 0.2 mm fins / 4 mm tall and a 21 mm half-length runs at u = 0.5 m/s, Re ~ 130, and **4.5 kPa core** at 6.06 LPM; 0.15 mm gaps ~ 8 kPa; 0.10 mm gaps ~ 18 kPa (core dP ~ 1/gap^2 at fin = gap). Adding slot, turn and plenum losses (1-5 kPa), the fin-side estimate of the 4 kW plate-only dP is **6-25 kPa**, overlapping only the low end of the QD-decomposition range. The two views reconcile only if the 4 kW loop used small (UQD04-class or smaller) couplings and/or 1/4-3/8 in hose, which is plausible for a lab TTV. **Working value: 4 kW plate-only 10-30 kPa at 6.06 LPM (central 20 kPa), low-medium confidence.**

### 3.3 Resulting window for the 15 kW plate at 18 LPM, 45 C, PG25

| Scenario | Plate-only dP at 18 LPM | Hydraulic power (W) | Comment |
|---|---|---|---|
| Fins opened to a budget, single split (CoolIT "optimized to minimize pressure drop") | **25-50 kPa** | 7.5-15 | most probable; consistent with unit-R not improving vs 4 kW |
| Same fins as 4 kW (0.15-0.2 mm), single split, scaled x3.1 | 30-80 kPa | 9-24 | plausible for a demonstration TTV |
| Fine fins (0.10 mm) kept, single split | 110-145 kPa | 33-44 | unlikely (not deployable); would contradict "optimized to minimize pressure drop" |
| Two-slot feed (flow length halved) with 4 kW fins | 15-40 kPa | 4.5-12 | possible but no external evidence of a second feed |
| Sibling reconstruction (`model_output.md` 9 kPa; corrected ~19-22 kPa in `hydraulic-detail.md`; 17-42 kPa pitch sensitivity) | 9-42 kPa | 3-13 | the 9 kPa figure is the pre-correction value and should be retired; 19-22 kPa is the low edge of the window |
| **Programme working assumption** | **35 kPa plate-only, range 20-60 kPa (tail to 140)** | 10.5 | state this explicitly whenever a "lower dP than CoolIT" claim is made |

Note that at 18 LPM the hydraulic power is < 0.3 % of the load in every scenario; the system-level penalty (CDU head, manifold and QD sizing) is the real cost ([Sib] test-metrics s.8). Hence the programme should compare **plate dP at fixed LPM/kW and 45 C**, and separately report port-to-port and plate-plus-UQD-pair values.

## 4. The 4 kW brief, page 2: what the curves must look like [D]

The page-2 charts (R vs flow, dP vs flow, inlet temperature, TTV heater size, plate-only vs full loop) could not be read by any agent in this workflow; only the table rows 93.4 % / 94.1 % / 97.3 % capture at 4.28 ... 6.06 LPM surfaced in search excerpts [Sib]. Three flow points spaced 4.28 / ~5.17 / 6.06 LPM (= 1.07 / ~1.29 / 1.5 LPM/kW) are the natural reading. What the curves must contain, from physics anchored on Tr < 0.009 C/W at 6.06 LPM (max-case basis):

**R vs flow.** Model R = R_fixed (TIM + base) + R_conv(Q) x (6.06/Q)^0.4 + f_cal / (m cp), with f_cal = 0.8-1.0 the fraction of the outlet rise seen by the hottest TC (split-flow exit region). Outlet-based caloric term 1/(m cp) for PG25: 3.53 mK/W at 4.28 LPM, 2.92 at 5.17, 2.49 at 6.06 (water: 3.39 / 2.80 / 2.39).

| Assumption set | R(4.28) | R(5.17) | R(6.06) | R(8.0) | Slope (mK/W per LPM) | Caloric share of the 4.28-6.06 change | Implied R_fixed (TIM + base), 25 cm2 heater |
|---|---|---|---|---|---|---|---|
| f_cal 0.8, R_conv 2.5 mK/W | 10.2 | 9.5 | 9.0 | 8.25 | -0.68 | 69 % | 4.5 mK/W = 0.113 cm2-K/W |
| f_cal 0.8, R_conv 3.5 | 10.35 | 9.6 | 9.0 | 8.15 | -0.76 | 61 % | 3.5 = 0.088 |
| f_cal 1.0, R_conv 2.5 | 10.4 | 9.6 | 9.0 | 8.1 | -0.79 | 74 % | 4.0 = 0.100 |
| f_cal 1.0, R_conv 3.5 | 10.6 | 9.7 | 9.0 | 8.0 | -0.88 | 67 % | 3.0 = 0.075 |

So the brief's R-vs-flow curve should fall from ~10.2-10.6 to < 9.0 mK/W across 4.28-6.06 LPM, and **60-75 % of that fall is caloric**; the convective part is 25-40 %. Any CoolIT curve steeper than ~ -0.9 mK/W per LPM would indicate a maldistributed or transitional core; flatter than ~ -0.65 would indicate the "max case" TC is not at the exit. This is the slope the orchestrator wanted for the caloric/convective split; it is a reconstruction, to be replaced by the real chart when retrieved.

**Heater size and the 0.18 vs 0.225 cm2-K/W disagreement.** Tom's Hardware's "shy of 200 W/cm2" fits 4000 W / 25 cm2 = 160 W/cm2 (a 50 x 50 mm heater) better than 4000/20 = 200 W/cm2 (which is not "shy of"). If "50 x 50 mm" were the plate footprint, the heater would be smaller still and the flux above 200 W/cm2, contradicting the same sentence. **Favoured reading: 50 x 50 mm heater, 25 cm2, R''_max <= 0.225 cm2-K/W, TIM included, 1.5 LPM/kW; 0.18 is the lower-area alternative (medium-low confidence).** On the 0.225 basis the 15 kW plate's heated area would be ~76 cm2 (max-case) to ~98 cm2 (average) at ~150-200 W/cm2 (script section B), i.e. roughly a 2 x 2 heater array inside a 130-185 mm plate, consistent with section 2.

**dP vs flow.** With 8 psi at 6.06 LPM and a laminar core plus quadratic manifold/QD terms (overall exponent 1.3-1.75), the loop curve passes through 4.3-5.1 psi at 4.28 LPM and ~12-14 psi at 8 LPM; a plate-only curve would lie 1.5-4x lower (section 3.2). If the brief's chart shows "plate only" and "full loop" as separate traces, the ratio between them at 6 LPM directly gives the coupling size used, which is the single most useful number to extract when the PDF is finally read.

**Inlet temperature.** Not in any excerpt. The 4 kW PR language ("warm water") and the later 15 kW test at 45 C make 40-45 C likely; a 25-30 C inlet would raise PG25 viscosity ~1.8x and the laminar dP with it, so the inlet temperature on the dP chart matters as much as the flow.

## 5. Split-Flow brief and the "30 % better" baseline

- Retrievable text of the May 2024 Split-Flow brief (coolitsystems.com PDF; scribd 1025620831) is qualitative: the split "halves the coolant's distance across the microchannels", lowering flow impedance and case-to-fluid resistance; no chart values surfaced in any index [Sib]. The "30 %" appears in the 4 kW PR ("30 % better thermal and flow performance than standard coldplates") and on NVIDIA's partner listing ("up to 30 % better coolant flow and heat capture"); the baseline is never named.
- **Most plausible baseline [D]:** CoolIT's own prior single-pass, edge-fed parallel-flow microchannel plate of the same footprint and fin geometry (the configuration the 2021 skived brief describes before "the centre of the fin array is removed for Split-Flow"). This is the only comparison CoolIT could run on its own TTVs without naming a competitor.
- **Physics check [I][D].** For identical fins, halving the flow length and halving the per-channel velocity cuts laminar core dP by ~4x (75 %); including unchanged port, plenum and slot losses, a total-plate reduction of 30-50 % is what one expects. Kisitu & Ortega (Villanova, InterPACK 2021) found **similar thermal resistance and significantly lower dP** for split vs parallel flow of the same geometry. Two readings of "30 % better thermal and flow" are therefore consistent with the evidence: (i) at equal flow, ~30 % lower total dP with little R change; or (ii) CoolIT re-spent the dP saving on finer/longer fins to get ~30 % lower case-to-fluid R at matched dP. Either way, **the "30 %" is a within-CoolIT architecture comparison, not a benchmark against another vendor, and it says nothing about absolute dP.** The programme should not cite it as a performance datum.

## 6. OMNI: ">300 W/cm2" and "up to 60 % lower R" conditions

- No test conditions (flow, inlet, heated area, TIM, basis of R) were published in May 2024 or since; nothing in any press reprint adds them [Sib].
- **Consistency analysis [D].** CoolIT's 2021 skived brief quoted <= 0.03 C/W for Ice Lake-class CPU plates. A "60 % lower" plate would be ~0.012 C/W, which is exactly the class of the March 2025 4 kW plate (< 0.009 C/W). The 60 % figure is therefore most plausibly CoolIT's own product progression (2021 skived CPU plate -> OMNI/4 kW-class plate), not a comparison against an industry microchannel benchmark; absolute values should not be inferred from it.
- **">300 W/cm2" feasibility.** With an all-in R'' of 0.18-0.225 cm2-K/W (TIM included), 300 W/cm2 gives a 54-68 K case-to-inlet rise; at 45 C inlet that is 99-113 C case, i.e. above any GPU limit. The claim is therefore meaningful only (a) at a low inlet (25-30 C, where PG25 viscosity also raises dP ~1.8x), (b) over a small hot-spot area (1,500 W / 300 W/cm2 = 5 cm2, a 22 x 22 mm die), or (c) with a TIM-less or low-impedance interface. It is a hot-spot-capability statement, not a plate-average operating point, and should be compared only with our hot-spot sub-heater KPI (`test-metrics.md` s.9.2), never with the 15 kW plate's 150-200 W/cm2 average.

## 7. What this means for the programme's claims

1. **"Lower dP than CoolIT at 1.2 LPM/kW"** needs CoolIT's curve and is unfalsifiable today. Until the curve exists, state the claim against the explicit working assumption (35 kPa plate-only, window 20-60 kPa) **and** against the physics bound: any single-split skived plate with <= 0.2 mm channels and a 50-80 mm half-length cannot be below ~15-20 kPa port-to-port at 18 LPM (script section E; `hydraulic-detail.md`). A plate at <= 10-12 kPa port-to-port with a stated port size therefore beats every plausible CoolIT value by >= 2x, and the most probable one by 3-5x.
2. **"Equal dT at 0.9 LPM/kW" is falsifiable now, without CoolIT's dP.** The caloric penalty of running 13.5 instead of 18 LPM is +4.25 K at the outlet and +2.1 K at the mean fluid (script section G). Our plate must therefore have a (TIM + base + convection) stack >= 2.1 K (average basis) or >= 3.4 K (max-case near the exit) lower than CoolIT's, which can be demonstrated on our own parity TTV against the brief's 34.4 K / 44.2 K figures. At 0.75 LPM/kW the required margin is 3.8 K / 6.1 K.
3. **Test-protocol consequences** (adds to `test-metrics.md` s.11): report dP at three boundaries (port-to-port with port bore stated; plate + hoses; plate + a named UQD pair), at six flows 25-150 % of 18 LPM at 45 +/- 2 C, as the OCP v1.0.0 spec that CoolIT itself authored requires; also at 25-30 C inlet to expose the viscosity term. Publish the R-vs-flow slope and its caloric decomposition, which CoolIT has only ever published for the 4 kW plate.
4. **Retire the 9 kPa "CoolIT-like" figure** in `model_output.md`; use the corrected 19-22 kPa as the low edge of the window, 35 kPa as the central value.
5. **Ask for the numbers.** The two documents that would close this gap are public but unreachable from this container: the 4 kW Technical Brief R2 page 2 (PDF, or scribd/docplayer mirror) and the OCP Single-Phase Cold Plate Test Specification v1.0.0 (whose example data set, if CoolIT supplied it, may be the 15 kW plate's dP curve). The OCP Global Summit (October 2026, San Jose) is this week or imminent; any CoolIT slides would not be indexed yet.

## 8. Key numbers (with units, basis and confidence)

| # | Item | Value | Source / basis | Confidence |
|---|---|---|---|---|
| 1 | 15 kW plate dP, plate-only, 18 LPM, 45 C | undisclosed; **working 35 kPa, window 20-60 kPa, tail to 140 kPa** | [D] s.3 | low |
| 2 | 15 kW TTV port type | barbed hose fittings with worm-drive clamps, no UQDs | [Brief] photos | high |
| 3 | 15 kW plate footprint | 130-185 mm square-ish (170-320 cm2); heated zone smaller | [D] photo scaling | low |
| 4 | 15 kW port-loss at 18 LPM (2 ports, K 1.5) | 92 / 27 / 9 kPa for 7 / 9.5 / 12.5 mm bores | [D] | medium (physics), low (bore) |
| 5 | Core dP scaling, single split, fixed LPM/kW and fins | dP ~ P; 4 kW -> 15 kW factor 3.0-3.2 | [D] s.3.1 | high (physics) |
| 6 | 4 kW loop dP | 8 psi = 55.2 kPa incl. fittings + QDs | PR/StorageReview [Sib] | medium |
| 7 | 4 kW plate-only dP, 6.06 LPM | 10-30 kPa (central 20) | [D] s.3.2 | low-medium |
| 8 | 4 kW R vs flow | ~10.2-10.6 -> < 9.0 mK/W over 4.28-6.06 LPM; slope -0.68 to -0.88 mK/W per LPM; 60-75 % caloric | [D] s.4 | medium (shape), low (values) |
| 9 | 4 kW unit resistance | R''_max <= 0.225 cm2-K/W (25 cm2 heater favoured over 20 cm2 / 0.18) | [D] from Tom's "shy of 200 W/cm2" + 50 x 50 mm | medium-low |
| 10 | 15 kW implied heated area at 0.225 cm2-K/W | 76 cm2 (max-case) to 98 cm2 (avg); 150-200 W/cm2 | [D] | low |
| 11 | Caloric penalty for 0.9 LPM/kW vs 1.2 | +4.25 K outlet, +2.1 K mean; 0.75 LPM/kW: +7.6 / +3.8 K | [D] PG25 1010 kg/m3, 3930 J/kg-K | high |
| 12 | Split-Flow "30 %" baseline | unnamed; most plausibly CoolIT's own edge-fed parallel plate; physics predicts 30-50 % total dP cut at equal fins | [V][I][D] | medium |
| 13 | OMNI "60 % lower R" baseline | unnamed; consistent with CoolIT's 2021 <= 0.03 C/W CPU plate -> ~0.012 C/W | [V][D] | low-medium |
| 14 | OMNI ">300 W/cm2" | no conditions; implies 54-68 K rise at 0.18-0.225 cm2-K/W, so hot-spot or low-inlet statement | [V][D] | medium (reasoning) |
| 15 | Hydraulic power at 18 LPM | 7.5 / 10.5 / 18 W at 25 / 35 / 60 kPa (21 / 30 / 51 W electric at 35 %) | [D] | high |

## 9. Gaps / unknowns

1. **15 kW plate dP** (any boundary, any flow): not public. No press outlet, no analyst note and no sibling search found it. Only CoolIT, or an OCP example data set, can supply it.
2. **4 kW brief page 2** (R vs flow, dP vs flow, plate-only vs loop traces, inlet temperature, TTV heater size): PDF unreachable; mirrors (scribd/docplayer/pdfcoffee) not searchable this turn. Section 4 is a reconstruction.
3. **Flow point of the 8 psi loop figure** (4.28 vs 6.06 LPM): unresolved; changes plate-only estimates by 1.6-1.8x.
4. **Coupling size in the 4 kW loop** (UQD02/04/06 or barbs): unknown; dominates the plate-only decomposition. Cv values used (1.2 / 1.8 / 3.0 for mated pairs) are from memory and must be checked against the OCP UQD spec and CPC/Staubli datasheets.
5. **Absolute scale of the 15 kW photos:** the terminal-block pitch, clamp band width and hose size imply different scales; the 130-185 mm range is the overlap of the self-consistent hypotheses. A single known dimension (e.g. the TTV base plate or heater size) would fix everything.
6. **Whether the 15 kW plate has one or several feed slots** under the lid: not visible externally; it changes the dP window by ~2x.
7. **Split-Flow brief charts** (if any) and the exact baseline of "30 %": not retrievable.
8. **OMNI test conditions** for > 300 W/cm2 and 60 %: never published.
9. **OCP cold-plate test spec v1.0.0 example data** and any **OCP Summit Oct 2026 / GTC March 2026 CoolIT slides**: not retrieved; the Summit material is too recent to be indexed.
10. **NVIDIA plate-level dP budgets** (GB300 / Rubin) remain NDA; secondary sources conflict (12-150 kPa) [Sib].

## 10. Sources

Primary CoolIT (read directly)
- 15 kW Tech Brief, June 2026: local extract `appendix/pdf/brief.txt`, photos `appendix/pdf/img/im-000.png`, `im-001.png`, `im-002.png`, page renders `page-1.png`, `page-3.png`; measurement crops `appendix/pdf/crops/`. Web copy: https://www.coolitsystems.com/resources/news/15kw-coldplate/ ; PR https://www.prnewswire.com/news-releases/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-roadmap-far-beyond-2030-302787344.html [Sib]

CoolIT documents cited via sibling reports (URLs verified by them in search indexes; not fetched here)
- 4000 W Technical Brief R2 (14 Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- 4000 W press release (13 Mar 2025): https://www.prnewswire.com/news-releases/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership-302401512.html ; https://www.coolitsystems.com/resources/news/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership/
- 4 kW coverage with the 8 psi and "shy of 200 W/cm2" statements: https://www.storagereview.com/news/coolit-unveils-4000w-cold-plate-setting-new-standard-for-single-phase-direct-liquid-cooling ; https://www.tomshardware.com/pc-components/liquid-cooling/coolit-unleashes-4kw-single-phase-dlc-cold-plate-seemingly-timed-for-nvidia-blackwell-ultra-chips ; https://www.servethehome.com/coolit-shows-off-a-4kw-coldplate-for-liquid-cooling/ ; https://www.hpcwire.com/2025/03/31/coolit-systems-4000w-breakthroughredefining-single-phase-dlc-for-ultra-high-wattage-ai-processors/
- Split-Flow Technology Tech Brief (May 2024): https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf ; mirror https://www.scribd.com/document/1025620831/Split-Flow-Technology-CoolIT-Tech-Brief
- Skived Coldplate Technical Brief (Feb 2021, <= 0.03 C/W): https://www.coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf
- OMNI launch (9 May 2024): https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled ; https://www.coolitsystems.com/omni/
- Coldplate technology page: https://www.coolitsystems.com/coldplate-technology/
- CoolIT CDU heads (CHx1000/1500/2000: 35/44/53 psi) via `coolit-products.md`

Independent / standards (via sibling reports)
- Kisitu & Ortega, split-flow vs parallel-flow microchannel plates, InterPACK 2021: https://par.nsf.gov/biblio/10341820 ; https://www.researchgate.net/publication/356363419
- OCP L-L CDU test methodology (1.5 LPM/kW, >= 40 psi): https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf
- OCP Single-Phase Direct-to-Chip Cold Plate Test Specification v1.0.0 (Oct 2026): referenced in `standards-reliability.md` / `test-metrics.md` (full text not retrieved)
- Electronics Cooling (Jun 2025) DLC design guidance, ~18 psi rack budget: referenced in `coolit-briefs-numbers.md`

Programme files used
- `appendix/research/coolit-briefs-numbers.md`, `coolit-products.md`, `test-metrics.md`; `appendix/physics/hydraulic-detail.md`, `physics/manifold-maldistribution.md`; `appendix/model_output.md`
- This note's arithmetic: `appendix/research/gap_dp_calc.py` (run with `python3 -I`)
