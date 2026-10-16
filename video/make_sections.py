#!/usr/bin/env python3
"""Per-part section solids for the video: each part STEP intersected with a half-space, exported as STL.
Cuts: X06 = keep x <= 0.6 (through the inlet line at x = 0 and the orifice at x = -1); Y10 = keep y <= 10 (across the lines)."""
import sys, pathlib, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "cad"))
import cadquery as cq
OUT = HERE.parent / "cad" / "out"; SEC = HERE / "sections"; SEC.mkdir(exist_ok=True)
PARTS = ["core", "grate_land", "grate_web", "plenum", "plenum_frames", "separator", "cap", "boss_in", "boss_out", "guard"]
CUTS = {"x06": ("x", 0.6), "y10": ("y", 10.0)}
def halfspace(axis, at):
    L = 400.0
    if axis == "x":
        return cq.Workplane("XY").box(L, L, L).translate((at - L / 2, 0, 0))
    return cq.Workplane("XY").box(L, L, L).translate((0, at - L / 2, 0))
for name in PARTS:
    p = OUT / f"{name}.step"
    if not p.exists():
        print("missing", p); continue
    t0 = time.time(); s = cq.importers.importStep(str(p)); print(name, "loaded", round(time.time() - t0, 1), "s", flush=True)
    for key, (axis, at) in CUTS.items():
        t0 = time.time()
        try:
            c = s.intersect(halfspace(axis, at))
            cq.exporters.export(c, str(SEC / f"{key}_{name}.stl"), tolerance=0.05, angularTolerance=0.2)
            print("  ", key, "ok", round(time.time() - t0, 1), "s", flush=True)
        except Exception as e:
            print("  ", key, "FAILED", e, flush=True)
print("done")
