# Gap report: TIM2 between the GPU package and the cold plate - what NVIDIA/ODMs use, measured impedances, bond line / clamp / flatness windows, liquid-metal and indium reliability, and whether Ni plating is required

Prepared 2026-10-13 for the "beat the CoolIT 15 kW cold plate" programme. Angle: the single largest lever in the benchmark stack is the interface (modelled at 20-50 % of the 34.4 K case-to-inlet budget, and the probable cause of the 10 K plate-to-plate spread at TC8). This report pins down what is actually known, with what confidence, about the TIM2 that will sit between a GB300/Rubin-class package and our plate.

**Source caveat (read first).** No live web search was possible for this agent: all eight planned queries (listed in Section 11) were refused because the per-turn WebSearch budget (200 calls, shared across the workflow) was already exhausted, and the single permitted WebFetch attempt (Honeywell PTM7950 datasheet via caplinq) failed on DNS, as the task warned. Everything below is therefore drawn from (a) numbers and URLs that sibling agents captured earlier in this workflow when search was available, tagged **[V]** (URL-verified by a sibling), **[Sib-snip]** (sibling read it from a search-engine extract only) or **[A]** (analyst/trade press), (b) arithmetic in `research/gap_tim2_calc.py`, tagged **[Calc]**, and (c) engineering knowledge tagged **[KB-H/M/L]** (high/medium/low confidence) that **must be checked against primary documents before it enters a specification**. Searches run successfully: 0.

## 1. Executive answer

1. **Nobody public says what TIM2 NVIDIA or its ODMs use on GB200/GB300 cold plates.** The only public data points are (i) an analyst note (Kuo, Jan 2026) that Vera Rubin Max-Q (1.8 kW) uses a "micro-channel cold plate + **gold-plated lid**", with a micro-channel lid not before 2H 2027 [A, V-URL], (ii) a low-reliability vendor blog (Naddod) that attributes a 0.02 cm2-K/W liquid-metal TIM to GB300 [Sib-snip], and (iii) OCP's OAI liquid-cooling guideline, which uses a **phase-change TIM** as its reference interface [V]. The gold-plated lid is the strongest hint that NVIDIA intends a **gallium liquid-metal TIM2 on Rubin** (gold and nickel are the only common finishes that survive gallium; bare copper and aluminium do not) [KB-H on chemistry; the inference is Medium].
2. **Through Blackwell the practice is almost certainly paste on the logic die and a soft gap-filler/putty on the HBM**, applied by the ODM at plate assembly, not by NVIDIA; liquid metal is not known to be used on any data-centre NVIDIA part. NVIDIA's public liquid-metal precedent is the consumer **RTX 5090 Founders Edition (Jan 2025)** [KB-H]; Sony's PS5 (2020, millions of units) is the volume precedent [KB-H]. Treat "NVIDIA uses liquid metal in the data centre" as **unproven**.
3. **Package form is disputed inside our own corpus and matters more than the TIM choice.** `chip-roadmap-requirements.md` lists H100/B200/B300 as *lidded* (KB-H); `gap-nvidia-rubin...md` and `physics/tim-and-direct-to-die.md` recall A100/H100/B200/B300 as **bare-die with a stiffener ring** (KB-M). This author's recollection agrees with bare-die for the SXM/puck parts (the HBM stacks are visibly exposed on H100 SXM5 and B200 photographs) [KB-M]. Resolve from an actual module photo or the NVIDIA thermal design guide before any mechanical design: a bare-die package needs a two-height contact (die + HBM, 50-200 um step, 0.1-0.3 mm compliant HBM interface), a lidded one needs a single flat 100 cm2 contact at a much lower pressure.
4. **Measured impedances (ASTM D5470-class, datasheet) [V]:** Shin-Etsu X23-7921-5 grease **0.050 cm2-K/W at 25 um / 20 psi**; X23-8117 **0.061**; Honeywell PTM7950 phase-change **0.04-0.08 cm2-K/W**. Liquid metal and indium: no datasheet D5470 value is on disk; physics (BLT 25 um, k 16-73 W/mK, two metal contacts) gives **0.007-0.02 cm2-K/W**, the Naddod figure (0.02) is consistent, and the programme's 0.015 planning value is mid-band [Calc, KB-M]. Reflowed indium solder: 0.015-0.03 at 100-200 um BLT [Calc, KB-M]. Indium *foil* (Heat-Spring class) is **not** a low-impedance option: 0.05-0.12 cm2-K/W and 50-100 psi [KB-M].
5. **Bond line is the whole story for pastes.** The 10.1 K plate-to-plate difference at CoolIT's TC8 corresponds to a **24-47 um BLT difference** for a 3-6 W/mK paste at 128 W/cm2 [Calc]. A 100 um warped-corner bond line of 3.5 W/mK grease costs **38 K** at 128 W/cm2 and **89 K** at 300 W/cm2; the same gap filled with liquid metal costs 3-7 K [Calc]. Bow control (plate flatness <= 25 um, compliant core) is worth as much as the TIM chemistry for any paste or PCM; for liquid metal it is second order.
6. **Clamp windows:** grease 15-30 psi, PCM 20-40 psi, graphite 50-150 psi, liquid metal 5-20 psi, indium foil 50-100 psi [KB-M]. On a ~100 cm2 Rubin-class lid, 20 psi is already **1.4 kN**; module retention hardware of order 300-1,000 N delivers only 4-12 psi there, which excludes graphite and indium foil and favours liquid metal or a PCM at the bottom of its window [Calc, KB-M]. On a 16 cm2 bare die pair the same hardware gives 27-90 psi, so die-crack and edge-loading limits (~0.1-0.3 MPa) govern instead [KB-M].
7. **Long-term pump-out/dry-out data for liquid metal or indium TIM2 under 10-65 C cycling on 100-120 mm packages: none is public.** What exists: OCP's thermal-cycling window (10-65 C operating, -40/+70 C storage; counts not captured) [Sib-snip]; consumer liquid-metal field history (PS5 since 2020, ASUS ROG laptops since 2020-21, RTX 5090 FE 2025) on 1-8 cm2 dies, all with Ni- or Au-finished counterfaces and a dam/foam containment [KB-M]; power-module indium/solder fatigue literature [KB-M]. The CTE shear strain per 55 K cycle at 25 um BLT is **0.6 (40 mm die pair) to 1.7 (108 mm)** for a copper plate on silicon - a regime where grease pumps out in 10^2-10^3 cycles and a reflowed solder joint fatigues; only a liquid or a soft pad survives it on copper [Calc, KB-M]. **Liquid metal at 100 cm2 is therefore a qualification programme, not a datasheet pick.**
8. **Nickel plating of the wetted copper path is not a published NVIDIA or OCP requirement.** It is a widespread *practice*: secondary vendor pages describe GB200/GB300 Group-A-class plates as Ni-plated copper [Sib-snip], OCP/ASHRAE wetted-material lists *allow* bare copper and Ni-plated copper [KB-M], and no sibling found an NVIDIA document on it [V-absence]. Decision rule: plate the **contact face** (electrolytic Ni 3-5 um, no Au top coat) wherever liquid metal is used, and plate the **wetted path** only if the compatibility soak or the customer's wetted-material list demands it, because 2 x 5 um electroless Ni-P removes 10 % of a 100 um channel gap and a 10 um high-P Ni-P layer on the heat path costs 0.02 cm2-K/W - more than the liquid metal it protects [Calc].

