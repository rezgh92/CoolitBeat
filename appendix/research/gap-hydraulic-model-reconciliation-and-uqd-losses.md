# Gap fill: reconciling the three internal hydraulic reconstructions, and the real cost of quick disconnects and hoses at 15-18 LPM

Date: 2026-10-13. Operating point throughout: 15 kW, 1.2 LPM/kW = 18 LPM PG25 at ~50 C film (rho 1005 kg/m3, mu 1.25 mPa s), 45 C inlet, 117 cm2 (108 x 108 mm) calibrated footprint, unless stated.

Calculation script and full output: `docs/cooling/appendix/research/recon/reconcile.py` and `recon/reconcile_output.txt` (run with `python3 -I`). It imports the model now on disk (`docs/cooling/model/coldplate_model.py`, commit 7f4ffd3 "Correct cold plate model: Darcy friction ...") and emulates the v1 model (commit 3a14c9f) analytically.

**Evidence status.** No web search could be run this turn (the shared 200-search budget was exhausted before this agent started; four queries were refused) and the single WebFetch attempt on the OCP UQD v2.0.0 PDF failed on DNS. Everything in Sections 1-3 is internal and verified by re-running code. Everything in Section 4 about coupling flow coefficients (Cv) is **engineering memory plus physics bounds, flagged [KB-L/M]**, and must be checked against the CPC / Staubli / Danfoss / Parker datasheets and the OCP UQD spec before it goes into a requirement.

---

## 1. Headline answers

