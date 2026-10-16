# Gap report: NVIDIA (GB300 / Vera Rubin / Rubin Ultra) plate-level envelope and package geometry, plus AMD MI455X, Google Ironwood, Trainium 3, Maia 200, and the origin of "1.2 LPM/kW"

Prepared 2026-10-13 for the cooling-architecture programme (benchmark: CoolIT 15 kW coldplate tech brief, June 2026).

## 0. Provenance and method (read first)

- **No live web search was possible in this task.** All 13 queries issued were refused because the per-turn WebSearch budget (200 calls, shared by every agent in the workflow) was already exhausted; WebFetch/curl are network-blocked in this container. I did not work around the limit. Section 10 lists the exact documents and queries to run when the budget resets.
- Sources used, in order of priority:
  1. **[Brief]** the CoolIT 15 kW tech brief (local extract).
  2. **[Sib]** facts already retrieved *with URLs* by sibling agents in this workflow (`chip-roadmap-requirements.md`, `coolit-briefs-numbers.md`, `coolit-products.md`, `competitors-singlephase.md`, `competitors-advanced.md`, `standards-reliability.md`, `test-metrics.md`, `ip-landscape.md`, `manufacturing-cost.md`, `gap-coolit-15kw-ttv-footprint-heater-map.md`, `physics/nonuniform-heatmap.md`). The URL is repeated here wherever a number is used.
  3. **[KB]** my own knowledge base (training data to ~June 2026), **not verified in this session**, tagged H/M/L confidence. KB-L numbers are leads, not requirements.
  4. **[D]** derived by me (energy balance, geometry arithmetic; script `gap_envelope_calc.py` in this directory).
- Vendor claims are tagged (V), independent/standards (I), analyst (A), secondary press (S).

The honest headline: **NVIDIA has never published a plate-level thermal or hydraulic requirement for GB200/GB300/Rubin in any public document that any agent in this workflow has found.** What exists publicly is rack-level (supply/return temperature, approximate rack flow), a 45 C design-inlet statement for Rubin-class MGX, and secondary-vendor plate numbers that are not NVIDIA's. The envelope below is therefore assembled, not copied, and each line carries its confidence.

## 1. One-line answers to the ten questions in the angle

