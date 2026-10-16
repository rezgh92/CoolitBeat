# PRISM: cold-plate architecture of record (final)

> **Status.** Architecture of record, 14 Oct 2026, for the line manager's funding decision. It supersedes the draft (`appendix/design/ARCHITECTURE-draft.md`) after six adversarial verifications, a completeness critic and a consistency audit (`04-verification.md`). Every number traces to a script under `appendix/`; modelled terms are ±25 % until tested.

Chief-architect final revision, 2026-10-14. For the line manager. This is the top-level architecture, not a detailed design.

**PRISM** = **P**roven-subset, **R**ecessed-meter, **I**nterdigitated, **S**kived **M**anifold cold plate. The design of record is **PRISM-15 Rev A** (the "PKG-A" lean stack from the gap-closer review, plus four fixes made in this revision).

**What changed since the draft.** Six verifications and a completeness critic found the draft's headline about 1.5 K optimistic, its cost about US$50 low, two manufacturing routes unbuildable as written, its Split-Flow design-around weak, and a dozen top-level views missing. Every number below is re-derived with each plate's own 2-D penalty and PG25 conductivity corrected to 0.49 W/mK. Appendix A lists the changes.

**Conventions.** Modelled terms are ±25 %. Costs are ±20 % until RFQs arrive. "Nominal" is the deterministic model value (within 0.1 K of the Monte Carlo P50). "Conservative" is the Monte Carlo P90. "Stretch" is the Tier 2 liquid-metal (LM) interface on the same plate; for cost it is the E1-gated C2 joining route on the same plate at the same volume. Filtration-gated grades (R+, P) are reported in separate rows, never in the stretch column. Scripts are in `appendix/verify/final/` (Appendix C).

---

## 0. Executive summary

### 0.1 The architecture in ten sentences

1. PRISM-15 Rev A is a single-phase, all-OFE-copper, single-braze hierarchical manifold micro-channel cold plate built only from conventional processes: skiving, gang milling, piercing, folding, deep drawing, vacuum brazing and fly-cutting.
2. From the die face up it has five layers: a 0.8 mm base with skived 0.15 mm fins at 0.15 mm gaps, 2.0 mm tall, kerfed at every inlet and outlet line; a 1.7 mm metered grate; a folded 0.8 mm copper plenum; a separator; and a drawn, arched, skirted cap.
3. Coolant is metered by graded 0.5 × 1.0 mm orifices pierced in the grate, lands on the grate's own lip rather than on the fins, enters each fin segment through a recessed window and kerf, and runs only 7.7 mm before it leaves.
4. Fin tips are brazed to the grate lands, so the 0.8 mm base carries pressure with no bow and holds PCM or liquid metal at datasheet resistance.
5. At CoolIT's operating point with the same paste class, Rev A predicts **31.0 K average / 38.7 K maximum** against CoolIT's measured 34.4 / 44.2 K (-10 % / -12 %). On a PCM pad it predicts **29.0 / 34.8 K**, against an estimated 32.5 / 40.3 K for CoolIT re-tested on PCM.
6. Plate pressure drop is **7.6 kPa** port-to-port at 18 LPM with 20 mm ports, against about 22 kPa (band 17-42) for our reconstruction of CoolIT's undisclosed value.
7. Rev A also wins on uniformity, case-temperature-limited capacity (+22-25 %), inlet headroom (+5.5 K at P50), height (20.8 mm against an estimated 22-28 mm) and the maximum at every OCP flow. Mass is at parity or better.
8. It does **not** win on: per-plate factory cost (US$165 against about US$126, +31 %); field record; fouling exclusion life at equal filtration; the average at very low flow (≤ 0.5 LPM/kW) or if CoolIT's heaters were only 100 cm2; and CoolIT's 4 kW point with the drop-in core. It also needs a supplied tray filter, which CoolIT's plate does not.
9. Cost per kW of capacity is at parity (+5-8 %) with vacuum braze and becomes a 6-9 % win with the E1-gated silver-free Cu-Sn belt-furnace joint (US$144).
10. A tranche-gated 12-month programme (US$8.4-10.7 M; US$2.3 M to the first gate) delivers an OCP-format result with an independent ISO/IEC 17025 repeat. Entry is through hyperscaler ASIC programmes, then NVIDIA reference designs; power electronics (800 VDC and SST SiC modules) is the second application.

### 0.2 Scorecard against CoolIT 15 kW

Conditions: 15 kW, 18 LPM PG25, 45 C inlet, 117 cm2 heated area unless stated. Plate = PRISM-15 Rev A, R-grade, 100k/yr. Sources: `appendix/verify/final/final_thermal.out`, `appendix/verify/final/final_system.out`, `appendix/verify/final/final_coolants.out`, `appendix/verify/final/final_transient.out`, `appendix/verify/ctl/cost_mass_height.out`. Cost and mass are the `appendix/verify/ctl/cost_mass_height.out` PKG-A values plus the Rev A additions (+US$3 factory, +0.07 kg); US$/kW divides by the `appendix/verify/final/final_thermal.out` capacities (Appendix A, consistency audit).

| Metric | CoolIT 15 kW | Conservative (P90) | Nominal | Stretch (LM / C2) | Verdict |
|---|---|---|---|---|---|
| Average dT, same paste | 34.4 K | 35.3 K | **31.0 K (-10 %)** | 23.9 K | win (P = 0.81-0.85) |
| Maximum dT, same paste | 44.2 K | 43.6 K | **38.7 K (-12 %)** | 28.8 K | win (P = 0.90-0.92) |
| Average / maximum, PCM 25 psi | 32.5 / 40.3 K (est., re-tested on PCM) | 32.3 / 38.5 K | **29.0 / 34.8 K** | - | win |
| Average / maximum, PCM at package retention | 34.4 / 42.2 K (est.) | - | 31.0 / 36.7 K | - | win |
| Average / maximum, paste, 100 cm2 "hard mode" | 34.4 / 44.2 K | 39.8 / 48.7 K | 34.7 / 43.1 K (+0.9 % / -2.4 %) | 26.5 / 31.5 K | **average lost (parity); maximum P = 0.57** |
| Same, R+ grade (≤ 33 µm absolute tray filter) | 34.4 / 44.2 K | 37.2 / 45.7 K | 32.2 / 40.3 K | 24.0 / 28.7 K | win (P = 0.69 / 0.79) |
| Maximum minus average, paste | 9.8 K | 9.5 K | 7.8 K | 4.8 K | win at nominal; parity at P90 |
| R(flow), OCP 25-150 % of rated | one point | - | maximum lower at every flow; average lower from 0.75 LPM/kW up | - | **average lost at 0.25 LPM/kW, parity at 0.5** |
| Plate dP, 18 LPM, 20 mm ports | undisclosed (~22, band 17-42) | ≤ 10 kPa (claim) | **7.6 kPa** | 7.6 kPa | win against any credible reconstruction |
| Plate dP, 36 LPM (characterisation) | est. 58-69 kPa | ≤ 30 kPa | 27.4 kPa | 27.4 kPa | win |
| Q capacity, Tcase,max ≤ 85 C, 1.2 LPM/kW | 12.9 kW paste / 14.8 kW PCM | ~13.8 / 15.6 kW (scaled) | **15.7 / 18.5 kW** | 25.5 kW thermal, **19.5 kW rated** | win |
| Inlet allowed at 15 kW (paste / PCM) | 40.8 / 44.7 C | 41.4 / 46.5 C | **46.3 / 50.2 C (+5.5 K)** | 52.3 C (return-limited) | win at P50; +0.6-1.8 K at P90 |
| CoolIT's 4 kW point (25 cm2, 6 LPM) | < 0.009 C/W | - | 0.0095 PCM / 0.0107 paste | 0.0076 (25 cm2), 0.0088 (20 cm2) | **lost on PCM and paste; LM and PRISM-S4 win; not like-for-like** |
| GPU-class uniform lid, 2.3 kW / 60 cm2, average | 16.1 K (model) | - | -0.2 to -0.5 K | - | parity; maximum 1-3 K lower |
| 350 W/cm2 four-die package, Tcase,max with LM | ~114 C (model) | - | ~98 C | - | win by ~16 K (model vs model); misses 85 C (P-grade ~88 C) |
| Absolute Tcase under a 1.5x power pulse | - | - | lower at every pulse length from 10 ms to 10 s | - | win (excursion up to 1.0 K larger at 100 ms) |
| Height at the bar | est. 22-28 mm | 22 mm (if E2 needs 6 mm plenums) | **20.8 mm** | 18.8 mm (triple arch) | probable win (CoolIT unmeasured) |
| Mass (plate + stubs + springs + backplate; no load frame) | est. 1.2-1.6 kg | 1.3 kg | **1.24 kg** | 1.12 kg (316L separator) | parity to probable win |
| External perimeter braze seams | 1 | 1 + 2 bosses | 1 + 2 bosses | same | parity (draft had 6) |
| Factory cost, 100k/yr | ~US$126 (116-137), like-sized | US$175 | **US$165 (+31 %)** | US$144 (+14 %) | **loss per plate** |
| Cost per kW of capacity (paste / PCM) | US$9.8 / 8.5 | - | US$10.5 / 8.9 (+5-8 %) | US$9.2 / 7.8 (-6 to -9 %) | parity → win (E1-gated) |
| Fouling exclusion life at equal filtration (50 µm absolute) | ~15 y (if 0.2 mm gaps) | - | ~7 y; ~12 y behind the supplied 33 µm cartridge | - | **loss at equal filtration** |
| Drop-in | yes | - | mechanically yes; needs supplied tray filter | - | **concession** |
| Field record | years | none | none | - | **loss** |
| Public data | 1 flow point, no dP | full OCP report | + independent 17025 repeat | + fouling-dose and real-silicon data | win |

### 0.3 Target applications, ranked

**First, AI accelerators:** (1) hyperscaler custom ASICs, whose owners control package, tray and loop and can adopt the tray filter and R+ grade; (2) NVIDIA reference-design plates via NVIDIA thermal engineering, with an MCL (micro-channel lid) co-design path; (3) 15-30 kW modules, Kyber-class blades, wafer-scale tiles; (4) CPU, NVSwitch and CPO plates in rack kits.

**Second, power electronics in the same PG25 loop:** (5) direct-substrate SiC coolers for 800 VDC rectifiers and solid-state transformers (PRISM-DC); (6) keyed-orifice shelf plates (no thermal claim); (7) SiC traction, licence only.

### 0.4 Decisions for the line manager

| # | Decision | Options | Recommendation |
|---|---|---|---|
| D1 | Public claim scope | (a) "beats on every metric" (false); (b) scoped claim, below; (c) maximum, dP and uniformity only | **(b)**, released only after G2 measurement. P(public at M12) ≈ 0.58 on the paste average, 0.68 on PCM average + maximum + dP |
| D2 | Channel and moat | (a) build-and-supply through a contract manufacturer (CM) to hyperscalers, NVIDIA via its thermal engineering; (b) licence to Group-A; (c) partner with an MMC vendor | **(a)**. A licence does not close: the premium consumes 50-90 % of a Group-A house's gross profit |
| D3 | Budget and gating | (a) full scope US$8.4-10.7 M; (b) lean ~US$8.3 M (drop the 40 kW rig upgrade, TTV-A2/TTV-D, R+/P and PRISM-DC demos, early Build-B dies; withdraw the > 18 kW capacity and 350 W/cm2 claims; ramp slips ~3 months); (c) tranches | **(c) then (a)**: US$2.3 M to G1 (M3), the rest released on a G1 pass |
| D4 | Rev A stack | (a) draft geometry, corrected (US$209, 26.4 mm, 1.74 kg, 6 seams); (b) Rev A with vacuum BAg braze (US$165); (c) Rev A + C2 Cu-Sn TLP belt braze (US$144) | **(b) as baseline, (c) decided at G1** on E1 coupon results |
| D5 | US launch date and site | (a) no US offers, sales or evaluation units before the FTO opinion, and no US sale before 10 Sep 2028 unless it clears earlier; (b) earlier US launch on the kerf design-around alone | **(a)**. Build site follows a CBP binding ruling: Vietnam or Mexico CM first; US second source if loose plates draw 25-50 % Section 232 duty; Taiwan only after TW I606224 is charted |
| D6 | Filtration | (a) tray cartridge mandatory and supplied (≥ 150 cm2, 33 µm absolute); (b) recommended only; (c) mandatory only for R+/P | **(a)**. Drop the word "drop-in" and say "mechanically drop-in, ships with a tray filter kit" |
| D7 | Hedges | (a) none; (b) US$0.4-0.6 M MCL-insert (T3B) design study with Jentech or AVC/Auras plus a two-phase watching brief; (c) full two-phase programme | **(b)** |

**The D1 claim we recommend:** "At CoolIT's published 15 kW operating point, PRISM beats CoolIT's plate like-for-like (same TIM class, heated area no smaller than CoolIT's estimate) on average and maximum case temperature, uniformity, case-limited capacity and inlet headroom. Its maximum is lower at every OCP flow. Its plate pressure drop is below any credible reconstruction of CoolIT's. It is lower at the bar and at parity or better on mass (both to be confirmed against a measured CoolIT plate), and at parity on cost per kW. It costs more per plate, ships with a tray filter, and has no field record yet." We do not claim the 4 kW point, the low-flow average or the 100 cm2 average.

---

## 1. Benchmark and the rules of the comparison

### 1.1 Benchmark facts and our reconstruction