## 2. What is actually known about the NVIDIA / ODM interface

| Item | Evidence on disk | Tag / confidence | Implication for us |
|---|---|---|---|
| Rubin (VR200, 2H 2026) lid | "Micro-channel cold plate + gold-plated lid" for Max-Q 1.8 kW; micro-channel lid for Max-P 2.3 kW not before 2H 2027 (Kuo via CTEE / CLS, Jan 2026) | [A] https://www.ctee.com.tw/news/20260107701081-430704 ; https://www.cls.cn/detail/2250526 ; Medium | A flat ~100 cm2 Au-finished lid is a liquid-metal-ready surface; Au must not be the *plate-side* finish (Au dissolves into Ga within hours) [KB-H] |
| Rubin Ultra (2027) | NVIDIA seeking micro-channel-lid / direct-to-chip partners (Digitimes Sep 2025; Wccftech) | [A] https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html ; https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/ ; Medium | The TIM2 problem disappears into the lid vendor's TIM1 problem; our core must be offerable *as* the lid insert |
| Rubin plate suppliers | Group-A: Jentech (lid/stiffener incumbent), AVC, Cooler Master, Delta; plate ASP ~US$400; NVIDIA centralised purchasing | [A] https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html ; Medium-High | Jentech's presence on a *plate* list is itself evidence that lid and plate are being co-specified (lid finish + TIM2 + plate finish as one system) |
| GB300 TIM | "Liquid-metal TIM 0.02 cm2-K/W, < 0.3 mm channels, 2-4 m/s, titanium >= 10 bar" | [Sib-snip] https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling ; **Low** (reseller blog, internally inconsistent) | Do not cite as fact; the 0.02 value is physically plausible for a 25-50 um gallium film |
| GB200/GB300 plate construction | Skived copper fins <= 0.5 mm / >= 3 mm tall, Ni-plated copper, PG25, 45 C, 1.7-1.8 LPM | [Sib-snip] https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ ; https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm ; Low-Medium | Ni-plated is the visible norm; whether the *wetted* path is plated is not stated |
| OCP reference TIM | OAI System Liquid Cooling Guidelines (Mar 2023): 1 kW OAM, phase-change TIM reference, case-to-inlet 0.015-0.016 C/W at high flow | [V] https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/ ; High | The OCP Cold Plate Test Spec v1.0.0 (Oct 2026, CoolIT-authored) measures R "with a recommended TIM"; a PCM is the most probable named TIM [Sib-snip, KB-M] |
| OCP thermal-cycling window | 10-65 C operating; -40/+70 C storage/shipping (cycle counts not captured) | [Sib-snip] https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf ; Medium | This is the pump-out test envelope the whole industry will quote |
| Package form, Blackwell | Sibling conflict: lidded (chip-roadmap, KB-H) vs bare-die + stiffener (Rubin gap report, TIM physics report, this author; KB-M) | **Unresolved** | Mechanical design cannot be frozen until resolved; see Section 4 |
| Google TPU | Bare-die cold plates since TPU v4; 80 psi CDU head "to enable advanced cold plate designs" | [V] https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/ ; High | Direct-to-die with a compliant/LM interface is already a hyperscale practice |
| Frore / delidded Rubin | LiquidJet pitch assumes delidded (bare-die) Rubin; claims 10-12 C reduction | [A] https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/ ; vendor | Shows the market expects a bare-die option for Rubin-class parts |
| NVIDIA consumer LM precedent | RTX 5090 Founders Edition uses liquid metal on the GB202 die (2025) | [KB-H] | NVIDIA has qualified gallium TIM on a ~7.5 cm2 die at ~575 W; not on HBM, not at 100 cm2 |
| Volume LM precedents | Sony PS5 (2020-, APU ~3 cm2, foam dam, grooved heat-sink face); ASUS ROG laptops (Conductonaut Extreme, 2020-21-, with a "fence"); Intel/AMD **do not** use LM as TIM1 (they use indium solder) | [KB-H/M] | The containment features (dam, grooves, Ni finish) are the proven recipe; none is at > 10 cm2 |

