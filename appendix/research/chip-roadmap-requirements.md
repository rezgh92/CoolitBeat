# AI-accelerator thermal requirements roadmap (2023-2029): what a cold plate must do to beat the CoolIT 15 kW benchmark

Prepared 2026-10-13 for the cooling-architecture programme. Angle: the thermal requirements of the *targets* (GPUs, AI ASICs, wafer-scale, power electronics), the facility/OCP boundary conditions (inlet temperature, flow per kW, pressure-drop budget, QD size, velocity, filtration) and what changes in 2027-2029.

## 0. Method and provenance (read first)

- **No live web searches were executed by this agent.** The per-turn WebSearch budget (200 calls, shared by all agents in the workflow) was already exhausted when this agent started; all 8 attempted queries were refused. WebFetch/curl are network-blocked in this container. I did not work around the limit.
- Sources used, in priority order:
  1. **[Brief]** the CoolIT 15 kW tech brief (June 2026), local extract.
  2. **[Sib]** numbers already retrieved *with URLs* by sibling research agents in this workflow (files `coolit-briefs-numbers.md`, `coolit-products.md`, `competitors-singlephase.md`, `competitors-advanced.md` in the same directory). These were web-searched earlier today; I quote their URL.
  3. **[KB]** my own knowledge base (training data to ~June 2026), **not verified in this session**. Each KB number carries a confidence tag (H/M/L). Treat KB-L numbers as leads to be confirmed before they go into a requirements document.
- Vendor claims are tagged (V); independent / peer-reviewed / standards bodies (I); analyst (A); derived by me (D).
- Where I compute heat flux, I use: die-average flux = (TDP minus HBM share) / logic-die area. HBM share assumed 25-40 W per stack for HBM3e 12-high, 35-45 W per stack for HBM4 (KB-M). These are design-planning estimates, not measurements.

## 1. The benchmark restated as a requirement

| Item | Value | Source |
|---|---|---|
| Power | 15 kW on 4 ceramic heaters (GPU + HBM zones) | [Brief] |
| Coolant / flow | water-glycol, 1.2 LPM/kW = 18 LPM | [Brief] |
| Inlet | 45 C (ASHRAE W45 class) | [Brief] |
| Case-to-inlet dT | avg 34.4 K (26.8-44.2 K across 3 plates x 8 TCs); avg Tcase ~80 C, hottest TC ~89 C | [Brief] |
| Case-to-inlet R | 0.00229 K/W (D); worst TC 0.00295 K/W (D) | [Sib] coolit-briefs-numbers.md |
| Coolant rise | ~12.6 K (PG25) -> outlet ~57.5 C (D) | [Sib] |
| Pressure drop | **not disclosed** (4 kW plate: 8 psi / 55 kPa full loop incl. QDs at ~6 LPM) | [Brief]; [Sib] https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf |
| Footprint / heat flux | not disclosed; sibling model calibrates to ~117 cm2 heated area, ~128 W/cm2 (D, +/-25 %) | [Sib] model_output.md |

The brief's own framing ("Tcase of 80 C, appropriate for processors today") is the key hook: **every real target below has a case/junction ceiling that fixes the allowable case-to-inlet R at 45 C inlet.** That is the number our plate has to beat per device, not "15 kW".

## 2. Target device table

Columns: TDP; logic silicon (die count x area); package / interposer; HBM; die-average heat flux (D); junction/case limit; cooling spec as shipped. Dates are launch/ramp dates.

### 2.1 NVIDIA

