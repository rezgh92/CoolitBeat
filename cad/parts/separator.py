#!/usr/bin/env python3
"""SEPARATOR: 1.8 mm plate (outline 121.0) with 5.0 x 8.0 windows to the inlet and outlet channels (IR-C1 in
design/DDD-cap.md; window sizes and positions are read from params.json). The guard is built by parts/hardware.py."""
import sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import cadquery as cq
from prism_cad import load_params, export_part


def build_separator(P):
    s_ = P["separator"]; L = P["lines"]
    s = (cq.Workplane("XY").workplane(offset=s_["z0"]).rect(s_["outline"], s_["outline"]).extrude(s_["t"])
         .edges("|Z").fillet(s_["corner_r"]))
    xin = [x for x, k in zip(L["x"], L["kind"]) if k == "in"]
    xout = [x for x, k in zip(L["x"], L["kind"]) if k == "out"]
    xedge = [-53.7, 53.7]
    iw, ow = s_["inlet_windows"], s_["outlet_windows"]
    pts_in = [(x, y) for x in xin for y in iw["y_centres"]]
    pts_out = [(x, y) for x in xout for y in ow["y_centres"]]
    pts_edge = [(x, y) for x in xedge for y in ow["y_centres"]]
    s = s.faces(">Z").workplane().pushPoints(pts_in).rect(iw["w_x"], iw["h_y"]).cutThruAll()
    s = s.faces(">Z").workplane().pushPoints(pts_out).rect(ow["w_x"], ow["h_y"]).cutThruAll()
    s = s.faces(">Z").workplane().pushPoints(pts_edge).rect(2.5, ow["h_y"]).cutThruAll()
    ph = s_["pin_holes"]
    s = s.faces(">Z").workplane().pushPoints(ph["positions"]).circle(ph["d"] / 2).cutThruAll()
    return s


if __name__ == "__main__":
    P = load_params()
    export_part("separator", build_separator(P))
