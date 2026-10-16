# Two-phase (flow-boiling) variant of the HMMC core: should it be in the architecture?

Script: `docs/cooling/appendix/physics/two-phase-option.py`
(full tables in `two-phase-option_output.md` next to it). Single-phase numbers come from our own
`docs/cooling/model/coldplate_model.py` so the comparison is on one footing.

**Bottom line.** Keep flow boiling as a *gated roadmap option*, not as part of the baseline architecture. On the
CoolIT operating point (45 C facility-class water, 15 kW, 128 W/cm2) a refrigerant HMMC is **hotter** than the
single-phase HMMC with liquid-metal TIM by 6-14 K at the Tsat (60 C) that a 45 C condenser actually forces, and
only reaches parity (within +/-2 K) at 30 kW with Tsat 55 C plus an enhanced boiling surface. The caloric term
(6.3 K) is indeed eliminated, but the isothermal condenser pinch costs 10-15 K, and in 100 um channels the
refrigerant's boiling HTC (10-25 kW/m2K, k_l = 0.07 W/mK) is no better than laminar PG25 (19 kW/m2K). The
single-phase "ultrafine" HMMC (0.05/0.05 x 0.6 mm) beats every two-phase case at Tsat >= 55 C.

## Method and assumptions

Same core as the single-phase design: Cu fins 0.1 mm, gaps 0.1 mm, 1.0 mm tall, 2 mm segments between inlet
and return slots, 1 mm base, 117 cm2 (108 x 108 mm). Dh = 182 um, L/Dh = 11, ~29,000 parallel 2-mm boiling
segments, total flow area 29 cm2, raw wetted/footprint area ratio 10.5. Uniform heating; +4 K hotspot penalty
on both technologies (boiling is mildly self-regulating, so this is slightly conservative for two-phase).

Fluid properties at Tsat 60 C from memory of REFPROP/manufacturer tables (**not web-verified in this run,
search budget exhausted; +/-10 %**): R1233zd(E) rho_l 1195, rho_v 19.5 kg/m3, hfg 172 kJ/kg, k_l 0.072,
mu_l 0.30 mPa s, sigma 11.5 mN/m, Psat 3.9 bar; R515B rho_v 62, hfg 128 kJ/kg, Psat 11.7 bar; Novec 7000
Psat 2.4 bar, rho_v 17.5; Novec 7100 Psat 1.0 bar (0.8 bar at 55 C), rho_v 8.8.

Equations:
- Flow: m = Q / (x_out hfg + cp_l dT_sub), dT_sub = 3 K; G = m / A_flow. Design x_out = 0.3.
- Tsat: isothermal condensation pins the pinch at the facility-water *outlet*: Tsat = 45 + Q/(m_fw cp) + 3 K.
- Wetted flux solved with fin efficiency coupled to h: q_w = q_fp / [(2 H eta + b)/p], eta = tanh(mH)/mH.
- Boiling HTC (three estimates, bracketing): Cooper nucleate pool boiling (Rp 1 um); Bertsch-Groll-Garimella
  2009 (Cooper + Hausen convective term with confinement-number enhancement; essentially Cooper here because
  Co = 5.5); Kandlikar-Balasubramanian 2004 laminar NBD branch with F_fl = 1 (upper bound, not credible beyond
  ~40 kW/m2K for these fluids). An "enhanced surface" case = 2.5 x Cooper (micro-porous / re-entrant cavities,
  literature 2-3x) is the realistic best case.
- CHF: Katto-Ohno 1984 (with subcooling factor); Qu-Mudawar 2004 q = 33.43 G hfg (rho_v/rho_l)^1.11
  We_L^-0.21 (L/Dh)^-0.36; Bowers-Mudawar 1994 q/(G hfg) = 0.16 We_L^-0.19 (L/Dh)^-0.54; hard cap
  q_w(x=1) = G b H hfg / ((2H+b) L); dryout assumed at x ~ 0.6 (literature 0.5-0.9 at G 100-300).
- dP: Lockhart-Martinelli laminar-laminar (C = 5) integrated over L; Zivi-slip acceleration; return slot,
  return manifold (5 m/s mixture, K = 4) and vapour port (12 m/s, K = 1.5) on homogeneous mixture density;
  2 kPa liquid-side inlet throttling (required for stability, see rules).
- Budget: dT_case-45 = (Tsat - 45) + q R_TIM + q t_base/k + q/h_eff.

## Results (R1233zd(E) unless stated; x_out 0.3)