**Working assumption until resolved:** B200/B300 = bare-die two-height package, TIM2 = ODM-applied grease on the dies + 0.2-0.5 mm putty/pad on HBM [KB-M]; Rubin = flat Au-finished lid with a liquid-metal-capable TIM2 at 1.8-2.3 kW [A + inference, Medium]; Rubin Ultra = micro-channel lid, TIM2 eliminated [A, Medium-Low].

## 3. Interface impedances: what is measured, what is physics

### 3.1 Datasheet / literature values on disk

| Material (class) | k (W/mK) | R'' (cm2-K/W) and condition | Source | Tag |
|---|---|---|---|---|
| Shin-Etsu X23-7921-5 (silicone grease) | 6.0 | **0.050** (5.0 mm2-K/W) at 25 um / 20 psi (0.14 MPa) | https://cdn.microsi.com/wp-content/uploads/2019/07/X23-7921-5-TDS-July-2019-.pdf | [V] |
| Shin-Etsu X23-8117 (grease) | ~6 | **0.061** (6.1 mm2-K/W), datasheet condition | https://www.microsi.com/applications-solutions/thermal-interface-material/tim-2/thermal-grease-X23-8117/ | [V] |
| Honeywell PTM7950 (phase-change pad, Tpc ~45 C) | 8.5 | **0.04-0.08** C-cm2/W (vendor range; pressure/thickness not captured; sheet 0.20-0.25 mm, post-reflow BLT ~20-40 um) | https://www.caplinq.com/ptm7950-most-thermally-conductive-phase-change-pad-with-very-low-thermal-impedance-that-works-in-vertical-applications-ptm7950.html | [V] range; conditions [KB-M] |
| Liquid metal on GB300 (claimed) | - | 0.02 | https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling | [Sib-snip], Low |
| OCP OAI 1 kW OAM with PCM, whole plate incl. TIM | - | 0.015-0.016 C/W case-to-inlet at high flow (= ~0.11-0.12 cm2-K/W on an assumed 8 cm2 die) | OCP OAI guideline (above) | [V], area assumed |
| Indium Corp Heat-Spring (patterned In foil, 0.2-0.3 mm) | 86 (bulk) | 0.05-0.12 at 50-100 psi; two dry metal contacts dominate | Indium Corp literature | [KB-M] |
| Galinstan / EGaIn / Ga-In-Sn commercial (Conductonaut class) | 16.5 / 26 / vendor 73 | 0.007-0.02 at 25 um (no datasheet D5470 on disk) | property tables | [KB-M] |
| Indium solder, reflowed (Intel/AMD TIM1 practice) | 86 | 0.015-0.03 at 100-200 um incl. metallisation interfaces; 0.005-0.01 only at <= 60 um | | [KB-M] |
| Sintered Ag (power modules) | 150-250 | 0.002-0.01 | | [KB-M] |
| Graphite / CNT pads (Hitachi TC-001, PGS, Carbice) | 20-40 through-plane | 0.035-0.13 at 50-150 psi | | [KB-M] |

