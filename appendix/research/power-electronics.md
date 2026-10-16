# Power electronics as a second application for a high-performance cold-plate architecture

Prepared 2026-10-13 for the "beat the CoolIT 15 kW coldplate" programme (Workflow 1, power-electronics angle). Covers the "SSD converters" request (read as **SiC converters**: silicon-carbide traction inverters, 800 VDC data-centre power, EV chargers, solid-state transformers, grid/HVDC, rail, renewables, drives) plus the other high-heat-flux niches (laser diodes, RF GaN, co-packaged optics, X-ray, directed energy, aerospace radar, quantum).

**Evidence status - read first.** The shared web-search budget for this workflow turn was exhausted before this agent ran a single query (6 queries attempted, 0 executed; WebFetch/curl are blocked per the task brief). Every number below therefore comes from one of three places:

- **[Brief]** - the CoolIT 15 kW tech brief (June 2026), read in full.
- **[Sib]** - a sibling agent's report in this scratchpad that *did* retrieve the figure online this session, with the URL it recorded.
- **[KB-H] / [KB-M] / [KB-L]** - this agent's own knowledge base (training cutoff June 2026), high / medium / low confidence. Datasheet-grade numbers (Rth, dP, flow) are given as ranges wide enough to be safe; anything sharper must be confirmed against the primary document listed in the Sources section before it is quoted externally.
- **[M]** - the programme's own scoping model (appendix/model_output.md).

Vendor claims are marked (V); peer-reviewed or independent data (I).

---

## 1. The benchmark, restated for power-electronics people

| Quantity | CoolIT 15 kW plate | Source |
|---|---|---|
| Heat load | 15 kW, 4 ceramic heaters (GPU + HBM zones) | [Brief] |
| Coolant / flow / inlet | water-glycol (PG25 class), 1.2 LPM/kW = 18 LPM, 45 C | [Brief] |
| Case-to-inlet dT | 34.4 K mean, 26.8-44.2 K across 8 TCs / 3 plates; Tcase ~80 C | [Brief] |
| Absolute R | 34.4 / 15,000 = 0.0023 K/W (mean), 0.0029 K/W (worst TC) | derived [Brief] |
| Area-specific R'' (model, footprint undisclosed) | ~0.27 cm2-K/W incl. paste TIM at an inferred 117 cm2 / 128 W/cm2 | [M] |
| Pressure drop | not disclosed (model estimate ~9 kPa plate-only) | [Brief], [M] |
| Construction | Split-Flow skived copper, "proven mass-manufacturing", thermal paste | [Brief] |

The number that matters for cross-market comparison is the **area-specific resistance of the plate itself (~0.1-0.15 cm2-K/W convective + base, excluding TIM)** and the **flow-length-limited dP**. Power-electronics coolers are routinely 3-10x worse than this on R'' but are designed to completely different constraints (viscous 50/50 glycol at 65 C, -40 C cold start, 15-year corrosion, cents-per-watt cost). Section 5 turns that into a fit matrix.

---

## 2. Application-by-application requirements

### 2.1 EV traction inverters (SiC / GaN, 100-400 kW)

**State of practice.** Every volume SiC traction module since 2018 is cooled by a **direct-cooled pin-fin baseplate** (forged Cu or Al pins integral to the module, O-ring sealed into a cast-aluminium inverter housing) or by Danfoss's **ShowerPower** (a moulded PPS turbulator that sweeps coolant in short meanders across a flat baseplate for die-to-die uniformity) [KB-H]. Representative platforms: Infineon HybridPACK Drive G1/G2 (Si IGBT and CoolSiC, 750/1200 V, up to ~300 kW), Infineon HybridPACK DSC (double-sided cooled), Semikron-Danfoss DCM 1000 / eMPack (ShowerPower, direct-cooled AMB), STMicro ACEPACK Drive (SiC 6-pack, pin-fin), Wolfspeed XM3 / WolfPACK (flat base, needs a cold plate), Hitachi/Denso double-sided "power cards" (Toyota, Audi) [KB-H].

