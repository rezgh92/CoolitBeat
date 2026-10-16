# Single-phase cold plate competitors vs. the CoolIT 15 kW benchmark

Research date: 2026-10-13. Scope: single-phase direct-to-chip cold plates and the best *published* numbers per vendor, normalised where possible against the CoolIT 15 kW tech brief (June 2026). 32 web searches were run (standard + extended); WebFetch/curl are blocked in this container, so every number below comes from search-result extracts of the cited page, not from a full read of the page. Secondary-source numbers are flagged. The per-turn search budget was exhausted before ~12 planned follow-up queries could run (listed under Gaps).

---

## 1. Benchmark restated, with derived metrics

Source: CoolIT 15 kW tech brief (local extract, June 2026) and the 1 June 2026 press release [1], DCD [2], Electronics360 (Computex 2026) [3].

| Item | Value | Note |
|---|---|---|
| Heat load | 15,000 W (4 ceramic heaters, GPU + HBM zones) | TTV, not a production GPU [2] |
| Coolant / flow | water-glycol, 1.2 LPM/kW = 18 LPM | "industry standard flow rate for AI systems" (CoolIT wording) |
| Inlet | 45 C | ASHRAE W45 class |
| Mean case-to-inlet dT | 34.4 K (plate averages 32.5 / 35.2 / 35.6 K) | 3 plates x 8 TCs |
| Worst / best single TC dT | 44.2 K / 26.8 K | |
| Derived mean R_case-inlet | **0.00229 K/W** | 34.4 / 15,000 |
| Derived worst-point R | **0.00295 K/W** | 44.2 / 15,000 |
| Hot-spot non-uniformity | 12.4 K between the hottest (dT5, avg 43.2 K) and coolest (dT7, avg 30.8 K) TC positions | about 36 % of the mean dT |
| Derived bulk coolant rise | ~12-13 K | 15 kW at 18 LPM, PG25-class fluid (cp ~3.85 kJ/kg-K, rho ~1.02 kg/L) |
| Derived caloric resistance 1/(m*cp) | ~0.00083-0.00085 K/W | ~36 % of the mean R is simply fluid heating; it is a floor unless flow rises |
| Pressure drop | **not disclosed** | the single most important missing number |
| Heater footprint / heat flux | **not disclosed** | prevents area-normalised (cm2-K/W) comparison |
| TIM | "standard thermal paste" | a 0.1 cm2-K/W grease on a 100 cm2 footprint alone costs 0.001 K/W = 15 K at 15 kW; on 200 cm2, 7.5 K |
| Construction | Split-Flow microchannel, "proven mass-manufacturing techniques" | skived/brazed copper implied, not stated |

CoolIT's own prior data points for scale [4][5]:

| CoolIT product | Rated | R (K/W) | Flow | Pressure drop | Other |
|---|---|---|---|---|---|
| 4000 W coldplate (Mar 2025) | 4 kW | **< 0.009** (Tcase,max to inlet, incl. TIM) | 6.06 LPM (= 1.5 LPM/kW) | ~8 psi (~55 kPa) **full loop incl. fittings and QDs** | 97.3 % heat capture; Split-Flow "30 % better" (vendor); built with OMNI all-metal joining |
| OMNI all-metal coldplates (2025) | > 1,500 W TDP | "up to 60 % lower than standard microchannel coldplates" (vendor) | n/a | n/a | > 300 W/cm2; unibody, no braze, no CTE mismatch [6][7] |
| 15 kW coldplate (Jun 2026) | 15 kW | 0.0023 mean / 0.0030 worst | 18 LPM | not disclosed | see above |

Observation: 4 kW at < 0.009 K/W implies dT < 36 K; 15 kW at 0.0023 K/W implies dT = 34 K. CoolIT has held dT roughly constant (~35 K at 45 C inlet, giving Tcase ~80 C) while scaling area and flow 3.75x. The absolute K/W therefore says little about intrinsic (area-specific) performance; the 15 kW plate is a scaling demonstration, not evidence of a lower cm2-K/W figure.

---

## 2. Competitor findings (per vendor)

### Tier 1 DLC specialists

**Boyd (Lytron/Aavid heritage).** On NVIDIA's recommended vendor list for cold plates, manifolds and CDUs; sells GB200 NVL72 cold plates and builds Google's Deschutes CDU [8][9][10]. No public thermal-resistance or W/cm2 figures for its GPU plates; the standard CPU/GPU datasheet shows R-vs-flow and dP-vs-flow curves only as graphs [11]. Only numeric Boyd datasheet found: Infineon HybridKIT DSC plate (power module, not GPU): Rth 0.026 K/W, max dP 125 mbar (12.5 kPa) at 10 LPM 50/50 WG [12].

**Vertiv (CoolTera acquisition, CoolChip).** Publishes CDU numbers, not cold plate numbers: CoolChip CDU 100 / 450 / 600 / 1,350 kW (also 121 kW and 2,300 kW variants listed) at 4 C approach [13]; GB200 NVL72 7 MW reference architecture, up to 132 kW/rack, co-developed with NVIDIA (Oct 2024) [14]. CoolTera cold plate data did not surface in the searches.

**Motivair (Schneider Electric).** "Dynamic Cold Plates": no skived microchannels, wide grooves with dynamic fluid distribution; launched at "up to 1,000 W per processor"; variants for MI300X, Ice Lake, SP3; series/parallel push-lock and dripless QDs [15][16][17]. CDUs 105 kW-2.5 MW. No R, flow or dP numbers published.

