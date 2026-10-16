# CrossComb: a conventionally manufactured N-slot distributed-feed cold plate that beats the CoolIT 15 kW Split-Flow plate

**Lens:** conventional-cost (key `conventional-cost`). Manufacturing-led architecture using only processes already run at >100k cold plates/yr: skiving, CNC/gang-slitting, stamping, vacuum brazing, laser welding, Ni plating. No etching, no diffusion bonding, no AM.
**Operating point throughout:** 15 kW, 18 LPM PG25 (1.2 LPM/kW), 45 C inlet, 117 cm2 calibrated footprint (108 x 108 mm, 128 W/cm2). Benchmark: 34.4 K average / 44.2 K maximum case-to-inlet, standard paste, dP undisclosed (our reconstruction ~25 kPa, band 17-42).
**Model runs:** `appendix/design/crosscomb_model_run.py` (imports `docs/cooling/model/coldplate_model.py` unchanged), output in `crosscomb_model_output.md`. Treat every modelled term as +/-25 %.

---

## 1. Concept in one page

**What it is.** A four-part, all-copper, single-braze-cycle plate: a **skived fine-fin core** (0.10 mm fins, 0.15 mm gaps, 2.0 mm tall, 1.0 mm base) crossed at 90 degrees by a **gang-slit copper comb** that forms 27 alternating inlet/outlet slots at 4 mm spacing, a **stamped selector floor** whose metering slits connect each slot to the right header, and a **CNC header bar** carrying two end-fed headers and 16 mm ports. The comb webs are vacuum-brazed to the fin tips, so the base is a tied plate-fin pressure vessel and can be 1.0 mm thick. Every fluid parcel enters at inlet temperature, travels 4 mm along a fin channel and leaves. The interface is a phase-change pad (Tier 1, drop-in) or liquid metal on Ni (Tier 2, OEM).

**Why it beats CoolIT.** CoolIT's 34.4 K decomposes as caloric 6.3 + paste 9 + 2 mm base 6.5 + convection 12.6 K, with a 54 mm single-split flow path that forces 0.2 mm fins (fine fins would cost 4x the pressure drop) and produces the 8.8 K systematic hot spot at the outlet edge. CrossComb removes the flow-length constraint: with 4 mm channels the fin friction is 0.24 kPa, so 0.15 mm gaps and a 2.0 mm fin height run at 18 LPM for 6.3 kPa port-to-port, not ~25 kPa. That buys convection 12.6 -> 10.1 K, base 6.5 -> 3.3 K, and the outlet-edge ramp 8.8 -> ~2 K. The PCM pad (which the stiff, bow-free sandwich can hold at its datasheet value) takes the TIM from 9 to 7 K. Net: **28.0 K average / 31.6 K maximum at 6.3 kPa (Tier 1)**, 22.9 / 25.5 K with liquid metal (Tier 2), and 30.0 / 35.5 K with CoolIT's own paste, like for like.

**The five decisive differentiators**

1. **4 mm flow length from a gang-slit comb, not a central slot.** 27 slots fed in parallel instead of one; fin friction becomes negligible, so fin geometry is chosen thermally, not hydraulically. Pressure drop 4x lower than the reconstructed benchmark and 86 % inertial, so it scales as Q^2 to 24.6 kPa at 36 LPM (benchmark ~70 kPa).
2. **Tied sandwich, 1.0 mm base.** Fin tips brazed to the comb webs make pressure self-equilibrating; the stack is ~24x stiffer than a 2 mm skived base, has zero pressure bow and 3x less mount/thermal bow, which is what lets a pad TIM hold 0.055 cm2K/W across a 100 mm package.
3. **Programmable zoning at zero tooling cost.** Slot pitch (skiving/slitting NC) and selector-slit width (stamping or laser pattern) set per-zone flow; die zones get 85-90 % of the flow, HBM columns 0.3-0.5x, dead area none. The across-die gradient on a 4-die package falls from 22-30 K (split-flow) to 6-8 K.
4. **Metered, fouling-tolerant hydraulics.** 1.2 x 12 mm selector slits (2.5 kPa) make the branch resistance inertial and 8x the header dynamic head, so slot-to-slot uniformity holds at 2x flow; a serviceable 50 um absolute inlet screen and 4 % dead-end bleed notches give a 0.15 mm channel a 10-year life on today's 50 um loops.
5. **Cost and supply chain identical in kind to the incumbent.** Skiving houses, horizontal mills, a stamping die, a vacuum-braze furnace and a laser cell; US$145 factory cost at 100k/yr (vs ~US$105 for a skived split-flow plate), i.e. a US$280-300 ASP plate with 45-50 % gross margin, at 1.7x the Q capacity of the benchmark (21 kW vs ~13 kW at T_case <= 85 C).

**Where it does not win:** height (33 mm at the header bar vs ~15-20 mm), mass (1.8 kg vs ~1.5 kg), a brazed (Ag-Cu eutectic) rather than filler-free joint, and on uniform low-flux (<50 W/cm2) GPU-class TTVs at 1.2 LPM/kW the average dT is 1-2 K worse (the fluid saturates toward outlet temperature); it still wins there on maximum dT, dP and at equal pumping power, and on real die-concentrated packages.

---

## 2. Thermal core

