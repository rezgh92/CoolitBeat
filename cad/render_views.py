#!/usr/bin/env python3
"""Render the report figures from the part STLs in out/ into renders/.
usage: python3 render_views.py            (full parts)   |   PRISM_CAD_LITE=1 python3 render_views.py
"""
import json, os, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from render_stl import Scene
OUT = HERE / "out"; R = HERE / "renders"; R.mkdir(exist_ok=True)
LITE = os.environ.get("PRISM_CAD_LITE", "0") == "1"
TAG = "-lite" if LITE else ""
COL = {"core": (184, 115, 51), "grate_land": (196, 128, 62), "grate_web": (204, 136, 70), "plenum": (210, 144, 82),
       "plenum_frames": (210, 144, 82), "separator": (170, 105, 50), "cap": (216, 152, 92), "boss_in": (150, 150, 155),
       "boss_out": (150, 150, 155), "guard": (190, 190, 195), "screws": (120, 120, 125), "frame": (90, 90, 95),
       "ttv_block": (150, 140, 128), "ttv_tiles": (232, 232, 226)}
PLATE = ["core", "grate_land", "grate_web", "plenum", "plenum_frames", "separator", "cap", "boss_in", "boss_out"]
CONTEXT = ["ttv_block", "ttv_tiles", "screws"]
EXPL = json.load(open(OUT / "exploded_offsets.json")) if (OUT / "exploded_offsets.json").exists() else {}


def stl(n):
    return str(OUT / f"{n}{TAG}.stl")


def scene(names, view, w=1800, h=1200, explode=False, clip=None, bg=(252, 252, 251)):
    s = Scene(width=w, height=h, view=view, background=bg)
    for n in names:
        p = stl(n)
        if not os.path.exists(p):
            continue
        s.add(p, color=COL[n], offset=(0, 0, EXPL.get(n, 0) if explode else 0), clip=clip)
    return s


figs = []
figs.append(scene(CONTEXT + PLATE, (35, 28)).render(str(R / "hero.png"), "PRISM-15 Rev A on the thermal test vehicle", verbose=True))
figs.append(scene(["ttv_block", "ttv_tiles", "screws"] + PLATE, (35, 22), h=1400, explode=True).render(str(R / "exploded.png"), "Exploded: core, grate land and web, plenum, separator, cap, bosses", verbose=True))
figs.append(scene(PLATE, (0, 89)).render(str(R / "top.png"), "Top view: 2 inlet arches, 4 outlet arches, 20 mm port bosses", verbose=True))
figs.append(scene(PLATE, (35, -40)).render(str(R / "underside.png"), "Die face (datum A) with ears and tap bosses", verbose=True))
figs.append(scene(["core"], (35, 30)).render(str(R / "core.png"), "Core: skived fin field with 15 kerf lines, rim, land, ears", verbose=True))
figs.append(scene(["grate_land", "grate_web"], (35, 35), explode=True).render(str(R / "grate.png"), "Metered grate: land plate (windows, recesses) and orifice web", verbose=True))
figs.append(scene(["plenum", "plenum_frames"], (35, 30)).render(str(R / "plenum.png"), "Folded plenum: 7 inlet and 8 outlet channels, end frames", verbose=True))
figs.append(scene(["cap", "boss_in", "boss_out"], (35, 35)).render(str(R / "cap.png"), "Drawn skirted cap: 2 inlet and 4 outlet arches, cross domes, outlet spine, port bosses", verbose=True))
# close-ups on the core: a kerf crossing the fins (full-mode fins are 0.15 mm, so clip a small window)
figs.append(scene(["core"], (40, 32), w=1600, h=1100, clip=((-4, 46, -1), (8, 55, 4))).render(str(R / "fin_closeup.png"), "Fin field close-up: 0.15 mm fins, a 0.3 mm kerf line, pocket corner", verbose=True))
# sections (STLs written by assembly.py). Each keeps the '-' side of its plane; look at the cut face from the '+' side.
P = json.load(open(HERE.parent / "design" / "params.json"))
xin = [x for x, k in zip(P["lines"]["x"], P["lines"]["kind"]) if k == "in"][3]
xout = [x for x, k in zip(P["lines"]["x"], P["lines"]["kind"]) if k == "out"][3]
SEC = [("section_across", (180, 6), None, "Cross-section across the lines at y = 10: alternating inlet and outlet channels over the kerfed fins"),
       ("section_across_closeup", (180, 6), ((-13, -200, -1), (13, 10.05, 13)), "Cross-section close-up: inlet line (orifice web, recess, lip, window, kerf) and outlet line"),
       ("section_inlet", (-90, 6), None, "Section along an inlet line: graded orifices along the plenum, recess and window"),
       ("section_inlet_closeup", (-90, 6), ((-200, -14, -1), (xin + 0.05, 14, 13)), "Inlet line close-up: orifice web, recess, lip, 1.2 mm window, kerf, fins, 0.85 mm base"),
       ("section_outlet", (-90, 6), None, "Section along an outlet line: outlet orifice row, window, kerf"),
       ("section_header", (180, 6), None, f"Section along the inlet arch at y = {P['bosses']['inlet']['y']:g} through the inlet dome and port boss")]
for name, view, clip, cap in SEC:
    src = name.replace("_closeup", "")
    p = OUT / f"{src}{TAG}.stl"
    if not p.exists():
        continue
    w, h = (1600, 1000) if clip else (1800, 900)
    s = Scene(width=w, height=h, view=view); s.add(str(p), color=(196, 128, 62), clip=clip)
    figs.append(s.render(str(R / f"{name}.png"), cap, verbose=True))
print(json.dumps(figs, indent=1))