| Parameter | Typical value | Confidence / source |
|---|---|---|
| Inverter efficiency / loss at peak | 97-98.5 % -> 2-4 kW heat at 200-300 kW; 1-2 kW continuous | [KB-M] |
| SiC die | 20-30 mm2 per die, 100-250 W peak per die -> **300-800 W/cm2 at the die**; spread through AMB (Si3N4 0.32 mm + 0.3 mm Cu) to **30-100 W/cm2 at the baseplate**, 20-30 W/cm2 module average | [KB-M]; [Sib] chip-roadmap gives 250-700 W/cm2 die, 30-80 W/cm2 baseplate |
| Tj,max / design Tj | 175 C (SiC), 150-160 C continuous design point | [KB-H] |
| Coolant | 50/50 water-ethylene-glycol (OAT/Si-OAT inhibited, aluminium-compatible) | [KB-H] |
| Inlet temperature | **65 C** standard test/spec point; some OEM loops 70-75 C (shared with motor); 85 C requested by some OEMs | [KB-H] for 65 C, [KB-M] for higher |
| Flow per module | 8-10 LPM (datasheet reference point 10 LPM) | [KB-H] |
| Module-side dP budget | 10-30 kPa at 10 LPM / 65 C; whole inverter typically <= 50 kPa out of a 100-150 kPa vehicle loop | [KB-M] |
| Rth(j-f) per switch, HybridPACK Drive class (IGBT) | ~0.09-0.10 K/W at 10 LPM 50/50 WEG 65 C | [KB-M] |
| Rth(j-f) per switch, CoolSiC HPD G2 class | ~0.08-0.12 K/W | [KB-L] |
| Boyd cold plate for HybridKIT DSC (double-sided module) | Rth 0.026 K/W, max dP 12.5 kPa at 10 LPM 50/50 WG | [Sib] https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf (V) |
| Double-sided cooling benefit | 30-50 % lower Rth(j-f) vs single-sided; ~2x current per die area | [KB-M] |
| Direct-substrate (DBC/AMB in coolant) benefit | removes baseplate + solder/sinter layer: 20-30 % lower Rth(j-f), better uniformity | [KB-M] |
| Embedded 3-D manifold on SiC (Purdue/Garimella 2019, water) | R'' of order 0.05 cm2-K/W, ~1 kW/cm2 class | [Sib] LK, IJHMT 130 (2019) 1108-1119 (I) |
| Cold-start viscosity | WEG 50/50 at -40 C ~50-100 mPa-s vs ~1.3 mPa-s at 65 C (50-80x) | [KB-M] |
| Qualification | ECPE AQG 324 (power cycling, thermal shock -40/+125 or +150 C, vibration, humidity), ISO 16750, IATF 16949 / PPAP; coolant pressure test ~2.5 bar operating / proof 5 bar class; 15 yr / 8,000 h life | [KB-M] |
| Volumes | ~20-22 M xEV (BEV+PHEV) sold in 2025, ~1.3 inverters per vehicle -> **25-35 M traction inverters/yr** in 2026-27 | [KB-M] |
| Cost sensitivity | extreme: inverter BOM $1,500-2,500 for 200 kW (= $8-12/kW); cooler/housing content $20-60; a flat cold plate for baseplate-less modules $15-40 | [KB-M] |

**Where the plate resistance sits.** For a pin-fin SiC module the junction-to-fluid stack is roughly: chip + sinter 10 %, AMB 25 %, baseplate solder + spreading 20 %, **convection 40-50 %** [KB-M]. Effective pin-fin HTC referenced to baseplate area is only 10-25 kW/m2-K (R''conv 0.4-1.0 cm2-K/W) because the pins are coarse (2-3 mm pitch) by design: cold-start dP, 15-year particulate/sludge tolerance and die-cast tolerances forbid sub-0.5 mm features [KB-M]. A plate core at 0.05-0.1 cm2-K/W convective would cut Rth(j-f) by 30-40 % - the same gain that double-sided cooling buys - and that gain converts directly into **15-20 % less SiC die area at equal Tj**, i.e. roughly $100-150 per 200 kW inverter at 2025 SiC prices (~$600-900 of SiC per inverter) [KB-M]. That is the only business case the automotive customer cares about; absolute Tcase is irrelevant.

**Why it is nevertheless a poor near-term fit for a copper micro-feature plate:** the module vendor (Infineon/ST/Danfoss/Wolfspeed/BYD) owns the pin-fin baseplate; the Tier-1 (Bosch, ZF, Vitesco, Denso, BorgWarner, Valeo, Hitachi Astemo) owns the aluminium housing; both are aluminium-chemistry loops with Si-OAT inhibitors that are hostile to bare copper (galvanic couple with the cast housing, copper-ion catalysed inhibitor depletion) [KB-M]; features finer than ~0.5 mm are a reliability non-starter; and qualification is 24-36 months. Realistic entry: (a) license the manifold/short-flow concept as a **forged or MIM Cu baseplate insert** to a module vendor, or (b) a flat copper plate for baseplate-less modules (WolfPACK / Easy / ACEPACK) in lower-volume, higher-margin segments (eVTOL, aerospace, motorsport, off-highway) [KB-M].

### 2.2 AI data-centre 800 VDC power architecture (NVIDIA 2025-2028)

**What was announced.** NVIDIA's 800 VDC architecture (blog May 2025; technical white paper and partner demos at OCP Summit October 2025) replaces the 54 V busbar / in-rack PSU-shelf model with **800 VDC distribution from a solid-state transformer (13.8 kV AC -> 800 VDC) or industrial rectifiers to the rack**, with DC-DC conversion to 50/12 V at the rack or compute-tray level; first deployment with **Kyber (Rubin Ultra NVL576, ~600 kW, 2H 2027)**, scaling to 1 MW+ racks [KB-M]; Kyber racks and rack-level power are 100 % liquid cooled at 45 C inlet [Sib] (chip-roadmap-requirements.md; DCD, igorslab). NVIDIA's headline claims: up to ~5 % end-to-end efficiency gain, ~45 % less copper, up to ~70 % lower maintenance (fewer PSUs), 1 MW through the same busbar cross-section [KB-M, V]. Named silicon partners: Infineon, Navitas, TI, ROHM, STMicro, onsemi; power-system partners: Delta, Flex, LITEON, Megmeet (power shelves/DC-DC); Eaton, Vertiv, Schneider Electric, ABB, Siemens, Hitachi Energy, Mitsubishi Electric, GE Vernova (SST, rectifiers, ESUs) [KB-M]. Vertiv stated it will launch an 800 VDC portfolio in 2H 2026 [KB-M]. Parallel hyperscaler route: OCP "Mt. Diablo" +/-400 VDC disaggregated power rack (Meta/Microsoft/Google, 2024-25) and Google's +/-400 VDC 1 MW rack plan (April 2025) [KB-M].

