# How cold-plate performance is measured and fairly compared: a benchmark protocol to beat the CoolIT 15 kW cold plate on a level field

Prepared 2026-10-13 for the cooling-architecture programme. Angle: metrics, test vehicles, measurement methods, normalisation rules and a concrete apples-to-apples protocol against the CoolIT 15 kW tech brief (June 2026).

## 0. Method and provenance (read first)

- **No live web searches could be run by this agent.** The per-turn WebSearch budget (200 calls, shared by all agents in this workflow) was already exhausted when this task started; all 10 queries issued were refused. WebFetch and curl are network-blocked in this container (one WebFetch attempt to coolitsystems.com failed on DNS; not retried).
- Evidence is therefore tagged:
  - **[Brief]** the CoolIT 15 kW tech brief (local extract `appendix/pdf/brief.txt`, read in full).
  - **[Sib]** a number found *with a URL* by a sibling research agent earlier in this run (files `coolit-briefs-numbers.md`, `coolit-products.md`, `competitors-singlephase.md`, `competitors-advanced.md`, `chip-roadmap-requirements.md`, `standards-reliability.md`, `power-electronics.md` in this directory; ~90 searches between them, all from search-result extracts, not full page reads). The URL is repeated in the Sources section.
  - **[Model]** sibling first-principles models in `appendix/model_output.md` and `appendix/physics/*.md` (1-D network, 2-D/3-D conduction, manifold network); treat as +/-25-30 %.
  - **[Calc]** arithmetic done here (`metrics_calc.py` in this directory).
  - **[KB-H/M/L]** this agent's background knowledge (training data to mid-2026), high / medium / low confidence; **every [KB] item must be verified against the primary document before it enters a test specification.**
- Vendor claims are marked (V); standards / peer-reviewed / independent data (I); derived numbers (D).

## 1. What CoolIT actually measured, and what the brief does not define

| Quantity | Value | Comment | Source |
|---|---|---|---|
| Heat load | 15,000 W on 4 ceramic heaters "simulating GPU and HBM zones" | per-heater power split not stated | [Brief] |
| Samples | 3 cold plates, 8 thermocouples each, "placed directly at the heater surface" | TC positions, groove method, bead type not stated | [Brief] |
| Coolant / flow | "standard water-glycol", 1.2 LPM/kW = 18 LPM | glycol fraction not stated (PG25 assumed) | [Brief] |
| Inlet | 45 C | outlet not stated | [Brief] |
| Result | dT(case - inlet) averaged over columns and rows = **34.4 K**; plate averages 32.5 / 35.2 / 35.6 K; 24 readings 26.8-44.2 K | "average Tcase ~80 C" | [Brief] |
| Derived mean R | 34.4 / 15,000 = **0.00229 K/W** (2.29 mK/W) | | [Calc] |
| Derived worst-TC R | 44.2 / 15,000 = **0.00295 K/W** | Tcase ~89 C at that point | [Calc] |
| Pressure drop | **not disclosed** | 4 kW plate: 8 psi (55 kPa) full loop incl. fittings and QDs at ~6 LPM | [Brief]; [Sib] 4 kW brief |
| Footprint / heated area | **not disclosed** | no cm2-K/W or W/cm2 can be formed | [Brief] |
| TIM | "standard thermal paste" | type, bond line, pressure not stated | [Brief] |
| Heat capture | not stated for 15 kW (4 kW plate: 93.4-97.3 %) | denominator of R is nominal electrical power | [Sib] 4 kW brief |

Two framing facts matter for a level-field comparison:

1. **CoolIT's two headline resistances are on different bases.** The 4 kW plate (March 2025) is quoted as "Tr < 0.009 C/W, maximum case temperature to fluid inlet, TIM included" [Sib]; the 15 kW brief leads with the *average* of 24 TCs (0.00229 K/W). On the same max-case basis the 15 kW plate is 0.00295 K/W. Any comparison must state which basis is used.
2. **CoolIT is now the primary author of the OCP Single-Phase Direct-to-Chip Cold Plate Test Specification v1.0.0 (Oct 2026)** [Sib], i.e. it is writing the yardstick: R = (Tcase - Tinlet)/P at multiple flows with a recommended TIM, dP at 45 +/- 2 C at >= 6 flow points from 25 % to 150 % of rated flow, burst (example > 20 bar), helium leak <= 1e-5 mbar-L/s, thermal cycling 10-65 C operating and -40/+70 C storage. The brief itself is *not yet* in that format (single flow point, no dP, no dP curve). Publishing our plate in full OCP v1.0.0 format is a differentiator before any thermal number is compared.

## 2. Thermal-resistance definitions and how they are (mis)compared

### 2.1 The definitions

| Symbol | Definition | Units | Who uses it | Notes |
|---|---|---|---|---|
| R_ca-in (case-to-inlet) | (T_case - T_inlet) / Q | K/W | CoolIT (both briefs), OCP test spec, OCP OAI guideline | includes TIM, base, fins, convection **and** the caloric (bulk fluid) rise; depends on flow rate and heated area |
| R_ca-mean | (T_case - T_fluid,mean) / Q, T_mean = (T_in + T_out)/2 | K/W | heat-exchanger literature, many papers | removes half the caloric term; still flow dependent |
| R_ca-out | (T_case - T_outlet) / Q | K/W | rarely | the "LMTD-free" floor; useful to isolate plate-intrinsic performance |
| R'' (unit / area-specific) | R x A_heated | cm2-K/W (= 1e-4 m2-K/W) | Mikros, PKU, two-phase vendors, literature | the only basis that transfers across footprints; needs a stated area |
| R_jc, R_ja, R_jf | junction-to-case / ambient / fluid | K/W | silicon vendors, JetCool datasheets (R_jf) | adds die + lid + TIM1; measured by JEDEC JESD51 electrical test methods on real silicon, not on a TTV |
| theta_JC per JESD51-14 | transient dual-interface junction-to-case | K/W | package vendors | not applicable to a cold plate test; quoted here only to avoid confusion [KB-H] |

