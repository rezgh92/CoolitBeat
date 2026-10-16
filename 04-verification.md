# How the architecture was stress-tested

This note records how the PRISM architecture was attacked before it reached `03-architecture.md`, and what each round changed. The detailed reports and scripts are in `appendix/`.

The review ran in five rounds. Each round could overturn the previous one, and several did.

| Round | What ran | Where |
|---|---|---|
| 1. Evidence | 12 research angles, a completeness critic, 10 targeted gap fills, one synthesis | `appendix/research/`, `01-benchmark-and-requirements.md` |
| 2. Physics | 8 quantitative checks with their own scripts, one synthesis | `appendix/physics/`, `02-physics-basis.md` |
| 3. Design panel | 8 independent architecture proposals, each scored by 3 judges (physics, manufacturing, strategy), then a merged draft | `appendix/design/` |
| 4. Verification | 5 adversarial refuters (physics, hydraulics, manufacturing, cost and market, IP), 1 gap-closer, a completeness critic, a final revision | `appendix/verify/verify-*.md`, `appendix/verify/final/` |
| 5. Audit | consistency and traceability audit: every script re-run, every cited number and file checked | `appendix/verify/audit/` |

## Round 2: what the physics checks changed

- **The first scoping model had channel friction 4x too low.** It used the Fanning friction factor in a Darcy formula. Fixed in `model/coldplate_model.py`.
- **Short manifold cells raise the coolant term.** A 4-8 mm cell stays nearly isothermal, so the wall runs hotter than a linear coolant ramp would suggest: 0.60-0.68 of the outlet rise instead of 0.5.
- **Fouling sets a channel floor.** A 10-year drop-in plate needs 0.15 mm gaps behind a 50 µm absolute screen. 0.10 mm needs loop filtration of 33 µm or better, and anything finer is off the roadmap.
- **The first manifold sizing failed.** Slots ran at 9 m/s against a 0.7 kPa branch and would have reversed flow. Headers and slots grew about tenfold in cross-section.
- **Two-phase and counter-flow interdigitation were rejected** for the baseline, with stated re-entry conditions.

## Round 3: what the design panel changed

Scores ranged from 54.7 to 61.3 out of 100. No proposal survived intact.

| Proposal | Mean score | Fate |
|---|---:|---|
| Proven-subset, 12-month programme (PSM-12) | 61.3 | base architecture |
| Advanced manufacturing | 60.3 | development rig, fin-conduction ceiling, lid rules grafted |
| Power-electronics-first | 59.7 | keyed orifices, filtration grades, direct-substrate SiC cooler grafted |
| Conventional-cost (CrossComb) | 59.2 | fly-cut-after-braze base, 100 % flow test grafted |
| Jet hybrid | 56.7 | coupon method and inertial branch rule grafted; jets dropped (IP, erosion, small gain) |
| Direct-to-die | 56.3 | interface tiers by face finish, liquid-metal containment grafted |
| System platform | 56.0 | filtration ladder, rack rules grafted |
| HMMC elite | 54.7 | interface tiers, HBM pedestal grafted; wide slot openings found to short-circuit about 70 % of the flow |

The judges found two problems that every proposal shared. Diffusion bonding crushes 0.15 mm fins at the pressure it needs. Wide feed openings over the fin tips let coolant bypass the fins, a Hele-Shaw effect worth up to 10.8 K in 2-D. The merged draft answered both with narrow recessed windows, full-height kerfs and a braze with low clamping load.

## Round 4: what verification changed

| Lane | Most important findings | Resolution in the final |
|---|---|---|
| Physics | Headline about 1.5 K optimistic, because it borrowed CoolIT's calibration-absorbed 2-D penalty. The CoolIT 4 kW point was a loss, not a tie. The 350 W/cm2 margin was mislabelled. | Every absolute number now carries the plate's own 2-D penalty, with PG25 conductivity corrected to 0.49 W/mK. The 4 kW loss and the 100 cm2 parity are stated as concessions. |
| Hydraulics | The 18-line layout left dead fin strips at the edges and overfed one segment 1.68x. Capacity claims broke the plate's own velocity limits. Segment-level imbalance was hidden by line-level checks. | 15-line layout with edge outlets. Ratings capped at 19.5 kW. Doubled outlet header and 0.5 kPa outlet orifice row bring segment max/min to 1.06. The water-table test now passes or fails at segment level. |
| Manufacturing | Stamped 4.5 mm plenum laminations cannot be made: the webs are too thin. A single unbonded braze strip passes proof testing undetected. | Folded 0.8 mm copper plenum and drawn cap replace the laminations and forged bar. Tie detection is gated at the first experiment, with a 1.0 mm base fallback. |
| Cost and market | Cost was about US$50 low (silver filler, furnace count, yield). The facility value case was overstated. Group-A suppliers cannot insert a new plate design into NVIDIA's centrally specified buy. | Cost re-based to US$165, against about US$126 for a like-sized incumbent. NVIDIA is approached through its thermal engineering team. Hyperscaler programmes lead. |
| IP | The kerf design-around of CoolIT's Split-Flow patents is weak. A Taiwan family member exists. The microjet position conflicted with the draft's own model. | No US sale before a freedom-to-operate opinion at M4, and none before September 2028 unless it clears. Jets now land on the grate lip, not the fins. Taiwan manufacture waits on a claim chart. |
| Gap-closer | The cost, height and mass penalties came from the forged bar, the thick laminations and a separate meter sheet, none of which the physics needs. | The lean stack was adopted as Rev A: 20.8 mm instead of 26.4 mm, 1.24 kg instead of 1.74 kg, US$165 instead of US$209. |

The completeness critic added the views a funding decision needs: rack and CDU integration, controls and telemetry, serviceability, leak safety, sustainability, compliance and tariffs, a competitor table beyond CoolIT, a P&L sketch, and 20 anticipated objections with answers.

## Round 5: what the audit found

All six final scripts re-ran and reproduced their stored outputs byte for byte. The audit corrected about a dozen stale or mismatched values, the largest being the PCM average (29.1 to 29.0 K) and the channel velocity (draft value, 0.15 to 0.20 m/s). It found no verifier's fatal issue silently dropped.

Items no final script re-derives, carried openly in the architecture's change log:

- the 350 W/cm2 case temperatures (about 98 C for the drop-in core, 88 C for the filtration-gated grade), now stated as a margin of about 16 K over a model of the split-flow plate;
- the tray-cartridge service lives;
- the lean-budget option of about US$8.3 M.

## What the review did not do

- **No hardware.** Every PRISM number is a model prediction. The first experiments (braze coupons, water table, purchased incumbent plates) are in the programme's first three months for that reason.
- **No CFD.** The 1-D, network and 2-D conjugate models were cross-checked against each other, not against a full 3-D solution. Single-cell CFD is a gate item before the design freeze.
- **No reading of the OCP test specification text.** The document was published in October 2026 and could not be fetched from this environment. Its recommended interface material and case definition matter to the comparison, and reading it is a month-one task.
- **No legal opinion.** The IP analysis is engineering triage for counsel, not advice.
