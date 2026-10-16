# DDD-perf: PRISM-15 Rev A predicted datasheet (OCP Cold Plate Test Specification format)

Detailed design definition, lane `perf`, 2026-10-16. Parent: `docs/cooling/03-architecture.md` (0.2 scorecard, 3.4 term budget, 4.1-4.3 hydraulics, 5.2 pressure ratings, 6.1-6.2, 6.6). Binding sibling lanes: `DDD-core.md` (base 0.85 nominal, 0.80-0.90, fallback 1.0; fins 0.15 / 0.15 x 2.0 at 0.30 pitch; segment 7.414 between kerfs, cell 7.714), `DDD-grate.md` (meter 2.31 kPa at 1.54 m/s, outlet row 0.50 kPa, segment max/min 1.092 at 18 LPM), `DDD-plenum.md` (channels 6.9 x 5.0, ≤ 0.62 m/s; separator windows 0.46 kPa), `DDD-mech.md` (bow, clamp), `DDD-mfg.md`. Script: `perf_datasheet.py` → `perf_datasheet.out`, `params-perf.json`. Method is the architecture's own (`appendix/verify/final/final_thermal.py`, `final_segbal.py`, `final_coolants.py` through `appendix/verify/ctl/harness.py`: absolute 2-D cell model `cell2d.py` for caloric + convection + base with PRISM's own z-unmixed penalty, 1-D TIM, maximum = average + 1.5 K flow maldistribution + TIM scatter scaled by flux + half the computed case ripple). Every number below is a **prediction** (model terms ±25 % until E2/E3); the test campaign in section 9 replaces them in the order given. All CoolIT-like values are a reconstruction and are labelled model-only; CoolIT's one measured point is 34.4 / 44.2 K at 15 kW, 18 LPM, paste.

## 0. Requirements carried into this lane

| ID | Requirement | Value | Source |
|---|---|---|---|
| F1 | Benchmark point reproduced at the as-designed values | 15 kW, 18 LPM PG25 (k 0.49), 45 C, 117 cm2 TTV-A | architecture 1.1, 6.1 |
| F2 | OCP format: R at ≥ 6 flows, 25-150 % of the rated flow, recommended TIM and paste; R'' per area; both average and 8-TC maximum bases | rated flow declared 1.0 LPM/kW = 15 LPM; flows 3.75 / 7.5 / 11.25 / 15 / 18 / 22.5 LPM | OCP spec v1.0.0 (§5.2 not yet read, R5); architecture 10.2 |
| F3 | dP at the same flows, 45 ± 2 C, three boundaries | port-to-port (20 mm bore stated), + stubs and barbs, + named UQD08 pair with measured Cv | architecture 1.3, 10.2 |
| F4 | External claims to hold | ≤ 10 kPa at 18 LPM; ≤ 30 kPa at 36 LPM; 85 C case limit; 65 C return cap | architecture 4.2, 7.3 |
| F5 | Coolant and inlet curves | PG25 primary; water secondary; 35 / 45 / 50 C inlet | architecture 6.6, 7.3 |
| F6 | Ratings capped by velocity rules, not by thermal capacity | meter ≤ 2.0 m/s mean at 150 % rated; port ≤ 1.5 m/s | architecture 4.1 |

## 1. Benchmark re-run: architecture (base 0.80) against as-designed (base 0.85)

`perf_datasheet.py` §1 re-runs `final_thermal.py` §1 unchanged at base 0.80 (reproduces 30.97 / 38.72, 29.05 / 34.80, 23.92 / 28.77 K exactly) and then at the DDD-core base. The base term scales with thickness (2.63 → 2.79 K); the 2-D penalty falls slightly (0.90 → 0.87) because the thicker base spreads the kerf-to-kerf ripple (pk-pk 5.49 → 5.39 K), so the maximum moves less than the average.

