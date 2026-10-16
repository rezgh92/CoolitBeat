#!/usr/bin/env python3
"""HARDWARE and context: port bosses (BOSS-IN, BOSS-OUT) with pilot, guard GUARD-C, captive spring screws,
load frame LF-15P (unchanged), thermal test vehicle (context only).
Bosses and guard follow design/DDD-cap.md sections 5 and 6 (params.json keys 'bosses', 'guard')."""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cadquery as cq
from prism_cad import load_params, export_part, RHO_SS, RHO_CU


def build_boss(P, key):
    """OD 26 / bore 20 body from body_z0 to z1 on a pilot d25.95 x 1.0 whose underside (z0) sits at the cap's
    internal crown inside the d26.1 port pocket; 0.5 x 45 deg ring-seat chamfer at the body foot.
    The stub-seat counterbore (d23 H8 x 8) and its face O-ring groove are not modelled."""
    b = P["bosses"]; p = b["pilot"]
    ro, ri, rp = b["od"] / 2, b["bore"] / 2, p["d"] / 2
    z0, zb, z1 = b["z0"], b["body_z0"], b["z1"]
    ch = p.get("chamfer_top", 0.0)
    pts = [(ri, z0), (rp, z0), (rp, zb), (ro - ch, zb), (ro, zb + ch), (ro, z1), (ri, z1)]
    boss = cq.Workplane("XZ").polyline(pts).close().revolve(360, (0, 0, 0), (0, 1, 0))
    return boss.translate((b[key]["x"], b[key]["y"], 0))


def build_guard(P):
    """GUARD-C: inverted mesh cup d30 x 5.0 under the inlet dome crown, centred on the inlet boss, as a 0.1 mm
    shell: side wall, flat bottom (corrugations not modelled), top annulus, 0.5 mm frame ring (d28 so that it clears
    the r 3.5 crown fillet) against the crown underside at z_top, and the retention collar d19.6 x 3.0 rising
    through the d20 opening into the boss bore (hook tabs not modelled)."""
    g = P["guard"]; b = P["bosses"]; col = g["collar"]
    cx, cy = b["inlet"]["x"], b["inlet"]["y"]
    t, ft = g["shell_t"], g["frame_t"]
    ro, r_ring = g["od"] / 2, g["frame_ring_od"] / 2
    r_col_o, r_col_i = col["d"] / 2, col["d"] / 2 - col["wall_t"]
    zb, zt = g["z_bottom"], g["z_top"]

    def wp(z):
        return cq.Workplane("XY").workplane(offset=z).center(cx, cy)

    wall = wp(zb).circle(ro).circle(ro - t).extrude(zt - ft - zb)
    bottom = wp(zb).circle(ro).extrude(t)
    top = wp(zt - ft - t).circle(ro).circle(r_col_i).extrude(t)
    ring = wp(zt - ft).circle(r_ring).circle(r_col_i).extrude(ft)
    collar = wp(zt).circle(r_col_o).circle(r_col_i).extrude(col["h"])
    return wall.union(bottom).union(top).union(ring).union(collar)


def build_screws(P):
    s = P["screws"]; ears = P["core"]["ears"]
    top = ears["top_z"]
    out = None
    for (x, y) in ears["positions"]:
        head = cq.Workplane("XY").workplane(offset=top + s["spring_len"]).center(x, y).circle(s["head_d"] / 2).extrude(3.0)
        spring = cq.Workplane("XY").workplane(offset=top).center(x, y).circle(s["spring_od"] / 2).circle(s["shank_d"] / 2 + 0.2).extrude(s["spring_len"])
        shank = cq.Workplane("XY").workplane(offset=top + s["spring_len"] - s["length"]).center(x, y).circle(s["shank_d"] / 2).extrude(s["length"])
        one = head.union(spring).union(shank)
        out = one if out is None else out.union(one)
    return out


def build_frame(P):
    f = P["frame"]; ears = P["core"]["ears"]; s = P["screws"]
    fr = cq.Workplane("XY").workplane(offset=f["z0"]).rect(f["outline"], f["outline"]).extrude(f["t"]).edges("|Z").fillet(3.0)
    return fr.cut(cq.Workplane("XY").workplane(offset=f["z0"] - 1).pushPoints(ears["positions"]).circle(s["shank_d"] / 2 + 0.1).extrude(f["t"] + 2))


def build_ttv(P):
    t = P["ttv"]
    blk = cq.Workplane("XY").workplane(offset=t["block"]["z0"]).rect(t["block"]["x"], t["block"]["y"]).extrude(t["block"]["z1"] - t["block"]["z0"])
    sz = t["tiles"]["size"]
    pts = [(sx * sz / 2, sy * sz / 2) for sx in (-1, 1) for sy in (-1, 1)]
    tiles = cq.Workplane("XY").workplane(offset=t["tiles"]["z0"]).pushPoints(pts).rect(sz - 0.2, sz - 0.2).extrude(t["tiles"]["z1"] - t["tiles"]["z0"])
    return blk, tiles


if __name__ == "__main__":
    P = load_params()
    export_part("boss_in", build_boss(P, "inlet"))
    export_part("boss_out", build_boss(P, "outlet"))
    export_part("guard", build_guard(P), rho=RHO_SS)
    export_part("screws", build_screws(P), rho=RHO_SS)
    export_part("frame", build_frame(P), rho=RHO_SS)
    blk, tiles = build_ttv(P)
    export_part("ttv_block", blk, rho=RHO_CU)
    export_part("ttv_tiles", tiles, rho=3.26e-3)