**Caloric term.** R_ca-in = R_ca-mean + 1/(2 m cp) for a uniformly heated single pass (and R_ca-mean + (1/(1-e^-NTU) - 1/NTU - 1/2) x dT_out/Q correction for an isothermal-wall manifold plate; [Model] hotspot-smoothing). At the benchmark point 1/(m cp) = 0.84 mK/W, so **0.42 mK/W of CoolIT's 2.29 mK/W (18 %) is fluid heating to the mean, and 0.84 mK/W (37 %) to the outlet** [Calc]. This term is set by flow rate and fluid alone; no fin geometry can remove it. It is why LPM/kW must be fixed before any R is compared.

### 2.2 Reconciling "0.009 C/W at 4 kW" with "34.4 K at 15 kW"

| Plate | Q | Basis | R (K/W) | Flow | Area | R'' (cm2-K/W) | Source |
|---|---|---|---|---|---|---|---|
| 4 kW (Mar 2025) | 4,000 W | max TC, TIM incl. | < 0.009 (dT_max < 36 K) | 6.06 LPM = 1.5 LPM/kW | 50 x 50 mm = 25 cm2 (160 W/cm2) (D); Tom's Hardware "shy of 200 W/cm2" | <= 0.225 (max basis) | [Sib] 4 kW brief, DCD, Tom's Hardware |
| 15 kW (Jun 2026) | 15,000 W | mean of 24 TCs | 0.00229 | 18 LPM = 1.2 LPM/kW | undisclosed | 0.138-0.344 for 60-150 cm2 | [Brief]; [Calc] |
| 15 kW | 15,000 W | max TC | 0.00295 | same | undisclosed | 0.177-0.442 for 60-150 cm2 | [Calc] |

Absolute K/W falls almost in proportion to power because CoolIT scaled area and flow by ~3.75x while holding dT at ~35 K (Tcase ~80 C at 45 C inlet). The 15 kW number is therefore a **scaling demonstration, not evidence of a lower area-specific resistance**; on a max-case basis and at a plausible 80-117 cm2 heated area it is 0.24-0.35 cm2-K/W, i.e. *no better* than the 4 kW plate's <= 0.225 cm2-K/W [Calc]. The sibling 1-D model reproduces 34.4 K with a skived split-flow plate of 117 cm2 (108 x 108 mm, 128 W/cm2) with budget caloric 6.3 | TIM 8.9 | base 6.5 | convection 12.6 K [Model].

### 2.3 Influence of footprint and heater count

- **Footprint.** For a fixed R'', R scales as 1/A. Quoting K/W without area lets a larger plate look better; quoting cm2-K/W without stating whether A is die area, heater area or plate area does the same in reverse. Rule: report R (K/W) **and** R'' with A_heated explicitly, and report q'' = Q/A_heated.
- **Heater count / power split.** CoolIT averages 8 TCs with equal weight regardless of which heater (GPU or HBM zone) they sit on. With unequal zone fluxes an unweighted mean under-represents the hot zone. The position means (31.3, 32.7, 36.0, 37.6, 43.2, 32.6, 30.8, 31.0 K) show TC5 is +8.8 K above the grand mean on all three plates (systematic, a flow-exit or high-flux zone), while TC8 varies 27.6-37.7 K between plates (assembly/TIM scatter, residual sd ~2.5 K) [Calc]; [Model]. Rule: report the **max TC**, the **power-weighted mean**, and the per-position plate-to-plate sd separately.
- **Heater size vs die size.** A ceramic heater of 20-30 cm2 at ~130 W/cm2 does not reproduce a reticle die at 300-400 W/cm2: TIM, base and convection terms scale with local flux, so the same plate that gives 34 K on a uniform TTV gives 80-93 K at a 350 W/cm2 die [Model] nonuniform-heatmap. A fair benchmark needs both a "CoolIT-equivalent" uniform TTV and a realistic die/HBM TTV (Section 9).

## 3. Thermal test vehicles (TTVs)

| TTV type | What it is | Strengths | Weaknesses | Availability / source |
|---|---|---|---|---|
| NVIDIA TTV (HGX / GB200 / GB300 class) | package-form-factor heater with embedded sensors supplied to cold-plate RVL partners | matches package size, lid, mounting load, HBM/GPU split | **NDA; no public spec**; secondary sources conflict on NVIDIA's plate R / dP requirements (0.6-1.6 LPM/kW, 12-150 kPa) [Sib] | existence [KB-M]; conditions [Sib] chip-roadmap |
| Intel TTV (Xeon sockets) | socketed heater package with on-die RTD/diode equivalents used to validate thermal solutions against TMSDG Tcase limits | standardised Tcase thermocouple method (groove in IHS) | CPU footprints only (~ 50-80 cm2), fluxes < 100 W/cm2 | [KB-M]; Intel TMSDG documents (pull directly) |
| Custom ceramic heaters (CoolIT 15 kW TTV; CoolIT 4 kW TTV) | AlN/alumina resistive heaters, 4 zones, 15 kW total; built in-house at Liquid Lab | any power; cheap; durable | uniform flux per zone; no lid warpage; no real TIM1; heater-to-TC placement defines "case" | [Brief]; [Sib] 4 kW brief |
| Accelsius / two-phase TTVs | 4,500 W per socket TTV (stopped at infrastructure limit) | shows multi-kW capability | no temperature data published | [Sib] competitors-advanced |
| Academic TTVs | ORNL 75 x 75 mm, 1 kW (17.8 W/cm2) with TIM; PKU silicon chips to 3,000 W/cm2 | peer-reviewed, dP reported | far from GPU conditions | [Sib] competitors-singlephase (IJHMT 2025; Nature Electronics 2025) |
| Real silicon (JetCool H100, Accelsius B200, ToneCooling GB300) | production GPU with on-die sensors | junction temperature, real workload | R_jf not R_ca; TIM1 + lid included; not reproducible across labs | [Sib] |

