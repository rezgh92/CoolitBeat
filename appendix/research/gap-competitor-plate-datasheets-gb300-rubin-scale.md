# Gap report: competitor GB300 / Rubin-class cold-plate datasheet numbers (R, flow, dP, price) and verification of the ToneCooling / FiberMall figures

Prepared 2026-10-13 for the "beat the CoolIT 15 kW cold plate" programme. Angle: what numeric thermal resistance, flow, pressure drop and price the volume incumbents (AVC, Cooler Master, Delta, Jentech, Auras) and challengers (Boyd, Mikros/Jabil, Wiwynn/Fabric8Labs, Motivair, Vertiv/CoolTera, JetCool) actually publish for GB200/GB300/Rubin-class plates, and whether the ToneCooling (0.013 K/W, 12 kPa) and FiberMall (< 0.03 K/W, < 20 kPa) figures are real datasheet values.

## 0. Method and an honest statement of what this session could and could not do

- **No live web search was possible.** All 14 planned queries (listed verbatim in Section 9) were refused because the per-turn WebSearch budget (200 calls, shared by every agent in this workflow) was already exhausted when this agent started. The single permitted WebFetch attempt (Boyd standard cold-plate datasheet PDF) failed on DNS, as the task warned. No workaround was attempted.
- What this report therefore does: (1) consolidates **every competitor plate number any sibling agent retrieved with a URL** into one table with a common basis; (2) runs **physics consistency checks** on the ToneCooling and FiberMall figures (caloric split, unit resistance at the known die areas, flow-normalisation to 1.0-1.5 LPM/kW); (3) **anchors the "conventional skived" unit-resistance band** from six independent directions so it is no longer a single ACT cut-sheet number; (4) states exactly which documents and queries close the remaining gap, and recommends the only method that reliably yields competitor R(flow)/dP(flow) curves (buy plates and test them under the OCP spec).
- Provenance tags: **[Sib]** = retrieved with URL by a sibling report in `appendix/research/` (URL repeated here); **[Brief]** = the local CoolIT 15 kW tech brief; **[M]** = sibling physics model (`appendix/physics/hydraulic-detail-output.txt`); **[D]** = derived in this report (`research/tools/competitor_normalise.py`); **[KB-x]** = author background knowledge, unverified this session (H/M/L confidence). V = vendor claim, I = independent/peer-reviewed, S = secondary (blog/analyst/press).

## 1. Headline answers

