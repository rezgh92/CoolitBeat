# hydraulic-detail: independent pressure-drop check, HMMC core vs skived split-flow plate

Script: `docs/cooling/appendix/physics/hydraulic-detail.py`
(full output in `hydraulic-detail-output.txt`, curves in `hydraulic-detail-curves.csv`). Operating point: 15 kW on
108 x 108 mm (117 cm2, 128 W/cm2), PG25 at ~50 C (rho 1005, mu 1.25 mPa s, cp 3930, k 0.52), 18 LPM nominal, 6-36 LPM swept.
Thermal terms are taken unchanged from `docs/cooling/model/coldplate_model.py` so that only the hydraulics differ.

## Headline

1. **The scoping model's laminar channel-friction term is 4x too low.** It uses the Shah & London *Fanning* f.Re but
   omits the factor 4 (dP = 4 f (L/Dh) rho u^2/2 = **2 f.Re mu u L / Dh^2**, which reduces to Hagen-Poiseuille 32 mu u L/D^2;
   the model has f.Re mu u L/(2 Dh^2)). Verified numerically (`check()`). Consequence: the CoolIT-like skived core is
   ~15 kPa, not ~4 kPa, and a total of ~22 kPa at 18 LPM (model said 8.6). The HMMC is barely affected because its
   channel friction is negligible (0.33 kPa). The architecture's hydraulic advantage is therefore *larger* than the model claims.
2. **HMMC core (nozzles + turns + 2 mm channels) = 1.4 kPa at 18 LPM vs 15.4 kPa for the skived core (11x).** The HMMC
   total (8.3 kPa) is dominated by plumbing: ports 3.0, level-1 headers 2.2, level-2 manifold channels 1.8 kPa.
3. **Pareto: HMMC wins at every pumping power.** At the CoolIT-like plate's 6.5 W hydraulic pumping power the HMMC
   (0.1 mm fins) runs 25 LPM and gives 22.2 K average vs 34.5 K (-12.3 K, -36 %); at equal average dT it needs 6.9 LPM
   and 0.17 W (37x less pumping power, 2.6x less flow). With 0.075 mm fins: 19.6 K at equal pumping power.
4. **The low core resistance creates a maldistribution problem**: the pressure variation along a level-2 manifold channel
   is ~30 % of the branch dP in the baseline (needs <= 10-20 %). Fix: 0.2 mm slots + 8 mm deep L2 channels (ratio 0.06),
   total still 8.6 kPa. Never feed L2 channels from one end only (ratio 1.2).

## Method and equations

Component loss network per fluid parcel, laminar correlations where Re < 2000:

| loss | equation | value used |
|---|---|---|
| fully developed laminar friction | dP = 2 f.Re(alpha) mu u L / Dh^2, f.Re = 24(1 - 1.3553a + 1.9467a^2 - 1.7012a^3 + 0.9564a^4 - 0.2537a^5) | Shah & London |
| developing flow (Hagenbach) | dP = K(x+) rho u^2/2, K -> K(inf) for x+ = L/(Dh Re) > 0.05 (all cases here have x+ >= 0.67) | K(inf) fit 0.6796 + 1.2197a + 3.3089a^2 - 9.5921a^3 + 8.9089a^4 - 2.9959a^5 (0.75-0.83 here); 1.4 as upper bound |
| sudden contraction | K = 0.5(1 - sigma) on the higher velocity | area ratios from geometry |
| sudden expansion | K = (1 - sigma)^2 on the upstream velocity (Borda-Carnot) | |
| 90-degree sharp turn | K_t = 1.2 (1.0-1.3 sensitivity) on the higher velocity | |
| dividing / combining manifold channel | friction = 1/2 of uniform-flow value (linearly decaying flow) + entrance 0.5 / exit 1.0 | |
| level-1 headers | K = 1.5 each on 1.2 m/s (sized for 18 LPM, scales with flow) | |
| ports / UQD | 3 kPa at 18 LPM, quadratic, identical for all plates | |