| Question | Answer | Confidence |
|---|---|---|
| Is the "4x friction-term error" real? | **Yes.** v1 used `dp = fRe_Fanning mu u L / (2 Dh^2)`; the correct Darcy form is `dp = 2 fRe_Fanning mu u L / Dh^2` (= 32 mu u L / D^2 for a round tube, fRe_F = 16). Verified numerically: v1/true = 0.25 exactly. Shah & London's polynomial is the Fanning one (gives 14.23 for a square duct, 24 for parallel plates; Darcy values are 56.9 / 96). | high |
| Which CoolIT-like number is right: 9 / 19 / 22 kPa? | **None is "wrong" once the boundary is stated.** 8.6 kPa = v1 with the bug (retire it). 19.5 kPa = v1 with the bug fixed and a flat 3 kPa port allowance. 21.8 kPa = independent network (adds Hagenbach and real plenum losses, same flat 3 kPa ports). **24.6 kPa = the model now on disk** (same core, real port loss for a 12 mm bore at 2.65 m/s = 8.1 kPa). The **core (channel + turns) is 15.0 kPa in all three corrected versions**; the spread is entirely in the plumbing allowance. Programme value for the 0.2/0.2 x 4 mm, 54 mm reconstruction: **20-25 kPa port-to-port at 18 LPM; 17-45 kPa over the plausible fin-pitch window; gap-dp's "35 kPa working, 20-60 window" stands.** | high (arithmetic), low (CoolIT's real geometry) |
| Which HMMC number is right: 5.0 / 6.2 / 8.3-8.6 kPa? | 6.2 kPa = v1 (bug immaterial: fin friction is 0.08 vs 0.33 kPa; bug-free v1 is 6.4). 8.3-8.6 kPa = hydraulic-detail's L = 2 mm geometry with a 2.2 kPa L1-header and 1.8 kPa L2 allowance and a flat 3 kPa port term. 5.0 kPa = manifold-maldistribution's **design H** (L = 4 mm, 16 mm ports, large CC headers, exact network). **5.3 kPa = model on disk, HMMC-R, which is design H** (ports 2.6 + orifice comb 2.0 + header 0.5 + channel 0.2). **Design of record is design H; model 5-5.5 kPa, claim <= 10 kPa port-to-port at 18 LPM, 16 mm ports, no QD.** The HMMC's dP is 85-95 % plumbing, so the honest window is 5-9 kPa depending on port bore and header sizing. | high (internal consistency) |
| 2 mm vs 4 mm flow length? | **4 mm.** Thermally identical in the model (entrance-dominated Nu; conv 10.1 K and avg dT 28.0 K for L = 2, 3, 4, 6 mm with HMMC-R). Hydraulically L = 4 mm costs 0.2 kPa more at 0.15 mm gaps (2.2 kPa at 0.075 mm gaps) but buys 1.2-1.6 mm machinable manifold walls, half the slot count (14 vs 27 inlet slots) and the branch resistance that the manifold needs for uniformity. Both later notes and the on-disk model already adopt 4 mm. | high |
| "0.2 mm slots + 8 mm deep L2" vs "centre-fed CC headers with 1.5 x 6 / 3.5 x 8 mm slots" | Not competing fixes: **they act at different manifold levels and both are needed in principle; design H is the one that was solved end-to-end.** hydraulic-detail fixed the *along-slot* (L2) uniformity with a 1-D proxy (pressure variation along the L2 channel <= 0.1-0.2 of the branch dP) by throttling at the 0.2 mm nozzle window and enlarging the L2 channel to 1.2 x 8 mm (u <= 0.6 m/s). manifold-maldistribution solved the full dividing/combining network at L1 *and* L2 and found (i) the originally specified 0.4 x 3 mm slot-as-manifold runs at 9 m/s and back-flows (which hydraulic-detail never modelled, because its L2 channel was a separate 1.2 x 4 mm passage), (ii) the L1 topology dominates: centre-fed/centre-collected (CC) headers beat any taper, (iii) the throttle can be the channel itself (4 mm, 0.075 mm gaps: 2.2 kPa) or an orifice lip (0.15 mm, 1.5 m/s jets), the former being easier to make. **Design H** = CC headers 10 x 15 / 14 x 20 mm, 3.5 x 8 mm open-bottom slots at 8 mm pitch, 16 mm ports, global max/min 1.10 at 18 LPM. The on-disk model adds a 2 kPa "orifice comb" to HMMC-R because its 0.15 mm gaps alone give only 0.23 kPa of branch resistance; that is the hydraulic-detail throttle idea re-applied where it is needed. | high |
| Is "3 kPa for ports + UQD" defensible? | **No.** 3 kPa at 18 LPM is a plausible *internal-port* allowance only for >= 16 mm bores (design H: 2.5 kPa at 1.5 m/s). A mated UQD pair (supply + return) at 18 LPM is **~20-35 kPa for UQD08 (Cv 3-4), ~80-185 kPa for UQD06 (Cv 1.3-2.0), ~500-1,250 kPa for UQD04**; only a 3/4-in / "UQD12-class" coupling (Cv 6-10) gets to 3-9 kPa. manifold-maldistribution's 25 kPa (UQD08) / ~100 kPa (UQD06) estimates are the right order. | medium (law), low (Cv values) |
| Does coupling size become the design driver? | **Yes, at 18 LPM through one loop.** With 1/2-in hose, 9.5 mm barbs and one UQD08 pair, the plate is 5-10 of 67-86 kPa (HMMC) or 25-35 of 86-111 kPa (skived). The "tray <= 70-100 kPa incl. QDs" requirement is met by the HMMC with a single UQD08 pair and full-bore (12 mm) stubs (45-65 kPa), is marginal for the skived reconstruction (64-90), and is **infeasible with UQD06/3/8-in plumbing for any plate (230-365 kPa)**. The "negative-pressure SKU, plate + tray <= 30-50 kPa" requirement is **infeasible at 18 LPM with one UQD08 pair** (45-65 kPa best case) and feasible only with (a) dual UQD08 ports or a 3/4-in-class coupling (15-28 kPa), or (b) 0.75-1.0 LPM/kW with a single UQD08 pair (18-45 kPa). | medium |

**Consequences for the downstream documents.** The "6 kPa vs ~9 kPa" comparison quoted in physics-options.md (lines 26, 247), manufacturing-cost.md (lines 20, 141, 205) and power-electronics.md (line 25) is the v1-bug comparison and understates the architecture's hydraulic advantage: replace with **"~5 kPa (model, claim <= 10) vs ~25 kPa (reconstruction, window 17-45, programme working value 35) port-to-port at 18 LPM, quick disconnects excluded"** and add the boundary statement every time. The plate's pumping power is irrelevant either way (1.5 W vs 7.4 W hydraulic); what matters is that a 5 kPa plate leaves the whole tray budget to the couplings.

---

## 2. The friction-term correction, verified

