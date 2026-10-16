# Standards, specifications and reliability requirements for a drop-in AI-server cold plate

Prepared 2026-10-13 for the cooling-architecture programme (benchmark: CoolIT 15 kW coldplate tech brief, June 2026).
Angle: what a cold plate must satisfy to be *drop-in compatible* with the OCP / NVIDIA MGX / ASHRAE W45 CDU-and-manifold ecosystem, and which reliability tests and failure modes govern the design.

## 0. Method and evidence quality (read first)

- **No live web searches were performed in this sub-task.** The shared per-turn WebSearch budget (200 calls across all agents) was already exhausted when this agent started; all six queries issued were refused. WebFetch and curl are network-blocked in this container (confirmed by sibling agents; not re-attempted).
- Evidence is therefore of three kinds, tagged throughout:
  - **[Sib]** = a number or document found *with a URL* by a sibling research agent earlier in this run (files coolit-briefs-numbers.md, coolit-products.md, competitors-singlephase.md, competitors-advanced.md, chip-roadmap-requirements.md in the same scratchpad). These carry a URL in the Sources section.
  - **[Brief]** = the CoolIT 15 kW tech brief itself (local extract).
  - **[KB-H/M/L]** = the author's background knowledge (training data to mid-2026), with High / Medium / Low confidence. **Every [KB] number must be verified against the primary document before it is written into a requirements specification.** Where a [KB] item has a well-known primary document, the document is named so it can be pulled directly.
- Vendor claims are marked (V); OCP/ASHRAE/peer-reviewed material is marked (I) for independent/industry-consensus.

## 1. Why the standards matter for beating CoolIT

CoolIT's brief frames its result entirely in ecosystem terms: "standard water-glycol coolant", "1.2 LPM/kW industry standard flow", "45 C inlet warm-water", "standard thermal paste", "proven mass-manufacturing" [Brief]. CoolIT is also the primary author of the new OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (Oct 2026) and a collaborator on OCP UQD v2.0.0 [Sib], i.e. it is shaping the yardstick. A competing plate that is thermally better but *not* drop-in (wrong fluid, wrong QD, too much pressure drop for the installed CDU fleet, non-approved wetted materials, no OCP-format test report) will lose. The checklist in Section 9 is therefore a hard gate, not a nice-to-have.

## 2. The boundary conditions imposed by the ecosystem

### 2.1 Facility and TCS temperature classes (ASHRAE TC 9.9)

| Class (ASHRAE Thermal Guidelines, 5th ed., 2021) | Facility water supply range | Typical heat-rejection plant | Source / confidence |
|---|---|---|---|
| W17 | 2-17 C | chiller | [Sib] Upsite summary of 5th ed.; [KB-H] |
| W27 | 2-27 C | cooling tower / chiller assist | same |
| W32 | 2-32 C | cooling tower, most climates | same |
| W40 | 2-40 C | dry cooler, most climates | same |
| **W45** | **2-45 C** | dry cooler, nearly all climates, chiller-less | same; this is the AI de-facto class [Sib] |
| W+ | > 45 C | dry cooler everywhere; heat-reuse ready | same |

Notes [KB-H]: the 5th edition (2021) renamed the 4th-edition classes W1-W5 to the temperature-named classes above and added W+. The ASHRAE TC 9.9 book "Liquid Cooling Guidelines for Datacom Equipment Centers" (2nd ed., 2014) and the TC 9.9 white paper "Water-Cooled Servers: Common Designs, Components, and Processes" (2019) are the two documents that define the facility-water-system (FWS) / technology-cooling-system (TCS) vocabulary, the CDU as the isolation point, and the common wetted-material lists used by OCP. [KB-M]

What the industry actually runs [Sib]: NVIDIA GB200 NVL72 max TCS supply 45 C, max return 65 C (QCT whitepaper); NVIDIA Vera Rubin MGX gen-3 "designed for 45 C inlet"; Supermicro DLC-2 and Lenovo Neptune up to 45 C; HPE GX 40 C; Uptime Institute notes a typical 40 C GPU supply limit; OCP L-L CDU methodology envelope 17-65 C. Nobody publishes cold-plate performance above 45 C.

**What "warm water 45 C" and "W+" imply for free cooling** [KB-M, approximate engineering arithmetic]:
- A dry cooler needs roughly 8-12 K approach to ambient dry-bulb at design load, and a liquid-to-liquid CDU adds a 2-5 C approach (OCP rates CDUs at 3-5 C ATD [Sib]). With a 45 C TCS supply the FWS can be ~40-42 C, so the plant is chiller-less up to ~30-33 C ambient, i.e. all but a few hundred hours per year in temperate climates and most hours even in hot-dry climates; adiabatic assist covers the rest.
- At W+ (50-60 C supply) the loop is chiller-less essentially everywhere and the return water (65-75 C) becomes directly usable for district heating / absorption chillers. This is why hyperscalers push for 45 C now and talk about higher.
- The penalty lands entirely on the cold plate: at 45 C inlet and an 80 C case ceiling the whole case-to-inlet budget is 35 K [Brief]; every +5 C of supply removes 5 K (~14 %) of that budget. A plate that holds Tcase at 50 C inlet is worth a chiller to the operator. The programme should therefore characterise at 45 **and 50 C** inlet (sibling requirement: "inlet envelope 17-50 C" [Sib]).