Geometry. HMMC: 0.1 mm Cu fins / 0.1 mm gaps / 1.0 mm tall (also 0.075 and 0.05), channels along x; inlet and outlet
slots 0.3 mm wide, 0.5 mm deep, running along y, alternating at 2 mm pitch (27 inlet, 27 outlet slots); above each slot a
level-2 manifold channel 1.2 x 4 mm (0.8 mm walls) fed from both ends by level-1 headers. Parallel channel segments:
540 channels x 54 segments = 29,160. Skived CoolIT-like: 0.2/0.2 x 4 mm, 54 mm half-length, centre inlet plenum 8 x 12 mm,
edge outlet plenums 6 x 12 mm. "Finer skived": 0.1/0.1 x 2 mm, 54 mm.

Velocities at 18 LPM: HMMC channel u = 0.103 m/s, Re = 15, Dh = 0.18 mm; slot 0.34 m/s; slot-to-channel window
0.69 m/s (the window, slot half-width x gap, is the throttle, not the channel); L2 manifold 1.16 m/s, Re 1700.
Skived: u = 0.69 m/s, Re = 213; finer skived u = 1.39 m/s.

## Results

Component breakdown at 18 LPM (Pa):

| component | CoolIT-like skived | finer skived | HMMC 0.1 x 1.0 |
|---|---:|---:|---:|
| ports | 3,000 | 3,000 | 3,000 |
| L1 headers / plenums (in + out) | 3,408 | 3,408 | 2,170 |
| L2 manifold channels (in + out) | - | - | 1,813 |
| nozzles (slot contraction, friction, expansion) | - | - | 131 |
| entry: window contraction + 90-deg turn + expansion | 352 | 1,224 | 514 |
| channel: fully developed + Hagenbach | 14,707 | 116,929 | 334 |
| exit: contraction + 90-deg turn + expansion | 318 | 1,594 | 384 |
| **core** | **15,376** | **119,747** | **1,362** |
| **total** | **21,784** | **126,155** | **8,346** |
| hydraulic pump power, W | 6.5 | 37.9 | 2.5 |

dP (core / total, kPa) and pump power (W) vs flow:

| LPM | CoolIT-like | finer skived | HMMC 0.10 | HMMC 0.075 | HMMC 0.05 |
|---:|---:|---:|---:|---:|---:|
| 6 | 4.9 / 5.6 / 0.56 | 39 / 40 / 4.0 | 0.2 / 1.2 / 0.12 | 0.3 / 1.3 / 0.13 | 0.6 / 1.5 / 0.15 |
| 12 | 10.1 / 12.9 / 2.6 | 79 / 82 / 16 | 0.7 / 4.0 / 0.80 | 0.9 / 4.1 / 0.83 | 1.3 / 4.6 / 0.92 |
| 18 | 15.4 / 21.8 / 6.5 | 120 / 126 / 38 | 1.4 / 8.3 / 2.5 | 1.6 / 8.6 / 2.6 | 2.3 / 9.3 / 2.8 |
| 24 | 20.9 / 32.3 / 12.9 | 161 / 173 / 69 | 2.2 / 14.3 / 5.7 | 2.6 / 14.6 / 5.9 | 3.5 / 15.6 / 6.2 |
| 30 | 26.6 / 44.4 / 22.2 | 204 / 221 / 111 | 3.3 / 21.8 / 10.9 | 3.7 / 22.3 / 11.1 | 4.9 / 23.4 / 11.7 |
| 36 | 32.5 / 58.1 / 34.9 | 247 / 272 / 163 | 4.6 / 31.0 / 18.6 | 5.1 / 31.5 / 18.9 | 6.5 / 32.9 / 19.7 |

The skived plate is 67 % viscous (linear in flow); the HMMC is 86 % inertial (quadratic), i.e. its total dP is set by
manifold and port velocities, not by the fins.

