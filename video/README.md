# PRISM-15 Rev A explainer video pipeline

A narrated 3D explainer (1920 × 1080, 30 fps, about 5 minutes) rendered from the parametric CAD in `../cad/out` with three.js in headless Chromium (SwiftShader WebGL, no GPU needed), narrated with the piper text-to-speech engine, and encoded with ffmpeg. Everything is deterministic: frame N is a pure function of the timeline, so the render can be split, resumed and re-run.

## Files

| File | Role |
|---|---|
| `script.json` | the twelve chapters: id, minimum length, narration text (numbers written out for the speech engine) |
| `narrate.py` | synthesises each chapter with piper, measures the audio, writes `timeline.json` (chapter start and end times, frame counts) and `audio/narration_master.wav` (each chapter's speech placed 0.6 s after its chapter starts) |
| `timeline.json` | the chapter schedule the renderer and the encoder share |
| `make_sections.py` | per-part section solids for the two cut views (`sections/x06_*.stl`: keep x ≤ 0.6 mm through the inlet line at x = 0; `sections/y10_*.stl`: keep y ≤ 10 mm across the lines), made with CadQuery from the part STEP files |
| `scene.html`, `scene.js` | the scene program: loads the part STLs and the section solids, builds the particle flow paths from `../design/params.json`, the orifice glow from the artwork CSV and the zoning panel from the PRISM-G example artwork; `window.renderFrame(T)` draws global time T. Materials are matcaps baked at start-up from image-based-lighting spheres (same look as the PMREM environment at a fraction of the software-rendering cost); `?mat=ibl` renders with the full environment map, `?mat=phong` without |
| `render.js` | Playwright driver: opens the page, calls `renderFrame` for each frame and writes `frames/000000.jpg` …; `--start/--end` split the range across workers, `--probe` renders a list of frames for contact sheets |
| `encode.sh` | ffmpeg: frames + narration master → H.264 / AAC MP4 |

## Chapters

1. Title and turntable. 2. The benchmark: CoolIT's published point and PRISM's predictions. 3. The stack: exploded assembly with labels. 4. The core: fins, base, kerfs. 5. The grate: land plate, meter web, graded orifices, jets on the lip. 6. The coolant path: a parcel followed from the inlet boss through the dome, arches, separator window, plenum channel, orifice, lip, window, kerf, fins, outlet row and outlet header, in two section views with hundreds of background parcels coloured by temperature. 7. The tie: fin tips brazed to the lands, the 0.85 mm base, the pressure load. 8. Zoning: flux-graded flow length and the PRISM-G artwork. 9. Manufacturing: stack-up, braze cycle, test sequence. 10. Predicted datasheet on the test vehicle. 11. Concessions and programme. 12. Closing.

## Regenerating

```
cd docs/cooling/video
pip install piper-tts            # speech engine; a voice model (.onnx + .json) is needed, e.g. en-us-ryan-medium
python3 narrate.py --voice /path/to/en-us-ryan-medium.onnx
python3 make_sections.py         # ~1 min; needs ../cad/out/*.step
npm install three@0.186.1        # in this folder (node_modules is not committed); playwright must be installed globally
http-server . -p 8766 -s &       # any static server; ES modules need http, not file://
node render.js --url http://127.0.0.1:8766/scene.html --out frames --start 0 --end $(python3 -c "import json;print(json.load(open('timeline.json'))['total_frames'])")
bash encode.sh frames PRISM-15-RevA-explainer.mp4
```

Render cost on a 4-core container without a GPU: about 1.5 s per frame (SwiftShader uses all cores, so parallel workers do not help); the full video takes about four hours. `node render.js --probe 120,1900,4200` renders single frames for review.
