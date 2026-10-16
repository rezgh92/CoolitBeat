# SYNTHESIS-physics: consolidated verdict on the HMMC cold plate vs the CoolIT 15 kW benchmark

Chief-engineer reconciliation of the seven physics reports (`hydraulic-detail`, `manifold-maldistribution`,
`hotspot-smoothing`, `nonuniform-heatmap`, `fouling-filtration`, `base-stress-stiffness`, `tim-and-direct-to-die`,
`two-phase-option`). Script: `SYNTHESIS-physics.py` (output `SYNTHESIS-physics.out`, same directory). Operating point
throughout: 15 kW on the calibrated 117 cm2 (108 x 108 mm, 128 W/cm2) footprint, 18 LPM PG25 (1.2 LPM/kW), 45 C inlet,
dT_out = 12.66 K. CoolIT measured: 34.4 K average, 44.2 K maximum case-to-inlet, pressure drop undisclosed.

## 0. Corrections applied to the scoping model

The sibling checks found five things in `coldplate_model.py` / `model_output.md` that change the numbers. All are
applied consistently in `SYNTHESIS-physics.py`; the first two must also be patched into the project model.

1. **Channel friction 4x low.** The model used the Fanning f.Re in a Darcy formula. Correct: dp = 2 f.Re mu u L / Dh^2.
   The CoolIT-like skived plate is ~22 kPa at 18 LPM (band 17-42 kPa for the undisclosed fin pitch), not 8.6. The HMMC
   is unaffected (its channel term is 0.2-0.8 kPa). The hydraulic advantage is 4x, not 1.4x.
2. **Caloric term for manifold plates is isothermal, not linear.** A 2-4 mm cell is isothermal at the fin scale, so the
   fluid picks up heat exponentially: dT_cal = dT_out [1/(1-e^-NTU) - 1/NTU] = 0.60-0.68 dT_out instead of 0.5. Costs
   +1.3 K (robust core) to +2.2 K (fine core) on the mean, confirmed by coupled 2-D finite volume within 0.05 K.
3. **Hot-spot term re-based.** Max - avg = flow-driven long-wave maldistribution + TIM/assembly scatter (max of 8 TCs).
   CoolIT's 9.8 K decomposes as 6.3 K intrinsic 54 mm ramp (+2.5 K for +/-10-20 % header maldistribution) and ~3.5 K
   paste/bow scatter. HMMC flow-driven: 0.25 K perfect, 1.3 K at +/-10 %, 2.3 K at +/-20 %; nominal 1.5 K. Scatter
   scaled by bow sensitivity: paste 3.5, PCM 1.5, liquid metal 0.6 K. The model's flat 4 K was the wrong shape.
4. **Channel-gap floor from fouling: 0.15 mm** for the 10-year drop-in SKU (W/d = 3 behind a 50 um absolute plate
   screen); 0.10 mm only behind <= 33 um absolute loop filtration; 0.05-0.075 mm not deployable (W/d <= 2-3, 1-3 year
   relative life, x2.5-4.6 channel dP at a 10 um film). The headline 19.8-22 K rows in `model_output.md` are off the
   roadmap.
5. **Manifold geometry of record = design H**, not the 0.3-0.5 mm slots / 4x8 mm headers in the model (those back-flow
   at 18 LPM). Design H: 8 mm slot pitch (4 mm flow length), centre-fed and centre-collected (CC) two-level headers
   10x15 / 14x20 mm, 3.5 x 8 mm slots, 16 mm ports: 5.0 kPa port-to-port at 18 LPM, global max/min 1.10. With 0.15 mm
   gaps the channel friction falls to 0.23 kPa, so a >= 0.4-0.5 mm orifice comb at each slot top restores a 2.2 kPa
   branch (92 x 0.5 mm holes per 108 mm slot at 1.2 m/s). Total stays ~5 kPa; the branch becomes inertial, so uniformity
   no longer degrades with flow.
6. Base 1.0 mm as-bonded / 0.8 mm finished, only in a tied sandwich (fin tips brazed to manifold webs).

## 1. Consolidated numbers (15 kW / 18 LPM / 45 C, nominal and P10-P90 Monte Carlo)

Monte Carlo (20k samples): h_eff +/-25 %, TIM lognormal with P90 at the report's upper value, base +/-10 %, caloric
+/-5 %, hot-spot terms +/-40 %, dP viscous +/-25 % / inertial +/-45 %. Q capacity = largest load with T_case,max <= 85 C
at constant 1.2 LPM/kW. The CoolIT-like row reproduces the measurement (34.6 / 44.6 K median vs 34.4 / 44.2 measured),
which is the calibration, not a prediction.

