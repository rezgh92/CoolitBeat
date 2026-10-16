# TIM strategy and direct-to-die: quantified options for the 128-350 W/cm2 regime

Key: `tim-and-direct-to-die`. Script: `tim-and-direct-to-die.py` (output in `tim-and-direct-to-die.out`). Operating point: 117 cm2 footprint, 15 kW = 128 W/cm2, 18 LPM PG25, 45 C inlet; hot-spot case 300 W/cm2 (35 kW on the same footprint at 1.2 LPM/kW, or a local hot zone).

**Source caveat.** The shared web-search budget was exhausted before this task ran, so no live datasheet fetch was possible. Datasheet values are taken from the sibling research notes that did fetch them (Shin-Etsu X23-7921-5: 0.050 cm2K/W at 25 um/20 psi; X23-8117: 0.061; Honeywell PTM7950: 0.04-0.08; Microsoft/Corintis "up to 3x", 65 % peak-rise reduction; TSMC CoWoS direct-to-silicon >2.6 kW; ORNL CuW direct-to-die; JetCool SmartLid has no public datasheet). Everything tagged [MEM] below is engineering memory and must be checked against vendor data before it enters a spec.

## 1. Method

The interface is modelled as `R'' = BLT/k + R_contact` (cm2K/W) and the interface drop as `dT_TIM = q'' * R''`. Min/nominal/max bands were built from physical BLT and k values, then reconciled with the quoted datasheet/literature bands. Full-stack numbers come from the team's own 1-D model (`coldplate_model.py`, HMMC-fine core: 0.075/0.075 x 1.0 mm Cu fins, 1 mm base, 2 mm flow length) by substituting `tim_R`. Package bow is modelled as a paraboloid gap `BLT(x,y) = BLT_min + w0 * ((x/L)^2 + (y/L)^2)/2` against a rigid plate, integrated over the 108 mm square. Ageing is a multiplier on nominal R''. CTE shear per cycle is `(alpha_plate - alpha_Si) * dT_cycle * half_length` (free-expansion upper bound). Everything is 1-D; treat each term as +/-30 %.

## 2. Option matrix

| Option | R'' adopted min / nom / max (cm2K/W) | Pressure | Flatness | Reliability | Service | Cost adder (117 cm2) [MEM] | Compatible with |
|---|---|---|---|---|---|---|---|
| 1 Standard grease (TIM2 on lid) | 0.04 / 0.07 / 0.17 (0.17 = 100 um warped-lid BLT) | 15-30 psi | <= 25 um | pump-out under warpage cycling, silicone dry-out > 85 C; 1.3-2x R'' at EOL | field rework | US$2-6 | any lidded package |
| 2 Phase-change pad (PTM7950 class, k 8.5) | 0.04 / 0.055 / 0.08 | 20-40 psi | <= 30 um | self-heals > 45 C; vendor < 10 % drift after 1000 cycles [MEM] | field rework (consumable) | US$4-12 | any lidded package (OCP OAI reference TIM) |
| 3 Graphite / CNT pad (Hitachi TC-001, PGS, Carbice, NeoGraf) | 0.035 / 0.065 / 0.13 | 50-150 psi | <= 50 um (absorbs 50-100 um bow) | no pump-out, no dry-out; creep, particle shedding | reusable, dry | US$8-30 | lids <= 50 cm2 where the clamp load exists |
| 4 Liquid metal Ga-In(-Sn) | 0.005 / 0.015 / 0.03 | 5-20 psi | <= 25 um | dissolves Cu (CuGa2), embrittles Al; oxide; migration; EGaIn freezes at 15.5 C | trained tech only | US$10-30 incl. Ni plating + dam | Ni-plated Cu lids (verify B200/B300 lid finish), bare Si; never Al |
| 5 Indium solder (reflowed) | 0.005 / 0.015 / 0.03 (0.005-0.01 only at BLT <= 60 um) | 0 (bonded) | <= 50 um | corner fatigue cracking under warpage; voids | not serviceable (plate+package = one FRU) | US$20-45 | OEM co-design on solderable lid; bare die only with CuW/CuMo/Si plate |
| 6 Sintered Ag | 0.002 / 0.005 / 0.01 | 5-30 MPa, 200-250 C | <= 20 um | power-module proven | never | US$25-60 | SiC-module baseplate SKU, not GPU TIM2 |
| 7 Direct-to-die (plate on bare die, LM + dam) | 0.005 / 0.015 / 0.03 at the interface; removes lid + TIM1 | 5-15 psi, < 0.3 MPa on die | <= 15 um, stepped for HBM/logic height (50-200 um) | as LM + die crack, warpage 100-300 um, CTE shear (sec. 5) | module-level | US$25-60 | bare-die modules (Google TPU; RTX 5090 FE precedent); B200/B300/MI355X need delidding |
| 8 In-die microfluidics (Microsoft/Corintis, TSMC) | 0.01 / 0.02 / 0.05 junction-to-fluid | n/a | n/a | seal/erosion/clogging (10-25 um filtration); vendor warranty | none | silicon-vendor cost | chip co-design only, 2028+ |