| # | Question | Best answer | Confidence |
|---|---|---|---|
| 1 | Per-plate / per-tray flow (LPM/kW) NVIDIA requires | Not public. Public rack-level evidence brackets **~1.0 LPM/kW nominal** (QCT/DCD: up to ~130 LPM for a 120-132 kW GB200 NVL72) with a **0.75 LPM/kW floor** implied by the 45 C in / 65 C out envelope. Vendor plate "datasheets" (1.6-1.7 LPM/kW) are not NVIDIA numbers. | Medium (rack), Low (plate) |
| 2 | dP allowance | Not public. The 12-150 kPa spread in secondary sources is a **level-mixing artefact**: ~12-40 kPa is the *plate* level (vendor GB200/GB300 plates), ~55 kPa is a *loop incl. QDs* (CoolIT 4 kW), ~124 kPa (18 psi) is a *rack TCS* worked example, 150 kPa (1.5 bar, Introl) is rack-level. Working plate budget: **<= 25-35 kPa at nominal flow**. | Medium |
| 3 | TCS supply/return temperatures | GB200 NVL72: **max supply 45 C, max return 65 C** (QCT whitepaper; DCD quoting NVIDIA) [Sib]. Vera Rubin MGX gen-3: **"designed for 45 C" liquid cooling** (NVIDIA OCP Oct-2025 blog via TechPowerUp) [Sib]. | High |
| 4 | Tcase / Tj limits | Not published per plate. NVIDIA data-centre GPUs report via nvidia-smi: A100/H100 class **max operating ~85 C, slowdown ~87-89 C, shutdown ~92-93 C; HBM max ~95 C** [KB-M]. CoolIT's "Tcase 80 C" convention [Brief] is therefore not a NVIDIA number; it is ~5-10 K below throttle at the die top. | Medium |
| 5 | Mounting load and flatness | NDA (NVIDIA thermal/mechanical design guides). Generic practice: bare-die contact pressure ~0.15-0.35 MPa (20-50 psi) over the die, lidded ~0.3-0.7 MPa; plate flatness <= 25-50 um over the footprint, Ra <= 0.8 um; 100-130 mm substrates warp 100-300 um over temperature [Sib standards-reliability; KB-M]. | Low-Medium |
| 6 | Lidded vs bare-die; gold-plated lid vs microchannel lid timing | NVIDIA data-centre GPUs through Blackwell are **bare-die with a stiffener ring** [KB-M]. Rubin: analyst (Kuo, Jan 2026) says Max-Q 1.8 kW uses "micro-channel cold plate + gold-plated lid"; **microchannel lid for 2.3 kW not before 2H 2027** [Sib ctee/cls]. Rubin Ultra: NVIDIA reported seeking microchannel-lid / direct-to-chip partners (Digitimes Sep 2025, Wccftech) [Sib]. Interpretation in section 7. | Low-Medium |
| 7 | Package edge length | Not public. TSMC CoWoS-L roadmap: 5.5x-reticle on **~100 x 100 mm substrate (2026, up to 12 HBM)** and 9.5x-reticle on **~120 x 150 mm substrate (2027)** [KB-M] -> Rubin ~100 mm class, Rubin Ultra ~120 x 150 mm class. | Medium |
| 8 | Die count / area, HBM count | Rubin: **2 reticle dies, 8 x HBM4 (288 GB)**; Rubin Ultra: **4 reticle dies, 16 x HBM4e (1 TB)** (NVIDIA GTC-2025 roadmap, via DCD/Igor's Lab) [Sib; KB-H]. Logic area ~16.5 cm2 (Rubin) / ~33 cm2 (Rubin Ultra) [D]. | High (counts), Medium (area) |
| 9 | HBM4-vs-logic height step | JEDEC HBM4 raised max stack package height to **775 um** for 12/16-high (HBM3/3E: 720 um) [KB-M]. Logic-die top height depends on NVIDIA/TSMC thinning (not public). Expected step **0 to +/-0.15 mm**, sign *not* guaranteed negative any more. The sibling TTV-B assumption of HBM 0.4 mm below the die top is an overestimate for any lidded package and a plausible upper bound only for bare-die with thick TIM1. | Low |
| 10 | Official TDPs | **Official**: B200 (HGX) 1,000 W; GB200 GPU 1,200 W (superchip 2,700 W); B300/GB300 1,400 W; MI355X 1,400 W; Maia 200 750 W. **Analyst / secondary only**: Rubin 1.8 / 2.3 kW; Rubin Ultra ~3.6 kW; MI455X ">2 kW"; Ironwood (not disclosed; ~10 MW per 9,216-chip pod -> ~1.1 kW all-in); Trainium 3 (not disclosed). | see section 2 |
| 11 | Origin of "1.2 LPM/kW" | **A CDU rating convention, not a silicon-vendor or OCP plate requirement.** CoolIT's own CHx2000 (Apr 2025) is rated "2,000 kW at 5 C approach at 1.2 LPM/kW"; its CHx1000 and the OCP L-L CDU methodology use 1.5 LPM/kW; Electronics Cooling (Jun 2025) calls 1.2 LPM/kW at 45 C "a common industry standard that many CDUs available today can meet" [Sib]. Physically it is the flow for a ~12.6 K rise in PG25 (12.1 K water), i.e. the top of the OCP OAI 7.5-12 K rise window [D]. | High |

## 2. TDPs: official vs analyst (the number the plate is sized to)

| Device | Platform / date | TDP | Status | Source |
|---|---|---|---|---|
| H100 SXM5 | HGX, 2022-23 | 700 W | official | NVIDIA datasheet [KB-H] |
| B200 | HGX B200, 2024-25 | 1,000 W | official | NVIDIA HGX B200 [KB-H] |
| B200 in GB200 | GB200 NVL72 | 1,200 W (superchip 2 GPU + Grace = 2,700 W) | official (NVIDIA GTC 2024) | [KB-H]; TrendForce rack TDP https://www.trendforce.com/presscenter/news/20240730-12232.html [Sib] |
| B300 / Blackwell Ultra | GB300 NVL72, 2025-26 | 1,400 W | official (NVIDIA GTC 2025 materials) | https://www.tweaktown.com/news/103938/ [Sib]; [KB-H] |
| Rubin (VR200) | Vera Rubin NVL144 (=72 packages), 2H 2026 | 1,800 W (Max-Q) / 2,300 W (Max-P); DCD "up to 2,300 W" | **analyst** (Ming-Chi Kuo, Jan 2026) | https://www.ctee.com.tw/news/20260107701081-430704 ; https://www.cls.cn/detail/2250526 ; DCD via coolit-briefs-numbers.md [Sib] |
| Rubin Ultra | Kyber NVL576, 2H 2027 | ~3,600 W per package; rack ~600 kW (rack figure is NVIDIA's) | **analyst** for the package; rack kW official (GTC 2025) | https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/ ; https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027 [Sib] |
| Feynman | 2028 | none public | - | - |
| AMD MI355X | 2025 | 1,400 W | official (AMD) | [KB-H] |
| AMD MI455X | Helios, 72 GPU rack, 2026 | ">2 kW" (secondary); not found in AMD materials | **secondary** | https://introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026 ; https://wccftech.com/amd-helios-ai-rack-mi455x-6th-gen-epyc-challenging-nvidia/amp/ [Sib] |
| Google Ironwood (TPU v7) | 2025 | not disclosed; 9,216-chip pod ~10 MW -> ~1.09 kW/chip *all-in* (host, network, cooling included); chip TDP plausibly 0.7-0.9 kW | **derived / KB-L** | STH Hot Chips 2025 https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/ [Sib]; pod MW [KB-M] |
| AWS Trainium 3 | Trn3 UltraServer (144 chips), Dec 2025 | not disclosed; first liquid-cooled Trainium | **KB-L** | - |
| Microsoft Maia 200 | Jan 2026 | 750 W, liquid-cooled (closed-loop sidekick HX) | official (Microsoft blog) [KB-M] | - |

Rack-level cross-checks [D, PG25]: 72 x 2.3 kW = 166 kW GPU-only, consistent with Kuo's ~230 kW VR NVL72 Max-P rack; 144 x 3.6 kW = 518 kW GPU-only, consistent with NVIDIA's ~600 kW Kyber. So the analyst package TDPs are at least rack-consistent even though NVIDIA has not stated them.

## 3. Package geometry (what the plate has to cover)

| Package | Logic silicon | Logic area [D] | HBM | Substrate / interposer class | Edge length | Form at the plate interface | Confidence |
|---|---|---|---|---|---|---|---|
| H100 (GH100) | 1 die, 814 mm2 | 8.1 cm2 | 5 (6 sites) x HBM3 | CoWoS-S ~2.5x reticle | ~70 mm class (not public) | **bare die + stiffener ring** (SXM5 and PCIe) | KB-M |
| B200 / B300 | 2 reticle dies (~800 mm2 each) | ~16 cm2 | 8 x HBM3e (12-high on B300) | CoWoS-L, ~3.3x reticle, LSI bridges | ~85-95 mm class (not public) | **bare die + stiffener** (GB200 superchip and GB300 "SXM puck") | KB-M |
| Rubin | 2 reticle dies (~830 mm2 each, N3 class) | ~16.6 cm2 | **8 x HBM4** (288 GB) | CoWoS-L 5.5x-reticle class, ~100 x 100 mm substrate | ~100 mm class | reported: gold-plated lid + microchannel cold plate (Max-Q); microchannel lid later (A) | counts KB-H; size KB-M; lid A |
| Rubin Ultra | **4 reticle dies** | ~33 cm2 | **16 x HBM4e** (1 TB) | CoWoS-L 9.5x-reticle class, ~120 x 150 mm substrate (TSMC 2027 roadmap) | ~120 x 150 mm class | undecided publicly; microchannel lid / direct-to-chip rumoured | counts KB-H; size KB-M |
| AMD MI455X | 8 XCD (N2) 3D-stacked on 2 AID (N3P) | ~11-12 cm2 of XCD (stacked; flux concentrated) | **12 x HBM4** (432 GB = 12 x 36 GB), 19.6 TB/s | CoWoS-L class | ~100 mm class (not public) | lidded (MI300/MI350 lineage) | KB-M |
| Google Ironwood | 2 compute dies | not public | 8 x HBM3e (192 GB, 7.4 TB/s) | CoWoS class | not public | **bare die** (Google: bare-die plates since TPU v4) | STH/Chips&Cheese [Sib]; KB-M |
| Microsoft Maia 200 | 1 die, TSMC N3 | ~8 cm2 (est.) | 6 x HBM3e? (216 GB) | CoWoS-S class | not public | not public | KB-L |
| AWS Trainium 3 | 1-2 dies, TSMC N3 | not public | HBM3e (144 GB class) | - | not public | not public | KB-L |

Die-average heat flux [D] with the HBM share removed (HBM3e 30 W/stack, HBM4 ~45 W/stack, both KB-M): B200 ~60 W/cm2, B300 ~72, Rubin 1.8 kW ~89, Rubin 2.3 kW ~117, Rubin Ultra 3.6 kW ~87, MI455X ~150+ (stacked XCDs), Maia 200 ~70. CoolIT's TTV (117 cm2 model calibration) is ~128 W/cm2 uniform. **No 2026-27 package has a die-average flux above ~160 W/cm2; the 300-400 W/cm2 figures are local hot spots** (SM/tensor clusters, 10-20 % of die area), not package averages.

## 4. The TCS envelope, reconciled by level

The order-of-magnitude dP spread and the 2x flow spread in prior reports disappear once each number is assigned to its level (plate / tray-loop / rack / CDU). Everything below is public or vendor data; NVIDIA's own plate spec remains NDA.

### 4.1 Temperatures

| Item | Value | Source |
|---|---|---|
| GB200 NVL72 facility/TCS supply | max **45 C**; max return **65 C**; up to ~130 LPM/rack | QCT whitepaper https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf ; DCD https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus [Sib] |
| GTC 2024 keynote (GB200 NVL72) | "25 C in, 45 C out, 2 L/s" (=120 LPM) | [KB-H] (widely quoted keynote line; not a spec) |
| Vera Rubin NVL144 MGX gen-3 | "designed for 45 C" liquid cooling, 100 % liquid, cable-free tray | https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production (citing NVIDIA OCP Oct-2025 blog) [Sib] |
| Kyber / Rubin Ultra | 45 C warm-water target stated by NVIDIA at GTC 2025 (keynote), 800 VDC, sidecar cooling rack | competitors-advanced.md [Sib]; [KB-M] |
| OCP L-L CDU methodology envelope | TCS 17-65 C | https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/ [Sib] |
| ASHRAE classes | W45 = 45 C supply allowable | https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/ [Sib] |

### 4.2 Flow (specific flow and per-package flow)

Energy balance, PG25 (rho 1.02 kg/L, cp 3.90 kJ/kg-K) [D]: 0.75 LPM/kW -> 20.1 K rise; 1.0 -> 15.1 K; 1.2 -> 12.6 K; 1.5 -> 10.1 K; 2.0 -> 7.5 K. (Water: 19.3 / 14.5 / 12.1 / 9.7 / 7.2 K.)

| Evidence | Specific flow | Level | Source |
|---|---|---|---|
| NVIDIA 45 in / 65 out envelope | 20 K max rise = **0.75 LPM/kW floor** | rack | QCT/DCD [Sib]; [D] |
| QCT: up to ~130 LPM at 120-132 kW with ~85 % liquid capture | **~1.0-1.2 LPM/kW** of liquid-captured heat | rack | QCT [Sib]; [D] |
| GTC-2024 "2 L/s" at 120 kW | ~1.0 LPM/kW | rack | [KB-H] |
| CoolIT CHx2000 rating | 1.2 LPM/kW | CDU | https://www.coolitsystems.com (CHx2000, Apr 2025) via coolit-products.md [Sib] |
| CoolIT CHx1000 rating; OCP L-L CDU methodology | 1.5 LPM/kW | CDU | https://hpcwire.com/2024/12/10/ai-performance-reliability-serviceability-with-coolits-chx1000-cdu/ ; OCP L-LCDU [Sib] |
| Electronics Cooling (Jun 2025) | 1.2 LPM/kW at 45 C "common standard many CDUs can meet"; 96 LPM for an 80 kW rack | CDU/rack | https://www.electronics-cooling.com/2025/06/direct-liquid-cooling-for-high-compute-servers/ [Sib] |
| OCP OAI guideline | 7.5-12 K coolant rise (1-2 LPM per OAM) | module | coolit-briefs-numbers.md [Sib] |
| Vendor GB200 superchip plate (FiberMall) | 1.8 LPM per 2.7 kW plate = 0.67 LPM/kW | plate (S, unreliable) | https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm [Sib] |
| Vendor GB300 GPU plate (ToneCooling) | 1.7 LPM at ~1.07 kW = 1.6 LPM/kW; 0.013 K/W; 12 kPa | plate (V) | https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ [Sib] |
| Frore Rubin claim | 0.87 LPM/kW (vs "1.41 conventional") | plate (V, S) | https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/ [Sib] |
| Introl | ~80 LPM/rack, 1.5 bar | rack (S) | competitors-singlephase.md [69] [Sib] |

Per-package flow at the candidate specific flows [D]: Rubin 2.3 kW -> 1.7 / 2.3 / 2.8 / 3.5 LPM at 0.75 / 1.0 / 1.2 / 1.5 LPM/kW; Rubin Ultra 3.6 kW -> 2.7 / 3.6 / 4.3 / 5.4 LPM; a 15 kW TTV -> 11.3 / 15 / 18 / 22.5 LPM. Rack flow at 1.0 LPM/kW: GB300 NVL72 ~125 LPM, VR NVL72 Max-P ~230 LPM, Kyber ~600 LPM (hence the move from 1/4-in to 1/2-in UQD08-class couplings reported for >200 kW racks, LinkedIn/unverified [Sib]).

**Conclusion on flow:** NVIDIA's public envelope is *rack-level* and sits at ~1.0 LPM/kW nominal with a 0.75 LPM/kW floor; 1.2 and 1.5 LPM/kW are CDU rating points; 1.6-1.7 LPM/kW per plate is a vendor marketing point; 0.6-0.67 LPM/kW figures are either unreliable or GPU-only accounting. The programme should fix **1.0 LPM/kW as the design point** and publish curves at 0.6, 0.75, 1.0, 1.2 and 1.5 LPM/kW (the 1.2 point is needed only to compare with the CoolIT brief).

### 4.3 Pressure drop, by level

| Level | Public figure | Source |
|---|---|---|
| Plate (GPU, ~1.1-2.7 kW) | <20 kPa at 1.8 LPM (GB200 superchip, S); 12 kPa at 1.7 LPM, "design target <40 kPa at 3 LPM" (GB300 GPU plate, V); 35 kPa at 2.5 LPM (alt.) | FiberMall; ToneCooling [Sib] |
| Plate + fittings + QDs (loop) | ~8 psi / 55 kPa at ~6 LPM (CoolIT 4 kW) | https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf [Sib] |
| Rack TCS loop (manifolds, QDs, trays) | ~18 psi / 124 kPa worked example at 1.2 LPM/kW; Introl 1.5 bar (150 kPa) | Electronics Cooling Jun 2025; Introl [Sib] |
| CDU secondary head available | CoolIT CHx1000 35 psi; CHx1500 44 psi; CHx2000 **53 psi** (365 kPa); OCP L-L CDU >= 40 psi at 1.5 LPM/kW; Google Deschutes **80 psi** (550 kPa) "to enable advanced cold plate designs"; OCP allows TCS components to see up to 100 psi | coolit-products.md; OCP L-LCDU; https://cloud.google.com/blog/topics/systems/enabling-1-mw-it-racks-and-liquid-cooling-at-ocp-emea-summit [Sib] |
| OCP cold-plate test spec v1.0.0 | dP reported at 45 +/- 2 C at >= 6 points from 25 % to 150 % of rated flow | https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf [Sib] |

Reading [D]: with ~124 kPa at the rack manifold and 30-40 % consumed by manifolds, QDs and hoses, a tray sees ~75-85 kPa; a GPU plate in a two-plate series string gets ~30-40 kPa, a plate in parallel ~60-80 kPa. That is exactly the 12-40 kPa band the vendor plates quote. So the plate-level budget is **not** 12-150 kPa; it is **~15-40 kPa at nominal flow**, and the programme's working requirement (plate-only <= 25 kPa at 1.0 LPM/kW, <= 35 kPa at 1.2 LPM/kW on the 15 kW TTV; tray <= 100 kPa including UQD08) is consistent with every public number. The 80 psi Deschutes head is a hyperscaler-ASIC (Google) option, not an NVIDIA one.

Hydraulic pumping power per rack [D]: 130 LPM at 124 kPa = 0.27 kW; 230 LPM at 124 kPa = 0.48 kW; 600 LPM at 124 kPa = 1.24 kW, at 276 kPa = 2.8 kW. Rack pumping is 0.2-0.5 % of rack power at today's budgets; it is the *CDU count and manifold/QD size* (proportional to LPM), not pump energy, that a lower-flow plate buys. See section 8.

## 5. Where "1.2 LPM/kW" comes from

1. It is **CoolIT's CDU rating basis**: CHx2000 (Apr 2025) is rated 2,000 kW at 5 C approach at 1.2 LPM/kW (53 psi head, ~2,400 LPM secondary) [Sib coolit-products.md]. CoolIT's previous "semiconductor industry recommended" number (4 kW brief, Mar 2025) was 1.5 LPM/kW, which is the CHx1000 rating and the OCP L-L CDU methodology basis [Sib]. The wording moved with the product.
2. It is the flow that gives a **~12-12.6 K coolant rise** (PG25 / water), i.e. the top of the OCP OAI 7.5-12 K recommended rise window [D; Sib].
3. Electronics Cooling (Jun 2025) describes it as "a common industry standard that many CDUs available today can meet" for 45 C inlet [Sib].
4. **No NVIDIA, OCP or ASHRAE document codifies it** (all sibling searches and this review agree). NVIDIA's own public envelope (45/65 C) implies 0.75 LPM/kW minimum and ~1.0 nominal.

Programme consequence: the "flow-equivalence" KPI should be defined as *the specific flow at which our plate reproduces CoolIT's 34.4 K average / 44.2 K maximum at 45 C inlet on the same TTV*; target <= 0.9 LPM/kW (25 % below the brief), with the design point stated at 1.0 LPM/kW.

## 6. Temperature limits and the silicon drop

| Item | Value | Source |
|---|---|---|
| NVIDIA A100/H100-class nvidia-smi limits | GPU max operating ~85 C; slowdown ~87-89 C; shutdown ~92-93 C; HBM max operating ~95 C | [KB-M] (nvidia-smi `-q -d TEMPERATURE` fields) |
| B200/B300/Rubin | not public; assume the same class | [KB-L] |
| HBM3e / HBM4 | JEDEC-class operating ceiling ~95 C (refresh doubling above 85 C) | [KB-M] |
| CoolIT convention | "Tcase ~80 C appropriate for processors today" | [Brief] |
| Bulk-silicon drop, flip-chip (active layer at the bottom, heat up through the bulk) [D] | at 120 W/cm2: 5.0 / 6.5 / 7.8 K for 500 / 650 / 775 um Si; at 350 W/cm2 hot spot: 15 / 19 / 23 K | k_Si ~1.2 W/cm-K at 85 C |
| Resulting die-top-to-inlet budget at 45 C inlet, 650 um Si, 120 W/cm2 [D] | Tj 85 C -> **33.5 K**; Tj 90 C -> 38.5 K | - |

Reading: CoolIT's 34.4 K average / 44.2 K maximum at 45 C is **at or above the Rubin-class budget** once the silicon drop is counted (Tj at a 44.2 K case-to-inlet hot spot would be ~96-100 C at 120-200 W/cm2). For a bare-die or thin-lid Rubin-class package the plate (including TIM) must deliver **<= ~28-30 K average and <= ~33-35 K maximum** at 45 C inlet and 1.0 LPM/kW. That is the requirement that matters, not "15 kW".

## 7. Package form, lid timing, mounting and the HBM4 step

### 7.1 What is public

- NVIDIA data-centre GPUs (A100, H100 SXM5/PCIe, B200 in GB200, B300 "SXM puck" in GB300) are **bare-die packages with a stiffener ring**; the heat sink / cold plate base contacts the GPU dies directly (thin TIM) and the HBM stacks through a thicker TIM layer [KB-M; GB300 puck: KB-M via SemiAnalysis Dec-2024 reporting].
- Kuo (Jan 2026): VR200 Max-Q (1.8 kW) = "micro-channel cold plate + gold-plated lid"; micro-channel lid needed for Max-P 2.3 kW, **not before 2H 2027** [Sib https://www.ctee.com.tw/news/20260107701081-430704].
- Digitimes (Sep 2025) and Wccftech: NVIDIA seeking microchannel-lid / direct-to-chip partners for Rubin Ultra [Sib https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html ; https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/].
- NVIDIA centralised Rubin cold-plate purchasing; Group-A: **Jentech** (lid/stiffener incumbent), AVC, Cooler Master, Delta; plate ASP ~US$400 [Sib https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html].
- CoolIT's own roadmap: "direct-to-die and micro-channel lids" [Brief]. Frore's Rubin pitch assumes delidded GPUs [Sib].
- JEDEC HBM4 (JESD270-4, Apr 2025): 2048-bit, up to 16-high, 24/32 Gb dies; max package height **775 um** for 12/16-high, up from 720 um (HBM3/3E) [KB-M].

### 7.2 Interpretation (hypothesis, Low confidence; needs the Rubin package photo or a Jentech/TSMC disclosure)

1. A gold-plated (gallium-compatible) **flat lid on Rubin** would be a departure from NVIDIA's bare-die lineage. The most plausible mechanical reason is the HBM4 height change: if HBM4 stacks are 775 um and the logic die is thinned to <= 775 um, the HBM can be **flush with or proud of** the GPU die, which a bare-die cold plate cannot load without cracking HBM. A lid with a stepped underside and TIM1 absorbs the step and presents a flat, plated surface for a liquid-metal or paste TIM2.
2. If (1) holds, **Rubin (2026) is a plate-vendor socket**: a flat ~100 mm lid, TIM2 on the plate side, 1.8-2.3 kW, 45 C inlet, ~2 LPM, plate dP <= 30-40 kPa. The gold plating implies NVIDIA intends liquid-metal TIM2 (gallium alloys attack bare Cu/Al; Au/Ni plating resists), which lowers the TIM share of the budget by 5-8 K versus paste [Sib physics/tim-and-direct-to-die.md].
3. **Rubin Ultra (2027) is where the socket moves**: a microchannel lid (coolant inside the lid, TIM1 only) makes the lid vendor (Jentech-class) the thermal owner and reduces the "cold plate" to a manifold cap with seals. A plate vendor competes there only by (a) supplying the microchannel-lid core itself, or (b) offering a direct-to-die plate with stepped/compliant contact as the alternative NVIDIA is reportedly evaluating.
4. Google (bare-die since TPU v4, 80 psi available) and Microsoft (Maia, in-silicon microfluidics research with Corintis) remain **bare-die / direct-to-die** customers regardless of what NVIDIA does [Sib].

### 7.3 Mounting load and flatness (no public NVIDIA numbers)

| Item | Working value | Basis |
|---|---|---|
| Bare-die contact pressure | 0.15-0.35 MPa (20-50 psi) over the die area; for ~16.6 cm2 of Rubin logic: 250-580 N (56-130 lbf) total | [KB-M] industry practice for bare-die GPU heat sinks |
| Lidded contact pressure | 0.3-0.7 MPa (45-100 psi) on the lid; paste BLT 20-50 um at that load | [KB-M]; Shin-Etsu X23-7921-5 0.05 cm2-K/W at 25 um / 20 psi [Sib coolit-briefs-numbers.md] |
| Plate flatness / finish | <= 25-50 um over the footprint; Ra <= 0.8 um | [Sib standards-reliability.md, KB-M] |
| Package warpage | 100-300 um over temperature for 100-130 mm substrates; needs compliant loading (spring screws, floating core) | [Sib standards-reliability.md] |
| HBM-zone load | HBM stacks must see lower pressure than the die; bare-die plates use a thicker, softer TIM over HBM (0.1-0.3 mm) or a stepped pedestal | [KB-M]; sibling pedestal result: 0.4 mm step filled with paste/pad fails above ~15-20 W/cm2; stepped Cu pedestal + 0.1 mm paste mandatory [Sib physics/nonuniform-heatmap.md] |
| Retention | 4 or 8 spring screws to a backplate; torque-limited; keep-outs for VRM and stiffener | [KB-M] |

## 8. What this fixes for the programme (recommended KPIs)

| KPI | Fix | Why |
|---|---|---|
| Design specific flow | **1.0 LPM/kW** (PG25, 45 C); publish 0.6 / 0.75 / 1.0 / 1.2 / 1.5 curves | NVIDIA rack envelope ~1.0 nominal, 0.75 floor; 1.2 is a CDU rating point; 1.2 curve needed only for the CoolIT comparison |
| Flow-equivalence KPI | LPM/kW at which our plate matches CoolIT's 34.4 K avg / 44.2 K max on the 15 kW TTV; target **<= 0.9 LPM/kW** | 25 % below the brief, in line with Frore's 0.87 claim (V) |
| Thermal KPI at 1.0 LPM/kW, 45 C | **<= 28 K average, <= 33 K maximum** die-top-to-inlet at Rubin-class flux (120 W/cm2 avg with 300-350 W/cm2 hot-spot patches) | Tj 85-90 C budget after the silicon drop (section 6) |
| Plate dP budget | **<= 25 kPa at 1.0 LPM/kW; <= 35 kPa at 1.2 LPM/kW** (15 kW TTV); tray <= 100 kPa incl. UQD08 | plate-level public band 12-40 kPa; rack 124 kPa; CDU 240-365 kPa |
| CDU-count value argument | state it as **LPM saved per MW**, not pump W: 1.2 -> 0.9 LPM/kW saves 300 LPM per MW (12.5 % of a CHx2000's ~2,400 LPM) and shrinks manifold/QD size; HX duty is unchanged, so the saving is in pumps, piping and QDs, not in HX area | section 4.3 arithmetic |
| Interface SKUs | (a) lidded-flat with paste; (b) lidded-flat with liquid-metal (plated contact face); (c) bare-die stepped/compliant (Blackwell/TPU/Maia class); (d) microchannel-lid core (Rubin Ultra option) | section 7 |
| Footprint envelope | 100 x 100 mm (Rubin / MI455X class) and 120 x 150 mm (Rubin Ultra class), per-channel flow length independent of package size | TSMC substrate roadmap [KB-M] |

## 9. Corrections to the TTV-B geometry

The sibling TTV-B ("4 dies x 26 x 33 mm at 350 W/cm2 + 16 HBM, HBM 0.4 mm lower") is a **2029+ stress case, not Rubin Ultra**:

- Rubin Ultra at the analyst 3.6 kW over ~33 cm2 of logic is **~87 W/cm2 die-average** [D], not 350 W/cm2 (which would be 11.6 kW of logic alone). The 300-400 W/cm2 figures are local hot spots over 10-20 % of each die. TTV-B should therefore carry **four 26 x 33 mm heaters at ~90-130 W/cm2 average with embedded 300-350 W/cm2 patches** (e.g. 2-4 patches of 3-5 cm2 per die), total 3.6-5 kW per package, and a second "stretch" setting at 2x.
- HBM4e count and placement are right (16 stacks, 8 per side in two columns of 4 is the natural CoWoS-L layout for a 4-reticle package) [KB-M]. HBM power ~40-50 W per stack (0.65-0.8 kW total, ~20 % of package power) [KB-L].
- HBM step: use **0 to 0.15 mm, both signs, as a test variable**, not a fixed -0.4 mm. For a lidded package the step is irrelevant at the plate interface (flat lid). For bare-die, the plate must tolerate HBM flush or proud of the die (load-limited contact over HBM).
- Footprint: ~120 x 150 mm substrate class for Rubin Ultra (TSMC 9.5x-reticle, 2027) versus ~100 x 100 mm for Rubin; CoolIT's photogrammetry-estimated ~143 mm plate body [Sib gap-coolit-15kw-ttv-footprint-heater-map.md] is already Rubin-Ultra-sized.

## 10. Gaps / unknowns and exactly what to pull next

1. **No live verification this session** (search budget exhausted). Every [KB] line above must be re-checked. Highest-value primary documents (titles as I know them): NVIDIA "DGX SuperPOD with DGX GB200 / GB300 Systems - Site Planning Guide" (docs.nvidia.com; lists facility-water temperature range, flow per rack, CDU requirements); NVIDIA OCP blog (13 Oct 2025) "Vera Rubin NVL144 MGX / Kyber" (45 C statement, 800 VDC); NVIDIA GTC 2026 keynote transcript (any stated Rubin TDP); NVIDIA Blackwell Ultra technical blog (Aug 2025; 1,400 W); TSMC 2025 Technology Symposium CoWoS roadmap (5.5x / 9.5x reticle, 100 x 100 and 120 x 150 mm substrates, HBM counts); JEDEC JESD270-4 press release and spec abstract (775 um); Microsoft Maia 200 blog (Jan 2026; 750 W); Google Ironwood blog (Apr 2025) and Hot Chips 2025 slides (chip TDP, if any); AWS re:Invent 2025 Trainium 3 page; AMD Helios / MI455X OCP-2025 materials (TDP); Electronics Cooling Jun 2025 full text (the 1.2 LPM/kW sentence and the 18 psi example); OCP OAI liquid-cooling guideline (7.5-12 K rise).
2. **NVIDIA plate-level R, dP, flow, Tcase, mounting load and flatness are NDA** (thermal/mechanical design guides for SXM/puck/Rubin modules). Only an RVL/Group-A relationship or an ODM partner can supply them; the public-level reconstruction in sections 4-7 is the best available.
3. Rubin, Rubin Ultra, MI455X, Ironwood and Trainium 3 **per-package TDPs are not vendor-published**; the analyst values are rack-consistent but unconfirmed.
4. **Rubin package form (bare-die vs lidded) and the gold-plated-lid report** rest on one analyst note and Taiwanese trade press; the HBM4-step mechanism in 7.2 is my hypothesis.
5. **HBM4 stack height vs Rubin logic-die thickness** (sign and magnitude of the step) is not public; JEDEC 775 um is KB-M.
6. **Package edge lengths** for B200/B300/Rubin/MI455X are not public; TSMC substrate classes are the proxy.
7. The FiberMall GB200 (1.8 LPM, <20 kPa, <0.03 K/W) and ToneCooling GB300 (1.7 LPM, 12 kPa, 0.013 K/W) numbers were read from search extracts, not datasheets, and are vendor marketing; they bracket the plate-level band but are not NVIDIA requirements.
8. Whether CoolIT applied 1.2 LPM/kW to one plate (18 LPM through one body) or split across zones is undisclosed [Sib]; the flow-equivalence KPI must state the plate-level flow explicitly.
9. Kyber blade hydraulic architecture (series vs parallel plates per blade, blind-mate manifold dP, UQD08 vs UQDB) is unverified (LinkedIn/KB-L).
10. Searches to run when the budget resets (mode extended for the numeric ones): `NVIDIA "DGX GB300" site planning liquid cooling supply temperature flow rate LPM`; `"Vera Rubin NVL144" "45" liquid cooling NVIDIA blog OCP 2025`; `"Rubin" GPU TDP watts GTC 2026 NVIDIA official`; `TSMC CoWoS-L "9.5" reticle "120 x 150" substrate 2027 HBM`; `JESD270-4 HBM4 "775" package height`; `"Maia 200" 750W liquid cooling Microsoft blog`; `Ironwood TPU "watts" OR "TDP" Hot Chips 2025`; `Trainium3 "liquid-cooled" TDP watts re:Invent 2025`; `MI455X TDP watts AMD Helios OCP 2025`; `"1.2 LPM/kW" site:electronics-cooling.com`; `"Kyber" rack "cold plate" OR "manifold" pressure kPa OR psi NVIDIA`; `NVIDIA SXM "cold plate" "mounting load" OR "flatness" design guide`; `Rubin "gold" lid Jentech liquid metal TIM 2026`.

## 11. Sources

Primary / local
- CoolIT 15 kW Tech Brief (June 2026): local extract `appendix/pdf/brief.txt`.

URLs carried over from sibling reports (retrieved by web search earlier in this workflow; the URL is as recorded there)
- CoolIT 4000 W coldplate Technical Brief (Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- CoolIT CHx1000 (1.5 LPM/kW): https://hpcwire.com/2024/12/10/ai-performance-reliability-serviceability-with-coolits-chx1000-cdu/
- QCT QoolRack / GB200 NVL72 whitepaper (45 C supply, 65 C return, ~130 LPM): https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf
- DCD, NVIDIA GB200 NVL72 liquid-cooled announcement: https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus
- Vertiv / NVIDIA GB200 NVL72 reference architecture (up to 132 kW): https://investors.vertiv.com/news/news-details/2024/Vertiv-Codevelops-with-NVIDIA-Complete-Power-and-Cooling-Blueprint-for-NVIDIA-GB200-NVL72-Platform/default.aspx
- TrendForce GB200 rack TDP: https://www.trendforce.com/presscenter/news/20240730-12232.html
- TechPowerUp, Vera Rubin NVL144 (45 C, 2026 volume production): https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production
- Barrack.ai Rubin breakdown (secondary): https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/
- Kuo via CTEE / CLS (Rubin 1.8 / 2.3 kW, gold-plated lid, microchannel lid 2H 2027): https://www.ctee.com.tw/news/20260107701081-430704 ; https://www.cls.cn/detail/2250526
- TweakTown, B300 1.4 kW: https://www.tweaktown.com/news/103938/
- Igor's Lab, NVL72 cooling BOM and Rubin Ultra 3.6 kW: https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
- DCD, Rubin Ultra NVL576 600 kW 2H 2027: https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027
- Digitimes, Rubin cooling design (Sep 2025): https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html
- Wccftech, NVIDIA may switch cooling for Rubin Ultra: https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/
- NVIDIA Rubin cold-plate Group-A suppliers: https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html
- AMD Helios / MI455X (secondary): https://introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026 ; https://wccftech.com/amd-helios-ai-rack-mi455x-6th-gen-epyc-challenging-nvidia/amp/
- STH, Google Ironwood at Hot Chips 2025: https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/
- Chips and Cheese, Google liquid cooling at Hot Chips 2025: https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips
- Google, 1 MW racks and Project Deschutes CDU (80 psi): https://cloud.google.com/blog/topics/systems/enabling-1-mw-it-racks-and-liquid-cooling-at-ocp-emea-summit ; https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
- Electronics Cooling (Jun 2025), DLC for high-compute servers (1.2 LPM/kW, 18 psi): https://www.electronics-cooling.com/2025/06/direct-liquid-cooling-for-high-compute-servers/
- OCP L-L CDU Test Methodology (1.5 LPM/kW, >= 40 psi, 17-65 C, 100 psi): https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- ASHRAE 5th-edition liquid classes (Upsite summary): https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/
- Vendor GB200/GB300 plate figures (secondary): https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/
- Frore Rubin claims (secondary): https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/
- JetCool RTX PRO 6000 SmartPlate datasheet (commercial pressure conventions): https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf

Knowledge-base items (no URL verified this session; see section 10 for the documents to pull): NVIDIA HGX B200 / GB200 / GB300 TDPs; GTC 2024 "2 L/s, 25 C in / 45 C out" keynote line; nvidia-smi temperature limits for A100/H100; bare-die packaging of A100/H100/B200/B300; SemiAnalysis GB300 "SXM puck" reporting (Dec 2024); TSMC CoWoS-L substrate roadmap (5.5x / 9.5x reticle, 100 x 100 and 120 x 150 mm); JEDEC JESD270-4 HBM4 (Apr 2025) 775 um height; Microsoft Maia 200 750 W (Jan 2026); AMD MI355X 1,400 W; MI400 12 x HBM4; Google Ironwood 2-die + 8 HBM3e, ~10 MW pod; AWS Trainium 3 (Dec 2025).

Internal workflow files used: `appendix/pdf/brief.txt`; `appendix/research/{chip-roadmap-requirements, coolit-briefs-numbers, coolit-products, competitors-singlephase, competitors-advanced, standards-reliability, test-metrics, ip-landscape, manufacturing-cost, gap-coolit-15kw-ttv-footprint-heater-map, gap-coolit-dp-flow-curves-and-claim-baselines}.md`; `appendix/physics/nonuniform-heatmap.md`; `appendix/research/gap_envelope_calc.py` (this agent's arithmetic).
