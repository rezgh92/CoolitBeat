#!/usr/bin/env python3
"""CAP: drawn 1.0 mm skirted cap, geometry of record from design/DDD-cap.md section 3 (params-cap.json).

One solid: lid 123.4 sq (z 12.1..13.1) on a skirt 121.5 inner / 123.4 outer down to the core land (z 1.5),
2 inlet + 4 outlet arches (internal 10.0 x 7.7, crown r_i 3.5 / r_e 4.5, vertical half-cup ends of plan
r_i 5 / r_e 6, i.e. full-round slot ends), two cross domes (internal 35 x 35 and 35 x 38, plan r_i 6 / r_e 7,
same crown section as the arches), the outlet spine (10 wide internal) joining the outlet dome to arch 4,
d26.1 port pockets through the dome crowns, and the two tap notches in the -y skirt.
The port bosses and the guard are built by parts/hardware.py.
"""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cadquery as cq
from prism_cad import load_params, export_part


def rbox(x, y, z0, z1, cx=0.0, cy=0.0, r=None, top_r=None, top_edges=None):
    """Box x by y from z0 to z1 centred on (cx, cy). r rounds the vertical edges; top_r fillets the crown
    (every top edge, or only the top edges parallel to top_edges = "X" | "Y")."""
    s = cq.Workplane("XY").workplane(offset=z0).center(cx, cy).rect(x, y).extrude(z1 - z0)
    if r:
        s = s.edges("|Z").fillet(r)
    if top_r:
        sel = s.edges(f"|{top_edges}").edges(">Z") if top_edges else s.edges(">Z")
        s = sel.fillet(top_r)
    return s


def slot(length, w, z0, z1, cy=0.0, top_r=None):
    """Stadium prism along X: end-to-end length, width w (full-round ends, plan radius w/2), crown fillet top_r.
    slot2D is used instead of a box with a |Z fillet of exactly w/2, which OpenCascade refuses."""
    s = cq.Workplane("XY").workplane(offset=z0).center(0, cy).slot2D(length, w, 0).extrude(z1 - z0)
    if top_r:
        s = s.edges(">Z").fillet(top_r)
    return s


def build_cap(P):
    c = P["cap"]; a = c["arches"]; d = c["cross_domes"]; sk = c["skirt"]; t = c["sheet_t"]
    z_lid0, z_lid1, z_top = c["lid_z0"], c["lid_z1"], c["top_z"]           # 12.1, 13.1, 20.8
    z_crown_i = z_lid0 + a["internal_h"]                                      # 19.8 (internal crown)
    r_i, r_e = a["crown_r_internal"], a["crown_r_external"]                   # 3.5, 4.5
    # lid + skirt: 123.4 r2 from the skirt foot to the lid top, minus the 121.5 r1 skirt interior up to the lid underside
    body = rbox(c["outline"], c["outline"], sk["z_bottom"], z_lid1, r=c["corner_r"])
    body = body.cut(rbox(sk["inner"], sk["inner"], sk["z_bottom"] - 0.1, z_lid0, r=sk["inner_corner_r"]))
    outer, inner = body, None

    def add(o, i):
        nonlocal outer, inner
        outer = outer.union(o)
        inner = i if inner is None else inner.union(i)

    # arches: slot plan (vertical ends, plan radius = half width), crowns r_i 3.5 / r_e 4.5, 1.0 wall all round
    for key in ("inlet", "outlet"):
        xe_i, xe_o = a[key]["x_end_internal_abs"], a[key]["x_end_external_abs"]
        for y in a[key]["y_centres"]:
            add(slot(2 * xe_o, a["external_w_y"], z_lid0, z_top, cy=y, top_r=r_e),
                slot(2 * xe_i, a["internal_w_y"], z_lid0 - 0.1, z_crown_i, cy=y, top_r=r_i))
    # cross domes (w_x, span_y internal; external = + 2 t), plan corners r_i 6 / r_e 7, same crown section
    for key in ("inlet", "outlet"):
        dm = d[key]
        add(rbox(dm["w_x"] + 2 * t, dm["span_y"] + 2 * t, z_lid0, z_top, cx=dm["x"], cy=dm["y"], r=d["plan_r_external"], top_r=r_e),
            rbox(dm["w_x"], dm["span_y"], z_lid0 - 0.1, z_crown_i, cx=dm["x"], cy=dm["y"], r=d["plan_r_internal"], top_r=r_i))
    # outlet spine: 10 wide internal at x 0, arch section, from the outlet dome to arch 4 (record: y 40..54). The solid
    # starts inside the dome's crown flat and ends at the arch-4 centre line so that both end faces lie inside the
    # neighbouring cavities (a channel running through the dome end wall, not a step against it).
    sp = d["outlet_spine"]; do = d["outlet"]
    y_s = do["y"] + do["span_y"] / 2 - r_i - 0.5
    y_e = a["outlet"]["y_centres"][-1]
    add(rbox(sp["w_x_external"], y_e - y_s, z_lid0, z_top, cy=(y_s + y_e) / 2, top_r=r_e, top_edges="Y"),
        rbox(sp["w_x_internal"], y_e - y_s, z_lid0 - 0.1, z_crown_i, cy=(y_s + y_e) / 2, top_r=r_i, top_edges="Y"))
    cap = outer.cut(inner)
    # port pockets d26.1 through the dome crowns; the boss pilot d25.95 x 1.0 closes them (underside at the internal crown)
    pk = c["port_pockets"]
    for (x, y) in pk["centres"]:
        cap = cap.cut(cq.Workplane("XY").workplane(offset=pk["floor_z"] - 0.5).center(x, y)
                      .circle(pk["d"] / 2).extrude(z_top - pk["floor_z"] + 1.0))
    # skirt notches over the core's tap bosses (-y edge)
    n = sk.get("tap_notches")
    if n:
        for x in n["x_centres"]:
            cap = cap.cut(cq.Workplane("XY").workplane(offset=n["z0"]).center(x, -c["outline"] / 2)
                          .rect(n["w"], 2 * t + 1.0).extrude(n["z1"] - n["z0"]))
    return cap


if __name__ == "__main__":
    P = load_params()
    export_part("cap", build_cap(P))
