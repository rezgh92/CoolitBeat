# Gap report: fine-channel fouling vs. the filtration rule - what TCS loops actually filter, what the field says about clogging, and the smallest channel a drop-in plate can carry

Date: 2026-10-13. Programme: beat the CoolIT 15 kW coldplate (June 2026 tech brief, `appendix/pdf/brief.txt`). Angle: resolve the contradiction between the "elite" fin geometry (0.05-0.075 mm gaps, 19.8-22 K average case-to-inlet in the sibling model) and the standards/manufacturing recommendation (>= 0.15 mm gaps with 50 um filtration, or 25 um point-of-use strainer plus demonstrated tolerance to 10-20 % channel blockage).

## 0. Retrieval status - read first

**Zero web searches ran in this task.** The turn's shared WebSearch budget (200 calls across every agent in the workflow) was already exhausted when the task started; all six opening queries were refused. The single permitted WebFetch attempt (Electronics360 Ecolab Q&A) failed on DNS (`getaddrinfo ENOTFOUND`), as the brief warned. No search-engine workaround was attempted.

Everything below is therefore built from three evidence classes, each tagged in every table:

- **[Sib-URL]**: facts sibling agents retrieved earlier in this run *with a URL* (listed in Sources). These are the only externally sourced items.
- **[Calc]**: numbers from the project's own physics (`appendix/physics/fouling-filtration.py/.out/.md`, `research/recon/coldplate_model_v2.py`), re-read and re-derived here.
- **[KB-H/M/L]**: the author's background knowledge of vendor datasheets and standards (high / medium / low confidence), **not verified this session**. Every micron rating attributed to a specific CDU or to NVIDIA is in this class. Treat as leads to confirm, not facts.

Consequence: this report cannot *close* the filtration-rating question with primary sources. What it does is (a) consolidate every sourced fact on disk, (b) state the best-estimate rating per entity with confidence, (c) show by physics that **the design decision is the same under every plausible rating**, so the architecture does not have to wait for the PDFs, and (d) give the exact 14-query retrieval plan and the plate-level qualification test that make the rule evidence-based.

## 1. Bottom line

