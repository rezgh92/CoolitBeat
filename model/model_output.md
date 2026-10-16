# Cold plate scoping model - CoolIT 15 kW benchmark operating point
Q = 15 kW, 1.2 LPM/kW -> 18 LPM PG25, 45 C inlet

Coolant outlet rise (energy balance): 12.7 K  (mdot = 0.301 kg/s, cp = 3930 J/kgK, Pr = 10.0); average caloric term for a long-channel plate: 6.3 K; for an isothermal short-cell plate: 0.60-0.68 x 12.7 K

## 1. Reverse-engineering the CoolIT 15 kW result (measured avg dT 34.4 K, max 44.2 K)
Footprint is undisclosed. Sweep it for a plausible skived split-flow plate:

| design | q'' W/cm2 | caloric | TIM | base | conv | **avg dT** | max dT | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow (60 cm2, paste)        |    250 |   6.3 |  17.5 |  12.8 |  24.8 | ** 61.4** |  74.6 | 0.246 |  25.0 |   7.5 |   5.6 |
| CoolIT-like skived split-flow (80 cm2, paste)        |    188 |   6.3 |  13.1 |   9.6 |  18.8 | ** 47.9** |  59.4 | 0.255 |  24.8 |   7.4 |   8.0 |
| CoolIT-like skived split-flow (100 cm2, paste)       |    150 |   6.3 |  10.5 |   7.7 |  15.2 | ** 39.7** |  50.2 | 0.265 |  24.7 |   7.4 |  10.4 |
| CoolIT-like skived split-flow (120 cm2, paste)       |    125 |   6.3 |   8.8 |   6.4 |  12.7 | ** 34.2** |  44.0 | 0.274 |  24.6 |   7.4 |  12.9 |
| CoolIT-like skived split-flow (150 cm2, paste)       |    100 |   6.3 |   7.0 |   5.1 |  10.3 | ** 28.7** |  37.8 | 0.287 |  24.5 |   7.3 |  16.5 |
| CoolIT-like skived split-flow (200 cm2, paste)       |     75 |   6.3 |   5.3 |   3.8 |   7.7 | ** 23.2** |  31.6 | 0.309 |  24.4 |   7.3 |  22.5 |

