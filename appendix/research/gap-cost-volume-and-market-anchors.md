# Gap fill: cost, volume and market anchors for the "beat CoolIT on manufacturability and cost" claim

*Prepared 2026-10-13 for the cold-plate programme (Workflow 1, gap-fill angle). Companion calculation file: `research/gap_cost_volume_calc.py` (all [D] numbers below are produced by it).*

## 0. Provenance and method (read first)

- **No live web search or fetch succeeded in this session.** The per-turn WebSearch budget (200 calls shared by every agent in the workflow) was already exhausted when this agent started; all four queued queries were refused. The single permitted WebFetch attempt (TechRadar / Morgan Stanley article) failed on DNS (`ENOTFOUND www.techradar.com`), as the task warned. No workaround was attempted.
- Consequently this report cannot deliver *RFQ-grade* numbers. What it does instead: (1) reconciles the internal contradictions in the existing reports so the programme has **one canonical cost/volume table**, (2) separates what is URL-verified from what is background knowledge, (3) adds cross-checks that constrain the unverified numbers from two or three independent directions, and (4) specifies the exact RFQ package and the searches needed to close the remaining gaps.
- Tags: **[A]** analyst/press figure whose URL a sibling agent verified from a search extract (not full text); **[Sib-URL]** vendor/standards page URL verified by a sibling; **[Brief]** CoolIT 15 kW tech brief (June 2026, local PDF); **[KB-H/M/L]** author's background knowledge, high/medium/low confidence, *not verified this session*; **[D]** derived here (arithmetic in `gap_cost_volume_calc.py`).

## 1. Executive summary

