# PRISM-15 Rev A: one-page briefing

16 October 2026. All performance figures are model predictions until the first plates are tested.

## What was asked and what exists now

The brief was to take CoolIT's published 15 kW cold plate as the benchmark and design a conventionally manufacturable plate that beats it, for AI data centres first. The result is PRISM-15 Rev A, a complete design package.

1. **Benchmark reconstruction.** CoolIT's brief gives three measured numbers at one test condition. The heated area, pressure drop and fin geometry it leaves out were rebuilt with a calibrated physics model, so every comparison is like-for-like.
2. **Architecture.** Competing proposals were scored by independent judges; the winner was attacked by adversarial reviewers on physics, hydraulics, manufacturing, cost and patents. The survivor became the architecture of record.
3. **Detailed design.** Eight design lanes (core, grate, plenum, cap, mounting, manufacturing, predicted datasheet, innovation register) turned it into dimensions, tolerances, materials, a bill of materials, a factory routing and a cost roll-up.
4. **Parametric CAD.** Fourteen real solids from one parameter file, checked for interference, exported as STEP, STL and DXF with drawings and renders.
5. **Communication.** A 37-page design report, a 23-slide review deck and a narrated 3D explainer video.

## How the plate works, in plain words

A cold plate is a copper block with thousands of tiny fins inside; coolant flows between the fins and carries the chip's heat away. CoolIT pushes the coolant in from one side and across the whole 54 mm fin field. PRISM feeds the fins from above through fifteen metered lines, so each drop of coolant travels only 7.7 mm along the fins before it leaves. Think of watering a lawn with one hose from the edge versus a sprinkler grid overhead.

That one change allows three things:

- **Finer fins.** With a short path the pressure penalty of thin fins disappears, so the fins are 0.15 mm thick at 0.15 mm gaps: far more heat-transfer area per square centimetre.
- **Even flow.** A thin metering plate with 756 graded holes gives every line the same flow at any flow rate, within 2 percent, so there are no hot stripes.
- **A thin base.** The fin tips are brazed to the plate above them, so the pressure is carried by thousands of small ties instead of a thick floor. The base under the chip is 0.85 mm instead of about 2 mm, which shortens the heat path and keeps the face flat under pressure.

Everything is ordinary copper sheet, stampings, one skived block and one vacuum braze cycle. Nothing is printed, and only one seam faces the outside.

## Why it beats CoolIT, and how to say it

At CoolIT's own test condition (15 kW over four heaters, 18 L/min of water-glycol at 45 °C) the chip runs about 3 K cooler on average and 5 K cooler at the hot spot, with one third of the pump pressure.

| What matters to a data centre | CoolIT, measured | PRISM, predicted |
|---|---|---|
| Average chip-to-coolant temperature rise (K) | 34.4 | 31.1 (29.2 on a phase-change pad) |
| Hottest point (K) | 44.2 | 38.8 (34.9 on a pad) |
| Pressure the pump must supply across the plate (kPa) | about 22, not published, reconstructed | 7.6 |
| Power the plate can take at an 85 °C chip (kW) | about 13 | 15.7 (18.4 on a pad) |
| Height (mm) | about 22 to 28 | 20.8 |
| Factory price per plate at 100k per year (US$) | about 126 | 165 |

**The 60-second version.** "CoolIT's plate runs the coolant across the fins from one edge, 54 mm, so the far side gets warm coolant and the fins must be coarse to keep the pump pressure down. Ours feeds the fins from above through fifteen metered lines, so each drop travels 7.7 mm. That lets us use fins half as thick, keep every line at the same flow, and braze the fins to the plate above so the base is under a millimetre. At CoolIT's own test point the chip runs about 3 K cooler on average and 5 K cooler at the hot spot, with one third of the pump pressure, and the plate carries 20 percent more power before the chip hits its limit. It is all conventional copper work and one braze cycle. It costs about a third more per plate, but the same per kilowatt of cooling. These are model predictions; the first three months and 2.3 million dollars buy the braze test that proves or kills it."

## What it does not win

Say these before anyone else does; the public claim is scoped to exclude them.

- Price per plate is about 31 percent higher at volume. Per kilowatt of cooling capacity it is at parity, and a silver-free braze route decided at month 3 brings it to about US$142.
- The fins are fine, so the plate ships with a 33 µm tray filter and a fouling claim backed by a dose test, not by field hours.
- No field record yet. First hardware is month 3; the 22-plate endurance run is months 5 to 11.
- At very low flow (below 0.5 L/min per kW), on a very small chip (100 cm²) and at CoolIT's 4 kW single-die point, the average temperature is only equal or worse. The hot spot still wins everywhere.
- CoolIT holds patents on side-fed plates in the United States until September 2028. A freedom-to-operate opinion is due at month 4; until it clears, no US sales or evaluation units, and the first builds and sales are outside the US.

## What the money buys

The programme is US$8.4 to 10.7 M over twelve months, released in tranches. The first US$2.3 M, to gate G1 at month 3, answers the one question that decides the plate: can the fin tips be brazed to the grate reliably, and can a single missed strip be caught on the production line. If yes, the rest is execution. If no, the fallback is a 1.0 mm base that still beats the benchmark by more than 2.5 K on the average.

| Month | Gate | What must be true |
|---|---|---|
| 3 | G1, design freeze | Braze coupons pass; missed strip detectable; join route and base thickness chosen |
| 6 | G2 | Five plates, three re-mounts: pad average at or below 31 K, hot spot at or below 36 K; one customer letter of intent |
| 9 | G3 | Independent laboratory repeats within 1.5 K |
| 12 | G4 | Public result in the industry's standard (OCP) test format |
| 18 | G5 | 300 to 500 plate pilot at the contract manufacturer; qualified product; volume 2029 |

Decisions requested now: approve the scoped public claim rather than "beats on every metric"; fund the first tranche; adopt the vacuum-braze build with the silver-free route decided at G1; make the tray filter a supplied part; hold US sales until the legal opinion clears. Probability of a decisive result at month 12 is about 0.43; the dominant failure mode is a one-to-three-month slip at the braze test, not a thermal miss.

## Where everything is

| Item | Where |
|---|---|
| Design report, 37 pages | `report/PRISM-15-RevA-design-report.pdf` |
| Review deck, 23 slides | `presentation/PRISM-15-RevA-review-deck.pptx` |
| CAD package | `cad/` (STEP, STL, DXF, drawings, renders), `design/params.json`, `design/bom.csv` |
| Architecture of record and its stress test | `03-architecture.md`, `04-verification.md` |
| Design definition and the eight lane documents | `05-detailed-design.md`, `design/DDD-*.md` |
| Calibrated physics model | `model/coldplate_model.py` |
| Narrated 3D explainer video | `video/PRISM-15-RevA-explainer.mp4` |

The CAD, the report figures and the video are all generated from one parameter file, so a change decided at gate G1 regenerates the whole package.