Indium metal foil (Indium Corp Heat-Spring) was also evaluated: 0.05-0.12 cm2K/W at 50-100 psi, i.e. no better than PCM and worse on clamp load; dropped.

## 3. Results

Interface drop `dT_TIM` (K), nominal (min-max):

| Option | 128 W/cm2 | 200 | 300 | 500 | Share of a 35 K budget at 128 / 300 |
|---|---|---|---|---|---|
| grease | 9.0 (5.1-21.8) | 14.0 | 21.0 (12-51) | 35.0 | 26 % / 60 % |
| PCM pad | 7.0 (5.1-10.2) | 11.0 | 16.5 (12-24) | 27.5 | 20 % / 47 % |
| graphite/CNT | 8.3 (4.5-16.6) | 13.0 | 19.5 (10.5-39) | 32.5 | 24 % / 56 % |
| liquid metal | 1.9 (0.6-3.8) | 3.0 | 4.5 (1.5-9) | 7.5 | 5 % / 13 % |
| indium solder | 1.9 (0.6-3.8) | 3.0 | 4.5 (1.5-9) | 7.5 | 5 % / 13 % |
| sintered Ag | 0.6 (0.3-1.3) | 1.0 | 1.5 (0.6-3) | 2.5 | 2 % / 4 % |
| direct-to-die LM (interface only) | 1.9 | 3.0 | 4.5 | 7.5 | 5 % / 13 % |
| in-die microfluidics (junction-to-fluid, replaces whole stack) | 2.6 (1.3-6.4) | 4.0 | 6.0 (3-15) | 10.0 | 7 % / 17 % |

Full stack, HMMC-fine core, case-to-inlet (K), 1.2 LPM/kW, nominal TIM, beginning of life:

| Stack | 15 kW / 128 W/cm2 avg / max | Tcase,max | Q cap at 85 C | 35 kW / 300 W/cm2 avg / max | Tcase,max |
|---|---|---|---|---|---|
| Benchmark CoolIT-like, paste 0.07 | 34.5 / 44.3 | 89.3 | 12.7 kW | 71.2 / 81.0 | 126.0 |
| HMMC-fine + grease 0.07 | 24.0 / 28.0 | 73.0 | 25.2 | 47.3 / 51.3 | 96.3 |
| HMMC-fine + PCM 0.055 | 22.0 / 26.0 | 71.0 | 28.3 | 42.8 / 46.8 | 91.8 |
| HMMC-fine + graphite 0.065 | 23.3 / 27.3 | 72.3 | 26.2 | 45.8 / 49.8 | 94.8 |
| HMMC-fine + liquid metal 0.015 | 16.9 / 20.9 | 65.9 | 42.1 | 30.8 / 34.8 | 79.8 |
| HMMC-fine + indium solder 0.015 | 16.9 / 20.9 | 65.9 | 42.1 | 30.8 / 34.8 | 79.8 |
| HMMC-fine + sintered Ag 0.005 | 15.6 / 19.6 | 64.6 | 47.9 | 27.8 / 31.8 | 76.8 |

Junction-to-inlet (1-D, no spreading credit for the lid; Si 775 um 0.060, TIM1 In 0.015, Cu lid 2.5 mm 0.064, HMMC core 0.068 cm2K/W, caloric 6.3 K):

| Junction stack | R'' cm2K/W | dTj-in at 128 | at 300 | Tj at 300, 45 C in |
|---|---|---|---|---|
| lidded + paste TIM2 | 0.276 | 41.7 | 89.2 | 134 |
| lidded + PCM | 0.261 | 39.8 | 84.7 | 130 |
| lidded + liquid-metal TIM2 | 0.221 | 34.7 | 72.7 | 118 |
| direct-to-die, LM on bare die | 0.142 | 24.5 | 49.0 | 94 |
| micro-channel lid soldered to die (In) | 0.135 | 23.7 | 47.0 | 92 |
| in-die microfluidics | 0.020 | 8.9 | 12.3 | 57 |

