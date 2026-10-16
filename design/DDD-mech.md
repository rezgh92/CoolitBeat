# DDD-mech: mounting and integration (spring screws, load frame, backplate, TTV interface, PRISM-G envelope, HBM pedestal), PRISM-15 Rev A

Detailed design definition, lane `mech`, 2026-10-15. Parent: `docs/cooling/03-architecture.md` (architecture of record: 2.2 stack, 2.3 tiers, 3.5 HBM pedestal, 5.1 parts and mass, 5.6 height and mass limits, 7.5 LM containment, 7.6 mechanical integration, 13.2 E3/E5). Binding sibling lanes: `DDD-core.md` / `params-core.json` (body 125 x 125, ears, datums A/B/C, die-face flatness, pedestal variant), `DDD-grate.md` / `params-grate.json`, `DDD-plenum.md` / `plenum_sep_data.json` (end frames at y = +-57.0..59.5, flanges at x = +-58.86..60.36, separator z 10.30-12.10, cap flat on z 12.10, separator windows at y -21/-7 inlet and +9/+23/+37/+51 outlet). Script: `mech_calc.py` -> `mech_calc.out`, `mech_calc_data.json`; parameters: `params-mech.json`. Verifier inputs honoured: `appendix/verify/verify-manufacturing.md` #22 (mass boundary: load frame excluded), `appendix/physics/base-stress-stiffness.out` (mounting and thermal bow method), `appendix/physics/nonuniform-heatmap.md` (pedestal + 0.1 mm compliant TIM), `appendix/research/gap-tim2-...md` (clamp windows), `gap-coolit-15kw-ttv-footprint-heater-map.md` (8-TC layout inference). Model terms +-25 % until E1/E3/E5; dimensions are drawing values, mm.

**Conventions.** X along the fins, Y along the lines, Z up from the die face (datum A), origin at the fin-field centre. Cap top flat at z 13.10 (separator top 12.10 + 1.0 mm cap sheet). Ears (core 3.7/3.8): 8 off, top z 1.50, holes at (+-40, +-66) and (+-66, +-40). Heated area 108 x 108 (|x|, |y| <= 54).

## 1. Requirements carried by this lane

| # | Requirement | Value | Source |
|---|---|---|---|
| M1 | Retention pressure on the TTV (PCM datasheet condition) | 25 psi = 0.172 MPa on 116.6 cm2 -> 2,011 N; TTV-100: 1,724 N | architecture 2.3, 7.6; task |
| M2 | Retention on a package | 4-12 psi on ~100 cm2 (276-827 N); bare die 0.15-0.35 MPa on the die block; window 0.3-1 kN | architecture 2.3, 7.6; gap-tim2 §4 |
| M3 | 8 spring-loaded captive screws, force set by geometry not torque; bearing on a stiff load frame within 10 mm of the heated area | lands at y = +-(56.8..59.5): 2.8-5.5 mm outside the field | task; architecture 7.6 |
| M4 | Clamp bow under 2 kN measured, not assumed; load-frame FEA at 0.3-1 kN and 2 kN in E1 | this lane gives the closed-form bound (section 7) | architecture 7.6 |
| M5 | Shock: the frame's hard stops carry the plate's inertial load, not the package | 30-50 g x 1.33 kg = 390-650 N; stops both ways (section 11) | architecture 7.6 |
| M6 | Mass: plate + stubs + springs + backplate, no load frame | 1.24 kg target; SKU limit PRISM-15 <= 1.4 kg, PRISM-G <= 0.9 kg plate only | architecture 0.2, 5.6 |
| M7 | Materials: no Al within the LM zone on T2/T3 SKUs; wetted list unchanged (this lane adds nothing wetted except 316L stubs) | steel frames on T2/T3; 6061 permitted on T1 fixtures only | architecture 7.5, 10.2 |
| M8 | Datum A registration of the plate to the TTV; 8 TCs replicating CoolIT's layout; TTV-A and TTV-100 | section 6 | architecture 1.3, 13.2 E3 |
| M9 | HBM stepped pedestal: step 0-0.4, +-0.05, in the post-braze fly-cut; compliant TIM 0.05-0.10 | section 8 | architecture 3.5; task |
| M10 | PRISM-G envelope: 110 x 120 field, ~19-21 mm at the bar, horizontal 10 mm ports | section 9 | architecture 2.3, 5.6 |
| M11 | Flatness of the die face <= 0.020 over the field, Ra <= 0.8; TIM tiers T1/T2/T3 by face finish | sign rule added in 7.3 | architecture 2.2, 2.3; core 1 |
| M12 | Orientation tests 0/90/180 deg, ISTA 3A / ASTM D4169 with the plate installed | envelope in section 11 | architecture 7.6, 13.2 E5 |

## 2. Mounting concept and load paths

### 2.1 Why the ears cannot carry the springs

The core's ears are 1.5 mm annealed OFE tabs (allowable 40 MPa) with the hole 3.5 mm outboard of the body edge. A screw bearing on an ear puts 6 F x 3.5 / (12 x 1.5^2) = 0.78 MPa per newton into the root (`mech_calc.out` §2): 31 MPa at 40 N, 47 MPa at 60 N, 195 MPa at 251 N. Even the lightest package kit exceeds the allowable; the TTV kit would fold the ears. The ears are therefore **pass-throughs and keepers only**: the shoulder of each screw passes through the Ø4.50 ear hole with 0.25 radial clearance and never loads it in service (lateral shock only, section 11).

### 2.2 Chosen load path

