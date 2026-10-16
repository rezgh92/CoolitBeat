#!/usr/bin/env python3
"""Drawing package: SVG orthographic views (hidden lines off), DXF 2-D artworks, dimension CSVs per part.
usage: python3 drawings.py      (uses LITE core for the SVG views to keep them fast; other parts full)
"""
import csv, json, os, pathlib, shutil, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cadquery as cq
import ezdxf
from prism_cad import OUT
D = HERE / "drawings"; D.mkdir(exist_ok=True)
DESIGN = HERE.parent / "design"
P = json.load(open(DESIGN / "params.json"))

VIEWS = {"top": (0, 0, 1), "front": (0, -1, 0), "right": (1, 0, 0), "iso": (1, -1, 0.8)}


def svg_views(name, shape, w=1200, h=900):
    for v, d in VIEWS.items():
        cq.exporters.export(shape, str(D / f"{name}_{v}.svg"), opt={"projectionDir": d, "width": w, "height": h,
                                                                   "showHidden": False, "strokeWidth": 0.4})


def load(name, lite=False):
    p = OUT / f"{name}{'-lite' if lite else ''}.step"
    return cq.importers.importStep(str(p)) if p.exists() else None


# 1. SVG views
files = []
for name, lite in (("core", True), ("grate_land", False), ("grate_web", False), ("plenum", False), ("separator", False), ("cap", False)):
    s = load(name, lite)
    if s is not None:
        svg_views(name, s); files += [f"{name}_{v}.svg" for v in VIEWS]
asm = None
for name, lite in (("core", True), ("grate_land", False), ("grate_web", False), ("plenum", False), ("plenum_frames", False),
                   ("separator", False), ("cap", False), ("boss_in", False), ("boss_out", False)):
    s = load(name, lite)
    if s is not None:
        asm = s if asm is None else asm.add(s)
if asm is not None:
    svg_views("assembly", asm); files += [f"assembly_{v}.svg" for v in VIEWS]

# 2. DXF artworks: copy the lane artworks, generate the separator window pattern and the cap blank outline
for src in ("artwork_prism15_ttv.dxf", "artwork_prism_g_example.dxf"):
    if (DESIGN / src).exists():
        shutil.copy(DESIGN / src, D / src); files.append(src)
if (OUT / "plenum_flat.dxf").exists():
    shutil.copy(OUT / "plenum_flat.dxf", D / "plenum_flat.dxf"); files.append("plenum_flat.dxf")

doc = ezdxf.new("R2010"); msp = doc.modelspace()
for layer, color in (("OUTLINE", 7), ("WINDOW", 5), ("PIN", 1)):
    doc.layers.add(layer, color=color)
sp = P["separator"]; L = P["lines"]
o = sp["outline"] / 2
msp.add_lwpolyline([(-o, -o), (o, -o), (o, o), (-o, o)], close=True, dxfattribs={"layer": "OUTLINE"})
def rect(cx, cy, w, h, layer):
    msp.add_lwpolyline([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)], close=True, dxfattribs={"layer": layer})
for x, k in zip(L["x"], L["kind"]):
    if k == "in":
        for y in sp["inlet_windows"]["y_centres"]:
            rect(x, y, sp["inlet_windows"]["w_x"], sp["inlet_windows"]["h_y"], "WINDOW")
    elif k == "out":
        for y in sp["outlet_windows"]["y_centres"]:
            rect(x, y, sp["outlet_windows"]["w_x"], sp["outlet_windows"]["h_y"], "WINDOW")
    else:
        for y in sp["outlet_windows"]["y_centres"]:
            rect(53.7 if x > 0 else -53.7, y, 2.5, sp["outlet_windows"]["h_y"], "WINDOW")
for (px, py) in sp["pin_holes"]["positions"]:
    msp.add_circle((px, py), sp["pin_holes"]["d"] / 2, dxfattribs={"layer": "PIN"})
doc.saveas(D / "separator_windows.dxf"); files.append("separator_windows.dxf")

# 3. Dimension CSVs from params.json (flattened), one per part group
def flatten(prefix, obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            flatten(f"{prefix}.{k}" if prefix else k, v, out)
    elif isinstance(obj, list) and obj and not isinstance(obj[0], (list, dict)) and len(obj) <= 16:
        out.append((prefix, " ".join(str(x) for x in obj)))
    elif isinstance(obj, list):
        out.append((prefix, f"[{len(obj)} values, see params.json]"))
    else:
        out.append((prefix, str(obj)))
for part in ("core", "grate_land", "grate_web", "plenum", "separator", "cap", "bosses", "guard", "screws", "lines"):
    rows = []; flatten("", P[part], rows)
    with open(D / f"dims_{part}.csv", "w", newline="") as f:
        wr = csv.writer(f); wr.writerow(["parameter", "value (mm unless stated)"]); wr.writerows(rows)
    files.append(f"dims_{part}.csv")

sizes = {f: (D / f).stat().st_size for f in files if (D / f).exists()}
print(json.dumps(sizes, indent=1))
