# verify-manufacturing: PRISM draft, manufacturing / mechanical integrity / inspection lane

Scope: draft sections 2.2, 3.1-3.2, 5.1-5.7 and E1. Numbers were re-derived in `verify/mfg_checks.py` (closed-form strip, plate, foundation and capillary models; ±25-30 %). The draft has no script for any 5.2 stress or for mass, and `arch/prism_cost.py` is hard-coded line items.

## Bottom line

The architecture is buildable with conventional processes. Two of its stated routes, however, are not right as written:

1. **The stamped 4.5 mm plenum laminations.** The stamping limit is the 1.5 mm web, not d/t. Web/t is 0.33, against ≥ 1-2 for conventional stamping and about 0.6 for fineblanking.
2. **The claim that the pressurised flatness scan plus the infrared screen "replace C-SAM" for tie integrity.** With kerfs, the critical defect is a single unbonded land strip. It is invisible to both screens and passes proof and sample burst.

Neither defect kills PRISM. Both make specific statements indefensible, and they move cost and inspection. Three further problems need fixing:

- The kerfing step is unproven at this scale.
- The header-bar top wall is 1 mm thinner than the stress table assumes.
- The unbonded-patch tolerance was never updated for the 35-50 MPa yield.

## Claims checked

| # | Claim (draft) | Draft | This check | Verdict |
|---|---|---|---|---|
| 1 | Skive 0.15/0.15 x 2.0 mm OFE over 108 mm (aspect 13) | feasible | Aspect 13 is inside the 10-25 skiving range. Stroke force is about 6-16 kN over 108 mm, which is normal skiving-machine class. | confirmed |
| 2 | "Skived on a 2.5 mm blank" | 2.5 mm | Volume balance h·t = p·d gives d = 1.0 mm, so the base is 1.5 mm during the skive. That is the floor of the ≥ 1.5-2 mm the CrossComb proposal itself cites. The fins stand 1.0 mm proud of the blank face, so the perimeter rim that seals the fin layer needs a ≥ 3.5-4.0 mm blank with a pocketed field. The rim is unspecified. | corrected |
| 3 | Gang-saw 0.3 mm kerfs through the fins; "cross-cutting skived fins is established practice" | 3 US$/plate, ±0.05 mm | No precedent found below about 0.4-0.5 mm fins at coarse pitch. Tooth force is 2-9 N against a fin-wall lateral collapse load of 1.4-5 N (cold-worked fin). Each plate has 12,960 exit-burr and chip sites. Bright-dip removes 2-5 µm, not 20-50 µm burrs. | refuted as precedent; unverifiable as process (fallback exists) |
| 4 | Kerf run-out / floor depth | not addressed | A 20-63 mm saw runs 6-11 mm past the full-depth point, against an 8.5 mm border. It notches the rim braze land and draws filler, unless the kerfs stop ≥ 8 mm short. Kerf overshoot into the base thins the defect-case hinge (#14). | corrected |
| 5 | Plenum layer: 2 stamped 4.5 mm laminations, "closed-end slots trivially stamped... punchable at d/t 1.0" | US$4 at 100k | d/t = 1 is fine (punch stress about 420 MPa). Web/t = 0.33, slot width 1.0t (guideline ≥ 1.5t), slot length 24t with a 1.5 mm web (guideline: long slots ≥ 4t from an edge). Shear force about 370 t per lamination. Burr and roll-over are 0.2-0.45 mm on 1.5 mm webs. | **refuted** |
| 6 | Floor grate 1.0 mm with 1.2 x 108 mm closed-end windows | stamped | d/t 1.2, web/t 4.8, guided blade punch at about 340 MPa. It is feasible, but the burr side must face away from the fin tips and the 4.8 mm strips need flattening. | confirmed (with deburr and flatten) |
| 7 | Meter: 486 oblong 0.5 x 0.9 mm orifices in 0.4 mm, ±0.02 mm | punchable | d/t 1.25, web/t ≥ 2.75: feasible as a perforating die. t/d = 0.8 is the thick-orifice regime at Re about 600, so Cd depends on die-roll orientation and direction (0.62-0.8). Backlit vision checks area, not Cd. | confirmed (feature); Cd unverified |
| 8 | Single-cycle vacuum braze, 6-7 parts, ≤ 0.2 MPa | feasible | 0.2 MPa is 3.1 kN per plate (320 kg of dead weight), so a differential-expansion fixture with stepped pads is needed. That load flattens a 100 µm bow in the 1.5 mm base with only 7 kPa. ≤ 0.6 MPa at the tips is creep-safe. | confirmed |
| 9 | Route B (5 µm Ag) gives the least wicking | least liquid | It gives about 7 µm of liquid, which can close only about 14 µm of tip gap, against a ±20 µm (40 µm range) tip plane. Expect partial bonding unless the tips are held to ±5-10 µm or the Ag is 8-10 µm. Route A (25 µm foil) delivers 3.4x the liquid needed, about 35 µm of gap-top fill per channel. | corrected |
| 10 | Wicking control: mask 0.3 mm from window edges; orifice ≥ 0.35 mm from joints | adequate | Capillary hierarchy favours the joint: 10-40 µm joint gaps give 47-190 kPa, the 0.15 mm gap 12.7 kPa and the 0.3 mm kerf 6.3 kPa. Corner wicking stops at the window edge. Plausible if filler volume is controlled. | plausible (E1) |
| 11 | Fin tips bonded over 80 % of length | 0.80 | Masking leaves 4.2 of 6 mm: **0.70**. At the E1 gate of 70 % of the land it is 0.56. | corrected |
| 12 | 30-80 plates per load; about 1.5 furnaces per 100k/yr | 1.5 | 1.3 furnaces (80 per load, 3 loads per day) to 5.4 (30 per load, 2 per day) at 85 % availability. Braze cost about US$20-30, not 16. | corrected |
| 13 | Fly-cut base to 1.0 ± 0.1 mm after braze on a tied field | feasible | Fins at 50 % solid give a foundation modulus of about 29 kN/mm³ and about 0.3 µm under 50 N of thrust, so no chatter. Tolerance is set by skive-base variation and as-brazed bow: RSS ±0.075, worst case ±0.13 mm. A 30 µm machining layer adds ≤ 14 µm of bow over 108 mm (3 µm over a die). | confirmed (if braze bow ≤ 50 µm) |
| 14 | Unbonded-patch tolerance "about 12 mm (yield at 1.5 MPa)" | 12 mm | This value was still computed at 70 MPa. At 35-50 MPa a square patch yields at proof at 8.6-10.2 mm, and a strip across the fins at 6.7-8.0 mm. **With kerfs, one unbonded land strip (6.3 mm kerf-to-kerf) gives 31-46 MPa at proof and plastic collapse at 3.5-5.0 MPa.** | **refuted** |
| 15 | Fin tie stress 7.8 MPa (19 local) at 3.1 MPa | 7.8 / 19 | 8.9 / 22 at f = 0.70; 11.1 / 28 at the gate value of 0.56; 16 / 40 at 4.5 MPa | corrected (still OK) |
| 16 | Plenum walls 12 MPa; separator 14 MPa; perimeter land SF ≥ 3 | as stated | 12.4; 13.9; 7.7 MPa (SF 4.5-6.5) | confirmed |
| 17 | Header-bar top wall 3.5 mm over 13 mm, 21 MPa | 21 / 31 | The stack-up gives 8 mm header + 3.5 mm = 11.5 mm, but the bar is 10.5 mm, so the wall is **2.5 mm**. That gives 36-49 MPa at design burst, 52-71 at sample, and plastic collapse at 4.5-6.4 MPa. | **corrected** |
| 18 | Load paths listed are complete | 6 rows | Two are missing: the floor-grate cantilever (23 / 34 MPa if the meter sheet is bonded; 46 / 67 MPa and 4.0 MPa collapse if not), and the plenum-wall/header-rib crossings under the bar (about 240 N each at 3.1 MPa, about 32-47 MPa local). | corrected |
| 19 | A missed internal joint is a bypass caught by infrared and dP | caught | A 25 µm gap bypasses 0.009 LPM (invisible but harmless); a 100 µm gap bypasses 0.6 LPM (visible). Each of the 6 interfaces is still an **external** perimeter seam, against 1 seam on the incumbent. | confirmed (internal); external-seam count omitted |
| 20 | Pressurised flatness scan: 12 mm patch ≈ 3 µm, 20 mm ≈ 20 µm, 1 µm resolution | marginal at 12 mm | 3.7 / 28 µm, which matches. But the yield-critical patch is 7-9 mm (0.4-1.2 µm) and the land-strip defect is 0.58 µm, so neither is detectable. Burst-critical patches (13-15 mm, 4-9 µm) are detectable. | corrected |
| 21 | 100 % infrared flow screen detects wicking blockage and maldistribution | yes | Lateral diffusion in Cu is 3.3 mm at 0.1 s and 10 mm at 1 s, so the screen resolves 5-10 mm features: a blocked inlet line, yes; 1 % of channels, no. Lapped Cu has an emissivity of 0.02-0.05, so a coating is needed. | corrected |
| 22 | Mass about 1.75 kg; body 14.9 mm; 25.4 mm at the bar | as stated | Stack 1.23 kg + bar 0.41 + stubs 0.10 = 1.74 kg. That **excludes** the 2 kN load frame or backplate (0.3-0.6 kg), which the 0.15 kg line cannot contain. Body 14.9 mm is confirmed. The bar needs 26.4 mm with a 3.5 mm wall (parity still holds). | confirmed / corrected |
| 23 | Copper buy about 2.5 kg, US$35 | 2.5 kg | About 3.5 kg buy (lamination slugs 0.7 kg, strip skeletons, rim block), 1.8 kg scrap, about US$41 | corrected |
| 24 | Factory cost US$160 at 100k (+45 %), 8-10 % worse per kW | 160 | Plenum +4-11, kerf support +2-7, braze +5-15, copper +6, plus 15 % overhead: **about US$180-205** (+65-85 %), 25-35 % worse per kW | corrected |

## Fatal issues (to specific claims, not to the architecture)

1. **The plenum-lamination stamping route is not manufacturable as specified.** 1.5 mm webs between 4.5 mm closed-end slots in 4.5 mm OFE (web/t 0.33) sit far outside conventional practice (web ≥ 1-2t; Mate gives 2t) and outside fineblanking (about 0.6t). The second punch bulges or tears the web, and burrs of 0.2-0.45 mm on 1.5 mm brazed walls would need face grinding. The statement "closed-end slots are trivially stamped in 1-4.5 mm copper" and the US$4 / US$2.5 cost lines are indefensible.
2. **Tie integrity cannot be screened per part as claimed.** Because kerfs cut every fin rib, an unbonded segment spans kerf to kerf. One unbonded land strip (one missing preform strip or one twisted grate strip) has the following effects:
   - it reaches yield at the 1.0 mm kerf hinges at the 1.55 MPa proof, or at about 0.9 mm with kerf overshoot;
   - it collapses plastically at 3.5-5 MPa, below or around the 4.5 MPa sample burst;
   - it still does not rupture, since membrane action holds at about 0.1 mm of bulge;
   - it bulges 0.6 µm at proof and changes no flow.

   So proof, the flatness scan, the infrared screen, dP and sample burst all pass it. The E1 gate (≥ 40 % bonded in any 10 mm cell) also admits it. The planned process patent and the "inspection moat" (7.2, 9.2 #3) rest on a method that misses the governing defect. The plate stays leak-tight at MAWP (hinge 20-31 MPa), so this is a **verification and rating** problem, not a safety one.

## Required changes

1. **Plenum layer.** Choose one: CNC-mill a single 9 mm plate (the draft's own prototype route; about US$8-15 at volume); 4 x 2.25 mm fine-blanked laminations (web/t 0.67); or 6 x 1.5 mm stamped laminations (web/t 1.0, +2-4 braze interfaces and seams). Re-cost the line and the 1M/yr path.
2. **Header-bar section.** Close the 1 mm stack-up error. Either use a 3.5 mm top wall with an 11.5 mm bar (26.4 mm overall), or 7 mm headers (0.89 m/s, still ≤ 1.0), or a third rib. Re-state 5.2 at the 2.5 mm or the chosen geometry.
3. **Complete the 5.2 load-path table.**
   - Add the grate cantilever, with the meter-sheet joint over the land made structural and gated.
   - Add the wall-rib crossings under the bar, with FEA in E1 and wider walls or ribs locally if needed.
   - Use f = 0.70 for the ties.
   - Replace "patch tolerance 12 mm" with 7-9 mm (square) and **one land strip** for the kerfed field.
4. **Re-scope inspection honestly.**
   - The flatness scan screens burst-relevant (≥ 13 mm) patches only.
   - Add per-strip process control: preform-presence vision, Ag thickness XRF per strip, grate-strip flatness.
   - Lot over-proof at 2.5-3.1 MPa with a before/after zero-pressure flatness map. Permanent set reveals hinge yielding.
   - Lot CT of full plates for filler presence per land strip (BAg-8 gives about 1.9x the attenuation of Cu, so presence is visible; 5 µm route-B Ag is marginal).
   - Change the E1 gate to "every land strip ≥ X % bonded over any 10 mm".
5. **Kerf process definition.**
   - Fill the fin gaps with a support medium (wax, ice or a melt-out polymer), saw, melt out and ultrasonic-clean.
   - Stop kerfs ≥ 8 mm from the rim, or finish the ends by EDM. Leave a 0.05-0.1 mm stub above the base to protect the hinge.
   - Replace "bright-dip deburr" with a measured burr limit (≤ 15 µm) and a chip-entrapment acceptance criterion.
   - Add kerfing (potted against unpotted) as an E1 factor.
6. **Base blank.** Specify a ≥ 3.5-4.0 mm blank with a pocketed field and rim, giving a ≥ 1.5-2.0 mm base during the skive. Update the copper buy to about 3.5 kg.
7. **Filler routes.** Route B needs a tip plane of ±5-10 µm (diamond planing along the fin direction, not an arc fly-cut across the fins) or 8-10 µm of Ag. Route A should drop to 12-15 µm foil, or perforated 25 µm foil, to cut excess liquid about 2x. Add tip-plane tolerance as an E1 factor.
8. **Braze capacity.** Restate as 2-5 furnaces per 100k/yr and US$20-30 per plate. Specify a differential-expansion fixture with pads stepped for the bar or separator top.
9. **Infrared screen.** Coat the as-brazed face with high-emissivity paint and run the screen **before** the face fly-cut, which removes the paint. Claim 5-10 mm resolution, not channel counts. Replace "≤ 1 % channels blocked by infrared" in E1 with CT and sectioning.
10. **Mass and cost scorecard.** State the mass boundary (with or without the load frame). Move the central cost to about US$190 (the draft's "conservative") and the per-kW penalty to about 25-35 %.

## Improvements

- Stamped parts: specify burr orientation, flattening to ±20 µm and orifice die-roll orientation; test Cd in both directions (back-flush).
- Control the 6 external perimeter seams (vs 1 on the incumbent); the green-laser perimeter seam also cuts leak-yield loss.
- Use fly-cut print-through as a free signal: unbonded regions deflect about 5-10 µm under thrust and spring back as bumps a post-cut flatness map can flag.
- Budget the confocal pressure-scan station (about US$0.2-0.4 M); it is missing.
- IP note for that lane: Nidec WO2026100588A1 (filed 2025-11-05, published 2026-05-15) claims fin tips brazed to the cover, with tip geometry that limits filler blockage. It shows fin-tip brazing is being industrialised, weakens the trade-secret moat, and belongs on the FTO list next to provisional #1.

## Evidence (web)

- Nidec fin-tip-brazed cold plate (WO2026100588A1): https://eureka.patsnap.com/patent/WO2026100588A1
- Copper softening under the cover in vacuum braze (fins designed to carry the cover): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10834847
- Filler capillary blockage in microchannel brazing is hard to detect by NDT (IIR): https://iifiir.org/en/fridoc/capillary-flow-of-liquid-metal-occurring-in-micro-channel-heat-29059
- Punching rules (hole spacing 2t; slots ≥ 1.5t; long slots ≥ 4t from an edge): https://www.mate.com/technical-resources/punch-press-resources/tips-techniques/punching/techniques/holes/ ; https://www.xometry.com/resources/industry-design-tips/stamping-design-tips/ ; https://www.metalformingmagazine.com/public/images/2013/10/digital/files/basic-html/page80.html
- Fineblanking minimum hole about 0.6t (vs 1.0t conventional): https://www.ai-online.com/fine-blanking ; https://www.thefabricator.com/thefabricator/article/bending/blanking-developments---part-ii
- Skived fins can be CNC machined afterwards (aluminium, 0.1/0.2 mm; no fine-pitch Cu cross-cut precedent found): https://www.eenewseurope.com/en/skiving-boosts-heat-sink-design/
- Alloy Enterprises Stack Forging is Al, laser-cut and diffusion-bonded, so it is not a Cu braze precedent: https://semiaccurate.com/2025/08/28/alloy-forges-very-complex-cold-plates/
- OFE temper yields (Aurubis): https://www.aurubis.com/dam/jcr:411b63c7-fe07-4508-ba63-027cf5083f30/PNA%20203_Cu-OFE_C10100-EN.pdf
- Wieland publishes FSW pin-fin plates, with no skived 0.1 mm data: https://www.wieland.com/products/electronics-cooling

No Kingka process data was found, and no source confirms cross-cut skived Cu fins at 0.3 mm pitch.