**nVent.** NVIDIA reference architecture (Nov 2024) is CDU + liquid-to-air + manifolds, not cold plates [18]; SC25 portfolio of row/rack CDUs and TCS manifolds [19]; Project Deschutes CDU 2 MW @ 3 C ATD, 500 GPM [20]. No cold plate numbers found.

**Asetek.** Exited HPC in 2021 [21]; data center liquid-cooling assets described by the company as "dormant"; a 2025 indication of interest for the liquid cooling business, buyer unnamed, no deal confirmed [22]. "InfraCool" returned nothing. Not a current competitor.

**JetCool (Flex) - microjet, single-phase.** H100 SmartPlate: 0.021 K/W at 3.2 LPM (vendor; vs 0.122 K/W air) [23]; third-party test claims ~25 % better than microchannel at 50 C PG25 inlet [24]; "beyond 1,500 W today" [25]. Datasheets for SP5 Turin (> 500 W) and RTX PRO 6000 (600 W). No multi-kW data.

**Mikros Technologies (Jabil since 1 Oct 2024) - Normal Flow.** Core thermal resistance "as low as 0.02 C-cm2/W" (< 0.018 on optics page); "> 1 kW/cm2 with as low as 30 C surface rise and 3 psi (20.7 kPa) drop" [26][27][28]; Ascutney AX-NV1 (H100) and AX-NV2 (Blackwell) plates exist but no numbers surfaced [29]. Jabil deal terms undisclosed [30]. "Dynamic Metals" was not searched (budget).

### OEM / system vendors

**Lenovo Neptune.** Inlet 18-45 C; coolant rise ~10-15 K through the plates; up to 100 % heat capture; copper water loops, patented CPU plates; some aluminium plates in the N1380 [31][32][33]. No R figures; no evidence of direct-to-die.

**HPE Cray EX / GX.** EX cold plates "handle chips in excess of 500 W" [34]; EX4000 ~400 kW/rack (third-party) [35]; GX is 100 % warm-water (40 C) fanless, ~400 kW/rack, 900 mm cabinet [36][37]; HPE claims 37 % less cooling power per blade vs hybrid DLC [38]. No plate-level numbers.

**Supermicro DLC-2.** Inlet up to 45 C; up to 98 % heat capture per rack; 250 kW in-rack CDU; plates on CPU, GPU, memory, PCIe switch and VRs [39]. No plate numbers.

**Dell IR7000.** Rack built for up to 480 kW with "nearly 100 %" heat capture; PowerCool is an enclosed rear-door HX (32-36 C water, up to 60 % cooling energy saving), not a cold plate [40][41]. No plate numbers.

### Asian ODM / component makers

**AVC (Asia Vital Components).** Estimated 40-50 % share of GB200/GB300 cold plates; already developing Vera Rubin plates for 1,800-2,300 W GPUs; 2024 revenue NT$71.8 bn [42][43]. No published thermal data.

**Auras, Cooler Master, Delta, Nidec, Foxconn/Ingrasys, Quanta/QCT.** No plate-level thermal numbers published. Cooler Master: single sealed direct-to-chip module [44]. Delta: copper microchannel base, custom designs [45]. Nidec: Deschutes CDU prototype 2 MW / 80 psi, > 5,000 CDUs shipped, cold-plate and QD capacity being added in Thailand/Philippines/China [46][47]. Foxconn claims its plates "boost heat transfer efficiency by more than 30 %" vs typical (vendor, no baseline) [48]; Ingrasys GB300 rack ~120 kW liquid with 1/4-in QDs, Vera Rubin > 200 kW with 1/2-in (LinkedIn, unverified) [49]. QCT: QoolRack L2A up to ~75 kW, cold plate sourcing not stated [50].

**Wiwynn (with Fabric8Labs).** Double-sided cold plate rated **up to 4 kW** (accelerator + vertical power ICs together), proprietary microchannels made by electrochemical 3D printing, "expects up to 40 % improvement" [51]; 3.5 kW ECAM plate shown at Computex 2025; ECAM session on "> 350 W/cm2" [52]; Aug 2026: NexGen double-sided and two-phase ECAM plates [53].

### Advanced manufacturing / design-tool players

**Fabric8Labs (ECAM).** Hot Chips 2023: 35 % thermal-resistance improvement, 100-1,000 W test [54]. UIUC + Fabric8 paper, Cell Reports Physical Science (2026), topology-optimised pure-copper plate: **32 % lower R at equal flow; 68 % lower dP at equal R** vs conventional pin fins, on a 2x2 GaN array (not a GPU); 30-50 um features; ~1,000 optimisation iterations [55][56][57]. Wiwynn demo: "48 % better than skived microchannel" (vendor) [58]; OCP 2025: "200 % improvement in temperature variance" (vendor, no baseline) [59]; marketing page "up to 8.2 C cooler" [60]. Giga Computing collaboration July 2026 [61]. No K/W, dP or price published for a GB200-class plate.

**Corintis (Microsoft).** In-chip microfluidics (channels etched in the die): up to **3x heat removal vs cold plates; 65 % lower max silicon temperature rise**; > 80 % lower vs air; $24 M Series A, Sept 2025; no deployment timeline [62][63][64]. Not a drop-in cold plate; requires silicon co-design.

