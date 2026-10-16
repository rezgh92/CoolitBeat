# PSM-12: a proven-subset manifold cold plate and a 12-month programme to beat the CoolIT 15 kW plate in public (key: risk-first-12mo)

Architecture proposal, 2026-10-14. Lens: programme risk. The question is which architecture and programme most reliably produce a public, OCP-format result that beats CoolIT's June 2026 numbers (34.4 K average and 44.2 K maximum case-to-inlet at 15 kW, 18 LPM PG25, 45 C inlet), with a published pressure drop, by **OCP Global Summit, 4-7 Oct 2027** (month 12), and that lead to a qualified product by month 18.

Numbers come from the unchanged project model (`docs/cooling/model/coldplate_model.py`) and the physics synthesis Monte Carlo (`physics/SYNTHESIS-physics.py`, 20k samples), both run with this geometry. Scripts and outputs: `appendix/design/risk/risk_run.py` (`risk_run.out`) and `risk_mc2.py` (`risk_mc2.out`). Treat each modelled term as +/-25 %.

---

## 1. Concept in one page

**What it is.** PSM-12 is an all-copper plate brazed in one vacuum cycle. It has four parts:

- a **skived fin core**: 0.15 mm fins, 0.15 mm gaps, 2.0 mm tall, on a base fly-cut to 1.0 mm;
- a **two-sided gang-slit distributor**: 3.0 x 9 mm plenums cut from the top, and 0.30 mm inlet and 0.60 mm outlet *window slits* cut from below through a 1.0 mm floor, at 4 mm spacing;
- a **stamped separator**;
- a **CNC centre header bar** carrying 16 mm ports and a 50 um absolute screen cartridge.

Each fluid parcel drops through an inlet slit, runs 4 mm along a fin channel and rises through the adjacent outlet slit. The continuous 0.30 mm slit is the flow meter, at about 1.6 kPa, so no extra orifice layer is needed. The floor lands between slits are brazed to 89 % of the fin-tip length. That turns the stack into a tied plate-fin pressure vessel, which is why a 1.0 mm base is safe.

**Why it beats CoolIT.** CoolIT's 34.4 K splits into four terms: caloric 6.3 K, paste 9 K, a 2 mm base 6.5 K and convection 12.6 K. Its flow path is 54 mm long, which forces 0.2 mm fins and produces a +8.8 K systematic hot spot at the outlet edge. PSM-12 changes three things:

- The 4 mm flow length makes fin friction negligible (0.28 kPa), so convection falls to 10.5 K and the ramp hot spot becomes about 1.5 K.
- The tied 1 mm base halves the base term to 3.3 K.
- The stiff, bow-free stack holds a phase-change pad (PCM) at its datasheet value.

Result with PCM, the expected OCP reference TIM: **28.4 K average / 31.4 K maximum at 5.6 kPa port-to-port**. With CoolIT's paste class it is 30.4 / 35.4 K.

**Why this is the low-risk choice.** Every kept feature already exists in volume production or in expired literature. Only one feature is a development item: the 1.0 mm tied base, which is gated at month 3 with two pre-modelled fallbacks.

The win does not hinge on any single novel element:

- Even the worst fallback (2.0 mm base, ±20 % flow maldistribution) beats CoolIT with PCM: 31.7 / 35.5 K at 5.6 kPa, P(beats both) = 0.85.
- In the Monte Carlo the PCM headline beats CoolIT on both average and maximum in **98 %** of samples, and is "decisive" (average ≤ 31 K and maximum ≤ 35.4 K) in **84 %**.

**Five decisive differentiators**

1. **4 mm flow length from window slits** over a skived field. This is the expired Harpole/Cooligy manifold-microchannel concept built with incumbent tools. It gives a 4x lower dP than the reconstructed benchmark and a 3x smaller flow-driven hot spot.
2. **Tied sandwich, 1.0 mm base, 89 % fin-tip bond.** Pressure bow is zero and mount plus thermal bow is about 3x lower. The base term is 3.3 K.
3. **Metering is an inertial slit, so uniformity does not degrade with flow.** The along-slot ratio is 20 (rule ≥ 15) and the slot-to-slot ratio is 8.8 (rule ≥ 6).
4. **Fouling is engineered, not assumed.** The smallest passage, 0.15 mm, is 3x the screen rating. The 0.30 mm slit is 6x. There is an integrated 50 um absolute screen and bleeds at the plenum dead-ends.
5. **Transparency as a weapon.** We publish the full OCP v1.0.0 report: 6-point R and dP curves, dP at three boundaries, 3 plates x 3 assemblies, k = 2 uncertainty, an on-rig proxy of the benchmark, and a named independent-lab repeat. CoolIT published one flow point and no dP.

**Feature triage: what is kept, and what goes to the roadmap**

| HMMC feature | Maturity evidence | Decision |
|---|---|---|
| Skived Cu fins 0.15/0.15 x 2.0 mm (aspect ratio 13) | GB200 norm ≤ 0.5 mm fins; 0.06/0.10 mm demonstrated | **keep**; 0.10 mm-fin variant (RF-10) built in the same lots as a hedge |
| 4 mm flow length, alternating slits | expired Harpole US 5,088,005 and Cooligy US 6,986,382; incumbent split-flow plates are the one-slit case | **keep** |
| Window-slit metering 0.30 mm | machined slit; meets the L2 ≥ 0.3 mm fouling rule | **keep** (it replaces the orifice comb) |
| Orifice comb + galleries (about 1,300 laser holes) | modelled, not built | drop to Rev B fallback |
| Etched laminate; diffusion bonding | furnace-limited; fin creep risk under bond pressure at 850-950 C (our assessment) | Gen-2 cost-down |
| One-cycle vacuum braze (BAg-8 / Ag-Cu) | commercial vacuum-brazed cold plates (Mersen Aquamax, Wakefield) | **keep**: shortest qualification |
| 1.0 mm tied base | analysed, not built | **keep, gated at M3** (F1 1.5 mm, F2 2.0 mm) |
| 0.10 mm channel core | needs ≤ 33 um loop filtration | roadmap (filtration-gated SKU) |
| Heat-proportional zoning, HBM pedestal | modelled | designed in; TTV-B stretch data in-year |
| PCM TIM | commercial (PTM7950 class), OCP reference interface | **headline** |
| Liquid metal (LM) TIM | no 100 cm2 cycling data | labelled stretch data only |
| Low-profile in-plane headers, direct-to-die | modelled | Rev C / roadmap |
| Two-phase, counter-flow, AM cores | rejected by physics synthesis | no |

