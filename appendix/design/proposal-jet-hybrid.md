# JetFin Hybrid (JH): a nozzle-metered slot-jet-into-micro-fin cold plate (key: jet-hybrid)

Architecture proposal, 2026-10-13. Benchmark: CoolIT 15 kW Split-Flow coldplate (June 2026): 15 kW, 18 LPM PG25, 45 C inlet, 34.4 K average / 44.2 K maximum case-to-inlet, paste TIM, pressure drop undisclosed (our reconstruction ~22-25 kPa, band 17-42 kPa). All performance numbers come from `design/jet/jet_hybrid_model.py` (full output in `design/jet/jet_hybrid_model.out`). That script imports the programme's `coldplate_model.py` unchanged for the CoolIT and HMMC reference rows and uses the same series network (isothermal-cell caloric term, TIM, base, convection, hot spot = flow term + TIM scatter) on the calibrated 117 cm2 footprint. Scoping accuracy is +/-25-30 % per term. It is not CFD.

## 1. Concept in one page

**What it is.** JH is a copper plate with a three-level manifold, diffusion-bonded in one furnace cycle. The last manifold level is a two-layer **nozzle-tie laminate** bonded directly onto the tips of a skived fin field (0.15 mm gaps, 0.10 mm fins, 2.0 mm tall, 1.0 mm base). The laminate carries 0.22 mm slot nozzles at 8 mm pitch, interleaved with 1.0 mm return slots. Each slot nozzle crosses all 432 fin gaps. In each gap it issues a planar jet at 1.55 m/s (18 LPM) that hits the base between the fins, turns, runs 3.4 mm along the channel and rises into the next return slot. The nozzle does three jobs at once:

1. **Metering.** The nozzle carries 1.76 kPa of the 1.97 kPa branch, which is 6.4x the header dynamic head. It is inertial, so flow uniformity does not depend on flow rate.
2. **Zoning.** The nozzle open-area map is the power map, set by photo-tool artwork.
3. **Heat transfer.** The plate pays the metering loss anyway. JH spends it at the fin roots, where the jet raises h, instead of in a comb that sits 8 mm upstream.

Over the dies of a real package the nozzle pitch closes to 6 mm (4 mm as a stretch option), and 91 % of the flow goes there. Over HBM and unheated margins the laminate carries open, upstream-metered slots with no jets. So the plate puts jets over the dies and metered channels over the HBM.

**The answer the lens was asked for.** Do jets beat the hierarchical manifold micro-channel (HMMC) at equal pumping power and equal fouling constraints?

- **As an area-filling core, no.** Continuity fixes the problem. At 18 LPM over 117 cm2 the volumetric flux is only 2.56 cm/s, so a fouling-tolerant 0.3-0.5 mm nozzle array reaching 1-5 m/s must be sparse (2-6 mm pitch). Martin, Womac and a laminar stagnation model then give area-averaged h of only 9-32 kW/m2K at 4-40 kPa (section 2.1). That is 4-14x below the HMMC-R's 127 kW/m2K finned h_eff at 5-6 kPa. The literature's 100-300 kW/m2K microjets use 31-150 um nozzles at 10-40x our flux density.
- **As a hybrid on the same 0.15 mm fins, marginally on a uniform 15 kW TTV.** h_eff rises from 127 to 147 kW/m2K (+15 %) at the same plate dP (5.5 vs 5.7-6.0 kPa). That is worth -1.1 K average / -1.2 K maximum, or -1.3 K at equal pumping power. This is inside the model's uncertainty band.
- **Over hot spots, yes.** At 350 W/cm2 reticle dies with heat-proportional zoning, the die-zone h_eff is 158 kW/m2K (6 mm pitch) to 172 kW/m2K (4 mm pitch), against 127-133 for the open-slot manifold. That is -3 to -7 K at the hottest die. It reaches the HMMC performance core's (HMMC-P) result without its 33 um loop filtration.
- **On coarse, fouling-proof channels, decisively.** Jets add +45 % h_eff to a 0.30 mm-gap core. That makes possible a screen-free SKU that still beats CoolIT on every thermal metric.

**Headline at 15 kW / 18 LPM / 45 C (robust core JH-R, Tier-1 PCM pad, Monte-Carlo median and P90 in brackets):**

| metric | CoolIT 15 kW | JH-R | change |
|---|---|---|---|
| average case-to-inlet dT | 34.4 K | 26.9 K (P90 30.3) | -22 % |
| maximum case-to-inlet dT | 44.2 K | 29.9 K (P90 33.4) | -32 % |
| plate dP port-to-port incl. clean screen | undisclosed (~22-25 kPa est.) | 5.5 kPa (P90 6.6) | ~-75 % |
| Q capacity at T_case,max <= 85 C, 1.2 LPM/kW | ~13 kW | 22.9 kW (P90 19.4) | +75 % |
| liquid-metal tier (Tier 2) avg / max | - | 21.8 / 23.9 K | -37 / -46 % |

**Decisive differentiators**

1. **Metering loss becomes heat transfer.** The plate is at the same ~5.5 kPa as the HMMC but has +15 % h_eff, and about 4x lower dP than the skived benchmark. Uniformity is set by an inertial nozzle (branch/head 6.4), so it holds from 9 to 36 LPM.
2. **Hot-spot performance at the robust fouling floor.** At 350 W/cm2 with liquid metal, JH-R reaches T_case,max 88.0 C at 6 mm pitch, and 84.5 C at 4 mm pitch with a 0.8 mm finished base. HMMC-R is 93.5 C and CoolIT-like split-flow is >100 C. All of this behind the same 50 um absolute screen as HMMC-R.
3. **Nozzle-programmed zoning.** One etched foil carries the power map. Zones are fed in parallel from shared headers, which is also the IP design-around to JetCool's series re-impingement claim.
4. **A fouling-proof variant (JH-X).** The minimum passage is 0.30 mm everywhere, so the plate needs no integrated screen on today's 50 um nominal loops. Relative fouling life is ~2.3x a skived plate. It still gives 32.2 / 35.2 K (PCM) against 34.4 / 44.2 K, at 5.1 kPa.
5. **Conventional manufacture.** The chain is skived fins, two photo-etched foils, a CNC block and one diffusion-bond cycle. There is no wafer lithography (unlike Frore LiquidJet). Factory cost is ~US$180 at 100k/yr.

**Where it does not win:**

