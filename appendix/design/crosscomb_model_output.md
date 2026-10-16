## A. 15 kW / 18 LPM PG25 / 45 C / 117 cm2 (128 W/cm2)
| design | LPM | cal | TIM | base | conv | **avg dT K** | max dT K | Tcase,max C | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow (117 cm2, paste) |  18.0 |  6.3 |  9.0 |  6.6 | 12.6 | **34.5** | 44.3 |  89.3 | 0.269 |  24.6 |  7.4 | 12.7 |
| CrossComb paste [conservative +/-20%]-R (117 cm2, paste 0.07) |  18.0 |  7.6 |  9.0 |  3.3 | 10.1 | **30.0** | 36.5 |  81.5 | 0.234 |   6.3 |  1.9 | 17.4 |
| CrossComb paste [nominal +/-10%]-R (117 cm2, paste 0.07) |  18.0 |  7.6 |  9.0 |  3.3 | 10.1 | **30.0** | 35.5 |  80.5 | 0.234 |   6.3 |  1.9 | 18.0 |
| CrossComb paste [stretch, verified +/-5%]-R (117 cm2, paste 0.07) |  18.0 |  7.6 |  9.0 |  3.3 | 10.1 | **30.0** | 34.8 |  79.8 | 0.234 |   6.3 |  1.9 | 18.5 |
| CrossComb PCM T1 [conservative]-R (117 cm2, PCM pad) |  18.0 |  7.6 |  7.1 |  3.3 | 10.1 | **28.0** | 32.6 |  77.6 | 0.219 |   6.3 |  1.9 | 20.5 |
| CrossComb PCM T1 [nominal]-R (117 cm2, PCM pad) |  18.0 |  7.6 |  7.1 |  3.3 | 10.1 | **28.0** | 31.6 |  76.6 | 0.219 |   6.3 |  1.9 | 21.2 |
| CrossComb PCM T1 [stretch]-R (117 cm2, PCM pad) |  18.0 |  7.6 |  7.1 |  3.3 | 10.1 | **28.0** | 30.9 |  75.9 | 0.219 |   6.3 |  1.9 | 21.7 |
| CrossComb LM T2 [conservative]-R (117 cm2, liquid metal) |  18.0 |  7.6 |  1.9 |  3.3 | 10.1 | **22.9** | 26.5 |  71.5 | 0.179 |   6.3 |  1.9 | 28.2 |
| CrossComb LM T2 [nominal]-R (117 cm2, liquid metal) |  18.0 |  7.6 |  1.9 |  3.3 | 10.1 | **22.9** | 25.5 |  70.5 | 0.179 |   6.3 |  1.9 | 29.2 |
| CrossComb LM T2 [stretch]-R (117 cm2, liquid metal) |  18.0 |  7.6 |  1.9 |  3.3 | 10.1 | **22.9** | 24.8 |  69.8 | 0.179 |   6.3 |  1.9 | 29.9 |
| CrossComb-P PCM (<=25um loops)-P (117 cm2, PCM pad) |  18.0 |  8.2 |  7.1 |  3.3 |  6.8 | **25.4** | 28.9 |  73.9 | 0.198 |   6.4 |  1.9 | 24.7 |
| CrossComb-P LM (<=25um loops)-P (117 cm2, liquid metal) |  18.0 |  8.2 |  1.9 |  3.3 |  6.8 | **20.2** | 22.8 |  67.8 | 0.158 |   6.4 |  1.9 | 36.4 |
| CrossComb PCM, 13 mm (1/2 in) ports-R (117 cm2, PCM pad) |  18.0 |  7.6 |  7.1 |  3.3 | 10.1 | **28.0** | 31.6 |  76.6 | 0.219 |   9.6 |  2.9 | 21.2 |
| CrossComb PCM, 0.8 mm base-R (117 cm2, PCM pad) |  18.0 |  7.6 |  7.1 |  2.6 | 10.1 | **27.4** | 30.9 |  75.9 | 0.214 |   6.3 |  1.9 | 21.9 |
| CrossComb PCM, 1.2 mm base-R (117 cm2, PCM pad) |  18.0 |  7.6 |  7.1 |  3.9 | 10.1 | **28.7** | 32.2 |  77.2 | 0.224 |   6.3 |  1.9 | 20.5 |
| CrossComb PCM water-R (117 cm2, PCM pad)       |  18.0 |  7.4 |  7.1 |  3.3 |  8.8 | **26.6** | 30.1 |  75.1 | 0.207 |   6.1 |  1.8 | 22.8 |