1. **The cost contradiction is a labelling error, not a modelling disagreement.** `manufacturing-cost.md` says "US$90-160 at 100k+/yr" in its summary but tabulates ~US$170 / ~105 / ~70 at 10k / 100k / 1M. A re-built nine-line model with explicit low/high per element gives **US$121-205 (mid 163) at 10k, US$70-133 (mid 102) at 100k and US$48-90 (mid 69) at 1M** [D, KB-M]. The table was right; the "90-160" band straddled the 10k and 100k columns. **Canonical figures to use from now on: ~US$165 / ~US$100 / ~US$70 (bare plate, no QDs), each +/- 25 %.**
2. **"US$300 per plate" is almost certainly a plate *assembly* price, not a bare-plate price.** The Morgan Stanley BOM (~US$49,860 per GB300 NVL72 rack, ~US$2,260 per compute tray, ~US$300 per CPU/GPU plate, ~US$200 per NVSwitch plate [A]) is internally consistent only if the US$300 line carries hoses and UQD halves: two UQD04/06 halves (US$15-40 each) plus hoses (US$8-15) absorb US$38-95 of it [D, KB-M]. Combined with AVC's company-level gross margin (~17-20 % [KB-M]) this means the **bare-plate price the ODM pays is more like US$200-260 and the incumbent's bare-plate cost US$100-180** - i.e. our US$100 at 100k is *parity*, not a 2-3x advantage. The 45-70 % "SKU margin" in the sibling reports is an upper bound that assumes the whole US$300 is plate.
3. **2026 NVL-class rack volume: use 35k (low) / 55k (base) / 80k (high).** The two sibling assumptions (30-50k vs 50-80k) are both inside the band produced by three independent triangulations: Nvidia GPU-count statements (67-125k if every Blackwell/Rubin GPU were racked, which it is not), rack-revenue arithmetic (43-83k) and 2025 analyst run-rates (25-35k) grown 1.5-2.3x [D, KB-L]. Plates: **4.4-10 M Nvidia-rack plates in 2026 (base ~7 M), 7.6-15 M in 2027** [D].
4. **ASPs**: GB300 CPU/GPU plate ~US$300, NVSwitch ~US$200, Vera Rubin plate "up to US$400", VR NVL144 cooling BOM ~US$55,710 [A: Morgan Stanley via TechRadar / igor'sLAB]; Rubin plate purchasing centralised by Nvidia with **Group-A = Jentech, AVC, Cooler Master, Delta** [A: TVBS 3188903, Digitimes a20260318PD231, March 2026]. No Nvidia confirmation exists; no public RVL document exists; Boyd states RVL membership for plates/manifolds/CDUs on its own site [Sib-URL]; CoolIT is a Nvidia Partner Network member but **not on the reported Group-A list** [Sib].
5. **CDU and TCS US$/kW**: no list price was verified. Constrained estimate: **CDU hardware US$120-300 per kW** (1-2 MW units US$250-500k), full TCS outside the rack US$200-500/kW, in-rack BOM **US$356/kW** [D from A]. Cross-check: CoolIT's "> US$11 B TCS spend in 2026" [Brief] divided by US$550-850/kW gives 13-20 GW of DLC IT, versus a bottom-up 11-13 GW (60k racks x 140 kW + 3-5 GW of hyperscaler ASICs) - the same order of magnitude, so the US$/kW band is credible [D].
6. **Operator value of +1 K supply temperature**: no published operator US$/K exists. Engineering value: +8-12 % dry-cooler capacity per K at an 8-12 K design approach (= US$0.8-2.0 M of dry-cooler capex per K per 100 MW IT at US$80-200/kW thermal), plus US$0.16-0.32 M/yr per K of trim-chiller energy in hot climates, plus US$0.14-0.35 M/yr per 100 MW if the kelvin is spent on Tj (0.2-0.5 %/K chip power) [D, KB-M/L]. **-10 kPa plate dP** is worth only ~US$70k/yr per 100 MW in pump energy, but if it allows one more rack per head-limited CDU it is worth **US$9-25 per plate** in CDU capex [D, KB-L].
7. **800 VDC power-shelf adjacency**: 9-26 kW of in-rack conversion heat per 600 kW-1 MW rack [D], 8-20 liquid-cooled power units per rack, plate ASP US$50-150 [KB-L]: **US$4-90 M/yr and 0.08-0.6 M plates/yr at 10-30k Kyber-class racks (2027-28)**. Real but an order of magnitude below the GPU-plate business; sell it as a rack kit, not a standalone product [D, Sib].

## 2. Canonical factory-cost model (bare GB-class plate, 100 x 120 mm skived Cu, welded lid, Ni-plated, no QDs)

Ranges are low/high at each annual volume; drivers stated so an RFQ can replace each line. All [KB-M] unless tagged.

| Cost element (US$ per plate) | 10k/yr | 100k/yr | 1M/yr | Driver / how to verify |
|---|---|---|---|---|
| OFHC copper stock 1.5-2.2 kg (plate ~0.9-1.4 kg finished), LME Cu ~US$10-12/kg 2026, net of 50-70 % swarf credit | 14-22 | 12-19 | 11-17 | LME copper price (public); plate mass from CAD [KB-H on price band, D on mass] |
| Skived fin core (2-5 min cycle, machine US$150-400k, 1-2 operators) | 25-40 | 15-28 | 11-20 | ask Winshare / LORI / Kingka / Wieland Microcool for 100 x 100 mm skived core quotes [KB-M] |
| Cover + ports (CNC at 10k-100k; stamped + CNC finish at 1M) | 30-50 | 12-25 | 6-12 | CNC shop rate US$40-80/h x 15-40 min [KB-M] |
| Join: vacuum braze / green-laser / FSW | 8-15 | 4-9 | 2.5-6 | see Section 3 |
| Electroless Ni-P 8-12 um, wetted path + contact face | 6-12 | 4-7 | 2.5-5 | plating houses quote per rack-load; ~300-400 cm2 plated area [KB-M] |
| Leaf spring, bracket, screws, O-rings | 14-22 | 9-16 | 6-11 | catalogue parts + stamped spring [KB-M] |
| Hose stubs / barbs / fittings (UQDs excluded) | 10-18 | 6-12 | 4-8 | [KB-M] |
| 100 % He leak + proof pressure + flow/dP test (OCP Cold Plate Test Spec v1.0.0 regime) | 6-10 | 3-6 | 2-4 | 3-6 min test cell time [KB-M]; spec [Sib-URL OCP] |
| Yield loss (95-98 %), scrap, overhead, logistics | 8-16 | 5-11 | 3-7 | [KB-M] |
| **Total, bare plate** | **121-205 (mid 163)** | **70-133 (mid 102)** | **48-90 (mid 69)** | [D] |
| + 2 x UQD04/06 halves + hoses (to compare with the US$300 line) | +38-95 | +38-95 | +30-70 | Staubli / Parker / CPC / Danfoss UQD list prices [KB-M] |

Resolution of the sibling contradiction: the summary line "US$90-160 at 100k+" in `manufacturing-cost.md` should be read as "~US$100 at 100k, ~US$70 at 1M, up to ~US$165 at 10k". The tabulated 170/105/70 stands.

### 2.1 What the ASP cross-checks imply for "beat on cost"

| Check | Result | Implication |
|---|---|---|
| Morgan Stanley BOM arithmetic [A -> D] | 18 trays x US$2,260 = US$40,680; residual US$9,180 covers 9 switch trays (18 x US$200 = US$3,600) and rack manifolds/QDs/hoses (US$5,580). Per compute tray: 6 x US$300 = US$1,800, residual US$460 for VR plates, tray hoses/QDs. Plates = 72 % of the rack cooling BOM | the US$300 figure is a *tray-level line item*; whether it includes the UQD halves is unstated |
| Taiwanese cooling-house margins [KB-M] | AVC company GM ~17-20 %, Auras ~20-24 %, Delta ~30-33 %, Jentech (lids) ~35-45 %; Cooler Master private | a plate SKU at 45-70 % GM would be visible in AVC's reported margin; it is not (liquid cooling lifted AVC's GM by a few points, not by 30) [KB-M] |
| Supplier cost at plausible SKU margins [D] | at US$300 ASP: 25 % GM -> US$225 cost; 40 % -> US$180; at US$400 (Rubin): 30 % -> US$280 | the incumbent's *landed* cost including UQDs, hoses, freight and warranty is US$180-260, and its bare plate US$100-180 |
| Our model at 100k [D] | bare plate US$70-133, mid US$102 | **parity with the incumbent, not a 2-3x advantage.** The honest cost claim is: "same cost structure, same supply base, +US$10-25 for the manifold laminate and laser lid, paid back by thermal margin, dP and uniformity" |