The in-die stack gives 79 % lower junction rise than lidded-paste in this arithmetic; Microsoft/Corintis quote 65 % on peak rise, so the model is in the right range and slightly optimistic.

Bow sensitivity (128 W/cm2, rigid plate; avg dT_TIM / corner-minus-centre spread): grease k 3.5 at 0/50/100/200 um bow: 10.7/0, 16.8/18, 23.0/37, 35.3/73 K; PCM: 5.6/0, 8.1/7.5, 10.6/15, 15.7/30 K; liquid metal: 1.5/0, 2.5/3, 3.6/6, 5.8/13 K. CoolIT's 10 K plate-to-plate spread at TC8 is what a 50-100 um bow difference does to grease. **Bow control is worth as much as the TIM choice for pastes; for liquid metal it is a second-order term.**

Ageing (EOL dT at 128 / 300 W/cm2): grease 11.6-17.9 / 27-42 K; PCM 7.4-9.2 / 17-21 K; graphite 7.7-8.8 / 18-21 K; LM 2.1-3.1 / 5-7 K (with Ni barrier; without, >2x after 1-3 years [MEM]); indium 1.9-2.5 / 4.5-6 K.

Ni barrier penalty: high-P electroless Ni-P (k ~5 W/mK) at 10 um = 0.020 cm2K/W = 6 K at 300 W/cm2, more than the liquid metal itself; electrolytic sulfamate Ni (k ~80) at 5 um = 0.0006 cm2K/W = 0.2 K.

Clamp load: a 300-1000 N module retention load [MEM, verify vs OAM/SXM specs] is only 4-12 psi over a 117 cm2 lid, below the minimum of every pad; on a 16 cm2 bare die pair it is 27-90 psi.

CTE shear per 40 K cycle at the die edge, Cu plate: 11.5 um (Blackwell ~40 mm die pair), 17 um (Rubin Ultra ~60 mm), 31 um (108 mm lid-less TTV) = shear strain 0.5-1.2 at 25 um BLT; CuW/CuMo/Mo: 2-10 um; Si lid: 0.

## 4. Recommendation per product tier

- **Tier 1, drop-in retrofit (lidded B200/B300/MI355X, field-serviceable).** PCM pad (PTM7950 class) at 20-30 psi with plate flatness <= 30 um over 100 mm and a floating/compliant core to cap effective bow at 50 um: 22 K avg / 26 K max at the benchmark point vs 34.4/44.2, and the TIM term is bounded 5-10 K with < 30 % ageing. Graphite/CNT is the alternative where a reusable dry interface matters and the lid is small enough to reach 50 psi. Do not use grease on 100+ mm packages: its bow and ageing tails (22 K, 2x) are what produced the benchmark's spread. At 300 W/cm2 every pad costs 16-20 K of a 35 K budget: Tier 1 does not reach the 2027-28 hot-spot regime.
- **Tier 2, OEM co-designed (plate ships with the module).** Liquid metal on a Ni-barriered plate: 16.9 K avg / 20.9 K max at 15 kW, 30.8 / 34.8 K at 300 W/cm2 (Tcase 80 C), Q-cap 42 kW. Mandatory: electrolytic Ni 3-5 um (or low-P ENi <= 5 um) on the plate contact face, **no Au top coat**, confirmed Ni finish on the lid, polymer dam/foam gasket, 20-30 um dispensed BLT, no aluminium anywhere in the module, storage above 16 C if EGaIn (Galinstan if cold storage is required). Sealed-FRU alternative: indium pre-form reflowed between the Ni/Au lid and Ni/Au plate (same 0.015, no serviceability, 0.3 K/cycle fatigue risk at corners; needs an OEM that accepts plate+package as one FRU).
- **Tier 3, chip co-designed (lidless / micro-channel lid, Rubin-Ultra-class and later).** Same HMMC core as a stepped pedestal plate bearing on the bare die through liquid metal with a dam (RTX 5090 FE precedent): junction-to-inlet 0.14 vs 0.28 cm2K/W, i.e. 24.5 K vs 41.7 K at 128 W/cm2 and 49 vs 89 K at 300 W/cm2. If the silicon vendor accepts a soldered micro-channel lid, the plate material must be CuW/CuMo or silicon (Cu gives 0.5-0.7 shear strain per cycle: solder fatigue, grease pump-out). Position the core as the micro-channel lid now; partner, do not compete, on in-die microfluidics (0.02 cm2K/W, 2028+).