**Diabatix (ColdStream).** Generative-design SaaS; EV cold plate case reports 25 % lower R, 15 % better uniformity, 50 % lower dP (attribution to the plate case uncertain); heatsink case 55 % lower R at equal dP [65][66]. No AI-GPU plate benchmark found.

### Hyperscaler / silicon reference designs

**NVIDIA GB200 / GB300.** Rack TDP ~140 kW NVL72 (TrendForce) [67]. Secondary "datasheet" numbers for a GB200 plate: 1.8 LPM/plate, 45 C inlet, PG25, **< 20 kPa, < 0.03 K/W** target, skived fins <= 0.5 mm [68]; Introl: ~80 L/min per rack (~0.6 LPM/kW), 1.5 bar [69]. These conflict and none is an NVIDIA document. Naddod's GB300 blog (liquid-metal TIM 0.02 cm2-K/W, < 0.3 mm channels, 2-4 m/s, titanium >= 10 bar) is low-reliability [70].

**NVIDIA Vera Rubin / Rubin Ultra / Kyber.** Rubin GPU 1,800 W (Max-Q) to ~2,300 W (Max-P), 100 % liquid, third-gen MGX designed for 45 C inlet (secondary sources citing NVIDIA blog) [71][72]; Rubin Ultra ~3,600 W/GPU (4 dies + 16 HBM4E) [73]; NVL576 Kyber ~600 kW, 2H 2027, needs a sidecar rack [74][75]. Cooling BOM ~$50 k per Blackwell Ultra NVL72, ~$55.7 k for VR NVL144, GPU plates rising to ~$400 each [73][76]. No NVIDIA plate R/dP published.

**Google TPU (Hot Chips 2025, OCP).** Split-flow cold plate found to beat straight-through; chips plumbed in series, capacity budgeted for the last chip; bare-die since TPUv4 (1.6x TPUv3 power); facility and TPU loops isolated; ~1 GW of liquid cooling over ~2,000 pods; CDU fleet availability ~99.999 % since 2020 [77][78]. Project Deschutes 5th-gen CDU (built by Boyd, contributed to OCP): **2 MW at 3 C ATD, 80 psi available** "to enable advanced cold plate designs" [79][80]. No plate R numbers.

### Peer-reviewed state of the art (single-phase water)

| Study | Geometry / material | Result | Source |
|---|---|---|---|
| ORNL, IJHMT vol. 256, Mar 2026 | 75 x 75 mm diamond pin-fin, Cu and CuW with integrated CuW spreader | chip-to-coolant incl. TIM **6.9 K/kW (Cu), 9.0 K/kW (CuW) at 1 kW, dP 9.0 kPa**, water; diamond pins ~15 % lower R than straight microchannel; CuW for low-CTE direct-to-die | [81][82] |
| PKU, Nature Electronics, Sep 2025 | 3-tier manifold + jet + sawtooth microchannel, 25 um channels, ~100 mL/min | **3,000 W/cm2 at 0.9 W/cm2 pumping power; 1,000 W/cm2 at 65 K rise (= 0.065 cm2-K/W), COP 13,000** | [83] |
| Bio-inspired Cu manifold microchannel, Energy 2025 | copper | ~2,000 W (633 W/cm2), **25.2 kPa, 0.0878 cm2-K/W** | [84] |
| Z-manifold cooler (cited 2025 review) | silicon/metal | 1,800 W/cm2 at 6 g/s, 54 kPa, 0.075 cm2-K/W | [84] |
| Stanford 3D manifold (2018/2020) | silicon | 250 W/cm2 at Tmax 90 C, < 3 kPa at 0.1 L/min; simulations to 850 W/cm2 | [85] |
| NTU embedded microfluidic diamond spreader | thinned GPU, research | junction-to-fluid 0.02 K/W at 2,000 W | [86] |
| ACT two-phase cut sheet (vendor comparison table) | n/a | typical single-phase plate ~0.150 cm2-K/W vs two-phase 0.080 | [87] |

---

## 3. Master comparison table

R = case/chip-to-inlet unless noted. "V" = vendor claim, "I" = independent / peer-reviewed, "S" = secondary (blog/analyst).