## 3. Process adders: what each option costs on top of the canonical plate (100k/yr unless stated)

| Option | Adder, US$ per plate | Basis | Confidence |
|---|---|---|---|
| Photochemically etched Cu manifold laminate, 1-2 layers of 0.2-0.3 mm C10100/C11000 | **+5-15** (2 layers), +3-8 (1 layer) | etching houses (Precision Micro, Fotofab, Tecan, Chinese PCE shops) price per 450 x 600 mm sheet US$30-80 at volume; a 100 x 120 mm part nests 15-20 per sheet -> US$2-5 per layer; phototool US$0.3-1.5k; plus a braze/weld or diffusion tack to the core | KB-M |
| Green-laser (515 nm disk) lid weld instead of vacuum braze | **-2 to +3** (cheaper than braze at >= 50k/yr; dearer at 10k because of amortisation) | cell US$300-600k (TruDisk 1-3 kW green + robot + fixture + fume); ~440 mm perimeter + bosses at 1-3 m/min = 20-60 s per plate; at 100k/yr amortisation ~US$1, labour/gas/optics US$1-2; at 10k/yr amortisation alone ~US$8-12 | KB-M |
| FSW lid (OMNI-class) | **+4-12** vs laser | machine US$0.5-1.5 M, W-Re / PCBN tool US$1-3k lasting ~50-200 m of copper weld -> US$3-10 tool cost per plate; 1-3 min cycle | KB-M |
| Electroless Ni-P plating of wetted path (if required by customer) | **+4-7** (already in the canonical model) | per-load racked plating; thickness 8-12 um; note 2 x 5 um removes 10 % of a 100 um gap [Sib gap-tim2] | KB-M |
| Electrolytic Ni 3-5 um on the *contact face only* (needed for liquid-metal TIM) | +1-3 | small masked area | KB-M |
| Liquid-metal TIM (Ga-In-Sn) applied at plate level | **+3-10** all-in | material is negligible (0.1-0.2 g at US$400-700/kg = US$0.04-0.14 [D]); cost is Ni/Au-plated faces, dispensing, foam containment ring, inspection and handling scrap | KB-M (material price KB-L; Ga prices spiked 2024-25 under Chinese export controls) |
| Indium pre-form TIM (0.1-0.2 mm, ~40 cm2) | **+5-15** | 4.4 g indium = US$1.3-2.2 material [D]; patterned pre-form suppliers (Indium Corp. class) quote US$5-15 at volume; reflow or compression fixture extra | KB-M |
| ECAM (Fabric8Labs) printed fin core instead of skived | **+20-60 at maturity; +50-150 today** | 12 cm3 of copper per fin field [D]; at 5-20 cm3/h per machine and US$0.5-1 M per machine, amortisation alone is US$8-60 per plate [D, KB-L]; Fabric8 publishes no price, throughput or plate-level R/dP [Sib] | KB-L |
| Full etched + diffusion-bonded laminate core (Mikros-class) | +40-80 | sibling estimate retained; furnace cycle 6-12 h, batches 50-500 | KB-M |
| Cu L-PBF plate | +300-700 | not a volume route | KB-M |

Net for the programme's base design (skived core + 1-2 etched manifold layers + laser lid + contact-face Ni + paste): **~US$110-125 at 100k/yr, ~US$80 at 1M, ~US$175-185 at 10k** [D].

## 4. ASP, procurement and supplier anchors