| design (core / TIM) | avg dT K (P10-P90) | max dT K | R'' cm2K/W | dP kPa | pump W | Q cap kW | deployable |
|---|---|---|---:|---|---|---|---|
| CoolIT-like skived split-flow 0.2/0.2x4, 2 mm base, paste 0.07 | **34.5** (30-42) | **44.3** (40-52) | 0.269 | 21.8 (19-25; geometry band 17-42) | 6.5 | 12.9 (10-15) | field-proven |
| HMMC-R robust 0.15/0.10x2.0 mm, L 4 mm, base 1.0, **same paste 0.07** | **30.0** (26-37) | **35.0** (31-42) | 0.234 | 5.0 (3.9-6.6) | 1.5 | 18.1 (14-22) | yes, 50 um abs screen |
| HMMC-R robust, PCM pad 0.055 **[Tier 1 drop-in]** | **28.0** (26-31) | **31.1** (29-35) | 0.219 | 5.0 | 1.5 | 21.5 (18-24) | yes |
| HMMC-R robust, liquid metal 0.015 **[Tier 2 OEM]** | **22.9** (22-25) | **25.0** (24-27) | 0.179 | 5.0 | 1.5 | 30.3 (27-33) | yes, Ni-plated lid |
| HMMC-P performance 0.10/0.10x1.5, L 4, PCM | 25.4 (23-29) | 28.4 (26-32) | 0.198 | 5.1 | 1.5 | 25.0 (21-29) | <= 33 um abs loops only |
| HMMC-P performance, liquid metal | 20.2 (19-22) | 22.3 (21-24) | 0.158 | 5.1 | 1.5 | 37.9 (33-42) | <= 33 um abs loops only |
| (reference only) HMMC-fine 0.075x1.0, LM | 19.2 (18-21) | 21.3 (20-23) | 0.150 | 5.1 | 1.5 | 42.7 | **no** (W/d <= 3) |
| HMMC-R, direct-to-die LM, base 0.8 **[Tier 3]** (case = die top) | 22.3 (21-24) | 24.4 (23-26) | 0.174 | 5.0 | 1.5 | 31.7 | chip co-design |

Term budget, robust core with PCM: caloric 7.6 (isothermal, NTU 1.25) + TIM 7.1 + base 3.3 + convection 10.1 = 28.0 K;
hot spot 1.5 flow + 1.5 scatter. Channel velocity 0.083 m/s, Re 19, h 13.2 kW/m2K, eta 0.56, h_eff 127 kW/m2K,
12,100 parallel 4 mm segments. Plate port-to-port 5.0 kPa = ports 2.5 + manifold 0.5 + channel 0.2 + orifice 2.0.
UQD08-class couplings add ~25 kPa per pair (estimate +/-50 %) and dominate the loop; UQD12-class or 3/4 in barbs ~5 kPa.

**Equal pumping power** (CoolIT-like 6.5 W hydraulic at 18 LPM): the HMMC runs 30 LPM (2.0 LPM/kW) at 13.3 kPa and the
caloric term falls to 4.3 K: HMMC-R PCM 24.6 / 27.6 K, HMMC-R LM 19.5 / 21.6 K, HMMC-P LM 16.4 / 18.5 K. At equal
average dT the robust core needs ~7 LPM and ~0.2 W, i.e. 30-40x less pumping power than the benchmark. Flow is a weak
lever (0.6 -> 2.5 LPM/kW moves HMMC-R PCM from 38 to 23.5 K); fins, TIM and manifold uniformity are the strong ones.

**Real package (4 reticle dies at 350 W/cm2 + 16 HBM, heat-proportional zoning, 1 mm base), hottest die cell,
case-to-inlet:** fit to the nonuniform-heatmap sweep dT = 33 + 3500/h_eff + 350 (R_TIM - 0.05).

| core | h_eff kW/m2K | paste 0.05 | PCM | LM | T_case,max with LM |
|---|---:|---:|---:|---:|---:|
| CoolIT-like split-flow, flow across die then HBM | 101 | 88.6 K (report) | - | ~76 K | ~121 C |
| HMMC-R robust 0.15 mm | 127 | 60.5 | 62.3 | 48.3 | **93 C** |
| HMMC-P performance 0.10 mm | 187 | 51.7 | 53.4 | 39.4 | **84 C** |
| HMMC-fine 0.075 mm (not deployable) | 239 | 47.7 | 49.4 | 35.4 | 80 C |