### 2.2 Flow per kW and the resulting coolant rise

| Convention | Value | Source |
|---|---|---|
| CoolIT 15 kW brief (2026) | 1.2 LPM/kW "industry standard flow rate for AI systems" | [Brief] |
| CoolIT 4 kW brief (2025) | 1.5 LPM/kW "semiconductor industry recommended" | [Sib] |
| OCP L-L CDU test methodology | 1.5 LPM/kW rating basis; >= 40 psi TCS head; TCS components may see up to 100 psi | [Sib] |
| OCP OAI liquid-cooling guideline (Mar 2023) | 1-2 LPM per 1 kW OAM; recommended 7.5-12 C coolant rise | [Sib] |
| Electronics Cooling (Jun 2025) | 1.2 LPM/kW at 45 C "a common standard many CDUs can meet"; ~18 psi (124 kPa) rack budget | [Sib] |
| NVIDIA GB200 NVL72 (QCT) | ~130 LPM/rack at ~120-130 kW, i.e. ~1.0 LPM/kW; 45 in / 65 C out envelope = 20 K = 0.75 LPM/kW | [Sib] |

Energy balance, PG25 (cp ~3.94 kJ/kg-K at 50 C, rho ~1.01-1.02 kg/L) [Sib]: 1.0 LPM/kW -> ~15 K; 1.2 -> ~12.6 K; 1.5 -> ~10 K. **No OCP, ASHRAE or NVIDIA document codifies 1.2 LPM/kW** [Sib]; it is a CDU-capability convention. A drop-in plate must publish full curves from 0.5 to 1.5 LPM/kW and must meet its thermal spec at the NVIDIA 0.75-1.0 LPM/kW envelope, where CoolIT has not published anything.

### 2.3 Pressure-drop budget and pressure ratings

| Item | Value | Source |
|---|---|---|
| Rack TCS loop (manifolds + QDs + trays) worked example | ~18 psi (124 kPa) at 1.2 LPM/kW | [Sib] Electronics Cooling Jun 2025 |
| CDU secondary head available | CoolIT CHx1000 35 psi; CHx1500 44 psi; CHx2000 53 psi; OCP L-L CDU >= 40 psi; Google Deschutes 80 psi "to enable advanced cold plate designs" | [Sib] |
| Max pressure TCS components may see (OCP L-L CDU methodology) | up to 100 psi (6.9 bar) | [Sib] |
| Vendor GPU-plate dP (GB200/GB300 class, ~1-2.7 kW) | < 20 kPa at 1.8 LPM; 12 kPa at 1.7 LPM; 35 kPa at 2.5 LPM | [Sib] (V, secondary) |
| CoolIT 4 kW plate, full loop incl. fittings and QDs | 8 psi (55 kPa) at ~6 LPM | [Sib] |
| CoolIT 15 kW plate | **pressure drop not disclosed** | [Brief] |
| JetCool RTX PRO 6000 SmartPlate rating | 72 psi (5.0 bar) continuous, 216 psi (14.9 bar) burst (= 3x) | [Sib] datasheet (V) |
| OCP Cold Plate Test Spec v1.0.0 | burst example > 20 bar; dP measured at 45 +/- 2 C at >= 6 flow points, 25-150 % of rated flow | [Sib] |
| Typical hyperscaler cold-plate MAWP in SOWs | 100-150 psi (7-10 bar) design pressure; proof 1.5x; burst >= 3x | [KB-M] |
| Negative-pressure loops (Chilldyne/Daikin) | plate must tolerate sub-atmospheric operation; available plate dP < 1 atm minus margin, in practice a few tens of kPa | [Sib] |

Working requirement adopted by the roadmap sibling [Sib]: plate-only dP <= 20-35 kPa at design flow, tray (2 GPU plates + CPU + QDs) <= 70-100 kPa, series plumbing of two plates still possible. This is consistent with both the installed CDU fleet (35-53 psi secondary head) and with negative-pressure compatibility.

### 2.4 Coolant: OCP PG25

| Property | Value | Source |
|---|---|---|
| Base fluid | 25 wt% propylene glycol in de-ionised water + corrosion inhibitor package (+ biocide in some formulations) | OCP Base Specification PG25 v1.0.0 [Sib URL]; [KB-H] for composition |
| Pre-mixed commercial equivalents | Dow DOWFROST LC-25 (cp 3.94 kJ/kg-K at 50 C); similar products from Clariant, Arteco, Kilfrost, Nalco/Ecolab | [Sib] ChemPoint page; [KB-M] |
| Freeze protection | approx. -10 C (25 wt% PG); chosen for shipping/storage, not operation | [KB-M] |
| Viscosity | ~2x water at 45-50 C -> laminar in microchannels (Re ~200 at 0.7 m/s in 0.2 mm gaps) | [Sib] model |
| In-service monitoring (OCP PG25 Guidelines v1.0.0, Oct 2026) | glycol concentration, pH, conductivity, inhibitor concentration, particle count, microbial count, with action limits | document exists [Sib URL]; **limit values not retrieved** [KB-L] |
| Typical action limits used by water-treatment vendors for PG-inhibited loops | pH 7.5-9.5; conductivity drift tracked vs. baseline; total bacteria < 10^3-10^4 CFU/mL; glycol +/- 2-3 % of nominal; copper < 1 ppm, iron < 1 ppm as corrosion indicators | [KB-L] |