1. **No Group-A supplier (AVC, Cooler Master, Delta, Jentech, Auras) publishes any plate-level K/W, LPM or kPa figure for GB200/GB300/Rubin plates.** Every sibling sweep and this consolidation confirm it. Their numbers exist only inside NVIDIA's NDA thermal design guides and ODM qualification reports. Publicly, the only facts are market share (AVC ~40-50 % of GB200/GB300 plates), Group-A membership (Jentech, AVC, Cooler Master, Delta for Rubin) and ASP (~US$300 GB300, ~US$400 Rubin) [Sib].
2. **ToneCooling's 0.0130-0.0133 K/W at 1.7 LPM / 12.06 kPa / 1,067 W is physically plausible but is not evidence of an elite plate.** 68 % of its 13.9 K case-to-inlet rise is the coolant's own caloric rise at 1.59 LPM/kW; the residual case-to-mean-fluid resistance is 8.6 mK/W, which is **0.14 cm2-K/W on a 16 cm2 B300 die area or 0.21 cm2-K/W on a 25 cm2 TTV heater** [D]. The latter is squarely a conventional skived-plate figure (Section 4). The number is a vendor product-page value read from a search extract (page content not verified this session), with no stated TIM, heater area, coolant, inlet temperature or pressure-tap boundary; the four-significant-figure precision suggests a single test or CFD report, not a tolerance-backed datasheet. **Confidence that it is a real measured figure: medium; that it is a datasheet guarantee: low.**
3. **FiberMall's "< 0.03 K/W, < 20 kPa at 1.8 LPM, 45 C, PG25" is a specification ceiling, not a measured datasheet value.** 0.03 K/W x 1,200 W = 36 K = exactly the 45 C-inlet / ~81 C-case budget; at 1.8 LPM it is 1.5 LPM/kW (the 2025 CDU convention). Read as a per-superchip (2.7 kW) figure it would mean an 81 K rise, which is impossible, so the sibling's "0.67 LPM/kW" reading is wrong and the figure is per GPU [D]. FiberMall is an optical-transceiver reseller's blog; the figures are not NVIDIA's and not a plate vendor's. **Confidence: low as data, medium as a statement of the NVIDIA-era design envelope.**
4. **The "conventional skived" band is now anchored at 0.14-0.22 cm2-K/W case-to-mean-fluid (0.18-0.25 case-to-inlet at 1.2-1.6 LPM/kW), TIM included**, from: the ACT comparison cut-sheet (0.15, V), CoolIT 4 kW (0.19-0.23, V+D), CoolIT 15 kW (0.19-0.23 avg, 0.25-0.30 worst, V+D), ToneCooling (0.14-0.21, V+D), Wakefield 700 W (0.18-0.22, V+D) and the sibling physics reconstruction of a 0.2/0.2 x 4 mm skived split-flow plate (0.22, M). Peer-reviewed manifold-microchannel plates sit at 0.065-0.09 (I) and Mikros claims 0.02 core (V) [Sib]. **The benchmark's unit performance is mid-band for conventional skived copper; it is "uncontested" only because nobody else has built a 15 kW TTV.**
5. **Real vendor R(flow) curves on disk: only JetCool's** (RTX PRO 6000: Rjf 0.058 -> 0.040 K/W over 0.6 -> 1.8 LPM at 600 W; Xeon 6: 0.065 -> 0.045 over 0.5 -> 2.0 LPM at 350 W; PG25 at 40 C; no dP curve) [Sib]. Only one independent fully-specified point exists at GPU scale (ORNL diamond pin-fin: 6.9 mK/W incl. TIM, 3 LPM water, 9.0 kPa, 1 kW) [Sib]. **No skived Group-A curve exists in the public domain; the programme should plan to generate its own by purchasing and testing 2-3 incumbent plates (Section 8).**
6. **Pressure drop is not an energy problem at plate level**: every plate-level point on disk (8-20 kPa at 1-3 LPM) gives a hydraulic COP of 2,000-3,100, i.e. 0.1-0.15 % of the cooled load at 35 % pump efficiency; CoolIT's 4 kW full-loop 55 kPa is COP 720 (0.4 %) [D]. dP matters for CDU head, manifold sizing and negative-pressure compatibility, not for PUE.

## 2. Consolidated table of every competitor plate number on disk (common basis)

R = case(or junction)-to-inlet unless noted. Caloric rise computed for PG25 (rho 1,010 kg/m3, cp 3,930 J/kg-K) or water (990, 4,180). R_c-mf = case-to-mean-fluid = R - 0.5 x caloric/P. R'' = R x assumed heated area. Areas: H100 die 8.1 cm2, B200/B300 two reticle dies ~16 cm2, GB202 ~7.5 cm2, OAM ~8 cm2 (assumed), CoolIT 4 kW heater 25 cm2 (favoured sibling reading), CoolIT 15 kW 100 cm2 (inferred 76-117) [Sib gap-nvidia-rubin; gap-coolit-dp-flow-curves].

