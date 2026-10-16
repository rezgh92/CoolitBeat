# HMMC-X: one tied-sandwich manifold cartridge for AI accelerators and SiC power electronics (key: power-electronics)

Architecture proposal, 2026-10-14. Benchmark: CoolIT 15 kW Split-Flow plate (June 2026): 15 kW, 18 LPM PG25 (1.2 LPM/kW), 45 C inlet, average case-to-inlet 34.4 K, maximum 44.2 K, paste TIM, dP undisclosed (our reconstruction ~25 kPa, band 17-42). Power-electronics baseline: Infineon HybridPACK Drive G2 CoolSiC pin-fin module (FS01MR12A8MA2B: Rth(j-f) 0.103 K/W typical, 0.113 maximum per switch, 10 L/min 50/50 water-glycol, 60 C [S1]; the G2 datasheets put module plus reference cooler at ~76 mbar = 7.6 kPa at 10 L/min, 65 C [S2]).

Numbers: AI from the project scoping model (`coldplate_model.py`, unmodified) in `design/pe/pe_ai_run.py`, P10-P90 bands from `SYNTHESIS-physics.md`. Power electronics from `design/pe/pe_fourier.py` (multilayer Fourier spreading model of one switch cell: 8 SiC dies of 4.5 mm = 1.62 cm2 on a 40 x 35 mm Si3N4 AMB cell; within 2 % of the 3-D finite-volume model `pe_stack.py`), with coolant-side h_eff and dP from the scoping model using WEG, PAO and PG25 properties (`pe_run*.py` / `.out`). Each term +/-25 %. [KB] = not re-verified this session; [S] = source list at the end.

---

## 1. Concept in one page

**What it is.** HMMC-X is built around a standard *cartridge*: a tied sandwich of a skived fin field, an etched tie grate and an etched metering comb, bonded into a 5-8 mm thick, self-contained, pressure-rated heat-exchange element. Coolant drops through comb holes, wets **4 mm of fin**, and leaves. Every fluid parcel enters the fins at inlet temperature. The cartridge goes into one of three bodies:

- **(a) Copper manifold body.** This is the AI plate: the PX-15 for 15 kW-class parts and the PX-GPU for 1.8-4 kW lids.
- **(b) Power-module baseplate.** The AMB substrate is soldered or Ag-sintered straight onto the cartridge face. The cartridge then O-rings into the inverter's coolant jacket in place of today's pin-fin baseplate.
- **(c) Double-sided power-card stack.**

The cartridge grade is set by what the loop's filtration and chemistry allow:

| grade | gap / fin / height, flow length | material | loop | h_eff (kW/m2K) |
|---|---|---|---|---|
| **C-R** (robust) | 0.15 / 0.10 / 2.0 mm, 4 mm | OFE Cu, bare | filtered PG25 / DI water (50 um absolute screen) | 127 (GPU TTV), 108 (WEG 65 C), 124 (power shelf) |
| **C-P** (performance, AI only) | 0.10 / 0.10 / 1.5 mm, 4 mm | OFE Cu | <= 33 um absolute loops | 187 |
| **C-D** (de-rated, data-centre power) | 0.25 / 0.20 / 3.0 mm, 6 mm | OFE Cu | PG25 rack loop | 72 |
| **C-A** (automotive) | 0.40 / 0.30 / 5.0 mm, 4 mm | OFE Cu, ENi 5-8 um | WEG 50/50, Al housings, no fine filter | 41 |
| **C-Al** | 0.50 / 0.50 / 5.0 mm, 4 mm | Al 6063, CAB-brazed | all-aluminium WEG loops | 25 |