Pareto crossovers against the CoolIT-like plate at 18 LPM (34.5 K avg / 44.3 K max, 21.8 kPa, 6.5 W):

| HMMC | basis | flow LPM | total kPa | W | caloric K | avg dT K | gain |
|---|---|---:|---:|---:|---:|---:|---|
| 0.10 x 1.0 | equal total dP | 30.0 | 21.8 | 10.9 | 3.8 | 21.4 | -13.1 K (-38 %) |
| 0.10 x 1.0 | equal pump power | 25.1 | 15.6 | 6.5 | 4.5 | 22.2 | -12.3 K (-36 %) |
| 0.10 x 1.0 | equal avg dT | 6.9 | 1.5 | 0.17 | 16.5 | 34.5 | 37x less pump power, 2.6x less flow |
| 0.075 x 1.0 | equal pump power | 24.9 | 15.7 | 6.5 | 4.6 | 19.6 | -14.9 K (-43 %) |
| 0.05 x 1.0 | equal pump power | 24.4 | 16.1 | 6.5 | 4.7 | 17.6 | -16.9 K (-49 %) |
| recommended (0.2 mm slots, L2 1.2 x 8) | equal pump power | 24.8 | 15.7 | 6.5 | 4.6 | 22.3 | -12.2 K |

Note the thermal gain at equal pumping power comes from the fin/TIM/base terms (conv 12.6 -> 8.0 K, base 6.6 -> 3.3 K,
TIM 9.0 -> 6.4 K), not from the extra flow: the caloric term only moves 6.3 -> 4.5 K. Spending the dP budget on more flow
is a weak lever; spending it on finer fins or on manifold uniformity is a strong one. (Max dT uses the model's inherited
hot-spot penalties, 9.8 K measured for CoolIT and 4 K assumed for HMMC; the latter is unverified.)

Sensitivities (HMMC 0.1 x 1.0, 18 LPM, core / total kPa): K_turn 1.0-1.3: 1.27-1.41 / 8.25-8.39; K(inf) = 1.4: 1.37 / 8.35
(irrelevant at Re 15); slot 0.15 / 0.20 / 0.40 mm: 4.96 / 2.81 / 0.88 core; flow length 3 / 4 mm (same L2 size): 3.0 / 5.3
core; fins 0.05 x 1.0: 2.3; fins 0.05 x 0.6: 3.2; L2 fed one end only: total 13.8 kPa and header variation 1.2x the branch dP.
Manufacturability variants with L2 channels resized to keep ~0.6-0.8 m/s: L = 3 mm, 1.8 x 6 mm channels (1.2 mm walls):
6.2 / 12.0 kPa; L = 4 mm, 2.4 x 8 mm (1.6 mm walls): 7.3 / 12.8 kPa, both with uniformity ratio <= 0.02 and avg dT 23 K at
equal pumping power. Skived-plate uncertainty (its fin pitch is a guess): 0.25/0.25 x 4 mm gives 10.2 / 16.6 kPa, 0.15/0.15 x 3
gives 36 / 42 kPa, so the benchmark total is 17-42 kPa; CoolIT does not disclose it.

## Comparison with published manifold-microchannel data

