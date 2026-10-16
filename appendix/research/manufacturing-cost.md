# Manufacturing routes, geometric limits, cost and reliability for high-performance copper cold plates

*Research angle: "how do we build a plate that beats CoolIT's 15 kW Split-Flow skived plate, and what does it cost at 10k-1M units/yr?" Compiled 2026-10-13 for the cold-plate programme.*

## 0. Provenance and method (read first)

- **Zero live web searches were executed by this agent.** The per-turn WebSearch budget (200 calls, shared by all agents in this workflow) was already exhausted when this agent started; all 8 queued queries were refused. WebFetch/curl are network-blocked in this container (one curl attempt: proxy 403). I did not work around the limit.
- Every number below is tagged:
  - **[Brief]** = read directly from the CoolIT 15 kW tech brief (June 2026) supplied locally.
  - **[Sib]** = taken from the sibling research files in this scratchpad (`coolit-products.md`, `coolit-briefs-numbers.md`, `competitors-singlephase.md`, `competitors-advanced.md`, `chip-roadmap-requirements.md`, `model_output.md`), which cite the URL for each fact; the URL is repeated here. Those agents read search-engine extracts, not full pages.
  - **[KB-H / KB-M / KB-L]** = the author's background knowledge of the cold-plate manufacturing industry (high / medium / low confidence), **not verified in this session**. Treat every KB cost figure as an engineering estimate to be confirmed by RFQ.
  - **[D]** = derived here.
- Vendor claims are marked (V); independent / peer-reviewed / standards data (I).

## 1. Executive summary

