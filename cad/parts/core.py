#!/usr/bin/env python3
"""CORE: base plate + skived fin field + kerfs + rim + land + ears + tap bosses + pin holes (one solid)."""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cadquery as cq
from prism_cad import load_params, comb_core, export_part, LITE


def build(P=None):
    P = P or load_params()
    c = P["core"]
    bt = c["base_t"]; tip = c["fin_tip_z"]; fin_h = tip - bt
    bx, by, br = c["body"]["x"], c["body"]["y"], c["body"]["corner_r"]
    # fin field on a base slab the size of the field (comb profile, no booleans), kerfs cut to the kerf floor
    core = comb_core(c["fin_field"]["x"], c["fin_field"]["y"], c["fin_pitch"], c["fin_t"], fin_h, bt,
                     c["kerf_x"], c["kerf_w"], None, kerf_floor_z=c["kerf_floor_z"])
    # body plate 125 x 125 r2, die face at z = 0
    body = cq.Workplane("XY").rect(bx, by).extrude(bt).edges("|Z").fillet(br)
    # rim: from the pocket wall to the rim outer, up to z = 2.8
    rim = (cq.Workplane("XY").workplane(offset=bt).rect(c["rim"]["outer"], c["rim"]["outer"])
           .extrude(c["rim"]["top_z"] - bt).edges("|Z").fillet(c["rim"]["corner_r"]))
    pocket = (cq.Workplane("XY").workplane(offset=bt).rect(c["pocket"]["x"], c["pocket"]["y"])
              .extrude(c["rim"]["top_z"] - bt + 0.1).edges("|Z").fillet(c["pocket"]["corner_r"]))
    rim = rim.cut(pocket)
    # land ring: rim outer -> body outline, up to z = 1.5
    land = (cq.Workplane("XY").workplane(offset=bt).rect(bx, by).extrude(c["land"]["top_z"] - bt).edges("|Z").fillet(br))
    land = land.cut(cq.Workplane("XY").workplane(offset=bt).rect(c["rim"]["outer"], c["rim"]["outer"]).extrude(2.0))
    # ears: lobes protruding 7 mm beyond the body, 12 wide, z 0..1.5, hole 3.4
    e = c["ears"]
    ears = None
    for (x, y) in e["positions"]:
        if abs(y) > abs(x):      # ear on a +/-y edge
            cx, cy = x, (by / 2 + e["protrusion"] / 2) * (1 if y > 0 else -1)
            w, h = e["w"], e["protrusion"] + 2.0
        else:
            cx, cy = (bx / 2 + e["protrusion"] / 2) * (1 if x > 0 else -1), y
            w, h = e["protrusion"] + 2.0, e["w"]
        lobe = cq.Workplane("XY").center(cx, cy).rect(w, h).extrude(e["top_z"]).edges("|Z").fillet(e["corner_r"])
        ears = lobe if ears is None else ears.union(lobe)
    holes = cq.Workplane("XY").pushPoints(e["positions"]).circle(e["hole_d"] / 2).extrude(5.0)
    # tap bosses on the -y edge
    t = c["tap_bosses"]
    taps = None
    for x in t["x_centres"]:
        b = (cq.Workplane("XY").center(x, -(by / 2 + t["protrusion"] / 2 - 0.5)).rect(t["w"], t["protrusion"] + 1.0)
             .extrude(t["top_z"]))
        taps = b if taps is None else taps.union(b)
    tap_holes = None
    for x in t["x_centres"]:
        h = (cq.Workplane("XZ").workplane(offset=by / 2 + t["protrusion"]).center(x, t["hole_z"])
             .circle(t["hole_d"] / 2).extrude(-t["hole_len"]))
        cb = (cq.Workplane("XZ").workplane(offset=by / 2 + t["protrusion"]).center(x, t["hole_z"])
              .circle(t["counterbore"][0] / 2).extrude(-t["counterbore"][1]))
        hh = h.union(cb)
        tap_holes = hh if tap_holes is None else tap_holes.union(hh)
    pins = (cq.Workplane("XY").workplane(offset=c["rim"]["top_z"] - c["pin_holes"]["depth"])
            .pushPoints(c["pin_holes"]["positions"]).circle(c["pin_holes"]["d"] / 2).extrude(c["pin_holes"]["depth"] + 0.1))
    solid = body.union(rim).union(land).union(ears).union(taps).union(core)
    solid = solid.cut(holes).cut(tap_holes).cut(pins)
    return solid


if __name__ == "__main__":
    s = build()
    export_part("core", s)
