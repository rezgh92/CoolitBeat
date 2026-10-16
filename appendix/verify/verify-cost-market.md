# Adversarial verification: cost, value and go-to-market (PRISM draft)

Independent model: `verify/cost_market_check.py` (Monte Carlo, 200k samples). `arch/prism_cost.py` was not reused; it is inspected in section 7.

## 1. Verdict in five lines

1. The **US$160 factory cost at 100k/yr is too low**. A bottom-up rebuild gives **US$195-225 (P50 about US$210)**. Even with every disputed line at its most favourable value, the floor is **about US$173**. The three largest misses are:
   - the braze filler was costed before the 2025-26 silver rally, at US$5 instead of US$13-24;
   - furnace loading and cycle time are optimistic;
   - the yield and overhead allowance of 15 % is below the judges' own 18-25 % rule for a non-reworkable bonded stack.
2. The incumbent comparison mixes plate sizes. The draft's "~US$110 CoolIT-class" figure is the research team's GB-class plate (100 x 120 mm), not a 125 mm, 15 kW-class plate. Like-for-like, the premium is **+50 to +83 % (P50 +66 %)**, not +45 %. Per kW of capacity PRISM is **about 27-29 % worse**, not 8-10 % worse.
3. **PRISM-G's US$120 has no derivation** anywhere in the draft or scripts. Applying the draft's own rate card gives US$126-134, and my bottom-up gives US$159-180. At that cost the **GPU-class facility TCO case inverts** (value/premium 0.3-1.0x). The 15 kW-class value case survives, but at about 2-10x rather than 15-60x.
4. The channel evidence has moved against the draft:
   - **AVC's gross margin is 32.6 % (2Q26), not 17-20 %**;
   - NVIDIA standardises the Rubin plate design and buys it centrally;
   - AVC already ships Google TPU v8 and AWS Trainium3 liquid cooling from 4Q26, and prioritises ASIC capacity because ASIC margins are higher;
   - analysts expect micro-channel lids (Jentech) or micro-channel cold plates (AVC, Auras) to displace plain lidded plates from 2027.

   The beachhead is therefore contested, and rank 2 (NVIDIA through a Group-A partner) goes through the wrong decision-maker.
5. The **12-month US$6.6 M budget adds up arithmetically** but omits about US$0.9-2.1 M of items. It also contradicts itself on Build-B tooling. Funded honestly, it is US$7.5-8.7 M with the US$1.1 M contingency kept. There is no revenue model and no plan for who funds scale-up capex of US$3.7-9 M per 100k/yr.

## 2. Unit cost (draft section 5.6) re-derived

Basis:

- LME copper cash US$14,395/t on 1 Sep 2026 (Cochilco) and US$14,737/t on 8 Sep 2026 (Westmetall), as the draft says.
- Silver about **US$65/oz** in early September 2026 (spot US$64.8-66.4).
- Everything else is an engineering estimate (KB) and must be replaced by RFQs.

| Line (100k/yr per SKU) | Draft | This check P10/P50/P90 | Verdict and basis |
|---|---:|---:|---|
| OFE copper | 35 | 35 / 39 / 43 | **corrected (+4)**. Part-by-part buy is 2.9 kg, not 2.5 (the 4.5 mm laminations need about 1.4 kg of strip for 0.55 kg finished); scrap about 1.3 kg. OFE at US$17-19/kg is the low end (US$17-22); the US$11.5/kg scrap credit is conservative. The errors partly cancel. |
| Skived core + tip planing | 22 | 14 / 20 / 28 | confirmed (research band US$15-28) |
| Kerfing | 3 | 2 / 3 / 6 | confirmed |
| Grate + meter (486 orifices) + separator | 5 | 4 / 6 / 9 | plausible. Die amortisation is not shown. |
| 2 x 4.5 mm laminations | 4 | 4 / 7 / 12 | **corrected**. Punching at d/t = 1 in 4.5 mm copper distorts the sheet, which must then be flattened or lapped to hold a braze gap of 50 µm or less over 125 mm. |
| Header bar | 12 | 10 / 14 / 20 | plausible-low |
| **Filler + clean** | **5** | **13-24** | **refuted**. 25 µm BAg-8 over about 410 cm² of lands is 10.2 g of filler and 7.4 g of Ag: **US$15.5 of silver alone** at US$65/oz. Route A totals US$19-24; route B (5 µm masked plate) US$13-19. No project file uses a silver price. |
| Vacuum braze + stack-up | 16 | 18 / 22 / 27 | **corrected**. 30-80 plates per load and 6-11 h cycles need **1.7-3.1 furnaces per 100k/yr (P50 2.2), not 1.5**; fixtures cost US$2-10 per plate-cycle; stacking six layers takes 4-12 min. |
| Fly-cut / stubs / hardware | 5 / 8 / 14 | ≈ same | confirmed |
| Test incl. IR screen | 9 | 7 / 10 / 14 | confirmed |
| Die set per SKU (5 stamping + 1 forging) | not shown | +1.3-3.3 | **missing**. The die set costs US$0.4-1.0 M per SKU and is amortised over 300k plates. |
| Yield, scrap, overhead | 15 % | 93 % mature yield, 12 % overhead: about +20 % | **corrected**. The judges set 18-25 % for a non-reworkable bonded stack at ramp. |
| **Factory cost, 100k** | **~160** | **197 / 209 / 222** | **corrected**. The floor is US$173. |
| Factory cost, 10k (ramp, laser-cut/CNC parts) | ~300 | 371 / 398 / 428 | **corrected**. This is the real cost for the first 18-24 months of sales. |
| 1M/yr | ~113 | not modelled | The scorecard's "Stretch US$113 at 1M/yr" sits beside the incumbent's 100k figure. That comparison is invalid: the incumbent costs about US$75 at 1M/yr. |