Nominal detail: NTU 1.25, cal_frac 0.60, h 13.2 kW/m2K, eta 0.56, h_eff 127 kW/m2K, u_ch 0.083 m/s Re 19, u_slot 0.07 m/s, u_port 1.49 m/s; dP: channel 0.23 + turns 0.01 + slot 0.00 + header 0.56 + slit+screen 2.90 + ports 2.57 = 6.3 kPa

## B. Flow sweep (117 cm2, 15 kW): CoolIT-like paste vs CrossComb PCM (nominal) vs CrossComb LM
| LPM/kW | LPM | CoolIT avg | max | dP | pump W | CC-PCM avg | max | dP | pump W | CC-LM avg | max |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 7.5 | 43.6 | 53.4 | 7.8 | 1.0 | 42.4 | 45.9 | 1.1 | 0.1 | 37.3 | 39.9 |
| 0.60 | 9.0 | 41.0 | 50.8 | 9.8 | 1.5 | 38.0 | 41.5 | 1.6 | 0.2 | 32.9 | 35.5 |
| 0.75 | 11.2 | 38.5 | 48.3 | 13.0 | 2.4 | 33.8 | 37.3 | 2.5 | 0.5 | 28.7 | 31.3 |
| 0.90 | 13.5 | 36.7 | 46.5 | 16.6 | 3.7 | 31.2 | 34.7 | 3.6 | 0.8 | 26.1 | 28.7 |
| 1.00 | 15.0 | 35.8 | 45.6 | 19.1 | 4.8 | 29.9 | 33.4 | 4.4 | 1.1 | 24.8 | 27.4 |
| 1.20 | 18.0 | 34.5 | 44.3 | 24.6 | 7.4 | 28.0 | 31.6 | 6.3 | 1.9 | 22.9 | 25.5 |
| 1.50 | 22.5 | 33.2 | 43.0 | 33.9 | 12.7 | 26.3 | 29.8 | 9.7 | 3.6 | 21.1 | 23.7 |
| 2.00 | 30.0 | 31.7 | 41.5 | 52.2 | 26.1 | 24.5 | 28.0 | 17.2 | 8.6 | 19.4 | 22.0 |
| 2.40 | 36.0 | 31.0 | 40.8 | 69.3 | 41.6 | 23.6 | 27.2 | 24.6 | 14.8 | 18.5 | 21.1 |
| 3.00 | 45.0 | 30.2 | 40.0 | 99.2 | 74.4 | 22.8 | 26.3 | 38.4 | 28.8 | 17.6 | 20.2 |
Flow-equivalence (PCM pad): 0.72 LPM/kW = 10.9 LPM gives 34.4 K avg (max 37.9), dP 2.3 kPa, pump 0.42 W
Flow-equivalence (paste 0.07): 0.82 LPM/kW = 12.3 LPM gives 34.4 K avg (max 39.9), dP 3.0 kPa, pump 0.61 W
Equal pump power (7.4 W): CrossComb PCM at 28.5 LPM (1.90 LPM/kW): avg 24.8 / max 28.3 K, dP 15.5 kPa