| Point (type) | P (W) | Flow (LPM) | LPM/kW | dT (K) | Caloric (K) | R_c-in (mK/W) | R_c-mf (mK/W) | A (cm2) | q'' (W/cm2) | R''_c-in | R''_c-mf (cm2-K/W) | dP (kPa) | Source |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ToneCooling GB300 GPU plate (V,S) | 1,067 | 1.70 | 1.59 | 13.9 | 9.5 | 13.0-13.3 | 8.6-8.9 | 16 (die) / 25 (TTV?) | 67 / 43 | 0.21 / 0.33 | **0.14 / 0.21** | 12.06 | https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ [Sib] |
| FiberMall GB200 plate "target" (S) | 1,200 | 1.80 | 1.50 | 36.0 | 10.1 | < 30 | < 25.8 | 16 | 75 | < 0.48 | < 0.41 | < 20 | https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm [Sib] |
| OCP OAI 1 kW OAM reference (I) | 1,000 | 2-5 (3.5 used) | 3.5 | 15.5 | 4.3 | 15-16 | 13.3 | 8 (assumed) | 125 | 0.12 | 0.11 | n/d | https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/ [Sib] |
| JetCool H100 SmartPlate (V) | 700 | 3.2 | 4.57 | 14.7 | 3.3 | 21 | 18.6 | 8.1 | 86 | 0.17 | 0.15 | n/d | https://www.businesswire.com/news/home/20240430522600/en [Sib] |
| JetCool RTX PRO 6000 datasheet, Rjf (V, datasheet) | 600 | 0.6 / 0.9 / 1.8 | 1.0 / 1.5 / 3.0 | 34.8 / 28.8 / 24.0 | 15.1 / 10.1 / 5.0 | 58 / ~48 / 40 | 45 / 40 / 36 | 7.5 | 80 | 0.44 / 0.36 / 0.30 | 0.34 / 0.30 / 0.27 | n/d | https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf [Sib] |
| JetCool Xeon 6 datasheet, Rjf (V, datasheet) | 350 | 0.5-2.0 | 1.4-5.7 | 22.8-15.8 | - | 65 -> 45 | - | - | - | - | - | n/d | https://info.jetcool.com/hubfs/Marketing%20Resources%202026/Intel%20Xeon%206_SmartPlate%20Datasheet.pdf [Sib] |
| Wakefield on-chip plate (V) | 700 | 1.6 | 2.29 | 18.7 | 6.6 | 26.7 | 22.0 | 8.1 | 86 | 0.22 | 0.18 | n/d | catalogue part, [Sib coolit-briefs-numbers.md] |
| ORNL Cu diamond pin-fin (I, IJHMT 2025/Mar 2026) | 1,000 | 3.0 (water) | 3.0 | 6.9 | 4.8 | 6.9 | 4.5 | 56.25 (full 75 x 75) | 18 | 0.39 | 0.25 | 9.0 | [Sib coolit-briefs-numbers.md / competitors-singlephase.md ref. ORNL] |
| CoolIT 4 kW (V) | 4,000 | 6.06 | 1.51 | < 36 | 10.0 | < 9 | < 7.8 | 25 | 160 | < 0.225 | < 0.19 | 55 (full loop incl. QDs) | CoolIT 4 kW brief via Tom's Hardware [Sib coolit-briefs-numbers.md] |
| CoolIT 15 kW avg / worst (V, benchmark) | 15,000 | 18 | 1.20 | 34.4 / 44.2 | 12.6 | 2.29 / 2.95 | 1.87 / 2.53 | 100 (inferred) | 150 | 0.23 / 0.30 | 0.19 / 0.25 | **n/d** | [Brief] |
| Boyd HybridKIT DSC power-module plate (V) | n/d | 10 (WEG 50/50) | - | - | - | 26 (basis n/d) | - | - | - | - | - | 12.5 | https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf [Sib] |
| Mikros Normal Flow core (V) | - | n/d | - | 30 K at 1 kW/cm2 | - | - | - | - | 1,000 | - | **0.02 core** | 20.7 (3 psi) at 1 kW/cm2 | https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/ [Sib] |
| Iceotope KUL SINK (V, immersion, for scale) | 1,000 | 7.0 | 7.0 | 39 | 2.2 | 39 | 38 | 8 | 125 | 0.31 | 0.30 | n/d | https://www.datacenterdynamics.com/en/news/iceotope-achieves-chip-cooling-up-to-and-beyond-1000w [Sib] |
| ACT cut-sheet "typical single-phase plate" (V, competitor's baseline) | - | - | - | - | - | - | - | - | - | - | **0.15** | - | https://www.1-act.com/wp-content/uploads/2025/11/TPCP-CS-01_TwoPhaseColdPlates-DataCenters-CutSheet_V1_2025-11-12_Web.pdf [Sib] |
| Sibling model: CoolIT-like 0.2/0.2 x 4 mm skived split-flow, 117 cm2 (M) | 15,000 | 18 | 1.20 | 34.5 / 44.3 | 12.7 | 2.30 | 1.88 | 117 | 128 | 0.27 | **0.22** | 21.8 total / 15.4 core | `appendix/physics/hydraulic-detail-output.txt` |

Vendors with **no plate-level number anywhere on disk**: AVC, Cooler Master, Delta, Jentech, Auras, Nidec, Foxconn/Ingrasys, Boyd GPU plates (curves exist only as un-fetchable graphs in https://info.boydcorp.com/hubfs/Thermal/Liquid-Cooling/Boyd-Standard-CPU-Liquid-Cold-Plate-Datasheets.pdf), Mikros/Jabil Ascutney AX-NV1/AX-NV2 (https://_dmarc.mikrosmanufacturing.com/ascutney-series/ lists the parts, no data), Wiwynn/Fabric8 4 kW double-sided ECAM plate (only "up to 40 % improvement expected", "48 % better than skived", "> 350 W/cm2", "200 % improvement in temperature variance" - all V, no baseline), Motivair Dynamic Cold Plate (no R/flow/dP), Vertiv/CoolTera (CDU numbers only), JetCool third-party H100 report (only "25 % lower total R incl. TIM vs tested microchannel plates from 1 LPM up, 50 C PG25", lab unnamed, PDF unreadable) [Sib competitors-singlephase.md, competitors-advanced.md].

## 3. Verification of the ToneCooling and FiberMall figures

### 3.1 ToneCooling (https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/)

What the sibling extract says: GPU plate for GB300 NVL72, ~1,067 W test power, 1.7 LPM, measured 0.0130-0.0133 C/W, dP 12.06 kPa, "design target < 40 kPa at 3 LPM", copper, Ni-plated [Sib coolit-briefs-numbers.md, chip-roadmap-requirements.md]. The page itself could not be fetched by any agent; all numbers come from search-engine extracts.

Physics checks [D]:

| Check | Result | Reading |
|---|---|---|
| Caloric rise at 1.7 LPM PG25 | 9.5 K of the 13.9 K total (68 %) | The figure is flow-dominated; the plate's own contribution is small |
| Case-to-mean-fluid R | 8.6-8.9 mK/W | - |
| R'' if measured on the B300 die (16 cm2, 67 W/cm2) | 0.14 cm2-K/W incl. TIM | top-decile skived performance; would need a thin or PCM TIM (0.03-0.05) and a 0.1 mm-class fin field |
| R'' if measured on a 25 cm2 TTV heater (43 W/cm2) | 0.21 cm2-K/W incl. TIM | ordinary skived plate, identical to the CoolIT 4 kW / 15 kW band |
| Test power vs B300 TDP | 1,067 W vs 1,400 W | at 1,400 W and the same R: dT 18.2-18.6 K, caloric 12.5 K; still within budget |
| Flow basis | 1.59 LPM/kW | well above NVIDIA's 0.75-1.0 LPM/kW rack envelope; a vendor-friendly rating point |
| dP 12.06 kPa at 1.7 LPM | hydraulic 0.34 W, COP 3,100 | consistent with a 0.2-0.3 mm skived core of ~50 mm flow length (sibling model: 5.6-9 kPa at 6-9 LPM for a 15 kW-sized plate; a smaller GPU plate at 1.7 LPM in the same band) |
| Normalised to 1.2 / 1.0 / 0.75 LPM/kW (R_conv ~ Q^-0.3, dP ~ Q^1.3-1.75, 40 % fixed share) | R = 14.9 / 16.4 / 19.3 mK/W; dT = 15.9 / 17.5 / 20.6 K; dP = 7-8 / 5-7 / 3-4.5 kPa | at NVIDIA's 0.75 LPM/kW floor a B300 at 1,400 W would sit at ~27 K case-to-inlet: comfortable |

Verdict: **plausible, conventional, unverified.** It cannot be cited as a datasheet guarantee (no tolerance, no boundary definitions, vendor marketing page), but as a *data point* it is consistent with the skived band and with the sibling physics model. If the heater area was the B300 die, it is the best skived number on record and should be reproduced in-house before being believed.

### 3.2 FiberMall (https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm)

What the sibling extract says: GB200 "liquid cooling plate", 1.8 LPM, 45 C inlet, PG25, "< 20 kPa", "< 0.03 K/W" target, skived copper fins <= 0.5 mm / >= 3 mm tall, Ni-plated [Sib].

Physics checks [D]:

| Check | Result | Reading |
|---|---|---|
| 0.03 K/W x 1,200 W (GB200 GPU) | 36 K -> Tcase 81 C at 45 C inlet | exactly the standard Tcase budget: this is a **ceiling spec**, not a performance figure |
| 0.03 K/W x 2,700 W (superchip) | 81 K | impossible; so 1.8 LPM is per GPU plate = 1.5 LPM/kW (2025 CDU convention), not 0.67 LPM/kW |
| R'' at 16 cm2 | < 0.48 cm2-K/W | any skived plate (0.14-0.22) meets it with > 2x margin |
| Normalised to 1.2 / 1.0 LPM/kW | dP 13.5-15 / 10-12 kPa | - |

Verdict: **not a datasheet value.** It is a correct statement of the design envelope a GB200 GPU plate must meet (consistent with the 45 C / ~80 C case budget used by CoolIT and by the sibling requirement table), republished by a reseller blog. It must not be used as a competitor performance point; it is the floor every supplier clears.

## 4. Anchoring the "conventional skived" unit-resistance band

The orchestrator flagged that the band for conventional skived plates (0.15 cm2-K/W per ACT; 0.18-0.27 inferred for CoolIT) was unanchored. Six independent directions now bracket it:

| Anchor | R''_c-mf (cm2-K/W, TIM incl.) | R''_c-in | Flux (W/cm2) | LPM/kW | Type | Caveat |
|---|---:|---:|---:|---:|---|---|
| ACT two-phase cut-sheet, "typical single-phase" | 0.15 | - | - | - | V (competitor's baseline) | no conditions |
| CoolIT 4 kW (25 cm2 heater favoured) | < 0.19 | < 0.225 | 160 | 1.5 | V + D | heater area inferred |
| CoolIT 15 kW avg (100 cm2 inferred) | 0.19 | 0.23 | 150 | 1.2 | V + D | area 76-117 -> 0.14-0.22 / 0.17-0.27 |
| CoolIT 15 kW worst TC | 0.25 | 0.30 | 150 | 1.2 | V + D | same |
| ToneCooling GB300 plate | 0.14 (die) - 0.21 (25 cm2 TTV) | 0.21-0.33 | 43-67 | 1.6 | V,S + D | heater area unknown |
| Wakefield 700 W on-chip plate | 0.18 | 0.22 | 86 | 2.3 | V + D | die area assumed 8.1 cm2 |
| Sibling physics model, 0.2/0.2 x 4 mm skived split-flow | 0.22 | 0.27 | 128 | 1.2 | M | calibrated to reproduce the benchmark's 34.5 K |
| Sibling model, finer 0.1/0.1 x 2 mm skived | 0.17 | 0.22 | 128 | 1.2 | M | dP 126 kPa at 18 LPM over 54 mm paths: not practical without a manifold |
| OCP OAI 1 kW OAM, PCM TIM | 0.11 | 0.12 | 125 | 3.5 | I | high flow, PCM TIM; die area assumed |
| JetCool H100 (jet, Rjf incl. die) | 0.15 | 0.17 | 86 | 4.6 | V | very high flow |
| Peer-reviewed manifold-microchannel (PKU, Z-manifold, bio-inspired) | 0.065-0.09 | - | 600-1,000+ | - | I | lab, silicon or Cu, small area |
| Mikros Normal Flow core | 0.02 (core only) | - | 1,000 | - | V | excludes TIM and base |

Conclusion: **conventional skived copper with paste/PCM TIM at 1.2-1.6 LPM/kW = 0.14-0.22 cm2-K/W case-to-mean-fluid, 0.18-0.25 case-to-inlet (worst-point up to 0.30).** The benchmark sits in the middle of that band. A manifold-microchannel or ECAM core at 0.065-0.09 (peer-reviewed) with a <= 0.02 cm2-K/W interface is a 2-3x unit-resistance step that no incumbent datasheet contradicts, because no incumbent datasheet exists.

What that implies for a Group-A plate scaled to the 15 kW TTV [D]: at R''_c-mf 0.14 / 0.18 / 0.21 cm2-K/W and 100 cm2 heated, average case-to-inlet = 27.3 / 33.3 / 37.8 K at 18 LPM (caloric 12.6 K included). I.e. **a ToneCooling-class or AVC-class skived plate enlarged to the CoolIT footprint would land within +/- 4 K of the benchmark's 34.4 K.** The benchmark demonstrates scale, not superiority.

## 5. The R(flow) / dP(flow) curves that exist, and a proxy for the ones that do not

### 5.1 Real vendor curves on disk (JetCool only)

| Plate | Flow (LPM) | Rjf (K/W) | R_j-mean-fluid (mK/W) [D] | Note |
|---|---:|---:|---:|---|
| JetCool RTX PRO 6000 SmartPlate, 600 W, PG25 40 C | 0.6 | 0.058 | 45.4 | datasheet |
| same | 0.9 (design, 1.5 LPM/kW) | ~0.048 | ~40 | interpolated |
| same | 1.8 | 0.040 | 35.8 | datasheet |
| JetCool Xeon 6 SmartPlate, 350 W | 0.5 -> 2.0 | 0.065 -> 0.045 | - | datasheet |

Fitted exponent of R_j-mean-fluid vs flow for the RTX PRO 6000 plate: **-0.22** (includes the fixed die + TIM1 share, so the purely convective exponent is steeper, ~-0.3 to -0.4) [D]. No dP curve is published; mechanical rating 72 psi continuous / 216 psi burst [Sib]. These are junction-to-fluid values on a 600 W GPU and are not transferable to a 1.4-3.6 kW socket except as the exponent.

### 5.2 Physics proxy for a Group-A skived plate (sibling model, 15 kW, 117 cm2, PG25 45 C) [M]

| LPM | LPM/kW | dT avg / max (K) | dP core / total (kPa) | Hydraulic W |
|---:|---:|---:|---:|---:|
| 6 | 0.40 | 47.4 / 57.2 | 4.9 / 5.6 | 0.56 |
| 9 | 0.60 | 41.0 / 50.8 | 7.5 / 9.1 | 1.36 |
| 12 | 0.80 | 37.8 / 47.6 | 10.1 / 12.9 | 2.58 |
| 15 | 1.00 | 35.8 / 45.6 | 12.7 / 17.1 | 4.29 |
| 18 | 1.20 | 34.5 / 44.3 | 15.4 / 21.8 | 6.54 |
| 24 | 1.60 | 32.8 / 42.6 | 20.9 / 32.3 | 12.9 |
| 36 | 2.40 | 31.0 / 40.8 | 32.5 / 58.1 | 34.9 |

This curve reproduces the benchmark's 34.4 K / 44.2 K at 18 LPM and is the best available stand-in for an incumbent skived plate's R(flow)/dP(flow) until a real one is measured. Its dP at 1.2 LPM/kW (22 kPa total) is consistent with the vendor-blog band (12-20 kPa for 1.1-1.2 kW plates at 1.5-1.6 LPM/kW) once scaled for size (sibling scaling: core dP ~ P at constant LPM/kW and fin geometry).

### 5.3 Pumping power at every plate-level point on disk [D]

| Point | P (W) | LPM | dP (kPa) | Hydraulic (W) | COP_hyd | Electrical at 35 % eff., % of load |
|---|---:|---:|---:|---:|---:|---:|
| ToneCooling GB300 | 1,067 | 1.7 | 12.1 | 0.34 | 3,100 | 0.09 % |
| FiberMall target | 1,200 | 1.8 | 20 | 0.60 | 2,000 | 0.14 % |
| ORNL pin-fin | 1,000 | 3.0 | 9.0 | 0.45 | 2,200 | 0.13 % |
| Mikros (flow unstated; 1 LPM assumed) | 1,000 | 1.0 | 20.7 | 0.35 | 2,900 | 0.10 % |
| CoolIT 4 kW full loop | 4,000 | 6.06 | 55 | 5.6 | 720 | 0.40 % |
| Sibling skived model, 15 kW | 15,000 | 18 | 21.8 | 6.5 | 2,300 | 0.12 % |

## 6. Price

Nothing new could be added. On disk: GB300 CPU/GPU plate ASP ~US$300, NVSwitch plate ~US$200, Rubin plate "up to US$400" (Morgan Stanley via TechRadar / igor'sLAB, A); IDTechEx US$300-500 per GPU plate, ~US$2,300 per 8-GPU server, ~US$55 k per rack (A); rack liquid-cooling BOM ~US$49.9 k (GB300 NVL72) / ~US$55.7 k (VR NVL144) (A); Group-A procurement centralised by NVIDIA [Sib market-business.md: https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html ; https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/]. No vendor-specific price, and no price for Mikros, Fabric8/Wiwynn, JetCool or Motivair plates, exists in any public source found by any agent. Sibling teardown estimate: factory cost US$70-170 for a skived/welded GB200-class plate depending on volume [Sib manufacturing-cost.md, KB-M].

## 7. What this means for the programme's "beat the market" claim

1. The commercial bar (1.4-3.6 kW socket, ~US$300-400, stated dP) **cannot be quantified from public Group-A data, and will not become quantifiable by more searching**; the data are NDA. The two routes that work are (a) buy incumbent plates and test them under the OCP Cold Plate Test Spec v1.0.0 (Section 8), and (b) obtain an ODM's qualification report under NDA.
2. Until then the defensible comparison basis is **unit resistance**: incumbent skived = 0.14-0.22 cm2-K/W c-mf (Section 4). A plate at <= 0.09 cm2-K/W c-mf incl. interface (sibling HMMC model: 0.095-0.19 depending on channel size; peer-reviewed MMC 0.065-0.09) beats every number on disk by 1.5-3x, at lower dP (sibling model: 8-9 kPa vs 22 kPa at 18 LPM).
3. The two most useful *published* numbers to beat remain CoolIT's own: 34.4 K avg / 44.2 K worst at 1.2 LPM/kW (15 kW) and < 0.009 K/W at 1.5 LPM/kW with 55 kPa full-loop dP (4 kW). ToneCooling's 12 kPa at 1.6 LPM/kW is the only plate-level dP from a volume-style vendor and should be matched or beaten at 1.0 LPM/kW on a same-size plate (normalised: ~5-7 kPa at 1.0 LPM/kW).
4. **Do not cite the FiberMall figure as a competitor datapoint.** It is a ceiling. Citing it would invite the rebuttal that every shipping plate clears it by 2x.

## 8. Recommended action: generate the missing curves in-house

Public search cannot produce Group-A R(flow)/dP(flow) curves. The reliable method:

- Purchase 2-3 incumbent GB200/GB300 GPU plates (AVC or Cooler Master parts are sold as "GB200/GB300 liquid-cooling kits" by secondary vendors such as ToneCooling at roughly US$300-1,500 each [KB-L on price]; an ODM partner can also release spare qualified plates).
- Test them on the programme's own TTV under the OCP Cold Plate Test Spec v1.0.0 (https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf): dP at 45 +/- 2 C at six flows (25-150 % of rated), R = (Tcase - Tin)/P with the recommended TIM [Sib].
- Report R and dP at 0.75 / 1.0 / 1.2 / 1.5 LPM/kW, with heater area stated, so the unit resistance and the exponents (R_conv ~ Q^-n, dP ~ Q^m) are measured rather than assumed. Budget: 4-8 weeks, < US$10 k. This single activity converts the "beats a vendor TTV demo" claim into "beats the market" with independent, reproducible data.

## 9. Gaps / unknowns and the exact searches to run when the budget resets

Not obtained this session (all because no search was possible):

1. Boyd standard CPU/GPU cold-plate datasheet curve values (R vs LPM, dP vs LPM) - PDF exists, graphs only; needs fetching and digitising.
2. Mikros/Jabil Ascutney AX-NV1 / AX-NV2 datasheet (K/W, LPM, kPa, price).
3. Any AVC, Cooler Master, Delta, Jentech or Auras plate-level figure (expected: none public).
4. Wiwynn/Fabric8Labs 4 kW double-sided ECAM plate: K/W, kPa, flow (OCP 2025 slides or Computex materials).
5. Fabric8Labs ECAM plate datasheet or white paper with absolute numbers.
6. JetCool third-party H100 report: lab name, absolute R values, flow range, dP (PDF: https://info.jetcool.com/hubfs/Marketing%20Resources%202024/Third%20Party%20Testing_JetCool_GPUs.pdf).
7. Motivair Dynamic Cold Plate (MI300X variant) datasheet.
8. Vertiv/CoolTera cold-plate datasheet (any).
9. Verification of the ToneCooling page content (heater area, coolant, inlet temperature, TIM, pressure-tap boundary) and the FiberMall page's source for "< 0.03 K/W".
10. Wakefield 0.0267 C/W part number and conditions.
11. Any per-vendor plate price (RFQ or ODM report).

Queries, in priority order (mode in brackets):

- `Boyd "liquid cold plate" GPU datasheet "thermal resistance" "pressure drop" pdf site:info.boydcorp.com` (extended)
- `"Mikros" "Ascutney" AX-NV2 datasheet "C/W" OR "K/W" kPa` (extended)
- `tonecooling GB300 NVL72 cold plate "0.013" "12.06" test conditions heater` (extended)
- `fibermall GB200 liquid cooling plate "0.03" "20 kPa" source` (standard)
- `Wiwynn Fabric8Labs "4 kW" double-sided cold plate "K/W" OR "kPa" OCP 2025 slides` (extended)
- `Fabric8Labs ECAM cold plate datasheet "thermal resistance" "pressure drop"` (extended)
- `JetCool "Third Party Testing" GPUs pdf microchannel "25%" laboratory` (extended)
- `Motivair "Dynamic Cold Plate" MI300X datasheet "thermal resistance"` (standard)
- `Vertiv CoolTera cold plate datasheet` (standard)
- `AVC Asia Vital Components GB300 OR Rubin cold plate "thermal resistance" specification` (extended)
- `Cooler Master GB200 coldplate datasheet "C/W" "LPM"` (extended)
- `Jentech microchannel lid Rubin thermal resistance 2026` (standard)
- `Auras "cold plate" GB300 datasheet` (standard)
- `"cold plate" "GB300" "C/W" "LPM" datasheet` (extended)
- `Wakefield "0.0267" cold plate 700W datasheet` (standard)

## 10. Sources

Primary / local:
- CoolIT 15 kW Tech Brief, June 2026: `appendix/pdf/brief.txt` (local extract)
- Sibling physics model, CoolIT-like skived plate curves: `appendix/physics/hydraulic-detail-output.txt`, `hydraulic-detail-curves.csv`
- This report's calculations: `appendix/research/tools/competitor_normalise.py`

Sibling-retrieved URLs reused here (all [Sib]):
- ToneCooling GB300 NVL72 cold plate: https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ ; GB200 kit: https://tonecooling.com/gb200-liquid-cooling-kit/
- FiberMall GB200 cold plate blog: https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm
- OCP OAI System Liquid Cooling Guidelines (Mar 2023): https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/
- OCP Cold Plate Test Specification v1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- JetCool H100 SmartPlate (Apr 2024): https://www.businesswire.com/news/home/20240430522600/en
- JetCool third-party testing: https://jetcool.com/post/third-party-testing-data/ ; PDF: https://info.jetcool.com/hubfs/Marketing%20Resources%202024/Third%20Party%20Testing_JetCool_GPUs.pdf
- JetCool RTX PRO 6000 datasheet: https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
- JetCool Xeon 6 datasheet: https://info.jetcool.com/hubfs/Marketing%20Resources%202026/Intel%20Xeon%206_SmartPlate%20Datasheet.pdf
- Boyd standard CPU/GPU cold plate datasheets (graphs only): https://info.boydcorp.com/hubfs/Thermal/Liquid-Cooling/Boyd-Standard-CPU-Liquid-Cold-Plate-Datasheets.pdf
- Boyd HybridKIT DSC datasheet: https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf
- Mikros Normal Flow performance: https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/ ; Ascutney series: https://_dmarc.mikrosmanufacturing.com/ascutney-series/ ; Jabil acquisition: https://www.businesswire.com/news/home/20241003396998/en/Jabil-Acquires-Mikros-Technologies-to-Support-Demand-for-Liquid-Cooling-in-AI-Data-Centers
- Wiwynn cold-plate page: https://www.wiwynn.com/technology/advanced-cooling/cold-plate-liquid-cooling ; OCP 2025: https://www.wiwynn.com/news/wiwynn-showcases-next-generation-ai-infrastructure-and-cooling-advances-at-ocp-global-summit-2025
- Fabric8Labs / Wiwynn Computex 2025: https://3dprinting.com/news/fabric8labs-and-wiwynn-to-demonstrate-ecam-cold-plate-technology-at-computex-2025/ ; OCP 2025 PR: https://www.prnewswire.com/news-releases/fabric8labs-to-showcase-advanced-ecam-cold-plate-solutions-with-wiwynn-at-ocp-global-summit-2025-302581679.html ; ECAM vs legacy: https://www.fabric8labs.com/ecam-vs-legacy-liquid-cooling-cold-plates/ ; UIUC paper news: https://mechse.illinois.edu/news/82871
- Motivair Dynamic Cold Plates: https://www.motivaircorp.com/products/dynamic-cold-plates/ ; DCD: https://www.datacenterdynamics.com/en/news/motivair-launches-dynamic-cold-plates-without-skived-microchannels/ ; MI300X PR: https://www.prweb.com/releases/motivair-launches-revolutionary-dynamic-cold-plate-for-amds-mi300x-302247342.html
- ACT two-phase cut sheet (0.15 cm2-K/W single-phase baseline): https://www.1-act.com/wp-content/uploads/2025/11/TPCP-CS-01_TwoPhaseColdPlates-DataCenters-CutSheet_V1_2025-11-12_Web.pdf
- Iceotope 1 kW KUL SINK: https://www.datacenterdynamics.com/en/news/iceotope-achieves-chip-cooling-up-to-and-beyond-1000w
- AVC share: https://news.tvbs.com.tw/english/3179423 ; https://www.taiwannews.com.tw/en/news/6215881
- Rubin Group-A suppliers and ~US$400 ASP: https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html
- Rack cooling BOM / plate ASP (Morgan Stanley via igor'sLAB): https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
- Cooler Master GPU/CPU coldplate page (no data): https://www.coolermaster.com/en-global/products/GPU%2FCPU-Coldplate.html
- Boyd NVIDIA collaboration pages: https://www.boydcorp.com/boyds-collaboration-with-nvidia.html ; https://www.boydcorp.com/thermal/liquid-cooling-systems/liquid-cold-plates/cold-plates-for-ai-server-cooling.html