| Parameter | Value | Confidence / source |
|---|---|---|
| Rack power | GB200 NVL72 120-140 kW (2025); VR NVL144 ~190-230 kW (2026); Kyber ~600 kW (2027); 1 MW+ (2028) | [Sib] chip-roadmap (TrendForce, Vertiv, DCD URLs) |
| In-rack conversion loss (800 V -> 50/12 V at 97.5-98.5 %) | **15-25 kW per MW rack**; 10-15 kW on a 600 kW Kyber | [KB-M]; [Sib] 20-40 kW/MW incl. SST |
| SST / facility-side loss (97-98 %) | 20-30 kW per MW, outside the rack (power room), liquid- or air-cooled | [KB-M] |
| Today's ORv3 power shelf (air) | 33 kW (6 x 5.5 kW Titanium PSUs), ~0.8-1.3 kW heat per shelf, ~70-100 W/in3 | [KB-M] |
| Next-gen AI PSU / DC-DC bricks | 8-12 kW GaN+SiC PSUs at ~98 % (Infineon, Navitas 2025) 100 W/in3 class; 800 V -> 50 V SiC/GaN LLC/DAB stages 50-100 kW per unit = **1-2 kW heat per unit** | [KB-M] |
| Device-level flux | GaN/SiC top-side-cooled discretes (TOLT, DFN 8x8): 5-30 W each, 10-30 W/cm2 at the package; SiC modules (Easy 2B/3B, WolfPACK) 200-800 W over 50-70 cm2 = 5-15 W/cm2 average, 100-300 W/cm2 at the die | [KB-M]; [Sib] 100-300 W/cm2 |
| Tj / component limits | SiC 150-175 C, GaN 150 C, planar magnetics 100-120 C, electrolytic/film caps 85-105 C | [KB-H] |
| Coolant / inlet | same TCS loop as the GPUs: OCP PG25, 30-45 C in, 65 C max return, 50 um filtration | [Sib] standards-reliability.md (OCP PG25, L-L CDU methodology) |
| dP budget | a power shelf/converter sits in parallel with GPU trays: must hit its flow at <= 20-50 kPa plate-level; rack TCS budget ~124 kPa (18 psi) at 1.2 LPM/kW | [Sib] Electronics Cooling Jun-2025 via standards-reliability.md; [KB-M] |
| Wetted materials | OCP/NVIDIA RVL practice: copper (often Ni-plated), stainless, brass, EPDM; **aluminium discouraged in the PG25 loop** (galvanic couple with copper plates) | [Sib] standards-reliability.md; [KB-M] |
| Required plate R'' | with Tj-Tin ~100 K available and 5-30 W/cm2, R'' of 0.5-2 cm2-K/W is sufficient; **TIM/gap pad (0.5-1.5 cm2-K/W) dominates**, not the plate | derived [KB-M] |
| Cost target | $50-150 per 2-5 kW power-shelf plate; $/kW of conversion hardware $50-100/kW | [KB-L] |
| Volume | tens of thousands of NVL-class racks/yr in 2026-27 (NVIDIA cooling BOM ~$50-56 k per rack [Sib]); 8-20 power units per rack; 800 VDC ramps from 2027 | [Sib] igorslab, DCD; [KB-M] |

**Reading.** Data-centre power electronics is the *easiest* thermal problem in this document (large dT budget, low flux) but it is **in our loop, with our customers, with our chemistry**: it must be copper/stainless, PG25-compatible, QD-connected (UQD04-08), leak-tested to OCP cold-plate spec, and it must not steal pressure head from the GPU plates. The winning product is therefore not a higher-performance core but a **low-dP, high-uniformity flat copper plate family (with the same manifold core de-rated for cost) that lets Delta/Flex/LITEON/Vertiv double converter density (W/in3) and delete fans** - sold as part of a rack cooling kit with the GPU plates and manifolds. CoolIT's "expanded cooling of peripheral components to maintain 100 % heat capture" line in the brief is exactly this market [Brief].

### 2.3 EV fast chargers (150 kW - 3.75 MW)