## C. Other loads/footprints at 1.2 LPM/kW (uniform TTV): CoolIT-like paste vs CrossComb PCM vs CrossComb LM
| design | LPM | cal | TIM | base | conv | **avg dT K** | max dT K | Tcase,max C | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow (36 cm2, paste)  |   1.2 |  6.3 |  1.9 |  1.4 |  2.8 | **12.5** | 19.6 |  64.6 | 0.450 |   1.0 |  0.0 |  4.3 |
| CrossComb-R (36 cm2, PCM pad)                  |   1.2 | 10.5 |  1.5 |  0.7 |  2.2 | **14.9** | 17.3 |  62.3 | 0.538 |   0.1 |  0.0 |  6.1 |
| CrossComb-R (36 cm2, liquid metal)             |   1.2 | 10.5 |  0.4 |  0.7 |  2.2 | **13.8** | 16.0 |  61.0 | 0.498 |   0.1 |  0.0 |  8.1 |
| CoolIT-like skived split-flow (45 cm2, paste)  |   1.7 |  6.3 |  2.2 |  1.6 |  3.1 | **13.2** | 20.4 |  65.4 | 0.426 |   1.5 |  0.0 |  5.4 |
| CrossComb-R (45 cm2, PCM pad)                  |   1.7 | 10.2 |  1.7 |  0.8 |  2.5 | **15.2** | 17.6 |  62.6 | 0.490 |   0.1 |  0.0 |  7.6 |
| CrossComb-R (45 cm2, liquid metal)             |   1.7 | 10.2 |  0.5 |  0.8 |  2.5 | **14.0** | 16.2 |  61.2 | 0.450 |   0.1 |  0.0 | 10.3 |
| CoolIT-like skived split-flow (60 cm2, paste)  |   2.8 |  6.3 |  2.7 |  2.0 |  3.9 | **14.8** | 22.2 |  67.2 | 0.387 |   2.5 |  0.1 |  7.1 |
| CrossComb-R (60 cm2, PCM pad)                  |   2.8 |  9.8 |  2.1 |  1.0 |  3.1 | **16.0** | 18.4 |  63.4 | 0.416 |   0.2 |  0.0 | 10.3 |
| CrossComb-R (60 cm2, liquid metal)             |   2.8 |  9.8 |  0.6 |  1.0 |  3.1 | **14.4** | 16.6 |  61.6 | 0.376 |   0.2 |  0.0 | 13.9 |
| CoolIT-like skived split-flow (80 cm2, paste)  |   4.3 |  6.3 |  3.2 |  2.3 |  4.5 | **16.3** | 23.8 |  68.8 | 0.363 |   4.1 |  0.3 |  9.4 |
| CrossComb-R (80 cm2, PCM pad)                  |   4.3 |  9.4 |  2.5 |  1.2 |  3.6 | **16.7** | 19.2 |  64.2 | 0.371 |   0.4 |  0.0 | 13.9 |
| CrossComb-R (80 cm2, liquid metal)             |   4.3 |  9.4 |  0.7 |  1.2 |  3.6 | **14.9** | 17.1 |  62.1 | 0.331 |   0.4 |  0.0 | 18.8 |
| CoolIT-like skived split-flow (117 cm2, paste) |   4.3 |  6.3 |  2.2 |  1.6 |  3.1 | **13.2** | 20.3 |  65.3 | 0.428 |   4.1 |  0.3 | 14.0 |
| CrossComb-R (117 cm2, PCM pad)                 |   4.3 | 10.3 |  1.7 |  0.8 |  2.5 | **15.2** | 17.6 |  62.6 | 0.495 |   0.4 |  0.0 | 19.9 |
| CrossComb-R (117 cm2, liquid metal)            |   4.3 | 10.3 |  0.5 |  0.8 |  2.5 | **14.0** | 16.1 |  61.1 | 0.455 |   0.4 |  0.0 | 26.6 |
| CoolIT-like skived split-flow (117 cm2, paste) |  18.0 |  6.3 |  9.0 |  6.6 | 12.6 | **34.5** | 44.3 |  89.3 | 0.269 |  24.6 |  7.4 | 12.7 |
| CrossComb-R (117 cm2, PCM pad)                 |  18.0 |  7.6 |  7.1 |  3.3 | 10.1 | **28.0** | 31.6 |  76.6 | 0.219 |   6.3 |  1.9 | 21.2 |
| CrossComb-R (117 cm2, liquid metal)            |  18.0 |  7.6 |  1.9 |  3.3 | 10.1 | **22.9** | 25.5 |  70.5 | 0.179 |   6.3 |  1.9 | 29.2 |
| CoolIT-like skived split-flow (117 cm2, paste) |  24.0 |  6.3 | 12.0 |  8.8 | 16.7 | **43.7** | 54.7 |  99.7 | 0.256 |  37.3 | 14.9 | 12.1 |
| CrossComb-R (117 cm2, PCM pad)                 |  24.0 |  7.3 |  9.4 |  4.4 | 13.3 | **34.4** | 38.4 |  83.4 | 0.201 |  11.1 |  4.4 | 21.2 |
| CrossComb-R (117 cm2, liquid metal)            |  24.0 |  7.3 |  2.6 |  4.4 | 13.3 | **27.6** | 30.4 |  75.4 | 0.161 |  11.1 |  4.4 | 29.5 |
| CoolIT-like skived split-flow (117 cm2, paste) |  30.0 |  6.3 | 15.0 | 11.0 | 20.7 | **52.9** | 65.0 | 110.0 | 0.248 |  52.2 | 26.1 | 11.6 |
| CrossComb-R (117 cm2, PCM pad)                 |  30.0 |  7.1 | 11.8 |  5.5 | 16.5 | **40.9** | 45.4 |  90.4 | 0.191 |  17.2 |  8.6 | 21.0 |
| CrossComb-R (117 cm2, liquid metal)            |  30.0 |  7.1 |  3.2 |  5.5 | 16.5 | **32.3** | 35.3 |  80.3 | 0.151 |  17.2 |  8.6 | 29.7 |
| CoolIT-like skived split-flow (150 cm2, paste) |  36.0 |  6.3 | 14.0 | 10.3 | 19.4 | **50.0** | 61.7 | 106.7 | 0.250 |  68.9 | 41.3 | 15.1 |
| CrossComb-R (150 cm2, PCM pad)                 |  36.0 |  7.2 | 11.0 |  5.1 | 15.4 | **38.8** | 43.1 |  88.1 | 0.194 |  24.5 | 14.7 | 27.1 |
| CrossComb-R (150 cm2, liquid metal)            |  36.0 |  7.2 |  3.0 |  5.1 | 15.4 | **30.8** | 33.7 |  78.7 | 0.154 |  24.5 | 14.7 | 38.0 |
| CoolIT-like skived split-flow (250 cm2, paste) |  60.0 |  6.3 | 14.0 | 10.3 | 19.4 | **50.0** | 61.7 | 106.7 | 0.250 | 157.4 | 157.4 | 25.1 |
| CrossComb-R (250 cm2, PCM pad)                 |  60.0 |  7.2 | 11.0 |  5.1 | 15.5 | **38.8** | 43.1 |  88.1 | 0.194 |  67.4 | 67.4 | 45.1 |
| CrossComb-R (250 cm2, liquid metal)            |  60.0 |  7.2 |  3.0 |  5.1 | 15.5 | **30.8** | 33.7 |  78.7 | 0.154 |  67.4 | 67.4 | 63.3 |