| Base (mm) | TIM | Caloric | TIM | Base | Conv | 2-D pen | Ripple pk-pk | **Avg K** | **Max K** | R'' avg (cm2K/W) | Shift vs architecture |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.80 (architecture) | paste | 7.52 | 8.97 | 2.63 | 10.94 | +0.90 | 5.49 | 30.97 | 38.72 | 0.242 | - |
| 0.80 | PCM | 7.52 | 7.05 | 2.63 | 10.94 | +0.90 | 5.49 | 29.05 | 34.80 | 0.227 | - |
| 0.80 | LM | 7.52 | 1.92 | 2.63 | 10.94 | +0.90 | 5.49 | 23.92 | 28.77 | 0.187 | - |
| **0.85 (as designed)** | paste | 7.52 | 8.97 | 2.79 | 10.94 | +0.87 | 5.39 | **31.11** | **38.81** | 0.243 | +0.14 / +0.09 K |
| **0.85** | PCM | 7.52 | 7.05 | 2.79 | 10.94 | +0.87 | 5.39 | **29.19** | **34.88** | 0.228 | +0.14 / +0.08 K |
| **0.85** | LM | 7.52 | 1.92 | 2.79 | 10.94 | +0.87 | 5.39 | **24.06** | **28.85** | 0.188 | +0.14 / +0.08 K |
| 0.90 (DDD-core max) | paste / PCM | - | - | 2.96 | - | +0.85 | 5.29 | 31.25 / 29.32 | 38.90 / 34.97 | 0.244 / 0.229 | +0.28 / +0.18 K |
| 1.00 (fallback) | paste / PCM | - | - | 3.29 | - | +0.93 | 5.00 | 31.66 / 29.74 | 39.17 / 35.24 | 0.247 / 0.232 | +0.69 / +0.45 K |

Channel state (unchanged by the base): u 0.198 m/s, Re 44, h 12.6 kW/m2K, h_eff 117 kW/m2K, NTU 1.16, fin dP 1.07 kPa, coolant rise 12.66 K. **Verdict:** the architecture's 31.0 / 38.7 K (paste) and 29.0 / 34.8 K (PCM) become 31.1 / 38.8 and 29.2 / 34.9 K; the shift (+0.14 / +0.09 K) is a tenth of the P10-P90 band (±3.5 K paste, ±2.9 K PCM at 117 cm2) and does not move any scorecard verdict (average -9.6 % / maximum -12.2 % against CoolIT on paste; -15.2 % / -21.1 % on PCM). The base tolerance 0.80-0.90 is worth ±0.14 K on the average. Deviation D-P1.

## 2. Segment balance and hot-spot allowance; case-temperature headroom

DDD-grate replaced the architecture's per-segment convention (max/min 1.061) with the lumped-row result 1.092 at 18 LPM, 1.122 at 27 and 1.057 at 9 LPM. The maximum carries a fixed 1.5 K flow-maldistribution term. `perf_datasheet.py` §2 evaluates the weakest segment (flow 1/sqrt(max/min) of the mean, assumed symmetric about the mean; same flux) with the same cell model:

| Flow | Segment max/min (DDD-grate 6.3) | Weakest segment flow | Core penalty of the weakest segment (caloric + convection) | Allowance | Margin |
|---|---|---|---|---|---|
| 9 LPM | 1.057 | 0.973 x mean | +0.59 K | 1.5 K | 0.91 K |
| 18 LPM | 1.092 | 0.957 x mean | +0.41 K | 1.5 K | 1.09 K |
| 27 LPM | 1.122 | 0.944 x mean | +0.35 K | 1.5 K | 1.15 K |

The 1.5 K allowance stands (it also covers the line-level 1.035 and the along-plenum ±2.2 %); no change to the published maximum (D-P2). Inlet temperature allowed at 15 kW, 18 LPM for Tcase,max ≤ 85 C and return ≤ 65 C: **46.2 C paste, 50.1 C PCM, 52.3 C LM** (return-limited; architecture 46.3 / 50.2 / 52.3).

## 3. Capacity (Tcase,max ≤ 85 C, 45 C inlet, 1.2 LPM/kW, 117 cm2)

| TIM | Thermal capacity (kW) | Architecture | Velocity-rated capacity (kW) | Governing |
|---|---|---|---|---|
| paste | 15.7 | 15.7 | 15.7 | thermal (meter 1.61 m/s at 18.8 LPM) |
| PCM | 18.4 | 18.5 | 18.4 | thermal, 0.1 kW below the velocity cap |
| LM | 25.4 | 25.5 | **19.5** | meter 2.0 m/s at 23.4 LPM; 25.4 kW needs the -HF artwork and dual UQD08 |

