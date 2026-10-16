#!/usr/bin/env python3
"""GRATE: land plate GRT-L (windows, recesses, lips) and meter web GRT-W (all orifices from the artwork CSV)."""
import sys, pathlib, csv, collections
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cadquery as cq
from prism_cad import load_params, export_part, LITE

REPO = HERE.parents[3]   # /home/user/Rez


def plate(outline, r, z0, t):
    return cq.Workplane("XY").workplane(offset=z0).rect(outline, outline).extrude(t).edges("|Z").fillet(r)


def build_land(P):
    g = P["grate_land"]; L = P["lines"]
    z0, t = g["z0"], g["t"]
    s = plate(g["outline"], g["corner_r"], z0, t)
    xin = [x for x, k in zip(L["x"], L["kind"]) if k == "in"]
    xint = [x for x, k in zip(L["x"], L["kind"]) if k in ("in", "out")]
    xedge = [-g["window_edge"]["x_centre_abs"], g["window_edge"]["x_centre_abs"]]
    # recesses from the top face (inlet lines)
    rc = g["recess_inlet"]
    s = (s.faces(">Z").workplane().pushPoints([(x, 0) for x in xin])
         .slot2D(rc["length"], rc["w"], angle=90).cutBlind(-rc["depth"]))
    # through windows: interior 1.2 x 108, edge 0.6 x 108
    wi, we = g["window_interior"], g["window_edge"]
    s = (s.faces("<Z").workplane().pushPoints([(x, 0) for x in xint]).slot2D(wi["length"], wi["w"], angle=90).cutThruAll())
    s = (s.faces("<Z").workplane().pushPoints([(x, 0) for x in xedge]).slot2D(we["length"], we["w"], angle=90).cutThruAll())
    # datum pin holes (one round, one slotted)
    ph = g["pin_holes"]
    (px, py), (qx, qy) = ph["positions"]
    s = s.faces("<Z").workplane().pushPoints([(px, py)]).circle(ph["d"] / 2).cutThruAll()
    s = s.faces("<Z").workplane().pushPoints([(qx, qy)]).slot2D(ph["d"] + ph["slot_long_axis_at_pos2"], ph["d"], angle=45).cutThruAll()
    return s


def build_web(P):
    """Meter web: ONE sketch (outline minus all holes) extruded once; no per-hole booleans."""
    g = P["grate_web"]
    z0, t = g["z0"], g["t"]
    rows = list(csv.DictReader(open(REPO / P["artwork_csv"])))
    if LITE:
        rows = rows[::5]
    sk = cq.Sketch().rect(g["outline"], g["outline"]).vertices().fillet(g["corner_r"]).reset()
    groups = collections.defaultdict(list)
    for r in rows:
        groups[(float(r["w_mm"]), float(r["h_mm"]))].append((float(r["x_mm"]), float(r["y_mm"])))
    for (w, h), pts in groups.items():
        sk = sk.push(pts).rect(w, h, mode="s").reset()
    ph = g["pin_holes"]
    sk = sk.push([tuple(p) for p in ph["positions"]]).circle(ph["d"] / 2, mode="s").reset()
    sk = sk.push([tuple(p) for p in g["fiducials"]]).circle(g["fiducial_d"] / 2, mode="s").reset()
    s = cq.Workplane("XY").workplane(offset=z0).placeSketch(sk).extrude(t)
    return s, len(rows)


if __name__ == "__main__":
    P = load_params()
    land = build_land(P)
    export_part("grate_land", land)
    web, n = build_web(P)
    r = export_part("grate_web", web)
    print({"orifices_modelled": n})