1. **What is filtered where (best estimate).** The installed TCS fleet filters at **50 um nominal at the CDU secondary** (CoolIT CHx, Vertiv CoolChip/XDU, Motivair, nVent, Nidec/Deschutes-class), with coarser 100-200 um basket strainers on the facility (FWS/primary) side, and typically **no filtration finer than the CDU inside the rack or tray**. 25 um is offered as an option by some CDU makers and is written into some hyperscaler/HPC SOWs. [KB-M for the 50 um norm; KB-L for any individual product; no product datasheet rating was verified this session.] The OCP PG25 Guidelines V1.0.0 (Oct 2026) are known to carry particle-count action limits [Sib-URL, values not captured]; no OCP or NVIDIA public document with a numeric micron rating is on disk.
2. **Nominal vs absolute matters more than 25 vs 50.** A 50 um *nominal* cartridge (the common CDU type) passes rigid particles to ~75-100 um; a 50 um wire-mesh strainer is close to absolute for rigid particles but passes fibres and soft elastomer. [Calc/KB-H] Hence "50 um filtration" implies a largest-passed rigid particle of ~90 um unless the operator can show a beta-rated element.
3. **Field evidence of clogging is qualitative but real.** Ecolab (CoolIT's owner since July 2026) publicly attributes recent field cold-plate performance problems to incomplete flushing/fill with particulates migrating into plates [Sib-URL, Electronics360 7 Oct 2026]. Google reports ~99.999 % CDU-fleet availability *with isolated loops and filtration* [Sib-URL]. Schneider says CDU ratings are not comparable unless filter dP is included [Sib-URL]. No vendor or Uptime dataset with clogging *rates* is on disk [Sib: standards-reliability.md gap 6].
4. **Shipping GB200/GB300 plates**: public (vendor-blog grade) bounds are skived copper, fins <= 0.5 mm, >= 3 mm tall, channels < 0.3 mm, nickel-plated [Sib-URL, S-grade]; nothing finer than ~0.2 mm is evidenced in volume, and **no evidence exists of plate-integral point-of-use strainers on GB-class trays** [KB-M]. The plates rely on the CDU filter.
5. **Resolution.** Under every plausible rating (25 um absolute, 50 um absolute, 50 um nominal), the physics gives the same ordering: **0.15 mm gap with a plate-integral 50 um absolute screen is the drop-in floor; 0.10 mm is a performance SKU only behind <= 33 um absolute loop filtration; 0.05-0.075 mm is not deployable** (W/d <= 2-3 even behind 25 um absolute, St > 1 impaction of 50 um Cu-oxide, x2.5-7 channel dP at a 10-20 um in-situ film). [Calc] The cost of the rule is **~2 K (0.10 -> 0.15 mm) and ~4 K (0.075 -> 0.15 mm) of average case-to-inlet dT** on the 15 kW TTV; the manifold (short flow length), not the sub-0.1 mm gap, is what beats the benchmark (26.1 K vs 34.4 K average at 0.15 mm). [Calc]
6. **Strainer dP adder**: 0.3-0.8 kPa clean for a 25 um pleated element of 20-50 cm2, rising to 5-12 kPa at 50 % blinding; a port-sized (1 cm2) 25 um screen is 17-51 kPa and unacceptable. A 50 um mesh of >= 30 cm2 is ~0.2 kPa clean / ~5 kPa at 50 % blinding. Budget **2-5 kPa (serviced at 3x clean dP)** in the plate dP spec. [Calc]
7. **Drop-in verdict**: with the 0.15 mm + 50 um-absolute-screen rule, the plate is drop-in behind any CDU in the fleet regardless of whether its filter is 50 um nominal or absolute, and needs no change to operator water-quality practice. The 0.10 mm SKU is not drop-in: it makes the plate screen the loop's finest filter, which must then be sized, monitored and serviced.

## 2. What filtration is specified where

| Entity / document | Filtration rating (best estimate) | Nominal or absolute | Evidence class | Source on disk |
|---|---|---|---|---|
| OCP PG25 Guidelines V1.0.0 (Oct 2026) | In-service monitoring with action limits for glycol %, pH, conductivity, inhibitor, **particle count**, microbial count; **micron rating and particle classes not captured** | unknown | [Sib-URL, snippet only] | https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf |
| OCP Base Spec PG25 v1.0.0 (2025) | Coolant composition/properties; no filtration number captured | - | [Sib-URL] | https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/ |
| OCP L-L CDU Test Methodology r1 | CDU rated at 1.5 LPM/kW, >= 40 psi TCS head, components to 100 psi; filter dP inside the rating boundary (Schneider's reading) | - | [Sib-URL] | https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/ ; https://blog.se.com/datacenter/2025/12/16/account-for-filtering-too-beware-of-how-cdu-rating-capacity-is-specified/ |
| OCP ACS / ORv3 Cold Plate Requirements (first gen, ~2021-22) | Believed to require plates to tolerate the particulate a 50 um TCS filter passes; document not located by any agent | - | [KB-L] | not located |
| ASHRAE TC 9.9 TCS water-quality table (Liquid Cooling Guidelines / "Water-Cooled Servers" 2019) | **50 um** filtration listed with pH, bacteria, chloride, sulfate limits | nominal (not stated) | [KB-M] | no URL this session |
| NVIDIA GB200/GB300 NVL72 liquid-cooling / site-prep guides | NDA. Public via partners: PG25, 45 C max supply, 65 C max return, ~130 LPM/rack. Filtration believed to be stated as **<= 50 um** at the CDU, deferring to OCP/ASHRAE water quality | - | temperatures/flow [Sib-URL]; micron [KB-L] | https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf |
| CoolIT CHx1000 / CHx1500 / CHx2000 | Secondary head 35 / 44 / 53 psi [Sib-URL]; secondary-loop cartridge filtration believed **50 um**, hot-swappable, with filter dP monitoring | nominal (cartridge) | heads [Sib-URL]; micron [KB-L/M] | https://www.coolitsystems.com/cdu-product/chx2000/ ; https://www.storagereview.com/news/coolit-chx1500-delivers-1500kw-of-precision-liquid-cooling |
| Vertiv CoolChip CDU (ex-Liebert XDU / CoolTera) | 100 kW-2.3 MW at 4 C approach [Sib-URL]; secondary filtration believed **50 um** with dP alarm | nominal | capacities [Sib-URL]; micron [KB-L] | https://www.vertiv.com/zh-CN/products-catalog/thermal-management/high-density-solutions/vertiv-coolchip-cdu/ |
| Google Project Deschutes CDU (Boyd/Nidec build, OCP contribution) | 2 MW at 3 C ATD, **80 psi available "to enable advanced cold plate designs"**; isolated TPU loop with filtration; ~99.999 % CDU availability since 2020 [Sib-URL]; micron rating not captured | - | [Sib-URL] except micron [KB-L: 50 um class] | https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/ ; https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips ; https://www.nidec.com/v=1764743613/files/topics/19006_ext_5_en_0.pdf |
| nVent CDUs / NVIDIA reference architecture (Nov 2024) | CDU + L2A + manifolds; secondary filtration believed **50 um** | nominal | architecture [Sib-URL]; micron [KB-L] | https://businesswire.com/news/home/20241118649897/en/nVent-Collaborates-with-NVIDIA-on-AI-Ready-Liquid-Cooling-Solutions/ |
| Motivair (Schneider) CDUs 105 kW-2.5 MW | secondary filtration believed 50 um (25 um option) | nominal | [KB-L] | https://www.motivaircorp.com/products/dynamic-cold-plates/ (plates only) |
| OEM DWC loops (Lenovo Neptune, HPE Cray EX, Dell DLC) | Water-quality specs believed to call **50 um** filtration at CDU/manifold; HPE/Lenovo add inline strainers at the cabinet/manifold level in some designs | nominal | [KB-M for 50 um; KB-L for strainers] | no URL this session |
| Negative-pressure (Chilldyne / Daikin) | Loop-level filtration inside the CDU; rating not on disk | - | [Sib-URL architecture only] | https://www.storagereview.com/review/high-performance-leak-free-liquid-cooling-chilldynes-cdu-and-cold-plates-in-action |

Reading of the table: **no document on disk states a numeric TCS filtration rating with a URL.** The 50 um norm is a consistent background-knowledge prior across ASHRAE, OCP-era CDU datasheets and OEM water-quality specs (KB-M), and nothing on disk contradicts it. Two things *are* sourced: the Oct-2026 OCP PG25 Guidelines do include particle-count action limits, and Schneider insists filter dP belongs inside the CDU rating - i.e. the industry is now treating particulates as a specified, monitored quantity.

## 3. Field evidence of clogging, and where the particles come from

| Item | What is known | Evidence class | Source |
|---|---|---|---|
| Ecolab / CoolIT (Bob Walicki, 7 Oct 2026) | Recent field cold-plate performance issues attributed to **incomplete flushing and fill, with particulates migrating into cold plates**; systemic microchannel vulnerability, not a CoolIT-specific defect; Ecolab (Nalco water chemistry) bought CoolIT for US$4.75 bn (closed July 2026) and markets commissioning/water-quality services | [Sib-URL] (sibling read a search extract; full text not fetched) | https://electronics360.globalspec.com/article/24164/q-a-ecolab-bets-on-liquid-cooling-for-ai-data-center-growth ; https://s204.q4cdn.com/218790897/files/doc_downloads/2026/03/Ecolab-to-Acquire-CoolIT-Systems.pdf |
| Google (Hot Chips 2025, OCP) | Facility and TPU loops **isolated**; filtration in the TPU loop; CDU-fleet availability ~99.999 % since 2020; ~1 GW liquid-cooled over ~2,000 pods | [Sib-URL] | https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips |
| Schneider Electric (Dec 2025) | CDU capacity ratings must include filter pressure drop; ratings without it are not comparable | [Sib-URL] | https://blog.se.com/datacenter/2025/12/16/account-for-filtering-too-beware-of-how-cdu-rating-capacity-is-specified/ |
| UTA (Agonafer group) accelerated degradation of copper cold plates in PG25 | Thesis exists (URL located); reports corrosion/degradation of copper microchannels under aged PG25; numeric R and dP drift **not captured** | [Sib-URL for existence; content KB-L] | https://uta-ir.tdl.org/uta-ir/handle/10106/31381 |
| Data Centre Review, "How to build reliable liquid cooling systems" (Aug 2026) | URL located; content not captured | [Sib-URL, unread] | https://datacentrereview.com/2026/08/how-to-build-reliable-liquid-cooling-systems/ |
| Uptime Institute surveys 2024-25 | Leaks are the top-ranked DLC concern, dominated by connections and human error; typical 40 C GPU supply limit [Sib-URL]; **no clogging-incident statistics retrievable** | leaks [KB-M]; 40 C [Sib-URL] | https://intelligence.uptimeinstitute.com/entity_pdf/node/153594/pdf |
| OCP ACS leak-detection white paper | System-side detection/intervention; no particulate content | [Sib-URL] | https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1 |
| JetCool | Its own marketing speaks of "avoiding filtration challenges", an admission that sub-mm jets are filtration-sensitive | [Sib-URL] | https://jetcool.com/post/understanding-direct-to-chip-liquid-cooling-approaches-and-performance-tradeoffs/ |
| Vendor plate clogging statistics (AVC, Cooler Master, Delta, Auras, CoolIT, Boyd) | **none published** | [Sib] | research/competitors-singlephase.md item 8 |

Particle classes that matter, with density and settling velocity in PG25 (mu = 1.25 mPa s) [Calc, `fouling-filtration.out` section A]:

| Source | rho (kg/m3) | size (um) | v_settle at 50 um (mm/s) | Enters via | Filterable? |
|---|---:|---|---:|---|---|
| Cu oxide flakes (Cu2O/CuO) | 6,000 | 1-50 | 5.4 | in-situ corrosion, mixed-metal galvanic | partly (formed downstream of the CDU) |
| Ni plating flakes | 8,900 | 1-200 | 8.6 | plate/manifold plating peel | yes if upstream |
| Braze flux residue, Cu machining chips | 3,000 | 10-500 | 2.2 | factory, inadequate flush | yes (commissioning flush) |
| Al(OH)3 gel | 2,400 | 1-100 | 1.5 | any aluminium in the loop | no (gel) |
| EPDM / UQD seal shedding | 1,100 | 10-300 | 0.10 | hoses, QD cycling | fibres pass meshes lengthwise |
| PTFE tape / sealant | 2,200 | 100-2,000 | 1.3 | installation | caught, but shreds |
| Inhibitor precipitate (silicate/phosphate) | 2,000 | 1-20 | 1.1 | chemistry drift | no (formed in situ) |
| Biofilm flocs | 1,050 | 20-1,000 | 0.05 | stagnant zones, 30-45 C | no (formed in situ) |

Two consequences the filtration debate usually misses [Calc]: (i) dense particles settle in **dead-end headers** (0.5 mm in a slot dead-end at 0.05 m/s, 22 mm in a rack manifold), not in 2 mm channels (22 um); so clogging clusters at slot ends and the first channels after the port; (ii) three of the eight particle classes are formed *inside* the plate loop and no CDU filter rating protects against them. Fine channels lose on these regardless of the filter standard (Section 5.3).

## 4. What shipping GB200/GB300 plates actually use

| Item | Public evidence | Evidence class | Source |
|---|---|---|---|
| Fin geometry, GB200 "liquid cooling plate" | skived copper, fins **<= 0.5 mm**, **>= 3 mm** tall, < 0.03 K/W target, < 20 kPa at 1.8 LPM, Ni-plated | [Sib-URL, S-grade reseller blog] | https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm |
| GB300 plate channels | "< 0.3 mm channels", 2-4 m/s (velocity figure flagged unreliable) | [Sib-URL, low reliability] | https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling |
| ToneCooling GB300 GPU plate | 0.013 K/W at 1.7 LPM, 12.06 kPa, Ni-plated Cu; sibling physics says consistent with a 0.2-0.3 mm skived core | [Sib-URL + Calc] | https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ |
| Finest commercial skived fin seen | 0.06 mm fins at 0.10 mm pitch (catalogue item; likely an air heat sink, not a qualified cold plate) | [Sib-URL] | https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink |
| CoolIT skived / Split-Flow briefs | fin pitch, thickness and height **not disclosed** anywhere indexed | [Sib] | research/coolit-products.md |
| Nickel plating | de-facto NVIDIA/ODM practice for GB-class plates; 5-15 um electroless Ni; throwing power poor inside sub-150 um channels | [KB-M]; vendor pages [Sib-URL] | research/manufacturing-cost.md |
| Plate-integral or tray-level point-of-use strainer | **no evidence of any on GB200/GB300 trays**; filtration is at the CDU; some OEM DWC designs (HPE/Lenovo) carry inline strainers at the cabinet manifold | [KB-M / KB-L] | none |
| Minimum gap in volume | effectively **0.2-0.3 mm** (skived fins 0.2-0.3 mm thick, 0.2-0.3 mm gaps, 3-5 mm tall) | [KB-M; consistent with all S-grade sources] | - |

So the installed plate fleet already runs **W/d_abs ~ 2-3 against a 50 um nominal filter (d_abs ~ 90 um)**, i.e. in the "bridging" regime of Section 5 - and it works, because long 4 mm-tall skived channels at 0.7 m/s have enough shear to move 50 um particles and because the fin count is small enough that a few blocked channels are thermally invisible. That calibration (0.2 mm skived on 50 um nominal = ~10-year life) is the anchor the sibling fouling model uses.

## 5. Physics reconciliation

### 5.1 Channel width vs filter rating (W/d_abs regimes) [Calc, `fouling-filtration.out` B]

| Last filter the plate sees | d_abs (um) | W = 0.05 | 0.075 | 0.10 | 0.15 | 0.20 | 0.30 |
|---|---:|---|---|---|---|---|---|
| 25 um absolute (pleated, beta >= 200) | 25 | 2.0 bridging | 3.0 deposition | 4.0 deposition | 6.0 deposition | 8.0 safe | 12 safe |
| 50 um absolute mesh | 50 | 1.0 bridging | 1.5 bridging | 2.0 bridging | 3.0 deposition | 4.0 deposition | 6.0 deposition |
| 50 um nominal (typical CDU cartridge) | ~90 | 0.6 sieve | 0.8 sieve | 1.1 bridging | 1.7 bridging | 2.2 bridging | 3.3 deposition |
| 100 um nominal / Y-strainer | ~180 | sieve | sieve | sieve | sieve | 1.1 bridging | 1.7 bridging |

W_min by the 3x (no-bridging) rule: **0.075 mm behind 25 um absolute; 0.15 mm behind 50 um absolute; 0.27 mm behind 50 um nominal with no plate screen.** Relative life (0.2 mm skived on 50 um nominal = 10 y): 0.05 mm = 1-2 y; 0.075 mm = 2-3 y; 0.10 mm = 3-6 y; 0.15 mm = 6-12 y (no mechanism behind 25 um abs); 0.20 mm = 10-15 y.

### 5.2 Inertial impaction at the slot-to-channel turn [Calc, `fouling-filtration.out` A]

St = rho_p d^2 u / (18 mu W), 50 um Cu oxide (rho 6,000): **1.7 at W = 0.05 mm, 1.1 at 0.075, 0.83 at 0.10, 0.56 at 0.15, 0.42 at 0.20 mm** at 0.5 m/s entry; at the HMMC's actual channel velocity (0.04-0.1 m/s) St falls to 0.12-0.68, and at W >= 0.15 mm it is < 0.3, i.e. dense particles follow the streamlines instead of impacting fin tips. The CoolIT-like split-flow at 0.69 m/s and 0.2 mm has St = 2.3 for the same particle, but its shear (0.69 m/s in a 4 mm-tall channel) exceeds the removal threshold for 50 um particles, which is why it survives. The HMMC at 0.04-0.1 m/s has **no shear self-cleaning** (wall shear 0.3-6 Pa; drag on an attached 10 um particle 0.3-5 nN vs ~35 nN adhesion) and relies entirely on exclusion. This is the mechanistic reason the fine-gap HMMC needs a wider W/d than a skived plate does.

### 5.3 In-situ film fouling (no filter protects against this) [Calc, `fouling-filtration.out` D]

| gap/fin/H (mm) | clean avg dT (K) | delta = 10 um | 20 um | 30 um | channel-only dP factor at 10 um |
|---|---:|---|---|---|---:|
| 0.05/0.05/0.6 | 19.8 | +0.7 K, x1.22 | +2.8 K, x7.0 | blocked | x4.6 |
| 0.075/0.075/0.8 | 22.0 | +0.6 K, x1.04 | +1.5 K, x1.18 | +4.0 K, x3.2 | x2.5 |
| 0.10/0.10/1.0 | 24.1 | +0.7 K, x1.01 | +1.4 K, x1.04 | +2.5 K, x1.14 | x1.95 |
| 0.15/0.10/1.5 | 27.1 | +0.6 K | +1.1 K | +1.7 K | x1.54 |
| 0.20/0.20/4.0 (skived-like) | 28.7 | +0.9 K | +1.8 K | +2.8 K | x1.37 |

The thermal penalty of a film is small at every width (fin-area ratio dilutes it); the **hydraulic** penalty is cubic in (W - 2 delta) and is what kills < 0.1 mm channels: a 20 um biofilm/precipitate layer - which forms downstream of any filter - multiplies 0.05 mm channel dP by 7 and blocks it at 30 um.

### 5.4 What a blocked channel cluster costs [Calc, `fouling-filtration.out` E]

10 % of channels blocked at random: +0.9 K average, +0.5 K local per 0.1 mm channel, no change in plate dP. 10 % blocked **as a cluster**: +7 K per 2 mm slot segment, +17 K per 4 mm cluster, +49-76 K for a 10.8 mm strip (2 mm Cu base). Clustered blockage is a die-killer at 128 W/cm2 for any architecture; distributed blockage is benign. Clusters form at slot dead-ends (settling) and the first channels after the port (impaction), so the "10-20 % blockage tolerance" requirement must be tested as *clustered* blockage at those locations, not as random channel removal.

### 5.5 The thermal cost of the rule [Calc, `fouling-filtration.out` F; 15 kW, 18 LPM, PG25 45 C, paste TIM]

| Design | avg dT (K) | max dT (K) | dP (kPa) | Deployable behind |
|---|---:|---:|---:|---|
| CoolIT-like skived split-flow (benchmark reconstruction) | 34.5 | 44.3 | 8.6 core (22 total) | 50 um nominal (proven) |
| HMMC 0.05/0.05 x 0.6 ("ultrafine") | 19.8 | ~24 | ~6.7 | nothing available |
| HMMC 0.075/0.075 x 0.8 ("fine") | 22.0 | ~26 | ~6.3 | nothing available (W/d = 3 only behind 25 um abs; St > 1) |
| HMMC 0.10/0.10 x 1.5 | 22.9 | 26.9 | 6.2 | <= 33 um absolute loop filtration only |
| **HMMC gap 0.15 / fin 0.10 x 2.0** | **26.1** | **30.1** | **6.1** | 50 um absolute plate screen; any CDU |
| HMMC gap 0.15 / fin 0.12 x 2.5 | 25.7 | 29.7 | 6.1 | same |
| HMMC 0.15/0.10 x 2.0 + 5 % header bleed | 26.5 | 30.5 | 6.1 | same (self-flushing dead-ends) |
| HMMC 0.15/0.10 x 2.0, liquid-metal TIM | 21.6 | 25.6 | 6.1 | same |

**The gain attributable to sub-0.15 mm gaps is 2.0 K (0.10 mm), 4.1 K (0.075 mm) and 6.3 K (0.05 mm) of average dT** - the "3-5 K" in the task statement is confirmed at 2-4 K for the realistic candidates. The step from the benchmark's 34.5 K to 26.1 K (8.4 K, 24 %) comes from the manifold (2 mm flow length) and a thinner base/TIM, and survives the filtration rule intact. Recovering the 4 K from a 0.075 mm gap is cheaper and safer through the interface (liquid-metal TIM: -4.5 K) than through the channel.

### 5.6 Strainer dP adder [Calc, `fouling-filtration.out` C and G; Ergun (conservative) values, 18 LPM]

| Screen | Effective area | Clean dP (kPa) | at 80 % open | at 50 % open | Pores / channel inlets |
|---|---:|---:|---:|---:|---:|
| 25 um pleated | 10 cm2 | 1.75 | 5.6 | 40 | 14x (W = 0.1), 17x (W = 0.15) |
| 25 um pleated | 20 cm2 | 0.78 | ~2.5 | ~18 | ~30x |
| 25 um pleated | 50 cm2 | 0.29 | ~0.9 | ~7 | ~70x |
| 25 um pleated | 117 cm2 (full plate) | 0.12 | 0.40 | 3.0 | 160-200x |
| 50 um mesh | 5 cm2 | 1.9 | 6.4 | 47 | 2-3x (too few) |
| 50 um mesh | 30 cm2 | ~0.2 | ~0.7 | ~5 | ~15x |
| 25 um, port-sized | 1 cm2 | 17-51 | - | - | unacceptable |

Rule: integrated screen area >= 20 cm2 for 25 um (>= 30 cm2 for 50 um), pore count >= 100x the channel-inlet count, clean dP < 0.5-0.8 kPa, service alarm at 3x clean dP (~2-3 kPa), **spec budget 2-5 kPa**. Loading, not clean dP, is the constraint: at a loop concentration of 1e-3 particles/mL above the screen rating, a 117 cm2 25 um screen reaches 50 % blinding in ~90 days, a 10 cm2 one in ~8 days. A plate screen finer than the CDU filter *becomes the loop's filter* and inherits its service interval - this is the operational reason a 25 um plate screen is not a free fix for the 0.075-0.10 mm channel.

## 6. Resolution: the rule, the SKUs, and the drop-in verdict

**Design rule (unchanged under any plausible filtration rating):**

1. Primary channel gap **>= 0.15 mm** (fins 0.10-0.12 mm, 1.5-2.5 mm tall), i.e. >= 3x a 50 um absolute screen and >= 6x a 25 um absolute loop filter. Expected relative life 0.6-1.2x a proven 0.2 mm skived plate on the same loop.
2. Plate-integral **50 um absolute (wire-mesh) screen**, >= 30 cm2, removable cartridge in the inlet fitting or at the tray/rack manifold, dP tap for monitoring. This makes the plate indifferent to whether the CDU element is nominal or absolute.
3. Hierarchical passages: port >= 3 mm, level-1 manifold >= 1 mm, level-2 slots >= 0.3 mm, channels 0.15 mm, metering orifices >= 0.4 mm, each stage > 2x the next so nothing sieves before the channels.
4. No dead-end sieving headers under the die: 5 % slot-end bleed through >= 0.6 mm orifices (slot-end velocity 0.62 m/s = 28x the settling velocity of 100 um Cu oxide); thermal cost +0.4 K.
5. Port-adjacent channels and slot ends placed outside the die footprint, or demonstrated by test to tolerate a 4 mm cluster (+17 K locally) without exceeding Tj.
6. Materials: all-copper wetted path, Ni only where the compatibility soak demands it (Ni flakes are the densest particle class), no aluminium, factory flush to a stated residue mass, low-shedding peroxide-cured EPDM, biocide-containing inhibited PG25 at pH 8-9.5.

**SKU structure:**

| SKU | Gap | avg dT at 15 kW / 18 LPM | Requires | Drop-in to installed CDU fleet? |
|---|---|---:|---|---|
| Standard | 0.15 mm | 26.1 K (25.7 with 0.12 x 2.5 fins) | plate 50 um abs screen | **Yes** - any CDU at 50 um nominal or absolute, no operator change |
| Standard + LM TIM | 0.15 mm | 21.6 K | same + liquid-metal interface | Yes |
| Performance | 0.10 mm | 22.9-24.1 K | loop filtration <= 33 um absolute **or** plate 25 um abs screen >= 50 cm2 serviced on dP | **No** - makes the plate the loop's filter; hyperscaler custom-ASIC programmes only (Google-class isolated loops, 80 psi head) |
| Ultrafine / fine | 0.05-0.075 mm | 19.8-22.0 K | no available filtration standard; St > 1; film-fouling x3-7 dP | **No** - remove from the roadmap unless a 10-15 um absolute loop standard emerges |

**Why this is robust to the unread PDFs.** If OCP PG25 Guidelines / NVIDIA turn out to specify 25 um: the Standard SKU gains margin (W/d = 6, no deposition mechanism) and the Performance SKU becomes drop-in behind a beta-rated 25 um element. If they specify 50 um nominal (the expected case): the Standard SKU is exactly at the proven skived-plate calibration point once its own 50 um absolute screen is counted. If they specify only particle-count classes (ISO 4406-style) with no micron rating: the plate screen is still what sets d_abs for the channels, and the loop class sets the screen's service interval (Section 5.6). In no case does 0.05-0.075 mm become deployable.

## 7. Making the rule evidence-based: the plate-level qualification test

Because no vendor publishes clogging data and the OCP Cold Plate Test Spec v1.0.0 (Oct 2026, CoolIT primary author) covers thermal, dP, burst, leak and cycling but (as far as captured) not particulate tolerance [Sib-URL], a published particulate-challenge result is a differentiator against the benchmark:

1. **Clean-loop baseline**: R and dP at 6 flow points per OCP v1.0.0.
2. **Graded-particle challenge** (ISO 12103-1 A3/A4 test dust plus 50-100 um copper and 100-300 um EPDM shreds), dosed upstream of the plate screen at 1e-3 and 1e-2 particles/mL above 50 um, 500 h recirculation at 1.2 LPM/kW, 45 C: record screen dP, plate dP and R every 24 h; pass = R drift < 5 %, plate dP drift < 10 %, screen dP < 3x clean at 500 h.
3. **Screen-bypass worst case**: same dose with the plate screen removed (simulates a torn element) to measure the clustered-blockage hot spot with IR on a glass-lidded TTV; pass = no 4 mm cluster forms within the die footprint in 100 h.
4. **In-situ film**: 2,000-3,000 h aged-PG25 soak at 65 C (inhibitor-depleted, bacteria seeded) per the UTA protocol class; pass = channel dP < 1.3x clean.
5. **Back-flush recovery**: reverse flow at 2x rated for 10 min restores dP to < 1.1x clean.

Items 2-3 give exactly the "demonstrated tolerance to 10-20 % channel blockage" the standards recommendation asks for, with the clustering caveat of Section 5.4 built in.

## 8. Retrieval plan for the next session with search budget (14 queries, priority order)

1. extended: `"OCP-PG25-Guidelines-V1.0.0" "particle" "micron" OR "um" "action limit"` - the single most consequential number.
2. extended: `"OCP" "cold plate requirements" ORv3 OR ACS "particulate" OR "filtration" "um"`.
3. extended: `CoolIT CHx2000 OR CHx1500 OR CHx1000 datasheet "filter" "micron"`.
4. extended: `Vertiv CoolChip CDU OR "Liebert XDU" datasheet "filtration" "micron"`.
5. extended: `"Project Deschutes" CDU OCP specification "filtration" OR "filter" "micron"`.
6. extended: `nVent CDU datasheet "50 micron" OR "25 micron" secondary`.
7. extended: `Motivair CDU datasheet "micron" filter secondary`.
8. extended: `NVIDIA "GB200 NVL72" OR "GB300" "liquid cooling" guide "filtration" "micron" OR "um"`.
9. extended: `Lenovo Neptune OR "ThinkSystem" "water quality" "50 micron" OR "50 um" filtration; HPE Cray EX "cooling" "micron" filter`.
10. extended: `ASHRAE TC 9.9 "Water-Cooled Servers" water quality table "filtration" "micron"`.
11. extended: `Ecolab CoolIT Walicki Electronics360 "flush" OR "flushing" particulate cold plate` (full text).
12. extended: `Uptime Institute 2025 OR 2026 survey "direct liquid cooling" incidents clogging OR "blocked" OR fouling`.
13. extended: `"University of Texas at Arlington" OR UTA cold plate PG25 "degradation" OR "fouling" "pressure drop" increase hours` (ITherm / InterPACK 2023-2026).
14. extended: `"cold plate" "blocked" OR "clogged" channels PG25 field failure 2025 2026; "skived" fin "0.1 mm" OR "100 um" clogging`.

If WebFetch stays DNS-blocked, ask the orchestrator for the OCP PG25 Guidelines, OCP cold-plate test spec and two CDU datasheets as uploads; a 15-minute read closes rows 1-8 of Section 2.

## 9. Gaps / unknowns

1. **No filtration micron rating was verified from any primary document this session** (zero searches, one failed fetch). Every product-level rating in Section 2 is background knowledge [KB-L/M].
2. OCP PG25 Guidelines V1.0.0: particle-count action limits exist [Sib-URL snippet] but their values, the ISO class used and any micron rating are unread.
3. Whether CDU secondary elements are nominal cartridges or absolute meshes (this moves d_abs from ~50 to ~90 um) is unknown per vendor.
4. NVIDIA's GB200/GB300/Rubin cold-plate and TCS water-quality requirements are NDA; no public micron number exists on disk.
5. No quantitative field clogging data (rates, time-to-failure, particle sources by mass) exists in the public domain on disk; Ecolab's statement is qualitative; Uptime incident statistics were not retrievable.
6. UTA PG25 degradation numbers (R and dP drift vs hours, particle counts) not captured; only the thesis URL.
7. Shipping GB200/GB300 fin geometry is known only from S-grade reseller blogs (<= 0.5 mm fins, < 0.3 mm channels); Group-A drawings are NDA; the 0.2-0.3 mm "volume minimum" is inference.
8. The sibling fouling model's absolute lifetimes rest on one calibration point (0.2 mm skived on 50 um nominal = 10 y) and a Wyss-type clogging law with 10x uncertainty in both the sticky-particle constant and loop cleanliness; only the *relative* ordering of channel widths is robust.
9. Screen dP values use the conservative (Ergun) end of a 3-7x spread between correlations at Re_d < 50; measure on hardware before fixing the 2-5 kPa budget.
10. The electroless-Ni thickness gradient inside 0.15 mm channels (plating consumes 2 x 5-15 um of gap) was not modelled; plate before fin closure or qualify bare copper.

## Sources

Sibling-verified URLs reused (retrieved earlier in this run; none re-fetched here):
- OCP PG25 Guidelines V1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
- OCP Base Specification PG25 v1.0.0: https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/
- OCP Single-Phase D2C Cold Plate Test Specification V1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- OCP L-L CDU Test Methodology & Performance Rating r1: https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- OCP ACS Cold Plate Leak Detection and Intervention white paper: https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1
- Schneider Electric, filter dP in CDU ratings (16 Dec 2025): https://blog.se.com/datacenter/2025/12/16/account-for-filtering-too-beware-of-how-cdu-rating-capacity-is-specified/
- Electronics360 Q&A with Ecolab (7 Oct 2026): https://electronics360.globalspec.com/article/24164/q-a-ecolab-bets-on-liquid-cooling-for-ai-data-center-growth
- Ecolab-CoolIT acquisition deck (Mar 2026): https://s204.q4cdn.com/218790897/files/doc_downloads/2026/03/Ecolab-to-Acquire-CoolIT-Systems.pdf ; https://www.businesswire.com/news/home/20260319353197/en/
- Google liquid cooling at Hot Chips 2025 (isolated loops, filtration, 99.999 % CDU availability): https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips
- Google Project Deschutes CDU (2 MW, 80 psi): https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/ ; https://cloud.google.com/blog/topics/systems/enabling-1-mw-it-racks-and-liquid-cooling-at-ocp-emea-summit ; Nidec Deschutes sheet: https://www.nidec.com/v=1764743613/files/topics/19006_ext_5_en_0.pdf ; nVent Deschutes (OCP): https://www.opencompute.org/?p=1743
- CoolIT CHx2000 (53 psi): https://www.coolitsystems.com/cdu-product/chx2000/ ; CHx1500 (44 psi): https://www.storagereview.com/news/coolit-chx1500-delivers-1500kw-of-precision-liquid-cooling ; CHx1000: https://www.hpcwire.com/2024/12/10/ai-performance-reliability-serviceability-with-coolits-chx1000-cdu/
- Vertiv CoolChip CDU: https://www.vertiv.com/zh-CN/products-catalog/thermal-management/high-density-solutions/vertiv-coolchip-cdu/
- nVent + NVIDIA reference architecture (Nov 2024): https://businesswire.com/news/home/20241118649897/en/nVent-Collaborates-with-NVIDIA-on-AI-Ready-Liquid-Cooling-Solutions/
- QCT GB200 NVL72 whitepaper (45 C in / 65 C out, ~130 LPM): https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf
- Uptime Institute (40 C GPU supply limit): https://intelligence.uptimeinstitute.com/entity_pdf/node/153594/pdf
- UTA thesis, degradation of copper cold plates in PG25: https://uta-ir.tdl.org/uta-ir/handle/10106/31381
- Data Centre Review (Aug 2026, unread): https://datacentrereview.com/2026/08/how-to-build-reliable-liquid-cooling-systems/
- FiberMall GB200 plate blog (fins <= 0.5 mm, >= 3 mm): https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm
- Naddod GB300 blog (< 0.3 mm channels; low reliability): https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling
- ToneCooling GB300 plate (0.013 K/W, 12.06 kPa): https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/
- USUSTK skived fin (0.06 mm fins / 0.10 mm pitch): https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink
- JetCool "filtration challenges" language: https://jetcool.com/post/understanding-direct-to-chip-liquid-cooling-approaches-and-performance-tradeoffs/
- Chilldyne negative-pressure loop: https://www.storagereview.com/review/high-performance-leak-free-liquid-cooling-chilldynes-cdu-and-cold-plates-in-action
- Motivair Dynamic Cold Plates: https://www.motivaircorp.com/products/dynamic-cold-plates/

Project files drawn on: `appendix/physics/fouling-filtration.py`, `.out`, `.md`; `research/standards-reliability.md` (sections 5.3, 7); `research/gap-ocp-test-spec-and-boundary-docs-full-read.md` (section 4); `research/chip-roadmap-requirements.md` (section 3.4); `research/manufacturing-cost.md`; `research/coolit-products.md`; `research/competitors-singlephase.md`; `research/gap-competitor-plate-datasheets-gb300-rubin-scale.md`.

Background-knowledge items named without URL (verify before use in a spec): ASHRAE TC 9.9 "Water-Cooled Servers" (2019) and Liquid Cooling Guidelines TCS water-quality table; OCP ACS/ORv3 Cold Plate Requirements; CoolIT CHx, Vertiv XDU/CoolChip, Motivair, nVent CDU datasheet filter ratings; Lenovo Neptune / HPE Cray EX / Dell DLC water-quality specifications; NVIDIA GB200/GB300 liquid-cooling guides; ISO 4406 / ISO 12103-1 test-dust classes; Wyss et al. (2006) successive-deposition clogging law.