## 5. Design rules

1. TIM budget: `dT_TIM = q'' R''`; at >= 200 W/cm2 any R'' > 0.03 cm2K/W fails a 35 K budget once ageing and bow are added. Specify R'' <= 0.02 (LM/In) for every product above 200 W/cm2.
2. Flatness and bow: plate contact face <= 25 um over 100 mm (lapped), compliant/floating core so the package-to-plate gap stays <= 50 um hot; verify with pressure film at 65 C.
3. Pressure: design the retention for 10-20 psi over the contact area; reject TIMs that need > 30 psi on lids > 50 cm2.
4. Liquid metal: electrolytic Ni 3-5 um, no Au, dam, 20-30 um BLT, Ni-finished counterface, no Al in the loop or module; re-measure R after 1000 cycles 10-65 C per OCP.
5. Nickel plating thermal check: `R'' = t/k`; keep t/k <= 0.001 cm2K/W (i.e. never high-P ENi > 5 um on a heat path).
6. Direct-to-die with Cu plate: liquid interface only; soldered die attach requires CTE <= 8 ppm/K plate (CuW, CuMo, Si).
7. Qualify each TIM at its own clamp pressure with ASTM D5470 and report BOL and post-cycling R'' with the plate data (test-metrics sibling).

## 6. Risks and uncertainties

- No live sources this session; PCM ageing, graphite k, LM ageing, clamp-load limits and costs are [MEM] and could be off by 2x.
- The task's 0.005-0.01 cm2K/W for indium solder requires BLT <= 60 um; production TIM1 is 100-200 um (0.015-0.03). Our nominal 0.015 is already a well-made joint.
- Package status: B200/B300 and MI300/MI355X lidded (sibling KB-H, agrees with author); the author recalls A100/H100 SXM modules as bare-die with a stiffener while the sibling table lists H100 as lidded: resolve from the Nvidia thermal design guide before any lidless claim. No public confirmation that Nvidia uses liquid metal on any data-center part; the RTX 5090 Founders Edition is the public precedent (consumer, bare die) [MEM]. JetCool SmartLid and any HPE/Lenovo direct-to-die product have no public datasheet.
- The sibling model's "direct-to-die, R''=0" row is unphysical for a bearing contact; use 0.015 (LM) and credit lid + TIM1 removal instead, as done here.
- 1-D lid term ignores spreading, so the lidded junction stacks are pessimistic by a few K; the comparison between stacks is robust, the absolute Tj values are not.

## Sources (via sibling research notes; URLs as recorded there)

- Shin-Etsu X23-7921-5 TDS: https://cdn.microsi.com/wp-content/uploads/2019/07/X23-7921-5-TDS-July-2019-.pdf ; X23-8117: https://www.microsi.com/applications-solutions/thermal-interface-material/tim-2/thermal-grease-X23-8117/
- Honeywell PTM7950: https://www.caplinq.com/ptm7950-most-thermally-conductive-phase-change-pad-with-very-low-thermal-impedance-that-works-in-vertical-applications-ptm7950.html
- Microsoft/Corintis in-chip microfluidics: https://www.hpcwire.com/2025/09/25/microfluidics-offers-3x-better-cooling-than-cold-plates-microsoft-says/ ; https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/ ; https://spectrum.ieee.org/microfluidics-cooling-ai-chips-corintis
- TSMC direct-to-silicon on CoWoS (ECTC 2025): https://semiwiki.com/semiconductor-manufacturers/tsmc/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/
- JetCool SmartLid / Flex: https://investors.flex.com/news/news-details/2024/Flex-Acquires-JetCool-to-Expand-Data-Center-and-Power-Portfolio/
- Frore LiquidJet delidded-Rubin claim: https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/
- Google TPU bare-die, 80 psi CDU: https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/
- Naddod GB300 liquid-metal 0.02 cm2K/W (low reliability): https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling
- ORNL CuW direct-to-die plate (IJHMT 256, 2026) and Kuo micro-channel-lid timing (CTEE Jan 2026): see competitors-singlephase.md and chip-roadmap-requirements.md.
- Memory-based physics: Prasher, "Thermal interface materials: historical perspective, status, and future directions", Proc. IEEE 94(8), 2006; DARPA ICECool programme reports; Galinstan/EGaIn property tables.
