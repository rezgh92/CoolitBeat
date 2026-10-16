# CoolitBeat: PRISM-15 Rev A cold plate

A single-phase, all-copper, direct-liquid-cooled cold plate designed to beat CoolIT Systems' published 15 kW cold plate at CoolIT's own operating point, with conventional manufacturing and one vacuum braze cycle. AI accelerators are the first application; SiC power conversion the second.

**Status (16 October 2026).** Architecture verified; design definition complete for every layer; parametric CAD checked (fourteen solids, zero interference); design report, review deck and explainer video produced. No hardware exists yet: every performance figure in this repository is a model prediction until the first braze coupons and plates are tested.

## Headline numbers at CoolIT's test point

15 kW over four heaters (117 cm²), 18 LPM PG25 at 45 °C inlet, standard paste.

| Metric | CoolIT 15 kW | PRISM-15 Rev A |
|---|---|---|
| Average case-to-inlet rise | 34.4 K measured | 31.1 K predicted (29.2 K on a phase-change pad) |
| Maximum case-to-inlet rise | 44.2 K measured | 38.8 K predicted (34.9 K on a pad) |
| Plate pressure drop, 20 mm ports | not published, ≈ 22 kPa reconstructed | 7.6 kPa |
| Load at an 85 °C case, paste / pad | ≈ 12.9 / 14.8 kW | 15.7 / 18.4 kW |
| Height at the bar | ≈ 22–28 mm | 20.8 mm |
| Factory cost per plate at 100k / yr | ≈ US$126 | US$165 (US$142 on the silver-free route) |

What it does not win: price per plate, fouling life at equal filtration (it ships with a 33 µm tray filter), field record, the average at very low flow or on a 100 cm² footprint, and CoolIT's 4 kW single-die point. US sales wait for a freedom-to-operate opinion (CoolIT's split-flow patents run to September 2028).

## Map of the repository

Read in this order. Folders are siblings on purpose: the CAD, report and video scripts locate `design/params.json` and `cad/out` relative to their own paths.

| Path | What it is |
|---|---|
| `00-briefing.md` | One-page briefing for a manager: what was done, how it works, why it beats CoolIT, what it does not win, what the money buys |
| `01-benchmark-and-requirements.md` | CoolIT reconstruction, the OCP test specification as arbiter, requirements |
| `02-physics-basis.md` | The physics the design rests on |
| `03-architecture.md` | Architecture of record, PRISM-15 Rev A (audited) |
| `04-verification.md` | How the architecture was stress-tested (five review rounds) |
| `05-detailed-design.md` | Design-definition synthesis: lane status, controlled stack, reconciliation decisions, deviations, open items mapped to experiments |
| `design/` | The eight design lanes (`DDD-core`, `DDD-grate`, `DDD-plenum`, `DDD-cap`, `DDD-mech`, `DDD-mfg`, `DDD-perf`, `DDD-innovation`) with their scripts and outputs; `params.json` (single source of truth for geometry); orifice artworks (`artwork_*.csv/.dxf`); `bom.csv` |
| `model/` | The calibrated 1-D / network / 2-D thermal-hydraulic model (`coldplate_model.py`) and its output |
| `cad/` | Parametric CAD (CadQuery): part scripts, assembly and interference check, STEP (xz-compressed) and STL outputs, DXF artworks and flat patterns, SVG drawings, renders; see `cad/README.md` |
| `report/` | The design report (`PRISM-15-RevA-design-report.pdf`, 37 pages) with its Markdown source and PDF builder |
| `presentation/` | The 23-slide review deck: `PRISM-15-RevA-review-deck.pptx` (PowerPoint) and the slide source files of the web deck (`project/`) |
| `video/` | The narrated 3D explainer video pipeline and `PRISM-15-RevA-explainer.mp4` (added when the render completes); see `video/README.md` |
| `appendix/` | Evidence: research sweep, physics checks, design-panel proposals and judge scores, verification reports, audit |
| `page/` | Builder for the one-page web summary |

## Deliverables at a glance

- **Design report**: `report/PRISM-15-RevA-design-report.pdf`
- **CAD package**: `cad/out/*.step.xz` (expand with `xz -d`), `cad/out/*.stl`, `cad/drawings/`, `cad/renders/`, `design/params.json`, `design/bom.csv`
- **Review deck**: `presentation/PRISM-15-RevA-review-deck.pptx`
- **Explainer video**: `video/PRISM-15-RevA-explainer.mp4`
- **Briefing**: `00-briefing.md`

## Regenerating

Everything downstream of the architecture is generated from `design/params.json` and the lane scripts.

```
cd cad && python3 parts/core.py parts/grate.py parts/plenum.py parts/separator.py parts/cap.py parts/hardware.py && python3 assembly.py && python3 render_views.py && python3 drawings.py
cd report && python3 build_pdf.py PRISM-15-RevA-design-report.md PRISM-15-RevA-design-report.pdf --cover-image ../cad/renders/hero.png
cd video && python3 narrate.py --voice <piper voice .onnx> && python3 make_sections.py && node render.js ... && bash encode.sh frames PRISM-15-RevA-explainer.mp4
```

Needs Python 3 with `cadquery`, `numpy`, `pillow`, `ezdxf`, `scipy`; `pandoc`; Node with `playwright` and `three`; `ffmpeg`; `piper-tts` for narration. Details in `cad/README.md` and `video/README.md`.

## Programme in one line

US$8.4–10.7 M over twelve months in tranches; the first US$2.3 M to gate G1 at month 3 buys the tie-braze experiment that decides the plate; a public OCP-format result at month 12; volume 2029. Decisions D1–D7 are in `03-architecture.md` section 0.4 and `00-briefing.md`.