| Element | Path | Note |
|---|---|---|
| Spring force | screw head -> spring -> load-frame lug -> frame body -> **two bearing lands on the cap top at y = +-(56.8..59.5), full width x -60..+60** -> cap 1.0 -> separator 1.8 -> plenum end frame PLN-F (y 57.0-59.5, solid OFE 2.5 x 5.78) -> grate web + land plate -> rim top (y 54.15-60.7) -> base -> die face -> TIM | every layer under the land is solid or a face joint in compression; bearing 3.35 MPa at the TTV clamp (one band carries 1,006 N over 2.7 x 120), 1.5 MPa on the 110 N kit |
| Screw reaction | screw shoulder bottomed on the stop face of the TTV carrier boss / product standoff (z -2.15 / -2.30) -> carrier or backplate | force is set by spring deflection = (head height fixed by the shoulder) - (lug height fixed by the plate); torque only seats the shoulder |
| Lateral | plate floats +-0.25 on the shoulders; located by the package/TTV datums, not by the screws | shoulders are the lateral hard stops |
| Vertical down (shock) | ear underside onto the boss/standoff top face after a gap g (0.15 TTV, 0.40 product nominal) | section 11 |
| Vertical up (shock) | frame rises against the spring until the lug meets the stop sleeve SLV on the screw (0.3 TTV / 0.8 product) -> screw -> backplate | section 11 |

**Why two lands and not four.** The cap top is flat across the full width only in the arch-free bands |y| >= 56.5 (the inlet arches occupy y -27..-1, the outlet arches y 3..57 with their ends reaching |x| ~58.5 to cover the edge-outlet windows at x 51.5-56.5), so a continuous land on the +-x sides does not exist; bearing on the cap over the field is excluded because the 1.8 mm separator over an outlet channel would see 64-83 MPa under a 3 mm line load; bearing on the base land outside the skirt leaves 0.4 mm of usable width after tolerances. Two full-length lands over the end frames are statically stable (two long runners), solid underneath, and give a clamp bow of 22.6 um at 2 kN / 5.4 um at 480 N (section 7), which the thermal bow of the hot base largely cancels in operation. Four-side bearing (6.7 um) is recorded as the fallback if E1 FEA or the water-table flatness scan says otherwise (open item O-M2).

### 2.3 Alternatives considered

| Option | Verdict |
|---|---|
| Springs on the ears, no frame (CoolIT-style) | rejected: 47-195 MPa in annealed ears; 8 point loads give 20-120 um corner bow (`base-stress-stiffness.out` §5) |
| 2.8 mm thick ears (rim height) | holds 110 N (25 MPa) but not the TTV; still point loading; core blank unchanged but ear mass x1.9; kept as a cost-down option for low-pressure LM SKUs (O-M4) |
| Flat 4 mm frame bearing on the cap +-y lands | rejected: the +-x members (11 wide) deflect 0.60 mm under 2 x 251 N; the frame must be a 16 mm deep ring (section 4) |
| Frame feet on the exposed base land outside the skirt (|x| 61.7-62.5) | rejected: 0.4 mm usable after skirt +-0.3 and body +-0.1 |
| Frame bearing on cap flats between the arches | rejected: 2 mm gaps consumed by draw radii |

## 3. Spring-loaded captive screw set (8 off per plate)

### 3.1 Parts

| Part | Spec | Dimension (mm) | Tolerance | Basis |
|---|---|---|---|---|
| CSS-15P / CSS-15T screw | 17-4PH H900 (or A2-70 for T1 pilots), passivated; M3x0.5-6g thread 6.0 long; shoulder Ø4.00 h8; head Ø8.5 x 3.0, hex socket 2.5 AF + cross slot; e-clip groove Ø3.2 x 0.7 | shoulder length Ls: **40.40 (P)**, **45.94 (T)**; groove top face 29.0 (P) / 36.0 (T) below the head underside | Ls +-0.10; shoulder h8; groove +-0.05 | `mech_calc.out` §4 stack: Ls = lug/pocket height + installed spring + 1.0 washer - stop face z |
| SPR-60 coil spring (default product kit) | 302 SS wire d 1.30, mean Ø 6.50 (OD 7.80), 8.6 active / 10.6 total coils, closed and ground, shot-peened, preset | L0 27.5, installed 22.0 -> 5.5 deflection | k 10.8 N/mm +-10 %; L0 +-0.5 | §3: 60 N; tau 592 MPa = 0.35 UTS; solid 13.8 |
| SPR-110 coil spring (high-pressure PCM / shipping-mounted kit) | 302 SS d 1.60, mean Ø 6.40 (OD 8.00), 11.0 active / 13 total | L0 27.4, installed 22.0 -> 5.4 deflection | k 20.4 N/mm +-10 % | §3: 110 N; tau 614 MPa = 0.36 UTS; solid 20.8 (margin 1.2 = lift-off stop) |
| DIE-TTV spring (TTV kit) | ISO 10243 heavy duty (red), Cr-Si rectangular wire, 12.5 OD x 6.3 bore x 32 L0 | installed 24.7 at 251 N (7.3 deflection, 22.8 % L0; limit 25 % at 2e6 cycles) | k ~34 N/mm (89 mm catalogue value 12.36 scaled 89/32; vendor sheet +-10 %, O-M1) | Accu TJH12.5-89 data; `mech_calc.out` §3 |
| SLV-P / SLV-T stop sleeve | 303 SS tube over the shoulder inside the spring: P Ø5.5/Ø4.1 x 21.2; T Ø6.2/Ø4.1 x 24.4 (also guides the die spring bore) | length = installed spring - lift-off travel (0.8 P / 0.3 T) | +-0.05 | section 11 |
| WSH-8 / WSH-13 washers | 301 SS Ø8.5/4.2 x 1.0 under the coil spring; Ø13/4.3 x 1.0 under the die spring | - | - | spring seat |
| E-clip | DIN 6799 size 3.2 (shaft 4), 0.6 thick, OD 7.4 | under the frame lug in free air (z 13.0-13.6 removed state, z ~9 mounted) | - | captive to the frame |
| STD-8 standoff (product backplate) | 17-4PH or 4140, Ø8.0 x 7.6 (for a 2.4 PCB + 5.2 package stack; package-specific), pressed into the backplate; top face = ear stop; Ø4.20 H9 bore 2.00 deep to the shoulder step; M3-6H from the step through | top at z -0.40 (ear gap 0.40 +-0.30 incl. package height); step at z -2.30 | top face +-0.05 to the backplate datum | §4 |
| Carrier boss (TTV, integral) | Ø9 boss on the carrier, top z -0.15 +-0.03; Ø4.20 H9 bore 2.00 deep; M3-6H x 8 | ear gap 0.15 (stack held +-0.05) | - | section 6 |