---

## 2. Thermal core

| Element | Specification | Rationale |
|---|---|---|
| Material | OFE Cu C10100/C10200 throughout; wetted path bare Cu with Ag-Cu braze fillets | k 390 W/mK; no H2 embrittlement; no Al, Zn or Ni in the loop |
| Fin field | 108 x 108 mm (TTV), fins along x, t 0.15 / gap 0.15 / pitch 0.30 / H 2.0 mm, 360 channels | h 13.3 kW/m2K, eta 0.65, h_eff 122 kW/m2K; aspect ratio 13 sits squarely in the commercial skiving window |
| Base | skived on a 2.5 mm blank, fly-cut after braze to 1.0 ± 0.1 mm (0.8 mm minimum under a die); perimeter land 1.8 mm, ≤ 4 mm unsupported | 3.3 K at 128 W/cm2; thinner is always better for the maximum |
| Flow path | inlet plenum → 0.30 mm slit → fin gaps → 4 mm along x (3.55 mm under the land) → 0.60 mm outlet slit → outlet plenum; 14 inlet + 14 outlet slits at 8 mm inlet pitch; 10,080 parallel 4 mm segments | channel velocity u 0.099 m/s, Re 22; isothermal cell, NTU 1.20 → caloric 0.60 x 12.7 = 7.6 K |
| Ripple | 8 mm period through 3 mm of Cu plus fins | < 0.7 K peak-to-peak at the case |
| Zoning (package SKUs) | die zone: 8 mm slit pitch, 0.30-0.45 mm slits; HBM columns: 16 mm pitch, 0.30 mm; unheated area: no slits. Die block takes ≥ 85-90 % of flow | heat-proportional zoning is worth 15 K at a 350 W/cm2 die; slit widths stay ≥ 0.30 mm for fouling |

**Nominal term budget (PCM):** caloric 7.6 + TIM 7.1 + base 3.3 + convection 10.5 = **28.4 K**. The hot spot adds flow maldistribution (±10 % long-wave) 1.5 K plus PCM scatter 1.5 K, giving **31.4 K**.

**Interface by tier**

| Tier | Package | Interface | R'' (cm2K/W) | Load |
|---|---|---|---|---|
| Demo headline / Tier 1 drop-in | flat TTV face; lidded B300, MI355X, Rubin | PCM pad (PTM7950 class); flatness ≤ 20 um, Ra ≤ 0.8 um | 0.055 (P90 0.08) | run at **15 psi (1.2 kN)**, within module-class loads; a second point at 25 psi |
| Like-for-like | as CoolIT | named grease (Shin-Etsu X23-7921-5 class), bond line (BLT) measured after test | 0.05-0.07 | same |
| Tier 2 OEM (stretch data) | Ni-finished lid | Ga-In-Sn LM, dam, 20-30 um BLT, 3-5 um electrolytic Ni on the contact face only | 0.015 | 10-20 psi |
| Tier 3 (roadmap) | bare die | stepped pedestal + LM | lid and TIM1 removed | ≤ 0.3 MPa on the die |

---

## 3. Hydraulic architecture

| Level | Feature | Size | Velocity at 18 LPM | dP at 18 LPM (kPa) | dP at 36 LPM (kPa) |
|---|---|---|---|---:|---:|
| L0 ports | 2 x 16 mm bore, vertical, in the centre bar | 16 mm | 1.49 m/s | 2.57 | 10.3 |
| Screen | 50 um absolute pleated 316L cartridge in the inlet boss, ≥ 12 cm2, serviceable | - | - | 0.40 clean (alarm at 1.2) | 1.6 |
| L1 headers | inlet 20 x 10 mm, outlet 24 x 12 mm, side by side on the centre line, mid-fed (9 LPM per half) | 200 / 288 mm2 | 0.75 / 0.52 m/s | 0.32 | 1.3 |
| L2 plenums | 28 plenums, 3.0 x 9 x 108 mm, 1.0 mm walls, fed/drained via separator windows at ±14 mm from centre | 27 mm2 | ≤ 0.50 m/s (long half) | < 0.05 | 0.2 |
| L3 meter | 0.30 mm inlet slit / 0.60 mm outlet slit through the 1.0 mm floor | - | slit 0.66; fin-gap entry 1.32 m/s | 1.6 + 0.4 | 8.0 |
| Channels | 0.15 x 2.0 x 4 mm | - | 0.099 m/s | 0.28 | 0.6 |
| **Plate, port-to-port** | | | | **5.6** (MC P90 7.2) | **~22** |

**Uniformity.** The branch is 2.48 kPa and 89 % inertial.

- Along each slot: branch / plenum dynamic head = 20 (rule ≥ 15 for centre-fed slots).
- Slot to slot: branch / header dynamic head = 8.8 (rule ≥ 6).

This is design-H class, so we expect global max/min ≤ 1.10 and a long-wave hot-spot term of 1.3-1.5 K. Because the meter is inertial, the ratios hold at 2x flow. Machining tolerance on the 0.30 mm slit (±0.02 mm) gives about ±7 % short-wave variation, which the 1 mm base smooths to ≤ 0.3 K. Uniformity is measured in Experiment 2 before any claim is made.

**Pressure-drop budget.** At 18 LPM the plate is 5.6 kPa and pumping power is 1.7 W. CoolIT-like plates are about 22-25 kPa (band 17-42) at about 6.5-7.4 W. At 36 LPM the plate is about 22 kPa and 13 W, against about 58-69 kPa for the CoolIT-like plate.

Rated flow is declared as 1.0 LPM/kW (15 LPM). Continuous operation is rated to 27 LPM, where the fin-entry jet reaches 2.0 m/s. The 36 LPM point is characterisation only.

**Couplings.** A UQD08 pair adds about 20-35 kPa at 18 LPM (Cv estimate, ±50 %) and dominates the loop. The tray loop (plate + 12 mm stubs + UQD08 pair) is about 45 kPa (40-65). We publish three dP boundaries:

1. port-to-port with the bore stated;
2. plate plus 1/2-in barbs and 0.5 m hose, as in CoolIT's TTV photograph;
3. plate plus a named UQD08 pair.

**Filtration and fouling.**

