# Adversarial review: PRISM hydraulics and flow distribution

Key `hydraulics`. Reviewer lane: the dP budget (4.2), uniformity (4.3), velocities and erosion, UQD08 couplings, rack rules, and the flow trades (6.2). Date 2026-10-14.

**Method.** I re-derived the numbers independently in `appendix/verify/`:

| Script | What it checks |
|---|---|
| `hyd_budget.py` | element dP with my own K, Cd and orifice-area choices, as a low / mid / high band |
| `plenum_check.py`, `plenum_xval.py` | new along-plenum solver, with distributed window feed, turbulent friction and four momentum-coefficient sets |
| `header_net2.py`, `header_net3.py`, `header_net4.py` | new line- and segment-level network: mid-fed headers, kerf node, left/right fin segments, outlet windows |
| `loop_rack.py` | UQD08 loops from vendor Cv, the port-bore boundary, equal pumping power at two boundaries, velocity caps |
| `rack.py` | 18-tray dividing/combining rack manifold, U vs Z, mixed racks, temperature drift |

I then inspected and re-ran the draft's `plenum_prism.py`, `prism_flow.py` and `prism_model.py`. PG25 at 45-50 C is taken as ρ 1005 kg/m3 and μ 1.25 mPa·s.

## 1. Verdict summary