| Element | Specification | Rationale |
|---|---|---|
| Material | OFE copper C10100/C10200 throughout (ETP C11000 excluded: H2 embrittlement in furnace atmospheres) | k 390 W/mK; braze-compatible; all-copper wetted path |
| Fin field | 108 x 108 mm (TTV) or package-specific; fins along x; 0.10 mm fin / 0.15 mm gap / 0.25 mm pitch / 2.0 mm tall; 432 fins | Fouling floor 0.15 mm behind a 50 um absolute screen; AR 20 is inside the commercial skiving window; h_eff 127 kW/m2K, eta 0.56 |
| Base | Skived at 2.0 mm (blank 2.8 mm), fly-cut after brazing to 1.0 +/- 0.1 mm, 0.8 mm minimum under the die; land 1.8 mm | 2 -> 1 mm is worth 3.3 K; thinner is better for max temperature (1 mm already smooths the 8 mm sawtooth to ~0.7 K pk-pk); 0.8 mm is the erosion + flatness floor |
| Flow path | Fluid descends from an inlet slot (3.0 mm wide) into the fin gaps, runs 4 mm along x under a 1.0 mm web, rises into the adjacent outlet slot; 13 inlet + 14 outlet slots at 4 mm centres; ~11,600 parallel 4 mm segments | Isothermal cell: caloric term 0.60 x 12.7 = 7.6 K (vs 6.3 linear) but no long-wave ramp; channel u 0.083 m/s, Re 19 |
| Zoning (real packages) | Slot pitch 8 mm over dies, 12-16 mm over HBM/periphery; selector slit width per slot sets zone flow (die block >= 85 % of flow); fin field cropped to die block + HBM columns; HBM stepped pedestal machined into the die-side face to within 0.05-0.1 mm of the HBM plane | Heat-proportional zoning restores 6.4 K fluid rise under the die and cuts 15 K off the hot die vs un-zoned; pads over a 0.4 mm HBM step fail above ~15 W/cm2 |
| Interface, Tier 1 (drop-in, lidded) | Phase-change pad (PTM7950 class, 0.055 cm2K/W) at 20-30 psi, plate flatness <= 20 um over the die, Ra <= 0.8 um | Bow-tolerant; no pump-out; the benchmark's 10 K plate-to-plate spread is grease on a bowing plate |
| Interface, Tier 2 (OEM co-design) | Ga-In-Sn liquid metal 0.015 cm2K/W on 3-5 um electrolytic Ni (no Au), polymer dam, 20-30 um BLT; no Al in module or loop | -5.1 K average; Ni t/k <= 0.001 cm2K/W |
| Interface, Tier 3 (chip co-design, bare die) | Same stack, die-side face machined as a stepped pedestal (two or three heights, +/-0.05 mm), LM + dam, 10-20 psi on die | Junction-to-inlet 0.14 vs 0.28 cm2K/W: ~28 K at 350 W/cm2; CuW/CuMo only if a soldered lid is demanded |

Nominal term budget, Tier 1 at the benchmark point: caloric 7.6 + TIM 7.1 + base 3.3 + convection 10.1 = **28.0 K**; hot-spot adders: flow maldistribution 1.3 K (+/-10 % long-wave) + 8 mm-period base ripple 0.7 K + PCM scatter 1.5 K = 3.6 K -> **31.6 K maximum**.

**Where conventional limits cap this core.** Skiving stops at ~0.20-0.25 mm pitch in production (h_eff <= 130-190 kW/m2K; convection >= 7-10 K at 128 W/cm2); the performance core (0.10/0.10 x 1.5 mm, h_eff 187) is skivable but gated by <= 25-33 um loop filtration, not by the machine. Base thickness cannot go below 0.8 mm finished (skiving needs >= 1.5-2 mm during the cut; fly-cutting takes the rest). Slot width and web width cannot go below ~2.5-3 mm and ~0.8-1.0 mm with slitting saws, so slot pitch >= 7-8 mm and flow length >= 3.5-4 mm; an etched 2 mm-pitch manifold would gain only ~0.5 K on the maximum. The paste/pad interface (7-9 K) remains the single largest term a drop-in plate carries; only Tier 2/3 remove it.

---

## 3. Hydraulic architecture

| Level | Feature | Size | Velocity at 18 LPM | Loss at 18 LPM |
|---|---|---|---|---|
| L0 ports | 2 x 16 mm bore horizontal stubs at one end of the header bar (U-type) | 16 mm | 1.49 m/s | 2.6 kPa (2 ports, turns) |
| Screen | 50 um absolute 316L pleated cartridge in the inlet boss, 12 cm2, serviceable from the port | - | - | 0.4 kPa clean; alarm at 3x |
| L1 headers | End-fed inlet 25 x 14 mm, outlet 30 x 14 mm, 3 mm walls, in the header bar | 350 / 420 mm2 | 0.86 / 0.71 m/s | 0.6 kPa; dynamic head 370 Pa |
| L2 selector slits | One 1.2 x 12 mm slit per slot in the 2 mm floor plate, under the matching header | 14.4 mm2 | 1.6 m/s jet | 2.5 kPa (metering) |
| L3 slots | 27 slots 3.0 wide x 10 deep x 108 long, centre-fed through the slit, open-bottom onto the fin tips | 30 mm2 | 0.38 m/s at entry | 0.07 kPa; dynamic head 74 Pa |
| Fin channels | 0.15 x 2.0 mm, 4 mm flow length, ~11,600 in parallel | 0.3 mm2 | 0.083 m/s | 0.24 kPa (friction + turns) |
| Bleed | 0.6 x 1 mm notch in each web at both slot ends (inlet -> outlet dead-end bleed, ~4 % of slot flow) | - | 1.4 m/s | +0.3 K thermal cost |
| **Plate port-to-port** | | | | **6.3 kPa** (9.6 kPa with 13 mm / 1/2 in ports) |

**Uniformity.** Branch resistance (slit + channel + turns) = 2.9 kPa, inertial. Slot-to-slot: 2.9 / 0.37 = 7.8x the header dynamic head (U-type rule >= 6) -> global max/min ~1.07 at 18 LPM, unchanged at 36 LPM because both terms scale as Q^2. Along-slot: the slot entry dynamic head is 74 Pa against a 0.27 kPa laminar branch (ratio 3.5-5, rule 15 for centre-fed slots) -> +/-10-12 % along the 54 mm half slot, i.e. the 1.3 K long-wave term carried in the model. This is the one hydraulic assumption that must be measured (Experiment 2); the Rev B remedy is a laser-perforated orifice strip (0.6 mm holes at 1.5 mm pitch) along each slot top, which needs a third laminate and ~US$6, and would cut the term to ~0.3 K.