Un-zoned HMMC loses 15 K of this (die block gets 30 % of flow); zoning is mandatory. HBM needs a stepped Cu pedestal with
<= 0.1 mm BLT (gap-filler pads fail above ~15-20 W/cm2 on every plate); with it HBM Tj is 84-91 C on the HMMC vs 105 C on
the split-flow plate whose HBM sits downstream of the dies.

## 2. Design rules that emerged

**Channel width (fouling floor).** Primary gap >= 3x the absolute rating of the last filter the plate sees, >= 6x where
possible. Today's loops (50 um nominal, ~90 um absolute) imply 0.27 mm without a plate screen; **0.15 mm with an
integrated 50 um absolute screen** (10-year SKU, relative life 0.6-1.2x a skived plate); 0.10 mm only behind <= 33 um
absolute (performance SKU, ~0.6x life). Hierarchical widths: port >= 3 mm, L1 >= 1 mm, L2 >= 0.3 mm, channel 0.15 mm,
each stage > 2x the next. Integrated screen >= 10 cm2 pleated or full-plate, clean dP < 0.5 kPa, alarm at 3x; 5 % bleed
from each slot dead-end through a >= 0.6 mm orifice (+0.4 K); keep port-adjacent channels and slot ends outside the die
(a blocked 4 mm cluster is +17 K at 128 W/cm2 regardless of architecture). All-Cu wetted path, Ni only where the TIM
needs it, no Al in the loop, ISO-cleanliness flush, dP monitoring port, reverse-flow tolerant.

**Header sizing (maldistribution).** Branch dP at design flow >= 6x the header-inlet dynamic head (U/CC) and >= 15x the
slot-entry dynamic head for centre-fed slots (Z-type needs 2-3x more); check at maximum rated flow. Velocity caps at
18 LPM: ports <= 1.5 m/s (>= 16 mm bore), headers <= 1.0 m/s, slot entry <= 0.5 m/s, descent between fins <= 0.5 m/s.
Outlet header 1.5-2x inlet area. Centre-feed and centre-collect every slot at mid-length (CC); never feed an L2 slot
from one end only; do not rely on taper (< 0.1 change for U/C/CC). Manifold block adds ~25 mm; the plate is ~30 mm thick.

**Flow length, pitch, metering.** 4 mm flow length (8 mm slot pitch) is the hydraulic optimum: channel friction scales
L^2 while Nu (entrance dominated, x* invariant) does not. Slot pitch <= 4x (base + fin) thickness so the 12.5 K fin-side
sawtooth reaches the case at < 0.5 K (1 mm base attenuates x25 at 4 mm period). When channel friction < 2 kPa, add an
orifice comb (>= 0.4-0.5 mm holes, W/d > 4, at the slot top so the jet decays over the 8 mm slot depth) to bring the
branch to >= 2.2 kPa. Counter-flow interdigitation is not worth building (<= 0.25 K; fin-scale costs +0.4 K via fin
recuperation).

**Base and construction.** 1.0 mm as-bonded / 0.8 mm minimum finished under the die, **only as a tied sandwich**: every
fin tip brazed or diffusion-bonded to the manifold web (>= 50 % bonded area; >= 30 % still SF 2.8 at 1.5 MPa burst with
Kt 2.5). Then pressure sets no limit (tie stress 2p = 3 MPa at burst), the perimeter land (<= 4 mm unsupported, or
stepped to 1.5-2 mm) governs at SF 5.8, pressure bow is zero (uniform BLT, a thermal benefit in itself), mount + thermal
bow over a 50 mm die is 4-25 + 6 um vs 13-77 + 19 um for the skived plate, and the stack is 24x stiffer and 0.2 kg
lighter. Design to annealed OFHC (70 MPa yield); finish-machine after bonding to <= 15-25 um flatness; move bolt bearing
toward the die edge; qualify with burst >= 4.5 MPa and >= 1000 power cycles (11 MPa thermal fatigue amplitude, SF ~6).
With 2 mm fins the core shear knock-down across fins rises (G_c ~ 1/H^2); re-check stiffness but the margin is large.

