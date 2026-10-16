# Two-phase (flow boiling) option for the HMMC core -- script output

HMMC core: b=0.10 mm, t=0.10 mm, H=1.0 mm, L=2.0 mm, Dh=182 um, L/Dh=11.0, segments=29250, flow area=29.25 cm2, raw area ratio=10.5, inlet/return slots=27 each

## 1. Saturation temperature forced by a 45 C facility-water condenser (isothermal pinch 3 K)
| facility flow LPM/kW | coolant | water rise K | Tsat required C |
|---:|---|---:|---:|
| 1.0 | PG25 | 15.2 | 63.2 |
| 1.0 | water | 14.5 | 62.5 |
| 1.2 | PG25 | 12.7 | 60.7 |
| 1.2 | water | 12.1 | 60.1 |
| 1.5 | PG25 | 10.1 | 58.1 |
| 1.5 | water | 9.7 | 57.7 |
| 2.0 | PG25 | 7.6 | 55.6 |
| 2.0 | water | 7.3 | 55.3 |
| 2.5 | PG25 | 6.1 | 54.1 |
| 2.5 | water | 5.8 | 53.8 |
| 3.0 | PG25 | 5.1 | 53.1 |
| 3.0 | water | 4.8 | 52.8 |
Single-phase comparison basis: benchmark plate inlet 45 C (CoolIT TTV); 'system basis' adds a 3 K liquid-liquid CDU approach (48 C).

## 2. Refrigerant flow for x_out = 0.2-0.5 (15 kW; 3 K inlet subcooling)
| fluid | x_out | mdot kg/s | liquid LPM | LPM/kW | G kg/m2s | Re_lo | vapour+liquid at exit LPM |
|---|---:|---:|---:|---:|---:|---:|---:|
| R1233zd(E) | 0.2 | 0.392 | 19.7 | 1.31 | 134 | 81 | 257 |
| R1233zd(E) | 0.3 | 0.270 | 13.6 | 0.90 | 92 | 56 | 259 |
| R1233zd(E) | 0.4 | 0.206 | 10.4 | 0.69 | 71 | 43 | 260 |
| R1233zd(E) | 0.5 | 0.167 | 8.4 | 0.56 | 57 | 35 | 261 |
| R515B | 0.2 | 0.498 | 28.8 | 1.92 | 170 | 214 | 119 |
| R515B | 0.3 | 0.350 | 20.2 | 1.34 | 120 | 150 | 116 |
| R515B | 0.4 | 0.269 | 15.5 | 1.04 | 92 | 115 | 114 |
| R515B | 0.5 | 0.219 | 12.6 | 0.84 | 75 | 94 | 112 |
| Novec 7000 | 0.2 | 0.516 | 23.4 | 1.56 | 177 | 107 | 373 |
| Novec 7000 | 0.3 | 0.361 | 16.3 | 1.09 | 123 | 75 | 383 |
| Novec 7000 | 0.4 | 0.278 | 12.6 | 0.84 | 95 | 58 | 388 |
| Novec 7000 | 0.5 | 0.225 | 10.2 | 0.68 | 77 | 47 | 391 |
| Novec 7100 | 0.2 | 0.574 | 24.1 | 1.60 | 196 | 96 | 801 |
| Novec 7100 | 0.3 | 0.402 | 16.9 | 1.12 | 137 | 67 | 833 |
| Novec 7100 | 0.4 | 0.309 | 13.0 | 0.86 | 106 | 52 | 850 |
| Novec 7100 | 0.5 | 0.251 | 10.5 | 0.70 | 86 | 42 | 861 |
Single-phase PG25 reference: 18 LPM (1.2 LPM/kW), G = 103 kg/m2s, Re = 15 in the same channels.