WebSearch was unavailable this turn (shared budget exhausted), so the literature values below are from memory and must be
verified before external use: Escher, Michel & Poulikakos (2010, J. Heat Transfer) ultrathin MMC, 2 x 2 cm, water,
~1.3 L/min: ~0.09 cm2 K/W at ~0.22 bar (moderate confidence); Drummond et al. (2018, IJHMT) hierarchical MMC array,
15-33 um channels, 150-470 um deep, pressure drops of order 10-160 kPa over ~1 L/min flows (low-moderate); Jung et al.
(2019, IJHMT) 3-D manifold embedded cooling, water, dP of order 10-60 kPa (low); Ryu, Choi & Kim (2003, IJHMT) numerical:
MMC halves thermal resistance vs straight microchannels at equal pumping power, optimum channel width ~ tens of um
(moderate); Harpole & Eninger (1991) originated the concept at ~1 bar class. Applying this script's network to
literature-class geometries gives core dP of 11 kPa (Escher-class, j = 5.4 cm/s, 50 um channels, 1 mm flow length),
4 kPa (Drummond-class) and 11 kPa (Jung-class): the same order as the reported 10-60 kPa (within ~2x, with their colder,
more viscous water and narrower manifold passages explaining much of the gap). Our plate runs at a volumetric flux of only
2.6 cm/s with 100 um channels and 0.3 mm slots, so a 1.4 kPa core is consistent with the literature scaling
(friction ~ j L^2/(H Dh^2), inertial terms ~ j^2/w_s^2); it is low because the plate is large, not because the physics is optimistic.

## Design rules

1. Use dP_fd = 2 f.Re mu u L / Dh^2 (Fanning f.Re); fix `coldplate_model.py` line `dp_ch`. All skived-plate dP figures in
   `model_output.md` are ~2.5x low in total (4x in the fin term).
2. For a manifold plate the fins are hydraulically free; the throttle is the slot-to-channel window (slot half-width x gap).
   Keep the window velocity 0.7-1.4 m/s: w_s = 0.15-0.3 mm for j = 2.6 cm/s. Core dP scales as (1/w_s)^2.
3. Flow-uniformity criterion: pressure variation along the L2 manifold channel (max of half the laminar friction and
   rho u_m^2/4) must be <= 0.1-0.2 of the branch (core) dP. Baseline fails (0.29). Meet it by (a) 0.2 mm slots and (b)
   L2 channels sized for u_m <= 0.6 m/s (1.2 x 8 mm for 2 mm pitch; 2.4 x 8 mm for 4 mm pitch), fed from both ends or
   tapered. One-end feed is not acceptable.
4. Spend the dP budget deliberately: target core 3-5 kPa (self-balancing), total <= 12 kPa at 18 LPM, which is still
   ~half of the skived benchmark and leaves a 2x margin for ports/UQDs sized for 15 kW plates.
5. Flow length 2-4 mm all work hydraulically (core 1.4-7.3 kPa); choose 3-4 mm for machinable 1.2-1.6 mm manifold
   walls. Fin height 0.6-1.5 mm changes core dP by only +15 % / -7 %; choose by fin efficiency and skiving limits.
6. Finer fins cost almost nothing hydraulically in the HMMC (0.05 mm: +0.9 kPa core) but are impossible in a 54 mm
   skived path (120 kPa). The manifold is the enabler for fine fins; do not pursue "finer skived".
7. At equal pumping power run 24-25 LPM (1.65 LPM/kW); at 1.2 LPM/kW keep 18 LPM and bank the dP margin for the
   facility loop. Pumping power at equal thermal performance is 37x lower (0.17 W vs 6.5 W per plate).

## Uncertainty and honesty check

Per-component +/-25 %; K_turn and K(inf) move the HMMC core by <10 %; the entry expansion term (171 Pa) may be partly
double-counted with the turn, so the core is 1.2-1.4 kPa. The dominant uncertainty is the plumbing (ports, headers:
+/-50 %), giving HMMC total 6-11 kPa. Not resolved here: 3-D flow in the slot-to-channel turn (bypass near fin tips if
the land is short relative to fin height; at land/H = 1.7 this needs CFD), manifold-level maldistribution across the 27
channels (L1 header design), transition in L2 channels at Re ~1700, and the 4 K hot-spot assumption. Nothing in this check
undermines the architecture; it strengthens the dP claim and adds a firm manifold-sizing rule. Practical risk: 100 um gaps
at 0.1 m/s have no self-flushing; require <= 50 um filtration and a clogging/fouling test, and prefer 0.1 mm over 0.05 mm
gaps unless the facility water spec is tight.