**dP at 2x flow (36 LPM):** 24.6 kPa (ports 10.3, slits + screen 11.6, header 2.2, channel 0.5); port velocity 3.0 m/s (local cap 3 m/s), everything else < 1.8 m/s; pumping power 14.8 W. The CoolIT-like reconstruction is 69 kPa / 42 W at the same flow. **Loop:** a UQD08 pair adds ~25 kPa (+/-50 %) and dominates; specify UQD08/UQDB08 or 5/8 in barbs for 15 kW-class trays and publish three dP boundaries (port-to-port, with stubs, with QD pair) per OCP v1.0.0.

**Filtration and fouling strategy.** Smallest wetted passage 0.15 mm = 3x the 50 um absolute screen rating (no bridging); every upstream passage > 2x the next (16 / 14 / 1.2 / 3.0 / 0.15 mm); slot dead-ends bled; port-adjacent channels outside the die on package SKUs; no self-cleaning at 0.08 m/s, so the screen is non-negotiable; dP tap ports on the header bar for monitoring; reverse-flow tolerant (symmetric comb); all-copper wetted path, Ag-Cu eutectic fillets only at structural lines, no Al, factory flush to < 0.1 mg residue. Relative life behind 50 um absolute: 0.6-1.2x a 0.2 mm skived plate; behind 25 um loop filtration no deposition mechanism exists.

---

## 4. Mechanical and construction

**Stack-up (bottom to top), 15 kW-class 125 x 125 mm plate**

| Part | Material / process | Thickness | Mass (finished) |
|---|---|---|---|
| Base plate | OFE Cu, skived field, outline-milled, tips fly-cut | 1.0 mm base (2.8 mm blank), 2.0 mm fins, 1.8 mm land | 0.39 kg |
| Comb | OFE Cu plate, 27 gang-slit through-slots, 1.2 mm underside relief over the field, 8 ear lobes, bleed notches | 10 mm | 0.62 kg |
| Floor plate | OFE Cu, stamped (laser-cut at 10k/yr), 27 selector slits | 2 mm | 0.28 kg |
| Header bar | OFE Cu block, CNC (forged near-net at 1M/yr), two headers milled from below, port bosses | 64 x 125 x 18 mm | 0.47 kg |
| Stubs, screen cartridge, springs, backplate | 316L / stamped steel | - | ~0.1 kg |
| **Total** | | **15 mm body, 33 mm at the bar** (plus stubs) | **~1.8 kg** (GPU-class 110 x 120 mm: ~1.5 kg) |

**Joining.** One vacuum-braze cycle joins all three interfaces: fin tips to comb webs (the structural ties), comb web tops and frame to the floor plate (seals adjacent slots from each other), floor plate to header bar (perimeter and the 3 mm land between headers). Filler: 5-8 um electroplated Ag on the comb (both faces) and header-bar underside, forming the Ag-Cu eutectic at ~790 C in a fixture-loaded stack (0.1-0.2 MPa), which confines the liquid to the contact lines and limits wicking into 0.15 mm gaps; BAg-8 25 um preforms are the fallback. Copper exits the furnace annealed: all stresses are checked against 70 MPa yield / 220 MPa UTS. An optional green-laser perimeter seam weld (< 1 min, ~US$3) makes the outer boundary a filler-free weld for customers who want OMNI-style messaging on the pressure boundary; the Ag-Cu fillets in the wetted path remain and must be declared.

**Base thickness logic.** Between fins a 1 mm base sees 0.0075 MPa at 2 MPa burst; the base is safe only because every fin is a tie: fin tensile 5 MPa, bond-line nominal 20 MPa over the 25 % of each fin tip that sits under a web, 12.5 MPa local in the fin tip with Kt 2.5 (SF 5.6 vs yield at burst; braze shear SF 5-10). Floor plate between webs: 2.3 MPa. Header-bar top wall, 4 mm over 30 mm: 56 MPa at 2 MPa burst (yield-safe). Perimeter seam shear ~2 MPa. Pressure bow is zero (self-equilibrated); mount bow 4-25 um and thermal bow 6 um over a 50 mm die at 300 N; in-plane thermal constraint 22 MPa, fatigue amplitude 11 MPa (SF ~6, to be covered by 1,000 power cycles).

**Flatness and finish.** After brazing the die-side face is fly-cut (removing ~1.0 mm to reach the 1.0 mm base) to <= 15-20 um over the die, Ra <= 0.8 um; this also absorbs any braze-induced distortion. Tier 2 adds 3-5 um electrolytic Ni on the contact face only (masked).

**Mounting.** Eight spring-loaded captive screws on the comb ears to a backplate, torque-limited, bearing points brought inside the ear toward the die edge (corner-only bolting on 108 mm consumes the whole 25 um budget even with the sandwich). Vacuum-stable body (no polymer walls) for negative-pressure loops.

**Pressure ratings.** MAWP 0.69 MPa (100 psi, OCP TCS envelope), proof 1.03 MPa (150 psi) 30 min, burst design >= 2.0 MPa (20 bar OCP example), sample burst test to >= 4.5 MPa; the design burst margin is set by the fin-tip braze, not by any wall.

---

## 5. Manufacturing route at volume

**Process chain (per plate, 100k/yr line)**