**Zoning.** Zone the manifold to heat, not area: die block >= 85-90 % of flow (2.5-3x average per area, gain saturates
there), HBM columns 0.3-0.5x, unheated area no slots. Implement by slot pitch (V'' ~ 1/L^2) or slot width/orifices at
fixed pitch; verify per-zone flow by test. Never route fluid over HBM after a die. Base 1.0 mm under dies (each extra mm
is +9 K at 350 W/cm2; spreading does not help a 26 x 33 mm source). Stepped Cu pedestal to the HBM plane within
0.05-0.1 mm, 0.05-0.1 mm compliant TIM. Specify the across-die case gradient: 6-8 K zoned HMMC vs 22-30 K split-flow.

**TIM by tier.** Tier 1 drop-in (lidded, serviceable): PCM pad (0.055) at 20-30 psi, plate flatness <= 30 um, package
gap <= 50 um hot; never grease on 100+ mm lids (its bow/ageing tails produced the benchmark's 10 K plate-to-plate
spread). Tier 2 OEM co-design: liquid metal 0.015 on 3-5 um electrolytic Ni, no Au, dam, 20-30 um BLT, Ni-finished lid,
no Al anywhere; sealed-FRU alternative indium pre-form. Tier 3 chip co-design: same core as a stepped pedestal on bare
die through liquid metal (junction-to-inlet 0.14 vs 0.28 cm2K/W, -28 K at 350 W/cm2); soldered micro-channel lid only in
CuW/CuMo/Si. Rule: R'' <= 0.02 cm2K/W above 200 W/cm2; Ni t/k <= 0.001 cm2K/W; retention 10-20 psi.

**Two-phase verdict: not in the baseline.** At the Tsat (60 C) a 45 C facility loop forces, a refrigerant HMMC is 6-14 K
hotter than the single-phase HMMC with liquid metal; parity needs Tsat 55 C (70 % more facility flow) plus an enhanced
boiling surface; boiling h in 100 um channels (10-25 kW/m2K) is no better than laminar PG25. Add 10 bar containment,
Ledinegg/vapour-backflow instability across 29,000 parallel segments, 1.4-1.6x dryout margin, 259 LPM of mixture per
plate, refrigerant CDUs incompatible with the PG25 loops operators are installing, and PFAS/F-gas exposure. Gate it on:
PFAS outcome leaving a 10-year window, facility water <= 40 C or 55-60 C heat reuse, and >= 300-400 W/cm2 over large areas.

**Modelling rules.** Darcy friction; isothermal caloric for cell lengths < ~10 mm; h_eff beyond ~250 kW/m2K buys little
at 1.2 LPM/kW because NTU > 2.4 saturates the fluid; long-wave flow uniformity is the hot-spot lever (+/-10 % = 1.3 K,
+/-20 % = 2.3 K, alternating patterns harmless); TIM bond-line (+/-10 um = +/-4 K with paste) is the largest remaining
hot-spot term for any pasted plate.

## 3. What undermines the concept, and what to change

1. **The headline 19.8-22 K numbers were built on channels we cannot deploy.** Fouling forces 0.15 mm gaps for a
   10-year product; convection rises from 5.4 to 10.1 K. Combined with the isothermal caloric penalty (+1.3 K) the
   drop-in HMMC with PCM is **28 K average, not 20-22 K**. Change: adopt the robust core as the product baseline, keep
   0.10 mm as a filtration-gated performance SKU, delete 0.05-0.075 mm from the roadmap. The manifold (short flow length,
   fresh fluid everywhere) is what delivers the win, not the sub-0.1 mm channel.
2. **With the same paste as CoolIT the mean margin is thin: 30.0 vs 34.5 K (-13 %)**, because the paste term (9 K) is now
   the largest after convection. The honest like-for-like claim is -4.5 K mean / -9 K max. Change: the product story must
   include the interface, and it legitimately can: the tied sandwich has zero pressure bow and 3x less mount/thermal bow,
   which is what lets a PCM pad or liquid metal hold its datasheet value. Lead with PCM (Tier 1) and liquid metal (Tier 2).
3. **The manifold as first specified does not work** (9 m/s slots, 43 kPa dynamic head against a 0.7 kPa branch, flow
   reversal). The fix costs packaging, not performance: ~10x the manifold cross-section, ~25 mm of header stack, 16 mm
   ports, centre-fed/centre-collected headers, and an orifice comb once the channels are widened. The architecture must
   carry a ~30 mm plate height and a UQD12-class coupling spec.
4. **At the 2027-28 reticle-die regime (350 W/cm2) the robust core does not reach T_case <= 85 C with liquid metal
   (93 C).** The performance core does (84 C), the fine core would (80 C) but is not deployable. Change: for the
   high-flux product, specify 25 um absolute loop filtration and the 0.10 mm core over the die zone only (the HBM and
   margin zones stay at 0.15 mm), or go direct-to-die (removing lid + TIM1 is worth ~28 K at the junction at 350 W/cm2,
   more than any fin refinement). Even the robust core beats the split-flow plate by 28-40 K at the hot die.