NVIDIA's GB200/GB300 reference designs use PG25 [Sib]. Practical consequence: the plate's thermal spec must be stated **in PG25 at 45 C**, not DI water (water is ~1.4 K better at the benchmark point per the sibling model [Sib]), and the wetted path must be compatible with the OCP inhibitor package (organic-acid / azole copper inhibitors), which rules out several elastomers and all aluminium in a copper loop.

### 2.5 Quick disconnects and rack interfaces

| Interface | Content | Source |
|---|---|---|
| OCP UQD spec v2.0.0 (Oct 2026) | UQD02 (1/8 in), UQD04 (1/4 in), UQD06 (3/8 in), UQD08 (1/2 in); UQDB blind-mate variants; cross-vendor interoperable (CPC, Staubli, Parker, Danfoss, others); CoolIT credited as collaborator | [Sib] URL; size list [KB-H] |
| Typical UQD vendor ratings | working pressure ~8-10 bar (CPC Everis UQD04: ~120 psi class), -40 to +115 C body rating, spill-free dry-break, thousands of mate cycles; UQDB adds misalignment tolerance (~ +/-1-2 mm) for blind mating | [KB-M] |
| GB200/GB300 compute trays | hose-type 1/4-3/8 in (UQD04/06-class) per tray; Ingrasys GB300 rack ~120 kW with 1/4-in QDs | [Sib] (secondary) |
| Rubin / Kyber (> 200 kW racks) | moving to 1/2-in (UQD08 / UQDB08); Kyber vertical blades with blind-mate manifolds | [Sib] (secondary, KB-L) |
| CDU-to-manifold | 1 in dry-break (Danfoss Hansen FD83-class) or hard pipe | [KB-M] |
| Rack form factors to support | EIA-310 19 in, OCP ORv3 21 in (blind-mate rear manifold), NVIDIA MGX / Kyber | [Sib] CoolIT manifold page lists EIA, ORV3, MGX |

Design consequence: the plate itself does not carry the QD, the tray loop does. "Drop-in" therefore means the plate's inlet/outlet must accept standard 3/8 in or 1/2 in hose barbs / push-lock or brazed stainless tube, with the loop-level QD being UQD04/06/08 or UQDB. A plate whose dP forces a bigger QD size than the tray already uses is not drop-in.

## 3. OCP cold-plate documents: what exists and what each covers

| Document | Status / date | What it covers (as known) | Source / confidence |
|---|---|---|---|
| OCP Single-Phase Direct-to-Chip Cold Plate Test Specification v1.0.0 | published Oct 2026 (primary author CoolIT) | Standard test method: thermal resistance R = (Tcase - Tinlet)/P at multiple flows with a recommended TIM; dP at 45 +/- 2 C at >= 6 flow points from 25 % to 150 % of rated flow; burst (example > 20 bar); helium leak <= 1e-5 mbar-L/s; thermal cycling 10-65 C (operating) and -40/+70 C (storage/shipping) | [Sib] URL (details read by sibling from search extract; full tables not retrieved) |
| OCP Cold Plate Development and Qualification white paper (with integrated comments) | 2024-25 | Development flow and qualification matrix for D2C plates: design review, CFD, TTV correlation, leak/proof/burst, pressure and thermal cycling, corrosion/compatibility soak, vibration and shock, cleanliness, long-duration flow test; reporting template | [Sib] URL; content summary [KB-M] |
| OCP ACS "Cold Plate Leak Detection and Intervention" white paper | 2024-25 | Leak-detection architecture (rope sensors, tray drip sensors, flow/pressure/level monitoring at CDU), intervention logic (isolate tray/rack, throttle, shutdown), leak size classes | [Sib] URL; content [KB-M] |
| OCP ACS Cold Plate Requirements (ORv3 era) | ~2021-22 | First-generation requirements: wetted-material list, working/proof/burst pressure, leak test, thermal/pressure cycling, mounting loads, labelling | [KB-M]; exact numbers not recalled, pull document |
| OCP "Guidelines for Liquid Cooling" (ACS / Data Center Facility) | 2021-22 | FWS/TCS architecture, CDU, water quality, commissioning, flushing | [KB-M] |
| OCP Base Specification PG25 v1.0.0 and OCP PG25 Guidelines v1.0.0 | 2025 / Oct 2026 | Coolant composition, properties, and in-service monitoring | [Sib] URLs |
| OCP UQD Design Spec v2.0.0 | Oct 2026 | Sizes, envelopes, interoperability, pressure/temperature classes, blind-mate | [Sib] URL |
| OCP L-L CDU Test Methodology & Performance Rating r1 | 2024-25 | CDU rating basis: 1.5 LPM/kW, >= 40 psi, TCS 17-65 C, components to 100 psi | [Sib] URL |
| OCP OAI System Liquid Cooling Guidelines | Mar 2023 | 1 kW OAM: 1-2 LPM, 7.5-12 C rise, case-to-inlet 0.015-0.016 C/W reference | [Sib] URL |
| OCP "Thermal Boundaries in AI Infrastructure" white paper | Oct 2026 | Single-phase cold-plate boundary "roughly 4,000 W" (fragment only) | [Sib] URL |
| OCP ORv3 Rack / Blind-Mate Manifold specs | 2021-24 | 21 in rack, rear vertical manifold, UQDB blind-mate positions, 48 V busbar | [KB-M] |