| # | Step | Process class / supplier type | Key tolerance | Time per plate |
|---|---|---|---|---|
| 1 | Base blank: OFE strip 2.8 mm, sheared/punched 125 x 125 | copper mill, stamping house | +/-0.05 mm | - |
| 2 | Skive fin field 108 x 108: 0.25 mm pitch, 0.10 mm fin, 2.0 mm tall, 2.0 mm base; programmed pitch for zoned SKUs | skiving house (Nakamura/Wieland/Alpha/Winshare class) or in-house skiving machine | pitch +/-0.01 mm, fin t +/-0.015 mm, height +/-0.1 mm | 3-4 min |
| 3 | Fin-tip trim and outline: fly-cut tips to a plane (+/-20 um), mill field outline and fin ends, deburr, clean | CNC / fly-cutter | tip plane +/-20 um | 1.5 min |
| 4 | Comb: 10 mm OFE plate; gang-slit 27 x 3.0 mm slots (27 saws on one arbor, 108 mm travel); face-mill 1.2 mm relief; laser/notch bleed features; ear holes | horizontal mill with gang slitting arbor (any machine shop) | slot width +/-0.05, web +/-0.05, web foot plane +/-20 um | 2-3 min |
| 5 | Floor plate: 2 mm OFE, progressive-die stamp with 27 slits (laser-cut below ~20k/yr) | stamping house (die US$60-90k) | slit +/-0.03 mm, position +/-0.05 | 0.1 min |
| 6 | Header bar: CNC from 18 mm OFE bar (forged near-net + finish CNC at 1M/yr), ports bored 16 mm, tap ports | CNC shop / forging house | header +/-0.1, flatness 20 um | 3 min (CNC) |
| 7 | Ag electroplate 5-8 um on comb (both faces) and bar underside; alkaline clean + deoxidise all parts | plating line | 5-8 um | batch |
| 8 | Stack in graphite/steel fixtures with 0.1-0.2 MPa load; vacuum braze 790 C, one cycle, 100-300 plates per load | vacuum furnace (brazing house or in-house) | - | 6-8 h cycle, batch |
| 9 | Optional green-laser perimeter seam; braze-in 316L stubs or laser-weld stubs | laser cell (Trumpf/IPG class) | - | < 1 min |
| 10 | Fly-cut die-side face to 1.0 mm base, flatness <= 20 um; Tier 2: mask + electrolytic Ni 3-5 um | CNC / plating | 15-20 um | 1.5 min |
| 11 | Flush (ISO 16232 count), fit screen cartridge, He leak (100 %, <= 1e-5 mbar-L/s, target 1e-6), dP at 3 flows (100 %, catches slit/seal bypass), proof 1.03 MPa (100 %), sample thermal (1/lot), burst and C-SAM (1/lot) | test cell | - | 4 min |

**Unit cost estimate (factory cost, GPU-class 110 x 120 mm plate, US$; 15 kW-class 125 mm plate ~ +15 %)**

| Element | CrossComb 10k/yr | 100k/yr | 1M/yr | Skived split-flow (ref.) 10k / 100k / 1M |
|---|---:|---:|---:|---|
| OFE copper (2.8 kg blank, 1.5 kg finished, 60 % swarf credit) | 30 | 26 | 22 | 18 / 16 / 14 |
| Skived core (0.25 mm pitch, 3-4 min) + tip trim/outline | 40 | 25 | 16 | 35 / 22 / 15 |
| Comb (gang-slit, relief, notches, ears) | 28 | 13 | 8 | - |
| Floor plate (laser / stamped) | 8 | 3 | 2 | - |
| Header bar (CNC / forged) | 30 | 14 | 7 | cover 40 / 18 / 8 |
| Stubs + 50 um screen cartridge | 18 | 12 | 8 | 15 / 10 / 7 |
| Ag plating or BAg-8 preforms | 9 | 6 | 4 | - |
| Vacuum braze cycle (one) | 14 | 8 | 5 | join 12 / 7 / 4 |
| Laser perimeter seam (optional) | 4 | 3 | 2 | - |
| Post-braze fly-cut, flatness | 8 | 5 | 3 | lap 3 / 2 / 1 |
| Ni plating (Tier 2 only, excluded) | (6) | (4) | (3) | 10 / 6 / 4 |
| Hardware (springs, backplate, ears) | 20 | 14 | 10 | 20 / 14 / 10 |
| 100 % leak + dP + proof, sampling | 10 | 6 | 4 | 8 / 5 / 3 |
| Yield loss (93 -> 97 %), scrap, overhead | 16 | 11 | 7 | 12 / 8 / 5 |
| **Factory cost** | **235** | **145** | **98** | **~170 / ~105 / ~70** |

Basis: process-class rates from the manufacturing-cost sweep (KB-M, to be confirmed by RFQ), copper at US$10-12/kg, braze and CNC rates from the same table. The premium over a skived split-flow plate is ~US$40 at 100k/yr (+38 %), mostly the comb, the extra copper and the second furnace-dependent joint; it is well inside the US$300-400 ASP window (gross margin ~50 % at US$290). Per kW of demonstrated capacity it is cheaper: US$165 / 21 kW = US$8/kW vs ~US$120 / 13 kW = US$9/kW for a 125 mm skived plate.

**Cost drivers, ranked:** copper mass (18 %), skiving machine time (17 %), comb machining (9 %), braze + plating (10 %), hardware (10 %), test (4 %). Copper mass is set by the 10 mm comb and the 18 mm bar; dropping the slot depth to 8 mm saves 0.12 kg but lowers the along-slot ratio to 2.2 (not recommended).

**Lead time and capacity.** Prototypes with all-CNC parts: parts in 4-5 weeks, braze trials in parallel, first full plates week 8-10, TTV data by month 4. Volume tooling: stamping die 10-12 weeks, braze fixtures 4 weeks, forged bar 12-16 weeks (1M/yr only). Capacity: skiving is the bottleneck at 100-300 plates/day/machine -> 2-3 machines per 100k/yr (capex US$2-4 M, identical to the incumbent route) plus a gang-slit mill, a furnace share and a laser cell (US$0.5-1 M). Second-sourcing through any Taiwanese/Vietnamese skiving + brazing house is possible because no proprietary process is involved.

**Yield risks (and the controls).** (1) Fin-tip braze voids: C-SAM sampling, burst test, fixture load and Ag thickness control. (2) Filler wicking into 0.15 mm gaps: plated-Ag quantity limits the liquid; stop-off on the frame; 100 % dP test detects blocked regions (>5 % channel loss shifts dP). (3) Slit-floor-to-web-top seal: a cross-leak between an inlet and outlet slot bypasses fins; 100 % dP-vs-flow slope test plus 1/lot thermal test. (4) Post-braze distortion: absorbed by the fly-cut (1.0 mm allowance). (5) Annealed copper: designed for 70 MPa throughout.

---