### 3.2 Physics check and temperature cost [Calc]

`R'' = BLT/k + R_contact`; `dT = q'' x R''`. Benchmark flux 128 W/cm2 (15 kW on the inferred ~117 cm2 TTV); Rubin die-average ~115-120 W/cm2 at 2.3 kW; 2027-28 hot-spot regime 300 W/cm2.

| Interface | R'' (cm2-K/W) | dT at 67 W/cm2 (B300 die avg) | at 128 | at 200 | at 300 |
|---|---|---|---|---|---|
| Grease k 3.5, 25 um | 0.083 | 5.6 | 10.7 | 16.7 | 25.0 |
| Grease k 3.5, 50 um | 0.155 | 10.4 | 19.8 | 31.0 | 46.5 |
| Grease k 3.5, 100 um (warped corner) | 0.298 | 19.9 | 38.1 | 59.5 | 89.3 |
| X23-7921-5, 25 um (= TDS 0.050) | 0.050 | 3.3 | 6.4 | 9.9 | 14.9 |
| X23-7921-5, 50 um | 0.091 | 6.1 | 11.7 | 18.3 | 27.4 |
| X23-7921-5, 100 um | 0.175 | 11.7 | 22.4 | 34.9 | 52.4 |
| PTM7950, 25 um | 0.049 | 3.3 | 6.3 | 9.9 | 14.8 |
| PTM7950, 50 um | 0.079 | 5.3 | 10.1 | 15.8 | 23.6 |
| Galinstan, 25 um | 0.019 | 1.3 | 2.5 | 3.8 | 5.7 |
| EGaIn, 25 um | 0.014 | 0.9 | 1.7 | 2.7 | 4.1 |
| EGaIn, 50 um | 0.023 | 1.6 | 3.0 | 4.6 | 7.0 |
| Conductonaut-class (vendor k 73), 25 um | 0.007 | 0.5 | 1.0 | 1.5 | 2.2 |
| Indium solder, 100 um | 0.017 | 1.1 | 2.1 | 3.3 | 5.0 |
| Indium solder, 200 um | 0.028 | 1.9 | 3.6 | 5.7 | 8.5 |
| Indium foil Heat-Spring, 200 um, 2 dry faces | 0.063 | 4.2 | 8.1 | 12.7 | 19.0 |
| Graphite pad, 150 um | 0.105 | 7.0 | 13.4 | 21.0 | 31.5 |

Reading: the sibling model's 0.015 cm2-K/W "elite" liquid-metal value is **mid-band physics**, not optimistic, *provided* the BLT is held at <= 25-50 um on a Ni/Au counterface; the datasheet 0.050 paste value is a **best case at 25 um**, which a 100 mm package cannot hold at its corners. At 300 W/cm2 paste consumes 15-30 K of a 35 K budget (sibling `chip-roadmap`: "requirement, not an option" is confirmed by the arithmetic).

## 4. Bond line, clamp pressure and flatness window

| Parameter | Value | Basis | Tag |
|---|---|---|---|
| Paste BLT on a flat, well-loaded lid | 20-50 um | Shin-Etsu TDS condition 25 um at 20 psi; sibling KB | [V]+[KB-M] |
| Paste BLT across a 100-130 mm CoWoS-L package | 25 um at centre to 100-300 um at corners (package bow 100-300 um over temperature) | sibling chip-roadmap / standards-reliability (KB-M); JEDEC warpage practice | [KB-M] |
| PCM post-reflow BLT | 20-40 um at 20-40 psi | PTM7950 class | [KB-M] |
| Liquid-metal BLT | 15-50 um dispensed/spread; needs dam | consumer practice | [KB-M] |
| Clamp window: grease / PCM / graphite / LM / In foil | 15-30 / 20-40 / 50-150 / 5-20 / 50-100 psi | sibling TIM report | [KB-M] |
| Force at 20 psi | 221 N on 16 cm2 die pair; 455 N on 33 cm2 (Rubin Ultra 4-die); **1,379 N on 100 cm2 lid**; 1,613 N on 117 cm2 TTV | p x A | [Calc] |
| Module retention load available (SXM/OAM class) | ~300-1,000 N -> 4-12 psi on 100 cm2, 27-90 psi on 16 cm2 | sibling TIM report [MEM]; verify against OCP OAM mechanical spec (public) and NVIDIA SXM guide (NDA) | [KB-L] |
| Bare-die pressure limit | ~0.1-0.3 MPa (15-45 psi) uniform; no edge loading; HBM at lower pressure than logic | industry practice | [KB-M] |
| Plate contact-face flatness | <= 25 um over 100 mm (lapped) for paste/PCM; <= 15 um stepped for bare die; Ra <= 0.8 um | sibling standards-reliability / TIM report | [KB-M] |
| HBM-to-logic height step (bare-die) | 0 to +/-150-200 um; sign not guaranteed since HBM4 (775 um max stack height, JESD270-4) | sibling chip-roadmap / Rubin gap | [KB-M] |
| CoolIT TC8 spread 10.1 K (plates 1 vs 2/3) as BLT | 24 um (k 3) / 28 um (k 3.5) / 47 um (k 6) / 67 um (k 8.5) | 10.1 K / 128 W/cm2 = 0.079 cm2-K/W | [Calc] |
| Bow sensitivity (108 mm, rigid plate), avg dT_TIM / corner-centre spread at 128 W/cm2 | grease: 10.7/0 K at 0 um bow -> 23.0/37 K at 100 um; PCM: 5.6/0 -> 10.6/15; LM: 1.5/0 -> 3.6/6.4 | sibling `physics/tim-and-direct-to-die` | [M] |

