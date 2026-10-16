# Manifold maldistribution and pressure drop of the two-level HMMC cold plate

Key `manifold-maldistribution`. Script `manifold-maldistribution.py`; full tables in `manifold-maldistribution.out.txt`. 108 x 108 mm, PG25 at 50 C, 18 and 36 LPM.

## 1. Bottom line

As specified (0.3-0.5 mm slots at 4 mm pitch, 4x8 mm headers) the manifold does not work: slots run at 9 m/s, a 43 kPa dynamic head against a 0.7 kPa channel resistance, and the model predicts flow reversal along the slots. Taper does not fix it. Three changes do: (i) make the channel branch the dominant resistance (2-3 kPa at 18 LPM) via 4 mm flow length and 0.075 mm gaps; (ii) feed and collect every slot at mid-length from two side-by-side headers on the plate centre line (centre inlet like CoolIT, but U-type at both levels); (iii) size for <= 1 m/s in headers and <= 0.5 m/s at slot entries. Design H then gives global max/min 1.10, 5.0 kPa port-to-port at 18 LPM (15.5 kPa at 36), all velocities <= 1.5 m/s, and a 0.3 K caloric hot-spot penalty.

## 2. Method and assumptions

Nested 1-D manifold network:

- Level 3 branch (per 2 mm slot segment): descent through the opening into the fin gaps (K = 1 + 0.5(1-phi), phi = b/(b+t)), laminar friction over L_ch = P/2 with Darcy f Re = 96(1 - 1.3553a + ...) (85 at aspect 0.1, i.e. 4 x Fanning 21), two 90-degree turns K = 1, ascent K = 1 + (1-phi)^2; dp = R1 q + R2 q^2.
- Level 2: inlet slot = dividing manifold, return slot = combining manifold, 54 nodes (27 per half slot). Static pressure marches by p_(k+1) = p_k + theta_d rho(u_k^2 - u_(k+1)^2)/2 - f(dL/Dh) rho u^2/2, theta_d = 1 (Bernoulli recovery); combining mirror with theta_c = 2 (zero axial momentum of entering flow). f laminar rectangular / Blasius, blended 2300-4000. Branch flows q_k = branch^-1(p_in,k - p_out,k + D), D by Brent so sum q = Q, relaxed fixed point.
- Level 1: same solver, 27 (or 14) branches with the fitted slot-pair law plus tee losses. Configs: U (both headers on one edge), Z (opposite edges), C (centre inlet header, two edge outlet headers), CC (inlet and outlet headers side by side on the centre line).
- Global max/min = slot-to-slot x along-slot of the extreme slots (conservative). Starved-segment penalty (single pass): dT_hot = 0.5 dT_out (1/phi_min - 1).
- Ports: bore velocity with 2 turns + expansion/contraction. UQD pair by Cv law; Cv values are estimates (+/-50 %), no datasheet could be fetched this turn.

Uncertainty: theta_d 0.6-1.3, theta_c 1-2.5 move the recommended design's global max/min between 1.06 and 1.15; K at channel Re 10-20 is +/-100 % but only toward more branch resistance. Treat dp as +/-30 %, ratios +/-0.05.

## 3. Results

### 3.1 Branch resistance (18 LPM, P = 4 mm, 27 inlet slots)

Gap 0.05 / 0.075 / 0.10 / 0.15 mm (H = 1 mm, 0.4 mm openings): 1.6 / 0.92 / 0.67 / 0.50 kPa per segment; channel velocity 0.10 m/s, Re 15, independent of gap at fin = gap. Side finding: `coldplate_model.py` puts the Fanning f Re in the Darcy formula and under-predicts channel friction 4x. Immaterial for HMMC (0.3 kPa), but the CoolIT-like reconstruction becomes ~19 kPa (not 9) and the "0.1 mm fins, 54 mm split-flow" row ~140 kPa (not 35).

### 3.2 Along-slot (Level 2), q_slot = 0.667 LPM