## 3. Flow-boiling HTC and convective term (x_out = 0.3, Tsat 60 C, paste TIM)
| fluid | Q kW | q_fp W/cm2 | q_w W/cm2 | h Cooper | h Bertsch | h Kandlikar(F=1) | eta (Cooper) | h_eff kW/m2K | conv K (Cooper) | conv K (Bertsch) | conv K (Kandlikar) | SP PG25 conv K |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1233zd(E) | 15 | 128 | 14.2 | 10.6 | 10.9 | 121.3 | 0.85 | 95 | 13.4 | 13.1 | 2.4 | 8.1 |
| R1233zd(E) | 30 | 256 | 31.0 | 17.9 | 17.4 | 121.3 | 0.78 | 148 | 17.4 | 17.7 | 4.7 | 15.6 |
| R1233zd(E) | 35 | 299 | 37.1 | 20.1 | 19.4 | 121.3 | 0.76 | 162 | 18.4 | 19.0 | 5.5 | 18.0 |
| R515B | 15 | 128 | 15.9 | 20.3 | 19.1 | 104.2 | 0.76 | 163 | 7.9 | 8.2 | 2.6 | 8.1 |
| R515B | 30 | 256 | 36.7 | 35.5 | 32.1 | 104.2 | 0.65 | 247 | 10.4 | 11.1 | 5.2 | 15.6 |
| R515B | 35 | 299 | 44.6 | 40.4 | 36.2 | 104.2 | 0.62 | 271 | 11.0 | 11.9 | 6.1 | 18.0 |
| Novec 7000 | 15 | 128 | 13.8 | 8.1 | 9.0 | 115.2 | 0.88 | 75 | 17.0 | 15.5 | 2.4 | 8.1 |
| Novec 7000 | 30 | 256 | 29.5 | 13.5 | 14.0 | 115.2 | 0.82 | 117 | 21.9 | 21.2 | 4.9 | 15.6 |
| Novec 7000 | 35 | 299 | 35.1 | 15.1 | 15.6 | 115.2 | 0.80 | 129 | 23.2 | 22.7 | 5.7 | 18.0 |
| Novec 7100 | 15 | 128 | 13.3 | 5.5 | 6.6 | 101.8 | 0.92 | 53 | 24.3 | 20.4 | 2.6 | 8.1 |
| Novec 7100 | 30 | 256 | 27.9 | 9.0 | 10.1 | 101.8 | 0.87 | 82 | 31.1 | 28.0 | 5.3 | 15.6 |
| Novec 7100 | 35 | 299 | 33.0 | 10.0 | 11.1 | 101.8 | 0.86 | 91 | 32.9 | 30.0 | 6.1 | 18.0 |
Single-phase PG25 HMMC at 15 kW: h = 19.4 kW/m2K, eta = 0.76, area ratio 8.1, h_eff = 158 kW/m2K.