**AI result vs CoolIT** (15 kW, 18 LPM, 45 C, 117 cm2; the core is identical to the programme's HMMC-R, so the power-electronics-first family gives up nothing on the AI side):

| metric | CoolIT 15 kW | PX-15 same paste | **PX-15 Tier 1 (PCM)** | PX-15 Tier 2 (liquid metal) |
|---|---|---|---|---|
| avg / max case-to-inlet | 34.4 / 44.2 K | 30.0 / 35.0 K | **28.0 / 31.1 K** | 22.9 / 25.0 K |
| plate dP, 18 LPM (incl. 50 um screen) | ~25 kPa est. | 5.7 kPa | **5.7 kPa** | 5.7 kPa |
| Q at T_case,max <= 85 C | ~12.7 kW | 18.4 kW | **21.6 kW** | 29.7 kW |

**Power-electronics result vs the HybridPACK Drive G2 pin-fin baseline** (10 L/min WEG 50/50, 65 C, six switches at 1 kW peak, 617 W/cm2 at the die):

| variant | Rth(j-f) per switch | dP at 10 L/min | hottest-switch Tj | SiC area at equal Tj |
|---|---|---|---|---|
| pin-fin baseline, series flow | 0.100 K/W | 7.6 kPa (-40 C: ~19, estimated) | 178.9 C | ref |
| **PE-A1**: C-A cartridge, solder (drop-in) | 0.082 (-18 %) | 2.9 kPa (-40 C: <= 10) | 156.9 C | -15 % |
| **PE-A2**: C-A cartridge, Ag sinter | 0.078 (-22 %) | 2.9 kPa | 152.6 C | -18 % |
| **PE-DS-R**: C-R direct-substrate (filtered loop) | 0.056 (-44 %) | 3.2 kPa | 129.3 C | -32 % |
| **PE-DSC**: C-A on both sides | 0.043 (-57 %) | 0.7 kPa per side | 115.7 C | -44 % |

**Five decisive differentiators:**

1. **Fresh coolant at every die and every switch.** A 4 mm flow length under a metering comb removes the serial caloric ramp: GPU flow-driven hot spot 1.5 K vs 8.8 K; on a six-pack the hottest switch sees 5.3 K of coolant rise instead of 8.1 K and the spread falls from 12.3 to 5.0 K.
2. **The manifold is what makes fine fins affordable in viscous, cold coolant.** Straight-through skived fins at 0.40 mm cost 8.4 kPa hot and **~370 kPa at -40 C**; the C-A cartridge costs 2.9 kPa and <= 10 kPa. At 0.15 mm, straight fins cost 113 kPa against 3.2 kPa. Without the manifold, the skived fin field cannot be used in an EV or a 15 kW plate.
3. **Tied sandwich.** Every fin tip is bonded, so pressure bow is zero and the plate is 24x stiffer than a plain 2 mm plate (6x a skived base). This allows a 1.0 mm base (half the base term), keeps bond lines uniform, and lets the fins carry <= 10 MPa of sinter pressure.
4. **One face, two interface families.** The same cartridge face is lapped for PCM or liquid metal (AI) or sintered to an AMB (power). In the data-centre PG25 loop this lets a SiC switch carry **1.71 kW vs 0.94 kW** (PCM on a skived plate) at Tj 150 C. That is 1.8x the loss per cm2 of SiC.
5. **One part family, one supply chain, one evidence base.** 800 VDC power plates ship in the same rack kit and pass the same OCP test matrix as the GPU plates. The automotive grade is a licensable baseplate, not a new business.

**Honest framing.** In automotive loops the coarse gaps (>= 0.4 mm) cap h_eff at ~41 kW/m2K. There, most of the Rth gain comes from fin *area* (0.30 mm skived fins vs ~2 mm pins), and the manifold contributes dP, cold-start capability and uniformity. The aluminium grade does not beat a *copper* pin-fin baseplate (+9 %); it beats aluminium pin fins by 9-17 %. Double-sided cooling is prior art, and our core adds 23 % on top of it (0.043 vs 0.055 K/W).

---

## 2. Thermal core

**Geometry and terms.**

| item | C-R (AI / data-centre power) | C-A (automotive) |
|---|---|---|
| fins | skived OFE C10100, 0.10 thick / 0.15 gap / 2.0 tall | 0.30 / 0.40 / 5.0 (H/t 17) |
| flow length / slot pitch | 4 mm / 8 mm | 4 mm / 8 mm |
| base | 1.0 mm as-bonded, 0.8 mm minimum finished | 2.0 mm (optimum is flat at 2-3 mm when h_eff is 41) |
| channel state | 0.083 m/s, Re 19 (PG25, 18 LPM); 0.069 m/s, Re 14 (WEG, 10 L/min) | 0.029 m/s, Re 16 (WEG, 10 L/min) |
| fin efficiency / h / h_eff | 0.56 / 13.2 / 127 kW/m2K (WEG: 0.62 / 10.3 / 108) | 0.65 / 4.2 / 41 kW/m2K |
| caloric | isothermal cell, NTU 1.25, 0.60 x dT_out | 0.55 x dT_out |
| AI term budget, Tier 1 | caloric 7.6 + PCM 7.1 + base 3.3 + convection 10.1 = 28.0 K; hot spot 1.5 flow + 1.5 scatter | - |

**Flow path** (all grades): port -> integrated screen -> L1 header -> centre-fed L2 slot -> comb holes -> plenum and tie grate -> 4 mm down the fin gaps in both directions -> outlet slot -> header -> port.

**Zoning.**
- *GPU/HBM.* Comb hole density follows the power map. The die block gets >= 85-90 % of the flow, HBM columns 0.3-0.5x average, and unheated area only an anti-stagnation bleed. HBM is never downstream of a die. A stepped Cu pedestal reaches the HBM plane within 0.05-0.1 mm.
- *Power modules.* Slots sit only under the switch/die rows. DC-link and busbar zones get none. In coarse laminar C-A channels, h barely depends on velocity (fully developed Nu), so zoning there buys caloric uniformity and saves flow; it does not raise h.

**Interface strategy by tier.**

| tier | application | interface | R'' (cm2K/W) |
|---|---|---|---|
| AI-T1 drop-in | lidded GPU/ASIC | PCM pad (PTM7950 class), 20-30 psi | 0.055 |
| AI-T2 OEM | Ni/Au lid | Ga-In liquid metal on 3-5 um Ni, dam | 0.015 |
| AI-T3 co-design | bare die | stepped pedestal, liquid metal | 0.015 (lid and TIM1 removed) |
| P1 drop-in | power module (module vendor process) | SnSb/SAC solder 0.10 mm | 0.020 |
| P2 sinter | power module | Ag sinter 0.04 mm, <= 10 MPa or pressureless | 0.003 |
| P3 assembly | baseplate-less modules / top-side-cooled discretes | PCM 0.08 (module-scale bond line) / isolating gap pad 0.5 | 0.08-0.5 |
| P4 double-sided | power card | sinter both sides + 1 mm Cu spacer | - |

**Calibration of the power baseline.** We fitted the pin-fin h_eff (referred to the base) to Infineon's 0.103 K/W, less 0.003 K/W for caloric rise. The result is **22.3 kW/m2K**. A Zukauskas estimate for 2 mm pins on a 3.0 x 2.6 mm staggered pitch, 8 mm tall, gives 39 kW/m2K with no tip bypass and 20-27 with 30-50 % bypass, so the fit is plausible. The relative gain grows with SiC area per switch: PE-A1 -9 / -18 / -25 % and PE-DS-R -35 / -44 / -50 % at 1.22 / 1.62 / 2.03 cm2.

---

## 3. Hydraulic architecture

**AI plate (PX-15), 18 LPM PG25.**
- *Velocities.* Ports 16 mm at 1.49 m/s; headers <= 1.0 m/s; slot entry <= 0.5 m/s; 0.5 mm comb holes ~1.2 m/s; fin gaps 0.083 m/s.
- *dP.* Ports 2.57 + headers 0.50 + comb 2.00 + channel 0.23 + turns 0.01 + clean screen 0.4 = **5.7 kPa** (4.2 kPa with 20 mm ports). At 36 LPM: 22.4 kPa and 13.5 W, vs 69.3 kPa for the CoolIT-like reconstruction.
- *Uniformity.* The branch is >= 6x the header head and >= 15x the slot-entry head, and it is inertial (comb-dominated), so global max/min 1.10 holds to 2x flow. Flow-driven hot spot 1.5 K at +/-10 %, 2.5 K at +/-20 %.
- *Couplings.* A UQD08 pair costs ~25 kPa at 18 LPM (+/-50 %), four times the plate. Specify 3/4 in (UQD12-class) for 15 kW (~5 kPa) and UQD08 for 2-4 LPM GPU plates.
- *Filtration.* Gap >= 3x the absolute rating of the last filter: integrated pleated 316L screen, 50 um absolute, >= 12 cm2, 0.4 kPa clean, alarm at 3x. 0.6 mm bleeds at slot dead-ends (+0.4 K). Each passage > 2x the next.

**Automotive cartridge in a jacket (PE-A), 10 L/min WEG 50/50.** Ports 14 mm, header 0.4 m/s, comb of 0.6 mm holes metering 1.5 kPa, branch-to-header-head ratio 18 (rule >= 6).

| condition | C-A cartridge | C-R cartridge | pin-fin module + reference cooler |
|---|---|---|---|
| 65 C, 10 L/min | **2.9 kPa** | 3.2 kPa | 7.6 kPa (datasheet [S2]) |
| 25 C, 10 L/min | 3.0 | 3.5 | ~8.0 (estimate) |
| -40 C, 10 L/min | 3.7 (<= 10 with laminar ports and holes) | 15.4 | ~19 (pins Re 14; more if the housing goes laminar) |
| 65 C, 20 L/min | 11.8 | 12.2 | ~30 (inertial scaling) |
| straight skived fins, no manifold, 65 C / -40 C | 8.4 / ~370 kPa (0.40 mm) | 113 / >6,000 kPa (0.15 mm) | - |

- *Screen and velocity.* 125 um absolute stainless screen in the housing (W/d 3.2), >= 15 cm2, with a 20 kPa bypass relief so a clog never starves the inverter. All velocities <= 1.2 m/s, far below Cu erosion limits.
- *Variants.* Double-sided: two cartridges fed in parallel from one header (5 + 5 L/min), 0.7-0.8 kPa per side. Dielectric: PAO-2 at 2.6 kPa for 10 L/min.

**Data-centre power plate (PE-DC), PG25.** A 2.4 kW plate at 2.9 L/min costs only 0.28 kPa. On a ~27 kPa rack header it would draw ~2.6x its rated flow and steal GPU head, so every PE-DC plate carries a keyed inlet orifice sized to the rack's branch dP. A UQD06 pair adds 2-5 kPa at 3 L/min; UQD04 (14-35 kPa) is avoided.

---

## 4. Mechanical & construction

**PX-15 AI plate stack.**
- *Layers and joining.* Cartridge: base 1.0 + fins 2.0 + tie grate 0.5 + plenum 1.5 + comb 0.4 = 5.4 mm, diffusion-bonded (OFE C10100, 850-950 C, 5-10 MPa, vacuum). It is vacuum-brazed (BAg-8 foil on rim and webs only, comb stopped off) into a CNC Cu manifold body (slots, in-plane headers, ports, screen cavity) under a 2.5 mm cover, or co-bonded in one cycle.
- *Envelope.* **~24 mm**, 148 x 152 mm, ~2.2 kg; an 18 mm low-profile variant costs +0.9 K.
- *Strength and ratings.* Designed to annealed OFHC (yield 70 MPa). Tie stress at 3 MPa with 50 % tip bond is 15 MPa; the <= 4 mm perimeter land governs at SF 5.8. MAWP 1.0 MPa, proof 1.5 MPa, burst >= 3.0 MPa (qualified >= 4.5 MPa), vacuum-stable.
- *Surface and mounting.* Lapped to <= 15 um over the die and <= 25 um over 100 mm. Spring screws bear within 10 mm of the die edge, at 20-30 psi (PCM) or 10-20 psi (liquid metal).

**C-A automotive cartridge.**
- *Layers.* Cu base 2.0 mm + skived fins 5.0 mm + stamped OFE tie-comb plate 0.8 mm, brazed to the fin tips = 7.8 mm. ENi-P 5-8 um (mid-phosphorus) all over after braze, which is 2.5-4 % of the gap. Top face lapped to <= 30 um. 4 mm O-ring flange; M4 screws at 1.8-2.2 Nm, as on HybridPACK Drive [S3].
- *Module-process compatibility.* Solder reflow at 250-300 C is harmless to an annealed part. For sintering, the fin field carries 23 MPa at 10 MPa tool pressure (yield 70 MPa), so specify <= 10 MPa, pressureless sinter, or comb-side support tooling.
- *Bow.* The stiffer cartridge cuts post-reflow bow but raises interface stress, so it needs FEA plus a power-cycling gate.
- *Vibration.* A free 5 x 0.3 mm Cu fin has f1 ~7 kHz, above the ISO 16750-3 band. The fins are tied, so nothing frets.
- *Pressure.* 2.5 bar operating / 5 bar proof (automotive); the cartridge itself bursts at >= 3 MPa.
- *Thermal mass.* 4.1 mm of Cu-equivalent per switch cell (20 J/K) vs 6.2 mm (30 J/K) for a pin-fin plate. Zth below 100 ms is unchanged (die/AMB). Where the drive cycle relies on 1-10 s heat storage, a 3 mm base costs nothing thermally (Rth 0.0775 vs 0.0776 K/W).

**PE-DS-R / PE-DC.** The AMB is sintered to a C-R cartridge with a 1.0 mm base (optimum 0.5-1.0 mm at h_eff 108), and a header plate is brazed on. The module vendor moulds frame and gel over it, with UQD06 ports. **PE-DSC:** a power card clamped (or sintered) between two cartridges through a 1 mm Cu spacer.

---

## 5. Manufacturing route at volume

All processes are conventional:

1. Skiving of OFE Cu fin fields: 0.10/0.15 mm (C-R) or 0.30/0.40 mm (C-A). Vendor class: Wieland Microcool, USUSTK, Winshare, Kingka, LORI [KB-M].
2. Photochemical etching of grate and comb (PCB/EMI-shield capacity, phototools US$0.5-3k). Stamping replaces etching for C-A at >= 1M/yr.
3. Joining: diffusion bonding for C-R (batches of 100-300 cartridges per cycle). Vacuum or CAB brazing for C-A (foil on comb webs only, stop-off against wicking into gaps) and for C-Al (Nocolok CAB, the EV-battery-plate chain).
4. CNC of AI manifold bodies. Die-cast or PPS-GF40 jackets are the customer's.
5. ENi plating (C-A), lapping, 100 % He leak (<= 1e-5 mbar L/s, target 1e-6), and 100 % flow/dP signature.

Licensee and channel candidates: pin-fin baseplate makers (Jentech, which is also a Rubin Group-A plate supplier [KB-M]; Dowa / Mitsubishi Materials class [KB-L]); module vendors (Infineon, ST, onsemi, Wolfspeed, BYD Semiconductor) for PE-DS; and the 800 VDC shelf makers (Delta, LITEON, Flex, Megmeet) for PE-DC.

**Unit cost estimates.** The basis is the `manufacturing-cost.md` route costs [KB-M] at Cu ~US$11/kg, to be confirmed by RFQ.

| part | 10k/yr | 100k/yr | 1M/yr | comparator |
|---|---|---|---|---|
| **PX-15 AI plate** (Cu 2.2 kg 25/23, skive 40/24, etch 26/11, cartridge bond 25/14, CNC body 80/34, cover+stubs 14/6, braze 30/16, screen 15/8, lap 12/6, frame 20/14, test 8/5; +12 % yield/overhead) | **~US$330** | **~US$180** | - | Group-A Rubin ASP ~US$400 |
| PX-GPU (110 x 120 mm) | ~US$230 | ~US$130 | - | GB200-class skived ~US$105 at 100k |
| PE-DC power-shelf plate, 2-3 kW, 2-4 C-R zones | ~US$150 | ~US$85 | - | target US$50-150 |
| PE-DS-R integrated cooler, 84 cm2 | ~US$60 | ~US$32 | ~US$20 | pin-fin baseplate US$15-40 |
| PE-A C-A cartridge | ~US$45 | ~US$28 | ~US$19 | forged Cu pin-fin US$15-25 at volume |
| PE-Al cartridge | ~US$30 | ~US$18 | ~US$11 | Al cold plate US$15-40 |

**Automotive value.** PE-A2 saves 18 % of SiC at equal Tj,max. On US$600-900 of SiC per 200 kW inverter (2025) that is US$110-160, or US$75-110 at an assumed -30 % SiC price by 2027. The cartridge premium is US$0-6, so the net is **~US$70-105 per inverter**. Alternatively the same change buys +14 % current, or ~26 K lower Tj for power-cycling life. Royalty target: US$2-5 per module.

**Lead times.** Cartridges 8-10 weeks; AI plates 10-12 weeks; 100k/yr bonding capacity in 9-12 months (2-3 furnaces, US$3-6M); automotive PPAP through a licensee in 24-36 months.

**Yield risks, ranked.** Unbonded tips or rims (flatness < 10 um per layer, C-scan, He leak). Braze wicking into 0.4 mm gaps. ENi thickness uniformity in deep 0.4 x 5 mm slots. Sinter cracking over a stiff base. Fin damage before bonding.

---

## 6. Predicted performance

**6.1 Benchmark point, 15 kW / 18 LPM / 45 C / 117 cm2** (model; P10-P90 from the 20k-sample Monte Carlo):

| design | caloric | TIM | base | conv | avg dT K | max dT K | R'' cm2K/W | dP kPa | pump W | Q cap kW | Tcase,max |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CoolIT-like reconstruction | 6.3 | 9.0 | 6.6 | 12.6 | 34.5 | 44.3 | 0.269 | 24.6 | 7.4 | 12.7 | 89 C |
| PX-15 C-R, same paste | 7.6 | 9.0 | 3.3 | 10.1 | 30.0 (26-37) | 35.0 (31-42) | 0.234 | 5.7 | 1.7 | 18.4 | 80 C |
| **PX-15 C-R, PCM (Tier 1)** | 7.6 | 7.1 | 3.3 | 10.1 | **28.0 (26-31)** | **31.1 (29-35)** | 0.219 | **5.7** | 1.7 | **21.6** | 76 C |
| PX-15 C-R, liquid metal (Tier 2) | 7.6 | 1.9 | 3.3 | 10.1 | 22.9 (22-25) | 25.0 (24-27) | 0.179 | 5.7 | 1.7 | 29.7 | 70 C |
| PX-15 C-P, liquid metal (<= 33 um loops) | 8.2 | 1.9 | 3.3 | 6.8 | 20.2 | 22.3 | 0.158 | 5.8 | 1.7 | 37.0 | 67 C |
| PX-15 C-R direct-to-die (Tier 3) | - | LM | 2.6 | 10.1 | 22.3 | 24.4 | 0.174 | 5.7 | 1.7 | ~31 | 69 C |
| (aluminium body and core, reference only) | 7.3 | 7.1 | 6.4 | 13.1 | 33.9 | 36.9 | 0.264 | 5.7 | 1.7 | 16.8 | 82 C |

**Flow trades (Tier 1).**
- 36 LPM: 23.6 / 26.7 K at 22.4 kPa.
- Equal pumping power (7.4 W, 29.4 LPM): 24.6 / 27.6 K, or 19.5 / 21.6 K with liquid metal.
- CoolIT's 34.4 K average is matched at **10.9 LPM** (0.72 LPM/kW), 2.1 kPa and 0.39 W.

**6.2 Real 2027-28 package** (4 reticle dies at 350 W/cm2 + 16 HBM, zoned), hottest die, case-to-inlet:

| core | PCM | liquid metal | T_case,max |
|---|---|---|---|
| CoolIT-like split-flow | 88.6 K (paste) | ~76 K | ~121 C |
| C-R | 62.3 K | 48.3 K | **93 C** (misses 85 C) |
| C-P (<= 33 um loops) | 53.5 K | 39.5 K | **84 C** |
| C-R direct-to-die | - | ~-28 K at the junction vs lidded | ~80 C |

**6.3 GPU-class plates** (lidded):

| case | CoolIT-like avg / max, dP | PX Tier 1 | PX Tier 2 |
|---|---|---|---|
| Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW | 16.1 / 23.5 K, 2.0 kPa | 18.4 / 20.3 K, 0.1 kPa | 16.9 / 18.5 K |
| Rubin Ultra-class 3.6 kW, 80 cm2, 1.0 LPM/kW | 17.6 / 25.1 K, 3.3 kPa | 19.1 / 21.1 K, 0.3 kPa | 17.3 / 19.0 K |
| CoolIT 4 kW point, 25 cm2, 1.5 LPM/kW | measured < 36 K | 31.0 / 34.4 K, 1.0 kPa | 24.6 / 26.8 K |

**6.4 Power electronics vs pin-fin and ShowerPower** (per switch, 1.62 cm2 SiC, 10 L/min WEG 65 C; module level 6 x 1 kW, outlet rise 9.7 K). At this equal loss the baseline exceeds the 175 C SiC limit; the last two columns show what holding the baseline's Tj buys instead:

| variant | h_eff kW/m2K | Rth mean / max K/W | vs pin-fin | dP kPa | Tj,max C | current at equal Tj | SiC area at equal Tj |
|---|---|---|---|---|---|---|---|
| pin-fin HPD G2 class, series flow | 22 | 0.100 / 0.106 | ref | 7.6 | 178.9 | ref | ref |
| pin-fin, transverse (parallel phases) | 22 | 0.100 / 0.106 | 0 % | 7.6 | 175.7 | +1 % | -2 % |
| ShowerPower-3D class (estimate, [KB-L]) | ~30 | 0.090 / 0.095 | -10 % | n/d ("very low", laminar [S4]) | 165.2 | +7 % | -9 % |
| **PE-A1** C-A, solder | 41 | 0.082 / 0.087 | **-18 %** | **2.9** | 156.9 | +11 % | -15 % |
| **PE-A2** C-A, sinter | 41 | 0.078 / 0.082 | **-22 %** | 2.9 | 152.6 | +14 % | -18 % |
| **PE-DS-R** C-R, sinter, filtered loop | 108 | 0.056 / 0.058 | **-44 %** | 3.2 | 129.3 | +33 % | -32 % |
| today's DSC, pin-fin-class h both sides | 22 | 0.055 / 0.059 | -45 % | 12.5 (Boyd plate [S5]) | 129.0 | +33 % | -36 % |
| **PE-DSC** C-A both sides | 41 | 0.043 / 0.045 | -57 % | 0.7 per side | 115.7 | +50 % | -44 % |
| PE-DSC-R, C-R both sides | 108 | 0.031 / 0.032 | -69 % | 0.8 per side | 103.3 | +72 % | -52 % |
| PE-Al cartridge on DBA | 25 | 0.109 | +9 % (Al pin-fin 0.120: -9 %) | 2.9 | 187.2 | -3 % | +6 % |

Published anchors, all consistent with this model's die-referenced 0.162 cm2K/W for the pin-fin baseline:
- NREL WEG jet impingement: ~0.15 cm2K/W die-referenced [S6].
- EPFL manifold-microchannel SiC module: 9.85 mm2K/W = 0.099 cm2K/W (water, lab) [S6].
- PE-DS-R: 0.091 cm2K/W.

**6.5 Dielectric coolant (PAO-2, 65 C).**
- C-A: 0.107 K/W (+37 % vs WEG), against 0.174 K/W for pin fins in PAO, so our advantage widens to -39 %.
- C-R in a filtered PAO loop: 0.074 K/W, better than pin fins in WEG.
- To hold the same caloric rise, PAO needs 2.1x the volume flow (11 kPa).
- Verdict: use dielectrics only where isolation or oil-integrated e-axles demand them; there the short-flow-length core differentiates most.

**6.6 Data-centre 800 VDC power** (PG25 at 45 C, Tj 150 C). Loss a 1.62 cm2 switch can carry:

| assembly | loss per switch | per cm2 of SiC |
|---|---|---|
| tube plate + gap pad | 0.34 kW | 208 W/cm2 |
| skived plate + gap pad | 0.55 kW | 337 W/cm2 |
| skived plate + PCM | 0.94 kW | 582 W/cm2 |
| PE-DC (0.25 mm de-rated core) + PCM | 1.09 kW | 674 W/cm2 |
| **PE-DS-R direct substrate** | **1.71 kW** | **1,055 W/cm2** |

With a gap pad, the plate choice moves Tj by only 6-7 K (64.8 vs 58.1 K at 400 W): the interface dominates. The product is therefore the sintered direct-substrate module, not a better plate under a pad.

**Where it does not win.**
1. Rubin-class flux (38-45 W/cm2) at 1.0-1.2 LPM/kW: the average is 1-2 K worse than split-flow (isothermal-cell caloric). It wins on maximum, dP and uniformity.
2. The 350 W/cm2 package with the robust core: 93 C.
3. Height: 24 mm, and 2.2 kg.
4. Coarse automotive features: -18 to -22 %, not -44 %.
5. Aluminium vs copper pin fins: +9 %.
6. The AI dP win is against a reconstruction.

---

## 7. Product family & applications

| product | cartridge / body | interface | what changes |
|---|---|---|---|
| PX-15 (15 kW TTV, Rubin Ultra / Feynman class) | C-R (C-P option), Cu body | PCM / LM | 3/4 in couplings, comb artwork per power map |
| PX-GPU (Rubin, MI455X, ASICs, 1.8-4 kW) | C-R, 110 x 120 mm, 16-18 mm | PCM / LM / bare die | UQD08, 12 mm bores |
| PX-CPU / NVSwitch / CPO switch | C-R, 1.5 mm fins | PCM | lasers held within +/-3 K by uniform feed |
| PX-Wafer / multi-chip | C-R, tiled headers | per-die pads | manifold scales; flow length stays 4 mm |
| **PE-DC** 800 VDC shelves, sidecars, DC-DC | C-R/C-D zones in a Cu plate | PCM / gap pad, or sintered PE-DS-R modules | keyed orifice, UQD06, magnetics potted to plain-channel zones |
| **PE-DS-R** SiC/GaN modules in PG25 or DI loops (SST front ends, solid-state breakers) | C-R as module baseplate | Ag sinter | sold to module vendors, 1.8x loss per cm2 SiC |
| **PE-A** EV traction six-packs, power cards | C-A in an O-ring jacket | solder / sinter / DSC | ENi, 125 um screen, AQG 324; licence |
| PE-Al chargers > 350 kW, MCS, ESS | C-Al | DBA / TIM | all-Al loops only |
| Niches: laser diodes, RF GaN (PAO), directed energy | C-R/C-P, Au/Ni | solder | isolation, DI water, ITAR |

**What "SSD converters" could mean.**
1. **SiC converters**, almost certainly a typo. Covered by PE-A, PE-DS and PE-DC.
2. **Solid-state transformers** (MV AC to 800 VDC), now commercial. Examples: Delta; Navitas/EPFL at 250 kW, 3.3 kV; Enphase IQ SST with 342 GaN modules per 1.25 MW at 98.5 %; Siemens/Reinhausen at 36 kV [S7]. 15-25 kW of heat per MW from expensive MV dies on isolated substrates. Medium-good fit via PE-DS-R, Ni/Au-plated for DI water.
3. **Solid-state DC breakers** for 800 VDC, ~0.5-1 kW of continuous conduction loss per 1,000 A [KB-L]. Same PE-DS-R part.
4. **SSD storage** (E1.S/E3.S, 25-40 W, ~1-2 W/cm2). Pads and serviceability dominate and our core solves nothing; at most a commodity rail.

**Recommendation.**
- *Best fit:*
  1. Data-centre 800 VDC power in the PG25 loop. Same loop, chemistry, customers and test spec, and fine channels are allowed. Delta/LITEON 110 kW shelves shed ~2.2-2.8 kW each [S7][KB].
  2. Premium SiC in sealed, filtered loops: hypercars, motorsport, eVTOL, heavy trucks and MCS.
  3. SST / MV power rooms.
- *License only:* volume EV traction. The module vendor owns the baseplate, AQG 324 takes 24-36 months, cost pressure is extreme, and Danfoss SP3D IP sits nearby.
- *Avoid:* rail, HVDC/STATCOM, PV/wind/ESS PCS and industrial drives (aluminium commodities, 20-40-year qualification, low flux), and SSD cooling.

---

## 8. Reliability, qualification & drop-in compatibility

**Data-centre (AI and PE-DC).**
- *Coolant and envelope.* OCP PG25 with bare OFE Cu, 316L stubs and peroxide-cured EPDM; no Al, Zn, non-DZR brass, NBR or silicone. Rated at 45 C (W45), characterised at 50 C (W+), outlet <= 65 C, curves at 0.5-1.5 LPM/kW in OCP Cold Plate Test Spec v1.0.0 format [S8].
- *Pressure and leak.* MAWP >= 100-150 psi, proof 1.5x, burst >= 3x and > 20 bar (ours >= 30 bar, qualification 45 bar); He <= 1e-5 mbar L/s on 100 % of parts.
- *Cycling.* 10,000 pressure cycles, 1,000 cycles at 10-65 C, 50 storage cycles at -40/+70 C and 1,000 power cycles, with R drift <= 5 % and dP drift <= 10 %.
- *Fouling and soak.* 500-1,000 h dosed-particulate test behind the screen; 1,000-3,000 h soak at 65 C with a Cu-ion tripwire < 1-2 ppm.
- *Leak-before-break.* Ductile annealed Cu, no brittle braze in the pressure boundary.

**Automotive (PE-A, run with the licensee).**
- *Module.* ECPE AQG 324 (PCsec/PCmin power cycling, thermal shock -40/+150 C, ISO 16750-3 vibration and shock), then IATF 16949 / PPAP.
- *Coolant and life.* ASTM D1384 / D2570 corrosion with OAT/Si-OAT WEG at 88-90 C on Cu/ENi, solder, brass, steel and cast-Al coupons; >= 1M pressure pulsations at 0.5-3 bar; -40 C cold-start flow; 15 years / 8,000 h [KB-M].
- *Galvanic rule.* The finned cartridge wets ~2x the area of a pin-fin plate (area ratio 14.9 vs ~7), so it is a larger cathode against the Al housing. Hence ENi all over (it blocks the Cu-ion release that pits aluminium), an electrically floating cartridge (insulating O-ring, isolated screws) and Si-OAT inhibitor.

**Our added tests:** clustered blockage at slot ends (+17 K for a blocked 4 mm cluster at 128 W/cm2); sinter-on-cartridge power cycling (>= 50k cycles at dTj 100 K); post-reflow bow maps; ENi cross-sections in 0.4 x 5 mm slots; independent-lab repeat of the AI headline point.

**Service life:** 10 years for AI plates (field-replaceable PCM, screen checked from the dP signature) and for PE-DC; life of vehicle, sealed, for automotive.

---

## 9. IP posture

- **Expired foundations we build on:** Tuckerman-Pease microchannels, the Harpole/TRW manifold microchannel (US 5,088,005), MIT/Creare normal-flow laminates, IBM cross-hatch distribution, the original Danfoss ShowerPower filings (~2003-05), pin-fin direct-cooled baseplates, and Cu skiving and diffusion bonding as public process art.
- **What we avoid:**
  - CoolIT's single-central-slot Split-Flow claims (US 8,746,330 / 9,603,284 / 12,495,513, to ~2028; verify).
  - Danfoss ShowerPower 3D meander/swirl baseplates (live to ~2039-41 [KB-L]). We use no meanders, no swirl elements and no flow along the baseplate.
  - JetCool/Flex jet arrays; Nvidia in-plate sensing and valves; two-phase dielectric families; Tier-1 housing IP.
- **Verify before design freeze:** Purdue embedded 3-D manifold on SiC (IJHMT 2019); EPFL/Corintis co-designed manifold microchannels and heat-map topologies (2020-25); newer Toyota/Denso/Hitachi double-sided card families; Mikros laminate continuations.
- **What we claim** (provisionals before any disclosure, then PCT):
  1. The pressure-rated tied cartridge used as a power-module baseplate, sintered or soldered to an AMB and O-ring sealed into a jacket.
  2. Comb hole density mapped to die or switch positions.
  3. A double-sided card with two cartridges fed in parallel from one header.
  4. A keyed-orifice power plate that self-balances against GPU branches.
  5. The manifold flow-length rule for cold, viscous coolant.
  6. The HMMC-E AI claims (comb, tie grate, pedestal, integrated screen).
- **FTO budget:** opinions on ~12 families, US$50-110k, 10-14 weeks.

---

## 10. Risks, experiments and roadmap

| risk | likelihood / impact | mitigation |
|---|---|---|
| Automotive coarse-gap gain (-18 to -22 %) too small to displace pin fins at their cost | medium / segment | lead with PE-DS-R in filtered loops; offer C-A with sinter; sell current headroom and life |
| Fouling and corrosion in Al/WEG loops (0.4 mm, ENi, 2x cathode area) | medium / life | 125 um screen with relief, ENi, isolated cartridge, D1384/D2570 gate |
| Sinter or solder cracking over a stiff cartridge; bow after reflow | medium / reliability | FEA, <= 10 MPa or pressureless sinter, >= 50k power cycles |
| Flow uniformity assumed (theta_c 1-2.5) | medium / +1 K | water table, comb is the regulator |
| Diffusion-bond yield and furnace capacity | medium / cost | C-scan, braze fallback, two bonding sources |
| 350 W/cm2 out of reach for C-R | certain / segment | C-P behind 25-33 um filtration; direct-to-die |
| Danfoss SP3D / EPFL-Corintis / Purdue IP | medium | FTO before freeze; narrow implementation claims |
| PE-DC plate starving GPU branches | low with orifice / high without | keyed orifice; mixed-rack test |
| SiC price deflation erodes the die-saving value | high / pricing | sell density (W/cm2 SiC) and life, not only area |

**Five experiments that retire the most risk:**
1. **Slot-pair water table plus bonded coupons** (8 weeks). Theta_c and uniformity at 18/36 LPM and at 10 L/min WEG; tip-bond fraction by C-scan; burst >= 4.5 MPa.
2. **Direct-substrate demonstrator** (12 weeks). Si3N4 AMB with 8 SiC (or resistor) dies, sintered to C-R and C-A cartridges. Rth(j-f) measured by Vsd(T) at 10 L/min WEG 65 C against an HPD G2 pin-fin module on Infineon's reference cooler, then 50k power cycles. This retires the -18 / -22 / -44 % claims and the sinter risk.
3. **Chemistry and fouling rigs** (16 weeks, start at month 1). C-A in a cast-Al loop with Si-OAT WEG at 90 C, dosed with ISO 12103 A2 dust and casting sand, behind a 125 um screen; C-R behind 50 um in PG25.
4. **Cold start, pulsation and vibration** (10 weeks). -40 C flow/dP curves, 1M pressure pulsations, ISO 16750-3 on a cartridge-in-jacket assembly.
5. **AI TTV-A parity plus a mixed-rack branch** (10 weeks after first plates). OCP-format 15 kW test (3 plates x 3 assemblies, PCM and liquid metal), then a PE-DC plate with keyed orifice in a 4-6-tray branch.

**Roadmap (months from go):**

| months | milestones |
|---|---|
| M0-3 | Detailed design, CFD, FTO searches, provisionals; vendors engaged; one 800 VDC shelf maker and one module vendor under NDA |
| M3-6 | C-R and C-A cartridges and coupons; fouling/chemistry rigs running; direct-substrate demonstrator built |
| M6-9 | PX-15 TTV-A parity; direct-substrate Rth; PE-DC shelf-plate samples; cold-start and vibration tests |
| M9-12 | Shared OCP qualification matrix for PX-15/PX-GPU and PE-DC; AQG-324-style pre-qualification of PE-DS with the module partner; pilot bonding line |
| M12-18 | AI customer qualification (hyperscaler ASIC first); first PE-DC PO in a rack kit; automotive licence term sheet; second bonding source. Data-centre products qualified at M15-18; automotive PPAP follows via the licensee (24-36 months) |

---

## 11. Scorecard vs CoolIT 15 kW

15 kW, 18 LPM PG25, 45 C, 117 cm2. Conservative = Tier 1 (C-R, PCM) at the Monte-Carlo P90; nominal = median; stretch = Tier 2 liquid metal on C-R [C-P in brackets].

| metric | CoolIT 15 kW | conservative | nominal | stretch |
|---|---|---|---|---|
| average case-to-inlet dT | 34.4 K | <= 32 K | **28.0 K** | 22.9 K [20.2] |
| maximum case-to-inlet dT | 44.2 K | <= 35 K | **31.1 K** | 25.0 K [22.3] |
| T_case,max at 15 kW | 89.2 C | <= 80 C | 76 C | 70 C [67] |
| same-paste like-for-like average / max | 34.4 / 44.2 K | <= 34 / <= 38 K | 30.0 / 35.0 K | 26.5 K at equal pump power |
| unit resistance R'' (avg) | 0.269 cm2K/W | <= 0.25 | 0.219 | 0.179 [0.158] |
| plate dP, 18 LPM, incl. screen | undisclosed, ~25 kPa est. | <= 8 kPa | **5.7 kPa** | 4.2 kPa (20 mm ports) |
| hydraulic pumping power, 18 LPM | ~7.4 W | <= 2.4 W | 1.7 W | 1.3 W |
| dP at 2x flow (36 LPM) | ~69 kPa (reconstruction) | <= 30 kPa | 22.4 kPa | ~16 kPa (20 mm ports) |
| Q capacity, T_case,max <= 85 C, 1.2 LPM/kW | ~12.7 kW | >= 18 kW | **21.6 kW** | 29.7 kW [37.0] |
| flow to match 34.4 K average | 18 LPM | <= 12 LPM | 10.9 LPM (0.39 W) | < 9 LPM (LM) |
| 350 W/cm2 reticle package, T_case,max | ~121-134 C | 107 C (PCM) | 93 C (LM) | 84 C [C-P, LM]; ~80 C direct-to-die |
| flow-driven hot spot (max - avg) / service life vs skived | 8.8 K / 1.0x | <= 2.5 K / >= 0.6x | 1.5 K / 1.0x | 0.7 K / 1.2x behind 25 um |
| unit cost, 15 kW class | n/d | US$330 (10k) | US$180 (100k) | ~US$155 (one-cycle co-bond, 300k/yr) |
| height / mass (we do not win this) | n/d (est. 12-20 mm) | 24 mm / 2.4 kg | 24 mm / 2.2 kg | 18 mm LP (+0.9 K) |
| **PE: Rth(j-f) vs HPD G2 pin-fin, 10 L/min WEG 65 C** | (0.100 K/W baseline) | -18 % (C-A, solder) | -22 % (C-A, sinter) | -44 % (C-R direct substrate); -57 % double-sided |
| **PE: module dP at 10 L/min, 65 C / -40 C** | (7.6 / ~19 kPa) | <= 4 / <= 12 kPa | 2.9 / ~4-10 kPa | 2.9 kPa |
| **PE (data-centre): loss per cm2 SiC at Tj 150 C, 45 C PG25** | (582 W/cm2, PCM on skived) | 674 W/cm2 (PE-DC + PCM) | 1,055 W/cm2 (PE-DS-R) | 1,055 W/cm2 + double-sided |

**Sources.**
- [S1] Infineon FS01MR12A8MA2B datasheet: https://www.infineon.com/assets/row/public/documents/10/49/infineon-fs01mr12a8ma2b-datasheet-cn.pdf
- [S2] Infineon FS980R08A7F32B datasheet (dP, 10 dm3/min, 65 C; value to be confirmed typ/max): https://www.infineon.com/assets/row/public/documents/10/49/infineon-fs980r08a7f32b-datasheet-en.pdf
- [S3] Infineon FS410R12A7P1B / FS1000R08A7P3B datasheets (pin-fin, M4 1.8-2.2 Nm, 760 g): https://www.infineon.com/assets/row/public/documents/10/49/infineon-fs410r12a7p1b-datasheet-en.pdf
- [S4] Danfoss DCM technical FAQ (laminar, very low dP): https://eepower.com/technical-articles/11-technical-faqs-about-the-danfoss-dcmtechnology-platform-for-automotive-traction-inverters/ ; ShowerPower 3D PCIM 2022: https://www.vde-verlag.de/proceedings-en/565822099.html
- [S5] Boyd HybridKIT DSC plate, 0.026 K/W, 12.5 kPa at 10 LPM: https://info.boydcorp.com/hubfs/Company/Partnerships/Boyd-HybridKIT-DSC-Liquid-Cold-Plate-Datasheet.pdf
- [S6] EPFL integrated manifold-microchannel SiC module: https://infoscience.epfl.ch/handle/20.500.14299/250011 ; NREL jet-impingement value per search summary (vde-verlag PCIM 2025 thermal-modelling paper context): https://www.vde-verlag.de/proceedings-en/566541305.html
- [S7] Nvidia 800 VDC blog: https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/ ; GTC 2026 partners (Delta 660 kW rack, six 110 kW shelves; LITEON 110 kW shelf): https://www.powerelectronicsnews.com/nvidia-gtc-2026-800-vdc-power-partnerships-from-grid-to-processor ; https://datacenter.news/story/delta-unveils-800-vdc-power-cooling-for-ai-data-centres ; Navitas/EPFL SST: https://www.yolegroup.com/industry-news/navitas-epfl-to-demonstrate-novel-solid-state-transformer-solution-for-ai-data-center-enabling-800-v-dc-implementation/ ; Enphase IQ SST: https://www.pv-magazine.com/2026/07/07/enphase-targets-800-v-dc-data-centers-with-distributed-solid-state-transformers/
- [S8] OCP cold-plate test spec, PG25, UQD and ASHRAE requirements as captured in `research/SYNTHESIS-benchmark-and-requirements.md` and `standards-reliability.md`.