| slot w x d mm | opening | feed | u_s0 m/s | dp_br / q_dyn | max/min | phi_min | dT_hot K |
|---|---|---|---:|---:|---:|---:|---:|
| 0.4 x 3 (as specified) | 0.4 | U or Z | 9.3 | 0.02 | back-flow | - | - |
| 0.4 x 3 | 0.4 | centre-fed | 4.6 | 0.06 | 32 | 0.21 | 24 |
| 1.5 x 6 | 0.4 | U | 1.23 | 0.9 | 3.3 | 0.58 | 4.7 |
| 1.5 x 6 | 0.4 | Z | 1.23 | 0.9 | 3.8 | 0.57 | 4.8 |
| 1.5 x 6 | 0.4 | CC (U halves) | 0.62 | 3.5 | 1.46 | 0.86 | 1.0 |
| 1.5 x 6 | 0.15 orifice | CC | 0.62 | 14 | 1.09 | 0.97 | 0.2 |
| 3.5 x 8, P = 8, 0.075 gaps | open | CC | 0.39 | 32 | 1.05 | 0.95 | 0.3 |

Mechanism (1.5 x 6, U): the inlet slot recovers +0.77 kPa toward its dead end while the return slot loses 1.53 kPa of momentum plus 0.4 kPa friction toward its exit, so the fed end gets 1.9x and the far end 0.6x the mean. Inlet-slot taper (area ratio 0.5-0.3) changes max/min by < 0.1 for U and C and helps only Z (3.8 -> 2.9): friction and recovery are the same order, so no taper cancels both. Centre feeding quarters both terms, which is why CC beats any taper.

### 3.3 Slot-to-slot (Level 1), 18 LPM, slots 1.5 x 6

| header mm | u_h0 m/s (centre-fed) | U | Z | C | CC |
|---|---:|---:|---:|---:|---:|
| 4 x 8 | 9.4 (4.7) | 17 | back-flow | 5.2 | 10 |
| 6 x 10 | 5.0 (2.5) | 3.4 (3.1 tapered) | 16 (5.6 tapered) | 1.70 | 2.6 |
| 8 x 12 | 3.1 (1.6) | 1.78 | 4.2 | 1.22 | 1.55 |
| 10 x 15 | 2.0 (1.0) | 1.29 | 1.83 | 1.08 | 1.21 |
| 12 x 20 | 1.25 (0.62) | 1.11 | 1.28 | 1.03 | 1.08 |

Header taper 0.5 helps Z strongly and U/C by < 10 %. At 36 LPM the ratios are nearly unchanged at ~4x the dp (Level-1 law is quadratic-dominated).

### 3.4 Design rule (continuous header-area scan)

Slot-to-slot max/min <= 1.10 needs dp_branch / (rho u_feed^2/2) >= 6 (U or CC), >= 14 (Z), >= 3 (C, whose outlet headers carry Q/4). For the laminar Level-2 branch (exponent 1, flow error = pressure error) the along-slot need is >= 15 for centre-fed half slots, >= 30 for single-end full-length slots. For a 2.5-3 kPa branch at 18 LPM this means header <= 1.0 m/s (>= 150 mm^2 per centre-fed half) and slot entry <= 0.5 m/s (>= 22 mm^2 per slot). Total header area / total slot-entry area came out 0.9-3.1 across every design that passed, so the area ratio alone is not the criterion; the dynamic-head ratio is.

### 3.5 Channel width and pitch (CC, 10x15 header)

At P = 4 mm with 1.5 x 6 slots, gap 0.05 / 0.075 / 0.10 / 0.15 mm gives global 1.42 / 1.63 / 1.76 / 1.90 at 8.9 / 8.2 / 7.9 / 7.8 kPa: finer gaps help (friction ~ 1/b^2) but nothing at 4 mm pitch reaches 1.10 without a 0.15 mm orifice lip (then 5.5-5.8 kPa, 1.08-1.10, but a 150 um feature and 1.5 m/s jets). Pitch 4 / 6 / 8 / 12 mm (0.075 x 1.0 fins, open slots P/2 - 0.5 wide, 6 mm deep) gives global 2.24 / 1.42 / 1.24 / 1.12 at 7.9 / 8.3 / 9.1 / 12.2 kPa. Channel friction scales with L^2 while the entrance-dominated Nusselt number is unchanged (x* invariant with L at fixed fin geometry), so 4-6 mm flow length buys robustness for 2-4 kPa.

### 3.6 Recommended design H and budget

P = 8 mm (14 + 14 slots), fins 0.075/0.075 x 1.0 mm, slots 3.5 x 8 mm open-bottom, inlet header 10 x 15 and outlet header 14 x 20 mm side by side on the centre line, centre ports, 16 mm bores.