| Vendor / product | Rated power | R (K/W) | R" (cm2-K/W) | Flow | dP | Heat flux | Mfg / material | Price hint | Date | Type |
|---|---|---|---|---|---|---|---|---|---|---|
| **CoolIT 15 kW** (benchmark) | 15 kW | 0.0023 mean / 0.0030 worst | n/a (area undisclosed) | 18 LPM (1.2 LPM/kW), WG, 45 C | **n/d** | n/d | Split-Flow microchannel, mass-mfg, paste TIM | n/d | Jun 2026 | V |
| CoolIT 4000 W | 4 kW | < 0.009 incl. TIM | n/a | 6.06 LPM (1.5 LPM/kW) | ~55 kPa full loop incl. QDs | n/d | OMNI all-metal joining | n/d | Mar 2025 | V |
| CoolIT OMNI | > 1.5 kW | "60 % lower than std microchannel" | n/d | n/d | n/d | > 300 W/cm2 | unibody all-metal | n/d | 2025 | V |
| ORNL Cu diamond pin-fin | 1 kW (test) | **0.0069** incl. TIM | ~0.39 over 56 cm2 footprint (derived) | n/d | **9.0 kPa** | ~18 W/cm2 avg | machined/AM Cu, CuW | research | Mar 2026 | I |
| ORNL CuW | 1 kW | 0.0090 incl. TIM | ~0.51 (derived) | n/d | 9.0 kPa | ~18 | CuW (low CTE) | research | Mar 2026 | I |
| ToneCooling GB300-class plate | ~1,067 W | 0.0130-0.0133 | n/d | 1.7 LPM (1.6 LPM/kW) | 12.06 kPa | n/d | copper | n/d | 2025-26 | V (S) |
| Generic GB200 plate target (FiberMall) | ~1.2 kW | < 0.03 | n/d | 1.8 LPM, PG25, 45 C | < 20 kPa | n/d | skived Cu, <= 0.5 mm fins | n/d | 2025 | S |
| JetCool H100 SmartPlate | 700 W class | 0.021 | n/d | 3.2 LPM (4.6 LPM/kW) | n/d | n/d | microjet | n/d | Apr 2024 | V (+3rd-party relative test) |
| Wakefield on-chip plate | n/d | 0.0267 | n/d | n/d | n/d | n/d | n/d | catalogue part | 2025 | V |
| Boyd HybridKIT DSC (power module) | n/d | 0.026 | n/d | 10 LPM 50/50 WG | 12.5 kPa | n/d | n/d | n/d | n/d | V |
| Mikros Normal Flow | n/d | n/d | **0.02 core** (< 0.018 optics) | n/d | **~20.7 kPa (3 psi) at 1 kW/cm2** | **> 1,000 W/cm2** at 30 K rise | normal-flow microchannel matrix | n/d | 2024-25 | V |
| Wiwynn double-sided ECAM | **4 kW** | n/d ("up to 40 % better" expected) | n/d | n/d | n/d | > 350 W/cm2 (ECAM) | ECAM Cu | n/d | 2025 | V |
| Fabric8Labs / UIUC TO plate | GaN 2x2 array | -32 % vs pin fin | n/d | equal flow | **-68 % at equal R** | n/d | ECAM pure Cu, 30-50 um | n/d | 2026 | I |
| Fabric8 / Wiwynn Computex | 3.5 kW | "48 % better than skived" | n/d | n/d | n/d | n/d | ECAM Cu | n/d | May 2025 | V |
| Corintis / Microsoft | GPU (Teams workload) | 3x heat removal vs cold plate; -65 % max Si rise | n/d | n/d | n/d | n/d | in-die etched channels | n/d | Sep 2025 | V (Microsoft) |
| PKU jet-manifold | lab chip | n/d | **0.065 at 1,000 W/cm2** | ~0.1 L/min | pumping 0.9 W/cm2 at 3,000 W/cm2 | **3,000 W/cm2** | silicon microfab | research | Sep 2025 | I |
| Bio-inspired Cu manifold | ~2 kW | n/d | 0.0878 | n/d | 25.2 kPa | 633 W/cm2 | copper | research | 2025 | I |
| Motivair Dynamic Cold Plate | up to 1 kW/processor (launch) | n/d | n/d | n/d | n/d | n/d | wide grooves, no skiving | n/d | 2023-25 | V |
| Lenovo Neptune | node-level | n/d | n/d | 18-45 C inlet, 10-15 K rise | n/d | n/d | Cu loops (some Al) | n/d | 2024-25 | V |
| HPE Cray EX / GX | > 500 W chips; ~400 kW/rack | n/d | n/d | 40 C (GX) | n/d | n/d | n/d | n/d | 2024-25 | V/S |
| Supermicro DLC-2 | 250 kW/rack CDU | n/d | n/d | <= 45 C inlet | n/d | n/d | n/d | n/d | May 2025 | V |
| Dell IR7000 | up to 480 kW/rack | n/d | n/d | eRDHx 32-36 C | n/d | n/d | n/d | n/d | 2024-25 | V |
| AVC | GB200/GB300 (40-50 % share), VR 1.8-2.3 kW | n/d | n/d | n/d | n/d | n/d | skived Cu (industry norm) | n/d | 2025-26 | S |
| NVIDIA Rubin / Rubin Ultra (requirement) | 2.3 kW / 3.6 kW per GPU | n/d | n/d | 45 C inlet | n/d | n/d | n/d | plates ~$400; ~$55.7 k per NVL144 cooling BOM | 2026-27 | S |
| Google TPU / Deschutes | n/d per chip | n/d | n/d | series chips, 80 psi available | n/d | n/d | split-flow Cu, bare die | n/d | Aug-Oct 2025 | V (Google) |
| Industry ASP (IDTechEx) | GPU plate | - | - | - | - | - | - | **$300-500 per plate; ~$2,300 per 8-GPU server; ~$55 k per rack** | 2025 | S |

n/d = not disclosed / not found.

---

## 4. Who is state of the art, per metric

1. **Absolute thermal resistance at > 4 kW.** No competitor publishes any K/W figure above ~4 kW. CoolIT's 15 kW plate (0.0023 K/W mean) stands alone at that scale; the nearest hardware is Wiwynn's 4 kW double-sided ECAM plate and the 3.5 kW Wiwynn/Fabric8 plate, both without numbers. The benchmark is therefore "uncontested" mainly because nobody else has published, not because it is intrinsically superior.

