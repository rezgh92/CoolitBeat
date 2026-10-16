# Fouling, clogging and filtration limits for fine micro-channel cold plates

**Key:** `fouling-filtration`  |  Script: `appendix/physics/fouling-filtration.py` (output: `fouling-filtration.out`)
**Operating point:** CoolIT 15 kW benchmark, 18 LPM PG25, 45 C in, 117 cm2 (108 x 108 mm), 128 W/cm2; HMMC candidate per `docs/cooling/model/coldplate_model.py`.

> Caveat on sources: the web-search budget for this run was exhausted before any query ran, so **no literature value below was re-verified online**. Industry numbers are from memory and tagged (H = confident, M = probable, L = recollection only). Verify before external use.

## 1. What today's loops look like (working assumptions)

| Item | Working value | Conf. |
|---|---|---|
| CDU / rack secondary-loop filtration (CoolIT CHx, Vertiv XDU, Motivair, nVent) | 50 um **nominal** cartridge or mesh; some offer 25 um pleated | M |
| GB200-class microchannel plate guidance | 25 um filtration recommended for the TCS loop | L |
| OCP ACS cold-plate requirements | plates must tolerate what a 50 um filter passes; particulate limited to ~50 um; inhibited PG25 / treated water | M |
| ASHRAE TC 9.9 TCS water quality | pH 7-9 (8-9.5 for mixed Cu/Al), inhibited, bacteria < 100 CFU/mL, Cl < 50 ppm, SO4 < 100 ppm, particulate < 50 um; conductivity limit loosely 1-3 mS/cm for inhibited glycol | M |
| Nominal vs absolute rating | 50 um nominal (85-95 % at 50 um) passes rigid particles to ~75-100 um; fibres and soft EPDM pass any mesh | H |
| Hydraulic rule of thumb | minimum flow passage >= 3x absolute filter rating (no bridging); >= 6x for no successive-deposition mechanism | M (3x is standard; 6x from Wyss/Dressaire microfluidic clogging work) |
| Field experience | skived 0.15-0.3 mm channels run 5-10 y on 50 um filters with periodic dP checks; < 0.1 mm channels have no fleet track record in DLC; JetCool nozzles are ~0.3-0.5 mm and rely on standard filtration | M |

Particle sources, with Stokes settling velocity v_s = (rho_p - rho) g d^2 / (18 mu) (PG25, mu = 1.25 mPa s):

| Source | rho (kg/m3) | size (um) | v_s at 50 um (mm/s) |
|---|---:|---|---:|
| Cu oxide flakes (galvanic / corrosion) | 6000 | 1-50 | 5.4 |
| Ni plating debris / peel flakes | 8900 | 1-200 | 8.6 |
| Brazing residue, Cu chips (factory) | 3000 | 10-500 | 2.2 |
| Al(OH)3 gel (mixed-metal loops) | 2400 | 1-100 | 1.5 |
| EPDM / UQD seal shedding | 1100 | 10-300 | 0.10 |
| PTFE tape / sealant (installation) | 2200 | 100-2000 | 1.3 |
| Inhibitor precipitates (silicate/phosphate) | 2000 | 1-20 | 1.1 |
| Biofilm flocs | 1050 | 20-1000 | 0.05 |

Settling matters only where residence time is long: a 50 um Cu-oxide particle falls 22 um in a 2 mm HMMC channel (2 % of height) but 0.5 mm at a slot dead-end (18 % of depth) and 22 mm in a rack manifold. **Dead-end headers, not channels, are where dense particles accumulate.**

## 2. Channel-width vs filter-rating regimes

W/d_abs (d_abs = largest particle the upstream filter passes):

| Filter | d_abs (um) | W=0.05 | 0.075 | 0.1 | 0.15 | 0.2 | 0.3 |
|---|---:|---|---|---|---|---|---|
| 25 um absolute | 25 | 2.0 bridging | 3.0 deposition | 4.0 deposition | 6.0 deposition | 8.0 safe | 12 safe |
| 50 um absolute mesh | 50 | 1.0 bridging | 1.5 bridging | 2.0 bridging | 3.0 deposition | 4.0 deposition | 6.0 deposition |
| 50 um nominal (typical loop) | ~90 | 0.6 sieve | 0.8 sieve | 1.1 bridging | 1.7 bridging | 2.2 bridging | 3.3 deposition |

