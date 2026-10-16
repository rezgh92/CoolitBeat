#!/usr/bin/env python3
"""PLENUM: folded 0.8 mm corrugation PLN-C (formed, one solid) + two end frames PLN-F; flat pattern DXF."""
import sys, pathlib, json
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cadquery as cq
from prism_cad import load_params, export_part, OUT, LITE


def centerline(P):
    """(x, z) centreline of the sheet, from the -x flange to the +x flange."""
    p = P["plenum"]; L = P["lines"]
    t = p["sheet_t"]; zb = p["z0"] + t / 2; zt = p["z1"] - t / 2
    off = p["wall_x_offset_from_line"]
    xs, kinds = L["x"], L["kind"]
    walls = [xs[0] - off] + [x + off for x in xs[:-1]] + [xs[-1] + off]     # 16 walls
    pts = [(-p["flange"]["at_x_abs"] - p["flange"]["w"] / 2 + 0.0, zt)]      # flange free end
    pts.append((walls[0], zt))
    z_of = {"in": zt, "out": zb, "edge_out": zb}
    for k in range(len(xs)):
        zk = z_of[kinds[k]]
        pts.append((walls[k], zk)); pts.append((walls[k + 1], zk))
    pts.append((walls[-1], zt))
    pts.append((p["flange"]["at_x_abs"] + p["flange"]["w"] / 2, zt))
    # flange free ends: extend a little beyond the wall so the fillet has room
    return pts


def build_corrugation(P):
    p = P["plenum"]; L = P["lines"]
    pts = centerline(P)
    w = cq.Wire.makePolygon([cq.Vector(x, 0, z) for x, z in pts], close=False)
    r_c = (p["bend_r_inner"] + p["bend_r_outer"]) / 2
    w = w.fillet2D(r_c, w.Vertices()[1:-1])
    outline = w.offset2D(p["sheet_t"] / 2, "arc")[0]
    face = cq.Face.makeFromWires(outline)
    ye = p["y_extent"]
    solid = cq.Workplane("XY").add(cq.Solid.extrudeLinear(face, cq.Vector(0, 2 * ye, 0))).translate((0, -ye, 0))
    # bottom slots over the outlet rows (through the bottom flats)
    xo = [x for x, k in zip(L["x"], L["kind"]) if k in ("out", "edge_out")]
    bs = p["bottom_slot"]
    cut = (cq.Workplane("XY").workplane(offset=p["z0"] - 0.1).pushPoints([(x, 0) for x in xo])
           .slot2D(bs["length"], bs["w"], angle=90).extrude(p["sheet_t"] + 0.2))
    solid = solid.cut(cut)
    # top windows in the inlet top flats
    xi = [x for x, k in zip(L["x"], L["kind"]) if k == "in"]
    tw = p["top_windows"]
    pts2 = [(x, y) for x in xi for y in tw["y_centres"]]
    cut2 = (cq.Workplane("XY").workplane(offset=p["z1"] - p["sheet_t"] - 0.1).pushPoints(pts2)
            .rect(tw["w_x"], tw["h_y"]).extrude(p["sheet_t"] + 0.2))
    solid = solid.cut(cut2)
    # bleed holes through the interior walls (alternating y ends), along x
    bh = p["bleed_holes"]
    off = p["wall_x_offset_from_line"]
    walls = [x + off for x in L["x"][:-1]]           # 14 interior walls
    holes = None
    for j, wx in enumerate(walls):
        y = bh["y_abs"] * (1 if j % 2 else -1)
        h = (cq.Workplane("YZ").workplane(offset=wx - 1.0).center(y, bh["z"]).circle(bh["d"] / 2).extrude(2.0))
        holes = h if holes is None else holes.union(h)
    solid = solid.cut(holes)
    return solid


def build_frames(P):
    p = P["plenum"]["end_frames"]; z0 = P["plenum"]["z0"]
    f = None
    for sgn in (-1, 1):
        b = cq.Workplane("XY").workplane(offset=z0).center(0, sgn * p["y_centre_abs"]).rect(p["x_len"], p["y_t"]).extrude(p["z_h"])
        f = b if f is None else f.union(b)
    return f


def flat_pattern_dxf(P):
    """Developed blank with fold lines and pierced features, from the plenum lane's data file."""
    import ezdxf
    data = json.load(open(HERE.parents[1] / "design" / "plenum_sep_data.json"))
    doc = ezdxf.new("R2010"); msp = doc.modelspace()
    for name, color in (("OUTLINE", 7), ("FOLD", 1), ("FEATURE", 5)):
        doc.layers.add(name, color=color)
    W = data["dev_width"]; Hy = 116.0
    msp.add_lwpolyline([(0, -Hy / 2), (W, -Hy / 2), (W, Hy / 2), (0, Hy / 2)], close=True, dxfattribs={"layer": "OUTLINE"})
    for a, b in data["folds"]:
        for s in (a, b):
            msp.add_line((s, -Hy / 2), (s, Hy / 2), dxfattribs={"layer": "FOLD"})
    f = data["features"]
    for wdw in f["top_flat_windows"]:
        s, y, w, h = wdw["s"], wdw["y"], wdw["w"], wdw["h"]
        msp.add_lwpolyline([(s - w / 2, y - h / 2), (s + w / 2, y - h / 2), (s + w / 2, y + h / 2), (s - w / 2, y + h / 2)], close=True, dxfattribs={"layer": "FEATURE"})
    for sl in f["bottom_flat_slots"]:
        s, y, w, l = sl["s"], sl["y"], sl["w"], sl["l"]
        msp.add_lwpolyline([(s - w / 2, y - l / 2), (s + w / 2, y - l / 2), (s + w / 2, y + l / 2), (s - w / 2, y + l / 2)], close=True, dxfattribs={"layer": "FEATURE"})
    for bh in f["bleed_holes"]:
        msp.add_circle((bh["s"], bh["y"]), bh["d"] / 2, dxfattribs={"layer": "FEATURE"})
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "plenum_flat.dxf"
    doc.saveas(path)
    return str(path), W


if __name__ == "__main__":
    P = load_params()
    c = build_corrugation(P)
    export_part("plenum", c)
    f = build_frames(P)
    export_part("plenum_frames", f)
    path, W = flat_pattern_dxf(P)
    print({"flat_pattern": path, "developed_width_mm": W})