2. **Absolute R at GPU scale (~1 kW), with pressure drop stated.** ORNL's copper diamond pin-fin plate (0.0069 K/W incl. TIM at 1 kW, 9 kPa, water, peer-reviewed, Mar 2026) is the best fully-specified datapoint, ahead of ToneCooling (0.013 K/W, 12 kPa), JetCool (0.021 K/W at 3.2 LPM) and the generic GB200 target (< 0.03 K/W, < 20 kPa). CoolIT's own 4 kW plate (< 0.009 K/W) is close to ORNL on K/W but at 4x the power and with ~55 kPa full-loop dP.

3. **Area-specific resistance.** Mikros Normal Flow (0.02 cm2-K/W core, vendor) is the lowest claimed; peer-reviewed single-phase water results cluster at 0.065-0.09 cm2-K/W total (PKU, Z-manifold, bio-inspired manifold). A conventional skived plate is quoted by a two-phase competitor at ~0.15 cm2-K/W. CoolIT's figure cannot be computed (area undisclosed).

4. **Heat flux.** PKU 3,000 W/cm2 (lab silicon) >> Mikros > 1,000 W/cm2 (vendor) > Wiwynn/ECAM > 350 W/cm2 > CoolIT OMNI > 300 W/cm2. GPU-package average flux today is only ~20-40 W/cm2 at package level (e.g. 1 kW over 56 cm2 = 18 W/cm2), so flux capability is not the binding constraint; conduction spreading, TIM and caloric rise are.

5. **Pressure drop / pumping power.** Best published: Mikros ~20.7 kPa at 1 kW/cm2 (vendor); ORNL 9 kPa at 1 kW (I); ToneCooling 12 kPa at 1.7 LPM (V); Fabric8/UIUC -68 % dP at equal R vs pin fins (I). Facility headroom is rising: Google Deschutes offers 80 psi (550 kPa) and OCP allows TCS components to see up to 100 psi (690 kPa) [88], so the industry is explicitly budgeting for higher-dP, higher-performance plates. CoolIT discloses only the 4 kW full-loop value (~55 kPa) and nothing for 15 kW.

6. **Hot-spot uniformity.** CoolIT 15 kW: 12.4 K spread across 8 TCs (36 % of mean dT). Fabric8/Wiwynn claim "200 % improvement in temperature variance" via power-map-tailored fins (vendor, no baseline). Corintis claims -65 % max silicon rise (in-die). Diabatix claims +15 % uniformity on an EV plate. No competitor publishes a per-TC map like CoolIT's; the benchmark is the only quantified uniformity dataset.

