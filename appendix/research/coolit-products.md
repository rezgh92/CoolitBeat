# CoolIT Systems deep dive: cold-plate technology, portfolio, business and weaknesses

*Research sweep for the "beat the CoolIT 15 kW cold plate" programme. Compiled 2026-10-13. WebFetch/curl were blocked in this container, so every fact below comes from search-engine snippets of the cited pages plus the 15 kW tech brief supplied locally. Vendor claims are labelled as such; derived numbers are labelled "derived".*

---

## 1. The benchmark: CoolIT 15 kW coldplate (tech brief, June 2026)

Source: CoolIT 15 kW Tech Brief (local copy, `appendix/pdf/brief.txt`), press release 1 June 2026 (https://www.coolitsystems.com/resources/news/15kw_press_release/), DCD (https://www.datacenterdynamics.com/en/news/coolit-designs-15kw-coldplate-to-future-proof-liquid-cooling-for-gpus/), Electronics360 (https://electronics360.globalspec.com/article/23837/computex-2026-coolit-pushes-single-phase-dlc-to-15-kw).

| Item | Value | Note |
|---|---|---|
| Announced | 1 June 2026 (Computex 2026, Taipei) | "first 15kW coldplate design" (vendor) |
| Architecture | Split-Flow microchannel, "industry-leading internal geometries, proven mass-manufacturing techniques", standard thermal paste TIM | geometry not disclosed |
| TTV | 4 ceramic heaters (GPU + HBM zones), 15 kW total, 8 thermocouples at heater surface | footprint not disclosed |
| Samples | 3 cold plates | plate-to-plate avg dT spread 32.5 / 35.2 / 35.6 C |
| Coolant | water-glycol, 1.2 LPM/kW = **18 LPM** (derived) | inlet 45 C |
| Avg case-to-inlet dT | **34.4 C** (range 26.8 to 44.2 C) | avg Tcase ~80 C; hottest TC ~89 C |
| Avg thermal resistance (case-to-inlet, incl. TIM) | **0.00229 C/W** (derived: 34.4/15000) | max-TC basis 0.00295 C/W; min 0.00179 C/W |
| Hot-spot non-uniformity | TC5 is the hottest on all 3 plates (41.5 / 44.2 / 44.0 C); intra-plate spread 14.7 to 16.6 C | HBM-vs-GPU zone or far-from-inlet zone; strong design target |
| Coolant temperature rise | ~12.5 K (derived: 15 kW / (0.306 kg/s x ~3.9 kJ/kgK for PG25)); outlet ~57.5 C | caloric resistance 1/(m cp) ~0.00084 K/W = ~37 % of the total average resistance |
| Pressure drop / pumping power | **NOT disclosed** | biggest open gap; the 4 kW plate was 8 psi full-loop at 6 LPM |
| Status | TTV demonstration; not a shipping SKU | "design", not product |

Derived observation: the 4 kW plate (50 x 50 mm, Tr < 0.009 C/W) gives a unit-area resistance of ~0.225 cm2-K/W. If the 15 kW plate kept the same per-area performance, its heated footprint would be ~100 cm2 (0.00229 x 100 = 0.23 cm2-K/W) and heat flux ~150 W/cm2. This is an inference, not a disclosed figure, but a Rubin-class multi-die package with HBM (4 heaters) is consistent with it.

Press framing: CoolIT says 15 kW is >10x today's GPU need and ~4x the March 2025 4 kW plate; Blackwell up to 1,200 W, Rubin up to 2,300 W, Rubin Ultra Kyber rack ~600 kW in 2H2027 (DCD, https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027). Dylan Patel (SemiAnalysis) is quoted in the release but only generically. Electronics360 notes that single-phase DLC scaling "has been called into question" and that the data are vendor-only.

---

## 2. Split-Flow architecture (patented)

Sources: Split-Flow tech brief R1, 8 May 2024 (https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf; Scribd mirror https://www.scribd.com/document/1025620831/Split-Flow-Technology-CoolIT-Tech-Brief), coldplate technology page (https://www.coolitsystems.com/coldplate-technology/), patents US 8,746,330 (https://patents.google.com/patent/US8746330B2/en) and US 9,603,284 (https://patents.google.com/patent/US9603284B2/en), insideHPC 2014 (https://insidehpc.com/2014/06/coolit-systems-patents-split-flow-heat-exchanger/).

- Mechanism: coolant enters a groove/slot over the **middle** of the microchannel fin array, splits and flows outward to outlets at both ends. Each channel region carries ~half the inlet mass flow over ~half the length. Patent text: this "lowers pressure drop compared with flow running the full channel length" and "lessens the required pump force".
- Vendor claims: "30% better thermal and flow performance than standard coldplates" (4 kW press release, March 2025, https://www.coolitsystems.com/resources/news/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership/); "drastically reduces internal pressure drop" and "reduces case-to-fluid thermal resistance" (coldplate technology page). Baseline and test conditions for the 30% are **not published**. No thermal-resistance-vs-flow or dP-vs-flow curves surfaced in any indexed copy of the brief.
- Used in "all CoolIT coldplates" (brief). The inlet slot sits over the die centre, which is also why CoolIT markets "hot-spot targeting".
- Patent family: US 8,746,330 B2 (application 12/189,476, 2008 filing, inventor Geoff Sean Lyon) and continuation US 9,603,284 B2 (application 14/283,163). A 2008 filing implies ordinary expiry around **2028** (20 years from filing plus any term adjustment) - inference; verify on USPTO Patent Center. CoolIT lists 8,746,330 on its patent marking page (https://www.coolitsystems.com/patents/).
- Independent science: Kisitu & Ortega (Villanova, InterPACK 2021; NSF PAR https://par.nsf.gov/biblio/10341820) built analytical models for top-in/side-exit (split-flow) microchannel cold plates: splitting halves branch flow rate and flow length, which lowers dP and raises h because flow stays thermally developing; but **geometrically identical split-flow and parallel-flow cold plates show similar thermal resistance** - i.e. the benefit is mainly hydraulic (lower dP at equal flow) or thermal only when the dP saving is re-spent on flow or finer fins. Parametric runs used 10.01 mL/s (thermal) and 8.12 mL/s (dP), channel aspect ratio 6 to 24, jet slot aspect ratio 0.17.

Implication for us: Split-Flow is a 2008-era idea whose core patent is near end of life; a two-slot (quad-split) or manifold-microchannel (distributed inlet/outlet) layout gives shorter flow lengths again and is not blocked by it (check continuations and US 12,188,733 family).

---

## 3. Skived microchannel coldplates

Sources: Skived Coldplate Technical Brief (URL path /uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf - the "Feb26" is almost certainly 26 Feb 2021, not 2026, given the upload folder) https://coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf; DCK repost https://datacenterknowledge.com/cooling/skived-coldplates-technical-brief; DCF tour 2026 https://www.datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale.

- Process: a planer cuts thin slices of the copper base and bends them up into fins, so fins and base are one piece (no fin-to-base joint resistance). A section of the fin array middle is removed to create the Split-Flow inlet slot.
- Published performance: RX3 CPU coldplate (Ice Lake era) **<= 0.03 C/W** thermal resistance; low-profile for 1U. Fin pitch, thickness, height: **not disclosed** anywhere indexed.
- Generic skived-fin bounds (not CoolIT): GB200-class skived copper plates are typically <= 0.5 mm fin thickness/pitch and >= 3 mm fin height, targeting < 0.03 C/W and <= 20 kPa (Fibermall vendor blog, https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm); finest commercial skived example 0.06 mm fins at 0.10 mm pitch (USUSTK, https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink). CoolIT's "industry-leading internal geometries" is presumably in the 0.1 to 0.3 mm fin / 0.1 to 0.3 mm gap range, but this is an inference.
- Third-party literature on CoolIT plates: Ramakrishnan et al., ASME J. Electronic Packaging 141(4), 2019 (https://asmedigitalcollection.asme.org/electronicpackaging/article-abstract/141/4/041005/955785) modelled "a commercially available cold plate by CoolIT" on a 6.45 cm2 mock processor, 31 W/cm2 at 13 cm3/s; literature values quoted there: CoolIT cold plate 0.031 K/W (lowest in their survey) and a second CoolIT study 0.051 K/W - older CPU-class products, not AI plates.

---

## 4. OMNI all-metal unibody coldplates (May 2024)

Sources: product page https://coolitsystems.com/?p=4082 and https://www.coolitsystems.com/coldplates/; press release 9 May 2024 https://coolitsystems.com/?p=4558; StorageReview https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled; DCF tour (above); OCP cold-plate white paper listing (https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/).

| Claim | Value | Baseline / caveat |
|---|---|---|
| TDP | > 1,500 W | vendor |
| Heat flux | > 300 W/cm2 | vendor; conditions undisclosed |
| Thermal resistance | "up to 60 % lower" | press release says "vs standard coldplates"; product page says "vs standard microchannel coldplates"; no flow, coolant, inlet T or test method given |
| Construction | single-metal unibody, "aerospace-grade metallic sealing requiring no brazing material", eliminates CTE mismatch of multi-material stacks | DCF 2026 tour: CoolIT has moved designs from brazing to **friction stir welding** to make a "unibody" copper structure - this is almost certainly the OMNI joining process (inference) |
| Shipping | at scale from June 2024 | optimised for GB200 Grace Blackwell; launch imagery showed GB200, H100, GH200, Intel Data Center GPU Max, 4th-gen Xeon plates; current page lists AMD Instinct MI355 |
| Used in | the second 4 kW prototype ("OMNI All-Metal Coldplate joining technology, which forms a coldplate's top and bottom into a single piece without brazing") | |

Note: the "60%" and the Split-Flow "30%" are separate marketing numbers with no common baseline; neither should be used as an engineering datum.

---

## 5. The 4 kW coldplate (March 2025) - the best-documented CoolIT data point

Sources: tech brief R2, 14 March 2025 https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf; press release https://www.coolitsystems.com/resources/news/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership/; HPCwire https://www.hpcwire.com/2025/03/31/coolit-systems-4000w-breakthroughredefining-single-phase-dlc-for-ultra-high-wattage-ai-processors/; STH https://www.servethehome.com/coolit-shows-off-a-4kw-coldplate-for-liquid-cooling/; Tom's Hardware https://www.tomshardware.com/pc-components/liquid-cooling/coolit-unleashes-4kw-single-phase-dlc-cold-plate-seemingly-timed-for-nvidia-blackwell-ultra-chips.

| Item | Value |
|---|---|
| Footprint | 50 x 50 mm (25 cm2) "slightly smaller than a Blackwell GPU" -> **160 W/cm2** (derived) |
| Thermal resistance | **Tr < 0.009 C/W**, measured from *maximum* case temperature to fluid inlet, **including TIM** -> dT_max <= 36 C at 4 kW |
| Unit-area resistance | ~0.225 cm2-K/W (derived) |
| Flow | 6.06 LPM (1.5 LPM/kW, "semiconductor industry's recommended flow rate") |
| Heat capture | 97.3 % at 6.06 LPM; 93.4 % at 4.28 LPM (brief table) |
| Pressure drop | **8 psi (55 kPa) full loop including fittings and QDs** at 6 LPM; plate-only not split out |
| Coolant dT | ~10 K (derived) ; caloric resistance ~0.0025 K/W = ~28 % of 0.009 |
| Manufacturing | in-house at Liquid Lab with "standard CNC machining and skiving equipment"; second unit with OMNI joining |
| Split-Flow claim | 30 % better thermal and flow performance vs standard coldplates |
| Industry context claimed | prior assumed single-phase ceiling 1,500 to 2,000 W (IDTechEx: ~1,500 W struggle, 2,000 W limit - https://www.scientific-computing.com/article/coldplate-innovation-raising-bar-thermal-ceiling) |

---

## 6. CDUs, manifolds, QDs, Liquid Lab

Sources: CoolIT CDU page https://coolitsystems.com/products/cdu; CHx2000 page https://www.coolitsystems.com/cdu-product/chx2000/ and blog https://www.coolitsystems.com/resources/news/chx2000-the-ai-cdu/; StorageReview CHx1500 https://www.storagereview.com/news/coolit-chx1500-delivers-1500kw-of-precision-liquid-cooling, CHx2000 https://www.storagereview.com/news/coolit-unveils-chx2000-cdu-with-2mw-liquid-cooling-capacity-in-standard-rack-footprint, CHx1000 https://www.storagereview.com/news/coolit-systems-chx1000-high-density-liquid-cooling-unit-for-ai-and-hpc, AHx/CHx500 https://www.storagereview.com/news/coolit-systems-launches-new-cdus-for-ai-and-hpc-cooling-solutions; Climate Control News table https://www.climatecontrolnews.com.au/cooling/cdu-performance-record; rack manifolds https://www.coolitsystems.com/products-services/server-products/rack-manifolds/; Liquid Lab https://www.hpcwire.com/off-the-wire/coolit-systems-opens-liquid-lab-innovation-center/.

| CDU | Capacity | Flow / head | Footprint | Notes |
|---|---|---|---|---|
| CHx2000 (Apr 2025) | 2,000 kW at 5 C approach, 1.2 LPM/kW; 2,269 kW at 4 C approach (PG25) | **53 psi** secondary head; ~2,400 LPM secondary (derived) | 750 x 1200 mm | "up to 12 GB200/GB300 NVL72 racks (120 kW)"; in production since Oct 2024 |
| CHx1500 (Mar 2025) | 1,500 kW at 5 C; 1,364 kW at 4 C | 2,100 LPM primary / 1,800 LPM secondary; N+N pumps 1,500 LPM at 34 psi; 44 psi secondary head | 750 x 1200 mm | row-based |
| CHx1000 (late 2024) | 1,000 kW at 3 C approach | up to 1.5 LPM/kW; N+N pumps 1,500 LPM at 35 psi | single rack 750 x 1200 mm | 10 in touchscreen, front/back service |
| CHx500 | stackable; 4 units = 2 MW in one rack | - | - | |
| AHx240 / AHx180 | > 240 kW (2-rack) / 180 kW | liquid-to-air, no facility water | | |
| Legacy | CHx650, CHx80 (80 kW in 4U), AHx20 | | | Dell-era |

- Manifolds: stainless steel; EIA, ORV3 and MGX rack series; Staubli dry-break QDs with "Rack DLC" passive coldplate loops. CoolIT is credited as a collaborator (not author) on the OCP UQD spec v2.0.0 (https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf). CoolIT's Ben Sutton is primary author of the OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf) - i.e. CoolIT is shaping how cold plates will be benchmarked.
- Liquid Lab (opened Feb 2022): 13,000 sq ft, >10 test areas, system-level rack chamber, environmental chambers, HALT chamber; Starfield labs add 18 thermal chambers, a 1 MW data-centre simulator and a **6 MW thermal load test rig** (DCF 2026).
- Flow standard: the "1.2 LPM/kW industry standard for AI" is consistent with ~85 % heat-to-liquid and ~10 K rise on a 120 kW NVL72 (~146 LPM) and with Nvidia's stated 45 C in / 65 C out (DCD GTC coverage https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus); no primary Nvidia document stating "1.2 LPM/kW" was found.

---

## 7. Roadmap statements

From the 15 kW brief: further coldplate optimisation (lower Tr and dP); **direct-to-die and micro-channel lids**; peripheral-component cooling for 100 % heat capture; server architecture for ultra-high density; system designs for > 1 MW racks. No product, date or data for direct-to-die or lids was found. Industry context: Nvidia is rumoured to be seeking microchannel-lid / direct-to-chip partners for Rubin Ultra (Wccftech https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/; Digitimes Sept 2025 https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html); Frore LiquidJet Nexus claims a 10 C reduction / 10 % token boost on delidded Rubin (vendor, https://www.tomshardware.com/pc-components/liquid-cooling/frore-shows-off-liquidjet-nexus-coldplate-for-nvidia-vera-rubin-other-ai-accelerators-offers-up-claimed-10-percent-token-generation-boost-over-rival-liquid-cooling-solutions).

---

## 8. Company, ownership, manufacturing footprint, partners

Sources: Ecolab announcement 19 Mar 2026 (https://www.businesswire.com/news/home/20260319353197/en/ ; deck https://s204.q4cdn.com/218790897/files/doc_downloads/2026/03/Ecolab-to-Acquire-CoolIT-Systems.pdf; 8-K https://www.sec.gov/Archives/edgar/data/31462/000110465926032446/tm269446d1_ex99-1.htm); close reports (https://itbrief.co.uk/story/ecolab-completes-usd-4-75-billion-coolit-takeover); Mubadala (https://www.mubadala.com/en/what-we-do/coolit; https://www.agbi.com/finance/2026/03/mubadala-offloads-minority-stake-in-nearly-5bn-coolit-deal/); 25-year release (https://www.coolitsystems.com/resources/news/coolit-25-years-liquid-cooling/); manufacturing (https://www.hpcwire.com/2025/06/25/coolit-systems-scales-north-american-manufacturing-to-cool-ais-next-wave/; https://manufacturing-today.com/news/marking-25-years-of-unparalleled-performance-and-technical-excellence-coolit-systems-continues-to-drive-global-ai-infrastructure/); Nvidia (https://www.coolitsystems.com/capabilities/co-innovation/nvidia/; https://www.coolitsystems.com/resources/news/coolit-systems-growing-liquid-cooling-product-line-manufacturing-capacity-to-support-nvidia-blackwell-platform-ramp/); Dell (https://www.datacenterdynamics.com/en/news/dell-emc-to-equip-poweredge-servers-with-coolit-liquid-cooled-systems/).

- Founded 2001, Calgary. Leadership: CEO Jason Waxman, CTO Kamal Mostafavi, COO Patrick McGinn. Previously consumer AIO maker (Corsair OEM), now 100 % data-centre.
- Ownership timeline: 2023 KKR Global Impact Fund II + Mubadala Investment Company (not "Mubadala Capital", not 2024); 19/20 Mar 2026 Ecolab definitive agreement, **US$4.75 bn cash** = 29x NTM and 24x 2027E adj. EBITDA; NTM revenue ~**US$550 M**, ~30 % adj. EBITDA margin (-> ~US$165 M EBITDA, ~8.6x sales, derived), organic growth > 30 %/yr, YTD sales +100 %; close reported 3 July 2026; CoolIT keeps its name and management. Mubadala's exit note: footprint > 300,000 sq ft, CDU capacity +25x, > 300 jobs added since 2023.
- Manufacturing: Calgary Starfield 1 (112,000 to 113,000 sq ft) + Starfield 3 (~200,000 sq ft combined per DCF 2026), 37,000 sq ft Innovation Center, +90,000 sq ft planned; production also in **China and Vietnam** (expanding in 2026); Liquid Lab centres in Calgary and **Taipei** (Taiwan = R&D/prototyping, no Taiwan factory found). Output: "hundreds of CDUs a month"; 100 % leak and functional test; AI optical screening and robotic automation; production scaled "25x in 18 months" (vendor).
- Partners/customers: Nvidia Partner Network; NA2 loop "custom designed for GB200"; OMNI for GB200; CHx2000 sized for GB200/GB300 NVL72. Dell factory-installed DLC since 2017 (PowerEdge); HPE Apollo 2000 option; Lenovo NeXtScale loop (2016); claims "4 of top 5 server OEMs and 4 of 5 hyperscalers" and "gigawatt-level capacity" (unnamed, self-reported). Enables Frontier (HPE/Cray, 100 % fanless) per CoolIT.
- Patents: "over 120 liquid-cooling patents" (company page); 50th patent in 2015 (US 9,057,567 Microchannel Coldplate, 9,052,252 leak detection, 9,055,697); US 12,188,733 (Jan 2025, modular fluid heat exchange with compliant member, continuation of US 11,725,886); US 12,101,906 fluid heat exchanger. Note: US 11,421,662 "Integrally supported cooling device" is **Nissens**, not CoolIT.
- Litigation: Asetek v. CoolIT - 2015 ~US$1.9 M damages; 2019 suit; Sept 2022 summary judgement of non-infringement on the '362 patent; Oct 2022 confidential global settlement; 2024 Fed. Cir. affirmed unpatentability of Asetek's US 10,078,354 (DCD https://www.datacenterdynamics.com/en/news/coolit-wins-patent-suit-brought-by-danish-cooling-firm-asetek/; insideHPC https://insidehpc.com/2022/10/coolit-system-district-court-rejects-asetek-patent-claims/).
- Recalls/failures: none found for CoolIT products. Ecolab's Bob Walicki (Electronics360 Q&A, 7 Oct 2026, https://electronics360.globalspec.com/article/24164/q-a-ecolab-bets-on-liquid-cooling-for-ai-data-center-growth) attributes recent field cold-plate performance issues to incomplete flushing/fill (particulates migrating into cold plates) - a systemic microchannel vulnerability, not a CoolIT-specific defect.

---

## 9. Pricing hints

No CoolIT list prices exist publicly. Reference points: Morgan Stanley (via TechRadar https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks; igor'sLAB https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/): GB300 NVL72 liquid-cooling BOM ~**US$49,860/rack**; ~US$2,260 per compute tray; **~US$300 per CPU/GPU cold plate**, ~US$200 per NVSwitch plate; Vera Rubin NVL144 ~US$55,710/rack with cold plates "up to US$400 per unit". CoolIT's CHx2000 (2 MW) pricing not public. At ~US$550 M revenue, CoolIT is a CDU/manifold/loop system vendor more than a commodity plate vendor.

---

## 10. Known weaknesses and attack surfaces (for our design)

1. **Pressure drop and pumping power undisclosed at 15 kW.** 18 LPM through one plate at microchannel gaps implies high dP; CHx2000's 53 psi secondary head hints at the loop budgets CoolIT designs to. Any competitor that publishes dP-vs-flow and W of pumping per kW at equal Tcase wins the transparency argument.
2. **Hot-spot non-uniformity**: 17 C spread between coolest and hottest thermocouple across the device; TC5 is the limiting zone on all three plates; hottest case 89 C at 45 C inlet. Uniform split-flow microchannels cannot locally tailor h; heat-map-matched channels (Corintis-style), zoned flow or local jet features attack this directly.
3. **Caloric penalty**: at 1.2 LPM/kW the coolant rise (~12.5 K) is ~37 % of the total case-to-inlet dT. Counter-flow / multi-pass layouts or higher-cp fluids cannot change physics, but splitting GPU and HBM zones into separate parallel branches fed with fresh inlet fluid does.
4. **Standard thermal paste TIM**: at 150 to 160 W/cm2 a 0.05 to 0.1 cm2-K/W paste costs 8 to 16 C. Liquid-metal, sintered or indium TIM, or direct-to-die, would remove a large share of CoolIT's 34 C. CoolIT lists direct-to-die/lids as future work only.
5. **Vendor-only validation**: all numbers come from CoolIT's TTVs; no independent lab data, no real-GPU data, no long-term fouling data for the 15 kW plate; it is a "design", not a shipping product.
6. **Particulate/fouling sensitivity** of sub-0.3 mm skived channels (acknowledged by Ecolab's own commissioning messaging); corrosion/erosion of copper in PG25 loops (UTA accelerated-degradation thesis https://uta-ir.tdl.org/uta-ir/handle/10106/31381).
7. **Nvidia procurement shift**: for Vera Rubin, Nvidia centralised cold-plate purchasing and named Jentech, AVC, Cooler Master and Delta as Group-A suppliers (TVBS https://news.tvbs.com.tw/english/3188903; Digitimes https://www.digitimes.com/news/a20260318PD231.html). CoolIT is not on that list; its GPU-plate volume increasingly depends on OEM/hyperscaler custom programmes and on CDUs/manifolds.
8. **Core Split-Flow patent (2008 filing) approaches expiry (~2028)**; continuations may extend some claims, but the central-inlet concept will be free to use.
9. **Scalability at > 20 to 30 kW**: single central slot means per-channel flow length still scales with die size; at Rubin-Ultra/Kyber package sizes a single split is no longer "short". Multi-slot manifold-microchannel layouts scale better.
10. **Integration risk**: Ecolab (water chemistry) acquisition at 29x EBITDA; management retention and roadmap continuity are unproven; litigation history with Asetek (settled).

---

## 11. Numbers to beat (summary table)

| Metric | CoolIT 15 kW (June 2026) | CoolIT 4 kW (Mar 2025) | OMNI (2024) |
|---|---|---|---|
| TDP demonstrated | 15 kW (TTV, 4 heaters) | 4 kW (TTV, 50 x 50 mm) | > 1.5 kW (rating) |
| Flow | 18 LPM (1.2 LPM/kW) | 6.06 LPM (1.5 LPM/kW) | n/a |
| Inlet | 45 C water-glycol | not stated (likely 45 C) | n/a |
| Avg case-to-inlet dT | 34.4 C (26.8 to 44.2) | <= 36 C (max-case basis) | n/a |
| R case-to-inlet incl. TIM | 0.00229 C/W avg; 0.00295 C/W max (derived) | < 0.009 C/W (max-case) | "60 % lower than standard microchannel" |
| Unit-area R | ~0.23 cm2-K/W (if ~100 cm2, inferred) | ~0.225 cm2-K/W (derived) | n/a |
| Heat flux | not disclosed (~150 W/cm2 inferred) | 160 W/cm2 (derived) | > 300 W/cm2 (claim) |
| Pressure drop | **not disclosed** | 8 psi / 55 kPa full loop at 6 LPM | not disclosed |
| Heat capture | not stated | 97.3 % at 6.06 LPM; 93.4 % at 4.28 LPM | n/a |
| TIM | standard paste | included in Tr | n/a |
| Construction | Split-Flow skived Cu, "proven mass manufacturing" | CNC + skiving; OMNI FSW-type unibody on 2nd unit | all-metal unibody, no braze |

---

## 12. Gaps / unknowns

- 15 kW plate: footprint, heat flux, fin geometry, plate dP, pumping power, coolant outlet T, heater layout (which TC is HBM vs GPU), TIM thickness/type, whether OMNI joining was used.
- Split-Flow and skived tech briefs: no indexed copy of their charts (Tr vs flow, dP vs flow) or of the baseline for the "30 %" claim.
- OMNI: exact joining process (friction stir welding is inferred from the DCF tour), the baseline for "60 % lower thermal resistance", and the conditions for "> 300 W/cm2".
- Rack DLC CPU/GPU coldplate datasheets (Tr, dP, flow per plate) - not public.
- Taiwan manufacturing: only R&D (Liquid Lab Taipei) found; no Taoyuan plant evidence. China/Vietnam plant sizes unknown.
- Customer names (hyperscalers) and unit volumes; CoolIT share of GB200/GB300 cold plates (SemiAnalysis paid report has it).
- CoolIT Computex 2026 booth product list; any GB300/Rubin loop SKUs; any CHx > 2 MW product.
- Exact Split-Flow patent expiry and the claim scope of continuations (US 12,188,733 family, US 12,101,906).
- Reliability statistics (MTBF, leak rates) - none public; only Ecolab's qualitative commissioning comments.

---

## Sources

- CoolIT 15 kW tech brief (local extract) and press release: https://www.coolitsystems.com/resources/news/15kw_press_release/ ; https://www.coolitsystems.com/resources/news/15kw-coldplate/ ; https://www.prnewswire.com/news-releases/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-roadmap-far-beyond-2030-302787344.html
- DCD 15 kW: https://www.datacenterdynamics.com/en/news/coolit-designs-15kw-coldplate-to-future-proof-liquid-cooling-for-gpus/
- Electronics360 Computex 2026: https://electronics360.globalspec.com/article/23837/computex-2026-coolit-pushes-single-phase-dlc-to-15-kw
- HPCwire 15 kW: https://www.hpcwire.com/off-the-wire/coolit-systems-demonstrates-15kw-coldplate-extending-single-phase-dlc-roadmap-far-beyond-2030/
- Scientific Computing, coldplate thermal ceiling: https://www.scientific-computing.com/article/coldplate-innovation-raising-bar-thermal-ceiling
- Split-Flow tech brief: https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf ; Scribd mirror https://www.scribd.com/document/1025620831/Split-Flow-Technology-CoolIT-Tech-Brief
- Coldplate technology page: https://www.coolitsystems.com/coldplate-technology/ ; coldplates page https://www.coolitsystems.com/coldplates/
- Split-Flow patents: https://patents.google.com/patent/US8746330B2/en ; https://patents.google.com/patent/US9603284B2/en ; https://patents.justia.com/patent/8746330 ; https://insidehpc.com/2014/06/coolit-systems-patents-split-flow-heat-exchanger/
- CoolIT patent marking page: https://www.coolitsystems.com/patents/ ; design engineering (>120 patents): https://www.coolitsystems.com/capabilities/design-engineering/ ; 2015 50th patent: https://insidehpc.com/2015/07/coolit-systems-lands-new-patents-for-liquid-cooling/ ; US 12,188,733: https://patentsgazette.uspto.gov/week01/OG/html/1530-1/US12188733-20250107.html
- Villanova split-flow model: https://par.nsf.gov/biblio/10341820 ; https://www.researchgate.net/publication/356363419_Thermal-Hydraulic_Analytical_Models_of_Split-Flow_Microchannel_Liquid-Cooled_Cold_Plates_With_Flow_Impingement
- Skived brief: https://coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf ; https://datacenterknowledge.com/cooling/skived-coldplates-technical-brief
- Ramakrishnan et al. 2019 (CoolIT plate modelled): https://asmedigitalcollection.asme.org/electronicpackaging/article-abstract/141/4/041005/955785 ; https://www.researchgate.net/publication/334079188_Thermal_Analysis_of_Cold_Plate_for_Direct_Liquid_Cooling_of_High_Performance_Servers
- OMNI: https://coolitsystems.com/?p=4082 ; https://coolitsystems.com/?p=4558 ; https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled
- 4 kW: https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf ; https://www.coolitsystems.com/resources/news/coolits-4000w-coldplate-establishes-single-phase-direct-liquid-cooling-technology-leadership/ ; https://www.hpcwire.com/2025/03/31/coolit-systems-4000w-breakthroughredefining-single-phase-dlc-for-ultra-high-wattage-ai-processors/ ; https://www.storagereview.com/news/coolit-unveils-4000w-cold-plate-setting-new-standard-for-single-phase-direct-liquid-cooling ; https://www.servethehome.com/coolit-shows-off-a-4kw-coldplate-for-liquid-cooling/
- CDUs: https://coolitsystems.com/products/cdu ; https://www.coolitsystems.com/cdu-product/chx2000/ ; https://www.coolitsystems.com/resources/news/chx2000-the-ai-cdu/ ; https://www.storagereview.com/news/coolit-unveils-chx2000-cdu-with-2mw-liquid-cooling-capacity-in-standard-rack-footprint ; https://www.storagereview.com/news/coolit-chx1500-delivers-1500kw-of-precision-liquid-cooling ; https://www.storagereview.com/news/coolit-systems-chx1000-high-density-liquid-cooling-unit-for-ai-and-hpc ; https://www.storagereview.com/news/coolit-systems-launches-new-cdus-for-ai-and-hpc-cooling-solutions ; https://www.climatecontrolnews.com.au/cooling/cdu-performance-record ; https://www.hpcwire.com/2024/12/10/ai-performance-reliability-serviceability-with-coolits-chx1000-cdu/
- Manifolds/QDs/OCP: https://www.coolitsystems.com/products-services/server-products/rack-manifolds/ ; https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf ; https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf ; https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/ ; https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
- Liquid Lab / manufacturing: https://www.hpcwire.com/off-the-wire/coolit-systems-opens-liquid-lab-innovation-center/ ; https://www.hpcwire.com/2025/06/25/coolit-systems-scales-north-american-manufacturing-to-cool-ais-next-wave/ ; https://www.datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale ; https://manufacturing-today.com/news/marking-25-years-of-unparalleled-performance-and-technical-excellence-coolit-systems-continues-to-drive-global-ai-infrastructure/ ; https://www.coolitsystems.com/resources/news/coolit-25-years-liquid-cooling/ ; https://www.coolitsystems.com/about/coolit-overview/ ; https://www.servethehome.com/how-liquid-cooling-is-prototyped-and-tested-in-the-coolit-liquid-lab-tour/coolit-systems-megawatt-scale-cdu-rear/
- Ownership: https://www.businesswire.com/news/home/20260319353197/en/Ecolab-to-Acquire-CoolIT-Systems,-a-Global-Leader-in-Advanced-Liquid-Cooling-for-Next-Gen-AI-Data-Centers ; https://s204.q4cdn.com/218790897/files/doc_downloads/2026/03/Ecolab-to-Acquire-CoolIT-Systems.pdf ; https://www.sec.gov/Archives/edgar/data/31462/000110465926032446/tm269446d1_ex99-1.htm ; https://itbrief.co.uk/story/ecolab-completes-usd-4-75-billion-coolit-takeover ; https://www.agbi.com/finance/2026/03/mubadala-offloads-minority-stake-in-nearly-5bn-coolit-deal/ ; https://www.mubadala.com/en/what-we-do/coolit ; https://gulfnews.com/business/markets/abu-dhabis-mubadala-kkr-acquire-canada-based-liquid-cooling-solutions-firm-1.96784139
- Nvidia/OEM partners: https://www.coolitsystems.com/capabilities/co-innovation/nvidia/ ; https://www.coolitsystems.com/resources/news/coolit-systems-growing-liquid-cooling-product-line-manufacturing-capacity-to-support-nvidia-blackwell-platform-ramp/ ; https://insidehpc.com/2024/10/coolit-systems-liquid-cooling-to-support-nvidia-blackwell ; https://www.datacenterdynamics.com/en/news/dell-emc-to-equip-poweredge-servers-with-coolit-liquid-cooled-systems/ ; https://www.storagereview.com/review/coolit ; https://www.hpcwire.com/off-the-wire/coolit-systems-supply-liquid-cooling-architecture-lenovos-nextscale-m5-system/
- Nvidia Rubin cold-plate suppliers: https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html ; https://global.iteschina.com/en/news/details/2995
- Rubin/Kyber/lids: https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027 ; https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/ ; https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html ; https://www.tomshardware.com/pc-components/liquid-cooling/frore-shows-off-liquidjet-nexus-coldplate-for-nvidia-vera-rubin-other-ai-accelerators-offers-up-claimed-10-percent-token-generation-boost-over-rival-liquid-cooling-solutions
- Pricing: https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks ; https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
- Litigation: https://www.datacenterdynamics.com/en/news/coolit-wins-patent-suit-brought-by-danish-cooling-firm-asetek/ ; https://insidehpc.com/2022/10/coolit-system-district-court-rejects-asetek-patent-claims/ ; https://www.inderes.fi/releases/asetek-litigation-update
- Reliability/fouling: https://electronics360.globalspec.com/article/24164/q-a-ecolab-bets-on-liquid-cooling-for-ai-data-center-growth ; https://datacentrereview.com/2026/08/how-to-build-reliable-liquid-cooling-systems/ ; https://uta-ir.tdl.org/uta-ir/handle/10106/31381 ; https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1
- Competitor framing: https://jetcool.com/post/understanding-direct-to-chip-liquid-cooling-approaches-and-performance-tradeoffs/ ; https://sacra.com/research/corintis
- Generic skived geometry: https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink
- GB200 coolant temperatures: https://datacenterdynamics.com/en/news/nvidia-announces-liquid-cooled-gb200-nvl72-system-with-72-blackwell-gpus
