# Gap fill: OCP Cold Plate Test Spec v1.0.0, "Thermal Boundaries in AI Infrastructure", PG25 Guidelines v1.0.0 and UQD v2.0.0 - what they specify, what we assumed, and where the two differ

Date: 2026-10-13. Angle: re-align the benchmark protocol (test-metrics.md Section 11) and the drop-in checklist (standards-reliability.md Section 9) to the OCP documents that will be used to judge any comparison with CoolIT's 15 kW coldplate, and understand the OCP "~4,000 W" single-phase boundary before the programme claims >20-30 kW scalability.

## 0. Retrieval status (read this first)

**No live retrieval was possible in this task.** The turn's shared WebSearch budget (200 calls, shared by every agent in the workflow) was already exhausted when this task started, so zero searches ran; the one permitted WebFetch attempt on the OCP test-spec PDF failed on DNS (`getaddrinfo ENOTFOUND www.opencompute.org`), as the task brief warned. No OCP PDF exists in the scratchpad (`research/dl/` is empty). Everything below is therefore built from:

- **[Sib-snip]**: text fragments of the OCP documents that sibling agents captured from search-engine extracts earlier in the run (secondary, but they are the indexed text of the real documents; the sibling reports tag them "details read from search extract; full tables not retrieved").
- **[Sib]**: sibling-report findings that were verified with URLs (OCP L-L CDU methodology, OCP OAI guideline, vendor datasheets).
- **[KB-H/M/L]**: background knowledge of the *predecessor* documents (Intel/OCP UQD v1.0, OCP OAI guideline, ASHRAE TC 9.9 water-quality tables, Intel Tcase method, JEDEC/ASTM methods) with high/medium/low confidence. The four Oct-2026 documents named in the task post-date the model's knowledge, so **none of their final text has been read by anyone in this programme**.
- **[Calc]**: calculations in `research/tools/boundary_calc.py`.

Consequence: this report (a) consolidates what is actually known, (b) states precisely which protocol/checklist lines rest on unverified assumptions, and (c) gives an exact retrieval plan (Section 8) so the next run with search budget can close the gap in <= 15 queries. Nothing here should be copied into a spec without the PDF check flagged in each row.

## 1. Document inventory and provenance

| Document | Date / status | Author / provenance | What we actually hold | Source |
|---|---|---|---|---|
| OCP Single-Phase Direct-to-Chip Cold Plate Test Specification V1.0.0 | Oct 2026 (uploaded to opencompute.org 2026/10) | Primary author Ben Sutton, CoolIT Systems [Sib]; OCP Cooling Environments project | Headline method only: R = (Tcase - Tinlet)/P at multiple flows with a recommended TIM; dP at 45 +/- 2 C at >= 6 flow points, 25-150 % of rated flow; burst example > 20 bar; He leak <= 1e-5 mbar-L/s; thermal cycling 10-65 C operating and -40/+70 C storage/shipping [Sib-snip] | https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf ; landing page https://www.opencompute.org/documents/ocp-cold-plate-test-specification-v1-0-0-pdf-1/ |
| OCP white paper "Thermal Boundaries in AI Infrastructure" | Oct 2026 | OCP Cooling Environments (authors not captured) | One fragment: single-phase cold-plate boundary "roughly 4,000 W"; Section 8.2 / Appendix B named in the task as the location; basis (per package / per die / flow / dP) **not captured** [Sib-snip] | https://www.opencompute.org/documents/white-paper-thermal-boundaries-in-ai-infrastructure/ |
| OCP PG25 Guidelines V1.0.0 | Oct 2026 | OCP Cooling Environments (Meta/Microsoft/Google/NVIDIA/Dow-class contributors expected) | Existence and scope only: in-service monitoring of glycol concentration, pH, conductivity, inhibitor, particle count, microbial count "with action limits" [Sib-snip]; **no limit values captured** | https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf |
| OCP Base Specification PG25 v1.0.0 | 2025 | OCP Cooling Environments | 25 wt % propylene glycol in DI water with inhibitor package; property tables exist [Sib]; composition/limits [KB-M] | https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/ |
| OCP Design Spec UQD v2.0.0 | Oct 2026 | OCP, Intel-originated; CoolIT credited as collaborator [Sib] | Sizes UQD02/04/06/08 and UQDB blind-mate variants; cross-vendor interoperability (CPC, Staubli, Parker, Danfoss) [Sib-snip + KB-H]; pressure/temperature classes and UQDB08 status **not captured** | https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf |
| OCP Cold Plate Development and Qualification white paper (with integrated comments) | 2024-25 | OCP Cooling Environments | Qualification-flow outline (design review, CFD, TTV correlation, leak/proof/burst, pressure and thermal cycling, compatibility soak, shock/vibration, cleanliness, long-duration flow; report template) [Sib, KB-M]; **no numbers captured** | https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/ |
| OCP L-L CDU Test Methodology & Performance Rating r1 | 2024-25 | OCP | CDU rating basis 1.5 LPM/kW; >= 40 psi TCS head; TCS components may see up to 100 psi; TCS envelope 17-65 C; ATD 3-5 C [Sib, URL-verified] | https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/ |
| OCP OAI System Liquid Cooling Guidelines | Mar 2023 | OCP OAI (Meta/Microsoft-led) | 1 kW OAM: 1-2 LPM per module; recommended coolant rise 7.5-12 C; case-to-inlet 0.015-0.016 C/W at high flow; PG25 or DI water; **phase-change TIM** as the reference interface [Sib, URL-verified] | https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/ |
| OCP ACS Cold Plate Leak Detection and Intervention white paper | 2024-25 | OCP ACS | Leak-detection architecture and intervention logic [Sib] | https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1 |
| OCP ACS / ORv3 "Cold Plate Requirements" (first generation) | ~2021-22 | Meta-led ORv3 liquid-cooling workstream | Not located with a URL by any agent; content [KB-L] | not located |