## 4. CHF / dryout margin on the wetted wall (x_out = 0.3 design flow, 3 K subcooling)
| fluid | q_fp W/cm2 | G | q_w W/cm2 | We_L | Katto-Ohno W/cm2 (regime) | Qu-Mudawar W/cm2* | Bowers-Mudawar W/cm2* | x=1 energy cap W/cm2 | dryout (x~0.6) W/cm2 | margin to dryout | margin to x=1 |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|
| R1233zd(E) | 128 | 92 | 14.2 | 1.24 | 37 (L-regime (x->1 energy limit)) | 222 | 67 | 38 | 23 | 1.60 | 2.66 |
| R1233zd(E) | 256 | 185 | 31.0 | 4.97 | 69 (L-regime (x->1 energy limit)) | 332 | 103 | 76 | 45 | 1.46 | 2.44 |
| R1233zd(E) | 299 | 216 | 37.1 | 6.76 | 80 (L-regime (x->1 energy limit)) | 363 | 113 | 88 | 53 | 1.43 | 2.38 |
| R515B | 128 | 120 | 15.9 | 5.00 | 34 (L-regime (x->1 energy limit)) | 673 | 49 | 36 | 22 | 1.37 | 2.29 |
| R515B | 256 | 239 | 36.7 | 19.99 | 64 (L-regime (x->1 energy limit)) | 1006 | 76 | 73 | 44 | 1.19 | 1.98 |
| R515B | 299 | 279 | 44.6 | 27.20 | 73 (L-regime (x->1 energy limit)) | 1100 | 84 | 85 | 51 | 1.14 | 1.91 |
| Novec 7000 | 128 | 123 | 13.8 | 2.42 | 35 (L-regime (x->1 energy limit)) | 148 | 57 | 37 | 22 | 1.60 | 2.67 |
| Novec 7000 | 256 | 247 | 29.5 | 9.68 | 66 (L-regime (x->1 energy limit)) | 222 | 88 | 73 | 44 | 1.49 | 2.49 |
| Novec 7000 | 299 | 288 | 35.1 | 13.18 | 76 (L-regime (x->1 energy limit)) | 242 | 97 | 86 | 51 | 1.47 | 2.44 |
| Novec 7100 | 128 | 137 | 13.3 | 2.51 | 35 (L-regime (x->1 energy limit)) | 63 | 57 | 37 | 22 | 1.66 | 2.76 |
| Novec 7100 | 256 | 275 | 27.9 | 10.04 | 66 (L-regime (x->1 energy limit)) | 94 | 87 | 73 | 44 | 1.58 | 2.63 |
| Novec 7100 | 299 | 320 | 33.0 | 13.67 | 76 (L-regime (x->1 energy limit)) | 103 | 96 | 85 | 51 | 1.56 | 2.59 |
*Qu-Mudawar (valid L/Dh >= 20, We_L >~ 5) and Bowers-Mudawar are extrapolated here and exceed the energy-balance cap -> non-physical; the binding limit at these low mass fluxes is dryout (quality), i.e. margin = x_dry/x_out ~ 2 at x_out = 0.3.
Fixed-flow stress test (flow sized for 15 kW at x_out = 0.3, then load raised):
| fluid | Q kW | x_out at fixed G | dryout? |
|---|---:|---:|---|
| R1233zd(E) | 15 | 0.30 | no |
| R1233zd(E) | 20 | 0.41 | no |
| R1233zd(E) | 25 | 0.52 | marginal |
| R1233zd(E) | 30 | 0.62 | YES (x > 0.6) |
| R1233zd(E) | 35 | 0.73 | YES (x > 0.6) |
| R515B | 15 | 0.30 | no |
| R515B | 20 | 0.41 | no |
| R515B | 25 | 0.52 | marginal |
| R515B | 30 | 0.64 | YES (x > 0.6) |
| R515B | 35 | 0.75 | YES (x > 0.6) |

## 5. Two-phase pressure drop budget (x_out = 0.3, Tsat 60 C)
| fluid | Q kW | core friction Pa | accel Pa | return slot Pa (u m/s) | return manifold Pa | vapour port Pa (d mm) | liquid inlet+orifice Pa | total kPa | exit mixture LPM | rho_mix kg/m3 | pump W |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1233zd(E) | 15 | 56 | 65 | 1140 (4.9) | 3131 | 6763 (21) | 2000 | 13.2 | 259 | 63 | 3.0 |
| R1233zd(E) | 30 | 112 | 260 | 4559 (9.9) | 3131 | 6763 (30) | 2000 | 16.8 | 518 | 63 | 7.6 |
| R515B | 15 | 34 | 40 | 658 (2.2) | 9071 | 19594 (14) | 2000 | 31.4 | 116 | 181 | 10.6 |
| R515B | 30 | 67 | 160 | 2633 (4.4) | 9071 | 19594 (20) | 2000 | 33.5 | 231 | 181 | 22.5 |
| Novec 7000 | 15 | 75 | 126 | 2250 (7.3) | 2829 | 6112 (26) | 2000 | 13.4 | 383 | 57 | 3.6 |
| Novec 7000 | 30 | 150 | 504 | 9001 (14.6) | 2829 | 6112 (37) | 2000 | 20.6 | 766 | 57 | 11.2 |
| Novec 7100 | 15 | 118 | 284 | 5449 (15.9) | 1446 | 3123 (38) | 2000 | 12.4 | 833 | 29 | 3.5 |
| Novec 7100 | 30 | 237 | 1134 | 21797 (31.7) | 1446 | 3123 (54) | 2000 | 29.7 | 1667 | 29 | 16.7 |
Single-phase HMMC PG25: 6.2 kPa / 1.9 W at 15 kW; 6.6 kPa / 4.0 W at 30 kW (36 LPM).

