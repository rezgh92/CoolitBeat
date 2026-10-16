# base-stress-stiffness: mechanical feasibility of a 0.8-1.0 mm Cu base under an HMMC manifold stack

Script: `docs/cooling/appendix/physics/base-stress-stiffness.py` (numpy, closed-form Roark/Timoshenko plate and sandwich theory; not FEA).

## 1. Question

The HMMC candidate (0.1 mm Cu fins / 0.1 mm gaps, 1.0 mm tall, 1.0 mm base, etched Cu manifold 1.5-2 mm, cover 2-3 mm) halves the base thickness of the CoolIT-like skived plate (2 mm base, 0.2/0.2 x 4 mm fins, ~3 mm cover). Does a 1 mm base survive pressure (operating 0.1-0.3 MPa, proof 2x, burst 3x = 1.5 MPa upper envelope), mounting (130-450 N), thermal cycling and handling, and what construction makes it work?

## 2. Loads, materials, assumptions

- Pressure: 0.3 MPa max operating, 0.6 MPa proof, **1.5 MPa burst** (upper end of OCP/Nvidia-type asks; the WebSearch budget was exhausted this run, so this is the task's envelope, not re-verified; published OCP MOPs I recall are 2-3.5 bar, so 1.5 MPa is conservative).
- Mounting force 130/300/450 N at four corner bolts, reacted by the die at the centre; die flatness/bow budget 25-50 um.
- OFHC Cu: E 117 GPa, nu 0.34, CTE 16.5 ppm/K. **Annealed** values (yield 70, UTS 220, endurance ~70 MPa) are used everywhere because brazing or diffusion bonding anneals the whole plate; half-hard (250/300 MPa) only for cold-joined builds. Braze lap-shear 100-200 MPa, Cu-Cu diffusion bond ~180 MPa. From memory, +/-25 %.
- Geometry: 108 x 108 mm wetted/heated span; HMMC manifold layer 1.75 mm at 60 % solid fraction; one 0.3 mm slot every 2 mm so 85 % of each fin tip is bonded to a manifold web; manifold-to-cover bonded over 50 % (headers 6 mm wide); 4 mm perimeter seal land where the base is not backed by fins.

Equations: fixed strip sigma = p b^2/(2 t^2), w = p b^4/(384 D); clamped square plate w = 0.00126 p a^4/D, M = 0.0513 p a^2; SS plate with central load w = 0.0116 P a^2/D, corner-supported ~6.1x (+/-30 %); layered D = sum E_i (I_i + A_i d_i^2)/(1-nu^2), fin layer carrying membrane stress only along fins, core shear G_c = E t^3/(H^2 p) across fins; tie stress = p pitch/(t_fin f_bond); Timoshenko bimetal curvature for the hot base on the cold stack.

## 3. Results

| quantity (108 mm plate, 1.5 MPa burst unless noted) | CoolIT-like skived, 2 mm base, free fin tips | HMMC tied sandwich, 1.0 mm base |
|---|---:|---:|
| base stress between fins (fixed strip) | 0.04 MPa (0.2 mm gap) | **0.0075 MPa**, w = 4e-8 um (SF > 9000) |
| base stress over 0.3 mm slot (fins continuous) | n/a | 0.07 MPa |
| base stress over 4 mm perimeter land | ~3 MPa (2 mm) | 12 MPa (SF 5.8 yield, 18 UTS) |
| fin / fin-tip-bond tie stress | fins untied | 3.0 / **3.5 MPa**; operating 0.7 MPa |
| tie SF at burst | - | 20 (annealed yield), 28-57 (braze shear), 51 (diffusion bond); with Kt 2.5 and only 30 % bonded area still 2.8 |
| burst ladder | ribbed base yields 0.58 / ruptures 1.8 MPa; 3 mm cover yields 0.18 / ruptures 0.55 MPa | fins 94 MPa, braze 43 MPa, cover over 6 mm header 24 MPa, **4 mm land 8.8 MPa (yield) / 27 MPa (rupture)** |
| perimeter seam shear (3 mm braze) at burst | 13.5 MPa (seam carries p x cavity) | 2.0 MPa (seam carries land strip only) |
| effective D, N.m per m | 379 base alone (1632 along fins / 88 across); 677 with cover in parallel | **2119** (2456 / 2208, 17 % shear knock-down across fins) = 6.0 mm solid-equivalent |
| stiffness ratio | 1 | 24x plain 2 mm plate, 6x skived base, 3.1x skived base+cover |
| global base bow under 0.3 MPa operating | 0.14 mm (ribbed base), cover 0.17 mm; at 1.5 MPa 0.68 mm, base stress 182 MPa | **0** (ties make p self-equilibrated; only land strip bends, 0.09 um) |
| mounting bow, 300 N, full span (SS edges .. corner bolts) | 60 .. 366 um | 19 .. 117 um |
| bow over 50 mm die (x0.21) | 13 .. 77 um | **4 .. 25 um** (spec 25-50) |
| thermal bow (hot base vs cold stack), 50 mm die / 108 mm | 19 / 89 um | **6 / 28 um** |
| in-plane thermal constraint stress in base | 14 MPa | 22 MPa (fatigue amplitude 11 MPa, SF ~6) |
| pressure-cycle fatigue | - | amplitude 0.35 MPa, SF ~200 |
| creep | 0.24-0.26 Tm, < 25 MPa: negligible for both | same |
| fin buckling under mount compression | - | 2.2 GPa critical vs 0.08 MPa applied |
| mass over footprint / thickness | 0.73 kg / 9.0 mm | 0.53 kg / 6.25 mm |

Key points behind the table:

1. **Between fins the 1 mm base is irrelevant to pressure.** With a 0.1 mm gap the fixed-strip stress is 7.5 kPa at 1.5 MPa burst; even a 0.5 mm base only reaches 30 kPa. Pressure alone would permit a base < 0.5 mm.
2. **The base is safe only because the fins are ties.** An untied 1 mm Cu plate spanning a 108 mm cavity sees 5.4 GPa and 23 mm bow at 1.5 MPa (1.1 GPa / 4.7 mm even at 0.3 MPa). For an untied base the admissible unsupported square span at 1.5 MPa is 12 mm (yield) / 22 mm (rupture) for 1 mm, 25 / 44 mm for 2 mm, 37 / 66 mm for 3 mm; an unsupported 108 mm cavity would need an 8.8 mm (yield) or 4.9 mm (rupture) plate. Bonding every fin tip to the manifold web (0.2 mm support pitch) turns the stack into a brazed plate-fin vessel: the tie stress is p x pitch/t_fin = 2p, i.e. 3 MPa at burst, and the computed burst limit moves to the perimeter land (8.8 MPa yield, 27 MPa rupture), 6-18x above 1.5 MPa. The perimeter seam load also drops 7x because the seam no longer carries p x cavity area.
3. **Side finding on the benchmark.** The CoolIT-like reconstruction (2 mm base, 4 mm free fins, 3 mm cover) cannot pass 1.5 MPa over a 108 mm cavity: the ribbed base is above yield (182 MPa) and the 3 mm cover yields at 0.18 MPa. The real CoolIT plate therefore has internal posts, fin tips soldered/brazed to the lid, or thicker walls. This does not change the thermal comparison, but the "2 mm base" in our reconstruction is probably the thermal-optimistic end for them.
4. **Pressure crowning dominates TIM contact in untied plates.** At 0.3 MPa the pressure force on a 117 cm2 base is 3.5 kN, 12x a 300 N mounting load; mean TIM pressure from 300 N over a 50 mm die is 0.12 MPa versus 0.3 MPa pushing the base outward. An untied 2 mm ribbed base bows 0.14 mm at operating pressure, so its bond line is set by coolant pressure, not by the mount. The tied sandwich has zero pressure bow, which is a direct thermal benefit (uniform BLT) in addition to the thinner base.
5. **Mounting and thermal bow favour the sandwich by 3x.** With corner bolts and 300 N, the sandwich upper bound is 25 um over a 50 mm die (at the tight end of the 25-50 um spec); the skived plate is 77 um. Thermal bow (hot base constrained by the cold stack) is 6 um vs 19 um over the die because the thin base runs only ~9 K above the stack and is 1/6 of the section. The price is a higher in-plane constraint stress in the thin base (22 vs 14 MPa), a fatigue amplitude of ~11 MPa against a ~70 MPa endurance limit: acceptable (SF ~6) but it must be covered by a power-cycling test, not just by calculation.
6. **Direct-to-die variant.** Cu-vs-Si mismatch gives 14-21 um relative edge displacement over a 50 mm die for 40-60 K; the 6 mm Cu sandwich is far stiffer than the die, so a bonded TIM must be compliant (indium, liquid metal). The thin base does not help here.

## 4. Conclusion on base thickness

A 1.0 mm base is justified **only in a tied construction** (fins bonded to base and to the manifold webs, manifold bonded to cover). In that construction pressure sets no meaningful limit: 0.5 mm would still pass 1.5 MPa burst locally (SF > 2000 between fins) and the governing feature becomes the unsupported perimeter land. The practical floor is set by non-pressure items: post-bond flatness machining 0.10-0.20 mm, erosion/corrosion allowance ~0.10 mm, etch/skive tolerance ~0.05 mm, and the spreading role of the base under hotspots (thermal, not mechanical). Recommend **1.0 mm as-bonded / 0.8 mm minimum finished under the die**, with the land region kept at <= 4 mm span or locally stepped to 1.5-2 mm. Burst 1.5 MPa passes with SF 5.8 (yield-based) on the land and SF 20 on the ties; a half-hard credit is not available because bonding anneals the plate.

## 5. Design rules

1. Bond every fin tip to the manifold layer (vacuum braze or diffusion bond); treat the stack as a plate-fin pressure vessel. Target >= 50 % bonded tip area; >= 30 % still gives SF 2.8 at burst with Kt 2.5. Verify by acoustic microscopy or CT on first articles and by a burst test to >= 4.5 MPa.
2. No base span unsupported by fins or webs > 4 mm at 1 mm thickness (12 mm absolute yield limit at 1.5 MPa). Put inlet/outlet plenums over the fin field or in the cover, never directly over bare base; step the base to >= 1.5 mm under any plenum wider than 4 mm.
3. Cover spans over headers <= 6 mm for a 2.5 mm cover (24 MPa yield-based burst); manifold-to-cover bonded fraction >= 50 %.
4. Design to annealed OFHC (yield 70 MPa) after any thermal joining; credit half-hard only for solder/sinter/plated constructions.
5. Finish-machine (lap or fly-cut) the base after bonding: budget 0.1-0.2 mm, so order 1.0 mm to deliver 0.8 mm minimum; target <= 15 um flatness over the die so that mount + thermal bow (4-25 um + 6 um) stays inside 50 um.
6. Move bolt bearing points toward the die edge or use a stiff load-spreading frame; corner bolting on 108 mm consumes the full 25 um budget at 300 N even with the sandwich.
7. Keep pressure-cycle stress trivial (it is: 0.35 MPa amplitude) but qualify thermal cycling of the thin base (22 MPa constraint stress, 11 MPa amplitude) with >= 1000 power cycles.
8. Handle the etched 1 mm base/fin sub-assembly in a fixture before bonding; after bonding the 6 mm sandwich is stiffer (24x) and lighter (0.53 vs 0.73 kg) than the skived plate.

Uncertainty: stiffness +/-20 %, corner-bolt bow +/-30 %, thermal bow +/-50 %, material and braze strengths from memory +/-25 %, pressure envelope not re-verified by search this run.
