# Cold-plate patent / IP landscape - freedom-to-operate awareness for the "beat CoolIT 15 kW" programme

*Research angle: which patent families fence off which cold-plate design spaces, what has expired, what is live, and what a new entrant should avoid or claim. High-level engineering awareness only; this is not a legal opinion and no claim charts were built.*
*Compiled 2026-10-13. Benchmark: CoolIT Systems 15 kW Split-Flow coldplate tech brief, June 2026.*

## 0. Method and evidence quality (read first)

- **Web searches run in this sub-task: 0.** The shared WebSearch budget for the workflow turn was exhausted before this angle started, and WebFetch/curl are network-blocked in the container. The task brief asked for 10-30 searches; they could not be run. A follow-up run with search budget should verify every item marked [KB].
- Evidence tiers used below:
  - **[S]** = sourced by a sibling research agent in this workflow with a URL (CoolIT patents and litigation, JetCool/Flex, Mikros/Jabil, Chilldyne/Daikin, Corintis/Microsoft, Fabric8, ICECool press, OCP documents). URLs are repeated in the Sources section.
  - **[KB-H] / [KB-M] / [KB-L]** = author background knowledge (training data to mid-2026), high / medium / low confidence. Patent numbers marked KB-M or KB-L must be checked on USPTO Patent Center or Google Patents before anyone relies on them.
  - **[D]** = derived here (e.g. expiry arithmetic from a known filing date).
- Expiry dates are computed as 20 years from the earliest non-provisional filing date (US applications filed after 8 June 1995), without patent-term adjustment (PTA, typically 0-3 years extra) and ignoring maintenance-fee lapses, which are common. Pre-1995 US patents ran 17 years from grant; all of those are long expired. Continuations inherit the parent's 20-year clock, so a "new" 2025 grant in a 2008 family still dies in 2028.

## 1. Summary