## 6. Case-to-45C budget: two-phase HMMC vs single-phase HMMC (hotspot +4 K on both)
| design | Q kW | q W/cm2 | Tsat-45 / caloric K | TIM K | base K | conv K | **avg dT K** | max dT K | flow LPM | dP kPa |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SP HMMC PG25, paste (thin BLT), plate inlet 45 C | 15 | 128 | 6.3 | 6.4 | 3.3 | 8.1 | **24.1** | 28.1 | 18 | 6.2 |
| SP HMMC PG25, paste (thin BLT), system basis (+3 K CDU) | 15 | 128 | 9.3 | 6.4 | 3.3 | 8.1 | **27.1** | 31.1 | 18 | 6.2 |
| SP HMMC PG25, liquid metal, plate inlet 45 C | 15 | 128 | 6.3 | 1.9 | 3.3 | 8.1 | **19.7** | 23.7 | 18 | 6.2 |
| SP HMMC PG25, liquid metal, system basis (+3 K CDU) | 15 | 128 | 9.3 | 1.9 | 3.3 | 8.1 | **22.7** | 26.7 | 18 | 6.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 60 C, h=cooper | 15 | 128 | 15.0 | 6.4 | 3.3 | 13.4 | **38.1** | 42.1 | 14 | 13.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 60 C, h=enhanced | 15 | 128 | 15.0 | 6.4 | 3.3 | 5.8 | **30.5** | 34.5 | 14 | 13.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 60 C, h=kandlikar | 15 | 128 | 15.0 | 6.4 | 3.3 | 2.4 | **27.1** | 31.1 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 60 C, h=cooper | 15 | 128 | 15.0 | 1.9 | 3.3 | 13.4 | **33.6** | 37.6 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 60 C, h=enhanced | 15 | 128 | 15.0 | 1.9 | 3.3 | 5.8 | **26.0** | 30.0 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 60 C, h=kandlikar | 15 | 128 | 15.0 | 1.9 | 3.3 | 2.4 | **22.6** | 26.6 | 14 | 13.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 55 C, h=cooper | 15 | 128 | 10.0 | 6.4 | 3.3 | 14.2 | **33.9** | 37.9 | 14 | 13.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 55 C, h=enhanced | 15 | 128 | 10.0 | 6.4 | 3.3 | 6.1 | **25.8** | 29.8 | 14 | 13.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 55 C, h=kandlikar | 15 | 128 | 10.0 | 6.4 | 3.3 | 2.4 | **22.1** | 26.1 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 55 C, h=cooper | 15 | 128 | 10.0 | 1.9 | 3.3 | 14.2 | **29.4** | 33.4 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 55 C, h=enhanced | 15 | 128 | 10.0 | 1.9 | 3.3 | 6.1 | **21.3** | 25.3 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 55 C, h=kandlikar | 15 | 128 | 10.0 | 1.9 | 3.3 | 2.4 | **17.6** | 21.6 | 14 | 13.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 50 C, h=cooper | 15 | 128 | 5.0 | 6.4 | 3.3 | 14.2 | **28.9** | 32.9 | 14 | 13.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 50 C, h=enhanced | 15 | 128 | 5.0 | 6.4 | 3.3 | 6.1 | **20.8** | 24.8 | 14 | 13.2 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 50 C, h=kandlikar | 15 | 128 | 5.0 | 6.4 | 3.3 | 2.4 | **17.1** | 21.1 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 50 C, h=cooper | 15 | 128 | 5.0 | 1.9 | 3.3 | 14.2 | **24.4** | 28.4 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 50 C, h=enhanced | 15 | 128 | 5.0 | 1.9 | 3.3 | 6.1 | **16.3** | 20.3 | 14 | 13.2 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 50 C, h=kandlikar | 15 | 128 | 5.0 | 1.9 | 3.3 | 2.4 | **12.6** | 16.6 | 14 | 13.2 |
| SP HMMC PG25, paste (thin BLT), plate inlet 45 C | 30 | 256 | 6.3 | 12.8 | 6.6 | 15.6 | **41.4** | 45.4 | 36 | 6.6 |
| SP HMMC PG25, paste (thin BLT), system basis (+3 K CDU) | 30 | 256 | 9.3 | 12.8 | 6.6 | 15.6 | **44.4** | 48.4 | 36 | 6.6 |
| SP HMMC PG25, liquid metal, plate inlet 45 C | 30 | 256 | 6.3 | 3.8 | 6.6 | 15.6 | **32.4** | 36.4 | 36 | 6.6 |
| SP HMMC PG25, liquid metal, system basis (+3 K CDU) | 30 | 256 | 9.3 | 3.8 | 6.6 | 15.6 | **35.4** | 39.4 | 36 | 6.6 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 60 C, h=cooper | 30 | 256 | 15.0 | 12.8 | 6.6 | 17.4 | **51.8** | 55.8 | 27 | 16.8 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 60 C, h=enhanced | 30 | 256 | 15.0 | 12.8 | 6.6 | 7.7 | **42.1** | 46.1 | 27 | 16.8 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 60 C, h=kandlikar | 30 | 256 | 15.0 | 12.8 | 6.6 | 4.7 | **39.1** | 43.1 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 60 C, h=cooper | 30 | 256 | 15.0 | 3.8 | 6.6 | 17.4 | **42.8** | 46.8 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 60 C, h=enhanced | 30 | 256 | 15.0 | 3.8 | 6.6 | 7.7 | **33.1** | 37.1 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 60 C, h=kandlikar | 30 | 256 | 15.0 | 3.8 | 6.6 | 4.7 | **30.2** | 34.2 | 27 | 16.8 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 55 C, h=cooper | 30 | 256 | 10.0 | 12.8 | 6.6 | 18.3 | **47.7** | 51.7 | 27 | 16.8 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 55 C, h=enhanced | 30 | 256 | 10.0 | 12.8 | 6.6 | 8.1 | **37.5** | 41.5 | 27 | 16.8 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 55 C, h=kandlikar | 30 | 256 | 10.0 | 12.8 | 6.6 | 4.7 | **34.1** | 38.1 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 55 C, h=cooper | 30 | 256 | 10.0 | 3.8 | 6.6 | 18.3 | **38.7** | 42.7 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 55 C, h=enhanced | 30 | 256 | 10.0 | 3.8 | 6.6 | 8.1 | **28.5** | 32.5 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 55 C, h=kandlikar | 30 | 256 | 10.0 | 3.8 | 6.6 | 4.7 | **25.2** | 29.2 | 27 | 16.8 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 50 C, h=cooper | 30 | 256 | 5.0 | 12.8 | 6.6 | 18.3 | **42.7** | 46.7 | 27 | 16.8 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 50 C, h=enhanced | 30 | 256 | 5.0 | 12.8 | 6.6 | 8.1 | **32.5** | 36.5 | 27 | 16.8 |
| 2P HMMC R1233zd(E), paste (thin BLT), Tsat 50 C, h=kandlikar | 30 | 256 | 5.0 | 12.8 | 6.6 | 4.7 | **29.1** | 33.1 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 50 C, h=cooper | 30 | 256 | 5.0 | 3.8 | 6.6 | 18.3 | **33.7** | 37.7 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 50 C, h=enhanced | 30 | 256 | 5.0 | 3.8 | 6.6 | 8.1 | **23.5** | 27.5 | 27 | 16.8 |
| 2P HMMC R1233zd(E), liquid metal, Tsat 50 C, h=kandlikar | 30 | 256 | 5.0 | 3.8 | 6.6 | 4.7 | **20.2** | 24.2 | 27 | 16.8 |