Bisection to ±0.1 kW (14 steps). CoolIT measured-basis capacity (flux-scaled terms) remains ~12.9 kW paste / ~14.8 kW PCM, so the +22-25 % capacity claim holds at +22 % (paste) and +24 % (PCM).

## 4. OCP-style thermal resistance table (15 kW, 45 C inlet, PG25 k 0.49, 117 cm2)

R = dT / Q (mK/W at 15 kW); R'' = dT x A / Q (cm2K/W, area-normalised, the number to compare across plates). Average basis = mean of the 8-TC case temperature minus inlet; max basis = hottest TC minus inlet. At 25-75 % of rated the outlet exceeds 65 C at 15 kW, so those points are tested at reduced power (≤ 4.9 / 9.9 / 14.8 kW); R is power-independent to first order.

| LPM | LPM/kW | % rated | Tout at 15 kW (C) | **PCM avg / max K** | PCM R mK/W avg / max | **PCM R'' cm2K/W avg / max** | paste avg / max K | paste R mK/W avg / max | paste R'' avg / max | LM avg / max K | CoolIT-like paste avg / max (model-only) | CoolIT-like PCM avg / max (model-only) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3.75 | 0.25 | 25 | 105.8 (!) | 66.9 / 79.0 | 4.46 / 5.27 | 0.522 / 0.616 | 68.8 / 83.0 | 4.59 / 5.53 | 0.537 / 0.647 | 61.7 / 73.0 | 58.8 / 92.6 | 56.9 / 88.8 |
| 7.50 | 0.50 | 50 | 75.4 (!) | 41.9 / 50.5 | 2.79 / 3.37 | 0.327 / 0.394 | 43.8 / 54.4 | 2.92 / 3.63 | 0.342 / 0.425 | 36.8 / 44.5 | 43.5 / 62.1 | 41.6 / 58.3 |
| 11.25 | 0.75 | 75 | 65.3 (!) | 34.5 / 41.5 | 2.30 / 2.77 | 0.269 / 0.324 | 36.4 / 45.4 | 2.43 / 3.03 | 0.284 / 0.354 | 29.4 / 35.5 | 38.4 / 51.9 | 36.5 / 48.1 |
| **15.00** | **1.00** | **100 (rated)** | 60.2 | **30.9 / 37.1** | 2.06 / 2.47 | **0.241 / 0.289** | 32.9 / 41.0 | 2.19 / 2.73 | 0.256 / 0.320 | 25.8 / 31.1 | 35.7 / 46.8 | 33.8 / 42.9 |
| **18.00** | **1.20** | **120 (benchmark)** | 57.7 | **29.2 / 34.9** | 1.95 / 2.33 | **0.228 / 0.272** | 31.1 / 38.8 | 2.07 / 2.59 | 0.243 / 0.303 | 24.1 / 28.9 | 34.4 / 44.2 (measured) | 32.5 / 40.3 |
| 22.50 | 1.50 | 150 | 55.1 | 27.4 / 32.7 | 1.83 / 2.18 | 0.214 / 0.255 | 29.4 / 36.6 | 1.96 / 2.44 | 0.229 / 0.285 | 22.3 / 26.6 | 33.0 / 41.5 | 31.1 / 37.7 |

Reading: the maximum is lower than the reconstruction at every flow; the average is lower from 0.75 LPM/kW up, at parity at 0.5 and lost by 17 % at 0.25 (isothermal-cell caloric penalty of any short-cell manifold, architecture 6.2 concession). Core R'' (convection + base + penalty) 0.114 cm2K/W; with caloric 0.171; the TIM is 0.055-0.070 of the total.

## 5. Pressure drop (PG25, 45 C; kPa)

Element budget at 18 LPM (DDD-grate as-designed meter and row in the architecture 4.2 frame): ports 1.60 (K 3.5 on the 20 mm bore), guard 0.30 (booked; 0.1-0.2 expected clean), headers 0.99, separator windows 0.46, plenums 0.19 + 0.02, meter **2.31**, windows/kerf/misc 0.08 + 0.08, outlet row **0.50**, fin channels 1.07 (viscous, from the cell model) = **7.60 kPa**, 81 % inertial. Inertial terms scale with (Q/18)^2 x rho/1005; viscous with Q/18 x mu/1.25 mPa·s. Barbs: two 316L stubs + 1/2-in barbs, 3.0 kPa at 18 LPM (`final_system.py` basis). UQD08 pair: two couplings in series, dP = SG (gpm/Cv)^2 psi each, vendor Cv 4.75 (CPC) and 3.65 (FITOK); it reproduces the architecture's 14-24 kPa pair band (13.8 / 23.4).