| Item | Value | Basis |
|---|---|---|
| Load and TTV | 15 kW; 4 ceramic heaters ("GPU and HBM zones"); 3 plates x 8 TCs at the heater surface | brief |
| Coolant | "standard water-glycol" (PG25 assumed); 1.2 LPM/kW = 18 LPM; 45 C inlet | brief |
| Measured | average 34.4 K (plates 32.5 / 35.2 / 35.6, SD 1.69 K); maximum 44.2 K (worst of 24 readings; mean of per-plate maxima 43.2 K) | brief; `appendix/verify/completeness_checks.py` |
| Not disclosed | dP, footprint, TIM identity, height, mass, cost, R(flow) | brief |
| CoolIT's stated goal | to show that "standard coldplate designs and standard system operation" suffice | brief |
| Footprint | ~120 cm2 (100-145) by photogrammetry; model recalibrates to 119 cm2 at k 0.49 | research synthesis; `appendix/verify/final/final_thermal.out` |
| Plate dP reconstruction | ~22 kPa port-to-port (17-42); core without ports 18.8 kPa | physics synthesis; verify-hydraulics |
| CoolIT 4 kW plate (Mar 2025) | 50 x 50 mm, < 0.009 C/W max-case incl. TIM, 6.06 LPM, 55 kPa full loop | CoolIT brief via press |
| CoolIT re-tested on PCM (our estimate) | 32.5 / 40.3 K | TIM 9.0 → 7.1 K, scatter 3.5 → 1.5 K |

**Reconstruction validity.** Our "CoolIT-like" model is calibrated at one point by footprint only. It predicts 0.0125 C/W for CoolIT's 4 kW plate against a measured < 0.009, at least 37 % high. Every model-only CoolIT-like comparison (GPU class, 350 W/cm2, flow sweep below and above 18 LPM) is therefore model-against-model and is labelled so. E0 replaces it with purchased-plate data.

### 1.2 The arbiter

The arbiter is the **OCP Single-Phase Direct-to-Chip Cold Plate Test Specification v1.0.0, effective 3 Sep 2026** (PDF posted October 2026). Its primary author also wrote CoolIT's brief. Section 5.2 (thermal resistance, recommended TIM, case definition) and the dP boundary are **not yet read**; reading them is a month-1 task (R5). Until then, we plan for both PCM and paste.

| Class | Metrics | Rule |
|---|---|---|
| A. Measured by the OCP spec | R at ≥ 6 flows (25-150 % of rated) with the recommended TIM; dP at ≥ 6 flows, 45 ± 2 C; proof, burst, leak; drift after cycling | beat where physics allows; publish all six points, including the ones we lose |
| B. Disclosed by CoolIT | average and maximum at 15 kW, 1.2 LPM/kW; 4 kW plate R; plate-to-plate spread | beat like-for-like: same TIM class, R'' per area, footprint sensitivity published |
| C. Measurable on a sample | height, mass, uniformity, capacity, inlet headroom, equal-pumping-power, cost, transient | beat where physics allows; state the rest |
| D. Not measurable at launch | field record, field fouling life | no claim; dose-qualified surrogate only |

### 1.3 Like-for-like rules and the pre-registered statistics

- Publish paste and PCM separately, each with the measured post-test bond line.
- Test on two TTVs: TTV-A (116.6 cm2) and TTV-100 (100 cm2 hard mode). Report R'' per area.
- Replicate CoolIT's 8-TC layout and publish both the TC average and an area average.
- Publish dP at three boundaries: port-to-port with bore stated; plus stubs and barbs; plus a named UQD08 pair with measured Cv.
- **Primary statistic:** a one-sided one-sample t-test of our plate means against CoolIT's published 34.4 K, treated as a fixed reference, at α 0.05. At a 3.4 K margin and a plate SD of 1.0-1.7 K this needs 3-4 plates for 80 % power. We will test **5 plates x 3 re-mounts**.
- **Secondary statistic:** Welch against CoolIT's three plates. With only three CoolIT plates, no margin below 2.84 K can reach α 0.05 however many plates we test; at 3.4 K, p ≈ 0.02-0.03 (`appendix/verify/final/final_system.out` §4). We lead with metrics whose margin is several times the scatter: maximum, maximum minus average, dP, capacity.
- **Maximum:** compared worst-of-N with worst-of-N (CoolIT 44.2 K), and mean of per-plate maxima with mean (CoolIT 43.2 K).
- **E0:** buy and test CoolIT-class incumbent plates on our own TTVs.

---

## 2. Architecture overview

### 2.1 What PRISM is

PRISM is an all-copper, single-braze **tied sandwich**: a fine skived fin field fed through a short-path manifold, so fin geometry is set by heat transfer and fouling, not pressure drop. Four ideas carry it: (1) **short flow length graded by flux**, 5-12 mm, 7.7 mm on the benchmark (3.3); (2) **an inertial graded meter in the grate**, whose orifice areas cancel the plenum pressure profile at every flow because both scale with velocity squared; (3) **full-height entry** through 0.3 mm kerfs under every line, which suppresses the Hele-Shaw short-circuit along the fin tips; (4) **ties**: fin tips brazed to the grate lands, so a 0.8 mm base carries pressure with no bow.

### 2.2 Stack-up and flow path (PRISM-15 Rev A, 125 x 125 mm body, 108 x 108 mm fin field)

```
 z (mm)  layer (process)                                function
 20.8  +----------------------------------------------+  two vertical 20 mm bosses (brazed); guard = inside-out radial diffuser
       | DRAWN SKIRTED CAP, 1.0 mm Cu, arched          |  inlet header 2 arches 12x8 mm; outlet header 4 arches (2x area)
 11.8  +==== skirt drawn down to the base land =======+  <- the only external perimeter seam (lap joint)
       | SEPARATOR 1.5 mm Cu (option 0.6 mm 316L)      |  windows to 7 inlet and 8 outlet channels
 10.3  +----------------------------------------------+
       | FOLDED PLENUM, 0.8 mm Cu, 5.0 mm channels     |  15 channels at 7.7 mm pitch, end frame
  4.5  +--o--------o--------o--------o-----------------+
       | METERED GRATE 1.7 mm, stepped recess          |  inlet: graded 0.5x1.0 mm orifices in a 0.4 mm web, offset over the
       |                                               |  grate lip; outlet: 0.5 kPa orifice row; lands brazed to fin tips
  2.8  +-||||||| |||||||| ||||||||--------------------+
       | FINS 2.0 mm, skived 0.15/0.15 (R-grade)       |  0.3 mm kerf under every line; 15 lines (7 in, 8 out, edge outlets)
  0.8  +----------------------------------------------+
       | BASE 0.8 mm, fly-cut after braze              |  <= 20 um flat, Ra <= 0.8 um; 1.0 mm fallback (+0.7 K)
  0.0  +==============================================+  <- TIM -> lid / TTV / bare die (tier dependent)

 Flow: port -> radial-diffuser guard -> inlet header (mid-fed) -> separator window -> inlet channel (floored by the grate)
       -> graded orifice (1.54 m/s, 2.3 kPa) -> jet strikes the grate lip -> 1.2 mm window -> kerf + fin tips
       -> 7.7 mm along 0.15 mm gaps (0.20 m/s, Re ~44) -> kerf + outlet window -> outlet orifice row (0.5 kPa)
       -> outlet channel -> separator window -> outlet header (4 arches) -> port
```

### 2.3 Product family and tiers

All members share one process chain, one braze route and one test cell.

| SKU | Application | What changes from PRISM-15 |
|---|---|---|
| **PRISM-15** | 15 kW TTV; 10-20 kW multi-die modules and ASIC sleds | baseline above |
| **PRISM-15-HF** | 20-30 kW, LM or P-grade | high-flow meter artwork, dual UQD08 or 3/4-in ports (velocity caps, 4.1) |
| **PRISM-G** | NVIDIA / AMD lidded packages, 1.8-4 kW, 110 x 120 mm | zoned flow length; 10 mm horizontal ports; ~19-21 mm at the bar |
| **PRISM-S4** | single-die 3-5 kW, 50 x 50 mm | R+ or P core, L 5 mm, 0.8 mm base, LM by default |
| **PRISM-S** | CPU, NVSwitch, CPO | small field, 12-24 mm cells, laser zones fed first |
| **PRISM-W** | wafer-scale tiles | plenum tiles repeat; one port pair per ~110 mm |
| **R+ / P grades** | loops with a ≤ 33 µm absolute tray filter | 0.12/0.12 x 1.8 mm (R+) or 0.10/0.10 x 1.5 mm (P) fins |
| **PRISM-DC** | 800 VDC rectifier and SST SiC modules | R core as an Ag-sintered direct-substrate cooler; or a keyed-orifice shelf plate |
| **PRISM-A** | SiC traction (licence) | coarse ≥ 0.5 mm grade, Ni-plated, for WEG loops |

**Per-SKU tooling.** Only the grate artwork (meter and outlet row, ~800 holes) changes per package. It is laser-pierced (~US$2-4 per plate), so a new zoning costs weeks, not a US$0.4-1.0 M die set; high-volume SKUs move to a perforating die once the artwork freezes. The folded plenum and cap are universal per pitch family.

**Interface tiers (set only by how the face is finished after brazing).**

| Tier | Package | Interface | Plate face |
|---|---|---|---|
| T1 drop-in | flat lid | PCM pad: 0.055 cm2K/W at 25 psi on the TTV, 0.07 at 4-12 psi package retention | lapped bare Cu |
| T2 OEM co-design | Ni or Au lid | Ga-In liquid metal, 20-30 µm bond line, non-fluorinated dam | 3-5 µm electrolytic Ni on the face only |
| T3 chip co-design | bare die | stepped pedestal + LM | crowned pedestal, Ni or W barrier |
| T3B roadmap | micro-channel lid | indium TIM1 by the OSAT | P core as an MCL insert (D7) |

---

## 3. Thermal core

### 3.1 Cores

| Item | R-grade (drop-in) | R+ grade | P-grade | Basis |
|---|---|---|---|---|
| Fins (thickness / gap / height) | 0.15 / 0.15 / 2.0 mm | 0.12 / 0.12 / 1.8 mm | 0.10 / 0.10 / 1.5 mm | gap ≥ 3x the last filter's absolute rating |
| Last filter | 50 µm abs guard + supplied 33 µm abs tray cartridge | ≤ 33 µm abs | ≤ 33 µm abs | `appendix/physics/fouling-filtration.md` |
| Exclusion life (relative model) | ~7 y behind 50 µm, ~12 y behind 33 µm | ~6 y | ~0.6x skived | gap-closer table |
| Flow length L | 7.7 mm on the TTV; flux-graded | 6 mm | 5 mm | 3.3 |
| Base | 0.8 mm (1.0 mm fallback) | 0.8 mm | 0.8 mm | E1 gate (5.2) |
| Channel state at 18 LPM | 0.20 m/s, Re ~44, h_eff ~117 kW/m2K | - | - | `appendix/verify/ctl/harness.py` `ev()` at Rev A inputs |

Thinner (0.10 mm) fins at a 0.15 mm gap and taller (2.5 mm) fins give no gain in 2-D (0.0 K and +0.3 K), so neither is used. A straight copper fin at a 0.15 mm gap cannot exceed h_eff ≈ 138 kW/m2K; once fouling fixes the gap, no fin geometry buys more.

### 3.2 Fin-level geometry: window, kerf and meter discharge

The 2-D cell model (`appendix/arch/cell2d.py`, reproduced within 0.05 K by verify-physics) treats the fluid as unmixed across the fin height, correct at Re 35-200. The kerf is worth 0.4 K on Rev A and 0.66 K on the draft core. Filling the inlet kerf by impaction costs +0.3 K.

**Meter discharge (changed).** The draft let 1.4-2.1 m/s jets cross a 1.0 mm stand-off onto the fin tips, the kerf floor and the 1.0 mm base. That broke the 0.5 m/s fin-entry cap, eroded the pressure boundary and moved PRISM toward the Microfabrica "microjet onto the heat-exchange region" claim. Rev A uses a **stepped recess** in the grate: a 2.5 mm-wide upper recess holds the orifices offset laterally so that each jet strikes the 0.65 mm-wide grate lip; the lower 1.2 mm window then feeds the fins at low velocity. The kerf-floor jet credit in `cell2d.py` is small (floor h of 6 vs 12 kW/m2K changes nothing), so the thermal cost is about 0 K. Single-cell CFD must confirm a fin-top velocity ≤ 0.5 m/s before the G1 freeze.

**Clearances.** The inlet channels have the grate itself as their floor (folded-plenum construction), so the nearest joint on the inlet face is a plenum wall ~3.4 mm away, and the land joints are 1.3 mm below with filler masked 0.3 mm back from the window edges. This removes the meter-sheet-to-grate interface that the draft had at the orifice plane.

### 3.3 Flux-graded flow length (corrected rule)

In 2-D, the average falls monotonically with L at every flux, the case-ripple crest is flat within 0.35 K over L 5-8 mm, and **L 4 mm is never best** (verify-physics). The draft's "4-5 mm at ≥ 250 W/cm2" branch is withdrawn.

| Zone flux | Flow length | Slot pitch |
|---|---|---|
| ≥ 250 W/cm2 | 5-6 mm (only where die geometry or HBM zoning needs it) | 10-12 mm |
| 100-250 W/cm2 | 6-8 mm (7.7 mm on the 15 kW TTV) | 12-16 mm |
| 50-100 W/cm2 | 8-12 mm | 16-24 mm |
| < 50 W/cm2 | 12 mm | 24 mm |

On uniform low-flux GPU lids, 12 mm cells bring the average to **parity** with split-flow (-0.2 to -0.5 K; a 3 mm copper lid erodes the gain), with a 1-3 K lower maximum. It is not a win on the average.

