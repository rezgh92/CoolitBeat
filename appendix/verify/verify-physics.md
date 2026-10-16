# Verification: thermal physics lane (PRISM draft)

Key: `physics`. Reviewer stance: adversarial. Date: 2026-10-14.

## 0. Verdict in one paragraph

The physics of PRISM holds up. The 2-D cell model is implemented correctly, and the term budgets are arithmetically right. PRISM still beats CoolIT's measured maximum and its uniformity at the benchmark point. The **absolute headline numbers, however, are about 1.5 K optimistic**. The draft subtracts CoolIT's own 2-D penalty (6.9 % of core) from PRISM's. That subtraction is valid only when PRISM is compared with the *footprint-calibrated CoolIT model* at the 2-D-recalibrated footprint (about 123-125 cm2). It is not valid for PRISM's own 117 cm2 TTV, nor for the "footprint-fair" Monte Carlo, which uses CoolIT's *measurement* at an independently drawn footprint.

Four other claims are wrong or overstated:

- the CoolIT 4 kW "tie";
- the 350 W/cm2 margin, where a TIM label is wrong;
- the "narrow win" on GPU-class lids, which is really parity;
- the high-flux branch of the flux-graded flow-length rule.

## 1. Method

I wrote an independent finite-volume x-z conjugate solver from scratch: `verify/vp_cell.py`. It has Hele-Shaw pressure, a two-temperature fin layer, kerf columns, end-face or top-window outlets and an optional layered base. It reproduces `cell2d.py` to within 0.05 K:

| Flow length | My solver | `cell2d.py` |
|---|---:|---:|
| L 4 mm | 23.99 K | 23.96 K |
| L 6 mm | 22.88 K | 22.83 K |
| L 8 mm | 22.28 K | 22.25 K |

The peak-to-peak values are identical (1.70 / 3.69 / 5.46 K). It also reproduces the CoolIT-like case, 27.25 K (+1.75 K), when I use the draft's outlet representation. Energy and mass close to 1e-4 and 1e-13. The grid is converged: going from d = 0.05 to 0.02 mm changes the result by +0.05 K.

The 1-D terms were checked analytically at NTU = heff·dTout/q'' = 1.20, which is independent of L:

| Term | Value |
|---|---:|
| Caloric | 7.57 K |
| Convection | 10.55 K |
| Base | 3.29 K |
| heff | 121.5 kW/m2K |
| Fin efficiency (eta) | 0.648 |

The TIM terms are 7.05 K (PCM), 8.97 K (paste) and 1.92 K (LM). All of these are **confirmed**.

Scripts are in `verify/`: `vp_cell.py` (solver), `vp_run1-3.py`, `vp_lid.py`, `vp_350*.py`, `vp_Lrule.py`, `vp_pen_flux.py`, `vp_mc*.py`.

## 2. The 2-D differential (draft 3.2 and 3.4): main finding

**The physics in cell2d is right.** Treating the fluid as unmixed in z is the correct treatment:

- The flow is laminar (Re about 34 in the gaps, about 100-200 at the kerf entry).
- The fluid's z-diffusion length over one transit is about 0.1 mm, against a 2 mm fin height.
- A local Nu-based h across the 0.15 mm gap does not double-count with the resolved z-stratification. Nu covers the y-direction and the grid covers z.

It omits kerf jet inertia (probably favourable), fin-tip conduction into the grate (conservative) and the **3-D y-discreteness of the orifices** (2c).

**(a) Subtracting the differential is a double count.** PRISM-15's own absolute penalty at L 6 mm is **+1.48 K (+6.9 % of core)**. The draft sets the "2-D diff" to 0.0 by subtracting 6.9 % of core, arguing that the CoolIT calibration "absorbed" CoolIT's penalty. In `coldplate_model.py`, however, the only calibration knob is **footprint**. The absorbed 1.75 K is therefore hidden in the "117 cm2", which is a model artefact. Recalibrating CoolIT with its 2-D penalty included gives 123 cm2 (5.5 % penalty) or 125 cm2 (6.9 %). PRISM evaluated *there* with its full penalty gives 28.6-28.8 / 33.2-33.5 K on PCM, which is essentially the draft's headline.

