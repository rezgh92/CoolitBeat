# hotspot-smoothing: hot-spot penalty of the HMMC cold plate vs split-flow

Script: `hotspot-smoothing.py` (same directory; full output in `run_final.txt`). Operating point: 15 kW, 18 LPM PG25, 45 C inlet, dT_out = 12.66 K, 128 W/cm2 on 117 cm2, paste 0.05 cm2K/W.

## Question

In a manifold micro-channel (HMMC) plate every fluid parcel enters from an inlet slot, runs ~2 mm along a 0.1 mm channel and exits through the next return slot, so the fin-side fluid temperature is a triangle wave of period 4 mm and amplitude +/-6.3 K. How much of that reaches the case? What happens with manifold maldistribution, with an interdigitated counter-flow variant, and for a split-flow plate whose fluid ramp spans 54 mm?

## Method

2-D steady conduction, finite-volume (x along the channel, z through thickness, per unit width in y), grid 20 um (converged to <0.02 K vs 10 um):

* Copper base t_b (0.5-2.0 mm), k = 390 W/mK.
* Fin layer (H = 1 mm, t = b = 0.1 mm, 50 % Cu) homogenised: k_xx = k_zz = 195 W/mK, k_yy = 0, with a distributed sink (2h/p)(T - T_f(x)) W/m3 from both fin faces; channel floor convects h(b/p) at the base/fin interface; fin tips adiabatic. This is more conservative than a lumped h_eff Robin boundary (also computed, analytic Fourier solution) because the fluid perturbation acts over the full fin height.
* Local laminar h from the thermally-developing parallel-plate H1 correlation (Shah & London: Nu_x = 1.49x*^-1/3 for x* < 2e-4; 8.235 + 8.68(1e3x*)^-0.506 exp(-164x*) for x* > 1e-3), scaled to the rectangular-duct Nu_fd of `coldplate_model.py`. HMMC: Re = 15, h = 18.4 kW/m2K fully developed, 19.4 mean, eta = 0.76, h_eff = 158 kW/m2K; split-flow: Re = 212, h_eff = 102 kW/m2K.
* Uniform 128 W/cm2 on top; TIM as a pure series resistance (no lateral conduction), so T_case(x) = T_cu,top(x) + q''R_TIM.
* Fluid: (i) "prescribed" linear rise over each cell (task statement) and (ii) "coupled": fluid energy balance m'cp dT_f/dx = q_f(x) solved self-consistently with the solid (fixed-point, 13 iterations).
* Maldistribution: slot flow factor (1+e) -> local rise 12.66/(1+e) K; two patterns: alternating slots (+e/-e, period 8 mm) and long-wavelength (a region at -e, another at +e, plate average = half/half mean).
* Counter-flow: fin-scale (two streams on the same x grid, each with half the fin faces/floors/capacity) and group-scale (groups w_g wide alternate direction; y-Fourier modes with the extra sink k_cu ky^2 in the base only).
* Split-flow: 54 mm domain, centre inlet, 0.2/0.2 x 4 mm fins, 2 mm base, local h, optional 5 mm unheated overhang.

Validation: uniform fluid at T_in + 6.33 K reproduces the 1-D budget exactly (24.15 K both).

## Results

### 1. Smoothing of the 4 mm sawtooth (plain HMMC, perfect distribution)

| base mm | fluid | avg case dT K | max-avg K | pk-pk case K | pk-pk fluid at fin K |
|---:|---|---:|---:|---:|---:|
| 0.8 | prescribed / coupled | 23.28 / 25.12 | 0.39 / 0.35 | 0.78 / 0.72 | 12.5 |
| 1.0 | prescribed / coupled | 23.94 / 25.78 | 0.28 / 0.25 | 0.57 / 0.52 | 12.5 |
| 1.5 | prescribed / coupled | 25.58 / 27.43 | 0.13 / 0.12 | 0.26 / 0.24 | 12.5 |
| 2.0 | prescribed / coupled | 27.23 / 29.08 | 0.06 / 0.05 | 0.12 / 0.11 | 12.5 |

The 12.5 K fin-side sawtooth arrives at the case as 0.5 K pk-pk with a 1 mm base (attenuation x25). The lumped-h_eff Fourier model (task formulation) gives even less (0.10 K max-avg; attenuation of the fundamental 1/(cosh kt + (k_cu k/h_eff) sinh kt), k = 2pi/4 mm; 0.016 for 1 mm base + 1 mm fins at 150 kW/m2K). Finer fins raise it slightly (fine 0.34-0.39 K, ultrafine 0.5-0.6 K with its 0.6 mm fin layer).