| LPM | % rated | **Plate port-to-port, 20 mm bore** | inertial / viscous | + stubs & barbs | + UQD08 pair, Cv 4.75 | + UQD08 pair, Cv 3.65 | Water port-to-port | CoolIT-like port-to-port (model-only) |
|---|---|---|---|---|---|---|---|---|
| 3.75 | 25 | **0.57** | 0.27 / 0.31 | 0.7 | 1.3 | 1.7 | 0.40 | 3.5 |
| 7.50 | 50 | **1.68** | 1.06 / 0.61 | 2.2 | 4.6 | 6.3 | 1.31 | 7.8 |
| 11.25 | 75 | **3.31** | 2.39 / 0.92 | 4.5 | 9.9 | 13.7 | 2.76 | 13.0 |
| 15.00 | 100 | **5.48** | 4.26 / 1.22 | 7.6 | 17.2 | 23.9 | 4.72 | 19.1 |
| 18.00 | 120 | **7.60** | 6.13 / 1.47 | 10.6 | 24.5 | 34.2 | 6.67 | 24.6 |
| 22.50 | 150 | **11.41** | 9.58 / 1.83 | 16.1 | 37.8 | 52.9 | 10.22 | 33.9 |
| 36.00 | 240 (characterisation) | **27.46** | 24.52 / 2.94 | 39.5 | 95.1 | 133.7 | 25.39 | 69.3 |

Claims held: 7.6 ≤ 10 kPa at 18 LPM; 27.5 ≤ 30 kPa at 36 LPM. Uncertainty: meter Cd ±10 % = +0.54 / -0.40 kPa at 18 LPM; guard 0.1-0.3; ports K 3.5 ±20 % = ±0.3; total band 6.9-8.4 kPa before test. The 25 % point (0.57 kPa) needs the 0-2 kPa transducer. Start-up at 17-25 C: 8.7-9.4 kPa (`final_system.out`).

## 6. Inlet temperature and coolant (15 kW; Tcase = Tinlet + dT)

PG25 properties at film ≈ inlet + 5 K (µ 1.60 / 1.25 / 1.12 mPa·s, k 0.48 / 0.49 / 0.495 W/mK at 35 / 45 / 50 C; ±10 %); water at 50 C film (µ 0.547, k 0.644). The case-to-inlet dT is nearly inlet-independent (< 0.3 K between 35 and 50 C: higher viscosity at 35 C lowers Re but the laminar h hardly moves); the inlet sets Tcase one-for-one.

| Case | LPM | PCM avg / max K | **Tcase PCM avg / max (C)** | paste avg / max K | Tcase paste avg / max (C) | Tout (C) | Plate dP (kPa) | Fin dP (kPa) |
|---|---|---|---|---|---|---|---|---|
| PG25, 35 C | 18.0 | 29.3 / 35.0 | 64.3 / 70.0 | 31.2 / 38.9 | 66.2 / 73.9 | 47.6 | 8.05 | 1.37 |
| PG25, 45 C | 15.0 | 30.9 / 37.1 | 75.9 / 82.1 | 32.9 / 41.0 | 77.9 / **86.0** | 60.2 | 5.48 | 0.89 |
| PG25, 45 C | 18.0 | 29.2 / 34.9 | 74.2 / 79.9 | 31.1 / 38.8 | 76.1 / 83.8 | 57.7 | 7.60 | 1.07 |
| PG25, 45 C | 22.5 | 27.4 / 32.7 | 72.4 / 77.7 | 29.4 / 36.6 | 74.4 / 81.6 | 55.1 | 11.41 | 1.33 |
| PG25, 50 C | 15.0 | 30.9 / 37.0 | 80.9 / **87.0** | 32.8 / 41.0 | 82.8 / **91.0** | **65.2** | 5.34 | 0.80 |
| PG25, 50 C | 18.0 | 29.1 / 34.8 | 79.1 / 84.8 | 31.0 / 38.8 | 81.0 / **88.8** | 62.7 | 7.43 | 0.96 |
| water, 45 C | 18.0 | 27.1 / 33.0 | 72.1 / 78.0 | 29.1 / 36.9 | 74.1 / 81.9 | 57.1 | 6.67 | 0.47 |

