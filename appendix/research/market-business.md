# Market and business context for a new cold-plate entrant (vs. the CoolIT 15 kW benchmark)

Prepared 2026-10-13 for the cooling-architecture programme. Angle: market size, unit volumes, price points, shares, buyers, design-in dynamics, M&A, margins, and the routes by which a new entrant can realistically win against CoolIT and the Taiwanese volume incumbents.

## 0. Method and provenance (read first)

- **No live web searches could be run by this agent**: the per-turn WebSearch budget (200 calls, shared across all agents in this workflow) was already exhausted by the sibling research agents, and WebFetch/curl are DNS-blocked in this container (one attempt made, `ENOTFOUND`). Searches run: 0 by this agent.
- Every number below is therefore tagged by provenance:
  - **[Brief]** - the CoolIT 15 kW tech brief (June 2026), read in full.
  - **[Sib: URL]** - a search-result extract recorded by a sibling agent earlier in this workflow (files `coolit-products.md`, `coolit-briefs-numbers.md`, `competitors-singlephase.md`, `competitors-advanced.md`, `manufacturing-cost.md`, `chip-roadmap-requirements.md`, `standards-reliability.md` in the same research folder). These carry URLs but were read as search snippets, not full pages.
  - **[D]** - arithmetic derived here from tagged inputs.
  - **[KB-H / KB-M / KB-L]** - the author's background knowledge (high / medium / low confidence), **not verified this session**. Treat as leads to confirm, not facts. Analyst market-size figures (Dell'Oro, Omdia, IDTechEx, Uptime) fall in this class and are given as ranges.
- Vendor claims are marked (V); analyst/press estimates (A); independent/standards (I).

## 1. Executive summary