W_min by the 3x rule: 0.075 mm (25 um abs), 0.15 mm (50 um abs), **0.27 mm (50 um nominal, i.e. today's loops without a plate-level screen)**.

Successive-deposition clogging (Wyss et al. 2006: a channel clogs after N* ~ C (W/d)^4 sticky particles; valid W/d 2.5-6) was turned into a particle budget with an ISO-4406-like distribution N(>d) ~ d^-2.2 truncated at d_abs. Absolute lifetimes are unknowable (C and loop cleanliness are each uncertain 10x), so lives are expressed **relative to a 0.2 mm skived channel on a 50 um nominal loop = 10 y (field calibration)**; C and concentration cancel:

| W (mm) | 90 um abs (50 nominal) | 50 um abs | 33 um abs | 25 um abs |
|---:|---:|---:|---:|---:|
| 0.05 | 1 y | 2 y | 2 y | 2 y |
| 0.075 | 2 y | 3 y | 3 y | 3 y |
| 0.1 | 3 y | 4 y | 4 y | 6 y |
| 0.15 | 6 y | 7 y | 12 y | no mechanism (W > 6 d_abs) |
| 0.2 | 10 y (ref) | 15 y | no mechanism | no mechanism |
| 0.3 | 23 y | no mechanism | no mechanism | no mechanism |

Two other mechanisms were checked at the model's actual channel velocities (HMMC u = 0.04-0.17 m/s because of ~20 000-60 000 parallel 2 mm segments; CoolIT-like 0.69 m/s):

- **No shear self-cleaning.** HMMC wall shear is 0.3-6 Pa; O'Neill drag on an attached 10 um particle is 0.3-5 nN versus ~35 nN rough-particle adhesion (JKR, W_A,eff 1.5e-3 J/m2). Anything that touches a fin stays. Skived plates at 0.69 m/s are also below the removal threshold for 10 um but above it for 50 um. The HMMC therefore relies entirely on **exclusion**, not on flow.
- **Inertial impaction at the slot-to-channel turn.** St = rho_p d^2 u / (18 mu W) for 50 um Cu oxide: 2.3 at W = 0.05, 0.7 at 0.1, 0.2 at 0.15-0.2 mm. Fine channels at higher velocity impact dense particles onto fin tips; 0.15 mm channels at 0.05 m/s do not.

## 3. Integrated inlet screen: pressure drop and loading

Plain-weave meshes (25 um opening/25 um wire, beta = 0.25; 50/36, beta = 0.34; 100/65, beta = 0.37). dP from a Brundrett-type screen correlation K = (7.125/Re + 0.88/ln(Re+1.25) + 0.055 log Re)(1-beta)/beta^2 cross-checked with Ergun on the mesh as a 2 d_w packed bed (d_eq = 1.5 d_w); the two differ 3-7x at Re_d < 50, so the conservative (Ergun) value sets areas. Clean, 18 LPM:

| Screen area | 25 um | 50 um | 100 um |
|---:|---:|---:|---:|
| 1 cm2 (port-sized) | 17-51 kPa | 8-28 kPa | 6-22 kPa |
| 5 cm2 | 1.0-4.2 kPa | 0.5-1.9 kPa | 0.3-1.2 kPa |
| 10 cm2 | 0.35-1.7 kPa | 0.16-0.73 kPa | 0.10-0.42 kPa |
| 117 cm2 (full plate) | 0.02-0.12 kPa | 0.01-0.04 kPa | < 0.03 kPa |

Area for < 2 kPa (conservative): 9 cm2 (25 um), 5 cm2 (50 um), 4 cm2 (100 um) clean; at 50 % pores blocked 180 / 86 / 46 cm2. A full-plate 25 um screen (4.7e6 pores) goes 0.12 -> 0.4 -> 3.0 kPa at 100/80/50 % open: **dP is not the constraint; loading is.** Days to 50 % blockage at a loop concentration c of particles above the screen rating: 25 um full-plate: 900 d at 1e-4/mL, 90 d at 1e-3/mL, 9 d at 1e-2/mL; a 5 cm2 50 um port cartridge: 13 d at 1e-4/mL. A plate-level screen finer than the CDU filter becomes the loop's filter and must be sized or serviced accordingly.

## 4. Uniform fouling film and 10 % channel blockage

Fouling film delta on all wetted surfaces (k_f = 0.6 W/mK, biofilm/gel), fixed 18 LPM, through the project model:

| gap/fin/H (mm) | clean dT (K) | delta = 10 um | 20 um | 30 um | channel-only dP factor at 10 um |
|---|---:|---|---|---|---:|
| 0.05/0.05/0.6 | 19.8 | +0.7 K, x1.22 | +2.8 K, x7.0 | blocked | x4.6 |
| 0.075/0.075/0.8 | 22.0 | +0.6 K, x1.04 | +1.5 K, x1.18 | +4.0 K, x3.2 | x2.5 |
| 0.1/0.1/1.0 | 24.1 | +0.7 K, x1.01 | +1.4 K, x1.04 | +2.5 K, x1.14 | x1.95 |
| 0.15/0.1/1.5 | 27.1 | +0.6 K, x1.00 | +1.1 K | +1.7 K | x1.54 |
| 0.15/0.15/2.0 | 26.5 | +0.8 K | +1.6 K | +2.5 K | x1.54 |
| 0.2/0.2/4.0 (skived-like) | 28.7 | +0.9 K | +1.8 K | +2.8 K | x1.37 |

The thermal penalty of a film is small for all widths (fin area ratio ~9 dilutes it); the hydraulic penalty is cubic in (b - 2 delta) and is what kills < 0.1 mm channels. Plate-level dP factors near 1.0 are an artefact of the HMMC channel term being only ~0.2 kPa of 6.2 kPa (see risk below).

10 % channels blocked: global effect is nil hydraulically (+0 % plate dP, 100 % flow on a 30-100 kPa branch) and +0.9 K on average conv dT. The local effect depends entirely on clustering. Base-spreading model (1 mm Cu base, h_eff = 158 kW/m2K, spreading length 1/m = 1.6 mm): excess case temperature = q a/(k t m) + q a^2/(2 k t) for a strip of half-width a (2-D disc with Bessel K0/K1 in brackets):

| Blocked region | excess hot spot |
|---|---:|
| one 0.1 mm channel | +0.5 K (0.1) |
| one 2 mm slot segment | +6.8 K (4.0) |
| 4 mm cluster | +17 K (11) |
| 10 mm cluster / 10 % as one strip | +67 K / +76 K (43 / 49) |

A thicker 2 mm base (CoolIT-like) only reduces the 10.8 mm-strip excess to +49 K. **Clustered blockage is a die-killer at 128 W/cm2 regardless of architecture; distributed blockage is benign.** Blockage clusters at slot dead-ends (settling) and at the first channels after the port (impaction), so those locations must be outside the die or must be flushed.

## 5. Fouling-tolerant HMMC variants (project model, 15 kW, 18 LPM, paste 0.05)

| Design | avg dT (K) | max dT (K) | dP (kPa) |
|---|---:|---:|---:|
| CoolIT-like skived split-flow (benchmark reconstruction) | 34.5 | 44.3 | 8.6 |
| HMMC 0.1/0.1 x 1.0 (baseline) | 24.1 | 28.1 | 6.2 |
| HMMC 0.1/0.1 x 1.5 | 22.9 | 26.9 | 6.2 |
| **HMMC gap 0.15 / fin 0.10 x 2.0** | **26.1** | **30.1** | 6.1 |
| HMMC gap 0.15 / fin 0.12 x 2.5 | 25.7 | 29.7 | 6.1 |
| HMMC gap 0.15 / fin 0.15 x 2.0 | 26.5 | 30.5 | 6.1 |
| HMMC gap 0.2 / fin 0.15 x 2.5 | 29.6 | 33.6 | 6.1 |
| HMMC 0.15/0.10 x 2.0 with 5 % flush bleed | 26.5 | 30.5 | 6.1 |
| HMMC 0.15/0.10 x 2.0, liquid-metal TIM | 21.6 | 25.6 | 6.1 |

Widening the gap from 0.10 to 0.15 mm costs ~2 K average (24.1 -> 26.1 K) and keeps a 24 % average / 32 % hot-spot margin over the benchmark; the manifold (short flow length) is what delivers the win, not the sub-0.1 mm channel.

## 6. Verdict: minimum channel width

**0.15 mm gap (fins 0.10-0.12 mm, 1.5-2.5 mm tall) is the defensible minimum for a 10-year drop-in product**, provided the plate carries its own 50 um absolute screen (W/d = 3, no bridging) and preferably sits behind a 25 um loop filter (W > 6 d_abs, no deposition mechanism). Relative-life estimate 0.6-1.2x a proven skived plate. 0.10 mm is a second, "performance" SKU only for loops that specify 25 um absolute CDU filtration (life ~0.6x skived; still in the slow-deposition regime, W/d = 4). 0.05-0.075 mm channels (HMMC-ultrafine/-fine, 19.8-22.0 K) are **not deployable**: W/d <= 2-3 even behind 25 um absolute, 1-3 y relative life, x2.5-4.6 channel dP at a 10 um film, impaction St > 1.

## 7. Design rules

1. Primary channel gap >= 3x the absolute rating of the last filter the plate sees; >= 6x where possible. Today's loops (50 um nominal) imply 0.27 mm without a plate screen; 0.15 mm with a 50 um absolute plate screen; 0.10 mm only with <= 33 um absolute.
2. Hierarchical widths: port >= 3 mm, level-1 manifold >= 1 mm, level-2 slots >= 0.3 mm, channels 0.15 mm; every upstream passage > 2x the next one so nothing sieves before the channels.
3. Integrated screen area >= 10 cm2 (pleated) or full-plate (117 cm2) with pore count >= 100x the channel-inlet count; clean dP < 0.5 kPa, alarm at 3x clean dP. Full-plate 25 um screen at 117 cm2: 0.12 kPa clean, 3 kPa at 50 % blocked, 160-200x inlet count.
4. No dead-end sieving headers under the die: give each inlet slot a 5 % bleed to the outlet through a >= 0.6 mm orifice (0.39 mm2 per slot at 1.5 kPa; slot-end velocity 0.6 m/s = 28x the settling velocity of 100 um Cu oxide). Thermal cost +0.4 K.
5. Put the port-adjacent channels and slot ends outside the die footprint, or accept +7 K per blocked 2 mm segment and +17 K per 4 mm cluster.
6. Serviceable: screen as a cartridge in the inlet fitting or at the rack manifold; plate dP port for monitoring; back-flush capable (reverse-flow tolerant manifold).
7. Materials: all-copper wetted path with Ni only where required (Ni flakes are the densest particle class); no Al anywhere in the loop; factory ISO-cleanliness flush to < 0.1 mg residue; EPDM hoses specified low-shedding; biocide-containing inhibited PG25 with pH 8-9.5.
8. Make the channel + metering dP >= 3x the manifold dynamic head (>= 1.5-2 kPa) with per-slot orifices (>= 0.4 mm, W/d > 4) rather than narrower channels.

## 8. Risks for the architecture

- The model's HMMC channel path is 0.19 kPa against a 0.5 kPa header dynamic head (ratio 0.37): flow distribution will be set by the manifold, not the channels, and any local fouling diverts flow away from the fouled region. Metering orifices are mandatory.
- Low channel velocity (0.04-0.1 m/s) means no self-cleaning and laminar deposition of fines; the plate's life is a function of loop cleanliness, which the product does not control. The screen becomes the loop's filter if it is finer than the CDU's.
- The 0.05-0.075 mm variants that produce the headline 19.8-22 K numbers should be removed from the roadmap unless a loop-level 10-15 um absolute filtration standard emerges.
- All literature values above are unverified in this run; the 25 um GB200 guidance and the ASHRAE particulate limit are the two most consequential and least certain.