- On the uniform TTV, the margin over the HMMC is only ~1 K.
- On 1.4-3.6 kW GPU plates at 1.2 LPM/kW, the jet gain is 0.6-1.3 K, because the jets are too slow.
- On large low-flux footprints the isothermal-cell caloric term makes any short-cell plate ~2 K worse than a long-channel plate on the average, though better on the maximum.
- Height (17.8 mm) and mass (~2.1 kg) are not claimed wins.
- Cost is +US$75 over a commodity skived plate.
- Jet erosion of Cu in PG25 is an open question that CoolIT itself is studying.

## 2. Thermal core

### 2.1 Why bare jets lose at 1.2 LPM/kW (model section A)

Jet velocity is set by flux and open-area ratio: Vj = j / Ar, where j = 2.56 cm/s at 18 LPM over 117 cm2. Area-averaged h on a bare base (H/D = 2), with jet dP at Cd 0.75 plus one lost dynamic head:

| LPM | d mm | pitch mm | Vj m/s | Re_d | h Martin ARN* | h Womac 1993 | h laminar stagnation | jet dP kPa |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 18 | 0.3 | 2.66 | 2.56 | 618 | 27 | 17 | 30 | 9.2 |
| 18 | 0.5 | 4.43 | 2.56 | 1031 | 23 | 14 | 23 | 9.2 |
| 18 | 0.5 | 6.27 | 5.13 | 2062 | 27 | 17 | 25 | 36.7 |
| 36 | 0.5 | 4.43 | 5.13 | 2062 | 37 | 20 | 32 | 36.7 |
| 36 | 0.3 | 3.76 | 10.3 | 2474 | 52 | 31 | 46 | 147 |

Martin values with Re < 2000 are extrapolated below the correlation's validity, so treat them as optimistic. For comparison, the HMMC-R finned h_eff is 127 kW/m2K at 5.7 kPa. Two corrections to the earlier draft (`jet_calc.py`):

- Martin's F2 = 0.5 Re^(2/3). The draft omitted the 0.5.
- The draft's turbulent wall-jet "Womac" term ignored continuity and gave 160-600 kW/m2K.

Jet h scales only as d^(-1/3) at fixed j and Ar (fouling-friendly), but its absolute level is capped by the low volumetric flux. Jets therefore need either extended surface or concentrated flow. JH uses both.

### 2.2 Geometry of record

| element | JH-R (robust, drop-in) | JH-P (performance, <= 33 um loops) | JH-X (screen-free) |
|---|---|---|---|
| fins gap / thickness / height | 0.15 / 0.10 / 2.0 mm, skived OFE Cu | 0.10 / 0.10 / 1.5 mm | 0.30 / 0.25 / 4.0 mm |
| base | 1.0 mm as-bonded, 0.8 mm finished under dies | same | same |
| nozzle slot (N1 foil 0.20 mm) | 0.22 mm, pitch P_r 8 mm (dies: 0.42 mm at 6 mm) | 0.18 mm at 6 mm | 0.30 mm at 10 mm |
| return slot | 1.0 mm, midway between nozzles | 1.0 mm | 1.0 mm |
| flow length nozzle-to-return | 3.4 mm | 2.4 mm | 4.4 mm |
| in-gap jet velocity at 18 LPM | 1.55 m/s (lamina slot 0.93 m/s) | 1.71 m/s | 1.57 m/s |
| channel velocity / Re | 0.085 m/s / 19 | 0.10 m/s | 0.06 m/s |
| h stagnation / jet column / channel | 42 / 22 / 13.6 kW/m2K | - | - |
| fin efficiency, h_eff | 0.52, **147 kW/m2K** (open-slot ref 127) | **209** (ref 188) | **88** (ref 60) |
| smallest passage / filter needed | 0.15 mm channel; 50 um abs plate screen | 0.10 mm; <= 33 um abs loop | 0.30 mm; 50 um nominal loop, no screen |

The cell model splits each half-cell into two regions.

- **Impingement region.** It runs over x1 = w_n/2 + 0.5 H, which is 28 % of the cell for JH-R. Here the fin walls see developing flow at (Vj + u_ch)/2 over the descent height, and the floor sees plane laminar stagnation flow (velocity gradient 0.6 Vj/w_n).
- **Channel region.** Downstream of the turn the flow is ordinary channel flow, with the thermal entrance restarted after impingement.

The jet increment is the most uncertain term. The Monte Carlo gives it a lognormal sigma of 0.30. The modelled 15-20 % gain sits below JetCool's vendor claim of 20-40 % lower R than micro-channel plates, and its third-party figure of 25 % including TIM, so the model is not more optimistic than the jet vendors.

### 2.3 Flow path and zoning

Fluid enters a 16 mm port, passes the integrated screen and goes into two L1 troughs on the plate centre-line (centre-fed, centre-collected). From there it goes down into L2 inlet galleries running across the fins, through 1.0 mm windows in the N2 stiffener foil, and through the N1 slot nozzles into the fin gaps. It impinges, turns, runs 3.4 mm and rises through return slots into the L2 outlet galleries, then into the outlet trough. No fluid ever passes over a second heated zone: every zone is in parallel.

Zoning for the 2027-28 package (4 x 26 x 33 mm dies at 350 W/cm2 plus 16 HBM at 40 W/cm2):

| zone | share of flow | flux vs average | feed |
|---|---|---|---|
| die block (~35 cm2) | 91 % | 3.0x | slot jets: 0.42 mm at 6 mm pitch (stretch 0.28 mm at 4 mm), 1.57 m/s |
| HBM columns | ~8 % | 0.32x | open 1.0 mm slots behind 0.5 mm gallery orifices sized to the same branch dP; Cu pedestal stepped to the HBM plane within 0.05-0.1 mm |
| unheated margin | ~1 % | 0.04x | no slots; 5 % slot-end bleeds only |

### 2.4 Interface strategy by tier

| tier | package | interface | JH-R avg / max at 15 kW TTV | 350 W/cm2 hot die T_case,max |
|---|---|---|---|---|
| 1, drop-in | lidded, serviceable | PCM pad, 0.055 cm2K/W, 20-30 psi, plate flatness <= 15 um over the die | 26.9 / 29.9 K | 102 C (6 mm) / 100 C (4 mm) |
| 2, OEM | Ni-finished lid | liquid metal 0.015 on 3-5 um electrolytic Ni, dam, 20-30 um BLT, no Al | 21.8 / 23.9 K | 88.0 C (6 mm) / 86.3 C (4 mm); 84.5 C with 0.8 mm base |
| 3, chip co-design | bare die | stepped pedestal plus liquid metal; removing lid and TIM1 is worth ~28 K at the junction at 350 W/cm2 | n/a (case = die top) | GPU Tj ~78 C vs ~106 C lidded-LM (6 mm pitch) |

## 3. Hydraulic architecture