Requirements for *our* TTV, derived from the above: (1) a 4-zone ceramic TTV that reproduces CoolIT's conditions exactly (uniform ~130 W/cm2, 15 kW, 8 TC positions); (2) a second "silicon-like" TTV with 4 die heaters at 300-400 W/cm2 plus 16 HBM heaters 0.3-0.5 mm lower, so that zoning, pedestal and TIM claims can be tested [Model]; (3) embedded sensors at known depth below the contact surface with a documented extrapolation to the surface; (4) guard heating or insulation so that heat capture >= 98 % (the 4 kW brief tested "without convection barrier or insulation" and captured only 93-97 % [Sib], i.e. up to 7 % of the denominator was lost to air, flattering R); (5) a measured per-zone power so that a power-weighted mean can be formed.

## 4. Case-temperature measurement

| Method | Standard / practice | Typical uncertainty | Notes |
|---|---|---|---|
| Thermocouple in a groove at the contact surface | Intel/AMD Tcase method: ~0.5-0.6 mm groove in the IHS, 36 AWG Type T bead, thermally conductive epoxy, bead flush with surface [KB-M] | +/-0.5 K (Type T special limits, calibrated +/-0.2 K) | the groove and bead perturb the TIM locally; bead depth of 0.3 mm in copper at 130 W/cm2 is ~0.1 K, in ceramic (k ~ 20-170 W/mK) up to 0.2-2 K [Calc, KB] |
| Embedded RTD / thin-film sensor in heater | custom TTVs | +/-0.1-0.3 K | depth correction required; best reproducibility |
| On-die diode / electrical test method | JEDEC JESD51-1 (junction), JESD51-14 (theta_JC, transient dual interface) [KB-H] | +/-1-2 K | gives T_j, not T_case; only on real silicon |
| IR thermography | n/a under a cold plate | - | only for open-face heater characterisation |
| ASTM D5470 | TIM thermal impedance (steady-state, between two metre bars) [KB-H] | 5-10 % on R_TIM | the right way to quantify the paste term separately |

"Placed directly at the heater surface" [Brief] is ambiguous (in a groove in the heater face under the TIM, or in the plate base?). The OCP v1.0.0 spec defines "case" and the TC method [Sib] (exact text not retrieved); our report must state bead depth, groove geometry and the extrapolation used. **Uncertainty budget** for R = (T_case - T_in)/Q [Calc]: with u(T_case) = 0.5 K, u(T_in) = 0.3 K, u(Q) = 0.5 % the relative standard uncertainty is 1.8 % (3.5 % at k = 2) at dT = 34 K; with calibrated sensors (0.2 / 0.1 K) and 0.3 % power it is 0.7 % (1.4 % at k = 2), and 0.9 % (1.9 %) at a dT of 25 K. A claimed 5-10 % improvement over CoolIT is therefore resolvable only with calibrated sensors and >= 3 plates x >= 3 assemblies.

## 5. The thermal-paste bond line and its share

At heat flux q'' the TIM drop is q'' x R''_TIM. Reference impedances: Shin-Etsu X23-7921-5 grease 0.05 cm2-K/W at 25 um / 20 psi; X23-8117 0.061; Honeywell PTM7950 phase-change 0.04-0.08 cm2-K/W [Sib] coolit-briefs-numbers. Large packages warp 100-300 um, so field bond lines are thicker than datasheet [Sib] chip-roadmap.

| Heated area | R''_TIM = 0.03 | 0.05 | 0.10 cm2-K/W |
|---|---|---|---|
| 80 cm2 (188 W/cm2) | 5.6 K (16 % of 34.4) | 9.4 K (27 %) | 18.8 K (55 %) |
| 117 cm2 (128 W/cm2) | 3.8 K (11 %) | 6.4 K (19 %) | 12.8 K (37 %) |
| 150 cm2 (100 W/cm2) | 3.0 K (9 %) | 5.0 K (15 %) | 10.0 K (29 %) |

[Calc]. Because the whole budget is 34.4 K of which ~6 K is fluid rise to the mean, CoolIT's paste must be <= ~0.1 cm2-K/W effective, and plausibly 20-40 % of the stack. The 10.1 K plate-to-plate difference at TC8 (37.7 vs 27.6 / 27.7 K) is consistent with a ~10-20 um bond-line difference of a 3 W/mK paste at ~130 W/cm2 (10 um = ~4 K) [Model] hotspot-smoothing. Protocol consequences: (a) name the TIM and measure its impedance per ASTM D5470 at the actual clamping pressure; (b) measure bond-line thickness post-test (shim or cross-section); (c) run a **TIM-less reference** (indium foil or liquid metal of known impedance <= 0.02 cm2-K/W) to separate plate from interface; (d) report R both with the OCP "recommended TIM" and with our best interface, labelled.

## 6. Flow-rate normalisation and the caloric rise

### 6.1 Why 1.2 LPM/kW

| Convention | Value | Source |
|---|---|---|
| CoolIT 15 kW brief (2026) | 1.2 LPM/kW, "industry standard flow rate for AI systems" | [Brief] |
| CoolIT 4 kW brief / PR (2025) | 1.5 LPM/kW, "semiconductor industry's recommended flow rate" | [Sib] |
| Electronics Cooling (Jun 2025) | 1.2 LPM/kW at 45 C is "a common industry standard that many CDUs available today can meet"; ~18 psi rack budget | [Sib] |
| OCP L-L CDU test methodology | CDUs rated at 1.5 LPM/kW, >= 40 psi TCS head | [Sib] |
| OCP OAI liquid-cooling guideline (Mar 2023) | 1-2 LPM per 1 kW OAM; recommended coolant rise 7.5-12 C | [Sib] |
| NVIDIA GB200 NVL72 (QCT whitepaper; GTC keynote) | 45 C max supply / 65 C max return (= 20 K = 0.75 LPM/kW); ~120-130 LPM per ~120 kW rack (~1.0 LPM/kW) | [Sib] |
| CoolIT CHx2000 CDU rating | 2,000 kW at 5 C approach and 1.2 LPM/kW | [Sib] coolit-products |