7. **Manufacturability and cost.** Incumbent volume technology is skived/brazed copper microchannel (AVC ~40-50 % of GB200/GB300 plates). ASP $300-500 per GPU plate (IDTechEx), rising to ~$400 for Rubin-class (Igor's Lab/TrendForce-type estimates). CoolIT emphasises "proven mass-manufacturing" and an all-metal unibody (OMNI) that removes braze and CTE-mismatch risk. ECAM (Fabric8) and topology optimisation give the biggest measured deltas (-32 % R / -68 % dP) but are not yet proven at GB200 volume or price.

8. **Reliability.** Differentiators cited: CoolIT OMNI unibody (no braze, no dissimilar-metal CTE); ORNL CuW for de-lidded direct-to-die CTE match; Google 99.999 % CDU availability with isolated loops and filtration; NVIDIA/ODMs moving to 1/2-in QDs for > 200 kW racks. No vendor publishes plate-level MTBF, corrosion or clogging data.

9. **Scalability to > 20-30 kW.** Silicon roadmap: Rubin 2.3 kW, Rubin Ultra ~3.6 kW per package (2027), 600 kW Kyber racks, 1 MW Google racks. Only CoolIT (15 kW) and Wiwynn (4 kW double-sided) have shown multi-kW single-package plates; CoolIT's own roadmap names direct-to-die and micro-channel lids as the next step, implicitly conceding that paste-TIM lidded plates are near their limit.

10. **Inlet temperature.** 45 C (W45) is now the de-facto AI standard (CoolIT, Supermicro DLC-2, Lenovo Neptune, NVIDIA gen-3 MGX); HPE GX runs 40 C; Uptime notes a typical 40 C limit for GPU rack coolant supply [89]. Nobody publishes performance at > 45 C.

---

## 5. Implications for a design that must beat the benchmark (research-derived, for the design team)

- The disclosed benchmark is a *system* number: ~12-13 K of the 34.4 K mean dT is bulk coolant heating at 1.2 LPM/kW. Any design judged at the same 1.2 LPM/kW cannot remove that term; counter-flow / split-flow / multi-pass-balanced layouts, or a higher LPM/kW (the Deschutes 80 psi budget invites this), are the levers.
- The TIM term is large at this scale: paste at ~0.1 cm2-K/W on a plausible 100-200 cm2 heater footprint is 7-15 K. Liquid-metal (0.02 cm2-K/W, Naddod secondary) or direct-to-die (ORNL CuW, Google bare-die) attack the biggest single resistance CoolIT left on the table.
- Peer-reviewed geometries (ORNL diamond pins -15 % R; UIUC topology-optimised -32 % R / -68 % dP; manifold microchannels 0.065-0.09 cm2-K/W) are all achievable by machining, skiving-plus-brazing, chemical etching or ECAM; none requires powder-bed printing.
- The benchmark's 12.4 K hot-spot spread is the easiest metric to beat visibly: power-map-tailored fin density (Fabric8/Wiwynn approach) or zoned parallel feeds.
- Pressure drop is undisclosed by CoolIT at 15 kW; publishing a full curve (plate-only and with QDs) at 18 LPM would itself be a competitive differentiator under the new OCP Cold Plate Test Specification V1.0.0 (Oct 2026) [90].

---

## 6. Gaps / unknowns

- CoolIT 15 kW: pressure drop, heater footprint/heat flux, TIM thickness, plate dimensions, materials, fin geometry, cost. None disclosed; DCD notes it was validated on a TTV only [2].
- No vendor other than CoolIT publishes K/W for any plate above ~1.1 kW (ToneCooling) / 4 kW (CoolIT). Wiwynn 4 kW and Fabric8 3.5 kW plates: no R, dP or flow.
- Boyd, Vertiv/CoolTera, Motivair, nVent, Auras, AVC, Cooler Master, Delta, Nidec, Foxconn/Ingrasys, Quanta, Jabil/Mikros Ascutney, Lenovo, HPE, Supermicro, Dell: no numeric plate R/dP found in search extracts; Boyd's datasheet curves and Motivair brochures exist as PDFs but could not be fetched (network blocked).
- NVIDIA GB200/GB300/Rubin cold plate requirements (flow per plate, dP budget, TCS supply temp) only via conflicting secondary sources (0.6-1.5 LPM/kW; 20-150 kPa). The origin of the "1.2 LPM/kW industry standard" could not be verified (search budget hit before that query ran).
- Google: no per-chip TDP or plate R from Hot Chips 2025 extracts; Ironwood per-chip power query not run.
- Asetek "InfraCool" and Mikros "Dynamic Metals": not found / not searched.
- Diabatix: only EV/heatsink case numbers; no AI-GPU benchmark.
- Corintis numbers are Microsoft's, on a Teams workload, baseline unspecified.
- ORNL etched-copper "5 K/kW at 2 kW" result [91] uses R1233zd(E) (likely two-phase) and is excluded from single-phase ranking pending a full read.
- Area-normalised comparison of the benchmark is impossible without the heater area; the derived R" values for ORNL assume the full 75 x 75 mm footprint is heated.
- Queries planned but not run (budget): ToneCooling and FiberMall datasheet verification, CoolIT 4 kW brief TTV size, "1.2 LPM/kW" origin, Mikros AX-NV2 specs, Vertiv/CoolTera, Google Ironwood TDP, Lenovo SC777 node power, NVIDIA June 2026 cooling announcement, Wakefield 0.0267 K/W conditions, Boyd datasheet curve values, NVIDIA GB200 dP budget.

---

## 7. Sources

1. CoolIT 15 kW press release, 1 Jun 2026 - https://www.coolitsystems.com/resources/news/15kw_press_release/
2. DCD, "CoolIT designs 15kW coldplate..." - https://www.datacenterdynamics.com/en/news/coolit-designs-15kw-coldplate-to-future-proof-liquid-cooling-for-gpus/
3. Electronics360, Computex 2026 - https://electronics360.globalspec.com/article/23837/computex-2026-coolit-pushes-single-phase-dlc-to-15-kw
4. CoolIT 4000W Technical Brief (R2, Mar 2025) - https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
5. CoolIT 4000W press release, 13 Mar 2025 - https://www.coolitsystems.com/resources/news/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership/
6. CoolIT OMNI product page - https://coolitsystems.com/?p=4082
7. StorageReview, OMNI all-metal coldplates - https://www.storagereview.com/news/coolit-systems-omni-all-metal-cold-plates-unveiled
8. Boyd collaboration with NVIDIA - https://www.boydcorp.com/boyds-collaboration-with-nvidia.html
9. Boyd cold plates for AI server cooling - https://www.boydcorp.com/thermal/liquid-cooling-systems/liquid-cold-plates/cold-plates-for-ai-server-cooling.html
10. Boyd cooling for NVIDIA AI systems - https://welcome.boydcorp.com/boyd-cooling-for-nvidia-ai-systems
11. Boyd standard CPU/GPU liquid cold plate datasheets - https://info.boydcorp.com/hubfs/Thermal/Liquid-Cooling/Boyd-Standard-CPU-Liquid-Cold-Plate-Datasheets.pdf
12. Boyd HybridKIT DSC cold plate datasheet - https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf
13. Vertiv CoolChip CDU - https://www.vertiv.com/zh-CN/products-catalog/thermal-management/high-density-solutions/vertiv-coolchip-cdu/
14. Vertiv GB200 NVL72 reference architecture (Oct 2024) - https://investors.vertiv.com/news/news-details/2024/Vertiv-Codevelops-with-NVIDIA-Complete-Power-and-Cooling-Blueprint-for-NVIDIA-GB200-NVL72-Platform/default.aspx
15. DCD, Motivair Dynamic Cold Plates - https://www.datacenterdynamics.com/en/news/motivair-launches-dynamic-cold-plates-without-skived-microchannels/
16. Motivair Dynamic Cold Plates - https://www.motivaircorp.com/products/dynamic-cold-plates/
17. Motivair MI300X cold plate - https://www.prweb.com/releases/motivair-launches-revolutionary-dynamic-cold-plate-for-amds-mi300x-302247342.html
18. nVent + NVIDIA (Nov 2024) - https://businesswire.com/news/home/20241118649897/en/nVent-Collaborates-with-NVIDIA-on-AI-Ready-Liquid-Cooling-Solutions/
19. nVent SC25 portfolio - https://www.businesswire.com/news/home/20251117098362/en/nVent-Unveils-New-Liquid-Cooling-and-Power-Portfolio-at-SC25
20. nVent Project Deschutes CDU (OCP) - https://www.opencompute.org/?p=1743
21. HPCwire, Asetek exits HPC (2021) - https://www.hpcwire.com/2021/09/22/asetek-announces-it-is-exiting-hpc/
22. OC3D, Asetek may sell liquid cooling business - https://overclock3d.net/news/cases_cooling/asetek-may-sell-its-liquid-cooling-business-to-an-unknown-buyer/
23. BusinessWire, JetCool H100 SmartPlate (Apr 2024) - https://www.businesswire.com/news/home/20240430522600/en
24. JetCool third-party GPU testing - https://info.jetcool.com/hubfs/Marketing%20Resources%202024/Third%20Party%20Testing_JetCool_GPUs.pdf
25. JetCool data center liquid cooling - https://jetcool.com/data-center-liquid-cooling/
26. Mikros performance page - https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/
27. Mikros overview - https://www.mikrostechnologies.com/home/overview/
28. Mikros optics application page - https://mikrostechnologies.com/applications/optics.html
29. Mikros Ascutney series - https://_dmarc.mikrosmanufacturing.com/ascutney-series/
30. Jabil acquires Mikros (Oct 2024) - https://www.businesswire.com/news/home/20241003396998/en/Jabil-Acquires-Mikros-Technologies-to-Support-Demand-for-Liquid-Cooling-in-AI-Data-Centers
31. HPCwire, Lenovo Neptune expansion - https://www.hpcwire.com/off-the-wire/lenovo-expands-neptune-liquid-cooling-to-advance-sustainable-ai-infrastructure/
32. Lenovo Press DS0187 - https://lenovopress.lenovo.com/ds0187
33. Lenovo HPC User Forum deck (Oct 2024) - https://www.hpcuserforum.com/wp-content/uploads/2024/11/Lenovo_Vendor-Update_HPC-UF-HLRS-Oct-2024.pdf
34. HPE Cray EX QuickSpecs - https://www.hpe.com/us/en/collaterals/collateral.a00094635enw.html
35. Glenn Klockwood, Cray EX - https://www.glennklockwood.com/garden/cray-ex
36. Glenn Klockwood, Cray GX - https://www.glennklockwood.com/garden/cray-gx
37. HPE direct liquid cooling - https://www.hpe.com/us/en/solutions/direct-liquid-cooling.html
38. DCD, HPE fanless DLC - https://www.datacenterdynamics.com/en/news/hpe-introduces-fanless-direct-liquid-cooling-system-architecture
39. Supermicro DLC-2 press release (May 2025) - https://www.supermicro.com/en/pressreleases/supermicros-dlc-2-next-generation-direct-liquid-cooling-solutions-aims-reduce-data
40. TweakTown, Dell IR7000 480 kW - https://tweaktown.com/news/101839/dell-ir7000-with-direct-liquid-cooling-up-to-480kw-per-rack-gb200-nvl4-144-b200-gpus/index.html
41. StorageReview, Dell IR rack systems - https://www.storagereview.com/news/dell-announces-integrated-rack-scalable-systems-for-dell-ai-factory
42. TVBS, AVC cold plate share - https://news.tvbs.com.tw/english/3179423
43. Taiwan News, AVC - https://www.taiwannews.com.tw/en/news/6215881
44. Cooler Master GPU/CPU coldplate - https://www.coolermaster.com/en-global/products/GPU%2FCPU-Coldplate.html
45. Delta liquid cooling solutions - https://www.deltaww.com/en-US/products/liquid-cooling-solutions
46. Nidec Deschutes CDU sheet - https://www.nidec.com/v=1764743613/files/topics/19006_ext_5_en_0.pdf
47. TechNews TW, Nidec CDU shipments - https://technews.tw/?p=1321939
48. Taiwan News, Foxconn cold plates - https://www.taiwannews.com.tw/en/news/6311653
49. LinkedIn post, GB300/Vera Rubin QDs (unverified) - https://tw.linkedin.com/in/bill-wang-6a826366
50. QCT QoolRack for GB200 NVL72 - https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf
51. Wiwynn cold-plate liquid cooling - https://www.wiwynn.com/technology/advanced-cooling/cold-plate-liquid-cooling
52. Wiwynn at OCP 2025 - https://www.wiwynn.com/news/wiwynn-showcases-next-generation-ai-infrastructure-and-cooling-advances-at-ocp-global-summit-2025
53. D2P, Fabric8Labs/Wiwynn NexGen (Aug 2026) - https://www.d2pmagazine.com/2026/08/14/fabric8labs-wiwynn-collaborating-to-develop-nexgen-3d-printed-cold-plates-for-ai-data-centers/
54. Fabric8Labs Hot Chips 2023 - https://www.hc2023.hotchips.org/assets/program/conference/day2/FPGAs%20Cooling/Fabric8Labs%20-%202023%20Hot%20Chips%20-%20ECAM%20for%20Cooling%20High%20Performance%20ICs%20(2023.08.29).pdf
55. UIUC MechSE news - https://mechse.illinois.edu/news/82871
56. HostingAdvice, 32 %/68 % figures - https://www.hostingadvice.com/blog/a-novel-3d-printed-copper-tree-could-cut-ai-cooling-by-32/
57. Metal AM, copper AM cold plate - https://www.metal-am.com/copper-am-cold-plate-improves-ai-data-centre-cooling/
58. 3DPrinting.com, Fabric8/Wiwynn Computex 2025 - https://3dprinting.com/news/fabric8labs-and-wiwynn-to-demonstrate-ecam-cold-plate-technology-at-computex-2025/
59. PR Newswire, Fabric8 at OCP 2025 - https://www.prnewswire.com/news-releases/fabric8labs-to-showcase-advanced-ecam-cold-plate-solutions-with-wiwynn-at-ocp-global-summit-2025-302581679.html
60. Fabric8Labs ECAM vs legacy - https://www.fabric8labs.com/ecam-vs-legacy-liquid-cooling-cold-plates/
61. GIGABYTE / Fabric8Labs (Jul 2026) - https://www.gigabyte.com/fi/press/news/2436
62. DCD, Microsoft + Corintis - https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/
63. IEEE Spectrum, Corintis - https://spectrum.ieee.org/microfluidics-cooling-ai-chips-corintis
64. Tech.eu, Corintis $24M - https://tech.eu/2025/09/25/corintis-lands-24m-and-microsoft-endorsement-for-chip-cooling-tech/
65. Diabatix EV cooling blog - https://www.diabatix.com/blog/ai-driving-better-ev-cooling
66. Diabatix cold plate generative design - https://www.diabatix.com/blog/optimizing-cold-plate-performance-through-generative-design
67. TrendForce, GB200 rack TDP - https://www.trendforce.com/presscenter/news/20240730-12232.html
68. FiberMall, GB200 liquid cooling plate (secondary) - https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm
69. Introl, GB200 NVL72 deployment (secondary) - https://introl.com/blog/gb200-nvl72-deployment-72-gpu-liquid-cooled
70. Naddod, GB300 liquid cooling (low reliability) - https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling
71. TechPowerUp, Vera Rubin NVL144 - https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production
72. Barrack.ai, Rubin GTC 2026 breakdown (secondary) - https://blog.barrack.ai/nvidia-rubin-specs-architecture-2026/
73. Igor's Lab, NVL72 cooling cost / Rubin Ultra 3.6 kW - https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
74. DCD, Rubin Ultra NVL576 600 kW - https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027
75. DCD, GTC rack density analysis - https://datacenterdynamics.com/en/analysis/nvidia-gtc-jensen-huang-data-center-rack-density
76. TechRadar, $50k NVL72 cooling - https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks
77. Chips and Cheese, Google liquid cooling at Hot Chips 2025 - https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips
78. ServeTheHome, Ironwood at Hot Chips 2025 - https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/
79. Google Cloud blog, 1 MW racks and liquid cooling (OCP EMEA) - https://cloud.google.com/blog/topics/systems/enabling-1-mw-it-racks-and-liquid-cooling-at-ocp-emea-summit
80. DCD, Google Deschutes CDU - https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
81. ORNL / IJHMT 256 (Mar 2026), CuW diamond pin-fin cold plates - https://www.sciencedirect.com/science/article/pii/S0017931025014152 (OSTI: https://www.osti.gov/pages/servlets/purl/3375134)
82. Electronics Cooling (Apr 2026), CuW cold plates - https://www.electronics-cooling.com/2026/04/high-performance-copper-tungsten-cold-plates-for-direct-to-chip-single-phase-liquid-cooling/
83. Nature Electronics 8, 810-817 (2025), jet-enhanced manifold microchannels - https://www.nature.com/articles/s41928-025-01449-4
84. Energy (2025), bio-inspired manifold microchannel cooling - https://www.sciencedirect.com/science/article/abs/pii/S0360544225049114
85. Stanford, embedded cooling with 3D manifold - https://nanoheat.stanford.edu/wp-content/uploads/2019/09/1-s2.0-S0017931018326206-main.pdf
86. NTU, embedded microfluidic diamond spreader - https://scholars.lib.ntu.edu.tw/handle/123456789/739908
87. ACT two-phase cold plate cut sheet (Nov 2025) - https://www.1-act.com/wp-content/uploads/2025/11/TPCP-CS-01_TwoPhaseColdPlates-DataCenters-CutSheet_V1_2025-11-12_Web.pdf
88. OCP L-LCDU test methodology (TCS up to 100 psi; 17-65 C; ASHRAE W classes) - https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
89. Uptime Institute (40 C GPU coolant supply limit) - https://intelligence.uptimeinstitute.com/entity_pdf/node/153594/pdf
90. OCP Single-Phase Direct-to-Chip Cold Plate Test Specification V1.0.0 (Oct 2026) - https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
91. Scalably etched copper cold plates with R1233zd(E) - https://www.sciencedirect.com/science/article/pii/S0017931025012736
92. Wakefield on-chip cold plate (Mouser) - https://www.mouser.in/new/wakefield/wakefield-thermal-on-chip-liquid-cold-plates/
93. ToneCooling GB300 NVL72 cold plate (fetch blocked; numbers from search extract) - https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/
94. IDTechEx cold plate ASP (repost) - https://onartificialintelligence.com/articles/34213/two-phase-d2c-cooling-in-data-center-thermal-management-cost-analysis
95. Schneider blog on CDU rating / TCS pressure drop - https://blog.se.com/datacenter/2025/12/16/account-for-filtering-too-beware-of-how-cdu-rating-capacity-is-specified/