| Item | Value | Source | Confidence |
|---|---|---|---|
| GB300 NVL72 liquid-cooling BOM | ~US$49,860 per rack; ~US$2,260 per compute tray | Morgan Stanley via TechRadar; igor'sLAB (2025) | A (URL sibling-verified; full text not read) |
| GB300 CPU/GPU plate; NVSwitch plate | ~US$300; ~US$200 | same | A |
| Vera Rubin NVL144 cooling BOM; Rubin plate | ~US$55,710 per rack; "up to US$400 per unit" | same | A |
| Rubin plate procurement | Nvidia centralised purchasing; **Group-A: Jentech, AVC, Cooler Master, Delta**; ASP ~US$400 | TVBS 3188903; Digitimes a20260318PD231 (Mar 2026) | A (press; Nvidia has not confirmed) |
| Second-tier Rubin plate suppliers | Auras, Nidec, Foxconn/Ingrasys in-house, Kaori, Jiate reported in Taiwanese press as "Group B" / backup | - | KB-L (not verified; may be wrong) |
| AVC share of GB200/GB300 plates | ~40-50 % | TVBS 3179423; Taiwan News 6215881 | A |
| AVC 2024 revenue | NT$71.8 bn (~US$2.2 B) | same | A |
| AVC 2025 revenue / GM | revenue up ~50 %+; GM ~18-21 % (liquid-cooling mix lifts GM 1-3 pts) | TWSE filings not read | KB-L |
| IDTechEx GPU plate ASP | US$300-500; ~US$2,300 per 8-GPU server; ~US$55k per rack | onartificialintelligence.com repost | A |
| Nvidia RVL (plates, manifolds, CDUs, QDs) | exists under NDA; **Boyd** states membership publicly; CoolIT states Nvidia Partner Network; Vertiv (CDU reference architecture), Delta, Cooler Master, AVC, Auras, Motivair and Supermicro are variously reported as listed | boydcorp.com [Sib-URL]; others KB-M | mixed |
| CoolIT | ~US$550 M NTM revenue, ~30 % adj. EBITDA; Ecolab US$4.75 B (closed Jul 2026); not on reported Group-A | businesswire 20260319353197 [Sib-URL] | I (8-K) |
| Nvidia plate-level R / dP requirement | none public; secondary: < 0.03 K/W, < 20 kPa at 1.8 LPM (fibermall); 0.013 K/W at 1.7 LPM, 12 kPa (ToneCooling) | [Sib-URL] | V/S |