1. **CoolIT's 15 kW plate is a conventional-manufacturing plate**: in-house CNC + skiving at the Liquid Lab, Split-Flow geometry, "proven mass-manufacturing techniques", standard thermal paste [Brief]; the second 4 kW unit used the OMNI all-metal unibody joining (no braze), which a 2026 factory tour attributes to **friction stir welding** [Sib: coolit-products.md; https://www.datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale]. So the benchmark can be beaten with the same toolset plus one extra layer, not with powder-bed printing.
2. **The volume-incumbent GPU plate (GB200/GB300) is a skived C1100/C1020 copper core (fins <= 0.5 mm, >= 3 mm tall), brazed or welded copper cover, Ni-plated wetted path, ~US$300 ASP, rising to ~US$400 for Rubin** [Sib: fibermall; TechRadar/Morgan Stanley; igor'sLAB; TVBS/Digitimes]. Our estimated factory cost of that plate is **US$90-160** at 100k+/yr [KB-M], i.e. there is 2-3x gross margin for NVIDIA's Group-A suppliers (Jentech, AVC, Cooler Master, Delta) [Sib: https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html].
3. **Skiving's hard limits**: commercial fins 0.1-0.5 mm thick at 0.2-1.0 mm pitch, aspect ratio (height/thickness) ~10-25 in copper, finest demonstrated 0.06 mm fins at 0.10 mm pitch [Sib: USUSTK https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink]; straight, one-directional, uniform-height fins; no internal manifold possible in the same operation. The thermal consequence (from `model_output.md` [Sib]) is that a long-flow-length skived array at 18 LPM is stuck at conv ~12-13 K of the 34.4 K budget, and going to 0.1/0.1 mm fins in the *same* split-flow layout quadruples dP (8.6 -> 35 kPa).
4. **The lowest-cost way to beat skived performance is not to replace skiving but to add a manifold layer above it**: a photochemically-etched 0.2-0.3 mm copper laminate (1-2 sheets) forming a manifold-microchannel (MMC) distributor that cuts the fin flow length from ~50 mm to 2-3 mm. The model [Sib: model_output.md] shows that this lets 0.1/0.1 mm or 0.075/0.075 mm skived fins run at **6 kPa instead of 35 kPa while cutting avg dT from 34.5 K to ~24 K** (max 44 -> 28 K) at the same 18 LPM and the same paste. Etched copper sheet costs US$3-10 per layer at volume [KB-M]; the all-metal join (FSW or green-laser weld) costs the same as CoolIT's OMNI. **Estimated cost adder: US$10-25 per plate (+10-20 %) on a US$90-160 factory cost** [KB-M].
5. **ECAM (Fabric8Labs) is the only non-conventional route with both the resolution (30-50 um) and a credible volume story** (Wiwynn 4 kW double-sided plate; GIGABYTE and Wiwynn NexGen programmes 2026) [Sib]; peer-reviewed data (UIUC, Cell Reports Physical Science 2026) show -32 % R at equal flow / -68 % dP at equal R vs pin fins [Sib]. But its unit cost, throughput and plate-level R/dP at GB200 scale are unpublished; we rate it as the **second-source / Gen-2 route**, not the base route.
6. **Copper L-PBF (green-laser), binder jet, MIM, casting and extrusion do not make the cut for a GPU plate**: resolution (>= 0.2-0.3 mm walls / 0.4-0.5 mm channels for L-PBF), porosity/leak risk (binder jet, MIM), or material (aluminium) [KB-M]. L-PBF stays the prototyping and manifold-cover tool.
7. **Qualification floor** (OCP Cold Plate Test Spec v1.0.0, Oct 2026, CoolIT primary author): dP at 45 +/- 2 C at >= 6 flow points (25-150 % of rated), R = (Tcase - Tin)/P with the recommended TIM, **burst > 20 bar example, He leak <= 1e-5 mbar-L/s, thermal cycling 10-65 C and -40/+70 C** [Sib: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf]. JetCool's shipping datasheet shows the commercial convention: **72 psi (5 bar) continuous / 216 psi (15 bar) burst** [Sib: JetCool RTX PRO 6000 datasheet]. OCP allows TCS components to see up to **100 psi (6.9 bar)** [Sib: OCP L-LCDU]. Design target: 10 bar proof, >= 20-30 bar burst.

## 2. The benchmark's manufacturing fingerprint

| Item | What the brief / CoolIT material says | Manufacturing inference |
|---|---|---|
| Fin/channel core | "industry-leading internal geometries, proven mass-manufacturing techniques" [Brief]; 4 kW plate built with "standard CNC machining and skiving equipment" [Sib: coolit-briefs-numbers.md] | Skived OFHC copper, fins plausibly 0.1-0.3 mm / gaps 0.1-0.3 mm, centre of fin field removed for Split-Flow inlet [Sib: skived brief https://coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf] |
| Joining | OMNI: "single-metal unibody, aerospace-grade metallic sealing requiring no brazing material, eliminates CTE mismatch" [Sib: https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled] ; DCF tour: moved from brazing to FSW [Sib] | FSW copper lid-to-body (inference); OMNI claimed > 300 W/cm2 and "up to 60 % lower R vs standard microchannel" with undefined baseline (V) |
| TIM | "standard thermal paste" [Brief] | ~0.05-0.1 cm2-K/W -> 7-15 K of the 34.4 K budget at ~100-200 cm2 [Sib: model_output.md] |
| Coolant / flow | water-glycol, 1.2 LPM/kW = 18 LPM, 45 C in [Brief]; caloric rise ~12.6 K (PG25) [Sib] | 18 LPM through one plate implies coarse-enough channels to keep dP tolerable; dP not disclosed |
| Result | avg dT 34.4 K, worst TC 44.2 K, spread 12.4 K across 8 TCs, plate-to-plate spread at TC8 10.1 K [Brief] | plate-to-plate spread at a fixed TC points at TIM / mounting variability, i.e. a manufacturing/assembly tolerance issue, not a fluid design limit [Sib: coolit-briefs-numbers.md] |
| Factory | Calgary (Starfield 1 + 3, ~200,000 sq ft), China and Vietnam production, 100 % leak + functional test, AI optical screening [Sib: coolit-products.md] | CoolIT is a loop/CDU system house (US$550 M NTM sales) more than a commodity plate house |

## 3. Route-by-route: limits, cost, volume, reliability

### 3.1 Summary matrix

Unit costs are **factory cost per GPU-class plate (~100 x 120 mm, ~1-1.5 kg Cu), excluding QD/fittings**, at 10k / 100k / 1M units per year. All cost rows are [KB-M] estimates unless tagged; geometric limits are [KB-H] unless tagged.

| Route | Role in a plate | Min feature (fin / channel) | Max aspect ratio | Tooling / NRE | Unit cost 10k / 100k / 1M | Throughput per machine | Lead time to first parts | Key reliability issue |
|---|---|---|---|---|---|---|---|---|
| **Skiving (Cu)** | fin core, monolithic with base | 0.1-0.2 mm commercial; 0.06 mm / 0.10 mm pitch demonstrated [Sib: USUSTK]; GB200 norm <= 0.5 mm, >= 3 mm tall [Sib: fibermall] | 10-25 typical; ~40 with special blades, fin curl/tilt risk | none (blade + program); US$5-20k fixtures | US$25-40 / 18-28 / 12-20 (core only) | ~100-300 plates/day | 1-3 weeks | fin tip burr, fin wobble, base thinning; fouling if gap < 3-4x filter rating |
| **Micro-milling / CNC** | covers, ports, prototypes, local pockets | slitting saw slots 0.2-0.3 mm; micro end-mill 0.1 mm dia at AR <= 5-10 | 5-10 (end mill), 20+ (slitting saw) | none | US$60-150 / 25-50 / 15-30 (cover + finishing) | low for fine fins; fine for covers | days | tool deflection, burrs in channels |
| **Wire EDM** | prototype fin fields, tooling, stacked thin cores | 0.1 mm kerf with 0.05-0.07 mm wire; fins 0.1 mm | > 50 | none | US$150-400 per plate-equivalent, mm2/min cutting; multi-wire stacks reduce by 5-10x | very low | days | recast layer; cost |
| **Photochemical etching (PCE) of Cu foil** | manifold layers, jet-nozzle plates, microchannel laminates | 50-100 um features in 100-200 um foil (etch factor ~1:1 depth); holes >= ~1x foil thickness | n/a (through-cut or half-etch) | phototool US$0.5-3k | US$8-15 / 4-8 / 2-5 per sheet | 1,000s of sheets/day | 1-2 weeks | isotropic undercut, dimensional +/- 25-50 um |
| **Diffusion bonding of Cu laminates** | monolithic 3-D manifold-microchannel cores (Mikros Normal Flow, VACCO-style) | inherits PCE: 50-100 um channels | n/a | fixtures US$10-50k | US$60-120 / 35-70 / 25-50 (bonded core) | furnace batches of 50-500 plates per 6-12 h cycle | 6-10 weeks | annealed Cu (low yield strength), voids/unbonded zones, H2 embrittlement of ETP Cu (use C10100/C10200) |
| **Vacuum brazing** | cover-to-core join (industry incumbent) | n/a | n/a | fixtures US$5-30k | US$6-15 / 4-10 / 3-7 per join | batch furnace, 100s/cycle | 2-4 weeks | braze run-into-channel, voids -> leaks, filler corrosion (Ag/P), Cu annealing |
| **Friction stir welding (Cu)** | all-metal unibody lid (OMNI-class) | n/a; needs 3-5 mm lip | n/a | tooling US$1-5k per tool; machine US$0.5-1.5 M | US$10-20 / 6-12 / 4-8 | 50-300 mm/min on Cu; 1-3 min/plate | 4-8 weeks | tool wear on Cu, HAZ softening, exit hole, distortion |
| **Laser welding (green/blue)** | lid seam, port bosses | n/a; penetration 1-3 mm | n/a | fixtures US$10-30k; cell US$0.4-1 M | US$3-8 / 2-5 / 1.5-3 | m/min seam speed, < 1 min/plate | 4-6 weeks | keyhole porosity, spatter into channels, needs clean OFHC |
| **Electron-beam welding** | lid seam for premium/aerospace plates | n/a; deep penetration | n/a | chamber batch | US$15-40 / 10-25 / 8-15 | batch vacuum | 4-6 weeks | cost, vacuum cycle |
| **Stamping / deep drawing (Cu or SS cover)** | covers, port bosses, single-level manifold caps | 0.5-1 mm features; bend radii >= 1x t | n/a | progressive die US$30-120k | US$6-12 / 3-6 / 1.5-3 | 10-60 parts/min | 8-12 weeks | springback, must be brazed/welded to core |
| **Cu L-PBF (green laser)** | prototypes, complex manifolds/covers, low volume | walls 0.15-0.25 mm; channels >= 0.4-0.5 mm (powder removal); Ra 10-20 um | ~10 (unsupported) | none; machine US$0.6-1.5 M; powder US$80-150/kg | US$400-900 / 250-500 / n.a. | 10-30 cm3/h -> 2-6 plates/day | days | residual porosity, surface roughness in channels, powder trapped |
| **Binder jet Cu** | low-cost AM manifolds (not fins) | ~0.3-0.5 mm features; 15-20 % sinter shrink | low | none | US$60-120 / 30-60 / 20-40 | 100s of parts/day | 2-4 weeks | 93-97 % density, 80-90 % IACS, through-porosity -> leak risk unless infiltrated |
| **ECAM (Fabric8Labs)** | printed Cu fin/manifold directly on base; full plate | **30-50 um** features [Sib: UIUC/Cell Rep. Phys. Sci. 2026]; > 350 W/cm2 (V) [Sib: Wiwynn OCP 2025] | high (electrodeposited) | none; proprietary tool | **not published**; Fabric8 claims cost-competitive with skived at scale [KB-L] | not published; "massively parallel" (V) | weeks | pure electrodeposited Cu (99.9 %), room-temperature, no powder; bond to substrate and long-term PG25 data not public |
| **Metal injection moulding (Cu)** | small heat sinks only | 0.3 mm walls; parts < ~100 g | low | mould US$30-150k | US$5-15 per small part | high | 10-14 weeks | 95-98 % density, 80-90 % IACS, porosity -> not leak-tight unmodified |
| **Al extrusion** | power-electronics plates, EV | channels >= 1 mm, walls >= 0.8-1 mm | ~10 | die US$5-20k | US$5-20 | very high | 4-6 weeks | aluminium incompatible with Cu/PG25 mixed loops (galvanic) [Sib: chip-roadmap-requirements.md] |
| **Casting (Al die / Cu investment)** | coarse manifolds, EV | >= 1.5-2 mm | low | die US$50-200k | US$5-25 | very high | 10-16 weeks | porosity; not for microchannels |
| **Electroforming / LIGA (Ni, Cu)** | jet-nozzle plates, < 50 um micro-orifices | 5-50 um | 5-20 | mask set US$5-20k | US$15-40 per nozzle plate at 100k | moderate | 3-6 weeks | Ni in Cu loop (galvanic, but Ni is already the plating standard) |
| **Laser micro-drilling (ps/fs, green)** | jet-nozzle plates in 0.1-0.3 mm Cu sheet | 50-200 um holes, taper 2-5 deg | hole depth ~5x dia | none | US$5-15 per plate (100s-1,000s of holes at 100-1,000 holes/s) | high | days | taper/recast; cheap enough for volume |
| **Injection-moulded PPS / PPSU manifold** | polymer manifold cap + O-ring to Cu core (consumer-AIO and legacy server style) | 0.5-1 mm walls/channels | n/a | mould US$50-150k | US$2-5 / 1.5-3 / 1-2 | very high | 8-12 weeks | CTE mismatch (PPS 20-50 ppm/K vs Cu 17), creep at 60-70 C, O-ring ageing, permeation; hyperscalers now prefer all-metal (OMNI argument) |

### 3.2 Notes by route

**Skiving.** A single carbide blade shears a thin layer of the copper block and bends it upright; the fin is monolithic with the base (no fin-base interface resistance), which is why skived Cu beats bonded/folded fins and why it became the GB200 norm. Limits: fins are straight and parallel in one direction; fin thickness and pitch can be varied along the stroke by programming (zoned density over hot spots is cheap), but fin height is uniform unless machined after; fin tip is slightly curled; base under the fins is 1.5-3 mm minimum for stiffness. Blade width caps the fin-field width at roughly 100-250 mm per pass [KB-M]. Copper fins below 0.1 mm wobble and are hard to Ni-plate uniformly. Equipment: Japanese and Taiwanese/Chinese specialty builders plus in-house machines at the big heat-sink houses (Nakamura Mfg, Wieland Microcool, Alpha Novatech, Winshare, LORI, USUSTK) [KB-L; vendor names not verified this session]. CoolIT runs skiving in-house [Sib].

**Micro-milling / CNC.** Fine for covers, ports, Split-Flow inlet pockets, mounting features, and for prototype fin fields (slitting saws make 0.2-0.3 mm slots at AR 20 but one slot per pass). It cannot economically make <= 0.15 mm channels over 100 cm2. Five-axis CNC of a copper cover with integrated manifold channels is the typical "manifold layer" today at US$25-50 in volume; it is what the etched laminate replaces.

**Wire EDM.** The only subtractive route to 0.1 mm fins at aspect ratio > 50 in copper, but at mm2/min cutting rates it is a prototype and tool-making process. Stacking 5-10 thin fin cores and cutting with multi-wire machines is used for semiconductor-equipment heat sinks, not for US$300 plates [KB-M].

**Photochemical etching + diffusion bonding.** This is the laminate route behind Mikros Normal Flow (now Jabil) - "core thermal resistance as low as 0.02 C-cm2/W, > 1 kW/cm2 at 30 C rise and 3 psi" (V) [Sib: https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/] - and behind VACCO's aerospace microchannel heat exchangers and Heatric/Parker printed-circuit heat exchangers (etched + diffusion-bonded stainless at industrial scale) [KB-M]. Copper etches cleanly in ferric chloride / cupric chloride; 100-200 um foils give 50-100 um channels with +/- 25 um tolerance; through-holes down to ~1x foil thickness. Diffusion bonding of copper: ~800-950 C, 5-20 MPa, 1-4 h in vacuum or H2; the stack comes out fully annealed (yield ~60-80 MPa), so burst strength must come from wall thickness and the bonded cover, and ETP copper (C11000) must be avoided in H2 (steam-embrittlement) - use OFE C10100/C10200 [KB-H]. Bond quality (void-free) is the yield driver; ultrasonic C-scan or He leak at 100 % is required. A fully laminated plate (10-20 layers) costs US$60-120 at 10k/yr; a **1-2 layer etched manifold insert, brazed or welded with the lid, costs US$5-15** and is the sweet spot [KB-M].

**Vacuum brazing.** Incumbent join for brazed Cu covers: BAg-8 (72Ag-28Cu, 780 C) or BCuP (self-fluxing on Cu, but P-rich joints are brittle and P can be leached in inhibited glycol) [KB-M]. Issues: filler wicking into 0.2 mm channels (blocks fins; needs stop-off and tight gap control), voids -> leak escapes, and the brazing cycle anneals the skived core. Vacuum brazing avoids flux residues, which otherwise contaminate PG25 inhibitors. It is cheap (US$3-10 per join in volume) and well understood; CoolIT's OMNI pitch ("no brazing material, no CTE mismatch") is a reliability-marketing argument against this join and against stainless-on-copper or plastic-on-copper assemblies [Sib: StorageReview OMNI].

**Friction stir welding.** Standard for aluminium EV battery plates (millions/yr); on copper it needs W-Re or PCBN tools, 50-300 mm/min, high spindle loads, and a 3-5 mm wide lip, and it leaves an exit hole (run-off tab) [KB-M]. Advantages: no filler, hermetic, no dissimilar metal, no channel contamination, proof pressure limited by parent copper only. This is almost certainly CoolIT OMNI (inference) [Sib]. Capex US$0.5-1.5 M per cell; cost per plate US$4-12 at 100k+.

**Laser welding.** Copper reflects ~95 % of 1 um IR, but 515 nm green disk lasers (Trumpf TruDisk) and 450 nm blue diode lasers (Laserline, Nuburu) now weld copper reliably at 1-3 mm penetration; already used for EV hairpins/busbars at high volume [KB-M]. Fastest and cheapest hermetic all-metal join (< 1 min per plate, US$1.5-5); porosity control requires clean, deoxidised OFHC surfaces and a welding-friendly lip design. **Recommended join for our base design**, with FSW as the alternative where the lip is thick.

**Electron-beam welding.** Best weld quality in copper (no reflectivity issue, deep narrow fusion zone) but vacuum cycle and chamber size make it US$8-25 per plate; appropriate for aerospace/HPC, not 1M/yr [KB-M].

**Stamping / forming.** Progressive-die stamped copper or 304/316 stainless covers with drawn port bosses cost US$1.5-6 in volume with US$30-120k tooling; they only give single-level manifolds (ribs/dimples) and must be brazed or welded to the core [KB-M]. Stainless covers on copper cores (used by some ODMs for cost and stiffness) need Ni-based or Ag-based braze and reintroduce the CTE mismatch OMNI criticises.

**Copper L-PBF.** Green-laser systems (Trumpf TruPrint with 515 nm, AMCM/EOS M 290 1 kW, Nikon SLM 280) now reach > 99.5 % density and ~95-100 % IACS in pure Cu [KB-M]. But the smallest leak-tight wall is ~0.2-0.3 mm, the smallest cleanable channel ~0.4-0.5 mm, roughness Ra 10-20 um, and a 1 kg plate takes hours at US$400-900. This is 3-8x the ASP of the incumbent plate; it serves prototypes, topology-optimised manifold covers at low volume, and marketing. Diabatix (ColdStream) is generative-design software, not a manufacturing route; its published cases (-25 % R, -50 % dP on an EV plate; -55 % R heatsink) are not GPU plates [Sib: https://www.diabatix.com/blog/optimizing-cold-plate-performance-through-generative-design].

**Binder jet copper and MIM.** Sintered copper from powder reaches 93-98 % density and 80-90 % IACS; residual interconnected porosity makes thin walls weep under He test unless infiltrated or over-sintered (then features coarsen). Both are size-limited (MIM < ~100 g) and coarse (>= 0.3 mm). Not GPU-plate routes [KB-M].

**ECAM (Fabric8Labs).** Electrochemical additive manufacturing deposits pure copper voxel-by-voxel at room temperature from an electrolyte, with no powder and no thermal step; the UIUC/Fabric8 topology-optimised plate used 30-50 um features and showed **-32 % R at equal flow, -68 % dP at equal R vs conventional pin fins** on a GaN array (I) [Sib: https://mechse.illinois.edu/news/82871 ; https://www.metal-am.com/copper-am-cold-plate-improves-ai-data-centre-cooling/]. Commercial traction: Wiwynn double-sided plate rated up to 4 kW (V), 3.5 kW plate at Computex 2025 "48 % better than skived" (V), OCP 2025 "200 % improvement in temperature variance" (V, no baseline), GIGABYTE collaboration July 2026, NexGen double-sided/two-phase plates Aug 2026 [Sib: 51-61 in competitors-singlephase.md]. **What is missing: any published K/W, kPa, unit price, or plates-per-day figure.** Fabric8 has publicly positioned ECAM as cost-competitive with legacy manufacturing [Sib: https://www.fabric8labs.com/ecam-vs-legacy-liquid-cooling-cold-plates/ ; cost claim strength KB-L]. Deposition rate is the physical cost driver (electrodeposition is um/min-class per voxel plane; parallelism across the build area is what makes it viable). Treat ECAM as the strongest second-source and as the route for a Gen-2 "conformal fin on power map" plate; secure a development agreement rather than betting the base design on it.

**Polymer manifolds vs all-metal.** PPS (Ryton/Fortron) and PPSU (Radel) injection-moulded caps with EPDM O-rings on a skived Cu core are the cheapest manifold (US$1-3) and were standard in consumer AIOs and early server loops; they fail the hyperscaler reliability narrative on creep at 60-70 C outlet, CTE mismatch under 10-65 C cycling, O-ring compression set, and glycol/inhibitor compatibility, which is precisely the argument CoolIT uses for OMNI [Sib: StorageReview OMNI]. All-metal (Cu-Cu welded) adds ~US$3-10 per plate over plastic-cap and is now table stakes for GB200-class procurement [KB-M].

## 4. Capability matrix for the three geometry classes we need

| Capability | Skiving | CNC | Wire EDM | PCE foil | PCE + diffusion bond | Cu L-PBF | Binder jet / MIM | ECAM | LIGA / electroform | Laser drilling | Stamping | Polymer moulding |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| (a) < 100 um fins / channels over 100 cm2 | **Yes, marginal** (0.06-0.1 mm demonstrated, fragile, fouling-prone) | No (AR too low) | Yes (slow, costly) | **Yes** (50-100 um in 100 um foil) | **Yes** (monolithic) | No (>= 0.2-0.3 mm) | No | **Yes** (30-50 um) | Yes (small areas) | n/a | No | No |
| (b) Multi-level 3-D manifolds | No | Partial (2-level, costly) | No | **Yes** (as stacked layers) | **Yes** (best) | **Yes** (coarse) | Partial (coarse) | **Yes** | No | No | Single level only | **Yes** (coarse, polymer) |
| (c) Jet-nozzle plates (50-300 um orifices, 100s-1,000s) | No | No (> 0.3 mm drills) | Partial (slow) | **Yes** (>= 1x foil t) | Yes | No | No | Yes | **Yes** (finest) | **Yes** (cheapest) | Partial (>= 0.3 mm punched) | Partial (>= 0.3 mm) |
| Volume readiness (1M/yr) | Proven | Proven (covers) | No | Proven (PCB/EMI industry) | Proven in SS (PCHE); Cu at 10-100k | No | n/a | Unproven, scaling | Niche | Proven (EV, filters) | Proven | Proven |
| All-metal, PG25-compatible | Yes | Yes | Yes | Yes | Yes | Yes | Porosity risk | Yes (electrodeposited Cu) | Ni | Yes | Yes (Cu/SS) | No |

Important system constraint on (a): CDU/TCS filtration is typically 50 um nominal (some 25 um) [Sib: chip-roadmap-requirements.md], and the usual rule is channel gap >= 3-4x filter rating, so **< 100 um channels require a 25 um point-of-use strainer at the plate inlet** (adds 2-5 kPa and a service item) or acceptance of fouling risk. Our recommended core uses 100-150 um gaps with a 2-3 mm flow length rather than < 100 um gaps; the manifold, not the channel width, buys the performance.

## 5. Cost: what the incumbent plate costs and where the money goes

### 5.1 Market price points

| Item | Value | Source | Type |
|---|---|---|---|
| GB300 NVL72 liquid-cooling BOM | ~US$49,860 per rack; ~US$2,260 per compute tray | Morgan Stanley via TechRadar https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks ; igor'sLAB https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/ [Sib] | analyst (S) |
| GB300 CPU/GPU cold plate ASP | ~US$300; NVSwitch plate ~US$200 | same [Sib] | analyst (S) |
| Vera Rubin NVL144 cooling BOM | ~US$55,710 per rack; cold plates "up to US$400 per unit" | same [Sib] | analyst (S) |
| Rubin plate procurement | NVIDIA centralised purchasing; Group-A: Jentech, AVC, Cooler Master, Delta; plate ASP ~US$400 | https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html [Sib] | press (S) |
| GPU plate ASP range | US$300-500 | IDTechEx repost https://onartificialintelligence.com/articles/34213/two-phase-d2c-cooling-in-data-center-thermal-management-cost-analysis [Sib] | analyst (S) |
| AVC share of GB200/GB300 plates | ~40-50 % | https://news.tvbs.com.tw/english/3179423 ; https://www.taiwannews.com.tw/en/news/6215881 [Sib] | press (S) |
| GB200 plate design targets (secondary) | 1.8 LPM, 45 C, PG25, < 20 kPa, < 0.03 K/W, skived fins <= 0.5 mm | https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm [Sib] | vendor blog (S) |
| GB300 plate (secondary) | 0.013 K/W at 1.7 LPM, 12 kPa | https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ [Sib] | vendor (V) |

### 5.2 Estimated factory-cost teardown of a GB200-class skived/welded plate [KB-M; to be confirmed by RFQ]

| Cost element | 10k/yr | 100k/yr | 1M/yr | Notes |
|---|---|---|---|---|
| OFHC copper (1.2-1.5 kg incl. machining loss, Cu ~US$10-12/kg 2026) | 18 | 16 | 14 | copper price is the floor; recycle swarf |
| Skiving core | 35 | 22 | 15 | 2-5 min/plate |
| Cover (CNC or stamped) + ports | 40 | 18 | 8 | stamped at 1M |
| Join (braze or laser/FSW) | 12 | 7 | 4 | |
| Electroless Ni plating (wetted path) | 10 | 6 | 4 | 5-15 um mid-P EN |
| Mounting hardware, leaf spring, bracket, O-rings | 20 | 14 | 10 | |
| Hose stubs / fittings (QDs excluded) | 15 | 10 | 7 | |
| 100 % He leak + pressure test + flow/dP test | 8 | 5 | 3 | |
| Yield loss (95 -> 98 %), scrap, overhead | 12 | 8 | 5 | |
| **Factory cost** | **~170** | **~105** | **~70** | |
| ASP observed | 300-400 | 300-400 | n/a | implies 45-70 % gross margin at Tier-1 for Rubin-class plates |

### 5.3 Cost adders for the performance-beating options (per plate, 100k/yr) [KB-M]

| Option | Adder | Performance effect (from model_output.md [Sib], 117 cm2, 15 kW, 18 LPM, paste) |
|---|---|---|
| Finer skived fins 0.1/0.1 mm x 2 mm in the same split-flow layout | +US$5-10 (slower skive, more scrap) | avg dT 34.5 -> 25.0 K but **dP 8.6 -> 35 kPa** |
| Thinner base 2.0 -> 1.0 mm under the fins (stiffened by lid) | ~0 | -3.3 K |
| + etched Cu manifold laminate (1-2 layers, 2-3 mm flow length) + laser/FSW lid | **+US$10-25** | **avg dT 25 K at 6 kPa; max dT 44 -> 29 K** |
| + 0.075/0.075 mm fins (skived or etched) | +US$5-15 | -1 K more; needs 25 um point-of-use strainer |
| + thin-BLT paste (0.05 cm2-K/W) via flatness/pressure control | +US$2-5 (lapping, spring) | -2.6 K |
| Full etched+diffusion-bonded laminate core (Mikros-class) | +US$40-80 | similar or better h, best manifolds, lowest dP; higher capex and yield risk |
| ECAM printed core | unpublished; assume +US$50-150 today, trending to parity (V) | -32 % R / -68 % dP class (I, GaN test), power-map-conformal fins |
| Cu L-PBF full plate | +US$300-700 | not viable for volume |
| Liquid-metal or indium TIM instead of paste | +US$5-30 + handling risk | -4.5 to -5.4 K (biggest single lever after the manifold) |

### 5.4 Tooling, lead time and volume capability

| Route | NRE | Prototype lead time | Time to 100k/yr capacity | Capex per 100k/yr |
|---|---|---|---|---|
| Skiving + CNC cover + braze | US$20-50k fixtures | 2-4 weeks | 3-6 months (machines are the constraint; ~100-300 plates/day each) | US$2-4 M |
| + etched manifold laminate | +US$5-10k phototools/fixtures | +1-2 weeks | PCE capacity is abundant (PCB/EMI shielding industry) | +US$0.3-0.5 M (bond/weld fixtures) |
| Laser-weld lid | US$30-60k fixtures | 4-6 weeks | 3 months | US$0.5-1 M per cell |
| FSW lid | US$30-60k | 4-8 weeks | 3-4 months | US$0.5-1.5 M per cell |
| Etched + diffusion-bonded core | US$50-150k | 6-10 weeks | 6-12 months (furnace capacity) | US$3-6 M |
| ECAM | development agreement | weeks (V) | unknown | unknown (Fabric8-owned) |
| Cu L-PBF | none | 3-7 days | not a volume route | US$0.6-1.5 M per machine (2-6 plates/day) |
| Stamped cover | US$30-120k die | 8-12 weeks | immediate once tooled | low |

Scale check [D]: an NVL72 rack carries ~72 GPU + 36 CPU + switch/VR plates (order 120-150 plates). Industry shipments of order 30-50k GB-class racks/yr in 2026 imply **4-7 M plates/yr**, which is why AVC's 40-50 % share and NVIDIA's four Group-A suppliers matter: the manufacturing route we choose must be sourceable at >= 100k plates/month from at least two Taiwanese/Chinese/Vietnamese houses, or we remain a niche vendor.

## 6. Plating, coolant compatibility, leak and burst requirements

| Requirement | Value | Source / confidence |
|---|---|---|
| Coolant | PG25 (25 % propylene glycol + inhibitors) is the OCP base spec and NVIDIA's fluid | https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/ ; OCP PG25 Guidelines V1.0.0 (Oct 2026) https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf [Sib] |
| Wetted materials | copper wetted path standard; stainless manifolds; **no aluminium** in mixed-metal PG25 loops (galvanic) | [Sib: chip-roadmap-requirements.md] ; Lenovo mixes some Al plates only within its own loops [Sib] |
| Nickel plating | Electroless Ni (mid-phosphorus, 5-15 um) on wetted copper is the de-facto NVIDIA/ODM practice for GB200-class plates to suppress copper-ion release, biofouling and galvanic coupling with stainless; plating thickness must be subtracted from channel gap (2 x 10 um = 20 % of a 100 um gap) and EN throwing power inside deep sub-150 um channels is poor (solution exchange), so **plate before skiving-field closure or accept 50-100 % thickness gradient** | [KB-M]; secondary vendor pages mention Ni-plated Cu for GB200/GB300 plates [Sib: fibermall; tonecooling] - not verified against an NVIDIA document |
| Velocity limits | copper channels <= 1.5-2.0 m/s continuous (erosion-corrosion), stainless <= 3 m/s | [KB-M; Sib: chip-roadmap-requirements.md] |
| Filtration | 50 um nominal at CDU (some 25 um); gap >= 3-4x filter rating -> >= 0.15-0.2 mm for 50 um | [Sib: chip-roadmap-requirements.md] |
| Pressure drop budget | plate < 20 kPa (GB200 secondary target); tray <= 70-100 kPa; CDU secondary head: CoolIT CHx2000 53 psi, Google Deschutes 80 psi, OCP TCS components up to 100 psi | [Sib: fibermall; coolit-products.md; https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/ ; https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/] |
| Proof / burst | OCP test spec example burst > 20 bar; JetCool datasheet 72 psi continuous / 216 psi burst; our target: 10 bar proof, >= 20-30 bar burst | [Sib: OCP Cold Plate Test Spec V1.0.0 ; JetCool RTX PRO 6000 datasheet https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf] |
| Leak test | He mass-spec <= 1e-5 mbar-L/s (OCP); typical production: He sniff/vacuum at 1e-6 to 1e-5 mbar-L/s plus pressure decay at 1.5x MAWP, 100 % of units | [Sib: OCP spec]; practice [KB-H] |
| Thermal cycling | 10-65 C operating and -40/+70 C non-operating cycles | [Sib: OCP spec] |
| Negative-pressure loops (Chilldyne) | available head < 1 atm minus margin -> low-dP plates only (< ~30 kPa) | [Sib: competitors-advanced.md] |

Manufacturing implications: (1) any braze filler must be Ag- or P-free-compatible with PG25 inhibitor packages or be isolated by Ni plating; (2) laser/FSW all-copper joins avoid the filler question entirely; (3) EN plating is best applied to the skived core and the etched manifold layer *before* joining (both open geometries) and the weld zone masked or left bare copper with a post-weld local passivation; (4) burst > 20 bar on an annealed (brazed or diffusion-bonded) copper lid of 100 x 120 mm needs ~3-4 mm lid thickness or ribs, whereas a cold-worked laser-welded lid can be 2-2.5 mm [KB-M].

## 7. Reliability by joining architecture

| Architecture | Failure modes | Mitigation | Field evidence |
|---|---|---|---|
| Skived Cu core + Cu cover, vacuum brazed (incumbent) | braze voids, filler wicking into fins, inhibitor attack on filler, annealed core, CTE fine (Cu-Cu) | stop-off, gap control, 100 % He test, Ni plate after braze | millions fielded in GB200 [Sib: AVC share]; no public MTBF |
| Skived Cu core + SS cover brazed | CTE mismatch (Cu 17 vs SS 16-17 ppm/K is close for 304; 430 SS lower), Ni-braze cost, galvanic couple inside loop | Ni plating; avoid | used by some ODMs for stiffness/cost [KB-L] |
| All-Cu unibody FSW / laser (OMNI-class) | HAZ softening, exit hole (FSW), porosity (laser), lip width consumes footprint | parameter control, run-off tabs, pre-weld cleaning | CoolIT OMNI since May 2024, > 1.5 kW (V) [Sib] |
| Etched + diffusion-bonded laminate | unbonded zones, annealed Cu, H2 embrittlement if ETP | OFE Cu, C-scan, 100 % He, thick outer plates | Mikros/Jabil Ascutney AX-NV1/NV2 exist [Sib]; aerospace PCHE heritage [KB-M] |
| Polymer manifold + O-ring | creep, compression set, permeation, CTE | derate T, EPDM, captured O-ring | legacy consumer/server loops; declining [KB-M] |
| Cu L-PBF monolithic | residual porosity, rough channels (fouling), powder residue | HIP, chemical polishing | prototypes only |
| ECAM | substrate bond, long-term PG25 exposure, unknowns | qualification with Wiwynn/GIGABYTE in progress | Wiwynn 4 kW plate (V), no field data [Sib] |

Fouling and corrosion: the UTA accelerated-degradation work on copper in PG25 loops [Sib: https://uta-ir.tdl.org/uta-ir/handle/10106/31381] and Ecolab's own commissioning messaging (Ecolab now owns CoolIT, US$4.75 bn, closed July 2026) [Sib: coolit-products.md] both point to sub-0.3 mm channels being water-quality-sensitive; the OCP leak-detection white paper [Sib: https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1] sets the system-side expectations. A short-flow-length manifold design is intrinsically more fouling-tolerant than a long serpentine of the same gap because every channel is only 2-3 mm long and fed in parallel.

## 8. Lowest-cost route to beat skived-fin performance (recommendation)

**Base architecture ("Skive + Etch + Weld", all-metal, conventional):**

1. **Core**: OFE copper, skived fins, **0.1 mm fin / 0.1-0.15 mm gap / 1.5-2 mm tall** over the GPU/HBM footprint, fin density programmed to the power map (denser over the TC5-class hot zone); base thinned to 1.0-1.2 mm under the fins (lid-stiffened). Cost: skived core US$20-30 at 100k [KB-M].
2. **Manifold**: 1-2 photochemically-etched copper laminates (0.2-0.3 mm each) forming alternating inlet/outlet slots perpendicular to the fins at 2-3 mm pitch (manifold-microchannel), plus optional 100-200 um etched or laser-drilled jet orifices over hot spots. Cost US$5-15 [KB-M].
3. **Lid**: stamped or CNC copper cover with the two-plenum distributor, joined by **green-laser welding** (or FSW) - all-copper unibody, no braze, no polymer, no CTE mismatch (matches OMNI's reliability pitch). Cost US$8-15 [KB-M].
4. **Finish**: electroless Ni on core and laminate before assembly; 100 % He leak at <= 1e-5 mbar-L/s; dP and R characterised per OCP Cold Plate Test Spec v1.0.0.
5. **TIM**: thin-BLT paste with controlled flatness/pressure as baseline (removes 2-3 K); liquid-metal or indium option as a qualified SKU (removes another 4-5 K) [Sib: model_output.md].

**Expected result at the benchmark condition (15 kW, 18 LPM, 45 C, paste, 117 cm2 assumed)**: avg dT ~24 K vs 34.4 K, max dT ~28-29 K vs 44.2 K, plate dP ~6 kPa vs an estimated ~9 kPa for the benchmark (undisclosed), pumping power ~2 W [Sib: model_output.md, +/- 25 %]. **Factory-cost adder US$10-25 on a US$90-160 plate; capacity path identical to the incumbent (skiving houses + PCE houses + laser-weld cells).**

**Why this is the cheapest winning route**: it keeps the two proven high-volume processes (skiving for fins, etching for thin sheet) and swaps the join to one that is already cheaper than brazing (laser). Every alternative that can also beat skived performance costs more: a full diffusion-bonded laminate (+US$40-80), ECAM (unpublished, likely +US$50-150 today), L-PBF (+US$300-700). ECAM is the right **Gen-2 / second source** because it is the only route that can print fins conformally to the power map at 30-50 um and has ODM traction (Wiwynn, GIGABYTE).

**Ranked alternatives**:

| Rank | Route | Beats benchmark? | Cost adder @100k | Volume risk | Verdict |
|---|---|---|---|---|---|
| 1 | Skive + etched manifold + laser/FSW lid | Yes (model) | +US$10-25 | low | **base** |
| 2 | Skive + CNC 2-level manifold cover + laser lid | Yes, slightly less (coarser manifold) | +US$15-35 | low | fallback if PCE supplier qualification slips |
| 3 | Etched + diffusion-bonded laminate core (Mikros-class) | Yes, best dP | +US$40-80 | medium (furnace capacity, yield) | premium SKU / optics & SiC |
| 4 | ECAM core (Fabric8) | Likely (I: -32 % R / -68 % dP on GaN) | unpublished | high (single supplier) | Gen-2, second source |
| 5 | Jet-plate (laser-drilled Cu sheet) over skived or flat base (JetCool-style) | Yes on hot spots; dP higher | +US$10-20 | low | hybrid option for > 300 W/cm2 zones |
| 6 | Cu L-PBF | Yes | +US$300-700 | none at volume | prototypes only |
| 7 | Polymer manifold on skived core | Yes thermally, no on reliability | -US$5 | low | rejected (OMNI argument) |

## 9. Power-electronics (SiC converter) variant

Same core architecture serves SiC/GaN 800 VDC power stages (100-300 W/cm2 die flux, Tj 150-175 C, 20-40 kW per MW rack) [Sib: chip-roadmap-requirements.md], but the industry norm there is a **direct-cooled pin-fin baseplate** (forged Cu or Al pin fins integral to the module baseplate, O-ring sealed into a cast or extruded aluminium housing) with 50/50 WEG at up to 65 C inlet and vibration/thermal-shock qualification (AQG 324 class) [KB-M]. Manufacturing route: forged Cu pin-fin baseplates (US$15-40), CAB-brazed or FSW aluminium housings (US$20-60), or our etched-manifold insert laid over a flat Cu baseplate. This is a separate SKU with aluminium-compatible loop chemistry, not a separate architecture [Sib: competitors-advanced.md].

## 10. Gaps / unknowns

- **No live search was possible for this agent**; every KB-tagged number (skiving aspect ratios, equipment vendors, per-process unit costs, plating practice, laser/FSW parameters, ECAM cost) needs confirmation by RFQ or vendor documents. Suggested follow-up queries: "skived fin minimum thickness 0.1 mm aspect ratio copper vendor datasheet", "Fabric8Labs ECAM throughput cost per cold plate", "NVIDIA cold plate nickel plating requirement wetted materials", "copper diffusion bonding microchannel cold plate cost", "green laser copper welding cold plate lid", "Wieland Microcool skived microchannel 0.1 mm", "Mikros Ascutney AX-NV2 datasheet pressure drop", "GB200 cold plate BOM teardown".
- CoolIT 15 kW plate: footprint, fin geometry, dP, whether OMNI joining was used, Ni plating, TIM thickness - all undisclosed [Brief].
- OMNI joining process (FSW inferred), its lip width, and the "> 300 W/cm2" / "60 % lower R" test conditions [Sib].
- ECAM: no published K/W, kPa, price, plates/day, or long-term PG25 data; Fabric8 cost-parity statements are vendor marketing.
- NVIDIA's actual wetted-material / plating specification for Group-A plates is not public; only secondary vendor blogs mention Ni-plated copper.
- Diffusion-bonded copper plate field reliability (Mikros/Jabil) and furnace capacity in Asia are unknown.
- GB200/Rubin plate cost teardowns are the author's estimates; analyst ASPs (US$300-400) are secondary (Morgan Stanley via press, IDTechEx repost).
- Filter rating vs channel gap rule (3-4x) is industry practice, not a standard; OCP PG25 Guidelines V1.0.0 (Oct 2026) may specify filtration - not read.
- "Sandvik" was listed in the task as a possible diffusion-bonding source; I know of no Sandvik cold-plate laminate product (Sandvik supplies strip/powder) - unverified either way.
- Whether a laser-welded 2-2.5 mm Cu lid reaches > 20 bar burst on a 100 x 120 mm plenum without ribs needs FEA/test.

## 11. Sources

Primary / standards:
- CoolIT 15 kW Tech Brief (June 2026), supplied locally (`appendix/pdf/brief.txt`).
- OCP Single-Phase Direct-to-Chip Cold Plate Test Specification V1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- OCP PG25 base specification v1.0.0: https://www.opencompute.org/documents/ocp-base-specification-pg25-v1-0-0-final-pdf/
- OCP PG25 Guidelines V1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
- OCP UQD design spec v2.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf
- OCP L-LCDU test methodology (TCS up to 100 psi): https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- OCP cold plate development and qualification white paper: https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/
- OCP cold plate leak detection white paper: https://opencompute.org/documents/acs-cold-plate-leak-detection-and-intervention-white-paper-pdf-1
- JetCool RTX PRO 6000 SmartPlate datasheet (72 psi / 216 psi burst): https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf

CoolIT:
- Skived Coldplate Technical Brief (Feb 2021): https://coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf ; https://datacenterknowledge.com/cooling/skived-coldplates-technical-brief
- 4000 W Technical Brief (Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- OMNI all-metal coldplates: https://coolitsystems.com/?p=4082 ; https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled
- DCF factory tour 2026 (FSW, Starfield): https://www.datacenterfrontier.com/cooling/article/55408060/dcf-tours-inside-coolit-where-ai-liquid-cooling-goes-to-scale
- 15 kW press release: https://www.coolitsystems.com/resources/news/15kw_press_release/

Cost / market:
- TechRadar (Morgan Stanley NVL72 cooling BOM): https://www.techradar.com/pro/got-a-spare-usd50-000-cooling-a-single-nvidia-blackwell-ultra-nvl72-rack-costs-as-much-as-a-tesla-model-y-and-its-only-going-to-get-more-expensive-with-new-racks
- igor'sLAB (US$300 plate, Rubin US$400): https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
- TVBS / Digitimes (Rubin Group-A suppliers, ASP ~US$400): https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html
- AVC share: https://news.tvbs.com.tw/english/3179423 ; https://www.taiwannews.com.tw/en/news/6215881
- IDTechEx ASP repost: https://onartificialintelligence.com/articles/34213/two-phase-d2c-cooling-in-data-center-thermal-management-cost-analysis
- FiberMall GB200 plate (secondary): https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm
- ToneCooling GB300 plate (vendor): https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/

Manufacturing routes / advanced:
- USUSTK finest skived fins (0.06 mm / 0.10 mm pitch): https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink
- Mikros Normal Flow performance: https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/ ; Jabil acquisition: https://www.businesswire.com/news/home/20241003396998/en/Jabil-Acquires-Mikros-Technologies-to-Support-Demand-for-Liquid-Cooling-in-AI-Data-Centers
- Fabric8Labs Hot Chips 2023: https://www.hc2023.hotchips.org/assets/program/conference/day2/FPGAs%20Cooling/Fabric8Labs%20-%202023%20Hot%20Chips%20-%20ECAM%20for%20Cooling%20High%20Performance%20ICs%20(2023.08.29).pdf
- UIUC / Fabric8 topology-optimised plate: https://mechse.illinois.edu/news/82871 ; https://www.metal-am.com/copper-am-cold-plate-improves-ai-data-centre-cooling/ ; https://www.hostingadvice.com/blog/a-novel-3d-printed-copper-tree-could-cut-ai-cooling-by-32/
- Fabric8 ECAM vs legacy: https://www.fabric8labs.com/ecam-vs-legacy-liquid-cooling-cold-plates/
- Wiwynn ECAM plates: https://www.wiwynn.com/technology/advanced-cooling/cold-plate-liquid-cooling ; https://www.wiwynn.com/news/wiwynn-showcases-next-generation-ai-infrastructure-and-cooling-advances-at-ocp-global-summit-2025 ; https://3dprinting.com/news/fabric8labs-and-wiwynn-to-demonstrate-ecam-cold-plate-technology-at-computex-2025/ ; https://www.d2pmagazine.com/2026/08/14/fabric8labs-wiwynn-collaborating-to-develop-nexgen-3d-printed-cold-plates-for-ai-data-centers/ ; GIGABYTE: https://www.gigabyte.com/fi/press/news/2436
- Diabatix: https://www.diabatix.com/blog/optimizing-cold-plate-performance-through-generative-design
- Motivair "no skived microchannels" plates: https://www.datacenterdynamics.com/en/news/motivair-launches-dynamic-cold-plates-without-skived-microchannels/
- ORNL CuW / diamond pin-fin plates (IJHMT 2026): https://www.sciencedirect.com/science/article/pii/S0017931025014152 ; https://www.electronics-cooling.com/2026/04/high-performance-copper-tungsten-cold-plates-for-direct-to-chip-single-phase-liquid-cooling/
- Scalably etched copper cold plates (IJHMT 2025): https://www.sciencedirect.com/science/article/pii/S0017931025012736
- Bio-inspired Cu manifold microchannel (Energy 2025): https://www.sciencedirect.com/science/article/abs/pii/S0360544225049114
- Kisitu & Ortega split-flow analysis: https://par.nsf.gov/biblio/10341820
- Copper corrosion in PG25 loops (UTA thesis): https://uta-ir.tdl.org/uta-ir/handle/10106/31381
- Google Deschutes CDU 80 psi: https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/

Internal (this workflow): `model_output.md` (1-D series-resistance model, +/- 25 %), `coolit-products.md`, `coolit-briefs-numbers.md`, `competitors-singlephase.md`, `competitors-advanced.md`, `chip-roadmap-requirements.md`.