| Parameter | Value | Confidence / source |
|---|---|---|
| Power classes | CCS 150-400 kW (2025 norm 350-400 kW); Tesla V4 cabinet 1.2 MW shared; MCS (trucks) up to 3.75 MW at 1,250 V / 3,000 A; China "liquid-cooled supercharging" 600 kW (Huawei), 1 MW class (Alpitronic HYC1000) | [KB-M] |
| Efficiency / heat | 95-97 % -> **10-18 kW heat per 350 kW charger, ~30 kW per 1 MW** | [KB-M] |
| Power module | 30-60 kW modules, 1200 V SiC in TO-247/discretes or baseplate-less modules; 97-98 % module efficiency | [KB-M] |
| Cooling today | air-cooled modules in cabinets dominate (<250 kW); **liquid-cooled modules and liquid-cooled cables (500-600 A, Huber+Suhner, Phoenix Contact) above 350 kW**; Huawei/Alpitronic/Tesla/Kempower fully liquid-cooled cabinets | [KB-M] |
| Coolant / inlet | WEG 50/50; inlet 40-55 C (outdoor 50 C ambient + radiator approach) | [KB-M] |
| Flux | 10-40 W/cm2 at the heat-sink interface; die 100-300 W/cm2 | [KB-M] |
| dP budget | 20-50 kPa per module, 100-200 kPa cabinet loop | [KB-L] |
| Material / cost | brazed or FSW aluminium with pressed-in tubes or machined channels, $30-80 per module plate; cabinet $100-200/kW all-in power electronics | [KB-M] |
| Volume | ~1.3-1.5 M public DC fast-charge ports installed worldwide end-2024 (China ~ 2/3); **0.6-1.0 M DC ports/yr** added 2025-27; MCS in the thousands/yr | [KB-M] |
| Qualification | IEC 61851 / IEC 62196, UL 2202/2231, IP55-65 outdoor, -30/+50 C, 10-15 yr | [KB-H] |

**Reading.** Moderate fit. Liquid cooling share is rising fast above 350 kW, the customers (Delta, Huawei, ABB, Alpitronic, Kempower, Tritium, Sinexcel, Infypower) are reachable, and dP matters because one pump serves cables + modules. But the loop is aluminium/WEG, flux is modest and $/kW rules; a copper micro-feature plate wins only in the **1 MW+ MCS cabinets** where cabinet volume and module count are the cost driver.

### 2.4 Solid-state transformers (SST) and MV SiC converters

| Parameter | Value | Confidence / source |
|---|---|---|
| Devices | 3.3 kV / 6.5 kV / 10 kV SiC MOSFET modules (Wolfspeed, Infineon, Mitsubishi, Hitachi, BYD), 1-3 kW loss per module | [KB-M] |
| SST efficiency / heat | 96-98 % per stage -> **20-40 kW per MW** (MV AC -> 800 VDC) | [KB-M] |
| Module flux | 10-30 W/cm2 average over 100-150 cm2 baseplate; 50-150 W/cm2 under the die | [KB-M] |
| Coolant | **deionised water (<1-5 uS/cm, mixed-bed polisher)** or WEG on cold plates floating at MV potential on insulating hose; inlet 40-50 C | [KB-M] |
| Tj | 150 C design, 175 C max | [KB-H] |
| Market | ~$0.4-0.7 B (2025), >15 %/yr; data-centre 800 VDC is the new demand driver (NVIDIA partners Hitachi Energy, Delta, Eaton, Schneider, Siemens, ABB); start-ups Amperesand (Wolfspeed/Temasek-backed) etc. | [KB-L] |
| Cost sensitivity | moderate: MV SiC dies are expensive ($/cm2 far above 1200 V parts), so **thermal performance = fewer dies**, like traction | [KB-M] |

**Reading.** Medium-good fit on physics and economics (expensive dies, moderate flux, large dT budget, DI-water-tolerant copper possible with Ni/Au plating), low volume in 2026-27 but the same buyers as the data-centre power room. Needs an isolated-plate (electrically floating) variant and DI-water erosion/corrosion qualification.

### 2.5 Grid / HVDC converters and STATCOM

| Parameter | Value | Confidence / source |
|---|---|---|
| Station loss | 0.7-1 % per VSC station -> **15-20 MW heat for a 2 GW bipole** | [KB-M] |
| Devices | 4.5 kV press-pack / StakPak IGBT, 2-3 kA, double-side cooled; 2-5 kW per device, 10-30 W/cm2 | [KB-M] |
| Coolant | DI water <0.5 uS/cm, 40-55 C inlet, Ni-plated Al or Cu heat sinks; valve-branch dP ~0.5-2 bar | [KB-M] |
| Market | HVDC capex ~$12-18 B/yr (2025), valve cooling systems ~$100-200 M/yr | [KB-L] |
| Fit | **low**: 40-year qualification (IEC 62501), vertically integrated incumbents (Hitachi Energy, Siemens Energy, GE Vernova, NR Electric, C-EPRI), low flux, DI water | [KB-M] |

### 2.6 Rail traction

Converters 1-2 MW per unit, 3.3 kV IGBT and now SiC (Hitachi, Mitsubishi, Toshiba, CRRC, Siemens), 2-3 % loss = 20-60 kW per converter box; WEG loops or heat-pipe/forced-air; inlet 40-70 C; 20-50 W/cm2; aluminium; EN 50155, IEC 61373 (vibration), EN 45545 (fire), 30-40 yr life; ~20-30 k rail vehicles/yr worldwide [KB-M]. **Low fit** (aluminium, long qualification, low flux).

### 2.7 Renewable inverters and ESS PCS

