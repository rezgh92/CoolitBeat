# Advanced / Non-Conventional Cooling Vendors vs. the CoolIT 15 kW Benchmark

**Research angle:** microjet impingement (JetCool, Frore), two-phase direct-to-chip (ZutaCore, Accelsius), negative-pressure single-phase (Chilldyne), precision/tank immersion (Iceotope, LiquidStack, Submer, GRC), in-silicon microfluidics (Microsoft/Corintis, DARPA ICECool, TSMC), and analyst outlooks on adoption 2026-2030.
**Date of research:** 2026-10-13.
**Method:** 16 WebSearch queries completed (standard + extended). The shared search budget was exhausted before the TSMC / Nvidia / xMEMS / Cooler Master / refrigerant-literature / analyst queries could run; WebFetch is network-blocked in this container (one attempt, DNS failure). Every number below that came from a search carries a URL. Items marked **[PRIOR KNOWLEDGE - UNVERIFIED]** come from the author's background knowledge and were *not* confirmed in this session; treat them as leads, not facts.

---

## 0. The benchmark we are measuring against (CoolIT 15 kW tech brief, June 2026)

| Item | Value | Note |
|---|---|---|
| TDP tested | 15,000 W | 4 ceramic heaters (GPU + HBM zones) |
| Coolant / flow | water-glycol, 1.2 LPM/kW = 18 LPM | "industry standard AI flow rate" |
| Inlet | 45 C | warm-water (W45-class) facility |
| Case-to-inlet dT (avg of 3 plates x 8 TCs) | 34.4 C (range 26.8-44.2 C) | hot-spot non-uniformity ~17 C across one plate |
| Derived R_case-inlet | 34.4 / 15,000 = **0.00229 K/W** | area not disclosed, so no cm2-K/W |
| Pressure drop | **not disclosed** | the single biggest hole in the brief |
| Architecture | Split-Flow, skived/microchannel, conventional mass manufacturing, thermal paste TIM | not direct-to-die |
| Prior 4 kW plate (Mar 2025) | R < 0.009 K/W | |
| OMNI unibody (vendor) | >300 W/cm2, "60% lower R vs standard microchannel" | vendor claim |

Everything below is framed against these numbers: R (K/W), LPM/kW, dP, hot-spot spread, and inlet temperature headroom.

---

## 1. Microjet impingement - JetCool (Flex)