- Every upstream passage is more than 2x the next: 16 > 10 > 3.0 > 0.30 > 0.15 mm.
- The 0.15 mm channel is 3x the 50 um absolute screen (no bridging); the slit is 6x (no deposition mechanism).
- Each inlet-plenum dead-end has a 0.6 mm bleed to the outlet side (about 4 % of flow, +0.3-0.4 K).
- On package SKUs, plenum ends and port-adjacent slits sit outside the die.
- Channels run at 0.1 m/s, so there is no shear self-cleaning and the screen is non-negotiable.
- dP taps on the bar; reverse-flow tolerant; factory flush to ISO 16232, < 0.1 mg residue.
- There is one open fouling risk: impaction of particles of 25 um or larger on fin tips under the 1.3 m/s slit jet (Stokes number 1.5-6). Experiment 4 tests it. The fallback is Rev B: 0.6 mm slits plus a per-plenum selector orifice.

---

## 4. Mechanical and construction

| Part | Process | Thickness | Mass |
|---|---|---|---|
| Base + fins | skived OFE C10100, 125 x 125 mm outline | 1.0 + 2.0 mm | 0.27 kg |
| Distributor | 10 mm OFE plate; plenums gang-slit from the top; slits gang-slit from below (0.30 / 0.60 mm saws); ears, bleeds | 10 mm | 0.67 kg |
| Separator | 1.5 mm OFE, stamped (laser-cut below 20k/yr), 28 feed windows | 1.5 mm | 0.21 kg |
| Header bar | CNC from a 64 x 125 x 15 mm bar (forged near-net at 1M/yr); ports, screen boss, dP taps | 15 mm | 0.53 kg |
| Stubs, screen, springs, backplate | 316L / steel | - | 0.15 kg |
| **Total** | | **14.5 mm plate, 29.5 mm at the bar** | **~1.8 kg** |

**Joining: one vacuum-braze cycle**, the incumbent cold-plate join. Furnace capacity is abundant, failure modes are known and the inspection toolkit exists (C-SAM, He leak). The cycle makes three interfaces: fin tips to floor lands (the structural ties), plenum walls and frame to the separator, and separator to the header bar.

Two filler routes are qualified in parallel in Experiment 1:

- (A) laser-cut 25 um BAg-8 foil preforms matching the land pattern;
- (B) 5 um Ag electroplate on the land faces, forming the Ag-Cu eutectic at about 790 C. This limits the liquid volume and therefore wicking into 0.15 mm gaps.

Friction-stir or laser welding cannot tie fin tips, so they serve only as an optional perimeter seam later. Diffusion bonding is Gen-2.

**Base thickness logic.** With 89 % of the fin-tip length bonded, tie stress = p x pitch / (t_fin x bonded fraction):

| Pressure | Nominal tie stress | With Kt 2.5 |
|---|---:|---:|
| MAWP 0.69 MPa | 1.6 MPa | - |
| design burst 2.0 MPa | 4.5 MPa | - |
| sample burst test 4.5 MPa | 10.1 MPa | 25 MPa |

All are below the 70 MPa yield of annealed Cu; braze strength is 100-200 MPa.

- Floor cantilevers beside the slits: 25 MPa at 4.5 MPa test pressure.
- Separator over a 3.0 mm plenum: 9 MPa.
- Pressure bow is zero; mount bow is 4-25 um and thermal bow 6 um over a 50 mm die.
- In-plane thermal fatigue amplitude is 11 MPa (SF ~6), covered by 1,000 power cycles.
- Risk-relevant property: an unbonded patch is tolerated up to about 12 mm at 1.0 mm base, about 18 mm at 1.5 mm and 25 mm at 2.0 mm (1.5 MPa, yield). That is the logic of fallbacks F1 and F2.

**Flatness and mounting.** The die face is fly-cut after braze to ≤ 20 um over the heated area, Ra ≤ 0.8 um; this also removes braze distortion. Eight spring-loaded captive screws act on the ears, with bearing points moved toward the heated area.

**Pressure ratings.** MAWP 0.69 MPa (100 psi); proof 1.03 MPa for 30 min on 100 % of parts; design burst ≥ 2.0 MPa (the OCP example is > 20 bar); sample burst ≥ 4.5 MPa; He leak ≤ 1e-6 mbar-L/s (OCP: 1e-5); vacuum-stable to -0.9 bar(g).

---

## 5. Manufacturing route at volume

| # | Step | Process class / supplier type | Key tolerance |
|---|---|---|---|
| 1 | OFE blanks, sheared | copper mill / stamping | ±0.05 mm |
| 2 | Skive fin field, 3-4 min | skiving house (Wieland / Nakamura / Winshare class) | fin t ±0.015, pitch ±0.01, H ±0.1 mm |
| 3 | Fly-cut fin tips to a plane; outline mill; clean | CNC | tip plane ±20 um |
| 4 | Distributor: gang-slit plenums from the top, flip, gang-slit slits from below; frame, ears, bleeds | horizontal mill with gang arbor | slit 0.30 ± 0.02, land plane ±20 um |
| 5 | Separator stamped; header bar CNC (forged at 1M/yr) | stamping house; CNC | ±0.05 / ±0.1 mm |
| 6 | Filler: foil preforms or Ag plate; deoxidise | plating line | 5 ± 1 um |
| 7 | Fixture stack (0.1-0.2 MPa), vacuum braze about 790 C, 100-300 plates per load | vacuum-braze house | - |
| 8 | Fly-cut die face to the 1.0 mm base, ≤ 20 um flatness; Tier 2 masked Ni | CNC / plating | 15-20 um |
| 9 | Flush and count; fit screen; 100 % He leak, proof, 3-point dP vs flow (catches slit cross-leaks and blockage); per lot: C-SAM, burst, thermal | test cell | - |

**Factory cost** (US$, 15 kW-class 125 mm plate, ±25 %, basis: manufacturing-cost process rates, Cu US$10-12/kg; RFQs in month 1):

| Element | 10k/yr | 100k/yr |
|---|---:|---:|
| Copper (about 3.0 kg blanks, 1.7 kg finished, swarf credit) | 30 | 26 |
| Skived core + trim | 40 | 25 |
| Distributor (two-sided gang slitting) | 30 | 15 |
| Separator | 8 | 3 |
| Header bar | 30 | 14 |
| Stubs + screen cartridge | 18 | 12 |
| Filler + braze cycle | 23 | 14 |
| Post-braze fly-cut | 8 | 5 |
| Hardware | 20 | 14 |
| Test | 10 | 6 |
| Yield loss / overhead | 18 | 14 |
| **Total** | **~235** | **~148** |