**Interpretation.** CoolIT's data already contain the repeatability KPI: plate 1 (TC8 = 37.7 K) versus plates 2 and 3 (27.6-27.7 K) is a ~25-50 um bond-line event, exactly the magnitude of a corner-bow or a dispense/clamp difference. Any pasted plate, ours included, will show the same unless the plate is lapped to <= 25 um, the core floats/complies to cap the hot gap at <= 50 um, and the clamp sits inside the TIM's pressure window. Specifying the **plate-to-plate R spread** (e.g. <= 2 K at any TC across 3 plates, OCP-format) is therefore a legitimate and winnable KPI against the benchmark.

## 5. Reliability: pump-out, dry-out, liquid-metal and indium cycling

| Mechanism | What is known | Tag | Design response |
|---|---|---|---|
| Grease pump-out | Driven by cyclic gap change; CTE shear strain per 55 K (10-65 C) cycle at 25 um BLT on a Cu plate: **0.61** (40 mm die pair), **0.92** (60 mm), **1.65** (108 mm) [Calc]; greases pump out within 10^2-10^3 cycles above ~0.3-0.5 strain; EOL R'' 1.3-2x BOL [KB-M] | [Calc]+[KB-M] | Do not use grease on > 50 cm2 contacts; PCM (self-healing above ~45 C) or liquid metal |
| Grease dry-out | Silicone oil separation/evaporation > 85 C over 1-3 years; worse at thin BLT and high flux | [KB-M] | Same |
| PCM (PTM7950 class) | Vendor-class claim: < 10 % drift after 1,000 cycles; no pump-out because it is solid below Tpc and re-wets above | [KB-M] (vendor reliability sheet not on disk) | Tier-1 default; qualify at our clamp pressure |
| Liquid metal on Cu | Ga dissolves Cu (CuGa2), >2x R'' after 1-3 years on bare Cu; embrittles Al instantly; dissolves Au in hours; Ga-Ni reaction slow below ~100 C, 5 um Ni is the industry floor (PS5 / ROG practice); EGaIn freezes at 15.5 C, Galinstan at -19 C; oxide skin pins the film but it migrates under cyclic bow on large areas | [KB-H chemistry / KB-M practice] | Electrolytic Ni 3-5 um on the plate face, no Au, dam/foam, 20-30 um BLT, no Al in the module; Galinstan if cold storage/shipping (-40 C OCP) is required |
| Liquid metal public cycling data | Consumer: PS5 (2020-), ROG laptops (2020-), RTX 5090 FE (2025) - 1-8 cm2 dies, years of field use, no public failure statistics; academic: Ga-alloy TIM cycling papers exist (Roy/Bhavnani-class IJHMT work, 2010s) at coupon scale | [KB-M] | **None at 100 cm2 or under 10-65 C x 1,000 cycles with a 100-300 um bowing package - this is the open qualification item** |
| Indium solder (reflowed TIM2) | Not field-serviceable; corner fatigue cracking under 0.6-1.7 strain/cycle on a Cu plate; works as TIM1 because the lid is CTE-managed and the joint is thin (100-200 um) | [KB-M] | Only as a sealed-FRU option with a CuW/CuMo/Si-CTE plate; not for a copper plate |
| Indium foil (compressed) | No pump-out/dry-out; needs 50-100 psi; 0.05-0.12 cm2-K/W | [KB-M] | Not useful above ~100 W/cm2 |
| OCP cycling envelope | 10-65 C operating; -40/+70 C storage; counts not captured; sibling planning value 1,000 operating / 50 storage cycles, acceptance R drift <= 5 %, dP <= 10 % | [Sib-snip]+[KB-M] | Adopt; add D5470 BOL/EOL on coupons and in-situ R on the TTV |
| Ni-plated contact face thermal penalty | electroless Ni-P high-P (k ~5): 5 um = 0.010, 10 um = 0.020 cm2-K/W (3-6 K at 300 W/cm2); electrolytic Ni (k ~80): 5 um = 0.0006 | [Calc] | Electrolytic only on the heat path |

