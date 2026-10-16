# Gap report: is US 12,495,513 a Split-Flow continuation, what do the CoolIT claims recite, and are the Cooligy / Purdue / IBM manifold families live?

*Angle: freedom-to-operate pre-screen for the recommended multi-slot manifold-microchannel architecture (zoned GPU/HBM feeds, stepped bare-die variant) against CoolIT's Split-Flow family (US 8,746,330 / 9,603,284 / 12,495,513), US 12,101,906, the compliant-member family (US 11,725,886 / 12,188,733), the Cooligy manifold/hot-spot families (US 7,104,312 / 7,156,159 / 7,000,684) and the Purdue HMMC / IBM Zurich MMC filings. Compiled 2026-10-13. Not a legal opinion.*

## 0. Evidence status - read first

- **Web searches performed in this run: 0.** Six WebSearch calls were attempted (US12495513B2 continuation; US9603284B2 claims; US8746330B2 claim 1; US12101906B2; US12188733/US11725886 compliant member; US7104312 Cooligy expiry); all six were refused because the workflow turn's shared 200-search budget was already exhausted. One WebFetch of patents.google.com/patent/US12495513B2 was attempted and failed on DNS (`getaddrinfo ENOTFOUND patents.google.com`); per instructions no further network attempts were made.
- Consequently **no patent claim text, continuity data, PTA, terminal-disclaimer, PTAB or INPADOC family record was retrieved in this run.** Everything below is either (a) sibling-sourced with a URL [S], (b) derived arithmetic [D], or (c) author background knowledge to mid-2026 at stated confidence [KB-H / KB-M / KB-L]. Each KB item is paired with the exact lookup that confirms or kills it (section 7).
- What this report adds over `ip-landscape.md`: (i) a date/term analysis that bounds the Split-Flow family's expiry at **Aug 2028 to ~mid-2031** rather than "~Aug 2028"; (ii) a claim-reading analysis showing that "use two or more inlet slots" is **not by itself a safe design-around** of an open-ended split-flow claim, and what is; (iii) the likely IPR history of the '330 patent, which changes which CoolIT patent actually matters; (iv) an expired-prior-art shield (Cooligy interwoven manifolds, Harpole, IBM TCM pistons) that is the real FTO backbone for the multi-slot and stepped-contact features; (v) a jurisdiction view for TW/CN/VN manufacture.

## 1. Bottom line