## 6. Predicted performance vs benchmark

**6.1 At 15 kW / 18 LPM PG25 / 45 C / 117 cm2 (model, +/-25 % per term)**

| Design | caloric | TIM | base | conv | **avg dT K** | max dT K | T_case,max C | R'' cm2K/W | dP kPa | pump W | Q cap kW (T_case <= 85 C) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow, paste (calibrated) | 6.3 | 9.0 | 6.6 | 12.6 | **34.5** | 44.3 | 89.3 | 0.269 | 24.6 (17-42) | 7.4 | 12.7 |
| CrossComb, same paste 0.07 (like-for-like) | 7.6 | 9.0 | 3.3 | 10.1 | **30.0** | 35.5 | 80.5 | 0.234 | 6.3 | 1.9 | 18.0 |
| **CrossComb Tier 1, PCM pad (nominal)** | 7.6 | 7.1 | 3.3 | 10.1 | **28.0** | **31.6** | 76.6 | 0.219 | **6.3** | 1.9 | **21.2** |
| CrossComb Tier 1, conservative (+/-20 % flow) | 7.6 | 7.1 | 3.3 | 10.1 | 28.0 (P90 ~32) | 32.6 (P90 ~36) | 77.6 | 0.219 | 6.3 (<= 10) | 1.9 | 20.5 |
| CrossComb Tier 2, liquid metal on Ni | 7.6 | 1.9 | 3.3 | 10.1 | **22.9** | 25.5 | 70.5 | 0.179 | 6.3 | 1.9 | 29.2 |
| CrossComb-P (0.10 mm core, <= 25 um loops), PCM | 8.2 | 7.1 | 3.3 | 6.8 | 25.4 | 28.9 | 73.9 | 0.198 | 6.4 | 1.9 | 24.7 |
| CrossComb-P, liquid metal | 8.2 | 1.9 | 3.3 | 6.8 | 20.2 | 22.8 | 67.8 | 0.158 | 6.4 | 1.9 | 36.4 |
| CrossComb Tier 1 with 1/2 in (13 mm) ports | | | | | 28.0 | 31.6 | 76.6 | 0.219 | 9.6 | 2.9 | 21.2 |
| CrossComb Tier 1, water instead of PG25 | 7.4 | 7.1 | 3.3 | 8.8 | 26.6 | 30.1 | 75.1 | 0.207 | 6.0 | 1.8 | 22.8 |

Max dT uses hot-spot = flow maldistribution (1.3 K nominal / 2.3 conservative / 0.6 stretch) + 0.7 K base ripple + TIM scatter (3.5 paste / 1.5 PCM / 0.6 LM). The CoolIT-like row is the calibration (reproduces 34.4 / 44.2), not a prediction.

**6.2 Flow and pumping-power trades.** CrossComb Tier 1 reaches the benchmark's 34.4 K average at **0.72 LPM/kW (10.9 LPM, 2.3 kPa, 0.4 W)**; with CoolIT's paste at 0.82 LPM/kW. At equal pumping power (7.4 W) it runs 28.5 LPM and gives 24.8 / 28.3 K. At 36 LPM: 23.6 / 27.2 K at 24.6 kPa (CoolIT-like 31.0 / 40.8 K at 69 kPa). Flow is a weak lever: 0.6 -> 2.4 LPM/kW moves Tier 1 from 38.0 to 23.6 K average.

**6.3 Real 2027-28 package (4 reticle dies + 16 HBM), hottest die cell, zoned, 1 mm base, LM on HBM pedestal.** Fit from the non-uniform-heatmap check: dT = 33 + 3500/h_eff + 350 (R_TIM - 0.05).

| Core / TIM | Stress case 350 W/cm2 die-average (2029+) | Rubin-Ultra-class 120 W/cm2 die-average | 200 W/cm2 |
|---|---:|---:|---:|
| CoolIT-like split-flow, paste / LM | 134 C / ~121 C | ~85 C (est.) | ~105 C (est.) |
| CrossComb robust core, PCM | 107 C | 71 C | 84 C |
| CrossComb robust core, LM | **93 C** | 66 C | 76 C |
| CrossComb-P core (<= 25 um loops), LM | **84.5 C** | 63 C | 70.5 C |
| CrossComb-P, direct-to-die LM (Tier 3) | ~80 C | | |

Honest reading: at a uniform 350 W/cm2 over four reticle dies the robust core does not hold T_case <= 85 C (93 C with LM) and the sawtooth/zoning granularity of an 8 mm comb costs ~1 K more than an etched manifold would; it still beats the split-flow plate by 28-41 K at the hot die. The performance core or direct-to-die reaches the line. For the realistic Rubin-Ultra package (die-average 90-130 W/cm2 with 300-350 W/cm2 patches of 3-5 cm2) the robust core with PCM holds ~71-84 C.

**6.4 GPU-class plates (2-4 kW), uniform TTVs at 1.2 LPM/kW, and die-zone estimate**

| Case | CoolIT-like paste avg / max / dP | CrossComb PCM avg / max / dP | CrossComb LM avg / max |
|---|---|---|---|
| 1.4 kW, 45 cm2 (31 W/cm2), 1.7 LPM | 13.2 / 20.4 K / 1.5 kPa | 15.2 / 17.6 K / 0.1 kPa | 14.0 / 16.2 K |
| 2.3 kW, 60 cm2, 2.8 LPM | 14.8 / 22.2 / 2.5 | 16.0 / 18.4 / 0.2 | 14.4 / 16.6 |
| 3.6 kW, 80 cm2, 4.3 LPM | 16.3 / 23.8 / 4.1 | 16.7 / 19.2 / 0.4 | 14.9 / 17.1 |
| same three at 2.0 LPM/kW (CrossComb only; pump < 0.1 W) | - | 10.5 / 12.8; 11.4 / 13.8; 12.3 / 14.8 | - |
| Rubin-class 2-die zone (16.6 cm2 at 117 W/cm2, 2.3 LPM total, 85 % to dies) | 32-49 / 42-59 K (range: all flow over dies .. area-share) | 28.3 / 31.7 K | 23.6 / 26.1 K |