Central PV inverters 1-5 MW (Sungrow 1+X modular 1.1 MW units are liquid-cooled; SMA, Huawei), wind converters 3-15 MW, ESS PCS 2-5 MW; 1.5-2.5 % loss; PrimePACK-class 1.7 kV IGBT modules at 30-60 W/cm2; WEG at 35-45 C; FSW/brazed aluminium; cooling content well under $1/kW; ~600-700 GW/yr PV inverters plus ~120-150 GW/yr wind [KB-M]. **Very low fit** (pure cost play, aluminium).

### 2.8 Industrial motor drives

ABB ACS880-LC, Siemens Sinamics, Danfoss VACON liquid-cooled drives for marine, mining, oil & gas; ~2 % loss; aluminium plates; drives market >$20 B/yr but liquid-cooled share <10 % [KB-M]. **Low fit.**

---

## 3. Other high-heat-flux niches

| Niche | Heat flux / load | Coolant & constraints | Market hint | Fit for a low-dP copper plate | Confidence |
|---|---|---|---|---|---|
| High-power laser diode bars / stacks (industrial fibre-laser pumps, medical, DE) | 200-500 W per 10 x 1-4 mm bar -> **500-1,000+ W/cm2** at the mount; ~40-50 % of input is heat | Cu microchannel coolers (300-500 um channels), DI water 1-10 uS/cm at 20-25 C, 0.3-0.5 LPM per bar, **dP 50-100 kPa per cooler**, Rth 0.3-0.5 K/W per bar; erosion/corrosion of Cu is the known life-limiter (Jenoptik ceramic-Cu hybrids) | high-power diode lasers ~$2.5-3 B (2025), coolers ~$100-200 M | **High on physics** (Mikros already sells "optics" plates at <0.018 cm2-K/W [Sib]); needs Au/Ni plating, DI compatibility, electrical isolation; small volume, high margin | [KB-M] |
| RF GaN (AESA radar, EW, satcom, 5G macro) | MMIC 10-100 W; **100-1,000 W/cm2 at the die, 1-30 kW/cm2 at gate fingers**; DARPA ICECool demo 1 kW/cm2 with 30 kW/cm2 hot spots (Lockheed) | Airborne: PAO (MIL-PRF-87252, ~8-10 mPa-s at 20 C, >100 at -40 C) in brazed Al plates, 20-60 C, 70-140 kPa budgets; ground/naval: WEG; ITAR, DO-160/MIL-STD-810 | RF GaN devices ~$2.5-3.5 B (2025); AESA radar >$10 B/yr | **Medium-high**: PAO viscosity makes a short-flow-length (low-dP) core genuinely differentiating; long qualification; need Al or plated-Cu variants | [Sib] for ICECool (eepower, electronics-cooling URLs); [KB-M] rest |
| Co-packaged optics (CPO) switches | NVIDIA Quantum-X / Spectrum-X Photonics (2026), Broadcom Bailly 51.2T; switch ASIC 1-2 kW + 16-18 optical engines at 15-30 W each + external laser sources 100-200 W; lasers must stay <70-80 C and within +/-2-3 K across the package | PG25, same TCS loop, 30-45 C; NVIDIA states its CPO switches are liquid-cooled | CPO optics ~$0.5-1 B 2026 -> several $B by 2028-29 (LightCounting-class forecasts) | **High**: same customers, loop and copper chemistry; uniformity and low dP are the spec; a natural second SKU of the GPU plate | [KB-M] |
| X-ray sources (CT rotating anodes 100-150 kW peak; industrial tubes; synchrotron absorbers 1-10 kW/cm2 on GlidCop) | very high local flux but oil-cooled tube envelopes or custom GlidCop absorbers | oil / DI water | tubes ~$2 B; absorbers tiny | **Low** (custom, non-plate) | [KB-M] |
| Directed energy (HEL 50-300 kW: HELIOS 60 kW, IFPC-HEL 300 kW, Iron Beam 100 kW) | 30-40 % wall-plug -> **100-500 kW of heat per weapon**, mostly diode pumps and fibre amplifiers; thermal is the gating SWaP item | WEG/PAO, compact, shock/vibration | US DoD DE spend ~$1-1.5 B/yr; global ~$5 B by 2030 | **Medium-high** (margin, performance-first); very low volume; ITAR | [KB-M] |
| Aerospace / space power & radar | T/R modules 5-20 W/channel, 50-100 W/cm2; satellite GaN SSPAs; eVTOL SiC inverters 20-40 kW/kg | PAO / fluorinated fluids / conduction to radiators; DO-160, vacuum-rated materials | AESA + space power ~$15 B/yr | **Medium** (performance-first but Al/brazed, long qualification) | [KB-M] |
| Quantum computing | dilution-refrigerator cryogenics; room-temperature control electronics (FPGA 50-100 W) air-cooled | - | hardware ~$1-2 B/yr | **None** today; photonic-quantum lasers are the only plate-shaped load | [KB-M] |
| Green-hydrogen rectifiers, induction heating, MRI gradient amplifiers | 1-2 % loss on 100 MW rectifiers; 100-200 kW peak amplifiers | DI water / WEG, Al/Cu | niche | Low | [KB-L] |

---

## 4. What a cold plate must deliver, by application (summary table)