**What it is.** Arrays of sub-millimetre liquid jets impinge normally on the lid (SmartPlate) or directly on the die (SmartLid, "liquid-to-die" in JetCool's own words). Jets break the boundary layer and can be aimed at hot spots, which is the mechanism behind lower R at equal flow. Flex acquired JetCool on 14 Nov 2024 after an OCP-2024 partnership for liquid-cooling-ready servers (Flex investor release: https://investors.flex.com/news/news-details/2024/Flex-Acquires-JetCool-to-Expand-Data-Center-and-Power-Portfolio/ ; partnership: https://jetcool.com/post/flex-and-jetcool-partner-to-develop-liquid-cooling-ready-servers-for-ai-and-high-density-workloads/).

**Published numbers.**

| Product / claim | Value | Conditions | Source | Type |
|---|---|---|---|---|
| H100 SmartPlate | R 0.122 C/W -> **0.021 C/W** | vs air-cooled H100 (not vs liquid) | https://jetcool.com/post/jetcool-unveils-breakthrough-energy-saving-liquid-cooling-for-nvidias-h100-gpus-enhancing-ai-cluster-efficiency-and-performance/ | vendor, Apr 2024 |
| H100 SmartPlate | 82% "performance improvement"; -15% cluster power; GPU -35 C "using 2% of cooled power"; inlet up to 60 C | vs air | same | vendor |
| Third-party H100 test | **25% lower total R (incl. TIM)** vs tested microchannel plates, "from 1 LPM up" | lab unnamed, report not public | https://jetcool.com/post/third-party-testing-data/ ; PDF: https://info.jetcool.com/hubfs/Marketing%20Resources%202024/Third%20Party%20Testing_JetCool_GPUs.pdf | vendor-reported third party |
| General claim | 20-40% lower R vs state-of-the-art microchannel | - | https://jetcool.com/data-center-liquid-cooling/ | vendor |
| RTX PRO 6000 SmartPlate | 600 W TDP; design flow 0.9 LPM (=1.5 LPM/kW); Rjf **~0.040-0.058 C/W** over 0.6-1.8 LPM; PG25 at 40 C inlet; inlet range 18-60 C; 72 psi continuous / 216 psi burst | datasheet | https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf | datasheet |
| Intel Xeon 6 SmartPlate | 350 W; 0.75 LPM design; Rjf ~0.045-0.065 C/W over 0.5-2.0 LPM | Dell R770 | https://info.jetcool.com/hubfs/Marketing%20Resources%202026/Intel%20Xeon%206_SmartPlate%20Datasheet.pdf | datasheet |
| AMD SP5 (Turin) SmartPlate | >500 W TDP | - | https://info.jetcool.com/hubfs/Marketing%20Resources%202026/AMD%20Turin%20SmartPlate%20Cold%20Plate%20Datasheet.pdf | datasheet |
| Capacity statement | SmartPlate "for processors exceeding 1,500 W" | third-party overview | https://www.dcbyte.com/?p=14633 | secondary |
| CDU | 300 kW/rack; >2 MW row | - | https://insidehpc.com/2024/11/flex-acquires-liquid-cooling-company-jetcool/ | vendor |

**Read-across to the 15 kW benchmark.** JetCool's best public R figure for a 600 W GPU (0.040 C/W junction-to-fluid at 1.5 LPM/kW) corresponds to ~24 C rise at 600 W; CoolIT achieves 34 C rise at 25x the power at 1.2 LPM/kW. These are not area-normalised, so the only transferable claim is the *relative* 20-40% (vendor) / 25% (third party, incl. TIM) R reduction versus microchannel at equal flow. If that scaled, a jet-impingement version of the 15 kW plate would land around **dT ~ 26-28 C** at 18 LPM, or match 34 C at roughly 60-70% of the flow.

**Caveats.** (1) Pressure drop is never published - jet arrays with sub-mm orifices typically pay a dP penalty and are filtration-sensitive (JetCool itself talks about "avoiding filtration challenges", which is an admission the issue exists). (2) The 0.021 C/W H100 number is vs. air, not vs. a competing cold plate. (3) The third-party report lab is unnamed and the PDF is not readable here. (4) SmartLid (fluid-to-die) has no public performance datasheet at all; the "1,500 W" is a SmartPlate statement.

---

## 2. Microjet "3D short-loop" cold plate - Frore Systems LiquidJet (launched 14 Oct 2025)

Frore (known for the AirJet piezo chip) entered DLC with a metal-wafer, semiconductor-process-fabricated jet cold plate.

| Claim | Value | Source | Type |
|---|---|---|---|
| Hot-spot heat flux | **600 W/cm2 at 40 C inlet** ("2x standard cold plates") | https://www.froresystems.com/media-room/frore-systems-introduces-liquidjet-redefining-coldplates-for-ai-data-centers ; product page https://www.froresystems.com/products/liquidjet-dlc-coldplate | vendor |
| Pressure drop | "4x lower": **0.94 psi -> 0.24 psi** (6.5 kPa -> 1.7 kPa); product page says "10x lower" (inconsistent) | https://www.club386.com/?p=120993 ; https://tech.yahoo.com/computing/articles/frores-liquidjet-coldplates-designed-handle-094300876.html | vendor; flow not stated |
| Flow efficiency | +50% kW per LPM | launch release | vendor |
| Max TDP | up to **4.4 kW** | https://www.3dtested.com/pc-components/liquid-cooling/frores-new-liquidjet-coldplates-are-equipped-to-handle-the-spiralling-power-demands-of-future-ai-gpus-built-to-handle-up-to-4-4kw-tdps-solution-could-be-deployed-in-power-hungry-feynman-data-centers | vendor |
| Rubin read-across | 6-12 C lower Tj vs conventional DTC; 10-25% tokens/W; ~2 LPM for ~2,300 W Rubin (0.87 LPM/kW) vs ~3.25 LPM (1.41 LPM/kW) conventional | https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/ ; https://www.remio.ai/post/frores-liquidjet-claim-puts-delidded-rubin-gpus-on-the-production-agenda | secondary reporting only |

**Caveats.** All numbers are relative to unnamed "standard" plates with no test conditions; the 4x vs 10x dP inconsistency across Frore's own materials is a red flag; no independent data; the Rubin figures appear only in trade press. Metal-wafer lithographic fabrication is not "conventional" manufacturing and its cost/yield at 100 x 100 mm plate sizes is unknown. Still, 600 W/cm2 is **2x CoolIT's OMNI >300 W/cm2 claim**, and 0.87 LPM/kW is 27% below CoolIT's 1.2 LPM/kW - these are the two numbers a competing design must at least match on paper.

---

## 3. Two-phase direct-to-chip, waterless dielectric - ZutaCore HyperCool

| Claim | Value | Source | Type |
|---|---|---|---|
| Per-chip capacity (progression) | 2,500 W (1U) -> 2,800 W (SC24 / Pegatron cert.) -> "4,000 W+" (current site) | https://zutacore.com/solutions ; https://www.eenewseurope.com/en/pegatron-certifies-zutacore-two-phase-direct-to-chip-liquid-cooling/ ; https://zutacore.com/ | vendor |
| Flow | **0.3 L/min per 1,000 W** (B200 1,200 W = 0.36 LPM) - i.e. **4x less than 1.2 LPM/kW** | https://zutacore.com/faq ; https://secondwatt.com/equipment/liquid-cooling/zutacore-hypercool | vendor |
| Fluids | Opteon SF33, R-1233zd(E): GWP ~1, ODP 0, ASHRAE A1 non-flammable | https://zutacore.com/faq ; https://trusted-oriole-7d4.notion.site/Advanced-liquid-cooling-technology-11ec2c849d648080b147ca70ed817fcf | vendor / secondary |
| Rack density | ">240 kW" (site); 120 kW (SC24); CPI HRU-Water 100 kW cabinet | https://zutacore.com/solutions ; https://convergedigest.com/zutacore-brings-waterless-cooling-for-amd-ai-gpus/ ; https://www.chatsworth.com/assets-proxy/public/asset/raw/663b2857ae13c25e14022b2b/6eb0a978/67993ee12229a03fb2000029/LIQUID_COOLING_HRU_WATER_APPLIC.pdf | vendor |
| Energy | "up to 82% savings" | https://zutacore.com/hubfs/Why%20Two%20Phase%20-%20v4.pdf | marketing |
| Market view | Counterpoint: ZutaCore "in pole position" for two-phase transition | https://counterpointresearch.com/en/insights/AI-Data-Centers-Zutacore-In-Pole-Position-To-Benefit-From-Transition-To-Two-Phase-Cooling | analyst (bullish) |

**Caveats.** No thermal resistance, no case temperature, no pressure drop are published; the 4,000 W figure is a web-page claim without a test report. Two-phase evaporators are limited by critical heat flux (CHF) and by vapour-quality maldistribution across a 4-heater footprint like CoolIT's TTV; dielectric HFO fluids have ~10x lower latent heat x density product than water sensible cooling at 1.2 LPM/kW only wins on *flow* not on *mass*; system needs a condenser/HRU, leak-detection for refrigerant, and the fluids (HFOs) are under PFAS regulatory scrutiny in the EU. Infrastructure compatibility: not plug-compatible with W45 water TCS loops - requires an HRU to the facility water.

---

## 4. Two-phase pumped refrigerant - Accelsius NeuCool (Innventure)

Accelsius is the most data-rich two-phase vendor and the only one with a (quasi-)independent benchmark in 2026.

| Milestone | Value | Source | Type |
|---|---|---|---|
| Oct 2024 | 2,200 W per chip tested | https://www.businesswire.com/news/home/20241010252640/en | vendor |
| 10 Apr 2025 | **4,500 W per GPU socket** on a TTV - "stopped at the power limit of the test infrastructure, not the cooling system"; 250 kW rack with in-row two-phase CDU | https://www.datacenterdynamics.com/en/news/accelsius-tests-ability-to-cool-4500-watt-chips ; https://secure.businesswire.com/news/home/20250410459051/en/ | vendor |
| 25 Sep 2025 | Two-phase reference design, "billions in energy savings" | https://secure.businesswire.com/news/home/20250925255544/en/ | vendor |
| 20 Apr 2026 | NeuCool IR150 (in-row, 150 kW class) general availability; HyperStart program (DCW 2026) | https://www.businesswire.com/news/home/20260420391618/en/ | vendor |
| 21 Jul 2026 | "Independent" benchmark (unnamed SI): 8x B200 server, ~40,000 operating points; **Tj 9 C lower than factory single-phase at warm water**; NeuCool at **54 C inlet matches single-phase at 45 C**; raising facility flow 1.5 -> 3.0 LPM/kW widened gap to 14 C | https://www.businesswire.com/news/home/20260721991081/en/ ; https://www.innventure.com/news/independent-benchmarks-show-accelsius-two-phase-direct-to-chip-cooling-delivers-9degc-lower-nvidia-b200-junction-temperatures-than-single-phase-in-warm-water-conditions | vendor-published, 3rd-party-run |
| Deployment | first IR150 installed at a DC training centre | https://www.facilitiesdive.com/news/accelsius-two-phase-data-center-cooling-technology-deployed-at-training-cen/828954/ | trade press |

**Read-across.** The 9 C Tj advantage on a ~1.2 kW B200 is the most defensible two-phase-vs-single-phase delta in the public record; CoolIT's 15 kW dT of 34 C means a 9 C improvement would be ~26% of the budget. The "54 C inlet = 45 C single-phase" statement is the real commercial value: +9 C facility water means more free-cooling hours. **Caveats:** 4,500 W test has no temperature data; the B200 white paper is not public; SI is unnamed; the comparison baseline is the "factory" cold plate of one server, not a best-in-class plate; the absolute cold-plate R is not published.

---

## 5. Negative-pressure single-phase - Chilldyne (acquired by Daikin Applied, 4 Nov 2025)

| Item | Value | Source |
|---|---|---|
| Cold plate rating | up to **2,000 W TDP** (design limit, not measured) | https://www.storagereview.com/news/chilldyne-starter-kit-enables-rapid-liquid-cooling-adoption-in-the-data-center |
| Starter kit | 300 LPM, 150 kW/rack | https://www.datacenterdynamics.com/en/news/chilldyne-launches-plug-and-play-liquid-cooling-starter-kit/ |
| CDUs | CF-CDU300 300 kW; CF-CDU1500 1,500 kW; 375 kW at 80% capture / 500 kW at 60% | https://www.storagereview.com/review/high-performance-leak-free-liquid-cooling-chilldynes-cdu-and-cold-plates-in-action |
| Acquisition | Daikin Applied, Nov 2025 | https://www.daikinapplied.com/news/news/daikin-applied-expands-data-center-offering-with-acquisition-of-chilldyne |

**Read-across.** Negative pressure is a *reliability* architecture (leak -> air in, not water out), not a thermal one; it caps the available dP across the plate at < 1 atm minus margin, which means a Chilldyne-compatible plate must be a **low-dP design** - directly relevant because CoolIT's undisclosed dP is likely its weak spot. A plate that hits 15 kW at, say, < 30 kPa would be unique in being negative-pressure compatible. No per-chip thermal data at GB200/Rubin class is public.

---

## 6. Immersion and precision immersion

| Vendor | Key numbers | Source | Caveat |
|---|---|---|---|
| **Iceotope** (precision/chassis immersion) | KUL SINK copper-pinned: **0.039 K/W at 1,000 W, 7 L/min** (7 LPM/kW!); R ~constant 250-1,000 W; "11.4% better than tank immersion"; rack lab test with Intel/HPE 19.6 kW: 4% perf, ~1 kW less rack energy, PUE 1.04 vs 1.4 assumed; 40% less power per kW ITE; 5-10x less fluid than tanks | https://www.datacenterdynamics.com/en/news/iceotope-achieves-chip-cooling-up-to-and-beyond-1000w ; https://www.iceotope.com/technology | ~2023 data; 0.039 K/W is 17x CoolIT's 0.0023 K/W and at 6x the specific flow |
| **LiquidStack** (2-phase immersion -> diversified) | tanks up to **252 kW/rack**; CDU-1MW for DTC; GigaModular CDU 2.5-10 MW (quoting Sep 2025); "DTC is the largest segment"; Novec withdrawn (PFAS), replacing with other fluids | https://www.datacenterdynamics.com/en/news/liquidstack-creates-a-coolant-distribution-unit-for-direct-to-chip-systems ; https://www.facilitiesdive.com/news/liquidstack-touts-modular-scalable-data-center-coolant/749676/ ; https://www.energy-xprt.com/products/2-phase-immersion-cooling-tanks-for-full-scale-data-center-deployments-1137101 | the 2-phase immersion pioneer now sells water CDUs - a market signal |
| **Submer** | SmartPodX OCP; Intel forced-convection immersion heat sink **1,000 W**; first ORv3 immersion in Europe (Stellium, 2025); ~100 kW in 2.4 m2 (secondary) | https://www.opencompute.org/news/submer-launches-smartpodx-the-worlds-first-green-ocp-and-hyperscale-ready-immersion-cooling-solution/ ; https://techpowerup.com/news-tags/Submer ; https://capacityglobal.com/news/article-uk-data-centre-unveils-immersion-cooling-proof-of-concept-for-ai-workloads/ ; https://introl.com/blog/building-100kw-gpu-racks-power-cooling-architecture | no GB200/Rubin-class per-chip data; fans needed above ~1 kW shows natural/forced immersion convection limit |
| **GRC** | ICEraQ Series 10 CDU 200 kW warm / 368 kW chilled (2021); 184 kW/rack (2023); current site 100 kW/rack; ICEraQ Micro >2 kW per U; Lonestar6 70 kW/rack | https://www.businesswire.com/news/home/20210518005857/en/ ; https://www.datacenterfrontier.com/cooling/article/11428163/grc-pushes-density-limits-with-support-for-200-kw-immersion-racks ; https://www.datacenterdynamics.com/en/news/grc-signs-oem-agreement-hpe/ | no 2025-26 announcements found; numbers declining over time |

**Read-across.** No immersion vendor publishes anything near 15 kW per device; single-phase immersion is fundamentally limited by dielectric-oil convection (Submer needs fans at 1 kW; Iceotope needs 7 LPM/kW to reach 0.039 K/W). Immersion is *not* the competitor for a 15 kW cold plate; its only remaining AI role is peripheral/100%-capture and edge. The 2026 commercial signal is clear: LiquidStack and Submer both added water-side DTC/CDU products.

---

## 7. In-silicon / embedded microfluidics

### 7.1 Microsoft + Corintis (announced 23-25 Sep 2025)

| Claim | Value | Source |
|---|---|---|
| Heat removal | **"up to 3x better than cold plates"** | https://www.hpcwire.com/2025/09/25/microfluidics-offers-3x-better-cooling-than-cold-plates-microsoft-says/ ; https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/ |
| Temperature | **65% reduction in maximum silicon temperature rise** (peak, not average) | https://hwbusters.com/news/microsofts-liquid-cooled-chips-could-rewrite-the-rules-for-ai-data-centers/ |
| Test | prototype; etched channels in the backside of the die; "simulated Teams meeting" workload; bio-inspired (leaf-vein) channel topology from AI optimisation | https://tech.eu/2025/09/25/corintis-lands-24m-and-microsoft-endorsement-for-chip-cooling-tech/ |
| Status | Microsoft "working on packaging, etching, manufacturing techniques"; enables 3D stacking; Sashi Majety: "still on cold plates in 5 years = stuck" | DCD above |
| Corintis funding | $24 M (Sep 2025) | https://www.yolegroup.com/industry-news/corintis-raises-24m-to-target-the-next-ai-bottleneck-and-collaborates-with-microsoft-for-chip-cooling-breakthrough/ |

**Caveats.** "Up to 3x" is a prototype, workload-dependent, lab number; it removes the TIM + lid + base spreading resistances entirely, so it is not comparable to a lidded plate. It requires the silicon vendor (TSMC/Nvidia/AMD/Microsoft Maia) to etch the die, fluid-seal the package, and accept water (or dielectric) against active silicon - a 2028+ production timeline at best. Corintis also sells conventional-mount, AI-optimised microchannel cold plates (not searched in this session - **[PRIOR KNOWLEDGE - UNVERIFIED]**).

### 7.2 DARPA ICECool (2012-2016)

Lockheed Phase I: embedded microfluidic cooling cut thermal resistance ~**4x** while cooling a demo die at **1 kW/cm2 with 30 kW/cm2 local hot spots**; Phase II: >6x RF output power from a GaN MMIC while running cooler (https://eepower.com/news/cool-technology-turns-down-the-heat-on-high-tech-equipment/ ; https://www.electronics-cooling.com/?p=20264). IBM (ICECool Applications, two-phase R1234ze in 3D stacks) and Georgia Tech (Bakir group, micro-pin-fin intra-chip cooling) results were **not retrieved** in this session - **[PRIOR KNOWLEDGE - UNVERIFIED]**: IBM/GT reported >1 kW/cm2 class single-phase water pin-fin cooling with junction-to-inlet resistance of order 0.01-0.02 cm2-K/W.

### 7.3 TSMC, Nvidia, Intel - NOT SEARCHED (budget exhausted) - [PRIOR KNOWLEDGE - UNVERIFIED]

- TSMC presented silicon-integrated microchannel water cooling at IEDM 2024 / 2025 Technology Symposium claiming ~**2.6 kW dissipation at ~63 C rise** on a SoIC-class test vehicle. Needs confirmation and source.
- Nvidia GTC 2025 roadmap: Rubin Ultra (2027) / Kyber NVL576 rack ~600 kW; per-GPU ~3.6 kW; Jensen stated 45 C warm-water inlet targets. Nvidia has not publicly committed to lidless/direct-to-silicon; CoolIT's brief itself lists "direct-to-die and micro-channel lids" as its own next step.
- Intel/TSMC lidless (bare-die) packages for DLC: OCP discussions 2025; no datasheet found here.

---

## 8. Other named vendors - not reached

- **xMEMS** (XMC-2400 piezo-MEMS "fan-on-a-chip", 2024; 2025 "uCooling" for optical transceivers) - **[PRIOR KNOWLEDGE - UNVERIFIED]**; milliwatt-to-watt class, irrelevant to a 15 kW plate except possibly for optics/peripheral 100% heat capture.
- **Cooler Master** data-centre cold plates / CDUs for GB200-class - no data retrieved; **[UNVERIFIED]**.
- **Hybrid jet + microchannel** academic work: a Sultan Qaboos / BJUT study on multi-micro-jet impingement at 100 W/cm2 found high performance at high flow "at the expense of excessive pressure drop" (https://squ.elsevierpure.com/ar/publications/thermal-characterization-of-multiple-micro-jet-impingement-coolin ; https://ir.bjut.edu.cn/item/49222) - consistent with the dP risk for jet plates.
- **Two-phase cold plate refrigerant literature (R1233zd(E), R515B, Opteon SF33, Novec 7000)** - not searched; **[PRIOR KNOWLEDGE - UNVERIFIED]**: flow-boiling microchannel CHF for HFO/HFC refrigerants is typically 200-500 W/cm2 base-area, HTC 20-60 kW/m2-K, with R1233zd(E) operating near 1-2 bar(a) at 30-50 C saturation; Novec 7000/7100 (3M) exited manufacture end-2025 under PFAS pressure (consistent with LiquidStack's statement above).

---

## 9. Analyst views on single-phase vs two-phase vs microfluidic (2026-2030)

Direct searches of Uptime, Omdia, Dell'Oro, SemiAnalysis and Jon Peddie could **not** be run (budget). What the retrieved sources do say:

| Source | Statement | URL |
|---|---|---|
| CoolIT (vendor market sizing, in brief) | >$5 B hyperscaler TCS spend 2025, >$11 B 2026; single-phase DLC "de facto standard" | benchmark brief |
| LiquidStack (2-phase immersion pioneer) | "DTC is currently the largest segment of the liquid cooling market"; AI racks to 600 kW by 2027 (echoing Jensen Huang) | https://www.facilitiesdive.com/news/liquidstack-touts-modular-scalable-data-center-coolant/749676/ |
| Counterpoint Research | two-phase transition coming; ZutaCore positioned to benefit | https://counterpointresearch.com/en/insights/AI-Data-Centers-Zutacore-In-Pole-Position-To-Benefit-From-Transition-To-Two-Phase-Cooling |
| Microsoft (Majety) | cold plates will be "stuck" within 5 years; in-chip microfluidics needed for 3D-stacked SoCs | https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/ |
| Accelsius / Innventure | two-phase matches single-phase at +9 C inlet | https://www.businesswire.com/news/home/20260721991081/en/ |

**[PRIOR KNOWLEDGE - UNVERIFIED] consensus from 2024-25 Uptime/Omdia/Dell'Oro commentary:** single-phase water DTC holds the overwhelming majority of DLC revenue through 2030; two-phase DTC is a single-digit-percent niche gated by refrigerant/PFAS regulation and facility unfamiliarity; immersion share is flat-to-declining for AI training; in-silicon microfluidics is a 2028-2030+ topic tied to chiplet/3D stacking rather than a cold-plate replacement.

---

## 10. Side-by-side scorecard vs the 15 kW benchmark

| Metric | CoolIT 15 kW (benchmark) | JetCool jet | Frore LiquidJet | ZutaCore 2-phase | Accelsius 2-phase | Microsoft/Corintis in-chip | Iceotope precision immersion |
|---|---|---|---|---|---|---|---|
| Max demonstrated per device | **15 kW** (TTV) | ~0.6 kW datasheet; "1.5 kW+" claim | 4.4 kW (claim) | 2.8 kW cert.; 4 kW+ claim | **4.5 kW** TTV (lab-limited) | prototype GPU | 1 kW |
| R or dT | dT 34.4 C @ 45 C in; 0.0023 K/W | Rjf 0.040 C/W @ 600 W; "-25% vs microchannel" | "-6-12 C Tj on Rubin" | n/a | **-9 C Tj vs single-phase** (B200) | "-65% peak dT; 3x heat removal" | 0.039 K/W @ 1 kW |
| Specific flow | 1.2 LPM/kW | 1.5 LPM/kW (RTX) | 0.87 LPM/kW (Rubin claim) | **0.3 LPM/kW** | n/a | n/a | 7 LPM/kW |
| Pressure drop | **undisclosed** | undisclosed | 0.24 psi (1.7 kPa) claim | undisclosed | undisclosed | n/a | n/a |
| Hot-spot capability | 17 C spread across 8 TCs | jets targetable | 600 W/cm2 | CHF-limited | CHF-limited | best (in-die) | poor |
| Inlet headroom | 45 C | up to 60 C | 40 C quoted | n/a | 54 C = 45 C single-phase | n/a | n/a |
| Manufacturing | conventional skive/braze | precision-drilled jet plate | metal-wafer litho | evaporator + HRU | evaporator + in-row CDU | die etch at foundry | pinned copper + chassis |
| Infra compatibility (W45 water TCS) | native | native | native | **needs HRU, refrigerant** | **needs refrigerant CDU** | needs chip vendor | needs dielectric chassis |
| Independent data | no (vendor TTV) | "third party", unnamed | none | none | SI-run, unnamed, 2026 | none | none |

---

## 11. What this means for a design that must beat CoolIT

1. **The gap to attack is pressure drop and flow, not raw dT.** Nobody except Frore (0.24 psi, unverified) publishes dP; CoolIT withholds it. A conventional-manufactured plate that delivers dT <= 30 C at 15 kW *and publishes* dP <= ~30-40 kPa at 18 LPM (or equal dT at <= 0.9 LPM/kW) wins on the metric the market is starting to care about (CDU pump energy, negative-pressure compatibility, rack manifold sizing at 600 kW).
2. **Jet impingement is the proven conventional lever** (JetCool third-party -25% R incl. TIM at equal flow; Frore 600 W/cm2). A hybrid jet-onto-microchannel/pin-fin core, drilled or stamped rather than wafer-lithographed, is manufacturable today. Budget the dP penalty carefully and specify filtration (<= 50 um) in the TCS spec.
3. **Hot-spot uniformity is where the benchmark is weakest** (26.8-44.2 C spread). Zoned jet density / zoned fin pitch mapped to the GPU vs HBM heat-flux map can likely cut the spread to < 8 C - a measurable, marketable win.
4. **Two-phase wins on flow (0.3 LPM/kW) and on inlet temperature (+9 C)** but loses on infrastructure compatibility and PFAS risk; the sensible architectural response is a single-phase water plate that *also* qualifies with a dielectric/refrigerant evaporator variant later, not a two-phase lead product.
5. **In-silicon microfluidics is the 2028+ threat, not a 2026 competitor.** Position the product as "direct-to-die ready" (lidless, bare-die contact with a compliant/indium or liquid-metal TIM) because CoolIT itself says that is its next step and Frore's Rubin pitch assumes delidding.
6. **Immersion is not a competitor at 15 kW per device.**
7. **Power electronics (SiC converters) read-across:** the same low-dP, hot-spot-zoned plate at 300-600 W/cm2 covers SiC modules (typically 100-300 W/cm2 on the baseplate), but with a glycol/oil-compatible, vibration-rated, brazed-aluminium variant - a separate SKU, not a separate architecture.

---

## 12. Gaps / unknowns

- **Not searched at all (search budget):** TSMC in-silicon microcooler figures; Nvidia Rubin Ultra/Kyber cooling specs and any "direct-to-silicon" statements; xMEMS 2025-26; Cooler Master DC cold plates; refrigerant two-phase cold-plate papers (R1233zd/R515B/SF33); Intel/TSMC lidless package specs; Corintis's own cold-plate product datasheets; Vertiv/Boyd/Auras jet or hybrid plates; **all analyst reports (Uptime 2025/2026 survey, Omdia, Dell'Oro, SemiAnalysis, Jon Peddie)**. All items in sections 7.3, 8 and the analyst consensus paragraph are flagged as unverified prior knowledge.
- **Pressure drop** is unpublished by CoolIT, JetCool, ZutaCore, Accelsius and Iceotope; Frore's single dP claim is internally inconsistent (4x vs 10x).
- **Heater / footprint area** of CoolIT's TTV is not disclosed, so no cm2-K/W or W/cm2 can be derived for the benchmark; area-normalised comparison with OMNI's >300 W/cm2 and Frore's 600 W/cm2 is therefore impossible.
- **No independent lab reports are public** for any vendor: JetCool's third-party PDF could not be fetched (network blocked), Accelsius's SI is unnamed and its white paper was not found.
- **JetCool SmartLid (liquid-to-die)** has no public thermal datasheet.
- **ZutaCore 4,000 W** and **Accelsius 4,500 W** have no accompanying temperature or resistance data.
- **CoolIT OMNI** "60% lower R" baseline conditions are undefined.
- Dates are missing on several vendor pages (ZutaCore, Iceotope, GRC), so "current" figures may be stale.

---

## Sources

1. CoolIT 15 kW tech brief (June 2026) - local extract /tmp/.../appendix/pdf/brief.txt
2. https://jetcool.com/post/jetcool-unveils-breakthrough-energy-saving-liquid-cooling-for-nvidias-h100-gpus-enhancing-ai-cluster-efficiency-and-performance/
3. https://jetcool.com/post/third-party-testing-data/
4. https://info.jetcool.com/hubfs/Marketing%20Resources%202024/Third%20Party%20Testing_JetCool_GPUs.pdf
5. https://jetcool.com/data-center-liquid-cooling/
6. https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
7. https://info.jetcool.com/hubfs/Marketing%20Resources%202026/Intel%20Xeon%206_SmartPlate%20Datasheet.pdf
8. https://info.jetcool.com/hubfs/Marketing%20Resources%202026/AMD%20Turin%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
9. https://www.dcbyte.com/?p=14633
10. https://investors.flex.com/news/news-details/2024/Flex-Acquires-JetCool-to-Expand-Data-Center-and-Power-Portfolio/
11. https://jetcool.com/post/flex-and-jetcool-partner-to-develop-liquid-cooling-ready-servers-for-ai-and-high-density-workloads/
12. https://insidehpc.com/2024/11/flex-acquires-liquid-cooling-company-jetcool/
13. https://www.froresystems.com/media-room/frore-systems-introduces-liquidjet-redefining-coldplates-for-ai-data-centers
14. https://www.froresystems.com/products/liquidjet-dlc-coldplate
15. https://www.club386.com/?p=120993
16. https://tech.yahoo.com/computing/articles/frores-liquidjet-coldplates-designed-handle-094300876.html
17. https://www.3dtested.com/pc-components/liquid-cooling/frores-new-liquidjet-coldplates-are-equipped-to-handle-the-spiralling-power-demands-of-future-ai-gpus-built-to-handle-up-to-4-4kw-tdps-solution-could-be-deployed-in-power-hungry-feynman-data-centers
18. https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/
19. https://www.remio.ai/post/frores-liquidjet-claim-puts-delidded-rubin-gpus-on-the-production-agenda
20. https://zutacore.com/solutions
21. https://zutacore.com/faq
22. https://zutacore.com/
23. https://zutacore.com/hubfs/Why%20Two%20Phase%20-%20v4.pdf
24. https://www.eenewseurope.com/en/pegatron-certifies-zutacore-two-phase-direct-to-chip-liquid-cooling/
25. https://convergedigest.com/zutacore-brings-waterless-cooling-for-amd-ai-gpus/
26. https://counterpointresearch.com/en/insights/AI-Data-Centers-Zutacore-In-Pole-Position-To-Benefit-From-Transition-To-Two-Phase-Cooling
27. https://www.chatsworth.com/assets-proxy/public/asset/raw/663b2857ae13c25e14022b2b/6eb0a978/67993ee12229a03fb2000029/LIQUID_COOLING_HRU_WATER_APPLIC.pdf
28. https://secondwatt.com/equipment/liquid-cooling/zutacore-hypercool
29. https://www.networkworld.com/article/2108453/zutacore-launches-liquid-cooling-for-advanced-nvidia-chips.html
30. https://www.datacenterdynamics.com/en/news/accelsius-tests-ability-to-cool-4500-watt-chips
31. https://secure.businesswire.com/news/home/20250410459051/en/Accelsius-Achieves-Industry-Leading-Thermal-Milestones-for-Next-Generation-AI-Computing
32. https://www.businesswire.com/news/home/20241010252640/en
33. https://secure.businesswire.com/news/home/20250925255544/en/Accelsius-Unveils-Two-Phase-Cooling-Reference-Design-Demonstrating-Billions-in-Potential-Energy-Savings
34. https://www.businesswire.com/news/home/20260420391618/en/Accelsius-Announces-General-Availability-of-NeuCool-IR150-and-Launches-NeuCool-HyperStart-Program-at-Data-Center-World-2026
35. https://www.businesswire.com/news/home/20260721991081/en/
36. https://www.innventure.com/news/independent-benchmarks-show-accelsius-two-phase-direct-to-chip-cooling-delivers-9degc-lower-nvidia-b200-junction-temperatures-than-single-phase-in-warm-water-conditions
37. https://www.facilitiesdive.com/news/accelsius-two-phase-data-center-cooling-technology-deployed-at-training-cen/828954/
38. https://www.storagereview.com/news/chilldyne-starter-kit-enables-rapid-liquid-cooling-adoption-in-the-data-center
39. https://www.datacenterdynamics.com/en/news/chilldyne-launches-plug-and-play-liquid-cooling-starter-kit/
40. https://www.storagereview.com/review/high-performance-leak-free-liquid-cooling-chilldynes-cdu-and-cold-plates-in-action
41. https://www.daikinapplied.com/news/news/daikin-applied-expands-data-center-offering-with-acquisition-of-chilldyne
42. https://www.datacenterdynamics.com/en/news/iceotope-achieves-chip-cooling-up-to-and-beyond-1000w
43. https://www.iceotope.com/technology
44. https://www.datacenterdynamics.com/en/news/liquidstack-creates-a-coolant-distribution-unit-for-direct-to-chip-systems
45. https://www.facilitiesdive.com/news/liquidstack-touts-modular-scalable-data-center-coolant/749676/
46. https://www.energy-xprt.com/products/2-phase-immersion-cooling-tanks-for-full-scale-data-center-deployments-1137101
47. https://www.opencompute.org/news/submer-launches-smartpodx-the-worlds-first-green-ocp-and-hyperscale-ready-immersion-cooling-solution/
48. https://techpowerup.com/news-tags/Submer
49. https://capacityglobal.com/news/article-uk-data-centre-unveils-immersion-cooling-proof-of-concept-for-ai-workloads/
50. https://introl.com/blog/building-100kw-gpu-racks-power-cooling-architecture
51. https://www.businesswire.com/news/home/20210518005857/en/
52. https://www.datacenterfrontier.com/cooling/article/11428163/grc-pushes-density-limits-with-support-for-200-kw-immersion-racks
53. https://www.datacenterdynamics.com/en/news/grc-signs-oem-agreement-hpe/
54. https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/
55. https://www.hpcwire.com/2025/09/25/microfluidics-offers-3x-better-cooling-than-cold-plates-microsoft-says/
56. https://hwbusters.com/news/microsofts-liquid-cooled-chips-could-rewrite-the-rules-for-ai-data-centers/
57. https://tech.eu/2025/09/25/corintis-lands-24m-and-microsoft-endorsement-for-chip-cooling-tech/
58. https://www.yolegroup.com/industry-news/corintis-raises-24m-to-target-the-next-ai-bottleneck-and-collaborates-with-microsoft-for-chip-cooling-breakthrough/
59. https://eepower.com/news/cool-technology-turns-down-the-heat-on-high-tech-equipment/
60. https://www.electronics-cooling.com/?p=20264
61. https://squ.elsevierpure.com/ar/publications/thermal-characterization-of-multiple-micro-jet-impingement-coolin
62. https://ir.bjut.edu.cn/item/49222