**Manifold levels at 18 LPM:**

| level | element | velocity | rule |
|---|---|---|---|
| L0 | 16 mm ports (20 mm option) | 1.49 m/s (0.95) | <= 1.5 m/s |
| L1 | inlet trough (enlarged 15 % vs HMMC-elite) / outlet trough 1.5x area | 0.78 / 0.52 m/s | head 0.31 kPa; branch / head = 6.4 >= 6 |
| L2 | 14 inlet galleries 3.0 x 7.0 mm, 14 outlet galleries 3.4 x 8.4 mm, 0.8 mm walls (dies: 2.3 mm galleries, 0.7 mm walls, 6 mm pitch) | <= 0.52 m/s | along-gallery head / branch <= 1/15 |
| L3 | N2 windows 1.0 mm, then N1 slot nozzles 0.22 mm | 0.2, then 0.93 m/s (1.55 m/s in the gaps) | nozzle 1.76 kPa, inertial |
| L4 | fin gaps, 3.4 mm | 0.085 m/s | 0.21 kPa incl. turns |

Hierarchy of passage widths: port 16 > trough 6 > gallery 3.0 > window 1.0 > nozzle 0.22 > channel 0.15 mm. Every stage is wider than the next, so the nozzle never becomes the sieve.

**dP budget, port-to-port, PG25 at 45 C:**

| flow | nozzle | channel + turns + return | troughs + galleries + tees | ports | screen (clean) | **total** | pump W |
|---|---:|---:|---:|---:|---:|---:|---:|
| 18 LPM (1.2 LPM/kW) | 1.76 | 0.21 | 0.61 | 2.57 | 0.40 | **5.5 kPa** | 1.7 |
| 18 LPM, 20 mm ports | 1.76 | 0.21 | 0.61 | 1.05 | 0.40 | 4.0 kPa | 1.2 |
| 36 LPM, 16 mm ports | 7.0 | 0.4 | 2.4 | 10.3 | 1.6 | **21.7 kPa** | 13.0 |
| 36 LPM, 20 mm ports | 7.0 | 0.4 | 2.4 | 4.2 | 1.6 | 15.6 kPa | 9.4 |

The Monte Carlo gives P10 / P50 / P90 = 4.5 / 5.6 / 6.6 kPa at 18 LPM. The external claim is <= 8 kPa at 18 LPM and <= 25 kPa at 36 LPM until CFD and test. The real-package die zone runs a 2.11 kPa core. HBM zones are orificed to the same branch dP.

**Uniformity.** The branch is 89 % inertial, so the branch-to-head ratio is flow-independent: global max/min target is <= 1.10 from 9 to 36 LPM, and the flow-driven hot spot is 1.5 K nominal (+/-10 %) and 2.5 K conservative (+/-20 %). Slot-width tolerance (laser +/-10 um, or PCE +/-15 um) maps to +/-5-7 % local flow. Systematic drift cancels across a sheet, and every plate is flow-signature tested.

**Velocity and erosion.** Copper erosion-corrosion guidance for hot water (<60 C) is ~1.5 m/s. CoolIT announced an impinging-jet erosion study in PG25 in 2025 with no published threshold. The jet velocity is therefore capped:

- 1.55 m/s nominal at 18 LPM;
- 1.94 m/s at the rated continuous maximum of 1.5 LPM/kW;
- 3.1 m/s at 36 LPM, allowed only as a qualification point until experiment E3 clears >= 3.5 m/s.

The fallback is a 3-5 um mid-P electroless Ni wetted path, which is the GB200 industry norm.

**Couplings.** A UQD08 pair costs ~25 kPa at 18 LPM, about 4.5x the plate. The 15 kW class needs UQD12-class or 3/4 in barbs (~5 kPa). Rubin-class plates (2-4 LPM) can use UQD08 at 1-2 kPa. A 5.5 kPa plate is compatible with negative-pressure loops.

**Filtration and fouling.**

| | JH-R | JH-P | JH-X |
|---|---|---|---|
| plate screen | 50 um abs pleated 316L, >= 12 cm2 (0.4 kPa clean), alarm at +2 kPa | 33 um abs, >= 15 cm2 | none (100-150 um installation strainer) |
| W/d at last filter | channel 3.0, nozzle 4.4 | 3.0 | 3.3 on 50 um nominal (~90 um abs) |
| relative life vs skived plate | 0.6-1.2x | ~0.6x | ~2.3x (23 y vs 10 y reference) |

The jet-specific fouling risk is impaction. The Stokes number is 6.9 for 50 um Cu oxide and 1.1 for 20 um at the jet. Dense particles that pass the screen reach the stagnation lines on the base, where wall shear is low. They cannot bridge a 0.15 mm gap, but they can build a film there (+0.6 K per 10 um). Experiment E3 tests exactly this. Other rules, unchanged from the HMMC programme:

- slot dead-ends bleed 5 % through 0.6 mm orifices;
- port-adjacent channels stay outside the die;
- the geometry is reverse-flow tolerant;
- factory flush to ISO 16232.

## 4. Mechanical and construction

**Stack-up (standard 15 kW class, 17.8 mm):**

| # | layer | thickness | process | function |
|---|---|---|---|---|
| 0 | base + fins | 1.0 + 2.0 mm | skived OFE C10100 | fin field 108 x 108 mm; perimeter land stepped to 2 mm |
| N1 | nozzle foil | 0.20 mm | photochemical etching (PCE) or green ps-laser | slot nozzles and return slots; bonded to every fin tip (85 % of fin length tied) |
| N2 | stiffener foil | 0.60 mm | PCE | 1.0 mm windows over nozzles, return windows; spreads tie loads to gallery walls |
| B | manifold block | 11.5 mm | CNC OFE: galleries from below, troughs and posts from above, port bores, screen cavity | L1/L2 |
| K | cover | 2.5 mm | Cu plate, lapped | closes troughs; post span <= 5.5 mm |

**Joining.** All five layers are joined in one vacuum diffusion-bond cycle (850-950 C, 5-10 MPa, OFE only, never H2 with ETP copper). There is no filler to wick into 0.22 mm nozzles or 0.15 mm gaps. The cycle anneals the stack, so the design uses annealed OFHC (yield 70 MPa, UTS 220 MPa). Braze is allowed only for the B-K joint and port bosses. A green-laser or friction-stir-welded perimeter seam is the fallback. Acceptance:

- 100 % He leak <= 1e-5 mbar L/s (target 1e-6);
- C-scan sampling of fin-tip bond fraction (>= 50 %, reject < 30 %);
- first-article CT;
- 100 % flow/dP signature (5.5 +/- 0.6 kPa at 18 LPM, 45 C).