Spring-rate and free-length tolerances convert to force bands at the installed length: SPR-60 +-6.0 (rate) +-5.4 (L0) +-3.3 (package height +-0.3) -> 60 +-9 N RSS per screw, 480 +-25 N on 8 (5 %); SPR-110 110 +-16 N; DIE-TTV 251 +-28 N per screw (rate) +-2 (stack) -> 2,011 +-80 N (4 %). Plate-to-plate clamp repeatability is therefore better than the TIM's own pressure sensitivity (PCM 20-40 psi window).

### 3.2 Function, assembly, torque

| Item | Specification |
|---|---|
| Captive screw in the frame | e-clip under the lug; the spring at 1.5 mm residual compression (16 N SPR-60, 31 N SPR-110, 52 N DIE) holds the head up and the clip against the lug; the screw cannot be lost |
| Captive plate in the frame (FRU) | four hook tabs on the product frame LF-15P under the tips of ears E1 (-40,-66), E4 (+40,+66), E6 (-66,+40), E7 (+66,-40): tab 6 wide, lip 1.0 x 0.6, lip underside at z -0.6, 1.0 float; the carrier/backplate/board must be clear below z -0.6 at (+-40, 70-71.5) and (70-71.5, +-40) |
| Installation | place the plate on the package (TIM applied), frame on the plate (lands on the cap, hooks engaged), start all 8 screws 2 turns; drive in a cross sequence to the hard stop at **0.40 +-0.05 N.m** (shoulder on the stop face; the torque rise is the stop signal); the spring force is then 60/110/251 N by geometry, independent of torque within 0.2-0.8 N.m |
| Thread engagement | 4.5 mm in steel (1.5 d) minimum; PEM S-M3 nuts not used where a standoff exists |
| Screw tension at the stop | 667 N torque preload + spring: 918 N (TTV) = 183 MPa on As 5.03 mm2 (41 % of A2-70 proof, 16 % of 17-4PH H900 yield); 777 N product kit | `mech_calc.out` §4 |
| Shoulder | Ø4.00 x 45.9 in compression 53 MPa; Euler 11.8 kN (pinned) | §4 |
| Re-use | 50 mount cycles (TTV 5 plates x 3 re-mounts x spares); replace springs at 1 % set; thread-locking patch (nylon) on CSS-15P for the product |
| Lubricant | none on the TIM side; dry-film MoS2 on the thread only (K 0.2 assumed) |
| Marking | kit letter on the head (P60 / P110 / T) |

## 4. Load frames

### 4.1 LF-15T (TTV test frame, fixture; 2 off + spare)

| Feature | Dimension (mm) | Tolerance | Basis |
|---|---|---|---|
| Material | 6061-T6 (T1 PCM/paste tests); 17-4PH H1025 twin for T2 liquid-metal tests (no Al within the LM zone) | - | M7 |
| Outline | 160 (x) x 150 (y) x 16.0 tall, z 13.10-29.10; corner R10 | +-0.2 | clears the arch tops (z 21.1) and the Ø26 port-boss flanges inside the window |
| Window | 118.6 (x, +-59.3) x 113.0 (y, +-56.5), corner R3 | +-0.1 | +-x inner faces 0.5 outside the outlet-arch ends (|x| <= 58.5 + 0.3) |
| Bearing lands (2) | y = +-(56.8..59.5) x full x; underside z 13.10; rest of the underside relieved 0.50 | lands ground coplanar 0.02, parallel to the lug plane 0.03 | section 2.2; cap land interface CAP-1 |
| +-x members | x 59.3..79.3 (20 wide) x 16 tall: I 6,206 mm4; mid deflection 16 um (Al) / 6 um (steel) under 2 x 251 N at y = +-40 -> lug force change 0.6 N | - | `mech_calc.out` §5 |
| +-y members | y 56.5..74 (17.5 wide) x 16 tall; lug bending 2.5 MPa | - | §5 |
| Lug holes (8) | Ø4.20 H9 through at (+-40, +-66), (+-66, +-40); spring pockets Ø13.2 x 10.0 deep from the top (floor z 19.10), floor flat 0.02; pocket breaks the +-x inner face by 0.1 (by design, the sleeve guides the spring) | position Ø0.05 to the window centre | ear positions, core 3.8 |
| Orientation / handling | one Ø3 H7 pin hole at (+70, -70) matching the carrier; two M4 lifting points; frame mass 0.46 kg (Al), 1.34 kg (steel) | - | within the architecture's 0.3-0.6 kg fixture boundary for Al |

### 4.2 LF-15P (product frame, ships with the FRU)

| Feature | Dimension (mm) | Tolerance | Basis |
|---|---|---|---|
| Material, process | 301 stainless 1/2 hard, 2.00 +-0.05 sheet, stamped and formed, passivated; 85 g | - | mass budget |
| +-y members | flat, z 13.10-15.10, y 56.5..72; bearing lands y 56.8..59.5 coined 0.10 proud (only the lands touch the cap) | lands coplanar 0.05 | section 2.2 |
| +-x members | hat section 14 wide (x 59.5..73.5) x 10 tall (z 13.6-23.6), 2.0 sheet: I ~930 mm4, mid deflection 17 um under 2 x 110 N | - | `mech_calc.out` §5 |
| Lugs (8) | in the bottom flange plane z 13.10-15.10 at the ear positions; hole Ø4.20 +0.10/-0; spring seat Ø8.4 coined 0.3 deep | position Ø0.10 | - |
| Hook tabs (4) | per 3.2 | - | FRU captivity |
| Window | 118.6 x 113.0 as LF-15T | - | - |
| Finish, marking | passivated; laser ID; kit letter | - | - |