| Device (date) | TDP | Logic silicon | Package | HBM | Die-avg flux (D) | Tj / Tcase limits | Cooling as shipped | Provenance |
|---|---|---|---|---|---|---|---|---|
| H100 SXM5 (2022-23) | 700 W (PCIe 350 W) | 1 x GH100, 814 mm2, TSMC 4N | CoWoS-S, lidded IHS | 5 x HBM3 (80 GB) | ~600 W / 8.1 cm2 = **~75 W/cm2** | GPU slowdown ~85-90 C, HW shutdown ~95 C; HBM3 Tj max 95 C | air (HGX) or DLC retrofit plates (0.021 K/W JetCool, V) | TDP/die: KB-H. Tj: KB-M. JetCool: [Sib] https://jetcool.com/post/jetcool-unveils-breakthrough-energy-saving-liquid-cooling-for-nvidias-h100-gpus-enhancing-ai-cluster-efficiency-and-performance/ |
| H200 (2024) | 700 W | same GH100 | CoWoS-S, lidded | 6 x HBM3e (141 GB) | ~75 W/cm2 | as H100 | air or DLC | KB-H |
| B200 (HGX, 2024-25) | 1,000 W (HGX), **1,200 W** in GB200 superchip (2 x B200 + Grace = 2,700 W) | 2 x reticle dies, ~1,600 mm2 total, TSMC 4NP, 208 B transistors | **CoWoS-L** (LSI bridges), lidded | 8 x HBM3e (180-192 GB) | ~950 W / 16 cm2 = **~60-70 W/cm2** at 1,000-1,200 W | GPU slowdown ~85-90 C (KB-L); HBM3e 95 C | GB200 NVL72: 100 % DLC; HGX B200 air at 1,000 W | TDP: KB-H; superchip 2,700 W: KB-H; die area: KB-M |
| B300 / Blackwell Ultra (GB300 NVL72, 2025-26) | **1,400 W** | same 2-die Blackwell silicon | CoWoS-L, lidded; GB300 moves GPU to socketed "SXM puck" modules with individual plates (KB-M) | 8 x HBM3e 12-high (288 GB) | ~1,150 W / 16 cm2 = **~70-75 W/cm2** | as B200 | 100 % DLC, PG25, 45 C inlet class | 1,400 W: [Sib] https://www.tweaktown.com/news/103938/ ; KB-H |
| GB200 NVL72 rack (2024-25) | 120 kW nominal (NVIDIA), up to 132 kW (Vertiv ref.), ~140 kW (TrendForce) | 72 B200 + 36 Grace, 18 compute trays (2 superchips = 5.4 kW GPU/CPU + ~1 kW misc each), 9 NVSwitch trays (DLC) | - | - | - | - | DLC: PG25; NVIDIA keynote GTC 2024: "25 C in, 45 C out, 2 L/s" (= 120 LPM, ~1.0 LPM/kW) (KB-H); QCT/DCD: max inlet 45 C, max return 65 C, up to ~130 LPM/rack | [Sib] https://www.trendforce.com/presscenter/news/20240730-12232.html ; https://investors.vertiv.com/news/news-details/2024/Vertiv-Codevelops-with-NVIDIA-Complete-Power-and-Cooling-Blueprint-for-NVIDIA-GB200-NVL72-Platform/default.aspx ; https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf ; https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus |
| Vera Rubin / VR200 NVL144 (2H 2026) | **1.8 kW (Max-Q) to 2.3 kW (Max-P)** per GPU package (A); DCD "up to 2,300 W" | 2 x reticle dies (~1,650 mm2), TSMC N3 class; "NVL144" counts dies, 72 packages | CoWoS-L; lidded with gold-plated lid + microchannel plate initially; **microchannel lid for 2.3 kW not before 2H 2027** (A, Kuo) | 8 x HBM4 (288 GB) | ~1,950 W / 16.5 cm2 = **~115-120 W/cm2** at 2.3 kW | not public; plan Tcase <= 80 C (brief convention) | 100 % DLC, cable-free MGX gen-3 tray, **designed for 45 C inlet**, 800 VDC-ready; rack ~190 kW (Max-Q) / ~230 kW (Max-P) (A) | [Sib] https://www.ctee.com.tw/news/20260107701081-430704 ; https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production ; https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/ ; NVIDIA OCP Oct-2025 blog (KB-M) |
| Rubin Ultra NVL576 / Kyber rack (2H 2027) | **~3.6 kW per package** (A); rack **~600 kW** | **4 x reticle dies (~3,300 mm2)** per package | CoWoS-L, ~9x-reticle class interposer; lid strategy undecided publicly (direct-to-chip / microchannel lid rumoured) | **16 x HBM4e (1 TB)** | ~3,000 W / 33 cm2 = **~90-100 W/cm2** (large area, but ~120 x 120 mm package -> spreading & warpage dominate) | not public | 100 % DLC, 800 VDC, 45 C inlet (KB-M); Kyber vertical blades, sidecar CDU rack; 1/2-in QDs (KB-L) | [Sib] https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/ ; https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027 ; https://datacenterdynamics.com/en/analysis/nvidia-gtc-jensen-huang-data-center-rack-density |
| Feynman (2028) | not disclosed; extrapolation 4-6 kW/package (D, L) | not disclosed; TSMC A16-class node (KB-L) | likely CoWoS-L/SoIC; candidate for in-package microfluidics (TSMC silicon microcooler, ECTC 2025) (KB-L) | HBM4e/HBM5 | >150 W/cm2 plausible (D, L) | - | DLC; Nvidia's 800 VDC roadmap covers 2027+ racks to >1 MW | KB-L; TSMC: [Sib] https://semiwiki.com/semiconductor-manufacturers/tsmc/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/ |
| NVIDIA 800 VDC power (announced May/Oct 2025, deploy 2027) | enables 1 MW+ racks; replaces 54 V busbar; partners Infineon, Navitas, TI, Delta, Eaton, Vertiv, Schneider (KB-M) | - | - | - | - | - | **Consequence for us:** power shelves / SST / 800 V DC-DC stages become liquid-cooled loads of 2-4 % of rack power (20-40 kW per MW rack) with SiC/GaN die fluxes of 100-300 W/cm2 and Tj 150-175 C (KB-M) | KB-M |

Notes on NVIDIA procurement: for Rubin, NVIDIA centralised cold-plate purchasing; Group-A suppliers named as Jentech, AVC, Cooler Master, Delta; plate ASP ~US$400; NVL144 cooling BOM ~US$55.7 k [Sib] https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html ; https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/ .

### 2.2 AMD