**Read-across:** the OCP test spec is the format in which our results must be published. CoolIT's brief is *not yet* in that format (no dP curve, no flow sweep, no burst/leak data). Publishing a full OCP-format report for our plate is itself a differentiator [Sib].

## 4. NVIDIA, Intel and AMD cold-plate requirements

| Source | What is public | Confidence |
|---|---|---|
| NVIDIA GB200/GB300 NVL72 liquid cooling / site-prep guides | Under NDA. Public via partners: PG25; 45 C max supply, 65 C max return; ~130 LPM per rack; UQD-class tray QDs; NVIDIA keeps a Recommended Vendor List (RVL) for cold plates, manifolds, CDUs and QDs (Boyd, CoolIT, Vertiv, Motivair/Schneider, Cooler Master, AVC, Auras, Delta, nVent, Staubli, CPC, Parker, Danfoss and others) | [Sib] for temperatures/flow/RVL mention; RVL membership list [KB-M] |
| NVIDIA Rubin (2026) | NVIDIA centralised cold-plate purchasing; Group-A suppliers Jentech, AVC, Cooler Master, Delta; plate ASP ~US$400; NVL144 cooling BOM ~US$55.7 k | [Sib] TVBS / Digitimes / Igor's Lab (secondary) |
| NVIDIA plate-level R and dP requirement | **not public**; secondary sources conflict (0.6-1.6 LPM/kW; 12-150 kPa; < 0.03 K/W "target" for a GB200 superchip plate) | [Sib] |
| NVIDIA qualification expectations (from RVL programmes) | 100 % leak test, OCP-style pressure/thermal cycling, PG25 compatibility soak, flatness/roughness and mounting-load limits for SXM/puck modules, TIM pressure window, serialised traceability | [KB-M] |
| Intel | Intel originated the UQD concept before donating it to OCP; Xeon Thermal Mechanical Specification and Design Guides (TMSDG) give Tcase limits, load (socket-dependent, typically 40-60 lbf-class for LGA, higher for liquid-cooled retention), flatness and contact-pressure windows; Intel/TSMC discussed lidless packages for DLC at OCP 2025 | [KB-M]; [Sib] for OCP-2025 lidless mention |
| AMD | SP5 / MI300 thermal design guides specify Tcase/Tj and mounting loads; MI455X / Helios is 100 % DLC in a double-wide OCP ORW rack | [KB-L] for guides; [Sib] for Helios |

Implication: there is no public NVIDIA "cold plate qualification spec" to copy; the OCP test spec plus the RVL-style tests above are the de-facto gate, and RVL admission is itself a commercial requirement for GB/Rubin-class programmes.

## 5. Materials, corrosion, velocity, filtration

### 5.1 Wetted-materials compatibility (copper / PG25 loops)

| Material | Status in copper-PG25 TCS loops | Notes / source |
|---|---|---|
| Copper (C101/C110, OFHC) | approved, the standard plate material | ASHRAE "Water-Cooled Servers" and OCP wetted lists [KB-H] |
| Nickel-plated copper | approved; used where copper-ion release or mixed-metal contact is a concern and on CDU heat exchangers | [KB-M]; CoolIT OMNI unibody is all-copper/no-braze (V) [Sib] |
| Stainless steel 304/316L | approved for manifolds, tubes, QD bodies (316L preferred) | [KB-H]; CoolIT manifolds are stainless [Sib] |
| Brass | only dezincification-resistant (DZR, e.g. CW602N) or low-zinc; standard yellow brass dezincifies in glycol loops | [KB-M] |
| Aluminium | **not** permitted in a copper loop (galvanic couple, pitting); only in all-aluminium loops with dedicated inhibitor | [KB-H]; Lenovo N1380 uses some Al plates in its own loop (V) [Sib] |
| Zinc / galvanised steel, cast iron | prohibited | [KB-H] |
| EPDM (peroxide-cured) | approved hose and O-ring material; sulphur-cured EPDM and NBR to be avoided (leaching, hardening) | [KB-M] |
| PTFE, PPSU, PEEK, PA12 (specific grades), FKM (specific grades) | generally approved; silicone prohibited (extractables, oil fouling of microchannels) | [KB-M] |
| Brazing filler (Cu-P, Ag-based) | approved if fully fluxless / vacuum brazed and residue-free; flux residues are a known corrosion and particulate source | [KB-M] |
| Solder (Sn-Ag, Sn-Pb) | avoided in wetted path (galvanic, creep) | [KB-M] |

Galvanic rule [KB-H]: keep all wetted metals within ~0.2-0.25 V of each other on the seawater galvanic series or electrically isolate them; copper-stainless is accepted in inhibited PG25; copper-aluminium is not.

### 5.2 Corrosion, erosion and microbiological mechanisms