**Pressure and the tie chain.** The pressure envelope is the base, perimeter walls, block and cover. The internal foils see only internal dP (<= 0.1 MPa), so a foil failure cannot leak externally (leak-before-break by construction).

- Base-to-cover ties run fin, N1, N2, gallery walls and posts.
- Fin tie stress at 3 MPa with 85 % bonded tips is 8.8 MPa (SF 8 on annealed yield).
- N1 over a 1.0 mm window: 38 MPa at 3 MPa burst (SF 1.9 on yield, 5.8 on UTS) and 12 MPa at MAWP.
- N1+N2 over a 3.0-3.4 mm gallery: 21-27 MPa at burst (SF 2.6-3.3).
- A single 0.25 mm foil over a 3 mm gallery would see 216 MPa, which is why the N2 stiffener exists.
- Ratings: MAWP 1.0 MPa (145 psi), proof 1.5 MPa, design burst >= 3.0 MPa (OCP example > 20 bar), first-article burst >= 4.5 MPa, vacuum-stable to -0.9 bar(g).

**Base thickness logic.** Between 0.15 mm tied gaps the base is irrelevant to pressure. Its floor is set by finish machining (0.1-0.2 mm), erosion allowance (0.1 mm) and skive tolerance: order 1.0 mm, deliver 0.8 mm under the dies. Each 0.2 mm removed is -1.8 K at 350 W/cm2.

**Flatness and mounting.**

- Lap after bonding to <= 15 um over the die and <= 25 um over 100 mm, Ra <= 0.4 um.
- Spring screws on a stiff frame bearing within 10 mm of the die edge.
- Retention 10-20 psi for liquid metal, 20-30 psi for PCM.
- Tied-sandwich mount bow over a 50 mm die is 4-25 um, versus 13-77 um for an untied skived plate (sibling base-stress check).

**Envelope.** The 15 kW-class body is 148 x 152 x 17.8 mm, ~2.1 kg. HMMC-elite is 21.1 mm because JH deletes its comb, plenum and grate. The low-profile LP15 version is 14.5 mm (fins 1.5 mm, block 9.5 mm, cover 2.0 mm) and costs +0.8 K and +1 kPa. The Rubin-class body is 110 x 120 x 15 mm, ~1.0 kg.

## 5. Manufacturing route at volume

Process chain (all conventional; capacity exists in TW/CN/VN/MX/EU):

1. **Skive** the fin field: 0.15/0.10 x 2.0 mm, 108 mm wide, 2-5 min, USUSTK/Wieland/Nakamura-class machines; CNC the base land.
2. **Make the foils.** N1 is a 0.20 mm OFE foil with 0.22 mm slots by double-sided PCE (feature >= foil thickness), +/-15 um. The alternative is green picosecond laser at +/-10 um, US$5-15 per plate. N2 is a 0.60 mm foil with 1.0 mm windows by PCE. Phototools cost US$0.5-3k; PCE capacity is abundant (PCB/EMI-shield industry).
3. **CNC the manifold block:** 3.0 mm slot-mill galleries (0.8 mm walls; 0.7 mm in die zones), troughs with 2.5 mm posts, bores, screen cavity.
4. **Clean** (alkaline/acid, deoxidise), stack in a graphite fixture, and **diffusion-bond** in batches of 50-200 per 8-12 h cycle.
5. **Finish:** lap the contact face, machine the pedestal step, mask and electrolytically Ni-plate the contact face (Tier 2), fit the screen cartridge and stubs.
6. **Test:** ISO 16232 flush, 100 % He leak, 100 % flow/dP signature, serialisation.

| cost element, 15 kW class (148 x 152 mm) | 10k/yr | 100k/yr |
|---|---:|---:|
| OFE copper ~2.2 kg incl. swarf | 25 | 23 |
| skived core | 40 | 24 |
| N1 + N2 foils (PCE) | 24 | 10 |
| CNC manifold block | 80 | 34 |
| cover + stubs | 14 | 6 |
| diffusion-bond cycle | 55 | 32 |
| screen, plug, taps | 15 | 8 |
| lapping, C-scan sampling, inspection | 12 | 6 |
| load frame, screws | 20 | 14 |
| He leak + flow test | 8 | 5 |
| **factory cost incl. 12 % yield/overhead** | **~US$330** | **~US$180** |
| Rubin-class plate (110 x 120 mm) | ~US$230 | ~US$128 |
| JH-X (no screen, coarser fins) | ~US$315 | ~US$170 |

**Cost basis and context.** Element costs come from `manufacturing-cost.md` and `gap-cost-volume-and-market-anchors.md` (KB-M; confirm by RFQ). The canonical GB200-class skived plate is ~US$165 at 10k and ~US$100 at 100k. JH is ~US$10 below HMMC-elite at 100k (one foil pair instead of three laminates) and remains far under the ~US$400 Rubin Group-A ASP. At 1M/yr it would be ~US$125, set by the stamped cover, a two-shift furnace and an automated foil stack.

**Lead time and capex.**

- First bonded alpha plates: 8-10 weeks (laser-cut N1 in days, block 2 weeks, furnace slot 4-6 weeks).
- 100k/yr capacity: 9-12 months.
- 2-3 vacuum furnaces at US$3-6 M are the gate.

**Yield risks, ranked:**

1. Unbonded fin tips under N1. Mitigation: foil flatness < 10 um, C-scan, burst sampling.
2. Nozzle-slot narrowing by bond-pressure creep at the slot edges. Mitigation: design the slot at +10 um; flow signature catches it.
3. Fin damage before bonding. Mitigation: fixtures.
4. N1-to-gallery registration. Tolerant by design, because the 0.22 mm slot sits under a 1.0 mm window.
5. Gallery-wall chatter at 0.7 mm walls.

## 6. Predicted performance vs benchmark

### 6.1 15 kW / 18 LPM PG25 / 45 C / 117 cm2 (model section C)