**Per-SKU volume matters more than the draft admits.** The cost columns are per-SKU volumes. Yet the beachhead sells *custom-zoned* plates ("meter artwork + plenum laminations per heat map, 2-3 weeks"). With hard dies, every zoning change costs US$0.4-1.0 M and takes 8-14 weeks. Five 20k/yr SKUs therefore cost close to the 10k column, not the 100k column.

## 3. Incumbent comparison and US$/kW

**The incumbent baseline is the wrong size.** "~US$110 at 100k" is the research canonical *GB-class* plate (100 x 120 mm, `gap-cost-volume`) with corrected copper. That figure is confirmed. A like-sized CoolIT 15 kW-class plate is 125-130 mm square, weighs 1.2-1.6 kg and has barbs of 1/2-3/4 in, so it costs about **US$116-137 (P50 126)**.

**The premium against that like-sized plate** is +50 / +66 / +83 %, or **US$67-99 per plate**. Against the GB-class plate the draft used, the premium is +69 to +108 %.

US$ per kW of Tcase-limited capacity (draft's own capacities): PRISM 10.8 (PCM) / 12.6 (paste) against CoolIT-15 8.5 / 9.8, versus the draft's 8.2 / 9.6 against 7.6 / 8.7. **Corrected: about 27-29 % worse per kW, not 8-10 %.**

**ASPs confirmed** (Morgan Stanley via TechRadar / igor'sLAB): GB300 plate about US$300, NVSwitch about US$200, Rubin "up to US$400"; a Taiwanese report gives US$150-300 generic.

**One correction in section 7.2.** "About US$400 per assembly, US$200-260 bare" mixes generations. The US$200-260 bare figure was derived from the *GB300* US$300 line. The same deduction applied to Rubin's US$400 gives **about US$300-360 bare**.

## 4. Facility value case (sections 5.6 and 6.7)

**Value per kelvin.** The draft says US$0.8-2.0 M per K per 100 MW. My value is **US$0.54-1.09 M (P50 0.78)**, so the claim is **corrected**.

- The physics is fine: at an 8-12 K design approach, +1 K of supply cuts dry-cooler UA by 7-13 % (LMTD check); an existing unit gains only 4-6 % capacity per K.
- Only the UA-proportional share (about 55-80 %) of installed cost scales; piping, foundations and electrical do not.
- The US$80-200/kW-thermal installed cost is **unverifiable**: no public dry-cooler price was found, only system-level anchors (US$4.5-5.2 M/MW with CDUs).

**Inlet headroom.** The draft says +7-11 K. Like-for-like it is **+7.0 K at P50**, so the claim is **corrected**.

- The "+11 K" pairs PRISM on PCM (51.7 C) against CoolIT on paste (40.8 C). That breaks the draft's own like-for-like rule. CoolIT re-tested on PCM is 44.7 C, which gives +7.0 K; paste against paste also gives +7.0 K.
- At the draft's own P90, headroom is **+2.2 K (paste) and +3.4 K (PCM)**.

**15 kW class.** Value/premium is **4.6-10x at P50 headroom and 1.8-4.2x at P90**, not 15-60x. The basis is about 6,700 plates per 100 MW and a price premium of the cost premium divided by 0.7. The case survives, but no 15 kW package ships in volume before about 2029.

**GPU class.**

- The draft's +2-3 K is not supported by its own table 3.3. The maxima improve by 1.7-2.4 K at nominal, the average by only 0.3-1.0 K, and the conservative case loses the average.
- With the draft's undocumented US$120 PRISM-G, value/premium is 1.6-3.3x.
- With a costed PRISM-G (US$159-180, a premium of US$43-71), it is **0.33-0.8x. The TCO case fails.**

**Capture is not addressed.**

- Supply temperature is set by the most limiting device on the loop and by the vendor's specification (NVIDIA markets Vera Rubin at 45 C "with no chillers", CES 2026). PRISM on the accelerators alone does not raise it.
- Facilities are designed once for 15-20 years, so the headroom is mostly spent on the *next* chip: option value, not capex avoided.
- The value reaches the plate buyer only when buyer and facility owner are the same party (hyperscaler self-build). It does not in colocation or in NVIDIA-centralised procurement.
- Because W45 is already sold as chiller-free in most climates, the strongest headroom story is **hot-climate campuses (design dry-bulb 45-50 C)**, where +7 K removes trim chillers or adiabatic water.

## 5. Channel, Group-A, beachhead

**Group-A list confirmed.** The four suppliers are Jentech, AVC, Cooler Master and Delta (TVBS, Digitimes 18 Mar 2026, Taiwan News). Later reporting says volume Rubin plates come mainly from AVC and Cooler Master. CoolIT is absent.

**Group-A margin of 17-20 %: refuted.** AVC reported gross margin of 24.4 % (2Q25), 29.8 % (1Q26) and **32.6 % (2Q26)**, and says ASIC products carry higher margins than GPU products.

- On a US$300-360 bare plate at 30-33 % GM, gross profit is about US$90-120, and the corrected premium of US$57-83 consumes 50-90 % of it. The licence-only conclusion survives; the stated arithmetic does not.

**The decision-maker for the NVIDIA channel is wrong.** Morgan Stanley flagged that NVIDIA uses a *standardised* cold-plate design under centralised purchasing. A Group-A house builds to NVIDIA's print and cannot insert PRISM on its own initiative. The entry point for rank 2 is NVIDIA's thermal engineering team (reference design), with Group-A only as the factory.

**Micro-channel lid (MCL) and micro-channel cold plate (MLCP) risk is not addressed.**

- JPMorgan (via TechNews) expected the MCL to replace cold plates on dual-die Rubin from 2H26 and to be mainstream in 2027; CLSA says timing is unconfirmed. Jentech leads MCL; AVC and Auras lead MLCP.
- By Feynman (2028) the "lidded PRISM-G on a Rubin Au lid" socket may not exist; the draft carries this only as a "T3B roadmap".

**The hyperscaler beachhead is contested.**

- AVC ships Google TPU v8 and AWS Trainium3 liquid products from 4Q26.
- AWS Trainium3 and AMD MI-series reportedly move to **double-sided plates at more than US$3,000 each** (rumour, UDN). This cuts both ways: a US$60-80 premium is only about 2-3 % of such an assembly, which *helps* the value argument.
- Samples at M12-15 and qualification at M18 miss the 2028 generation's design-ins: realistic volume is **2029, not 2028**.
- Google runs multiple loops to keep cold-plate water very clean (ServeTheHome, Hot Chips 2025), which supports the filtration-gated P-grade at Google specifically.

**Market size.** CoolIT's figure of more than US$11 B TCS in 2026 is unverifiable but plausible: third-party reports say US$4-8 B, yet AVC alone runs at about US$6 B/yr with roughly 30 % from liquid cooling.

**Supplier liability is not addressed.** A leak in a US$4-9 M rack brings indemnity demands; a new entrant needs a liability and insurance plan.

## 6. Budget, staffing, applications

**Budget arithmetic: confirmed.** The lines sum to US$5.48 M, or US$6.58 M with 20 % contingency. That implies US$228k per FTE-year, which is plausible for North America.

**Missing items: US$0.9-2.1 M.**

- Build-B stamping and forging dies, US$0.25-0.6 M. Section 10.3 builds Build B with stamped parts at M6-9, but the tooling sits in the M12-18 budget.
- Confocal scanner, He leak detector and D5470 tester, US$0.3-0.6 M.
- CFD/FEA licences and CT services, US$0.1-0.25 M.
- 25 kW lab fit-out, US$0.1-0.3 M.
- Business development and customer engineering, US$0.15-0.35 M.

**Staffing.** The 14.5 FTE include only one applications FTE and no business development or cost engineering. A co-design beachhead needs 1-2 more.

**Scale-up.** Capex at the contract manufacturer is US$3.7-9 M per 100k/yr: furnaces, skiving, test line, dies and fixtures. Nobody is assigned to fund it, and there is no P&L.

**Applications.** The mission says power electronics comes second. The draft ranks it 6-7, behind CPU/NVSwitch/CPO, and concedes that the PRISM-DC shelf plate has no thermal advantage. A judge called a 1.8 kg copper stack "overkill for 5-30 W/cm² shelves".

- The draft has no PRISM-DC cost, and the 800 VDC shelf market is only US$4-90 M/yr (research estimate).
- SSTs are real but early (OCP SST spec v0.3; Eaton 2 MW; Enphase volume 2028). Only the direct-substrate SST/rectifier module has a thermal case, and it needs a module partner and a cost line.

## 7. Script inspection (`arch/prism_cost.py`)

- Every number is hard-coded: no silver price, die amortisation or capex.
- Yield is a flat percentage on the line sum, not modelled at the braze step.
- The incumbent (US$112, GB-class) and the capacities are constants. PRISM-G (US$120) is in no script.
- The arithmetic is correct (258 / 138 / 100.5 rising to 304 / 159 / 113).

## 8. Fatal issues, required changes, improvements

**Fatal (claim-level, not physics):**

- **F1.** The value case "15-60x / 1.5-6x the premium" is indefensible as published. The GPU-class case inverts at a costed PRISM-G. The 15 kW case is 2-10x, and its +11 K headroom is not like-for-like.
- **F2.** The "+45 % / 8-10 % worse per kW" cost concession is understated. The corrected figures are +50-83 % per plate and about 27-29 % worse per kW. US$120 for PRISM-G is unsupported.

**Required changes:**

1. Re-cost (silver US$60-72/oz, 2-3 furnaces per 100k, 18-25 % yield/overhead at ramp, per-SKU dies): **US$175-225** at 100k, **about US$370-430** at the 10k ramp.
2. Compare against a like-sized 15 kW incumbent (US$116-137); state US$/kW as about 27-29 % worse.
3. Derive PRISM-G bottom-up and gate the GPU-class TCO claim on it.
4. Restate headroom like-for-like as **+7 K at P50 and +2-3 K at P90**. Use US$0.5-1.1 M per K per 100 MW, marked unverified. Add the capture conditions: loop-wide margin, vendor specification and owner-operator.
5. Correct Group-A GM to about 30-33 % and Rubin bare ASP to about US$300-360. Route rank 2 through NVIDIA thermal engineering and MCL/MLCP co-design, not a Group-A licence.
6. Move ASIC volume to 2029. Name the incumbent (AVC already ships TPU v8 and Trainium3).
7. Fix the Build-B tooling contradiction. Fund the missing US$0.9-2.1 M or cut scope explicitly. Add 1-2 business-development or customer-engineering FTE.
8. Either re-rank power electronics to second as the mission asks, or justify the deviation. Cost PRISM-DC.

**Improvements:**

- Silver-thrifty filler: Ag on fin-tip lands only, or Cu-Sn TLP (route C) as the cost-down.
- Make the meter sheet the only per-SKU part (laser-cut or etched, no die) and keep laminations universal, so the 2-3 week zoning claim is true.
- Pitch value on double-sided ASIC assemblies (premium about 2-3 % of ASP) and hot-climate campuses.
- Add a one-page P&L and a CM capex-funding plan.

## Sources

- Cochilco daily LME report, 1 Sep 2026: https://www.cochilco.cl/web/download/1035/septiembre-2026/16810/rueda-01-09-2026.pdf
- Westmetall LME data: https://www.westmetall.com/de/markdaten.php
- Silver spot, Sep 2026: https://naturalresourcestocks.net/silver-price-today-sep-02-2026/ ; https://zerolivenews.onrender.com/news/233102/silver-price-today-wednesday-september-9-2026-silver-prices-hold-in-the-66-range-as-us-ira
- AVC 2Q26 results: https://quartr.com/events/asia-vital-components-co-ltd-3017-q2-2026_F9DdyrDC ; https://money.udn.com/money/story/5607/9762915 ; https://money.udn.com/money/story/5607/9788094
- Group-A suppliers: https://www.taiwannews.com.tw/news/6435018 ; https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html
- MCL timing and the NVIDIA standardised design: https://technews.tw/2025/09/04/nvidia-rubin-gpu-use-microchannel-lid/ ; https://money.udn.com/money/story/5607/9423686 ; https://wantrich.chinatimes.com/news/20260304900004-420101
- Rubin cooling BOM: https://cloudnews.tech/rubin-nvl144-makes-liquid-cooling-more-expensive-e48200-per-rack-17-more-than-nvl72/ ; https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks
- NVIDIA "45 C, no chillers" at CES 2026: https://www.datacenterdynamics.com/en/news/vera-rubin-hot-water-cooling-reveal-triggers-hvac-share-drop
- Heat-rejection cost anchors (system-level only): https://archdesk.com/blog/global-ai-data-center-construction-2026
- Google clean-loop practice: https://www.servethehome.com/googles-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/
- SST landscape: https://www.bayern-innovativ.de/en/emagazine/detail/new-transformer-for-data-centers ; https://pv-magazine-usa.com/?p=20319 ; https://datacenterrichness.substack.com/p/tech-titans-outline-their-vision
- DLC market range: https://axis-intelligence.com/data-center-liquid-cooling-statistics/
- OCP Cold Plate Test Specification v1.0.0 (effective 3 Sep 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