| Check | Result |
|---|---|
| Round tube, mu 1.25 mPa s, u 0.5 m/s, L 50 mm, D 0.4 mm: Hagen-Poiseuille 32 mu u L / D^2 | 6,250 Pa |
| Correct Fanning form 2 (fRe_F = 16) mu u L / D^2 | 6,250 Pa |
| Correct Darcy form (fRe_D = 64) mu u L / (2 D^2) | 6,250 Pa |
| v1 form fRe_F mu u L / (2 D^2) | 1,562.5 Pa = **0.25 x true** |
| Shah & London polynomial 24 (1 - 1.3553 a + 1.9467 a^2 - 1.7012 a^3 + 0.9564 a^4 - 0.2537 a^5) at a = 1 | 14.23 = square-duct **Fanning** fRe (Darcy 56.9) |
| same at a -> 0 | 24.0 = parallel-plate **Fanning** fRe (Darcy 96) |
| at a = 0.05 (0.2 x 4 mm channel) | Fanning 22.5, Darcy 89.9 |

So the polynomial in all three internal scripts is the Fanning one, and the only error was v1's prefactor. manifold-maldistribution.py uses `96 x polynomial` with the Darcy formula (correct); hydraulic-detail.py uses `2 x 24 x polynomial x mu u L / Dh^2` (correct); the on-disk v2 model uses `2 * fRe * mu * u * L / Dh**2` (correct). The textbook anchors are Shah & London (1978) *Laminar Flow Forced Convection in Ducts* (Fanning f Re tables) and any fluids text (White, *Fluid Mechanics*, Table 6.4: Darcy f Re = 96 for parallel plates, 56.9 square, 64 circular).

---

## 3. Reconciliation of the reconstructions on one component basis

### 3.1 CoolIT-like skived split-flow plate (0.2 mm fins / 0.2 mm gaps / 4 mm tall, 54 mm half-length, 117 cm2), 18 LPM, kPa

| component | v1 (bug) | v1 + 4x fix | hydraulic-detail | v2 on disk | comment |
|---|---:|---:|---:|---:|---:|
| channel friction (fully developed) | 3.63 | 14.53 | 14.71 (incl. Hagenbach) | 14.53 | u = 0.69 m/s, Re 212, x+ >> 0.05 |
| turns / entry / exit on channel velocity | 0.48 (K 2.0) | 0.48 | 0.67 | 0.48 | |
| plenums / headers | 1.45 (K 2 at 1.2 m/s) | 1.45 | 3.41 (K 1 on each plenum, 8 x 12 / 6 x 12 mm) | 1.45 | +/-50 % either way |
| ports | 3.00 flat ("fittings / UQD / ports") | 3.00 flat | 3.00 flat | 8.13 (12 mm bore, 2.65 m/s, K 2.3) | the only real disagreement |
| **total port-to-port** | **8.56** | **19.46** | **21.78** | **24.59** | |
| core only (channel + turns) | 4.1 | 15.0 | 15.4 | 15.0 | **agrees within 3 %** |

Reading: the three corrected reconstructions are the same core with different plumbing allowances. Quote the plate as **"core ~15 kPa, port-to-port 20-25 kPa at 18 LPM (12-16 mm ports)"**. The fin pitch is a guess, so the honest window from the on-disk model is:

| skived fins gap/fin x H (mm) | u_ch m/s | channel kPa | port-to-port kPa | avg dT K |
|---|---:|---:|---:|---:|
| 0.25/0.25 x 4.0 | 0.69 | 9.4 | 19.4 | 38.2 |
| **0.20/0.20 x 4.0 (calibrated)** | 0.69 | 14.5 | **24.6** | 34.5 |
| 0.15/0.15 x 3.0 | 0.92 | 34.4 | 44.9 | 31.4 |
| 0.15/0.10 x 2.0 | 1.16 | 43.8 | 54.7 | 32.0 |
| 0.10/0.10 x 2.0 ("finer skived") | 1.39 | 116 | 128 | 28.3 |

The 128-158 kPa rows confirm hydraulic-detail's "~140 kPa, not 35" for fine fins in a 54 mm split-flow path, and are why "finer skived" is not a route. CoolIT's own statement that the plate was "optimized to minimize pressure drop" plus its 4 kW loop datum (8 psi = 55 kPa full loop incl. QDs at ~6 LPM, gap-dp report) are consistent with the 0.2-0.25 mm rows, i.e. **CoolIT's 15 kW plate most probably sits at 20-45 kPa port-to-port at 18 LPM**; the gap-dp working value of 35 kPa (20-60) needs no change.

### 3.2 HMMC variants, 18 LPM, kPa