On a uniform low-flux TTV at 1.2 LPM/kW the isothermal cell saturates the fluid (NTU 4-5, caloric 0.8 x dT_out) and the average is 1-2 K worse than the linear-ramp split-flow plate; the maximum is 3-5 K better and dP is 10-20x lower, and at 2.0 LPM/kW (still < 0.5 kPa) the average wins by 3-4 K. On a real die-concentrated package the zoned plate wins at the die by 4-20 K. This is the one regime where "beats in every aspect" needs the qualifier "at equal pumping power".

---

## 7. Product family and applications

| SKU | Footprint / load | What changes | Interface |
|---|---|---|---|
| CC-15 (flagship / TTV) | 125 x 125 mm, 10-25 kW, 117-150 cm2 heated | Baseline described above | PCM (T1), LM (T2) |
| CC-G (Rubin, MI455X) | 110 x 120 mm plate, 100 mm package, 1.8-2.3 kW, 2-2.8 LPM | Fin field cropped to 2 dies + 8 HBM; 8 mm pitch over dies, 12 mm over HBM; HBM slits 0.3-0.5x; stepped pedestal | PCM on gold/Ni lid, or LM |
| CC-GU (Rubin Ultra) | 130 x 160 mm plate, 120 x 150 mm package, ~3.6 kW | 4-die block zoned, 16 HBM columns; two header pairs if slot length > 110 mm | LM (T2), bare-die stepped (T3) |
| CC-C (Grace/Turin/Xeon CPU) | 60-70 mm plates, 0.5-1 kW | 8-slot comb, 2 mm fins, 13 mm ports; uniform pitch | PCM |
| CC-S (NVSwitch/NIC/CPO) | 50-80 mm, 0.5-2 kW, +/-3 K uniformity for optics | Same core; optics zones get fresh-inlet slots; no screen (rack-level) | PCM / pad |
| CC-W (wafer-scale, multi-chip, SoW) | 200 x 300 mm and up | Flow length stays 4 mm regardless of size: tile the comb and add header pairs per 110 mm; split-flow cannot scale this way | compliant per-die pads |
| CC-P (800 VDC power shelves, SST, DC-DC in the PG25 loop) | 5-30 W/cm2, Tj 150-175 C, 20-50 kPa budget | De-rated core 0.20/0.30 x 3 mm, 16 mm pitch, flat face for Easy/WolfPACK baseplates and top-side-cooled discretes, +/-3 K die-to-die, same comb/bar | PCM / gap pad |
| CC-A (EV traction, chargers, rail; WEG/Al loops) | 65-75 C inlet, -40 C start, 2.5/5 bar class | Same architecture in aluminium: skived Al fins 0.5/0.8 mm, stamped AlSi-clad floor, CAB/vacuum-brazed (EV plate-fin HX chain, >1M/yr); O-ring jacket variant for pin-fin modules | module baseplate |
| Laser-diode / DE niche | 500-1,000 W/cm2 bars, DI water | CrossComb-P core, Au/Ni plated, electrically isolated stubs | direct |

The data-centre power-electronics SKU is the same part family in the same loop and chemistry (copper, PG25, UQD, OCP test spec) and is the natural "100 % heat capture" companion to the GPU plate; automotive is a separate aluminium family sharing only the architecture and the brazing know-how.

---

## 8. Reliability, qualification and drop-in compatibility

| Requirement | CrossComb position |
|---|---|
| Coolant / inlet | OCP PG25; spec at 45 C, characterised 17-50 C; W+ (50 C) data published (T_case,max 81.6 C at 15 kW with PCM) |
| Flow / dP | Full spec at 0.75-1.0 LPM/kW (33.8 / 29.9 K avg at 15 kW); plate dP 6.3 kPa at 1.2 LPM/kW, 24.6 at 2.4; tray <= 100 kPa with UQD08; negative-pressure compatible (plate + stubs < 15 kPa) |
| Pressure | MAWP 0.69 MPa, proof 1.03 MPa, burst >= 2.0 MPa design, >= 4.5 MPa sample; pressure cycling 10,000 x 0-MAWP |
| Leak | He <= 1e-5 mbar-L/s (target 1e-6), 100 %; no polymer in the pressure boundary |
| Thermal cycling | 10-65 C operating 1,000 cycles; -40/+70 C storage 50 cycles; R drift <= 5 %, dP <= 10 % |
| Power cycling | >= 1,000 cycles 50-100 % load (thin-base fatigue, PCM re-flow); re-measure R and BLT |
| Wetted materials | OFE Cu, Ag-Cu eutectic fillets (declared), 316L stubs and screen, peroxide EPDM; no Al, Zn, NBR, silicone, no P-bearing filler; optional 2-3 um EN on the open core before braze if a customer list demands Ni |
| Corrosion / soak | 1,000-3,000 h PG25 at 65 C, 1.5x flow, coupons; Cu < 1 ppm; dP drift <= 10 % |
| Fouling | Accelerated ISO 4406-dosed test (100x particle load) behind the 50 um absolute screen, 1,000 h, with local hot-spot mapping; screen dP alarm at 3x clean; service by cartridge |
| Leak-before-break | Ductile annealed copper, no brittle filler, burst >= 3x MAWP; perimeter laser seam as redundant boundary; tray drip/rope sensors per OCP ACS; no in-plate sensing |
| Interfaces | 16 mm (5/8 in) or 13 mm (1/2 in) stubs; UQD08/UQDB08 tray couplings; EIA-310, ORv3, MGX gen-3 tray envelopes (33 mm bar height to be checked against the MGX puck envelope: the one open drop-in question) |
| Mechanical | Flatness <= 20 um over the die, Ra <= 0.8 um; PCM at 20-30 psi; retention within the package vendor window; stepped pedestal +/-0.05 mm |
| Reporting | OCP Cold Plate Test Spec v1.0.0 format: R vs flow at >= 6 points with the recommended TIM, dP at 45 +/- 2 C at 6 points and three boundaries, heater area stated (K/W and cm2K/W), 3 plates x 3 assemblies, k = 2 uncertainty, plate-to-plate CpK; independent repeat (ORNL/university) of the headline point |
| Service life | 10-year design life; relative fouling life 0.6-1.2x a 0.2 mm skived plate behind 50 um absolute, > 1.2x behind 25 um; no self-cleaning, so cleanliness is a loop-side spec we write into the SOW |
| Manufacturing QA | PFMEA, control plan, MSA, CpK >= 1.33 on leak and dP, serialised traceability, RoHS/REACH |