### 2. Side effect: the isothermal-wall caloric penalty (undermines the 1-D mean)

Because the surface is isothermal at the cell scale, the fluid picks up heat front-loaded and rises exponentially, not linearly. Plate NTU = h_eff A/(m cp). Mean fin-side wall rise: linear/uniform-flux (1-D model) = dT_out(1/2 + 1/NTU); isothermal = dT_out/(1 - e^-NTU).

| design | NTU | case dT 1-D (linear) K | case dT isothermal K | penalty K |
|---|---:|---:|---:|---:|
| HMMC 0.1/0.1x1.0, base 1 mm | 1.56 | 24.15 | 25.73 (FV coupled 25.78) | +1.6 |
| HMMC-fine 0.075, base 1 mm | 2.36 | 21.39 | 23.68 (FV 23.73) | +2.3 |
| HMMC-ultrafine 0.05x0.6, base 1 mm | 3.36 | 19.80 | 22.81 (FV 22.35) | +3.0 |
| CoolIT-like split-flow, base 2 mm | 1.00 | 31.91 | not isothermal; FV coupled 32.06 | +0.1 |

Effective caloric fraction for the HMMC is 0.625-0.74 of dT_out, not 0.5. The smoothing that removes the hot spot (max falls from 1-D "avg + 6.3" = 30.3 K to 26.0 K) costs 1.6 K on the mean. `coldplate_model.py` should use caloric = dT_out/(1-e^-NTU) - dT_out/NTU for manifold designs.

### 3. Maldistribution (plain HMMC, 1 mm base, coupled fluid)

| e | pattern | plate avg K | max-avg K | starved region avg K |
|---:|---|---:|---:|---:|
| 0 | perfect | 25.78 | 0.25 | - |
| +/-10 % | alternating slots | 25.84 | 0.27 | - |
| +/-10 % | long-wavelength | 25.89 | 1.25 | 26.87 |
| +/-20 % | alternating slots | 26.01 | 0.33 | - |
| +/-20 % | long-wavelength | 26.23 | 2.33 | 28.26 |

Analytic (isothermal cell, starved rise dT_out/((1-e)(1-e^-NTU/(1-e)))): 0.95 K and 1.97 K. Alternating patterns are smoothed; long-wavelength (header-driven) patterns are not and dominate the budget.

### 4. Interdigitated counter-flow

Fin-scale (adjacent channels opposed): max-avg 0.01 K perfect, 0.17/0.36 K alternating +/-10/20 %, 1.05/2.18 K long-wave +/-10/20 % (vs plain 0.25 / 0.27, 0.33 / 1.25, 2.33). But the shared fin is a recuperator (the hot exiting stream re-heats the cold entering stream): mean +0.37 K (26.13 vs 25.77 K at constant h). Group-scale (groups of 5 channels, w_g = 1 mm) removes the sawtooth to 0.025 K without the recuperator penalty; 2 mm groups 0.13 K; >= 8 mm no benefit. Net value of counter-flow in any form: <= 0.25 K.

### 5. CoolIT-like split-flow (54 mm paths, no smoothing; Fourier attenuation 0.75 at 108 mm period)

| case | avg K | max-avg K | avg-min K | centre / 27 mm / edge K |
|---|---:|---:|---:|---|
| linear fluid, mean h | 31.90 | 5.43 | 5.43 | 26.5 / 31.9 / 37.3 |
| coupled, local h (entrance) | 32.06 | 5.73 | 7.83 | 24.2 / 32.4 / 37.8 |
| + 5 mm unheated overhang at exit | 31.55 | 4.42 | 7.31 | 24.2 / 32.4 / 29.4 |
| +/-10 % channel-to-channel along header | 32.13 | 6.97 | 8.13 | - |
| +/-20 % channel-to-channel along header | 32.33 | 8.41 | 8.53 | - |

CoolIT data decomposition (8 TCs x 3 plates): grand mean 34.4 K; TC5 is +8.8 K on all three plates (systematic, flow-exit/starved region); TC7 -3.6 K; location x plate residual std 2.5 K, max residual 8.6 K (TC8 plate 1) = TIM/assembly scatter (10 um of 3 W/mK paste = 4.3 K at 128 W/cm2). Quoted 9.8 K = 8.8 K systematic + scatter. The model reproduces 5.7 K (perfect) to 8.4 K (+/-20 %), i.e. their spread is intrinsic to a 54 mm single-pass ramp plus entrance cooling of the centre.