| Claim (draft section) | Draft | Independent value | Verdict |
|---|---|---|---|
| Plate dP, 18 LPM, 20 mm ports (4.2) | 5.9 kPa; claim ≤ 7.5 | 5.5 mid, band 4.0-7.9 | confirmed; claim is about P85 |
| Plate dP, 16 mm ports | 8.2; claim ≤ 10 | 8.3, band 6.0-11.5 | confirmed; claim can be exceeded |
| Meter orifice 0.5 x 0.9 mm, Cd 0.72, 1.37 m/s | 1.82 kPa | 1.82 if rectangular (0.45 mm2). An oblong punch is 0.396 mm2, giving 1.56 m/s and 2.35 kPa. Credible Cd at Re 700-840 and t/Dh 0.6 is 0.61-0.80 | corrected (area undefined) |
| Ports K 3.5 at 20 mm (1.60 kPa) + tees (0.80) | 2.4 kPa | 1.8-3.0; the outlet combining tee is under-counted | confirmed within ±25 % |
| Separator windows | 0.56 (table) | 0.42-0.70; the script uses 0.46, so the table sums to 5.96 while the script gives 5.86 | confirmed; internal inconsistency |
| Fin channels 0.15 x 2.0 mm, 0.15 m/s | 0.65 kPa | 0.62-0.66 (Re 34.6, Darcy fRe 87) | confirmed |
| Window, kerf and outlet turn | 0.08 kPa | 0.05-0.15, rising to 0.3-0.5 if about half the line flow descends the 0.3 mm kerf (kerf area is only 1.33x the orifice area) | unverifiable; likely low |
| Guard screen, clean | 0.30 kPa | 0.1-0.2 for square-weave 50 µm mesh. Dutch-weave or sintered-felt "absolute" media would be 1-30 kPa | confirmed only if the media is square weave |
| 82 % inertial | 0.826 | 0.826 (4.84 / 5.86) | confirmed |
| Flow sweep 4.2 / 12.4 / 21.4 kPa at 15 / 27 / 36 LPM | as stated | arithmetic exact; 36 LPM band 15.6-28.6 | confirmed; "≤ 27 kPa at 36 LPM" is marginal |
| "About 70 % lower / 3.7x" vs the reconstruction | 5.9 vs ~22 | At matched bores: 71 % (3.5x) at 20 mm, 64 % (2.8x) at 16 mm, 47 % (1.9x) at 12 mm (½-in barbs, as in CoolIT's TTV photograph). Core without ports: 4.3 vs 18.8 kPa | corrected (boundary-dependent) |
| Along-plenum max/min (4.3) | 1.065-1.085 offset; 1.04 centre mine 1.036-1.076 offset, 1.01-1.03 centre. The draft's `run()` gives 1.064-1.084 with PRISM geometry, but the filed `__main__` runs only 3 mm-plenum cases | confirmed; script not reproducible as filed |
| "A 0.9 kPa branch gives 1.3-1.5" | from `plenum_prism.py` | that result is for a 3 x 7 mm plenum at 1.29 LPM. On PRISM's 4.5 x 9 mm plenum at 2 LPM it is 1.16-1.22 | corrected |
| Slot-to-slot ratio 9.8; global ≤ 1.10 | line level | line level 1.04-1.07, or 1.09-1.13 if the port jet lands undiffused on the centre window. **Segment level 1.23-1.43 at 18 LPM and 1.41-1.71 at 36 LPM** | refuted at the fin-segment level |
| Ratios fall ≤ 13 % at 2x flow | line ratio | confirmed for lines. The segment protection term (viscous fins) halves at 2x | corrected |
| 18 plenums, 9 in / 9 out, 6,480 segments | as stated | 18 alternating lines give 17 segments per row (6,120): one edge inlet feeds one segment at 1.68x, plus two 3 mm dead-end strips over the heated area (5.6 %) | refuted (layout) |
| Fin-entry 0.41 m/s vs PSM-12's 1.32 m/s | under the 0.5 m/s cap | 0.41 m/s is an area mean; the 1.56-2.1 m/s jet travels only 1.0 mm (inside its potential core) to the fin tops, then hits the 1.0 mm base | refuted as a like-for-like comparison |
| Dead-end bleed, 0.6 mm hole, ~4 % | 4 % | 1.2 % at 2.55 kPa; 4 % needs a 1.1 mm hole | corrected |
| UQD08 pair 20-35 kPa at 18 LPM | Cv 3-4 estimate | vendor Cv: FITOK 3.65-3.76; CPC Everis ~4.75 max; Danfoss 5.32 (unconfirmed snippet). Pair dP 14-24 kPa (11 at Cv 5.3) | corrected (lower) |
| Single-UQD08 tray loop: PRISM 30-45, CoolIT-like 64-90 kPa | as stated | 40-49 and 56-79 (1 m ½-in hose, four 12 mm stubs) | corrected |
| Dual UQD08 loop 15-25 kPa | as stated | 15-18 | confirmed |
| "UQD12" not in OCP v2.0.0 | not confirmed | vendor UQD brochures (Stäubli, Danfoss, FITOK) list sizes only up to UQD08; the spec table itself was not read | confirmed (secondary) |
| 63 mm manifold or ~10 kPa orifice; U beats Z | sysplat model | my independent rack model: 1.058 (63 U), 1.136 (63 Z), 1.155 (50 U), 1.096 (50 U + orifice); matches sysplat to ±0.004 | confirmed for homogeneous racks |
| Keyed orifice only on low-dP auxiliary plates | rule | In a mixed rack, unorificed PRISM trays over-draw +10 % (single UQD08) or **+35 %** (dual UQD08), and incumbent trays lose 10-35 % (CDU flow-limited) | corrected: the rule must cover PRISM itself |
| Equal pumping power: 28.5 LPM gives 25.1 / 30.0 K | plate-only boundary | right at plate boundary. At the tray-loop boundary (single UQD08): 19.3-21.7 LPM, about 27.3-27.8 / 32.2-32.7 K. At 28.5 LPM the meter runs 2.17 m/s, over the 2.0 m/s cap | corrected |
| Flow to match 34.4 K: 11.1 LPM, outlet 65.5 C | as stated | violates the draft's own 65 C rule. The return-limited minimum is 11.2-11.4 LPM, giving 34.0-34.2 K | corrected (minor) |
| 2x flow (36 LPM) 21.4 kPa, 12.8 W; CoolIT-like 58-69 kPa | as stated | 21.4 kPa and 12.85 W are exact; CoolIT-like 58-61 (22 kPa base), up to ~90 on the 35 kPa working value | confirmed |
| Q capacity at 1.2 LPM/kW: LM 26.4, P + PCM 23.3, P + LM 34.1 kW; 25-30 kW cases | as stated | flows of 28-41 LPM. The 20 mm port exceeds 1.5 m/s above 28.3 LPM (23.6 kW); the meter exceeds 2.0 m/s above 26.2 LPM (21.9 kW, rectangular area) or 23.0 LPM (19.2 kW, oblong) | refuted against the draft's own velocity rules |

## 2. Pressure-drop budget

My mid estimate is 5.5 kPa, so the 5.9 kPa headline stands. The uncertainty sits in the meter (about 31 % of plate dP) and in the untested ports and tees (40 %).

The draft never fixes the orifice shape. "Oblong" normally means a 0.396 mm2 stadium, but the 219 mm2 total assumes a 0.45 mm2 rectangle. At Re 700-840 and t/Dh ≈ 0.6, Cd is Re-dependent (0.61-0.80) and shifts up to ±20 % with which way the punch rollover faces. With an oblong area and Cd 0.65, the meter is 2.9 kPa and the plate 7.9 kPa, which breaks the ≤ 7.5 kPa claim.

## 3. Flow distribution

**Line level.** Each inlet line is metered, so the line-level claims hold (1.04-1.08). One caveat: the centre inlet window sits directly under the 20 mm port, and an undiffused port jet raises line max/min to 1.09-1.13. The guard cylinder removes the jet only if it is specified as an inside-out radial diffuser.

**Segment level: the uniformity claim fails.** The meter sets each line's flow, not its left/right split between fin segments. Only the viscous segment resistance (0.67 kPa) governs that split. It must resist the outlet-header combining head (226 Pa x k_c ≈ 2), the outlet-window loss (about 226 Pa) and unequal edge-window flows: a protection ratio of about 1.5-3 against the draft's own rule of ≥ 6.

Segment max/min is therefore 1.23-1.43 at 18 LPM and 1.41-1.71 at 36 LPM, with the minimum segment at 0.80-0.89 of nominal. The thermal cost (+0.6-1.0 K on the starved segment) fits the 1.5 K flow-driven hot-spot budget, so it is not fatal. But E2's ≤ 1.10 criterion fails if measured per segment and misleads if measured per line.

Three fixes were modelled:

| Fix | Segment max/min at 18 / 36 LPM | dP cost |
|---|---|---|
| 0.5-1.0 kPa outlet-side orifice row | 1.07-1.10 / 1.08-1.12 | adds 0.5-1.0 kPa |
| Split the meter: 1.3 kPa inlet + 0.6 kPa outlet | 1.10 / 1.12 | none |
| Outlet header area doubled + half-area edge outlet windows | 1.07 / 1.12 | none |

**Layout error.** Eighteen alternating plenums across a 108 mm field cannot finish with outlets on both edges. As drawn:

- the inlet line at x = -51 mm has no left-hand outlet, so its whole meter flow goes into one segment at 1.68x nominal;
- the strips at x = ±(51-54) mm are dead-ended fins over the heated TTV area.

By conduction estimate (3.84 W/mm through a 1.0 mm base over about 1.5 mm), those strips run about 10-15 K above their neighbours, so a TC near the heater edge would lose the 33.3 K maximum claim. The draft's own 6,480-segment count implies the correct layout: 19 lines (9 inlets; 10 outlets, with edge outlets at ±54 mm and half-area windows). As drawn, a centre port also feeds 5 windows on one side and 4 on the other (10 / 8 LPM, not 9 / 9).

Geometry clash: headers 26 and 30 mm wide centred at ±14 mm touch at y = -1 mm with no wall between them, so the centres need to move to about ±16 mm. The inlet header's tie rib also runs under the port bore.

## 4. Velocities and erosion

Bulk velocities at 18 LPM are benign: ports 0.95, headers 0.67-0.87, windows and plenums ≤ 0.53, fins 0.154 m/s. Fin wall shear is 7.7 Pa, against about 26 Pa in CoolIT-class 0.2 mm channels, which is a real advantage. The risks are local:

1. **Meter orifices.** Mean velocity is 1.37-1.56 m/s, the vena contracta about 2.1 m/s, and inlet-edge shear about 80 Pa. At the 150 % rated flow of 22.5 LPM, the mean is 1.71-1.95 m/s.
2. **Jets onto the base.** The jets reach the fin tops and the kerf floor of the 1.0 mm base (the pressure boundary) at about 1-2 m/s. The draft's "0.41 m/s fin entry" does not answer the judges' impaction and erosion objection; the jet has only moved 1 mm upstream.
3. **Outlet-side temperature band.** The Copper Development Association guidance is 1.2-1.5 m/s for hot water below 60 C and 0.6-0.9 m/s above 60 C. At the headroom case (51.7 C inlet, about 64 C outlet), the outlet side is in the above-60 C band, so the 0.95 m/s outlet port is marginal. The 16 mm option (1.49 m/s at 18 LPM, 1.87 m/s at 22.5 LPM) fails the draft's own rule inside the OCP sweep.

## 5. Couplings

Vendor data put the UQD08 Cv per mated coupling at 3.65-4.75 (5.3 unconfirmed), so a pair costs 14-24 kPa at 18 LPM. That is lower than the draft's 20-35 kPa, which slightly helps both plates.

At 18 LPM, the coupling's 10 mm bore runs 3.8 m/s. The vendors' 5 m/s reference flow is 22.5-23.6 LPM. At 36 LPM a single pair runs 7.6 m/s and 56-96 kPa, so 2x flow and any rating above about 19 kW need dual pairs.

The dual-pair variant feeds the headers from both ends. That changes the header topology from mid-fed, and 4.3 has not analysed it.

## 6. Rack balancing and the 82 % inertial question

**Inertial dP is not a balancing defect.** It favours PRISM:

- Branch flow goes as ΔP^0.5: a 20 % header-dP drop costs PRISM 11.6 % of its flow, against 15.8 % for a CoolIT-like plate.
- Flow barely depends on viscosity: a 25 C start-up shifts flow only about 4 % toward PRISM in a mixed rack.
- With UQD08s, hose and stubs added, every branch is 75-96 % inertial anyway.

The real rack problem is **low absolute dP in a shared header**, as the mixed-rack row in section 1 shows. Restoring balance takes keyed orifices of about 20-50 kPa on the PRISM branch. That spends the plate's dP advantage, which pays only in PRISM-homogeneous racks with lower CDU head.

**A second consequence: dP cannot see fin fouling.** The fins are 11 % of plate dP and under 2 % of the tray loop. A 10 µm deposit on each wall raises fin dP 54 % but plate dP only 6 %, and it costs about 1-1.5 K. E4's "core dP drift ≤ 10 %" must therefore use taps across the fin field (inlet plenum to outlet plenum), not port to port.

## 7. Fatal issues (as written)

1. **The 18-plenum layout is inconsistent with the 6,480-segment count.** As drawn, it leaves 3 mm dead-end fin strips over the heated area at both edges (estimated +10-15 K locally) and an edge inlet line dumping 1.68x into one segment. If built as specified, the maximum-temperature claim is exposed. It is trivially fixable with 19 lines.
2. **The published Q-capacity figures exceed the draft's own velocity caps** (LM 26.4 kW, P-grade 23.3 / 34.1 kW, 25-30 kW cases), so those public claims cannot be defended without re-sizing the meter and ports.

## 8. Required changes

1. Adopt 19 lines (9 in, 10 out), with edge outlets at ±54 mm and half-area edge outlet windows. Put the inlet port at x = 0 over a window, the outlet port between windows, and header centres at about ±16 mm.
2. Add segment-level balancing: either an outlet-side orifice row of 0.5-1.0 kPa (or split the meter 1.3 / 0.6 kPa), or a doubled outlet header with matched edge windows. Redefine the E2 metric as segment-level max/min, measured by dye or IR per segment.
3. Define the orifice geometry: either rectangular with corner radii at 0.45 mm2, or an oblong 0.5 x 1.0 mm stadium. Also define the punch direction relative to forward flow. Measure Cd(Re) on coupons at Re 300-1,600.
4. Specify the guard as square-weave mesh, built as an inside-out radial diffuser in the port boss. Keep a ≤ 1 kPa allowance.
5. Restate the comparisons at matched boundaries: core 4.3 vs 18.8 kPa; port-to-port at a stated common bore (3.5x at 20 mm, 1.9x at 12 mm); tray loop with named UQD08 Cv. Label equal-pumping-power as plate-only and add the loop-boundary row (about 20 LPM, 27.5 K).
6. Cap Q-capacity at the flow that meets the velocity rules (about 22 kW for this meter), or declare a high-flow meter SKU.
7. Extend keyed orifices to PRISM branches in any mixed rack.
8. Use fin-field dP taps for fouling and E4. Add base-thickness measurement under the jets (UT or sectioning) at 1x / 1.5x / 2x.
9. Make the offset-orifice option (jets on the grate lip) the baseline. It removes base impingement at about 0 K.
10. Fix the bleed size (1.1 mm for 4 %), the 0.56 / 0.46 kPa separator inconsistency, and `plenum_prism.py`'s main block.

## 9. Improvements

- Drop the 16 mm port option, or rate it at ≤ 12 LPM.
- Lead with core dP and the three-boundary table, using UQD08 Cv measured in E0.
- Use 2 kPa-range transducers so the OCP 25 % point (0.42 kPa) is measurable.
- Run single-cell CFD (orifice, window, kerf, segment) before Rev A to settle the kerf share, jet velocity and kerf loss.

**Sources:**

- [CPC Everis UQD08 / UQDB08 spec sheet](https://www.cpcworldwide.com/Portals/0/Downloadable-Content/TRM/Literature/Spec-Sheets/CPC-Everis-UQDB08-UQD08-Spec-Sheet.pdf) (Cv ~4.75 max)
- [FITOK UQD series](https://www.fitok.com/tmp/file/Liquid_Cooling_Universal_Quick_Disconnect_UQD_Series_EN.pdf) (UQD08 Cv 3.65 / 3.70 / 3.76)
- [Danfoss UQD fact sheet](https://assets.danfoss.com/documents/580741/AI423953312825en-001101.pdf) (23.6 LPM at 5 m/s; UQD04 Cv 1.37)
- [Stäubli UQD brochure](https://www.staubli.com/content/dam/fcs/brochures/products/uqd/uqd-thermal-management-standard-staubli-en.pdf) (23.56 LPM at 5 m/s)
- [Parker QCD thermal management brochure](https://www.wilson-company.com/images/document/QCD/Parker-QCD-Thermal-Management.pdf)
- [Copper Development Association: copper piping design velocities](https://live.copper.org/applications/plumbing/techcorner/designing_piping_systems.php)
