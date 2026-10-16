# Cold-plate / direct-liquid-cooling physics options: quantitative literature review against the CoolIT 15 kW benchmark

Prepared 2026-10-13 for the "beat the CoolIT 15 kW coldplate" architecture program (Workflow 1, physics-and-literature angle).

**Method and provenance note (read first).** The shared per-turn WebSearch budget (200 calls across all agents) was already exhausted when this sub-task started, so **zero new web searches were run here** and WebFetch/curl are blocked by network policy. Every number below is therefore tagged:

- **[U]** = number with a URL, harvested from the sibling research notes written earlier in this run (coolit-briefs-numbers.md, coolit-products.md, competitors-singlephase.md, competitors-advanced.md), which were themselves built from ~100 web searches today. URLs are reproduced in the Sources section.
- **[M]** = our own first-principles model output (appendix/model_output.md and physics/run1.txt: 1-D series resistance network + 2-D conduction hot-spot solver, calibrated to reproduce CoolIT's 34.4 K at 15 kW / 18 LPM PG25 / 45 C with a 117 cm2 footprint, 128 W/cm2). Treat as +/-25 %.
- **[LK]** = literature knowledge from the named paper (author, journal, year, DOI where known), **not re-verified online in this session**. These are the classic, heavily-cited results; the numbers are given to the precision I am confident of, and anything softer is marked "approx." or given as a range. They must be spot-checked against the papers before being quoted externally.
- **(V)** vendor claim, **(I)** independent / peer-reviewed / standards body.

---

## 0. The benchmark, restated in physics terms

| Quantity | Value | Basis |
|---|---|---|
| Power, flow, inlet | 15 kW, 18 LPM (1.2 LPM/kW) water-glycol, 45 C | CoolIT brief [U] |
| Mean case-to-inlet dT | 34.4 K (TC range 26.8-44.2 K; 3 plates x 8 TCs) | CoolIT brief [U] |
| Absolute R_case-inlet | 0.00229 K/W mean, 0.00295 K/W worst TC | derived [U] |
| Fluid caloric rise (PG25, cp 3.93 kJ/kgK, 0.301 kg/s) | 12.7 K outlet; 6.3 K to mean fluid | energy balance [M] |
| Hot spot | TC5 is +8.8 K above the grand mean on all three plates (systematic, not random); plate-to-plate residual std 2.5 K (TIM/assembly scatter) | run1.txt s.7 [M] |
| Footprint / heat flux | undisclosed; 117 cm2 / 128 W/cm2 reproduces 34.4 K with a skived split-flow model (0.2/0.2 x 4 mm fins, 2 mm base, paste 0.07 cm2K/W) | [M]; sibling note infers 61-100 cm2 / 150-250 W/cm2 from the 4 kW plate's ~0.18 cm2K/W [U] |
| Calibrated resistance budget (34.5 K) | caloric 6.3 + TIM 9.0 + base conduction 6.6 + convection 12.6 K | [M] |
| Implied unit resistance | ~0.27 cm2K/W (117 cm2) ; 0.15-0.23 cm2K/W if the footprint is 64-100 cm2 | [M], [U] |
| Pressure drop | **not disclosed**; model estimate ~9 kPa plate-only; CoolIT's 4 kW plate: 8 psi (55 kPa) full loop incl. QDs at 6 LPM | [M], [U] |

The budget decomposition is the key to ranking levers: at 1.2 LPM/kW roughly **18 % is caloric (fixed by flow), 26 % TIM, 19 % base conduction, 37 % convection**. The hot-spot excess (+9.8 K worst TC over mean) is a fifth, separate target. A credible "beat in every aspect" design has to attack TIM, convection and hot-spot simultaneously while *lowering* pressure drop, which is exactly what a short-flow-length manifold geometry plus a better interface does.

---

## 1. Parallel microchannel heat sinks (Tuckerman-Pease lineage)

| Item | Value | Source |
|---|---|---|
| Tuckerman & Pease 1981, Si microchannels 50 um wide x ~300 um deep, DI water, 1 x 1 cm | **790 W/cm2 at 71 K rise -> R'' = 0.09 cm2K/W**; flow 8.6 cm3/s; dP ~31 psi (~214 kPa) | IEEE EDL-2(5) 126-129, doi:10.1109/EDL.1981.25367 [LK] |
| Laminar fully-developed Nu (rectangular duct, H1/H2) | 4-8 depending on aspect ratio | Shah & London 1978 [LK] |
| Resulting wall HTC, water (k ~0.62 W/mK) | Dh = 0.5 mm: 6-10 kW/m2K; Dh = 0.2 mm: 15-25 kW/m2K; Dh = 0.1 mm: 30-50 kW/m2K; PG25 ~25 % lower | h = Nu k / Dh [LK]; model h = 10.2 (0.2 mm gap), 19.4 (0.1 mm), 38 (0.05 mm) kW/m2K [M] |
| Effective base-area HTC incl. fin area ratio (5-10x) and fin efficiency (0.5-0.8) | 100-350 kW/m2K | [M] s.0 of run1.txt |
| Typical commercial Cu microchannel plate unit resistance (incl. TIM) | 0.10-0.20 cm2K/W; ACT quotes "typical single-phase plate ~0.150 cm2K/W" (V) | [U] ACT cut sheet |
| Pressure-drop scaling (laminar) | dP = f Re (mu u L)/(2 Dh^2), i.e. dP ∝ u L / Dh^2 and, at fixed total flow and plate area, dP ∝ L^2 / (Dh^2 x open fraction) | Shah & London [LK] |

**Physics take-away.** In laminar flow h ∝ 1/Dh but dP ∝ L/Dh^2, so halving the channel width doubles h and quadruples dP for the same flow length. The only way to get fine-channel h without the dP is to shorten L, which is the manifold argument in section 3. Model: going from 0.2/0.2 x 4 mm to 0.1/0.1 x 2 mm fins on the CoolIT-like 54 mm flow paths cuts convection 12.6 -> 6.4 K but raises dP 8.6 -> 35 kPa; feeding the same fins through a 2 mm-flow-length manifold gets the same 6.4 K at 6.1 kPa [M].

---

## 2. Skived-fin cold plates (the benchmark's own technology)

| Item | Value | Source |
|---|---|---|
| CoolIT skived RX3 CPU plate | <= 0.03 C/W (CPU class) | CoolIT skived brief 2021 [U] |
| Commercial fine limit for skiving | 0.06 mm fins at 0.10 mm pitch (USUSTK); GB200-class plates typically <= 0.5 mm fin/pitch, >= 3 mm high, target < 0.03 K/W and <= 20 kPa at 1.8 LPM | [U] |
| Older CoolIT CPU plates in peer-reviewed survey | 0.031 and 0.051 K/W on a 6.45 cm2 mock processor | Ramakrishnan et al., ASME JEP 141(4) 2019 [U] |
| Split-flow vs straight-through | similar R, lower dP; optimum channel aspect ratio ~12 | Kisitu & Ortega, InterPACK 2021 [U] |
| ToneCooling GB300 plate (V) | 0.0130-0.0133 K/W at 1.7 LPM, 12.06 kPa (1,067 W) | [U] |
| OCP OAI guideline 1 kW OAM (I) | case-to-inlet 0.015-0.016 K/W at 2-5 LPM PG25, phase-change TIM | OCP OAI Liquid Cooling Guidelines Mar 2023 [U] |

**Strengths:** fin and base are one piece (no joint resistance), cheap, mature. **Limits:** fin thickness/pitch floor ~0.1 mm in production, fin height/gap aspect ratio limited, and the geometry is inherently uniform (cannot be locally tailored to a heat map). The CoolIT split-flow halves the path length (54 mm on a 108 mm plate in our model), but the streamwise caloric ramp still produces a **5.4-7.9 K centre-to-edge case gradient** and a 20 % flow-starved channel adds another ~3 K at its exit [M run1 s.6].

---

## 3. Manifold microchannel (MMC) and hierarchical MMC heat sinks

| Item | Value | Source |
|---|---|---|
| Harpole & Eninger 1991 | first MMC concept/optimisation; predicted ~1 kW/cm2-class capability in Si at modest dP by feeding each short channel segment from a manifold | 7th IEEE SEMI-THERM, 1991 [LK] |
| Copeland, Behnia, Nakayama 1997 | isothermal MMC analysis; R'' of order 0.05-0.1 cm2K/W with dP a few tens of kPa | IEEE Trans. CPMT-A 20(2) 1997 [LK] |
| Escher et al. (IBM Zurich) 2010 "ultra-thin heat sink" | Si MMC, 2 x 2 cm: **R'' approx. 0.087 cm2K/W at 1.3 L/min, dP approx. 0.22 bar (22 kPa)** | ASME J. Heat Transfer 132, 081402, 2010 [LK, approx.] |
| Drummond, Weibel, Garimella et al. 2018 hierarchical MMC (HMMC), HFE-7100 two-phase | base heat flux approx. **910 W/cm2** at dP approx. 160 kPa; single-phase variant with background + hot-spot heating: background approx. 1 kW/cm2 and hot spots approx. 2.6 kW/cm2 | IJHMT 117 (2018) 319-330 and IJHMT 126 (2018) 1289-1301 [LK, approx.] |
| Jung, Weibel, Garimella et al. 2019, 3D-manifold embedded cooling for SiC | single-phase water, approx. 1 kW/cm2 class, R'' of order 0.05 cm2K/W | IJHMT 130 (2019) 1108-1119 [LK, approx.] |
| Stanford 3D manifold (Asheghi/Goodson) | 250 W/cm2 at Tmax 90 C with < 3 kPa at 0.1 L/min; simulations to 850 W/cm2 | [U] |
| PKU, Nature Electronics Sep 2025 (I) | 3-tier manifold + jet + sawtooth microchannel, 25 um channels: **3,000 W/cm2 at 0.9 W/cm2 pumping power; 1,000 W/cm2 at 65 K rise = 0.065 cm2K/W; COP 13,000** | [U] |
| Bio-inspired Cu manifold microchannel, Energy 2025 (I) | ~2 kW, 633 W/cm2, **25.2 kPa, 0.0878 cm2K/W** | [U] |
| Z-manifold cooler (2025 review) (I) | 1,800 W/cm2 at 6 g/s, 54 kPa, 0.075 cm2K/W | [U] |
| Mikros "Normal Flow" (V, Jabil) | core R'' 0.02 cm2K/W (< 0.018 optics); > 1 kW/cm2 at 30 K rise and ~20.7 kPa | [U] |
| Our HMMC model at the benchmark point (117 cm2, paste 0.05) | avg dT 24.1 K (fins 0.1/0.1 x 1 mm), 22.0 K (0.075 mm), 19.8 K (0.05 mm); dP 6.2-6.7 kPa; max dT 28.1 / 26.0 / 23.8 K | [M] |

**Why MMC is the primary single-phase lever.** The manifold decouples h from dP: flow length drops from ~50 mm to 1-3 mm, so dP ∝ L falls 10-50x at equal channel size, and the saved dP budget buys 2-4x finer channels (h 2-4x). Equally important for a 4-heater, 100 cm2-class footprint: every parcel of fluid enters at T_in, so the streamwise caloric ramp becomes a 4 mm-period ripple that the copper base smooths to **< 0.6 K at the case** (vs 5-8 K centre-to-edge for the split-flow plate) [M run1 s.2, s.6]. Peer-reviewed MMC unit resistances cluster at **0.065-0.09 cm2K/W total** (PKU, Z-manifold, bio-inspired) versus ~0.15 for a conventional plate and ~0.27 inferred for the benchmark: a 2-3x unit-resistance gap that is real, published and achievable in copper by skiving/etching + a machined or stamped manifold layer (no powder-bed AM required).

**Risks:** manifold-to-channel maldistribution (section 14), more parts/joints (brazed or FSW manifold), and fine channels needing <= 50 um filtration.

---

## 4. Jet impingement arrays

| Item | Value | Source |
|---|---|---|
| Single-phase submerged water microjet arrays, stagnation-zone HTC | **100-300 kW/m2K** (area-averaged over the array 50-150 kW/m2K); jet Re 1,000-10,000, nozzle 50-500 um | Browne, Michna, Jensen, Peles, IJHMT 2010/2011; Rau & Garimella hybrid jet/microchannel (ASME JEP 2014) [LK] |
| Kandlikar & Bapat 2007 comparison | jets, sprays and microchannels all reach the 1 kW/cm2 class; jets win on local h, microchannels on pumping power at low flux | Heat Transfer Eng. 28(11) 911-923 [LK] |
| JetCool (Flex) H100 SmartPlate (V) | 0.021 K/W at 3.2 LPM (vs 0.122 air) | [U] |
| JetCool third-party test (V-reported) | **25 % lower total R incl. TIM vs tested microchannel plates "from 1 LPM up"** | [U] |
| JetCool RTX PRO 6000 datasheet (V) | Rjf 0.040-0.058 K/W over 0.6-1.8 LPM, 600 W, PG25 40 C; 72 psi continuous rating | [U] |
| Frore LiquidJet (V, Oct 2025) | 600 W/cm2 hot-spot at 40 C inlet; dP "4x lower" 6.5 -> 1.7 kPa (product page says 10x: inconsistent) | [U] |
| PKU jet-enhanced manifold (I) | see section 3: 0.065 cm2K/W at 1 kW/cm2 | [U] |
| Academic multi-microjet at 100 W/cm2 | high performance "at the expense of excessive pressure drop" | [U] (SQU/BJUT) |

**Physics.** A jet thins the boundary layer to ~ nozzle-diameter scale, giving h 3-10x a fully-developed channel at the stagnation point, but h decays within 1-2 nozzle diameters, so array-averaged h is governed by nozzle pitch, and spent-flow cross-flow degrades downstream jets unless each jet has a local return path (return-flow / "distributed return" designs, which is what JetCool, Frore and the PKU device all do; this is essentially a manifold with normal-impingement inlets). Unit resistance of the best jet devices is therefore the same ~0.06-0.09 cm2K/W band as MMC. **Downsides:** sub-100 um nozzles are fouling-sensitive (JetCool's own "avoiding filtration challenges" language; specify <= 50 um filtration), erosion/cavitation of Cu under high-velocity PG25 is a 10-year reliability question with no public data, and jet dP is rarely published. **Read-across:** a 25 % R reduction on the benchmark's ~28 K case-to-mean-fluid term is ~7 K, comparable to a fine-channel MMC at the same flow.

---

## 5. Hot-spot-targeted channels, counter-flow and multi-pass

| Item | Value | Source |
|---|---|---|
| Sharma, Tiwari, Poulikakos et al. 2015, hot-spot-targeted embedded microchannels | at equal max chip temperature the targeted design cut temperature non-uniformity roughly 2x and pumping power by > 2x versus uniform channels (hot-spot/background flux ratio ~5) | Applied Energy 138 (2015) 414-422 [LK, approx.] |
| Vafai & Zhu 1999 two-layer counter-flow microchannel | halves the streamwise base temperature gradient relative to single-layer at similar pumping power | IJHMT 42 (1999) 2287-2297 [LK] |
| Corintis (Microsoft partner) | "heat-map matched", AI-optimised channel topology; 65 % lower peak silicon temperature rise in-die | [U] |
| Our model: fin-scale interdigitated counter-flow HMMC | case max-avg 0.28 K -> 0.00 K (perfect distribution); group-scale counter-flow with 1 mm groups: 0.025 K | [M run1 s.5] |
| Our model: 4-zone parallel feeding (each heater its own fresh-inlet branch) | caloric term stays 6.3 K average but the zone-to-zone caloric difference goes to zero; flow can be apportioned to the TC5-type hot zone | [M] inference |
| Measured benchmark hot spot | TC5 +8.8 K above mean on all 3 plates; worst TC 44.2 K vs mean 34.4 K | [U] |

**Physics.** At fixed 1.2 LPM/kW the *average* caloric rise (6.3 K to mean fluid) is thermodynamically fixed; what design controls is (a) *where* the hot fluid is, (b) how much heat-transfer area and flow each zone gets. Three levers, in increasing cost: (1) a manifold/short-flow geometry removes the streamwise ramp (worth 5-6 K on *max* dT in the model: 34.8 -> 29.0 K at identical fins); (2) zoned flow allocation and locally finer fins under the hottest heater (TC5) can convert the +9.8 K worst-point excess into ~2-3 K, i.e. **-6 to -7 K on max case temperature at zero mean-dT cost**; (3) counter-flow interdigitation removes the remaining sub-K ripple, which is not worth its complexity for a copper plate (the base already smooths it) but is relevant for thin direct-to-die lids.

---

## 6. Two-phase flow boiling in microchannels

| Item | Value | Source |
|---|---|---|
| Mudawar & Bowers 1999, subcooled water, 0.4-2.5 mm tubes, very high velocity | CHF up to **27,600 W/cm2** (the record), at ~40 m/s and high subcooling: shows the ceiling, not a practical operating point | IJHMT 42 (1999) 1405-1428 [LK] |
| Lee & Mudawar 2009, HFE-7100 micro-channels, subcooled | heat fluxes approx. 1 kW/cm2 dissipated at low inlet temperature | IEEE Trans. CPMT 32(2) 453-465, 2009 [LK, approx.] |
| Qu & Mudawar 2003/2004, water microchannel flow boiling | HTC 20-60 kW/m2K; CHF ~ 200-300 W/cm2 for saturated water in 231 x 713 um channels; severe pressure-drop and parallel-channel instabilities; inlet restrictors needed | IJHMT 46 (2003) 2755-2771 and 47 (2004) 2045-2059 [LK] |
| Kandlikar 2010 CHF scale analysis | CHF in microchannels bounded by evaporation momentum vs surface tension; practical saturated-flow CHF for dielectrics 100-500 W/cm2 base area | Trans. ASME J. Heat Transfer 132 (2010) 081501 [LK] |
| Drummond/Weibel/Garimella HMMC two-phase | ~910 W/cm2 HFE-7100 (section 3) | [LK, approx.] |
| ACT two-phase cut sheet (V) | two-phase plate ~0.080 cm2K/W vs single-phase ~0.150 | [U] |
| Wiwynn two-phase (V) | 2.5 kW at 125 W/cm2, 45 C saturation | [U] |
| Parallel two-phase GPU plates, R245fa (I, 2026) | 2,300 W/chip (~300 W/cm2), total R of order 1e-3 K/W | [U] |
| Accelsius NeuCool "independent" B200 benchmark (V-published) | Tj **9 C lower** than factory single-phase at warm water; 54 C inlet matches single-phase at 45 C; flow ~0.3 LPM/kW | [U] |
| ZutaCore HyperCool (V) | 2,500 -> 2,800 -> "4,000 W+" per chip; no R, Tcase or dP published | [U] |
| Fluids | Novec 7000/7100 exiting manufacture end-2025 (PFAS); R1233zd(E), R1234ze, R515B, Opteon SF33 are the candidates; latent-heat x density is ~10x below water sensible capacity per litre at 12 K rise | [U], [LK] |

**Physics.** Boiling HTC (20-60 kW/m2K for dielectrics) is *not* higher than a fine single-phase water microchannel; the two-phase gains are (a) near-isothermal fluid (no caloric ramp: the 6.3 K average / 12.7 K outlet term disappears), (b) 3-4x lower volumetric flow and pump power, (c) higher allowable inlet temperature. The costs are CHF ceilings of a few hundred W/cm2 base area for dielectrics at practical mass flux, parallel-channel/manifold instabilities, vapour-quality maldistribution across a 4-heater footprint, a condenser/HRU instead of a plain water loop, refrigerant leak detection, and PFAS regulatory exposure. **Verdict for a 15 kW, 45 C facility-water, 1.2 LPM/kW benchmark:** two-phase cannot be judged on the same axis (different fluid and flow), and single-phase water at 0.065-0.09 cm2K/W already matches ACT's quoted two-phase unit resistance. It is the right *second SKU* (same manifold core, dielectric evaporator) for inlet-temperature-limited or flow-limited sites, not the lead architecture.

---

## 7. Embedded / intra-chip cooling (ICECool, Microsoft/Corintis, TSMC)

| Item | Value | Source |
|---|---|---|
| DARPA ICECool (2012-2016), Lockheed Phase I | embedded microfluidics cut thermal resistance ~4x; demo die at **1 kW/cm2 with 30 kW/cm2 local hot spots**; Phase II > 6x GaN MMIC RF output | [U] |
| IBM ICECool (Schultz et al.) | embedded two-phase R1234ze in radially-expanding channels in 3D-stack-compatible chips; several hundred W/cm2 at junction < ~70-80 C | ASME J. Electron. Packag. 138 (2016) [LK, approx.] |
| Georgia Tech (Bakir) micro-pin-fin intra-chip, single-phase water | ~1 kW/cm2 class; junction-to-inlet of order 0.01-0.03 cm2K/W | [LK, approx.; flagged unverified in sibling note] |
| Microsoft + Corintis (Sep 2025) | "up to 3x better heat removal than cold plates"; **65 % reduction in max silicon temperature rise**; channels etched in die backside; production "packaging, etching, manufacturing" still open | [U] |
| TSMC direct-to-silicon on CoWoS (ECTC 2025) (I) | > 2.6 kW sustained on a 3.3x-reticle test package, dT < 63 C | [U] |
| NTU embedded microfluidic diamond spreader | junction-to-fluid 0.02 K/W at 2,000 W (thinned GPU) | [U] |

**Physics.** Removing TIM1 + lid + TIM2 + base and putting water within ~100 um of the junction eliminates ~60-70 % of the lidded stack; the 65 % Microsoft figure is exactly that arithmetic. It requires the silicon vendor to etch, seal and warrant the die, so it is a **2028+ platform decision owned by Nvidia/AMD/TSMC/hyperscalers**, not a cold-plate vendor product. The practical reading for us: design the plate so the same manifold core becomes a **micro-channel lid / direct-to-die lid** (CoolIT itself lists "direct-to-die and micro-channel lids" as its next step [U]).

---

## 8. Direct-to-die / lidless cooling and TIM elimination

The benchmark's thermocouples sit at the heater (case) surface, so its 34.4 K already excludes TIM1 and die. The only interface inside the measured stack is **TIM2 = "standard thermal paste"**, which the model puts at ~9 K (26 %) of the 34.5 K budget.

| Interface | R'' (cm2K/W) | Notes / source |
|---|---|---|
| Thermal grease, typical lidded-GPU bond line (50-100 um, warped lid) | **0.05-0.20** | Shin-Etsu X23-7921-5 datasheet: 5.0 mm2K/W = 0.050 cm2K/W at 25 um / 20 psi; X23-8117: 0.061 [U]; thicker real bond lines 0.1-0.2 [LK] |
| Phase-change pad (Honeywell PTM7950) | 0.04-0.08 | [U] |
| Graphite / carbon-fibre pads | 0.05-0.15 | [LK] |
| Liquid metal (Ga-In-Sn, k 20-80 W/mK, 20-50 um) | **0.01-0.03** | [LK]; Naddod GB300 blog quotes 0.02 (low reliability) [U]; requires Ni/anti-diffusion barrier on Cu, no Al, gasket containment |
| Indium solder (k ~86 W/mK, 100-200 um incl. metallisation interfaces) | **0.005-0.01** | [LK]; standard TIM1 for Intel/AMD/Nvidia lids; needs reflow, CTE-matched or compliant stack |
| Sintered silver (k 150-250 W/mK, 20-50 um) | 0.002-0.01 | [LK]; power-module practice; die-attach, not field-serviceable |
| Direct-to-die (plate on bare die, water-side) | 0 (but CTE: Cu 17 vs Si 2.6 ppm/K) | ORNL used CuW for this reason; Google bare-die since TPUv4 [U] |

Model impact at 128 W/cm2 [M]: paste 0.07 -> 0.05 thin-BLT: **-2.6 K**; liquid metal (0.015): **-7.1 K**; indium (0.008): **-8.0 K**; direct-to-die: **-9.0 K** (and a thinner lid-free path). This is the single largest lever available at fixed flow, and it is the one CoolIT explicitly did not use.

---

## 9. TPMS / gyroid / lattice additive geometries and topology optimisation

| Item | Value | Source |
|---|---|---|
| TPMS (gyroid, Schwarz-D/P) heat-sink studies 2020-2024 | volumetric HTC and Nu per unit volume typically 1.5-3x pin-fin lattices; friction factor also 2-5x higher; at *equal pumping power* the thermal-hydraulic performance factor is ~1.0-1.5 | Kaur & Singh, Therm. Sci. Eng. Prog. 2021; Attarzadeh et al., Appl. Therm. Eng. 2021; Alteneiji et al. 2022 [LK, approx.] |
| L-PBF copper conductivity | pure Cu 300-380 W/mK depending on green-laser process; CuCrZr ~300-320 W/mK; surface roughness Ra 10-20 um; minimum wall ~0.15-0.3 mm | [LK] |
| Fabric8Labs / UIUC ECAM topology-optimised Cu plate (I, 2026) | **32 % lower R at equal flow; 68 % lower dP at equal R** vs conventional pin fins, on a 2x2 GaN array; 30-50 um features; ~1,000 optimisation iterations | [U] |
| Fabric8Labs Hot Chips 2023 (V) | 35 % R improvement, 100-1,000 W | [U] |
| Wiwynn / Fabric8 ECAM plates (V) | 4 kW double-sided; "48 % better than skived"; "> 350 W/cm2" | [U] |
| Diabatix generative design (V) | cold-plate case studies claim ~10-30 % R or dP improvements vs baseline | [U] blog pages |

**Real gains vs hype.** The thermal problem of a GPU cold plate is a *near-wall* problem: 80-90 % of the resistance sits in the first 1-2 mm above the base (TIM, base, fin root). TPMS lattices maximise surface area per *volume*, which helps heat exchangers and regenerators, not a plate whose heat enters through one face. In the laminar, low-Re regime of DLC the gyroid's tortuous path buys mixing that the flow does not need and dP it cannot afford. The genuinely useful AM/optimisation results are the *topology-optimised branching manifolds* (UIUC/Fabric8, Corintis), whose gain comes from flow distribution and local fin density, i.e. from the same physics as sections 3 and 5, and which can be reproduced by machined/etched/stamped manifolds plus skived or etched fins. Expected gain of a well-done TPMS core vs a well-done fine MMC at equal dP: **0 to -3 K**, with a conductivity penalty if printed in L-PBF Cu (base term +10-30 %).

---

## 10. Pin-fin arrays

| Item | Value | Source |
|---|---|---|
| Peles, Kosar et al. 2005-2007 micro-pin-fin heat sinks, water | Nu correlations for Re_d 10-1,000; staggered circular pins give 1.5-2.5x the h of a plain channel at 2-4x the dP; endwall effects dominate at H/d < 2 | IJHMT 48 (2005) 3615-3627 [LK] |
| ORNL diamond-shaped pin fins, 75 x 75 mm Cu plate, water, 1 kW (I, Mar 2026) | **6.9 K/kW incl. TIM (Cu), 9.0 K/kW (CuW), 9.0 kPa**; ~15 % lower R than straight microchannels; pins H 4 mm, S 0.5 mm, 1 x 4 mm | [U] |
| Brunschwiler et al. (IBM) interlayer pin-fin cooling | in-line/staggered pins for 3D stacks, several hundred W/cm2 per layer at ~1 bar | Microsyst. Technol. 2009 [LK, approx.] |

**Physics.** Pins add leading-edge boundary-layer restarts and wake mixing (h up 1.5-2.5x) but lose fin efficiency (round pins conduct worse than plates per unit base area) and raise dP. They are a good choice where the flow must turn or spread (under a manifold slot, around heater corners) and for CTE-matched materials that cannot be skived (CuW, Cu-diamond). Net: a secondary lever (-1 to -3 K) used locally, not a plate-wide architecture.

---

## 11. Surface enhancement (nanostructures, wettability)

| Item | Value | Source |
|---|---|---|
| Pool boiling, Si nanopillar / micro-structured surfaces | CHF 100 -> ~208 W/cm2 (>100 % enhancement); HTC 2-3x | Chu, Enright, Wang, Appl. Phys. Lett. 100, 241603 (2012) [LK] |
| Flow boiling, porous/nanowire coatings in microchannels | CHF +50-100 %, HTC +50-200 %, delayed instability | Kandlikar group; Yang et al. (Bakir/Chen) Nature Comm. 2014-ish [LK, approx.] |
| Single-phase laminar microchannels | roughness only matters for Re > ~1,000 (transition); nanocoatings add negligible area at the boundary-layer scale and risk fouling nuclei | Kandlikar et al., Phys. Fluids 2005 [LK] |

**Verdict:** zero lever for the single-phase product (0 K); 1.5-2x CHF margin for the two-phase SKU, where it is worth a sintered-copper or etched micro-structure on the evaporator floor.

---

## 12. Materials

| Material | k (W/mK) | CTE (ppm/K) | Role / source |
|---|---|---|---|
| Cu (OFHC) | 385-400 | 17 | base/fins; [LK] |
| Al 6061/6063 | 160-200 | 23 | low-cost power-electronics plates; model: Al base/fins +4.7 K at the benchmark point [M] |
| CuW (W80-90) | 170-210 | 6.5-8.3 | CTE-matched for direct-to-die; ORNL CuW plate 9.0 vs Cu 6.9 K/kW (+30 % R) [U] |
| Mo-Cu (Mo70Cu30) | 170-250 | 7-9 | lids, spreaders [LK] |
| AlSiC | 170-200 | 7-9 | baseplates for IGBT/SiC modules [LK] |
| Cu-diamond composites (Element Six, Sumitomo, Plansee) | 500-900 | 6-8 | spreaders/bases; machinable with difficulty; USD 10s-100s per cm2 [LK] |
| CVD diamond (Element Six TM-grade) | 1,500-2,200 | 1-2 | heat spreaders for GaN; NTU embedded diamond spreader 0.02 K/W at 2 kW [U]; price prohibitive at 100 cm2 |
| L-PBF Cu / CuCrZr | 300-380 / 300-320 | 17 | AM cores; k penalty 5-25 % [LK] |

Model sensitivity [M]: the Cu base conduction term is 6.6 K at 2 mm, 3.3 K at 1 mm. A Cu-diamond base (k 700) at 1 mm would be ~1.8 K (**-1.5 K**), a CVD-diamond spreader insert under the hottest heater **-2 to -3 K locally**. Thinning Cu is cheaper than exotic k: the 2-D solver shows a 1 mm base already smooths the HMMC fluid ripple to 0.28 K, so going from 2 to 1 mm costs almost nothing in hot-spot (0.06 -> 0.28 K) and gains 3.3 K [M run1 s.8]. Below ~0.8 mm, stiffness/flatness and maldistribution smoothing suffer.

---

## 13. Spreading resistance for non-uniform heating

| Item | Value | Source |
|---|---|---|
| Lee, Song, Au, Moran 1995 closed-form spreading resistance (circular source on finite disc with convective boundary) | R_sp = (1 - 1.410 e + 0.344 e^3 + 0.043 e^5 + 0.034 e^7) / (4 k a) x phi(tau, Bi) with e = a/b, tau = t/b | ASME/JSME Thermal Eng. Conf. 1995 [LK] |
| Yovanovich, Muzychka, Culham 1999 isoflux rectangles on compound flux channels | general series solution; for a source occupying > ~50 % of the spreader, spreading < 10 % of 1-D conduction | J. Thermophys. Heat Transfer 13(4) 495-500 [LK] |
| Half-space limit | R_sp = 1/(4 k a) for a circular source radius a (k = 390, a = 5 mm: 0.13 K/W) | [LK] |
| Benchmark relevance | four heaters (GPU + HBM zones) nearly fill the footprint; with a 1-2 mm base and h_eff 100-340 kW/m2K the "spreading length" sqrt(k t / h_eff) is only 1-3 mm, so the plate cannot spread between zones and each heater is cooled by the fins directly above it. The +8.8 K TC5 hot spot is therefore a *local flux / local flow* problem, not a spreading problem | [M] inference |

**Design consequence:** do not try to fix hot spots with thick or exotic spreaders (they add 1-D resistance everywhere); fix them with local fin density and local flow (section 5). A spreader is justified only for direct-to-die on a small, very-high-flux die (> 300 W/cm2) where the spreader area can exceed the die area several-fold.

---

## 14. Flow maldistribution in manifolds

| Item | Value | Source |
|---|---|---|
| Bajura & Jones 1976; Kumaran et al. 2013 | Z-type (opposite-end) headers give the worst maldistribution, U-type and tapered headers the best; keep header flow area >= 4-10x the sum of channel areas and header velocity head << channel dP to hold channel-to-channel flow within +/-10 % | ASME J. Fluids Eng. 98 (1976); Appl. Therm. Eng. 58 (2013) 205-216 [LK] |
| Our model, split-flow plate | a 10 % / 20 % starved channel adds +0.9 / +1.8 K at its exit; a +/-20 % half/half pattern gives 8.4 K max-avg | [M run1 s.6] |
| Our model, HMMC | +/-20 % long-wavelength maldistribution adds only 1.4-1.9 K to max-avg because each cell's rise is 12.7/(1+e) K and the base smooths adjacent cells | [M run1 s.4, s.8] |
| Drummond/Weibel HMMC | inlet/outlet manifold symmetry and slot taper were required to keep per-channel flow uniform; non-uniform inlet distribution explicitly degraded hot-spot performance | [LK, qualitative] |

**Physics.** Maldistribution sensitivity scales with the per-channel caloric rise and the flow length; the short-flow manifold is 4-5x more tolerant than the split-flow plate for the same percentage error. The manifold layer therefore needs (a) a tapered/U-type feed with area ratio >= 5, (b) per-zone orifices sized by CFD to the heat map, (c) a CFD-validated +/-10 % spec, and (d) a low enough channel dP that header dynamic head is negligible (6 kPa plate dP helps here).

---

## 15. Pumping power vs thermal resistance Pareto

| Design (117 cm2, 15 kW, 18 LPM PG25, 45 C) | avg dT (K) | max dT (K) | dP (kPa) | hydraulic power (W) | source |
|---|---|---|---|---|---|
| CoolIT-like skived split-flow (0.2/0.2 x 4 mm, 2 mm base, paste 0.07) | 34.5 | 44.3 | 8.6 | 2.6 | [M] (dP not disclosed by CoolIT) |
| same, 1 mm base | 31.2 | 41.0 | 8.6 | 2.6 | [M] |
| same, fins 0.1/0.1 x 2 mm, still 54 mm flow length | 25.0 | 34.8 | 35.4 | 10.6 | [M] |
| HMMC 0.1/0.1 x 2 mm, 2 mm flow length | 25.0 | 29.0 | 6.1 | 1.8 | [M] |
| HMMC-fine 0.075 mm, thin-BLT paste 0.05 | 22.0 | 26.0 | 6.3 | 1.9 | [M] |
| HMMC-ultrafine 0.05/0.05 x 0.6 mm, paste 0.05 | 19.8 | 23.8 | 6.7 | 2.0 | [M] |
| HMMC + liquid-metal TIM | 19.7 | 23.7 | 6.2 | 1.9 | [M] |
| HMMC + indium | 18.8 | 22.8 | 6.2 | 1.9 | [M] |
| HMMC direct-to-die | 17.1 | 21.1 | 6.2 | 1.9 | [M] |
| HMMC-ultrafine + liquid metal (stacked, estimate) | ~15.3 | ~19.5 | ~6.7 | 2.0 | [M] arithmetic |
| Reference: Mikros Normal Flow (V) | 30 K at 1 kW/cm2 | - | 20.7 | - | [U] |
| Reference: ORNL Cu diamond pin-fin 1 kW (I) | 6.9 K | - | 9.0 | - | [U] |
| Reference: OCP TCS budgets | rack 18 psi (124 kPa) at 1.2 LPM/kW; CDU head >= 40 psi at 1.5 LPM/kW; Google Deschutes 80 psi available; components to 100 psi | [U] |

Classic result (Knight, Goodling, Hall 1991-92, ASME JEP 113/114 [LK]): for a fixed pumping power the optimum laminar microchannel sits at the largest fin count the dP allows; the manifold shifts that frontier by replacing L with L/N. At the benchmark's flow, the model's **HMMC Pareto point is simultaneously ~30-45 % lower dT and ~25-30 % lower dP** than the calibrated skived split-flow plate; hydraulic power is < 0.02 % of the 15 kW in every case, so the dP budget is really about CDU head, rack manifolds and negative-pressure compatibility (Chilldyne-type loops cap plate dP well below 1 bar [U]), not energy.

---

## 16. Ranked levers by expected dT reduction at fixed 1.2 LPM/kW (benchmark footprint, 45 C inlet)

Baseline: 34.4 K mean / 44.2 K worst TC. Reductions are *not* simply additive where they act on the same term; the stacked estimate at the end accounts for that.

| Rank | Lever | Mean dT change | Worst-TC change | dP effect | Manufacturability | Evidence grade |
|---|---|---|---|---|---|---|
| 1 | Replace paste TIM2: thin-BLT paste / liquid metal / indium / direct-to-die | -2.6 / -7.1 / -8.0 / -9.0 K | same + ~2 K (TIM scatter removed) | none | LM needs Ni barrier + gasket; indium needs reflow; D2D is a platform decision | [M] + datasheets [U] + [LK] |
| 2 | Finer fins (0.2 -> 0.1 -> 0.05 mm gap) enabled by short-flow manifold feeding | -4.5 to -8.8 K | same | neutral to -30 % (with manifold); +300 % without | skived or chemically etched Cu fins + machined/stamped Cu manifold, brazed or FSW; filtration <= 50 um | [M]; peer-reviewed MMC 0.065-0.09 cm2K/W [U]; Drummond/Weibel [LK] |
| 3 | Manifold / short flow length (removes streamwise caloric ramp; maldistribution tolerance) | 0 K on mean | **-5 to -6 K** (plus 4-5x lower sensitivity to maldistribution) | **-25 to -80 %** | as above | [M]; Harpole-Eninger, Copeland, Escher [LK] |
| 4 | Zoned flow / fin-density allocation to the heat map (TC5 zone) | 0 K | -6 to -7 K (9.8 -> ~3 K excess) | ~0 | orifice plate in the manifold; CFD-sized | Sharma/Poulikakos [LK]; Corintis 65 % peak [U]; [M] |
| 5 | Base 2 -> 1 mm Cu | -3.3 K | -3.1 K (hot-spot ripple +0.2 K) | 0 | trivial; flatness control | [M] |
| 6 | Jet impingement core (alternative to 2+3, not additive) | ~-7 K (25 % of case-to-fluid) | similar | undisclosed; likely higher than MMC | drilled/etched nozzle plate; fouling risk | JetCool 3rd-party 25 % [U]; PKU [U]; [LK] |
| 7 | Water instead of PG25 (where facility allows) | -1.4 K | -1.4 K | -2 % | none | [M] |
| 8 | Cu-diamond base or local CVD-diamond insert | -1.5 K / -2 to -3 K local | same | 0 | costly, machining/joining risk | [LK]; NTU [U] |
| 9 | Pin fins (local, under manifold slots / heater corners) | -1 to -3 K local | local | +dP | machinable | ORNL -15 % [U]; Peles [LK] |
| 10 | Topology-optimised / TPMS AM core (vs a good MMC at equal dP) | 0 to -3 K | 0 to -2 K | can be -30 to -68 % vs pin fins at equal R | L-PBF/ECAM Cu; k penalty; not required | UIUC/Fabric8 [U]; TPMS reviews [LK] |
| 11 | Counter-flow interdigitation (fin-scale) | 0 K | -0.3 K (Cu plate); meaningful only for thin D2D lids | +complexity | not worth it for Cu plate | [M run1 s.5]; Vafai & Zhu [LK] |
| 12 | Surface nano-enhancement, single-phase | 0 K | 0 K | 0 | - | Kandlikar [LK] |
| 13 | Two-phase dielectric evaporator (different axis: not fixed 1.2 LPM/kW water) | ~-9 K Tj at GPU scale (V), at 0.3 LPM/kW; CHF-limited at 15 kW/4-heater | - | lower flow, needs HRU | second SKU | Accelsius [U]; Mudawar/Kandlikar [LK] |
| 14 | Embedded in-die microfluidics | -65 % peak rise (prototype) | - | - | silicon-vendor owned, 2028+ | Microsoft/Corintis, TSMC [U] |

**Stacked, conventionally manufacturable "elite" single-phase point (levers 1-5, 7 excluded):** fine-channel copper HMMC (0.05-0.075 mm gaps, 0.6-1 mm fins, 1 mm base) fed by a zoned, tapered manifold with liquid-metal or indium TIM2: model **mean dT ~15-17 K, worst-point ~19-21 K, plate dP ~6-7 kPa at 18 LPM PG25** [M], i.e. roughly **half** the benchmark's mean dT and **less than half** its worst-point dT at (probably) lower pressure drop than its undisclosed value, with headroom to ~30-40 kW at 80 C case in the same footprint (model Q-cap 29-41 kW). The peer-reviewed unit-resistance band for this class (0.065-0.09 cm2K/W, [U]) applied to a 117 cm2 footprint gives 7.6-10.5 K case-to-mean-fluid, consistent with the model's 9-11 K (17-19 K total minus 6.3 K caloric). The direct-to-die variant of the same core is the path to the 2028+ micro-channel-lid market.

---

## Gaps / unknowns

1. **No web searches were run in this sub-task** (budget exhausted before it started). All [LK] numbers (Tuckerman-Pease 790 W/cm2 / 0.09 cm2K/W; Escher 0.087 cm2K/W / 22 kPa; Drummond HMMC ~910 W/cm2 two-phase and ~1 kW/cm2 background + ~2.6 kW/cm2 hot spot single-phase; Mudawar-Bowers 27.6 kW/cm2 CHF; Qu-Mudawar CHF/HTC; Sharma hot-spot ~2x; Chu-Enright-Wang 208 W/cm2; Lee 1995 / Yovanovich 1999 formulae; TPMS performance factors; material k/CTE values) are from memory of the cited papers and need verification against the DOIs before external use. The ones I am least sure of are marked "approx.": IBM ICECool and Georgia Tech intra-chip resistances, Jung 2019 numbers, Drummond's exact values, and Sharma 2015's exact ratios.
2. **Benchmark footprint and dP are undisclosed**, so all area-normalised comparisons (cm2K/W, W/cm2) rest on the 117 cm2 model calibration or the sibling note's 61-100 cm2 inference. If the real footprint is ~65 cm2 the benchmark's unit resistance is ~0.15 cm2K/W (better than modelled) and the TIM share is larger; the lever ranking is unchanged but the absolute K values shift.
3. **TIM2 identity** ("standard thermal paste") and bond line are unknown; the 9 K model allocation is bounded 5-15 K by datasheet values [U].
4. **Jet-array pressure drop and 10-year erosion/fouling data** are unpublished by every vendor; the 25 % JetCool advantage is vendor-reported third-party data.
5. **Liquid-metal TIM2 reliability on a 100 cm2 copper plate** (Ga embrittlement of Al, Cu dissolution, pump-out under thermal cycling, containment) has no public long-term data at this scale; indium TIM2 on a field-replaceable plate is unusual.
6. **Manifold maldistribution** is modelled only as prescribed +/-10-20 % patterns; a 3-D CFD of the actual tapered manifold with 4-zone orifices is needed.
7. **Two-phase 15 kW on a 4-heater TTV** has no public data; CHF margin at 128-250 W/cm2 with R1233zd(E) at 1.2-2 bar and the vapour-quality distribution across zones are unquantified.
8. **AM cost/yield at 100 x 100 mm** (ECAM, L-PBF Cu) and Fabric8's plate-level K/W, dP and price are unpublished; the UIUC 32 %/68 % result is on a 2x2 GaN array.
9. **Nvidia Rubin/Rubin Ultra cold-plate requirements** (per-plate LPM, dP budget, lidded vs bare-die) exist only in conflicting secondary sources (0.6-1.5 LPM/kW; 20-150 kPa) [U].
10. **Not covered quantitatively:** spray cooling, hybrid jet-microchannel optimisation papers (Rau/Garimella numbers), thermosyphon/loop heat pipes, electrohydrodynamic enhancement, graphene/CNT TIMs, and SiC-module-specific baseplate data (typical 100-300 W/cm2 baseplate flux per the sibling note).

---

## Sources

**Benchmark and CoolIT**
- CoolIT 15 kW Tech Brief (June 2026), PDF text supplied locally; page: https://www.coolitsystems.com/resources/news/15kw-coldplate/
- CoolIT 15 kW press release: https://www.coolitsystems.com/resources/news/15kw_press_release/
- CoolIT 4000 W Technical Brief R2 (Mar 2025): https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf
- CoolIT Skived Coldplate Technical Brief (Feb 2021): https://coolitsystems.com/wp-content/uploads/2021/02/CoolIT-Skived-Coldplate-Technical-Brief-Feb26.pdf
- CoolIT Split-Flow Tech Brief (May 2024): https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf
- CoolIT OMNI: https://www.coolitsystems.com/omni/ ; https://www.storagereview.com/news/coolit-systems-omni-all-metal-coldplates-unveiled
- CoolIT coldplate technology page: https://www.coolitsystems.com/coldplate-technology/
- Ramakrishnan et al., ASME J. Electronic Packaging 141(4) 2019 (CoolIT plate survey): https://asmedigitalcollection.asme.org/electronicpackaging/article-abstract/141/4/041005/955785
- Kisitu & Ortega, InterPACK 2021 (split-flow models): https://par.nsf.gov/biblio/10341820

**Peer-reviewed / independent (URL-backed)**
- ORNL, IJHMT 256 (2026), Cu/CuW diamond pin-fin cold plates: https://www.sciencedirect.com/science/article/pii/S0017931025014152 ; OSTI: https://www.osti.gov/pages/servlets/purl/3375134 ; Electronics Cooling (Apr 2026): https://www.electronics-cooling.com/2026/04/high-performance-copper-tungsten-cold-plates-for-direct-to-chip-single-phase-liquid-cooling/
- PKU, Nature Electronics 8, 810-817 (2025), jet-enhanced manifold microchannels: https://www.nature.com/articles/s41928-025-01449-4
- Bio-inspired Cu manifold microchannel, Energy (2025): https://www.sciencedirect.com/science/article/abs/pii/S0360544225049114
- Stanford 3D-manifold embedded cooling (IJHMT 2018): https://nanoheat.stanford.edu/wp-content/uploads/2019/09/1-s2.0-S0017931018326206-main.pdf
- NTU embedded microfluidic diamond spreader: https://scholars.lib.ntu.edu.tw/handle/123456789/739908
- UIUC / Fabric8Labs topology-optimised Cu plate (Cell Rep. Phys. Sci. 2026): https://mechse.illinois.edu/news/82871 ; https://www.hostingadvice.com/blog/a-novel-3d-printed-copper-tree-could-cut-ai-cooling-by-32/ ; https://www.metal-am.com/copper-am-cold-plate-improves-ai-data-centre-cooling/
- Parallel two-phase GPU plates, R245fa (2026): https://www.sciencedirect.com/science/article/abs/pii/S1359431126009294
- Scalably etched copper cold plates with R1233zd(E): https://www.sciencedirect.com/science/article/pii/S0017931025012736
- TSMC direct-to-silicon on CoWoS (ECTC 2025): https://semiwiki.com/semiconductor-manufacturers/tsmc/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/
- Multi-microjet at 100 W/cm2 (SQU/BJUT): https://squ.elsevierpure.com/ar/publications/thermal-characterization-of-multiple-micro-jet-impingement-coolin
- DARPA ICECool (Lockheed): https://eepower.com/news/cool-technology-turns-down-the-heat-on-high-tech-equipment/ ; https://www.electronics-cooling.com/?p=20264
- Microsoft + Corintis: https://www.hpcwire.com/2025/09/25/microfluidics-offers-3x-better-cooling-than-cold-plates-microsoft-says/ ; https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/ ; https://hwbusters.com/news/microsofts-liquid-cooled-chips-could-rewrite-the-rules-for-ai-data-centers/ ; https://spectrum.ieee.org/microfluidics-cooling-ai-chips-corintis
- Google liquid cooling, Hot Chips 2025: https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips ; Deschutes CDU: https://www.datacenterdynamics.com/en/news/hyperscalers-prepare-for-1mw-racks-at-ocp-emea-google-announces-new-cdu/
- OCP OAI Liquid Cooling Guidelines (Mar 2023): https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/
- OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (2026): https://www.opencompute.org/documents/ocp-cold-plate-test-specification-v1-0-0-pdf-1/
- OCP L-L CDU Test Methodology: https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf/
- Electronics Cooling, DLC for high-compute servers (Jun 2025): https://www.electronics-cooling.com/2025/06/direct-liquid-cooling-for-high-compute-servers/

**Vendor (URL-backed)**
- JetCool H100 SmartPlate: https://jetcool.com/post/jetcool-unveils-breakthrough-energy-saving-liquid-cooling-for-nvidias-h100-gpus-enhancing-ai-cluster-efficiency-and-performance/ ; third-party test: https://jetcool.com/post/third-party-testing-data/ ; RTX PRO 6000 datasheet: https://info.jetcool.com/hubfs/Marketing%20Resources%202026/NVIDIA%20RTX%20PRO%206000%20SmartPlate%20Cold%20Plate%20Datasheet.pdf
- Frore LiquidJet: https://www.froresystems.com/media-room/frore-systems-introduces-liquidjet-redefining-coldplates-for-ai-data-centers ; https://www.club386.com/?p=120993
- Mikros Normal Flow: https://www.mikrostechnologies.com/microchannel-liquid-cooling/performance/ ; https://www.mikrostechnologies.com/home/overview/
- ACT two-phase cold plate cut sheet (Nov 2025): https://www.1-act.com/wp-content/uploads/2025/11/TPCP-CS-01_TwoPhaseColdPlates-DataCenters-CutSheet_V1_2025-11-12_Web.pdf
- Wiwynn two-phase 2.5 kW: https://www.wiwynn.com/whitepapers/innovative-two-phase-cold-plate-solutions-for-future-high-power-ai-chips ; Wiwynn/Fabric8 ECAM: https://www.wiwynn.com/technology/advanced-cooling/cold-plate-liquid-cooling ; https://www.fabric8labs.com/ecam-vs-legacy-liquid-cooling-cold-plates/ ; Hot Chips 2023: https://www.hc2023.hotchips.org/assets/program/conference/day2/FPGAs%20Cooling/Fabric8Labs%20-%202023%20Hot%20Chips%20-%20ECAM%20for%20Cooling%20High%20Performance%20ICs%20(2023.08.29).pdf
- Accelsius B200 benchmark: https://www.businesswire.com/news/home/20260721991081/en/ ; https://www.innventure.com/news/independent-benchmarks-show-accelsius-two-phase-direct-to-chip-cooling-delivers-9degc-lower-nvidia-b200-junction-temperatures-than-single-phase-in-warm-water-conditions
- ZutaCore: https://zutacore.com/solutions ; https://www.storagereview.com/news/zutacore-targets-high-density-blackwell-pcie-servers-with-waterless-two-phase-cooling
- Diabatix: https://www.diabatix.com/blog/optimizing-cold-plate-performance-through-generative-design
- ToneCooling GB300 plate: https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ ; FiberMall GB200 plate (secondary): https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; Naddod GB300 (low reliability): https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling
- USUSTK skived fins 0.06/0.10 mm: https://www.globalspec.com/FeaturedProducts/Detail/USUSTK/370123/AI_Server_Copper_SkivedFin_Heat_Sink
- TIM datasheets: Shin-Etsu X23-7921-5: https://cdn.microsi.com/wp-content/uploads/2019/07/X23-7921-5-TDS-July-2019-.pdf ; X23-8117: https://www.microsi.com/applications-solutions/thermal-interface-material/tim-2/thermal-grease-X23-8117/ ; Honeywell PTM7950: https://www.caplinq.com/ptm7950-most-thermally-conductive-phase-change-pad-with-very-low-thermal-impedance-that-works-in-vertical-applications-ptm7950.html
- PG25 properties (Dow DOWFROST LC-25): https://www.chempoint.com/en-ca/products/dow/dowfrost-glycol-thermal-fluids/dowfrost-propylene-glycol-thermal-fluids/dowfrost-lc-25
- Chilldyne / Daikin negative-pressure: see competitors-advanced.md section 5 (DCD coverage, Nov 2025)

**Literature knowledge, not re-verified online in this session [LK]**
- Tuckerman & Pease, "High-performance heat sinking for VLSI", IEEE Electron Device Lett. EDL-2(5), 126-129 (1981), doi:10.1109/EDL.1981.25367
- Shah & London, Laminar Flow Forced Convection in Ducts, Academic Press (1978)
- Harpole & Eninger, "Micro-channel heat exchanger optimization", 7th IEEE SEMI-THERM (1991)
- Copeland, Behnia, Nakayama, "Manifold microchannel heat sinks: isothermal analysis", IEEE Trans. CPMT-A 20(2) (1997)
- Escher, Michel, Poulikakos et al., "A novel high performance, ultra thin heat sink for electronics", ASME J. Heat Transfer 132, 081402 (2010)
- Drummond, Back, Sinanis, Janes, Peroulis, Weibel, Garimella, "A hierarchical manifold microchannel heat sink array for high-heat-flux two-phase cooling of electronics", IJHMT 117, 319-330 (2018); and "Characterization of hierarchical manifold microchannel heat sink arrays under simultaneous background and hotspot heating conditions", IJHMT 126, 1289-1301 (2018)
- Jung, Weibel, Garimella et al., "Embedded cooling with 3D manifold for vehicle power electronics application: single-phase thermal-fluid performance", IJHMT 130, 1108-1119 (2019)
- Kandlikar & Bapat, "Evaluation of jet impingement, spray and microchannel chip cooling options for high heat flux removal", Heat Transfer Eng. 28(11), 911-923 (2007)
- Browne, Michna, Jensen, Peles, "Microjet array single-phase and flow boiling heat transfer with R134a", IJHMT 53 (2010); Michna et al., IJHMT 54 (2011)
- Rau & Garimella, hybrid jet impingement/microchannel, ASME J. Electron. Packag. 136 (2014)
- Sharma, Tiwari, Poulikakos et al., "A novel method of energy efficient hotspot-targeted embedded liquid cooling for electronics", Applied Energy 138, 414-422 (2015)
- Vafai & Zhu, "Analysis of two-layered micro-channel heat sink concept in electronic cooling", IJHMT 42, 2287-2297 (1999)
- Mudawar & Bowers, "Ultra-high critical heat flux (CHF) for subcooled water flow boiling - I", IJHMT 42, 1405-1428 (1999)
- Lee & Mudawar, "Low-temperature two-phase microchannel cooling for high-heat-flux thermal management of defense electronics", IEEE Trans. CPMT 32(2), 453-465 (2009)
- Qu & Mudawar, IJHMT 46, 2755-2771 (2003) and IJHMT 47, 2045-2059 (2004)
- Kandlikar, "A scale analysis based theoretical force balance model for critical heat flux (CHF) during saturated flow boiling in microchannels and minichannels", ASME J. Heat Transfer 132, 081501 (2010)
- Schultz et al. (IBM), embedded two-phase cooling with radial channels, ASME J. Electron. Packag. 138 (2016)
- Peles, Kosar et al., "Forced convective heat transfer across a pin fin micro heat sink", IJHMT 48, 3615-3627 (2005)
- Brunschwiler et al. (IBM), "Interlayer cooling potential in vertically integrated packages", Microsyst. Technol. 15 (2009)
- Chu, Enright, Wang, "Structured surfaces for enhanced pool boiling heat transfer", Appl. Phys. Lett. 100, 241603 (2012)
- Kandlikar et al., "Characterization of surface roughness effects on pressure drop in single-phase flow in minichannels", Phys. Fluids 17, 100606 (2005)
- Lee, Song, Au, Moran, "Constriction/spreading resistance model for electronics packaging", ASME/JSME Thermal Eng. Joint Conf. 4, 199-206 (1995)
- Yovanovich, Muzychka, Culham, "Spreading resistance of isoflux rectangles and strips on compound flux channels", J. Thermophys. Heat Transfer 13(4), 495-500 (1999)
- Bajura & Jones, "Flow distribution manifolds", ASME J. Fluids Eng. 98, 654-666 (1976); Kumaran, Kumaraguruparan, Sornakumar, Appl. Therm. Eng. 58, 205-216 (2013)
- Knight, Goodling, Hall, "Optimal thermal design of forced convection heat sinks - analytical", ASME J. Electron. Packag. 113, 313-321 (1991); Knight et al., IEEE Trans. CHMT 15 (1992)
- Kaur & Singh, "Flow and thermal transport characteristics of TPMS-based gyroid and Schwarz-P cellular materials", Therm. Sci. Eng. Prog. 2021; Attarzadeh et al., Appl. Therm. Eng. 2021

**Our model files**
- docs/cooling/appendix/model_output.md (1-D series network, lever sweep)
- docs/cooling/appendix/physics/run1.txt and hotspot-smoothing.py (2-D hot-spot / maldistribution solver)