### 6. Base-thickness trade-off (plain HMMC, coupled)

| base mm | avg K | max perfect K | max with +/-20 % long-wave K |
|---:|---:|---:|---:|
| 0.5 | 24.11 | 24.69 | 27.25 |
| 0.8 | 25.12 | 25.47 | 28.00 |
| 1.0 | 25.78 | 26.04 | 28.56 |
| 1.5 | 27.43 | 27.55 | 30.05 |
| 2.0 | 29.08 | 29.13 | 31.62 |

Thinner always wins on max temperature; 1 mm base already smooths the 4 mm sawtooth, so base thickness is set by stiffness/manufacturing, not by hot-spot smoothing.

## Conclusions: hot-spot penalty to claim (max - avg, flow-driven)

* (a) Plain HMMC, 1 mm base: 0.25 K perfect, 1.3 K at +/-10 %, 2.3 K at +/-20 % long-wave maldistribution. Claim 2.5 K (replace hotspot_K = 4.0 in the model with 2.5 K, conditional on +/-20 % slot-to-slot flow uniformity; 1.5 K if the manifold is verified to +/-10 %).
* (b) Counter-flow HMMC: 0.0 / 1.05 / 2.2 K for the same cases; mean +0.4 K (fin-scale recuperation). Claim 2.2 K; the 0.1-0.3 K gain does not justify the interleaved manifold. If used, use group-scale (5-channel, 1 mm groups), not fin-scale.
* CoolIT split-flow: 5.7 K intrinsic, 7-8.4 K with +/-10-20 % header maldistribution; measured 8.8 K systematic / 9.8 K max.
* Apples-to-apples with CoolIT's 9.8 K (which includes +2.5 K std TIM/assembly scatter, max-of-8 ~ +3.5 K): HMMC measured-equivalent hot spot ~5-6 K, split-flow ~9-10 K. TIM scatter, not flow, becomes the dominant hot-spot term for HMMC.
* Corrected HMMC baseline at 15 kW / 18 LPM / paste 0.05: avg 25.8 K (not 24.1), max 26.0 K perfect, 28.6 K with +/-20 % maldistribution; vs CoolIT 34.4 / 44.2 K. Margin on the mean 8.6 K, on the max 15.6 K.

## Design rules

1. Hot-spot attenuation of a fluid-temperature wave of period L through conductive thickness t with convective h_eff: ~1/(cosh(2pi t/L) + (k_cu 2pi/(L h_eff)) sinh(2pi t/L)). With t >= L/4 of copper the wave is gone (x25 at t = L/4). Slot pitch <= 4x (base + fin) thickness.
2. Short-cell manifold plates are isothermal; budget caloric = dT_out/(1-e^-NTU) - dT_out/NTU (0.63 dT_out at NTU 1.6, 0.74 at NTU 3.4). Pushing h_eff beyond ~250 kW/m2K buys little at 1.2 LPM/kW because the fluid saturates (NTU > 2.4); raise flow or accept it.
3. Long-wavelength slot-to-slot (and slot-end-to-end) flow uniformity is the real hot-spot lever: +/-10 % = 1.3 K, +/-20 % = 2.3 K. Alternating patterns are harmless (0.3 K). Design the two-level header for < +/-10 % and verify by CFD/flow test; prefer symmetric (centre-fed, H-tree) headers over U/Z.
4. Counter-flow interdigitation: not worth it (<= 0.25 K); fin-scale interdigitation costs 0.4 K on the mean via fin recuperation.
5. Base: 0.8-1.0 mm Cu; thinner is better for max temperature; do not thicken for smoothing.
6. TIM bond-line control (+/-10 um = +/-4 K) is the largest remaining hot-spot term for any pasted plate; it is the same for us and CoolIT unless we move to thin-BLT/liquid metal/direct-to-die.

## Uncertainty

Model is +/-20 % on the hot-spot numbers: homogenised fin layer (exact for thin fins; group-scale y-smoothing uses a linear sawtooth source, conservative), straight-entrance Nu for what is really an impinging/turning slot flow (local h near slots underestimated -> real sawtooth residual slightly smaller), no TIM lateral conduction (any die/lid/heater spreading reduces the residual further), no plate-edge spreading, no across-channel maldistribution inside a slot (treat with the same +/-e rule). The isothermal-wall caloric correction (+1.6 K) is robust (standard eps-NTU result, confirmed by the coupled FV within 0.05 K) and should be adopted. Maldistribution magnitudes (+/-10/20 %) are assumptions, not predictions; the architecture must specify and verify them.