So 28.4 K is "PRISM tested at about 124 cm2". It is **not** "PRISM on our 117 cm2 TTV", which is what the scorecard, the M12 gate and the "pub" Monte Carlo basis state. Corrected values on a 117 cm2 TTV:

| Build | Draft avg / max | Corrected avg / max |
|---|---|---|
| PCM 25 psi | 28.4 / 33.3 | **29.9 / 34.8 K** |
| Paste 0.07 | 30.4 / 37.2 | **31.8 / 38.7 K** |
| PCM at module retention | 30.4 / 35.2 | 31.8 / 36.7 K |
| LM | 23.3 / 27.3 | 24.8 / 28.7 K |
| P + PCM | 25.4 / 29.7 | 26.7 / 31.0 K |
| P + paste | 27.4 / 33.6 | 28.6 / 34.9 K |

Effect on capacity and headroom:

| Metric | Draft | Corrected |
|---|---|---|
| Q capacity, PCM | 19.4 kW | 18.2 kW |
| Q capacity, paste | 16.6 kW | 15.7 kW |
| Q capacity, LM | 26.4 kW | 24.2 kW |
| Inlet headroom, PCM | 51.7 C | 50.2 C |
| Inlet headroom, paste | 47.8 C | 46.3 C |

The like-for-like paste win on the average shrinks from -12 % to **-7.6 %**. On the maximum it shrinks from -16 % to -12 %.

**(b) CoolIT's 6.9 % is itself an artefact of the model setup.** It comes from modelling the split-flow exit as a 1 mm top window at the fin end. With a realistic full-height end-face exit, the penalty is **+5.5 %** (1.41 K). For other plausible undisclosed CoolIT fin sets it ranges from 3.5 to 11.4 %:

| CoolIT fin set (thickness / gap x height) | Base | Penalty |
|---|---|---:|
| 0.2 / 0.2 x 3 mm | 1.5 mm | 3.5 % |
| 0.15 / 0.15 x 3 mm | - | 4.7 % |
| 0.1 / 0.2 x 4 mm | - | 11.4 % |

So even under the draft's own logic, PRISM's differential is +1.4 % of core (+0.3 K), not 0.0 K, with a range of -1.0 to +0.7 K. Comparing differentials is legitimate only between two 2-D models at a declared common footprint, with this geometry uncertainty carried explicitly.

**(c) Kerf and Hele-Shaw claims are confirmed with caveats.**