| Device (date) | TDP | Logic silicon | Package | HBM | Die-avg flux (D) | Limits | Cooling | Provenance |
|---|---|---|---|---|---|---|---|---|
| MI355X (Jun 2025) | **1,400 W** (MI350X air: 1,000 W) | 8 XCDs (N3P) 3D-stacked on 2 IODs (N6); ~1,800-2,000 mm2 total silicon (KB-L) | CoWoS-S + SoIC hybrid bonding, lidded | 8 x HBM3E (288 GB) | power concentrated in stacked XCDs: ~1,100 W / ~9 cm2 = **~120 W/cm2 at XCD level** (D, L) | Tjmax not public (~95-105 C class, KB-L) | DLC; 128-GPU liquid-cooled racks | 1,400 W: KB-H; CoolIT lists MI355 plates [Sib] coolit-products.md |
| MI400 / MI450 / MI455X, Helios rack (2026) | **>2 kW per GPU** (secondary; range 1.6-2.3 kW) | N2-class XCDs, 2 IODs (KB-L) | CoWoS-L/SoIC (KB-L) | **432 GB HBM4**, 19.6 TB/s (KB-H) | ~100-130 W/cm2 (D, L) | - | Helios: 72 GPUs, double-wide OCP ORW rack, 100 % DLC; rack ~160-200 kW (D, L) | [Sib] https://introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026 ; https://wccftech.com/amd-helios-ai-rack-mi455x-6th-gen-epyc-challenging-nvidia/amp/ |

### 2.3 Hyperscaler ASICs and others

| Device (date) | TDP | Silicon / package | HBM | Flux (D) | Cooling | Provenance |
|---|---|---|---|---|---|---|
| Google TPU v7 Ironwood (2025) | not disclosed; pod of 9,216 chips ~10 MW -> **~1.1 kW/chip all-in** incl. host/network/cooling; chip TDP est. 600-900 W (D, L) | single large die + 8 x HBM3e (192 GB), 7.4 TB/s (KB-M) | 8 | ~80-110 W/cm2 (D, L) | **Bare-die (lidless) cold plates since TPU v4**; chips plumbed **in series** (capacity budgeted for last chip); split-flow plate found to beat straight-through; ~1 GW of DLC over ~2,000 pods; Project Deschutes CDU 2 MW at 3 C ATD, **80 psi available** "to enable advanced cold plate designs" | [Sib] https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/ ; https://cloud.google.com/blog/topics/systems/enabling-1-mw-it-racks-and-liquid-cooling-at-ocp-emea-summit ; https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/ |
| AWS Trainium 3 (Dec 2025) | not disclosed; est. 0.8-1.2 kW (D, L); Trainium2 was ~500 W air-cooled (KB-M) | TSMC 3 nm; Trn3 UltraServer 144 chips (KB-M) | HBM3e | - | first liquid-cooled Trainium generation (KB-M) | KB |
| Microsoft Maia 200 (Jan 2026) | **~750 W** (KB-M) | TSMC 3 nm, ~10 PF FP4 (KB-M) | 216 GB HBM3e (KB-M) | ~70-90 W/cm2 (D, L) | DLC via second-gen closed-loop "sidekick" rack HX; Microsoft/Corintis in-silicon microfluidics prototype "up to 3x" heat removal (V, prototype) | KB; Corintis: [Sib] competitors-advanced.md |
| Meta MTIA (v2 2024; next-gen 2026) | MTIA v2: 90 W (KB-H); next-gen training part with Broadcom: not disclosed, expected >1 kW DLC (KB-L) | TSMC 5 nm (v2) | LPDDR5 (v2); HBM (next) | low (v2) | air (v2); DLC planned (L) | KB |
| Cerebras WSE-3 / CS-3 (2024) | **CS-3 system ~23 kW peak**; wafer ~15-20 kW (KB-H) | **46,225 mm2** wafer-scale, 4 T transistors, 900 k cores, TSMC 5 nm (KB-H) | 44 GB on-wafer SRAM, no HBM | ~20 kW / 462 cm2 = **~43 W/cm2** (low flux, enormous area) | Custom "engine block" water cold plate; wafer clamped through a compliant per-die thermal interface to handle CTE/warpage; closed internal water loop with redundant pumps, heat exchanged to facility water or air; 15U chassis (KB-M) | KB |
| Intel Gaudi 3 (2024) | **900 W OAM** (HL-325L air; HL-335 liquid variant) (KB-M) | 2 dies, TSMC 5 nm; 8 x HBM2e 128 GB (KB-H) | 8 | ~60 W/cm2 (D, L) | air or DLC OAM | KB |
| Intel Jaguar Shores (2027-28) / Crescent Island (2H 2026 sampling) | not disclosed; Crescent Island is an air-cooled inference part (Xe3P, 160 GB LPDDR5X) (KB-M) | - | - | - | - | KB |
| Broadcom custom XPUs (Google, Meta, OpenAI 10 GW deal 2026-29, ByteDance) | not disclosed per part; packaging roadmap implies 1.5-3 kW | **3.5D XDSiP: up to 6,000 mm2 of 3D-stacked silicon and 12 HBM stacks, production 2026** (V, KB-M) | up to 12 | >100 W/cm2 at logic tier (D, L) | DLC | KB |
| Groq LPU (v1; next-gen Samsung 4 nm) | ~300 W class card, SRAM-only, air-cooled (KB-M); NVIDIA licensing/asset deal Dec 2025 (KB-M) | GF 14 nm (v1) | none | low | air | KB |