| design | h_eff | caloric | TIM | base | conv | **avg dT** | max dT | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow, paste (calibration) | 101 | 6.3 | 9.0 | 6.6 | 12.6 | **34.5** | 44.3 | 0.269 | 24.6 | 7.4 | 12.7 |
| HMMC-R, PCM (programme reference) | 127 | 7.6 | 7.1 | 3.3 | 10.1 | **28.0** | 31.1 | 0.219 | 5.7 | 1.7 | 21.6 |
| JH-R, same paste 0.07 (like-for-like) | 147 | 7.8 | 9.0 | 3.3 | 8.8 | **28.8** | 33.8 | 0.225 | 5.5 | 1.7 | 19.4 |
| **JH-R, PCM (Tier 1)** | 147 | 7.8 | 7.1 | 3.3 | 8.8 | **26.9** | **29.9** | 0.210 | 5.5 | 1.7 | 22.9 |
| JH-R, liquid metal (Tier 2) | 147 | 7.8 | 1.9 | 3.3 | 8.8 | **21.8** | 23.9 | 0.170 | 5.5 | 1.7 | 32.3 |
| JH-P, PCM / LM (<= 33 um loops) | 209 | 8.4 | 7.1 / 1.9 | 3.3 | 6.1 | **24.8 / 19.7** | 27.8 / 21.8 | 0.194 / 0.154 | 6.1 | 1.8 | 26.1 / 39.1 |
| JH-X, PCM / LM (screen-free) | 88 | 7.2 | 7.1 / 1.9 | 3.3 | 14.6 | **32.2 / 27.0** | 35.2 / 29.1 | 0.251 / 0.211 | 5.1 | 1.5 | 17.9 / 23.2 |

Monte Carlo (20k samples), JH-R:

| TIM | avg P10 / P50 / P90 K | max P10 / P50 / P90 K | Q cap pessimistic / median / optimistic kW |
|---|---|---|---|
| PCM | 24.5 / 27.0 / 30.3 | 27.4 / 30.0 / 33.4 | 19.4 / 22.9 / 26.3 |
| liquid metal | 20.4 / 21.9 / 24.0 | 22.4 / 24.0 / 26.2 | 27.7 / 32.0 / 36.0 |
| paste | 25.0 / 28.9 / 35.5 | 29.7 / 33.9 / 40.7 | 14.6 / 19.3 / 23.9 |

With CoolIT's paste the P90 average (35.5 K) does not beat 34.4 K. The like-for-like win is certain only on the maximum (P90 40.7 vs 44.2 K) and the dP.

**Flow and pumping power (PCM):**

| LPM/kW | 0.6 | 1.0 | 1.2 | 1.5 | 2.0 | 2.4 |
|---|---:|---:|---:|---:|---:|---:|
| JH-R avg / max K | 37.5 / 40.5 | 28.9 / 31.9 | 26.9 / 29.9 | 24.9 / 27.9 | 22.9 / 25.9 | 21.9 / 24.9 |
| JH-R dP kPa | 1.5 | 3.9 | 5.5 | 8.6 | 15.1 | 21.7 |
| HMMC-R avg K | 38.0 | 29.9 | 28.0 | 26.3 | 24.5 | 23.6 |