**Bottom line on the "elite" point.** The 15-17 K mean case-to-inlet projection with a 0.015 cm2-K/W interface is physically sound at BOL. Its risk is not the impedance but **containment and ageing of ~1.6 g of gallium alloy over 100 cm2 across 1,000+ bow cycles**, for which no public data exist. The programme should carry PCM (0.055) as the qualified baseline and liquid metal as a Tier-2 OEM option gated by our own cycling data.

## 6. Is nickel plating of the wetted path an NVIDIA / OCP requirement?

| Question | Answer | Tag |
|---|---|---|
| Does any public NVIDIA document require Ni plating of wetted copper? | None found by any agent in this workflow (NVIDIA HGX/MGX liquid-cooling design guides are NDA) | [V-absence], Medium |
| Does OCP require it? | No. OCP ACS / ASHRAE TC 9.9 wetted-material lists *approve* copper and Ni-plated copper (and 304/316 SS, EPDM); they discourage aluminium, zinc, soft solder in PG25 loops | [KB-M] |
| What do Group-A plates look like? | Secondary vendor pages describe GB200/GB300 plates as Ni-plated copper (exterior visibly bright); internal plating not stated | [Sib-snip] Low-Medium |
| Why plate at all? | (a) copper-ion release / biofouling control in PG25 loops with mixed metals; (b) cosmetics and tarnish; (c) **gallium compatibility of the contact face** (the only thermally *necessary* reason) | [KB-M] |
| Hydraulic cost | 2 x 3 / 5 / 10 um plating on a 100 um gap = 6 / 10 / 20 % gap loss; electroless Ni throwing power in sub-150 um deep channels is poor (50-100 % thickness gradient) | [Calc]+[KB-M] |
| Thermal cost on the heat path | see Section 5 last row; high-P Ni-P at 10 um costs more than the liquid metal | [Calc] |
| Recommendation | Electrolytic Ni 3-5 um on the **contact face only** when LM is used; wetted path bare OFE copper by default, Ni-plated wetted path as a customer-selectable option justified by the PG25 compatibility soak; never plate after fin-field closure | [KB-M] |

## 7. Spec consequences for the programme

| Tier | Interface | Target R'' (cm2-K/W) | Pressure | Plate finish | Qualification gate |
|---|---|---|---|---|---|
| 1 Drop-in (lidded or bare-die, serviceable) | PCM pad, PTM7950 class | 0.055 nominal, <= 0.08 at 50 um | 20-30 psi | lapped Cu <= 25 um flatness, Ra <= 0.8 um | D5470 at 20 and 30 psi, BOL and after 1,000 x 10-65 C; 3-plate TTV spread <= 2 K/TC |
| 2 OEM co-design | Ga-In(-Sn) liquid metal with dam | 0.015 nominal, <= 0.03 EOL | 5-15 psi | electrolytic Ni 3-5 um, no Au; counterface Ni or Au | as above + 2,000 cycles + Cu/Ni/Ga cross-section + migration inspection; -40 C storage with Galinstan |
| 2b OEM sealed FRU | reflowed In pre-form | 0.015 | 0 (bonded) | Ni/Au solderable | only with CTE <= 8 ppm/K plate (CuW/CuMo); corner-crack inspection after cycling |
| 3 Chip co-design | direct-to-die LM / micro-channel lid | 0.015 at the die, lid + TIM1 removed | < 0.3 MPa on die | stepped pedestal, Ni | silicon-vendor programme |

Reporting rule (OCP-format, beats the benchmark on transparency alone): name the TIM, report D5470 R'' at the clamp pressure used, measured BLT after test, R per TC for 3 plates BOL and post-cycling, with the TIM-less (indium/LM reference) R so plate and interface are separable.

## 8. Key numbers (one line each)