---

## 9. IP posture

**Built on expired foundations:** Tuckerman-Pease parallel microchannels (1984, expired), Harpole/TRW manifold microchannel cold plate (US 5,088,005, expired ~2010), Walpole/MIT alternating-flow channels (expired), Cooligy multi-level manifold and hot-spot-targeted fluid delivery (US 7,156,159 / 7,104,312, expired 2023-25, verify), brazed plate-fin construction (public domain), TWI friction stir welding (expired). The concept-level stack (skived fins + multi-slot manifold + alternating inlet/outlet slots + zoned feeds + brazed ties + welded lid) reads on nothing live at the concept level.

**What we avoid:** a single central inlet slot over one fin field with bidirectional exit (CoolIT Split-Flow US 8,746,330 / 9,603,284 / 12,495,513, expiry ~Aug 2028 + PTA; the priority chain of 12,495,513 and CA/CN/TW/EP counterparts must be verified before freeze); discrete microjet arrays with per-jet returns and jet-on-die lids (JetCool/Flex, Frore, Microsoft, Nvidia); two-phase dielectric evaporators; in-plate sensors, valves or leak sensing (Nvidia intelligent-plate families, CoolIT 9,052,252); CoolIT's compliant-member family (11,725,886 / 12,188,733) on the bare-die SKU. The orifice-strip Rev B must be checked against the PKU jet-enhanced manifold and JetCool language before adoption (holes feeding fin roots, not free jets on a wall, is the distinction to preserve).

**What we claim (US provisionals before any disclosure):** (1) the crossed-comb construction: skived fine-fin core, gang-slit comb with webs brazed to fin tips at 90 degrees, stamped selector floor with per-slot metering slits, header bar; (2) slot-pitch and slit-width programming of zone flow tied to a package power map, including the branch-ratio rule (branch >= 6x header dynamic head) and the dead-end bleed notch; (3) the pocket-relief/tip-trim method that sets the fin-tip and land planes for a single-cycle braze; (4) the stepped bare-die pedestal variant and the power-module jacket variant; (5) Ag-plated eutectic bonding of fin tips (process claim, narrow). Defensive publication for slot pitches, slit sizes and the aluminium variant. Verification list before freeze: CoolIT family claims and counterparts, Cooligy expiry/assignee (Vertiv?), Purdue HMMC and IBM Zurich ultrathin-sink families, Corintis heat-map topologies, Nvidia 2021-26 zoned-plate grants, Taiwanese utility models at detailed design. Budget US$40-100k for an FTO opinion on ~10 families.

---

## 10. Risks, experiments and roadmap

**Risks and mitigations (ranked)**

| # | Risk | Consequence | Mitigation |
|---|---|---|---|
| 1 | Fin-tip braze: voids, or filler wicking into 0.15 mm gaps | Loss of ties (burst), blocked channels (+7-17 K local) | Plated-Ag eutectic with controlled quantity; fixture load; C-SAM + burst + flow-dP sampling; BAg-8 preform fallback |
| 2 | Along-slot flow uniformity worse than +/-12 % (ratio 3.5-5 vs rule 15) | +1-2 K on maximum; grows with flow | Experiment 2 first; Rev B orifice strip (+US$6, -1 K) ready; deeper (12 mm) slot variant (+0.25 kg) |
| 3 | 1 mm base after post-braze fly-cut: breakthrough, flatness, thermal fatigue | Scrap, bow, cracks | 1.0 mm allowance, in-line thickness gauging, 1,000 power cycles, 0.8 mm floor |
| 4 | Fouling at 0.15 mm on dirty loops (no self-cleaning) | Life < 10 y, local hot spots | Integrated 50 um absolute screen, bleed notches, dP alarm, SOW cleanliness spec, 25 um loop recommendation |
| 5 | Benchmark reconstruction is uncertain in CoolIT's favour (fin pitch, base, dP band 17-42 kPa) | Smaller dP margin than claimed | Claim against the physics bound (any single-split 0.2 mm plate >= 15-20 kPa at 18 LPM); publish three dP boundaries |
| 6 | 33 mm bar height / 1.8 kg vs tray envelope | Not drop-in on some trays | Confirm MGX gen-3 puck envelope; low-profile variant (slot 8 mm, headers 25 x 10, 27 mm) at ratio ~5 |
| 7 | Tier 2 liquid metal: Ni barrier, migration, Al exclusion, 16 C freezing | Field failures if mis-specified | OEM co-design only; electrolytic Ni, dam, Galinstan; sealed-FRU indium alternative |
| 8 | Ag-Cu fillets in the wetted path vs "no braze" marketing | Procurement objection | Declare materials; 3,000 h soak data; laser-welded outer seam |
| 9 | Vendor cost rates are KB-M, not RFQ | +/-25 % on US$145 | Three RFQs (skiving, brazing, stamping) in month 1 |
| 10 | GPU-class uniform-TTV average parity at 1.2 LPM/kW | Loses a naive comparison | Lead with die-realistic TTV-B, max dT and equal-pump-power curves |

**The five experiments that retire the most risk**