No OCP, ASHRAE or NVIDIA document codifies 1.2 LPM/kW; it is a CDU-capability convention that CoolIT itself moved to from 1.5 LPM/kW between 2025 and 2026 [Sib]. Lower LPM/kW is *harder* for the plate (bigger caloric rise) but cheaper for the facility (smaller CDUs, manifolds, QDs, pumps). A plate specified at 0.75-1.0 LPM/kW (NVIDIA's envelope) with the same Tcase beats one specified at 1.2 LPM/kW on the metric hyperscalers pay for.

### 6.2 Computed caloric rise, PG25 at 45 C inlet, 15 kW [Calc]

Energy balance: dT_bulk = Q / (m cp), m = rho x V. Properties used: PG25 at 45 C rho = 1010 kg/m3, cp = 3,930 J/kg-K (Dow DOWFROST LC-25 class; [Sib] ChemPoint page gives cp 3.94 kJ/kg-K at 50 C; other values [KB-M], +/-3 %).

| Specific flow | Volume flow | Fluid | m (kg/s) | m cp (W/K) | 1/(m cp) (mK/W) | dT_bulk (K) | T_out (C) | T_mean (C) |
|---|---|---|---|---|---|---|---|---|
| 0.75 LPM/kW | 11.25 LPM | PG25 | 0.189 | 744 | 1.34 | **20.2** | 65.2 | 55.1 |
| 1.0 | 15.0 | PG25 | 0.253 | 992 | 1.01 | **15.1** | 60.1 | 52.6 |
| **1.2 (benchmark)** | **18.0** | **PG25** | **0.303** | **1,191** | **0.84** | **12.6** | **57.6** | **51.3** |
| 1.2 | 18.0 | water | 0.297 | 1,241 | 0.81 | 12.1 | 57.1 | 51.0 |
| 1.5 | 22.5 | PG25 | 0.379 | 1,488 | 0.67 | 10.1 | 55.1 | 50.0 |
| 2.0 | 30.0 | PG25 | 0.505 | 1,985 | 0.50 | 7.6 | 52.6 | 48.8 |

At the benchmark point: **15,000 W / (0.303 kg/s x 3,930 J/kg-K) = 12.6 K**, outlet 57.6 C, mean fluid 51.3 C. Of CoolIT's 34.4 K, 12.6 K (37 %) is inlet-to-outlet fluid heating and 6.3 K (18 %) inlet-to-mean. The case-to-mean-fluid resistance is 1.87 mK/W and the case-to-outlet floor 1.45 mK/W [Calc]. The 12.6 K rise is at the top of the OCP OAI 7.5-12 C window; at NVIDIA's 0.75 LPM/kW the rise is 20 K and the outlet 65 C, exactly NVIDIA's return limit.

## 7. Pressure drop, pumping power, COP and the Pareto

### 7.1 Measurement rules

- OCP v1.0.0: dP at 45 +/- 2 C coolant temperature, >= 6 flow points, 25-150 % of rated flow [Sib]. Temperature matters because the plate is laminar (Re ~ 15-200 in 0.1-0.2 mm gaps [Model]) and laminar dP is proportional to viscosity: PG25 viscosity falls from ~2.6 mPa-s at 25 C to ~1.45 mPa-s at 45 C, so **a dP measured at 25 C is ~1.8x the 45 C value** [Calc, KB-M]. Report the fluid temperature at which dP was taken, and use the mean fluid temperature, not the inlet, when correlating.
- Define the boundary: plate-only (pressure taps at the plate ports, port-loss corrected), plate + hoses, plate + UQD pair. CoolIT's only published dP is 8 psi "full loop incl. fittings and QDs" for the 4 kW plate [Sib]; a plate-only number would be lower. Vendor GB200/GB300 plates quote < 20 kPa at 1.8 LPM, 12 kPa at 1.7 LPM, 35 kPa at 2.5 LPM, basis unstated [Sib].
- Report dP vs flow as a curve (laminar: linear, plus quadratic port/manifold losses), fit dP = a V + b V^2, and quote a at 45 C.

### 7.2 Pumping power and COP at 18 LPM (3.0e-4 m3/s) [Calc]

| Plate dP | psi | Hydraulic power | COP_hyd = Q / P_hyd | Electrical at 35 % pump efficiency | COP_elec | % of 15 kW |
|---|---|---|---|---|---|---|
| 10 kPa | 1.5 | 3.0 W | 5,000 | 8.6 W | 1,750 | 0.06 |
| 20 kPa | 2.9 | 6.0 W | 2,500 | 17 W | 875 | 0.11 |
| 35 kPa | 5.1 | 10.5 W | 1,430 | 30 W | 500 | 0.20 |
| 55 kPa | 8.0 | 16.5 W | 910 | 47 W | 318 | 0.31 |
| 100 kPa | 14.5 | 30 W | 500 | 86 W | 175 | 0.57 |
| 150 kPa | 21.8 | 45 W | 333 | 129 W | 117 | 0.86 |

The plate's pumping power is < 1 % of the load in every case; the real cost of dP is **system-level**: CDU secondary head (CoolIT CHx1000/1500/2000: 35/44/53 psi; Google Deschutes 80 psi; OCP allows components to see 100 psi [Sib]), manifold and QD sizing, and compatibility with negative-pressure loops (Chilldyne-type, plate + tray must fit in a few tens of kPa [Sib]). A 2 MW CDU at 53 psi and ~2,400 LPM is ~15 kW hydraulic [Sib] chip-roadmap. The right system metric is therefore **plate dP at a fixed LPM/kW and 45 C**, not plate pumping watts.

### 7.3 The thermal-resistance vs pressure-drop Pareto

For a given fin technology, R falls and dP rises with flow; the design-space frontier is the curve R(dP) at fixed Q, A and T_in. Independent anchors on that frontier: Kisitu & Ortega (Villanova, InterPACK 2021) show geometrically identical split-flow and parallel-flow plates have **similar R but split-flow has significantly lower dP** (shorter path, half the per-channel flow) [Sib]; Fabric8/UIUC topology-optimised copper shows -32 % R at equal flow or -68 % dP at equal R vs pin fins (Cell Reports Physical Science 2026, GaN array) [Sib]; ORNL diamond pin-fin copper gives 6.9 K/kW incl. TIM at 1 kW and 9.0 kPa (IJHMT 2025) [Sib]; the sibling manifold-microchannel design reaches 24 K avg at 18 LPM and ~6 kPa, vs 34.5 K at ~9-19 kPa for the skived split-flow reconstruction [Model] (the manifold-maldistribution note corrects the split-flow dP to ~19 kPa after a friction-factor fix). The protocol must therefore report **R at three flows and dP at six flows** so the frontier, not a point, is compared; a plate wins if its curve lies below CoolIT's at every flow, or if it reaches CoolIT's 34.4 K at a lower LPM/kW.

## 8. Coolant properties and inlet-temperature effects

| Property | PG25 @ 25 C | PG25 @ 45 C | PG25 @ 51 C (benchmark mean) | Water @ 45 C | Effect on the test |
|---|---|---|---|---|---|
| Density rho (kg/m3) | ~1,021 | ~1,010 | ~1,007 | 990 | m for a given LPM |
| Specific heat cp (J/kg-K) | ~3,880 | ~3,930 | ~3,940 | 4,180 | caloric rise: PG25 +4 % vs water |
| Thermal conductivity k (W/m-K) | ~0.455 | ~0.475 | ~0.478 | 0.637 | laminar h = Nu k / D_h: PG25 h is ~25 % lower than water at the same geometry |
| Viscosity mu (mPa-s) | ~2.6 | ~1.45 | ~1.30 | 0.60 | laminar dP proportional to mu: PG25 ~2.4x water at 45 C; 25 C ~1.8x 45 C |
| Prandtl | ~22 | ~12 | ~11 | 3.9 | thermal entrance length x* shorter for PG25 -> developing-flow Nu enhancement larger |
| rho cp (kJ/m3-K) | 3,961 | 3,969 | 3,968 | 4,138 | volumetric heat capacity 4 % below water |

Values: cp at 50 C from Dow DOWFROST LC-25 via [Sib] ChemPoint page; remaining values [KB-M] (+/-3-5 %), to be replaced by the OCP PG25 base spec v1.0.0 tables [Sib URL] before publication. The sibling model gives water 1.4 K better than PG25 at the benchmark point (22.7 vs 24.1 K) [Model]. Rules: (1) test in **OCP PG25** (NVIDIA's fluid) and report DI water as a secondary curve; (2) hold inlet at 45.0 +/- 0.5 C and log outlet; (3) repeat at 25, 35 and 50 C inlet because R falls slightly with temperature (lower mu, higher k) and dP falls strongly; a plate that holds Tcase at 50 C inlet (W+) is worth a chiller to the operator [Sib] standards-reliability.

## 9. Uniformity, hot spots and transient response

### 9.1 Uniformity metrics on CoolIT's own data [Calc]

| Metric | Definition | CoolIT 15 kW value | Comment |
|---|---|---|---|
| U1 range | max - min over 8 TCs, per plate | 14.7 / 16.6 / 16.3 K | sensitive to one outlier (TC8 on plate 1) |
| U2 max-minus-mean | T_max - T_mean per plate | 9.0 / 9.0 / 8.4 K | the number that sets the Tcase ceiling; recommend as the headline uniformity KPI |
| U3 CoV | sd / mean per plate | 15.5 / 14.7 / 14.1 % | 5 K sd on a 34 K mean |
| U4 position spread | max - min of the 8 position means | 12.4 K (43.2 vs 30.8) | systematic design non-uniformity |
| U5 plate-to-plate repeatability | sd of plate means (n = 3); max spread at one position | 1.66 K; 10.1 K (TC8) | the 10 K is assembly/TIM, not flow design |

Decomposition [Model] hotspot-smoothing: TC5 is +8.8 K on all three plates (systematic), TC7 is -3.6 K; the location x plate residual sd is 2.5 K with a max residual of 8.6 K. A single-pass 54 mm split-flow ramp with entrance cooling at the centre reproduces 5.7 K (perfect distribution) to 8.4 K (+/-20 % channel maldistribution) of max-minus-mean, so most of CoolIT's spread is intrinsic to the architecture, and ~6 K of it is caloric gradient [Model]. Targets that would be unambiguous wins: U2 <= 4-6 K, U4 <= 6 K, U5 position max spread <= 3 K.

### 9.2 Hot-spot handling

A uniform TTV cannot test hot-spot capability. Proposal: a sub-heater of 4-8 cm2 at 3-4x the background flux (400-500 W/cm2 at 128 W/cm2 background), located (a) at the plate centre and (b) at a corner/outlet position, with a TC in each. KPI: local max-minus-mean and the local R'' = (T_hot - T_in)/q''_hot. Vendor references on this axis are unverified: CoolIT OMNI "> 300 W/cm2" (no conditions), Frore 600 W/cm2 at 40 C inlet, Mikros > 1 kW/cm2 at ~30 K and 20.7 kPa, PKU 1,000 W/cm2 at 65 K (0.065 cm2-K/W, peer-reviewed) [Sib].

### 9.3 Transient response

Order-of-magnitude: a 108 x 108 x 8 mm copper plate holds ~400 J/K, the fluid in it ~40 J/K, and the case-to-mean-fluid conductance at the benchmark point is ~530 W/K, so the plate's own time constant is ~0.8 s and fluid residence ~30 ms [Calc]; the TTV ceramic/copper stack and the loop reservoir (minutes) dominate the measured settling. AI training loads swing between idle and full power at 0.1-10 Hz [KB-M]; the relevant KPIs are (1) steady-state criterion (dT drift < 0.2 K over 10 min, used for every R point), (2) Tcase overshoot and 90 % settling time for a 50 -> 100 % power step, and (3) Tcase excursion amplitude under a 0.5 Hz 50/100 % square wave. Thermal cycling for TIM pump-out (OCP: 10-65 C operating cycles; re-measure R and dP afterwards, drift <= 5 % R, <= 10 % dP) is a reliability test, not a performance metric, but must be in the same report [Sib] OCP v1.0.0.

## 10. Standardised reporting and third-party validation

| Source of data | Independence | What it gives | Limits |
|---|---|---|---|
| CoolIT Liquid Lab (Calgary, Taipei; 6 MW rig, HALT, environmental chambers) | vendor | all CoolIT numbers | no independent validation of any CoolIT plate exists [Sib] |
| NVIDIA / Intel / AMD partner qualification | silicon vendor, NDA | pass/fail against package specs | results never public |
| JetCool "third-party" GPU test (unnamed lab) | vendor-reported | -25 % total R vs microchannel at 50 C PG25 | lab unnamed, PDF unreadable here [Sib] |
| Accelsius B200 benchmark (unnamed SI, Jul 2026) | SI-run, vendor-published | -9 C Tj vs single-phase at warm water | SI unnamed, baseline is a "factory" plate [Sib] |
| OCP Cold Plate Test Spec v1.0.0 (Oct 2026) and Cold Plate Development & Qualification white paper | industry consensus (CoolIT primary author) | the report format, test conditions, qualification matrix | full tables not retrieved; pull the PDF [Sib] |
| OCP OAI guideline (Mar 2023) | industry | 1 kW OAM reference: R_ca-in 0.015-0.016 K/W at high flow, PG25/DI, phase-change TIM | older, CPU/OAM scale [Sib] |
| University labs: Villanova (Ortega), UT Arlington (Agonafer), Binghamton ES2, Purdue (Garimella), Stanford, ORNL, PKU | peer-reviewed | geometry-level physics with dP | not at 15 kW; UTA/Binghamton named from [KB-M] |

Recommendation: run the protocol in-house, then commission a **named** university or national lab (ORNL already publishes copper cold-plate data with dP [Sib]) to repeat the headline point with its own TTV and sensors, and publish both in OCP v1.0.0 format.

## 11. Proposed apples-to-apples protocol vs the CoolIT 15 kW result

### 11.1 Two TTVs

**TTV-A "CoolIT-equivalent" (parity test).** 4 ceramic heaters in a 2 x 2 array on a 108 x 108 mm copper spreader (117 cm2, 128 W/cm2 at 15 kW; the sibling calibration [Model]; adjust if CoolIT's footprint becomes known), each heater individually powered and metered (+/-0.3 %), guard insulation to >= 98 % capture (verified by fluid-side calorimetry: Q_fluid = m cp dT_out must agree with electrical power within 3 %). 8 TCs in 0.5 mm grooves at the contact face at positions mirroring a 2 x 4 grid (one per heater half, so that centre, mid and edge/outlet locations are covered), plus 4 extra TCs at the geometric centre and the three corners. Bead depth and extrapolation documented. Lidded configuration (nickel-plated copper "lid" 2 mm, to carry a paste TIM) and flat-face configuration.

**TTV-B "Rubin-Ultra-like" (realism test).** Same base, 4 die heaters 26 x 33 mm at 300-400 W/cm2 (12-15 kW) and 16 HBM heaters 11 x 12 mm at 40-60 W/cm2, HBM top 0.4 mm below die top [Model] nonuniform-heatmap; one TC per die centre, one per die corner, one per HBM column; this is where zoning, pedestals and low-impedance TIMs show their value (model: 88.6 K hot-die dT for a CoolIT-like plate vs 36.5 K for a zoned manifold plate with liquid metal [Model]).

### 11.2 Test matrix

| Variable | Levels | Notes |
|---|---|---|
| Power | 5, 10, 15 kW on TTV-A; 10, 12.85, 15 kW on TTV-B | 15 kW is the comparison point; 20-30 kW stretch on TTV-A if the heaters allow |
| Specific flow | 0.5, 0.75, 1.0, **1.2**, 1.5 LPM/kW (R); 25-150 % of rated in >= 6 steps (dP) | 1.2 LPM/kW at 45 C is the CoolIT parity point; 0.75-1.0 is NVIDIA's envelope |
| Inlet | 25, 35, **45**, 50 C | dP corrected to 45 C mean-fluid viscosity |
| Coolant | OCP PG25 (primary); DI water (secondary) | log glycol fraction by refractometer |
| TIM | (i) OCP "recommended TIM"; (ii) a named standard paste at a measured BLT (e.g. Shin-Etsu X23-7921-5 class); (iii) best interface (liquid metal / indium); (iv) TIM-less reference on TTV-B bare dies | ASTM D5470 impedance of each at the clamping pressure used |
| Samples | >= 3 plates x >= 3 assemblies each (9 R values per point) | gives U5 and CpK |
| Transient | 50 -> 100 % step; 0.5 Hz square wave; 100 thermal cycles 10-65 C then re-test | per Section 9.3 |

### 11.3 Compact KPI set and "beat CoolIT" thresholds

| # | KPI | Definition | CoolIT 15 kW value | Threshold to claim a win |
|---|---|---|---|---|
| 1 | R_avg | mean (T_case - T_in)/Q, 8 TCs, 3 plates, 1.2 LPM/kW PG25 45 C, standard paste | 2.29 mK/W (34.4 K) | <= 1.8 mK/W (<= 27 K) |
| 2 | R_max | worst TC, same conditions | 2.95 mK/W (44.2 K) | <= 2.2 mK/W (<= 33 K) |
| 3 | R'' | R_max x A_heated, A stated | 0.24-0.35 cm2-K/W (area inferred) | <= 0.18 cm2-K/W with paste; <= 0.12 with liquid metal; <= 0.09 direct-to-die |
| 4 | U2 | T_max - T_mean per plate | 8.4-9.0 K | <= 6 K (uniform TTV); <= 8 K across dies on TTV-B |
| 5 | U5 | max plate-to-plate spread at a position; sd of plate means | 10.1 K; 1.66 K | <= 3 K; <= 1 K |
| 6 | dP_plate | plate-only at 1.2 LPM/kW, 45 C, PG25 | not disclosed (4 kW loop: 55 kPa at 6 LPM) | <= 35 kPa, and <= 25 kPa at 1.0 LPM/kW; publish the 6-point curve |
| 7 | Flow-equivalence | LPM/kW at which the plate reaches dT = 34.4 K avg | 1.2 by definition | <= 0.9 LPM/kW |
| 8 | Inlet headroom | inlet temperature at which T_case,max = 85 C at 15 kW, 1.2 LPM/kW | ~41 C (89 C max at 45 C inlet) (D) | >= 50 C |
| 9 | Heat capture | Q_fluid / Q_electrical | 4 kW plate 93-97 %; 15 kW not stated | >= 98 % stated with method |
| 10 | Hot-spot R'' | (T_hot - T_in)/q''_hot at 400-500 W/cm2 sub-heater | n/a | <= 0.12 cm2-K/W with paste |
| 11 | Transient | overshoot and 90 % settling for 50 -> 100 % step | n/a | overshoot <= 2 K; settling <= 10 s (plate-limited) |
| 12 | Post-cycling drift | R and dP change after 100 cycles 10-65 C | n/a | <= 5 % R, <= 10 % dP |

All KPIs reported with k = 2 uncertainty (target <= 2 % on R, <= 3 % on dP), fluid temperature for dP, TIM identity and BLT, heater map and per-heater power, and a statement of whether numbers are average or max basis. Two headline lines only: "R_max at 1.2 LPM/kW, 45 C, PG25, OCP TIM" and "dP_plate at the same point". Everything else is in the OCP-format annex.

### 11.4 Why this is level and still favourable

The parity test reproduces CoolIT's disclosed conditions exactly (same power, flow, inlet, paste class, 8-TC averaging), so the comparison is defensible even without CoolIT's undisclosed footprint; the flow sweep and dP curve expose what the brief withholds; and the realism TTV, hot-spot sub-heater, inlet sweep and repeatability KPIs test precisely the three places where the benchmark is weakest by CoolIT's own data: hot-spot spread (U2 ~9 K, U4 12.4 K), assembly scatter (10 K at TC8) and the undisclosed pressure drop.

## 12. Gaps / unknowns

1. **No live searches** were possible in this task; items tagged [KB] (PG25 property values except cp, Intel groove TC method, JESD51 scope, ASTM D5470, NVIDIA/Intel TTV existence and NDA status, pump efficiency, AI load transient frequencies, university lab names) must be verified against primary documents.
2. The OCP Cold Plate Test Spec v1.0.0 PDF (Oct 2026) was located by URL but its full text (definition of "case", TC method, recommended TIM, rated-flow definition, report template) was not read; the whole protocol in Section 11 should be re-aligned to it line by line.
3. CoolIT's 15 kW heated area, heater layout, per-heater power, TC positions, TIM and pressure drop remain undisclosed; the 117 cm2 / 128 W/cm2 calibration is a model inference (+/-25 %), and all R'' values for the benchmark are scenario-based.
4. Whether CoolIT's 8 TCs are in the heater face, in the TIM, or in the plate base changes the meaning of "case" by several K at 130 W/cm2; not clarified anywhere public.
5. PG25 property values at 45-51 C other than cp are from memory; the OCP PG25 base specification v1.0.0 tables should replace them.
6. The sibling dP reconstruction of the CoolIT-like plate changed from ~9 kPa to ~19 kPa after a friction-factor correction; CoolIT's real 15 kW dP could be anywhere from ~10 to > 50 kPa.
7. No public, named, independent laboratory has measured any CoolIT, JetCool, Accelsius or Frore plate; "third-party" claims are vendor-published with unnamed labs.
8. NVIDIA's plate-level R and dP requirements for GB300/Rubin are NDA; secondary sources conflict (0.6-1.6 LPM/kW; 12-150 kPa).
9. Transient KPIs (overshoot, settling) have no industry benchmark values; thresholds in Section 11.3 are proposals.
10. The 4 kW tech brief's R-vs-flow chart, inlet temperature and TTV heater size were never readable; the 93.4 % / 97.3 % capture rows come from index excerpts.

## Sources

CoolIT primary (via [Sib] coolit-briefs-numbers.md and coolit-products.md)
- 15 kW tech brief: local extract; page https://www.coolitsystems.com/resources/news/15kw-coldplate/ ; PR https://www.prnewswire.com/news-releases/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-roadmap-far-beyond-2030-302787344.html
- 4000 W Technical Brief R2 (14 Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf ; PR: https://www.prnewswire.com/news-releases/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership-302401512.html
- Coldplate technology page: https://www.coolitsystems.com/coldplate-technology/ ; OMNI: https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled
- Split-Flow brief: https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf
- Tom's Hardware state of play 2025 ("shy of 200 W/cm2"): https://www.tomshardware.com/pc-components/cooling/the-data-center-cooling-state-of-play-2025-liquid-cooling-is-on-the-rise-thermal-density-demands-skyrocket-in-ai-data-centers-and-tsmc-leads-with-direct-to-silicon-solutions
- DCD 15 kW: https://www.datacenterdynamics.com/en/news/coolit-designs-15kw-coldplate-to-future-proof-liquid-cooling-for-gpus/ ; Electronics360: https://electronics360.globalspec.com/article/23837/computex-2026-coolit-pushes-single-phase-dlc-to-15-kw
- CHx2000 CDU (1.2 LPM/kW rating, 53 psi): https://www.coolitsystems.com/cdu-product/chx2000/ ; CHx1000 (1.5 LPM/kW): https://www.hpcwire.com/2024/12/10/ai-performance-reliability-serviceability-with-coolits-chx1000-cdu/
- Liquid Lab / 6 MW rig: https://www.datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale

Standards and industry documents
- OCP Single-Phase Direct-to-Chip Cold Plate Test Specification v1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf and https://www.opencompute.org/documents/ocp-cold-plate-test-specification-v1-0-0-pdf-1/
- OCP Cold Plate Development and Qualification white paper: https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/
- OCP OAI System Liquid Cooling Guidelines (Mar 2023): https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/
- OCP L-L CDU Test Methodology and Performance Rating r1: https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- OCP PG25 base specification v1.0.0: https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/ ; PG25 Guidelines v1.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
- OCP Thermal Boundaries in AI Infrastructure (Oct 2026): https://www.opencompute.org/documents/white-paper-thermal-boundaries-in-ai-infrastructure/
- ASHRAE 5th-edition liquid classes (Upsite summary): https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/
- Electronics Cooling, Direct Liquid Cooling for High-Compute Servers (Jun 2025; 1.2 LPM/kW, 18 psi): https://www.electronics-cooling.com/2025/06/direct-liquid-cooling-for-high-compute-servers/
- QCT GB200 NVL72 whitepaper (45/65 C, ~130 LPM): https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf ; DCD GB200: https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus
- Google Deschutes CDU 80 psi: https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
- Schneider on CDU rating and filter dP: https://blog.se.com/datacenter/2025/12/16/account-for-filtering-too-beware-of-how-cdu-rating-capacity-is-specified/

Independent / peer-reviewed comparators
- Kisitu & Ortega, split-flow vs parallel microchannel models (InterPACK 2021): https://par.nsf.gov/biblio/10341820
- ORNL Cu/CuW diamond pin-fin plates, IJHMT 2025/26 (6.9 K/kW, 9.0 kPa): https://www.sciencedirect.com/science/article/pii/S0017931025014152 ; Electronics Cooling Apr 2026: https://www.electronics-cooling.com/2026/04/high-performance-copper-tungsten-cold-plates-for-direct-to-chip-single-phase-liquid-cooling/
- PKU jet-manifold microchannels, Nature Electronics 2025 (1,000 W/cm2 at 65 K): https://www.nature.com/articles/s41928-025-01449-4
- UIUC / Fabric8Labs topology-optimised copper plate (-32 % R / -68 % dP): https://mechse.illinois.edu/news/82871
- Bio-inspired manifold microchannel, Energy 2025 (0.0878 cm2-K/W, 25.2 kPa): https://www.sciencedirect.com/science/article/abs/pii/S0360544225049114
- Accelsius B200 independent benchmark (Jul 2026): https://www.businesswire.com/news/home/20260721991081/en/
- JetCool third-party testing: https://jetcool.com/post/third-party-testing-data/ ; RTX PRO 6000 datasheet (R_jf, PG25 40 C): https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
- Frore LiquidJet (600 W/cm2, 0.24 psi): https://www.froresystems.com/media-room/frore-systems-introduces-liquidjet-redefining-coldplates-for-ai-data-centers
- Mikros Normal Flow (0.02 cm2-K/W, 20.7 kPa at 1 kW/cm2): https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/
- Vendor GB200/GB300 plate figures (secondary): https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/
- TIM data: Shin-Etsu X23-7921-5 https://cdn.microsi.com/wp-content/uploads/2019/07/X23-7921-5-TDS-July-2019-.pdf ; Honeywell PTM7950 https://www.caplinq.com/ptm7950-most-thermally-conductive-phase-change-pad-with-very-low-thermal-impedance-that-works-in-vertical-applications-ptm7950.html
- PG25 (Dow DOWFROST LC-25) properties: https://www.chempoint.com/en-ca/products/dow/dowfrost-glycol-thermal-fluids/dowfrost-propylene-glycol-thermal-fluids/dowfrost-lc-25
- Chilldyne negative-pressure (dP constraint): https://www.storagereview.com/review/high-performance-leak-free-liquid-cooling-chilldynes-cdu-and-cold-plates-in-action
- ECPE AQG 324 (power-electronics qualification, for the SiC variant): https://www.ecpe.org (document named from [Sib] power-electronics.md; URL not verified)

Documents named from background knowledge (no URL verified this session; pull directly): JEDEC JESD51-1, JESD51-2, JESD51-14 (thermal measurement methods); ASTM D5470 (TIM thermal impedance); Intel Xeon Thermal Mechanical Specification and Design Guides (Tcase thermocouple groove method); NVIDIA MGX / HGX thermal test vehicle and liquid-cooling design guides (NDA); ASHRAE TC 9.9 Thermal Guidelines 5th ed. (2021) liquid-cooling chapter.

Local workflow files used: `appendix/pdf/brief.txt`; `appendix/model_output.md`; `appendix/physics/hotspot-smoothing.md`, `nonuniform-heatmap.md`, `manifold-maldistribution.md`; `appendix/research/{coolit-briefs-numbers, coolit-products, competitors-singlephase, competitors-advanced, chip-roadmap-requirements, standards-reliability, power-electronics}.md`; `appendix/research/metrics_calc.py` (this agent's arithmetic).