The incumbent skived split-flow plate is about US$170 at 10k and US$105 at 100k. Our premium is about US$43 at 100k, but **cost per kW of Tcase-limited capacity is 17 % lower** (US$148 / 21.1 kW = 7.0 $/kW against US$105 / 12.7 kW = 8.3 $/kW). This fits inside the US$300-400 ASP window.

**Lead time.**

- Prototype parts: 3-4 weeks.
- Skived cores: 2-4 weeks at a skiving house. Backup: single-saw micro-slitting in-house, about 4 h per core, for the first 3-5 plates.
- Braze slots: 2-3 weeks.
- First plates: week 8-10.
- Volume tooling: stamping die 10-12 weeks, braze fixtures 4 weeks.
- Capacity: 2-3 skiving machines per 100k/yr (US$2-4 M, same as the incumbent route).
- No proprietary process, so any Taiwanese or Vietnamese skive-and-braze house can second-source.

**Yield risks:**

1. fin-tip voids or filler wicking (controlled by filler volume, C-SAM and the dP slope test);
2. slit-to-separator cross-leak (100 % dP test);
3. fly-cut breakthrough (in-line thickness gauging);
4. fin damage before braze (fixtures).

---

## 6. Predicted performance vs benchmark

### 6.1 Benchmark point: 15 kW, 18 LPM PG25, 45 C, 117 cm2 (128 W/cm2)

| Design | Cal | TIM | Base | Conv | **Avg dT** | **Max dT** | R'' | dP (kPa) | Pump (W) | Qcap (kW) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT measured | | | | | 34.4 | 44.2 | 0.27 | n/d | n/d | ~13 |
| CoolIT-like reconstruction (calibration) | 6.3 | 9.0 | 6.6 | 12.6 | 34.5 | 44.3 | 0.269 | 24.6 | 7.4 | 12.7 |
| PSM-12 RF-15, paste 0.07 (like-for-like) | 7.6 | 9.0 | 3.3 | 10.5 | **30.4** | **35.4** | 0.237 | 5.6 | 1.7 | 18.0 |
| PSM-12 RF-15, named paste at 25 um BLT, 0.05 | 7.6 | 6.4 | 3.3 | 10.5 | 27.8 | 32.8 | 0.217 | 5.6 | 1.7 | 20.3 |
| **PSM-12 RF-15, PCM (headline)** | 7.6 | 7.1 | 3.3 | 10.5 | **28.4** | **31.4** | 0.222 | **5.6** | **1.7** | **21.1** |
| PSM-12 RF-15, LM (stretch) | 7.6 | 1.9 | 3.3 | 10.5 | 23.3 | 25.4 | 0.182 | 5.6 | 1.7 | 28.9 |
| RF-10 hedge (fin 0.10), PCM | 7.6 | 7.1 | 3.3 | 10.1 | 28.0 | 31.1 | 0.219 | 5.5 | 1.7 | 21.6 |
| Fallback F1: base 1.5 mm, PCM | 7.6 | 7.1 | 4.9 | 10.5 | 30.1 | 33.1 | 0.235 | 5.6 | 1.7 | 19.6 |
| Fallback F2: base 2.0 mm, ±20 % flow, PCM | 7.6 | 7.1 | 6.6 | 10.5 | 31.7 | 35.5 | 0.247 | 5.6 | 1.7 | 17.8 |
| Upside U1: 3.0 mm fins, PCM | 7.7 | 7.1 | 3.3 | 9.6 | 27.6 | 30.6 | 0.215 | 5.5 | 1.6 | 22.1 |

**Win probabilities** (physics Monte Carlo, 20k samples; model uncertainty only):

| Case | Avg P10/P50/P90 (K) | Max P10/P50/P90 (K) | P(avg < 34.4) | P(max < 44.2) | P(decisive: avg ≤ 31 and max ≤ 35.4) |
|---|---|---|---:|---:|---:|
| Paste, uncontrolled BLT | 26.4/30.5/37.5 | 31.4/35.6/42.6 | **0.79** | 0.93 | 0.47 |
| Paste, controlled and measured BLT | 27.1/29.2/31.7 | 31.1/33.3/35.9 | 0.99 | 1.00 | 0.81 |
| **PCM** | 26.1/28.5/31.9 | 29.1/31.6/35.0 | **0.98** | **1.00** | **0.84** |
| PCM, ±20 % flow | 26.1/28.5/31.9 | 29.8/32.5/35.9 | 0.98 | 1.00 | 0.83 |
| F1 base 1.5 mm, PCM | 27.7/30.2/33.6 | 30.7/33.3/36.7 | 0.94 | 1.00 | 0.64 |
| F2 base 2.0 mm, PCM | 29.3/31.8/35.1 | 33.1/35.7/39.1 | 0.85 | 1.00 | 0.35 |

Two programme decisions follow.

1. **The headline is made with the OCP reference TIM.** The paste result is published anyway, but the paste average margin is only robust if the bond line is controlled and measured (Experiment 3).
2. **The TTV must not be smaller than CoolIT's.** At a 100 cm2 footprint ("hard mode", 150 W/cm2), P(avg win) falls to 0.81 with PCM and 0.52 with uncontrolled paste. We therefore build at 117 cm2, slightly *below* the 120 cm2 photogrammetry estimate, and publish R'' per area.

**Other measures at 15 kW**

| Measure | PSM-12 RF-15 | CoolIT-like |
|---|---|---|
| Flow sweep, PCM avg / max | 0.75 LPM/kW: 34.2 / 37.2 K; 1.0: 30.3 / 33.3 K (dP 3.9 kPa); 1.5: 26.6 / 29.6 K | 1.0 LPM/kW: 35.8 / 45.6 K (fails the Rubin-class ≤ 28-30 / 33-35 K budget) |
| Flow to match CoolIT's 34.4 K average | 11.1 LPM with PCM; 12.6 LPM with paste; 8.5 LPM with LM | 18 LPM |
| At 2x flow (36 LPM), PCM | 24.0 / 27.0 K at 21.8 kPa, 13 W | 31.0 / 40.8 K at about 58 kPa, 35 W |
| At equal pumping power (6.5 W = 28.7 LPM) | 25.1 / 28.1 K (PCM); 27.0 / 32.1 K (paste) | 34.5 / 44.3 K |
| Inlet temperature at which Tcase,max = 85 C | 53.6 C (PCM); 49.6 C (paste); 59.6 C (LM) | 40.7 C |
| Q capacity, Tcase,max ≤ 85 C | 21.1 kW (P10-P90 18.1-23.7) | ~13 kW |