Calibrated footprint: 119 cm2 (109 x 109 mm, 126 W/cm2) reproduces 34.4 K -> adopted as the working assumption (CoolIT's 4 kW plate was 50 x 50 mm at ~0.225 cm2K/W, consistent with ~100-120 cm2 here).
Budget: caloric 6.3 | TIM 8.8 | base 6.4 | conv 12.8 K; channel u = 0.69 m/s, Re = 210; dP ~ 25 kPa port-to-port (estimate; undisclosed; 17-42 kPa for plausible fin pitches).

## 2. Lever-by-lever at the calibrated footprint (119 cm2), same flow, inlet and paste
| design | q'' W/cm2 | caloric | TIM | base | conv | **avg dT** | max dT | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow (119 cm2, paste)       |    126 |   6.3 |   8.8 |   6.5 |  12.9 | ** 34.5** |  44.2 | 0.273 |  24.6 |   7.4 |  12.7 |
| + base 2.0 -> 1.0 mm (tied sandwich)                 |    126 |   6.3 |   8.8 |   3.2 |  12.9 | ** 31.2** |  41.0 | 0.248 |  24.6 |   7.4 |  14.4 |
| + fins 0.2/0.2x4 -> 0.10/0.15x2 mm, still split-flow |    126 |   6.3 |   8.8 |   3.2 |  10.3 | ** 28.7** |  38.4 | 0.227 |  54.6 |  16.4 |  16.0 |
| + manifold feed, 4 mm flow length (HMMC-R core)      |    126 |   7.6 |   8.8 |   3.2 |  10.3 | ** 29.9** |  34.9 | 0.238 |   5.3 |   1.6 |  18.4 |
| + PCM pad TIM (Tier 1)                               |    126 |   7.6 |   6.9 |   3.2 |  10.3 | ** 28.1** |  31.0 | 0.223 |   5.3 |   1.6 |  21.6 |
| + liquid metal TIM on Ni (Tier 2)                    |    126 |   7.6 |   1.9 |   3.2 |  10.3 | ** 23.0** |  25.1 | 0.183 |   5.3 |   1.6 |  29.5 |

## 3. Product tiers at 119 cm2 (15 kW, 18 LPM, 45 C)
| design | q'' W/cm2 | caloric | TIM | base | conv | **avg dT** | max dT | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow (119 cm2, paste)       |    126 |   6.3 |   8.8 |   6.5 |  12.9 | ** 34.5** |  44.2 | 0.273 |  24.6 |   7.4 |  12.7 |
| HMMC-R like-for-like (119 cm2, paste 0.07)           |    126 |   7.6 |   8.8 |   3.2 |  10.3 | ** 29.9** |  34.9 | 0.238 |   5.3 |   1.6 |  18.4 |
| HMMC-R Tier 1 drop-in (119 cm2, PCM pad)             |    126 |   7.6 |   6.9 |   3.2 |  10.3 | ** 28.1** |  31.0 | 0.223 |   5.3 |   1.6 |  21.6 |
| HMMC-R Tier 2 OEM (119 cm2, liquid metal)            |    126 |   7.6 |   1.9 |   3.2 |  10.3 | ** 23.0** |  25.1 | 0.183 |   5.3 |   1.6 |  29.5 |
| HMMC-P (<=33um loops) (119 cm2, PCM pad)             |    126 |   8.1 |   6.9 |   3.2 |   7.0 | ** 25.3** |  28.3 | 0.201 |   5.4 |   1.6 |  25.3 |
| HMMC-P (<=33um loops) (119 cm2, liquid metal)        |    126 |   8.1 |   1.9 |   3.2 |   7.0 | ** 20.3** |  22.3 | 0.161 |   5.4 |   1.6 |  36.9 |
| HMMC-R Tier 3 D2D (119 cm2, direct-to-die)           |    126 |   7.6 |   0.0 |   2.6 |  10.3 | ** 20.5** |  22.6 | 0.162 |   5.3 |   1.6 |  35.3 |
| HMMC-F (NOT deployable, ref.) (119 cm2, liquid metal) |    126 |   8.6 |   1.9 |   3.2 |   5.5 | ** 19.2** |  21.3 | 0.152 |   6.3 |   1.9 |  41.4 |
| HMMC-R aluminium (119 cm2, PCM pad)                  |    126 |   7.3 |   6.9 |   6.3 |  13.3 | ** 33.9** |  36.8 | 0.269 |   5.3 |   1.6 |  16.8 |

Tier 1 detail: NTU 1.23, caloric fraction 0.60, h 12.5 kW/m2K, eta 0.58, h_eff 122 kW/m2K, channel u 0.082 m/s (Re 18), port u 1.49 m/s; dP split: channel 0.23 + turns 0.01 + slot 0.00 + header 0.50 + orifice 2.00 + ports 2.57 = 5.3 kPa (quick disconnects excluded).

## 4. Fin/channel geometry sweep (HMMC manifold, 119 cm2, PCM pad, 4 mm flow length)
Deployability: gap >= 0.15 mm behind a 50 um absolute screen (10-year SKU); 0.10 mm only
behind <= 33 um absolute filtration; < 0.10 mm not deployable (fouling).

| gap (mm) | fin (mm) | H (mm) | h kW/m2K | eta | h_eff kW/m2K | NTU | cal K | conv K | avg dT K | max dT K | dP kPa |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.075 | 0.075 | 1.0 | 24.4 | 0.67 | 229 | 2.30 | 8.6 | 5.5 | 24.2 | 27.2 | 7.3 |
| 0.075 | 0.075 | 1.5 | 24.8 | 0.49 | 256 | 2.57 | 8.8 | 4.9 | 23.9 | 26.8 | 6.5 |
| 0.075 | 0.075 | 2.0 | 25.0 | 0.38 | 264 | 2.66 | 8.8 | 4.8 | 23.8 | 26.8 | 6.2 |
| 0.075 | 0.075 | 3.0 | 25.1 | 0.25 | 268 | 2.69 | 8.9 | 4.7 | 23.7 | 26.7 | 5.8 |
| 0.100 | 0.100 | 1.0 | 18.3 | 0.77 | 151 | 1.51 | 7.9 | 8.4 | 26.4 | 29.4 | 6.4 |
| 0.100 | 0.100 | 1.5 | 18.6 | 0.61 | 180 | 1.81 | 8.1 | 7.0 | 25.3 | 28.3 | 5.9 |
| 0.100 | 0.100 | 2.0 | 18.7 | 0.49 | 193 | 1.94 | 8.3 | 6.5 | 25.0 | 27.9 | 5.7 |
| 0.100 | 0.100 | 3.0 | 18.9 | 0.34 | 200 | 2.01 | 8.3 | 6.3 | 24.8 | 27.8 | 5.5 |
| 0.150 | 0.100 | 1.0 | 12.2 | 0.83 | 89 | 0.89 | 7.3 | 14.2 | 31.6 | 34.6 | 5.6 |
| 0.150 | 0.100 | 1.5 | 12.4 | 0.70 | 111 | 1.11 | 7.5 | 11.4 | 29.0 | 32.0 | 5.4 |
| 0.150 | 0.100 | 2.0 | 12.5 | 0.58 | 122 | 1.23 | 7.6 | 10.3 | 28.1 | 31.0 | 5.3 |
| 0.150 | 0.100 | 3.0 | 12.6 | 0.41 | 131 | 1.31 | 7.7 | 9.6 | 27.5 | 30.5 | 5.2 |
| 0.150 | 0.150 | 1.0 | 12.4 | 0.88 | 79 | 0.79 | 7.2 | 15.9 | 33.3 | 36.2 | 5.7 |
| 0.150 | 0.150 | 1.5 | 12.5 | 0.77 | 102 | 1.03 | 7.4 | 12.3 | 29.9 | 32.8 | 5.5 |
| 0.150 | 0.150 | 2.0 | 12.6 | 0.66 | 117 | 1.17 | 7.5 | 10.8 | 28.5 | 31.5 | 5.4 |
| 0.150 | 0.150 | 3.0 | 12.6 | 0.49 | 130 | 1.30 | 7.7 | 9.7 | 27.6 | 30.5 | 5.3 |
| 0.200 | 0.150 | 1.0 | 9.5 | 0.90 | 54 | 0.55 | 6.9 | 23.2 | 40.2 | 43.2 | 5.4 |
| 0.200 | 0.150 | 1.5 | 9.5 | 0.81 | 71 | 0.72 | 7.1 | 17.6 | 34.9 | 37.9 | 5.3 |
| 0.200 | 0.150 | 2.0 | 9.5 | 0.71 | 83 | 0.83 | 7.2 | 15.2 | 32.5 | 35.5 | 5.2 |
| 0.200 | 0.150 | 3.0 | 9.5 | 0.55 | 95 | 0.95 | 7.3 | 13.3 | 30.8 | 33.7 | 5.2 |

## 5. Flow sensitivity (119 cm2): CoolIT-like (paste) vs HMMC-R Tier 1 (PCM) vs Tier 2 (LM)
| LPM/kW | flow LPM | CoolIT avg | max | dP kPa | pump W | T1 avg | max | dP kPa | pump W | T2 avg | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.6 | 9 | 41.0 | 57.1 | 9.8 | 1.5 | 38.0 | 40.9 | 1.4 | 0.2 | 32.9 | 35.0 |
| 0.8 | 12 | 37.8 | 50.7 | 14.2 | 2.8 | 32.8 | 35.8 | 2.4 | 0.5 | 27.8 | 29.9 |
| 1.0 | 15 | 35.8 | 46.8 | 19.1 | 4.8 | 29.9 | 32.9 | 3.7 | 0.9 | 24.9 | 27.0 |
| 1.2 | 18 | 34.5 | 44.2 | 24.6 | 7.4 | 28.1 | 31.0 | 5.3 | 1.6 | 23.0 | 25.1 |
| 1.5 | 22 | 33.1 | 41.6 | 33.9 | 12.7 | 26.3 | 29.2 | 8.2 | 3.1 | 21.2 | 23.3 |
| 2.0 | 30 | 31.7 | 38.9 | 52.1 | 26.1 | 24.5 | 27.5 | 14.5 | 7.3 | 19.5 | 21.6 |
| 2.5 | 38 | 30.8 | 37.3 | 73.9 | 46.2 | 23.5 | 26.5 | 22.6 | 14.1 | 18.4 | 20.5 |

Equal-pumping-power reading: the HMMC at 2.0 LPM/kW spends about what the skived plate spends at 1.2 LPM/kW.

## 6. Scaling to other loads / footprints (1.2 LPM/kW)
| design | q'' W/cm2 | caloric | TIM | base | conv | **avg dT** | max dT | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow (45 cm2, paste)        |     31 |   6.3 |   2.2 |   1.6 |   3.3 | ** 13.4** |  20.5 | 0.429 |   1.5 |   0.0 |   5.3 |
| HMMC-R (45 cm2, PCM pad)                             |     31 |  10.2 |   1.7 |   0.8 |   2.6 | ** 15.3** |  17.1 | 0.491 |   0.1 |   0.0 |   7.7 |
| HMMC-R (45 cm2, liquid metal)                        |     31 |  10.2 |   0.5 |   0.8 |   2.6 | ** 14.0** |  15.7 | 0.451 |   0.1 |   0.0 |  10.2 |
| CoolIT-like skived split-flow (60 cm2, paste)        |     38 |   6.3 |   2.7 |   2.0 |   4.0 | ** 15.0** |  22.4 | 0.391 |   2.5 |   0.1 |   7.0 |
| HMMC-R (60 cm2, PCM pad)                             |     38 |   9.7 |   2.1 |   1.0 |   3.2 | ** 16.0** |  17.9 | 0.417 |   0.2 |   0.0 |  10.4 |
| HMMC-R (60 cm2, liquid metal)                        |     38 |   9.7 |   0.6 |   1.0 |   3.2 | ** 14.5** |  16.1 | 0.377 |   0.2 |   0.0 |  13.8 |
| CoolIT-like skived split-flow (80 cm2, paste)        |     45 |   6.3 |   3.2 |   2.3 |   4.7 | ** 16.5** |  24.0 | 0.366 |   4.1 |   0.3 |   9.3 |
| HMMC-R (80 cm2, PCM pad)                             |     45 |   9.4 |   2.5 |   1.2 |   3.8 | ** 16.7** |  18.8 | 0.372 |   0.4 |   0.0 |  14.0 |
| HMMC-R (80 cm2, liquid metal)                        |     45 |   9.4 |   0.7 |   1.2 |   3.8 | ** 14.9** |  16.6 | 0.332 |   0.4 |   0.0 |  18.7 |
| CoolIT-like skived split-flow (119 cm2, paste)       |    126 |   6.3 |   8.8 |   6.5 |  12.9 | ** 34.5** |  44.2 | 0.273 |  24.6 |   7.4 |  12.7 |
| HMMC-R (119 cm2, PCM pad)                            |    126 |   7.6 |   6.9 |   3.2 |  10.3 | ** 28.1** |  31.0 | 0.223 |   5.3 |   1.6 |  21.6 |
| HMMC-R (119 cm2, liquid metal)                       |    126 |   7.6 |   1.9 |   3.2 |  10.3 | ** 23.0** |  25.1 | 0.183 |   5.3 |   1.6 |  29.5 |
| CoolIT-like skived split-flow (119 cm2, paste)       |    210 |   6.3 |  14.7 |  10.8 |  21.0 | ** 52.8** |  64.9 | 0.251 |  52.1 |  26.1 |  11.6 |
| HMMC-R (119 cm2, PCM pad)                            |    210 |   7.1 |  11.6 |   5.4 |  16.8 | ** 40.9** |  44.8 | 0.195 |  14.5 |   7.3 |  21.4 |
| HMMC-R (119 cm2, liquid metal)                       |    210 |   7.1 |   3.2 |   5.4 |  16.8 | ** 32.5** |  35.0 | 0.155 |  14.5 |   7.3 |  30.0 |
| CoolIT-like skived split-flow (150 cm2, paste)       |    200 |   6.3 |  14.0 |  10.3 |  20.0 | ** 50.6** |  62.4 | 0.253 |  68.9 |  41.3 |  14.8 |
| HMMC-R (150 cm2, PCM pad)                            |    200 |   7.2 |  11.0 |   5.1 |  16.0 | ** 39.3** |  43.1 | 0.196 |  20.7 |  12.4 |  27.1 |
| HMMC-R (150 cm2, liquid metal)                       |    200 |   7.2 |   3.0 |   5.1 |  16.0 | ** 31.3** |  33.7 | 0.156 |  20.7 |  12.4 |  37.8 |
| CoolIT-like skived split-flow (250 cm2, paste)       |    200 |   6.3 |  14.0 |  10.3 |  20.0 | ** 50.6** |  62.4 | 0.253 | 157.4 | 157.4 |  24.7 |
| HMMC-R (250 cm2, PCM pad)                            |    200 |   7.2 |  11.0 |   5.1 |  16.0 | ** 39.3** |  43.2 | 0.197 |  56.8 |  56.8 |  45.1 |
| HMMC-R (250 cm2, liquid metal)                       |    200 |   7.2 |   3.0 |   5.1 |  16.0 | ** 31.3** |  33.8 | 0.157 |  56.8 |  56.8 |  62.9 |

## 7. Water vs PG25 (HMMC-R Tier 1, 119 cm2, 15 kW, 1.2 LPM/kW)
- PG25 @ ~50C: avg dT 28.1 K, max 31.0 K, dP 5.3 kPa
- water @ 50C: avg dT 26.3 K, max 29.3 K, dP 5.1 kPa

Caveats: 1-D series network, laminar correlations, uniform heating; non-uniform GPU+HBM packages,
manifold maldistribution (assumed +/-10 % -> 1.5 K) and TIM bond-line variation are handled as
lumped hot-spot terms. Treat +/-25 % per term; see the physics-check reports for the 2-D/network checks.