| Application | Plate flux (avg / local, W/cm2) | Coolant, inlet | Available dT (Tj or Tcase - Tin) | Required plate R'' incl. interface (cm2-K/W) | dP budget (kPa) | Material norm | Cost class | Volume class | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| AI GPU/ASIC (benchmark) | 120-250 / 300+ | PG25, 45 C | **~35 K** | **<= 0.15-0.27** | 10-50 plate; ~124 rack | Cu (Ni-plated) | $200-400/plate | 10^5-10^6 plates/yr | [Brief], [Sib], [M] |
| CPO switch / optical engines | 50-150 / 200 | PG25, 30-45 C | 25-35 K (lasers <70-80 C) | <= 0.2, uniformity +/-3 K | 10-30 | Cu | $150-300 | 10^4-10^5 | [KB-M] |
| DC 800 VDC power shelves / DC-DC | 5-30 / 100-300 (die) | PG25, 30-45 C | 80-110 K (Tj 150-175 C) | 0.5-2 (gap-pad limited) | 20-50 | Cu/stainless (loop chemistry) | $50-150 | 10^5-10^6 units/yr from 2027 | [KB-M] |
| SST / MV SiC | 10-30 / 50-150 | DI water or WEG, 40-50 C | 90-110 K | 0.3-0.8 | 30-100 | Cu or Ni-Al, isolated | $100-300 | 10^3-10^4 | [KB-M] |
| EV traction inverter | 20-30 / 30-100 (300-800 die) | WEG 50/50, 65-75 C | **80-100 K** | 0.4-1.0 today (pin-fin); 0.1-0.2 would save 15-20 % SiC | 10-30 module; cold-start at -40 C governs | Al housing + Cu/Al pin-fin baseplate | $20-60 | 10^7 /yr | [KB-M] |
| EV fast charger >350 kW | 10-40 / 100-300 (die) | WEG 50/50, 40-55 C | 90-110 K | 0.5-1.5 | 20-50 | Al brazed/FSW | $30-80 | 10^5-10^6 modules/yr | [KB-M] |
| HVDC / STATCOM | 10-30 | DI water <0.5 uS/cm, 40-55 C | 60-80 K | 0.5-1.0 | 50-200 | Ni-Al / Cu | low | 10^3-10^4 | [KB-M] |
| Rail traction | 20-50 | WEG or air, 40-70 C | 60-80 K | 0.5-1.0 | 30-100 | Al | low | 10^4 | [KB-M] |
| PV / wind / ESS | 30-60 | WEG, 35-45 C | 70-90 K | 0.5-1.0 | 30-100 | Al | very low | 10^6 | [KB-M] |
| Laser diode bars | 500-1,000+ | DI water 1-10 uS/cm, 20-25 C | **30-40 K** (Tj <60-70 C) | **<= 0.03-0.05** | 50-100 per cooler | Cu (Au/Ni) | $50-200/bar | 10^5 bars/yr | [KB-M] |
| RF GaN / radar | 100-1,000 (die), 50-100 (plate) | PAO or WEG, 20-60 C | 100-150 K (Tj 200-225 C) but reliability wants <150 C | 0.1-0.3 | 70-140 | Al (PAO) / plated Cu | $200-2,000 | 10^3-10^4 | [KB-M] |
| Directed energy | 200-1,000 (diodes) | WEG / PAO | 30-40 K | <= 0.05 | 50-150 | Cu | high | 10^1-10^2 systems | [KB-M] |

**Physics note on viscosity (why low-dP architecture matters more outside the data centre).** In laminar micro-channel flow dP scales with viscosity; PG25 at 45 C is ~1.1-1.3 mPa-s, WEG 50/50 at 65 C ~1.3-1.5 mPa-s (and ~3.5 at 25 C, 50-100 at -40 C), PAO-2 ~8-10 mPa-s at 20 C [KB-M]. A short-flow-length manifold core that gives fine-channel h at 2-3x lower dP than a long-channel plate [M] therefore buys proportionally more in WEG, PAO and cold-start cases - but only if the channel features themselves survive the particulate, corrosion and cold-start environment (>= 0.3-0.5 mm minimum features for automotive/charger loops; 0.1 mm is acceptable only in filtered PG25 / DI water loops).

---

## 5. Fit matrix: where a high-performance, low-dP copper cold-plate architecture wins

Scoring 1 (poor) to 5 (excellent); "Cu OK?" asks whether the loop chemistry accepts copper.