| item | 15 kW (128 W/cm2) | 30 kW (256 W/cm2) | 35 kW (300 W/cm2) |
|---|---:|---:|---:|
| refrigerant flow (liquid) | 0.27 kg/s = 13.6 LPM (0.9 LPM/kW) | 27 LPM | 32 LPM |
| exit mixture volume flow | 259 LPM (rho_mix 63 kg/m3) | 518 LPM | 600 LPM |
| channel mass flux G / Re_lo | 92 kg/m2s / 56 | 185 / 112 | 216 / 131 |
| wetted wall flux q_w | 14.2 W/cm2 | 31 W/cm2 | 37 W/cm2 |
| h Cooper / enhanced / Kandlikar (kW/m2K) | 10.6 / 26 / 121 | 17.9 / 45 / 121 | 20 / 50 / 121 |
| conv term 2P (Cooper / enhanced / Kandlikar) | 13.4 / 5.8 / 2.4 K | 17.4 / 7.7 / 4.7 K | 18.4 / 8.2 / 5.5 K |
| conv term single-phase PG25 (same core) | 8.1 K | 15.6 K | 18.0 K |
| CHF Katto-Ohno (L-regime = x->1 limit) | 37 W/cm2 | 69 | 80 |
| x = 1 energy cap / dryout (x 0.6) | 38 / 23 W/cm2 | 76 / 45 | 88 / 53 |
| margin to dryout | 1.6 | 1.5 | 1.4 |
| Qu-Mudawar / Bowers-Mudawar (extrapolated) | 222 / 67 W/cm2 (non-physical, > cap) | 332 / 103 | 363 / 113 |
| plate dP (core 0.1 kPa; slot+manifold+port dominate) | 13 kPa, 3 W pump | 17 kPa, 8 W | ~18 kPa |
| single-phase HMMC dP | 6.2 kPa, 1.9 W (18 LPM) | 6.6 kPa, 4 W (36 LPM) | - |

Tsat forced by a 45 C facility loop with 3 K pinch: 60.7 C at 1.2 LPM/kW PG25, 58 C at 1.5, 55.6 C at 2.0,
53 C at 3.0 LPM/kW. Tsat 55 C therefore needs ~70 % more facility-water flow than the CoolIT benchmark.

**Case-to-45 C budget, average dT (max = +4 K), liquid-metal TIM both sides:**

| design | 15 kW | 30 kW |
|---|---:|---:|
| SP HMMC, PG25 45 C inlet (caloric 6.3 + TIM + base + conv) | **19.7** | **32.4** |
| SP HMMC ultrafine 0.05/0.05 x 0.6 mm | **15.3** | **24.1** |
| 2P HMMC, Tsat 60 C: Cooper / enhanced / Kandlikar | 33.6 / 26.0 / 22.6 | 42.8 / 33.1 / 30.2 |
| 2P HMMC, Tsat 55 C | 29.4 / 21.3 / 17.6 | 38.7 / 28.5 / 25.2 |
| 2P HMMC, Tsat 50 C (needs <40 C facility water) | 24.4 / 16.3 / 12.6 | 33.7 / 23.5 / 20.2 |
| **net benefit of 2P vs SP-LM, Tsat 60 / 55 / 50** | **-6 / -2 / +3 K** (enhanced) | **-1 / +4 / +9 K** (enhanced) |

With paste instead of liquid metal every row shifts by the same TIM term, so the ranking does not change.
Bracket: plain-Cu Cooper gives -14 to -10 K at Tsat 60; the Kandlikar upper bound gives -3 to +2 K.
Flux crossover (liquid metal, Tsat 60, enhanced surface) vs the baseline SP core is ~300-400 W/cm2; vs the
SP ultrafine core there is no crossover below 500 W/cm2.

Other fluids: R515B has the best HTC (20 kW/m2K Cooper) and 3x denser vapour (8 LPM/kW instead of 18) but
sits at 11-12 bar at 60 C (16 bar in a no-flow fault), carries 8.9 % R227ea (GWP ~300, HFC quota) and has
only 1.2-1.4x dryout margin. Novec 7000/7100: worst h (5-8 kW/m2K), 7100 sub-atmospheric at 55 C (air
ingress, 61 LPM/kW vapour), and 3M ended Novec manufacture with its PFAS exit (end-2025). Not candidates.

## Practical issues (summary)

1. **Condenser pinch is structural.** Isothermal condensation must sit above the facility-water *outlet*;
   a counter-flow liquid-liquid CDU only pays the 3 K approach. This 7-12 K handicap exceeds the 6.3 K
   caloric saving. The variant only makes sense with facility water <= 35-40 C or a 55-60 C heat-reuse need.
2. **Parallel-channel maldistribution / Ledinegg instability.** 29,000 segments share two manifold levels; a
   segment making more vapour has higher resistance and receives *less* liquid (positive feedback, the
   opposite of single-phase). Per-slot inlet orifices with liquid dP >= 2-3x the two-phase core dP are
   mandatory (included in the dP budget). Vapour back-flow into shared inlet slots is a specific HMMC risk.