### 6.2 Real 2027-28 package: 4 x 26 x 33 mm dies at 350 W/cm2 + 16 HBM, zoned, hottest die cell

| Plate | Paste 0.05 | PCM | LM |
|---|---|---|---|
| CoolIT-like split-flow | 88.6 K (134 C) | - | ~76 K (121 C) |
| PSM-12 RF-15 | 61.8 K (107 C) | 63.5 K (109 C) | **49.5 K (95 C)** |
| Performance core over the die zone only (0.10/0.10 x 1.5 mm, ≤ 33 um loops) | 51.7 K | 53.4 K | 39.4 K (84 C) |
| Direct-to-die (roadmap) | | | about 80 C |

**PSM-12 does not reach 85 C at 350 W/cm2**, even with LM. This is a 2029+ stress case, so it is roadmap material and not a 12-month claim. At realistic Rubin-class die flux the plate wins clearly (indicative 1-D die-zone results, 88 % of flow to the dies):

| Package | CoolIT-like avg / max | PSM-12 PCM avg / max | PSM-12 LM avg / max |
|---|---|---|---|
| Rubin-class, 2.3 kW on 16.6 cm2 of die | 33.9 / 43.6 K | 28.1 / 31.1 K | 23.1 / 25.2 K |
| Rubin-Ultra-class, 3.6 kW | 29.1 / 38.1 K | 25.0 / 27.7 K | - |

### 6.3 GPU-class plates (2-4 kW): where it does not win

On *uniform, low-flux* TTVs at 1.2 LPM/kW the isothermal-cell caloric penalty dominates, and **PSM-12 loses on average by 0.5-2 K**:

| Load / footprint | CoolIT-like avg | PSM-12 PCM avg | PSM-12 avg with LM |
|---|---:|---:|---:|
| 1.4 kW / 45 cm2 | 13.2 K | 15.3 K | 14.0 K |
| 2.3 kW / 60 cm2 | 14.8 K | 16.0 K | - |
| 3.6 kW / 80 cm2 | 16.3 K | 16.8 K | - |

It still wins on maximum dT (17.1 vs 20.4 K at 1.4 kW) and on dP. On die-concentrated packages it wins (B300-class: 21.4 / 23.8 K vs 23.9 / 32.3 K). Our GPU-class marketing must therefore lead with real-package and maximum-dT data.