### Net benefit of the two-phase variant (negative = two-phase is hotter), vs SP HMMC + liquid metal, plate-inlet basis
| Q kW | Tsat C | benefit K (Cooper h, plain Cu) | benefit K (2.5x Cooper, enhanced surface) | benefit K (Kandlikar h, upper bound) |
|---:|---:|---:|---:|---:|
| 15 | 60 | -14.0 | -6.3 | -2.9 |
| 15 | 55 | -9.7 | -1.6 | +2.1 |
| 15 | 50 | -4.7 | +3.4 | +7.1 |
| 30 | 60 | -10.4 | -0.7 | +2.2 |
| 30 | 55 | -6.3 | +3.9 | +7.2 |
| 30 | 50 | -1.3 | +8.9 | +12.2 |

## 7. Footprint-flux crossover (liquid metal TIM, 117 cm2, SP at 1.2 LPM/kW; 2P R1233zd(E), x_out = 0.3)
| q W/cm2 | Q kW | SP avg dT | 2P Tsat 60 (Cooper/enhanced/Kandlikar) | 2P Tsat 55 (Cooper/enhanced/Kandlikar) | SP ultrafine 0.05/0.05x0.6 avg dT |
|---:|---:|---:|---|---|---:|
| 128 | 15 | 19.6 | 33.6 / 26.0 / 22.6 | 29.4 / 21.3 / 17.6 | 15.3 |
| 200 | 23 | 26.9 | 39.0 / 30.1 / 26.8 | 34.8 / 25.4 / 21.8 | 20.3 |
| 256 | 30 | 32.3 | 42.8 / 33.1 / 30.1 | 38.7 / 28.5 / 25.1 | 24.1 |
| 300 | 35 | 36.6 | 45.6 / 35.4 / 32.7 | 41.6 / 30.8 / 27.7 | 27.2 |
| 400 | 47 | 46.1 | 51.9 / 40.6 / 38.7 | 48.0 / 36.1 / 33.7 | 34.0 |
| 500 | 58 | 55.3 | 57.9 / 45.7 / 44.6 | 54.0 / 41.2 / 39.6 | 40.7 |

