# LoopCore: a passive HMMC cold plate inside an instrumented, self-balancing tray loop (key: system-platform)

Architecture proposal, 2026-10-14. Benchmark: CoolIT 15 kW Split-Flow plate (June 2026): 18 LPM PG25, 45 C, 34.4 K average / 44.2 K maximum case-to-inlet, paste, dP undisclosed (our reconstruction ~25 kPa, band 17-42). Our numbers come from the project scoping model run with this geometry (`design/sysplat/sysplat_run.py` and its `.out`); bands come from the Monte Carlo in `physics/SYNTHESIS-physics.md`. Treat every term as +/-25 %. Couplings use Cv 3-4 per UQD08; catalogue Cv is 3.65-3.76 ([FITOK](https://www.fitok.com/tmp/file/Liquid_Cooling_Universal_Quick_Disconnect_UQD_Series_EN.pdf)) and up to 4.75 ([CPC](https://www.cpcworldwide.com/Portals/0/Downloadable-Content/TRM/Literature/Spec-Sheets/CPC-Everis-UQDB08-UQD08-Spec-Sheet.pdf)), so our loop figures are conservative.

## 1. Concept in one page

**What it is.** LoopCore sells three things as one platform:

1. **A passive plate family** built on a hierarchical manifold micro-channel (HMMC) core: 0.15 mm gaps, 4 mm flow length, a 1.0 mm tied-sandwich base and a zoned orifice comb. LoopCore-15 covers 10-30 kW modules and LoopCore-G covers 1.4-4 kW packages. The plate has no electronics, no service plug and no polymer.
2. **A Tray Fluid Module (TFM)** at the tray bulkhead. It carries the UQDB08 couplings, a serviceable 50 um cartridge, and a keyed orifice that both balances and measures flow. It also holds 2 RTDs, 3 pressure sensors and a leak hub, all reporting to the BMC.
3. **A loop specification:** equal-dP balancing rule, filtration ladder, commissioning protocol, CDU interface class and OCP-format data pack.

**Why it beats CoolIT (15 kW, 18 LPM PG25, 45 C, 117 cm2):**

| metric | CoolIT 15 kW | LoopCore-15 Tier 1 (PCM) | Tier 2 (liquid metal) |
|---|---|---|---|
| average / maximum case-to-inlet | 34.4 / 44.2 K | **28.0 / 31.1 K** | 22.9 / 25.0 K |
| plate dP, port-to-port | undisclosed (~25 kPa est.) | **3.7 kPa** | 3.7 kPa |
| tray loop incl. couplings | ~65-80 kPa est. (1x UQD08) | **26-29 kPa** (2x UQDB08 + metering) | same |
| Q at Tcase,max <= 85 C | ~13 kW | **21.6 kW** | 29.7 kW |
| inlet allowed for Tcase,max = 85 C | 40.8 C | **53.9 C** | 60.0 C |
| per-plate flow, heat, dP and leak telemetry | none | yes | yes |

**Five decisive differentiators**

1. **A 3.7 kPa plate that hands the pressure budget back to the system.** Each tray uses 21 kPa less at 18 LPM on the same coupling. At 1.0 LPM/kW Tier 1 is 29.9 / 32.9 K, and at the 65 C return floor (0.75 LPM/kW) 33.8 / 36.8 K. Both beat the benchmark at 1.2 LPM/kW. TCS flow falls 17-37 %, so 100 MW needs 42 or 32 CDUs instead of 50. Negative-pressure loops become feasible, and 2x flow fits in 99-115 kPa.
2. **Warm-water headroom.** The 15 kW plate allows 13 K more inlet temperature (9 K at P90); GPU-class lidded plates allow 3 K more. That is worth US$2.5-26 M of dry-cooler capex per 100 MW.
3. **Passive heart, smart periphery.** Sensors live in the tray module, not the plate. The plate stays a sealed 10-year part, clear of in-plate sensing IP, and the sensors stay serviceable. Per-plate resistance, heat capture and fouling become measurable in the field.
4. **Self-balancing mixed racks.** Keyed orifices give every branch the same dP at its rated flow, so GPU, CPU, 800 VDC shelf and backside VPD plates share one manifold. Without that rule, a power-shelf plate draws 2.6x its rated flow.
5. **Deployability engineered in.** We keep the 0.15 mm channel floor and add a filtration ladder plus a commissioning protocol that keeps plates out of the flush loop. That protocol targets the field failure Ecolab cites. The plate is leak-before-break, and OCP v1.0 data is published at three dP boundaries.

**Honest framing.** With CoolIT's paste the mean gain is only 13 % (30.0 vs 34.4 K). On lidded GPU-class packages at 30-45 W/cm2 our average is 1-3 K worse with PCM. There we win on maximum, dP against real market plates, and function.

## 2. Thermal core

**Robust core (LoopCore-15/R, 108 x 108 mm field = 117 cm2 reference)**

| item | value | consequence |
|---|---|---|
| fins | skived OFE Cu, 0.10 mm thick, 0.15 mm gap, 2.0 mm tall | h_eff 127 kW/m2K (h 13.2 kW/m2K, eta 0.56) |
| flow length | 4 mm (inlet slots at 8 mm pitch) | 12,100 parallel segments; 0.083 m/s, Re 19 |
| base | 1.0 mm tied sandwich, >= 0.8 mm finished under the die | 3.3 K (CoolIT-like: 6.6 K) |
| caloric | isothermal cells, NTU 1.25 | 7.6 K (+1.3 K vs a linear ramp) |
| Tier 1 budget | caloric 7.6 + PCM 7.1 + base 3.3 + convection 10.1 | 28.0 K; hot spot 1.5 flow + 1.5 scatter |

The performance core (0.10/0.10 x 1.5 mm, h_eff 187 kW/m2K) is sold only for loops with <= 33 um absolute filtration, over the die zone. Channels below 0.10 mm are excluded because they foul.

**Flow path.** Coolant enters both ends of the centreline inlet header through captive 50 um screens. It drops into 14 centre-fed inlet slots, passes 0.5 mm comb holes into a 1.5 mm plenum and the tie grate, and runs 4 mm each way along the fins. It leaves through the outlet slots and outlet header. Every parcel meets the fins at inlet temperature, so HBM is never downstream of a die.

**Zoning (one comb artwork per package).**
- **Die block:** 85-90 % of the flow.
- **HBM columns:** 0.3-0.5x average per area. HBM gets a stepped Cu pedestal and a 0.05-0.10 mm compliant TIM, because gap pads fail above ~15-20 W/cm2.
- **Unheated margin:** 2 %, against stagnation.
- **VR skirt:** 3-5 %. This is a 3 mm Cu flange over the VRM ring with milled 1 x 3 mm channels and 6-12 W/mK gap pads. A 15 kW package loses 1.1-1.5 kW in its VRMs, so 100 % heat capture needs it.

**Interface strategy by tier (same core)**

| tier | package | interface | R'' cm2K/W | retention |
|---|---|---|---|---|
| 1 drop-in | flat lid (B300, MI355X, Rubin) | PCM pad on lapped bare Cu | 0.055 | 20-30 psi |
| 2 OEM co-design | Au/Ni lid | Ga-In liquid metal with dam on a 3-5 um Ni face | 0.015 | 10-20 psi |
| 3 chip co-design | bare die / micro-channel-lid socket | stepped pedestal, liquid metal, 0.8 mm base | lid + TIM1 removed | <= 0.3 MPa |

Grease is never specified on 100+ mm lids; its bond-line scatter most plausibly explains CoolIT's 10 K plate-to-plate spread.

## 3. Hydraulic architecture

**Manifold levels at 18 LPM (LoopCore-15)**

| level | element | velocity | rule met |
|---|---|---|---|
| L0 | 2 in + 2 out ports, 16 mm bore; one in/out pair at each header end | 0.75 m/s (1.49 at 36 LPM) | <= 1.5 m/s at 2x flow |
| L1 | inlet trough 29 x 6 mm fed from both ends; outlet trough 43 x 6 mm | 0.86 / 0.58 m/s | branch/head 6.1 >= 6 |
| L2 | 14 inlet slots 3.3 x 6.5 mm, centre-fed; 14 outlet slots 3.3 x 8.4 mm | 0.50 m/s | branch/slot head >= 15 |
| L3 | 0.5 mm comb holes (92 per uniform slot), 1.5 mm plenum, 50 % open grate | 1.2 m/s holes | inertial 2.0 kPa branch |
| L4 | fin gaps, 4 mm | 0.083 m/s | 0.23 kPa |

Dual-end ports halve the header flow, so the plate needs no perimeter loops and stays at 21 mm. They also give each end its own UQDB08 pair and make the plate reverse-flow tolerant for back-flushing. Passages step down: port 16 > trough 6 > slot 3.3 > hole 0.5 > channel 0.15 mm. Each slot dead-end bleeds 5 % of its flow through a 0.6 mm hole, so dense particles cannot settle under the die (+0.4 K).

**Plate dP budget, port-to-port, PG25 at 45 C (model)**

| flow | channel | turns | troughs | comb | ports | screens (clean) | **total** | hydraulic W |
|---|---|---|---|---|---|---|---|---|
| 18 LPM (1.2 LPM/kW) | 0.23 | 0.01 | 0.50 | 2.00 | 0.64 | 0.30 | **3.7 kPa** | 1.1 |
| 36 LPM (2.4 LPM/kW) | 0.5 | 0.05 | 2.0 | 8.0 | 2.6 | 0.85 | **13.9 kPa** | 8.4 |

We claim <= 8 kPa at 18 LPM and <= 20 kPa at 36 LPM until CFD and test confirm. Ports are 17 % of the total, so the claim survives a +/-50 % error on port K. Uniformity across slots is 1.06-1.15 max/min (momentum-coefficient uncertainty), with a target of <= 1.10. Because the branch is 90 % inertial, uniformity does not degrade with flow.

**Tray loop for one 15 kW plate (1 m hose, fittings, TFM, couplings; kPa)**

| configuration | 18 LPM | 15 LPM | 11.25 LPM | 36 LPM |
|---|---|---|---|---|
| CoolIT-like + 1x UQD08, 12 mm stubs, 1/2-in hose | 65-80 | 47-58 | 29-35 | 225-287 |
| CoolIT-like + 2x UQD08, 5/8-in | 36-40 | 27-30 | 18-19 | 115-130 |
| LoopCore + 1x UQD08, 12 mm stubs, 1/2-in hose | 44-59 | 31-41 | 18-24 | 170-231 |
| LoopCore + 2x UQDB08, no orifice | 16-19 | 11-14 | 6-8 | 59-75 |
| **LoopCore + 2x UQDB08 + 10 kPa metering orifice (standard)** | **26-29** | **18-21** | **10-12** | 99-115 |

At 18 LPM the standard loop is couplings 4.9-8.7, hose 1.9, fittings 4.2, TFM 0.8, orifice 10.0 and plate 3.7 kPa. Coupling class decides feasibility. A single UQD08 cannot carry 2x flow for any plate. Dual UQDB08 can, without a non-standard 3/4-in coupling. The low plate dP pays for the orifice and keeps the loop under half the benchmark's.

**Rack balancing.** We modelled 18 trays x 15 kW (324 LPM) on a dividing/combining manifold at 2U pitch with momentum coefficients theta_d = 1 and theta_c = 2.

| branch at 18 LPM | 50 mm header, U | 50 mm, Z | 63 mm, U | 63 mm, Z |
|---|---|---|---|---|
| CoolIT-like + 1x UQD08 (72 kPa) | 1.036 | 1.081 | 1.014 | 1.032 |
| LoopCore, 2x UQDB08, no orifice (17 kPa) | 1.152 (+0.5 K) | 1.363 (+1.4 K) | 1.057 | 1.135 |
| **LoopCore standard (27 kPa)** | 1.096 (+0.3 K) | 1.222 (+0.9 K) | **1.036 (+0.1 K)** | 1.085 |

Values are tray flow max/min, with the Tier 1 maximum-dT penalty at the worst tray in brackets. Two findings follow:

- **A low-dP plate needs a 63 mm (2.5-in) manifold or the orifice; we specify both.** Direct return (U) beats reverse return (Z) because momentum, not friction, dominates.
- **Imbalance among identical trays is not thermally critical**, because the HMMC is weakly flow-sensitive (+1.4 K at -13 %). The orifice earns its place three other ways:
  - **Mixed loads.** A 2 kW power-shelf branch (4 kPa intrinsic) on a 27 kPa header draws 3.1 LPM, 2.6x rated. Ten of them take 6 % of the GPU flow unless their orifices add 23 kPa.
  - **Flow measurement.** It gives a 10 kPa signal at rated flow; water calibration yields +/-3 % flow and +/-4 % heat accuracy.
  - **Runaway protection.** It caps flow when neighbouring trays are removed.

**Filtration ladder and fouling strategy**

| stage | element | job |
|---|---|---|
| commissioning | flush loop with plate bypass jumpers and 5-10 um bags. Plates connect only at a proposed ISO 4406 <= 16/14/11 with no particle > 50 um, to check against the unread OCP PG25 limits. | removes installation debris (the failure mode Ecolab cites) |
| CDU | 25 um full-flow filter + 5 um side-stream polisher (5-10 % of flow) | bulk cleanliness |
| TFM | 50 um absolute cartridge, >= 20 cm2, serviceable (0.5 kPa) | catches rack and coupling debris |
| plate | 2 captive 50 um absolute screens, >= 12 cm2 each, permanent (0.30 kPa) | protects the 0.15 mm channels (W/d = 3) |

Hoses from TFM to plate are corrugated 316L or PTFE-lined, not EPDM, to cut shedding. The TFM alarms at +2 kPa over the plate's factory dP signature (screen at ~3x clean, or channel fouling). Recovery is a reverse back-flush at 2x rated flow through the TFM ports. Life relative to a skived plate is 0.6-1.2x behind a 50 um nominal CDU filter and >= 1.0x behind 25 um.

## 4. Mechanical and construction

**Stack-up**

| layer | LoopCore-15 | LoopCore-G | process |
|---|---|---|---|
| base + fins | 1.0 + 2.0 mm | 1.0 + 2.0 mm | skived OFE Cu |
| tie grate | 0.5 mm | 0.5 mm | photo-etched; bonds >= 50 % of every fin tip |
| plenum | 1.5 mm | 1.0 mm | double-sided etched; bleed notches |
| comb | 0.4 mm | 0.4 mm | etched; zone artwork per SKU |
| slots (manifold block) | 6.5-8.4 mm | 4.0 mm | CNC (forged near-net at >= 100k/yr) |
| troughs | 6 mm | 3 mm | same block |
| cover | 2.5 mm | 2.0 mm | Cu plate |
| **total height** | **21 mm** (LP18 variant 18 mm) | **14 mm** | |
| body / mass | 148 x 152 mm, ~2.2 kg | 110 x 120 mm, ~0.9 kg | |

**Joining.** One vacuum braze at ~790 C, with 5-8 um plated Ag, bonds fin tips, layers and rim for 100-300 plates per cycle. A green-laser perimeter seam follows. The 316L stubs and captive screens are laser-welded after brazing, so the screens never see the furnace. Diffusion bonding is the premium route. No polymer sits in the pressure boundary.

**Base thickness logic.** Every fin tip is tied to the grate, so base pressure stress is negligible (0.015 MPa at 3 MPa). Finish machining, a 0.1 mm erosion allowance and skive tolerance set the floor: order 1.0 mm, deliver >= 0.8 mm. The tied sandwich has zero pressure bow and is 24x stiffer than a free 2 mm base. Bow over a 50 mm die is 4-25 + 6 um, against 13-77 + 19 um for a skived plate. That stiffness lets PCM or liquid metal hold its datasheet value.

**Pressure ratings.** MAWP 1.0 MPa (145 psi, above the 100 psi UQD class); 100 % proof at 1.5 MPa; burst >= 3.0 MPa by design, qualified at >= 4.5 MPa; vacuum to -0.9 bar(g). Tie stress at 3 MPa is 15 MPa (SF 4.7 on 70 MPa annealed yield). The perimeter land governs at SF 5.8; thermal-fatigue SF is ~6.

**Leak-before-break.** Ductile annealed Cu with burst >= 4.5x MAWP weeps long before rupture. Three channels detect the weep: a drip-tray rope sensor (OCP ACS), a TFM flow/dP anomaly, and CDU make-up volume.

**Flatness and mounting.** The face is lapped to <= 15 um over the die and <= 25 um over 100 mm, Ra <= 0.4 um. Spring screws bear within 10 mm of the die edge; the hot package gap must be <= 50 um.

## 5. Manufacturing route at volume

**Process chain**

1. Skive the fin field, 2-4 min per plate (Wieland, Nakamura or Taiwanese/Vietnamese skiving houses). Fly-cut the tips to a +/-20 um plane.
2. Photo-etch the grate, plenum and comb in the PCB/EMI-shield etching industry (+/-25 um on 0.5 mm holes).
3. CNC the manifold block; switch to forged near-net plus finish CNC at volume.
4. Ag-plate, clean, fixture and vacuum braze.
5. Laser-seal the perimeter and laser-weld the stubs with captive screens.
6. Lap the face; for Tier 2, mask and Ni-plate it.
7. Flush to ISO 16232. Test 100 % for He leak (target 1e-6 mbar-L/s), proof and a **3-flow dP signature**, binned to +/-5 % and stored in the paired TFM EEPROM. C-scan, burst and TTV-test one plate per lot.
8. TFM: CNC 316L body with welded UQDB08 halves, keyed orifice (+/-1 % area), wells, MEMS sensors and hub PCB. Water-calibrate, then He leak test.

**Factory cost estimate** (US$, +/-25 %). Process rates come from `manufacturing-cost.md` and `gap-cost-volume-and-market-anchors.md` (KB-M, to be RFQ-confirmed); copper at US$10-12/kg.

| element | LoopCore-15 10k / 100k | LoopCore-G 10k / 100k |
|---|---|---|
| copper + skived core | 66 / 47 | 41 / 28 |
| etched laminates + CNC block + cover | 108 / 48 | 65 / 29 |
| stubs, screens, braze, laser seam | 50 / 29 | 31 / 18 |
| finish, frame, 100 % test | 40 / 25 | 34 / 21 |
| yield, scrap, overhead (12 %) | 32 / 18 | 21 / 12 |
| **plate factory cost** | **~295 / ~165** | **~190 / ~110** |
| TFM (dual / single UQDB08 pair) | ~200 / ~120 | ~150 / ~90 |
| of which sensing + metering adder | ~100 / ~55 | ~100 / ~55 |

A GB-class skived/welded plate costs ~US$165-170 (10k) and ~US$100-105 (100k). LoopCore-G adds ~US$5-10 at 100k, inside the ~US$400 Group-A ASP. LoopCore-15 costs US$7.6 per kW of Tcase-limited capacity (165 / 21.6), against ~US$9 for a 15 kW skived plate (~115 / 12.7).

**Lead time.** Alpha plates take 10-12 weeks from design freeze; TFMs take 8-10. A 100k/yr line (2-3 skiving machines, one vacuum furnace, a laser cell, outsourced etching) costs US$3-5 M and takes 9-12 months.

**Yield risks:**
- fin-tip braze voids (C-scan, burst sampling);
- Ag wicking into the 0.15 mm gaps (plating-quantity control; caught as a > 5 % dP shift);
- slot cross-leaks (dP-vs-flow slope);
- post-braze distortion (1.0 mm finish allowance);
- TFM calibration drift (100 % water rig).

## 6. Predicted performance vs benchmark

### 6.1 15 kW / 18 LPM / 45 C / 117 cm2 (model; P10-P90 in brackets)

| design | caloric | TIM | base | conv | avg dT K | max dT K | R'' cm2K/W | plate dP kPa | pump W | Q cap kW | Tcase,max |
|---|---|---|---|---|---|---|---|---|---|---|---|
| CoolIT-like reconstruction (calibrated) | 6.3 | 9.0 | 6.6 | 12.6 | 34.5 | 44.3 | 0.269 | 24.6 | 7.4 | 12.7 | 89 C |
| LoopCore-15/R same paste | 7.6 | 9.0 | 3.3 | 10.1 | 30.0 (26-37) | 35.0 (31-42) | 0.234 | 3.7 | 1.1 | 18.4 | 80 C |
| **LoopCore-15/R PCM (Tier 1)** | 7.6 | 7.1 | 3.3 | 10.1 | **28.0 (26-31)** | **31.1 (29-35)** | 0.219 | **3.7** | 1.1 | **21.6 (18-24)** | **76 C** |
| LoopCore-15/R LM (Tier 2) | 7.6 | 1.9 | 3.3 | 10.1 | 22.9 (22-25) | 25.0 (24-27) | 0.179 | 3.7 | 1.1 | 29.7 | 70 C |
| LoopCore-15/P LM (<= 33 um loops) | 8.2 | 1.9 | 3.3 | 6.8 | 20.2 | 22.3 | 0.158 | 3.8 | 1.1 | 37.0 | 67 C |

Further variants: Tier 3 direct-to-die on the TTV gives 20.3 / 22.4 K; the LP18 low-profile plate gives 28.9 / 31.9 K at 5.0 kPa and 20.6 kW.

**Flow and pump-power operating points (Tier 1 avg / max, plate dP)**

| LPM/kW | CoolIT-like | LoopCore Tier 1 | outlet |
|---|---|---|---|
| 0.75 | 38.5 / 48.3 K, 13.0 kPa | **33.8 / 36.8 K, 1.5 kPa** | 65.3 C |
| 1.0 (design) | 35.8 / 45.6 K, 19.1 kPa | **29.9 / 32.9 K, 2.6 kPa** | 60.2 C |
| 1.2 | 34.5 / 44.3 K, 24.6 kPa | 28.0 / 31.1 K, 3.7 kPa | 57.7 C |
| 2.4 (2x) | 31.0 / 40.8 K, 69.3 kPa | 23.6 / 26.7 K, 13.9 kPa | 51.3 C |

- **Flow equivalence.** Tier 1 matches CoolIT's 34.4 K average at 0.72 LPM/kW and its 44.2 K maximum at 0.52 LPM/kW. Tier 2 does so at 0.56 / 0.43, and same paste at 0.82 on the average. In practice the floor is 0.75 LPM/kW, set by the 65 C return limit rather than by the plate.
- **Equal hydraulic power.** At CoolIT's 7.4 W, LoopCore runs 34.5 LPM (2.3 LPM/kW, 12.8 kPa) and reaches 23.8 / 26.8 K (Tier 1) or 18.7 / 20.8 K (Tier 2).
- **50 C inlet (W+).** At 1.0 LPM/kW Tier 1 gives Tcase,max 82.9 C.

### 6.2 Real 2027-28 package: 4 x 26 x 33 mm dies at 350 W/cm2 + 16 HBM, zoned, hottest die cell

| core / TIM | case-to-inlet | Tcase,max (45 C) |
|---|---|---|
| CoolIT-like split-flow, paste (flow crosses dies, then HBM) | 88.6 K | ~134 C (LM ~121 C) |
| LoopCore R, PCM | 62.3 K | 107 C |
| LoopCore R, LM | 48.3 K | **93 C (misses 85 C)** |
| LoopCore P die-zone core, LM, 25 um loop | 39.5 K | **84.5 C** |
| Tier 3 direct-to-die | removes ~28 K at the junction | ~80 C at die top |

Without zoning the same plate is 15 K worse, so zoning is mandatory; it is a change of comb artwork, not a new plate. Across-die case gradient is 6-8 K, against 22-30 K for split-flow. HBM Tj is 84-91 C with the pedestal, against 105 C on a split-flow plate.

### 6.3 GPU-class plates (LoopCore-G: single 8 mm in/out, dual at 6 LPM; 2 kPa comb at rated flow)

| case | CoolIT-like paste avg / max | LoopCore T1 PCM | LoopCore T2 LM | plate dP CoolIT-like / ours |
|---|---|---|---|---|
| B300 1.4 kW, 45 cm2, 1.0 LPM/kW | 14.5 / 21.7 K | 17.7 / 19.6 K | 16.5 / 18.1 K | 1.2 / 2.8 kPa |
| Rubin 2.3 kW, 60 cm2, 1.0 LPM/kW | 16.1 / 23.5 K | 18.4 / 20.3 K | 16.9 / 18.5 K | 2.0 / 3.2 kPa |
| Rubin Ultra 3.6 kW, 80 cm2, 1.0 LPM/kW | 17.6 / 25.1 K | 19.1 / 21.1 K | 17.3 / 19.0 K | 3.3 / 4.2 kPa |
| CoolIT 4 kW point, 25 cm2, 1.5 LPM/kW | measured < 36 K max | 31.0 / 34.4 K | 24.6 / 26.8 K | - / 4.1 kPa |
| Rubin die zone (16.6 cm2, 1.94 kW), 1.0 LPM/kW, crude | 35.7 / 45.2 K | 27.8 / 30.7 K | 23.1 / 25.2 K | - |

**Where we do not win.**

1. On a uniformly heated lid at 30-45 W/cm2 our average is 1.3-3.2 K worse with PCM. We win the maximum by 2-4 K; with liquid metal the average reaches parity.
2. GPU-class plate dP (2.8-4.2 kPa) matches the scaled reconstruction. It is ~6x lower only against published market plates (12 kPa at 1.7 LPM).
3. At 0.75 LPM/kW our GPU-class maximum is 25.3 K, against 22.2 K for CoolIT-like at 1.2. At GPU class the fewer-CDUs claim holds only down to 1.0 LPM/kW.
4. The die-zone row gives neither design any lateral-spreading credit.

**GPU tray (4 x 2.3 kW + 2 x 0.5 kW CPU, 10.2 LPM).** With per-plate UQD04-class hot-swap couplings, TFM, metering and a UQDB08 pair, the tray totals 28-45 kPa; with UQD06-class couplings, 21-28 kPa. A vendor-plate tray without these is 26-31 kPa. **In the same budget we add single-GPU hot-swap, metering and telemetry.**

### 6.4 Facility-level value (100 MW IT, liquid-captured)

The TCS network outside the tray is assumed at 140 kPa at 1.2 LPM/kW: CDU heat exchanger and filter 70, row piping 50, rack manifold 20. CDUs are CHx2000-class (2,400 LPM, flow-limited) and pump wire-to-water efficiency is 60 %.

| scenario | TCS LPM | CDUs | TCS dP | pump electric | GWh/yr | PUE delta |
|---|---|---|---|---|---|---|
| A CoolIT-like, 1x UQD08, 1.2 LPM/kW | 120,000 | 50 | 212 kPa | 708 kW | 6.20 | 0 |
| B LoopCore, 1x UQD08, 1.2 LPM/kW | 120,000 | 50 | 191 | 638 | 5.59 | -0.0007 |
| C LoopCore, 1.0 LPM/kW (better Tcase than A) | 100,000 | 42 | 133 | 369 | 3.23 | -0.0034 |
| D LoopCore, 0.75 LPM/kW (15 kW class only) | 75,000 | 32 | 75 | 156 | 1.36 | -0.0055 |
| E LoopCore standard loop, 1.0 LPM/kW | 100,000 | 42 | 116 | 323 | 2.83 | -0.0038 |

| lever | value per 100 MW (estimates) |
|---|---|
| 8 fewer CDUs (C) / 18 fewer (D) at US$250-500k | US$2-4 M / US$4.5-9 M capex (heat-exchanger duty unchanged) |
| pump energy, C vs A | -339 kW, 3.0 GWh/yr, ~US$0.24 M/yr |
| warm water, GPU class (+3.1 K) | US$2.5-6.2 M dry-cooler capex + US$0.5-1.0 M/yr (hot climate) |
| warm water, 15 kW class (+9.2 / +13.1 / +19.2 K) | US$7.4-18 / 10.5-26 / 15-38 M capex + US$1.5-6 M/yr |
| -21 kPa per tray | a 25 um point-of-use filter, or one more rack per head-limited CDU (US$9-25 per plate) |
| platform premium, GPU class | 39,000 plates x US$5-10 + 9,800 TFMs x US$55 = **US$0.7-0.9 M** |

The flow and supply-temperature levers spend the same thermal margin, so they are **not additive**; an operator chooses a mix. Pump energy is the smallest lever.

## 7. Product family, applications and commercial architecture

| SKU | target | changes vs base |
|---|---|---|
| LoopCore-G T1/T2 | Rubin / MI455X / B300 flat lids, 1.4-4 kW | 14 mm, comb artwork per power map, Ni face for liquid metal |
| LoopCore-G T3 | bare die (TPU, Maia, Trainium), micro-channel-lid socket | stepped pedestal, 0.8 mm base; P core over the die on 25 um loops |
| LoopCore-15 | multi-die modules, superchip boards, wafer-scale tiles (field scales at constant 4 mm flow length) | dual-end 16 mm ports, VR skirt, 2.5-in manifold |
| LoopCore-X | CPU, NVSwitch, NIC/CPO, 0.3-2 kW | small field; optics on the return leg |
| VPD backside plate | vertical power delivery under the package | 0.5 mm-gap core, in series on the return leg |
| LoopCore-P | 800 VDC shelves and SSTs, 1-2 kW, 5-30 W/cm2, SiC Tj 150-175 C | 0.3-0.5 mm gaps, no screen; keyed orifice so it cannot starve GPU branches |
| EV / industrial SiC | WEG 50/50, 65 C, Al loops, AQG 324 | licence only (the module vendor owns the baseplate) |

**Compatibility.**
- **NVL72 / NVL144 MGX 1U trays:** LoopCore-G fits at 14 mm; the TFM sits at the rear bulkhead with UQDB08.
- **Kyber vertical blades:** outlets mount at the high point, and the symmetric centre-fed headers self-vent in either orientation. Kyber's blade coupling is not public, so the interface must be confirmed under NDA. Kyber-class racks may shed over 100 kW from peripherals ([StorageReview](https://www.storagereview.com/?p=150594)), which is why the VR skirt and VPD plate matter.
- **ORv3:** rear blind-mate UQDB08.

**Commercial architecture.** Sell plate + TFM + data pack; **do not build CDUs**. The CDU market is crowded (CoolIT/Ecolab, Vertiv, Schneider-Motivair, Boyd/Eaton) and is CoolIT's strongest ground. Instead, publish a "LoopCore-Ready" CDU class (25 um full-flow filtration, side-stream polishing, >= 35 psi head, 1.0 LPM/kW rating, inlet to 55 C) and certify partners.

| channel | offer | why |
|---|---|---|
| NVIDIA Rubin / Rubin Ultra (Group-A) | licence core + comb tooling to a Group-A house; MGX-compatible LoopCore-G with OCP data | same skive/etch/braze supply base; CoolIT is outside Group-A |
| hyperscaler ASICs (beachhead) | co-designed plate + TFM + rack balancing + telemetry schema | they own the spec and capture the CDU and warm-water value |
| OEMs (Dell, HPE, Lenovo, Supermicro) | branded kits: plates, TFMs, tray loops, 2.5-in manifold | DLC differentiation, less captive to Group-A |
| lid partner (Jentech class) | Tier 3 core as micro-channel-lid insert | NVIDIA reportedly seeking lid partners |

What we offer each party:
- **CDU:** 17-37 % less flow and 21 kPa of head back per tray.
- **Operator:** warmer water and verifiable heat capture.
- **OEM:** 14 mm height, 0.9 kg, compact thermal models, dP at three boundaries, and independent-lab data on 3 plates x 3 assemblies.

## 8. Reliability, qualification and drop-in compatibility

**Drop-in requirements met.**
- OCP PG25 coolant; ASHRAE W45, characterised at 50-55 C; flow curves 0.6-2.4 LPM/kW.
- OCP UQD v2.0.0 UQDB08 couplings; MAWP 1.0 MPa; 100 % He leak <= 1e-5 mbar-L/s.
- Wetted path: OFE Cu, fluxless Ag braze, 316L, peroxide-cured EPDM (coupling seals only), PTFE. No Al, Zn, brass, NBR or silicone; Ni only on the dry Tier 2 contact face.
- Velocity <= 1.5 m/s in Cu at 2x flow; comb holes at 1.2 m/s, far from cavitation.
- Telemetry exposed as BMC sensors (PLDM/Redfish).

**Test plan outline**

| test | condition | pass |
|---|---|---|
| thermal (OCP v1.0) | 6 flows, 45 C, named PCM and LM, 3 x 3 builds, independent lab | Tier 1 <= 32 / <= 35 K; CpK >= 1.33 |
| dP | 3 boundaries incl. named UQDB08 pair | <= 8 kPa port-to-port at 18 LPM |
| proof / burst / vacuum | 1.5 MPa (100 %); >= 4.5 MPa (samples); -0.9 bar(g) | no leak or deformation |
| pressure / thermal / power cycling | 100,000 x 0-1.0 MPa; 1,000 x 10-65 C; 1,000 power cycles | R drift <= 5 %, dP <= 10 % |
| PG25 soak | 3,000 h, 65 C, 1.5x flow | dP drift <= 10 % |
| particulate challenge | 500 h dosed; one plate without screens | R drift < 5 %; no die-zone cluster |
| TFM | 1,000 h at 65 C; ISTA 3A; 500 mate cycles | flow +/-3 %, delta-T +/-0.1 K |

**Service life.** Plate: 10 years, sealed. TFM sensors: 7-year server life, with RTDs in dry wells that can be replaced live. Cartridge: serviced on dP alarm, expected after >= 3 years behind a 25 um CDU filter. The commissioning protocol is a warranty condition.

## 9. IP posture

| space | action |
|---|---|
| CoolIT Split-Flow ('330 / '284 / '513 + CIPs; US expiry Aug 2028 to ~mid-2031) | many interdigitated slots, separate etched manifold, rib-separated zones. "Comprising" makes ">= 2 slots" alone unsafe, so chart the claims (US$25-60k) before US sales. |
| CoolIT compliant member (11,725,886 / 12,188,733) | rigid stepped pedestal only |
| in-plate leak detection (CoolIT 9,052,252, ~2032) | drip-tray sensing per OCP ACS |
| NVIDIA "intelligent cold plate" filings | Passive plate; TFM telemetry is read-only, with a fixed orifice and no actuator or control loop. **An FTO opinion on the TFM is a gate.** |
| blind-mate couplings (HPE and others) | buy OCP UQDB parts from licensed vendors |
| microjets (JetCool/Flex, Frore) | comb jets decay in a 1.5 mm plenum, no impingement; claim review |

**Expired foundations we build on:** Tuckerman-Pease microchannels (1981); Harpole manifold micro-channel (US 5,088,005); Walpole US 5,099,910; the US 5,145,001 normal-flow laminate; Cooligy multi-level manifolds (expired 2023); IBM TCM pistons (1976); ISO 5167 orifice metering, balancing valves, EN 1434 heat meters and Tichelmann reverse return.

**Provisionals to file before disclosure:**
1. a factory dP signature paired with the tray module, used to infer screen loading, fouling and TIM drift from field telemetry;
2. keyed per-class orifices that implement the equal-dP rule in mixed-load racks;
3. dual-end-fed centreline headers with dual couplings and symmetric back-flush;
4. captive stub screens combined with the commissioning bypass protocol;
5. a VR skirt fed by comb holes;
6. the skive + etched laminate + tied-sandwich stack (shared with sibling proposals).

## 10. Risks, experiments and roadmap

| risk | mitigation |
|---|---|
| coupling Cv and CoolIT's real dP unknown (+/-50 %) | E1; quote dP only at named boundaries |
| manifold uniformity (hot spot 1.5 -> 2.5 K) | E2; inertial orifice comb |
| tip-bond fraction < 30 % | E3; C-scan acceptance |
| fouling of 0.15 mm channels (life 0.6x) | E4; filtration ladder; commissioning protocol |
| PCM/LM losing datasheet values on 100+ mm lids | E3 interface cycling |
| TFM drift; NVIDIA intelligent-plate IP | E5; FTO; fall back to an orifice-only TFM |
| market gate (Group-A, NDA envelope); Ecolab chemistry + CDU + plate bundle | licence route; hyperscaler beachhead; open CDU class |
| 21 mm height in 1U | LP18 (+0.9 K); 2U, blade or sidecar formats |
| 350 W/cm2 misses 85 C on the R core (93 C) | P die-zone core on 25 um loops (84.5 C) or Tier 3 |

**The five experiments that retire the most risk**

1. **E1, rig and incumbents (8 weeks, < US$40k).** Build an OCP-format rig and test 2-3 bought incumbent plates plus named UQD08/UQDB08 pairs at 5-40 LPM. This pins the benchmark dP and coupling Cv.
2. **E2, slot-pair water table plus CFD.** Pin theta_c and global max/min.
3. **E3, tied-sandwich coupons and TTV interface.** C-scan, burst >= 4.5 MPa, 1,000 power cycles, and D5470 on PCM and LM before and after cycling.
4. **E4, fouling challenge.** 500 h dosed on a 0.15 mm core with captive screens, plus a screen-bypass blockage run under IR.
5. **E5, instrumented mini-rack (4-6 trays).** Mixed GPU and power-shelf branches: verify +/-5 % calorimetry, equal-dP balance, fouling-alarm sensitivity, back-flush recovery and negative-pressure operation.

**Roadmap to a qualified product (12-18 months)**

| months | milestones |
|---|---|
| 0-3 | E1, E2, E3 coupons; FTO; provisionals; TTVs (117 cm2 parity, Rubin-class zoned); partner MoUs |
| 3-6 | 10 alpha plates per SKU + 10 TFMs; OCP characterisation; E4 |
| 6-9 | production-intent beta; 3 x 3 builds; independent lab; E5; reliability starts |
| 9-12 | design freeze; public OCP report; hyperscaler samples; CM trial line |
| 12-18 | qualification complete; RVL/AVL submission; pilot 1-5k/month for 2H 2027-2028 ramps |

## 11. Scorecard vs CoolIT 15 kW

Conservative is Monte Carlo P90 or the Cv-low case; nominal is the model median; stretch is Tier 2 (performance core in brackets). Conditions are 15 kW, 18 LPM PG25, 45 C, 117 cm2 unless stated.

| metric | CoolIT 15 kW | conservative | nominal | stretch |
|---|---|---|---|---|
| average dT | 34.4 K | <= 32 K | 28.0 K | 22.9 K [20.2] |
| maximum dT | 44.2 K | <= 35 K | 31.1 K | 25.0 K [22.3] |
| same-paste average | 34.4 K | <= 34 K | 30.0 K | 25.8 K at equal pump power |
| Tcase,max | 89.2 C | <= 80 C | 76 C | 70 C [67 C] |
| max - avg | 9.8 K | <= 4 K | 3.1 K | 2.1 K |
| plate dP, port-to-port | undisclosed (~25 est.) | <= 8 kPa | 3.7 kPa | 3.7 kPa |
| tray loop incl. couplings | ~65-80 kPa est. | <= 40 kPa | 26-29 kPa | 16-19 kPa (no orifice) |
| Q at Tcase,max <= 85 C | ~13 kW | >= 18 kW | 21.6 kW | 29.7 kW [37.0] |
| inlet for Tcase,max 85 C | 40.8 C | >= 50 C | 53.9 C | 60.0 C |
| flow at <= benchmark Tcase | 1.2 LPM/kW | 1.0 | 0.75 (return-limited) | 0.75 with Tier 2 at 28.7 / 30.8 K |
| CDUs per 100 MW (flow-limited) | 50 | 42 | 42 (GPU) / 32 (15 kW) | 32 |
| TCS pump power per 100 MW | ~708 kW | 638 kW | 369 kW | 156 kW |
| real package, 350 W/cm2, Tcase,max | ~134 C | 107 C (PCM) | 93 C (LM) | 84.5 C (P core) |
| GPU-class Rubin lid at 1.0 LPM/kW, avg / max | 16.1 / 23.5 K | ~20.4 / ~22.3 K (+2 K est.) | 18.4 / 20.3 K (avg loses) | 16.9 / 18.5 K |
| plate-to-plate spread | 10.1 K | <= 3 K | 2 K | 1 K |
| per-plate telemetry | none | flow, delta-T, dP | calorimetry +/-4-5 % | plus R-drift and fouling prognostics |
| heat capture | 93-97 % (4 kW plate, uninsulated) | >= 95 % | >= 98 % measured per tray | ~100 % with VR skirt + VPD plate |
| tray loop at 1.0 LPM/kW (negative-pressure budget 30-50 kPa) | 47-58 kPa (marginal to out) | 31-41 kPa (1x UQD08) | 18-21 kPa | 11-14 kPa |
| burst / leak | undisclosed | >= 3.0 MPa, 1e-5 | >= 4.5 MPa, 1e-6 | same, zero pressure bow |
| fouling life vs skived | 1.0x | >= 0.6x | 1.0x | 1.2x behind 25 um |
| height / mass (15 kW; GPU class 14 mm / 0.9 kg) | ~10-13 mm + bar (est.) | 21 mm / 2.2 kg (worse) | 21 mm | 18 mm LP (+0.9 K) |
| plate factory cost at 100k (15 kW / GPU class) | ~US$100-115 | US$205 / US$135 (+25 %) | US$165 / US$110, + US$55 TFM adder per tray | US$145 / US$100 (forged block) |
| US$ per kW of Tcase-limited capacity | ~US$9 | US$9.2 | US$7.6 | US$5.6 (Tier 2) |
| transparency | 1 flow point, no dP | full OCP v1.0 report | + 3 dP boundaries, 3 x 3 builds | + independent lab and field telemetry |

**Where we lose or only tie:** 15 kW-class height and mass; GPU-class average dT on uniformly heated lids with PCM; GPU-class plate dP against the reconstruction (we win only against published market plates); fouling life (parity at best); bare-plate cost (+US$5-60).