3. **Dryout at hotspots.** Margin is only 1.4-1.6x at x_out 0.3; a 2x local hotspot pushes local x_out to
   ~0.6 and can dry out (wall temperature then runs away). With flow sized for 15 kW, 25 kW is marginal
   (x_out 0.52) and 30 kW dries out. Flow must track load, unlike single-phase where overload only costs dT.
4. **Vapour volumes and pressure containment.** 259 LPM of mixture leave a 15 kW plate (vs 18 LPM PG25):
   21-30 mm return port, 5 m/s headers; a 1 MW rack at x 0.3 returns ~0.3 m3/s (DN100 at ~40 m/s).
   R1233zd(E) plates need >= 10 bar rating (6 bar at an 80 C no-flow fault), helium-tight brazing,
   refrigerant-grade QDs, no elastomer permeation; R515B needs 25-30 bar.
5. **Cost and infrastructure.** R1233zd(E) ~USD 15-30/kg, R515B 20-40/kg (vs cents for PG25); kg per server,
   50-200 kg per rack CDU; a dedicated refrigerant CDU (ZutaCore/Accelsius class) with magnetically coupled
   pump, subcooling/NPSH control, receiver, leak detection. Incompatible with the PG25 TCS loops operators
   are installing now, which is CoolIT's whole pitch.
6. **Regulation (mid-2026 knowledge, not web-verified here).** EU F-gas Reg. 2024/573: HFC quota phase-down
   to 2050 (R515B's R227ea share is inside it); HFO/HCFO such as R1233zd(E) are Annex II (reporting, no
   quota). The ECHA universal PFAS restriction (2023 dossier; RAC/SEAC opinions 2025-2026; Commission
   decision expected 2026-2027) covers HFOs, HCFOs and HFEs; time-limited refrigerant derogations were
   floated, but data-centre cooling has an obvious non-fluorinated alternative (water/PG single-phase), which
   weakens any derogation case. TFA formation and RAC's TFA reprotoxic proposal add pressure. US: AIM Act
   does not block either fluid; Minnesota/Maine PFAS-in-products laws (2032 bans) can capture refrigerants
   in shipped hardware. 3M's PFAS exit removed Novec; Chemours/Honeywell/AGC remain.

## Design rules

1. Do not put two-phase in the baseline. Baseline = single-phase HMMC (ultrafine core where manufacturable)
   with liquid-metal/indium TIM; that already exceeds any two-phase case at Tsat >= 55 C by 5-15 K.
2. Gate the two-phase roadmap on three triggers: (a) PFAS/F-gas outcome leaves a >= 10-year window for
   R1233zd(E)-class fluids; (b) a customer with facility water <= 40 C or a 55-60 C heat-reuse requirement
   (then Tsat 50 C makes 2P worth +3 to +9 K); (c) footprint flux >= 300-400 W/cm2 over large areas, where
   single-phase conv (0.06 K per W/cm2) outgrows boiling (~q^0.33).
3. If built: R1233zd(E) first choice (3.9 bar, GWP 1, A1); R515B only if vapour-volume constraints dominate
   and a 25-30 bar plate is acceptable; no HFEs.
4. Size refrigerant flow for x_out <= 0.3 at the *hotspot* flux, not the average; control flow with load.
5. Per-slot inlet orifices with liquid dP >= 2x the two-phase core dP; separate (not alternating-shared)
   return slots if the HMMC manifold is reused; return headers and port at <= 5 and <= 12 m/s mixture.
6. Use enhanced boiling surfaces (micro-porous coating or re-entrant cavities on the fin walls); plain Cu
   gives Cooper-level h (10-20 kW/m2K) and loses to laminar PG25. Fin height can drop to 0.5-0.6 mm since
   eta falls to 0.6-0.8 at h > 30 kW/m2K.
7. Plate design pressure >= 10 bar (R1233zd(E)), helium-tight, no elastomers in the wetted path.
8. Treat all HTC numbers as +/-50 % (Cooper vs Kandlikar spread is 10x); CHF numbers are quality limits
   (Katto-Ohno L-regime), not DNB, and Qu-Mudawar is outside its range here (L/Dh = 11, We_L 1-7).

## Honest caveats

Two of the three drivers are well estimated (condenser pinch; energy balance / dryout quality); the third,
boiling HTC in 100-um, 2-mm channels at G ~ 100 kg/m2s, spans 10-120 kW/m2K across correlations. Even at
the optimistic end the variant does not beat single-phase HMMC at the benchmark condition; it wins only with
colder facility water or extreme flux. Nothing here undermines the single-phase architecture; the
"future-proofing" argument for two-phase is matched by the ultrafine single-phase core to ~500 W/cm2.
