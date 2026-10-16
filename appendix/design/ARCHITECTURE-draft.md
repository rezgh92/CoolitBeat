# PRISM: the consolidated cold-plate architecture of record (draft)

Chief-architect synthesis, 2026-10-14. Status: draft for the line manager. It consolidates eight judged proposals (Appendix A) into one top-level architecture. It does not contain a detailed design.

**PRISM** stands for **P**roven-subset, **R**ecessed-meter, **I**nterdigitated, **S**kived **M**anifold cold plate.

**Inputs.** The CoolIT 15 kW tech brief (`pdf/brief.txt`), `research/SYNTHESIS-benchmark-and-requirements.md` and the angle and gap reports, `physics/SYNTHESIS-physics.md` and its sibling reports, the eight proposals and 24 judge reports, and the project scoping model `docs/cooling/model/coldplate_model.py`, which was run unchanged.

**New calculations for this draft** are listed in Appendix D (scripts and outputs in `appendix/arch/`).

Treat every modelled term as ±25 %, and treat costs as ±20 % until RFQs arrive.

---

## 0. Executive summary

**The architecture in ten sentences**

1. PRISM is a single-phase, all-OFE-copper, vacuum-brazed hierarchical manifold micro-channel cold plate built only from conventional processes. From the die face up, it is: a skived fin field (0.15 mm fins, 0.15 mm gaps, 2.0 mm tall) kerfed at every inlet and outlet line; a stamped floor grate; a stamped orifice meter sheet; a laminated plenum layer; a stamped separator; and a forged-and-CNC header bar.
2. Each coolant parcel is metered by a 0.5 x 0.9 mm orifice. It drops through a recessed window into a kerf and runs 6 mm along a fin segment before leaving through an interior outlet window. The flow length is graded 4-12 mm by local heat flux. This removes split-flow's 54 mm caloric ramp and the pressure penalty that forces split-flow plates onto 0.2 mm fins.
3. The fin tips are brazed to the floor-grate lands over 80 % of their length. The result is a tied sandwich with a 1.0 mm base, no pressure bow, and a face stiff enough to hold a PCM pad or liquid metal at its datasheet value.
4. PRISM is the winning risk-first proposal, PSM-12, with three structural corrections forced by the judges and by our own 2-D checks:
   - the flow meter moves off the braze plane into a separately stamped sheet;
   - the fins are kerfed so that coolant enters each fin segment over its full height;
   - the benchmark-class slot pitch opens from 8 mm to 12 mm.
   Together these recover about 1.9 K that the corrected PSM-12 had lost (section 3.4).
5. At CoolIT's operating point (15 kW, 18 LPM PG25, 45 C inlet, 117 cm2 heated area) PRISM predicts:
   - **28.4 K average / 33.3 K maximum with a PCM pad** (P90 31.7 / 36.9 K);
   - **30.4 / 37.2 K with CoolIT's paste class**;
   - against CoolIT's measured **34.4 / 44.2 K**;
   - at **5.9 kPa port-to-port with 20 mm ports**, against about 22 kPa for our reconstruction of CoolIT's plate.
6. The robust wins are:
   - maximum case temperature, 16-25 % lower;
   - uniformity: maximum minus average of 4.9 K against 9.8 K;
   - plate-to-plate spread;
   - pressure drop, about 70 % lower;
   - case-temperature-limited capacity, 30-50 % higher;
   - inlet-temperature headroom, 7-11 K more.
   The average win is real but depends on footprint. It is 12 % like-for-like on paste, and becomes parity if CoolIT's heaters were really only 100 cm2.
7. The stretch tiers are liquid metal (Tier 2: 23.3 / 27.3 K) and the filtration-gated P-grade (0.10 mm gaps behind ≤ 33 µm absolute filtration: 25.4 / 29.7 K with PCM).
8. PRISM does **not** beat CoolIT on per-plate factory cost: about US$160 against about US$110 at 100k/yr, or 8-10 % worse per kW of capacity. It also loses on field track record. At CoolIT's small single-die 4 kW point the drop-in core only ties, at 0.0093 against < 0.009 C/W with PCM. It is at parity on height (about 25 mm at the bar) and slightly heavier on mass (about 1.6-1.75 kg against an estimated 1.2-1.6 kg).
9. A 12-month gated programme costs US$6.6 M, rising to US$9.5-10 M for a qualified product at M18. It delivers an OCP-format public result with an independent-lab repeat at OCP Global Summit 2027. The single make-or-break item is the fin-tip tie braze, gated at M3 with three alternative join routes and a 1.5 mm-base fallback.
10. Market entry is through hyperscaler custom-ASIC programmes via a contract-manufacturing partner, then NVIDIA volume via a Group-A/B manufacturing partnership. The second application is 800 VDC power-conversion plates and direct-substrate SiC modules in the same PG25 loop.

**Scorecard vs CoolIT 15 kW.** Conditions: 15 kW, 18 LPM PG25, 45 C inlet, 117 cm2.

- **Conservative**: PRISM-15 R-grade at the Monte Carlo P90, using the TIM named in the row.
- **Nominal**: the median.
- **Stretch**: Tier 2 liquid metal, with the filtration-gated P-grade in brackets.

| Metric | CoolIT 15 kW | Conservative | Nominal | Stretch |
|---|---|---|---|---|
| Average dT, PCM (OCP TIM assumed) | 34.4 K | 31.7 K | **28.4 K (-17 %)** | 23.3 K [P + LM 20.3] |
| Average dT, same paste as CoolIT | 34.4 K | 34.7 K (parity) | **30.4 K (-12 %)** | [P-grade 27.4 K] |
| Maximum dT, PCM | 44.2 K | 36.9 K | **33.3 K (-25 %)** | 27.3 K [23.6] |
| Maximum dT, same paste | 44.2 K | 42.0 K | **37.2 K (-16 %)** | [33.6 K] |
| Maximum minus average | 9.8 K | 6.8 K (paste) | 4.9 K (PCM) | 4.0 K (LM) |
| Plate dP port-to-port, 18 LPM | not disclosed (est. ~22, band 17-42) | ≤ 7.5 kPa | **5.9 kPa** (20 mm ports); 8.2 kPa (16 mm) | 5.9 kPa |
| Plate dP, 36 LPM | est. 58-69 kPa | ≤ 27 kPa | 21.4 kPa | 21.4 kPa |
| Q capacity at Tcase,max ≤ 85 C, 1.2 LPM/kW | ~12.9 kW | 16.6 kW (paste) | **19.4 kW** (PCM) | 26.4 kW [34.1] |
| Inlet allowed at 15 kW (85 C case, 65 C return) | 40.8 C | 47.8 C | **51.7 C** | 52.3 C (set by the return limit) |
| 350 W/cm2 four-die package, Tcase,max | ~134 C paste / ~121 C LM | 108 C (PCM) | 93-94 C (LM) | [84 C P-grade]; ~80 C direct-to-die |
| CoolIT's own 4 kW point (25 cm2, 6 LPM) | < 0.009 C/W | 0.0105 (paste, **loses**) | 0.0093 (PCM, **ties**) | 0.0074 LM [0.0081 P + PCM] |
| GPU-class uniform lid, 2.3 kW / 60 cm2, 1.0 LPM/kW, average | 16.1 K | 18.5 K (4 mm cells, **loses**) | 15.5 K (flux-graded 12 mm cells) | 13.4 K (LM) |
| Height at bar / mass | est. 22-28 mm / 1.2-1.6 kg | 26 mm / 1.85 kg | ~25 mm (parity) / ~1.6-1.75 kg (slightly heavier) | GPU-class ~20 mm / 0.85 kg |
| Factory cost at 100k/yr | ~US$110 (incumbent class) | US$190 | **US$160 (loses, +45 %)** | US$113 at 1M/yr |
| Public data | 1 flow point, no dP | full OCP v1.0.0 report | + independent-lab repeat | + fouling and real-silicon data |

**Target applications, ranked**

1. Hyperscaler custom AI ASICs with large multi-die packages. These buyers own both the package and the loop, so they can add the tray filter that the P-grade needs.
2. NVIDIA Rubin Ultra / Feynman-class plates (2-6 kW per package) through a Group-A/B manufacturing partner.
3. 15-30 kW multi-die modules, superchip boards and wafer-scale tiles.
4. CPU, NVSwitch and co-packaged-optics switch plates.
5. 800 VDC in-rack power conversion, solid-state transformers and solid-state breakers in the PG25 loop.
6. SiC traction (licence only).

**The three decisions the line manager must take**

- **D1. Claim scope and lead grade.** Approve the public claim: "beats CoolIT's 15 kW plate on every metric the OCP Cold Plate Test Specification v1.0.0 measures and on every metric CoolIT disclosed; at parity on height; slightly heavier; more expensive per plate". Lead with the drop-in R-grade. Also choose whether to fund the P-grade plus tray-filter kit as the decisive like-for-like product. Recommendation: lead with R-grade, carry P-grade as stretch data, and decide at G2 (M6).
- **D2. Channel and moat.** Choose build-and-supply through a contract manufacturer for hyperscaler ASICs first, with NVIDIA volume through a manufacturing partnership with a Group-A/B house. Do not rely on a licensing model: the moat is process know-how and data, not patents. The alternative is a licence-first route.
- **D3. Budget and gating.** Approve US$6.6 M for 12 months (US$9.5-10 M to M18), with:
  - kill/pivot gates at M3 (tie braze) and M6 (measured parity);
  - US sales gated on a Split-Flow claim chart, because that patent family is live until 2028-2032.

---

## 1. Benchmark recap and what "beating CoolIT in every aspect" means

### 1.1 Benchmark facts and our reconstruction

| Item | Value | Basis |
|---|---|---|
| Load, TTV | 15 kW; 4 ceramic heaters ("GPU and HBM zones"); 3 plates x 8 TCs at the heater surface | brief |
| Coolant, flow, inlet | water-glycol (PG25 assumed); 1.2 LPM/kW = 18 LPM; 45 C | brief |
| Measured | average 34.4 K (plates 32.5 / 35.2 / 35.6), maximum 44.2 K (TC5); spread 10.1 K at TC8 | brief |
| Not disclosed | pressure drop, footprint, TIM identity, height, mass, cost, R vs flow | brief |
| Footprint | ~120 cm2 (100-145) by photogrammetry; 117 cm2 calibration kept (128 W/cm2) | research synthesis C1 |
| Term budget (1-D, calibrated) | caloric 6.3 + paste 9.0 + 2 mm base 6.6 + convection 12.6 = 34.5 K; hot spot 6.3 ramp + 3.5 scatter | physics synthesis |
| Same 2-D physics as our cell model | +1.75 K penalty vs 1-D (z-unmixed fluid in a 4 mm-tall, 54 mm channel); absorbed by the calibration | `run_coolit2d.py` |
| Plate dP | ~22 kPa port-to-port (17-42 band; working value 35, 20-60) | physics synthesis; gap-dP |
| CoolIT 4 kW plate (Mar 2025) | 50 x 50 mm, < 0.009 C/W max-case incl. TIM at 6.06 LPM; 55 kPa full loop | coolit-briefs |
| CoolIT re-tested on PCM (our estimate) | 32.5 K average / 40.3 K maximum (TIM 9.0 → 7.1 K; scatter 3.5 → 1.5 K) | this draft |

### 1.2 The arbiter, and how we will read "every measurable aspect"

The arbiter is the **OCP Single-Phase D2C Cold Plate Test Specification v1.0.0** (October 2026). Its primary author, Ben Sutton, also wrote CoolIT's brief, so a win measured in that format cannot be dismissed. The judges correctly said the literal claim cannot be made for any proposal. We therefore sort every metric into four classes and set a rule for each.

| Class | Metrics | Rule |
|---|---|---|
| A. Measured by the OCP spec | R = (Tcase - Tin)/P at ≥ 6 flows with the spec's recommended TIM; dP at ≥ 6 flows, 45 ± 2 C; proof, burst, leak; drift after cycling | **must beat** at the recommended TIM (identity unverified: plan for PCM and paste) |
| B. Disclosed by CoolIT | average and maximum dT at 15 kW / 1.2 LPM/kW; 4 kW plate R; plate-to-plate spread | **must beat like-for-like**: same TIM class, R'' per area, footprint sensitivity published |
| C. Not disclosed but measurable on a sample | height, mass, uniformity, Q capacity, inlet headroom, equal-pumping-power and equal-flow curves, cost | beat where physics allows; state the rest openly |
| D. Not measurable at launch | field track record, 10-year fouling life | no claim until our own data exist |

