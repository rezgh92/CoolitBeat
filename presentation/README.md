# Presentation

| File | What it is |
|---|---|
| `PRISM-15-RevA-review-deck.pptx` | The 23-slide design review deck as a structured PowerPoint file (theme, layouts, placeholders, sections, speaker notes). Built by `build_pptx.js` from the same content as the web deck. |
| `build_pptx.js` | Generator (pptxgenjs). `THEME` at the top holds the fonts and the twelve theme colours; the three layouts (`TITLE`, `CONTENT`, `DARK`) hold the frame. To move the deck onto a company template, replace the theme colours and fonts there and rebuild, or open the file in PowerPoint and apply the company theme: every text run uses scheme colours, so it follows the theme. |
| `project/` | The slide source of the web version of the deck (Claude Slides artifact files: `deck.json` and one HTML file per slide). |

Rebuild: `node build_pptx.js` with `pptxgenjs` installed (`npm install pptxgenjs`) and the pptx skill's `apply_theme.js` reachable through `PPTX_SKILL`. The deck has not yet been placed on a company template: none was supplied.