| Mechanism | Governing parameter | Common limit / practice | Source |
|---|---|---|---|
| Erosion-corrosion of copper | wall velocity, particulates, entrained air | copper channels/tubes <= 1.5-2.0 m/s continuous; stainless <= 3 m/s; microchannel designs typically 0.3-1.5 m/s | [KB-M]; one low-reliability vendor blog quotes 2-4 m/s [Sib] |
| Cavitation at orifices/jets | local static pressure vs vapour pressure, sharp-edged orifices | avoid local velocities > ~5 m/s in sub-100 um jets without pressure margin; no public 10-year jet erosion data | [Sib] (gap noted), [KB-M] |
| Dezincification | zinc content of brass, chloride, glycol | use DZR brass or eliminate brass | [KB-M] |
| Galvanic | mixed metals, conductivity | material list above; conductivity trend monitoring | [KB-H] |
| Inhibitor depletion / glycol degradation to organic acids | temperature, oxygen ingress, time | pH and inhibitor assays; PG25 Guidelines action limits; replace or re-dose | [Sib] PG25 Guidelines exist; limits [KB-L] |
| Microbiologically influenced corrosion (MIC) / biofilm | stagnant zones, nutrient (glycol), 30-45 C | biocide package, no dead legs, bacterial counts, filter screens; UTA accelerated-degradation thesis on copper in PG25 loops | [Sib] UTA thesis URL; [KB-M] |
| Particulate fouling of sub-0.3 mm channels | commissioning debris, braze residue, corrosion products | Ecolab (CoolIT's new owner) attributes recent field cold-plate issues to incomplete flushing/fill (particulates migrating into plates); Google runs isolated loops with filtration and reports ~99.999 % CDU availability | [Sib] Electronics360 Q&A Oct 2026; [Sib] Google Hot Chips 2025 |

### 5.3 Filtration and minimum passage size

| Item | Value | Source |
|---|---|---|
| CDU secondary-side filtration commonly specified | 50 um (some operators 25 um); strainers at rack ~100 um | [KB-M] |
| Sibling design rule | minimum internal gap >= 0.15 mm wherever only 50 um filtration is guaranteed, or a short-channel manifold layout that tolerates partial blockage | [Sib] chip-roadmap requirements |
| Fine-channel / jet designs | sub-100 um jets or 50-75 um gaps need <= 25-50 um filtration and are fouling-sensitive (JetCool's own "avoiding filtration challenges" language) | [Sib] |
| Schneider on CDU rating | account for filter dP in the TCS budget; CDU capacity ratings are not comparable without it | [Sib] Schneider blog Dec 2025 |

Rule of thumb for the architecture [KB-M]: smallest wetted passage >= 3x the absolute filter rating protects against bridging; if the thermal design needs 50-100 um gaps, the programme must (a) specify 25 um absolute filtration at the CDU *and* in-tray last-chance screens, and (b) prove by test that a 10-20 % blocked channel population does not raise the hot-spot temperature beyond spec (manifold-fed short channels are far more tolerant than long split-flow channels [Sib]).

## 6. Reliability qualification: the test matrix a drop-in plate must pass

Values below combine the OCP Cold Plate Test Spec v1.0.0 items that the sibling retrieved [Sib] with typical hyperscaler / OEM SOW values [KB-M]. The OCP numbers should be read directly from the PDF before adoption.

| Test | Typical requirement | Source / confidence |
|---|---|---|
| Proof (hydrostatic) pressure | 1.5x MAWP (e.g. 150-225 psi / 10-15 bar) for 5-30 min, no leak, no permanent deformation | [KB-M] |
| Burst pressure | >= 3x MAWP; OCP example > 20 bar; JetCool datasheet 216 psi burst vs 72 psi continuous | [Sib] OCP, JetCool; [KB-M] |
| Leak rate (helium mass spectrometry or pressure decay) | He <= 1e-5 mbar-L/s per OCP; many SOWs ask 1e-6; 100 % production leak test | [Sib] OCP; [KB-M] |
| Pressure cycling | 0 -> MAWP -> 0, 10,000 to 100,000 cycles (programme dependent), then leak test | [KB-M] |
| Thermal cycling | OCP: 10-65 C operating, -40/+70 C non-operating; typically 100-1,000 cycles; then leak and dP re-check | [Sib] OCP; cycle counts [KB-M] |
| Long-duration flow / corrosion soak | PG25 at 65 C, 1,000-3,000 h at 1.5x rated flow; dP drift <= 10 %, no visible pitting, coupon mass loss and coolant metal ions below limits | [KB-M] |
| Compatibility soak of elastomers | hose/O-rings in PG25 at 70-90 C, 1,000 h; hardness/volume change limits | [KB-M] |
| Vibration and shock (shipping) | ISTA 3A/3E or ASTM D4169 packaged; operational per OCP ORv3 / NEBS-lite | [KB-M] |
| Drop / handling | packaged drop; QD mating cycles (>= 1,000) | [KB-M] |
| Cleanliness | flushed to a particle spec (ISO 16232-style count or a mass/size limit), capped and shipped dry or pre-filled with PG25; no residual flux or machining oil | [KB-M] |
| Dimensional / mounting | flatness of contact face typically <= 25-50 um over the die/lid footprint, Ra <= 0.8 um, mounting load within the package vendor's window; bolt torque spec | [KB-M] |
| Thermal performance correlation | OCP test method on a TTV; R vs flow at >= 6 points; dP vs flow at 45 C; plate-to-plate CpK on R and dP (CoolIT's own data show 10 K plate-to-plate spread at one TC, which is a CpK problem not a design problem) | [Sib] OCP; [Brief] |
| Manufacturing qualification | automotive-style APQP/PPAP packages (FMEA, control plan, MSA, CpK >= 1.33 on dP and leak) are increasingly requested by hyperscalers and ODMs; 100 % serialised traceability | [KB-M]; CoolIT states 100 % leak and functional test, AI optical screening [Sib] |
| Design life / MTBF | 5-7 year server life, 10-year plate design life, 10-year EPDM hose life; MTBF targets for the plate itself are set by leak-rate statistics (no vendor publishes plate MTBF) | [KB-M]; [Sib] "no vendor publishes MTBF" |
| Regulatory | RoHS/REACH; UL 94 V-0 for any polymer in the tray; coolant SDS; no PFAS in wetted polymers increasingly requested (EU) | [KB-M] |

## 7. Field failure modes and the architectures that address them

| Failure mode | Where it happens | Evidence | Mitigation relevant to our architecture |
|---|---|---|---|
| Leaks at fittings, hose crimps, QDs, during install/service | tray loop, not the plate core | Uptime Institute surveys repeatedly rank leaks as the top DLC concern, dominated by connections and human error rather than plate bodies; OCP ACS leak-detection white paper exists for this reason | [KB-M] for Uptime; [Sib] OCP ACS URL. Minimise joints: unibody or single-braze plate, brazed stainless stubs, fewer hose segments, UQDB blind-mate |
| Coolant quality drift (inhibitor depletion, pH, bacteria, glycol loss) | whole TCS | OCP PG25 Guidelines (Oct 2026); Ecolab positioning (water chemistry) behind its US$4.75 bn CoolIT purchase | [Sib]. Design for monitorability: low-dP plate leaves pressure budget for CDU filters and sensors |
| Particulate migration into microchannels after commissioning | plates with < 0.3 mm channels | Ecolab's Walicki (Oct 2026) | [Sib]. Short, manifold-fed channels and a specified min gap or 25 um filtration |
| Air entrainment / cavitation / pump issues in negative-pressure or low-NPSH loops | plate inlet orifices | Chilldyne-type loops run below atmospheric | [Sib]. Vacuum-tolerant plate body; no thin covers that collapse at -0.8 bar |
| TIM pump-out / dry-out under thermal cycling at > 100 W/cm2 | lid-plate interface | large packages warp 100-300 um; CoolIT's 10 K plate-to-plate spread | [Sib]; [Brief]. Compliant mounting, controlled bond line, PCM/liquid-metal TIM options |
| Mixed-metal corrosion when operators mix vendor loops | TCS | OCP wetted lists exist to prevent it | [KB-H]. Copper/316L/EPDM only |

**Leak-before-break and negative pressure** [KB-M + Sib]: "Leak-before-break" is a fracture-mechanics design principle (a crack grows through-wall and leaks detectably before it reaches the critical length for rupture); for a cold plate it translates to ductile copper/stainless construction, no brittle brazes under cyclic pressure, and burst >= 3x MAWP. Negative-pressure architecture (Chilldyne, acquired by Daikin Applied, Nov 2025) goes further: the loop runs below atmospheric so a breach draws air in instead of pushing coolant out; the price is that total plate+tray dP must fit inside roughly 0.5-0.8 bar, which makes low-dP plates the only candidates [Sib].

## 8. What this means for the competitive position

1. CoolIT has published R (as dT at 1.2 LPM/kW) but *not* dP, burst, leak, cycling, materials or CpK for the 15 kW plate [Brief]. A plate reported in full OCP v1.0.0 format with dP at six flow points and a complete qualification matrix beats it on transparency before any thermal comparison.
2. The two ecosystem constraints that most shape our architecture are the **dP budget** (<= 20-35 kPa plate-only, so it drops into CHx-class CDUs, 1/4-3/8 in QD trays and negative-pressure loops) and the **filtration/passage-size** rule (either >= 0.15 mm gaps or a blockage-tolerant manifold layout with 25 um filtration specified) [Sib].
3. The 45 C class is now fixed; W+ (50 C) characterisation is cheap insurance and a saleable feature.
4. Materials: copper core, 316L stubs, peroxide-cured EPDM, no brass unless DZR, no aluminium, no silicone; vacuum-brazed or unibody construction; nickel plating optional and to be justified by the compatibility soak.

## 9. Drop-in compatibility checklist (requirements the architecture must satisfy)

| # | Requirement | Target value | Basis |
|---|---|---|---|
| 1 | Coolant | OCP PG25 (25 wt% PG, inhibited); performance stated in PG25; DI-water curve as secondary | [Sib] OCP PG25 |
| 2 | Inlet temperature envelope | operate 17-50 C; spec point 45 C (ASHRAE W45); publish 50 C (W+) data | [Sib] ASHRAE/NVIDIA |
| 3 | Outlet temperature | <= 65 C at NVIDIA envelope; no component rated below 70 C continuous | [Sib] QCT |
| 4 | Flow | full spec at 0.75-1.0 LPM/kW; curves 0.5-1.5 LPM/kW; CoolIT comparison point 1.2 LPM/kW | [Sib] |
| 5 | Pressure drop | plate-only <= 25 kPa at 1.0 LPM/kW and <= 35 kPa at 1.2 LPM/kW on the 15 kW TTV; tray <= 100 kPa incl. QDs; measured per OCP at 45 +/- 2 C, >= 6 points | [Sib] roadmap + OCP |
| 6 | Pressure rating | MAWP >= 100 psi (6.9 bar), preferred 150 psi (10.3 bar); proof 1.5x; burst >= 3x and >= 20 bar; vacuum-tolerant to -0.9 bar(g) | OCP L-L CDU (100 psi) [Sib]; OCP burst example [Sib]; [KB-M] |
| 7 | Leak | He <= 1e-5 mbar-L/s (target 1e-6); 100 % production leak test; no polymer in the primary pressure boundary | [Sib] OCP; [KB-M] |
| 8 | Cycling | thermal 10-65 C operating and -40/+70 C storage per OCP; pressure cycling >= 10,000 cycles 0-MAWP | [Sib] OCP; [KB-M] |
| 9 | Wetted materials | Cu (bare or Ni-plated), 316L, peroxide EPDM, PTFE/PPSU/PEEK; DZR brass only if unavoidable; no Al, Zn, NBR, silicone; fluxless/vacuum braze or unibody | [KB-H/M]; OCP/ASHRAE lists |
| 10 | Velocity | <= 1.5-2.0 m/s in copper passages at 150 % rated flow; no jet/orifice > 5 m/s without cavitation margin analysis | [KB-M] |
| 11 | Filtration / passage | smallest passage >= 3x the specified absolute filter rating (>= 0.15 mm with 50 um filters) OR 25 um filtration specified plus demonstrated tolerance to 10-20 % channel blockage | [Sib]; [KB-M] |
| 12 | Interfaces | 3/8 in or 1/2 in stainless stubs / push-lock; tray QDs UQD04/06/08 and UQDB per OCP UQD v2.0.0; EIA-310, ORv3 and MGX/Kyber tray envelopes | [Sib] |
| 13 | Mechanical | flatness <= 25-50 um over footprint, Ra <= 0.8 um; mounting load and TIM pressure within package vendor window; compliant loading for 100-130 mm packages warping 100-300 um | [KB-M]; [Sib] |
| 14 | Thermal reporting | OCP Cold Plate Test Spec v1.0.0 format: R case-to-inlet vs flow with named TIM, dP vs flow at 45 C, both absolute (K/W) and unit (cm2-K/W) with heater area stated; plate-to-plate CpK | [Sib] |
| 15 | Hot-spot uniformity | max-minus-average <= 6 K on the 4-zone TTV (CoolIT ~10 K); HBM zones fed with inlet-temperature fluid | [Brief]; [Sib] |
| 16 | Corrosion / compatibility | 1,000-3,000 h PG25 soak at 65 C with coupons; dP drift <= 10 %; copper and iron in coolant below limits | [KB-M] |
| 17 | Cleanliness | flushed, particle-counted, capped; shipped dry or pre-filled with PG25 | [KB-M] |
| 18 | Leak detection / serviceability | compatible with tray drip sensors and rope sensors; drains/vents for hot-swap; QD mating cycles >= 1,000 | [Sib] OCP ACS paper; [KB-M] |
| 19 | Negative-pressure compatibility (optional SKU) | plate + tray dP <= ~30-50 kPa at rated flow; body stable under vacuum | [Sib] Chilldyne |
| 20 | Manufacturing quality system | PPAP-style package: PFMEA, control plan, MSA, CpK >= 1.33 on leak and dP; serialised traceability; RoHS/REACH | [KB-M] |
| 21 | Cost | <= ~US$400 ASP for a Rubin-class GPU plate (NVIDIA Group-A price point) | [Sib] |
| 22 | Commercial gate | OCP-format test report; path to NVIDIA RVL / ODM qualification; coolant-vendor (Ecolab/Nalco, Dow, Clariant) compatibility letters | [Sib]; [KB-M] |

## 10. Gaps / unknowns

1. **No live searches** were possible; every [KB] value (proof/burst multiples, cycle counts, filter ratings, velocity limits, elastomer lists, UQD vendor pressure ratings, PG25 action limits, RVL membership, Uptime failure statistics, Intel/AMD guide values) is from memory and must be checked against the primary PDFs before use in a spec.
2. The OCP Cold Plate Test Spec v1.0.0, UQD v2.0.0 and PG25 Guidelines v1.0.0 PDFs (all Oct 2026 uploads) were located by URL but not read in full; the sibling extract gives the headline test conditions only. Pull and read all three.
3. The original OCP ACS "Cold Plate Requirements" (ORv3 era) and the OCP "Liquid Cooling Guidelines" documents were not located with URLs in this run; their exact pressure, materials and test tables are needed.
4. NVIDIA's GB200/GB300/Rubin cold-plate R and dP requirements are NDA; secondary sources conflict (0.6-1.6 LPM/kW; 12-150 kPa). Obtain the MGX / DGX site-prep and liquid-cooling design guides directly.
5. No independent data on 10-year erosion/cavitation of copper under PG25 at microjet or sub-0.1 mm channel velocities exists in the public domain.
6. No vendor publishes plate-level MTBF, field leak rates or clogging statistics; the Uptime Institute survey numbers on DLC incidents were not retrievable this session.
7. ASHRAE's exact W-class table (2 C lower bound for all classes vs class-specific lower bounds) and any 2024-2026 TC 9.9 addenda on liquid cooling should be confirmed from the 5th-edition book.
8. The pressure rating and temperature class tables inside OCP UQD v2.0.0 (and whether UQDB08 is finalised) were not retrieved.
9. Whether NVIDIA/ODM GB-class plates are nickel-plated or bare copper is not public.

## Sources

Primary / standards documents (URLs located by sibling agents in this run):
- OCP Single-Phase Direct-to-Chip Cold Plate Test Specification V1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf and https://www.opencompute.org/documents/ocp-cold-plate-test-specification-v1-0-0-pdf-1/
- OCP UQD Design Specification v2.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf
- OCP PG25 Guidelines V1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
- OCP Base Specification PG25 v1.0.0: https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/
- OCP Cold Plate Development and Qualification white paper: https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/
- OCP ACS Cold Plate Leak Detection and Intervention white paper: https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1
- OCP L-L CDU Test Methodology and Performance Rating r1: https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- OCP OAI System Liquid Cooling Guidelines (Mar 2023): https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/
- OCP white paper, Thermal Boundaries in AI Infrastructure (Oct 2026): https://www.opencompute.org/documents/white-paper-thermal-boundaries-in-ai-infrastructure/
- ASHRAE 5th-edition liquid classes (Upsite summary): https://www.upsite.com/blog/major-changes-to-ashraes-fifth-edition-of-thermal-guidelines-part-3-liquid-cooling-chapter-updates/ ; Green Grid glossary: https://www.thegreengrid.org/resources/glossary/W
- QCT QoolRack GB200 NVL72 whitepaper (45 C in / 65 C out, ~130 LPM): https://blog.qct.io/wp-content/uploads/2025/04/QCT-Qoolrack-Stand-Alone_Advanced-Liquid-Cooling-for-NVIDIA-GB200-NVL72-Systems.pdf
- Vertiv / NVIDIA GB200 NVL72 reference architecture: https://investors.vertiv.com/news/news-details/2024/Vertiv-Codevelops-with-NVIDIA-Complete-Power-and-Cooling-Blueprint-for-NVIDIA-GB200-NVL72-Platform/default.aspx
- TechPowerUp, Vera Rubin NVL144 designed for 45 C inlet: https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production
- Uptime Institute (40 C GPU coolant supply limit): https://intelligence.uptimeinstitute.com/entity_pdf/node/153594/pdf
- Google Deschutes CDU (80 psi, 2 MW): https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/ ; Google liquid cooling at Hot Chips 2025: https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips
- Schneider Electric on CDU rating and filter dP: https://blog.se.com/datacenter/2025/12/16/account-for-filtering-too-beware-of-how-cdu-rating-capacity-is-specified/
- Ecolab / CoolIT field particulate comments (Electronics360, Oct 2026): https://electronics360.globalspec.com/article/24164/q-a-ecolab-bets-on-liquid-cooling-for-ai-data-center-growth
- Data Centre Review, how to build reliable liquid cooling systems (Aug 2026): https://datacentrereview.com/2026/08/how-to-build-reliable-liquid-cooling-systems/
- UTA thesis, accelerated degradation of copper cold plates in PG25 loops: https://uta-ir.tdl.org/uta-ir/handle/10106/31381
- Chilldyne negative-pressure: https://www.storagereview.com/review/high-performance-leak-free-liquid-cooling-chilldynes-cdu-and-cold-plates-in-action ; Daikin acquisition: https://www.daikinapplied.com/news/news/daikin-applied-expands-data-center-offering-with-acquisition-of-chilldyne
- JetCool RTX PRO 6000 SmartPlate datasheet (72 psi continuous / 216 psi burst): https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
- Dow DOWFROST LC-25 properties: https://www.chempoint.com/en-ca/products/dow/dowfrost-glycol-thermal-fluids/dowfrost-propylene-glycol-thermal-fluids/dowfrost-lc-25
- CoolIT rack manifolds (EIA / ORV3 / MGX, stainless, Staubli QDs): https://www.coolitsystems.com/products-services/server-products/rack-manifolds/
- CoolIT 4 kW tech brief (8 psi full-loop): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- NVIDIA Rubin cold-plate supplier list (TVBS / Digitimes): https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html
- Vendor GB200/GB300 plate dP figures (secondary): https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/
- Low-reliability vendor blog quoting 2-4 m/s channel velocity (flagged): https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling

Documents named from background knowledge (no URL verified this session; pull directly):
- ASHRAE TC 9.9, Thermal Guidelines for Data Processing Environments, 5th ed. (2021), liquid-cooling chapter (classes W17-W45, W+).
- ASHRAE TC 9.9, Liquid Cooling Guidelines for Datacom Equipment Centers, 2nd ed. (2014).
- ASHRAE TC 9.9 white paper, Water-Cooled Servers: Common Designs, Components, and Processes (2019).
- OCP ACS Cold Plate Requirements (ORv3 era, ~2021-22) and OCP ACS Liquid Cooling Guidelines / Facility Water System guidelines.
- OCP ORv3 Rack and Blind-Mate Manifold specifications.
- Intel Xeon Thermal Mechanical Specification and Design Guides (TMSDG); AMD SP5 / Instinct thermal design guides.
- Uptime Institute annual data-center surveys (2024, 2025) and DLC guidance notes.
- ISO 16232 (cleanliness of fluid components), ISTA 3A/3E and ASTM D4169 (shipping), AIAG PPAP manual.