5. **The reconstruction of the benchmark is uncertain in CoolIT's favour.** Their fin pitch is a guess (dP 17-42 kPa);
   their real plate must have tied fins or posts (a free 2 mm base / 3 mm cover cannot pass 1.5 MPa over 108 mm), so
   their base is probably thicker than our 2 mm, and the 34.4 K may contain more TIM scatter than we assign. None of this
   changes the ranking; it widens the CoolIT-like band, not the HMMC band.
6. **Flow uniformity is an assumption until measured**: the +/-10 % that gives the 1.5 K hot spot depends on momentum
   coefficients (theta_c 1-2.5 spans global 1.06-1.15). A water-table or CFD test of one slot pair is the cheapest
   single experiment in the programme. Low channel velocity (0.08 m/s) means no self-cleaning; the plate's life is a
   function of loop cleanliness the product does not control, so the integrated screen is non-negotiable.
7. **Two-phase and counter-flow interdigitation are not upgrades**; both are removed from the baseline (see rules).

## 4. Updated targets to claim vs CoolIT (15 kW, 18 LPM PG25, 45 C inlet, 117 cm2)

Conservative = Tier 1 drop-in (robust core, PCM) at the P90 of the Monte Carlo; nominal = its median; stretch = Tier 2
liquid metal on the robust core, with the performance core (25 um loops) in brackets.

| metric | CoolIT 15 kW | conservative | nominal | stretch |
|---|---|---|---|---|
| average case-to-inlet dT | 34.4 K (measured) | <= 32 K (-7 %) | 28 K (-19 %) | 23 K (-33 %) [20 K, -41 %] |
| maximum case-to-inlet dT | 44.2 K (measured) | <= 35 K (-21 %) | 31 K (-30 %) | 25 K (-43 %) [22.5 K, -49 %] |
| T_case,max at 15 kW | 89.2 C | <= 80 C | 76 C | 70 C [67.5 C] |
| same-paste like-for-like average | 34.4 K | <= 34 K | 30 K (-13 %) | 26.5 K at equal pump power |
| unit resistance R'' (avg) | 0.269 cm2K/W | <= 0.25 | 0.219 | 0.179 [0.158] |
| flow-driven hot spot (max - avg) | 8.8 K systematic (9.8 total) | <= 2.5 K (+/-20 % verified) | 1.5 K (+/-10 %) | 0.7 K (global 1.10 measured) |
| plate dP port-to-port, 18 LPM | undisclosed; est. 22 kPa (17-42) | <= 10 kPa | 5 kPa | 4 kPa (20 mm ports) |
| hydraulic pumping power, 18 LPM | ~6.5 W est. | <= 3 W | 1.5 W | 1.2 W |
| Q capacity, T_case,max <= 85 C, 1.2 LPM/kW | ~13 kW (15 kW runs at 89 C) | >= 18 kW | 21.5 kW | 30 kW [38 kW] |
| reticle die 350 W/cm2, T_case,max (zoned, real package) | ~134 C (paste) | 107 C (PCM) | 93 C (LM) | 84 C [LM, 0.10 mm core]; ~80 C direct-to-die |
| flow at equal thermal performance | 18 LPM | <= 9 LPM | 7 LPM (0.2 W) | 6 LPM |
| service life vs skived plate (50 um abs screen) | 1.0x (10 y ref.) | >= 0.6x | 1.0x | 1.2x behind 25 um |

Claims to avoid: anything that depends on 0.05-0.075 mm channels; "< 10 % flow non-uniformity" without tying it to
18 LPM or the orifice variant; any dP figure that omits the quick disconnects; any 350 W/cm2 figure without zoning.

## 5. Verification before these targets go external

CFD of the slot-to-channel turn; water-table test of one slot pair (theta_c); fouling test of a 0.15 mm core behind a
50 um absolute screen with ISO-4406 dosed PG25; burst >= 4.5 MPa plus acoustic microscopy of the fin-tip bond; 1000 power
cycles; ASTM D5470 for PCM and liquid metal, BOL and post-cycling; re-verify the recalled literature values (25 um GB200
guidance, ASHRAE particulate limit, UQD Cv, OCP burst envelope, PCM ageing) that no report could fetch this run.
