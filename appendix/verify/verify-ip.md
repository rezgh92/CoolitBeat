# Verify: IP / freedom-to-operate lane for the PRISM draft

Adversarial review of `design/ARCHITECTURE-draft.md` sections 0 (D3), 9.1, 9.2 and R1/R8, 2026-10-14. **This is engineering-level patent reading, not legal advice.** Outside counsel must confirm every item.

## 0. Evidence basis

- About 40 web searches across patent snippets, CAFC, PTAB and the trade press. WebFetch is blocked, so **no full claim set was read**, and claim wording comes from snippets.
- The earlier IP research files ran zero searches.
- My own checks are `verify/ip_entry_split.py` (Darcy entry split and term arithmetic) and `verify/ip_endfed_cost.py` (which uses the draft's own `cell2d.py`).

## 1. Bottom line

1. **The kerf argument is a weak design-around.** A 0.3 mm kerf opens the inter-fin flow path; it does not end it. The passage between two outlet windows stays "continuous" (the parent abstract's wording), with the inlet at its middle. About 49 % of each segment's inflow enters through fin tips under the 1.2 mm window, not through the kerf "end". The kerf is worth 2.6 % of the cell dT, which reads as an insubstantial difference under the doctrine of equivalents. Every manifold-microchannel cell is a repeated split flow.
2. **The prior-art shield is mis-framed and mis-cited.** US law has no practising-the-prior-art defence to literal infringement (*Tate Access Floors*, 2002). US 5,088,005 is Ciaccio / Sundstrand, not Harpole / TRW. Manifold-microchannel art was already argued against '330 in IPR2015-01276, and the claims survived at least in part: CoolIT asserted them again in 2019-22.
3. **The family lists are wrong.**
   - '906 is in the 2008 family and expires about 9 Sep 2028.
   - The revived '567 claim is a compliant-member claim, and its remand outcome is unknown.
   - '878 claim 1 needs a pump.
   - 9,909,820, 10,274,266 and 10,415,597 are missing.
   - TW I606224 is live to about 2032, which refutes "no foreign counterparts".
4. **Microfabrica exposure is understated, and the 0.4 mm-offset fallback puts the jets on fin tips.**
5. **Live manifold-microchannel patents are missing:** Intel 12,133,357 and 11,804,418, and Toyota 11,428,478 (gridded fins in an MMC heat sink).
6. **Of the five filings, only #1 (narrow) and #5 are worth filing.**

## 2. Claims checked

| # | Draft claim | Draft value | Our value | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | Kerfs at every inlet and outlet line mean "no channel has an inlet between its ends" | design-around | The kerf does not interrupt the flow path. 49 % of segment inflow enters via fin tops under the window. Kerf value is 2.6 % of cell dT | **refuted** as a robust design-around | '330/'284 abstract; `ip_entry_split.py`; draft 3.2 table |
| 2 | '567: "claims revived" (listed as Split-Flow) | revived | Fed. Cir. vacated and remanded on "matingly engaged". Claim 1 recites a compliant member engaged with the housing; remand result unverified | **corrected** | CAFC 22-1221 (7 Mar 2024); IPWatchdog; Crowell |
| 3 | '906 "unknown scope" | unknown | 15/462,753, filed 17 Mar 2017, continuation of '284. Claims an inlet passage feeding each microchannel between its ends; a dependent claim has a larger outlet for the central channel. Expiry about 9 Sep 2028 | **corrected** | USPTO PDF '513 front matter; Google family table |
| 4 | Parent family ends 11 Aug 2028 to about mid-2031 | window | Statutory 11 Aug 2028. '906 PTA is about 29 days. '330 PTA unread (bound about Jun 2031). '513 likely has a terminal disclaimer | **confirmed as a bound; likely narrower** | arithmetic in script; Google expiry estimate |
| 5 | CIP claims run to about Feb 2032 plus PTA | Feb 2032 | Date confirmed ('691 filed 21 Feb 2012). The claims read so far need a pump ('878) or a compliant member ('567). '691 and '350 are unread. Three more family members omitted | **corrected** (date right, relevance and list wrong) | gazette US 12,460,878; CoolIT patent list |
| 6 | "Non-US deliveries are not blocked (no foreign counterparts)" | none | TW I606224 (2012 family) live to about 2032 if annuities are paid; DE and JP utility models expired | **refuted** | Google Patents family entries |
| 7 | Memo maps PRISM to "expired Harpole US 5,088,005" | Harpole / TRW | US 5,088,005 = Ciaccio / Sundstrand, fee-expired. Harpole and Eninger (SEMI-THERM 1991) is non-patent literature | **refuted** (citation) | Google Patents US5088005A |
| 8 | Cooligy 6,986,382 / 7,156,159 / 7,104,312 / 7,000,684 expired | expired | '382 shows "Expired - Lifetime" (assignee Vertiv); '684 filed 6 Oct 2003; the others are 2003 filings, status not individually seen | **confirmed ('382); plausible (others)** | Google Patents |
| 9 | Microfabrica 12,255,123: priority Mar 2021, runs to about 2042 | about 2042 | Filed 18 Mar 2022 from a 18 Mar 2021 provisional; granted 18 Mar 2025 | **confirmed** | Justia |
| 10 | Microfabrica position: "distribution, not jet cooling"; fallback offset ≥ 0.4 mm puts jets on the grate lip | low risk | The draft's model credits kerf-floor impingement; the gaps are inside the 15-300 µm range; the 0.4 mm offset lands jets on fin tips | **refuted** (fallback geometry) | draft 2.2/3.2; `cell2d.py` h_floor_in; USPTO text |
| 11 | JetCool / Flex numbers | as listed | 11,018,077 and 11,594,470 are assigned to MIT (licensed); 11,191,184, 11,277,937 and 12,432,878 are JetCool | **confirmed** (assignee nuance) | Golden/Justia; gazette |
| 12 | "CoolIT enforces competently" | yes | Sued Asetek on Split-Flow (D. Del. 2014); counter-asserted '330/'284/'266 (N.D. Cal. 2019-22, claim construction orders 2020-21); '200 survived IPR (2020); won the '567 appeal (2024) | **confirmed, and stronger than stated** | DCD; CourtListener; electronics-cooling |
| 13 | FTO budget US$80-140k for about 12 families | US$80-140k | at least 20 US patents in at least 9 families, plus TW. Charts and formal opinions are likely about US$150-250k [background knowledge] | **corrected** | count in section 5 |

## 3. The kerf design-around under stress

**Literal reading.**

- CoolIT will define "microchannel" by the *flow passage* between adjacent fins, not by the fin segment. Under that reading, the passage from one outlet window to the next is 12 mm long and continuous across the open kerf.
  - The 1.2 mm window in the floor grate, together with the kerf, forms "an elongate inlet opening" in the middle 20 % of that passage, which is '330 dependent claim 3.
  - Outlet windows lie "adjacent" to each end.
- Even if the segment reading is adopted, the window overhangs 0.45 mm of fin tips on each side of the kerf (7.9 % of a 5.7 mm segment, 75 % of the window area). That is an opening in a plate over the channel between its ends.
- '513's independent claim recites walls defining microchannels, an elongate inlet between the ends, **a plate and seal separating the inlet path from the outlet paths**, opposed sub-flows, and a housing with ports. Its dependents cover a seal forming part of the plate and a plate and seal as a single piece.
  - PRISM's stamped, brazed floor grate, meter sheet and separator are plates, and the braze joints seal. So the "distribution in separate stamped laminations" design-in arguably *supplies* this element rather than avoiding it.
- "Interior outlets only" does not help either. The claims refer to the ends of each microchannel, not to the ends of the fin field.

**Doctrine of equivalents.**

- Function, way and result are the same: a transverse slot over parallel channels divides the flow into opposed sub-flows that halve the path length.
- The draft markets PRISM as removing "split-flow's 54 mm caloric ramp" by doing exactly this at 12 mm pitch.
- The kerf's measured effect is 0.6 K (2.6 %). If the kerfs are dropped (the R1 fallback), the design-around is gone entirely.

**Limits on equivalents, which are the real protection.**

- *Ensnarement* (*Wilson Sporting Goods*, 1990): any equivalent broad enough to cover PRISM must still be patentable over expired art. That art includes Cooligy '382 (interdigitated fingers); Delphi US 7,331,378 (interleaved manifold over microchannels, priority Jan 2006, before CoolIT's Aug 2007 provisional; status to verify); LLNL Bonde US 5,099,311; Walpole US 5,099,910; and Harpole and Eninger 1991.
- Estoppel from amendments and arguments in prosecution, and from patent-owner arguments in IPR2015-01276 (constructions of "spaced from" and "adjacent", and the Kang seal / "direct contact" dispute), may narrow the claims further. None of it has been read.

**Our own admissions.** Section 2.1 of the draft says the kerfs let coolant "enter each fin segment over its full height". The proposed filing 1 would put that into a public patent record. Written that way, it describes the kerf as part of the inlet opening. Filings and marketing must avoid "split", "between the ends" and "halves the path".

**A cheaper, stronger structural fix exists.**

- Narrow the inlet window to the kerf width plus braze tolerance (about 0.3-0.5 mm), so that each segment is fed only through its end face.
- The draft's own `cell2d.py` gives **-0.11 K** for this (−0.21 K with both windows narrowed). It is thermally neutral.
- The cost is a 4x higher downflow velocity in the window and tighter window-to-kerf alignment (±0.05 mm). It also puts the meter jets straight into the kerf, so it must be co-designed with the Microfabrica fix.
- It removes the "opening over the channel between its ends" reading. It does **not** remove the continuous-flow-path reading. Only expiry, invalidity or a licence removes that.

## 4. Other families

- **Microfabrica US 12,255,123.** According to the judges' reading, claim 1 covers a micro cold plate with header inlet and outlet and a "hybrid microjet and microchannel heat transfer array" whose microjets direct fluid onto the primary heat-exchange region. The description gives post-jetting channels of 15-300 µm.
  - PRISM has 0.5 x 0.9 mm orifices at 1.37 m/s, about 4.7 hydraulic diameters of submerged stand-off to the kerf floor, inside the jet's potential core. That is impingement, and the draft's model counts it as such.
  - Risk depends on dimension limits in the claims (whether "micro" sets a size ceiling) and on the parent family (US 9,953,899 and siblings, to about 2036).
  - Fix: discharge the meter sideways or into a settling layer of at least 8-10 hydraulic diameters, and delete the 0.4 mm offset fallback.
- **JetCool / Flex / MIT.** Their claims centre on microjets aimed at the package or die with local returns. PRISM has no per-jet returns and no open cavity, so risk is low to medium, but the families must be charted together with Microfabrica.
- **Intel 12,133,357; Intel 11,804,418; Toyota 11,428,478.** All are live to about 2039-41. Generic manifold-microchannel paths (into the fins toward the base, along the fins, then away) and gridded fin assemblies are close to PRISM. Claim scope is unread. **Add them to the chart.**
- **HUST 12,178,022.** It needs a power module and a zigzag diverter, so it is a low risk for PRISM, but it is prior art against filing 2.
- **Not verified in this run:** Purdue HMMC (two-phase vapor-venting US 12,550,296 surfaced), IBM Zurich, Mikros/Jabil, Alloy Enterprises.
- **2024-26 filings by Nvidia, Delta, AVC, Cooler Master, Jentech or Auras:** none found matching manifold microchannels with skived fins. Unpublished applications filed after about Apr 2025 cannot be seen yet.
- **Continuation threat.** CoolIT files continuations serially ('330 → '284 → '906 → '513; '691 → … → '878). After a full OCP disclosure in 2027, it could draft new claims against PRISM in any still-pending child, within the 2008 or 2012 specification and their 2028 or 2032 terms. Check for pending children.

## 5. The proposed filings (section 9.2)

| # | Filing | Closest art | Assessment |
|---|---|---|---|
| 1 | Tied, kerfed skived manifold plate, recessed window, stamped meter off the braze plane | Cooligy '159/'382; Toyota '478 (gridded fins); Intel '418; cross-cut skived fins (the draft calls this "established practice"); brazed plate-fin ties; PKU 2025 | Novel only as a narrow combination with numeric limits (kerf/window ratio, orifice-to-braze clearance ≥ 0.35 mm, meter/header head ratio ≥ 6). Detectable by teardown. Easy to design around. Low to medium value; mind the admissions risk |
| 2 | Flux-graded flow length (4-12 mm by zone flux) | Cooligy '312 (expired); Toyota 11,149,937 (graded MMC, fee-expired); HUST '022; Corintis; own PSM-12 slit-pitch zoning | **Anticipated or obvious.** A selection "rule" also risks rejection under 35 USC 101. Publish defensively instead |
| 3 | Pressurised-flatness tie screen plus infrared flow fingerprint | infrared and flow inspection of heat exchangers; proof-test metrology | Only infringed inside a competitor's factory, so it cannot be enforced against offshore makers. Patenting requires enabling disclosure, which conflicts with "kept as trade secrets in detail". **Keep it as a trade secret** |
| 4 | Filtration ladder, gap ≥ 3x the absolute filter rating | bridging and filtration rules of thumb; OCP and vendor guidance | Obvious. A system claim would be infringed by customers. Publish in OCP |
| 5 | Defensive publication of the TTV proxy method | — | Fine. First clear Nvidia US 12,446,195 for our own TTV |

## 6. Risk table (US unless stated)

| Family | Live through | Literal | DOE | Invalidity strength | Overall before mitigation | After recommended mitigation |
|---|---|---|---|---|---|---|
| Split-Flow 2008: '330, '284, '906, '513 | about Aug-Sep 2028 (+ '330 PTA ≤ Jun 2031) | **Medium-high** | High, limited by ensnarement | Medium (MMC art already argued in IPR2015-01276; claims survived in part) | **High** for US sales before expiry | Medium-low (narrow window, opinion, post-expiry launch) |
| 2012 family: '567, '691, '820, '266, '597, '350, '878 | about Feb 2032 (+ PTA) | Low on the claims read (pump, compliant member); unknown for '691/'350/'820/'597 | Low-medium | Medium ('567 and '266 have IPR history) | Medium (unknown) | Low if charts clear |
| TW I606224 | about Mar 2032 (Taiwan manufacture) | unknown | — | — | **Medium** for Group-A manufacture | chart via TIPO |
| Microfabrica 12,255,123 + 2016 family | 2042 / 2036 | **Medium-high** | Medium | Medium (Sung & Mudawar, IBM Parida) | **High** | Medium-low (redesign the meter discharge) |
| JetCool / MIT / Flex | 2037-45 | Low-medium | Low | Medium | Medium | Low |
| Intel '357 / '418; Toyota '478 | 2039-41 | unknown (close) | Medium | unknown | **Medium** | chart |
| CoolIT compliant member ('886 / '733) on T3 | about 2040 | Low (spring-screw gimbal) | Low | Medium (IBM TCM) | Low | Low |
| Unpublished CoolIT / Nvidia / Group-A applications | 2045+ | unknown | — | — | Medium | monitor |

## 7. Recommended FTO plan

1. **Weeks 0-2 (internal, about US$5k).** Pull complete claims, file wrappers, PTA and terminal disclaimers for:
   - '330 (including the IPR2015-01276 final written decision and the Feb 2018 certificate), '284, '906 and '513;
   - all seven 2012-family patents, including the '567 remand status (IPR2020-00747/-00825) and the '266 decision;
   - TW I606224 claims and annuity status;
   - the N.D. Cal. 3:19-cv-00410 claim construction orders (Docs 149 and 258).

   Then check Patent Center for pending continuations, and verify the expiry of Delphi '378 and the Cooligy patents.
2. **Before design freeze.**
   - Narrow the inlet windows to the kerf (-0.1 K).
   - Make the kerfs mandatory: drop the no-kerf R1 fallback for US SKUs, or tie it to post-expiry sales.
   - Redesign the meter discharge to stay outside the Microfabrica claim; delete the 0.4 mm offset fallback.
   - Rewrite the prior-art memo around Cooligy '382, Delphi '378, Bonde '311, Walpole and Harpole 1991, framed as invalidity and ensnarement evidence.
3. **Weeks 2-8 (outside counsel, about US$150-250k).** Claim charts and opinions on the frozen CAD and its variants (R, P, G-zoned, T3) against every row in section 6. A formal opinion also serves as the defence to willfulness (*Halo*, 2016).
4. **Commercial.**
   - No US offers, sales or US-site evaluation units of PRISM before the opinion. US law has no research exemption for commercial evaluation, so pre-expiry US demos are infringing acts even if damages are small.
   - Plan the US launch on or after **10 Sep 2028**, or later if the '330 PTA is longer.
   - Taiwan manufacture waits on the TW I606224 chart.
   - Budget for IP indemnity to hyperscalers and Nvidia partners, or IP insurance. A CoolIT/Ecolab suit (US$3-5M through trial) exceeds what a US$6.6M programme can absorb.
5. **Filings.** Keep filing 1 (narrow) and filing 5. Turn filings 2 and 4 into defensive publications. Keep filing 3 as a trade secret. Draft every filing without "split" language.

## Sources

- CAFC, *CoolIT v. Vidal*, 22-1221 (7 Mar 2024): https://cafc.uscourts.gov/opinions-orders/22-1221.OPINION.3-7-2024_2282155.pdf ; https://ipwatchdog.com/2024/03/08/federal-circuit-reverses-ptab-claim-construction-reviving-cooling-patent/id=174182/ ; https://www.crowell.com/en/insights/client-alerts/patent-counsel-do-your-patents-claim-engagement-of-components-as-intended
- Split-Flow family: https://patents.google.com/patent/US8746330B2/en ; https://patents.google.com/patent/US9603284B2/en ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12495513 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12101906 ; https://patents.google.com/patent/US12101906 ; https://patents.google.com/patent/US20210045262A1
- 2012 family: https://patentsgazette.uspto.gov/week44/OG/html/1540-1/US12460878-20251104.html ; https://www.coolitsystems.com/patents/ ; https://patents.google.com/patent/TWI606224B/en ; https://patents.google.com/patent/DE202012002974U1/en ; https://patents.google.com/patent/JP3179086U/en
- Litigation and IPR: https://www.courtlistener.com/opinion/9601660/asetek-danmark-as-v-coolit-systems-inc/ ; https://ptacts.uspto.gov/ptacts/public-informations/petitions/1462205/download-documents?artifactId=XWNK-IwOLHOfj0IrvNHwfX8Z76YXprRiedj5bSYh-whz9Dth4nbN8rI ; https://ai-lab.exparte.com/case/ptab/IPR2015-01276/doc/16 ; https://bit-tech.net/news/tech/cooling/coolit-split-flow-asetek/1/ ; https://www.datacenterdynamics.com/en/news/coolit-wins-patent-suit-brought-by-danish-cooling-firm-asetek/ ; https://www.electronics-cooling.com/2020/10/coolit-prevails-against-asetek-ptab-determines-no-challenged-claims-unpatentable/ ; https://www.docketalarm.com/cases/PTAB/IPR2020-00825/Asetek_Danmark_A-S_v._CoolIT_Systems_Inc/10-12-2021-Board/Final_Written_Decision__original-50-Final_Written_Decision__original/
- Prior art: https://patents.google.com/patent/US5088005 ; https://patents.google.com/patent/US6986382 ; https://patents.google.com/patent/US7331378 ; https://patents.google.com/patent/US5099311 ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5099910
- Other live art: https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12255123 ; https://patents.justia.com/assignee/microfabrica-inc ; https://patents.google.com/patent/US11428478 ; https://patents.google.com/patent/US11149937 ; https://patents.google.com/patent/US12178022 ; https://patentsgazette.uspto.gov/week44/OG/html/1527-5/US12133357-20241029.html ; https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11804418 ; https://golden.com/wiki/US_Patent_11018077_Modular_microjet_cooling_of_packaged_electronic_components-3VDGAEA ; https://patentsgazette.uspto.gov/week39/OG/html/1538-5/US12432878-20250930.html