| Question | Best answer today | Confidence | What settles it |
|---|---|---|---|
| Is US 12,495,513 a true continuation of the Aug-2008 Split-Flow family? | **Almost certainly yes.** It carries the parent's exact title "Fluid heat exchanger configured to provide a split flow" (a continuation keeps the parent's specification and normally its title; a fresh 2020s filing would carry a new title) and it issued ~23 Dec 2025 [D from number], which fits a chain of serial continuations kept co-pending since '284 issued in Mar 2017. CoolIT uses exactly this practice elsewhere ('886 -> '733). | KB-M + [D] | Patent Center "Continuity" tab for 12,495,513; Google Patents "priority/continuation" line; expect "continuation of 14/283,163 ... continuation of 12/189,476". |
| Expiry of the family | **Not before 11 Aug 2028; not after ~mid-2031.** 20 years from the 11 Aug 2008 non-provisional filing = 11 Aug 2028 [D]. The '330 patent took 2,129 days to issue (filed Aug 2008, granted 10 Jun 2014 [S insideHPC]); up to 1,034 days of "B-delay" PTA is arithmetically possible, less applicant delay and any RCE time, so the '330 term could run to 2029-2031. '284 and '513 almost certainly carry terminal disclaimers to '330 and cannot outlive it. | [D] for bounds; KB-M on TDs | Patent Center: '330 PTA figure on the front page / "Adjustments" tab; TD entries in '284 and '513 file wrappers. |
| What do the independent claims recite? | '330: a lidded heat exchanger with a fin field; an inlet opening in the manifold positioned over the microchannels **between their ends** so the flow **splits into opposing directions**, with outlet passages collecting from the channel ends [KB-M on concept, KB-L on wording; see 2.2]. '284: same disclosure, re-claimed; wording unknown here. '513: unknown; two scenarios in 2.2. **None of the three can claim zoned GPU/HBM feeds or multi-slot manifolds unless the 2008 specification discloses them, which (KB-L) it does not.** | KB-M / KB-L | Read the three claim sets (Google Patents or image-ppubs PDFs already linked by siblings). |
| Does our architecture read on it? | **Possibly, if a claim is as broad as "an inlet opening between the ends causing split flow":** in a manifold-microchannel plate every inlet slot sits between the ends of a continuous skived channel and splits the flow. "Comprising" + "an" = one or more, so adding slots does not avoid such a claim. What avoids it is (i) limitations CoolIT had to add to get past multi-slot prior art (Cooligy interwoven manifolds, Harpole MMC), (ii) structural differences we should design in (segmented fins, interior outlets, no end-of-channel outlets), and (iii) the fact that our design practises **expired** Cooligy/Harpole art, which invalidates any claim that would read on it. See section 4. | KB-M (law), KB-L (claim wording) | File-wrapper review of 12/189,476, 14/283,163 and the '513 application; claim chart against our CAD. |
| Compliant-member family (11,725,886 / 12,188,733) vs our stepped bare-die contact | A **rigid stepped base** is not a "compliant member". Risk appears only if we add spring-loaded floating pedestals between the core and housing; even then, IBM TCM spring-loaded pistons (US 3,993,123, 1976) and 2021-2024 bare-die plates are prior art. Priority date of the family is unknown (sibling guessed 2020-21; a 2011-13 modular-systems root is also plausible, KB-L). | KB-M | Read '886 claim 1; Continuity tab for its earliest priority. |
| US 12,101,906 "Fluid heat exchanger" | Issued ~24 Sep 2024 [D]. Priority and claims unknown; could be the "zoned"/current-product filing. **Highest-priority unknown.** | none | Read claims; Continuity tab. |
| CA/CN/TW/EP counterparts of Split-Flow | **Probably none** for the 2008 family (small-company US-only filing; no PCT recalled) [KB-L]. Later CoolIT families (2017+) do have PCT/CN filings in some cases [KB-L]. | KB-L | Espacenet INPADOC family of US 8,746,330 (or its A1 publication). |
| Cooligy US 7,104,312 / 7,156,159 / 7,000,684 | **Expired** (2003 filings -> mid/late 2023; many lapsed earlier for fees). Interwoven-manifold US 6,986,382 (2003) also expired ~May 2023. Portfolio went Cooligy -> Emerson Network Power (2005) -> Liebert/Vertiv (2016) [KB-L on current holder]. Expired status does not depend on owner. | KB-M | Google Patents "status: expired" line; USPTO maintenance-fee records. |
| Purdue HMMC, IBM Zurich MMC | Purdue (Weibel/Garimella/Drummond, DARPA ICECool, 2015-2019 filings) would run to **2035-2039** if granted - numbers not known here; claims (if any) are die-embedded silicon HMMC, two-phase, with specific hierarchical manifold geometry. IBM Zurich (Escher/Michel/Brunschwiler, 2008-2011 filings) would run to **2028-2031** if maintained; IBM lapses aggressively [KB-M]. Neither is likely to read on a copper skived-fin plate with an etched manifold layer, but both must be checked. | KB-L / KB-M | Google Patents: assignee "Purdue Research Foundation" + "manifold microchannel"; assignee IBM + inventor Escher/Michel/Brunschwiler 2008-2012. |

## 2. CoolIT Split-Flow family

### 2.1 Chain and dates