| Application | Thermal need for our R'' | Values low dP | Cu OK? | Same customers / loop as AI DC | Cost tolerance | Qualification time | Volume (2027) | Overall | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| AI GPU / ASIC plates | 5 | 4 | 5 | 5 | 4 | 3 (12-18 mo RVL) | 5 | **5** | primary |
| CPO switches / optical engines | 4 | 4 | 5 | 5 | 4 | 3 | 3 | **4.5** | second SKU of the GPU plate |
| 800 VDC power shelves / DC-DC (in-rack) | 2 | 5 | 5 | 5 | 2 | 3 | 4 | **4** | de-rated "rack power kit" plate; sell density + 100 % heat capture |
| Laser diodes / directed energy | 5 | 3 | 4 (plated, DI) | 1 | 5 | 2 (DE) / 4 (industrial) | 2 | **3.5** | high-margin niche; proves 1 kW/cm2 claims |
| SST / MV SiC (incl. DC power room) | 3 | 3 | 4 (isolated) | 4 | 4 | 2 | 2 | **3.5** | 2027-28 adjacency via Hitachi Energy / Delta / Eaton |
| RF GaN / radar | 4 | 5 (PAO) | 3 (plated) | 1 | 5 | 1 (ITAR, DO-160) | 2 | **3** | partner-led, long cycle |
| EV fast chargers >350 kW / MCS | 2 | 4 | 2 (WEG-Al loops) | 2 | 2 | 3 | 4 | **2.5** | only 1 MW+ cabinets; aluminium variant |
| EV traction inverters | 3 (die savings) | 4 (cold start) | 1 | 1 | 1 | 1 (AQG 324, PPAP) | 5 | **2** | license core to a module vendor; no direct plate business |
| Rail traction | 2 | 2 | 2 | 1 | 2 | 1 | 2 | **1.5** | no |
| HVDC / STATCOM | 2 | 2 | 3 | 1 | 2 | 1 | 1 | **1.5** | no |
| PV / wind / ESS / drives | 1 | 2 | 1 | 1 | 1 | 2 | 5 | **1** | no (aluminium commodity) |
| X-ray, quantum | 1-2 | - | - | 1 | - | - | 1 | **1** | no |

**Which require aluminium / low cost:** traction inverters, fast chargers, rail, renewables, drives, HVDC (Ni-plated Al). Those are serviceable only with an aluminium-compatible variant (brazed/FSW aluminium carrier with a coarse 0.5-1 mm manifold core, Si-OAT coolant, 2.5/5 bar pressure class, -40/+125 C cycling, IEC 61373-class vibration), which is a **different SKU family, not a different architecture** [Sib] (competitors-advanced.md, manufacturing-cost.md reach the same conclusion).

**Which reward a premium copper plate:** AI GPU/ASIC, CPO, 800 VDC rack power (de-rated), laser diodes / directed energy, SST / MV SiC, RF GaN. All but the last two share the PG25 / copper / UQD ecosystem, which is why the programme should treat "data-centre power electronics" as an extension of the GPU product line rather than as the automotive "SiC converter" business a colleague may have had in mind.

---

## 6. Design requirements that power electronics adds to the architecture

1. **Interface flexibility.** Three interfaces must be supported by the same core: (a) flat lidded package with paste (GPU), (b) flat module baseplate or top-side-cooled discretes through gap pad / phase-change TIM (power shelves, chargers), (c) **direct-cooled baseplate** where the module's pin-fin or flat Cu base *is* the wetted wall and our part is the manifold/jacket with an O-ring groove (traction, some SST modules) [KB-H].
2. **Uniformity across many dies.** Converters have 6-24 dies in series along the flow; power modules fail at the hottest die. ShowerPower's selling point is die-to-die uniformity, and the programme's manifold core already gives short flow paths and zoned flow [M] - this should be stated as a spec (**<= +/-3 K die-to-die at full load**).
3. **Viscous and cold coolant.** Design flow passages so dP at WEG 50/50, 25 C stays within budget and that -40 C start-up does not stall the loop; keep minimum feature >= 0.3-0.5 mm for aluminium/WEG loops, 0.1 mm only for filtered PG25 / DI water.
4. **Electrical isolation options.** SST/HVDC/laser-diode plates sit at potential: insulating hoses, DI-water compatibility (Ni/Au plating on Cu, velocity < 2-3 m/s to avoid erosion), creepage/clearance in the mounting.
5. **Qualification stack per segment.** OCP cold-plate test spec v1.0.0 (Oct 2026, CoolIT-authored) for data centre [Sib]; AQG 324 + ISO 16750 for automotive; IEC 61373 / EN 45545 for rail; DO-160 / MIL-STD-810 for aero; IEC 62501 for HVDC [KB-M].
6. **Pressure class.** Data-centre 7-10 bar design / 1.5x proof / 3x burst [Sib]; automotive 2.5 bar / 5 bar; aerospace PAO loops up to 10-14 bar [KB-M].
7. **The die-saving argument is the sales pitch for every SiC segment.** Quantify Rth(j-f) reduction -> die-area reduction -> $ per unit; 30-40 % lower convective R'' is worth 15-20 % SiC area [KB-M].

---

## 7. Gaps / unknowns

- **No live web search was possible for this agent** (shared budget exhausted before the first query). All [KB] values must be confirmed. Priority confirmations, with suggested queries:
  1. Infineon HybridPACK Drive G2 CoolSiC datasheet: Rth(j-f), flow, dP at 10 LPM 65 C ("FS03MR12A6MA1B datasheet Rth(j-f) pressure drop").
  2. Danfoss DCM 1000X / ShowerPower 3D Rth and dP claims vs pin-fin ("Danfoss ShowerPower 3D pressure drop thermal resistance DCM1000X").
  3. STMicro ACEPACK Drive SiC datasheet Rth(j-f) and coolant conditions.
  4. NVIDIA 800 VDC white paper (OCP Oct 2025): rack-level vs tray-level conversion split, efficiency claims, Kyber power-shelf cooling ("NVIDIA 800 VDC white paper OCP 2025 Kyber power shelf liquid cooled").
  5. Delta / Flex / LITEON / Vertiv 800 VDC liquid-cooled power shelf specs (kW, W/in3, coolant, dP) 2026.
  6. OCP Mt. Diablo +/-400 VDC spec v1.0 and Google 1 MW rack power blog (Apr 2025).
  7. DC fast charger annual port additions 2025 (IEA Global EV Outlook 2026) and MCS deployments.
  8. SST market size 2025-2030 (analyst) and Amperesand / Hitachi Energy data-centre SST announcements.
  9. Laser-diode microchannel cooler datasheets (Jenoptik, DILAS/Coherent, Focuslight): dP, flow, Rth, conductivity spec.
  10. RF GaN / AESA cold-plate PAO conditions (MIL-PRF-87252 properties; typical dP budgets).
  11. CPO switch thermal specs (NVIDIA Quantum-X Photonics datasheet; Broadcom CPO thermal papers).