**Read-across:** every merchant and hyperscaler part launching 2026-27 is 1-2.3 kW per package, lidded or bare-die, 8-16 HBM stacks, on CoWoS-L / SoIC with 100-120 mm package edges. Only Cerebras exceeds 10 kW per "device", and it does so at ~43 W/cm2 over 462 cm2. **The 15 kW single-package TTV is therefore a 2028+ (Feynman / Rubin-Ultra-successor) scenario; the commercial battleground to 2028 is 1.4-3.6 kW packages at 70-130 W/cm2 die-average with 2-4x local hotspots.**

## 3. Boundary conditions: inlet temperature, flow, pressure drop, QDs, velocity, filtration

### 3.1 Inlet temperature classes and the resulting R budget

| Item | Value | Provenance |
|---|---|---|
| ASHRAE liquid classes (Thermal Guidelines 5th ed., 2021) | W17 (2-17 C), W27 (2-27), W32 (2-32), W40 (2-40), **W45 (2-45 C)**, W+ (>45 C) facility-water supply | [Sib] https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/ ; KB-H |
| NVIDIA GB200 NVL72 | max TCS supply 45 C, max return 65 C (QCT/DCD); GTC-2024 keynote 25 C in / 45 C out at 2 L/s (KB-H) | [Sib] QCT, DCD links above |
| NVIDIA Rubin MGX gen-3 | designed for 45 C inlet | [Sib] TechPowerUp link above; KB-M |
| OCP L-L CDU methodology | TCS 17-65 C envelope; references ASHRAE W classes | [Sib] https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/ |
| Industry practice | 45 C (W45) is now the de-facto AI standard (CoolIT, Supermicro DLC-2, Lenovo Neptune, NVIDIA MGX); HPE GX 40 C; Uptime notes typical 40 C GPU supply limit; nobody publishes >45 C performance; Accelsius two-phase claims 54 C inlet parity with single-phase at 45 C (V) | [Sib] competitors-singlephase.md ; https://www.businesswire.com/news/home/20260721991081/en/ |

Required case-to-inlet resistance at 45 C inlet, Tcase ceiling 80 C (dT budget 35 K), and the same at W+ 50 C inlet (30 K):

| Device | P (W) | R_case-inlet required @45 C (K/W) | @50 C (K/W) | Note |
|---|---:|---:|---:|---|
| H100 | 700 | 0.050 | 0.043 | JetCool 0.021 (V), OCP OAI 0.015-0.016 at 1 kW (I): easy |
| B200 (GB200) | 1,200 | 0.029 | 0.025 | generic GB200 plate target <0.03 (V) [Sib] fibermall - marginal! |
| B300 | 1,400 | 0.025 | 0.021 | ToneCooling GB300 plate 0.013 (V) [Sib] tonecooling |
| Rubin Max-P | 2,300 | 0.0152 | 0.0130 | CoolIT 4 kW plate <0.009 at 4 kW (V) shows feasibility |
| Rubin Ultra | 3,600 | 0.0097 | 0.0083 | at the single-phase "~4,000 W boundary" OCP fragment cites [Sib] https://www.opencompute.org/documents/white-paper-thermal-boundaries-in-ai-infrastructure/ |
| 15 kW TTV | 15,000 | 0.00233 | 0.0020 | CoolIT 0.00229 avg = exactly on the 80 C line; worst TC 0.00295 = 89 C |

In unit terms, R'' = dT / q''. With 35 K: 120 W/cm2 -> **0.29 cm2-K/W**; 200 -> 0.175; 300 -> 0.117; 500 -> 0.07. A good paste TIM alone is 0.05-0.10 cm2-K/W (Shin-Etsu X23-7921-5: 0.05 at 25 um/20 psi; Honeywell PTM7950: 0.04-0.08) [Sib] coolit-briefs-numbers.md. **At >=300 W/cm2 the TIM consumes 40-90 % of the whole budget, so paste-on-lid designs cannot meet 2028 hotspot fluxes; indium/liquid-metal/direct-to-die becomes a requirement, not an option.**

### 3.2 Flow per kW

