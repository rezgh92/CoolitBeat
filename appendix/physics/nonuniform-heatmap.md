# Non-uniform heat-map check: reticle dies + HBM on the 15 kW-class cold plate

Key: `nonuniform-heatmap`. Script: `docs/cooling/appendix/physics/nonuniform-heatmap.py` (full console output in `nonuniform-heatmap.out` beside it).

## 1. Question

The benchmark (CoolIT 15 kW brief) and our 1-D model both assume a uniform 128 W/cm2 TTV over 117 cm2. A real 15 kW-class accelerator concentrates ~93 % of the heat on four reticle dies at 300-400 W/cm2, with HBM at 20-80 W/cm2 sitting 0.3-0.5 mm lower. Does the HMMC architecture still beat a CoolIT-like skived split-flow plate, by how much, and what does zoning and the non-planar HBM interface require?

## 2. Package and operating point

| item | value |
|---|---|
| plate / base footprint | 108 x 108 mm (117 cm2, calibrated), Cu k = 390 W/mK |
| GPU dies | 4 x 26 x 33 mm (2x2 block, 1 mm gaps), 350 W/cm2 -> 4 x 3.0 kW = 12.0 kW |
| HBM | 16 x 11 x 12 mm (2 cols x 4 rows per side), 40 W/cm2 -> 53 W/stack, 0.85 kW |
| total / flow | 12.85 kW; 1.2 LPM/kW = 15.4 LPM PG25 (rho 1005, cp 3930), 45 C inlet |
| stretch case | dies 400 W/cm2 + HBM 60 W/cm2 = 15.0 kW at 18 LPM |
| die TIM | paste 0.07 cm2K/W (CoolIT-like), 0.05 (HMMC thin BLT), liquid metal 0.015 |
| HBM step | HBM top 0.4 mm below die top |
| Tj estimates | GPU: + q'' x 0.05 cm2K/W (lidless, 0.6 mm Si); HBM: + P_stack x 0.3 K/W (+-50 %) |

Note: the task's "HBM total 1.5-3 kW" is inconsistent with 16 stacks at 20-40 W/cm2 (21 cm2 -> 0.4-0.85 kW); I kept the flux values and swept HBM flux to 80 W/cm2 (1.7 kW) instead.

## 3. Method