- The CoolIT 15 kW plate's footprint, fin geometry and dP are undisclosed, so cross-market R'' comparisons rest on the programme model's 117 cm2 assumption [M].
- No public NVIDIA/OCP thermal specification exists yet for 800 VDC power shelves; the 15-25 kW/MW in-rack loss figure is derived from efficiency assumptions, not disclosed data.
- Automotive Rth(j-f) figures are quoted as ranges; per-OEM inlet temperatures (65 vs 75 vs 85 C) and dP allocations are NDA items.
- Market sizes are order-of-magnitude knowledge-base values; none were checked against 2026 analyst reports.

---

## 8. Sources

Retrieved this session by sibling agents (URLs as they recorded them):
- CoolIT 15 kW tech brief (June 2026) - appendix/pdf/brief.txt
- Boyd HybridKIT DSC cold plate datasheet (Rth 0.026 K/W, 12.5 kPa at 10 LPM 50/50 WG) - https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf
- ORNL Cu/CuW diamond pin-fin cold plates, IJHMT 256 (Mar 2026), 6.9 K/kW incl. TIM at 1 kW, 9 kPa - https://www.sciencedirect.com/science/article/pii/S0017931025014152 ; https://www.osti.gov/pages/servlets/purl/3375134
- Lockheed / DARPA ICECool embedded microfluidic GaN cooling (1 kW/cm2, 30 kW/cm2 hot spots) - https://eepower.com/news/cool-technology-turns-down-the-heat-on-high-tech-equipment/ ; https://www.electronics-cooling.com/?p=20264
- UIUC / Fabric8Labs topology-optimised Cu plate on a 2x2 GaN array (-32 % R at equal flow, -68 % dP at equal R) - https://mechse.illinois.edu/news/82871 ; https://www.metal-am.com/copper-am-cold-plate-improves-ai-data-centre-cooling/
- NVIDIA Rubin Ultra NVL576 / Kyber ~600 kW, 2H 2027 - https://datacenterdynamics.com/en/news/nvidias-rubin-ultra-nvl576-rack-expected-to-be-600kw-coming-second-half-of-2027
- NVL72 / NVL144 cooling BOM (~$50-56 k per rack) - https://www.igorslab.de/en/nvidia-nvl72-liquid-cooling-reaches-50-000-dollars-next-generation-surpasses-everything/
- Vertiv / NVIDIA GB200 NVL72 reference architecture, up to 132 kW/rack - https://investors.vertiv.com/news/news-details/2024/Vertiv-Codevelops-with-NVIDIA-Complete-Power-and-Cooling-Blueprint-for-NVIDIA-GB200-NVL72-Platform/default.aspx
- OCP PG25 base spec, L-L CDU test methodology (1.5 LPM/kW, >= 40 psi, components to 100 psi), UQD v2.0.0, cold-plate test spec v1.0.0 - as listed in appendix/research/standards-reliability.md
- Jung, Weibel, Garimella et al., "Embedded cooling with 3D manifold for vehicle power electronics application", IJHMT 130 (2019) 1108-1119 (cited by sibling from literature knowledge, not retrieved)

Primary documents to pull for the [KB] items (URLs from memory, unverified this session):
- NVIDIA, "NVIDIA 800 VDC architecture will power the next generation of AI factories" (developer blog, May 2025) - https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/
- NVIDIA 800 VDC technical white paper and OCP Summit Oct 2025 partner announcements (blogs.nvidia.com, Oct 2025)
- Infineon HybridPACK Drive G2 / CoolSiC product pages and datasheets (infineon.com)
- Semikron-Danfoss ShowerPower / DCM 1000 pages (semikron-danfoss.com)
- STMicroelectronics ACEPACK Drive product page (st.com)
- Wolfspeed XM3 / WolfPACK datasheets (wolfspeed.com)
- ECPE AQG 324 guideline (ecpe.org)
- OCP Mt. Diablo +/-400 VDC power rack specification (opencompute.org); Google Cloud blog on +/-400 VDC 1 MW racks (Apr 2025)
- IEA Global EV Outlook 2025/2026 (charging infrastructure chapter)
- Vertiv press release on 800 VDC portfolio (May 2025, vertiv.com)
- MIL-PRF-87252 (PAO coolant) and Jenoptik / Coherent-DILAS microchannel cooler datasheets