1. **The foundational single-phase geometries are public domain.** Tuckerman-Pease parallel microchannels (1981/1984), Harpole's TRW manifold microchannel cold plate (1992), MIT's alternating counter-flow microchannels (Walpole 1992), Valenzuela/Creare normal-flow laminates (1992, the Mikros root), IBM/Unisys jet-impingement and cross-hatch distribution patents (1985-1991), and Cooligy/Stanford's hot-spot-targeted and multi-level manifold microchannel family (2003-2006 filings) are all expired [KB-H for the 1980s-1992 items; KB-M for Cooligy]. A manifold-fed, zoned, counter-flow, fine-fin copper plate made by skiving + etching + welding sits almost entirely on expired art.
2. **CoolIT's Split-Flow family (US 8,746,330; continuation US 9,603,284; further continuation US 12,495,513) descends from an August 2008 filing and should expire around August 2028 (plus any PTA)** [S for numbers and 2008 filing; D for expiry]. Until then a single central inlet slot over a fin field with flow exiting both ends is CoolIT territory in the US; a multi-slot manifold (N >= 2 inlet slots, interdigitated outlets) is the obvious design-around and is also the better thermal architecture. Non-US counterparts (CA, CN, TW, EP) were not checked.
3. **Asetek's integrated pump-head patents (US 8,240,362 / US 8,245,764, November 2003 Danish priority, PCT 2004) expired in or about November 2024** [KB-H], and the continuation US 10,078,354 was held unpatentable in an IPR brought by CoolIT and affirmed by the Federal Circuit in 2024 [S]. The 2012-2022 Asetek-CoolIT litigation ended in a confidential global settlement in October 2022 after a September 2022 summary judgment of non-infringement on the '362 patent [S]. The "pump in the cold plate" space is therefore essentially open, which is consistent with Asetek having exited HPC in 2021 and describing its data-centre business as dormant [S].
4. **Crowded and live spaces to steer around:** (a) sub-millimetre microjet arrays with local return paths and jet-onto-bare-die lids (JetCool/Flex since Nov 2024, Frore 2023-2025, Microsoft, Nvidia) [S/KB-M]; (b) two-phase dielectric direct-to-chip evaporators and their fluids (ZutaCore, Accelsius with Nokia Bell Labs IP, Nvidia, Wiwynn, IBM ICECool, 3M/Chemours/Honeywell fluid patents) [KB-M]; (c) negative-pressure system claims (Chilldyne, now Daikin Applied) [S/KB-M]; (d) in-silicon / embedded microfluidics (Corintis, Microsoft, TSMC, IBM, Georgia Tech, Lockheed) [S/KB-M]; (e) micro-channel lids and direct-to-die packaging (Intel, Nvidia, Jentech, TSMC, AMD) [KB-M]; (f) Nvidia's 2020-2026 "intelligent"/sensor-controlled cold plate and rack-cooling filings, which are mostly control-system claims rather than passive geometry [KB-M].
5. **Ownership has consolidated into litigation-capable parents:** Ecolab owns CoolIT (US$4.75 B, closed July 2026; CoolIT states 150+ liquid-cooling patents) [S]; Flex owns JetCool (Nov 2024) [S]; Jabil owns Mikros (Oct 2024) [S]; Daikin Applied owns Chilldyne (Nov 2025) [S]; Eaton is acquiring Boyd Thermal (announced Oct 2025) [KB-M]; Vertiv owns CoolTera and, via Emerson Network Power, probably the legacy Cooligy portfolio [KB-L]. Expect these owners to assert or cross-license rather than ignore a new entrant that takes Nvidia or hyperscaler sockets.
6. **What to claim ourselves (provisionals before any disclosure):** the specific skive-core + photo-etched manifold laminate + laser/FSW lid stack; power-map-programmed skived fin pitch (prior art: Cooligy US 7,104,312, expired, so claims must be narrower than "denser fins over hot spots"); zoned parallel feeds for GPU vs HBM regions with fresh inlet fluid to each zone; negative-pressure-compatible low-dP plate with vacuum-stable body; stepped bare-die compliance for HBM/logic height differences (watch CoolIT's "compliant member" family US 11,725,886 / US 12,188,733); and the dual-use GPU / SiC-module variant with a direct-cooled baseplate interface.

## 2. The benchmark's own IP position (CoolIT Systems, now Ecolab)

| Item | Detail | Status / expiry | Relevance to us | Source / confidence |
|---|---|---|---|---|
| US 8,746,330 B2 "Fluid heat exchanger configured to provide a split flow" | Inventor Geoff Sean Lyon; application 12/189,476 filed Aug 2008 (provisional Aug 2007); granted 10 Jun 2014. Coolant enters a slot over the middle of the fin array, splits, exits at both ends; halves flow length and per-channel flow | Live; expiry ~Aug 2028 + PTA [D] | Core Split-Flow claim. Single central inlet over a fin field = CoolIT territory until 2028 | [S] patents.google.com/patent/US8746330B2 ; insidehpc.com 2014 ; coolitsystems.com/patents |
| US 9,603,284 B2 (continuation, app 14/283,163) | Filed May 2014, granted Mar 2017 | Live; same ~2028 clock [D] | Broader/different claim wording on the same disclosure; check independent claims for "at least one inlet" language | [S] patents.google.com/patent/US9603284B2 |
| US 12,495,513 "Fluid heat exchanger configured to provide a split flow" | Further continuation, granted ~late 2025 | Live; same ~2028 clock if it claims priority to 2008 [D]; if it is a new 2020s filing the clock runs to the 2040s - **must verify** | Could carry claims tuned to current products (e.g. multi-zone split flow) | [S] image-ppubs.uspto.gov ... 12495513 ; [D] |
| US 9,057,567 / US 9,055,697 "Fluid heat exchange systems"; US 9,052,252 (leak detection) | 2015 grants; CoolIT's "50th patent" announcement | Filed ~2011-2012 -> expiry ~2031-2032 [KB-M] | Microchannel coldplate + system claims; leak detection in manifolds/plates | [S] insidehpc.com 2015 ; [KB-M] |
| US 11,725,886 -> US 12,188,733 "Modular fluid heat exchange systems" with a compliant member | US 12,188,733 granted 7 Jan 2025 | Filed ~2020-2021 -> expiry ~2040-2041 [KB-M] | Compliance between heat exchanger and housing; relevant to any stepped-height bare-die or floating-core mounting we design | [S] patentsgazette.uspto.gov ... US12188733 ; content [KB-L] |
| US 12,101,906 "Fluid heat exchanger" | Granted Sep 2024 | Unknown priority; could be 2030s-2040s | Unknown claim scope - review | [S] number only |
| "Rack DCLC" / CDU / manifold families (e.g. modular heat-transfer systems, CDU with redundant pumps, manifold sensors) | 2012-2024 filings | 2032-2044 | System-level; not plate geometry. Relevant only if we build manifolds/CDUs | [KB-L]; numbers not verified |
| OMNI all-metal unibody (FSW/laser-joined, no braze) | Launched May 2024; a 2026 factory tour attributes it to friction stir welding | Any 2023-2024 applications would run to 2043-2044 and may still be unpublished at first search | FSW of copper itself is old art (TWI's 1991 FSW patent expired ~2011-2015) [KB-H]; CoolIT could only claim specific plate constructions (lip geometry, weld-path-around-ports, etc.) | [S] storagereview OMNI ; DCF tour ; [KB-M] |
| Portfolio size | "over 120" (site) -> "150+" liquid-cooling patents (blog 28 Jul 2026) | - | Dense; expect families on quick disconnects, manifolds, CDU control, leak detection | [S] coolitsystems.com design-engineering ; blog Jul 2026 |
| Litigation posture | Defendant/counter-claimant vs Asetek 2012-2022; won summary judgment 2022; invalidated Asetek '354 by IPR (Fed. Cir. 2024); settled globally Oct 2022 | - | CoolIT litigates competently and uses IPRs. Ecolab adds balance-sheet | [S] DCD ; insideHPC 2022 ; inderes.fi |

**Trade secrets.** The 15 kW brief discloses no fin geometry, footprint, dP, or TIM; "industry-leading internal geometries" is a trade secret, not a patent. Do not recruit CoolIT/Ecolab engineers into roles where their knowledge of those geometries would be used; document independent development (lab notebooks, CFD history) from day one.

**Non-US counterparts.** CoolIT manufactures in Calgary, China and Vietnam [S] and sells into Taiwan ODM supply chains; it very likely has CA/CN/TW/EP Split-Flow counterparts. Not checked. If we manufacture in Taiwan/China/Vietnam, FTO must be run in those jurisdictions, not only the US.

## 3. Term primer (why "expired" needs care)

| Rule | Consequence for this landscape |
|---|---|
| US patents filed after 8 Jun 1995: 20 years from earliest non-provisional filing; continuations/divisionals inherit that date; PTA can add months to ~3 years | CoolIT 2008 family -> ~2028; Asetek 2004 PCT family -> ~2024; Cooligy 2003-2005 -> 2023-2025 |
| US patents filed before 8 Jun 1995: longer of 17 years from grant or 20 years from filing | Tuckerman-Pease (1984 grant) expired ~2001; Harpole (1992) ~2009-2010; Walpole (1992) ~2009-2011; Valenzuela (1992) ~2009-2011; IBM cross-hatch (1991) ~2008-2010 |
| Maintenance fees due at 3.5 / 7.5 / 11.5 years; many corporate patents lapse early | IBM in particular prunes aggressively; many 2005-2015 IBM cold-plate patents may already be lapsed. Check "expired - fee related" status |
| Terminal disclaimers tie continuation expiry to the parent | US 12,495,513, if a true continuation of 8,746,330, cannot outlive Aug 2028 + PTA |
| Expired = free to practise the claims, but the disclosure is also prior art against **our** claims | Cooligy's expired hot-spot-targeting patents prevent us from claiming "denser fins over hot spots" broadly; we must claim the specific manufacturable implementation |

## 4. Landscape by player and design space

### 4.1 Foundational single-phase families (expired - the open ground)

| Family | Number / title | Assignee, dates | Status | What it covers | Conf. |
|---|---|---|---|---|---|
| Parallel microchannel heat sink | US 4,450,472 "Method and means for improved heat removal in compact semiconductor integrated circuits" | Stanford (Tuckerman, Pease); filed Mar 1981, granted May 1984 | Expired ~2001 | Etched parallel microchannels in/under the die; 790 W/cm2 demo (EDL 1981) | KB-H |
| Manifold microchannel (MMC) cold plate | US 5,088,005 "Cold plate for cooling electronics" | TRW (G. Harpole); filed May 1990, granted Feb 1992 | Expired ~2009-2010 | Manifold layer feeding many short channel segments in parallel; the MMC concept (Harpole & Eninger, SEMI-THERM 1991) | KB-M/H |
| Alternating counter-flow microchannels | US 5,099,910 "Microchannel heat sink with alternating flow directions" | MIT Lincoln Lab (Walpole, Missaggia); filed Jan 1991, granted Mar 1992 | Expired ~2009-2011 | Adjacent channels flow in opposite directions to flatten the streamwise temperature ramp | KB-M |
| Normal-flow laminate heat exchanger | US 5,145,001 "High heat flux compact heat exchanger" | Creare Inc. (J. Valenzuela), filed 1991, granted Sep 1992 - the root of Mikros "Normal Flow" | Expired ~2009-2011 | Stacked etched laminates; fluid flows normal to the heated surface through short passages; >1 kW/cm2 class | KB-M |
| Jet impingement on chips | e.g. US 4,750,086 "Apparatus for cooling integrated circuit chips with forced coolant jet" (Unisys, 1988); IBM 1980s TCM/jet work; US 5,016,090 "Cross-hatch flow distribution and applications thereof" (IBM, Galyon et al., 1991) | 1985-1991 | All expired by ~2008-2010 | Liquid jets normal to chip; cross-hatch manifold distributing fluid to jets/channels with local returns | KB-M (numbers), KB-H (that 1980s jet art is expired) |
| Hot-spot-targeted flexible fluid delivery | US 7,104,312 "Method and apparatus for flexible fluid delivery for cooling desired hot spots in a heat producing device" | Cooligy (Goodson, Kenny, Zhou, Upadhya et al.); filed ~2003-2004, granted Sep 2006 | Expired ~2023-2024 (20 y from filing) | Manifold routing more coolant / finer channels to hot spots; non-uniform channel density matched to power map | KB-M |
| Multi-level / interwoven manifold microchannel | US 7,156,159 "Multi-level microchannel heat exchangers"; US 7,000,684 "...efficient vertical fluid delivery..."; related US 7,188,662, US 7,021,369 (hermetic loop) | Cooligy; filed 2003-2005; granted 2006-2007; Cooligy bought by Emerson 2005; likely with Vertiv since 2016 | Expired or expiring 2023-2025; verify each | 3-D manifold above a microchannel/pin field with vertical inlet/outlet distribution - the modern HMMC layout | KB-M (numbers), KB-L (current owner) |
| Friction stir welding | TWI "Improvements relating to friction welding" (GB priority Dec 1991; US 5,460,317) | TWI | Expired ~2011-2015 worldwide | Process; copper FSW parameters are know-how, not patent | KB-H |

**Read-across:** a copper plate with (i) skived fine fins, (ii) a multi-slot manifold layer feeding 1-3 mm flow segments, (iii) alternating inlet/outlet slots (counter-flow), (iv) zoned feeds, (v) FSW/laser lid, uses nothing but expired foundational art at the concept level. Residual risk sits only in narrow modern implementations (section 4.3-4.6).

### 4.2 Integrated pump-in-cold-plate (Asetek) and the Asetek v. CoolIT history

| Item | Detail | Status | Conf. |
|---|---|---|---|
| US 8,240,362 and US 8,245,764 "Cooling system for a computer system" (A. Eriksen) | Danish priority Nov 2003, PCT Nov 2004, granted Aug 2012; dual-chamber pump head integrated with the cold plate and reservoir (the AIO architecture) | **Expired ~Nov 2024** (20 y from PCT) [D]; check PTA | KB-H |
| US 10,078,354 (continuation) | Asserted in the 2019 suit; CoolIT IPR -> PTAB unpatentable -> Fed. Cir. affirmed 2024 | Dead | [S] DCD |
| Asetek v. CoolIT I (N.D. Cal., filed 2012) | Resolved ~2015; DCD reports ~US$1.9 M damages | Closed | [S] DCD (details KB-L) |
| Asetek v. CoolIT II (N.D. Cal., filed 2019) | CoolIT counter-asserted its own plate/system patents; Sept 2022 summary judgment of non-infringement on '362; Oct 2022 confidential global settlement | Closed | [S] DCD ; insideHPC ; inderes.fi |
| Asetek v. CMI (Cooler Master) and v. Corsair | Fed. Cir. 2016 affirmed infringement/injunction vs CMI; Corsair settled | Family now expired; moot for new products | KB-M |
| Asetek status | Exited HPC Sept 2021; DC assets "dormant"; 2025 indication of interest from an unnamed buyer | Portfolio possibly for sale cheaply | [S] hpcwire 2021 ; overclock3d |

**Read-across:** For data-centre plates the pump lives in the CDU, so this family never mattered much to us; but tray-level pump-assisted or "pumped cold plate" ideas are now free of Asetek's claims. CoolIT's own 2010s system patents (pumps in CDU/rack, redundant pump control) remain live and are the ones to review if we ever build a CDU.

### 4.3 Microjet impingement (crowded, live)

| Player | What is claimed / known | Term window | Conf. |
|---|---|---|---|
| JetCool Technologies (MIT Lincoln Lab spin-out, founded 2019; **acquired by Flex 14 Nov 2024**) | Sub-mm microjet arrays impinging on the lid (SmartPlate) or directly on die (SmartLid "liquid-to-die"); hot-spot-aimed jets; local return paths; 20-40 % lower R vs microchannel (vendor), 25 % incl. TIM (vendor-reported third party). Families stem from Lincoln Lab 2017-2019 filings licensed to JetCool plus JetCool's own 2020-2024 filings | ~2037-2044 | [S] jetcool.com ; investors.flex.com ; patent numbers [KB-L], none verified |
| Frore Systems LiquidJet (launched 14 Oct 2025) | Metal-wafer, semiconductor-process jet cold plate; claims 600 W/cm2 hot-spot flux; filings 2023-2025 | ~2043-2045 | [S] froresystems.com ; [KB-L] |
| Microsoft | Jet impingement on bare die / lidless packages, immersion and two-phase families, 2020-2024 filings | ~2040-2044 | KB-M |
| Nvidia | Jet/hybrid cold plates within the Heydari-era filings (2020-2023) | ~2040-2043 | KB-M |
| Academic | Purdue (Garimella/Weibel: hybrid jet-microchannel, HMMC), Stanford (Goodson), Georgia Tech (Bakir) | 2033-2040 for granted ones | KB-L |

**Read-across:** The sibling physics model treats jet cores as an *alternative* to the manifold-microchannel core, not an add-on. If we keep to slot-fed manifold microchannels (slots feed fins, no free jets onto a plain wall, no discrete orifice array with per-jet returns), we stay outside the JetCool/Frore claim language as generally understood. A "jet-enhanced manifold" (orifices in the manifold floor impinging on fin roots) edges toward JetCool and the PKU 2025 Nature Electronics work and needs a claim review before adoption.

### 4.4 Two-phase direct-to-chip dielectric (crowded, live; avoid unless licensing)

| Player | Notes | Term window | Conf. |
|---|---|---|---|
| ZutaCore (founded 2016) | Waterless two-phase direct-on-chip evaporator with enhanced nucleation surface; 0.3 LPM/kW; 2,800 W certified, "4 kW+" claimed; patents 2017-2024 | ~2037-2044 | [S] zutacore.com ; eenewseurope ; [KB-M] |
| Accelsius (Innventure, 2022) | NeuCool pumped-refrigerant two-phase; IP licensed from Nokia Bell Labs; 4,500 W per socket TTV (Apr 2025); independent-ish 2026 benchmark -9 C Tj vs single-phase | Bell Labs families ~2035-2042; Accelsius own 2042+ | [S] businesswire ; DCD ; Bell Labs origin [KB-M] |
| Wiwynn, Nvidia, IBM ICECool (R1234ze embedded two-phase), 3M/Chemours/Honeywell (fluid formulations, e.g. R-1233zd(E) blends) | Fluid patents are a separate FTO layer | 2030s-2040s | KB-M |

### 4.5 Negative-pressure single-phase (system claims live)

Chilldyne (founder Steve Harrington; **acquired by Daikin Applied 4 Nov 2025**) holds families filed ~2012-2016 on vacuum-side CDUs, air-tolerant plates/lines and leak-proof operation (expiry ~2032-2036) [S] daikinapplied.com ; storagereview ; numbers [KB-L]. A low-dP plate that merely *works* under negative pressure does not practise a vacuum-CDU claim; building or bundling the vacuum CDU would need review. Keep the plate body vacuum-stable (no collapse, no O-ring unseating) and advertise "negative-pressure compatible" without claiming the system.

### 4.6 Embedded / in-silicon microfluidics (2028+; crowded; not for an entrant)

Corintis (EPFL spin-off; US$24 M Sep 2025; Microsoft partnership; "up to 3x" vs cold plates on a prototype) [S] ; Microsoft; TSMC (ECTC 2025 direct-to-silicon on CoWoS, >2.6 kW) [S]; IBM ICECool (Schultz/Colgan, 2013-2017); Lockheed Martin (ICECool, 1 kW/cm2 with 30 kW/cm2 hot spots) [S] eepower ; Georgia Tech (Bakir, monolithic microfluidic Si). Expiry 2033-2045. Requires the silicon vendor to etch the die; irrelevant to a 2026-2028 copper plate, but our product should be "direct-to-die ready" (bare-die compliant variant), which brushes section 4.7 instead.

### 4.7 Micro-channel lids, direct-to-die and bare-die compliance (emerging thicket)

| Player | Notes | Conf. |
|---|---|---|
| Intel | "Liquid-cooled integrated heat spreader" / microchannel IHS / jet-in-lid families, 2015-2023 filings (expiry 2035-2043) | KB-M |
| Nvidia | 2023-2026 filings on microchannel lids, two-phase lids, "intelligent cold plates" with sensors/flow controllers, hybrid liquid/air trays, in-rack CDUs; dozens of Heydari et al. applications 2020-2023 | KB-M |
| Jentech (3653.TW) | Lid/IHS incumbent and Rubin Group-A plate supplier; TW/US filings on micro-channel lids | [S] TVBS/Digitimes (Group-A) ; patents [KB-L] |
| TSMC / AMD | Package-level direct-to-silicon and lid designs | KB-M |
| Google | Bare-die TPU plates since TPU v4, split-flow found better than straight-through (Hot Chips 2025); Google's plate patents not reviewed; Deschutes CDU contributed to OCP (open licence) | [S] competitors-singlephase.md ; [KB-L] |
| CoolIT | "direct-to-die and micro-channel lids" are stated roadmap (15 kW brief); compliant-member family US 11,725,886 / 12,188,733 | [S] brief ; gazette |

**Read-across:** Our lidded-package plate is clear. A bare-die variant should claim the specific stepped-height / compliant interface, and must be checked against CoolIT's compliant-member claims and Intel/Nvidia lid claims. Nvidia's "intelligent" claims mostly require sensors + controllers + flow actuators in the plate or tray; a passive plate does not read on them.

### 4.8 Laminate "normal flow" and diffusion-bonded cores (Mikros / Jabil)

Root patent US 5,145,001 expired [KB-M]. Mikros filed continuing families through the 2000s-2010s on normal-flow laminate designs and bonded-laminate manufacturing (expiry roughly 2025-2035) [KB-L], and Jabil owns them since 1 Oct 2024 [S] businesswire. Mikros claims 0.02 cm2-K/W core and >1 kW/cm2 at 3 psi [S] mikrostechnologies.com. If we offer an etched + diffusion-bonded premium SKU (sibling manufacturing option 3), run FTO on live Mikros families; a skived core with an etched manifold layer (option 1) is structurally different (fins are skived, flow is parallel to the base inside the fin field) and is the lower-risk route.

### 4.9 Power electronics (SiC) cooling

Danfoss ShowerPower (Olesen; original ~2003-2005 filings, expired or expiring ~2023-2025; ShowerPower 3D 2019+ filings live to ~2039-2041) [KB-M/L]; direct-cooled pin-fin baseplates are owned by module vendors (Infineon, Wolfspeed, ST, Danfoss) and are old art; Boyd HybridKIT DSC plate 0.026 K/W / 12.5 kPa at 10 LPM [S] boydcorp.com. Purdue/Garimella embedded 3-D manifold on SiC (IJHMT 2019) may be patented by Purdue Research Foundation [KB-L]. An SiC-converter SKU using our manifold core against a flat module baseplate is low-risk; a module-integrated (wetted baseplate) version must respect the module vendor's own designs and the Tier-1's housing IP.

### 4.10 Taiwanese volume makers (AVC, Auras, Cooler Master, Delta, Jentech, Nidec)

These hold many TW utility models and narrow US/CN patents on skived plates, sealed D2C modules, and QD/manifold details (2018-2026) [KB-M]. Narrow claims; risk is low but non-zero for specific features (e.g. a particular lid-port-seal construction). Check at detailed-design stage.

### 4.11 Additive / ECAM process patents (Fabric8Labs)

Fabric8Labs' ECAM patents (2016-2024) cover the electrochemical printing process and tooling, not plate geometry [KB-M]; the UIUC topology-optimised plate work (-32 % R / -68 % dP vs pin fins) is academic [S] manufacturing-cost.md. Since our plate is skived/etched/welded, these are irrelevant unless we buy ECAM cores.

## 5. Design-space heat map

| Design space | Foundational art | Live blocking risk | Verdict for our plate |
|---|---|---|---|
| Straight parallel skived microchannels, lidded package | Expired (Tuckerman-Pease) | Low (TW utility models) | Open |
| Single central-slot split flow | CoolIT 2008 family | **Medium until ~Aug 2028 (US)**; non-US unknown | Avoid single-slot; use >= 2 slots / interdigitated manifold; re-check Aug 2028 |
| Manifold microchannel (multi-slot, short flow length) | Expired (Harpole, Cooligy, Walpole) | Low-medium (Purdue HMMC, IBM Zurich Escher 2009-2011, Corintis 2022+, Nvidia 2021+) | Open with a claim review of 4-6 modern families |
| Counter-flow / alternating slots | Expired (Walpole 1992) | Low | Open |
| Power-map-tailored fin/channel density | Expired (Cooligy 7,104,312) | Medium for "AI-generated / bio-inspired" topologies (Corintis, Fabric8) | Open for skived pitch modulation; claim the manufacturing-specific version |
| Zoned parallel feeds (GPU vs HBM with fresh inlet fluid) | Old art in multi-chip modules (IBM TCM era) | Low-medium (Nvidia 2021+ hybrid-zone plates; CoolIT 12,495,513 unknown) | Open pending review of the two named families |
| Jet impingement arrays, jet-onto-die lids | Expired 1980s roots | **High** (JetCool/Flex, Frore, Microsoft, Nvidia) | Avoid as a core; license if ever needed |
| Integrated pump in plate | Expired (Asetek Nov 2024) | Low (CoolIT system claims only) | Open, not needed |
| Two-phase dielectric direct-to-chip | IBM/ICECool, Bell Labs | **High** (ZutaCore, Accelsius, Nvidia, fluids) | Avoid; second-SKU only via licence |
| Negative-pressure systems | Chilldyne 2012-2016 | Medium (system claims, Daikin) | Plate: open; CDU: review |
| In-silicon microfluidics | Tuckerman-Pease expired | High and silicon-vendor-gated | Not our business |
| Micro-channel lids / direct-to-die compliance | Intel 2015+ | Medium-high (Intel, Nvidia, Jentech, TSMC, CoolIT compliant member) | Bare-die variant: claim-review before launch |
| All-metal FSW/laser unibody | FSW expired | Low-medium (possible CoolIT OMNI applications 2023-24, unpublished at first) | Open; monitor CoolIT publications 2025-2026 |
| Leak detection in plate / manifold | - | Medium (CoolIT 9,052,252 to ~2032; Nvidia; Supermicro) | Use tray-level sensors per OCP ACS white paper; avoid in-plate sensing claims |
| Sensors + flow control in plate ("intelligent cold plate") | - | High (Nvidia 2020-2026) | Keep the plate passive |

## 6. What a new entrant should do (engineering-level FTO plan, not legal advice)

**Avoid / design around**
1. Single central inlet slot with bidirectional exit over one fin field (CoolIT Split-Flow) until the family's expiry is confirmed (expected ~Aug 2028 + PTA, US). Use two or more inlet slots with interdigitated outlet slots; this is the manifold-microchannel architecture the physics model already prefers (sibling: mean dT ~24 K vs 34.4 K; dP ~6 kPa).
2. Discrete orifice-array microjets with per-jet returns and any "liquid-to-die" jet lid (JetCool/Flex, Frore, Microsoft).
3. Two-phase dielectric evaporators and proprietary fluid blends.
4. Active elements in the plate (sensors, valves, controllers) that read on Nvidia's intelligent-cold-plate filings.
5. In-plate leak sensing (CoolIT 9,052,252 family) - use tray/rack sensing instead.

**Verify before freezing the design (ordered by urgency)**
1. Claim 1 of US 8,746,330, US 9,603,284, US 12,495,513 and the priority chain of 12,495,513; CA/CN/TW/EP counterparts; PTA on 8,746,330.
2. CoolIT US 12,101,906 and US 11,725,886 / 12,188,733 (compliant member) claim scope.
3. Cooligy 7,104,312 / 7,156,159 / 7,000,684 expiry and current assignee (Vertiv?) - confirm expired.
4. Purdue Research Foundation HMMC patents (Garimella/Weibel/Drummond, ~2016-2019 filings) and IBM Zurich (Escher/Michel "ultra-thin heat sink", 2009-2011) - the two modern MMC families closest to our core.
5. Corintis EP/WO/US filings (2022-2025) on heat-map-matched channel topologies.
6. Nvidia 2021-2026 cold-plate grants (hybrid-zone plates, microchannel lids).
7. Mikros/Jabil live laminate families - only if the diffusion-bonded SKU proceeds.
8. Chilldyne/Daikin system claims - only if a vacuum CDU is bundled.
9. Taiwanese utility models (AVC, Auras, Cooler Master, Delta, Jentech) at detailed-design review.

**Claim (file US provisionals before any customer disclosure, OCP contribution or conference talk)**
- The manufacturing stack: skived OFE copper fin core (0.1 mm fins, 0.1-0.15 mm gaps, 1.5-2 mm tall), photochemically etched 0.2-0.3 mm copper manifold laminate(s) forming tapered interdigitated inlet/outlet slots, laser- or FSW-joined lid, Ni plating applied pre-join. Claim the combination and the taper/slot-pitch rules that give <= +/-X % per-segment flow.
- Zoned feeds: separate parallel branches for GPU and HBM regions, each fed with inlet-temperature fluid, with orifice-sized flow balancing; claim the branch-ratio rule tied to the power map.
- Power-map-programmed skived pitch (variable fin pitch produced by skiving-stroke control) - claim the process and the resulting monotonic pitch profile, not "denser fins over hot spots" (Cooligy prior art).
- Negative-pressure-compatible construction (vacuum-stable body, captive seals, plate dP <= 30-50 kPa at rated flow).
- Stepped bare-die interface (two or three contact heights, +/-200 um compliance) and the dual-use SiC-module interface.
- Test/qualification method claims are weak and conflict with OCP's open spec; publish in OCP format instead for credibility (CoolIT co-authored the OCP Cold Plate Test Specification V1.0.0, Oct 2026 [S]).

**Defensive publication.** For variants we will not patent (e.g. specific slot pitches, counter-flow orderings), publish a short technical disclosure so nobody else can patent them against us.

**Jurisdictions and budget [KB-M].** FTO searches in US, CN, TW, EP (DE), JP, KR; manufacturing in Taiwan/Vietnam adds TW/VN. Rough cost: professional FTO search + opinion on ~10 families US$40-100 k; US provisional + PCT per family US$15-40 k through national phase. Timeline: landscape search 4-6 weeks; opinion 4-8 weeks; file provisionals within 1-2 months of design freeze.

**Standards and open IP.** OCP contributions (Google Deschutes CDU, OCP cold-plate test and PG25 specs, UQD v2.0.0) are licensed under OCP's contribution agreements [S] opencompute.org; using the test specs and UQD interface is IP-safe and improves credibility against CoolIT's undisclosed dP.

## 7. Numbers that matter for the IP timeline

| Item | Value | Source | Conf. |
|---|---|---|---|
| CoolIT Split-Flow earliest non-provisional filing | Aug 2008 (app 12/189,476) | [S] patents.google.com US8746330B2 | High |
| Expected US expiry of Split-Flow family | ~Aug 2028 + PTA | [D] | Medium (PTA unknown; 12,495,513 chain unverified) |
| Asetek '362/'764 priority / expiry | Nov 2003 DK; PCT Nov 2004; expired ~Nov 2024 | [KB-H], [D] | High-medium |
| Asetek v. CoolIT II summary judgment / settlement | Sept 2022 / Oct 2022 | [S] DCD, insideHPC | High |
| Fed. Cir. affirmance of unpatentability, Asetek US 10,078,354 | 2024 | [S] DCD | High |
| CoolIT patent count | >120 (site) -> 150+ (Jul 2026 blog) | [S] | High (vendor) |
| Ecolab-CoolIT | US$4.75 B; closed ~2 Jul 2026 | [S] businesswire | High |
| Flex-JetCool | 14 Nov 2024 | [S] investors.flex.com | High |
| Jabil-Mikros | 1 Oct 2024 | [S] businesswire | High |
| Daikin Applied-Chilldyne | 4 Nov 2025 | [S] daikinapplied.com | High |
| Corintis funding | US$24 M, Sep 2025 | [S] yolegroup | High |
| Tuckerman-Pease patent / expiry | US 4,450,472; granted 1984; expired ~2001 | [KB-H] | High |
| Harpole MMC patent / expiry | US 5,088,005; 1992; expired ~2009-10 | [KB-M] | Medium |
| Walpole alternating-flow / expiry | US 5,099,910; 1992; expired ~2009-11 | [KB-M] | Medium |
| Valenzuela normal-flow / expiry | US 5,145,001; 1992; expired ~2009-11 | [KB-M] | Medium |
| Cooligy hot-spot family / expiry | US 7,104,312 (2006 grant); expired ~2023-24 | [KB-M] | Medium |
| FTO search + opinion cost (10 families) | US$40-100 k | [KB-M] | Medium |

## 8. Gaps / unknowns

- No live searches were possible; every [KB] patent number, date and assignee above is unverified in this session. Priority verification list is in section 6.
- Whether US 12,495,513 is a true continuation of the 2008 Split-Flow family (dies 2028) or a new filing (lives to 2040s), and what its independent claims recite (e.g. multiple slots, zoned split flow).
- Existence and status of CoolIT CA/CN/TW/EP counterparts of Split-Flow, and any OMNI (unibody welded plate) applications filed 2023-2024.
- JetCool/Flex, Frore, ZutaCore, Chilldyne, Corintis, Purdue, IBM Zurich and Nvidia patent numbers and independent-claim scope - only the design-space characterisation is given.
- Current owner of the Cooligy portfolio (Emerson -> Vertiv assumed) and whether any Cooligy continuation filed after 2005 is still live.
- Mikros/Jabil live families after the 1992 root patent.
- Google's split-flow usage (Hot Chips 2025) - whether it licenses CoolIT, designs around, or holds its own patents; Google's TPU plate patents were not reviewed.
- Nvidia's contractual IP terms for Group-A plate suppliers (NDA) and whether Nvidia requires licences/indemnities from plate vendors.
- Standard-essential or OCP-licensed IP on UQD/manifold interfaces beyond the OCP contribution licence.
- Trade-secret exposure through Taiwanese CM partners who also build CoolIT or Group-A plates.

## 9. Sources

Sibling-sourced URLs (retrieved by other agents in this workflow; this agent ran no searches):

- CoolIT Split-Flow patents: https://patents.google.com/patent/US8746330B2/en ; https://patents.google.com/patent/US9603284B2/en ; https://patents.justia.com/patent/8746330 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9603284 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12495513 ; https://insidehpc.com/2014/06/coolit-systems-patents-split-flow-heat-exchanger/
- CoolIT patent marking / portfolio: https://www.coolitsystems.com/patents/ ; https://www.coolitsystems.com/capabilities/design-engineering/ ; https://insidehpc.com/2015/07/coolit-systems-lands-new-patents-for-liquid-cooling/ ; https://patentsgazette.uspto.gov/week01/OG/html/1530-1/US12188733-20250107.html ; https://www.coolitsystems.com/resources/news/coolit-behind-the-worlds-most-advanced-ai-coldplates/
- CoolIT Split-Flow and OMNI briefs: https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf ; https://www.coolitsystems.com/coldplate-technology/ ; https://www.coolitsystems.com/omni/ ; https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled ; https://www.datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale
- Asetek v. CoolIT litigation: https://www.datacenterdynamics.com/en/news/coolit-wins-patent-suit-brought-by-danish-cooling-firm-asetek/ ; https://insidehpc.com/2022/10/coolit-system-district-court-rejects-asetek-patent-claims/ ; https://www.inderes.fi/releases/asetek-litigation-update
- Asetek status: https://www.hpcwire.com/2021/09/22/asetek-announces-it-is-exiting-hpc/ ; https://overclock3d.net/news/cases_cooling/asetek-may-sell-its-liquid-cooling-business-to-an-unknown-buyer/
- Ecolab-CoolIT: https://www.businesswire.com/news/home/20260319353197/en/Ecolab-to-Acquire-CoolIT-Systems ; https://www.coolitsystems.com/resources/news/ecolab-to-acquire-coolit-systems/
- JetCool / Flex: https://investors.flex.com/news/news-details/2024/Flex-Acquires-JetCool-to-Expand-Data-Center-and-Power-Portfolio/ ; https://jetcool.com/data-center-liquid-cooling/ ; https://jetcool.com/post/third-party-testing-data/ ; https://jetcool.com/post/understanding-direct-to-chip-liquid-cooling-approaches-and-performance-tradeoffs/
- Frore LiquidJet: https://www.froresystems.com/media-room/frore-systems-introduces-liquidjet-redefining-coldplates-for-ai-data-centers ; https://www.froresystems.com/products/liquidjet-dlc-coldplate
- Mikros / Jabil: https://www.businesswire.com/news/home/20241003396998/en/Jabil-Acquires-Mikros-Technologies-to-Support-Demand-for-Liquid-Cooling-in-AI-Data-Centers ; https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/ ; https://www.mikrostechnologies.com/home/overview/
- ZutaCore: https://zutacore.com/solutions ; https://zutacore.com/faq ; https://www.eenewseurope.com/en/pegatron-certifies-zutacore-two-phase-direct-to-chip-liquid-cooling/
- Accelsius: https://www.datacenterdynamics.com/en/news/accelsius-tests-ability-to-cool-4500-watt-chips ; https://www.businesswire.com/news/home/20260721991081/en/
- Chilldyne / Daikin: https://www.daikinapplied.com/news/news/daikin-applied-expands-data-center-offering-with-acquisition-of-chilldyne ; https://www.storagereview.com/review/high-performance-leak-free-liquid-cooling-chilldynes-cdu-and-cold-plates-in-action
- Corintis / Microsoft: https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/ ; https://www.hpcwire.com/2025/09/25/microfluidics-offers-3x-better-cooling-than-cold-plates-microsoft-says/ ; https://www.yolegroup.com/industry-news/corintis-raises-24m-to-target-the-next-ai-bottleneck-and-collaborates-with-microsoft-for-chip-cooling-breakthrough/ ; https://sacra.com/research/corintis
- DARPA ICECool: https://eepower.com/news/cool-technology-turns-down-the-heat-on-high-tech-equipment/ ; https://www.electronics-cooling.com/?p=20264
- Fabric8Labs / ECAM: https://www.fabric8labs.com/ecam-vs-legacy-liquid-cooling-cold-plates/ ; https://www.d2pmagazine.com/2026/08/14/fabric8labs-wiwynn-collaborating-to-develop-nexgen-3d-printed-cold-plates-for-ai-data-centers/
- Boyd: https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf ; https://www.boydcorp.com/boyds-collaboration-with-nvidia.html
- Nvidia Rubin plate procurement (Group-A): https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html ; lids: https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/ ; https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html
- OCP open specifications: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf ; https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf ; https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf ; https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1
- Split-flow independent analysis: https://par.nsf.gov/biblio/10341820 (Kisitu & Ortega, InterPACK 2021)
- Literature roots (not retrieved; bibliographic): Tuckerman & Pease, IEEE EDL-2(5) 1981, doi:10.1109/EDL.1981.25367 ; Harpole & Eninger, SEMI-THERM 1991 ; Copeland, Behnia, Nakayama, IEEE Trans. CPMT-A 20(2) 1997 ; Escher et al., ASME J. Heat Transfer 132, 081402 (2010) ; Drummond et al., IJHMT 117 (2018) ; PKU jet-enhanced manifold microchannels, Nature Electronics 8 (2025) https://www.nature.com/articles/s41928-025-01449-4

Background-knowledge items with no URL in this session (verify on Google Patents / USPTO Patent Center): US 4,450,472 ; US 5,088,005 ; US 5,099,910 ; US 5,145,001 ; US 5,016,090 ; US 4,750,086 ; US 7,104,312 ; US 7,156,159 ; US 7,000,684 ; US 7,021,369 ; US 5,460,317 ; US 8,240,362 ; US 8,245,764 ; US 10,078,354 ; Asetek v. CMI (Fed. Cir. 2016) ; Eaton-Boyd (Oct 2025) ; Accelsius-Nokia Bell Labs licence ; Danfoss ShowerPower families ; Purdue HMMC filings ; Intel liquid-cooled IHS families ; Nvidia Heydari-era filings.