Bold = above the 85 C case limit or the 65 C return cap: at 50 C inlet the plate holds 15 kW only on PCM at ≥ 18 LPM (and LM); paste at 45 C needs ≥ 18 LPM. Water is worth -2.1 K average, -1.9 K maximum and -12 % dP against PG25 (architecture 6.6 gave -2.1 / -1.9 at base 0.80). PG30 / EG25: +0.5 / +0.1 K on the average (`final_coolants.out`, unchanged by the base within 0.01 K).

## 7. Predicted datasheet, one block (the numbers for the sales sheet, all P50 model predictions)

| Item | PCM pad (recommended) | Paste 0.07 | Liquid metal (Tier 2) |
|---|---|---|---|
| R'' average / max, 18 LPM (cm2K/W) | 0.228 / 0.272 | 0.243 / 0.303 | 0.188 / 0.225 |
| R average / max, 18 LPM, 15 kW (mK/W) | 1.95 / 2.33 | 2.07 / 2.59 | 1.60 / 1.92 |
| dT avg / max at 15 kW, 18 LPM (K) | 29.2 / 34.9 | 31.1 / 38.8 | 24.1 / 28.9 |
| dT avg / max at 15 kW, 15 LPM rated (K) | 30.9 / 37.1 | 32.9 / 41.0 | 25.8 / 31.1 |
| Inlet allowed at 15 kW, 18 LPM (C) | 50.1 | 46.2 | 52.3 (return-limited) |
| Capacity, 85 C case, 45 C in, 1.2 LPM/kW (kW) | 18.4 | 15.7 | 19.5 rated (25.4 thermal) |
| Plate dP 15 / 18 / 22.5 / 36 LPM (kPa, 20 mm bore) | 5.5 / 7.6 / 11.4 / 27.5 | same | same |
| With barbs + UQD08 pair, 18 LPM (kPa) | 24.5 (Cv 4.75) - 34.2 (Cv 3.65) | same | same |
| P10 / P50 / P90, 18 LPM (K), from `final_thermal.out` §2 at base 0.80 + 0.14 | avg 26.7 / 29.3 / 32.4; max 32.3 / 35.2 / 38.6 | avg 27.9 / 31.2 / 35.4; max 35.6 / 39.3 / 43.7 | avg 22.2 / 24.2 / 26.4; max 26.9 / 29.2 / 31.8 |

## 8. Design margins (velocity, pressure, structure, bow)

Velocity caps are the architecture's rating rules (4.1); the plate's thermal capacity is higher than its velocity-rated capacity for every TIM, so the velocity caps govern the published rating.

| Quantity | 15 LPM (rated) | 18 LPM (benchmark) | 22.5 LPM (150 % rated) | Cap | Margin at 150 % | Basis |
|---|---|---|---|---|---|---|
| Port velocity, 20 mm bore (m/s) | 0.80 | 0.95 | 1.19 | ≤ 1.5 at 150 % rated | 1.26x (cap reached at 28.3 LPM) | architecture 4.1; 22 mm outlet bore option for the > 60 C return band (0.79 m/s at 18) |
| Meter mean orifice velocity (m/s) | 1.28 | 1.54 | 1.93 | ≤ 2.0 mean | 1.04x (cap at 23.4 LPM = 19.5 kW at 1.2 LPM/kW) | DDD-grate 6.1, 195.1 mm2, Cd 0.72 |
| Meter largest single orifice (m/s) | 1.37 | 1.64 | 2.05 | mean-velocity rule | 6 % above mean | DDD-grate 6.1 (step 5 at y +15) |
| Outlet row (m/s) | 0.60 | 0.72 | 0.90 | 0.5 kPa row at 18 | - | DDD-grate 6.3 |
| Inlet header, two arches 161 mm2 per half (m/s) | 0.78 | 0.93 | 1.16 | ≤ 1.5 | 1.29x | architecture 4.1 |
| Outlet header, four arches 322 mm2 per half (m/s) | 0.39 | 0.47 | 0.58 | ≤ 0.9 CDA band for return > 60 C | 1.55x | architecture 4.1, 7.3 |
| Plenum half-channel 6.9 x 5.0 (m/s) | 0.52 | 0.62 | 0.78 | ≤ 0.9 CDA | 1.15x | DDD-plenum P3 |
| Window face mean (m/s) / fin-top estimate | 0.28 / 0.33 | 0.33 / 0.40 | 0.41 / 0.50 | fin-top ≤ 0.5 (E2 CFD gate) | 1.0x at 150 % (20 % at 18 LPM) | DDD-grate 5 |
| Fin channel (m/s), Re | 0.165, 37 | 0.198, 44 | 0.248, 55 | laminar | - | `harness.ev` |
| Guard face, 25 cm2 square weave (m/s) | 0.10 | 0.12 | 0.15 | 0.1-0.2 kPa clean | - | architecture 4.1 |