1. **Market size.** CoolIT's own sizing puts hyperscaler/CSP spend on DLC *technology cooling systems* (cold plates + CDUs + manifolds/piping) at **> US$5 B in 2025 and > US$11 B in 2026** [Brief]. A bottom-up cross-check (racks x cooling BOM, Section 2.2) lands in the same range, so the figure is credible even though it is a vendor number. Analyst houses (Dell'Oro, Omdia, IDTechEx) publish lower "liquid cooling equipment" numbers because they count narrower scopes [KB-M]; none could be fetched this session.
2. **Volumes.** An NVL72-class rack carries ~108 CPU/GPU plates + ~18 NVSwitch plates = **~126 plates** [D from Sib: Morgan Stanley BOM]. At 30-50 k GB-class racks/yr (2026) that is **4-7 M Nvidia-rack plates/yr** [Sib: manufacturing-cost.md, D]; adding hyperscaler ASICs and AMD Helios gives an order-of-magnitude **8-15 M DLC cold plates in 2026** [D, KB-L].
3. **Price.** GPU/CPU plate ASP **~US$300 (GB300)**, **up to ~US$400 (Vera Rubin)**, NVSwitch plate ~US$200; rack-level liquid-cooling BOM **~US$49.9 k (GB300 NVL72)** and **~US$55.7 k (VR NVL144)** (Morgan Stanley via TechRadar / igor'sLAB, A) [Sib]. IDTechEx: US$300-500 per GPU plate, ~US$2.3 k per 8-GPU server, ~US$55 k per rack (A) [Sib].
4. **Shares.** AVC holds an estimated **40-50 % of GB200/GB300 cold plates** (press, A) [Sib]. For Rubin, **Nvidia centralised plate purchasing and named Jentech, AVC, Cooler Master and Delta as "Group-A" suppliers** (TVBS/Digitimes, A) [Sib]. CoolIT (~US$550 M NTM revenue, ~30 % adj. EBITDA margin, acquired by Ecolab for US$4.75 B in 2026) is a CDU/loop/system vendor more than a commodity plate vendor [Sib].
5. **Who buys and what wins.** Nvidia defines the plate envelope (mounting, TIM, inlet 45 C, flow, dP budget) and keeps a Recommended Vendor List; ODMs (Foxconn/Ingrasys, Quanta, Wiwynn, Supermicro) and OEMs (Dell, HPE, Lenovo) integrate; hyperscalers run their own plate programmes for their own ASICs (Google bare-die TPU plates since TPUv4; Google Deschutes CDU built by Boyd) [Sib]. Design-ins are won on **qualification status + capacity + price + leak record**, with thermal margin as the tie-breaker [KB-M].
6. **M&A.** The sector has consolidated into industrial/infra majors: Ecolab-CoolIT (US$4.75 B, 2026) [Sib]; Flex-JetCool (Nov 2024) [Sib]; Jabil-Mikros (Oct 2024) [Sib]; Daikin-Chilldyne (Nov 2025) [Sib]; Vertiv-CoolTera (Dec 2023) [KB-H]; Schneider-Motivair (2024-25) [KB-H]; Eaton-Boyd Thermal (announced Oct 2025, ~US$9.5 B) [KB-M]; Corintis US$24 M (Sep 2025) [Sib]; Asetek's data-centre business is dormant [Sib].
7. **Margins.** CoolIT ~30 % adj. EBITDA at the system level [Sib]; our teardown implies **45-70 % gross margin on a Rubin-class plate at the Tier-1 ASP** (factory cost US$70-170 vs ASP US$300-400) [Sib: manufacturing-cost.md, KB-M], but the Taiwanese component houses report **company-level gross margins of only ~15-25 %** once ODM price pressure, plating, test and logistics are included [KB-L].
8. **Value of performance to an operator.** 10 kPa lower plate dP is worth only ~3 W hydraulic per 15 kW plate (~0.04 % of rack power) [D]; its real value is CDU head, series plumbing, filter margin and negative-pressure compatibility. 1 K lower case-to-inlet dT, converted into +1 K facility supply, is worth roughly **+10 % dry-cooler capacity (or ~10 % less dry-cooler capex) at a 10 K design approach** and ~2-3 % of trim-chiller energy [D, KB-M]; converted into lower Tj it buys ~0.1-0.3 % GPU power (leakage) and reliability margin [KB-L].
9. **How a new entrant wins.** Not by shipping a better plate into Nvidia's Group-A channel alone (gatekept, price-capped at ~US$400, capacity-gated at >100 k plates/month). The realistic sequence is: (a) hyperscaler custom-ASIC programmes (Google/AWS/Meta/Microsoft/OpenAI-Broadcom), which tolerate novel plates and higher dP (Google: 80 psi available "to enable advanced cold plate designs") [Sib]; (b) a manufacturing/licensing partnership with a Group-A house or a Western CM (Jabil, Flex, Boyd/Eaton) for Nvidia volume; (c) a micro-channel-lid / direct-to-die co-design bid for Rubin Ultra (2H 2027), where Nvidia is reported to be seeking partners [Sib]; (d) the 800 VDC power-electronics adjacency (SiC/GaN power shelves) as a second, less gatekept SKU.
10. **The benchmark's commercial soft spots**: no dP, no footprint, no independent data, paste TIM, 12-17 K hot-spot spread, and CoolIT is not on Nvidia's Rubin Group-A list [Brief, Sib]. A plate reported in full OCP Cold Plate Test Spec v1.0.0 format (dP at six flow points, burst, leak, cycling) with independent-lab data beats CoolIT on transparency before any thermal comparison [Sib].

## 2. Market size 2025-2030

### 2.1 Published figures

| Source | Scope | 2024 | 2025 | 2026 | 2028-2030 | Provenance |
|---|---|---|---|---|---|---|
| CoolIT (tech brief, Jun 2026) | Hyperscaler/CSP spend on DLC TCS (cold plates, CDUs, piping/manifolds) | - | **> US$5 B** | **> US$11 B** | - | [Brief] (V) |
| Ecolab deal metrics for CoolIT | CoolIT NTM revenue ~US$550 M; organic growth > 30 %/yr; YTD sales +100 % | - | ~US$550 M (NTM) | - | - | [Sib: businesswire.com/news/home/20260319353197/en/ ; s204.q4cdn.com Ecolab deck] (I, SEC 8-K) |
| Dell'Oro (DCPI / liquid cooling) | "Liquid cooling" equipment revenue (DLC + immersion, CDUs, RDHx) | ~US$1-2 B | ~US$2.5-4 B | ~US$4-6 B | ~US$8-12 B by 2029-30 | [KB-L] - could not be fetched; Dell'Oro has repeatedly raised its forecast and called liquid cooling the fastest-growing DCPI segment (> 40 % CAGR) [KB-M] |
| Omdia (data-centre thermal management) | Liquid cooling share of thermal-management revenue | ~US$2-3 B | ~US$3.5-5 B | ~US$5-7 B | >US$10 B by 2029 | [KB-L] |
| IDTechEx (Thermal Management for Data Centers 2025-2035) | Liquid cooling incl. D2C and immersion | - | - | - | > US$10 B by 2035 (older edition said ~US$5 B) | [KB-L]; IDTechEx ASP data: US$300-500 per GPU plate [Sib: onartificialintelligence.com/articles/34213/...] (A) |
| Uptime Institute (Cooling Systems Survey 2024/2025) | Adoption, not revenue: ~20-25 % of operators run some DLC; leaks are the top-ranked DLC concern; typical GPU coolant supply limit ~40 C | - | - | - | - | [KB-M]; 40 C note [Sib: intelligence.uptimeinstitute.com/entity_pdf/node/153594/pdf] |

Reconciliation: the analyst numbers are lower than CoolIT's because they (i) count vendor revenue of liquid-cooling *equipment* rather than CSP *spend* including installation/piping, (ii) often exclude in-server cold plates that ship inside the ODM's rack BOM, and (iii) were set before the 2025-26 Blackwell/Rubin ramp. The bottom-up check below suggests CoolIT's US$5 B / US$11 B is the right order of magnitude for total TCS spend.

### 2.2 Bottom-up cross-check [D]

| Input | 2025 | 2026 | 2027 | Provenance |
|---|---|---|---|---|
| NVL72-class racks shipped (GB200 + GB300 + VR200) | 25-35 k | 50-80 k | 80-120 k (incl. Kyber/NVL576 equivalents) | [KB-L]; sibling assumption 30-50 k in 2026 [Sib: manufacturing-cost.md] |
| Rack-level liquid-cooling BOM (plates, manifolds, QDs, hoses) | ~US$50 k | US$50-56 k | ~US$56 k+ | [Sib: TechRadar / igor'sLAB Morgan Stanley] (A) |
| In-rack TCS spend | US$1.3-1.8 B | US$2.5-4.5 B | US$4.5-6.7 B | [D] |
| CDUs, row manifolds, TCS piping, commissioning (x1.0-1.5 of rack BOM) | US$1.3-2.7 B | US$2.5-6.7 B | US$4.5-10 B | [KB-M] multiplier; CDU ASP ~US$200-400 per kW [KB-L] |
| Non-Nvidia DLC (Google TPU, AWS Trainium, AMD Helios, Microsoft Maia, Cerebras, HPC) | +30-60 % | +30-50 % | +30-50 % | [KB-L]; Google alone runs ~1 GW of DLC over ~2,000 pods [Sib: chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips] |
| **Total TCS spend** | **US$3.5-7 B** | **US$6.5-16 B** | **US$12-25 B** | [D] - brackets CoolIT's > US$5 B / > US$11 B |

Implication: the plate itself is **~25-40 % of TCS spend** (plates ~US$2-5 B in 2026 [D]); CDUs, manifolds and piping are the rest. This is why CoolIT (CHx CDUs, manifolds, loops) and Vertiv (CoolChip CDUs) make most of their money outside the plate.

## 3. Unit volumes: GPUs, plates per device, plates per year

| Item | Value | Provenance |
|---|---|---|
| Nvidia data-centre GPU shipments | ~3.8 M (2023); Huang at GTC Mar 2025: top-4 CSPs bought 1.3 M Hopper in 2024 and **3.6 M Blackwell in 2025 (orders)**; Huang Oct 2025: **~20 M Blackwell + Rubin GPUs** visible through 2026 vs ~4 M Hopper at the same point | [KB-H for the two Huang quotes; KB-M for 2023] |
| GPUs per NVL72 rack | 72 GPU packages + 36 Grace CPUs + 9 NVSwitch trays (18 switch ASICs) | [Sib: chip-roadmap-requirements.md] |
| Cold plates per rack | 18 compute trays x (4 GPU + 2 CPU plates) = 108; 9 switch trays x 2 = 18; **~126 plates** (plus VR/power-stage plates in Rubin trays) | [D from Sib: Morgan Stanley US$2,260 per compute tray, ~US$300 per CPU/GPU plate, ~US$200 per NVSwitch plate] |
| Plates per GPU / per CPU / per switch | 1 / 1 / 1 (GB300 moves GPUs to socketed "SXM puck" modules with individual plates [KB-M]); Rubin adds plates on power stages and NICs toward 100 % heat capture | [Sib]; [KB-M] |
| Nvidia-rack plates per year | 2025: 3-4.5 M; **2026: 6-10 M**; 2027: 10-15 M | [D: racks x 126] |
| Hyperscaler ASIC plates (TPU v7, Trainium 2/3, Maia 200, MTIA) | 2026: 2-4 M (TPU ~1.5-2.5 M chips/yr [KB-L]; Trainium ~1-1.5 M [KB-L]; one plate per package, double-sided in some Wiwynn/Fabric8 designs [Sib]) | [KB-L] |
| AMD Helios (MI455X, 72 GPUs/rack, 100 % DLC) | 2026-27: low-single-digit M plates | [Sib: introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026]; volume [KB-L] |
| **Total DLC cold plates, 2026** | **~8-15 M units** | [D] |
| Required supplier scale to be relevant on Nvidia programmes | >= 100 k plates/month from >= 2 sites (Taiwan / Vietnam / China / Mexico) | [Sib: manufacturing-cost.md] [KB-M] |

## 4. Price points and margins

| Item | Value | Provenance |
|---|---|---|
| GB300 NVL72 liquid-cooling BOM per rack | ~US$49,860; ~US$2,260 per compute tray | [Sib: techradar.com/pro/got-a-spare-usd50-000-... ; igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-...] (A, Morgan Stanley) |
| GB300 CPU/GPU plate ASP | ~US$300; NVSwitch plate ~US$200 | same (A) |
| Vera Rubin NVL144 cooling BOM | ~US$55,710 per rack; plates "up to US$400 per unit" | same (A) |
| Rubin plate procurement | Nvidia centralised purchasing; Group-A: Jentech, AVC, Cooler Master, Delta; plate ASP ~US$400 | [Sib: news.tvbs.com.tw/english/3188903 ; digitimes.com/news/a20260318PD231.html] (A) |
| GPU plate ASP range (industry) | US$300-500; ~US$2,300 per 8-GPU server; ~US$55 k per rack | [Sib: IDTechEx repost, onartificialintelligence.com/articles/34213] (A) |
| Per-kW TCS cost at rack level | ~US$50 k / 140 kW = **~US$360 per kW IT** | [D] |
| CDU ASP | ~US$200-400 per kW (1-2 MW class units ~US$300-700 k) | [KB-L] |
| Estimated factory cost, skived/welded GB200-class plate | ~US$170 (10 k/yr), ~US$105 (100 k/yr), ~US$70 (1 M/yr) | [Sib: manufacturing-cost.md] [KB-M] |
| Implied Tier-1 plate gross margin at US$300-400 ASP | 45-70 % at the SKU level | [Sib: manufacturing-cost.md] [KB-M] |
| Company-level gross margins of Taiwanese cooling houses (AVC, Auras, Cooler Master, Delta thermal) | ~15-25 % (mix of fans, heat pipes, plates; ODM price pressure) | [KB-L] |
| Jentech (lids/IHS; Group-A for Rubin) gross margin | ~35-45 % | [KB-L] |
| CoolIT | ~US$550 M NTM revenue, ~30 % adj. EBITDA margin; Ecolab paid 29x NTM adj. EBITDA (~8.6x sales) | [Sib: Ecolab deck / 8-K] (I) |
| Vertiv (company level, thermal is one segment) | adjusted operating margin ~20 % (2025) | [KB-M] |
| AVC 2024 revenue | NT$71.8 bn (~US$2.2 B) | [Sib: news.tvbs.com.tw/english/3179423 ; taiwannews.com.tw/en/news/6215881] |

Reading: the *plate SKU* can be very profitable for whoever owns the Nvidia slot, but ODM/Nvidia purchasing compresses company-level margins; the system vendors (CoolIT, Vertiv, Schneider/Motivair, Boyd/Eaton) earn their margin on CDUs, manifolds, service and water chemistry (the explicit logic of Ecolab's purchase).

## 5. Competitive landscape and shares

| Vendor | Role in cold plates | Ownership / 2024-26 event | Share / position hint | Nvidia status | Provenance |
|---|---|---|---|---|---|
| AVC (Asia Vital Components, 3017.TW) | Volume GPU/CPU plates, skived Cu | public | **~40-50 % of GB200/GB300 plates**; developing VR plates for 1.8-2.3 kW | Group-A (Rubin) | [Sib: TVBS, Taiwan News] (A) |
| Cooler Master | Sealed D2C modules, plates | private/Taiwan | Group-A (Rubin); material Blackwell share | Group-A | [Sib: coolermaster.com GPU/CPU coldplate page; TVBS] |
| Delta Electronics | Cu microchannel plates, CDUs, power | public | Group-A (Rubin); also 800 VDC power partner | Group-A | [Sib: deltaww.com liquid-cooling page; TVBS] |
| Jentech (3653.TW) | IHS/lids; micro-channel lids | public | Group-A (Rubin) - the lid incumbent for any direct-to-die/lid co-design | Group-A | [Sib: TVBS/Digitimes]; role [KB-M] |
| Auras (3324.TW) | Plates, CDUs, manifolds | public | second-tier Blackwell plate supplier; strong with ODMs | RVL [KB-M] | [KB-M] |
| CoolIT Systems | Plates (OMNI, NA2 loop), CHx CDUs (up to 2 MW), manifolds; author of OCP cold-plate test spec | KKR + Mubadala (2023) -> **Ecolab US$4.75 B (closed Jul 2026)** | ~US$550 M revenue; "4 of top 5 OEMs, 4 of 5 hyperscalers" (V); **not on Rubin Group-A list** | Nvidia Partner Network; NA2 loop for GB200 | [Sib: businesswire 20260319353197; itbrief.co.uk; coolitsystems.com NVIDIA page] |
| Boyd | Plates, manifolds, CDUs (builds Google Deschutes CDU); Nvidia RVL | Goldman Sachs AM -> **Eaton (announced Oct 2025, ~US$9.5 B)** [KB-M] | Largest Western thermal CM; TPU/Meta programmes [KB-M] | RVL | [Sib: boydcorp.com NVIDIA collaboration pages] |
| Vertiv | CoolChip CDUs (100 kW-2.3 MW), CoolTera plates, GB200 NVL72 7 MW reference architecture with Nvidia | acquired CoolTera (Dec 2023) [KB-H] | CDU leader; plates minor | Reference-design partner | [Sib: investors.vertiv.com GB200 blueprint; vertiv.com CoolChip] |
| Schneider Electric / Motivair | CDUs 105 kW-2.5 MW; "Dynamic Cold Plates" (no skived microchannels) | Schneider bought 75 % of Motivair (announced Oct 2024, ~US$850 M) [KB-H] | HPC heritage; plates small | Reference-design partner | [Sib: motivaircorp.com; datacenterdynamics Motivair] |
| Nidec | CDUs (> 5,000 shipped), Deschutes prototype 2 MW / 80 psi; adding plate and QD capacity in Thailand/Philippines/China | public (Japan) | CDU volume leader with Google | - | [Sib: nidec.com Deschutes sheet; technews.tw/?p=1321939] |
| JetCool | Microjet SmartPlate/SmartLid | **Flex acquired (Nov 2024)** | Niche/retrofit; Flex integration into trays | - | [Sib: investors.flex.com JetCool release] |
| Mikros | Normal-Flow laminated plates (AX-NV1/NV2) | **Jabil acquired (Oct 2024)** | Niche | - | [Sib: businesswire 20241003396998] |
| Fabric8Labs / Wiwynn / GIGABYTE | ECAM-printed Cu plates (4 kW double-sided) | VC-backed; Wiwynn NexGen (Aug 2026), GIGABYTE (Jul 2026) | Gen-2 challenger via ODMs | - | [Sib: d2pmagazine 2026/08/14; gigabyte.com/press/news/2436] |
| Asetek | - | exited HPC 2021; DC assets "dormant"; 2025 indication of interest from unnamed buyer | not a competitor | - | [Sib: hpcwire 2021; overclock3d] |
| Accelsius, ZutaCore (two-phase) | 2-phase D2C | Accelsius via Innventure (public); ZutaCore VC | single-digit % niche | - | [Sib: businesswire 20260721991081; counterpointresearch] |
| Chilldyne | negative-pressure plates/CDUs | **Daikin Applied acquired (Nov 2025)** | niche | - | [Sib: daikinapplied.com news] |
| Corintis | in-silicon / heat-map-matched microfluidics | US$24 M (Sep 2025), Microsoft partnership | 2028+ | - | [Sib: yolegroup.com; tech.eu] |
| Foxconn/Ingrasys, Quanta/QCT, Wiwynn, Supermicro, Inventec, Pegatron | ODM tray/rack integrators; some in-house plates (Foxconn claims +30 % heat transfer, V) | public | buy plates to Nvidia spec | ODM partners | [Sib: taiwannews 6311653; blog.qct.io QoolRack] |

Market-share summary [D, KB-L]: in **GPU/CPU plates for Nvidia racks** the Taiwanese four (AVC, Cooler Master, Delta, Auras) plus Jentech hold ~80-90 % of units; CoolIT, Boyd, Vertiv/CoolTera, Motivair, Jabil/Mikros, Flex/JetCool share the rest, concentrated in OEM-branded systems (Dell, HPE, Lenovo) and HPC. In **CDUs** Vertiv, CoolIT, Nidec/Boyd (Google), Motivair/Schneider, nVent, Delta and Envicool lead. In **hyperscaler ASIC plates**, each hyperscaler designs and dual-sources (Boyd, AVC, Delta, Nidec, Auras, Jabil, Flex) [KB-M].

## 6. Buyers, design-in dynamics, qualification

### 6.1 Who actually buys a GPU cold plate

| Buyer | What they control | How they buy | Provenance |
|---|---|---|---|
| **Nvidia** | Thermal/mechanical envelope of the SXM/puck module and tray (mounting, TIM window, 45 C inlet, 65 C return, per-tray flow, dP allowance), the Recommended Vendor List (plates, manifolds, CDUs, QDs), and for Rubin the **plate purchase itself** (centralised; Group-A list) | Annual platform cadence (Blackwell 2024-25, Blackwell Ultra 2025-26, Rubin 2H 2026, Rubin Ultra 2H 2027, Feynman 2028); design freeze ~12 months before ramp; NDA liquid-cooling design guides | [Sib: TVBS/Digitimes; QCT whitepaper; standards-reliability.md]; cadence [KB-H]; freeze timing [KB-M] |
| **ODMs** (Foxconn/Ingrasys, Quanta, Wiwynn, Supermicro, Inventec, Pegatron, ZT/AMD) | Tray and rack integration, hose/QD routing, leak test, cost | Buy to Nvidia AVL at target cost; multi-source; squeeze ASP | [Sib: QCT, Ingrasys notes] [KB-M] |
| **OEMs** (Dell IR7000, HPE GX/Cray EX, Lenovo Neptune, Supermicro DLC-2) | Branded DLC systems; may use own plates (HPE, Lenovo) or partners (Dell-CoolIT since 2017) | Multi-year supply agreements; warranty-driven qualification | [Sib: coolit-products.md; competitors-singlephase.md] |
| **Hyperscalers** (Google, AWS, Meta, Microsoft, Oracle, xAI, OpenAI/Broadcom) | For their own ASICs: the whole plate spec (bare-die, series plumbing, 80 psi head available at Google); for Nvidia racks: facility water class, CDU, leak/commissioning standards | Direct engineering engagement + contract manufacturing; TCO-based; OCP contributions | [Sib: Google Hot Chips 2025, Deschutes CDU] |

### 6.2 What wins a design-in (ranked) [KB-M, informed by Sib]

1. **Qualification status** - on Nvidia's RVL/AVL or a hyperscaler's AVL; OCP-format test package (leak <= 1e-5 mbar-L/s He, burst > 20 bar, pressure and thermal cycling, PG25 soak, cleanliness) [Sib: OCP Cold Plate Test Spec v1.0.0]. Without this nothing else matters.
2. **Capacity and footprint** - >= 100 k plates/month, two geographies, APQP/PPAP-style controls, 100 % serialised leak test [Sib: manufacturing-cost.md; standards-reliability.md].
3. **Price** - ~US$300-400 ASP at Rubin class; ODMs will not pay a premium for thermal margin they do not need to meet Nvidia's spec [Sib; KB-M].
4. **Leak/reliability record** - leaks are the top operator concern (Uptime), dominated by connections; all-metal unibody (OMNI argument) is now table stakes [Sib: standards-reliability.md].
5. **Thermal margin / dP** - matters when it changes something the buyer pays for: higher inlet (chiller-less hours), lower flow (CDU count), Tj headroom (boost clocks), or hot-spot control on the HBM zone. CoolIT's brief is explicit that the *system* value is "suitable for 45 C inlet" [Brief].

### 6.3 Qualification cycle [KB-M]

Plate-level qualification to an OCP-style matrix takes **~4-8 months** (design review, CFD-TTV correlation, 1,000-h corrosion soak, 10 k-100 k pressure cycles, 100-1,000 thermal cycles, vibration/shock); platform integration and ODM/Nvidia approval adds **3-6 months**; first revenue follows the platform ramp. A new entrant should therefore plan **12-18 months** from first TTV data to first volume PO, and align to a platform (Rubin Ultra 2H 2027 or Feynman 2028) rather than to the current one.

### 6.4 Nvidia's role: does it design the plate?

- For GB200/GB300, Nvidia published the rack/tray reference design and the envelope; plates were designed by suppliers to that envelope and procured by ODMs from the RVL [Sib; KB-M].
- For **Vera Rubin, Nvidia moved to centralised plate purchasing with a short Group-A list** (Jentech, AVC, Cooler Master, Delta) [Sib: TVBS/Digitimes]. Nvidia is reported to be seeking **micro-channel-lid / direct-to-chip** partners for Rubin Ultra (Wccftech; Digitimes Sep 2025) [Sib: coolit-products.md], and analysts (Kuo) say the 2.3 kW Rubin part ships first with a gold-plated lid + microchannel plate, with a microchannel lid not before 2H 2027 [Sib: ctee.com.tw 20260107701081].
- The **MGX** modular reference architecture (gen-3 for Rubin, cable-free, designed for 45 C inlet) fixes tray geometry, manifold position and QD interfaces, which is what makes a plate "drop-in" [Sib: techpowerup 342049]. "Nvidia-Certified" applies to systems, not to plates; the plate-level gate is RVL/AVL membership [KB-M].

## 7. M&A and funding 2023-2026

| Date | Deal | Value | What it signals | Provenance |
|---|---|---|---|---|
| Apr 2023 | KKR (+ Mubadala) acquire CoolIT | ~US$270 M (reported) [KB-L] | PE enters DLC pre-Blackwell | [Sib: gulfnews; mubadala.com] |
| Dec 2023 | Vertiv acquires CoolTera (UK CDU/plates) | undisclosed | CDU majors buy plate/CDU IP | [KB-H] |
| Oct 2024 | Jabil acquires Mikros Technologies | undisclosed | EMS majors buy plate tech | [Sib: businesswire 20241003396998] |
| Oct 2024 - Feb 2025 | Schneider Electric buys 75 % of Motivair | ~US$850 M [KB-H] | Power/cooling majors buy CDU capacity | [KB-H] |
| Nov 2024 | Flex acquires JetCool | undisclosed | EMS majors buy microjet IP | [Sib: investors.flex.com] |
| Sep 2025 | Corintis raises US$24 M; Microsoft microfluidics partnership | US$24 M | In-silicon cooling funded as 2028+ option | [Sib: yolegroup.com; tech.eu] |
| Oct 2025 | Eaton to acquire Boyd Thermal | ~US$9.5 B [KB-M] | Largest thermal CM goes to an electrical major | [KB-M] |
| Nov 2025 | Daikin Applied acquires Chilldyne | undisclosed | HVAC majors buy negative-pressure niche | [Sib: daikinapplied.com] |
| Mar-Jul 2026 | **Ecolab acquires CoolIT** | **US$4.75 B cash; 29x NTM adj. EBITDA; ~8.6x sales** | Water-chemistry major buys the DLC system leader; Mubadala exits | [Sib: businesswire 20260319353197; SEC 8-K; agbi.com] |
| 2025-26 | Fabric8Labs - Wiwynn / GIGABYTE programmes | (funding undisclosed this session) | ECAM moves from demo to ODM programmes | [Sib: d2pmagazine; gigabyte.com] |
| 2025 | Asetek: indication of interest for dormant DC liquid-cooling business | - | Legacy IP available cheaply | [Sib: overclock3d] |

Valuation read-across [D]: Ecolab paid ~8.6x sales for a ~30 % EBITDA-margin, > 30 %-growth system vendor. A plate-only start-up with no CDU/service attach will be valued on design-in wins, not on this multiple; the strategic buyers (Eaton, Ecolab, Schneider, Vertiv, Flex, Jabil, Daikin, Delta, Nidec) are the realistic exit set.

## 8. What performance is worth to an operator (quantified)

| Lever | Physics / arithmetic | Operator value | Provenance |
|---|---|---|---|
| **10 kPa lower plate dP** at 18 LPM | hydraulic power = 0.0003 m3/s x 10,000 Pa = **3 W per 15 kW plate**; at rack level (144 LPM for 120 kW at 1.2 LPM/kW) 24 W hydraulic, ~50 W electrical at ~50 % wire-to-water efficiency = **~0.04 % of rack power**; per GW of IT ~0.4 MW ~ 3.5 GWh/yr ~ **US$0.3 M/yr at US$0.08/kWh** | Energy value is small. The real value is **capex/compatibility**: fits CHx-class CDU heads (35-53 psi secondary) with two plates in series, leaves budget for 25-50 um filters (Schneider: filter dP must be in the rating), enables negative-pressure loops (< 1 atm available), and lets one CDU serve more racks | [D]; CDU heads [Sib: coolit-products.md]; filter [Sib: blog.se.com 2025/12/16]; Chilldyne [Sib] |
| **1 K lower case-to-inlet dT**, spent as +1 K facility supply | Dry cooler capacity ~ UA x (T_fluid - T_ambient); at a ~10 K design approach, +1 K = **~+10 % capacity** or ~10 % less dry-cooler area/fans for the same heat; trim-chiller energy falls ~2-3 % per K of setpoint (industry rule) | For a 100 MW DLC campus with dry coolers at ~US$100-200/kW [KB-L]: ~US$1-2 M capex per K, plus more chiller-less hours in hot climates; a 5-10 K improvement moves a W45 site to W+ (50-55 C), i.e. chiller-less almost everywhere | [D]; approach and chiller rule [KB-M]; W classes [Sib: upsite.com ASHRAE 5th ed. summary] |
| **1 K lower Tj** at fixed inlet | leakage ~ doubles per 20-30 K; leakage 20-30 % of GPU power -> ~0.1-0.3 % GPU power per K; Arrhenius reliability ~ -5 to -7 % FIT per K | 1 GW fleet: 1-3 MW (~US$0.7-2 M/yr); plus boost-clock headroom (Frore claims +10 % tokens from -10 C, V) | [KB-L]; Frore [Sib: tomshardware Frore LiquidJet] (V) |
| **Flow reduction** (same Tcase at 0.75-1.0 instead of 1.2 LPM/kW) | 20-40 % fewer LPM per kW -> fewer/ smaller CDUs, pumps, manifolds; Nvidia's own 45 C in / 65 C out envelope is 0.75 LPM/kW | CDU capex ~US$200-400/kW [KB-L] -> 20-40 % of that; also smaller QDs/hoses | [Sib: chip-roadmap-requirements.md energy balance] |
| **Hot-spot uniformity** (CoolIT: 12-17 K spread; TC5 limiting) | HBM Tj max 95 C sits at the package edge where coolant is hottest; uniformity sets the usable budget, not the mean | Removes 6-10 K of "wasted" margin on the worst zone at zero mean-dT cost | [Brief]; [Sib: physics-options.md] |
| **Reliability (all-metal, fewer joints)** | leaks dominated by connections and human error (Uptime); no vendor publishes plate MTBF | A single rack leak event can idle US$3-4 M of GB300 hardware; operators pay for unibody and blind-mate UQDB | [Sib: standards-reliability.md] [KB-M] |

Net: for a *plate* vendor, **inlet-temperature headroom and uniformity are the monetisable thermal metrics; dP is monetised through CDU count and compatibility, not energy.** CoolIT sells exactly this ("suitable for 45 C inlet") and, tellingly, does not publish dP [Brief].

## 9. How a new entrant can realistically win

| # | Route | Why it can work | Why it is hard | Verdict |
|---|---|---|---|---|
| 1 | **Hyperscaler custom-ASIC plates** (Google TPU, AWS Trainium, Meta MTIA, Microsoft Maia, OpenAI/Broadcom) | Buyers own the spec, run bare-die, allow 80 psi, evaluate on TCO, and dual-source Western CMs; volumes 1-3 M plates/yr each | Needs a CM partner for capacity; long NDAs; Google already has Boyd/Nidec | **Beachhead** - highest probability of a paid design-in within 12-18 months |
| 2 | **Nvidia Rubin / Rubin Ultra via a Group-A or Western CM partner** (license core + manifold IP; or sell the etched-manifold insert as a sub-component) | Nvidia buys centrally at ~US$400; a drop-in MGX plate with lower dT and dP has a clear pitch; our route keeps skiving + etching + laser weld, so Group-A houses can make it | Gatekept list; capacity >= 100 k/month; price-capped; CoolIT itself is outside the list | **Partner, do not go direct** |
| 3 | **Micro-channel lid / direct-to-die co-design** for Rubin Ultra (2H 2027) / Feynman | Nvidia reported to be seeking lid partners; paste TIM is the largest resistance in the CoolIT stack (8-16 K at 150-250 W/cm2); our manifold core becomes the lid | Jentech is the lid incumbent; requires TSMC/Nvidia packaging buy-in; warranty on die | **High prize, low odds alone - pursue with Jentech-class partner** |
| 4 | **OEM-branded systems** (Dell, HPE, Lenovo, Supermicro) | They differentiate on DLC and are less captive to Nvidia's Group-A; Dell-CoolIT shows a single-vendor model works | Incumbent relationships; CoolIT/Ecolab, Boyd/Eaton | Secondary channel |
| 5 | **800 VDC power electronics** (SiC/GaN power shelves, SSTs; 15-40 kW loss per MW rack) and automotive/industrial SiC inverters | Less gatekept; higher Tj (150-175 C) and 65 C inlet suit a lower-R plate; same core, different SKU | Automotive pin-fin baseplates are a commoditised, cost-driven market (Boyd, Dana, Modine, Hanon) [KB-M] | **Second SKU**, not the lead |
| 6 | **Transparency / standards play** | Publish full OCP v1.0.0 reports, dP at 6 flow points, independent-lab (ORNL / university) data; CoolIT discloses no dP and no independent data | Costs money; does not by itself win volume | **Do it** - it is the cheapest way to beat the benchmark "in every aspect" that CoolIT left open |
| 7 | Two-phase or immersion lead product | +9 C inlet (Accelsius, V) | Facility unfamiliarity, PFAS, single-digit share through 2030 [KB-M] | Keep as a later variant only |

Recommended commercial architecture [D]: (i) lead with a **water/PG25 single-phase, all-copper, conventionally manufactured plate** that beats the benchmark on mean dT, worst-point dT and dP at the same 1.2 LPM/kW and also meets spec at 0.75-1.0 LPM/kW; (ii) qualify it in OCP format with independent data; (iii) sign a hyperscaler ASIC programme and a CM/Group-A manufacturing partner in parallel; (iv) position the same core as a micro-channel-lid candidate for 2027-28; (v) ship a pin-fin/power-electronics derivative for 800 VDC shelves.

## 10. Application breadth

| Application | 2026-28 volume signal | Fit for the architecture | Provenance |
|---|---|---|---|
| AI GPUs/ASICs in NVL72/NVL144/Helios/TPU/Trainium racks (1.4-3.6 kW per package, 70-130 W/cm2 die average, 45 C inlet) | 8-15 M plates/yr (2026) rising to 15-25 M (2027) | Primary | [D]; [Sib: chip-roadmap-requirements.md] |
| NVSwitch / networking ASICs and NICs (toward 100 % heat capture) | ~18 switch plates per NVL72 + NIC/DPU plates | Same core, smaller footprint | [D from Sib] |
| CPUs (Grace, Xeon 6, Turin) | 36 per NVL72; 2 per 2U server | Commodity (JetCool, CoolIT, Auras all ship) | [Sib: JetCool datasheets] |
| 800 VDC power shelves / SST / DC-DC (SiC/GaN) | 15-40 kW loss per 1 MW rack from 2027 | Pin-fin baseplate SKU; 65 C inlet | [Sib: chip-roadmap-requirements.md] [KB-M] |
| Automotive / industrial SiC inverters | large but commoditised; Boyd DSC plate 0.026 K/W, 12.5 kPa at 10 LPM | Low-margin; only if the same line can serve it | [Sib: Boyd HybridKIT datasheet] |
| HPC (Cray EX/GX, Frontier-class) | smaller, warm-water 40 C | Yes; HPE/Cray uses own plates | [Sib] |
| Retrofit HGX air-to-liquid | niche | JetCool model | [Sib] |

## 11. Gaps / unknowns

1. **No analyst report could be read this session** (Dell'Oro, Omdia, IDTechEx, Uptime, SemiAnalysis, TrendForce, Morgan Stanley primary). All analyst market-size and share figures above are [KB-L/M] ranges or secondary press reposts; confirm by pulling the primary reports.
2. **Rack shipment counts** (GB200/GB300/VR200 2025-27) are [KB-L]; the plate-volume estimates scale directly with them.
3. **Nvidia's plate-level R and dP requirements, RVL membership and Group-A terms** are NDA; the Group-A list and ~US$400 ASP come from Taiwanese press (TVBS/Digitimes) and have not been confirmed by Nvidia.
4. **Market shares other than AVC's 40-50 %** are the author's estimates; no vendor publishes plate unit shares. SemiAnalysis's paid report reportedly has CoolIT's GB200/GB300 share [Sib: coolit-products.md].
5. **Margins**: SKU-level 45-70 % is derived from an unverified cost teardown; company-level Taiwanese gross margins (15-25 %) and Jentech (35-45 %) are from memory; verify in TWSE filings.
6. **M&A values**: Eaton-Boyd (~US$9.5 B), Schneider-Motivair (~US$850 M), KKR-CoolIT (~US$270 M), Vertiv-CoolTera date are [KB]; Ecolab-CoolIT, Flex-JetCool, Jabil-Mikros, Daikin-Chilldyne, Corintis are sibling-sourced with URLs. Fabric8Labs funding rounds, JetCool pre-acquisition funding, ZutaCore/Accelsius funding not retrieved.
7. **Operator value quantification** (dry-cooler approach, chiller %/K, leakage %/K, CDU US$/kW, dry-cooler US$/kW) is engineering arithmetic with [KB-M/L] coefficients; no published operator study quantifying US$ per K or per kPa was retrieved.
8. **Qualification cycle lengths** (4-8 months plate, 12-18 months to PO) are experience-based [KB-M]; the OCP test matrix itself is sourced.
9. **Hyperscaler ASIC plate volumes and sourcing** (who makes TPU/Trainium/Maia plates) are [KB-L].
10. **CDU pricing** (US$200-400/kW) is [KB-L]; no list prices were retrieved for CHx2000, CoolChip or Deschutes units.
11. Follow-up searches to run when budget allows: "Dell'Oro liquid cooling forecast 2026", "Omdia liquid cooling market 2026", "IDTechEx data center liquid cooling 2035", "Uptime Institute cooling survey 2025 direct liquid cooling adoption", "GB300 NVL72 rack shipments 2026 TrendForce", "Eaton Boyd Thermal acquisition", "Schneider Motivair acquisition value", "Vertiv CoolTera acquisition", "Fabric8Labs funding 2025", "AVC gross margin 2025", "Jentech microchannel lid Rubin Ultra", "Nvidia recommended vendor list cold plate", "SemiAnalysis liquid cooling market share cold plate".

## 12. Sources

Benchmark:
- CoolIT 15 kW Tech Brief (June 2026) - local extract `docs/cooling/appendix/pdf/brief.txt`; press release https://www.coolitsystems.com/resources/news/15kw_press_release/ ; DCD https://www.datacenterdynamics.com/en/news/coolit-designs-15kw-coldplate-to-future-proof-liquid-cooling-for-gpus/

CoolIT corporate / Ecolab (sibling-sourced):
- Ecolab to acquire CoolIT (19 Mar 2026): https://www.businesswire.com/news/home/20260319353197/en/ ; deck https://s204.q4cdn.com/218790897/files/doc_downloads/2026/03/Ecolab-to-Acquire-CoolIT-Systems.pdf ; SEC 8-K https://www.sec.gov/Archives/edgar/data/31462/000110465926032446/tm269446d1_ex99-1.htm ; close https://itbrief.co.uk/story/ecolab-completes-usd-4-75-billion-coolit-takeover ; Mubadala exit https://www.agbi.com/finance/2026/03/mubadala-offloads-minority-stake-in-nearly-5bn-coolit-deal/ ; https://www.mubadala.com/en/what-we-do/coolit ; KKR/Mubadala 2023 https://gulfnews.com/business/markets/abu-dhabis-mubadala-kkr-acquire-canada-based-liquid-cooling-solutions-firm-1.96784139
- CoolIT manufacturing scale-up: https://www.hpcwire.com/2025/06/25/coolit-systems-scales-north-american-manufacturing-to-cool-ais-next-wave/ ; Nvidia partnership https://www.coolitsystems.com/capabilities/co-innovation/nvidia/ ; Dell https://www.datacenterdynamics.com/en/news/dell-emc-to-equip-poweredge-servers-with-coolit-liquid-cooled-systems/
- Ecolab Q&A on field cold-plate issues (Oct 2026): https://electronics360.globalspec.com/article/24164/q-a-ecolab-bets-on-liquid-cooling-for-ai-data-center-growth

Pricing / BOM / procurement (sibling-sourced):
- Morgan Stanley NVL72 cooling BOM via TechRadar: https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks ; igor'sLAB https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
- Nvidia Rubin centralised purchasing, Group-A suppliers: https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html
- AVC share of GB200/GB300 plates: https://news.tvbs.com.tw/english/3179423 ; https://www.taiwannews.com.tw/en/news/6215881
- IDTechEx cold-plate ASP (repost): https://onartificialintelligence.com/articles/34213/two-phase-d2c-cooling-in-data-center-thermal-management-cost-analysis
- Rubin TDP / lid timing (Kuo via CTEE): https://www.ctee.com.tw/news/20260107701081-430704 ; Rubin NVL144 45 C MGX gen-3: https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production ; Rubin Ultra 600 kW: https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027
- Nvidia seeking lid/direct-to-chip partners: https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/ ; https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html
- TrendForce GB200 rack TDP: https://www.trendforce.com/presscenter/news/20240730-12232.html ; QCT GB200 NVL72 whitepaper: https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf

Competitors / M&A (sibling-sourced):
- Boyd-Nvidia: https://www.boydcorp.com/boyds-collaboration-with-nvidia.html ; https://welcome.boydcorp.com/boyd-cooling-for-nvidia-ai-systems ; Boyd HybridKIT DSC datasheet https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf
- Vertiv GB200 blueprint: https://investors.vertiv.com/news/news-details/2024/Vertiv-Codevelops-with-NVIDIA-Complete-Power-and-Cooling-Blueprint-for-NVIDIA-GB200-NVL72-Platform/default.aspx ; CoolChip CDU https://www.vertiv.com/zh-CN/products-catalog/thermal-management/high-density-solutions/vertiv-coolchip-cdu/
- Motivair: https://www.motivaircorp.com/products/dynamic-cold-plates/ ; https://www.datacenterdynamics.com/en/news/motivair-launches-dynamic-cold-plates-without-skived-microchannels/
- Flex acquires JetCool: https://investors.flex.com/news/news-details/2024/Flex-Acquires-JetCool-to-Expand-Data-Center-and-Power-Portfolio/ ; https://insidehpc.com/2024/11/flex-acquires-liquid-cooling-company-jetcool/
- Jabil acquires Mikros: https://www.businesswire.com/news/home/20241003396998/en/Jabil-Acquires-Mikros-Technologies-to-Support-Demand-for-Liquid-Cooling-in-AI-Data-Centers
- Daikin acquires Chilldyne: https://www.daikinapplied.com/news/news/daikin-applied-expands-data-center-offering-with-acquisition-of-chilldyne
- Corintis US$24 M: https://www.yolegroup.com/industry-news/corintis-raises-24m-to-target-the-next-ai-bottleneck-and-collaborates-with-microsoft-for-chip-cooling-breakthrough/ ; https://tech.eu/2025/09/25/corintis-lands-24m-and-microsoft-endorsement-for-chip-cooling-tech/
- Asetek: https://www.hpcwire.com/2021/09/22/asetek-announces-it-is-exiting-hpc/ ; https://overclock3d.net/news/cases_cooling/asetek-may-sell-its-liquid-cooling-business-to-an-unknown-buyer/
- Fabric8Labs / Wiwynn / GIGABYTE: https://www.d2pmagazine.com/2026/08/14/fabric8labs-wiwynn-collaborating-to-develop-nexgen-3d-printed-cold-plates-for-ai-data-centers/ ; https://www.gigabyte.com/fi/press/news/2436 ; https://www.wiwynn.com/technology/advanced-cooling/cold-plate-liquid-cooling
- Nidec CDUs: https://www.nidec.com/v=1764743613/files/topics/19006_ext_5_en_0.pdf ; https://technews.tw/?p=1321939
- Foxconn plates: https://www.taiwannews.com.tw/en/news/6311653 ; Cooler Master: https://www.coolermaster.com/en-global/products/GPU%2FCPU-Coldplate.html ; Delta: https://www.deltaww.com/en-US/products/liquid-cooling-solutions
- Accelsius two-phase benchmark (Jul 2026): https://www.businesswire.com/news/home/20260721991081/en/ ; Counterpoint on ZutaCore: https://counterpointresearch.com/en/insights/AI-Data-Centers-Zutacore-In-Pole-Position-To-Benefit-From-Transition-To-Two-Phase-Cooling ; LiquidStack on DTC share: https://www.facilitiesdive.com/news/liquidstack-touts-modular-scalable-data-center-coolant/749676/
- AMD Helios: https://introl.com/blog/amd-helios-mi455x-nvidia-competition-ces-2026
- Frore LiquidJet (Rubin, +10 % tokens, V): https://www.tomshardware.com/pc-components/liquid-cooling/frore-shows-off-liquidjet-nexus-coldplate-for-nvidia-vera-rubin-other-ai-accelerators-offers-up-claimed-10-percent-token-generation-boost-over-rival-liquid-cooling-solutions

Hyperscalers / standards / operator context (sibling-sourced):
- Google liquid cooling at Hot Chips 2025: https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips ; Google 1 MW racks / Deschutes CDU: https://cloud.google.com/blog/topics/systems/enabling-1-mw-it-racks-and-liquid-cooling-at-ocp-emea-summit ; https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
- OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf ; OCP cold-plate development & qualification white paper: https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/ ; OCP L-L CDU methodology: https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/ ; OCP PG25 guidelines: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
- Uptime Institute (40 C GPU supply limit): https://intelligence.uptimeinstitute.com/entity_pdf/node/153594/pdf
- ASHRAE 5th-edition liquid classes (summary): https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/
- Schneider on CDU rating and filter dP: https://blog.se.com/datacenter/2025/12/16/account-for-filtering-too-beware-of-how-cdu-rating-capacity-is-specified/
- Supermicro DLC-2: https://www.supermicro.com/en/pressreleases/supermicros-dlc-2-next-generation-direct-liquid-cooling-solutions-aims-reduce-data
- Microsoft/Corintis microfluidics: https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/

Items cited from background knowledge with no URL verified this session [KB]: Dell'Oro / Omdia / IDTechEx / Uptime market figures; Nvidia GTC 2025 and GTC-DC Oct 2025 shipment statements (3.6 M Blackwell orders by top-4 CSPs; ~20 M Blackwell+Rubin through 2026); Vertiv-CoolTera (Dec 2023); Schneider-Motivair (~US$850 M, 75 %); Eaton-Boyd Thermal (~US$9.5 B, Oct 2025); KKR-CoolIT ~US$270 M (2023); Taiwanese vendor gross margins; CDU and dry-cooler US$/kW; chiller %/K and leakage %/K rules of thumb.