**Other places it does not win:** body height (29.5 mm at the bar vs an estimated 22-28 mm), mass (about 1.8 kg vs an estimated 1.2-1.6 kg), filler-free construction (CoolIT's OMNI line is friction-stir welded), field track record, and fouling life (parity at best).

### 6.4 Claims we will and will not make (public, month 12)

**Will make (only if measured):**

- average, maximum and per-TC dT at 15 kW / 18 LPM PG25 / 45 C, with (a) the OCP reference TIM and (b) a named paste at a measured BLT; 3 plates x 3 assemblies, k = 2 uncertainty;
- R and R'' vs flow at 6 points from 0.5 to 1.5 LPM/kW;
- dP at ≥ 6 flows at three boundaries;
- pumping power and the flow needed to match 34.4 K;
- Q capacity measured to 18 kW (the heater limit) and extrapolated from the measured R beyond that;
- inlet headroom from a 35-53 C sweep;
- plate-to-plate spread and heat capture ≥ 98 %;
- proof, leak and sample burst; interim cycling results;
- an independent-lab repeat of the headline point;
- the on-rig benchmark proxy result.

**Will not make:**

- a 10-year life or fouling-parity claim (until Experiment 4 plus field data);
- anything that relies on channels below 0.15 mm;
- LM numbers presented as like-for-like;
- 350 W/cm2 or real-package claims before TTV-B is measured;
- "N kW per package" scalability (we state W/cm2 at R'', dT and LPM/kW instead);
- "no braze";
- CoolIT's dP stated as fact (we give ours plus the ≥ 15-20 kPa physics floor for single-split 0.2 mm plates);
- uniformity better than 10 % unless measured;
- "OCP certified" (we say "tested per OCP v1.0.0").

---

## 7. Product family and applications

Every family member uses the same core, braze route and test cell. They are sequenced by risk.

| SKU | Application | What changes | Timing |
|---|---|---|---|
| PSM-15 | demo vehicle; hyperscaler custom ASICs with large packages (bare die, 80 psi loops, buying on TCO) | none | M12 demo, M18 qualified |
| PSM-R | Rubin-class lidded, 100 x 100 mm, 2-4 kW | zoned slit pitch, 10-12 mm ports, PCM (Tier 1) or LM (Tier 2); licence or contract-manufacture via a Group-A or Western CM | M15-24 |
| PSM-RU | Rubin Ultra (120 x 150 mm, 3.6 kW) | stepped HBM pedestal machined into the fly-cut face; LM; micro-channel-lid co-design with a lid maker | 2028 |
| PSM-S | CPU / NVSwitch / CPO switch ASICs | small plates at low flux: average parity, sold on dP (series loops) and laser-zone uniformity | opportunistic |
| PSM-W | wafer-scale / multi-chip | tile the plenums; flow length stays 4 mm at any size; ports and headers scale | on demand |
| PSM-P | 800 VDC power shelves, in-rack SiC/GaN (5-30 W/cm2) | 0.3-0.5 mm channels (no fine-fin need at low flux), same braze line, plate dP ≤ 20 kPa so GPU plates are not starved; US$50-150 | 2028 |
| EV SiC traction | WEG 50/50 at 65 C, Al loops, AQG 324 | Al controlled-atmosphere-braze version with ≥ 0.3-0.5 mm channels; **licence only** | licence |
| SST / medium-voltage SiC; laser / RF GaN | DI water | 0.15 mm allowed behind DI polishing filters; premium niche | 2028+ |

---

## 8. Reliability, qualification and drop-in compatibility

### 8.1 Demonstration TTV and protocol (the month-12 deliverable)

**TTV-A (parity).**

- Heaters: 4 AlN thick-film tiles, 53 x 53 mm on a 54 mm pitch (2 x 2, about 117 cm2), contact face lapped to ≤ 10 um. Watlow ULTRAMIC is rated to 155 W/cm2, so 15 kW runs at 83 % of rating; tiles come from two suppliers (Watlow and Durex/Oasis classes).
- Sensors: 8 TCs mirrored to CoolIT's 2-per-heater layout (centre-of-heater and outlet-side positions) plus 4 extra (geometric centre and three corners). Type T, 36 AWG, calibrated to ±0.2 K, in 0.4 mm diamond-ground grooves in the heater face, with bead depth published. AlN gives a small, published bias (+0.5 K).
- Power: per-heater DC power metered to ±0.3 %.
- Heat capture: guard heaters and insulation for ≥ 98 % capture, with calorimetric closure ≤ 3 %.
- Spares and high-load variant: two TTVs. A Cu-block cartridge variant (TTV-A2) runs Q-capacity points to 25 kW.

**Rig.** A 25 kW PG25 loop (25.0 ± 0.5 wt %, checked by refractometer), Coriolis flowmeter (±0.2 %), 45 ± 0.2 C inlet, differential pressure taps at the three boundaries.

**Matrix.**

| Variable | Levels |
|---|---|
| Power | 5 / 10 / 15 / 18 kW |
| Flow | 0.5 / 0.75 / 1.0 / 1.2 / 1.5 LPM/kW (thermal); dP at 25-150 % of the 15 LPM rated flow (≥ 6 points) plus 36 LPM |
| Inlet | 35 / 45 / 50 / 53 C |
| TIM | OCP reference (PCM) at 15 and 25 psi; named paste with post-test BLT; LM (stretch) |
| Samples | 3 plates x 3 re-mounts |

**Benchmark proxy and calibration.** An **edge-fed single-pass skived reference plate** (0.2/0.2 x 4 mm fins, 2 mm base, paste; it has no central slot and does not practise Split-Flow) is predicted at **34.5 K average**, the same as CoolIT. It is our on-rig proxy for the benchmark. Purchased incumbent GPU plates calibrate a small TTV-G; first-sale exhaustion permits testing them.

**Additional tests.**

- Flow uniformity: Experiment 2 rig plus the in-situ 12-TC signature.
- Fouling: Experiment 4.
- TTV-B (4 die heaters at 300-350 W/cm2 + 16 HBM heaters 0.4 mm lower): built M6-10; stretch data at M12.

### 8.2 Requirements and qualification plan

| Requirement | Target | By M12 | By M18 |
|---|---|---|---|
| OCP v1.0.0 thermal + dP report | full | yes | yes |
| MAWP / proof / burst | 100 psi / 150 psi / ≥ 20 bar design, ≥ 45 bar sample | proof 100 %, 3 bursts | lot sampling |
| He leak | ≤ 1e-6 mbar-L/s, 100 % of parts | yes | yes |
| Thermal cycling | 1,000 cycles at 10-65 C operating, 50 at -40/+70 C storage; R drift ≤ 5 %, dP ≤ 10 % | 500 interim | complete |
| Pressure cycling | 10,000 cycles, 0 to MAWP | complete | - |
| Power cycling | 1,000 cycles at ΔT 40 K | complete | - |
| PG25 soak | 3,000 h at 65 C with coupons; dP drift ≤ 10 %; dissolved Cu tracked | 2,000 h | complete |
| Particulate challenge | Experiment 4, 1,000 h | complete | field pilot |
| Shock / vibration, cleanliness | per hyperscaler statement of work | - | yes |
| Quality | PFMEA, control plan, CpK ≥ 1.33 on leak and dP, PPAP | draft | yes |

**Wetted materials:** OFE Cu, Ag-Cu braze fillets (declared), 316L stubs and screen, peroxide-cured EPDM at the fittings only. No Al, Zn, NBR or silicone. An EN-plated variant is skived with a 0.16 mm gap so it still has 0.15 mm after 5 um of plating.

**Leak-before-break.** Annealed ductile Cu is tied everywhere and burst/MAWP is ≥ 3. A crack in the 1.5 mm separator or a bar wall weeps detectably long before rupture. The plate is vacuum-stable for negative-pressure loops.

**Drop-in.** The plate keeps ≥ 50 % of the tray dP budget for the UQD pair. It uses 1/2-in class stubs (UQD08/UQDB08), mounts at 0.6-1.2 kN spring load, and its outlet temperature is 57.7 C at 15 kW (within the ASHRAE W45 and ≤ 65 C return envelope). **Design life** is 7 years at 65 C outlet. A 10-year claim waits for data.

---

## 9. IP posture

**What we avoid.** CoolIT's Split-Flow family (US 8,746,330 / 9,603,284 / 12,495,513 and CIP branches) expires between Aug 2028 and about mid-2031. A multi-slot design is *not* a design-around on its own, because "comprising an inlet opening" also reads on several openings. Designed-in differences:

- all outlets are interior (no collection at the fin-field ends);
- distribution sits in a separate distributor layer;
- zones are separated by solid ribs;
- optionally, fins are segmented under the outlet slits (gang saw, about +0.2 K), decided after the claim chart.

Also avoided:

- the compliant-member family (US 11,725,886 / 12,188,733): we use a rigid base and no spring pedestals;
- microjet arrays: our slit feeds a fin field, not a jet onto the die;
- two-phase and in-silicon families;
- NVIDIA's AlN-heater TTV patent (US 12,446,195): our TTV is internal test equipment built from commercial heaters, and claims are checked in month 1.

**What we build on (expired).** Harpole US 5,088,005 (manifold microchannel); Cooligy US 6,986,382 (interwoven manifolds), 7,156,159 (multi-level), 7,104,312 (hot-spot delivery) and 7,000,684 (vertical feed); IBM TCM US 3,993,123. A dated memo maps each feature to these figures and serves as an invalidity shield.

**What we can claim (provisionals before any disclosure, then PCT):**

1. a window-slit-metered tied sandwich, with ≥ 80 % land bond and a ≤ 1.0 mm base, made in one braze cycle;
2. a two-sided gang-slit distributor process;
3. an integrated screen with a dP signature plus dead-end bleeds;
4. zoning by slit pitch and width;
5. the benchmark-proxy test method (defensive publication).

**Cost and timing.** FTO steps 1-3 (continuity and claims) in month 1 for about US$10k. A claim chart plus opinion for US$25-60k before any US sale. The demo is not a sale, and US volume (≥ M18, mid-2028) lines up with the expiry window.

---

## 10. Risks, experiments, roadmap, staffing

### 10.1 What could make us miss, and the fallback

| # | Miss mode | Probability | Early warning | Fallback (pre-modelled) |
|---|---|---|---|---|
| 1 | Fin-tip braze voids or wicking (ties fail, channels blocked) | medium | Experiment 1 C-SAM < 80 % bonded, flow test, burst < 4.5 MPa at M3 | Filler route B. Then **F1** (1.5 mm base; PCM 30.1 / 33.1 K, P(win) 0.94). Then **F2** (2.0 mm; 31.7 / 35.5 K, P 0.85). Or diffusion bond at a heat-exchanger house (+8 weeks). Thermal demo plates need only the 100 psi proof, so the burst qualification decouples from the demo |
| 2 | Paste like-for-like average loses (P 0.21 with uncontrolled BLT) | medium | M5 D5470 and BLT data | Controlled BLT (P 0.99). Lead with the OCP TIM; publish the paste result regardless (maximum and dP still win) |
| 3 | Benchmark ambiguity (footprint 100-145 cm2, "case" definition, TC bias) is used against us | medium | reviewer feedback | 117 cm2 TTV, AlN bias published, R'' per area, the on-rig proxy, offer to test any CoolIT plate on our rig |
| 4 | Flow maldistribution worse than ±15 % | low-medium | Experiment 2 at M3 | Rev B: per-slit width grading, or the orifice comb (+1 layer, 4 weeks); costs ≤ 1 K on the maximum |
| 5 | Thermal shortfall (h_eff -25 %) | low | first TTV data at M5 | U1 3.0 mm fins (-0.8 K); RF-10 cores already in the lot (-0.4 K) |
| 6 | TTV heater cracking or bias at 128-155 W/cm2 | medium | commissioning at M3-4 | two suppliers, spares, Cu-block TTV-A2 |
| 7 | Supplier lead times (AI-boom skiving and braze capacity) | medium | RFQ responses at M1 | two skiving houses + two braze houses; in-house micro-slit cores |
| 8 | CoolIT publishes a better plate or OCP data first | medium | market | the LM stretch is held in reserve; lead with the dP curve, per-area R'' and the independent repeat |
| 9 | Fouling impaction at the slit (product risk, not demo risk) | low-medium | Experiment 4 | Rev B (0.6 mm slits + selector orifice); no life claim until data |
| 10 | Claim chart finds a read on '513 | low | M2-4 | fin segmentation, the expiry-aligned launch, invalidity memo |

Overall (judgement): about **0.7** probability of the decisive result on schedule at M12, and about **0.9** of "beats CoolIT on average, maximum and published dP" by M12 using the fallbacks. The dominant failure mode is a 1-3 month slip (TTV or braze), not a thermal miss.

### 10.2 The five experiments that retire the most risk

| # | Experiment | When | Cost | Pass criterion | Retires |
|---|---|---|---:|---|---|
| E1 | Braze-tie coupon matrix: 60 x 60 mm, RF-15 / RF-10 x filler A / B x 2 fixture loads (24 coupons + 2 full plates); C-SAM, CT, flow test, pull, burst, fly-cut flatness | M0.5-3 | US$60k | bonded ≥ 80 % of land (≥ 50 % in any 10 mm cell); ≤ 2 % of channels blocked; burst ≥ 4.5 MPa; flatness ≤ 20 um | risk 1; base thickness |
| E2 | Full-scale flow rig: transparent plenum/header replica on a machined Cu slit floor; 28 plenum taps + dye; 9 / 18 / 27 / 36 LPM | M1-3 | US$60k | global max/min ≤ 1.15 at 18 LPM and ≤ 1.20 at 27 LPM | risk 4 |
| E3 | Rig calibration + TIM metrology: TTV-A commissioning, edge-fed proxy, purchased plates; ASTM D5470 of PCM / paste / LM at 15 and 25 psi; BLT control | M2-5 | US$120k | proxy within ±3 K of 34.5 K; re-mount repeat ≤ 1 K; heat capture ≥ 98 % | risks 2, 3, 6 |
| E4 | Accelerated fouling: quarter-scale plate behind the 50 um screen; PG25 dosed with ISO 12103-1 dust + Cu oxide + EPDM at 10-100x loop levels; 1,000 h at 65 C; clustered-blockage probe at plenum ends | M4-10 | US$90k | core dP drift ≤ 10 %; average dT drift ≤ 1 K; no clustered blockage; screen loading curve | risk 9; life claim |
| E5 | Thermo-mechanical endurance on first articles: 1,000 power cycles + 10,000 pressure cycles + 2,000 h soak, then burst | M5-11 | US$150k | R drift ≤ 5 %, dP ≤ 10 %, He-tight; burst ≥ 4.5 MPa after cycling | the 1 mm base; qualification |

### 10.3 Roadmap and gates (M0 = Nov 2026)

| Months | Work | Gate |
|---|---|---|
| 0-1 | RFQs (skiving x2, braze x2, CNC, stamping); long-lead orders (chiller, Coriolis, heaters); FTO steps 1-3; provisionals drafted | - |
| 1-3 | E1, E2; CFD of slit and plenum; detailed design | **G1 (M3): Rev A freeze**: base 1.0 / F1, slit widths, RF-15 vs RF-10 |
| 3-5 | Build A (12 plates); TTV-A commissioning; E3; E4 starts | - |
| 5-6 | Internal parity: 3 plates x 3 assemblies, all TIMs | **G2 (M6)**: commit publicly only if PCM avg ≤ 31 K and max ≤ 35.4 K measured |
| 6-9 | Build B (20 plates, production-intent braze house); E5; independent-lab repeat booked (ORNL or university class); TTV-B build | **G3 (M9)**: repeat within ±1.5 K |
| 9-12 | OCP-format report and white paper; TTV-B stretch data; provisionals converted | **G4 (M11-12)**: public at OCP Global Summit, 4-7 Oct 2027 |
| 12-18 | Build C pilot (150 plates at a CM); full qualification matrix; PPAP; samples to two hyperscaler ASIC programmes and one Group-A/CM licensee; FTO opinion | **G5 (M18)**: qualified product; Rev C low-profile and PSM-R zoned variants sampled |

### 10.4 Staffing and cost envelope

| Role | FTE |
|---|---:|
| Programme lead / chief engineer | 1 |
| Thermal-fluids (model, CFD, correlation) | 2 |
| Mechanical design / FEA | 2 |
| Manufacturing and supplier engineering (skive, braze, CNC) | 2 |
| Test lab lead + 2 technicians | 3 |
| Reliability / materials / fouling | 1.5 |
| Quality (PFMEA, metrology) | 1 |
| Applications / OCP / customers | 1 |
| IP coordination + programme admin (external counsel extra) | 0.5 |
| **Total** | **14** |

| 12-month budget item | US$ M |
|---|---:|
| Labour (14 FTE, US$230k loaded) | 3.2 |
| 25 kW test stand (chiller, PG25 loop, Coriolis, dP, 25 kW DC supplies, DAQ, guard heaters) | 0.45 |
| TTVs (2 x A, A2, B, G) | 0.25 |
| Flow rig + fouling rig | 0.14 |
| Prototypes (about 80 plates in 3 builds) + coupons | 0.30 |
| Reliability testing (chambers or outsourced) | 0.25 |
| Independent-lab repeat | 0.15 |
| FTO, claim chart, provisionals | 0.20 |
| CFD licences / compute, reference plates, OCP travel | 0.16 |
| Contingency (20 %) | 1.0 |
| **Total, 12 months** | **~6.1 (range 5-7)** |

Months 12-18 add US$2.5-3.5 M (tooling, pilot run, PPAP, qualification), for an **18-month total of US$8.5-10 M**.

---

## 11. Scorecard vs CoolIT 15 kW

Conditions: 15 kW, 18 LPM PG25, 45 C inlet, 117 cm2. Columns:

- **Conservative**: PCM headline at the Monte Carlo P90, or the stated fallback.
- **Nominal**: PCM median (RF-15).
- **Stretch**: LM (Tier 2), or the stated variant.

| Metric | CoolIT 15 kW | Conservative | Nominal | Stretch |
|---|---|---|---|---|
| Average case-to-inlet dT | 34.4 K (measured) | ≤ 32 K (P90 31.9) | **28.4 K** (-17 %) | 23.3 K (-32 %) |
| Maximum case-to-inlet dT | 44.2 K (measured) | ≤ 35 K (P90 35.0) | **31.4 K** (-29 %) | 25.4 K (-43 %) |
| Same-paste average / maximum | 34.4 / 44.2 K | 31.7 / 35.9 K (controlled-BLT P90; uncontrolled P90 37.5 / 42.6) | 30.4 / 35.4 K | 27.8 / 32.8 K (paste 0.05) |
| Tcase,max at 15 kW | 89.2 C | ≤ 80 C | 76.4 C | 70.4 C |
| Resistance R / unit R'' (average) | 2.29 mK/W / 0.269 cm2K/W | ≤ 2.13 / ≤ 0.25 | 1.90 / 0.222 | 1.55 / 0.182 |
| Max minus average | 9.8 K | ≤ 4 K | 3.0 K | 2.1 K |
| Plate-to-plate spread at one TC | 10.1 K | ≤ 3 K | ≤ 2 K | ≤ 1 K |
| Plate dP port-to-port, 18 LPM | undisclosed (est. 22-25, band 17-42) | ≤ 10 kPa (P90 7.2) | **5.6 kPa** | 4.1 kPa (20 mm ports) |
| Plate dP at 36 LPM | est. 58-69 kPa | ≤ 30 kPa | 22 kPa | 16 kPa (20 mm ports) |
| Tray loop with a UQD08 pair, 18 LPM | est. 64-90 kPa | ≤ 65 kPa | ~45 kPa | ~40 kPa |
| Hydraulic pumping power, 18 LPM | ~6.5-7.4 W (est.) | ≤ 3 W | 1.7 W | 1.2 W |
| Flow to match 34.4 K average | 18 LPM | ≤ 13 LPM | 11.1 LPM | 8.5 LPM |
| Q capacity, Tcase,max ≤ 85 C | ~13 kW | ≥ 18 kW (P10 18.1) | **21.1 kW** | 28.9-29.6 kW |
| Inlet headroom (Tcase,max = 85 C) | ~41 C | ≥ 50 C | 53.6 C | 59.6 C |
| Equal pumping power (6.5 W), avg / max | 34.5 / 44.3 K | ≤ 28 / 31 K | 25.1 / 28.1 K | 20.0 / 22.1 K |
| 350 W/cm2 four-die package, Tcase,max | ~134 C (paste) | 109 C (PCM) | 95 C (LM) | 84 C (performance core, ≤ 33 um loops) |
| Uniform low-flux GPU TTV (1.4 kW, 45 cm2), average | 13.2 K | 15.3 K (**loses**) | 15.3 K (**loses**) | 14.0 K (**loses**) |
| Burst / leak | n/d | ≥ 2.0 MPa design / 1e-5 | ≥ 4.5 MPa sample / 1e-6 | - |
| Height at bar / plate | est. 22-28 / 10-13 mm | 29.5 / 14.5 mm (**worse**) | 29.5 / 14.5 mm | 21 mm (Rev C, roadmap) |
| Mass | est. 1.2-1.6 kg | 1.9 kg (**worse**) | 1.8 kg | 1.6 kg |
| Factory cost at 100k/yr; US$ per kW of capacity | incumbent ~US$105; 8.3 $/kW | ≤ US$185; ≤ 10 $/kW | US$148; 7.0 $/kW | US$125; 5.9 $/kW |
| Service life behind the 50 um screen | 1.0x (10-year reference) | not claimed at M12 | ≥ 0.6x target | 1.2x behind 25 um |
| Model P(beats on both average and maximum) | - | 0.85 (F2 fallback) | **0.98** | 1.00 |
| Public data | June 2026, 1 flow point, no dP | M12 full OCP report | + independent repeat | + CpK, fouling, TTV-B |

Sources: CoolIT 15 kW Tech Brief (local `pdf/brief.txt`); OCP Global Summit 2027 dates ([OCP](https://www.opencompute.org/news/ocp-global-summit-is-moving-to-a-new-location/)); Watlow ULTRAMIC AlN heater rating ([Eurotherm/Watlow](https://www.eurotherm.com/?p=141148)); Durex/Oasis multi-layer AlN heaters ([New Equipment Digest](https://www.newequipment.com/product-directory/process-equipment/heating-equipment/product/55102853/20781-ceramic-heater)); NVIDIA AlN TTV patent US 12,446,195 ([USPTO Gazette](https://patentsgazette.uspto.gov/week41/OG/html/1539-2/US12446195-20251014.html)); commercial vacuum-brazed cold plates ([Mersen Aquamax](https://us.mersen.com/products/engineering/aquamaxr-vacuum-brazed-cold-plates), [Wakefield](https://www.richardsonrfpd.com/ep-insights/high-performance-liquid-cold-plate-heat-sink-from-wakefield-thermal/)). All other values come from the project evidence base: `research/SYNTHESIS-benchmark-and-requirements.md`, `physics/SYNTHESIS-physics.md` and the sibling physics reports, `research/manufacturing-cost.md`, `research/gap-*.md`.