The FRU for a product is therefore: plate + LF-15P + 8 x CSS-15P + 8 springs + 8 sleeves/washers/clips = 1.36 kg (section 12); the backplate BP-15P with its 8 standoffs stays with the board.

## 5. Retention force budget

| Interface | Pressure window | Area (cm2) | Force (N) | Per screw (N) | Kit | Result |
|---|---|---|---|---|---|---|
| TTV-A, 4 x 54 x 54 AlN, PCM datasheet | 25 psi (0.172 MPa) | 116.6 | 2,011 | 251 | DIE-TTV, carrier stop z -2.15 | 25.0 psi; +-4 % |
| TTV-100 hard mode, 4 x 50 x 50 Cu-block | 25 psi | 100.0 | 1,724 | 216 | DIE-TTV, carrier stop z -1.11 (stop 1.04 higher -> 6.3 mm deflection) | 25.0 psi |
| TTV, paste comparison runs (20 psi condition, Shin-Etsu TDS) | 20 psi | 116.6 | 1,609 | 201 | DIE-TTV with 1.5 mm shim under the frame lands (-1.5 mm deflection) | 20.0 psi |
| Lidded ~100 cm2 package, PCM at package retention | 4-12 psi | 100 | 276-827 | 35-103 | SPR-60 (480 N) or SPR-110 (880 N) | 7.0 / 12.8 psi |
| Lidded package, liquid metal (T2) | 5-15 psi | 100 | 345-1,034 | - | SPR-60 | 7.0 psi |
| Bare-die 2-die Rubin class, die block 16.6 cm2 (T3) | 0.15-0.35 MPa on the die | 16.6 | 249-581 | - | SPR-60 | 0.29 MPa (41.9 psi) on the die; HBM pedestal load-limited by the 0.05-0.10 compliant TIM |
| Bare-die 4-die, 33 cm2 | 0.15-0.35 MPa | 33 | 495-1,155 | - | SPR-60 (0.145 MPa) or SPR-110 (0.27 MPa) | kit per package |
| Architecture window for packages | 0.3-1 kN | - | 480 / 880 | 60 / 110 | both kits inside the window | M2 met |

Force path checks: lands 3.35 MPa (TTV) / 1.5 MPa (product) on annealed Cu (40); separator under the land is backed by the end frame; fin ties under the rim see no clamp load (the rim is solid). Pressure (MAWP 1.03 MPa x 117 cm2 = 12 kN) is self-equilibrated by the ties and does not enter the clamp budget (architecture 5.2).

## 6. TTV interface (OCP-format test, E3)

### 6.1 Test vehicles

| Item | TTV-A (parity) | TTV-100 (hard mode) |
|---|---|---|
| Heaters | 4 AlN thick-film tiles 54.0 x 54.0 x 2.5 (Watlow ULTRAMIC 600 class, 155 W/cm2 rating, 15 kW = 129 W/cm2 = 83 % of rating; two suppliers), on a 54.3 pitch (0.3 gaps), centres (+-27.15, +-27.15); heated area 116.6 cm2 | 4 OFE Cu blocks 50 x 50 x 25 with 4 x 500 W cartridge heaters each (30 kW), centres (+-25.15, +-25.15), 100 cm2 |
| Contact face | the four tiles lapped together in one setup: coplanar <= 0.010, flatness 0.005 per tile, Ra <= 0.4; face plane = z 0.00 +-0.03 to the carrier datum | Ni-plated 5 um, lapped as left |
| Carrier | 17-4PH H1025 175 x 175 x 16 (304 alternate); top face z -1.00; window 109.0 x 109.0 for the tile block; tiles bonded to a MACOR/alumina insulator on a guard-heated Cu spreader (>= 98 % capture) | same carrier outline and screw pattern, window 101 x 101 |
| Screw bosses (8) | Ø9, top z -0.15 +-0.03 (ear stop), bore Ø4.20 H9 x 2.00 to the step z -2.15 (shoulder stop), M3-6H x 8 | top z +0.89, step z -1.11 (same screw, 6.3 mm deflection) |
| Datum stops | B1, B2: hardened pads 6 x 1.0 at the x = -62.5 face, y = +-40, contact z 0.4-1.3; C1: at the y = -62.5 face, x = +28 (clear of the tap bosses); pushers: 3 spring plungers 15 N on the +x face (y +-40) and +y face (x +28) | same |
| Orientation | pocket 26 x 8 x 3 in the -y rail at x -5..+21 for the two dP-tap bosses (all SKUs carry the bosses): the plate fits one way only | same |
| Registration | plate to tiles +-0.10 (pad 0.02 + body +-0.10); repeatability of a re-mount +-0.05 | - |
| Instrumentation ports | 2 x 1/16-in fittings for the plate's dP-tap stubs (-T plates), inlet/outlet RTDs within 100 mm of the stubs, Coriolis flow | - |

### 6.2 Thermocouples (replicating CoolIT's 2-per-heater layout; positions inferred, `gap-coolit-...heater-map.md` §5)