Read-across: CoolIT wrote the test spec, collaborated on UQD v2.0.0, and its new owner Ecolab is positioning on coolant chemistry (PG25 Guidelines territory) [Sib coolit-products, market-business]. The three yardsticks that will be applied to our plate are all CoolIT-adjacent; the only defence is to publish in their format with more complete data than CoolIT itself has (the 15 kW brief has one flow point, no dP, no TIM identity, no cycling data [Brief]).

## 2. OCP Cold Plate Test Specification V1.0.0: known text vs. open questions

### 2.1 What is captured [Sib-snip]

| Item | Captured value | Confidence |
|---|---|---|
| Thermal metric | R = (T_case - T_inlet) / P, absolute K/W, measured at multiple flow rates, with a *recommended* TIM | medium (snippet) |
| dP measurement | coolant at 45 +/- 2 C; >= 6 flow points spanning 25 % to 150 % of rated flow | medium |
| Burst | "example > 20 bar" (wording suggests an example/illustrative value, not a universal shall) | medium-low |
| Leak | helium <= 1e-5 mbar-L/s | medium |
| Thermal cycling | 10-65 C operating; -40 / +70 C storage/shipping | medium; cycle counts not captured |

### 2.2 What the task asked for and is NOT captured (with the best available prior)

| Question | Best prior | Basis / confidence | Protocol consequence until verified |
|---|---|---|---|
| Definition of "case" | Top surface of the package lid (IHS) or heater face at the geometric centre of each heated zone; TC bead in a shallow groove, flush with the surface, under the TIM | Intel TMSDG/TTV Tcase convention (36 AWG Type T bead, ~0.3-0.5 mm groove, thermally conductive epoxy, zero-degree lead exit) [KB-M]; OCP OAI guideline uses "case" the same way [Sib]; the sibling photogrammetry concludes CoolIT's TCs are in the TTV heater face, the same plane [Sib gap-ttv] | Report bead depth, groove size, bead material, and the surface-extrapolation correction (0.4-5 K depending on heater material at 125 W/cm2 [Sib gap-ttv]) |
| TC count / positions | Likely "one per heated zone minimum, at the zone centre; additional at corners/edges", possibly a minimum of 4-8 | OCP OAI used multiple TCs on the OAM; CoolIT used 8 on 4 heaters [Brief]; [KB-L] | Keep 8 mirrored positions + 4 extra (centre and three corners) as in test-metrics 11; label which would be OCP-mandatory vs extra |
| Recommended TIM | A named phase-change material (PTM7950-class) is the most probable, because the OCP OAI guideline's reference interface is a phase-change TIM and CoolIT's own "standard thermal paste" wording would otherwise be codified as grease | OCP OAI [Sib]; sibling TIM report lists PTM7950 as "OCP OAI reference TIM" [Sib tim]; [KB-M] | Run every plate with (i) the OCP-recommended TIM, whatever it is, (ii) a named grease at measured BLT, (iii) best interface; ASTM D5470 impedance at the actual clamp pressure for each |
| Rated flow | Manufacturer-declared flow at which thermal performance is quoted; dP sweep is 25-150 % of it. Whether the spec also fixes a per-kW convention (1.2 or 1.5 LPM/kW) is unknown; OCP's only codified per-kW basis is 1.5 LPM/kW in the L-L CDU methodology [Sib] | [Sib-snip] + [Sib] | Declare rated flow = **1.0 LPM/kW (15 LPM at 15 kW)**; the 25-150 % sweep (3.75-22.5 LPM) then brackets CoolIT's 18 LPM (1.2) and NVIDIA's 0.75 LPM/kW envelope, so one curve answers both |
| dP boundary (plate-only vs with QDs/hoses) | Unknown. OCP CDU methodology measures at CDU ports; OAI guideline reports module-level dP including the OAM's hoses but excluding rack QDs [KB-M]. Most probable test-spec boundary: pressure taps at the plate's own inlet/outlet fittings (plate + fittings, no QD, no hose), with the spec requiring the boundary to be stated | [KB-M] | Report three dP curves: plate-only (port-loss corrected), plate + stubs/hose, plate + UQD pair; name the tap locations and fluid temperature. CoolIT's only dP datum (4 kW: 8 psi "full loop incl. fittings and QDs") and its 15 kW TTV with 1/2-in barbs [Sib gap-dp, gap-ttv] cannot be compared to any of these without that statement |
| Proof pressure | Not captured; industry convention 1.5x MAWP, 5-30 min, no leak, no permanent deformation | hyperscaler SOWs [KB-M] | Keep 1.5x; state MAWP explicitly (>= 100 psi / 6.9 bar, preferred 150 psi) |
| Burst | "> 20 bar example" [Sib-snip]; convention >= 3x MAWP (JetCool datasheet: 72 psi continuous / 216 psi burst = 3x [Sib]) | medium | Design burst >= 3x MAWP and >= 20 bar (both) |
| Pressure cycling | Not captured; typical SOW 10,000-100,000 cycles between 0 and MAWP at 0.1-1 Hz | [KB-L] | Keep >= 10,000 cycles 0-MAWP; verify count and waveform |
| Thermal cycling count / ramp | Temperature windows captured [Sib-snip]; counts not. Typical 100-1,000 cycles operating, 10-50 cycles non-operating, with leak + R + dP re-check | [KB-M] | Keep 1,000 operating / 50 storage cycles; acceptance drift R <= 5 %, dP <= 10 % |
| Heat-capture / calorimetry | Not captured. Likely requires fluid-side energy balance (m cp dT) vs electrical power agreement | OAI guideline reports heat capture; CoolIT 4 kW brief reported 93-97 % capture "without insulation" [Sib] | Require >= 98 % capture with guard insulation; publish the energy-balance closure |
| Report template | Not captured. Expected fields: plate ID, TTV description and heater map, TIM and BLT, coolant (PG25 lot, glycol % by refractometer), inlet temperature, flow points, per-TC temperatures, R per flow, dP per flow with boundary, uncertainty, cycling results, leak result, burst result, photos | [Sib standards 3; KB-M] | test-metrics Section 11 already lists all of these; add "OCP template section numbers" column once the PDF is read |