| Pressure / structure | Value | Allowable or limit | Margin | Basis |
|---|---|---|---|---|
| MAWP / 100 % proof / design burst / sample burst | 1.03 / 1.55 / ≥ 3.1 / ≥ 4.5 MPa | 150 psi class; leak-before-break (ductile Cu) | burst ≥ 3x MAWP | architecture 5.2 |
| Folded plenum wall 0.8 at 7.714 pitch, tension at 3.1 MPa | 29.8 MPa | 40 MPa (post-braze annealed OFE, design) | 1.34x | `ctl/pkgA_dp_stress.out` |
| Separator 1.8 over the 6.9 outlet channel at 3.1 MPa | 22.8 MPa | 40 MPa | 1.75x | 32.8 MPa at 1.5 mm scaled t^-2 (DDD-plenum 1.8 mm) |
| Arched cap 1.0 mm r 6 hoop / port pocket r 12 at 1.5 | 18.6 / 24.8 MPa | 40 MPa | 2.2x / 1.6x | `pkgA_dp_stress.out` (cap lane to confirm on the CAD arches 12 x 8) |
| Grate web 0.40 over the 2.70 recess, meter dP 9.2 kPa at 36 LPM | 0.21 MPa | 40 MPa | > 100x | DDD-grate 8 |
| Recess floor cantilever, 0.75 lip at t 0.50 | 7.5 MPa | 40 MPa | 5.3x | DDD-grate 8 |
| Governing defect: one unbonded land strip, base 0.85, span 7.4 kerf-to-kerf | collapse 1.8-2.6 MPa; proof bulge ~1.8 µm | leak-tight at MAWP; confocal 1 µm resolution | below design burst: the 0.85 base stays gated on E1 per-strip detection | `pkgA_dp_stress` at 0.8 mm (1.6-2.3 MPa, 2.2 µm) scaled t^2 and t^-3 |
| Pressure load on the tied base, 1.03 MPa x 117 cm2 | 12 kN | self-equilibrated by the fin ties | does not enter the clamp budget | DDD-mech 5 |
| Clamp bow, 2 kN TTV / 480 N product, 2-side lands at y ±58.2 | 22.6 / 5.4 µm concave | thermal bow +18.7 µm convex at 15 kW | net -4.0 µm on the TTV; form rule 0-10 µm concave at 20 C | DDD-mech 7, O-M2 |
| Case-temperature headroom at 15 kW, 18 LPM | inlet allowed 46.2 C paste / 50.1 C PCM / 52.3 C LM (P50) | Tcase,max ≤ 85 C, return ≤ 65 C | +1.2 / +5.1 K over 45 C (paste / PCM) | section 2 |

## 9. What to measure first (E0/E3 order, before any public number)