| TC | Tile | x | y | Role | Line context |
|---|---|---|---|---|---|
| TC1 / TC2 | H1 (-,-) | -27.15 / -27.15 | -27.15 / -48.0 | centre / outer-edge ("outlet-edge" in CoolIT's split-flow) | mid-segment between lines k3 (-30.86, in) and k4 (-23.14, out): 3.7 / 4.0 mm from the kerfs |
| TC3 / TC4 | H2 (+,-) | +27.15 | -27.15 / -48.0 | centre / edge | between k10 (out) and k11 (in) |
| TC5 / TC6 | H3 (-,+) | -27.15 | +27.15 / +48.0 | centre / edge | as H1 |
| TC7 / TC8 | H4 (+,+) | +27.15 | +27.15 / +48.0 | centre / edge | as H2 |
| TC9-TC12 (extra, published separately) | H4 / H1 / H2 / H3 | +2.0 / -51.0 / +51.0 / -51.0 | +2.0 / -51.0 / -51.0 / +51.0 | geometric centre, three corners | corner TCs sit 3 mm inside the field edge, under the edge-outlet segments |

Construction: type T, 36 AWG, calibrated +-0.2 K; bead in a 0.5 wide x 0.5 deep groove diamond-ground from the tile edge, bead centre 0.25 +-0.05 below the face, cemented and lapped flush; bead-depth bias published (+0.5 K at 129 W/cm2 on AlN). TTV-100 uses the same relative positions scaled to the 50 mm blocks ((+-25.15, +-25.15) and (+-25.15, +-44.0)). The mid-segment TC placement reads close to the segment average (case-ripple crest flat within 0.35 K over L 5-8 mm, architecture 3.3); a TC over a kerf would read 0.2-0.4 K lower, which is why position is held to +-0.10.

## 7. Bow: clamp, thermal, net, and the die-face form rule

### 7.1 Stiffness and clamp bow (`mech_calc.out` §6)

Sandwich about the x axis (span in y between the lands): neutral axis z 6.57, EI 2.18e9 N.mm2 over 125 mm (1.74e7 N.mm2 per mm), across-fin shear knock-down 0.83 applied (`base-stress-stiffness.out` §3 method).

| Clamp | 2-side bearing (lands y = +-58.2), concave bow over 116 (um) | 4-side bearing would give (um) |
|---|---:|---:|
| TTV-A 2,011 N | 22.6 | 6.7 |
| TTV-100 1,724 N | 19.4 | 5.7 |
| Product 480 N | 5.4 | 1.6 |
| Product 880 N | 9.9 | 2.9 |

Concave = centre of the die face lifted off the TIM relative to the +-y edges; cylindrical (no x component).

### 7.2 Thermal bow (hot base against the cool stack; laminate solution, `mech_calc.out` §6)

| Condition | Layer temperatures | Curvature (1/m) | Bow over 108 (um) | Over one 54 mm tile (um) |
|---|---|---:|---:|---:|
| 15 kW PCM benchmark | base 65.7 C, fins 58, grate 51.5, plenum/separator/cap 51 (fluid mean) | 0.0128 | 18.7 convex | 4.7 |
| Tcase,max 85 C, paste | base face ~76 C | 0.0217 | 31.7 convex | 7.9 |

Convex = die-face centre proud, corners lift; spherical (both axes). Sensitivity: 1.27 um per K of base-to-stack temperature difference.

### 7.3 Net bow and the form rule

| Case | y direction (um, + convex) | x direction (um) | Consequence |
|---|---:|---:|---|
| TTV 2 kN, 15 kW | 18.7 - 22.6 = **-4.0** | +18.7 | essentially flat in y; corners lift ~19 um in x: PCM +0.3-0.5 K at the x edges, paste +1 K (TIM report bow sensitivity 0.05 / 0.12 K per um) |
| TTV 2 kN, cold (mount check) | -22.6 | 0 | centre lifted 23 um before power: PCM re-flows hot; irrelevant to the hot reading |
| Product 480 N, 15 kW-class flux | +13.3 | +18.7 | corners lift 13-19 um: PCM ~0.5 K, LM 0.1 K |
| Product 880 N | +8.8 | +18.7 | - |

**Die-face form rule (adds to core 1 / M11):** flatness 0.020 over the 108 x 108 projection, measured at 20 C, with the centre **low** (concave) by 0 to 10 um permitted and convex form not permitted; the T3 "crowned pedestal" of the architecture is deleted for T1/T2 (the thermal bow supplies the crown in operation). For the TTV plates the fly-cut target is 5 um concave. E1/E3 verify by a pressurised, heated flatness scan on the first five plates (O-M2).

### 7.4 Differential in-plane expansion, 20 -> 85 C over 108 mm (copper 17.0 ppm/K)

| Counterface | alpha (ppm/K) | Free slip edge-to-edge (um) | Per side (um) | TIM shear strain at 25 um BLT | Note |
|---|---:|---:|---:|---:|---|
| AlN tile TTV | 4.5 | 87.8 | 43.9 | 1.75 | PCM re-wets; paste pumps out in 1e2-1e3 cycles (report paste as BOL only) |
| Si bare die (33 mm die) | 2.6 | 101 over 108; 31 over a 33 mm die | 15.5 per die side | 0.6 | LM or PCM only (T3) |
| Cu-block TTV-100 | 17.0 | 0 | 0 | 0 | - |
| Organic substrate (CoWoS-L eff.) | 12 | 35 | 17.6 | 0.70 | lidded Cu lid matches the plate |
| 17-4PH frame vs plate | 10.8 | 43 | 22 | - | frame lands slide 22 um on the cap: dry, Ra 0.8, no fretting concern at 2 MPa |

The plate is not bonded to any counterface, so no bimetal plate-package bow arises; the TIM takes the slip. Reflowed-solder TIM2 on a copper plate is excluded for this reason (gap-tim2 §5).

## 8. HBM stepped pedestal (T3 bare-die SKUs; PRISM-G-D)

| Item | Specification | Tolerance | Basis |
|---|---|---|---|
| Definition | S = (die top) - (HBM top) of the package, signed; plate face: die zone(s) at z = 0, HBM zone at z = -S (pedestal proud toward a lower HBM) | S 0 to 0.40 per package (Rubin report: expect 0 to +-0.15, sign not guaranteed) | architecture 3.5; gap-rubin §7.2 |
| Base thickness | under the die 0.85 (0.80 min) always; under the HBM 0.85 + S (thicker: fine at 20-80 W/cm2) | base min 0.80 | core base_t |
| Negative S (HBM proud) | allowed to |S| <= 0.05 by pocketing the HBM zone (base 0.80 under HBM); beyond that the whole root plane is raised by |S| (die base 0.85 + |S|, +0.7 K per 0.25 mm) | - | pressure boundary (one unbonded strip at 0.45 mm base collapses at proof) |
| Die-zone pocket outline | die block outline + 0.50 per side, corner R0.5, wall 90 deg | +-0.05 position to the ear-hole datums | core hbm_pedestal_variant edge rule; nonuniform-heatmap: >= 0.5 clearance to the die edge |
| Step height S | S | **+-0.05** (task; core process target +-0.02 for S <= 0.2) | measured at 9 points per zone by CMM/confocal |
| Flatness | 0.010 per die pocket; 0.020 over each HBM pedestal; 0.020 overall | - | core die_face |
| Fly-cut sequence | post-braze: (1) fly-cut the whole face to the HBM plane z = -S (removal 1.20 - S of the 2.0 skive base); (2) pocket the die zones by S to z = 0 with a Ø10-16 PCD end mill, 0.05 finishing pass; (3) deburr the step edge R <= 0.1; (4) flatness map | removal set by probing the rim (datum A') | core 2 fly-cut allowance 1.20 |
| HBM compliant TIM | PCM pad or Ga-free putty 0.05-0.10 BLT (R'' ~0.28 cm2K/W with 0.1 mm paste-class; indium 0.06); never a gap-filler pad above 15-20 W/cm2 | BLT 0.05-0.10 | nonuniform-heatmap §5 |
| Load sharing | HBM pedestal carries only the compliant-TIM reaction (<= 0.05 MPa at 0.1 mm compression); die pressure 0.15-0.35 MPa from the kit | - | section 5 |
| Finish | T3: 3-5 um electrolytic Ni on the face only (both zones), no Au; LM dam around the die pocket per architecture 7.5 | - | architecture 2.3 |

## 9. PRISM-G variant envelope (GPU-class, 110 x 120 field; `grate` lane example ART-G-EX-A: 17 lines, L 5.5 die / 11 HBM)

| Item | PRISM-G value | Basis |
|---|---|---|
| Field, body | 110 (x, fin length) x 120 (y); body 127 x 137, corner R2 (border 8.5 as PRISM-15) | core border rule |
| Fins, kerfs | 400 fins at 0.30; 15 interior kerfs at x = 0, +-5.5, +-11, +-16.5, +-22, +-27.5, +-33, +-44 (same count as PRISM-15: arbor re-spaced), edge channels at +-55 | grate PRISM-G example |
| Grate / separator outline | 124.6 x 134.6 (grate lane assumption; resolve with IR-M4) | params-grate |
| Height at the bar | 19.1 (separator top 12.10 + 6.0 arches + 1.0 cap); 17.1 over the lands | architecture ~19-21; cap lane |
| Ports | 2 x 316L stubs Ø10 bore, OD 12, horizontal, both out of the +y end, axes z 12.0, inside a drawn port box y 68.5-85, |x| <= 35, z 6-19.1; UQD04/06 hoses | architecture 2.3, 5.6 |
| Ears, screws | 8 at (+-40, +-72) and (+-68, +-45), Ø4.50; same CSS-15P / SPR-60 / SPR-110 set; Ls_P re-cut for the module stack (NDA) | this lane |
| Frame LF-G | lands on the cap at y = +-(62.8..65.5) over the end frames (3-5.5 mm outside the field); window 124.6 x 125; port box clears the +y member via a 70 x 14 notch | section 4 |
| Backplate | the module's own bolster/backplate if one exists; else BP-G 0.8 mm 301 130 x 140 with 8 STD-8 | NDA |
| Mass, plate only | 1,148 g all-Cu, 1,030 g with the 0.6 mm 316L separator (scale 1.114 of the Rev A lanes, cap 0.85x for the 6 mm arches) vs the 0.9 kg limit: **not met** (Deviation D-M3) | `mech_calc.out` §10 |
| Which parts change | core (blank, kerf arbor spacing, ears, pedestal program), GRT-L (17 windows, 8 recesses), GRT-W (ART-G), PLN-C (new fold tool; see O-G2), PLN-F (130.7 long), separator (outline, 17 x windows), cap (6 mm arches, port boxes, stubs), LF-G, BP-G. **Unchanged:** CSS-15P, springs, sleeves, clips, washers, STD-8, guard screen, process chain, test cell | architecture 2.3 "only the artwork changes" holds for the grate web; the fold tool and cap are per pitch family |
| O-G2 (to grate/plenum lanes) | at 11 mm pitch the inside channel is 10.2 wide and the 1.8 separator reaches ~72 MPa at design burst (32.8 x (10.2/6.9)^2): PRISM-G needs a uniform 5.5 mm fold (21 walls) with un-orificed HBM-zone channels, or 2.5 mm separator, or mid-span dummy walls | architecture 5.2 allowable 40 |

## 10. Handling, shipping, poka-yoke

| Item | Specification |
|---|---|
| Handling datums | ear holes E1 (-40, -66) and E4 (+40, +66) take Ø4.45 g6 fixture pins (handling jigs, fly-cut and inspection fixtures); body edges B/C for the TTV carrier; the die face is never a fixture datum after lapping |
| Lift points | ears (8, by hand or jig) or the frame's two M4 points (TTV); never the stubs, never the cap arches; a plate is held by its edges only below z 1.5 |
| Face protection | HDPE snap cover 126 x 126 x 3, located on four ears, standing 0.5 off the face on the land ring; fitted at the fly-cut station, removed at TIM application; ESD-safe |
| Ports | push-on PE caps on the 20 mm stubs (0.5 bar N2 fill retained; dew point <= -40 C per architecture 5.3); tamper label across a cap |
| Orientation | tap bosses on -y at x 0 and +15.4 key the carrier pocket (6.1); ports key the hoses; the frame is 4-fold symmetric and needs no orientation; serial + flow arrow lasered on the cap flat at (-45, -45) |
| Permitted clamping surfaces in processing fixtures | rim top ring before the grate is placed (core process); after braze: the cap flat band |y| >= 56.5 and the ears; vacuum chuck on the cap flat for the fly-cut is excluded (arches), use the ear pins + land ring |
| Shipping (plates) | single-cell PE foam, face down on the cover, 20 per tray; ISTA 3A packaged test on the tray (E5) |
| Shipping (FRU mounted on a module) | SPR-110 kit mandatory (lift-off margin at 50 g, section 11) or a shipping bracket between the frame and the backplate |
| LM FRUs (T2) | shipped pre-wetted with the dam and cover, >= -10 C (architecture 7.4); no Al in the FRU: steel frame, clips, screws |

## 11. Shock and vibration envelope

| Condition | Level used for design | Basis / status |
|---|---|---|
| Operating random vibration, rack level | 0.5 g rms, 5-500 Hz, 30 min per axis | server-class practice (OCP ORv3 IT-gear and NEBS-lite usage; the ORv3 base spec table was not retrievable this session) [KB-M, confirm in E5 planning] |
| Operating shock | 10 g, 11 ms half-sine, 3 axes both directions | [KB-M] |
| NEBS GR-63-CORE office vibration | 0.1 g, 5-100 Hz sine sweep | vendor summaries of GR-63 §5.4 [KB-M] |
| NEBS GR-63-CORE Zone 4 earthquake | VERTEQII waveform, ~1.5-2 g at the frame base, SRS up to ~5 g at the top of the frame | incompliancemag GR-63 summary (searched) |
| Non-operating, packaged (ISTA 3A / ASTM D4169 DC-level) | 30-50 g at the plate inside the package (cushion-dependent); drops 0.46-0.76 m | architecture 7.6 |
| Non-operating, module-level transport | 30 g, 11 ms half-sine; 1.5 g rms random 5-500 Hz | [KB-M] |

Consequences (`mech_calc.out` §8; FRU 1.33 kg = plate 1.24 + LF-15P 0.085):

| Load | Force (N) | Downward (into the package) | Upward (lift-off) | Lateral |
|---|---:|---|---|---|
| 0.5 g rms operating | 6.5 | nothing | nothing | held by friction (mu 0.2 x 480 = 96 N) |
| 10 g operating | 130 | adds 0.03 MPa on a 33 cm2 die block, inside the window | held (480 / 880 N clamp) | slides 0.25 to the shoulders; ear bearing 2.7 MPa |
| 30 g non-op | 390 | ear stop engages after g = 0.15 (TTV) / 0.1-0.7 (product) of package compression; the stop then carries the excess | held | ear bearing 8 MPa (< 40) |
| 50 g non-op | 650 | as above | **lifts off with SPR-60** (480 N): frame rises 0.8 mm to the SLV stop, the screws carry it, the TIM opens 0.8 mm and re-closes (PCM re-flows at first power-up); **held with SPR-110** (880 N) | ear bearing 13.5 MPa |
| Spring-mass mode (plate floating on 8 springs, if the package compliance were zero) | - | 8 x 10.8 N/mm, 1.33 kg: 40 Hz (SPR-60), 56 Hz (SPR-110); in practice the plate is pressed on the package and the package/board stiffness sets the mode | - | - |

Rule: the hard stops carry inertial loads in both directions beyond the clamp window (M5): downward through the ear-to-boss stop, upward through the sleeve stop; the package never sees more than clamp + the stop gap's elastic share. Vibration fatigue of the springs is nil (operating amplitude < 0.01 mm). The 2.0 mm plate body edges are not loaded. E5 runs the ISTA sequence and the orientation tests (0/90/180 deg) with the SPR-60 and SPR-110 kits and inspects the TIM print after each.

## 12. Mass budget (g; lane values where they exist)

| Part | Mass | Basis |
|---|---:|---|
| Core (base, fins, rim, ears, bosses) | 282.0 | params-core |
| Grate GRT-L + GRT-W | 201.0 | params-grate |
| Plenum PLN-C + 2 PLN-F | 161.6 | plenum_sep_data |
| Separator 1.80 Cu | 173.7 | plenum_sep_data |
| Cap (drawn 1.0, skirt, 6 arches, 2 port pockets, 2 brazed 20 mm bosses) | 250.0 | allocation = architecture 5.1 (mass_height.out lean 176 excludes the skirt) |
| Stubs 2 x 316L 20 ID x 1.0 x 30 | 31.5 | this lane |
| Guard screen + radial diffuser | 10.0 | this lane |
| 8 x CSS-15P | 42.5 | Ø4 x 40.4 + head |
| 8 x SPR-60 | 18.2 | §9 |
| 8 x SLV-P + WSH-8 + e-clip | 19.7 | §9 |
| Backplate BP-15P 0.8 mm 301, 118 sq, Ø60 hole | 70.1 | §9 |
| 8 x STD-8 | 17.5 | §9 |
| **Total, architecture boundary (no load frame)** | **1,277.8** | target 1,240 (+38 g, D-M1); limit 1,400 |
| + LF-15P product frame | 85.0 -> 1,362.8 | <= 1,400 SKU limit |
| Option: 0.6 mm 316L separator | -105.7 -> 1,172 / 1,257 | architecture stretch |
| TTV fixture (not in the plate mass): LF-15T Al 0.46 kg, steel 1.34 kg; carrier 3.9 kg | - | section 4 |

## 13. Interfaces: requests to the other lanes

| ID | Lane | Request | Consequence if refused |
|---|---|---|---|
| IR-M1 | core | make the ear hole Ø4.50 +0.10/-0 the default (core 3.8 lists it as the M4 option); position Ø0.10 kept | a Ø3.0 shoulder / M2.5 screw set (clamp per screw <= 150 N; TTV needs 10 screws) |
| IR-M2 | cap | flat lands on the cap top at |y| 56.5-59.7, x -60..+60, z 13.10 +-0.10, flat 0.05, coplanar 0.08; no arch, pocket or emboss at |y| >= 56.0; skirt-corner inside radius <= 1.0; inlet arches end at |x| <= 52, outlet arches at |x| <= 58.8; port-boss flanges <= Ø26 inside |x| <= 50, -40 <= y <= 50 | +y land shrinks to 1.7 mm (bearing 4.9 MPa, still < 40) or the frame moves to 4-side bearing on a cap land ring that the arch ends do not allow |
| IR-M3 | plenum/separator (and cap) | move the outlet windows from y = +9/+23/+37/+51 to +7/+21/+35/+49 so the last outlet arch ends at y <= 55.5 and the +y land equals the -y one; re-run `plenum_sep.py` (expected per-orifice max/min change < 0.005) | +y land 1.7 mm wide (IR-M2 consequence) |
| IR-M4 | grate, plenum, cap, core | resolve the outline conflict: core rim lap face 121.4 (skirt inner 60.7, outer 61.7) vs grate/separator outline 122.6 and plenum flange edge 120.7; this lane assumes the core (skirt outer 61.7, body edge exposed 0.8) and a 123 +-0.3 cap | handling cover and carrier pocket re-dimensioned; no effect on the frame (it bears on the cap top) |
| IR-M5 | core | die-face form rule 7.3 (concave 0-10 um allowed, convex not); TTV plates fly-cut to 5 um concave | corners lift 19-32 um hot: +0.5-1 K on PCM/paste maxima |
| IR-M6 | cap | the -T dP-tap stubs and the two 20 mm bosses stay inside the frame window; cap flat at (-45, -45) for marking | - |
| IR-M7 | grate (PRISM-G) | O-G2: uniform 5.5 mm fold or separator stiffening for the 11 mm HBM pitch | PRISM-G separator over-stressed at burst |

## 14. Deviations from the architecture of record

| ID | Architecture | This lane | Reason | Consequence |
|---|---|---|---|---|
| D-M1 | mass 1.24 kg (plate + stubs + springs + backplate) | 1.278 kg on the same boundary | the 8-screw set with Ø4 shoulders and stop sleeves weighs 80 g, the 1.8 mm separator +35 g; cap allocated at 250 g | +38 g (3 %); within the 1.4 kg SKU limit; 316L separator recovers -106 g |
| D-M2 | "no load frame" boundary; frame 0.3-0.6 kg implied only for the TTV | a product load frame LF-15P (85 g) is mandatory on every package mount because the ears cannot carry springs | ear stress 47-195 MPa | FRU 1.36 kg; cost +US$2-3 (stamping) |
| D-M3 | PRISM-G <= 0.9 kg plate only | 1.03-1.15 kg by scaling Rev A | the 127 x 137 body and the stack thicknesses do not scale down | limit to be restated (~1.05 kg with the 316L separator) or the border trimmed (8.5 -> 7.0 saves ~60 g) |
| D-M4 | bow under the 2 kN TTV clamp "measured, not assumed" | closed-form 22.6 um concave (2-side) with the thermal bow 18.7 um convex cancelling in operation; form rule IR-M5 | - | E1 FEA and the heated flatness scan remain the verification (O-M2) |
| D-M5 | HBM step "+-0.05, pedestal cut in the same fly-cut"; core lane 0-0.2 +-0.02 | S 0-0.40 signed, +-0.05 (core target +-0.02 for S <= 0.2); negative S beyond 0.05 raises the whole root plane | HBM4 may sit flush or proud | +0.7 K per 0.25 mm of raised root on such packages |
| D-M6 | T3 "crowned pedestal" | deleted for T1/T2; T3 die pockets flat 0.010 | the hot base supplies 19-32 um of convexity by itself | - |

## 15. Open items and the tests that close them

| ID | Item | Closes at |
|---|---|---|
| O-M1 | DIE-TTV rate (34 N/mm +-10 % estimated from the 89 mm catalogue value): measure 8 springs; adjust Ls_T or the carrier step so that 8 x F = 2,011 +-40 N | E3 rig build |
| O-M2 | Clamp + thermal bow: FEA of the frame/plate at 0.48, 0.88 and 2.0 kN with the real cap; heated pressurised flatness scan on 5 plates; decide 2-side vs 4-side bearing and the concave pre-form value | E1 (M2), E3 (M4) |
| O-M3 | Shock/vibration levels: pull the ORv3 base spec, OCP cold-plate qualification white paper and GR-63-CORE tables; replace the [KB-M] rows of section 11 | E5 planning (M5) |
| O-M4 | 2.8 mm ears as a frame-less option for LM SKUs (<= 110 N per screw) | G1 cost review |
| O-M5 | Hook-tab lip at z -0.6 vs board keep-outs on real modules (NDA guides) | first customer ICD |
| O-M6 | Carrier boss / standoff top as the ear stop: verify no contact at the minimum gap (0.10) across the package height band; else move to a shim-set gap | E3, first module fit |
| O-M7 | TC layout inference (centre + outer-edge per heater): confirm against CoolIT's TTV when a plate is purchased (E0) and against OCP spec §5.2 | E0, R5 (M1) |
| O-M8 | PRISM-G port-box geometry and 1U stack (horizontal Ø10 stubs at z 12) with the cap lane | PRISM-G design start |

## 16. Files

| File | Content |
|---|---|
| `mech_calc.py` / `mech_calc.out` / `mech_calc_data.json` | force budget, ear stress, spring design, screw stacks and stress, frame stiffness, sandwich EI, clamp and thermal bow, expansion slip, shock loads, mass budget, PRISM-G envelope |
| `params-mech.json` | screw positions and set, frame LF-15T / LF-15P, backplate and standoffs, TTV carrier and TC positions, pedestal, PRISM-G, bow, shock, mass |