### 2.3 Items in our protocol that the OCP spec cannot be assumed to contain

- Power-weighted mean vs unweighted mean of TCs, and max-TC basis: OCP almost certainly reports per-TC data and leaves the average to the reader; CoolIT's brief uses an unweighted 8-TC mean [Brief]. Our report must give max, unweighted mean (CoolIT-comparable) and power-weighted mean.
- Unit resistance (cm2-K/W) with heater area: OCP uses absolute K/W [Sib-snip]; we report both.
- Uncertainty budget (k = 2) and plate-to-plate CpK: not expected in v1.0.0; keep as our differentiator (CoolIT's 10.1 K plate-to-plate spread at TC8 [Brief] is exactly what CpK reporting exposes).
- Transient step/cycle response: not expected in a steady-state test spec; keep as an annex.

## 3. The OCP "~4,000 W" single-phase boundary: what it can mean and how it reconciles with 15 kW

Only the fragment "roughly 4,000 W" is known [Sib-snip]. Three physically distinct readings fit the number; each has different consequences for our >20-30 kW claim. All calculations use PG25 at ~50 C (rho 1,010 kg/m3, cp 3,930 J/kg-K) [Sib test-metrics] and a 35 K case-to-inlet budget (80 C case at 45 C inlet, CoolIT's own convention [Brief]).

| Reading | Arithmetic | Result | Fit to "~4,000 W" | Consequence |
|---|---|---|---|---|
| **A. Per-package area x flux x unit-resistance budget** (lidded package with TIM, 25-33 cm2 effective heated area, practical R'' incl. paste 0.2-0.3 cm2-K/W) | Q = A x dT / R'' = 25-33 cm2 x 30-35 K / (0.2-0.3) | **3.5-4.6 kW** at 120-175 W/cm2 [Calc] | exact | This is CoolIT's own 4 kW plate (50 x 50 mm heater, 160 W/cm2, R''max <= 0.225 cm2-K/W [Sib test-metrics]). The 15 kW plate does **not** break this boundary: it spreads 15 kW over ~120 cm2 (four heaters, ~125 W/cm2, R''avg ~0.275 / R''max ~0.355 cm2-K/W [Sib gap-ttv]), i.e. a *larger* area at *equal or worse* unit resistance. A per-package boundary moves only if R'' falls. |
| **B. Per-die flux limit for direct-to-die single-phase microchannels** | one reticle die ~8.3 cm2 at the ~500 W/cm2 practical single-phase water limit | **~4.1 kW per die** [Calc] | exact | Requires R'' ~ 0.07 cm2-K/W with no TIM, i.e. the peer-reviewed manifold-microchannel band (0.065-0.09 cm2-K/W [Sib physics-options]). If Appendix B is written this way, the boundary is a *flux* boundary and a two-die Rubin-class package is ~8 kW, not 4. |
| **C. Hydraulic / interface boundary at AI flow rates** (1.5 LPM/kW through a 1/4-in UQD04-class tray coupling) | 4 kW -> 6 LPM; UQD04 pair dP 22-41 kPa at 6 LPM [Sib gap-dp]; 15 kW -> 18 LPM -> (18/6)^2 = 9x -> 200-370 kPa for the QD pair alone; hose velocity 14.8 m/s in 1/4-in, 3.7 m/s in 1/2-in [Calc] | 4-5 kW is the ceiling per UQD04 loop; 15 kW needs UQD08/1/2-in | good | CoolIT's 15 kW TTV is plumbed with 1/2-in-class barbs and hose, not tray QDs [Sib gap-ttv]; the demonstration sidesteps the interface boundary. A tray-level 15 kW claim must be made with UQD08/UQDB08 and the QD dP included. |

What does *not* fit: a caloric reading. The bulk rise at fixed LPM/kW is independent of Q (0.75 LPM/kW -> 20.2 K; 1.0 -> 15.1 K; 1.2 -> 12.6 K; 1.5 -> 10.1 K [Calc]), so the coolant itself sets no wattage boundary, only a per-kW flow requirement.

**Working conclusion [Calc + Sib]:** until Section 8.2 / Appendix B is read, treat the OCP boundary as reading A (per-package, lidded, with TIM, at ~0.2-0.3 cm2-K/W and 35 K). On that basis (i) CoolIT's 15 kW and the OCP 4 kW are not in contradiction: 15 kW is 4 kW x ~4x area; (ii) the honest statement of our scalability is "**X W per cm2 of heated area at R'' = Y cm2-K/W, dT = 35 K, at Z LPM/kW**", not "N kW per plate"; (iii) the only way to move the per-package boundary is to cut R'' (TIM2 to <= 0.02-0.05 cm2-K/W via PCM/liquid metal, short-flow-length manifold core at 0.065-0.09 cm2-K/W [Sib physics-options, tim]), which the sibling model already shows takes the benchmark footprint from 15 kW at 34.4 K to ~15-17 K mean, i.e. headroom to ~30-40 kW in the same 120 cm2 at 80 C case [Sib physics-options]. That is a defensible >20-30 kW claim *per 120 cm2 plate*, and a ~8-12 kW claim *per two-die package* - never a per-package 15-30 kW claim.

## 4. OCP PG25 base spec and PG25 Guidelines: what the action limits are likely to be

Captured: the Guidelines monitor glycol concentration, pH, conductivity, inhibitor concentration, particle count and microbial count with action limits [Sib-snip]; values not captured. The base spec is 25 wt % PG in DI water with an inhibitor package; cp ~3.94 kJ/kg-K at 50 C (Dow DOWFROST LC-25 class [Sib]).

Best prior for the limit table, from the ASHRAE TC 9.9 TCS water-quality guidance that the OCP documents descend from [KB-M; sibling fouling report quotes the same table at M confidence]:

| Parameter | Likely limit / action band | Confidence | Why it matters to the plate |
|---|---|---|---|
| Glycol concentration | 25 +/- 2-3 wt % (refractometer); freeze protection ~ -10 C | KB-M | viscosity and cp at the test point; log the lot and % in every test |
| pH | 7.5-9.5 (ASHRAE 7-9 general; 8-9.5 for copper-dominant inhibited loops) | KB-M | copper passivation window; elastomer selection |
| Conductivity | inhibited PG25 is intrinsically ~1-3 mS/cm; the action limit is a *drift* limit, not a purity limit | KB-L | not a plate design input |
| Inhibitor reserve | >= 80 % of as-shipped (organic-acid / azole copper package) | KB-L | depletion precedes copper corrosion in sub-0.3 mm channels |
| Chloride / sulfate | < 25-50 ppm Cl; < 100 ppm SO4 | KB-M | pitting of copper; stainless crevice corrosion at QDs |
| Bacteria | < 100-1,000 CFU/mL; biocide dosing | KB-M | biofilm in 2-3 mm manifold-fed channels; no dead legs |
| Particulate / filtration | 50 um nominal at the CDU as the common floor; 25 um recommended for sub-0.2 mm channel plates; particle count by ISO 4406-type classes | KB-M | the single most important input to our minimum-passage rule (>= 3x absolute filter rating; 0.15 mm at 50 um absolute, 0.27 mm at 50 um nominal; 0.075 mm only with 25 um absolute) [Sib fouling] |
| Dissolved copper / iron | < 1-2 ppm Cu as a corrosion tripwire | KB-L | plate-side corrosion monitoring during the 1,000-3,000 h soak |

Ecolab (CoolIT's owner since July 2026) publicly attributes recent field cold-plate problems to incomplete flushing and particulates migrating into plates [Sib coolit-products, Electronics360 Oct 2026]. That is the commercial reason the Guidelines exist and the technical reason our architecture should keep the smallest wetted passage at >= 0.15 mm wherever only CDU-level 50 um filtration is guaranteed, or add a 25 um last-chance screen at the plate inlet (2-5 kPa) [Sib manufacturing-cost, fouling].

## 5. OCP UQD v2.0.0: sizes known, classes unknown

| Item | Known | Confidence | Source |
|---|---|---|---|
| Sizes | UQD02 (1/8 in), UQD04 (1/4 in), UQD06 (3/8 in), UQD08 (1/2 in); UQDB blind-mate variants for ORv3 vertical manifolds | high | [Sib-snip] + [KB-H] |
| Interoperability | cross-vendor mating (CPC Everis, Staubli, Parker, Danfoss, others) is the spec's purpose; v2.0.0 credits CoolIT as collaborator | high | [Sib] |
| Pressure classes | **not captured.** Predecessor (Intel-origin UQD v1.0) and vendor datasheets: working ~7-8.6 bar (100-125 psi), proof 1.5x, burst >= 3-4x; vacuum-tolerant | KB-L/M | sibling standards table (KB-M) |
| Temperature classes | **not captured.** Vendor bodies -40 to +115 C; fluid service typically 2-65 C (OCP TCS envelope 17-65 C [Sib L-L CDU]) | KB-M | |
| Mating cycles / spill | dry-break, double shut-off, spillage < a few drops per cycle, >= 1,000 cycles (vendors quote thousands) | KB-M | |
| UQDB08 status | **unknown** whether v2.0.0 finalises a 1/2-in blind-mate envelope; secondary sources say NVIDIA/ODMs are moving to 1/2-in for > 200 kW racks (Rubin / Kyber) | low | [Sib chip-roadmap, competitors-singlephase] |

Design consequence (unchanged from standards-reliability Section 9, item 12, but now with the reason): the plate must not force the tray to a larger QD than the tray already carries. For a 15 kW-class load the tray QD *will* be UQD08/UQDB08 (reading C above), so the plate's stubs should be 1/2-in-class (12-13 mm bore), and the plate-only dP should leave >= 50 % of the tray budget to the QD pair and hoses.

## 6. Other OCP values that are verified and should be carried forward unchanged

| Value | Source | Status |
|---|---|---|
| CDU rating basis 1.5 LPM/kW; >= 40 psi (2.8 bar) TCS head; TCS components may see up to 100 psi (6.9 bar); TCS 17-65 C; ATD 3-5 C | OCP L-L CDU methodology r1 [Sib, URL-verified] | keep |
| 1 kW OAM: 1-2 LPM; coolant rise 7.5-12 C; case-to-inlet 0.015-0.016 C/W at high flow; phase-change TIM reference | OCP OAI guideline Mar 2023 [Sib, URL-verified] | keep; use 7.5-12 C as the OCP rise window (1.2 LPM/kW PG25 gives 12.6 K, at the top edge) |
| No OCP/ASHRAE/NVIDIA document codifies 1.2 LPM/kW | [Sib coolit-briefs, URL-verified Electronics Cooling Jun 2025] | keep |
| CoolIT 4 kW plate: R < 0.009 C/W max-case incl. TIM at 1.5 LPM/kW; 8 psi full loop incl. QDs | CoolIT 4 kW brief [Sib] | keep |

## 7. Line-by-line re-alignment of test-metrics Section 11 and standards-reliability Section 9

Legend: OK = consistent with captured OCP text; ASSUMED = rests on [KB] and must be checked against the PDF; ADD = OCP will probably require it and we had not listed it explicitly.

| # | Our protocol / checklist line | OCP status | Action |
|---|---|---|---|
| T1 | R = (Tcase - Tin)/Q, absolute K/W, PG25, 45 C inlet | OK [Sib-snip] | also give cm2-K/W with heater area |
| T2 | R at >= 3 flows | OK ("multiple flows") | adopt the same >= 6 points as dP, 25-150 % of rated |
| T3 | Rated flow declared as 1.0 LPM/kW (15 LPM) | ASSUMED (definition not captured) | declare explicitly; show 18 LPM and 11.25 LPM as named points |
| T4 | dP at 45 +/- 2 C, >= 6 points, 25-150 % rated | OK [Sib-snip] | state mean-fluid temperature used for correlation |
| T5 | dP boundary plate-only (port-loss corrected) | ASSUMED | publish three boundaries (Section 2.2) |
| T6 | TIM: OCP recommended + named grease + best interface | ASSUMED (TIM identity not captured; PCM most probable) | obtain the named TIM from the PDF; D5470 at clamp pressure |
| T7 | TCs: 8 mirrored + 4 extra; groove, bead depth, extrapolation documented | ASSUMED (case definition and TC method not captured) | keep; mark which are OCP-mandatory after reading |
| T8 | Heat capture >= 98 % with guard insulation; energy-balance closure <= 3 % | ADD | OCP likely requires calorimetric closure; keep |
| T9 | Uncertainty k = 2; plate-to-plate CpK; power-weighted mean | beyond OCP | keep as differentiator |
| T10 | Post-cycling R drift <= 5 %, dP <= 10 % | ASSUMED (acceptance not captured) | verify |
| S5 | Plate-only dP <= 25 kPa at 1.0 LPM/kW, <= 35 kPa at 1.2; tray <= 100 kPa incl. QDs | self-set targets; OCP gives method not limits | keep; derive tray budget from CDU head (40 psi OCP floor) |
| S6 | MAWP >= 100 psi (6.9 bar), preferred 150 psi; proof 1.5x; burst >= 3x and >= 20 bar; vacuum to -0.9 bar(g) | burst 20 bar OK [Sib-snip]; proof multiple ASSUMED; MAWP from OCP CDU 100 psi [Sib] | verify proof value and hold time |
| S7 | He leak <= 1e-5 mbar-L/s (target 1e-6); 100 % production test | OK [Sib-snip]; 1e-6 target is ours | keep |
| S8 | Thermal cycling 10-65 C / -40/+70 C; pressure cycling >= 10,000 cycles 0-MAWP | windows OK [Sib-snip]; counts and pressure cycling ASSUMED | verify counts, ramp rates, dwell |
| S9 | Wetted materials Cu / Ni-Cu / 316L / peroxide EPDM / PTFE-PPSU-PEEK; no Al, Zn, NBR, silicone | ASSUMED (OCP wetted list not read; ASHRAE-derived) | verify against PG25 base spec compatibility annex |
| S11 | Smallest passage >= 3x absolute filter rating, or 25 um filtration + blockage tolerance | ASSUMED (PG25 Guidelines filtration rating not captured) | verify the filtration micron rating and whether it is nominal or absolute - this single number sets our minimum channel width |
| S12 | 3/8 or 1/2 in stubs; tray QDs UQD04/06/08, UQDB per v2.0.0 | sizes OK; pressure/temperature class ASSUMED; UQDB08 status unknown | verify; specify 1/2-in-class stubs for 15 kW |
| S14 | Thermal reporting in OCP v1.0.0 format | OK in principle; template not captured | map to template section numbers after reading |
| S16 | 1,000-3,000 h PG25 soak at 65 C with coupons; dP drift <= 10 % | ASSUMED | verify whether the Development & Qualification paper fixes duration |
| S17 | Cleanliness: flushed, particle-counted, capped | ASSUMED | verify whether PG25 Guidelines give a shipping-cleanliness class |
| S23 | Scalability claim ">20-30 kW" | must be restated per Section 3: per-cm2 and per-package, with R'', dT, LPM/kW and QD size | reword in all deliverables |

## 8. Retrieval plan for the next run (<= 15 queries, in priority order)

1. extended: "OCP-Cold-Plate-Test-Specification-V1.0.0" "case temperature" thermocouple groove - capture the case definition and TC method.
2. extended: "Cold Plate Test Specification" OCP "recommended" "thermal interface material" - capture the named TIM and clamp pressure.
3. extended: "Cold Plate Test Specification" OCP "rated flow" definition "pressure drop" "pressure taps" - capture rated-flow and dP boundary.
4. extended: "Cold Plate Test Specification" OCP "proof pressure" "burst" "cycles" "helium" table - capture the numeric table and cycle counts.
5. extended: "Thermal Boundaries in AI Infrastructure" OCP "4,000 W" OR "4 kW" "single-phase" "Appendix B" - capture the basis of the boundary (per package / per die, flow, dP, R'').
6. extended: "Thermal Boundaries in AI Infrastructure" OCP "8.2" cold plate "W/cm2" - capture the flux assumption.
7. extended: "OCP-PG25-Guidelines-V1.0.0" "action limit" OR "action level" filtration "micron" "particle" - capture the filtration rating (nominal vs absolute) and particle-count classes.
8. extended: "OCP-PG25-Guidelines-V1.0.0" pH conductivity "inhibitor" "glycol concentration" table - capture the chemistry action limits.
9. extended: "OCP Base Specification PG25" v1.0.0 "wetted materials" OR "compatibility" table - capture the approved-materials list.
10. extended: "OCP-Design-Spec_UQD_v2.0.0" "pressure" "class" OR "rating" "temperature" table - capture the pressure/temperature classes.
11. extended: "UQD v2.0.0" UQDB08 OR "UQDB 08" "1/2" blind mate OCP - capture UQDB08 status.
12. extended: OCP "Cold Plate Development and Qualification" "pressure cycling" OR "thermal cycling" cycles table - capture the qualification matrix numbers.
13. standard: OCP ORv3 "cold plate" requirements "proof pressure" "burst pressure" Meta - locate the first-generation requirements document.
14. standard: CPC Everis UQD04 datasheet pressure temperature Cv; Staubli OCP UQD datasheet Cv - verify the QD Cv values used in the dP decomposition [Sib gap-dp].
15. standard: ASHRAE TC 9.9 "Water-Cooled Servers" water quality table pH chloride sulfate bacteria - verify the Section 4 priors.

If WebFetch remains blocked, ask the orchestrator for a session with the OCP PDFs attached as uploads; a 20-minute read of the four PDFs closes every ASSUMED row in Section 7.

## 9. Gaps / unknowns

1. **Zero live sources in this task.** Every row marked ASSUMED or [KB] above is unverified; the captured OCP text [Sib-snip] is itself from search-engine extracts, not the PDFs.
2. OCP Cold Plate Test Spec v1.0.0: case definition, TC method, recommended TIM, rated-flow definition, dP boundary and tap positions, proof value, pressure-cycling and thermal-cycling counts, acceptance drift limits, report template - all unread.
3. OCP "Thermal Boundaries in AI Infrastructure": the basis of "~4,000 W" (per package vs per die, assumed R'', dT, flux, LPM/kW, QD size) is unread; Section 3 gives three candidate readings, all consistent with the number, with different consequences.
4. OCP PG25 Guidelines v1.0.0: no action-limit values captured; the filtration micron rating and whether it is nominal or absolute is the single most consequential unknown for the channel-width decision.
5. OCP UQD v2.0.0: pressure/temperature class table and UQDB08 status unread; QD Cv values used by the sibling dP decomposition are from memory.
6. OCP Cold Plate Development & Qualification white paper: no numbers captured (cycle counts, soak durations, cleanliness classes, shock/vibration levels).
7. First-generation OCP ACS / ORv3 cold-plate requirements document not located by any agent.
8. Whether CoolIT's "case" (heater-face TC) is metrologically equivalent to an OCP lid-groove Tcase depends on the heater material and bead depth (0.4-5 K at 125 W/cm2 [Sib gap-ttv]); only the PDF plus a CoolIT disclosure can settle it.

## Sources

Primary OCP documents (URLs located by sibling agents with search; none read in full by any agent):
- OCP Single-Phase Direct-to-Chip Cold Plate Test Specification V1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf ; https://www.opencompute.org/documents/ocp-cold-plate-test-specification-v1-0-0-pdf-1/
- OCP white paper, Thermal Boundaries in AI Infrastructure (Oct 2026): https://www.opencompute.org/documents/white-paper-thermal-boundaries-in-ai-infrastructure/
- OCP PG25 Guidelines V1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
- OCP Base Specification PG25 v1.0.0: https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/
- OCP Design Spec UQD v2.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf
- OCP Cold Plate Development and Qualification white paper: https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/
- OCP ACS Cold Plate Leak Detection and Intervention white paper: https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1
- OCP L-L CDU Test Methodology and Performance Rating r1: https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- OCP OAI System Liquid Cooling Guidelines (Mar 2023): https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/

Benchmark and sibling-verified sources reused:
- CoolIT 15 kW Tech Brief (June 2026): local extract `appendix/pdf/brief.txt`
- CoolIT 4 kW Technical Brief R2 (Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- JetCool RTX PRO 6000 SmartPlate datasheet (72 psi continuous / 216 psi burst): https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
- Dow DOWFROST LC-25 (PG25-class) properties: https://www.chempoint.com/en-ca/products/dow/dowfrost-glycol-thermal-fluids/dowfrost-propylene-glycol-thermal-fluids/dowfrost-lc-25
- Google Deschutes CDU (80 psi): https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
- Electronics360 Computex 2026 CoolIT 15 kW: https://electronics360.globalspec.com/article/23837/computex-2026-coolit-pushes-single-phase-dlc-to-15-kw
- UTA thesis, copper degradation in PG25 loops: https://uta-ir.tdl.org/uta-ir/handle/10106/31381

Sibling reports drawn on: `research/standards-reliability.md`, `research/test-metrics.md`, `research/coolit-briefs-numbers.md`, `research/chip-roadmap-requirements.md`, `research/gap-coolit-dp-flow-curves-and-claim-baselines.md`, `research/gap-coolit-15kw-ttv-footprint-heater-map.md`, `physics/fouling-filtration.md`, `physics/tim-and-direct-to-die.md`, `physics/physics-options.md`. Calculation script: `research/tools/boundary_calc.py`.

Background-knowledge documents named without URL (verify): Intel Thermal Mechanical Specification and Design Guides (Tcase groove thermocouple method); Intel/OCP UQD specification v1.0 (2020-21); ASHRAE TC 9.9 "Water-Cooled Servers: Common Designs, Components, and Processes" (2019) water-quality table; ASTM D5470; JEDEC JESD51-14; ISO 4406 particle-count classes.