| component | v1 HMMC (L 2 mm, 0.1/0.1 x 1.0, 0.3 mm slots) | hydraulic-detail (same core) | manifold-maldist. design H (L 4 mm, 0.075 gaps, 3.5 x 8 slots, CC) | v2 HMMC-R on disk (design H, 0.15/0.10 x 2.0) |
|---|---:|---:|---:|---:|
| channel friction | 0.08 (bug; true 0.33) | 0.33 | 2.22 | 0.23 |
| turns, entry, exit, nozzles | 0.02 + 0.09 slot | 1.03 | 0.06 + 0.02 | 0.01 |
| orifice comb (metering) | - | - | - (channel is the throttle) | 2.00 |
| L2 slots / manifold channels | - | 1.81 | 0.11 net (recovery - friction) | - |
| L1 headers + tees | 2.01 (K 4 at 1.0 m/s) | 2.17 | 0.05 net + 0.24 tees | 0.50 |
| ports | 4.00 flat | 3.00 flat | 2.53 (16 mm, 1.5 m/s) | 2.57 (16 mm, 1.49 m/s) |
| **total port-to-port** | **6.20** | **8.35 (8.6 with 0.2 mm slots / 8 mm L2)** | **4.99** | **5.32** |
| share that is plumbing (headers + ports + slots) | 97 % | 84 % | 58 % | 58 % (incl. orifice) |