- Paste datasheet floor: **0.050 cm2-K/W at 25 um / 20 psi** (Shin-Etsu X23-7921-5) [V].
- PCM: **0.04-0.08 cm2-K/W** (Honeywell PTM7950) [V].
- Liquid metal planning value: **0.015 cm2-K/W** (0.007-0.03 band) [Calc/KB-M]; Naddod claim for GB300: 0.02 [Sib-snip, Low].
- TC8 spread 10.1 K = **24-47 um** BLT difference for a 3-6 W/mK paste at 128 W/cm2 [Calc].
- 20 psi on a 100 cm2 lid = **1.38 kN**; module retention ~0.3-1 kN gives 4-12 psi there [Calc/KB-L].
- CTE shear strain per 10-65 C cycle, Cu on Si, 25 um BLT: **0.6-1.7** [Calc].
- Ni-P (high-P) 10 um on the heat path = **0.020 cm2-K/W = 6 K at 300 W/cm2**; electrolytic Ni 5 um = 0.0006 [Calc].
- Liquid-metal inventory at 25 um over 100 cm2: **1.6 g** [Calc].
- OCP cycling window: **10-65 C operating, -40/+70 C storage** [Sib-snip].
- Rubin Max-Q: **gold-plated lid + micro-channel cold plate, 1.8 kW**; micro-channel lid >= 2H 2027 (Kuo) [A].

## 9. Sources

Captured by sibling agents when search was available (URLs as recorded; not re-fetched this session):

- Shin-Etsu X23-7921-5 TDS: https://cdn.microsi.com/wp-content/uploads/2019/07/X23-7921-5-TDS-July-2019-.pdf
- Shin-Etsu X23-8117: https://www.microsi.com/applications-solutions/thermal-interface-material/tim-2/thermal-grease-X23-8117/
- Honeywell PTM7950 (caplinq page): https://www.caplinq.com/ptm7950-most-thermally-conductive-phase-change-pad-with-very-low-thermal-impedance-that-works-in-vertical-applications-ptm7950.html
- OCP OAI System Liquid Cooling Guidelines (Mar 2023): https://www.opencompute.org/documents/oai-system-liquid-cooling-guidelines-in-ocp-template-mar-3-2023-update-pdf/
- OCP Single-Phase D2C Cold Plate Test Specification v1.0.0 (Oct 2026): https://www.opencompute.org/wp-content/uploads/2026/10/OCP-Cold-Plate-Test-Specification-V1.0.0.pdf ; landing page https://www.opencompute.org/documents/ocp-cold-plate-test-specification-v1-0-0-pdf-1/
- OCP Cold Plate Development and Qualification white paper: https://www.opencompute.org/documents/ocp-cold-plate-development-and-qualification-with-integrated-comments-pdf/
- OCP PG25 Guidelines v1.0.0: https://www.opencompute.org/wp-content/uploads/2026/10/OCP-PG25-Guidelines-V1.0.0.pdf
- Kuo via CTEE / CLS (Rubin gold-plated lid, micro-channel lid 2H 2027): https://www.ctee.com.tw/news/20260107701081-430704 ; https://www.cls.cn/detail/2250526
- Digitimes (Rubin cooling design, Sep 2025): https://apps.digitimes.com/news/a20250912PD215/nvidia-rubin-cooling-design.html ; Wccftech: https://wccftech.com/nvidia-might-switch-cooling-solutions-with-rubin-ultra/
- NVIDIA Rubin Group-A plate suppliers: https://news.tvbs.com.tw/english/3188903 ; https://www.digitimes.com/news/a20260318PD231.html
- Naddod GB300 liquid-cooling blog (low reliability): https://www.naddod.com/de/blog/technical-analysis-of-gb300-liquid-cooling
- ToneCooling GB300 plate page: https://tonecooling.com/nvidia-gb300-nvl72-liquid-cold-plate/ ; FiberMall GB200 plate blog: https://www.fibermall.com/blog/nvidia-gb200-liquid-cooling-plate.htm
- Google TPU bare-die / 80 psi (Hot Chips 2025): https://www.servethehome.com/google-ironwood-tpu-swings-for-reasoning-model-leadership-at-hot-chips-2025/ ; https://chipsandcheese.com/p/googles-liquid-cooling-at-hot-chips
- Frore delidded-Rubin claim: https://hwbusters.com/news/frores-liquidjet-coldplate-claims-12c-off-rubin-and-a-third-less-coolant-flow/
- ORNL CuW direct-to-die plates: https://www.electronics-cooling.com/2026/04/high-performance-copper-tungsten-cold-plates-for-direct-to-chip-single-phase-liquid-cooling/
- TSMC direct-to-silicon on CoWoS (ECTC 2025): https://semiwiki.com/semiconductor-manufacturers/tsmc/362017-breaking-the-thermal-wall-tsmc-demonstrates-direct-to-silicon-liquid-cooling-on-cowos/
- CoolIT 15 kW brief (benchmark): `appendix/pdf/brief.txt`; CoolIT 4 kW brief: https://www.coolitsystems.com/wp-content/uploads/2025/03/4000W-coldplate-Technical-Brief-f-1.pdf

