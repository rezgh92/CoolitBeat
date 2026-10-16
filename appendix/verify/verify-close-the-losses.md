# Gap-closer: turning PRISM's concessions into wins

Key: `close-the-losses`. Lane: constructive. Date: 2026-10-14.

Scripts and outputs are in `appendix/verify/ctl/`. All thermal numbers use the draft's own 2-D cell model (`arch/cell2d.py`) for the **absolute** core, so each PRISM variant carries its own z-unmixed penalty. This is the verify-physics method, and it reproduces that report's corrected baseline exactly: 29.90 / 34.75 K on PCM and 31.83 / 38.67 K on paste at 117 cm2. All cost numbers use the verify-cost-market basis: September 2026 Cu and Ag, the same triangular inputs and the same yield/overhead.

The starting point is therefore the *corrected* PRISM, not the draft's claims:

- headline about 1.3-1.5 K worse than the draft states;
- cost **US$209 (197-222) against about US$126 (116-137)** for a like-sized incumbent, i.e. +66 %;
- 4 kW point **lost** at 0.0095 C/W;
- average at 100 cm2 **lost** by 3.6 %;
- mass 1.74 kg;
- 26.4 mm at the bar.

## 0. Bottom line

1. **Three concessions can be turned into wins with conventional moves that break nothing else:** height, mass and cost per kW. The moves are:
   - merge the meter into the grate;
   - replace the plenum laminations with one folded 0.8 mm Cu corrugation;
   - replace the forged bar with a drawn, arched Cu cap;
   - spend about 1.2 kPa of the dP margin on 5 mm-deep plenums, with **graded orifice artwork**;
   - lengthen the flow length to L 7.7 mm (15 lines instead of 19);
   - use a 0.8 mm base.

   The result, **PKG-A**, is still a drop-in R-grade plate:
   - **20.8 mm at the bar** (18.8 mm with a triple-arch header), against 26.4 mm corrected and 22-28 mm estimated for CoolIT;
   - **1.17 kg** (1.04 kg with a 0.6 mm 316L separator), against 1.74 kg and 1.2-1.6 kg estimated;
   - **US$162 (153-172)**, against US$209;
   - cost per kW at **parity** (+1 to +4 %).

   With an E1-gated silver-free Cu-Sn TLP joint in a belt furnace (route C, already in the draft's E1 plan), cost drops to **US$141 (132-150)**, **9-12 % better per kW** than the incumbent.
2. **Per-plate factory cost cannot be made a robust win.** PKG-A is +29 % (+16 to +42 %) against the like-sized incumbent; the C2 route is +12 % (+1 to +24 %), with P(cost ≤ incumbent) = 0.08. The residual US$10-35 is the price of the hierarchy: at least 4 brazed interfaces, a kerf operation, a finer skive and a per-plate flow screen, against a 2-part split-flow plate. This concession is irreducible per plate. It closes per kW of capacity, and per installed kW if the plate's 15 kPa dP saving releases CDU head.
3. **The 4 kW single-die point is not a tie, and it is not a like-for-like comparison at all.** The draft's own CoolIT reconstruction cannot reproduce CoolIT's < 0.009 C/W at 25 cm2 under any TIM or coolant:
   - 0.0130 with paste on PG25;
   - **0.0094 even with liquid metal and water**.

   At identical conditions on paste or PCM, the drop-in PRISM core is **0.80-0.83x** the reconstruction. A dedicated 50 x 50 mm SKU (**PRISM-S4**: R+ or P core, L 5-6, 0.8 mm base) beats < 0.009 in absolute terms:
   - with **LM** at 20-25 cm2: 0.0062-0.0079 C/W, 12-31 % better;
   - with **PCM** only on a 25 cm2 heater: 0.0082-0.0087, 3-9 % better.

   With paste at ≤ 25 cm2 it is **physically irreducible** for any fouling-safe laminar-fin plate: the best case is 0.0093-0.0110.
4. **The 100 cm2 like-for-like paste average is near-irreducible for the 0.15 mm R-grade.**
   - PKG-A reaches 34.25 K against 34.4 K (P = 0.50): parity, not a win.
   - The theoretical floor at the R-grade h_eff ceiling is about 32.3-33.1 K.
   - It becomes a win only with a filtration-gated **R+ core** (0.12 mm gap, ≤ 25-33 µm absolute tray filter): **31.9 K, -7 %, P = 0.75**, maximum P = 0.84.
   - **New flag:** the paste *maximum* at 100 cm2 is P = 0.57-0.61 for every drop-in variant. It is not a robust win either.
5. **Field record is irreducible at launch.** It is a time metric (Class D).
6. **10-year fouling.** At equal filtration, a 0.15 mm gap has shorter exclusion life than a 0.2 mm gap (about 7 against 15 years behind 50 µm absolute, from the project's own model). Closing that would need ≥ 0.2 mm gaps, which cost +4.7 K on the paste average (36.5 K: the average is lost). It is irreducible as a like-for-like plate claim. It can be converted into a measurable launch claim: a **10-year-equivalent particulate-dose qualification**, 100x dosing for 1,000 h. That is not a field claim.

## 1. Concession scorecard (corrected starting point, then moves)

| Concession (draft wording) | Corrected starting point | Best move set | Result | Verdict |
|---|---|---|---|---|
| Factory cost +45 % per plate (US$160 vs ~110); +8-10 % per kW | US$209 vs 126 like-sized (+66 %); +33-36 % per kW | PKG-A lean stack; option C2 silver-free belt braze | US$162 (+29 %); per kW +1 to +4 %. C2: US$141 (+12 %); per kW -9 to -12 % | **per kW: parity (PKG-A) → win (C2, E1-gated). Per plate: irreducible premium, +10-30 %** |
| Mass +0.1-0.5 kg | 1.74 kg (excl. TTV load frame) vs est. 1.2-1.6 | metered grate, folded plenum, arched cap, 0.8 base; optional 316L separator | 1.17 kg (1.04 kg) | **win, probable** (CoolIT's mass is unmeasured; weigh the E0 plates) |
| Height "at parity" (~25 mm) | 26.4 mm (2.5 mm top-wall error fixed) | 5 mm plenums bought with dP + graded meter; arched cap; merged grate | 20.8 mm (18.8 mm triple-arch) | **win, probable** against the 22-28 mm estimate |
| 4 kW point "ties" (0.0093 vs < 0.009, PCM) | 0.0095 PCM / 0.0108 paste: **loses** | PRISM-S4 SKU (R+ or P, L 5-6, 0.8 base); LM default | LM 0.0062-0.0079 (20-25 cm2); PCM 0.0082-0.0087 (25 cm2 only) | **LM win; PCM narrow win at 25 cm2; paste irreducible.** Not like-for-like until head-to-head |
| Average parity if CoolIT footprint is 100 cm2 (paste) | 35.64 K: **loses** 3.6 % (P 0.33) | PKG-A (L 7.7, base 0.8); PKG-B R+ | PKG-A 34.25 (P 0.50); PKG-B 31.91 (P 0.75) | **R-grade: parity, near-irreducible. R+ grade: win (filtration-gated)** |
| (new) Paste maximum at 100 cm2 | 43.15 K, P(max < 44.2) 0.57 | as above | PKG-A 42.73 (0.61); PKG-B 40.03 (0.84) | not a robust drop-in win; restate |
| No field record | — | dose-equivalent tests, pilot fleet, process-proven subset | — | **irreducible at launch** |
| No 10-year fouling claim | R 0.15 mm: ~7 y relative behind 50 µm abs vs 15 y for 0.2 mm | redesign E4 as 100x dose x 1,000 h | launch claim "10-year particulate-dose qualified" | **like-for-like life irreducible; a measurable surrogate is available** |

## 2. Detail by concession

### 2.1 Factory cost (`ctl/cost_mass_height.py`)

Same basis as `verify/cost_market_check.py`: 200k Monte Carlo draws, US$65/oz Ag, US$14.6k/t Cu, OFE premium, scrap credit, mature yield of 0.93, overhead of 0.12, US$ at 100k/yr per SKU, P50.

| Line | C0 draft (verifier basis) | C1 = PKG-A | C2 = PKG-A + route C belt braze | C3 = PKG-B (R+) |
|---|---:|---:|---:|---:|
| Copper (buy / finished kg) | 38.8 (2.91 / 1.60) | **22.1** (1.43 / 1.02) | 22.1 | 22.1 |
| Skive | 20.5 | 20.5 | 20.5 | 25.0 (+22 % strokes) |
| Kerf (19 → 15 lines) | 3.5 | 2.8 | 2.8 | 3.5 |
| Stampings (grate/meter/separator) | 6.3 | 6.8 (grate with gang-milled recess and pierced web) | 6.8 | 7.1 |
| Plenum | 7.5 (2 laminations; stamping route refuted) | **4.4** (folded 0.8 mm Cu + end frame) | 4.4 | 4.4 |
| Header | 14.5 (forged + CNC bar) | **5.3** (drawn arched cap + 2 bosses) | 5.3 | 5.3 |
| Filler | 18.5 (6 interfaces, ~410 cm2) | 14.7 (4 interfaces, ~280 cm2) | **4.3** (masked Sn plate, Cu-Sn TLP) | 14.7 |
| Braze (furnaces per 100k) | 21.9 (2.2) | 17.6 (1.6: +30 % per load, -10 % cycle) | **8.5** (continuous N2/H2 belt) | 17.6 |
| Dies, fly-cut, stubs + guard, hardware, test | 40.5 | 40.2 | 40.2 | 40.2 |
| **Factory cost P10 / P50 / P90** | **197 / 209 / 222** | **153 / 162 / 172** | **132 / 141 / 150** | **159 / 169 / 180** |
| Premium vs like-sized incumbent (116 / 126 / 137) | +50 / +66 / +83 % | +16 / +29 / +42 % | +1 / +12 / +24 % | +21 / +34 / +48 % |
| US$/kW, paste (CoolIT 9.77) | 13.25 (+36 %) | 10.20 (+4 %) | **8.86 (-9 %)** | 9.66 (-1 %) |
| US$/kW, PCM (CoolIT 8.52) | 11.31 (+33 %) | 8.63 (+1 %) | **7.49 (-12 %)** | - |

Capacities in the per-kW rows are own-penalty values from `ctl/lean_pkg.out` (paste / PCM): C0 15.8 / 18.5; C1 and C2 15.9 / 18.8; C3 17.5 / 21.0. The CoolIT values are the draft's 12.9 / 14.8 kW.

**What each move buys, and why it is safe:**

- **Metered grate (merge meter + grate).**
  - **Design:** one 1.7 mm OFE sheet. Inlet windows are gang-milled 1.3 mm deep from the fin side, leaving a 0.4 mm web. The 0.5 x 1.0 mm orifices are pierced through that web (d/t 1.25, punchable). Outlet windows are through-cut.
  - **What it removes:** one part, plus the ~110-130 cm2 grate/meter braze interface. That interface sits exactly at the orifice plane, so removing it eliminates the main wicking path to the meter. It also removes the unbonded-meter cantilever case flagged by verify-manufacturing (46 / 67 MPa).
  - **Stress:** the grate cantilever to the outlet-window edge is 28.6 MPa at the 3.1 MPa design burst (allowable 40 MPa). The extra 0.3 mm of thickness pays for the longer L 7.7 arm.
- **Folded plenum.**
  - **Design:** a 0.8 mm Cu square-wave corrugation, 5.0 mm channels at 7.7 mm line pitch. Folded Cu fins of 0.25-0.5 mm x 5-12 mm are a standard cold-plate product, so this is conventional.
  - **Wiring:** inlet channels have the grate as their floor, so the orifices open into a channel with no braze joint within about 3 mm. Outlet channels have the corrugation's bottom flat as their floor, with wide non-critical slots over the outlet windows.
  - **What it fixes:** it replaces the refuted 4.5 mm-lamination stamping route (web/t 0.33) and removes the lam/lam interface.
  - **Stress:** wall tension is 29.8 MPa at design burst.
- **Arched drawn cap instead of the forged bar.**
  - Each header half is two 12 mm-wide arches 8 mm tall, 1.0 mm Cu: hoop stress 18.6 MPa at 3.1 MPa. This also removes verify-manufacturing's top-wall error (36-49 MPa on a flat 2.5 mm wall).
  - The port pockets are drawn to r 12 mm at 1.5 mm wall (24.8 MPa), with brazed bosses.
  - Header velocity is 0.93 m/s. The slot-to-slot ratio is 3.9 kPa / 435 Pa = 9.0, above the ≥ 6 rule.
- **Copper buy halves** (2.9 → 1.4 kg). Most of the C0 buy was scrap: 4.5 mm lamination slugs and forging flash.
- **Furnace loading.** A 1.0 kg, 20.8 mm stack loads about 30 % more plates per fixture and cycles faster, so 2.2 → 1.6 vacuum furnaces per 100k/yr.
- **C2 (E1-gated).** Route C, a Cu-Sn TLP joint from about 3 µm of masked electroplated Sn, is already one of the draft's four E1 join routes. Running it in a continuous N2/H2 belt furnace removes about US$14 of silver and about US$9 of batch-vacuum cost.
  - **Risks:**
    - TLP homogenisation time;
    - brittle Cu3Sn if under-reacted, critical on fin-tip ties loaded in tension;
    - H2 is compatible with OFE but not with ETP copper.
  - **Synergy:** route C is also the draft's only answer to a mandated Ni-plated wetted path (R7).

**Equal-cost comparison.**

- **At equal cost per kW of case-limited capacity:** PKG-A is at parity, C2 wins by 9-12 %.
- **At equal per-plate price:** the incumbent's US$126 buys 12.9 kW (paste). C2's US$141 buys 15.9 kW (+23 %), 5.8 K more inlet headroom like-for-like and 15 kPa less dP.
- **System-level credit:** the research base values "-10 kPa per plate" at US$9-25 of CDU capex per plate, when the CDU is head-limited. PRISM saves about 15 kPa, which covers the C2 premium. This is contingent, so it is stated, not counted.

**Not enough to make per-plate cost a win:**

- dropping the kerfs: -US$3.4, but +0.4-0.7 K and the Split-Flow design-around is lost;
- dropping the guard: -US$2-3;
- sampling the IR screen instead of 100 %: -US$2.

Even all three together leave C2 at about US$132 (+5 %).

**GPU class (outside the 15 kW benchmark, flagged).** Applying the same moves to PRISM-G with verify-cost-market's scaling factors gives about US$148 (C1 route) or about US$129 (C2 route), against US$159-180 for the verifier's bottom-up PRISM-G and US$105-110 for GB-class incumbents. GPU-class per-plate cost stays a loss: +17 to +35 %.

### 2.2 Mass (`ctl/mass_height.py`)

The boundary matches the draft: plate plus 0.15 kg of stubs, guard, springs and backplate, without the 2 kN TTV load frame.

| Part | Draft (kg) | PKG-A (kg) |
|---|---:|---:|
| Base + fins | 0.270 | 0.251 (0.8 mm base) |
| Grate + meter | 0.160 | 0.211 (merged, 1.7 mm) |
| Plenum layer | 0.550 | 0.186 (folded 0.8 mm + end frame) |
| Separator | 0.210 | 0.191 (1.5 mm Cu); 0.068 as 0.6 mm 316L |
| Header | 0.410 | 0.176 (arched cap + bosses) |
| Stubs, guard, springs, backplate | 0.150 | 0.150 |
| **Total** | **1.75** | **1.17 (1.04 with 316L separator)** |

**316L separator (option).** 316L is already on the draft's wetted list.

- **Advantages:** it is about 5x stronger after the braze cycle (yield about 200 MPa against 40 MPa), and its CTE is within about 1 ppm/K of OFE. That is about 3e-5 strain over a 30 K swing, so no meaningful bimetal bow.
- **Costs:** it needs a 2-3 µm Ni strike to wet with Ag-Cu, which is one more process. It also sets up a mild Cu-anodic galvanic couple, already present in every 316L-manifold loop and covered by the 3,000 h coupon soak.

**Aluminium rejected for wetted parts.**

- An Al-Cu couple of about 0.5 V in PG25 deposits Cu on Al and pits it.
- There is no common braze cycle: Al melts at 660 C and the Cu-Al eutectic forms at 548 C. A gasketed joint would add a seal and a leak path.
- The OCP / ASHRAE mixed-metal limits would apply.

Al is fine for the non-wetted backplate or load frame.

### 2.3 Height (`ctl/plenum_height.py`, `ctl/plenum_graded.py`, `ctl/mass_height.py`)

| Stack (mm) | Base | Fins | Grate | Meter | Plenum | Separator | Header | Body | At the bar |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Draft | 1.0 | 2.0 | 1.0 | 0.4 | 9.0 | 1.5 | 10.5 | 14.9 | 25.4 (26.4 corrected) |
| PKG-A | 0.8 | 2.0 | 1.7 | - | 5.8 (5.0 channel + 0.8 sheet) | 1.5 | 9.0 (arched) | 11.8 | **20.8** |
| PKG-A, triple-arch header | | | | | | | 7.0 | 11.8 | **18.8** |

**The enabling hydraulic move.** The along-plenum profile is momentum-driven and therefore scales with u²; the meter is inertial and also scales with u². So **orifice areas graded along y cancel the profile at every flow**.

Five punch sizes spanning 1.16x in area give the following along-plenum max/min, from the draft's own plenum physics with per-branch R2:

| Layout | Ungraded | Graded |
|---|---:|---:|
| PKG-A (7 inlets, 6.9 x 5.0 mm, meter 2.3 kPa) | 1.14 | **1.061 at 18 LPM, 1.068 at 36 LPM** |
| Draft (9 inlets, 4.5 x 9.0 mm) | 1.083 | - |

The meter rises from 1.82 to 2.3 kPa (1.54 m/s at 18 LPM, 1.92 m/s at 150 % of rated flow, inside the 2.0 m/s cap). The graded artwork costs nothing: it is the same punch or laser file.

**Plate dP** (`ctl/pkgA_dp_stress.py`, the draft's element method):

| Flow | PKG-A | Draft | CoolIT reconstruction |
|---|---:|---:|---:|
| 18 LPM | **7.1 kPa** | 5.9 | ~22 |
| 36 LPM | 25.4 kPa (claim ≤ 27 holds) | 21.4 | - |

The dP win stays at about -68 %.

**Horizontal ports do not help height at 18 LPM.** A ≥ 16-20 mm bore needs a ≥ 20-24 mm boss. The draft's own dual-½-in horizontal variant is 32 mm at the bar. Vertical bosses on a 7-9 mm cap are the height winner. PRISM-G keeps its 10 mm horizontal ports at 2-4 LPM.

### 2.4 CoolIT's 4 kW point (`ctl/sku4kw.py`)

Conditions: 4 kW, 6 LPM, own 2-D penalty, max-case R in C/W. The CoolIT figure is < 0.009, with TIM, coolant and heater area all undisclosed.

| Build | 25 cm2, PG25: paste / PCM / LM | 20 cm2, PG25: paste / PCM / LM |
|---|---|---|
| Drop-in R (L 6, base 1.0) | 0.0108 / **0.0095** / 0.0077 | 0.0128 / 0.0113 / 0.0089 |
| R, L 5, base 0.8 | 0.0106 / 0.0094 / 0.0075 | 0.0126 / 0.0110 / 0.0087 |
| **R+ 0.12/0.12 x 1.8, L 5-6, base 0.8** | 0.0099 / **0.0087** / **0.0068** | 0.0117 / 0.0102 / **0.0078** |
| **P 0.10/0.10 x 1.5, L 5, base 0.8** | 0.0095 / **0.0082** / **0.0064** | 0.0112 / 0.0096 / **0.0073** |
| P, L 5, base 0.6 | 0.0093 / 0.0081 / 0.0062 | 0.0110 / 0.0095 / 0.0071 |
| P, L 4, base 1.0 (the lane's suggested L 4) | 0.0096 / 0.0084 / 0.0065 | 0.0114 / 0.0098 / 0.0075 |
| CoolIT reconstruction (0.2/0.2 x 4, 2 mm base) | 0.0130 / 0.0118 / 0.0099 | 0.0156 / 0.0141 / 0.0117 |
| CoolIT reconstruction, water | 0.0125 / 0.0113 / **0.0094** | 0.0150 / 0.0135 / 0.0111 |

Readings:

1. **The reconstruction cannot reach < 0.009 under any combination tried.** CoolIT's 4 kW test therefore ran under undisclosed conditions or with a different plate geometry, for example a TC in a Cu TTV block, a heater above 25 cm2, a solder TIM or finer fins. Heat capture of only 93-97 % also points to a TTV with large parasitic paths.
2. At identical conditions, on paste or PCM, PRISM is **0.80-0.83x (drop-in R), 0.73-0.76x (R+) and 0.69-0.73x (P)** of the reconstruction; with LM it is 0.62-0.77x. A *relative* claim is defensible; an absolute "tie" or "loss" is not.
3. L 4 is worse than L 5 at 160-200 W/cm2, which agrees with verify-physics. Use L 5-6, not L 4.
4. **Dedicated SKU, PRISM-S4:**
   - 50 x 50 mm;
   - P core (≤ 33 µm absolute loop) or R+ core (≤ 25-33 µm), L 5, 0.8 mm base;
   - Tier 2 LM as default; PCM option for dies ≥ 25 cm2.

   It wins in absolute terms with LM at 20-25 cm2 (-12 to -31 %), and with PCM only at 25 cm2 (-3 to -9 %).
5. **Irreducible part.** With paste at ≤ 25 cm2, even the 0.6 mm-base P core is 0.0093-0.0110. TIM (11-14 K) plus convection at the 0.10 mm-gap h_eff ceiling exceeds the 36 K budget. Only the interface tier (LM or D2D) wins.
6. **Decisive action.** Extend E0 to CoolIT's 4 kW-class plate, or its closest product, and test both on a 25 cm2 TTV in OCP format with the same TIM.

### 2.5 Average (and maximum) at a 100 cm2 footprint (`ctl/sweep_core.py`, `ctl/sweep2.py`, `ctl/lean_pkg.py`)

All rows are on paste, 15 kW, 18 LPM. P values are from the Monte Carlo (draft distributions, own penalty N(pen, 0.01 core)).

| Variant | 100 cm2 avg / max (P avg, P max) | 117 cm2 avg / max (P avg, P max) |
|---|---|---|
| Corrected baseline (R, L 6, base 1.0) | 35.64 / 43.15 (0.33, 0.57) | 31.83 / 38.67 (0.78, 0.93) |
| Base 0.8 | 34.85 / 42.61 | 31.14 / 38.23 |
| Base 0.6 | 34.04 / 42.13 | 30.44 / 37.84 |
| L 8 | 35.05 / 43.46 | 31.25 / 38.99 |
| H 1.5 / H 2.5 | 36.73 / 44.15 ; 35.61 / 43.21 | 32.74 / 39.52 ; 31.85 / 38.77 |
| 0.10 mm fins at 0.15 mm gap | 35.64 / 43.43 (no gain) | 31.83 / 38.94 |
| No kerf | 36.29 / 43.96 (kerf worth 0.64 K) | 32.47 / 39.43 |
| **PKG-A: L 7.7, base 0.8** | **34.25 / 42.73 (0.50, 0.61)** | **30.57 / 38.39 (0.88, 0.94)** |
| R base 0.6 + L 8 | 33.44 / 42.45 | 29.85 / 38.17 |
| R+ 0.13 / 0.13 x 1.9, base 0.8 | 32.84 / 40.84 | 29.40 / 36.73 |
| **PKG-B: R+ 0.12 / 0.12 x 1.8, L 6, base 0.8** | **31.91 / 40.03 (0.75, 0.84)** | **28.59 / 36.03 (0.96, 0.98)** |
| P 0.10 / 0.10 x 1.5, L 6, base 0.8 | 30.08 / 38.46 | 26.99 / 34.71 |
| 0.20 mm gap (fouling-parity core) | 40.99 / 48.24 | 36.49 / 43.08 (**loses** avg) |

**Why the R-grade is stuck near parity.** At 150 W/cm2 the paste term alone is 10.5 K and caloric 7.6 K. Even at the draft's stated ceiling for a 0.15 mm gap (h_eff ≈ 138 kW/m2K), convection is 10.9 K. With a 0.6-0.8 mm base and about 1 K of 2-D penalty, the floor is about 32.3-33.1 K, i.e. -4 to -6 % at the theoretical limit. Practically it is parity.

**What closes it:**

- a ≤ 0.13 mm gap. R+ needs a ≤ 25-33 µm absolute tray cartridge for about 6-10 years of exclusion life, against about 5 years behind 50 µm absolute (interpolated from `physics/fouling-filtration.md`);
- or a lower-R'' interface.

**Unverified upside.** A tied, flat face reduces the mean paste bond line. That is worth -0.2 to -0.5 K per µm at 128-150 W/cm2 (k_paste 3-6 W/mK), so 3 µm gives about -0.6 to -1.5 K. It must be *measured* on both plates (post-test BLT, already a draft rule), not modelled.

**The paste maximum at 100 cm2** is only P = 0.57-0.61 for every drop-in variant. Paste scatter (4.1 K) and the ripple crest (2-3 K) dominate it. PKG-B (0.84) or a scatter-reducing assembly process (stencilled paste on a ≤ 10 µm face) are the levers. The draft's "maximum wins hold at every footprint" must go, as verify-physics also found.

### 2.6 Field record and 10-year fouling

**Field record** cannot be beaten at launch, because it is a time metric. Three things narrow the gap:

- every process step is already fielded in incumbent plates (skive, stamp, vacuum braze, fly-cut);
- a 300-500-plate hyperscaler pilot from M12 gives about 150-500 plate-years by M18-24;
- serialised proof, He, dP and IR records on 100 % of plates.

**Fouling life, like-for-like.** On the project's own Wyss-based model, exclusion life at equal filtration scales steeply with W/d:

| Gap | Behind 50 µm absolute | Behind 33 µm absolute |
|---|---:|---:|
| 0.15 mm (R) | 7 y | 12 y |
| 0.20 mm (presumed CoolIT) | 15 y | - |
| 0.12 mm (R+) | about 5 y | about 6 y |

Parity would need ≥ 0.2 mm gaps, which lose the paste average at 117 cm2 (36.5 K). This is irreducible. One caveat: CoolIT's gap is undisclosed, and if it is 0.15 mm the comparison is parity.

**Convertible into a launch claim.** The successive-deposition mechanism is dose-driven, so concentration x time is a valid accelerant to first order. Redesign E4 as ISO 12103 + CuO + EPDM at 100x the assumed loop concentration for 1,000 h. That is about 11.4 years of particulate dose, measured with **fin-field dP taps** rather than port taps (port-to-port dP cannot see fin fouling; verify-hydraulics). Claim "10-year-equivalent particulate dose, ≤ 10 % core dP and ≤ 1 K drift" at launch. Chemistry and biofouling remain time-bound.

## 3. Best package and scorecard deltas

**PKG-A (drop-in R-grade; recommended as the new baseline):**

- fins, kerfs and filtration unchanged: R 0.15 / 0.15 x 2.0, 0.3 mm kerfs at every line, 50 µm guard;
- **L 7.7 mm** (7 inlet and 8 outlet lines);
- **0.8 mm base**, E1-gated;
- **1.7 mm metered grate** (meter merged);
- **folded 0.8 mm Cu plenum, 5 mm channels**, inlet channels floored by the grate;
- **graded orifice artwork** (5 sizes);
- 1.5 mm separator (0.6 mm 316L optional);
- **drawn 1.0 mm arched cap** with brazed 20 mm bosses;
- **6 parts in 5 layers, with 4 planar brazed interfaces**, against 7 parts and 6 interfaces.

C2 is the E1-gated route-C/belt-furnace cost option. PKG-B is the R+ core for filtered (≤ 25-33 µm) hyperscaler loops.

| Metric (15 kW, 18 LPM PG25, 45 C) | CoolIT | Draft claim | Corrected draft | **PKG-A** | PKG-B (R+) |
|---|---|---|---|---|---|
| Average / maximum, paste, 117 cm2 | 34.4 / 44.2 | 30.4 / 37.2 | 31.8 / 38.7 | **30.6 / 38.4 (-11 % / -13 %)** | 28.6 / 36.0 |
| Average / maximum, PCM 25 psi, 117 cm2 | (32.5 / 40.3 on PCM) | 28.4 / 33.3 | 29.9 / 34.8 | **28.7 / 34.5** | 26.7 / 32.1 |
| Average / maximum, LM, 117 cm2 | - | 23.3 / 27.3 | 24.8 / 28.7 | 23.5 / 28.4 | 21.5 / 26.1 |
| Average / maximum, paste, 100 cm2 | 34.4 / 44.2 | 34.0 / 41.7 | 35.6 / 43.2 | **34.3 / 42.7 (parity)** | **31.9 / 40.0** |
| P(avg < 34.4), paste: 117 / 100 cm2 | - | 0.88 / - | 0.78 / 0.33 | 0.88 / 0.50 | 0.96 / 0.75 |
| P(max < 44.2), paste: 117 / 100 cm2 | - | 0.97 / - | 0.93 / 0.57 | 0.94 / 0.61 | 0.98 / 0.84 |
| Q capacity, paste / PCM (85 C case, 1.2 LPM/kW) | 12.9 / 14.8 | 16.6 / 19.4 | 15.8 / 18.5 | 15.9 / 18.8 | 17.5 / 21.0 |
| Inlet allowed, paste / PCM (CoolIT 40.8 / 44.7 on PCM) | 40.8 | 47.8 / 51.7 | 46.3 / 50.3 | 46.6 / 50.5 (+5.8 K like-for-like) | 49.0 / 52.3 |
| Plate dP, 18 LPM, 20 mm ports | ~22 | 5.9 | 5.5-5.9 | **7.1** | ~7.0 |
| Along-plenum max/min | - | 1.065-1.085 | 1.04-1.08 (line) | **1.061 / 1.068 (18 / 36 LPM)** | similar |
| Height at the bar | est. 22-28 | 25.4 | 26.4 | **20.8 (18.8)** | 20.8 |
| Mass | est. 1.2-1.6 | 1.6-1.75 | 1.74 + frame | **1.17 (1.04)** | 1.17 |
| Factory cost, 100k/yr | 126 (116-137) like-sized | 160 | 209 | **162**; C2 **141** | 169 |
| US$/kW, paste / PCM | 9.8 / 8.5 | 9.6 / 8.2 | 13.3 / 11.3 | 10.2 / 8.6 (parity); C2 8.9 / 7.5 (win) | 9.7 / - |
| 4 kW, 25 cm2 | < 0.009 | 0.0093 "tie" | 0.0095 (loss) | PRISM-S4: LM 0.0064-0.0068; PCM 0.0082-0.0087 | - |
| Parts / planar brazed interfaces | ~2 / 1 seam | 7 / 6 | 7 / 6 | **6 / 4** (corrugation + end frame share one layer) | 6 / 4 |

## 4. What the package costs elsewhere (checked)

**dP:** +1.2 kPa (7.1 against 5.9). The dP win is still about -68 %. The 36 LPM value is 25.4 kPa, under the ≤ 27 claim. Meter velocity at 150 % of rated flow is 1.92 m/s (cap 2.0). The Q-capacity flow of 22.6 LPM stays inside the velocity rules.

**Maximum and capacity:** essentially unchanged. The longer cell raises the ripple crest by about 1 K, and the 0.8 mm base and L 7.7 give that back. If the maximum is prioritised over the average, use L 6 with base 0.8: 31.1 / 38.2 K.

**Defect tolerance: the one real cost.**

- A single unbonded land strip at 0.8 mm base and a 7.4 mm kerf-to-kerf span reaches 67-99 MPa at the 1.55 MPa proof, and collapses at 1.6-2.3 MPa. That is below the 3.1 MPa design burst.
- Its proof bulge, however, rises to about 2.2 µm (from 0.58 µm), which becomes detectable by the draft's pressurised flatness scan (about 1 µm resolution).
- **Gate:** base 0.8 is gated on E1 proving per-strip detection, plus the verify-manufacturing per-strip controls. The fallback is base 1.0 at +0.7 K (PKG-A at 1.0 mm: 31.3 / 38.8 K paste).

**Segment-level balance** (verify-hydraulics: 1.23-1.43). L 7.7 raises the viscous fin resistance from 0.65 to 1.07 kPa, so the left/right protection ratio rises 1.6x. The remaining fix is the verifier's split meter or outlet-side orifice row.

**IP:** the kerf-at-every-line Split-Flow design-around is unchanged.

**Fouling:** the R-grade is unchanged. PKG-B is a separate, filtration-gated grade.

**High-flux zones:** keep L 5-6 in zones at ≥ 250 W/cm2 (die SKUs). L 7.7 applies at 100-250 W/cm2.

## 5. Ideas evaluated and not adopted

| Idea | Result |
|---|---|
| Al header or plenums | rejected: galvanic couple, no common braze, gasket leak path |
| 316L separator or cap | optional: -0.12 kg, about -US$1, plus a Ni-strike process |
| 0.15 mm fins at 0.20 mm gap in low-flux zones | PRISM-G only. Skive pitch is programmable along x, so it saves about 10-20 % of skive strokes (US$2-4). On the uniform 15 kW TTV it costs +4.7 K wherever applied. |
| P-grade inserts only under dies | PRISM-G / die SKUs (bands in x); not applicable to the uniform TTV |
| Eliminate the guard screen | -US$2-3, -0.3 kPa. Only for SKUs sold with a mandatory ≤ 50 µm absolute tray cartridge. Keep the guard on the drop-in R-grade, since fouling is the open concession. |
| Drop the kerfs | -US$3.4, +0.4-0.7 K, and weakens the IP design-around: no |
| Thinner (0.10 mm) fins at 0.15 mm gap; taller (2.5 mm) fins | no gain (0.0 / +0.3 K and 0.0 K): confirms the draft |
| L 4 for the 4 kW SKU | worse than L 5 |
| Horizontal single port pair for height | no gain at 18 LPM |

## 6. Required changes to the draft (from this lane)

1. **Replace the 6.7 concession table:**
   - **height and mass become wins** (PKG-A), confirmed by weighing and measuring the E0 incumbent plates;
   - **cost per kW becomes parity (PKG-A) or a win (C2)**;
   - **per-plate cost** is restated as an irreducible +10-30 % premium on the verifier basis (not +45 % against a GB-class plate);
   - **the 4 kW point is "not comparable; PRISM-S4 wins with LM, and with P/R+ on PCM at 25 cm2"**;
   - **100 cm2 is "parity (R) / win (R+)"**, and the paste maximum at 100 cm2 is not robust;
   - **fouling and field record are irreducible**, with the dose-equivalent E4 surrogate.
2. **Adopt PKG-A as Rev A:**
   - metered grate;
   - folded plenum with inlet channels floored by the grate;
   - arched cap;
   - 5 mm plenums with graded meter artwork;
   - L 7.7 with 15 lines, which fixes verify-hydraulics' 18-line edge-layout error by construction: 7 inlet and 8 outlet lines with edge outlets;
   - 0.8 mm base gated in E1.
3. **Add to E1:**
   - a route-C belt-furnace cell (C2);
   - per-strip unbonded-land detection at 0.8 mm base;
   - folded-corrugation pitch and alignment tolerance against the grate windows.
4. **Add the PRISM-S4 SKU** to 2.3 and 6.4, and extend E0 to a CoolIT 4 kW-class plate on a 25 cm2 TTV.
5. **Re-cost** with `ctl/cost_mass_height.py`: US$162 (PKG-A) / US$141 (C2) against US$126 like-sized. Re-cost PRISM-G with the same moves (about US$129-148); GPU-class per-plate cost remains a loss.

## 7. Files

All under `appendix/verify/ctl/`:

| File | Content |
|---|---|
| `harness.py` | scoping model plus cell2d absolute core; reproduces verify-physics |
| `sweep_core.py` / `.out`, `sweep2.py` / `.out` | fin, base, L, gap and kerf moves at 100 and 117 cm2 |
| `lean_pkg.py` / `.out` | package scorecard, capacity, Monte Carlo |
| `sku4kw.py` / `.out` | 4 kW SKU and reconstruction inconsistency |
| `plenum_height.py` / `.out`, `plenum_graded.py` / `.out`, `plenum_graded_pkgA.out` | plenum depth against uniformity; graded meter |
| `pkgA_dp_stress.py` / `.out` | dP and changed load paths |
| `cost_mass_height.py` / `.out`, `mass_height.py` / `.out` | cost (verifier basis), mass, height |