* **Base conduction (3-D, spectral).** Steady conduction in the Cu base (thickness t) is solved exactly as a 2-D cosine series (adiabatic edges) with top flux q''(x,y) and a Robin fin-side condition, i.e. the Lee/Yovanovich/Muzychka multi-source spreading solution on a 0.5 mm grid. Check V2: one 26 x 33 mm die at 350 W/cm2 agrees with the Lee et al. (1995) closed form within 5-7 %; spreading lowers the die-centre temperature < 2 % relative to 1-D for t <= 3 mm, so **for a reticle die the base is a pure series resistance**.
* **Fin side.** Fins are lumped into h_eff from the 1-D model's laminar correlations: CoolIT-like 101 kW/m2K, HMMC (0.1/0.1 x 1 mm, L = 2 mm) 157-167, HMMC-fine (0.075 x 0.8 mm) 215-225; nearly flow-independent, so zoning does not change h.
* **Fluid energy balance.** HMMC: every 2 mm segment gets inlet fluid, T_f = T_in + 0.5 q''_bot/(rho cp V''_local), with V'' set by the manifold (slot pitch, V'' ~ 1/L^2 at constant manifold pressure, or slot width). Split-flow: T_f(s) = T_in + integral(q''_bot ds)/(m' cp) marching outward from the centre feed per strip. Both are linear in bottom temperature, so slab + fluid are solved together with GMRES (energy balance closes < 0.1 %). An explicit fixed-point coupling diverges in starved zones.
* **Case/junction.** T_case = T_base,top + q'' R''_TIM(local). Check V1: the uniform 15 kW TTV reproduces the 1-D model (34.7 K / 24.3 K avg) and gives a split-flow outlet-edge max of 40.3 K, i.e. ~6 K of CoolIT's 9.8 K hot-spot penalty is caloric gradient.
* **Cases.** C-x-U / C-y-U: split-flow across the dies then HBM (x) or along the HBM columns (y). C-y-Z: channel zoning (die columns 1.75x, HBM 0.3x, margin 0.1x). H-U: uniform HMMC. H-Z1: 2x over the die block (1.53/0.77). H-Z2: heat-proportional 3-zone (die block 3.0x = 91 % of flow, HBM columns 0.32x, unheated 0.04x). H-Z3: 2.9/0.5/0.04.

## 4. Results (primary package, case-to-inlet dT in K; Tj in C)

| config | h_eff die | T_f under die avg/max | die case dT avg / max | Tj GPU max | T_f under HBM avg/max | HBM case dT max (pedestal) | Tj HBM max | across-die spread p99-p2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| C-x-U CoolIT-like, flow across die then HBM | 101 | 9.1/18.1 | 80.0 / **88.6** | 151 | 19.6/20.8 | 43.8 | 105 | 28.5 |
| C-y-U CoolIT-like, flow along HBM columns | 101 | 11.3/23.1 | 82.1 / 93.2 | 156 | 1.2/6.0 | 31.5 | 92 | 30.7 |
| C-y-Z CoolIT-like, zoned channels | 103 | 6.5/13.2 | 77.4 / 85.0 | 147 | 4.2/16.0 | 36.4 | 97 | 22.5 |
| H-U HMMC uniform flow | 157 | 18.1/20.1 | 64.0 / 68.8 | 131 | 2.2/5.0 | 23.3 | 84 | 22.1 |
| H-Z1 HMMC 2x over dies | 160 | 12.0/13.2 | 57.9 / 61.5 | 124 | 2.8/5.8 | 23.3 | 84 | 17.3 |
| H-Z2 HMMC heat-proportional | 167 | 6.4/6.7 | 52.3 / **54.1** | 117 | 7.2/12.9 | 29.9 | 91 | 7.6 |
| H-Z3 HMMC 2.9/0.5/0.04 | 167 | 6.6/6.9 | 52.5 / 54.4 | 117 | 4.8/10.3 | 28.5 | 89 | 8.1 |
| H-Z2f HMMC-fine 0.075 mm | 225 | 6.4/6.7 | 47.3 / 48.7 | 111 | 7.0/12.0 | 27.4 | 88 | 6.2 |
| H-Z2-LM HMMC + liquid-metal die TIM | 167 | 6.4/6.7 | 40.0 / 41.9 | 104 | 7.2/12.9 | 29.9 | 91 | 7.6 |
| H-Z2f-LM HMMC-fine + liquid metal | 225 | 6.4/6.7 | 35.1 / **36.5** | 99 | 7.0/12.0 | 27.4 | 88 | 6.2 |

Budget at the hottest die cell (caloric | base+conv | TIM): C-x-U 13.9 | 50.2 | 24.5 = 88.6 K; H-U 20.1 | 31.2 | 17.5 = 68.8; H-Z2 6.7 | 29.9 | 17.5 = 54.1; H-Z2f-LM 6.7 | 24.5 | 5.2 = 36.5. Pressure drop (1-D model, +-30 %): CoolIT-like 7.9 kPa, HMMC uniform 6.2, HMMC-Z2 6.9 kPa (3x die-zone velocity adds 0.7 kPa; channel dP is only 0.07 kPa at baseline).

**Zoning sweep (HMMC, HBM zone 0.32x):** die-zone factor 1.0 / 1.5 / 2.0 / 2.5 / 3.0 gives T_f,die 18.1 / 12.2 / 9.2 / 7.5 / 6.4 K and die max dT 68.8 / 61.8 / 58.1 / 55.7 / 54.1 K. The gain saturates around 2.5-3x (die block takes 75-90 % of flow).

**Base thickness x h_eff (die max dT, H-Z2 fluid, paste 0.05):** 1 mm: 68 / 57 / 51 / 47 / 43 K at h = 100 / 150 / 200 / 250 / 350 kW/m2K; 2 mm adds +8-9 K; 3 mm adds +17-18 K. Thinner is strictly better for reticle dies.

**Die-flux sweep (die max dT / Tj GPU):** at 200 W/cm2 (1.7 kW/die, 7.7 kW): C-x-U 56 K / 111 C, H-Z2 33.5 K / 88 C, H-Z2f-LM 23 K / 78 C. At 250: 67 / 124 vs 40 / 98 vs 28 / 85. At 400 (15.0 kW stretch, 18 LPM): C-x-U 99 K / 164 C, H-Z2 61 K / 126 C, H-Z2f-LM 41 K / 106 C.

**HBM interface (0.4 mm step, 40 W/cm2, R'' in cm2K/W; HBM case dT max / Tj):**

| config | base-top under HBM avg/max | paste 0.45 mm (1.16) | pad 5 W/mK (1.05) | Cu pedestal + 0.1 mm paste (0.28) | pedestal + indium (0.06) |
|---|---:|---:|---:|---:|---:|
| C-x-U | 25.5/32.6 | 78.8 / 140 C | 74.6 / 135 C | 43.8 / 105 C | 35.1 / 96 C |
| C-y-Z | 10.6/25.2 | 71.4 / 132 C | 67.2 / 128 C | 36.4 / 97 C | 27.7 / 88 C |
| H-U | 5.7/12.1 | 58.3 / 119 C | 54.1 / 115 C | 23.3 / 84 C | 14.6 / 75 C |
| H-Z2 | 10.7/18.7 | 64.9 / 126 C | 60.7 / 122 C | 29.9 / 91 C | 21.2 / 82 C |
| H-Z3 | 8.5/17.3 | 63.5 / 124 C | 59.3 / 120 C | 28.5 / 89 C | 19.8 / 81 C |

HBM flux sensitivity (pedestal + paste, Tj HBM): 20 / 40 / 60 / 80 W/cm2 -> C-x-U 90 / 105 / 119 / 134 C; H-Z2 75 / 91 / 107 / 123 C; with a 5 W/mK pad even H-Z2 gives 91 / 122 / 153 / 184 C.

**Die-to-HBM coupling** (HBM base-top with dies on minus dies off, same flow): C-x-U +20.1 K avg / +26 K max (almost all fluid preheat, 19.6 K); C-y-Z +3.1 avg / +15.3 max (base conduction at the HBM row adjacent to the die edge); H-Z2 +2.1 avg / +8.8 max.

## 5. Interpretation (honest)

1. **The uniform TTV hides the real problem.** TIM, base and convection scale with die flux (2.7x the TTV average). The CoolIT-like plate goes from 34 K (TTV) to 80-93 K at the hot die; an un-zoned HMMC from 24 K to 64-69 K. Nothing meets T_case <= 85 C at 350 W/cm2 with paste.
2. **An un-zoned HMMC loses much of its fresh-fluid advantage:** the die block gets only 30 % of the flow, so fluid under the die rises 36 K per segment (18 K mean), worse than split-flow (9-11 K). Heat-proportional zoning restores 6.4 K, cuts 15 K off the hot die and shrinks the across-die gradient from 22 K to 7-8 K, for +0.7 kPa. The task's "2x" zoning captures only half of this.
3. **The die TIM gates < 85 C.** Paste is 17.5-24.5 K at 350 W/cm2; the best paste HMMC (H-Z2f) reaches 48.7 K (T_case 94 C). Liquid metal/indium/sintered interfaces are required: H-Z2f-LM gives 36.5 K (T_case 81.5 C, Tj ~ 99 C). Paste stays viable to ~200-250 W/cm2 with zoned HMMC, ~150 W/cm2 for CoolIT-like.
4. **HMMC margin over CoolIT-like under real loading:** 34.5 K at the hot die with paste (54.1 vs 88.6 K), 52 K with liquid metal and fine fins, 3x the 10 K margin on the uniform TTV.
5. **HBM:** filling the 0.4 mm step with paste or a 5 W/mK pad adds 1.05-1.16 cm2K/W (42-46 K at 40 W/cm2) and fails above ~15-20 W/cm2 on every plate. A stepped Cu pedestal with a 0.1 mm paste BLT is mandatory; with it HMMC holds HBM Tj at 84-91 C (40 W/cm2) versus 105 C on the split-flow plate whose HBM sits downstream of the dies. Indium on the pedestal buys 9 K more; HBM above ~50 W/cm2 needs it or >= 0.5x HBM-zone flow.
6. **Die-to-HBM risk:** the GPU runs 25-30 K hotter than HBM in all HMMC cases. The 95 C HBM limit, not the GPU, sets the inlet ceiling in the split-flow x-orientation (20 K fluid preheat) and in any gap-filler design. In the zoned HMMC the HBM sees < 13 K fluid rise and < 9 K base coupling, so HBM is not the limiter once the pedestal is used.

Uncertainties: h_eff +-25 % (+-6-8 K on die dT at 350 W/cm2); TIM R'' +-30 % (+-5-7 K paste, +-2 K LM); R_jc,HBM +-50 % (+-8 K HBM Tj); R_jc,GPU +-40 % (+-7 K GPU Tj); on-die hot spots (2-3x local peaks) not modelled, add 5-15 K at the junction; intra-segment fluid variation averaged; manifold maldistribution assumed zero, so the zoning figures are manifold design targets, not guarantees.

## 6. Design rules

* **Zone the manifold to heat, not area:** die block >= 85-90 % of flow (2.5-3x average flow per area), HBM columns 0.3-0.5x, unheated area ~0 (no slots). Implement by slot pitch (V'' ~ 1/L^2: ~1.2 mm flow length over dies, ~3.5 mm over HBM) or slot width/orifices at a fixed 2 mm pitch; verify per-zone flow by test, since maldistribution re-creates the 15 K penalty.
* **Never route fluid over HBM after a die.** HMMC does this by construction; any serial-flow plate must run channels along the HBM columns and restrict them.
* **Base 1.0 mm (0.8 mm if stiffness allows) under dies;** spreading does not help a 26 x 33 mm source and each extra mm costs 9 K at 350 W/cm2.
* **Die interface R''_TIM <= 0.02 cm2K/W above 250 W/cm2** (liquid metal with Ni/Au barrier, indium pre-form or sintered Ag); paste only <= 200-250 W/cm2 with a zoned HMMC. Target h_eff >= 200 kW/m2K over dies (0.075 mm fins) so base + convection <= 25 K at 350 W/cm2.
* **Non-planar HBM: machine a stepped Cu pedestal** to within 0.05-0.1 mm of the HBM plane (offset tolerance +-0.05 mm, flatness 0.02 mm) with a 0.05-0.1 mm compliant TIM (paste <= 0.3 cm2K/W or indium 0.06). The extra 0.4 mm Cu costs 0.4 K. No gap-filler pads above ~15 W/cm2. Keep >= 0.5 mm clearance from the die edge and keep the pedestal inside the HBM flow zone.
* **Spec the across-die case gradient:** zoned HMMC gives 6-8 K over one die versus 22-30 K for split-flow or un-zoned HMMC; this drives die stress and throttle uniformity.
* **Design the HBM zone for Tj <= 85-90 C:** HBM case dT <= 25 K at 40 W/cm2 and 45 C inlet, i.e. fluid rise under HBM <= 10 K (>= 0.5x flow per area) with pedestal + paste, or 0.32x with pedestal + indium.