| Patent | Application / filing | Grant | Term basis | Expected expiry | Status notes | Source / confidence |
|---|---|---|---|---|---|---|
| US 8,746,330 B2 "Fluid heat exchanger configured to provide a split flow" (Lyon) | 12/189,476, filed 11 Aug 2008 (provisional Aug 2007 - does not count for term) | 10 Jun 2014 | 20 y from 11 Aug 2008 = **11 Aug 2028** + PTA (0 to ~1,034 days) | **11 Aug 2028 to ~mid-2031** | Listed on CoolIT's marking page [S]. Counter-asserted by CoolIT against Asetek (2019-22) and, by recollection, challenged in an Asetek IPR with a Federal Circuit appeal (*CoolIT Systems v. Vidal*, 2024) - see 2.3 | [S] patents.google.com US8746330B2; insidehpc 2014; coolitsystems.com/patents. Day-of-month and PTA bound [KB-M]/[D] |
| US 9,603,284 B2 (continuation) | 14/283,163, filed ~20 May 2014 (before '330 issued, so co-pending) | ~21 Mar 2017 | Same 2008 clock; almost certainly terminally disclaimed to '330 | Same as '330 | Also counter-asserted vs Asetek [KB-M]; IPR status unknown | [S] patents.google.com US9603284B2; dates [KB-M] |
| (intermediate continuation(s), 2017-2024) | Unknown serial(s); must have been filed before 21 Mar 2017 and kept co-pending | - | - | - | Required for '513 to be a continuation; existence inferred, not seen | [D] inference |
| US 12,495,513 B2, same title | Unknown serial; filed 2022-2024 as a continuation (inferred) | **~23 Dec 2025** [D from number interpolation, +/- 2 weeks] | If continuation: 2008 clock + TD -> same as '330. If a new filing (title reuse would be unusual): 2042-2044 | **Same as '330 (likely)** | Sibling found it on image-ppubs.uspto.gov; title identical to '330 [S] | [S] number/title; [D] date; [KB-M] continuation |

Grant-date interpolation anchors: US 12,000,000 issued 4 Jun 2024 (USPTO milestone, KB-H) and US 12,188,733 issued 7 Jan 2025 (gazette URL week01/.../US12188733-20250107 [S]); implied rate ~6,090 patents/week; this reproduces the sibling's "Sep 2024" for 12,101,906 (estimate 24 Sep 2024) and gives 23 Dec 2025 for 12,495,513.

### 2.2 What the independent claims recite (best available characterisation)

**US 8,746,330 (KB-M on substance, KB-L on wording).** The claims are apparatus claims to a heat exchanger comprising: a housing/manifold body defining inlet and outlet passages; a heat sink with a base and a plurality of fins defining microchannels having first and second (opposed) ends; an inlet opening (a transverse slot in the manifold) positioned over the microchannels **at a location between the first and second ends** so that fluid entering the microchannels **splits**, a first portion flowing toward the first ends and a second portion toward the second ends; and outlet passage(s) in fluid communication with the microchannels at or near those ends. One limitation recalled from the Federal Circuit appeal is that the heat sink is "matingly engaged" with the housing/manifold (the construction of that phrase was the appeal issue). Dependent claims (KB-L) include the slot offset from the channel midpoint (biasing flow to a hotter region), fin pitch/height ranges, and an integrated pump.

**US 9,603,284 (KB-L).** Same 2008 specification. Continuation claims typically broaden one axis (e.g. drop "matingly engaged", recite "an opening" rather than "a slot", or add "a plurality of fins arranged in a first region and a second region"). Wording not recalled; must be read.

**US 12,495,513 (unknown).** Two scenarios:

| Scenario | What the claims would look like | Consequence for us |
|---|---|---|
| A (likely): continuation claims re-drafted after the Asetek IPR art to secure what survived | Narrower structural claims: slot geometry relative to fins, housing/manifold engagement, outlet placement at fin-field ends, maybe pump integration | Expires with '330 (<= ~2031); our interior-outlet, segmented-fin manifold design is distinguishable; low risk |
| B (possible): claims drafted toward current products - "a plurality of inlet openings" or "first and second fin regions each with its own split-flow inlet" | Only valid to the extent the 2008 spec supports it (written-description limit of a continuation). A multi-slot or zoned claim issued on a 2008 spec that shows a single slot would be vulnerable under 35 USC 112(a), and in any case is anticipated by Cooligy US 6,986,382 (interwoven manifolds, 2003) and Harpole US 5,088,005 (1992) | Still expires <= ~2031; invalidity defences strong; but literal-infringement exposure in the US until then -> needs a formal claim chart before US sales |

Decision rule: if the '513 Continuity tab shows "continuation of 12/189,476", the clock is fixed and the only questions are claim wording and the '330 PTA. If it shows a 2020s priority with no link to 12/189,476 (unlikely), treat it as a 2040s patent and read it as the primary blocking reference.

### 2.3 Likely IPR history (unverified recollection - changes which patent matters)

In *Asetek Danmark A/S v. CoolIT Systems* (N.D. Cal., filed 2019; global settlement Oct 2022 [S DCD/insideHPC]), CoolIT counter-asserted a set of its own patents that, by recollection, included US 8,746,330, 9,603,284, 9,057,567, 9,453,691 and 10,274,266 [KB-M on the set, KB-L on individual numbers]. Asetek petitioned for inter partes review of CoolIT's counter-asserted patents in 2020 [KB-M]. CoolIT appealed at least one adverse PTAB final written decision; the Federal Circuit decided *CoolIT Systems, Inc. v. Vidal* (non-precedential, 2024), which by recollection concerned the '330 patent and the Board's construction of "matingly engaged" [KB-L on patent identity; KB-L on outcome, leaning "affirmed unpatentability of the challenged claims"].

Why this matters: if the challenged '330 claims were cancelled, (a) the "patented Split-Flow" that CoolIT markets in the June 2026 brief rests on '284 and the newly issued '513, (b) the '513 claims were almost certainly drafted around the IPR prior art (so they are narrower and more structural, favouring scenario A), and (c) the IPR record itself is a ready-made invalidity/claim-construction map for us (the art Asetek used is public). Lookups: PTAB P-TACTS search "CoolIT" (patent owner) for 2020 petitions; the '330 and '284 records on Patent Center for an IPR certificate; the Fed. Cir. opinion text (cafc.uscourts.gov, "CoolIT v. Vidal").

### 2.4 PTA and terminal-disclaimer arithmetic

- '330 pendency 2,129 days; three-year B-delay threshold exceeded by 1,034 days [D]. Realistic PTA is lower (applicant response delays and any RCE period are deducted); typical for a 2008-2014 case: 300-900 days [KB-M]. **Plan for a US expiry window of Aug 2028 to mid-2031 until the Patent Center figure is read.**
- '284 and '513 as continuations with overlapping claims would have terminal disclaimers to '330; a TD disclaims any term beyond the reference patent's expiry, so neither outlives '330 even if '330's claims were cancelled in an IPR (the disclaimer references the expiry date, not the claims) [KB-M].
- Maintenance fees: '330 (3.5 y 2017, 7.5 y 2021, 11.5 y due ~Dec 2025-Jun 2026); '284 (11.5 y due ~2028). CoolIT markets the family, so lapse is unlikely, but the 11.5-year fee status of '330 is a two-minute check.

### 2.5 Foreign counterparts (CA / CN / TW / EP / VN)

- 2008 Split-Flow family: no PCT or foreign filing recalled; CoolIT was a small Calgary company filing in the US only at that time [KB-L]. A Canadian counterpart is the only plausible one. If confirmed absent, **manufacture in Taiwan, China or Vietnam carries no Split-Flow risk; US importation does** (district court or ITC Section 337 exclusion, which an Ecolab-owned CoolIT [S: $4.75 B, closed July 2026] can afford).
- Post-2015 CoolIT families: some have WO/CN/TW publications (coldplate assemblies, leak detection, couplings) [KB-L]. The ones that matter for us are whatever '906 and the '886 family are; check their INPADOC families, and run an assignee search on TIPO (Taiwan) and CNIPA for "CoolIT Systems" / "酷利特" style transliterations.
- Vietnam: no CoolIT VN filings expected [KB-L]; VN risk is negligible for the plate; verify once if Vietnam is the final assembly site.

## 3. The other two CoolIT families

| Family | What is known | What it would cover | Our exposure | Source / confidence |
|---|---|---|---|---|
| US 11,725,886 -> US 12,188,733 "Modular fluid heat exchange systems", compliant member | '733 issued 7 Jan 2025, continuation of '886 [S gazette]. Priority unknown: sibling guessed ~2020-21 (expiry ~2040-41); the title echoes CoolIT's 2011-2013 "modular heat-transfer systems" filings, so a 2011-13 root (expiry 2031-33) is plausible [KB-L] | A heat-exchanger core carried in a housing with a compliant member (spring/elastomer) urging the core toward the heat source or sealing it, allowing float/tolerance take-up [KB-L from gazette abstract as relayed] | Rigid stepped base: none. Spring-loaded independent HBM pedestals: possible literal overlap; invalidity shield = IBM TCM pistons US 3,993,123 (1976, expired), 1980s-90s multi-chip-module spring contacts, and 2021-24 bare-die TPU/GB200 plates | [S] + [KB-L] |
| US 12,101,906 "Fluid heat exchanger" | Issued ~24 Sep 2024 [D]. Nothing else known | Candidates: (a) another Split-Flow continuation with a new title (would show 12/189,476 in Continuity); (b) a 2021-23 filing on the current zoned GPU/HBM plates (expiry 2041-43); (c) a continuation of the 2011-12 "fluid heat exchange systems" family (expiry 2031-32) | Unknown; if (b) it is the single most important patent to read | [S] number only |

## 4. Claim-reading analysis: does a multi-slot zoned manifold read on Split-Flow?

1. **Open-ended claims.** US claims use "comprising"; "a"/"an" in such a claim means "one or more" (*Baldwin Graphic Systems v. Siebert*, Fed. Cir. 2008; *KCJ Corp. v. Kinetic Concepts*, 2000) [KB-H]. A claim reciting "an inlet opening positioned between the first and second ends of the microchannels such that fluid splits into opposing directions" is literally met by a plate with three, five or nine such openings, **provided the other limitations are met**. The earlier IP report's "N >= 2 slots is the obvious design-around" is therefore incomplete.
2. **Where the real distinctions sit.** In a manifold-microchannel plate (our architecture) the outlet slots are interior and interdigitated with the inlet slots; fluid never reaches the "first end" or "second end" of the fin field. If the '330/'284/'513 claims recite outlets "at the first and second ends" or "end manifolds", a segmented-fin, interior-outlet design does not literally infringe, and doctrine-of-equivalents reach is limited by whatever CoolIT argued to distinguish Cooligy's interwoven manifolds and Harpole's MMC during prosecution (prosecution-history estoppel; *Festo*). **Action: pull the file wrappers and read every office-action response for how CoolIT characterised multi-slot art.**
3. **Practising expired prior art.** The strongest shield is to make our manifold squarely an embodiment of expired art: Harpole US 5,088,005 (TRW, filed May 1990, granted Feb 1992, expired ~May 2010 [D]); Cooligy US 6,986,382 "Interwoven manifolds for pressure drop reduction in microchannel heat exchangers" (filed ~May 2003, expired ~May 2023 [D/KB-M]); Cooligy US 7,156,159 "Multi-level microchannel heat exchangers" (filed ~Jul 2003, expired ~Jul 2023); Walpole US 5,099,910 (alternating counter-flow, expired ~2011). A claim that reads on this art is invalid ("that which infringes if later, anticipates if earlier"). Document the mapping in the design file now (a dated engineering memo mapping each slot/outlet feature to the specific figure of the expired patent). This also protects the zoned-feed feature: Cooligy US 7,104,312 (hot-spot-targeted delivery, filed ~Oct 2003, expired ~Oct 2023) and 7,000,684 (vertical fluid delivery, expired ~Oct 2023) disclose routing more coolant to hotter regions and vertical manifold feeds.
4. **Design-in differentiators that cost nothing thermally** (choose at the CAD stage, before any CoolIT claim is read, so they are not "after-the-fact"): (a) fins segmented at each outlet slot, not one continuous field; (b) all outlets interior - no collection at the fin-field ends; (c) manifold distribution in a separate etched laminate, not in the housing; (d) zone separation by a solid rib with independent inlet feeds; (e) rigid stepped base for bare-die, no spring members between core and housing.
5. **Calendar.** First production shipments of the recommended design are 2028 or later; the Split-Flow family expires between Aug 2028 and ~mid-2031. A US launch before expiry needs the claim chart; a launch after it needs nothing for this family. Price the difference: a US-only delay versus an opinion letter (US$25-60 k for a three-patent chart + opinion [KB-M]).

## 5. Cooligy, Purdue, IBM Zurich, Corintis - status table

| Family | Filing / grant | Expected status Oct 2026 | Relevance | Confidence |
|---|---|---|---|---|
| Cooligy US 7,104,312 "flexible fluid delivery for cooling desired hot spots" | filed ~Oct 2003; granted Sep 2006 | **Expired** (~Oct 2023; may have lapsed earlier) | Prior art for power-map-tailored channel density and zoned feeds - shields us, limits what we can claim | KB-M |
| Cooligy US 7,156,159 "Multi-level microchannel heat exchangers" | filed ~Jul 2003; granted Jan 2007 | **Expired** (~Jul 2023) | 3-D manifold over microchannels = our layered manifold | KB-M |
| Cooligy US 7,000,684 "efficient vertical fluid delivery" | filed ~Oct 2003; granted Feb 2006 | **Expired** (~Oct 2023) | Vertical slot feeds into a channel/pin field | KB-M |
| Cooligy US 6,986,382 "Interwoven manifolds" | filed ~May 2003; granted Jan 2006 | **Expired** (~May 2023) | Alternating inlet/outlet slots - the direct anchor for our multi-slot layout | KB-M |
| Cooligy US 6,988,534 (hot-spot delivery, sibling of '312), US 7,017,654 (channel forming), US 7,021,369 (hermetic loop), US 7,188,662 (fluid delivery), US 7,836,597 (high surface/volume structures) | 2003-2005 filings | Expired 2023-2025 (last ~2025) | Fabrication and loop claims | KB-L |
| Cooligy portfolio owner | Cooligy -> Emerson Network Power (Dec 2005) -> Liebert/Vertiv (2016 spin-out) | Irrelevant to expired items; relevant only if any post-2006 continuation exists (none recalled) | - | KB-L |
| Purdue Research Foundation HMMC (Weibel, Garimella, Drummond, Peroulis; DARPA ICECool) | 2015-2019 filings; grants unknown | Live to 2035-2039 if granted and maintained | Hierarchical manifold + silicon microchannels etched in the die, two-phase HFE-7100; claims (if any) tied to die-embedded geometry | KB-L |
| Purdue/Garimella 3-D manifold embedded cooling for SiC (Jung 2019) | ~2017-2019 filings, if any | Live to 2037-2039 if granted | Only for a module-integrated (wetted-baseplate) SiC SKU | KB-L |
| IBM Zurich MMC "ultra-thin heat sink" (Escher, Michel, Brunschwiler, Poulikakos) | 2008-2011 filings | Live to 2028-2031 only if maintained; IBM lapses many | Silicon MMC with specific manifold/channel ratios; unlikely to read on a copper skived plate | KB-M |
| Corintis (EPFL spin-off) WO/EP/US 2022-2025 | 2022-2025 | Live to 2042-2045 | AI/bio-inspired, heat-map-matched in-silicon channel topologies; our skived variable-pitch fins are a different structure and sit on expired Cooligy '312 art | [S] funding/partnership; claims [KB-L] |
| IBM TCM US 3,993,123 "Gas encapsulated cooling module" (Chu, Hwang, Simons) | 1976 | Expired ~1993 | Spring-loaded per-chip pistons = prior art for any "compliant member" contact claim | KB-M |

## 6. Recommended FTO plan (ranked, with cost/time)

1. **Week 1, free, 2 hours:** Patent Center Continuity tabs for 12,495,513, 12,101,906, 11,725,886; PTA figure for 8,746,330; TD entries; maintenance-fee status; PTAB P-TACTS "CoolIT" 2020 petitions and any IPR certificates. This resolves the expiry window and the IPR hypothesis.
2. **Week 1-2, free:** read the independent claims of all six CoolIT patents and the 2008 specification's figures; note whether any figure shows more than one inlet slot or more than one fin region (written-description ceiling for '513).
3. **Week 2-3:** Espacenet INPADOC families for US 8,746,330, 11,725,886, 12,101,906; TIPO and CNIPA assignee searches for CoolIT; VN check only if Vietnam is the assembly site.
4. **Week 3-6, US$25-60 k:** outside counsel claim chart of our frozen manifold CAD against '284, '513, '906 and '886/'733 plus an opinion letter; include the prior-art mapping memo (Harpole, Cooligy '382/'159/'312/'684, Walpole, IBM TCM) as an invalidity backstop.
5. **Before any disclosure:** file provisionals on the specific skived-core + etched-manifold laminate + weld stack, the zoned-feed rib and port layout, the stepped bare-die base, and the pitch-modulation process - all narrower than the expired Cooligy concepts.
6. **Monitor:** Google Patents alert for assignee "CoolIT Systems" and "Ecolab" with CPC H01L 23/473, F28F 3/12, H05K 7/20; OMNI-related applications filed 2023-24 publish 2025-26.

## 7. Verification checklist (exact lookups)

| Item | Where | What to record |
|---|---|---|
| '513 continuity chain | patents.google.com/patent/US12495513B2 ("Priority"/"Application" lines); Patent Center > 12495513 > Continuity | Each "continuation of" serial back to 12/189,476; filing date of the '513 application |
| '330 PTA, TD, fees | Patent Center > 8746330 > front page ("(*) Notice: ... extended or adjusted under 35 U.S.C. 154(b) by N days") and Fees tab | N days; 11.5-y fee paid?; expiry = 11 Aug 2028 + N |
| '284 / '513 TDs | Patent Center file wrappers > "Terminal Disclaimer" documents | TD reference patent and date |
| IPR history | ptacts.uspto.gov search patent 8746330 / 9603284; cafc.uscourts.gov "CoolIT v. Vidal" | Petition numbers, instituted claims, FWD outcome, certificate |
| Claims | Google Patents or image-ppubs.uspto.gov PDFs (links in Sources) | Verbatim independent claims of '330, '284, '513, '906, '886, '733 |
| Foreign families | worldwide.espacenet.com INPADOC family for US8746330, US11725886, US12101906; TIPO (twpat) and CNIPA assignee "CoolIT" | Country codes, status (granted/pending/lapsed) |
| Cooligy status | Google Patents status line for US7104312, US7156159, US7000684, US6986382; USPTO maintenance-fee records | "Expired" + lapse reason/date; current assignee |
| Purdue / IBM | Google Patents assignee:"Purdue Research Foundation" inventor Weibel OR Garimella "manifold"; assignee IBM inventor Escher OR Michel OR Brunschwiler 2008-2012 | Numbers, claim 1, status |

## Key numbers

| Item | Value | Source | Confidence |
|---|---|---|---|
| Split-Flow earliest non-provisional filing | 11 Aug 2008 (app 12/189,476) | [S] Google Patents US8746330B2 (month/year); day [KB-M] | High (month) |
| '330 grant | 10 Jun 2014 | [S] insideHPC Jun 2014 | High |
| Statutory expiry without PTA | 11 Aug 2028 | [D] | High |
| Maximum arithmetically possible '330 B-delay PTA | 1,034 days (-> ~Jun 2031) | [D] | High as a bound; actual likely 300-900 d [KB-M] |
| '284 filing / grant | ~20 May 2014 / ~21 Mar 2017 (app 14/283,163) | [S] app number; dates [KB-M] | Medium |
| '513 issue date | ~23 Dec 2025 (+/- 2 weeks) | [D] number interpolation (anchors 12,000,000 = 4 Jun 2024; 12,188,733 = 7 Jan 2025 [S]) | Medium-high |
| '906 issue date | ~24 Sep 2024 | [D] same method; matches sibling "Sep 2024" | High |
| '733 issue date | 7 Jan 2025 | [S] USPTO gazette URL | High |
| Cooligy '312 / '684 / '159 / '382 expiry | ~Oct 2023 / ~Oct 2023 / ~Jul 2023 / ~May 2023 | [D] from recalled 2003 filing months [KB-M] | Medium |
| Harpole US 5,088,005 expiry | ~May 2010 (later of 17 y from Feb 1992 grant, 20 y from May 1990 filing) | [D]/[KB-M] | Medium |
| IBM TCM US 3,993,123 | 1976, expired ~1993 | [KB-M] | Medium |
| Claim chart + opinion cost | US$25-60 k, 3-6 weeks | [KB-M] | Medium |
| Searches run this task | 0 performed (6 refused; 1 WebFetch DNS failure) | this run | High |

## Gaps / unknowns

1. **Verbatim independent claims of all six CoolIT patents** - nothing was read; every claim characterisation above is recollection or scenario.
2. **'513 continuity data** (the single fact the angle asked for) - inferred from the title and date, not seen.
3. **'330 PTA figure** - sets the family's expiry anywhere from Aug 2028 to mid-2031.
4. **IPR outcome for '330/'284** - the *CoolIT v. Vidal* recollection could be wrong on patent identity or result; if wrong, '330 claims are all live.
5. **US 12,101,906 priority and subject matter** - could be the zoned-plate patent that matters most; completely unknown.
6. **'886/'733 earliest priority** (2011-13 vs 2020-21) and claim 1 text.
7. **Foreign counterparts** - none checked; TW/CN assignee searches not run.
8. **Purdue and IBM Zurich patent numbers** - none recalled with confidence; the sibling physics report cites the papers (Escher 2010; Drummond 2018; Jung 2019), not patents.
9. **Corintis publication numbers** (WO 2023-2025) - not known.
10. **Whether Google (Hot Chips 2025 split-flow TPU plates) licenses CoolIT, holds its own split-flow patents, or relies on expiry** - would indicate how CoolIT polices the family.
11. **Any CoolIT/Ecolab application filed 2023-2026 on OMNI unibody or 15 kW-class plates** - unpublished or unsearched.

## Sources

Sibling-sourced URLs (not re-fetched in this run):
- https://patents.google.com/patent/US8746330B2/en (Split-Flow parent; app 12/189,476; inventor Lyon)
- https://patents.google.com/patent/US9603284B2/en (continuation; app 14/283,163)
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9603284
- https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12495513 (same title as '330)
- https://patents.justia.com/patent/8746330
- https://insidehpc.com/2014/06/coolit-systems-patents-split-flow-heat-exchanger/ (grant, Jun 2014)
- https://www.coolitsystems.com/patents/ (virtual marking; lists 8,746,330)
- https://patentsgazette.uspto.gov/week01/OG/html/1530-1/US12188733-20250107.html (US 12,188,733, 7 Jan 2025, continuation of 11,725,886, compliant member)
- https://coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf and https://www.coolitsystems.com/coldplate-technology/ ("patented Split-Flow")
- https://www.datacenterdynamics.com/en/news/coolit-wins-patent-suit-brought-by-danish-cooling-firm-asetek/ ; https://insidehpc.com/2022/10/coolit-system-district-court-rejects-asetek-patent-claims/ (Asetek v. CoolIT: 2022 SJ, settlement, 2024 Fed. Cir. on Asetek '354)
- https://par.nsf.gov/biblio/10341820 (Kisitu & Ortega, InterPACK 2021 - split-flow independent analysis)
- CoolIT 15 kW Tech Brief, June 2026 (local: appendix/pdf/brief.txt) - "patented Split-Flow architecture"

Lookups to run (URLs are the canonical forms; none retrieved here):
- https://patents.google.com/patent/US12495513B2/en ; https://patents.google.com/patent/US12101906B2/en ; https://patents.google.com/patent/US11725886B2/en ; https://patents.google.com/patent/US12188733B2/en
- https://patentcenter.uspto.gov/applications/ (Continuity, PTA, fees, TDs for 12495513 / 8746330 / 9603284)
- https://ptacts.uspto.gov/ (IPR records, search by patent 8746330 / 9603284)
- https://cafc.uscourts.gov/ (search "CoolIT Systems v. Vidal", 2024)
- https://patents.google.com/patent/US7104312B2 ; US7156159B2 ; US7000684B2 ; US6986382B2 ; US5088005A ; US5099910A ; US3993123A
- https://worldwide.espacenet.com/ (INPADOC family of US8746330B2, US11725886B2, US12101906B2)
- https://twpat.tipo.gov.tw/ and https://pss-system.cponline.cnipa.gov.cn/ (assignee CoolIT Systems)

Background-knowledge items with no URL in this session (verify before external use): the '330 claim wording and "matingly engaged" issue; the set of CoolIT counter-asserted patents; Asetek's 2020 IPR petitions; *CoolIT v. Vidal* (Fed. Cir. 2024) identity and outcome; '284 filing/grant dates; Cooligy filing months and the Emerson/Vertiv chain; Purdue and IBM Zurich filing windows; IBM TCM US 3,993,123; claim-construction case law cited in section 4.