- The kerf is worth 0.66 K at L 6 mm (no kerf: 23.54 K, which matches the draft's +0.6 K).
- If the inlet kerf fills (impaction), the cost is +0.30 K; if both kerfs fill, +0.66 K.
- The kerf permeability ratio of 8 (w²/12 against phi·g²/12) is reasonable. A ratio of 4-16 moves the result by ±0.25 K.
- A floor h of 6k against 12k changes nothing.

**Unmodelled 3-D effect.** The orifices sit at 2 mm pitch along y. The jet leaves the vena contracta at about 1.9 m/s, so its stagnation pressure is about 1-1.8 kPa. The downstream resistance is only about 0.73 kPa (fins plus turn). The gaps directly under each orifice are therefore over-fed, and the fin tips there see about 1.4-1.9 m/s impingement. The "0.41 m/s mean fin entry" is a y-average and does not show this. Base spreading (conduction length about 1.8 mm, against a 2 mm period) should keep the thermal cost to about 0.3 K or less, but this needs one 3-D CFD cell.

**Fluid properties.** PG25 k = 0.52 W/mK is about 5 % high; the 30 vol % value at 50 C is about 0.47. Using 0.49 adds +0.42 K to PRISM's core.

## 3. Budgets (draft 3.4)

Every row is arithmetically **confirmed** against the draft's inputs, except the 2-D column (see section 2). The ripple crest of 1.85 K matches the computed peak-to-peak of 3.69 K. The inputs to the hot-spot terms are assumptions that remain **unverifiable** until test:

- flow maldistribution 1.5 K;
- PCM scatter 1.5 K, against 3.5 K for paste;
- LM scatter 0.6 K.

## 4. Flux-graded flow length (3.3) and GPU-class numbers

**High-flux branch: refuted.** The rule assigns 4-5 mm to zones at or above 250 W/cm2, but my 2-D runs do not support it. At 350, 200 and 128 W/cm2:

- **L 4 mm is the worst flow length on both the average and the crest.**
- The crest (average plus half the peak-to-peak) is flat to within 0.35 K across L 5-8 mm. For example, at 350 W/cm2 the crest is 49.55 / 49.19 / 49.24 / 49.47 K for L 4 / 5 / 6 / 8 mm.
- The average falls monotonically with L.

Short cells at high flux need a hydraulic justification, not a thermal one.

**Low-flux branch: the PRISM-internal gain is confirmed, but the claimed win over CoolIT is really parity.** Test case: 2.3 kW on 60 cm2 at 1.0 LPM/kW, both plates in 2-D, both with R'' 0.07, CoolIT with an end-face exit.

| Case | PRISM L 12 mm minus CoolIT, average |
|---|---:|
| No lid | -0.50 K |
| 3 mm Cu lid (case = lid top) | **-0.20 K** |

The lid re-isothermalises each 12 mm cell. It raises PRISM's average by 0.63 K but CoolIT's by only 0.33 K. The draft cites the lid to smooth the ripple on the maximum, but the same mechanism erodes the average advantage. A 0.2-0.5 K difference on about 17 K is far inside the ±25 % convention, so this is parity.

The maximum advantage (about 1-3 K) is plausible. Two scripts bias the maximum in opposite directions:

- `run_gpu.py` gives PRISM the PCM scatter (1.5 K) while giving CoolIT the paste scatter (3.5 K), even though R'' is 0.07 on both.
- The scoping model's fixed 6.3 K ramp (8a) is too small at 1.0 LPM/kW.

The net effect is slightly conservative for PRISM.

**The baseline itself is not credible off its calibration point.** The CoolIT-like reconstruction predicts **0.0126 C/W** for CoolIT's 4 kW plate (25 cm2), against a measured < 0.009, which is at least 37 % high even with the ramp corrected. The model is calibrated at a single point by footprint and misses the only other CoolIT datum by at least 37 %. Every model-only "CoolIT-like" comparison inherits this error: GPU class, 350 W/cm2, the flow sweep and Q capacity.

## 5. The 350 W/cm2 package (6.3)

- **A TIM label is wrong.** The CoolIT-like 88.6 K in the heat-map report uses **paste 0.07** (budget TIM 24.5 K; `R_PASTE_CI = 0.07e-4`), not 0.05 as the table header says. Like-for-like values:
  - paste 0.05: **81.6 K**;
  - LM: **69.4 K (about 114 C)**, not about 76 K (121 C).
- **PRISM's own penalty is larger than the term used.** At 350 W/cm2 it is **+3.76 K** (8.7 %) for R at L 5 mm and H 2.0 mm, against the +1.6 K used. For the P-grade it is **+3.06 K**, against the +0.2 K used.
- **Taller fins barely help in 2-D.** The 2.5 mm "die SKU" fins gain only **0.33 K** in 2-D, against 1.3 K in 1-D. This matches the draft's own finding at 128 W/cm2 that taller fins are worse.
- **The fit's caloric term is slightly low.** It came from a linear-caloric heat-map, and the isothermal-cell correction adds about 0.5 K at NTU 0.47.

Corrected Tcase,max with LM:

| Build | Draft | Corrected |
|---|---|---|
| R | 93-94 C | **about 97 C** |
| P-grade | 84 C | **about 87 C (misses 85 C)** |

The like-for-like margin over split-flow is **about 18-20 K, not 27-28 K**.

## 6. CoolIT's 4 kW point (6.4)

The claim that PRISM "ties with PCM" is **refuted**. Using the draft's own method, PRISM is at 0.0093 C/W, which is already above CoolIT's < 0.009. With PRISM's own penalty the results are:

| Build | 25 cm2 heater | 20 cm2 heater |
|---|---:|---:|
| R + PCM | **0.0096-0.0097** (7-8 % worse) | **0.0115** (28 % worse) |
| R + paste | 0.0109 | - |
| P + PCM | 0.0084 | 0.0100 (loses) |
| R + LM | 0.0078 (wins) | 0.0093 (loses) |

The 20 cm2 case reflects Tom's Hardware's "shy of 200 W/cm2". The drop-in core loses this CoolIT-disclosed metric. This conflicts with the "every metric CoolIT disclosed" wording in D1.

## 7. Monte Carlo and footprint-fair probabilities (6.1)

The Monte Carlo has five methodology problems:

1. **The 2-D term is wrong on both bases.** It is the differential (0.5 ± 2 %) rather than PRISM's own penalty, on both the "pub" basis and the "fair" basis. On the "fair" basis this double-counts: CoolIT is represented by its measurement at an independently drawn footprint, *and* PRISM is credited with CoolIT's calibration-absorbed penalty.
2. **The "one-sided bias" is not one-sided.** The c2d draw is symmetric about +0.5 %.
3. **The footprint-fair basis is not a stress test.** The triangle tri(100, 120, 145) has a mean of 121.7 cm2, which is above 117, so it is more favourable than the "pub" basis. This explains why P rises from 0.88 to 0.90.
4. **Model-form error is excluded,** although the 4 kW miss of at least 37 % shows it is the dominant uncertainty.

Results recomputed with PRISM's own penalty, N(f(q''), 0.01), and the draft's other distributions:

| Build | Draft P(avg < 34.4) pub / fair | Corrected | Draft P(max < 44.2) | Corrected |
|---|---|---|---|---|
| R paste | 0.88 / 0.90 | **0.79 / 0.82** | 0.97 / 0.96 | **0.93** |
| R PCM 25 psi | 0.99 / 0.98 | 0.96 / 0.96 | 1.00 | 1.00 |
| R PCM at module retention | 0.94 | **0.85** | 1.00 | 1.00 |
| P paste | 0.98 | 0.96 | 1.00 | 0.99 |

Corrected P10 / P50 / P90 for R paste, average: 28.8 / 32.0 / 36.1 K.

Other corrected results:

- With CoolIT's footprint below 105 cm2, the paste average wins only with P = 0.39.
- With the footprint below 110 cm2, the paste maximum wins with P = 0.73.
- Deterministically at 100 cm2, paste gives **35.7 / 43.4 K**. It loses the average by 1.3 K, and the maximum margin is only 0.8 K. The draft's statement that "maximum... wins hold at every footprint" is **refuted** for the like-for-like paste case.
- The model-only probability of the decisive PCM result (≤ 31 / ≤ 36 K) is **0.62**, against 0.81 in the draft's own Monte Carlo. The draft's judgement figure of about 0.6 including programme risk should drop to about 0.45.

## 8. Code review: `docs/cooling/model/coldplate_model.py`

1. **Bug: the split-flow ramp hot spot is fixed.** `hotspot_flow_K` stays at 6.3 K at any flow, but the intrinsic split-flow ramp is 0.5·dT_out. This makes the CoolIT-like maximum wrong at every flow except 1.2 LPM/kW:

   | Flow | Model maximum | Correct maximum |
   |---|---:|---:|
   | 0.75 LPM/kW | 48.3 K | 52.1 K |
   | 1.0 LPM/kW | 45.6 K | 46.9 K |
   | 2.4 LPM/kW | 40.8 K | 37.7 K |

   The draft's 6.2 table and the GPU-class maxima inherit this error.
2. **Footprint is the only calibration knob.** Every model-form error (2-D penalty, k_f, Nu, TIM) ends up in "117 cm2", which is then reused as if it were a physical TTV size. This is the root cause of the error in section 2.
3. **`Q_cap` is slightly inconsistent.** It subtracts the hot spot at the evaluated Q, so the scatter does not scale to Q_cap, and it holds NTU fixed. This gives 12.70 kW against a consistent 12.94 kW. The draft avoids the problem by using bisection.
4. **PG25 conductivity is high.** k = 0.52 W/mK is about 5 % high. The density of 1005 kg/m3 is slightly low.
5. **Minor.** The Stephan correlation (uniform wall temperature) is added to an H1 Nu; the fin tip is adiabatic (conservative for a tied sandwich); the caloric switch is binary, with no L-dependence, which is why cell2d was needed.

Housekeeping: `prism_model.py`'s header ("R +5.2 %") and `prism_model.out` (L 4 mm, 29.6 / 33.4 K) are stale and contradict the draft.

## 9. Fatal issues (to the public claim, not to the architecture)

1. **The headline is about 1.5 K optimistic.** The 28.4 / 33.3 K (PCM) and 30.4 / 37.2 K (paste) values, quoted "at 117 cm2", rest on subtracting CoolIT's calibration-absorbed penalty. Publishing them as predictions for our TTV is indefensible.
2. **D1's "every metric CoolIT disclosed" is false for the drop-in core.** The 4 kW plate resistance is lost with PCM (by 7-28 %) and with paste.
3. **The 350 W/cm2 "beats split-flow by 27-28 K" compares paste 0.07 with paste 0.05.** The true margin is about 18-20 K, and the P-grade does not reach 85 C.

## 10. Required changes

1. Use PRISM's own absolute 2-D penalty in every absolute prediction:
   - headline, scorecard and Monte Carlo;
   - Q capacity and headroom;
   - 4 kW point, 350 W/cm2 and 25-30 kW cases.

   Keep any differential only as a model-to-model statement at a declared, recalibrated footprint (about 124 cm2), with a CoolIT-geometry band of 3.5-11.4 %.
2. Republish the probabilities: paste average P = 0.79-0.82; maximum P = 0.93; decisive PCM result 0.62 model-only and about 0.45 including programme risk.
3. Rewrite the footprint text: at 100 cm2 with paste the average is a loss of about 1.3 K and the maximum margin is 0.8 K. Delete "maximum wins hold at every footprint".
4. Change the 4 kW point from "ties" to "loses". Only LM qualifies at 25 cm2.
5. In 6.3:
   - fix the CoolIT-like TIM label and the LM value (69 K / 114 C);
   - apply the full penalty (+3.8 K for R, +3.1 K for P);
   - cut the 2.5 mm fin gain to 0.3 K;
   - state that the P-grade is about 87 C.
6. Restate the GPU-class average as parity (lid-dependent, -0.2 to -0.5 K). Keep the maximum win, and disclose that the reconstruction misses CoolIT's 4 kW plate by at least 37 %.
7. Change the flux-graded rule's high-flux branch to 5-6 mm, or justify 4-5 mm on hydraulics.
8. Patch `coldplate_model.py`:
   - set the ramp hot spot to 0.5·dT_out;
   - set PG25 k to about 0.49 W/mK;
   - regenerate the CoolIT-like column in 6.2.

   Remove or regenerate the stale `prism_model.out`.

## 11. Improvements

- Calibrate the CoolIT reconstruction on both CoolIT points (15 kW and 4 kW), or test purchased incumbent plates, before quoting any model-only "CoolIT-like" number.
- Run one 3-D CFD cell (2 mm orifice pitch by 6 mm) for y-maldistribution and fin-tip impingement.
- Model the lid explicitly for lidded-package claims; re-check the P-grade at L 5-6 mm.