| Source | Guidance | Provenance |
|---|---|---|
| CoolIT 15 kW brief (2026) | 1.2 LPM/kW "industry standard flow rate for AI systems" | [Brief] |
| CoolIT 4 kW brief (2025) | 1.5 LPM/kW "semiconductor industry recommended" | [Sib] coolit-briefs-numbers.md |
| NVIDIA GTC 2024 keynote, GB200 NVL72 | 2 L/s per ~120 kW rack = **~1.0 LPM/kW** (25 C in / 45 C out) | KB-H |
| QCT/NVIDIA GB200 NVL72 | up to ~130 LPM per rack (~1.0-1.1 LPM/kW) | [Sib] QCT link |
| OCP OAI liquid cooling guideline (Mar 2023) | 1-2 LPM per 1 kW OAM; **7.5-12 C coolant rise** recommended | [Sib] https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/ |
| OCP L-L CDU test methodology | 1.5 LPM/kW rating basis | [Sib] OCP L-LCDU link |
| Electronics Cooling (Jun 2025) | 1.2 LPM/kW at 45 C "a common standard many CDUs can meet"; 96 LPM for 80 kW rack; ~18 psi rack budget | [Sib] coolit-briefs-numbers.md |
| Vendor plates | GB200 superchip plate 1.8 LPM (~0.67 LPM/kW at 2.7 kW); GB300 GPU plate 1.7 LPM (1.6 LPM/kW); Frore Rubin claim 0.87 LPM/kW vs 1.41 conventional (V) | [Sib] https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ ; https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/ |

Energy-balance implication (PG25, cp ~3.9 kJ/kg-K, rho ~1.02): 1.0 LPM/kW -> 15 K rise; 1.2 -> 12.6 K; 1.5 -> 10 K. NVIDIA's own 45 C in / 65 C out envelope is a 20 K rise = **0.75 LPM/kW**. Our design flow target should be stated at 0.75-1.0 LPM/kW (CDU and manifold sizing is the hyperscaler's cost driver), with full performance curves at 0.5-1.5 LPM/kW.

### 3.3 Pressure-drop budget

| Level | Value | Provenance |
|---|---|---|
| GPU plate (vendor targets) | <20 kPa at 1.8 LPM (GB200); 12 kPa at 1.7 LPM (GB300, 0.013 K/W); 35 kPa at 2.5 LPM; design target <40 kPa at 3 LPM | [Sib] fibermall; tonecooling |
| CoolIT 4 kW plate | 8 psi / 55 kPa full loop incl. fittings and QDs at ~6 LPM | [Sib] CoolIT 4 kW brief |
| Rack (whole TCS loop incl. manifolds, QDs, trays) | ~18 psi (124 kPa) worked example at 1.2 LPM/kW | [Sib] Electronics Cooling Jun 2025 |
| CDU secondary head available | CoolIT CHx1000 35 psi; CHx1500 44 psi; CHx2000 **53 psi**; OCP L-L CDU >=40 psi at 1.5 LPM/kW; Google Deschutes **80 psi**; OCP allows TCS components to see up to **100 psi** | [Sib] coolit-products.md ; OCP L-LCDU ; Google/DCD Deschutes links |
| OCP Cold Plate Test Spec v1.0.0 (Oct 2026, CoolIT primary author) | dP measured at 45 +/- 2 C at >= 6 flow points from 25 % to 150 % of rated flow; burst example >20 bar; He leak <= 1e-5 mbar-L/s; thermal cycling 10-65 C and -40/+70 C | [Sib] https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf |
| Negative-pressure systems (Chilldyne) | plate must work below 1 atm available head, i.e. low-dP designs only | [Sib] competitors-advanced.md |

Working requirement: **plate-only dP <= 20-35 kPa at design flow; tray (2 GPU plates + CPU + QDs) <= 70-100 kPa; keep two plates in series possible (NVIDIA/Google series plumbing).** Pumping power at 15 kW / 18 LPM: 30 kPa = 9 W (0.06 % of load), 100 kPa = 30 W, 150 kPa = 45 W [Sib] coolit-briefs-numbers.md. The CDU, not the plate, is where pumping power actually matters: a 2 MW CDU at 53 psi secondary head and ~2,400 LPM is ~15 kW of hydraulic power before pump efficiency.

### 3.4 Quick disconnects, velocity, filtration, coolant