| Pa | 18 LPM | 36 LPM | | 18 LPM | 36 LPM |
|---|---:|---:|---|---:|---:|
| ports (bore, turns) | 2525 | 10099 | L3 channel friction | 2222 | 4445 |
| L1 headers (net) | -188 | -763 | L3 openings + turns | 56 | 222 |
| L1-L2 tees | 236 | 947 | **plate port-to-port** | **4988** | **15469** |
| L2 slots (net) | 107 | 365 | UQD08-class pair (est.) | 25000 | 100000 |
| global max/min | 1.10 | 1.18 | phi_min / dT_hot | 0.95 / 0.3 K | 0.92 / 0.3 K |

Velocities at 18 LPM: port 1.5, header 1.0, slot entry 0.4, between-fin descent 0.12, channel 0.21 m/s, all under the 2 m/s Cu/Ni erosion rule of thumb (3 m/s local cap). At 36 LPM only the 16 mm ports (3.0) and header (2.0) exceed 2 m/s; design I (20 mm ports, 14x20 / 20x25 headers, 10 mm slots) gives 9.4 kPa, global 1.08, <= 1.9 m/s. Plate pump power 1.5 W at 18 LPM. Flow sweep of H: global 1.06 (9 LPM) -> 1.10 (18) -> 1.18 (36), because the laminar branch grows ~Q and manifold terms ~Q^2; the caloric penalty stays 0.3 K since dT_out falls with flow.

### 3.7 Realistic dp claim

Model 5 kPa at 18 LPM; claim **<= 10 kPa port-to-port at 18 LPM, <= 25 kPa at 36 LPM** to cover CFD/test discovery. Couplings dominate the loop: UQD08-class pair ~25 kPa at 18 LPM by Cv estimate, UQD06 ~100 kPa; specify 3/4 in barbs or UQD12-class (~5 kPa) or dual UQD08 ports. "20-40 kPa at 1.5-2 LPM" for GPU plates could not be verified this turn. Against the corrected ~19 kPa skived split-flow reconstruction, a 5-10 kPa HMMC plate is a 2-4x advantage, not 6 vs 9 kPa.

## 4. Design rules

1. Branch dominates: dp_branch at design flow >= 6x the header-inlet dynamic head (U/CC) and >= 15x the slot-entry dynamic head (centre-fed slots); Z-type needs 2-3x more. Check at maximum rated flow.
2. Centre-feed and centre-collect: both Level-1 headers on the centre line, every slot fed and drained at mid-length. Opposite-edge (Z) layouts are 2-5x worse and the only case where taper pays.
3. Velocity caps at 18 LPM: ports <= 1.5 m/s (>= 16 mm bore), headers <= 1.0 m/s, slot entry <= 0.5 m/s, opening descent <= 0.5 m/s; scale areas with flow.
4. Outlet header area 1.5-2x the inlet header (combining losses are ~2x dividing recovery).
5. Prefer 8 mm slot pitch (4 mm flow length) with 0.075 mm gaps and open slot bottoms; if pitch must stay 4 mm, a 0.15 mm orifice lip is mandatory.
6. Do not rely on taper for U/C/CC manifolds (< 0.1 change).
7. Manifold block adds ~25 mm height (8 mm slots + 15-20 mm headers + walls).

## 5. Findings that bear on the architecture

- The slot and header dimensions in the current HMMC definition are not viable at 18 LPM; the manifold must be ~10x larger in cross-section and the plate ~25 mm thick. The architecture must carry this packaging statement.
- The 2 mm flow length is not a thermal requirement; 4 mm is the better hydraulic choice. Hand to the thermal check: base-temperature ripple over an 8 mm period and the gap-tolerance sensitivity (dp ~ 1/b^2, so +/-10 % gap = -/+20 % local flow).
- Uniformity of the laminar design degrades with flow (1.10 at 18, 1.18 at 36 LPM); thermally negligible (0.3 K), but any "< 10 %" claim should be tied to 18 LPM or an orifice-regulated variant.
- Momentum-coefficient uncertainty spans global 1.06-1.15; a CFD or water-table test of one slot pair is the cheapest way to pin theta_c.
- Quick disconnects, not the plate, set the loop pressure drop at 18 LPM; the spec must name the coupling class.