GPU-class at 2.0 LPM/kW (CrossComb has the dP headroom):
| design | LPM | cal | TIM | base | conv | **avg dT K** | max dT K | Tcase,max C | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CoolIT-like skived split-flow (45 cm2, paste)  |   1.7 |  6.3 |  2.2 |  1.6 |  3.1 | **13.2** | 20.4 |  65.4 | 0.426 |   1.5 |  0.0 |  5.4 |
| CrossComb-R (45 cm2, PCM pad)                  |   2.8 |  5.5 |  1.7 |  0.8 |  2.5 | **10.5** | 12.8 |  57.8 | 0.337 |   0.2 |  0.0 |  9.0 |
| CoolIT-like skived split-flow (60 cm2, paste)  |   2.8 |  6.3 |  2.7 |  2.0 |  3.9 | **14.8** | 22.2 |  67.2 | 0.387 |   2.5 |  0.1 |  7.1 |
| CrossComb-R (60 cm2, PCM pad)                  |   4.6 |  5.2 |  2.1 |  1.0 |  3.1 | **11.4** | 13.8 |  58.8 | 0.297 |   0.5 |  0.0 | 12.1 |
| CoolIT-like skived split-flow (80 cm2, paste)  |   4.3 |  6.3 |  3.2 |  2.3 |  4.5 | **16.3** | 23.8 |  68.8 | 0.363 |   4.1 |  0.3 |  9.4 |
| CrossComb-R (80 cm2, PCM pad)                  |   7.2 |  5.0 |  2.5 |  1.2 |  3.6 | **12.3** | 14.8 |  59.8 | 0.272 |   1.1 |  0.1 | 16.2 |