## 8. Fluid practicalities
| fluid | Psat 55 C bar | Psat 60 C bar | Psat ~80 C (no-flow fault) bar est. | rho_v kg/m3 | vapour LPM per kW at x_out 0.3 | GWP | status |
|---|---:|---:|---:|---:|---:|---|---|
| R1233zd(E) | 3.3 | 3.9 | 6.1 | 19.5 | 18 | 1 (AR5) / 3.7 (AR6), ODP 0.0003 | HCFO, A1, in production (Honeywell/Arkema/Chinese); PFAS-restriction scope |
| R515B | 10.3 | 11.7 | 15.9 | 62.0 | 8 | ~299 (AR4), contains 8.9 % R227ea (HFC) | HFO/HFC blend, A1; HFC content inside EU quota; 11-12 bar at 60 C |
| Novec 7000 | 2.0 | 2.4 | 4.0 | 17.5 | 27 | ~530 | HFE; 3M exited PFAS manufacture end-2025 -> supply ending; PFAS scope |
| Novec 7100 | 0.8 | 1.0 | 1.7 | 8.8 | 61 | ~320 | HFE; sub-atmospheric at 55 C (air ingress); 3M exit; PFAS scope |

Tsat sensitivity to pressure drop, R1233zd(E) ~60 C: dP/dT ~ 11 kPa/K -> a 10 kPa plate+line drop lowers outlet Tsat by ~0.9 K (benign).