Sibling reports drawn on: `physics/tim-and-direct-to-die.md` (+ `.out`), `physics/hotspot-smoothing.md`, `physics/nonuniform-heatmap.md`, `physics/SYNTHESIS-physics.md`, `research/chip-roadmap-requirements.md`, `research/gap-nvidia-rubin-plate-envelope-and-package-geometry.md`, `research/gap-ocp-test-spec-and-boundary-docs-full-read.md`, `research/standards-reliability.md`, `research/manufacturing-cost.md`, `research/coolit-briefs-numbers.md`, `research/test-metrics.md`, `research/gap-competitor-plate-datasheets-gb300-rubin-scale.md`. Calculation script: `research/gap_tim2_calc.py`.

Knowledge-based items without URL (verify): Honeywell PTM7950 TDS (k 8.5 W/mK, Tpc ~45 C, ASTM D5470); Indium Corp Heat-Spring literature; Ga-alloy property tables (Galinstan k 16.5, mp -19 C; EGaIn k 26, mp 15.5 C); CuGa2 / AuGa2 intermetallic chemistry; PS5 / ROG / RTX 5090 FE teardowns; Intel STIM (indium TIM1) practice; JEDEC JESD22-B112A warpage; OCP OAM mechanical spec (public) for retention loads; ASHRAE TC 9.9 "Water-Cooled Servers" wetted-material table; Roy/Bhavnani-class IJHMT liquid-metal TIM papers.

## 10. Gaps / unknowns

1. **TIM2 identity on GB200/GB300 cold plates** (grease vs PCM, product name, HBM filler) - not public; obtainable only from an ODM teardown or an NVIDIA design guide under NDA.
2. **Blackwell package form (lidded vs bare-die + stiffener)** - sibling reports conflict; this author leans bare-die (KB-M). Must be settled from a module photo / NVIDIA guide before mechanical design.
3. **Rubin lid finish and TIM2** rest on one analyst note; "gold-plated lid" could be a lid *exterior* finish for cosmetics/solderability rather than a liquid-metal enabler.
4. **No ASTM D5470 datasheet value for any liquid-metal or indium TIM2 on disk**; the 0.015 cm2-K/W planning value is physics plus one low-reliability blog.
5. **No public long-term pump-out / migration data for liquid metal or indium TIM2 at 100 cm2 under 10-65 C cycling** on a 100-300 um bowing package; consumer precedents are 1-8 cm2.
6. **PTM7950 reliability sheet** (1,000-cycle drift, bake, pump-out) and its impedance-vs-pressure curve were not retrieved; values are a vendor range.
7. **NVIDIA SXM/puck mounting load, flatness and TIM-pressure window** - NDA; OCP OAM mechanical spec (public) was not read for the retention-load figure.
8. **OCP Cold Plate Test Spec v1.0.0 "recommended TIM"** name and clamp pressure, and thermal-cycling counts/acceptance limits - PDF not read (only a search snippet).
9. **Whether NVIDIA's wetted-material list requires or merely permits Ni-plated copper** - not public.
10. **Shin-Etsu X23-7921-5 impedance-vs-BLT/pressure curve** - only the single 25 um / 20 psi point is on disk.

## 11. Searches that could not be run (re-run when the budget resets; `extended` for the numeric ones)

1. `GB300 OR GB200 SXM puck "thermal interface material" cold plate liquid metal OR PTM7950 OR "phase change"` (standard)
2. `Honeywell PTM7950 ASTM D5470 thermal impedance bond line thickness pressure psi datasheet` (standard)
3. `liquid metal TIM pump-out thermal cycling reliability data center GPU cold plate 2025 2026` (extended)
4. `Indium Corporation Heat-Spring indium foil TIM2 cold plate GPU data center thermal impedance` (standard)
5. `NVIDIA SXM cold plate flatness specification um mounting load design guide thermal` (extended)
6. `"nickel plated" copper cold plate NVIDIA OR OCP wetted material requirement PG25 GB200` (standard)
7. `Shin-Etsu X23-7921-5 thermal impedance vs bond line thickness pressure curve mm2 K/W` (standard)
8. `"TIM2" "cold plate" "GB300" OR "Rubin" liquid metal OR "phase change" thermal interface` (extended)

Additional queries worth adding: `Rubin "gold" lid Jentech liquid metal TIM 2026`; `RTX 5090 Founders Edition liquid metal nickel plated vapor chamber teardown`; `OCP OAM 2.0 specification heatsink mounting load lbf`; `Ga-In-Sn copper dissolution nickel barrier thermal cycling paper`; `Intel STIM indium thermal interface junction temperature improvement`; `ASHRAE TC 9.9 water-cooled servers wetted materials copper nickel plated`.