**Like-for-like rules we impose on ourselves**

- Publish paste and PCM results separately, each with the measured post-test bond line.
- Report the architecture-only delta.
- Build the TTV no smaller than CoolIT's estimated footprint, and add a 100 cm2 "hard mode" TTV.
- Publish dP at three named boundaries: port-to-port with the bore stated; plus stubs and barbs as in CoolIT's photograph; plus a named UQD08 pair.
- Show 3 plates x 3 re-mounts at k = 2 uncertainty, with an independent-lab repeat.

---

## 2. Architecture overview

### 2.1 What PRISM is

PRISM is an all-copper, single-braze-cycle **tied sandwich**. A fine skived fin field is fed through a short-path manifold, so the fin geometry is set by heat transfer and fouling rather than by pressure drop.

Four ideas carry it:

1. **Short, flux-graded flow length.** Each fin segment is 4-12 mm long, chosen by the local heat flux (section 3.3). It is 6 mm on the 15 kW TTV.
2. **An inertial meter that never touches a braze joint.** A stamped 0.4 mm sheet carries one row of 0.5 x 0.9 mm orifices per inlet line. It sits 1.0 mm above the fin tips, over a recessed window.
3. **Full-height entry.** 0.3 mm kerfs through the fins under every inlet and outlet line let coolant enter and leave each fin segment over its full height. This suppresses the Hele-Shaw short-circuit along the fin tips that judges found in every top-fed design.
4. **A tied sandwich.** Fin tips are brazed to the floor-grate lands, so a 1.0 mm base carries pressure with no bow.

### 2.2 Stack-up and flow path (PRISM-15, benchmark build, 125 x 125 mm body, 108 x 108 mm fin field)

```
   z (mm)   layer (process)                                  function
   25.4  +---------------------------------------------+
         | HEADER BAR, 10.5 mm (forged + CNC)          |  inlet hdr 2x(12x8) | outlet hdr 2x(14x8), ribbed;
         |  [IN]==>  mid-fed   ...  mid-fed  ==>[OUT]  |  vertical 20 mm ports (or dual 1/2-in pairs); guard screen
   14.9  +---------------------------------------------+
         | SEPARATOR 1.5 mm (stamped)                  |  18 feed windows 4.5 x 14 mm (inlet at y=-14, outlet at y=+14)
   13.4  +----+----+----+----+----+----+----+----+-----+
         |PLENUM LAYER 9.0 mm (2 stamped laminations)  |  18 plenums 4.5 x 9 x 108 mm, 1.5 mm walls, alternating in/out
         | in | out| in | out| in |  ...              |  (6 mm pitch = 12 mm inlet-to-inlet)
    4.4  +-ooo-+----+-ooo-+----+-ooo-+-----------------+
         | METER SHEET 0.4 mm (stamped)                |  inlet lines: 54 orifices 0.5 x 0.9 mm @ 2 mm; outlet lines: open 1.2 mm
    4.0  +=[ ]=+=[ ]=+=[ ]=+============================+
         | FLOOR GRATE 1.0 mm (stamped)                |  1.2 mm windows (recess); lands 4.8 mm brazed to fin tips
    3.0  +||||||| ||||||| ||||||| |||||||||||||||||||||+
         | FINS 2.0 mm (skived RF-15: 0.15/0.15)       |  0.3 mm full-height kerf under every window
    1.0  +---------------------------------------------+
         | BASE 1.0 mm (fly-cut after braze)           |  die face, <= 20 um flat, Ra <= 0.8 um
    0.0  +=============================================+  <- TIM -> lid / TTV / bare die (tier dependent)

   Flow:  port -> guard screen -> inlet header (mid-fed) -> separator window -> inlet plenum (centre-fed)
          -> meter orifice (1.37 m/s, 1.8 kPa) -> recessed window -> kerf + fin tops -> 6 mm along fin gaps (0.15 m/s)
          -> kerf + outlet window -> outlet plenum -> separator window -> outlet header -> port
```

### 2.3 Product family and tiers

All family members share one process chain, one braze route and one test cell.

| SKU | Application | What changes from PRISM-15 |
|---|---|---|
| **PRISM-15** | 15 kW TTV demo; 10-30 kW multi-die modules and ASIC sleds | baseline above; 12 mm slot pitch; 20 mm ports |
| **PRISM-G** | Rubin / Rubin Ultra / MI455X-class lidded packages, 1.8-4 kW, 110 x 120 mm | zoned: 8-10 mm pitch over dies, 16-24 mm over HBM and margin; 10 mm horizontal ports; plenum 5 mm; ~20 mm at the bar |
| **PRISM-S** | CPU, NVSwitch, CPO switch ASICs (0.3-2 kW) | small field; uniform 16-24 mm pitch; laser zones fed first |
| **PRISM-W** | wafer-scale and multi-chip tiles | plenum tiles repeated; flow length stays fixed at any size; one port pair per ~110 mm |
| **PRISM-P (grade)** | high-flux dies on loops filtered to ≤ 33 µm absolute | 0.10 / 0.10 x 1.5 mm fins (die zone only, or the whole field) |
| **PRISM-DC** | 800 VDC shelves, SST, solid-state breakers in the PG25 loop | Ag-sintered direct-substrate cartridge on the R core, or a plate with a keyed inlet orifice |
| **PRISM-A** | SiC traction (licence) | coarse ≥ 0.5 mm aluminium or Ni-plated Cu grade for WEG / Al loops |

**Interface tiers on the same core.** The tier is set only by finishing the face after the braze (a graft from direct-to-die).

| Tier | Package | Interface | Plate face |
|---|---|---|---|
| T1 drop-in | flat lid (Rubin Au lid, MI355X / MI455X, B200) | PCM pad (PTM7950 class): 0.055 at 25 psi on the TTV, 0.07 at module retention (4-12 psi) | lapped bare Cu, ≤ 20 µm |
| T2 OEM co-design | Ni / Au lid | Ga-In liquid metal, 20-30 µm bond line, dam | 3-5 µm electrolytic Ni on the face only, **no Au** |
| T3 chip co-design | bare die (hyperscaler ASIC) | stepped pedestal + liquid metal; lid and TIM1 removed | fly-cut pedestal crowned to hot-state warpage, Ni or W, dam, moat |
| T3B (roadmap) | micro-channel lid | indium TIM1 soldered by the OSAT | P core as lid insert; CTE-matched rules (8.3) |

---

## 3. Thermal core specification

### 3.1 Cores

| Item | R-grade (robust, drop-in) | P-grade (performance, filtration-gated) | Why |
|---|---|---|---|
| Fins | skived OFE C10100, 0.15 thick / 0.15 gap / 2.0 tall (pitch 0.30, aspect 13); 360 fins on 108 mm | 0.10 / 0.10 / 1.5 mm | 0.15 mm is the 10-year fouling floor behind a 50 µm absolute screen. Thinner 0.10 mm fins at 0.15 gap model 0.6 K *worse* in 2-D (more z-variation of fin temperature), so the PSM-12 "RF-10 hedge" is dropped. |
| Kerfs | 0.3 mm full-height gang-saw cut under every inlet and outlet window | same | Coolant enters and leaves each segment over its full height. Cross-cutting skived fins is established practice (pin-fin conversion). |
| Flow length (L) | 6 mm on the 15 kW TTV; graded 4-12 mm by local flux (3.3) | 4 mm | sets caloric, 2-D penalty and ripple (3.4) |
| Base | skived on a 2.5 mm blank, fly-cut after braze to **1.0 ± 0.1 mm** (0.8 mm minimum under a die); perimeter land 1.8 mm, ≤ 4 mm unsupported | same | 3.3 K at 128 W/cm2; each extra mm costs +9 K at 350 W/cm2 |
| Channel state, 18 LPM | 0.15 m/s, Re 34 (6 mm cells), h 13.3 kW/m2K, fin efficiency 0.65, h_eff 122 kW/m2K | h_eff 187 kW/m2K | laminar, no shear self-cleaning |
| Ceiling | straight Cu fins at a 0.15 mm gap cannot exceed h_eff ≈ 138 kW/m2K; skiving reaches about 90 % of it | ceiling 207 kW/m2K | graft from advanced-manufacturing: once fouling fixes the gap, no printed fin geometry buys more |

### 3.2 Fin-level geometry: recessed meter, window and kerf (the main change from PSM-12)

The judges raised three objections to PSM-12's fin-level design:

1. The only flow meter, a 0.30 mm gang-sawn slit, sat exactly where braze fillets, filler wicking and fly-cut burrs form.
2. A 1.32 m/s fin-entry jet broke the 0.5 m/s velocity cap between fins (impaction, erosion).
3. A 2-D Hele-Shaw effect added a one-sided bias of +0.8-1.7 K.