Reading: for Rubin, the plate is a **four-supplier, Nvidia-bought commodity at ~US$400 including whatever Nvidia bundles into the line**. A new entrant does not displace Group-A on cost; it enters through (a) an ODM/hyperscaler ASIC programme (Wiwynn/Fabric8 precedent), (b) Group-B qualification for a Rubin Ultra / Kyber refresh where thermal margin is scarce, or (c) co-design with the lid supplier (Jentech's presence on a *plate* list is the signal that lid + TIM2 + plate are being specified as one system [Sib gap-tim2]).

## 5. Rack shipments and plate volumes, 2025-2027

### 5.1 Three independent triangulations for 2026 [D; inputs KB-L/M]

| Method | Inputs | 2026 NVL72-equivalent racks |
|---|---|---|
| Analyst run-rate growth | 2025 GB200/GB300 NVL72 ~25-35k (TrendForce / Morgan Stanley class figures, 2025) [KB-M]; 2026 growth 1.5-2.3x on GB300 + VR200 ramp | **38-80k** |
| GPU-count | Huang (GTC-DC Oct 2025): ~20 M Blackwell + Rubin GPUs visible through CY2026 [KB-H on the quote]; 2026 share 8-12 M GPUs; NVL-rack share of GPUs 60-75 % (rest HGX boxes) | 67-125k *if all shipped*; ordering visibility is not shipment; discount 30-40 % for HGX/air and timing -> **45-85k** |
| Rack revenue | Nvidia data-centre revenue attributable to NVL racks 2026 US$150-250 B [KB-L]; rack ASP US$3.0-3.5 M [KB-M] | **43-83k** |
| **Adopted band** | | **35k low / 55k base / 80k high** |

Both sibling assumptions (30-50k; 50-80k) sit inside this band; the base case splits them. Rubin Ultra / Kyber (~600 kW, 2H 2027 [Sib-URL DCD]) should be counted as NVL72-equivalents by GPU count (NVL576 = 144 packages = 2 NVL72-equivalents by package count) when converting to plates.

### 5.2 Plates per rack and per year [D]

| Rack | Plates per rack | Basis |
|---|---|---|
| GB300 NVL72 | 108 CPU/GPU + 18 NVSwitch = **126** | Morgan Stanley BOM arithmetic [A -> D] |
| VR NVL144 (Rubin) | **~150** (126 + NIC / VR / power-stage plates toward 100 % heat capture) | [KB-M]; Nvidia MGX gen-3 cable-free tray, 100 % liquid [Sib-URL techpowerup] |
| Kyber NVL576 | ~300 by package count (plus power shelves, Section 9) | [D] |

| Year | Racks (NVL72-eq.) | Nvidia-rack plates (126-150/rack) | + hyperscaler ASIC / AMD plates | Total DLC plates |
|---|---|---|---|---|
| 2025 | 25-35k | 3.1-5.2 M | +1-2 M | 4-7 M |
| **2026** | **35-80k (base 55k)** | **4.4-12 M (base ~7-8 M)** | +2-4 M | **6.5-16 M (base ~10 M)** |
| 2027 | 60-120k | 7.6-18 M | +3-6 M | 11-24 M |

Plate revenue cross-check: 7.5 M Nvidia-rack plates x US$300 = US$2.25 B, i.e. ~20 % of CoolIT's US$11 B 2026 TCS figure, consistent with "plates are 25-40 % of TCS spend" [Sib market-business] once ASIC plates are added.

## 6. CDU and TCS cost per kW

| Item | Value | Basis | Confidence |
|---|---|---|---|
| In-rack liquid-cooling BOM per kW IT | **US$356/kW** (US$49,860 / 140 kW) | [D from A] | medium-high |
| CDU hardware (1-2 MW in-row / row units: CoolIT CHx1500/CHx2000, Vertiv CoolChip 1,350-2,300 kW, Motivair, Boyd/Google Deschutes) | **US$120-300 per kW**; US$250-500k per 1-2 MW unit | no list prices public; budgetary quotes and HPC tender awards cluster here | KB-L |
| TCS outside the rack (CDU + row manifolds + piping + valves + commissioning) | US$200-500 per kW IT | 1.0-1.5x the in-rack BOM [Sib market-business, KB-M] | KB-L |
| Total TCS | **US$550-850 per kW IT** | sum | KB-L |
| Cross-check vs CoolIT "> US$11 B 2026 TCS spend" [Brief] | US$11 B / (550-850) = **13-20 GW** of DLC IT in 2026; bottom-up 60k racks x 140 kW = 8.4 GW + 3-5 GW ASICs = 11-13 GW | same order of magnitude; the band is credible, the lower end of US$/kW slightly favoured | [D] |
| CDU per rack | US$18-42k per rack at 12-14 racks per 2 MW CDU | [D] | KB-L |
| CHx2000 | 2,000 kW at 5 C approach, 1.2 LPM/kW; 53 psi secondary head; "up to 12 GB200/GB300 NVL72 racks" | [Sib-URL coolitsystems.com; storagereview] | V |

## 7. Operator value of +1 K supply temperature and -10 kPa plate dP

No operator (Google, Microsoft, Meta, AWS, Oracle, CoreWeave) has published a US$-per-kelvin or US$-per-kPa figure for DLC supply conditions to my knowledge [KB-M on the absence]. The closest public anchors are: ASHRAE TC 9.9 W-classes (W45 = chiller-less dry-cooler operation in nearly all climates) [Sib-URL upsite summary]; the DOE/FEMP/LBNL rule that each +1 F of chilled-water setpoint saves ~1-2 % of chiller energy (~2-3.5 %/K) [KB-M]; Nvidia's GB200 "45 C warm water" and 25x energy / 300x water efficiency marketing claims (V) [KB-M]; CoolIT's own framing that the *system* value of its plate is "suitable for 45 C inlet" [Brief].

### 7.1 +1 K of case-to-inlet margin, spent as +1 K facility supply [D]

| Mechanism | Value per 100 MW IT | Basis |
|---|---|---|
| Dry-cooler capacity (Q = UA x approach; design approach 8-12 K) | **+8-12 % capacity per K**, or 8-12 % fewer dry coolers = **US$0.8-2.0 M capex per K** at US$80-200/kW thermal installed | KB-L on US$/kW; D |
| Trim-chiller energy, hot climate (Phoenix / Riyadh / Singapore class) | 100-200 fewer trim hours per K x 100 MW / COP 5 = 2-4 GWh/yr = **US$0.16-0.32 M/yr per K** | KB-L on hours (TMY-derived) |
| Trim-chiller capex | peak trim load falls ~proportionally to (T_amb,max - T_supply + approach); at 10 K of design deficit, -10 % per K of chiller/condenser capacity | KB-M |
| Chiller-less hours in temperate climates | already ~100 % at W45; value is resilience margin, not energy | KB-M |
| Spent on Tj instead (0.2-0.5 %/K chip power on N3/N2 class silicon) | 1.8-4.4 GWh/yr = **US$0.14-0.35 M/yr per K**, or equivalent boost-clock headroom | KB-M on %/K |
| Spent on flow instead (same Tcase at 1.0 vs 1.2 LPM/kW) | -17 % LPM -> -17 % of CDU/pump/manifold capex (~US$30-80/kW of the US$200-500/kW) | D, KB-L |

So a plate that delivers the benchmark's 80 C case at a **50 C** instead of 45 C inlet (5 K) is worth roughly **US$4-10 M of heat-rejection capex plus US$1-2 M/yr of energy per 100 MW** - an order of magnitude more than the plate price premium (5 K x 126 plates x ~US$25 adder x 700 racks = US$2.2 M per 100 MW). This is the business case to put in front of operators, with the caveat that every coefficient above is a rule of thumb awaiting an operator-validated number.

### 7.2 -10 kPa plate pressure drop [D]

| Mechanism | Value | Basis |
|---|---|---|
| Hydraulic power | 3 W per 15 kW plate; ~70 W hydraulic / ~140 W electrical per 140 kW rack (2-3 plates in series-equivalent); **US$70k/yr per 100 MW IT** at US$0.08/kWh | D |
| CDU head budget (CHx2000 53 psi = 365 kPa; CHx1000 35 psi = 240 kPa) | 20-30 kPa saved per tray = 6-12 % of secondary head -> +3-6 % flow at fixed pump curve, or room for a 25 um point-of-use filter (+7-20 kPa clean), or **one more rack per head-limited CDU = US$9-25 per plate of CDU capex** | [Sib-URL CDU heads]; D; KB-L on CDU price |
| Negative-pressure (leak-proof) loops (Chilldyne-class, < 1 atm available) | enabling, not monetised | [Sib] |

Conclusion: dP is a **compatibility and CDU-count** argument, not an energy argument; state it as "fits two plates in series under a 35 psi CDU with a 25 um filter" rather than as W saved.

## 8. 800 VDC / SiC power-electronics anchors

| Item | Value | Source | Confidence |
|---|---|---|---|
| Nvidia 800 VDC architecture | announced May 2025 (developer blog); white paper + partner demos OCP Oct 2025; first deployment with Kyber (Rubin Ultra NVL576, ~600 kW, 2H 2027) | developer.nvidia.com blog [Sib-URL]; DCD 600 kW [Sib-URL] | I / A |
| Power-system partners | Delta, Flex, LITEON, Megmeet (shelves / DC-DC); Eaton, Vertiv, Schneider, ABB, Siemens, Hitachi Energy, Mitsubishi Electric, GE Vernova (SST / rectifiers); silicon: Infineon, Navitas, TI, ROHM, ST, onsemi | Nvidia Oct 2025 announcements | KB-M (names), not re-verified |
| In-rack conversion heat (800 V -> 50/12 V at 97.5-98.5 %) | **9-15 kW on a 600 kW rack; 15-26 kW on a 1 MW rack** | D | KB-M on efficiency |
| Power units per rack; heat per unit | 8-20 units; 1-2 kW each (50-100 kW DC-DC stages) | KB-M | low-medium |
| Liquid-cooled 800 VDC power-shelf specs (kW, W/in3, coolant, dP) from Delta / Flex / LITEON | **not found by any agent**; no public thermal spec exists yet | [Sib power-electronics] | gap |
| Plate ASP; cost target | US$50-150 per 2-5 kW power-shelf plate; US$50-100/kW of conversion hardware | KB-L | low |
| Volume and revenue (2027-28) | 10-30k Kyber-class racks x 8-20 units = **0.08-0.6 M plates/yr = US$4-90 M/yr** | D | low |
| EV traction SiC (the colleague's "SSD converter" reading) | inverter BOM US$8-12/kW; cooler/housing content US$20-60; module vendor owns the pin-fin baseplate; aluminium/Si-OAT loops; AQG 324 qualification 24-36 months | [Sib power-electronics, KB-M] | poor near-term fit; license-only |

Reading: the 800 VDC shelf is the *same loop, same customers, same chemistry* as the GPU plate and should be a de-rated SKU in a rack cooling kit; it is not a stand-alone business case (US$4-90 M/yr at maturity vs US$2-5 B/yr of GPU/ASIC plates).

## 9. How to convert this into RFQ-grade numbers (the package to send)

Send one drawing package to at least two houses per process and ask for 10k / 100k / 1M per year pricing, FOB factory, with NRE separated:

1. **Skived core**: C10100/C10200 OFE, 100 x 120 x 12 mm blank, fin field 90 x 100 mm, fins 0.15 mm / gap 0.15 mm / 2.0 mm tall (and an alternate at 0.10/0.10/1.5), base 1.2 mm under fins, flatness 25 um over the contact face. Vendors: Winshare Thermal, LORI (Shenzhen), Kingka Tech, Wieland Microcool (US/DE), Boyd, Auras (if willing), USUSTK.
2. **Etched manifold laminate**: 2 layers of 0.25 mm C11000 (or C10100), slot pattern at 2.5 mm pitch, +/- 30 um, 20 parts per sheet. Vendors: Precision Micro (UK), Fotofab / Photofabrication Engineering (US), Tecan (UK), Micrometal (DE), 2-3 Shenzhen PCE houses.
3. **Lid + weld**: stamped or CNC C11000 cover with weld lip 3 mm; green-laser seam (Trumpf / IPG / Laserline job shops) and FSW (Stirtec, TWI-licensed shops, Taiwanese EV-battery FSW houses) quoted separately; He leak 1e-5 mbar-L/s, proof 10 bar, burst > 20 bar [Sib-URL OCP test spec].
4. **Plating**: electroless Ni-P 8-12 um mid-P on wetted path; electrolytic Ni 3-5 um on contact face; ask for throwing-power guarantee in 0.15 mm channels.
5. **TIM**: liquid-metal dispensing service quote (Indium Corp., Arieca, Thermal Grizzly OEM, Chinese Ga-alloy suppliers) and indium pre-form quote (Indium Corp. Heat-Spring class, 40 cm2 x 0.15 mm).
6. **ECAM**: development quote from Fabric8Labs for a 100 x 120 mm fin field at 10k and 100k/yr with throughput and lead time disclosed.
7. **UQDs**: Staubli / Parker / CPC / Danfoss UQD04-08 list and 100k pricing (to settle what the US$300 line contains).
8. **CDU**: budgetary quotes for a 1.5-2 MW CDU from CoolIT/Ecolab, Vertiv, Motivair/Schneider, Boyd, Delta - to replace the US$120-300/kW band.

Searches to run when the budget resets (extended mode for numeric ones): `Morgan Stanley "GB300" "NVL72" liquid cooling "$49,860" OR "$2,260" cold plate "$300"`; `TrendForce "NVL72" rack shipments 2026 forecast GB300 VR200`; `Digitimes OR TVBS Rubin cold plate "Group A" Jentech AVC "Cooler Master" Delta`; `AVC 3017 2025 gross margin liquid cooling TWSE`; `"skived" copper cold plate "100x100" price MOQ Winshare OR LORI`; `photochemical etching copper 0.3 mm price per sheet volume`; `green laser copper welding cost per part cold plate`; `electroless nickel plating cold plate price per piece`; `Fabric8Labs ECAM throughput capacity plates per year 2026`; `Dell'Oro liquid cooling forecast 2026 2027`; `IDTechEx data center liquid cooling 2026-2036 cold plate ASP`; `CDU price "per kW" OR "$/kW" 2 MW CoolIT CHx2000 OR Vertiv CoolChip quote`; `dry cooler installed cost "per kW" data center 2025`; `NVIDIA 800 VDC power shelf liquid cooled Delta Flex LITEON kW spec OCP 2025`; `"cold plate" "BOM" OR "factory cost" GB200 teardown`.

## 10. Gaps / unknowns

1. **No number in this report was verified live.** Every [A] figure was URL-verified by a sibling from a search extract, not from full text; every [KB] figure is background knowledge. The RFQ package in Section 9 is the only way to RFQ-grade cost.
2. **Whether the Morgan Stanley US$300 includes UQD halves and hoses** is unknown and swings the incumbent's bare-plate price by US$40-95. This single fact decides whether "beat on cost" is credible; it is the first thing to settle (read the full TechRadar / igor'sLAB text or the Morgan Stanley note).
3. **AVC / Auras / Jentech 2025 margins** are not read from filings; the 17-20 % AVC GM is background knowledge.
4. **2026 rack shipments** remain a 2.3x band (35-80k); no TrendForce / Morgan Stanley / SemiAnalysis 2026 figure was read.
5. **Nvidia RVL membership**, Group-A terms, and any Group-B list are NDA or press-only; CoolIT's absence from Group-A is press-only.
6. **CDU and dry-cooler US$/kW** have no verified price point; the cross-check against CoolIT's US$11 B only bounds them to the right order of magnitude.
7. **Operator US$/K and US$/kPa** do not exist publicly; Section 7 is engineering arithmetic on rule-of-thumb coefficients (approach, chiller %/K, chip %/K, trim hours).
8. **ECAM cost and throughput** are undisclosed; the +US$20-60 / +50-150 bands are derived from an assumed 5-20 cm3/h deposition rate that Fabric8 has not published.
9. **800 VDC power-shelf thermal specs** (kW, dP, coolant) are unpublished by Delta / Flex / LITEON / Nvidia; the whole Section 8 volume case is derived.
10. **Copper price** is assumed at US$10-12/kg; a 2026 LME quote should replace it (copper is 10-15 % of the bare-plate cost, so +/- 20 % on copper moves the total by +/- 2-3 %).

## 11. Sources

URL-verified by sibling agents (search extracts; full text not read):
- TechRadar (Morgan Stanley NVL72 cooling BOM, US$49,860 / US$2,260 / US$300 / US$200; VR NVL144 US$55,710, US$400): https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks
- igor'sLAB (same BOM; Rubin Ultra 3.6 kW): https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
- TVBS (Rubin Group-A: Jentech, AVC, Cooler Master, Delta; centralised purchasing; ~US$400): https://news.tvbs.com.tw/english/3188903
- Digitimes (same, 18 Mar 2026): https://www.digitimes.com/news/a20260318PD231.html
- TVBS / Taiwan News (AVC 40-50 % share; NT$71.8 bn 2024 revenue): https://news.tvbs.com.tw/english/3179423 ; https://www.taiwannews.com.tw/en/news/6215881
- IDTechEx repost (US$300-500 per GPU plate; US$2,300 per 8-GPU server; US$55k per rack): https://onartificialintelligence.com/articles/34213/two-phase-d2c-cooling-in-data-center-thermal-management-cost-analysis
- Ecolab / CoolIT 8-K and deck (US$550 M NTM revenue; US$4.75 B): https://www.businesswire.com/news/home/20260319353197/en/
- CoolIT CHx2000 (2 MW, 53 psi, 12 racks): https://www.coolitsystems.com/cdu-product/chx2000/ ; https://www.storagereview.com/news/coolit-unveils-chx2000-cdu-with-2mw-liquid-cooling-capacity-in-standard-rack-footprint
- Vertiv CoolChip CDU: https://www.vertiv.com/zh-CN/products-catalog/thermal-management/high-density-solutions/vertiv-coolchip-cdu/
- Google Deschutes CDU 80 psi: https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
- OCP Cold Plate Test Specification v1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- OCP L-L CDU test methodology (1.5 LPM/kW; >= 40 psi; TCS to 100 psi): https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- ASHRAE 5th-edition W-classes (Upsite summary): https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/
- Nvidia 800 VDC architecture blog (May 2025): https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/
- DCD, Rubin Ultra NVL576 ~600 kW, 2H 2027: https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027
- TechPowerUp, Vera Rubin NVL144 (45 C, 2026 volume): https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production
- TrendForce GB200 NVL72 rack TDP: https://www.trendforce.com/presscenter/news/20240730-12232.html
- Boyd (Nvidia RVL statement; Deschutes CDU): https://www.boydcorp.com (Nvidia collaboration pages, per sibling)
- Fabric8Labs / Wiwynn / UIUC: https://www.fabric8labs.com/ecam-vs-legacy-liquid-cooling-cold-plates/ ; https://www.d2pmagazine.com/2026/08/14/fabric8labs-wiwynn-collaborating-to-develop-nexgen-3d-printed-cold-plates-for-ai-data-centers/ ; https://mechse.illinois.edu/news/82871
- Vendor plate figures (secondary): https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/
- CoolIT 15 kW tech brief (June 2026), local: `docs/cooling/appendix/pdf/brief.txt`

Sibling reports used: `research/manufacturing-cost.md`, `research/market-business.md`, `research/power-electronics.md`, `research/coolit-products.md`, `research/standards-reliability.md`, `research/chip-roadmap-requirements.md`, `research/competitors-singlephase.md`, `research/gap-competitor-plate-datasheets-gb300-rubin-scale.md`, `research/gap-tim2-interface-impedance-and-reliability.md`, `research/gap-nvidia-rubin-plate-envelope-and-package-geometry.md`.

Background-knowledge items with no URL (to verify): LME copper ~US$10-12/kg (2026); AVC / Auras / Delta / Jentech gross margins; NVL72 rack ASP US$3.0-3.5 M; Nvidia "~20 M Blackwell + Rubin GPUs through 2026" (GTC-DC Oct 2025); 2025 NVL72 shipments 25-35k (TrendForce / Morgan Stanley class); UQD04/06 half prices US$15-40; PCE sheet prices; green-laser / FSW cell costs and cycle times; electroless Ni pricing; gallium-alloy and indium prices; Fabric8 deposition rate; DOE/FEMP chiller-setpoint rule; dry-cooler US$/kW; chip power %/K; 800 VDC partner names and conversion efficiencies.