## D. Die-zone estimate, Rubin-class 2-die package (16.6 cm2 logic at 117 W/cm2 = 1.95 kW; 2.3 kW total at 1.0 LPM/kW = 2.3 LPM)
Zoned CrossComb: die zone gets 85 % of flow (1.96 LPM). CoolIT-like split-flow: die zone sees the fresh centre fluid but at 
area-proportional flow (16.6/60 of 2.3 LPM = 0.64 LPM) and a long ramp; both evaluated on the 16.6 cm2 die footprint.
| design | LPM | cal | TIM | base | conv | **avg dT K** | max dT K | Tcase,max C | R'' cm2K/W | dP kPa | pump W | Q cap kW |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| CrossComb zoned die zone, PCM                  |   2.0 |  9.5 |  6.5 |  3.0 |  9.3 | **28.3** | 31.7 |  76.7 | 0.241 |   0.3 |  0.0 |  2.8 |
| CrossComb zoned die zone, LM                   |   2.0 |  9.5 |  1.8 |  3.0 |  9.3 | **23.6** | 26.1 |  71.1 | 0.201 |   0.3 |  0.0 |  3.9 |
| CoolIT-like die zone (area-share flow), paste  |   0.6 | 23.1 |  8.2 |  6.0 | 11.9 | **49.2** | 58.8 | 103.8 | 0.419 |   0.5 |  0.0 |  0.5 |
| CoolIT-like die zone (all 2.3 LPM over dies), paste |   2.3 |  6.4 |  8.2 |  6.0 | 11.6 | **32.3** | 41.8 |  86.8 | 0.275 |   2.1 |  0.1 |  1.8 |