We modelled all three with a 2-D conjugate cell model in which the fluid is not mixed across the fin height (z). It reproduces judge model A exactly (24.78 K for PSM's slit).

| Geometry, 128 W/cm2, 1.0 mm base | 1-D (synthesis) caloric + conv + base | 2-D | Differential vs the calibrated CoolIT reconstruction (its own 2-D penalty is +6.9 %) |
|---|---:|---:|---:|
| PSM-12 slit 0.30 / 0.60 at the fin tips, no kerf, L 4 mm | 21.43 K | 24.78 K | **+1.9 K** |
| hmmc-elite 3.3 mm openings over 0.7 mm walls | 20.98 K | 33.23 K | +10.8 K (fatal, as the judge found) |
| Recessed 1.2 mm windows + 0.3 mm kerfs, L 4 mm | 21.43 K | 24.02 K | +1.1 K |
| **Recessed 1.2 mm windows + 0.3 mm kerfs, L 6 mm (PRISM-15)** | 21.37 K | 22.83 K | **0.0 K** |
| Recessed windows, **no** kerf, L 6 mm | 21.43 K | 23.54 K | +0.6 K |
| Same, L 8 mm | 21.37 K | 22.25 K | -0.6 K (but case ripple 5.5 K peak-to-peak) |
| P-grade, windows + kerfs, L 4 mm | 18.29 K | 19.63 K | +0.1 K |

**What we specify**

- **Floor grate.** Each inlet and outlet line has a 1.2 mm-wide, 1.0 mm-deep window cut through a stamped 1.0 mm floor grate. The fin tips under the window are left free. The fins below have a 0.3 mm kerf on the window centre line.
- **Meter sheet.** A stamped 0.4 mm meter sheet sits on top of the grate. Each inlet line has 54 oblong orifices, 0.50 x 0.90 mm, at 2 mm pitch. Each outlet line is an open 1.2 mm slot.
- **Clearances.** Every orifice edge is ≥ 0.35 mm sideways and 1.0 mm vertically from the nearest braze joint. The filler is masked within 0.3 mm of the window edges.
- **Inspection.** The meter is measured by backlit vision while the sheet is still open, *before* the braze, and verified after the braze by the 100 % infrared flow screen (5.4).
- **Fin-entry velocity.** Mean entry into the fins across the window and kerf is 0.41 m/s, under the 0.5 m/s cap. PSM-12's was 1.32 m/s.

### 3.3 Flux-graded flow length (new rule)

The isothermal-cell caloric penalty that makes short-cell plates lose the *average* on low-flux lids is a function of cell length. In a 4 mm cell, lateral conduction in the base and fins (conduction length about 2.5 mm) holds the wall nearly isothermal, so the wall must run hotter than the fluid leaving the cell. Longer cells let the wall follow the fluid ramp.

The 2-D model (differential method, both plates in 2-D) gives:

| Case, 1.0 LPM/kW, R'' 0.07 on both | CoolIT-like avg / max | PRISM, 4 mm cells | 8 mm | 12 mm |
|---|---|---|---|---|
| 1.4 kW on 45 cm2 (31 W/cm2) | 14.5 / 21.7 K | 17.2 / 19.5 | 15.5 / 19.6 | **14.2 / 20.0** |
| 2.3 kW on 60 cm2 (38 W/cm2) | 16.1 / 23.5 K | 18.5 / 21.0 | 16.7 / 21.1 | **15.5 / 21.5** |
| 3.6 kW on 80 cm2 (45 W/cm2) | 17.6 / 25.1 K | 19.6 / 22.2 | 17.7 / 22.3 | **16.6 / 22.7** |
| 15 kW on 117 cm2 (128 W/cm2, paste, 1.2 LPM/kW) | 34.5 / 44.3 K | 31.5 / 37.3 | 29.8 / 37.5 | - (L 6 mm: **30.4 / 37.2**) |

**Rule: choose flow length by zone flux.**

| Zone flux | Flow length | Slot pitch |
|---|---|---|
| ≥ 250 W/cm2 | 4-5 mm | 8-10 mm |
| 100-250 W/cm2 | 6 mm | 12 mm |
| 50-100 W/cm2 | 8 mm | 16 mm |
| < 50 W/cm2 | 12 mm | 24 mm |

Unheated margin gets no slots, only bleeds.

Longer cells raise the case ripple, which costs on the maximum. On real packages that ripple is smoothed by the lid. This rule converts the "uniform low-flux GPU lid" concession that every judged proposal carried (−1 to −3 K on the average) into a narrow win (−0.3 to −1.0 K average, −1.7 to −2.4 K maximum). It is a refinement of PSM-12's zoning by slit pitch.

### 3.4 Term budgets at the benchmark point

| Build | Caloric | TIM | Base | Conv | 2-D diff | **Avg** | Hot spot (flow + scatter + ripple) | **Max** | R'' cm2K/W |
|---|---:|---:|---:|---:|---:|---:|---|---:|---:|
| CoolIT-like (calibration) | 6.3 | 9.0 | 6.6 | 12.6 | (in calibration) | 34.5 | 6.3 + 3.5 | 44.3 | 0.269 |
| PSM-12 as proposed, corrected | 7.6 | 7.1 | 3.3 | 10.5 | +1.9 | 30.3 | 1.5 + 1.5 + 0.9 | 34.2 | 0.236 |
| **PRISM-15, PCM at 25 psi (TTV headline)** | 7.6 | 7.1 | 3.3 | 10.5 | 0.0 | **28.4** | 1.5 + 1.5 + 1.85 | **33.3** | 0.222 |
| PRISM-15, paste 0.07 (like-for-like) | 7.6 | 9.0 | 3.3 | 10.5 | 0.0 | **30.4** | 1.5 + 3.5 + 1.85 | **37.2** | 0.237 |
| PRISM-15, PCM at module retention (0.07) | 7.6 | 9.0 | 3.3 | 10.5 | 0.0 | 30.4 | 1.5 + 1.5 + 1.85 | 35.2 | 0.237 |
| PRISM-15, liquid metal (T2) | 7.6 | 1.9 | 3.3 | 10.5 | 0.0 | **23.3** | 1.5 + 0.6 + 1.85 | **27.3** | 0.182 |
| PRISM-15, PCM, 0.8 mm base (stretch) | 7.6 | 7.1 | 2.6 | 10.5 | 0.0 | 27.8 | as above | 32.6 | 0.217 |
| PRISM-P, PCM (L 4 mm) | 8.2 | 7.1 | 3.3 | 6.8 | +0.1 | 25.4 | 1.5 + 1.5 + 1.2 | 29.7 | 0.198 |
| PRISM-P, paste | 8.2 | 9.0 | 3.3 | 6.8 | +0.1 | 27.4 | 1.5 + 3.5 + 1.2 | 33.6 | 0.213 |
| PRISM-P, LM | 8.2 | 1.9 | 3.3 | 6.8 | +0.1 | 20.3 | 1.5 + 0.6 + 1.2 | 23.6 | 0.158 |
| PRISM-15 T3 direct-to-die (LM, 0.8 mm pedestal; case = die top) | 7.6 | 1.9 | 2.6 | 10.5 | 0.0 | 22.6 | | 26.6 | 0.177 |

Notes on the inputs:

- **Ripple.** The 2-D case shows a peak-to-peak sawtooth of 1.70 K at L 4 mm and 3.7 K at L 6 mm. The crest (half of that: 0.85 and 1.85 K) is added to the maximum in full because a TC may sit on a crest.
- **PCM pressure.** The PCM value at 25 psi (2.0 kN on 117 cm2) answers the judge's finding that 15 psi leaves PTM7950-class pads at 0.06-0.08. Real packages at 0.3-1 kN of retention are budgeted at 0.07.

### 3.5 Zoning and HBM

Zoning is done by heat, not by area (graft from hmmc-elite and the physics synthesis):

- the die block gets 85-90 % of the flow;
- HBM columns get 0.3-0.5x the average flow per area;
- unheated margin gets slot-end bleeds only.

The levers are slot pitch (flux-graded, 3.3) and orifice pitch or size in the meter sheet. A new package needs new meter artwork and plenum laminations, which is a 2-3 week die change; laser-cut parts are used meanwhile. HBM never sits downstream of a die, because every zone is fed in parallel.

The HBM pedestal is a stepped Cu step machined into the face during the post-braze fly-cut, within ±0.05 mm of the HBM plane, with 0.05-0.10 mm compliant TIM. Gap-filler pads are never used above about 15 W/cm2. The across-die case gradient is specified as a product metric: 6-8 K on PRISM against 22-30 K on split-flow.

---

## 4. Hydraulic architecture

### 4.1 Levels, sizes and velocities (PRISM-15 at 18 LPM; rated flow declared as 1.0 LPM/kW = 15 LPM per the OCP sweep)

| Level | Element | Size | Velocity at 18 LPM | Rule it satisfies |
|---|---|---|---|---|
| L0 | 2 ports, vertical in the bar | **20 mm bore** (16 mm option) | 0.95 m/s (1.49 with 16 mm) | ≤ 1.5 m/s in Cu at 150 % of rated flow; 16 mm bores exceed this above 18 LPM, so Q-capacity ratings use 20 mm |
| Guard | 50 µm absolute pleated 316L cylinder in the inlet boss, ≥ 25 cm2, serviceable from the port | | 0.3 kPa clean | last-chance guard only; primary filtration is upstream (4.4) |
| L1 | inlet header 2 x (12 x 8) mm, outlet 2 x (14 x 8) mm, side by side on the centre line, mid-fed (9 LPM per half), 2 mm tie rib in each | 192 / 224 mm2 | 0.78 / 0.67 m/s | header ≤ 1.0 m/s; outlet 1.2x inlet area |
| L1-L2 | separator windows 4.5 x 14 mm (inlet at y = -14 mm, outlet at y = +14 mm) | 63 mm2 | 0.53 m/s | |
| L2 | 18 plenums 4.5 x 9 x 108 mm, 1.5 mm walls, alternating inlet and outlet at 6 mm | 40.5 mm2 | ≤ 0.52 m/s on the long half | slot entry ≤ 0.5 m/s |
| L3 | meter: 54 orifices of 0.50 x 0.90 mm per inlet line (486 per plate), 0.4 mm sheet | 219 mm2 total | 1.37 m/s (1.71 at 1.5 LPM/kW) | inertial; ≥ 0.4 mm feature = 8x the guard rating |
| L3' | recessed window 1.2 x 1.0 mm + 0.3 mm kerf | | 0.41 m/s mean fin entry | ≤ 0.5 m/s between fins |
| L4 | fin gaps 0.15 x 2.0 mm, 6 mm per segment (6,480 parallel segments) | | 0.15 m/s (Re 34) | 0.65 kPa |

Passage hierarchy: port 20 > header 8 > plenum 4.5 > window 1.2 > orifice 0.5 > kerf 0.3 > gap 0.15 mm. Every stage is more than 1.5-2x wider than the next, so nothing sieves upstream of the channels. Each inlet-plenum dead-end bleeds about 4 % of its flow through a 0.6 mm hole into the neighbouring outlet plenum, at a cost of about 0.3 K. Plenum ends and port-adjacent lines sit outside the die on package SKUs. The plate is symmetric and the orifices meter in both directions, so it can be back-flushed.

### 4.2 Pressure-drop budget (PG25, 45 C)

| Element | kPa at 18 LPM | Character |
|---|---:|---|
| Ports, 20 mm, K 3.5 combined (judge: 3-4, not 2.3) | 1.6 (3.9 with 16 mm) | inertial |
| Guard screen, clean | 0.30 | viscous |
| Headers, mid-fed tees, K 1.5 each side | 0.80 | inertial |
| Separator windows, in + out | 0.56 | inertial |
| Plenums (friction + combining momentum) | 0.15 | mixed |
| **Meter orifices (Cd 0.72)** | **1.82** | inertial |
| Window, kerf turn, outlet window | 0.08 | inertial |
| Fin channels | 0.65 | viscous |
| **Plate, port-to-port** | **5.9** (8.2 with 16 mm ports) | 82 % inertial |

| Flow | 15 LPM (rated) | 18 LPM | 27 LPM | 36 LPM (2x, characterisation only) |
|---|---:|---:|---:|---:|
| PRISM-15, 20 mm ports | 4.2 kPa | **5.9 kPa** (1.8 W) | 12.4 kPa | 21.4 kPa (12.8 W) |
| PRISM-15, 16 mm ports | 5.8 | 8.2 (2.5 W) | 17.6 | 30.7 |
| CoolIT-like reconstruction | ~17 | ~22 (6.5 W) | ~40 | 58-69 (35-42 W) |

**External claim:** ≤ 7.5 kPa at 18 LPM with 20 mm ports (≤ 10 kPa with 16 mm), and ≤ 27 kPa at 36 LPM, until CFD and test confirm. The plate is about 3.7x lower than the reconstruction (2.7x with 16 mm ports). CoolIT's pressure drop is undisclosed, so we publish ours against the physics floor of ≥ 15-20 kPa for any single-split plate with 0.2 mm fins, never as a measured CoolIT value.

**Couplings dominate the loop.** A UQD08 pair costs about 20-35 kPa at 18 LPM (Cv estimate, ±50 %). "UQD12" is not confirmed in OCP UQD v2.0.0, so the standards-compliant 15 kW options are:

- **dual UQD08 pairs**: tray loop about 15-25 kPa with PRISM;
- a 3/4-in hard-plumbed sled;
- a single UQD08 pair: about 30-45 kPa with PRISM, against 64-90 kPa estimated for a CoolIT-like plate.

Three graft rules from system-platform apply in a rack:

- A low-dP plate needs either a 63 mm (2.5-in) rack manifold or a branch orifice of about 10 kPa.
- Direct return (U) beats reverse return (Z), because momentum rather than friction dominates.
- Every low-dP auxiliary plate (power shelf, NVSwitch, VPD) carries a **keyed inlet orifice** sized to the branch dP, so it cannot draw 2.6x its rated flow and starve GPU branches.

### 4.3 Uniformity: target, margin and verification

| Ratio | PRISM-15 | Rule | Result |
|---|---:|---:|---|
| Along-plenum: distributed branch (meter + fins + turn = 2.55 kPa) / long-half plenum head (136 Pa) | 18.7 | ≥ 15 (centre-fed) | 1-D plenum model, offset feed ±14 mm: **max/min 1.065-1.085** at 18, 27 and 36 LPM; truly centre-fed 1.04 |
| Slot-to-slot: branch + windows (3.0 kPa) / header head (306 Pa) | 9.8 | ≥ 6 (U / centre-collected) | global max/min ≤ 1.10 expected |
| Inertial fraction of the branch | 0.74 | - | ratios fall by ≤ 13 % at 2x flow, still above both rules |
| Orifice tolerance (punched ± 0.02 mm on 0.50 mm) | ±4 % area per orifice, random | | averaged over 54 orifices per line, smoothed by the base: < 0.3 K |

Two lessons from this check. First, the low-velocity, centre-fed plenums only work with a meter of at least about 2 kPa. With the fin-entry loss gone, a 0.9 kPa branch would give 1.3-1.5 max/min (`plenum_prism.py`). Second, the meter sheet therefore stays even though the judges liked PSM-12's single-feature slit: a slit recessed off the braze plane provides only about 0.5 kPa.

The flow-driven hot-spot term is budgeted at 1.5 K (±10 %) nominal and 2.5 K (±20 %) conservative. It is **verified, not assumed**, at three points:

- **E2 water table at M3.** A clear-SLA and printed-manifold replica on a thick-base kerfed core, with dye and taps at 9, 18, 27 and 36 LPM. Pass: max/min ≤ 1.10 at 18 LPM and ≤ 1.12 at 27 LPM.
- **100 % infrared flow-uniformity screen in production** (section 5.4).
- **Per-zone flow test** of every zoned artwork on TTV-B.

### 4.4 Filtration and fouling strategy (a ladder, not a single screen)

The judges showed that a 12 cm2 plate screen becomes the loop's filter and blinds in weeks at 1e-4 particles/mL. The fouling rule is pore count ≥ 100x the channel inlets, which means ≥ 150 cm2 of 50 µm media for one plate. PRISM therefore moves primary filtration upstream (graft from system-platform) and keeps only a guard in the plate:

| Stage | Element | Job |
|---|---|---|
| Commissioning | flush with plate bypass jumpers and 5-10 µm bags; connect plates only at ISO 4406 ≤ 16/14/11 with no particle > 50 µm (to be checked against the OCP PG25 Guidelines limits) | removes installation debris, the failure mode Ecolab cites |
| CDU (recommendation) | 25 µm full-flow + 5 µm side-stream | bulk cleanliness |
| Tray (recommended for R-grade, **required** for P-grade) | serviceable pleated cartridge, ≥ 150 cm2: 50 µm absolute (R) or ≤ 25-33 µm absolute (P); 316L or PTFE-lined hoses downstream | the filter that sets channel life |
| Plate | 50 µm absolute guard, ≥ 25 cm2 | catches tray-to-plate debris only, so years of loading |

**Channel rule.** The gap must be at least 3x the absolute rating of the last filter: 0.15 mm behind 50 µm (R), 0.10 mm only behind ≤ 33 µm (P). Channels finer than 0.10 mm stay off the roadmap.

**Life.** Without the tray cartridge, the R-grade on a 50 µm-nominal fleet loop runs at a service interval set by loop debris. That is a disclosed drop-in condition: CoolIT's 0.2 mm channels behind about 90 µm absolute sit at W/d 2.2, so they are not immune either.

**Impaction risk.** Particles ≤ 50 µm that pass the guard may deposit at the kerf floor under the meter jets (Stokes number about 1-2). They cannot block a 0.15 mm gap, but a kerf that fills reverts that line to PSM-12-like top entry, at a cost of about +1 K. Experiment E4 tests this.

---

## 5. Mechanical construction and manufacturing route

### 5.1 Stack-up, parts and joining

| # | Part | Material / process (prototype → volume) | Thickness | Mass |
|---|---|---|---|---|
| 1 | Base + fins | OFE C10100 strip; skived (Wieland / Nakamura / Winshare / Kingka class); tips fly-cut to a ±20 µm plane; 18 kerfs by gang saw; bright-dip deburr | 1.0 + 2.0 mm (2.5 mm blank) | 0.27 kg |
| 2 | Floor grate | OFE 1.0 mm; laser-cut → progressive-die stamped; closed-end 1.2 mm windows | 1.0 mm | 0.11 kg |
| 3 | Meter sheet | OFE 0.4 mm; laser-cut → stamped (486 oblong orifices, ≥ 0.4 mm so punchable at d/t ≥ 1) | 0.4 mm | 0.05 kg |
| 4 | Plenum layer | OFE; CNC end-milled → 2 stamped laminations of 4.5 mm (closed-end 4.5 mm slots, punchable at d/t 1.0) | 9.0 mm | 0.55 kg (0.40 with border pocketing) |
| 5 | Separator | OFE 1.5 mm, stamped (thickness set by FEA, 1.5-2.0) | 1.5 mm | 0.21 kg |
| 6 | Header bar | OFE; CNC → forged near-net + finish CNC; ribbed headers, port bosses, dP taps, guard cavity | 10.5 mm | 0.41 kg |
| 7 | Stubs, guard, springs, backplate | 316L / steel | | 0.15 kg |
| | **Total** | | **14.9 mm body, ~25.4 mm at the bar** | **~1.75 kg (~1.6 kg pocketed)** |

**Why stamping and laminations instead of PSM-12's gang-slit distributor.** The judges showed that a 9-10 mm-deep, 108 mm-long closed-end slot cannot be gang-slit inside a 125 mm outline. The saw run-out breaks through the ends. This flaw was flagged on CrossComb, and PSM-12's plenums have the same geometry. Closed-end slots are trivially stamped in 1-4.5 mm copper, and laminations braze in the same cycle. Their internal joints only separate inlet plenums from outlet plenums, so a missed joint is a bypass that the infrared and dP tests catch. It is not an external leak.

**Joining: one vacuum-braze cycle at about 790 C**, the incumbent cold-plate joint. Four routes are qualified in parallel in E1, so no single filler chemistry can stop the programme:

| Route | Filler | Load | Role |
|---|---|---|---|
| A | 25 µm BAg-8 laser-cut preforms matching the lands | ≤ 0.2 MPa | baseline (PSM-12) |
| B | 5 µm electroplated Ag on mating faces → Ag-Cu eutectic; masked off 0.3 mm from window edges | ≤ 0.2 MPa | least liquid → least wicking (PSM-12 / CrossComb) |
| C | Cu-Sn or Ag-Sn transient-liquid-phase interlayer at 600-700 C | ≤ 0.5 MPa | no capillary flow; judge graft (hmmc-elite) |
| D | Low-pressure solid-state diffusion bond, load carried by the lands and walls (≤ 1-2 MPa effective at fin tips) | heat-exchanger house | slow fallback; avoids the 25-50 MPa fin-tip stress that killed the diffusion-bond proposals |

No route puts more than about 1 MPa effective on the 0.15 mm fin tips. An optional green-laser perimeter seam can make the *outer* boundary filler-free (graft from CrossComb). The Ag-Cu fillets in the wetted path remain and are declared.

### 5.2 Base thickness, ties and pressure ratings

Ratings: MAWP 1.03 MPa (150 psi, the OCP preferred class); 100 % proof at 1.55 MPa; design burst ≥ 3.1 MPa (3x MAWP); sample burst ≥ 4.5 MPa; vacuum-stable to -0.9 bar(g).

Every allowable is post-braze annealed OFE copper with grain growth: **yield 35-50 MPa, design value 40 MPa** (judge correction; PSM-12 used 70 MPa). UTS is about 200 MPa.

| Load path | Stress at design burst 3.1 MPa | At sample burst 4.5 MPa | Comment |
|---|---:|---:|---|
| Fin tie: p x pitch / (t x bonded fraction 0.80) | 7.8 MPa (19 with Kt 2.5) | 11.3 (28 local) | local yield at the fillet toe at 4.5 MPa is acceptable (ductile, UTS-governed); ≥ 30 % bonded still survives 1.5 MPa |
| Plenum walls (1.5 mm, 25 % of area), tension | 12 MPa | 18 MPa | why the walls are 1.5 mm, not PSM-12's 1.0 |
| Separator over a 4.5 mm plenum (1.5 mm) | 14 MPa | 20 MPa | 2.0 mm separator if FEA asks |
| Header-bar top wall over 13 mm rib-split headers (3.5 mm) | 21 MPa | 31 MPa | ribs mandatory: an un-ribbed 30 mm span fails, as judges showed on CrossComb and LoopCore |
| Base between ties | negligible | negligible | tie spacing ≤ 1.2 mm under windows; 0.3 mm under kerfs |
| Perimeter land (≤ 4 mm unsupported, stepped 1.8 mm) | SF ≥ 3 on yield | | governs the external boundary |

Further mechanical results:

- **Unbonded-patch tolerance** at 1.0 mm base is about 12 mm (yield at 1.5 MPa). This sets the screen in 5.4.
- **Bow.** Pressure bow is zero. Mount bow plus thermal bow over a 50 mm die is about 4-25 + 6 µm at 300 N. At the 2 kN PCM clamp of the TTV it must be re-checked: scaled linearly it is 27-170 µm, too pessimistic because the tied stack is far stiffer than the free base. FEA in E1 decides.
- **Bearing points** are moved to within 10 mm of the heated area.
- **Thermal fatigue** amplitude in the base is about 11 MPa, covered by 1,000 power cycles.

**Leak-before-break.** The external boundary is ductile annealed copper with burst ≥ 3x MAWP. Internal layers see only internal dP plus tie loads, so a failed internal joint produces bypass, not a leak.

### 5.3 Flatness, mounting and the face

The die face is fly-cut after brazing to ≤ 20 µm over the heated area, Ra ≤ 0.8 µm. This also removes braze distortion: the plate is thick during processing and thin afterwards, a graft from CrossComb. The HBM pedestal step is cut in the same operation. Tier 2 adds masked electrolytic Ni of 3-5 µm on the contact face only.

Eight spring-loaded captive screws act on a stiff load frame. Retention is:

- 20-30 psi on the TTV;
- the package vendor's window (4-12 psi typical) on real modules;
- 6-15 psi on bare die, with stiffener hard stops that engage at 50 µm overtravel (graft from direct-to-die).

### 5.4 Inspection: what replaces C-SAM

Acoustic microscopy cannot resolve 0.15 mm fin-tip joints through the fin field or through a 10 mm annealed distributor, as all three judges noted. The production screen is therefore built from four other methods:

1. **Pressurised flatness scan during the 100 % proof test.** A confocal line scanner maps the base at 0 and 1.55 MPa; the difference removes the static shape. A 12 mm unbonded patch (the critical size) bulges about 3 µm and a 20 mm patch about 20 µm, against about 1 µm differential resolution, so detection at the critical size is marginal and must be validated in E1. Sampled plates are proofed at 2 MPa for more signal. Unbonded tips that still touch the land do not change flow, so the infrared screen cannot see them.
2. **100 % infrared flow-uniformity screen.** A 20→45 C water step at 10 LPM is imaged on the face in 30-60 s. It maps the flow through each inlet line and detects wicking blockage, cross-leaks between plenums and maldistribution. Equipment costs about US$0.15-0.25 M per line, or about US$1-2 per plate.
3. **100 % three-point dP versus flow**, with CpK ≥ 1.33, plus 100 % He leak at ≤ 1e-6 mbar·L/s (OCP requires 1e-5).
4. **Lot sampling.** CT and sectioning of witness coupons brazed in the same load, plus burst and a sampled TTV thermal test.

### 5.5 Process chain at volume

1. Shear OFE blanks.
2. Skive the fin field (3-4 min; 2-3 machines per 100k/yr), fly-cut tips to ±20 µm, gang-saw the kerfs (±0.05 mm), bright-dip.
3. Stamp the floor grate, meter sheet (orifices ±0.02 mm), separator and two plenum laminations (progressive dies, TW / VN / MX).
4. Forge and finish-CNC the header bar.
5. Ag-plate (route B) or place preforms (route A); vision-check every meter sheet.
6. Fixture the stack (≤ 0.2 MPa) and vacuum-braze at about 790 C, **30-80 plates per load** (fixture-limited, judge correction; about 1.5 furnaces per 100k/yr).
7. Fly-cut the face to 1.0 mm with in-line ultrasonic thickness gauging; cut the pedestal step; Ni-plate for Tier 2.
8. Fit guard and stubs; ISO 16232 flush; proof + pressurised flatness scan; He leak; 3-point dP; infrared flow screen; serialise.

Every step uses the supply base the Group-A houses already run. Two sources per process are qualified by M18.

### 5.6 Unit cost

Basis: copper corrected to the September 2026 LME (about US$14.4-14.7k/t, Westmetall and Cochilco, as cited by the judges), with OFE mill product at US$17-19/kg and scrap at about US$11.5/kg. Braze is fixture-limited at 30-80 plates per load, and the infrared screen is included. Accuracy is ±20 %; RFQs follow in month 1.

| Element (PRISM-15) | 10k/yr | 100k/yr | 1M/yr |
|---|---:|---:|---:|
| OFE copper (~2.5 kg buy, ~0.85 kg scrap credit) | 38 | 35 | 32 |
| Skived core + tip planing | 40 | 22 | 15 |
| Kerfing + deburr | 6 | 3 | 2 |
| Floor grate + meter sheet + separator (laser-cut → stamped) | 24 | 5 | 3 |
| Plenum layer (CNC → 2 laminations) | 30 | 4 | 2.5 |
| Header bar (CNC → forged) | 30 | 12 | 7 |
| Filler + clean | 9 | 5 | 4 |
| Vacuum braze | 25 | 16 | 10 |
| Post-braze fly-cut | 8 | 5 | 3 |
| Stubs + guard | 14 | 8 | 6 |
| Hardware | 20 | 14 | 10 |
| Test incl. infrared screen | 14 | 9 | 6 |
| Yield, scrap, overhead (18 / 15 / 12 %) | 46 | 21 | 12 |
| **Factory cost** | **~US$300** | **~US$160** | **~US$113** |

**Comparison with the incumbent.** A skived split-flow plate of CoolIT's class costs about US$175 / 110 / 75, with the copper correction applied. PRISM is therefore **about +45 % per plate at 100k/yr**.

**Per kW of capacity** limited by Tcase,max ≤ 85 C:

| Plate | TIM | US$ per kW |
|---|---|---:|
| PRISM-15 | PCM | 8.2 |
| CoolIT-like | PCM | 7.6 |
| PRISM-15 | paste | 9.6 |
| CoolIT-like | paste | 8.7 |

So PRISM is 8-10 % worse per kW. PSM-12's "17 % cheaper per kW" does not survive the copper and like-for-like corrections. The PRISM-G GPU-class plate is about US$120 against about US$105-110 at 100k/yr.

**The value case is facility-side, not plate-side.** At about US$0.8-2.0 M of dry-cooler capex per kelvin of supply temperature per 100 MW, PRISM's +7 to +11 K inlet headroom on 15 kW-class plates is worth far more than the plate premium. That premium is about 6,700 plates x US$50, or US$0.33 M, per 100 MW. For GPU-class plates the margin is +2-3 K, worth US$1.6-6 M against a premium of about US$1 M per 100 MW.

### 5.7 Height, mass and the 1U question

| Variant | Body | At the bar | Ports | Installed (estimate) | Mass |
|---|---|---|---|---|---|
| PRISM-15 | 14.9 mm | ~25.4 mm | vertical 20 mm | ~40 mm with fittings | ~1.6-1.75 kg |
| PRISM-15, dual 1/2-in pairs (UQD08-compatible, both-end-fed) | 14.9 mm | ~32 mm (13 mm horizontal bores) | horizontal | ~32 mm | ~1.7-1.85 kg |
| PRISM-G (Rubin class, 110 x 120 mm, 2-4 LPM) | ~11 mm (5 mm plenums) | ~19-21 mm | horizontal 10 mm at the bar ends | ~21 mm | ~0.85 kg |
| CoolIT 15 kW (estimate) | 10-13 mm | 22-28 mm | barbs on the bar | n/a | 1.2-1.6 kg |

The 15 kW TTV class is not a 1U-tray product for anyone. Its real homes are ASIC sleds, Kyber-class blades and 2U boards. The volume GPU-class plate fits the estimated 25-30 mm 1U budget above the lid with horizontal ports, which resolves the judge's drop-in objection for the primary socket. Height is therefore claimed at **parity** and mass as **slightly worse** (+0.1-0.5 kg); neither is claimed as a win. PSM-12's 29.5 mm bar with vertical 16 mm stubs (45-55 mm installed) is retired.

---

## 6. Performance predictions

All numbers come from the scoping model plus the three corrections in section 3.4. The Monte Carlo uses 20k samples with the synthesis conventions:

- h_eff ±25 %;
- TIM lognormal with P90 at the stated upper value;
- base ±10 %;
- hot-spot terms ±40 %;
- 2-D differential +0.5 ± 2 % of core (one-sided bias);
- ripple ±30 %.

"Footprint-fair" means our plate is evaluated at CoolIT's true footprint, drawn from a triangular distribution over 100 / 120 / 145 cm2, and compared with 34.4 / 44.2 K. That answers the judges' point that a self-chosen 117 cm2 TTV can flatter us.

### 6.1 The benchmark point

| Build | Avg P10 / P50 / P90 | Max P10 / P50 / P90 | P(avg < 34.4): at 117 / footprint-fair | P(max < 44.2) | P(beats CoolIT re-tested on the same TIM: avg / max) |
|---|---|---|---|---|---|
| PRISM-15, paste (like-for-like) | 27.4 / 30.6 / 34.7 | 34.2 / 37.7 / 42.0 | 0.88 / 0.90 | 0.97 / 0.96 | 0.90 / 0.96 |
| PRISM-15, PCM 25 psi | 26.2 / 28.7 / 31.7 | 31.0 / 33.7 / 36.9 | 0.99 / 0.98 | 1.00 | 0.97 / 0.99 |
| PRISM-15, PCM at module retention | 28.1 / 30.6 / 33.6 | 32.9 / 35.6 / 38.8 | 0.94 / 0.94 | 1.00 | 0.97 / 0.99 |
| PRISM-15, LM | 21.8 / 23.6 / 25.8 | 25.6 / 27.7 / 30.1 | 1.00 | 1.00 | 0.99 / 1.00 |
| PRISM-P, paste | 24.7 / 27.5 / 31.6 | 30.8 / 34.0 / 38.1 | 0.98 / 0.98 | 1.00 | 0.98 / 1.00 |
| PRISM-P, PCM | 23.5 / 25.6 / 28.3 | 27.7 / 30.0 / 32.8 | 1.00 | 1.00 | 1.00 / 1.00 |

These probabilities are model-term only. Process, schedule and TIM-identity risks are folded into the programme estimate in 10.4.

**Footprint sensitivity (deterministic).** At 100 cm2, the hard mode:

| Build | PRISM at 100 cm2 avg / max | Against |
|---|---|---|
| PRISM-15, paste | 34.0 / 41.7 K | CoolIT measured 34.4 / 44.2 |
| PRISM-15, PCM | 31.7 / 37.1 K | CoolIT re-tested on PCM 32.1 / 39.6 |
| PRISM-P, paste | 30.3 / 37.4 K | CoolIT measured 34.4 / 44.2 |

At 145 cm2: PRISM-15 paste 26.3 / 32.1 K. The like-for-like **average** win therefore disappears if CoolIT's heaters were 100 cm2. The maximum, dP, capacity and headroom wins hold at every footprint. This is why the public claim leads with the maximum, R'' per area, both TTV sizes, and the dP curve.

### 6.2 Flow, pumping-power and temperature trades (PRISM-15, PCM unless stated)

| Condition | PRISM-15 | CoolIT-like |
|---|---|---|
| 0.75 LPM/kW (the 65 C return floor), 11.25 LPM | 34.2 / 39.0 K at 2.5 kPa (paste 36.1 / 43.0) | 38.5 / 48.3 K |
| 1.0 LPM/kW (design point) | 30.3 / 35.1 K at 4.2 kPa (paste 32.2 / 39.1) | 35.8 / 45.6 K |
| 1.2 LPM/kW (benchmark) | 28.4 / 33.3 K at 5.9 kPa | 34.5 / 44.3 K at ~22 kPa |
| 2.4 LPM/kW (2x) | 24.0 / 28.8 K at 21.4 kPa | 31.0 / 40.8 K at 58-69 kPa |
| Equal pumping power (6.5 W, 28.5 LPM) | 25.1 / 30.0 K (paste 27.1 / 33.9; LM 20.0 / 24.0) | 34.5 / 44.3 K |
| Flow to match 34.4 K average | 11.1 LPM (0.74 LPM/kW, 0.46 W; outlet 65.5 C, at the return limit) | 18 LPM |
| Same with paste | 12.6 LPM (0.84 LPM/kW) | |
| Inlet temperature for Tcase,max = 85 C at 15 kW | **51.7 C** (paste 47.8; LM limited to 52.3 by the 65 C return) | 40.8 C |
| Q capacity at Tcase,max ≤ 85 C, 1.2 LPM/kW (20 mm ports) | 19.4 kW (paste 16.6; at module retention 17.9; LM 26.4; P + PCM 23.3) | ~12.9 kW (~14.8 re-tested on PCM) |

Corrections to PSM-12's figures:

- PSM-12's "53.6 C inlet headroom" implied a 66.3 C outlet, above the 65 C return limit. Every headroom figure here takes the lower of the thermal limit and the return limit.
- Flow and supply-temperature levers spend the same thermal margin, so they **are not additive** (graft from system-platform).

### 6.3 Real 2027-28 package: four 26 x 33 mm dies at 350 W/cm2 plus 16 HBM, zoned (2029+ stress case)

The hottest die cell uses the non-uniform heat-map fit plus our 2-D differential (+1.6 K for the 5 mm die-zone cell):

| Core in the die zone | Paste 0.05 | PCM | LM | Tcase,max with LM |
|---|---|---|---|---|
| CoolIT-like split-flow (2-D heat-map result) | 88.6 K | - | ~76 K | ~121 C |
| PRISM R, L 5 mm, 2.0 mm fins | 61.7 K | 63.4 K | 49.4 K | 94 C |
| PRISM R, L 5 mm, 2.5 mm fins (die SKU) | 60.4 K | 62.1 K | 48.1 K | **93 C** |
| PRISM-P die zone (≤ 33 µm loops) | 51.1 K | 52.9 K | 38.9 K | **84 C** |
| Tier 3 direct-to-die (lid and TIM1 removed) | | | | **~80 C**; about 28 K lower at the junction |

The drop-in R core does **not** reach 85 C at 350 W/cm2 over whole dies. It beats split-flow by 27-28 K. The analyst view of Rubin Ultra is about 87 W/cm2 die-average with 300-400 W/cm2 local spots, so this is a 2029+ key performance indicator, not a 2027 specification.

At realistic Rubin-class flux (2.3 kW on 16.6 cm2 of die, 88 % of the flow to the dies), PSM-12's indicative 1-D die-zone method corrected by our differential gives about 28.5 / 31.5 K (PCM) against 33.9 / 43.6 K for CoolIT-like. HBM junction temperature is 84-91 C on the stepped pedestal, against about 105 C on a split-flow plate whose HBM sits downstream of the dies.

### 6.4 GPU-class plates (1.4-4 kW) and CoolIT's 4 kW point

- **Uniform lids** (the convention CoolIT and the OCP may use): with flux-graded 12 mm cells PRISM wins narrowly (table 3.3: averages 14.2 / 15.5 / 16.6 K against 14.5 / 16.1 / 17.6 K; maxima 20.0-22.7 K against 21.7-25.1 K). With PSM-12's 4 mm cells it would lose the average by 1.9-2.7 K. PRISM-G plate dP is about 2-3 kPa, because the meter is sized for uniformity at GPU flows. That is parity with the scaled reconstruction (1.5-4 kPa) and well below the about 12 kPa published for market GB300 plates; dP is not a GPU-class differentiator.
- **Die-concentrated packages** (B300 / Rubin / Rubin Ultra with zoning): PRISM wins at the die by 4-15 K (6.3).
- **CoolIT's measured 4 kW plate** (50 x 50 mm, 6 LPM, < 0.009 C/W max-case incl. TIM):

| PRISM build at 25 cm2 | Max-case R |
|---|---:|
| R-grade, PCM | 0.0093 C/W (0.0091 with a 0.8 mm base) |
| R-grade, paste | 0.0105 C/W |
| R-grade, LM | 0.0074 C/W |
| P-grade, PCM | 0.0081 C/W |

  This is the one CoolIT-disclosed point where the drop-in core only **ties with PCM and loses with paste**. At a small single-die footprint split-flow's half-length is only 25 mm, so its ramp penalty is small, while convection at 160 W/cm2 dominates. The manifold advantage grows with footprint and with heat-map non-uniformity. For ≤ 25 cm2 single-die plates we therefore sell Tier 2 or the P-grade, or we do not claim a win.

### 6.5 15-30 kW and wafer-scale

| Case | PCM: avg / max (Tcase,max) | LM: avg / max (Tcase,max) | Notes |
|---|---|---|---|
| 25 kW on 117 cm2 | 41.4 / 48.5 K (94 C) | 32.9 / 38.5 K (83 C) | |
| 30 kW on 150 cm2 | 39.3 / 46.1 K (91 C) | 31.3 / 36.7 K (82 C) | above about 20 kW per 117 cm2 the product is Tier 2 or P-grade |
| 20 kW wafer-scale on 460 cm2 (8 mm cells) | 16.2 / 19.1 K | | flow length is independent of size, so the plenum tiles simply repeat with one port pair per ~110 mm; split-flow cannot scale this way |

### 6.6 Power electronics (positions corrected by the judges)

| Product | Honest position |
|---|---|
| PRISM-DC direct-substrate cartridge (R core, Ag-sintered AMB, PG25 or DI loop) for SST, 800 VDC conversion and solid-state breakers | Core-only gain about 1.38x the loss per cm2 of SiC at equal sinter interface, not 1.8x: the rest of PE's headline was the sinter replacing PCM, which any plate can do. Sell power density and lower Tj for power-cycling life, not die-area savings. Demonstrate by Vsd(T) against a pin-fin module on the same housing. |
| PRISM-DC shelf plate (gap-pad or PCM interface) | The interface dominates (6-7 K plate-to-plate difference at 400 W). Value lies in the keyed orifice and rack-kit integration, not thermal performance. |
| SiC traction (licence only) | Gain -9 to -25 %, mostly from fin area; dP at parity in the same housing (the PE proposal compared unlike housings). Not drop-in: needs a module-vendor baseplate and a new housing manifold. Features ≥ 0.5 mm in WEG / Al loops; cold case -30 C. Net value about US$0-40 per inverter; royalties about 2030-31. |

### 6.7 Where PRISM does not win, and why that is acceptable

| Metric | Result | Why acceptable / what we do |
|---|---|---|
| Factory cost per plate | +45 % (US$160 vs ~110 at 100k); +8-10 % per kW | The facility value is worth about 15-60x the premium per 100 MW for 15 kW-class plates (+7-11 K inlet) and 1.5-6x for GPU-class plates (+2-3 K). We sell TCO and offer a 1M/yr cost-down path (~US$113). |
| Field track record | none | Independent-lab repeat, published CpK, 1,000-h fouling data before any life claim |
| Mass | ~1.6-1.75 vs est. 1.2-1.6 kg | immaterial to buyers; border pocketing |
| Average at a 100 cm2 footprint, like-for-like paste | parity | lead with maximum, R'' per area, dP; test on both TTV sizes |
| 4 kW single-die point, drop-in core | ties with PCM, loses with paste | Tier 2 / P-grade for small high-flux dies |
| 350 W/cm2 over whole dies, drop-in core | 93 C (misses 85 C) | P-grade / direct-to-die; 2029+ case |
| Filler-free construction | no (Ag-Cu fillets) | declared; laser-welded outer seam option |
| 10-year fouling life | not claimed until E4 + pilot | engineered ladder (4.4) |

---

## 7. Applications and market entry

### 7.1 Ranked applications and what changes

| Rank | Application | PRISM variant | What changes | Entry timing |
|---|---|---|---|---|
| 1 | Hyperscaler custom AI ASICs (large multi-die packages; TPU / Trainium / Maia class; buyer owns package, tray and loop; allows 80 psi and a tray filter) | PRISM-15 or PRISM-G, zoned; P-grade over the dies with the tray filter; Tier 3 bare die later | meter artwork + plenum laminations per heat map (2-3 weeks); tray cartridge | samples M12-15; qualified M18; volume 2028 |
| 2 | NVIDIA Rubin Ultra / Feynman-class lidded plates (2-6 kW) | PRISM-G, T1 PCM, then T2 LM on the Au/Ni lid | MGX tray envelope; horizontal 10 mm ports; ≤ 21 mm at the bar | through a Group-A/B manufacturing partner; platform design freeze about 12 months before ramp, so realistically Feynman (2028), with volume from 2029 |
| 3 | 15-30 kW multi-die modules, superchip boards, Kyber-class blades | PRISM-15, T2 LM above 20 kW | dual UQD08 or 3/4-in plumbing | 2028 |
| 4 | Wafer-scale / multi-chip / system-on-wafer | PRISM-W tiles | repeated plenum tiles, port pair per ~110 mm, per-die pads | on demand |
| 5 | CPU, NVSwitch, co-packaged optics switches | PRISM-S | uniform 16-24 mm pitch; optics zones fed first (±3 K) | opportunistic, in the same rack kit |
| 6 | 800 VDC in-rack power (Kyber 2027+), SST front ends, solid-state DC breakers | PRISM-DC (direct-substrate cartridge or keyed-orifice shelf plate) | Ag-sinter interface; keyed orifice; same PG25, OCP test matrix and customers | 2028 |
| 7 | SiC traction inverters, chargers | PRISM-A (licence) | coarse ≥ 0.5 mm grade, Al-compatible or Ni-plated, AQG 324 | licence term sheet 2028, vehicles about 2030-31 |
| 8 | Laser diodes, RF GaN, directed energy | P-grade + CVD-diamond insert ≤ 2 cm2 | DI water, Au/Ni | niche, high margin |

**On "SSD converters".** The mission's power-electronics list almost certainly means **SiC** converters, covered by ranks 6-7. Two other readings are also addressed:

- **Solid-state transformers and solid-state breakers** for 800 VDC: about 15-25 kW of heat per MW on isolated substrates. They fit PRISM-DC well.
- **SSD storage** (E1.S / E3.S, 25-40 W, about 1-2 W/cm2): pads and serviceability dominate and the core solves nothing. Excluded.

### 7.2 Go-to-market path and business model

The judges found that every proposal's licensing story lacked a moat. The concept practises expired Harpole / Cooligy art and every process is second-sourceable, so patents cannot protect PRISM against Group-A houses after a full OCP disclosure. PRISM therefore uses a build-and-partner model:

1. **Beachhead: hyperscaler ASIC programmes.** We co-design the zoned plate, tray filter and data pack, and supply plates built by a contract manufacturer (a Western CM or a non-Group-A Taiwanese or Vietnamese skive-and-braze house) under our process recipe, our inspection and our test cell. Buyers who own the package and the loop are the only ones who can adopt the P-grade or a bare-die tier quickly.
2. **NVIDIA volume through a manufacturing partnership.** NVIDIA buys Rubin plates centrally from Group-A (Jentech, AVC, Cooler Master, Delta; about US$400 per assembly, US$200-260 bare). We offer a Group-A or rumoured Group-B house a know-how-plus-supply agreement (recipe, fixtures, infrared screen, zoning tool, engineering), not a bare patent licence. CoolIT is absent from Group-A.
3. **OEM kits** (Dell, HPE, Lenovo, Supermicro): plates, tray filters and the 63 mm rack manifold, sold on facility value.
4. **Transparency as the marketing weapon.** A full OCP v1.0.0 report, independent-lab repeat, and dP at three boundaries. This is the axis CoolIT, as the spec's author, cannot dismiss.

**What actually protects the position**

- the tie-braze recipe and its two filler routes (trade secret);
- the infrared and pressurised-flatness inspection methods;
- the heat-map-to-artwork zoning tool and its two-week turnaround;
- calibrated test data and the independent repeat;
- customer co-design relationships.

Narrow patents (section 9) are defensive. **Margin realism:** a Group-A gross margin of 17-20 % at a bare-plate ASP of about US$200-260 cannot carry a +45 % factory cost through a pure licence. The economics close only where facility value is priced in, which is the hyperscaler TCO purchase.

---

## 8. Reliability, qualification and compatibility

### 8.1 Drop-in checklist

| # | Requirement | PRISM-15 position |
|---|---|---|
| 1 | OCP thermal metric | R at ≥ 6 flows (0.5-1.5 LPM/kW) with the OCP recommended TIM *and* paste; R'' per area; two TTV sizes (117 and 100 cm2) |
| 2 | OCP dP | ≥ 6 points over 25-150 % of the 15 LPM rated flow, 45 ± 2 C, three boundaries (port bore stated, + barbs and hose, + named UQD08 pair) |
| 3 | Pressure | MAWP 150 psi; proof 1.5x on 100 % of parts; burst ≥ 3.1 MPa design, ≥ 4.5 MPa sample; vacuum to -0.9 bar(g) |
| 4 | Leak | He ≤ 1e-6 mbar·L/s, 100 % |
| 5 | Cycling | 1,000 cycles at 10-65 C operating; 50 cycles at -40 / +70 C storage; 10,000 pressure cycles 0-MAWP; 1,000 power cycles; drift ≤ 5 % in R and ≤ 10 % in dP |
| 6 | Coolant, temperature | OCP PG25, rated at 45 C (W45) and characterised at 50 C (W+); outlet ≤ 65 C stated with every headroom figure; water as secondary curve |
| 7 | Couplings | OCP UQD v2.0.0 UQD08 / UQDB08 (dual pairs for 15 kW); no non-standard "UQD12" |
| 8 | Wetted materials | OFE Cu, Ag-Cu braze fillets (declared), 316L, peroxide-cured EPDM, PTFE; no Al, Zn, NBR or silicone; Ni only on the contact face (T2) |
| 9 | Filtration | ladder in 4.4; the channel rule is published as a specification line |
| 10 | Velocity | ≤ 1.5 m/s in ports and headers and ≤ 2.0 m/s at the meter at 150 % of rated flow; fin entry ≤ 0.5 m/s |
| 11 | Mechanical | flatness ≤ 20 µm, Ra ≤ 0.8 µm; load inside the package window; hard stops on bare die |
| 12 | Cleanliness / soak | ISO 16232 flush; 3,000 h PG25 at 65 C with coupons; Cu ions tracked |
| 13 | Beyond OCP | 1,000 h dosed particulate challenge; clustered-blockage probe; meter erosion test |
| 14 | Quality | PFMEA, control plan, MSA, CpK ≥ 1.33 on leak and dP, PPAP-style package, serialised infrared and dP records |
| 15 | Reporting | 3 plates x 3 re-mounts, k = 2, plate-to-plate spread ≤ 2 K as a KPI, independent repeat |

**Open compatibility risk: a mandated Ni-plated wetted path** (reported on GB200-class plates, secondary sources). Pre-braze electroless Ni-P does not survive a 790 C BAg cycle, and post-braze flow-plating through 0.15 mm gaps has poor throwing power. Route C (TLP at 600-700 C) with pre-plated electrolytic Ni is the only candidate. Carried as R7 with an E1 sub-test; meanwhile we argue from the OCP wetted list, where Ni plating is practice, not a requirement.

### 8.2 Fouling strategy and service life

Fouling is handled by the filtration ladder (4.4), the passage hierarchy, dead-end bleeds and slot ends kept outside the die, plus a dP signature on every plate. The R-grade has a **10-year design-life target**, claimed publicly only after:

- E4: 1,000 h dosed challenge behind the guard, with core dP drift ≤ 10 % and average dT drift ≤ 1 K;
- a field pilot.

The relative-life band behind 50 µm absolute is 0.6-1.2x a skived 0.2 mm plate. The P-grade is about 0.6x unless a ≤ 25 µm tray cartridge is used. PCM is field-replaceable. LM (T2/T3) is a factory pre-wetted, capped field-replaceable unit with a 5-year inspection interval.

### 8.3 Tier 2 / Tier 3 specific rules (graft from direct-to-die)

- **Liquid-metal containment as a designed subsystem:**
  - 3-5 µm electrolytic Ni (never high-P electroless Ni on the heat path) or a 1 µm sputtered W barrier;
  - no Au anywhere on the plate face;
  - FKM dam and capture moat;
  - conformal coat on passives within 5 mm;
  - Galinstan where -40 C storage applies;
  - porosity test.
- **Bare die:** load-limited kinematic float at 6-15 psi on the dies; stiffener hard stops for shock; HBM is never a bearing surface (≥ 30 µm gap).
- **Gating evidence:** a TTV-C real-silicon test vehicle (diode dies tiled 4x on a warping 120 mm substrate with HBM dummies) is the only acceptable proof of junction-level claims.
- **No public data above about 10 cm2:** no LM reliability data exist above about 10 cm2, so Tier 2 is published as stretch data until our own 1,000-cycle warped-package results are in.
- **Gallium supply:** about 2 g per plate; dual non-Chinese and recycled sources; 12-month stock.
- **Micro-channel-lid inserts (T3B, graft from advanced-manufacturing):**
  - the indium TIM1 bond line scales with lid CTE mismatch: about 259 µm for a Cu lid against 79-88 µm for a 7 ppm/K lid, and about 130 µm once qualified to -40/+125 C;
  - fins on CTE-mismatched substrates are segmented into strips of ≤ 2 mm;
  - diamond is used only in hot-spot inserts of ≤ 2 cm2 (-5 K Cu-diamond, -12 K CVD on a 2 x 2 mm, +650 W/cm2 patch).

---

## 9. IP posture

This section is not a legal opinion. Claim text has not been read for most families, and outside counsel must confirm everything below.

### 9.1 What we must avoid or clear

| Family | Status | PRISM position |
|---|---|---|
| **CoolIT Split-Flow**: US 8,746,330, 9,603,284, 12,495,513 (2008 parent); 9,057,567 (claims revived when the Federal Circuit vacated the PTAB decision, *CoolIT v. Vidal*, 7 Mar 2024); CIP 9,453,691 (filed 21 Feb 2012) and its continuations 11,994,350 and 12,460,878 (issued 4 Nov 2025); 12,101,906 (unknown scope) | Parent-family claims run 11 Aug 2028 to about mid-2031 depending on PTA. **Claims relying on the 2012 CIP matter run to about Feb 2032 plus PTA.** CoolIT enforces competently and Ecolab can fund it. | **Design-ins:** kerfs at every inlet *and* outlet line, so each fin segment runs one way and no channel has an inlet between its ends; interior outlets only; distribution in separate stamped laminations; zones split by solid walls; a dated memo maps each feature to expired Harpole US 5,088,005 and Cooligy US 6,986,382 / 7,156,159 / 7,104,312 / 7,000,684. **Claim chart on the whole family incl. the CIP branch (US$40-80k) at M2-4; no US sale before the opinion.** Non-US deliveries are not blocked (no foreign counterparts recalled). |
| Microfabrica US 12,255,123 (hybrid microjet + microchannel micro cold plate, priority Mar 2021, to ~2042) and parent family US 9,953,899 etc. (to ~2036) | live | The meter orifices discharge into a 1.0 mm recessed window and kerf, which is distribution rather than jet cooling of the heat-exchange surface. The 2-D credit we take for kerf-floor impingement is small (h 15 kW/m2K over 5 % of the area). **Claim-chart before freeze.** Fallback at about 0 K cost: offset the orifice rows ≥ 0.4 mm from the kerf so the jets land on the grate lip. Sung and Mudawar (Purdue, 2006-09) and IBM distributed-return jets are prior art for validity. |
| JetCool / Flex (US 10,665,529, 11,018,077, 11,594,470, 12,432,878, 11,191,184, 11,277,937) and Frore (unpublished) | live to 2037-45 | No open cavity onto the package, no series re-impingement, no jets on the die; parallel zones. Checked together with Microfabrica. |
| CoolIT compliant-member family (11,725,886 / 12,188,733) | live | rigid stepped base; the Tier 3 float is a conventional spring-screw gimbal (IBM TCM US 3,993,123 is prior art) |
| NVIDIA "intelligent" plates; CoolIT in-plate leak sensing 9,052,252 | live | the plate is passive, with no sensors or valves; telemetry, if wanted, lives in the tray |
| NVIDIA AlN-heater TTV (US 12,446,195) | live | our TTV is internal test equipment built from commercial heaters; claims checked in month 1 |
| Toyota double-sided MMC cards (US 11,849,569 / 11,596,088, to ~2040-41); HUST US 12,178,022; Danfoss ShowerPower 3D | live | PRISM-DC is single-sided direct-substrate; no meanders or swirl; double-sided power cards are out of scope until cleared |
| Purdue HMMC, IBM Zurich MMC (2008-19 filings), Mikros / Jabil laminates, Alloy Enterprises stack forging | live if granted and maintained | stamped and brazed (not diffusion-bonded etched laminates); include in the M2-4 search |

### 9.2 What we file (provisionals before any disclosure, PCT after)

1. A tied, skived manifold plate whose fins are kerfed at every inlet and outlet line, under a recessed window, fed by a separately stamped orifice meter that sits off the braze plane.
2. The flux-graded flow-length rule: cell length per zone chosen from local flux to minimise caloric + convective + ripple terms (4-12 mm).
3. The production verification of tie bonds by pressurised flatness scan during proof, plus the infrared flow-uniformity fingerprint (process claims; also kept as trade secrets in detail).
4. The tray-to-plate filtration ladder with a published channel rule (gap ≥ 3x the last filter's absolute rating).
5. A defensive publication of the benchmark-proxy TTV method.

These are narrow by design. The moat is know-how and data (section 7.2). The FTO search and opinion on about 12 families is budgeted at US$80-140k.

---

## 10. Risks, experiments and roadmap

### 10.1 Risk register (ranked) with pre-modelled fallbacks

| # | Risk | Likelihood / impact | Early warning | Fallback (modelled) |
|---|---|---|---|---|
| R1 | Fin-tip tie braze: voids, wicking into 0.15 mm gaps, kerf damage | medium / programme-critical | E1 at M3: sectioned bond < 70 %, > 1 % channels blocked by infrared, burst < 4.5 MPa | Route B → C (TLP) → D (low-pressure DB). Then a 1.5 mm base (still tied; PCM 30.0 / 34.9 K, paste 32.0 / 38.8 K: still beats on max, dP and capacity). If kerfing damages fins: skip the kerfs, at +0.6 K (L 6 mm, 2-D) and with a weaker Split-Flow design-around. |
| R2 | Uniformity worse than 1.10 | low-medium / +1-2 K on max | E2 water table at M3 | re-artwork the meter (+0.5-1 kPa); centre-fed plenum variant (1.04) |
| R3 | 2-D penalty larger than modelled | medium / +1-2 K | printed-manifold rig at M2-3; TTV data at M5 | 8 mm cells on the TTV (-0.6 K average); P-grade die zone |
| R4 | Benchmark ambiguity (footprint, "case", TC bias) used against us | high / claim credibility | reviewer feedback | both TTV sizes; R'' per area; AlN bias published; purchased incumbent plates on our rig; standing offer to test any CoolIT plate |
| R5 | OCP recommended TIM is a paste, not PCM | medium / average margin halves | read the OCP PDF in month 1 | lead with maximum, dP, capacity; controlled-bond-line paste data; P-grade stretch |
| R6 | Fouling and impaction at kerf floors; meter erosion | low-medium / life claim | E4 | no life claim until data; offset orifices; tray cartridge mandatory for P-grade |
| R7 | Customer mandates a Ni-plated wetted path | medium / socket access | early ODM / hyperscaler SOW reading | TLP route C with pre-plated Ni; argue from the OCP list |
| R8 | IP: Split-Flow CIP branch, Microfabrica, JetCool | medium / US launch timing | claim chart at M2-4 | design-ins in 9.1; non-US deliveries first; launch after the opinion |
| R9 | Cost above US$190 at 100k | medium / channel | RFQs at M1 | border pocketing, forged bar, fewer laminations; target US$145 by Gen-2 |
| R10 | TTV heaters at 128-155 W/cm2 crack or bias | medium / schedule | commissioning at M3-4 | two heater suppliers; Cu-block TTV-A2 |
| R11 | Supplier capacity (skiving and braze in the AI boom) | medium / schedule | RFQ responses at M1 | two skiving + two braze houses; laser-cut and CNC prototype parts |
| R12 | CoolIT publishes a better plate first, in its own format | medium / marketing | market | the Tier 2 and P-grade data held in reserve; transparency package |

### 10.2 Experiments that retire the most risk

| # | Experiment | When / cost | Pass criterion | Retires |
|---|---|---|---|---|
| E0 | Buy 2-3 incumbent GPU plates and named UQD08 / UQDB08 pairs; measure R, dP and Cv on our rig (graft: system-platform, risk-first) | M0-2 / US$40k | rig repeatability ≤ 1 K; Cv recorded | R4; coupling budget |
| E1 | Tie-braze coupon matrix: 60 x 60 mm kerfed RF-15 cores x routes A / B / C x 2 fixture loads (24 coupons + 2 full plates); sectioning, CT, pressurised flatness, infrared, pull, burst, fly-cut flatness; Ni-wetted sub-test | M0.5-3 / US$80k | land bond ≥ 70 % overall and ≥ 40 % in any 10 mm cell; ≤ 1 % channels blocked; burst ≥ 4.5 MPa; flatness ≤ 20 µm | R1, R7 |
| E2 | Printed-manifold development rig (graft: advanced-manufacturing): clear-SLA water table of plenums, meter and headers, plus a printed or CNC manifold bolted on a **2.5 mm-base** kerfed skived core with a metal C-seal (thick base because an untied 1 mm base bows); dye, taps, thermal | M1-3 / US$90k | max/min ≤ 1.10 at 18 LPM, ≤ 1.12 at 27 LPM; convection within ±15 % of model | R2, R3 |
| E3 | TTV commissioning and TIM metrology: TTV-A = 4 AlN tiles of 54 x 54 mm = 116.6 cm2 (15 kW at 129 W/cm2, 83 % of the 155 W/cm2 rating, 18 kW limit; PSM-12's 53 mm tiles gave only 112 cm2) and TTV-100 = 4 x 50 mm tiles (hard mode); edge-fed benchmark proxy (matches the *average* only); D5470 at 25 psi and at module retention for PCM, paste and LM | M2-5 / US$140k | heat capture ≥ 98 %; re-mount repeat ≤ 1 K | R4, R5, R10 |
| E4 | Fouling, impaction and erosion: quarter-scale plate behind the guard (± tray cartridge); PG25 dosed with ISO 12103 dust, Cu oxide and EPDM at 10-100x loop levels; 1,000 h at 65 C; meter orifices at 1x / 1.5x / 2x | M3-10 / US$100k | core dP drift ≤ 10 %; average dT drift ≤ 1 K; no kerf-floor clustered blockage; no measurable orifice wall loss | R6 |
| E5 | Endurance on first articles: 1,000 power cycles, 10,000 pressure cycles, 2,000 h soak, then burst | M5-11 / US$150k | R drift ≤ 5 %, dP ≤ 10 %, He-tight, burst ≥ 4.5 MPa after cycling | ties and qualification |
| E6 | IP: continuity, PTA and claim reads, then claim chart and opinion (Split-Flow incl. CIP, Microfabrica, JetCool) | M1-4 / US$80-140k | clear or designed-around | R8 |

### 10.3 Roadmap and gates (M0 = November 2026)

| Months | Work | Gate |
|---|---|---|
| 0-1 | RFQs (2 skiving, 2 braze, stamping, forging); long-lead rig items; read the OCP PDF (TIM, case, boundaries); FTO step 1; provisionals drafted | - |
| 1-3 | E0, E1, E2; CFD of meter, window and kerf; detailed design | **G1 (M3) Rev A freeze**: join route, base (1.0 / 1.5), cell length, meter artwork |
| 3-5 | Build A (12 plates; laser-cut and CNC parts); TTV commissioning; E3; E4 starts | - |
| 5-6 | Internal parity: 3 plates x 3 assemblies, PCM and paste, both TTVs | **G2 (M6)**: commit publicly only if measured PCM is ≤ 31 K average and ≤ 36 K maximum, and paste ≤ 33 K average; decide on the P-grade kit (D1) |
| 6-9 | Build B (20 plates at the production-intent braze house, stamped parts); E5; independent-lab repeat booked; TTV-B (die-realistic, zoned) | **G3 (M9)**: repeat within ±1.5 K |
| 9-12 | OCP-format report and white paper; TTV-B data; P-grade and Tier 2 stretch data; provisionals converted | **G4 (M11-12)**: public at OCP Global Summit (4-7 Oct 2027) |
| 12-18 | Build C pilot (150 plates at the CM); full qualification matrix; PPAP; samples to two hyperscaler ASIC programmes and one Group-A/B partner; FTO opinion; PRISM-G zoned and PRISM-DC samples | **G5 (M18)**: qualified product |

### 10.4 Staffing, budget and probability

- **Team:** 14-15 FTE: programme lead, thermal-fluids 2, mechanical / FEA 2, manufacturing and supplier 2, test lab 3, reliability / materials / fouling 1.5, quality 1, applications / OCP 1, IP coordination 0.5.
- **12-month budget, about US$6.6 M (±15 %):**

| Item | US$ M |
|---|---:|
| Labour | 3.3 |
| 25 kW PG25 rig | 0.45 |
| TTVs, incl. the 100 cm2 hard-mode variant | 0.3 |
| Flow, printed-manifold and fouling rigs | 0.23 |
| Infrared flow-screen station | 0.2 |
| Prototypes and coupons | 0.35 |
| Reliability | 0.25 |
| Independent lab | 0.15 |
| IP | 0.25 |
| Contingency 20 % | 1.1 |

- **Months 12-18:** US$3-3.5 M (tooling, pilot, PPAP). **18-month total US$9.5-10 M.**
- **Probability (judgement, all risks):**
  - about 0.75 for "beats CoolIT on average, maximum and published dP with PCM" in public at M12;
  - about 0.6 for the decisive result (PCM ≤ 31 / ≤ 36 K measured) at M12;
  - about 0.75-0.8 for a footprint-fair like-for-like paste average win.

  The dominant failure mode is a 1-3 month slip at E1 or TTV commissioning, not a thermal miss. PSM-12's 0.7 / 0.98 were model-only and are withdrawn.

---

## 11. Appendix

### A. Proposals considered, scores, and disposition

| Key (title) | Mean (physics / mfg / strategy) | Taken into PRISM | Why it did not win as written |
|---|---|---|---|
| **risk-first-12mo** (PSM-12) | **61.3** (62 / 59 / 63) | **Base architecture**: skived core, single braze, tied 1 mm base, centre bar, gated 12-month programme, two filler routes, transparency package, claims-we-will-not-make, proxy and purchased plates, R'' per area | Meter at the braze plane; 1.32 m/s fin-entry jet; gang-slit closed plenums not machinable; uncorrected copper cost; 29.5 mm bar with vertical stubs; FTO timing; model-only probabilities |
| advanced-manufacturing (AM-Gated HMMC) | 60.3 (63 / 57 / 61) | printed-manifold rig (E2); fin-conduction ceiling; AM route screen and contamination rules; CTE-matched lid rules; dP signature | one-shot diffusion bond crushes fins (25-50 MPa at tips); 18 mm height not closed; X module ties bare-die LM; no go-to-market |
| power-electronics (HMMC-X) | 59.7 (63 / 57 / 59) | keyed inlet orifice; grade ladder by filtration; direct-substrate SiC module; galvanic rules; Vsd(T) demonstrator | PE dP and 1.8x claims compared unlike housings and comparators; automotive not drop-in; channel conflict (Delta, Flex, Jentech); IP anticipated |
| conventional-cost (CrossComb) | 59.2 (58.5 / 60 / 59) | fly-cut-after-braze base; 100 % three-flow dP with CpK; stamped selector floor (→ meter sheet); laser outer seam; warm-water TCO pitch | gang-slit closed slots impossible; along-slot ratio 3.6 vs 15; tie stress SF 1.4; screen undersized; cost understated |
| jet-hybrid (JetFin) | 56.7 (57 / 55 / 58) | swappable-insert coupon; inertial branch rule; leak-before-break by construction; artwork zoning | jet increment (~1 K) inside model noise; impaction / erosion; Microfabrica US 12,255,123; bond creep; no route to volume |
| direct-to-die (DD3) | 56.3 (55 / 56 / 58) | tier set by face finishing; LM containment subsystem; float + hard stops; crowned pedestal; TTV-C; manifold-cap end-state | lead tier depends on unqualified 80-150 cm2 LM; TIM1 liability; no Nvidia socket; headline was an interface swap |
| system-platform (LoopCore) | 56.0 (56 / 54 / 58) | filtration ladder + commissioning protocol; keyed-orifice rule; 63 mm U-manifold; non-additive levers; E0; VR skirt (~11 % of flow) | 2.5 mm cover over 29-43 mm troughs fails proof; tray-module telemetry blind to clustered fouling; not drop-in in NVIDIA's channel |
| hmmc-elite (HMMC-E) | 54.7 (51 / 56 / 57) | interface tiers, no grease on ≥ 100 mm lids; HBM pedestal; hole-density zoning; coupling class in every dP claim | 3.3 mm openings over 0.7 mm walls short-circuit about 70 % of the flow (+10.8 K in 2-D); tie stress 43-86 MPa; diffusion bond infeasible; no Ni route |

### B. Judge-flagged fatal flaws of the winning direction (PSM-12) and their resolution

| Flaw (judges) | Resolution in PRISM | Status |
|---|---|---|
| "Beats in every aspect" not defensible (height, mass, low-flux GPU average, 350 W/cm2, cost, record, fouling) | Metric classes A-D with OCP as arbiter (1.2). Height brought to parity (25 mm at the bar; GPU-class 20 mm, horizontal ports). Low-flux GPU average turned into a narrow win by flux-graded cells (3.3). 350 W/cm2 framed as a 2029+ KPI where we beat CoolIT by 27 K. Cost, mass, record and the 4 kW tie stated openly (6.7). | resolved / disclosed (D1) |
| Headline win comes from the TIM | Like-for-like rows lead: paste 30.4 / 37.2 K; PCM against CoolIT re-tested on PCM 28.4 vs 32.5 K average. Footprint-fair Monte Carlo published. Average parity at 100 cm2 disclosed. | resolved; residual risk R5 |
| Meter slit sits where fillets, wicking and burrs form | Meter moved to a stamped sheet 1.0 mm above the braze plane, ≥ 0.35 mm from any joint, vision-inspected before braze, infrared-verified after | resolved (verify E1 / E2) |
| Installed height 45-55 mm; no 1U home | 20 mm vertical ports on a 10.5 mm bar for the 15 kW class (not a 1U product); PRISM-G ≤ 21 mm with horizontal ports for 1U | resolved |
| Enabling braze has no precedent and no inline NDT; fallbacks all need ties | Four join routes incl. TLP and low-pressure DB; pressurised flatness scan + infrared screen + coupon CT / sectioning replace C-SAM; 1.5 mm-base fallback modelled (still beats on max, dP, capacity) | carried as R1 (gate M3) |
| Cost case does not survive correction | Rebuilt with September 2026 copper and fixture-limited braze: US$160 at 100k (+45 % vs incumbent), +8-10 % per kW | disclosed (D1) |
| FTO timing wrong (CIP to ~2032; *CoolIT v. Vidal*) | Whole family listed; kerf design-in; claim chart before any US sale | carried as R8 |
| Licensing has no moat | Build-and-partner model; moat = recipe, inspection, zoning tool, data (7.2) | resolved in model (D2) |
| P(decisive) 0.7 / 0.98 model-only | Footprint-fair Monte Carlo; programme probabilities 0.6-0.8 by judgement | resolved |
| 2-D bias +0.8-1.7 K; U1 3 mm fins a penalty; PCM at 15 psi optimistic; ripple 1-1.5 K | Kerfs + 6 mm cells bring the 2-D differential to 0 (cell2d); taller fins rejected (+0.4 K at 2.5 mm in 2-D); PCM at 25 psi on the TTV and 0.07 on packages; ripple crest counted in full (1.85 K) | resolved |

**Flaws of the other proposals that matter for the grafts:**

- **Diffusion-bond fin crush** (AM, PE, JH, DD3, HMMC-E). No route exceeds about 1 MPa at the fin tips.
- **Hele-Shaw bypass** (HMMC-E; all comb designs). Narrow recessed windows + kerfs; quantified in 3.2.
- **Undersized plate screens** (CrossComb, LoopCore, DD3, PE). Ladder with tray-level primary filtration.
- **Cover and header spans** (LoopCore, CrossComb). Rib-split headers, 1.5 mm walls, separator span 4.5 mm (5.2).
- **Liquid-metal containment and TIM1 liability** (DD3). Tier 2 / 3 stay stretch tiers until our warped-package cycling data exist; the first bare-die socket is a hyperscaler owning package and plate.
- **Jet IP and erosion** (JH). No jet cooling; meter ≤ 1.71 m/s at 150 % of rated flow; fin entry 0.41 m/s; Microfabrica, JetCool and Frore claim-charted.
- **PE claim inflation** (PE). Corrected positions in 6.6.
- **AM single-source, X-module economics** (AM). AM is development-only, plus niche housings.

### C. Disputed numbers, re-derived

| Number in a proposal | Re-derived (this draft) | Basis |
|---|---|---|
| PSM-12 28.4 / 31.4 K (PCM) | 30.3 / 34.2 K as proposed; **PRISM 28.4 / 33.3 K** | 2-D differential +1.9 K for slit-at-tips (cell2d vs CoolIT 2-D +6.9 %); ripple crest |
| PSM-12 paste 30.4 / 35.4 K | PRISM 30.4 / 37.2 K | same; paste scatter 3.5 K + ripple 1.85 K |
| PSM-12 dP 5.6 kPa | PRISM 5.9 kPa (20 mm ports) / 8.2 kPa (16 mm) | element budget with port K 3.5, windows, meter Cd 0.72 |
| PSM-12 meter 1.6 kPa from the slit | about 0.5 kPa for a recessed slit; the 1.6 kPa came from the fin-entry jet | slit loss K ≈ 2.3 at 0.66 m/s; plenum model needs ≥ 2 kPa |
| "Every passage has precedent; 1 development item" | 2 items remain (tie braze; stamped meter + kerf) plus process qualification of the infrared screen | 5.1-5.4 |
| Q capacity 21.1 kW (PCM) | 19.4 kW (PCM, 25 psi); 17.9 (module retention); 16.6 (paste); CoolIT ~12.9 / ~14.8 on PCM | flux-scaled terms incl. ripple and scatter |
| Inlet headroom 53.6 C | 51.7 C (limited by the 65 C return for LM: 52.3) | min(thermal, return) |
| Flow to match 34.4 K: 11.1 LPM | 11.1 LPM (PCM, outlet 65.5 C); 12.6 LPM paste | prism_flow.py |
| Cost US$148, 7.0 $/kW | US$160 ± 20 %; 8.2 $/kW PCM vs 7.6 (CoolIT on PCM) | prism_cost.py; corrected copper |
| GPU-class average loses 0.5-2 K | 4 mm cells lose 1.9-2.7 K in 2-D; 12 mm cells win by 0.3-1.0 K | run_gpu.py, run_lowflux.py |
| CoolIT 4 kW point "parity / win" | R-grade 0.0093 (PCM), 0.0105 (paste) vs < 0.009: tie / loss; LM 0.0074 | prism_scorecard.py |
| 350 W/cm2, 95 C LM (PSM-12) | 93-94 C (R, die SKU), 84 C (P) | heat-map fit + 2-D differential 1.6 K |
| Annealed yield 70 MPa | 35-50 MPa after braze; 40 MPa design value | judge correction |

### D. Files

All new calculations are in `appendix/arch/`:

| File | Content |
|---|---|
| `cell2d.py` | generalised 2-D conjugate cell model, validated against judge model A |
| `run_kerf.py`, `run_final_cell.py`, `run_L128.py`, `run_L.py` | fin-level geometry, kerf and flow-length studies |
| `run_lowflux.py`, `run_gpu.py` | GPU-class uniform lids and flux-graded flow length |
| `run_coolit2d.py` | CoolIT-like 2-D penalty |
| `plenum_prism.py` | along-plenum uniformity |
| `prism_model.py`, `prism_scorecard.py` (`.out`), `prism_flow.py` | scorecard, Monte Carlo, flow trades |
| `prism_cost.py` | unit cost |

Supporting evidence: `physics/SYNTHESIS-physics.md`, `research/SYNTHESIS-benchmark-and-requirements.md`, `design/proposal-*.md`, and the judge notes relayed with this task.

External sources cited via the evidence base and judges:

- CoolIT 15 kW brief: https://www.coolitsystems.com/resources/news/15kw-coldplate/
- OCP Cold Plate Test Spec v1.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- LME copper, September 2026: https://www.westmetall.com/de/markdaten.php ; https://www.reporteminero.cl/noticia/noticias/2026/09/precio-cobre-cochilco-lme-promedio-alza-inventarios-2026
- US 12,460,878 gazette: https://patentsgazette.uspto.gov/week44/OG/html/1540-1/US12460878-20251104.html