1. **Rig repeatability on the incumbent plate (E0):** ≤ 1 K on the 8-TC maximum, ≤ 0.3 K on the average, same TTV-A and TIM lots; measure the real UQD08 pair Cv at 6 flows (vendor 3.65-4.75 spans 1.7x in dP).
2. **Plate dP at 6 flows, 45 ± 2 C, three boundaries,** transducers 0-2 / 0-10 / 0-100 kPa (0.57 kPa at 25 %, 27.5 kPa at 36 LPM). Cheapest test, carries the ≤ 10 kPa claim and exposes the meter Cd (±10 % = +0.54 / -0.40 kPa) before any thermal test.
3. **Meter Cd on coupons (E2) in both flow directions, Re 300-1700, 5 sizes.** If Cd ≠ 0.72 the artwork scales all areas by 0.72/Cd; the thermal numbers do not move, the dP table does.
4. **Fin-field dP taps** (1.0 mm, inlet and outlet plenums, first five plates): isolates the 1.07 kPa viscous fin term; > 1.3 kPa = filler in kerfs or windows, < 0.9 kPa = missed tip joints (bypass).
5. **Average case temperature at 18 LPM on PCM** (decision metric, P(avg ≤ 31 & max ≤ 36) = 0.63): three mountings, two plates; then the 15 LPM rated point; then the 6-flow sweep at reduced power for 25-75 %.
6. **Maximum-minus-average** at 18 LPM: 7.7 K paste / 5.7 K PCM predicted (P90 9.5 K paste); more points at segment balance (R2) or TIM, separated by the dP taps and an IR scan at 2 kW.
7. **Heated, pressurised flatness scan** (O-M2): clamp 22.6 vs thermal 18.7 µm is a difference of near-equal terms; measure before fixing the concave pre-form.
8. **Proof 1.55 MPa with confocal scan and lot over-proof 2.5-3.1 MPa** (per-strip detection at base 0.85 is the gate for the base thickness; otherwise 1.0 mm, +0.55 K average).
9. **Water, 35 / 50 C inlet and one cold start-up point (17-25 C, dP 8.7-9.4 kPa)** last: property-shift checks on the model, not rating points.

## 10. Deviations, open items, files

| ID | Item | Effect | Owner / gate |
|---|---|---|---|
| D-P1 | Base 0.85 (DDD-core final) instead of the architecture's 0.80: benchmark avg +0.14 K, max +0.09 K for every TIM | 31.1 / 38.8 K paste, 29.2 / 34.9 K PCM, 24.1 / 28.9 K LM; R'' 0.243 / 0.228 / 0.188 cm2K/W | recorded; the architecture's 31.0 / 38.7 stands as the P50 claim within its ±0.2 K rounding only on the maximum; the datasheet uses 31.1 / 38.8 |
| D-P2 | Segment max/min 1.092 (lumped row, DDD-grate D5) instead of 1.061: the weakest segment runs +0.41 K core at 18 LPM, inside the 1.5 K flow hot-spot allowance (margin 1.09 K); the allowance is left at 1.5 K | nil on the published maximum | E2 water table ≤ 1.15 confirms |
| D-P3 | Meter 2.31 kPa (artwork, flow-weighted) vs 2.30 budget; plenums 0.19 inertial + 0.02 viscous; misc split 0.08 / 0.08 | plate dP 7.61 kPa at 18 LPM, rounds to the 7.6 claimed | - |
| D-P4 | UQD08 pair computed as two couplings in series from the vendor Cv (SG 1.007); the architecture's 14-24 kPa band reproduced (13.8 / 23.4) | tray-loop boundary numbers unchanged | E0 measures the real pair |
| O-P1 | Inlet-temperature cases use PG25 property fits at film ≈ inlet + 5 K (µ 1.60 / 1.25 / 1.12 mPa·s at 35 / 45 / 50 C, ±10 %); the case-to-inlet dT moves < 0.3 K between 35 and 50 C | datasheet lists Tcase = Tinlet + dT with the property shift included | property table from the coolant vendor in M1 |
| O-P2 | Capacity bisection at 1.2 LPM/kW (14 steps, ±0.1 kW); the velocity-rated 19.5 kW governs for PCM and LM | rated capacity 19.5 kW PCM/LM, thermal for paste | - |
| O-P3 | CoolIT-like columns are a reconstruction (footprint 119.3 cm2 recalibrated at k 0.49, ramp hot spot 0.5 dT_out): model-only at every flow, measured only at 18 LPM (34.4 / 44.2 K) | labelled model-only in every table | E0 measures a real incumbent |

Files: `perf_datasheet.py` (prints every table here; ~5 min, from this directory), `perf_datasheet.out`, `params-perf.json` (headline numbers, written by the script). Upstream: `appendix/verify/final/final_thermal.py`, `final_segbal.py`, `final_coolants.py`, `appendix/verify/ctl/harness.py`, `appendix/arch/cell2d.py`, `model/coldplate_model.py`.