## E. 2027-28 stress package: hottest die cell, fit dT = 33 + 3500/h_eff + 350 (R_TIM - 0.05) [nonuniform-heatmap]
  R robust 0.15 mm         paste 0.05: hot-die case dT  60.6 K -> T_case 105.6 C
  R robust 0.15 mm         PCM 0.055 : hot-die case dT  62.3 K -> T_case 107.3 C
  R robust 0.15 mm         LM 0.015  : hot-die case dT  48.3 K -> T_case  93.3 C
  P performance 0.10 mm    paste 0.05: hot-die case dT  51.7 K -> T_case  96.7 C
  P performance 0.10 mm    PCM 0.055 : hot-die case dT  53.5 K -> T_case  98.5 C
  P performance 0.10 mm    LM 0.015  : hot-die case dT  39.5 K -> T_case  84.5 C
  CoolIT-like split-flow (report): 88.6 K paste -> 134 C; ~76 K LM -> ~121 C
  Rubin-class die-average 120 W/cm2, R robust PCM: hot-die dT ~25.8 K -> 70.8 C
  Rubin-class die-average 200 W/cm2, R robust PCM: hot-die dT ~38.6 K -> 83.6 C
  Rubin-class die-average 120 W/cm2, R robust LM: hot-die dT ~21.0 K -> 66.0 C
  Rubin-class die-average 200 W/cm2, R robust LM: hot-die dT ~30.6 K -> 75.6 C
  Rubin-class die-average 120 W/cm2, P perf PCM: hot-die dT ~22.8 K -> 67.8 C
  Rubin-class die-average 200 W/cm2, P perf PCM: hot-die dT ~33.5 K -> 78.5 C
  Rubin-class die-average 120 W/cm2, P perf LM: hot-die dT ~18.0 K -> 63.0 C
  Rubin-class die-average 200 W/cm2, P perf LM: hot-die dT ~25.5 K -> 70.5 C

## F. 2x flow (36 LPM) dP and velocities
CrossComb at 36 LPM: dP 24.6 kPa (ch 0.46, header 2.23, slit+screen 11.60, ports 10.29), u_port 2.98 m/s, u_slot 0.13, u_ch 0.165, pump 14.8 W, avg 23.6/max 27.2
CoolIT-like at 36 LPM: dP 69.3 kPa, pump 41.6 W, avg 31.0/max 40.8

## G. Geometry/hydraulic sanity (hand calc)
  slot 3.0 x 8 mm: entry u 0.48 m/s, dyn head 116 Pa, branch/dyn = 2.2
  slot 3.0 x 10 mm: entry u 0.38 m/s, dyn head 74 Pa, branch/dyn = 3.5
  slot 3.0 x 12 mm: entry u 0.32 m/s, dyn head 52 Pa, branch/dyn = 5.0
  slot 3.0 x 15 mm: entry u 0.26 m/s, dyn head 33 Pa, branch/dyn = 7.9
  selector slit 1.2 x 12 mm: u 1.60 m/s, dp 1.94 kPa at 18 LPM
  selector slit 1.5 x 12 mm: u 1.28 m/s, dp 1.24 kPa at 18 LPM
  selector slit 2.0 x 12 mm: u 0.96 m/s, dp 0.70 kPa at 18 LPM
  end-fed header 20x10 mm: u 1.50 m/s, dyn head 1131 Pa (branch ~2.8 kPa -> ratio 2)
  end-fed header 15x10 mm: u 2.00 m/s, dyn head 2010 Pa (branch ~2.8 kPa -> ratio 1)
  end-fed header 25x12 mm: u 1.00 m/s, dyn head 502 Pa (branch ~2.8 kPa -> ratio 6)
  burst 1.5 MPa: fin tensile 3.8 MPa, bond-line nominal 15 MPa (25 % bonded), Kt2.5 local 9 MPa in fin tip
  burst 2.0 MPa: fin tensile 5.0 MPa, bond-line nominal 20 MPa (25 % bonded), Kt2.5 local 12 MPa in fin tip
  period 4 mm, Cu 2 mm: Fourier attenuation 0.015 -> 0.19 K pk-pk (FV ~2x) 
  period 8 mm, Cu 3 mm: Fourier attenuation 0.056 -> 0.71 K pk-pk (FV ~2x) 
  period 12 mm, Cu 3 mm: Fourier attenuation 0.161 -> 2.05 K pk-pk (FV ~2x) 
  15kW-class 125x125: blank 3.28 kg, finished ~2.39 kg (base 0.39, comb net 0.62, floor 0.28, cover 1.20)
  GPU-class 110x120: blank 2.83 kg, finished ~2.10 kg (base 0.33, comb net 0.54, floor 0.24, cover 1.08)