1. **Braze-tie coupon (month 1-2):** 50 x 50 mm skived core + gang-slit comb, Ag-eutectic and BAg-8 variants; C-SAM bonded fraction, pull test, burst to >= 4.5 MPa, sectioning and flow test for wicking. Retires risks 1 and 3.
2. **Flow-distribution rig (month 1-3):** full-size comb + floor + bar with an acrylic lid, per-slot and along-slot flow by dye/thermal tracer at 9, 18, 36 LPM; measures theta_c, header and slot ratios; decides the orifice strip. Retires risk 2.
3. **TTV-A parity test (month 3-5):** three plates x three assemblies on a CoolIT-equivalent 4-heater 108 x 108 mm TTV, 15 kW, 18 LPM PG25, 45 C, PCM and named paste, OCP v1.0.0 format, dP at six points and three boundaries, 25-50 C inlet sweep. Retires the headline claim and risk 5.
4. **Accelerated fouling (month 3-8):** 0.15 mm core behind the 50 um absolute cartridge with ISO 4406-dosed PG25 at 100x load, 1,000 h, dP drift, local hot-spot map, cartridge loading. Retires risk 4 and sets the SOW.
5. **Reliability block and TTV-B (month 5-10):** 1,000 power cycles, 10,000 pressure cycles, 1,000-3,000 h soak with coupons, burst; then the die-realistic 4-die + 16-HBM TTV with zoned comb, pedestal and LM. Retires risks 3, 7 and the 2027-28 claim.

**12-18 month roadmap**

| Months | Milestone |
|---|---|
| 0-2 | RFQs (skiving, brazing, stamping, CNC); braze coupons; flow rig; provisionals filed; FTO search started |
| 2-4 | Prototype build (all-CNC floor and bar), 10 plates; TTV-A parity data; design freeze of slot/slit geometry (Rev A or Rev B) |
| 4-6 | OCP-format report with independent repeat; customer samples to two hyperscaler ASIC programmes and one Group-A/CM partner; MGX envelope check |
| 5-9 | Volume tooling (stamping die, braze fixtures, laser cell), PFMEA/control plan; fouling test running |
| 7-12 | Full qualification matrix (OCP + RVL-style); TTV-B zoned package test; Tier 2 LM qualification with an OEM |
| 9-14 | Pilot line 1-2k plates/month at a CM; CpK data; PPAP package |
| 12-18 | RVL/AVL admission, first volume PO, ramp to 10k/month; CC-P power-shelf SKU released; CC-GU bare-die variant sampled for Rubin Ultra |

---

## 11. Scorecard vs CoolIT 15 kW

Conditions: 15 kW, 18 LPM PG25, 45 C, 117 cm2. Conservative = Tier 1 at +/-20 % flow uniformity and the P90 of the physics Monte Carlo; nominal = Tier 1 median; stretch = Tier 2 liquid metal on the robust core [performance core in brackets].

| Metric | CoolIT 15 kW (benchmark) | Conservative | Nominal | Stretch |
|---|---|---|---|---|
| Average case-to-inlet dT | 34.4 K (measured) | <= 32 K (-7 %) | **28.0 K** (-19 %) | 22.9 K (-33 %) [20.2 K] |
| Maximum case-to-inlet dT | 44.2 K (measured) | <= 36 K (-19 %) | **31.6 K** (-29 %) | 25.5 K (-42 %) [22.8 K] |
| T_case,max at 15 kW | 89.2 C | <= 81 C | 76.6 C | 70.5 C [67.8 C] |
| Same-paste like-for-like average / max | 34.4 / 44.2 K | <= 34 / <= 38 K | 30.0 / 35.5 K | 26.5 K at equal pump power |
| Unit resistance R'' (average) | 0.269 cm2K/W (117 cm2 basis) | <= 0.25 | 0.219 | 0.179 [0.158] |
| Flow-driven hot spot (max - avg, systematic) | 8.8 K (9.8 total) | <= 3.0 K | 2.0 K | 1.3 K |
| Plate-to-plate spread at one position | 10.1 K | <= 4 K | <= 3 K | <= 2 K |
| Plate dP port-to-port, 18 LPM | undisclosed; est. ~25 kPa (17-42) | <= 10 kPa (13 mm ports) | **6.3 kPa** (16 mm ports) | 5 kPa (20 mm ports, no screen) |
| Plate dP at 36 LPM | est. ~70 kPa | <= 30 kPa | 24.6 kPa | 18 kPa |
| Hydraulic pumping power, 18 LPM | ~7.4 W est. | <= 3 W | 1.9 W | 1.5 W |
| Q capacity at T_case,max <= 85 C, 1.2 LPM/kW | ~12.7 kW | >= 18 kW | **21 kW** | 29 kW [36 kW] |
| Flow for CoolIT's 34.4 K average | 18 LPM (1.2 LPM/kW) | <= 12.3 LPM (paste) | 10.9 LPM (0.72 LPM/kW) | 8 LPM |
| 2027-28 four-reticle package, 350 W/cm2, T_case,max | ~134 C paste / ~121 C LM | 107 C (PCM) | 93 C (LM) | 84.5 C [P-core LM]; ~80 C direct-to-die |
| Rubin-Ultra-class die (120 W/cm2 avg), T_case,max | ~85 C (est.) | <= 76 C | 71 C (PCM) | 66 C (LM) |
| Factory cost, GPU-class plate, 100k/yr | ~US$105 (skived split-flow est.) | <= US$165 | US$145 | US$125 |
| Height / mass | ~15-20 mm / ~1.5 kg (est.) | 33 mm / 1.9 kg | 33 mm / 1.8 kg | 27 mm / 1.6 kg (low-profile) |
| Service life behind 50 um absolute screen | 1.0x (10 y reference) | >= 0.6x | 1.0x | 1.2x (25 um loops) |
| Transparency | one flow point, no dP, vendor-only | full OCP v1.0.0 report | + independent repeat | + CpK and fouling data |

Claims to avoid externally: anything resting on < 0.15 mm channels for the drop-in SKU; "< 10 % flow non-uniformity" before the flow rig has measured it; any dP figure without the port bore and coupling class; any 350 W/cm2 figure without zoning and the interface named; "no braze" (there is Ag-Cu eutectic in the wetted path). Where the design does not beat the benchmark (height, mass, filler-free construction, uniform low-flux average at 1.2 LPM/kW) the proposal says so above.