Reading: the four HMMC totals differ because they are four different manifold geometries, not because of the friction bug (which moves the HMMC by 0.25 kPa). The 8.3-8.6 kPa figure carries a 4 kPa L1+L2 allowance at 1.0-1.2 m/s header velocities that design H deliberately halves by using 10 x 15 / 14 x 20 mm centre-line headers (u <= 1 m/s, mostly recovered) and 16 mm ports. **Design H is the design of record (manifold-maldistribution Section 3.6, SYNTHESIS-physics item 5, and the v2 model's `hmmc()` docstring all say so).** Its published claim should stay at **<= 10 kPa port-to-port at 18 LPM, <= 25 kPa at 36 LPM, 16 mm ports, quick disconnects excluded**, which keeps a 2x margin over the 5.0-5.3 kPa model for CFD/test discovery and for the +/-50 % uncertainty on port and tee losses.

Flow-length check (v2 HMMC-R, 18 LPM): L = 2 / 3 / 4 / 6 mm gives channel friction 0.06 / 0.13 / 0.23 / 0.54 kPa, total 5.1 / 5.2 / 5.3 / 5.7 kPa, and the *same* conv 10.1 K / avg dT 28.0 K. The thermal model is entrance-dominated (x* invariant), so flow length is a free hydraulic/manufacturing variable: 4 mm is chosen for manifold-wall machinability and branch resistance, exactly as manifold-maldistribution concluded.

### 3.3 Which maldistribution fix

| aspect | hydraulic-detail ("0.2 mm slots + 8 mm deep L2") | manifold-maldistribution (design H) | reconciliation |
|---|---|---|---|
| what "slot" means | 0.3 -> 0.2 mm nozzle under a separate 1.2 x 4 -> 1.2 x 8 mm L2 channel | the 3.5 x 8 mm open-bottom distribution channel itself (no separate nozzle) | different naming of the same two-level stack; the original 0.4 x 3 mm "slot" with no L2 channel above it (9 m/s) is what back-flows |
| level analysed | L2 only, 1-D proxy (max of half friction, rho u^2/4) vs branch dP; L1 assumed "fed from both ends", K 1.5 | L1 + L2 + L3 nested dividing/combining network with momentum recovery (theta_d 1, theta_c 2) | manifold-maldistribution supersedes; it reproduces hydraulic-detail's L2 conclusion (u_L2 <= 0.6 m/s) and adds the L1 rule |
| throttle | nozzle window (0.2 mm) | channel friction (4 mm, 0.075 mm gaps: 2.2 kPa) or 0.15 mm orifice lip | v2 model uses an orifice comb (2.0 kPa) for the 0.15 mm-gap R core; nozzle vs comb is a manufacturing choice |
| L1 topology | not resolved | **CC (centre-fed and centre-collected) is required**; U/Z 2-5x worse; taper useless for U/C/CC | adopt CC |
| uniformity result | ratio 0.06 (proxy) | global max/min 1.10 at 18 LPM, 1.18 at 36 LPM, dT_hot 0.3 K | quote the latter |
| packaging | not stated | manifold block adds ~25 mm height (8 mm slots + 15-20 mm headers + walls); ~30 mm plate | carry into the architecture |

Both notes agree on the governing rule: the branch (core) dP must be >= 6x the header-inlet dynamic head and >= 15x the slot-entry dynamic head at the maximum rated flow. Design H satisfies it; the originally specified 0.3-0.5 mm slots / 4 x 8 mm headers do not. The momentum-coefficient uncertainty (global 1.06-1.15) is the first thing a single-slot-pair CFD or water-table test should pin down.

---

## 4. Loop losses outside the plate: quick disconnects, hoses, barbs

### 4.1 Coupling flow coefficients and the Cv law

dP per mated coupling = SG (Q[gpm] / Cv)^2 psi; a plate loop has **two** mated couplings (supply and return), so the "pair" numbers below are 2x. PG25 SG ~1.01-1.02 (taken as 1.0 in the table, +2 %).

| coupling (OCP size, nominal) | Cv per mated coupling | basis / confidence | pair dP at 11.25 LPM (0.75 LPM/kW) | 15 LPM (1.0) | **18 LPM (1.2)** | 36 LPM |
|---|---|---|---:|---:|---:|---:|
| UQD02 (1/8 in) | 0.2-0.3 | KB-L | 1,360-3,060 kPa | 2,420-5,440 | 3,480-7,840 | - |
| UQD04 (1/4 in) | 0.5-0.8 | KB-M (CPC LQ4/UQD04-class ~0.6) | 190-490 | 340-870 | **490-1,250** | 1,960-5,000 |
| UQD06 (3/8 in) | 1.3-2.0 | KB-L/M | 31-72 | 54-129 | **78-185** | 313-742 |
| UQD08 (1/2 in) | 3.0-4.0 | KB-L/M (CPC UQD08-class ~3.5-3.7) | 8-14 | 14-24 | **20-35** | 78-139 |
| UQDB08 (1/2 in blind-mate) | 2.5-4.0 | KB-L (blind-mate valving usually equal or slightly more restrictive) | 8-20 | 14-35 | **20-50** | 78-200 |
| 3/4-in class ("UQD12", not confirmed to exist in OCP v2.0.0) | 6-10 | KB-L; physics bound | 1-3 | 2-6 | **3-9** | 13-35 |

Physics cross-check (independent of memory): expressing the Cv ranges as a loss coefficient on the nominal bore gives K = 1.7 (UQD08, 10 mm bore, 3.8 m/s at 18 LPM), 3.4 (UQD06, 8 mm, 6.0 m/s), 3.2 (UQD04, 5 mm, 15 m/s), 2.2 (3/4-in, 16 mm, 1.5 m/s). Valved dry-break couplings with a poppet in each half sit at K ~1.5-4 on the bore, so the ranges are physically consistent even if the exact Cv values are not yet verified. The bore velocities themselves are the warning: 15 m/s in a UQD04 and 6 m/s in a UQD06 at 18 LPM exceed any erosion/noise rule (2-3 m/s), independent of dP.

Where the numbers come from and how to verify them (not fetched this turn):
- OCP Design Spec UQD v2.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf - pull the per-size rated-flow / maximum pressure-drop table (the Intel-origin v1.0 spec had one; its values are not reliably remembered and are therefore not quoted).
- CPC (Dover) Everis UQD02/04/06/08 and UQDB datasheets (cpcworldwide.com): "Flow coefficient Cv" line per size.
- Staubli SPC/UQD-compliant series (staubli.com): Kv (m3/h) = 0.865 Cv, or the dP-vs-flow curve.
- Danfoss Hansen UQD series (danfoss.com): Cv per size.
- Parker UQDB blind-mate (parker.com): dP vs flow curve at 20 LPM.

### 4.2 Hose friction (smooth EPDM, Blasius; PG25 at 50 C), kPa per metre

| hose ID | 11.25 LPM | 15 LPM | **18 LPM** | 36 LPM | u at 18 LPM |
|---|---:|---:|---:|---:|---:|
| 1/4 in (6.4 mm) | 67 | 110 | **151** | 509 | 9.5 m/s |
| 3/8 in (9.5 mm) | 9.8 | 16 | **22** | 75 | 4.2 m/s |
| 1/2 in (12.7 mm) | 2.5 | 4.1 | **5.6** | 19 | 2.4 m/s |
| 5/8 in (15.9 mm) | 0.8 | 1.4 | **1.9** | 6.5 | 1.5 m/s |
| 3/4 in (19 mm) | 0.4 | 0.6 | **0.8** | 2.8 | 1.1 m/s |

### 4.3 Barbs and stubs (K = 1.0 per fitting on the barb bore; a 1/2-in barb has a 9-10 mm bore)

| fitting | 11.25 LPM each / x4 | 15 LPM each / x4 | **18 LPM each / x4** |
|---|---:|---:|---:|
| 3/8-in barb, 7 mm bore | 12 / 48 | 21 / 85 | **31 / 122** |
| 1/2-in barb, 9.5 mm bore | 3.5 / 14 | 6.3 / 25 | **9.0 / 36** |
| 1/2-in full-bore stub, 12 mm | 1.4 / 6 | 2.5 / 10 | **3.5 / 14** |
| 5/8-3/4-in, 15 mm bore | 0.6 / 2 | 1.0 / 4 | **1.4 / 6** |

The barb row is the overlooked term: four 1/2-in barbs (plate in/out, QD in/out) at 18 LPM cost as much as the HMMC plate seven times over. Full-bore stainless stubs or push-lock fittings are worth 20-25 kPa per loop.

### 4.4 Tray-loop budgets for one 15 kW plate (1 m of hose, four fittings, one QD pair, plate), kPa

Plate values: HMMC design H 5.3 model / 10 claim (scaled with flow^1.8); skived reconstruction 24.6 model / 35 programme working value (flow^1.3).

| loop at **18 LPM** | hose | fittings | QD pair | plate | **total** | <= 100 | <= 70 | <= 50 | <= 30 |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| 3/8-in hose, 7 mm barbs, UQD06 pair + HMMC | 22 | 122 | 78-185 | 5-10 | **228-340** | no | no | no | no |
| same + skived | 22 | 122 | 78-185 | 25-35 | **247-365** | no | no | no | no |
| 1/2-in hose, 9.5 mm barbs, UQD08 pair + HMMC | 6 | 36 | 20-35 | 5-10 | **67-86** | yes | marginal | no | no |
| same + skived | 6 | 36 | 20-35 | 25-35 | **86-111** | marginal | no | no | no |
| 1/2-in hose, 12 mm stubs, UQD08 pair + HMMC | 6 | 14 | 20-35 | 5-10 | **45-65** | yes | yes | marginal | no |
| same + skived | 6 | 14 | 20-35 | 25-35 | **64-90** | yes | marginal | no | no |
| 1/2-in hose, 12 mm stubs, **dual UQD08 pairs** (9 LPM each) + HMMC | 6 | 4 | 5-9 | 5-10 | **19-28** | yes | yes | yes | yes |
| same + skived | 6 | 4 | 5-9 | 25-35 | **39-53** | yes | yes | marginal | no |
| 3/4-in hose, 15 mm stubs, 3/4-in-class pair + HMMC | 1 | 6 | 3-9 | 5-10 | **15-25** | yes | yes | yes | yes |
| same + skived | 1 | 6 | 3-9 | 25-35 | **34-50** | yes | yes | marginal | no |

| loop at **15 LPM (1.0 LPM/kW)** | total HMMC | total skived | | loop at **11.25 LPM (0.75 LPM/kW)** | total HMMC | total skived |
|---|---:|---:|---|---|---:|---:|
| 1/2-in, 9.5 mm barbs, UQD08 | 47-60 | 62-81 | | same | 26-34 | 38-49 |
| 1/2-in, 12 mm stubs, UQD08 | **31-45** | 47-66 | | same | **18-26** | 29-41 |
| dual UQD08 | 14-20 | 29-40 | | same | 8-12 | 19-26 |
| 3/4-in class | 11-18 | 26-38 | | same | 6-10 | 17-25 |

Readings:
1. **At 18 LPM through one loop, the coupling and fittings are 85-95 % of the loop dP for the HMMC and 65-75 % for the skived plate.** The plate's 5 vs 25 kPa still matters (it is the difference between "yes" and "marginal" at the 70 kPa line), but the coupling class decides feasibility.
2. **UQD06 / 3/8-in plumbing cannot carry 18 LPM** (> 200 kPa, 6 m/s in the coupling). Any 15 kW-class tray loop is 1/2-in minimum. This is consistent with the sibling note that NVIDIA/ODMs move to 1/2-in (UQD08/UQDB08) for > 200 kW racks [chip-roadmap-requirements, KB-L].
3. **The "tray <= 70-100 kPa incl. QDs" requirement is feasible at 18 LPM only with UQD08 + full-bore stubs + a <= 10 kPa plate** (45-65 kPa). With the skived reconstruction it is marginal (64-90). That is a genuine, quotable architectural advantage, but it must be stated at the loop boundary, not as "6 vs 9 kPa".
4. **The "negative-pressure SKU, plate + tray <= 30-50 kPa" requirement is infeasible at 18 LPM with a single UQD08 pair** (best case 45 kPa). It is feasible with dual UQD08 ports (19-28 kPa) or a 3/4-in-class coupling (15-25 kPa), or by running the HMMC at 0.75-1.0 LPM/kW with one UQD08 pair (18-45 kPa). The thermal case for the lower flow already exists: hydraulic-detail's Pareto shows the HMMC matching the skived plate's 34.5 K at 6.9 LPM, and the on-disk model gives HMMC-R Tier 1 29.9 K at 1.0 LPM/kW and 32.8 K at 0.8 LPM/kW versus the benchmark's 34.4 K at 1.2 LPM/kW. **Recommend making 1.0 LPM/kW the headline operating point for the negative-pressure and single-UQD08 configurations.**
5. Hydraulic power is not the issue (QD pair 7.5 W at 25 kPa; plate 1.5 W); CDU head, manifold sizing and negative-pressure compatibility are.
6. Context [KB, secondary]: a GB200 NVL72 compute tray today sees ~6-7 LPM through one QD pair (120-150 LPM per rack, ~88 % to 18 compute trays). A single 15 kW plate at 1.2 LPM/kW asks 2.5-3x that flow through one pair, i.e. 6-9x the coupling dP for the same size. The 15 kW demonstration therefore sits outside the interface envelope of the installed tray plumbing; CoolIT's TTV sidestepped this with 1/2-in barbs and hoses and no QDs [gap-ttv], which is a legitimate reason it published no dP.

---

## 5. What to change in the programme documents

1. **Retire "~9 kPa" and "6 vs 9 kPa"** (physics-options.md 26/247, manufacturing-cost.md 20/141/205, power-electronics.md 25). Replace with: CoolIT-like reconstruction **~25 kPa port-to-port at 18 LPM (window 17-45 kPa; programme working value 35 kPa, 20-60)**; HMMC design H **~5 kPa model, <= 10 kPa claim**, both with 12-16 mm ports and **no quick disconnects**. Advantage: **3-5x on the plate, not 1.5x.**
2. **State the boundary on every dP number**: (a) port-to-port with port bore; (b) plate + stubs/hose; (c) plate + named coupling pair. Report all three on the OCP cold-plate test-spec format at 6 flows, 45 +/- 2 C.
3. **Rewrite the requirement rows**: "plate-only <= 25 kPa at 1.0 LPM/kW, <= 35 kPa at 1.2 LPM/kW" is fine as a ceiling; add "**HMMC target <= 10 kPa at 18 LPM**". "Tray <= 70-100 kPa incl. QDs" must say "**with one UQD08/UQDB08 pair and full-bore (>= 12 mm) stubs, 1/2-in hose**". The negative-pressure row must say "**<= 30-50 kPa at 1.0 LPM/kW with one UQD08 pair, or at 1.2 LPM/kW with dual UQD08 / 3/4-in-class coupling**".
4. **Plate interface spec**: 16 mm internal ports (design H), 1/2-in-class full-bore stubs as standard, an optional dual-port (2 in / 2 out) variant for >= 15 kW at 1.2 LPM/kW and for negative-pressure loops. The HMMC's centre-line CC headers make dual ports natural (one inlet per header end).
5. **Replace the flat 3-4 kPa "ports / UQD" term** in hydraulic-detail.py and any remaining v1-derived tables with the v2 model's bore-based port term plus an explicit coupling term by Cv (sensitivity +/-50 % until datasheets are read).
6. **Do not pursue "finer skived"**: 0.10 mm fins in a 54 mm split-flow path are 128-158 kPa port-to-port (Section 3.1), confirming hydraulic-detail; the manifold is the enabler for fine fins.

---

## 6. Gaps / unknowns

1. **Coupling Cv values are unverified** (all [KB-L/M]). Needed: CPC Everis UQD04/06/08 and UQDB08 Cv; Staubli SPC Kv; Danfoss Hansen UQD Cv; Parker UQDB08 dP-vs-flow; and the OCP UQD v2.0.0 rated-flow / max-dP table. The pair-dP table scales as 1/Cv^2, so a 30 % Cv error is a 70 % dP error. Until verified, quote UQD08 pair as "20-35 kPa at 18 LPM (+/-50 %)".
2. **Does OCP UQD v2.0.0 define anything above UQD08** (a 3/4-in or "UQD12" envelope)? Unknown. If not, the only standards-compliant routes to <= 30 kPa at 18 LPM are dual UQD08 ports or lower specific flow.
3. **GB200/GB300/Rubin tray coupling size and per-tray flow** are secondary/KB (~6-7 LPM per tray, UQD04/06-class today, 1/2-in for > 200 kW racks); NVIDIA's plate and tray dP budgets are NDA.
4. **CoolIT's real 15 kW plate dP** remains undisclosed; the 20-45 kPa window rests on a fin-pitch guess calibrated only to the thermal result.
5. **Barb/stub K = 1.0 and hose smoothness** are engineering assumptions (+/-50 %); measured EPDM hose with crimped barbs can be worse.
6. **Design H's L1/L2 momentum coefficients** (global uniformity 1.06-1.15) need one CFD or water-table test; the orifice-comb alternative (v2 HMMC-R) needs a 150 um-feature manufacturability check.
7. The v2 model's port term (K 2.3 on bore velocity) is itself an estimate; the HMMC total is 50 % ports, so the claim should stay at <= 10 kPa until a prototype is measured.
8. Negative-pressure loop headroom ("<= 30-50 kPa") is the sibling's working number for Chilldyne-type systems, not a Chilldyne specification.

---

## 7. Sources

Internal (all re-run or re-read this turn):
- `docs/cooling/model/coldplate_model.py` and `model_output.md` (commit 7f4ffd3, Darcy-corrected v2); v1 = commit 3a14c9f (bug: `dp_ch = fRe * mu * u * L / (2 * Dh**2)`).
- `docs/cooling/appendix/physics/hydraulic-detail.md` (+ `.py`, `-output.txt`): 21.8 kPa skived / 8.3-8.6 kPa HMMC, 0.2 mm slot + 8 mm L2 fix.
- `.../appendix/physics/manifold-maldistribution.md` (+ `.py`, `.out.txt`): design H, 4.99 kPa, CC headers, UQD Cv-law table (Cv 0.6 / 1.8 / 3.5 / 8.0 estimates).
- `.../appendix/physics/SYNTHESIS-physics.md`: design H as geometry of record; "UQD08-class ~25 kPa per pair; UQD12-class / 3/4-in ~5 kPa".
- `.../appendix/research/gap-coolit-dp-flow-curves-and-claim-baselines.md` (+ `gap_dp_calc.py`): 4 kW loop 8 psi incl. QDs; 15 kW working 35 kPa (20-60); barbed TTV ports.
- `.../appendix/research/gap-ocp-test-spec-and-boundary-docs-full-read.md`, `standards-reliability.md`, `chip-roadmap-requirements.md`: requirement rows (plate <= 25/35 kPa; tray <= 70-100 kPa incl. UQD08; negative-pressure <= 30-50 kPa), UQD size list, 1/2-in trend.
- `.../appendix/research/recon/reconcile.py`, `reconcile_output.txt` (this report's arithmetic).

External (named, not fetched this turn; verify):
- OCP Design Spec UQD v2.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Design-Spec_UQD_v2.0.0.pdf
- OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf
- CPC Everis UQD / UQDB datasheets: https://www.cpcworldwide.com (Cv per size)
- Staubli SPC / UQD-compliant couplings: https://www.staubli.com (Kv per size)
- Danfoss Hansen UQD: https://www.danfoss.com
- Parker UQDB blind-mate: https://www.parker.com
- Chilldyne negative-pressure CDU (dP constraint context): https://www.storagereview.com/review/high-performance-leak-free-liquid-cooling-chilldynes-cdu-and-cold-plates-in-action
- Shah, R.K. & London, A.L. (1978), *Laminar Flow Forced Convection in Ducts*, Academic Press (Fanning f Re tables: 24 parallel plates, 14.23 square); Steinke & Kandlikar (2006) K(inf) fit; White, *Fluid Mechanics*, Table 6.4 (Darcy f Re 96 / 56.9 / 64).