- **Equal pumping power, 1.8 W (HMMC-R's figure at 18 LPM):** JH-R gives 26.6 / 29.6 K at 18.5 LPM; HMMC-R gives 27.9 / 30.9 K.
- **Equal pumping power, 6.5 W (CoolIT-like):** JH-R gives 23.2 / 26.2 K at 28.5 LPM (paste 25.2 / 30.2 K, liquid metal 18.1 / 20.2 K); HMMC-R gives 24.8 / 27.8 K.
- **CoolIT's 34.4 K average:** JH-R needs only 10.5 LPM (0.70 LPM/kW, 0.34 W) with PCM, 8.2 LPM with liquid metal, 11.7 LPM with paste.
- **Inlet temperature allowed for T_case,max 85 C at 15 kW:** 55.1 C (PCM), 61.1 C (liquid metal), 51.2 C (paste), versus ~40.8 C for CoolIT.
- **At 2x flow (36 LPM):** 21.9 / 24.9 K (PCM) and 16.8 / 18.9 K (liquid metal), at 21.7 kPa (15.6 kPa with 20 mm ports).

### 6.2 Real 2027-28 package: 4 reticle dies at 350 W/cm2 + 16 HBM (12.85 kW, 15.4 LPM; model section D)

Hottest-die case-to-inlet = caloric 6.7 + base 9.0 + q R_TIM + q / h_eff. This is the nonuniform-heatmap fit, which reproduces HMMC-R at 60.5 / 48.3 K.

| core (die zone) | h_eff | paste 0.05 | PCM | liquid metal | T_case,max LM (1.0 / 0.8 mm base) |
|---|---:|---:|---:|---:|---|
| CoolIT-like split-flow (heatmap 2-D result) | 101 | 88.6 K | - | ~76 K | ~121 C |
| HMMC-R (synthesis) | 127 | 60.7 | 62.5 | 48.5 | 93.5 / 91.7 C |
| HMMC-P (<= 33 um loops) | 187 | 51.9 | 53.6 | 39.6 | 84.6 / 82.8 C |
| **JH-R, 6 mm die pitch (nominal)** | 158 | 55.3 | 57.0 | 43.0 | **88.0 / 86.2 C** |
| JH-R, 4 mm die pitch (etched gallery laminate) | 172 | 53.6 | 55.3 | 41.3 | 86.3 / **84.5 C** |
| JH-P, 6 / 4 mm | 216 / 226 | 49.4 / 48.7 | 51.1 / 50.4 | 37.1 / 36.4 | 82.1 / 80.3 C; 81.4 / 79.6 C |
| JH-X, 6 mm | 105 | 66.5 | 68.3 | 54.3 | 99.3 C (not for this regime) |

Honest reading:

- **Size of the jet increment.** In our own model the like-for-like open-slot die zone is 133 kW/m2K. The jet increment at the hot die is therefore 3.0-4.7 K against that baseline, and 5.5-7.2 K against the synthesis HMMC-R row.
- **What meets 85 C.** T_case <= 85 C at 350 W/cm2 needs liquid metal plus either JH-R at 4 mm pitch with a 0.8 mm base, or JH-P. Direct-to-die (Tier 3) adds ~28 K of junction margin.
- **Die gradient and HBM.** The across-die case gradient is 6-8 K, against 22-30 K for split-flow. HBM Tj is 88-91 C at 40 W/cm2 (pedestal plus 0.1 mm paste) and 81-82 C with indium. CoolIT-like is 105 C because its HBM sits downstream of the dies. JH routes fresh fluid to each zone in parallel.

### 6.3 GPU-class plates, 1.4-3.6 kW (model sections E and G)

| case at 1.2 LPM/kW, die-concentrated (90 % of flow on the die block) | die W/cm2 | Vj m/s | JH-R die case-to-inlet PCM / LM | open-slot ref | jet gain |
|---|---:|---:|---|---|---:|
| B300-class 1.4 kW, 2 dies | 71 | 0.66 | 21.1 / 17.8 K | 21.7 / 18.4 K | 0.6 K |
| Rubin-class 2.3 kW, 2 dies | 118 | 0.81 | 27.7 / 22.2 K | 29.1 / 23.5 K | 1.3 K |
| Rubin-Ultra-class 3.6 kW, 4 dies | 91 | 0.62 | 24.4 / 20.1 K | 25.2 / 20.9 K | 0.8 K |

- **Jet benefit at GPU scale.** At GPU-class flows the jets run at 0.6-0.8 m/s and the benefit is about 1 K. JH is sold there for its zoning and metering, not its jets.
- **Uniform-footprint convention** (model section 6: 31-45 W/cm2 over 45-80 cm2). CoolIT-like gives 13.2-16.3 K average / 20.4-23.8 K maximum. JH-R gives 15.3-16.7 / 17.1-18.7 K. JH is ~2 K worse on the average because the caloric term dominates, and 3-5 K better on the maximum.
- **Against CoolIT's own 4 kW plate** (50 x 50 mm, 4 kW, 6 LPM, < 0.009 C/W max-case incl. TIM). JH-R gives 0.0081 C/W with PCM and 0.0062 C/W with liquid metal. With paste it gives 0.0093 C/W, which does not beat CoolIT.

## 7. Product family and applications

| SKU | target | what changes |
|---|---|---|
| JH-R15 / JH-R15Z | 15 kW TTV-class and 2027-28 multi-reticle packages | uniform 8 mm nozzles (TTV) or zoned artwork (6/4 mm die pitch, metered HBM slots, stepped HBM pedestal); 16-20 mm ports, UQD12-class |
| JH-P15Z | 350-400 W/cm2 dies on <= 25-33 um loops | 0.10 mm fins; the only lidded route to <= 82 C at 350 W/cm2 |
| JH-R-Rubin / Rubin Ultra | 1.8-3.6 kW packages, 110 x 120 mm | jets over dies only; value is zoning, uniformity and dP (UQD08); thermal parity with HMMC +/-1 K |
| JH-X | legacy or dirty 50 um nominal loops, retrofit, edge sites | 0.30 mm passages, no screen; beats CoolIT on avg (PCM -6 %), max (-20 %) and dP (~-75 %); ~2.3x fouling life |
| CPU / NVSwitch / NIC | 300-800 W, low flux | jets irrelevant; JH-X-lite or simple manifold plate sharing the frame and ports |
| wafer-scale / multi-chip | 20-30 kW wafers, chiplet arrays | tiled JH cells with per-die artwork; dP is independent of size because all cells are parallel; ports scale (2-4 pairs) |
| 800 VDC power shelf (Kyber, 9-26 kW per rack) | same PG25 TCS loop, 5-30 W/cm2 | gap pad dominates, so jets bring nothing; JH-X body as a kit item at US$50-150 |
| SiC EV / charger modules | 50/50 WEG at 65 C, -40 C cold start, Al loops | aluminium-brazed JH (Al nozzle foil, Controlled Atmosphere Brazing (CAB)), die-mapped 0.4-0.5 mm slots over each switch. The jets are inertial, so cold-start dP rises an estimated ~2-4x, not the 50-80x of a viscous micro-channel. License to module or Tier-1 makers; AQG 324 takes 24-36 months |
| niches | laser-diode bars (500-1,000 W/cm2), RF GaN, directed energy | point-targeted jets are the natural fit; DI water, Ni-plated Cu, custom |

## 8. Reliability, qualification and drop-in compatibility

**Drop-in.**

- Thermal spec stated in PG25 at 45 C at 0.5-1.5 LPM/kW (the 1.2 LPM/kW convention is a CDU rating, not a silicon requirement).
- Fits the ASHRAE W45 and OCP TCS envelope (17-65 C, components to 100 psi).
- Couplings per OCP UQD v2.0.0 (UQD08 for Rubin-class).
- Mounting frames per vendor; flatness <= 15 um over the die.
- Operates under negative pressure.
- Data published in the OCP Cold Plate Test Spec v1.0.0 format: R = (T_case - T_in)/P at >= 6 flow points from 25 % to 150 % of rated flow, dP at 45 +/- 2 C, named TIM, three plates plus an independent lab. CoolIT's 15 kW brief gives one flow point and no dP.

**Wetted materials.**

- OFE Cu (C10100/C10200) throughout.
- 316L screen; peroxide-cured EPDM seals.
- No Al, no solder, no braze filler in the fin and nozzle path.
- Ni only on the contact face (Tier 2), or optionally ENi on the wetted path if E3 demands it.

**Qualification matrix:**

| test | condition |
|---|---|
| He leak | 100 %, <= 1e-5 mbar L/s (target 1e-6) |
| proof / burst | 1.5 MPa / >= 3.0 MPa design, >= 4.5 MPa first articles |
| pressure cycling | 0-1.0 MPa, 50k cycles |
| thermal cycling | 10-65 C, 1,000 cycles operating; -40/+70 C storage |
| power cycling | 1,000 cycles, 11 MPa base fatigue amplitude, SF ~6 |
| PG25 soak | 2,000-5,000 h at 65 C, ion release and inhibitor depletion |
| jet erosion | 3,000 h at 1x / 1.5x / 2x / 2.6x Vj, dosed PG25 at 60 C (E3) |
| fouling | ISO 4406 18/16/13 dosing plus 20-50 um Cu oxide, 2,000 h, dP and R drift |
| shipping | shock/vibration ISTA 3A / ASTM D4169 |
| cleanliness | ISO 16232 |
| re-check | TIM BOL and post-cycling per ASTM D5470 |

**Service life.**

- JH-R: 10 years behind its 50 um absolute screen, the same channel floor as HMMC-R.
- JH-X: target 15+ years, screen-free.
- The plate dP signature is the fouling alarm: +2 kPa means the screen is at 3x clean.

## 9. IP posture

**Live families to avoid** (USPTO records found this session; claim text read only in summary, so counsel must confirm):

| family | claim elements as summarised | JH design-around |
|---|---|---|
| MIT / JetCool "Modular microjet cooling of packaged electronic components", US 10,665,529 / 11,018,077 / 11,594,470 (2017 priority, to ~2038) | base with microjet nozzles and an exit port, raised sidewalls forming a cavity open toward the packaged device, attached to the package | sealed plate; no open cavity; coolant never touches the package; nozzles are slots in a foil bonded to fin tips |
| JetCool "Internal recirculation cooling module", US 12,432,878 (filed 2024, to ~2044) | jet plate with two nozzle-array segments; the first impingement volume feeds the second inlet plenum (series re-impingement) | every slot fed in parallel from inlet galleries; spent fluid always goes to outlet galleries; no staging |
| MIT / JetCool embedded microjets in RF devices, US 10,651,112 / 10,903,141 / 11,322,426; direct-contact and re-entrant plates, US 11,191,184 / 11,277,937; co-located nozzles, US 12,100,643 | jets in the device or substrate; fluid on the component | none of these features |
| Frore LiquidJet (2023-25 filings, unpublished; "3-D short-loop jet channels", metal-wafer semiconductor process, multistage hot-spot concentration) | unknown | skived fins plus PCE foils, not lithographed wafer microstructures; parallel, not multistage, zones; re-search at months 3 and 9 |
| CoolIT Split-Flow, US 8,746,330 / 9,603,284 / 12,495,513 (expiry Aug 2028 to ~mid-2031) | inlet opening between the channel ends, so flow splits to both ends | interior outlets, no end collection, distribution in a separate laminate, expired-art shield (below). Ready fallback: end-fed segmented fins with an impingement trench under each nozzle (inlet at segment ends, outlet between them), costing -12 % h_eff (+0.9 K TTV, +3.5 K at the hot die) |
| Microsoft / Nvidia / Intel jet-on-die and micro-channel lid filings (2020-24) | jets on bare die, liquid-cooled lids | Tier 3 is a plate on bare die through liquid metal, with no coolant on the die; claim-check the stepped pedestal |

**Expired or public foundations we build on:**

- Harpole manifold micro-channel, US 5,088,005 (expired ~2010).
- IBM cross-hatch jet/channel distribution, US 5,016,090.
- Unisys chip jet, US 4,750,086.
- Liquid jet cold plate US 5,316,075 (expired, fee-related).
- Cooligy interwoven manifolds, US 6,986,382; multi-level, US 7,156,159; hot-spot-targeted delivery, US 7,104,312 (all expired 2023-24).
- Tuckerman-Pease, US 4,450,472.
- Published prior art (no patent found): Sung & Mudawar slot-jet-into-micro-channel hybrids (Purdue, 2006-2009) and IBM's distributed-return jet arrays (Brunschwiler, 2006).

**What we can claim** (provisionals before any disclosure):

1. A cold plate whose only flow-metering restriction is an impinging slot-nozzle foil bonded to the fin tips, with a branch-to-header head ratio >= 6 and a per-zone open-area map proportional to the device power map.
2. The N1/N2 nozzle-tie laminate as both pressure tie and nozzle.
3. Parallel hybrid zoning: jets over logic, upstream-metered open slots over HBM, fed from shared centre-line headers.
4. A screen-free coarse jet-fin core with every passage >= 3.3x the absolute rating of a nominal loop filter.
5. A velocity-capped, erosion-qualified jet rule.
6. Die-mapped inertial-jet SiC module coolers for viscous cold-start loops.

**Budget.** Outside-counsel claim charts against JetCool, Split-Flow and Frore cost US$40-80k, in weeks 3-8.

## 10. Risks, experiments and roadmap

| risk | impact | mitigation |
|---|---|---|
| jet increment smaller than modelled (+/-50 % on the increment) | TTV falls back to HMMC-R parity (28.0 / 31.1 K, still -19 / -30 % vs CoolIT); hot die +3-5 K | E1 coupon before tooling; HMMC comb as a drop-in fallback in the same block |
| erosion-corrosion at 1.5-3.1 m/s | wall loss at stagnation lines | velocity cap; E3; ENi wetted-path fallback |
| stagnation-line particle deposition (St 1-7) | +0.5-2 K drift | screen; dP/R trend monitoring; E3 |
| N1 bond / slot creep | maldistribution, unbonded ties | slot +10 um design, C-scan, flow signature, E4 |
| zoning accuracy in real packages | die gets < 85 % of flow, +5-15 K | per-zone flow test (E2), artwork trim loop |
| Split-Flow or unpublished Frore claims | injunction risk until 2028-31 | claim charts; trench fallback; expired-art shield |
| market access (Nvidia Group-A centralised Rubin buying) | no socket | enter through hyperscaler ASIC/ODM programmes, the JH-X retrofit, and Rubin Ultra / Kyber Group-B refresh |
| height 17.8 mm and mass 2.1 kg | 1U fit | LP15 (14.5 mm, +0.8 K) |

**Five experiments that retire the most risk:**

1. **E1, single-cell coupon** (months 1-3, ~US$50k). A heated 8 x 30 mm Cu coupon with 0.15/0.10 x 2.0 fins and swappable N1 foils (open slot, 0.22 jet, 0.18 jet, trench) in PCM-free PG25 at 45 C. Measure h_eff and dP against Vj from 0.5 to 3 m/s. Kill or confirm the +15-35 % increment.
2. **E2, full-plate flow distribution** (months 2-4). Water table plus CFD of the slot-to-fin turn, with per-zone flow metering of the zoned artwork. Target global max/min <= 1.10 at 9, 18 and 36 LPM.
3. **E3, jet erosion and fouling loop** (months 2-8). Six coupons at 1.5 / 2.3 / 3.1 / 4.0 m/s in 60 C PG25 dosed to ISO 4406 18/16/13 plus Cu oxide, 3,000 h; profilometry, mass loss, h re-test.
4. **E4, bonded-stack mechanics** (months 3-7). Diffusion-bond N1/N2 to skived fins; C-scan tie fraction; burst >= 4.5 MPa; 1,000 power cycles; pressure cycling.
5. **E5, OCP-format 15 kW TTV and 350 W/cm2 real-package TTV** (months 6-10). Four zones, 8 TCs, 6 flow points, PCM and liquid metal, three plates plus an independent lab. Confirms the scorecard.

**Roadmap from October 2026:**

| months | phase | work |
|---|---|---|
| M0-3 | concept | E1, CFD, claim charts, provisionals, RFQs |
| M3-6 | alpha | 10 plates, laser-cut N1, job-shop furnace; E2 and E4 start; E3 running |
| M6-9 | beta | TTV and zoned versions; E5; OCP report |
| M9-12 | design freeze, DVT | full qualification matrix; customer samples |
| M12-15 | PVT | 1-5k/yr pilot line; hyperscaler and RVL qualification |
| M15-18 (Jan-Apr 2028) | release | qualified product; volume ramp 2H 2028, as Split-Flow expires |

## 11. Scorecard vs CoolIT 15 kW

15 kW, 18 LPM PG25, 45 C inlet, 117 cm2.

- **Conservative:** JH-R with PCM at the Monte-Carlo P90.
- **Nominal:** the median.
- **Stretch:** JH-R with liquid metal, with the JH-P liquid-metal value in brackets.

| metric | CoolIT 15 kW | conservative | nominal | stretch |
|---|---|---|---|---|
| average case-to-inlet dT | 34.4 K | <= 30.3 K (-12 %) | 26.9 K (-22 %) | 21.8 K (-37 %) [19.7 K, -43 %] |
| maximum case-to-inlet dT | 44.2 K | <= 33.4 K (-24 %) | 29.9 K (-32 %) | 23.9 K (-46 %) [21.8 K, -51 %] |
| T_case,max at 15 kW, 45 C inlet | 89.2 C | <= 78.4 C | 74.9 C | 68.9 C [66.8 C] |
| same-paste like-for-like avg / max | 34.4 / 44.2 K | <= 35.5 / 40.7 K (average not guaranteed) | 28.8 / 33.8 K | 25.2 / 30.2 K at equal pump power |
| unit resistance R'' (avg, incl. TIM) | 0.269 cm2K/W | <= 0.237 | 0.210 | 0.170 [0.154] |
| flow-driven hot spot (max - avg) | 8.8 K systematic (9.8 total) | <= 2.5 K | 1.5 K | 0.7 K |
| plate dP at 18 LPM, incl. screen | undisclosed (est. 22-25, band 17-42) | <= 8 kPa (MC P90 6.6) | 5.5 kPa | 4.0 kPa (20 mm ports) |
| plate dP at 36 LPM | - | <= 25 kPa | 21.7 kPa | 15.6 kPa |
| hydraulic pump power at 18 LPM | ~6.5-7.4 W | <= 2.4 W | 1.7 W | 1.2 W |
| Q capacity, T_case,max <= 85 C, 1.2 LPM/kW | ~13 kW | >= 19.4 kW | 22.9 kW | 32.3 kW [39.1 kW] |
| flow for CoolIT's 34.4 K average | 18 LPM | <= 11.7 LPM (paste) | 10.5 LPM (0.70 LPM/kW, 0.34 W) | 8.2 LPM (LM) |
| inlet allowed for T_case,max 85 C at 15 kW | ~40.8 C | >= 51.2 C | 55.1 C | 61.1 C [63.2 C] |
| equal pumping power (6.5 W) avg / max | 34.4 / 44.2 K | <= 25.2 / 30.2 K (paste) | 23.2 / 26.2 K | 18.1 / 20.2 K |
| 350 W/cm2 reticle die T_case,max (zoned) | ~134 C (paste, 2-D) | 102 C (PCM, 6 mm) | 88.0 C (LM, 6 mm) | 84.5 C (LM, 4 mm, 0.8 mm base) [80.3 C]; direct-to-die ~-28 K at Tj |
| across-die case gradient at 350 W/cm2 | 22-30 K | <= 10 K | 6-8 K | ~6 K |
| HBM Tj at 40 W/cm2 | 105 C | <= 91 C | 89 C | 82 C (indium pedestal) |
| filtration needed / screen-free option | 50 um nominal loop | 50 um abs plate screen | same | JH-X: no screen, 32.2 / 35.2 K (PCM) |
| relative fouling life (skived = 1.0, 10 y) | 1.0x | >= 0.6x | 1.0x | 2.3x (JH-X) |
| GPU-class 4 kW plate (50 x 50 mm, 6 LPM) | < 0.009 C/W (4 kW plate) | 0.0093 C/W (paste, does not win) | 0.0081 C/W (PCM) | 0.0062 C/W (LM) |
| plate height / mass (15 kW class) | undisclosed (skived split-flow est. 12-25 mm / 1.5-2.5 kg) | 17.8 mm / 2.3 kg | 17.8 mm / 2.1 kg | 14.5 mm LP15 (+0.8 K); no mass win claimed |
| factory cost at 100k/yr (15 kW / Rubin class) | n/d (GB200-class skived ~US$100; Rubin ASP ~US$400) | <= US$215 / 155 | US$180 / 128 | US$165 / 120 (1M/yr ~US$125 / 90) |
| disclosure | one flow point, no dP, unnamed paste | full OCP v1.0.0 report, 6-point dP curve, independent repeat | same | same |

**Claims to avoid externally:**

- any bare-jet h figure;
- any "jets beat manifold micro-channels" statement without the hot-spot qualifier;
- any velocity above 2 m/s until E3 passes;
- a like-for-like paste average win at P90;
- any 350 W/cm2 figure without zoning and liquid metal;
- any dP that omits the coupling class.

**Sources:**

- Evidence base (local): `physics/SYNTHESIS-physics.md`, fouling-filtration, hydraulic-detail, manifold-maldistribution, nonuniform-heatmap, base-stress-stiffness, tim-and-direct-to-die; `research/ip-landscape.md`, gap-splitflow-continuation-claims-fto, manufacturing-cost, gap-cost-volume-and-market-anchors, power-electronics, standards-reliability, gap-ocp-test-spec, competitors-advanced; `design/proposal-hmmc-elite.md`.
- JetCool and MIT patents: [US 12,432,878](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12432878), [Official Gazette entry](https://patentsgazette.uspto.gov/week39/OG/html/1538-5/US12432878-20250930.html), [US 11,594,470](https://patents.google.com/patent/US11594470), [MIT TLO](https://tlo.mit.edu/industry-entrepreneurs/available-technologies/modular-microjet-cooling-packaged-electronic), [US 10,651,112](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10651112), [JetCool assignee list](https://patents.justia.com/assignee/jetcool-technologies-inc?page=2), [US 12,100,643](https://patents.google.com/patent/US12100643).
- Frore: [LiquidJet announcement](https://www.froresystems.com/blog/frore-systems-introduces-liquidjet-tm-redefining-coldplates-for-ai-data-centers), [hwbusters report](https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/).
- Expired jet cold plate: [US 5,316,075](https://patents.google.com/patent/US5316075).
- Jet literature: [IBM distributed-return jets](https://research.ibm.com/publications/direct-liquid-jet-impingement-cooling-with-micronsized-nozzle-array-and-distributed-return-architecture), [Sung & Mudawar hybrid micro-channel/micro-jet](https://engineering.purdue.edu/mudawar/files/articles-all/2008/2008-03.pdf), Martin, Adv. Heat Transfer 13 (1977) 1-60, [Womac et al., J. Heat Transfer 116 (1994)](https://iifiir.org/en/fridoc/correlating-equations-for-impingement-cooling-of-small-heat-sources-100826).
- Copper erosion: [CoolIT erosion study](https://www.coolitsystems.com/resources/news/erosion-in-liquid-cooling-systems-investigating-velocity-dependent-degradation-mechanisms/), [copper velocity guidance](https://engineeringtoolbox.com/copper-pipes-water-velocities-d_1081.html).