### 3.4 Term budget at the benchmark (k = 0.49, own 2-D penalty)

| Build | Caloric | TIM | Base | Conv | 2-D pen | **Avg** | Max | R'' (cm2K/W) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT measured (calibration budget) | 6.3 | 9.0 | 6.6 | 12.6 | in calibration | **34.4** | 44.2 | 0.268 |
| Draft core (L 6, base 1.0), paste, corrected | 7.5 | 9.0 | 3.3 | 11.0 | +1.5 | 32.2 | 39.0 | 0.251 |
| **Rev A, paste** | 7.5 | 9.0 | 2.6 | 10.9 | +0.9 | **31.0** | **38.7** | 0.242 |
| **Rev A, PCM 25 psi** | 7.5 | 7.1 | 2.6 | 10.9 | +0.9 | **29.0** | **34.8** | 0.227 |
| Rev A, PCM at package retention | 7.5 | 9.0 | 2.6 | 10.9 | +0.9 | 31.0 | 36.7 | 0.242 |
| Rev A, LM (T2) | 7.5 | 1.9 | 2.6 | 10.9 | +0.9 | 23.9 | 28.8 | 0.187 |
| Rev A, 1.0 mm base fallback, paste | 7.5 | 9.0 | 3.3 | 10.9 | +0.9 | 31.7 | 39.2 | 0.247 |
| R+ grade, paste | 7.9 | 9.0 | 2.6 | 8.5 | +0.9 | 28.9 | 36.3 | 0.225 |
| P-grade (L 5), PCM | 8.1 | 7.1 | 2.6 | 7.1 | +0.8 | 25.7 | 30.8 | 0.201 |

Maximum = average + 1.5 K flow maldistribution + TIM scatter scaled by flux (3.5 K paste, 1.5 K PCM, 0.6 K LM at 128 W/cm2) + half the computed case ripple. Rev A's core R'' (convection, base and penalty) is 0.113 cm2K/W; with caloric it is 0.171.

### 3.5 Zoning and HBM