| Item | Value | Provenance |
|---|---|---|
| OCP UQD spec v2.0.0 (Oct 2026) | UQD02 (1/8 in), UQD04 (1/4 in), UQD06 (3/8 in), UQD08 (1/2 in); UQDB blind-mate variants; CoolIT credited as collaborator | [Sib] https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf ; sizes KB-H |
| GB200/GB300 trays | hose-type UQD04/UQD06-class per tray (KB-L); ODMs/NVIDIA moving to **1/2-in (UQD08/UQDB08) for >200 kW racks** (Rubin/Kyber) | [Sib] competitors-singlephase.md (LinkedIn, unverified); KB-L |
| Coolant | PG25 (25 % propylene glycol + inhibitors) is the OCP base spec and NVIDIA's fluid; cp ~3.94 kJ/kg-K at 50 C, viscosity ~2x water -> laminar in microchannels (Re ~200 at 0.7 m/s in 0.2 mm gaps) | [Sib] https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/ ; model_output.md |
| Max coolant velocity | copper tubing/channels **<= 1.5-2.0 m/s** continuous (erosion-corrosion), stainless manifolds <= 3 m/s; microchannel designs typically 0.5-2 m/s; "2-4 m/s" seen in one low-reliability GB300 blog | KB-M; [Sib] naddod (low reliability) |
| Filtration | TCS-side 50 um nominal (some 25 um) at the CDU, plus strainers at rack; channel minimum gap should be >= 3-4x the filter rating -> **>= 0.15-0.2 mm gaps for 50 um filtration**; finest commercial skived fins 0.06 mm thick at 0.10 mm pitch exist but are fouling-sensitive; Ecolab (CoolIT's owner since 2026) markets commissioning/water-quality services for exactly this reason | KB-M; [Sib] coolit-products.md ; https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink |
| Materials | copper wetted path standard; stainless manifolds; avoid aluminium in mixed-metal PG25 loops (galvanic); CuW baseplates for CTE-matched direct-to-die (ORNL) | [Sib] competitors-singlephase.md (ORNL/IJHMT 2025) |

## 4. Package geometry: lidded vs lidless, HBM height, CoWoS-L, warpage

| Topic | Fact | Provenance |
|---|---|---|
| Lidded (IHS) | NVIDIA H100/H200/B200/B300, AMD MI300/MI355X, Intel Gaudi 3 ship with an integrated heat spreader; cold plate contacts lid via paste/PCM TIM | KB-H |
| Bare-die / lidless | Google TPU bare-die since TPU v4; Microsoft Maia and Corintis prototyping in-silicon channels; TSMC demonstrated **direct-to-silicon liquid cooling on CoWoS, >2.6 kW sustained, dT <63 C** (ECTC 2025); NVIDIA rumoured to seek microchannel-lid / direct-to-chip partners for Rubin Ultra; Kuo: Rubin 2.3 kW needs microchannel lid, not before 2H 2027; CoolIT's own roadmap: "direct-to-die and micro-channel lids" next | [Sib] semiwiki TSMC link; https://wccftech.com/nvidia-might-switch-cooling-so ; ctee Kuo link; [Brief] |
| HBM vs logic height | JEDEC HBM4 (Apr 2025) raised max stack package height to **775 um** for 12/16-high (from 720 um) (KB-M); logic die on CoWoS is thinned to a different thickness, so a bare-die package presents **two or three top-surface heights differing by ~50-200 um** plus interposer tilt; the IHS normally absorbs this with stepped underside + thick TIM. A lidless or "lid-less-equivalent" plate must have stepped/compliant contact per zone (KB-M) | KB-M; task statement |
| HBM temperature | HBM3e/HBM4 Tj max 95 C (JEDEC-class, KB-M) is **lower** than the logic die's ~100-105 C, while HBM sits at the package edge where coolant is hottest in a single-pass plate -> HBM zone needs its own inlet-fed branch (CoolIT TTV: hottest TC5 and coolest TC8 differ by 12-17 K [Brief]) | KB-M; [Brief] |
| CoWoS-L and size | Blackwell/Rubin on CoWoS-L (RDL interposer + LSI bridges); Rubin Ultra 4 reticles; TSMC roadmap ~9x reticle (2027) and SoW-X wafer-level in 2027+ (KB-M). Packages of 100-120 mm edge warp 100-300 um over temperature; lid flatness/TIM bond-line variation then dominates plate-to-plate spread (CoolIT: 10 K plate-to-plate at one TC [Brief]) | KB-M; [Brief] |
| Heat flux trajectory | die-average: 75 W/cm2 (H100) -> 70 (B300) -> 115-120 (Rubin) -> 90-100 (Rubin Ultra) -> >150 (2028, D). Local hotspots on SM/tensor clusters run 2-4x the average: **300-500 W/cm2 today, ~1 kW/cm2 targeted by 2028-29** (TSMC/DARPA/Mikros/Corintis class claims; Frore 600 W/cm2 (V); CoolIT OMNI >300 W/cm2 (V); Mikros ~20.7 kPa at 1 kW/cm2 (V)) | D; [Sib] competitors-advanced.md, competitors-singlephase.md |
| Single-phase ceiling as the industry frames it | IDTechEx "struggles ~1.5 kW, 2.0 kW limit" (A); OCP Thermal Boundaries (Oct 2026) "roughly 4,000 W" per package (fragment); CoolIT 15 kW TTV (V) | [Sib] coolit-briefs-numbers.md |

## 5. Power electronics (secondary target)

| Item | Value | Provenance |
|---|---|---|
| Automotive SiC traction inverter modules (Infineon HybridPACK DSC / HybridKIT) | Tj max 175 C; WEG 50/50 at 65 C inlet; Boyd DSC plate Rth 0.026 K/W, max dP 12.5 kPa at 10 LPM | [Sib] competitors-singlephase.md (Boyd datasheet); KB-H for Tj/coolant |
| Die-level flux | SiC MOSFET dies 20-40 mm2 at 100-300 W each -> 250-700 W/cm2 at the die, spread through DBC/AMB substrate to ~30-80 W/cm2 at the baseplate | KB-M |
| Data-centre 800 VDC (NVIDIA 2027) | power shelves, SSTs and 800 V-to-48 V/12 V stages at 97-98.5 % efficiency: 15-30 kW of loss per 1 MW rack, increasingly liquid-cooled; SiC/GaN Tj 150-175 C allows 45-55 C inlet with modest R | KB-M |

Implication: a plate core that hits <=0.2 cm2-K/W (incl. interface) at 20-35 kPa serves both markets; the power-electronics version needs 65 C inlet tolerance, WEG 50/50 viscosity (2x PG25), and pin-fin direct-cooled baseplates (industry norm) rather than lids.

## 6. Requirement set for the programme (derived)

| Requirement | Target to *beat CoolIT* and meet 2027-29 silicon | Basis |
|---|---|---|
| R_case-inlet at 45 C, PG25 | <= 0.0075 K/W at 3.6 kW (Rubin Ultra, Tcase <= 72 C); <= 0.012 K/W at 2.3 kW; **<= 0.0018 K/W avg / <= 0.0022 worst-TC on the 15 kW TTV** (i.e. <= 27 K avg, <= 33 K max vs CoolIT 34.4 / 44.2) | Section 3.1; [Brief] |
| Unit resistance incl. TIM | <= 0.18 cm2-K/W with paste; <= 0.12 with indium/liquid-metal; <= 0.09 direct-to-die (sibling model: HMMC 0.15-0.19, D2D 0.13) | model_output.md |
| Hot-spot uniformity | max-minus-avg <= 6 K across GPU + HBM zones at 15 kW (CoolIT: ~10 K); HBM zone fed from inlet | [Brief] |
| Flow | full performance at **0.75-1.0 LPM/kW** (NVIDIA 45/65 C envelope), curves 0.5-1.5 LPM/kW | Section 3.2 |
| Pressure drop (publish it) | plate-only <= 25 kPa at 1.0 LPM/kW; <= 35 kPa at 1.2 LPM/kW on 15 kW TTV; tray <= 100 kPa incl. UQD08 | Section 3.3 |
| Inlet envelope | 17-50 C (W45 + W+ margin); characterise at 50 C | Section 3.1 |
| Fouling robustness | min internal gap >= 0.15 mm wherever 50 um filtration is specified, or a manifold-microchannel layout whose short channels tolerate partial blockage | Section 3.4 |
| Velocity | <= 2 m/s in copper | Section 3.4 |
| Package compatibility | lidded (paste/PCM), lidded-indium, and stepped bare-die (two heights, +/-200 um warpage compliance) variants from one core | Section 4 |
| Scalability | 100 x 100 mm (Rubin) to 130 x 130 mm (Rubin Ultra / 15 kW TTV) with per-channel flow length independent of package size (multi-slot manifold), >= 30 kW capability demonstrated | model_output.md; Section 2 |
| Qualification | OCP Cold Plate Test Spec v1.0.0 (dP at 6 flow points, burst > 20 bar, He leak <= 1e-5 mbar-L/s, thermal cycling) | Section 3.3 |
| Cost | <= US$400 ASP per Rubin-class plate (NVIDIA Group-A price point) | Section 2.1 |

## 7. Gaps / unknowns

1. **No live verification this session.** All [KB] items (Tjmax values, Trainium 3 / Maia 200 / Ironwood TDPs, Gaudi 3 liquid variant, Broadcom 3.5D numbers, JEDEC HBM4 775 um, UQD size mapping to GB200 trays, velocity/filtration norms, NVIDIA GTC-2024 "2 L/s" quote) must be re-checked against primary documents before use in a requirements spec.
2. NVIDIA has published **no cold-plate R or dP requirement** for GB200/GB300/Rubin in any public document found by sibling agents; secondary sources conflict (0.6-1.6 LPM/kW; 12-150 kPa). The NVIDIA MGX / DGX site-prep guides (supply temperature range, per-tray flow, dP allowance) should be obtained directly.
3. The origin of "1.2 LPM/kW industry standard" is not codified by OCP, ASHRAE or NVIDIA; it is a CDU-capability convention (Electronics Cooling, Jun 2025).
4. CoolIT 15 kW TTV footprint, heater areas and dP are undisclosed; the 117 cm2 / 128 W/cm2 calibration is a model inference (+/-25 %).
5. Rubin / Rubin Ultra / MI450 per-package TDPs are analyst figures (Kuo, TrendForce, Igor's Lab), not vendor-published; Feynman has no public numbers at all.
6. HBM4 stack height vs logic-die height on actual Rubin packages (sign and magnitude of the step) is not public; needed for any bare-die variant.
7. OCP "Thermal Boundaries in AI Infrastructure" (Oct 2026) was seen only as a fragment ("~4,000 W" single-phase boundary); Section 8.2 / Appendix B should be read in full.
8. Cerebras WSE-3 thermal-interface construction, coolant and inlet limits are not public beyond the 23 kW system figure.
9. Google Ironwood per-chip TDP and plate R were not retrieved; the "bare-die since TPU v4" and "series plumbing" statements come from Hot Chips 2025 reporting via sibling agents.
10. Power-electronics (SiC) target numbers are generic KB values; a specific 800 VDC power-shelf thermal spec (NVIDIA/OCP) was not available.

## 8. Sources

Sibling-retrieved (web-searched earlier today in this workflow; URL as recorded):
- CoolIT 4 kW tech brief R2 (Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- CoolIT coldplate technology page: https://www.coolitsystems.com/coldplate-technology/
- TrendForce GB200 rack TDP (Jul 2024): https://www.trendforce.com/presscenter/news/20240730-12232.html
- Vertiv GB200 NVL72 reference architecture, up to 132 kW (Oct 2024): https://investors.vertiv.com/news/news-details/2024/Vertiv-Codevelops-with-NVIDIA-Complete-Power-and-Cooling-Blueprint-for-NVIDIA-GB200-NVL72-Platform/default.aspx
- QCT QoolRack GB200 NVL72 whitepaper (45 C in / 65 C out, ~130 LPM) (Apr 2025): https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf
- DCD, NVIDIA liquid-cooled GB200 NVL72 (Mar 2024): https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus
- TweakTown GB300 1,400 W (GTC 2025): https://www.tweaktown.com/news/103938/
- TechPowerUp Vera Rubin NVL144 (45 C, 2026 volume): https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production
- CTEE / Kuo, Rubin 1.8/2.3 kW, microchannel lid 2H 2027 (Jan 2026): https://www.ctee.com.tw/news/20260107701081-430704 ; https://www.cls.cn/detail/2250526
- Barrack.ai Rubin GTC 2026 breakdown: https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/
- Igor's Lab, NVL72 cooling BOM, Rubin Ultra 3.6 kW: https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
- DCD, Rubin Ultra NVL576 600 kW 2H 2027: https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027
- DCD, GTC rack density analysis: https://datacenterdynamics.com/en/analysis/nvidia-gtc-jensen-huang-data-center-rack-density
- NVIDIA Rubin cold-plate suppliers (TVBS, Digitimes, Mar 2026): https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html
- AMD Helios / MI455X: https://introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026 ; https://wccftech.com/amd-helios-ai-rack-mi455x-6th-gen-epyc-challenging-nvidia/amp/
- STH, Ironwood at Hot Chips 2025: https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/
- Google Cloud blog, 1 MW racks / Deschutes CDU: https://cloud.google.com/blog/topics/systems/enabling-1-mw-it-racks-and-liquid-cooling-at-ocp-emea-summit ; DCD: https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
- TSMC direct-to-silicon on CoWoS (ECTC 2025, SemiWiki): https://semiwiki.com/semiconductor-manufacturers/tsmc/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/
- OCP OAI System Liquid Cooling Guidelines (Mar 2023): https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/
- OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- OCP Cold Plate Development and Qualification white paper: https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/
- OCP L-L CDU Test Methodology (1.5 LPM/kW, >= 40 psi, TCS to 100 psi): https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- OCP Thermal Boundaries in AI Infrastructure (Oct 2026): https://www.opencompute.org/documents/white-paper-thermal-boundaries-in-ai-infrastructure/
- OCP PG25 base specification v1.0.0: https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/
- OCP UQD design spec v2.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf
- ASHRAE 5th-edition liquid classes (Upsite summary): https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/
- Vendor GB200/GB300 plate data: https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ ; https://tonecooling.com/gb200-liquid-cooling-kit/
- Introl GB200 NVL72 deployment (secondary): https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled
- Naddod GB300 liquid cooling (low reliability): https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling
- JetCool H100 SmartPlate (Apr 2024): https://jetcool.com/post/jetcool-unveils-breakthrough-energy-saving-liquid-cooling-for-nvidias-h100-gpus-enhancing-ai-cluster-efficiency-and-performance/ ; RTX PRO 6000 datasheet: https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
- Frore LiquidJet Rubin claims: https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/
- Accelsius two-phase B200 benchmark (Jul 2026): https://www.businesswire.com/news/home/20260721991081/en/
- Finest skived fins (USUSTK): https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink
- Dow PG25 properties: https://www.chempoint.com/en-ca/products/dow/dowfrost-glycol-thermal-fluids/dowfrost-propylene-glycol-thermal-fluids/dowfrost-lc-25
- NVIDIA may switch cooling for Rubin Ultra (Wccftech, as recorded): https://wccftech.com/nvidia-might-switch-cooling-so

Knowledge-base items (not verified this session; primary documents to pull): NVIDIA H100/B200/B300 datasheets and GTC 2024/2025/2026 keynotes; NVIDIA blog "800 VDC architecture" (May 2025) and OCP Oct-2025 Vera Rubin NVL144 / Kyber posts; AMD MI350 series launch (Jun 2025) and Helios (Oct 2025 OCP); Google Ironwood blog (Apr 2025); AWS re:Invent 2025 Trainium3; Microsoft Maia 200 blog (Jan 2026); Cerebras CS-3 product brief; Intel Gaudi 3 white paper; Broadcom 3.5D XDSiP release (Dec 2024); JEDEC JESD270-4 HBM4 (Apr 2025); ASHRAE Liquid Cooling Guidelines for Datacom Equipment Centers.