Zoning is by heat: the die block gets 85-90 % of the flow, HBM columns 0.3-0.5x the average flow per area, and unheated margin only slot-end bleeds (1.1 mm hole for 4 % of plenum flow; the draft's 0.6 mm hole gives only 1.2 %). Every zone is fed in parallel, so HBM never sits downstream of a die. The HBM pedestal is cut in the same post-braze fly-cut, ±0.05 mm.

---

## 4. Hydraulic architecture

### 4.1 Levels, sizes and velocities (18 LPM; rated flow declared as 1.0 LPM/kW = 15 LPM)

| Level | Element | Velocity at 18 LPM | Rule |
|---|---|---|---|
| Ports | 2 x 20 mm vertical bosses | 0.95 m/s | ≤ 1.5 m/s at 150 % of rated (met to 28 LPM). The 16 mm option is dropped: it breaks the rule at 22.5 LPM |
| Guard | 50 µm absolute **square-weave** 316L, inside-out radial diffuser in the inlet boss, ≥ 25 cm2 | 0.12 m/s face | 0.1-0.2 kPa clean; diffusing the port jet keeps line max/min at 1.03, not 1.06 |
| Headers | inlet 2 arches (161 mm2 per half), outlet 4 arches (322 mm2 per half), mid-fed | 0.93 / 0.47 m/s | outlet area 2x inlet for segment balance |
| Plenums | 7 inlet channels 6.9 x 5.0 mm, 8 outlet channels | ≤ 0.62 m/s | graded orifice artwork |
| Meter | graded 0.5 x 1.0 mm orifices, 5 sizes spanning 1.16x in area; shape and punch direction specified; Cd(Re) measured on coupons in both directions | 1.54 m/s; 1.92 m/s at 22.5 LPM | ≤ 2.0 m/s at 150 % of rated |
| Outlet row | orifices in the outlet window web | - | 0.5 kPa |
| Fins | 0.15 x 2.0 mm gaps, 7.7 mm segments, 5,040 parallel segments | 0.20 m/s | 1.07 kPa |

Passage hierarchy: port 20 > header 8 > plenum 5 > window 1.2 > orifice 0.5 > kerf 0.3 > gap 0.15 mm. Nothing sieves upstream of the fins. The plate is symmetric and can be back-flushed (Cd measured in reverse).

**Velocity caps limit ratings.** The meter reaches 2.0 m/s at 23.4 LPM, so the standard plate is rated to **19.5 kW at 1.2 LPM/kW**. Higher thermal capacities (LM 25.5 kW, P-grade 22.5-33 kW) need the -HF artwork and dual UQD08 or 3/4-in plumbing; a single UQD08 pair tops out at 18 LPM (3.8 m/s).

### 4.2 Pressure-drop budget (PG25, 45 C)

| Element | kPa at 18 LPM |
|---|---:|
| Ports, K 3.5 combined | 1.60 |
| Guard (square weave, clean; 0.1-0.2 expected, 0.30 booked) | 0.30 |
| Headers (tees) | 0.99 |
| Separator windows | 0.46 |
| Plenums | 0.21 |
| **Graded meter** | **2.30** |
| Windows, kerf turn, misc. | 0.16 |
| Outlet orifice row | 0.50 |
| Fin channels (viscous) | 1.07 |
| **Plate, port-to-port** | **7.6** (81 % inertial) |

| Flow | 15 LPM | 18 LPM | 22.5 LPM | 36 LPM (characterisation) |
|---|---:|---:|---:|---:|
| Rev A | 5.5 | **7.6** | 11.4 | 27.4 |
| CoolIT-like reconstruction | ~17-19 | ~22-25 | ~30-34 | 58-69 |

**External claim:** ≤ 10 kPa at 18 LPM with 20 mm ports, ≤ 30 kPa at 36 LPM. Matched-boundary ratios: core without ports ~6.0 vs 18.8 kPa; port-to-port 2.7x at matched 20 mm bores and 1.7x at 12 mm (½-in barbs, as in CoolIT's photograph). CoolIT's value is undisclosed, so we publish ours against the reconstruction band, never as a measured CoolIT number. The reconstruction may be low: scaled to GPU size it gives 1.5-4 kPa against ~12 kPa published for a GB300 plate.

**Couplings.** Vendor Cv (FITOK 3.65-3.76, CPC ~4.75) gives a UQD08 pair 14-24 kPa at 18 LPM. Tray loop with one UQD08 pair: Rev A 42-51 kPa against 56-79 kPa for a CoolIT-like plate; with dual pairs, about 17-20 kPa.

### 4.3 Uniformity: line, along-plenum and segment level

| Level | Draft as written | Rev A | Source |
|---|---|---|---|
| Layout | 18 lines: an edge inlet dumps 1.68x into one segment and 3 mm dead-end strips sit over the heater edge (+10-15 K locally) | 15 lines, 7 inlet and 8 outlet, edge outlets with half-area windows | verify-hydraulics; this revision |
| Along-plenum max/min | 1.04-1.08 | 1.061 at 18 LPM, 1.068 at 36 LPM (graded) | `appendix/verify/ctl/plenum_graded_pkgA.out` |
| Line max/min | 1.04-1.07 | 1.03 (diffused port jet), 1.06 undiffused | `appendix/verify/final/final_segbal.out` |
| **Segment max/min** | 1.23-1.43 (18 LPM), 1.41-1.71 (36 LPM) | **1.06 (18 LPM), 1.08 (36 LPM)**; 1.36 / 1.79 without the two outlet fixes | `appendix/verify/final/final_segbal.out` |

The meter fixes each line's flow but not the split between its left and right segments. Only the viscous fin resistance resists that split, against outlet-side pressure differences. Rev A fixes it with a doubled outlet header (four arches, no height or dP cost) and a 0.5 kPa outlet orifice row. The flow hot-spot term stays at 1.5 K nominal.

**Verification.** The E2 water table measures **segment-level** max/min by dye and IR, not line level. Pass: ≤ 1.15 at 18 LPM and ≤ 1.20 at 27 LPM, combined over along-plenum and segment effects.

---

## 5. Mechanical construction and manufacturing

### 5.1 Parts and joining

| # | Part | Process (prototype → volume) | Mass (kg) |
|---|---|---|---:|
| 1 | Base + fins | OFE C10100 blank ≥ 3.5-4.0 mm with pocketed field and rim (≥ 1.5 mm base during the skive); skived; tips diamond-planed along the fins to ±5-10 µm; kerfs sawn with a melt-out support fill, stopped ≥ 8 mm from the rim, 0.05-0.1 mm stub above the base, burr ≤ 15 µm | 0.25 |
| 2 | Metered grate | 1.7 mm OFE; stepped recess gang-milled from the fin side; orifices pierced through the 0.4 mm web (laser for prototypes and per-SKU artwork) | 0.21 |
| 3 | Folded plenum | 0.8 mm OFE square-wave corrugation, 5 mm channels, plus end frame | 0.19 |
| 4 | Separator | 1.5 mm OFE (option: 0.6 mm 316L with Ni strike, -0.12 kg) | 0.19 |
| 5 | Skirted cap | 1.0 mm OFE, deep-drawn with arches and port pockets; brazed 20 mm bosses | 0.25 |
| 6 | Stubs, guard, springs, backplate | 316L / steel | 0.15 |
| | **Total** | 11.8 mm body, **20.8 mm at the bar** | **1.24** (excl. 0.3-0.6 kg load frame) |

The cap skirt wraps the inner layers and laps onto the base land. The inner layer edges are therefore internal: a missed internal joint gives bypass, not a leak. External seams fall from six (draft) to one perimeter lap plus two bosses, the same count as an incumbent with barbs.

**Joining.** One brazing cycle; four routes qualified in parallel in E1:

| Route | Filler | Note |
|---|---|---|
| A | BAg-8 preforms, **12-15 µm or perforated 25 µm** | 25 µm foil carries 3.4x the liquid needed and fills gap tops |
| B | 8-10 µm electroplated Ag, masked 0.3 mm from window edges | 5 µm only closes 14 µm of tip gap against a ±20 µm plane |
| C | ~3 µm masked Sn → Cu-Sn transient liquid phase, continuous N2/H2 belt furnace | **C2 cost route** (US$144): replaces the ~US$15 BAg filler line with ~US$4 of Sn and removes ~US$9 of batch-vacuum cost; risks: homogenisation time, brittle Cu3Sn if under-reacted; also the only route compatible with a pre-plated Ni wetted path |
| D | low-pressure diffusion bond | slow fallback |

No route puts more than about 1 MPa on the fin tips. Ag-Cu or Cu-Sn fillets in the wetted path are declared.

### 5.2 Pressure ratings and load paths

MAWP 1.03 MPa (150 psi); 100 % proof 1.55 MPa; design burst ≥ 3.1 MPa; sample burst ≥ 4.5 MPa; vacuum-stable to -0.9 bar(g). Allowable: post-braze annealed OFE, yield 35-50 MPa, **design 40 MPa**.

| Load path at 3.1 MPa | Stress | Source |
|---|---:|---|
| Fin tie, bonded fraction 0.70 (0.56 at the gate value) | 8.9 (11.1) MPa; 22 (28) MPa local | verify-manufacturing |
| Folded plenum wall, 0.8 mm at 7.7 mm pitch | 29.8 MPa | `appendix/verify/ctl/pkgA_dp_stress.out` |
| Separator, 1.5 mm over 6.9 mm channels | 32.8 MPa | same |
| Grate cantilever to the outlet window edge | 28.6 MPa | same |
| Arched cap hoop, 1.0 mm at r 6 mm; port pocket r 12 mm at 1.5 mm | 18.6 / 24.8 MPa | same |
| Perimeter lap | SF 4.5-6.5 | verify-manufacturing |
| Plenum-wall / cap crossings | FEA in E1 | open |

**Governing defect.** With kerfs, one unbonded land strip spans kerf to kerf. At 0.8 mm base it reaches 67-99 MPa at proof and collapses at 1.6-2.3 MPa, below design burst, but stays leak-tight at MAWP: a rating and verification problem, not a safety one. Its proof bulge is about 2.2 µm, which the confocal scan (1 µm resolution) can see; at a 1.0 mm base it was 0.58 µm and invisible. **The 0.8 mm base is gated on E1 demonstrating per-strip detection**; otherwise Rev A runs at 1.0 mm (+0.7 K).

### 5.3 Inspection and production test sequence

Acoustic microscopy cannot resolve the fin-tip joints. The screen is:

1. Per-strip process control before braze: preform-presence vision, Ag or Sn thickness by XRF, grate flatness ±20 µm.
2. **Dry He leak** at ≤ 1e-6 mbar·L/s, before any wet step (water masks leaks).
3. Hydrostatic proof at 1.55 MPa with a confocal pressurised-flatness scan (detects patches ≥ 13 mm at any base, and single land strips at 0.8 mm base once E1 proves it).
4. Lot over-proof at 2.5-3.1 MPa with a before/after zero-pressure flatness map (permanent set reveals hinge yielding); lot CT for filler presence per strip.
5. Three-point dP against flow, CpK ≥ 1.33.
6. IR flow screen on the coated as-brazed face, **before** the face fly-cut removes the coating. It resolves 5-10 mm features (a blocked line, not 1 % of channels).
7. Fly-cut, ISO 16232 flush to a cleanliness code with no particle > 50 µm; chip-entrapment check by CT or flush gravimetry on samples (~10,800 kerf burr and chip sites, 15 kerfs x 360 fins x 2 cut faces, lie downstream of every filter).
8. **Vacuum-bake dry** to an outlet dew point ≤ -40 C, then N2 fill and cap. All SKUs ship dry. LM FRUs ship with LM applied but are stored at ≥ -10 C (Galinstan freezes at about -19 C).

### 5.4 Unit cost (verifier basis: Cu US$14.6k/t, Ag US$65/oz, 93-94 % mature yield, 12 % overhead)

| Line (US$, 100k/yr per SKU, P50) | Draft, verifier basis | Rev A (vacuum BAg) | Rev A + C2 |
|---|---:|---:|---:|
| Copper (buy / finished kg) | 38.8 (2.91 / 1.60) | 22.1 (1.43 / 1.02) | 22.1 |
| Skive, kerf | 24.0 | 23.3 | 23.3 |
| Stampings / grate | 6.3 | 6.8 | 6.8 |
| Plenum | 7.5 | 4.4 | 4.4 |
| Header / cap | 14.5 | 5.3 | 5.3 |
| Filler | 18.5 | 14.7 | 4.3 |
| Braze | 21.9 (2.2 furnaces) | 17.6 (1.6 furnaces) | 8.5 (belt) |
| Dies, fly-cut, stubs, hardware, test | 40.5 | 40.2 | 40.2 |
| Rev A additions (skirt, outlet arches, stepped recess, outlet row) | - | ~2.5 | ~2.5 |
| **Factory cost P50 (P10-P90)** | **209 (197-222)** | **~165 (155-175)** | **~144 (134-153)** |
| Premium vs like-sized incumbent (US$126; 116-137) | +66 % | +31 % (+18 to +44 %) | +14 % (+3 to +26 %) |
| US$/kW, paste / PCM (CoolIT 9.8 / 8.5) | 13.3 / 11.3 | 10.5 / 8.9 | 9.2 / 7.8 |

At the 10k/yr ramp (laser-cut and CNC parts, 75-92 % yield) the cost is **US$370-430** for the first 18-24 months. The incumbent at 1M/yr is about US$75; we make no 1M/yr comparison.

### 5.5 Scale-up and supply chain

| Item | Plan |
|---|---|
| Ramp | M12-18: 300-500-plate pilot at the CM (laser parts). M18-24: 10k/yr (1 furnace, 1-2 skivers). M24-36: 100k/yr (1.6 vacuum furnaces or 1 belt line, 2-3 skivers, 1 test line). Yield learning 75 % → 93 % |
| Capex | US$3.7-9 M per 100k/yr at the CM; funded by the CM against a volume commitment, or co-funded under a supply agreement. We fund fixtures, the IR station and test cells (~US$1-1.6 M per line) |
| CM selection | vacuum-braze and Cu experience; IATF-style quality; non-Group-A; outside Taiwan until TW I606224 is charted; runs our recipe, inspection and test cell |
| Dual sourcing | two skiving houses, two braze houses (one belt-capable for C2), two OFE strip mills, two drawing/forming shops; qualification gates at M12 (first source) and M18 (second) |
| Long-lead items | vacuum furnaces 9-12 months; skiving machines 6-9 months; belt furnace 6-9 months; drawing dies 8-14 weeks; confocal scanner 3-4 months |
| Commodities | Cu ~1.4 kg buy per plate and Ag ~5 g (route A; ~2-3 g route B): US$5-12 per plate of silver at US$60-72/oz (filler line US$14.7). Index both in supply contracts; hedge 6-12 months of forward Ag; C2 removes the exposure |

### 5.6 Height, mass and integration

The 15 kW class is not a 1U product for anyone; its homes are ASIC sleds, Kyber-class blades and 2U boards. Horizontal ports do not reduce height at 18 LPM (a 16-20 mm bore needs a ≥ 20-24 mm boss). PRISM-G keeps 10 mm horizontal ports at 2-4 LPM for the 1U GPU socket. **Mass limits per SKU:** PRISM-15 ≤ 1.4 kg, PRISM-G ≤ 0.9 kg (plate only).

---

## 6. Performance predictions

### 6.1 Benchmark point and probabilities

Monte Carlo (40k draws; draft distributions; PRISM's own 2-D penalty; optional model-form error of 8 % on the core):

| Build | Avg P10/P50/P90 | Max P10/P50/P90 | P(avg < 34.4) | P(max < 44.2) | With model-form error |
|---|---|---|---|---|---|
| Rev A, paste, 117 cm2 | 27.8 / 31.1 / 35.3 | 35.5 / 39.2 / 43.6 | 0.85 | 0.92 | 0.81 / 0.90 |
| Rev A, PCM, 117 cm2 | 26.6 / 29.2 / 32.3 | 32.2 / 35.1 / 38.5 | 0.98 | 1.00 | 0.95 / 1.00 |
| Rev A, paste, 100 cm2 | 31.0 / 34.9 / 39.8 | 39.4 / 43.6 / 48.7 | **0.44** | **0.57** | 0.44 / 0.55 |
| R+ grade, paste, 100 cm2 | 28.8 / 32.4 / 37.2 | 36.8 / 40.7 / 45.7 | 0.72 | 0.82 | 0.69 / 0.79 |
| P-grade, paste, 117 cm2 | 24.7 / 27.7 / 31.8 | 31.8 / 35.0 / 39.3 | 0.97 | 0.99 | 0.96 / 0.99 |

The decisive PCM result (≤ 31 K average and ≤ 36 K maximum) has model probability **0.60-0.63**. With programme risk (join route by G1: 0.8; rig repeatability by M6: 0.9) it is **about 0.43**.

**Footprint.** If CoolIT's heaters were 100 cm2, the R-grade paste average is lost by 0.3 K (parity) and the maximum margin is only 1.1 K. The draft's "maximum wins hold at every footprint" is withdrawn. Only the filtration-gated R+ grade, or LM, wins robustly at 100 cm2.

### 6.2 OCP flow sweep (15 kW, 45 C inlet; CoolIT-like patched: ramp = 0.5 dT_out, k 0.49, footprint 119 cm2)

| LPM/kW (% rated) | Outlet C | Rev A paste avg / max | CoolIT-like paste avg / max | Rev A PCM avg / max | CoolIT-like PCM avg / max | Rev A dP | CoolIT-like dP |
|---|---|---|---|---|---|---:|---:|
| 0.25 (25 %) | 106 (!) | **68.6** / 82.9 | 58.8 / 92.6 | 66.6 / 79.0 | 56.9 / 88.8 | 0.6 | 3.5 |
| 0.50 (50 %) | 75 (!) | 43.7 / 54.4 | 43.5 / 62.1 | 41.7 / 50.4 | 41.6 / 58.3 | 1.7 | 7.8 |
| 0.75 (75 %) | 65.3 (!) | 36.3 / 45.4 | 38.4 / 51.9 | 34.3 / 41.4 | 36.5 / 48.1 | 3.3 | 13.0 |
| 1.00 (100 %) | 60.2 | 32.7 / 40.9 | 35.7 / 46.8 | 30.8 / 37.0 | 33.8 / 42.9 | 5.5 | 19.1 |
| 1.20 (120 %) | 57.7 | 31.0 / 38.7 | 34.4 / 44.2 | 29.0 / 34.8 | 32.5 / 40.3 | 7.6 | 24.6 |
| 1.50 (150 %) | 55.1 | 29.2 / 36.5 | 33.0 / 41.5 | 27.3 / 32.6 | 31.1 / 37.7 | 11.4 | 33.9 |

(!) = outlet above 65 C at 15 kW. R is independent of power to first order, so these points are tested at reduced power (≤ 4.9 / 9.9 / 14.8 kW). **At 0.25 LPM/kW Rev A loses the average by 17 %; at 0.5 it is at parity.** The cause is the isothermal-cell caloric penalty of any short-cell manifold: at high NTU each cell's wall runs near the cell outlet temperature, while a long channel's wall tracks the mean. The maximum is lower at every flow. CoolIT-like values off 1.2 LPM/kW are model-only.

**Trades.** Equal pumping power is ~28 LPM at the plate boundary (beyond our meter cap) and 19-22 LPM at the tray-loop boundary with one UQD08 (~27.5 / 32.5 K on PCM). Matching 34.4 K needs ~11.4 LPM, set by the 65 C return. Flow and supply-temperature margins are the same margin, not additive.

### 6.3 CoolIT's 4 kW point (4 kW, 6.06 LPM, 50 x 50 mm)

| Build | 25 cm2 heater: paste / PCM / LM (C/W) | 20 cm2 heater: paste / PCM / LM |
|---|---|---|
| Drop-in Rev A core | 0.0107 / 0.0095 / 0.0076 | 0.0127 / 0.0112 / 0.0088 |
| **PRISM-S4, R+ core** | 0.0099 / **0.0087** / **0.0068** | 0.0118 / 0.0103 / **0.0079** |
| **PRISM-S4, P core** | 0.0095 / **0.0083** / **0.0064** | 0.0112 / 0.0097 / **0.0074** |
| CoolIT-like reconstruction | 0.0125 (paste) | - |

The drop-in core loses on PCM and paste. LM wins on any core at 25 cm2; PRISM-S4 also wins on PCM at 25 cm2; paste never wins. Our reconstruction cannot reproduce CoolIT's < 0.009 under any condition, so CoolIT's 4 kW test conditions differ from its 15 kW test. No claim until E0 tests a CoolIT 4 kW-class plate on our 25 cm2 TTV with the same TIM.

### 6.4 GPU class, 350 W/cm2 and high power

| Case | Result | Note |
|---|---|---|
| Uniform low-flux lid, 1.4-3.6 kW | average parity (-0.2 to -0.5 K), maximum 1-3 K lower | verify-physics; model vs model |
| Die-concentrated Rubin-class (2.3 kW on 16.6 cm2 of die) | maximum ~8-10 K lower (indicative) | model vs an unvalidated reconstruction; TTV-B verifies |
| Four 26 x 33 mm dies at 350 W/cm2 | CoolIT-like 81.6 K (paste 0.05) / ~114 C with LM; Rev A R with LM ~98 C; P-grade with LM ~88 C | the draft's 88.6 K was at paste 0.07; **margin ~16 K like-for-like (114 vs 98 C, model vs model); nothing drop-in reaches 85 C**; a 2029+ KPI |
| 25 kW on 117 cm2 at 30 LPM (-HF) | PCM 95 C (fails); LM 84 C; P-grade + LM 78 C | `appendix/verify/final/final_thermal.out` §6 |
| 30 kW on 150 cm2 at 36 LPM (-HF) | PCM 92 C (fails); LM 83 C | above ~20 kW per 117 cm2 the product is T2 or P-grade |
| 20 kW wafer-scale, 460 cm2 | PCM 65 C; flow length is independent of size | plenum tiles repeat |

### 6.5 Transient power excursions

AI workloads swing package power in milliseconds to seconds. Rev A's 0.8 mm base has 0.28 J/K/cm2 of near-die heat capacity against 0.69 for a 2 mm base. A 1-D network (`appendix/verify/final/final_transient.py`) applies a 1.5x pulse on top of steady 1.0x (paste, both plates):

| Config | Plate | Steady 1.0x | Peak after 10 ms | 100 ms | 1 s | 10 s |
|---|---|---:|---:|---:|---:|---:|
| TTV | Rev A | 31.0 | 33.9 | 41.8 | 46.4 | 46.4 |
| TTV | CoolIT-like | 34.9 | 37.9 | 44.7 | 52.4 | 52.4 |
| 3 mm Cu lid | Rev A | 31.4 | 31.5 | 35.6 | 46.8 | 47.1 |
| 3 mm Cu lid | CoolIT-like | 35.4 | 35.4 | 39.1 | 52.0 | 53.0 |

The thin base lets Rev A rise up to 1.0 K more than the incumbent within 100 ms. Its absolute peak is still 2.9-6 K lower at every pulse length, because it starts lower and settles lower. **Transient KPI:** peak Tcase - Tin under a 1.5x, 100 ms pulse ≤ incumbent - 2 K, measured on TTV-A with a pulsed supply (E3).

### 6.6 Coolants

| Coolant (45 C inlet, 18 LPM, paste) | Rev A avg / max |
|---|---|
| PG25 | 31.0 / 38.7 K |
| PG30 | 31.5 / 39.2 K |
| EG25 | 31.1 / 39.0 K |
| Water | 28.9 / 36.8 K |
| PG25 at a 20 C film (start-up) | 31.4 / 39.1 K; channel dP 2.2 kPa |

The architecture works across glycol and water loops; ratings are published for PG25 with PG30, EG25 and water as secondary curves.

---

## 7. System integration

### 7.1 Rack and CDU

Reference rack: 18 trays x 1 PRISM-15 = 324 LPM, 270 kW; four racks ≈ 1.08 MW (72 packages).

| Boundary (18 LPM per package) | Rev A | CoolIT-like |
|---|---|---|
| Plate port-to-port | 7.6 kPa | ~22 kPa |
| + one UQD08 pair (tray loop) | 42-51 kPa | 56-79 kPa |
| Tray loop with dual UQD08 | 17-20 kPa | ~30-35 kPa |
| + rack manifold and CDU (80-180 kPa) | saving 6-18 % of loop head | - |

**Value at system level (contingent, not counted in the plate case).**
- Homogeneous racks: 6-18 % less loop head. That is either about 6 % more racks per head-limited CDU (assumed 250 kPa available) or about 58 kW of pump power per 100 MW (US$40k/yr), plus a CDU capex credit of US$9-25 per plate (US$60-167k per 100 MW) when the CDU is head-limited.
- **Mixed racks: zero.** Un-orificed PRISM branches over-draw 10-35 % and starve incumbent trays. Every PRISM branch in a rack shared with higher-dP plates carries a keyed 20-50 kPa orifice.
- Manifold rules: 63 mm U-type rack manifold (1.058 max/min; Z-type 1.136), or a ~10 kPa branch orifice on 50 mm. The dual-UQD08 both-end-fed header variant changes the header topology and gets its own network check in E2.
- Start-up at 17-25 C: plate dP 8.7-9.4 kPa (CoolIT-like ~33-41 kPa, assumed 16 kPa viscous); flow share shifts only ~4 %.
- Turndown: below 0.5 LPM/kW Rev A's average R exceeds an incumbent's (6.2). This is harmless at low IT load, and ratings are published to 0.25 LPM/kW.

**CDU control guidance.** Run the CDU on secondary differential-pressure set-point with a supply-temperature reset. Rev A's flat R(flow) above 1.0 LPM/kW means more flow buys little, so spend margin on supply temperature, never on both.

### 7.2 Filtration, fouling and service life

| Stage | Element | Life at loop concentration of particles > 50 µm: 1e-4 / 1e-3 / 1e-2 per mL |
|---|---|---|
| Commissioning | flush with plate bypass jumpers; 5-10 µm bags; connect plates only after particle-count acceptance (OCP PG25 Guidelines limits, to be read in M1) | - |
| CDU | 25 µm full-flow + 5 µm side-stream (recommendation) | - |
| **Tray cartridge (mandatory, supplied)** | ≥ 150 cm2 pleated, 33 µm absolute, 316L housing, dP taps | ~160 d / 16 d / 1.6 d to 50 % blockage |
| Plate guard | 50 µm square-weave, 25 cm2 | behind the cartridge: years. **Without it: 65 d / 6 d / 0.6 d** |

Lives scale by area from `appendix/physics/fouling-filtration.md` (13 days for 5 cm2 at 1e-4/mL). Without the cartridge the guard becomes the loop filter; hence D6. The cartridge is changed on a 3x-clean-dP alarm, not on a calendar.

**Life claim.** Exclusion life behind the 33 µm cartridge is ~12 years on the relative model (~7 years at 50 µm; ~15 years for a 0.2 mm gap at 50 µm). At launch we claim only a **dose qualification**: 100x particle dose for 1,000 h (~11 years of dose) with ≤ 10 % fin-field dP drift and ≤ 1 K drift (E4). Chemistry and biofouling remain time-bound and are not claimed.

### 7.3 Controls and telemetry

Port-to-port dP is ~80 % inertial: a 10 µm deposit raises fin dP 54 % but plate dP only ~8 %. Plate dP therefore cannot see fouling.

| Signal | Where | Alarm |
|---|---|---|
| Fin-field dP (inlet plenum to outlet plenum taps, brought out to the tray fluid module) | R+ and P grades, pilot fleet, all qualification plates | +10 % warning, +25 % service (≈ 2 µm and 5 µm deposit per wall) |
| BMC-inferred resistance drift: (Tcase or Tj - Tin)/P at known flow, rolling 7-day median | every plate, via existing package sensors | +5 % warning, +10 % service |
| Tray cartridge and guard dP | tray fluid module | 3x clean dP |
| Inlet temperature and flow | CDU / rack | below dew point + 2 K: alarm |

Sensor definitions are published as PLDM/Redfish sensor records so OEM BMCs can expose them. The plate itself stays passive. NVIDIA "intelligent plate" filings and CoolIT US 9,052,252 (in-plate leak sensing) are charted before any tray-module design.

**Operating envelope.** Inlet 17-52 C (thermal limit at 15 kW: 46 C paste, 50 C PCM; return ≤ 65 C). Minimum inlet ≥ room dew point + 2 K (ASHRAE W17 class operation needs a condensation check). Copper-side bulk velocity ≤ 0.9 m/s where the return exceeds 60 C (Copper Development Association band); the 20 mm outlet port runs 0.95 m/s at 18 LPM, so the headroom rating uses a 22 mm outlet bore (0.79 m/s).

### 7.4 Serviceability

| Item | Procedure and owner |
|---|---|
| Tray cartridge | dry-break isolation valves either side; change on dP alarm; owner: hyperscaler or OEM site service; MTTR ~10 min |
| Plate guard | serviced only with the tray drained (back-flush preferred); owner: OEM depot |
| Disconnect and back-flush | close tray valves, disconnect and cap the UQD pair, drain via the cartridge housing; back-flush at 1.2x rated for 10 min through a 25 µm bag (Cd qualified in reverse) |
| PCM rework | standard pad replacement at GPU or package swap |
| LM FRU | factory pre-wetted plate-and-dam unit; replaced as a unit at package RMA (not inspected in the field); returned to the factory for rework |
| Spares | 2 % plates, 10 % cartridges per site per year (planning) |

### 7.5 Safety and leak management

| Hazard | Mitigation | Target or test |
|---|---|---|
| External leak | 1 perimeter lap + 2 bosses; dry He 100 %; proof 100 %; leak-before-break (ductile Cu, burst ≥ 3x MAWP); compatible with OCP ACS drip trays and rope sensors | ≤ 50 ppm leakers at shipment; ≤ 10 leaks per million plate-years (~1 FIT) design target; R90/C90 at 10 years on leak-tightness (zero failures in n = 22) |
| LM escape | dam + capture moat; conformal coat within 5 mm; **no aluminium within the LM zone** (Ga embrittles Al: steel load frames and backplates on T2/T3 SKUs); store ≥ -10 C | E5 porosity and cycling on warped packages |
| HV fault (PRISM-DC at 800 VDC on a conductive PG25 loop) | isolation in the module (Si3N4 AMB); plate bonded to protective earth; creepage and clearance per IEC 62477-1 at pollution degree 2 including the wet-fault case; all plates on one earth to prevent stray-current corrosion | UL/IEC 62477-1 isolation test plan |
| Over-pressure | MAWP 1.03 MPa; CDU relief | burst ≥ 3.1 MPa |
| Freeze | ship dry (5.3 step 8); PG25 in service | -40 C dry storage |

**Negative-pressure option.** With dual UQD08 pairs the Rev A tray loop needs only 17-20 kPa, so it fits sub-atmospheric (leak-proof) loops at 18 LPM. We will publish a rating curve for plate plus dual UQD08 at 30-50 kPa below atmospheric and market it as an option.

### 7.6 Mechanical integration

| Item | Requirement |
|---|---|
| Shock and vibration | ISTA 3A / ASTM D4169 with the plate installed. A 1.24 kg plate at 30-50 g gives 365-610 N; the load frame's hard stops must carry it, not the package (window 0.3-1 kN) |
| Clamp | load-frame FEA at 0.3-1 kN (packages) and 2 kN (TTV) in E1; bow under the 2 kN TTV clamp measured, not assumed |
| Orientation | tests at 0, 90 and 180 degrees; vertical blades fill at ≥ 1.5x rated flow for 10 min with ports up; pass: dP stable within 2 % and Tcase within 0.5 K of horizontal |
| Venting | commissioning degas through the CDU; header arches slope to the outlet port |

---

## 8. Applications and market entry

### 8.1 Ranked applications

| Rank | Application | Variant | Entry |
|---|---|---|---|
| A1 | Hyperscaler custom ASICs (TPU, Trainium, Maia, MTIA class) | PRISM-15 or -G zoned; R+ over dies with the tray filter | samples M12-15, qualified M18-24, **volume 2029** (AVC already ships TPU v8 and Trainium3 liquid products from 4Q26: the socket is contested) |
| A2 | NVIDIA reference designs | PRISM-G T1/T2; MCL insert (T3B) | through **NVIDIA thermal engineering** (central standardised design and purchasing); Group-A only as factory; realistic platform 2029-30 |
| A3 | 15-30 kW modules, Kyber-class blades, wafer-scale | PRISM-15, -15-HF, -W | 2028-29 |
| A4 | CPU / NVSwitch / CPO | PRISM-S | rack-kit only |
| P1 | 800 VDC rectifier and SST SiC modules | PRISM-DC direct-substrate cooler | demonstrator M9-12 with a module partner; volume 2028+ |
| P2 | 800 VDC shelf plates | keyed-orifice plate | rack-kit only |
| P3 | SiC traction | PRISM-A | licence 2028, vehicles ~2030-31 |

### 8.2 Power electronics, the second application

**Reference module:** a 1200 V SiC half-bridge for an 800 VDC rectifier or SST stage, 1.62 cm2 of SiC per switch, Ag-sintered Si3N4 AMB, PG25 at 45 C.

| Metric | Skived split-flow plate | PRISM-DC R core | Basis |
|---|---|---|---|
| ΔTj to coolant per 400 W switch, equal Ag-sinter interface | 31.4 K | 22.8 K | judge-corrected PE model (`appendix/design/pe/pe_run.out` B7) |
| Loss per cm2 of SiC at Tj 150 C | ref | **1.38x** | same |
| Power-cycling life at equal loss profile, cycles ≥ 1-2 s | ref | ~4-5x (ΔTj^-4.4 to ^-5 scaling of a 27 % smaller swing) | CIPS/LESIT-type exponent; to be measured |
| SiC area at equal loss and Tj | ref | ~-28 % | 1/1.38 |
| Cost at 100k/yr | pin-fin baseplate US$15-40 | ~US$35-55 (proposal US$32 at pre-rally copper, scaled by the verifier's corrections) | RFQ needed |

Limits: under a gap pad the shelf plate has no thermal advantage; automotive coarse-gap gains are 9-25 %, mostly fin area; below ~100 ms the die and AMB set Zth. Partner shortlist: SiC module makers (Infineon, Wolfspeed, onsemi, ST, Navitas) and 800 VDC shelf and SST makers (Delta, LITEON, Eaton). HV rules: 7.5.

**On "SSD converters".** The mission most likely means SiC converters (P1-P3). Solid-state transformers and solid-state DC breakers (15-25 kW of heat per MW, isolated substrates) fit PRISM-DC. SSD storage drives (E1.S / E3.S, 25-40 W, 1-2 W/cm2) gain nothing from the core and are excluded.

### 8.3 Go-to-market and business model

1. **Hyperscaler beachhead.** Co-design the zoned plate, tray filter and data pack; supply through a non-Group-A CM under our recipe, inspection and test cell. Google's clean multi-loop practice makes it the natural first R+ customer.
2. **NVIDIA via its thermal engineering team**, offering the reference-design data pack and an MCL-insert co-design (D7), with Group-A as manufacturer.
3. **OEM kits** (Dell, HPE, Lenovo, Supermicro): plate, tray filter, keyed orifices, rack-manifold rules.
4. **Transparency** as marketing: full OCP report, independent repeat, dP at three boundaries.

**Moat (what actually protects us):** the tie-braze recipe and per-strip controls (trade secret), the graded-artwork zoning tool, calibrated data, and co-design relationships. Patents are narrow and defensive (12). Time to copy after the OCP disclosure: 12-24 months for AVC/Auras-class houses (9.3).

### 8.4 Customer requirements and interface control

| Item | Plan |
|---|---|
| Target accounts | 2-3 hyperscaler ASIC programmes; one OEM; NVIDIA thermal engineering |
| NDA envelopes | MGX/Kyber tray CAD and the NVIDIA thermal design guide via an OEM partner (not yet obtained) |
| LOIs | at least one by G2 (M6); none, and D1 publication is re-scoped |
| Interface control drawing per SKU (PRISM-15, -G, -S4) | mount pattern, port type and position, load-frame and retention window, keep-outs, height, mass limit, flatness, TIM, coolant, flow and dP rating, pressure rating, leak class, cleanliness code, shipping state |
| Qualification | hyperscaler: 12-18 months from samples to first PO; NVIDIA reference design: engagement M6-12, design-in for a 2029-30 platform; OEM: 12-18 months after qualification |

### 8.5 P&L sketch (planning assumptions; `appendix/verify/final/final_system.out` §8-9, re-based from its US$162 / 141 to US$165 / 144)

| Case | ASP | Factory cost | CM margin + 3 % warranty | Our gross profit per plate |
|---|---:|---:|---:|---:|
| Hyperscaler ramp, 10k/yr | US$600 | US$400 | US$66 | US$134 (22 %) |
| Hyperscaler, 100k/yr, Rev A | US$330 | US$165 | US$30 | ~US$135 (41 %) |
| Hyperscaler, 100k/yr, C2 | US$330 | US$144 | US$27 | ~US$160 (48 %) |

Opex after qualification is about US$5 M/yr, including product-liability insurance (US$0.3-0.6 M/yr for leaks in US$4-9 M racks) and an IP reserve. A CoolIT/Ecolab suit would cost US$3-5 M through trial, so we buy IP-defence insurance or carry indemnity caps in contracts. Break-even is about 33-37k plates/yr; first revenue 2028 (non-US) and 2029 (US); break-even 2030-31.

**Facility value (15 kW class, per 100 MW = 6,667 plates).** At US$0.54-1.09 M per K per 100 MW (dry-cooler UA scaling; installed cost unverified) and +5.5 K headroom at P50, value is US$3.0-6.0 M against a price premium of US$0.37 M (Rev A) or US$0.17 M (C2): 8-16x and 18-35x. At P90 headroom (+0.6-1.8 K) it is 2-4x and 4-8x. Capture needs a loop-wide margin, a vendor inlet specification that allows it, and a buyer who owns the facility. NVIDIA already sells W45 as chiller-free, so the best story is hot-climate campuses and future-proofing for the next chip. **GPU class:** lean PRISM-G costs US$129-148 against ~US$110; value/premium is 0.3-3x. It is not a value case on its own.

---

## 9. Competitive landscape beyond CoolIT

### 9.1 Normalised comparison

V = vendor-only figure; I = independent or peer-reviewed. R'' is case-to-inlet including TIM unless stated.

| Player and product | Thermal figure (normalised where possible) | dP / flow | Flux | Filtration need | TRL / volume | What it would need to beat Rev A |
|---|---|---|---|---|---|---|
| **PRISM-15 Rev A** | 0.242 (paste) / 0.227 (PCM) cm2K/W at 1.2 LPM/kW PG25; core 0.113 | 7.6 kPa at 18 LPM | 128-200 W/cm2 drop-in; 350 with P + LM (misses 85 C) | 33 µm abs tray | TRL 4 now; 6 at M12; 7 at M18 | - |
| CoolIT 15 kW split-flow | 0.268 at 117 cm2 (0.23 if 100 cm2), paste | undisclosed (~22) | 128-150 | ~50 µm | demonstrator; volume maker | LM TIM on the same plate gives ~27.4 / 34.3 K (beats Rev A on paste and on PCM; loses to Rev A LM 23.9 / 28.8) |
| CoolIT OMNI (V) | "up to 60 % lower R than standard microchannel", no conditions | n/d | > 300 W/cm2 | n/d | product | publish conditions; area-normalised data |
| JetCool SmartPlate / Flex (V) | Rjf 0.040-0.058 K/W at 600 W over 1.0-3.0 LPM/kW (junction-referenced, ~7.5 cm2 die); 3rd-party "-25 % vs microchannel" | n/d | n/d | sub-mm jets | volume (Dell) | multi-kW, area-normalised data with dP |
| Frore LiquidJet (V) | 600 W/cm2 hot spot at 40 C; -6 to -12 C Tj on Rubin (press) | 1.7 kPa (claims inconsistent 4x vs 10x); 0.87 LPM/kW | 600 W/cm2 | fine | TRL 6-7; wafer-litho fab | conventional cost; independent data |
| Fabric8 / Wiwynn ECAM | 4 kW double-sided "48 % better than skived" (V); UIUC/Fabric8 -32 % R, -68 % dP vs pin fins (I, GaN) | n/d | > 350 W/cm2 (V) | 30-50 µm features | TRL 6-7 | 15 kW-class data; cost |
| ORNL diamond pin-fin (I) | 6.9 mK/W incl. TIM at 1 kW, water, 56 cm2 (18 W/cm2) | 9 kPa at 3 LPM | low | coarse | TRL 4 | high-flux data |
| ToneCooling GB300 (V) | 13 mK/W at 1.07 kW, 1.59 LPM/kW; c-to-mean-fluid 0.14-0.21 cm2K/W | 12 kPa | ~43-67 | n/d | product | conventional-band plate |
| AVC / Auras MLCP; Jentech MCL | no public data | - | - | - | Group-A volume; MCL expected mainstream from 2027 (analyst) | NVIDIA's choice decides the socket |
| Mikros / Jabil Normal Flow (V) | 0.02 cm2K/W core | 20.7 kPa at 1 kW/cm2 | > 1,000 W/cm2 | fine laminate | niche | system-level data at 15 kW |
| Accelsius NeuCool, two-phase (V, unnamed SI) | -9 C Tj on B200; 54 C inlet ≈ 45 C single-phase | - | 4.5 kW socket test | refrigerant loop | GA 2026 | holds where facility water ≤ 40 C; at 45 C, physics says two-phase is 6-14 K hotter than single-phase + LM |
| ZutaCore HyperCool, two-phase (V) | 0.3 LPM/kW; 2.8 kW certified | - | - | dielectric | product | 15 kW data |
| Corintis / Microsoft in-die (V); TSMC direct-to-silicon (unverified) | up to 3x heat removal, -65 % max Si rise; TSMC ~2.6 kW at ~63 K rise | - | - | - | prototype / research, 2028+ | silicon co-design (not a plate) |
| Peer-reviewed MMC (I) | 0.065-0.09 cm2K/W total (lab, small area) | - | 600-1,000+ | fine | lab | scale and filtration |
| Boyd, Vertiv/CoolTera, Motivair, nVent, Delta, Cooler Master | no public plate data | - | - | - | volume | - |

### 9.2 Why not two-phase or immersion now

At a 45 C facility loop, condensation pins saturation near 60 C, so a refrigerant manifold plate is **6-14 K hotter** than single-phase PRISM with LM: the condenser pinch costs 10-15 K and boiling HTC in 0.1 mm channels is no better than laminar PG25 (`appendix/physics/two-phase-option.md`). Accelsius's "+9 K" is measured against factory single-phase plates, not against a manifold plate. Immersion does not reach 15 kW packages. **Re-entry triggers:** facility water ≤ 40 C becoming standard; package flux above ~400 W/cm2 over whole dies; or an EU PFAS outcome that frees a low-GWP non-fluorinated refrigerant. D7 funds a watching brief.

### 9.3 Competitor response and time to copy

| Player | What it can copy | How fast | What stays ours |
|---|---|---|---|
| CoolIT / Ecolab | short-path manifold (it has OMNI); publish in its own OCP format; bundle chemistry and filtration | 12-24 months; continuations within its 2008/2012 specifications | per-strip tie-braze control; zoning tool; data lead |
| AVC / Auras (MLCP) | skive, kerf, fold, braze: all in their supply base | 12-18 months after the full OCP report | recipe, inspection, CM relationships |
| Jentech (MCL) | MCL with integrated manifold | already on NVIDIA's roadmap | MCL-insert co-design (D7) |
| Nidec | fin-tip-brazed covers (WO2026100588, published May 2026) | already industrialising | narrows our trade-secret moat; FTO item |

The moat is time and data, not patents. It lasts 12-24 months after publication, so the OCP disclosure is timed to coincide with samples in customers' hands.

---

## 10. Reliability, qualification and compatibility

### 10.1 Reliability targets and demonstration

| Attribute | Target | Demonstration |
|---|---|---|
| Leak-tightness, 10-year | R90/C90 | zero failures in n = 22 after 10,000 pressure cycles (0-MAWP), 1,000 thermal cycles 10-65 C, 50 storage cycles -40/+70 C (dry) |
| Thermal drift | R drift ≤ 5 %, dP drift ≤ 10 % | same 22 plates; Weibull fit on any drift |
| Tie integrity | no plastic set at proof; burst ≥ 4.5 MPa after cycling | lot over-proof + burst on 5 of the 22 |
| Particulate | ≤ 10 % fin-field dP, ≤ 1 K after 100x dose x 1,000 h | E4 quarter-scale plates |
| LM (T2) | no pump-out or dry-out after 1,000 cycles on a warped 120 mm package | TTV-C real-silicon vehicle; no claim above 10 cm2 until done |

**Acceleration.** Pressure cycles map about 1:1 to pump starts and transients (10,000 ≈ 10 years at ~3 per day). Thermal cycles use a Coffin-Manson model on the braze joints: a 55 K test swing against 15-20 K in the field gives an acceleration factor of ~8-13 at exponent 2, so 1,000 cycles cover ~10 years of daily cycling. Particulate dose is accelerated 100x by concentration.

The **life claim** is split into a dose-qualified claim (launch) and a field claim (after 300-500 pilot plates, 150-500 plate-years by M18-24). The draft's "10-year design life" is withdrawn as a field claim.

### 10.2 Drop-in and OCP compatibility checklist (condensed)

| Item | Rev A position |
|---|---|
| OCP thermal | R at 6 flows (25-150 % of rated) with the recommended TIM and with paste; R'' per area; both TTVs; low-flow average loss published |
| OCP dP | 6 points, 45 ± 2 C, three boundaries; 0-2 kPa transducers so the 25 % point (~0.6 kPa) is measurable |
| Pressure, leak | MAWP 150 psi; proof 1.5x 100 %; He ≤ 1e-6 mbar·L/s (OCP 1e-5) |
| Couplings | UQD08 / UQDB08 per OCP UQD v2.0.0; dual pairs above 18 LPM; no "UQD12" |
| Wetted materials | OFE Cu, Ag-Cu or Cu-Sn fillets (declared), 316L, peroxide-cured EPDM, PPSU/PEEK; **no Al, Zn, NBR, silicone or PTFE**; Ni only on the contact face |
| Quality | PFMEA, control plan, MSA, CpK ≥ 1.33 on leak and dP, PPAP-style package, serialised He, proof, dP and IR records |

**Open compatibility risk: a mandated Ni-plated wetted path.** Pre-braze electroless Ni-P does not survive a 790 C BAg cycle. Route C (Cu-Sn TLP at 600-700 C) with pre-plated electrolytic Ni is the only candidate (R7).

### 10.3 Coolant chemistry

The wetted path holds Ag-Cu fillets (routes A/B) or Cu-Sn intermetallics (route C) in PG25 for 10 years, with low wall shear in the fins (~10 Pa against ~26 Pa in 0.2 mm channels).

| E5c test | Content |
|---|---|
| Coupons and joints | Ag-Cu and Cu-Sn brazed coupons, OFE, 316L, EPDM, PPSU |
| Fluids | OCP-reference PG25 with two named inhibitor packages (one azole-based, one from a second supplier); PG30; water + inhibitor |
| Conditions | flowing loop at 65 C, 3,000 h, wall shear matched to the fins |
| Measurements | Cu, Ag and Sn ion release (ICP-MS); azole depletion (HPLC); pH, conductivity; galvanic current of Ag/Cu and Cu3Sn/Cu couples (zero-resistance ammeter); cross-sections; ATP and plate counts in 0.15 mm gap coupons with and without biocide |
| Pass | OCP PG25 Guidelines action limits (read in M1); no selective attack of fillets deeper than 10 µm |

**Commercial risk.** Ecolab/Nalco, CoolIT's owner, sells loop chemistry. We qualify at least two non-Ecolab inhibitor packages so that no customer depends on a competitor's chemistry.

---

## 11. Sustainability and compliance

### 11.1 Sustainability

| Metric | Rev A | CoolIT | Basis |
|---|---|---|---|
| Return temperature at 1.2 LPM/kW (P50 thermal limit, paste / PCM) | 59.0 / 62.9 C | 53.5 / 57.4 C | `appendix/verify/final/final_system.out` §2 |
| Return at 1.0 LPM/kW | 61.5 / 65.0 C | 56.0 / 59.9 C | same |
| Heat-pump COP lifting reuse heat to 80 C (PCM, 1.2 LPM/kW) | ~7.6 | ~6.2 | 50 % of Carnot |
| 100 MW site reusing 20 MW (EnEfG energy-reuse factor 20 % for new German DCs from Jul 2028) | ~0.8 MW less heat-pump power, ~US$0.5 M/yr | - | contingent on loop-wide supply temperature |
| Adiabatic water avoided, 100 MW, +5.5 K | hot-dry site: ~24-48 thousand m3/yr; temperate: ~0; humid tropics: 0 | - | illustrative climate hours |
| Cradle-to-gate CO2e per plate (screening) | ~8.6 kg (C2: ~7.6) | ~10.7 kg (est.) | Cu ~4.5 kg/kg, Ag ~200 kg/kg; ISO 14067 study in M6-9 |
| Pump-energy saving | ~76 kWh/yr per plate (~30 kgCO2e/yr) | - | homogeneous racks only; pays back embodied carbon in ~4 months |

**PFAS-free bill of materials.** The draft used PTFE-lined hoses and an FKM dam; ECHA RAC kept fluoropolymers in scope of the EU PFAS restriction (final opinion 2 Mar 2026). Rev A uses EPDM hoses, PPSU/PEEK fittings, EPDM seals and a non-fluorinated LM dam (Ni-plated copper ridge plus epoxy), all qualified in E5c. The plate is >95 % copper by mass and fully recyclable.

### 11.2 Compliance matrix (owner: 0.5 FTE compliance engineer plus outside customs counsel)

| Regime | PRISM-15 / -G / -S4 | PRISM-DC | Action |
|---|---|---|---|
| IEC/UL 62368-1, Annex G liquid-filled components (clause number differs by edition) | OEM certifies the system; we supply pressure, leak and material evidence | same | test-report package by M12 |
| IEC 62477-1 / UL isolation | - | required | isolation plan with module partner |
| PED 2014/68/EU | Art. 4(3) sound engineering practice (small volume, ~10 bar); no CE marking | same | SEP file |
| RoHS / REACH | Cd-free BAg; Pb-free Sn; SVHC declaration | same | declarations at sampling |
| Conflict minerals (US 1502, EU 2017/821) | Sn (route C), W (T3 barrier) | Sn | CMRT from suppliers |
| EU PFAS | PFAS-free BOM | same | E5c |
| Export | expected EAR99; confirm | same | classification by M6 |
| **US Section 232 (copper)** | 50 % on articles entirely or almost entirely of copper; 25 % on listed derivatives since 6 Apr 2026; heat-exchanger parts proposed for inclusion (not final) | same | **CBP binding ruling on the plate's HTS classification** (loose plate vs server part) |

**Landed cost at a US site** (`appendix/verify/final/final_system.out` §3, Rev A at US$162 basis; add ~US$3 for the Rev A additions):

| Build site | No 232 exposure | 25 % | 50 % |
|---|---:|---:|---:|
| Vietnam | US$162 | US$213 | US$264 |
| Taiwan (blocked until TW I606224 is charted) | US$166 | US$219 | US$271 |
| Mexico | US$178 | US$235 | US$292 |
| US (1.3x factory cost, COMEX copper) | US$218 | US$218 | US$218 |

Plates integrated into servers abroad may enter as server parts; loose plates (spares, US tray integration) are the exposed case. The ruling, not the factory cost, decides the site (D5).

---

## 12. IP posture

This is engineering-level reading, not a legal opinion. No full claim set has been read; outside counsel must confirm everything.

### 12.1 Families to clear

| Family | Live through | Risk before mitigation | Position |
|---|---|---|---|
| **CoolIT Split-Flow 2008**: US 8,746,330, 9,603,284, 12,101,906, 12,495,513 | 11 Aug-9 Sep 2028; '330 PTA unread (≤ ~Jun 2031) | **high** for US sales before expiry | The kerf is a weak design-around: the inter-fin passage stays continuous, ~49 % of inflow enters through fin tips under the window, the kerf is worth only 2.6 % of cell dT, and our brazed plates may supply '513's plate-and-seal element. Defences: invalidity (claims partly survived IPR2015-01276), ensnarement, missing limitations. **No US offers, sales or evaluation units before the opinion; US launch ≥ 10 Sep 2028 unless it clears.** Kerfs mandatory on US SKUs |
| CoolIT 2011-12 family: '567 (compliant member; remanded, outcome unknown), 9,453,691, 9,909,820, 10,274,266 (2021 IPR, some claims unpatentable), 10,415,597, 11,994,350, 12,460,878 (pump volute) | ~Feb 2032 + PTA | medium (unread claims) | chart; claims read so far need a pump or a compliant member |
| **TW I606224** (2012 family) | ~2032 if maintained | medium for Taiwan manufacture | chart via TIPO before any Taiwan build |
| Microfabrica US 12,255,123 (to ~2042) and 2016 family (~2036) | 2042 | high → medium-low | the draft's 0.4 mm offset fallback put jets on fin tips and is deleted; Rev A's jets land on the grate lip (3.2); chart after CFD |
| JetCool / MIT / Flex | 2037-45 | low-medium | no per-jet returns, no open cavity; chart |
| Intel US 12,133,357 and 11,804,418; Toyota US 11,428,478 (gridded microchannel assembly) | 2039-41 | medium | added to the chart |
| Nidec WO2026100588 (fin tips brazed to cover) | pending | medium | added to the chart |
| CoolIT compliant member ('886 / '733) | ~2040 | low | spring-screw gimbal on T3 |
| NVIDIA "intelligent plate"; CoolIT 9,052,252 | live | low | plate passive; chart before any tray module |
| NVIDIA AlN-heater TTV US 12,446,195 | live | low | clear before publishing our TTV method |

**Prior-art memo, corrected.** US 5,088,005 is Ciaccio / Sundstrand, not Harpole / TRW; Harpole and Eninger (1991) is non-patent literature. The anchors are Cooligy US 6,986,382 (expired), Delphi US 7,331,378 (status to verify), LLNL US 5,099,311 and Walpole US 5,099,910, framed as invalidity and ensnarement evidence. US law has no "practising the prior art" defence to literal infringement.

### 12.2 Filings and plan

| # | Filing | Decision |
|---|---|---|
| 1 | Tied, kerfed skived manifold plate with a graded meter in a stepped grate | file, narrow, with numeric limits; written without "split", "between the ends" or "halves the path" |
| 2 | Flux-graded flow-length rule | defensive publication (anticipated by Cooligy '312, Toyota '937, HUST '022) |
| 3 | Tie-bond screening and IR fingerprint | trade secret (unenforceable offshore; patenting would disclose it) |
| 4 | Filtration ladder | publish through OCP |
| 5 | TTV proxy method | defensive publication after clearing US 12,446,195 |

**Prototype location.** There is no research exemption for commercial development, so building and testing prototypes in the US is itself a technical exposure until Sep 2028. Locate Build A/B testing outside the US, or accept it as a low-damages risk on counsel's written advice; US customer evaluations wait for the opinion.

FTO budget: US$150-250k for charts and formal opinions on ≥ 20 US patents plus TW I606224; weeks 0-2 internal pull of claims, IPR decisions and claim-construction orders; opinion **at M4, before any US demo**. Monitor CoolIT continuations pending after the 2027 disclosure.

---

## 13. Risks, experiments, roadmap, budget and organisation

### 13.1 Risk register (ranked)

| # | Risk | Likelihood / impact | Early warning | Fallback |
|---|---|---|---|---|
| R1 | Tie braze: voids, wicking, kerf damage; per-strip detection at 0.8 mm base fails | medium / critical | E1 at M3 | routes B → C → D; base 1.0 mm (+0.7 K, still wins at 117 cm2); no-kerf (+0.4 K) **non-US only** |
| R2 | Segment-level uniformity worse than 1.15 | low-medium / +1-2 K on max | E2 at M3 | re-artwork the outlet row (+0.5 kPa) |
| R3 | Meter discharge CFD shows fin-top velocity > 0.5 m/s | medium / erosion, IP | CFD at M2 | wider lip, lower orifice velocity |
| R4 | Benchmark ambiguity used against us (footprint, case, TC bias) | high / credibility | reviewers | two TTVs, R'' per area, 8-TC replication, purchased plates, standing offer to test any CoolIT plate |
| R5 | OCP recommended TIM is a paste | medium / average margin falls to -10 % | read §5.2 in M1 | lead with maximum, uniformity, dP, capacity |
| R6 | Fouling or kerf impaction | low-medium / life claim | E4 | dose claim only; mandatory cartridge |
| R7 | Mandated Ni wetted path | medium / socket access | SOW reading | route C with pre-plated Ni |
| R8 | IP: Split-Flow, TW I606224, Microfabrica | **high / US timing** | FTO at M4 | non-US first; US ≥ Sep 2028; indemnity insurance |
| R9 | Cost above US$175 at 100k | medium / channel | RFQs at M1 | C2 route; meter-only per-SKU tooling |
| R10 | TTV heaters crack at 150 W/cm2 | medium / schedule | commissioning M3-4 | Cu-block cartridge TTVs |
| R11 | Supplier capacity (furnaces, skivers) | medium / schedule | RFQs | two sources each; long-lead orders at M1 |
| R12 | MCL / MLCP displaces lidded plates at NVIDIA | medium-high / rank A2 | analyst and customer signals | D7 MCL-insert study; G2 pivot decision |
| R13 | Section 232 classification | medium / landed cost +US$50-110 | CBP ruling | site decision tree (11.2) |
| R14 | CoolIT publishes a better plate in its own OCP format | medium / marketing | market | R+ and LM data in reserve; transparency |

### 13.2 Experiments

| # | Experiment | When / cost | Pass criterion |
|---|---|---|---|
| E0 | buy 2-3 incumbent GPU plates, a CoolIT 4 kW-class plate and UQD08 pairs; measure R, dP, Cv; weigh and measure height | M0-2 / US$40-60k | rig repeatability ≤ 1 K; Cv recorded |
| E1 | tie-braze matrix: kerfed coupons x routes A/B/C (+ belt C2) x base 0.8/1.0 x potted/unpotted kerfing x tip-plane tolerance; corrugation alignment; per-strip detection | M0.5-3 / US$120k | **every land strip ≥ 70 % bonded over any 10 mm**; unbonded-strip bulge detected at 0.8 mm; burst ≥ 4.5 MPa; flatness ≤ 20 µm |
| E2 | water table + single-cell CFD of orifice, lip, window, kerf | M1-3 / US$90k | segment max/min ≤ 1.15 at 18 LPM; fin-top velocity ≤ 0.5 m/s |
| E3 | TTV commissioning: TTV-A (AlN, ≤ 18 kW), TTV-100 and TTV-A2 (Cu-block cartridge heaters, 30 kW), TTV-25 (4 kW point), TTV-D (Cu-neck, ≤ 400 W/cm2); D5470 TIM metrology; pulsed-power transient | M2-5 / US$200k | heat capture ≥ 98 %; re-mount repeat ≤ 1 K |
| E4 | dose-equivalent fouling: 100x ISO 12103 + CuO + EPDM for 1,000 h, fin-field dP taps; orifice and lip erosion at 1x / 1.5x / 2x; base thickness under the lip by UT | M3-10 / US$100k | fin-field dP ≤ +10 %; dT ≤ +1 K; no measurable erosion |
| E5 | endurance on 22 plates (10.1); E5c chemistry (10.3); ISTA shock and vibration; orientation | M5-11 / US$250k | 10.1 targets |
| E6 | FTO claim pulls, charts, opinion | M0-4 / US$150-250k | clear, design-around or launch-date decision |

### 13.3 Test-infrastructure capability matrix

| Claim | Rig / TTV | Capability | Uncertainty (k = 2) | Status |
|---|---|---|---|---|
| Average, maximum at 15 kW, 117 cm2 | 40 kW PG25 rig, TTV-A | 18 kW at 155 W/cm2 rating (83 % at 15 kW) | ±0.6 K, ±3 % R | measurable |
| 100 cm2 hard mode | TTV-100 (Cu-block) | 30 kW | ±0.7 K | the AlN version would run at 97 % of rating: replaced |
| Q capacity 15.7-19.5 kW | TTV-A2 | 30 kW | ±4 % | direct above 18 kW only on TTV-A2 |
| 4 kW point | TTV-25 | 6 kW | ±3 % | measurable |
| 350 W/cm2 KPI | TTV-D Cu-neck | ≤ 400 W/cm2 | ±8 % | **case is a neck face, not a lid: published as R'' only** |
| dP at 6 flows | 0-2 / 0-10 / 0-100 kPa transducers | 0.4-70 kPa | ±0.25 % FS | measurable |
| Transient | pulsed supply, 1 kHz logging | 10 ms-10 s | ±0.3 K | measurable |
| Independent repeat | ISO/IEC 17025-accredited lab (scope: temperature, flow, dP), selected by M6 | - | lab's | booked at G2 |

### 13.4 Requirements traceability (abridged)

| Mission requirement | Design feature | Experiment | Pass | Gate |
|---|---|---|---|---|
| Beat average and maximum like-for-like | 7.7 mm flux-graded cells, tied 0.8 mm base, kerfs | E3 + build A/B | paste ≤ 33 K average, PCM ≤ 31 / ≤ 36 K | G2 |
| Beat uniformity | graded meter, outlet row, doubled outlet header | E2, E3 | segment ≤ 1.15; max - avg ≤ 8 K paste | G1, G2 |
| Lower dP | short path, ~80 % inertial | E0, E3 | ≤ 10 kPa at 18 LPM | G2 |
| Capacity and headroom | as above | E3 (TTV-A2) | ≥ 15.5 kW paste | G3 |
| Height, mass | skirted arched cap, folded plenum | E0 weighing; Build A | ≤ 21 mm, ≤ 1.3 kg | G1 |
| Durability | per-strip controls, dry test sequence | E1, E5 | 10.1 | G3, G5 |
| Fouling | mandatory cartridge, guard | E4 | dose claim | G4 |
| Freedom to operate | stepped meter discharge; kerfs; launch date | E6 | opinion | before any US demo |

Claims with no row (GPU-class win, 10-year field life, 4 kW with the drop-in core) are deleted.

### 13.5 Roadmap and gates (M0 = November 2026)

| Months | Work | Gate (kill authority: line manager, on gate-board advice) |
|---|---|---|
| 0-1 | RFQs; long-lead orders; read OCP §5.2 and PG25 Guidelines; FTO pulls; CBP ruling request; NDA envelope requests | - |
| 1-3 | E0, E1, E2, CFD; detailed design | **G1 (M3) Rev A freeze**: join route, base 0.8/1.0, C2 go/no-go. Kill if no route passes E1 by M5 |
| 3-5 | Build A (12 plates, laser/CNC parts); E3; E4 start | - |
| 4 | FTO opinion | US demo decision |
| 5-6 | 5 plates x 3 re-mounts, paste and PCM, both TTVs | **G2 (M6)**: PCM ≤ 31 / ≤ 36 K and paste ≤ 33 K, else re-scope D1 or pivot to MCL insert / licensing; ≥ 1 LOI; R+ kit decision |
| 6-9 | Build B (20 plates, production-intent dies); E5; independent lab | **G3 (M9)**: repeat within ±1.5 K |
| 9-12 | OCP-format report; R+ and LM stretch data | **G4 (M11-12)**: public at OCP Global Summit 2027 (US venue: data only, no offers, unless the opinion clears) |
| 12-18 | 300-500-plate pilot at the CM; PPAP; samples to two hyperscaler programmes; PRISM-G and PRISM-DC samples | **G5 (M18)**: qualified product |
| 18-36 | ramp 10k → 100k/yr (5.5) | volume 2029 |

### 13.6 Budget and probability

**12 months: US$7.3-8.9 M before contingency, US$8.4-10.7 M with 15-20 % contingency** (`appendix/verify/final/final_system.out` §6). Main lines: labour US$3.9-4.1 M (18 FTE); rigs, TTVs, IR station US$1.4-1.6 M; confocal, He, D5470 US$0.3-0.6 M; Build-B dies (moved forward) US$0.25-0.6 M; prototypes US$0.35 M; reliability and chemistry US$0.38-0.5 M; IP US$0.25-0.35 M; independent lab US$0.15 M; CFD/FEA/CT, fit-out, compliance, E0 US$0.3-0.7 M. **Tranche to G1: about US$2.3 M.** Months 12-18 add US$3.0-3.8 M (pilot, PPAP, remaining tooling); 18-month total US$11.4-14.5 M. Lean option (D3b): ~US$8.3 M with contingency.

**Probabilities (model x programme factors 0.8 x 0.9):** decisive PCM result at M12 **0.43**; paste average win at 117 cm2 0.58; paste maximum win 0.65; PCM average + maximum + dP 0.68; paste average win at 100 cm2: 0.32 (R-grade), 0.50 (R+). The dominant failure mode is a 1-3 month slip at E1 or TTV commissioning, not a thermal miss.

### 13.7 Organisation and decision rights

**Team (18 FTE budgeted; the roles below sum to 17.5, leaving 0.5 FTE unassigned):** programme lead 1 (accountable for gate recommendations); thermal-fluids 2 (chief architect within; responsible for E2, E3, design freeze); mechanical/FEA 2 (E1, load paths); manufacturing and supplier 2 (RFQs, builds, ramp); supplier-quality engineer at the Asian CM 1 (PPAP, per-strip controls); test lab 3 (E3, E5); reliability, materials and chemistry 1.5 (E4, E5c); quality 1; business development and customer engineering 1.5 (LOIs, ICDs); applications/OCP 1; compliance 0.5; cost engineering 0.5; IP coordination 0.5 with outside counsel (E6).

**Gate board:** line manager (chair, holds kill authority), finance delegate, programme lead, chief architect, plus an ex-OEM thermal architect (voting on technical gates) and patent counsel (advisory). Kill criteria are the gate conditions in 13.5.

### 13.8 Options analysis for the funding decision

| Option | Cost / time | P(public win vs CoolIT's published number) | Margin like-for-like | Moat |
|---|---|---|---|---|
| (a) TIM / interface programme on incumbent plates (LM) | US$2-3 M / 9-12 months | ~0.5 (LM unqualified above 10 cm2) | none (same plate) | none |
| **(b) PRISM Rev A** | US$8.4-10.7 M / 12 months | 0.58-0.68 | -3.4 K average, -5.5 K maximum (paste) | process know-how, data, 12-24 months |
| (c) license or partner an MMC vendor (Mikros/Jabil, AVC MLCP) | US$1-3 M + royalties / 6-12 months | unknown (no public 15 kW data) | unknown | partner's |
| (d) MCL co-design with Jentech | US$1-2 M / 2027-28 | n/a | n/a | shared |
| (e) two-phase hedge | US$0.2-0.3 M watching brief | n/a at 45 C | 6-14 K worse at 45 C | - |

Recommendation: **(b)**, with (a) folded in as the Tier 2 LM work it already contains, and (d) + (e) as the D7 hedge. Option (a) alone would beat CoolIT's published number with a different TIM, which CoolIT can match the next day.

---

## 14. Anticipated objections and our answers

1. **"You barely beat us like-for-like."** On paste, 31.0 K against 34.4 K: 1.5 K better than your best plate, and p ≈ 0.02-0.03 even by Welch against your three plates. The robust margins are the maximum (-5.5 K), uniformity, capacity (+22 %) and dP (~3x).
2. **"It is a TIM and clamp story."** Our headline is paste against paste; PCM is separate, and at package retention Rev A is 31.0 / 36.7 K. Our own 2-D penalty is now carried in full. An incumbent plate with LM (27.4 / 34.3 K) loses to Rev A with LM (23.9 / 28.8 K).
3. **"You beat a standard demonstrator."** True, and we say so. We publish in the OCP format CoolIT wrote and will test any CoolIT plate offered, including OMNI.
4. **"Not drop-in."** Stated: mechanically drop-in, ships with a mandatory tray filter; mixed racks need keyed orifices; R+ and P need ≤ 33 µm filtration.
5. **"The dP win evaporates at system level."** It is 6-18 % of loop head in homogeneous racks and zero in mixed racks. We value it as contingent and do not count it in the plate case.
6. **"You lose our 4 kW point."** The drop-in core does on PCM and paste. LM and PRISM-S4 beat < 0.009 C/W, but our reconstruction of your plate misses that datum by ≥ 37 %, so we claim nothing until a head-to-head.
7. **"Split-Flow, plainly."** The kerf is a weak design-around. No US offers, sales or evaluations before an opinion; unless it clears, no US sale before 10 Sep 2028.
8. **"Your maximum statistic is not ours."** We compare worst-of-N with worst-of-N and mean of plate maxima with 43.2 K. The edge-layout error is fixed and segment balance is 1.06.
9. **"Cost is understated; tariffs."** Corrected: US$165 (+31 %) against a like-sized US$126; parity per kW, better with C2. Section 232 exposure is 0-50 % by classification; a CBP ruling drives the site.
10. **"You cannot inspect your critical joint."** At 0.8 mm base an unbonded land strip bulges 2.2 µm at proof and is detectable; the base is gated on proving it. Per-strip controls, over-proof and CT are added; external seams fall to one.
11. **"Your fouling is worse and invisible."** At equal filtration, yes (7 against 15 years); behind our 33 µm cartridge ~12 years. Fin-field dP taps and BMC resistance drift make it visible.
12. **(NVIDIA) "Why switch our socket?"** On uniform lids we are at parity on the average and 1-3 K better on the maximum, at higher cost. We offer the reference-design data pack and an MCL-insert co-design, not a cost argument.
13. **(NVIDIA) "Transient?"** The thin base adds up to 1.0 K of excursion within 100 ms; absolute Tcase is 2.9-6 K lower at every pulse from 10 ms to 10 s. Measured in E3.
14. **"Your 350 W/cm2 margin is mislabeled."** Corrected to ~16 K like-for-like (114 vs 98 C); no drop-in plate reaches 85 C; published as R'' on a Cu-neck TTV.
15. **"Capacity exceeds your rigs and rules."** Ratings are capped at 19.5 kW by meter velocity; higher figures are thermal limits for the -HF SKU. A 30 kW TTV and a 40 kW rig are budgeted.
16. **"Two-phase beats your headroom."** At 45 C facility water a manifold two-phase plate is 6-14 K hotter than ours with LM; Accelsius compares with factory single-phase plates.
17. **"Your LM tier is not field-engineered."** Fixed: storage ≥ -10 C, no Al in the LM zone, non-fluorinated dam, FRU swapped at RMA, no claim above 10 cm2 until warped-package data exist.
18. **"You have not read the spec."** Correct today; §5.2 is a month-1 task and we plan for paste and PCM. Date corrected (effective 3 Sep 2026).
19. **"Your moat disappears on publication."** Agreed: 12-24 months of know-how and data. Disclosure is timed with samples at customers.
20. **"Sustainability and compliance are missing."** Added: PFAS-free BOM, 62368-1 evidence package, 59-65 C return water, water and carbon screening.

---

## Appendix A. Change log from draft to final

| Source | Changes made |
|---|---|
| **verify-physics** | own 2-D penalty in every absolute number (draft core PCM 28.4/33.3 → 29.9/34.8 K); probabilities republished; 4 kW "tie" → loss; 100 cm2 average → parity/loss and "maximum holds at every footprint" deleted; 350 W/cm2 label fixed (88.6 K was paste 0.07), margin → ~17-20 K, P-grade ~88 C; GPU-class average → parity; flux rule high-flux branch → 5-6 mm; scoping-model ramp patched; PG25 k → 0.49 (applied here, +0.4 K) |
| **verify-hydraulics** | 18-line edge error fixed; segment balance added; orifice shape and punch direction specified; square-weave radial-diffuser guard; matched-boundary dP; UQD08 pair → 14-24 kPa; tray loop → 42-51 kPa; equal-pumping-power labelled; return-limited flow-to-match; capacity capped at velocity rules; keyed orifices on PRISM in mixed racks; fin-field dP taps; jets kept off the base; 16 mm port dropped; bleed 1.1 mm |
| **verify-manufacturing** | lamination stamping refuted → folded plenum; bar stack error removed (arched cap); load paths completed; tie fraction 0.70; governing defect = one land strip; inspection re-scoped; kerf process defined; ≥ 3.5-4 mm blank; filler routes resized; furnace count corrected; mass boundary stated; Nidec on the FTO list |
| **verify-cost-market** | silver, furnaces, dies and yield costed (draft US$209, not 160); like-sized incumbent US$126; ramp US$370-430; 1M/yr comparison removed; PRISM-G costed; value case restated; Group-A GM 30-33 %; NVIDIA via thermal engineering; ASIC volume 2029; budget completed; P&L; OCP date |
| **verify-ip** | kerf design-around stated as weak; family lists corrected incl. TW I606224; prior-art memo corrected; Microfabrica fallback deleted and meter discharge redesigned; Intel, Toyota, Nidec added; opinion at M4 before any US demo; US launch ≥ 10 Sep 2028; filings 2-4 → publication or trade secret |
| **close-the-losses** | PKG-A adopted as Rev A (height 26.4 → 20.8 mm; mass 1.74 → 1.24 kg; cost US$209 → 165; per kW parity); C2 route; PRISM-S4; R+ grade; dose-equivalent E4 |
| **completeness critic** | 24 missing views added (sections 6.2, 6.5, 7, 8.2-8.5, 9, 10, 11, 13.3-13.8); 20 inconsistencies fixed, including PE ranking, capacity versus rigs, FTO timing, programme risk, life claim, scorecard column rules, per-SKU tooling, like-for-like headroom, LM storage, dry test sequence |
| **this revision** | k 0.49 re-run; OCP sweep (new concession: average at ≤ 0.5 LPM/kW); transient model; segment balance on the Rev A layout (outlet header 2x + outlet row); skirted cap (one perimeter seam); stepped grate (jets on the lip); mandatory 33 µm cartridge; +0.07 kg and +US$2.5 for these |
| **consistency audit** | All six final scripts re-run and reproduce their `.out` files exactly. Script notes: (1) `appendix/verify/ctl/cost_mass_height.py` costs PKG-A without the Rev A additions and its US$/kW lines still use the k 0.52 capacities (15.9 / 18.8 kW); the figures here are its P50 + US$3 over the `appendix/verify/final/final_thermal.out` capacities (15.7 / 18.5 kW), and an audit re-run with both changes gives 156/165/175 and 135/144/153 (±US$1 of 5.4); (2) `appendix/verify/final/final_system.py` §3, §8 and §9 run at US$162 / 141 and are re-based in 8.5 and 11.2; (3) `appendix/verify/completeness_checks.py` gives CoolIT + LM as 27.4 / 35.3 K from the synthesis lever (-9 K on the maximum, k 0.52), whereas the PCM re-test rule of 1.1 and the patched CoolIT-like model both give ~27.4 / 34.3 K, now used in 9.1 and 14. Corrected stale draft values: channel 0.15 → 0.20 m/s, Re ~35 → ~44, wall shear 7.7 → ~10 Pa (5,040 segments, not 6,480); kerf sites 12,960 → ~10,800 (15 lines, not 18); fouling plate-dP sensitivity 6 → ~8 % (fin dP is 1.07 of 7.6 kPa); silver US$13-24 → US$5-12 (route A thinned). PCM average 29.1 → 29.0 K (script 29.05 is 29.047). Guard dP and team FTE reconciled. Not re-derived by any final script: the 350 W/cm2 Tcase values (98 / 88 C; verify-physics gave 97 / 87 C at k 0.52; the quoted ~17-20 K margin was verify-physics', while 114 - 98 C is 16 K; the margin is now stated as ~16 K in 0.2, 6.4 and 14) and the tray-cartridge lives (160 / 16 / 1.6 d) |

## Appendix B. Proposals and scores

| Proposal | Mean score (physics / mfg / strategy) | Taken into PRISM |
|---|---|---|
| risk-first-12mo (PSM-12) | 61.3 (62 / 59 / 63) | base architecture: skived core, single braze, tied base, gated programme, transparency, purchased plates |
| advanced-manufacturing | 60.3 | printed-manifold rig; fin-conduction ceiling; CTE rules for MCL inserts |
| power-electronics | 59.7 | keyed orifice; grade ladder; direct-substrate SiC cooler (1.38x, judge-corrected) |
| conventional-cost (CrossComb) | 59.2 | fly-cut after braze; 3-point dP with CpK; laser seam option |
| jet-hybrid | 56.7 | inertial branch rule; leak-before-break |
| direct-to-die | 56.3 | interface tiers by face finishing; LM containment; TTV-C |
| system-platform | 56.0 | filtration ladder; keyed-orifice rule; 63 mm U-manifold; non-additive levers; E0 |
| hmmc-elite | 54.7 | HBM pedestal; zoning by heat |

Judge scores are in `appendix/design/panel_results.json`.

## Appendix C. Files

All under `appendix/`. New for this revision: `appendix/verify/final/final_thermal.py`, `appendix/verify/final/final_segbal.py`, `appendix/verify/final/final_transient.py`, `appendix/verify/final/final_coolants.py`, `appendix/verify/final/final_system.py` and their `.out` files. Verifier work: `appendix/verify/verify-*.md`, `appendix/verify/ctl/*` (gap-closer harness, PKG-A cost, mass, height, graded plenum, 4 kW SKU), `appendix/verify/vp_*.py`, `appendix/verify/hyd_budget.py`, `header_net*.py`, `appendix/verify/loop_rack.py`, `appendix/verify/rack.py`, `appendix/verify/mfg_checks.py`, `appendix/verify/cost_market_check.py`, `ip_*.py`, `appendix/verify/completeness_checks.py`. Models: `appendix/arch/cell2d.py`; `model/coldplate_model.py` (unchanged; patches applied in the scripts).

External sources: CoolIT 15 kW brief (https://www.coolitsystems.com/resources/news/15kw-coldplate/); OCP Cold Plate Test Specification v1.0.0 (https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf); Section 232 copper (https://phillipslytle.com/administration-restructures-section-232-tariffs-on-metal-and-derivative-products/ ; https://www.steelorbis.com/steel-news/latest-news/us-proposes-expanding-section-232-tariffs-to-14-additional-derivative-product-categories-1470151.htm); UQD vendor Cv and patent sources as listed in `appendix/verify/verify-hydraulics.md` and `appendix/verify/verify-ip.md`.
