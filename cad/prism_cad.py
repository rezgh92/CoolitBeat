#!/usr/bin/env python3
"""
Shared scaffold for the PRISM-15 Rev A parametric CAD (CadQuery 2.8 / OCCT).

- load_params(): reads design/params.json (all dimensions in mm) and applies LITE mode
  when the environment variable PRISM_CAD_LITE=1 is set (coarser fin pitch and fewer
  orifices, so a part builds in seconds while a script is being developed; the final
  export always runs in full mode).
- comb_core(): the proven boolean-free way to build the skived fin field: a single
  comb profile in the YZ plane (base + all fins) extruded along X, then the kerfs cut.
  Full mode: ~2 s extrude, ~3 min kerf cut, ~6 min STEP write, 85 MB STEP (xz: see
  export_part, which also writes a .step.xz for the repository).
- export_part(): STEP (+xz), STL, mass/volume/bbox report line, optional DXF of a
  2-D sketch.

Conventions: X along the fins, Y across the fins (lines run along Y), Z up from the
die face (z = 0 at the base's die face, so the base occupies 0..base_t). Origin at the
centre of the fin field. Parts are modelled in their assembled position so the
assembly step only has to combine them.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import time

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
DESIGN = HERE.parent / "design"
OUT = HERE / "out"
RHO_CU = 8.94e-3      # g/mm3
RHO_SS = 7.95e-3
LITE = os.environ.get("PRISM_CAD_LITE", "0") == "1"


def load_params(path: pathlib.Path | None = None) -> dict:
    p = json.load(open(path or DESIGN / "params.json"))
    if LITE:
        p = _lite(p)
    return p


def _lite(p: dict) -> dict:
    """Coarsen the fin field 10x and keep every 5th orifice so builds take seconds."""
    p = json.loads(json.dumps(p))
    core = p.get("core", {})
    if "fin_pitch" in core:
        core["fin_pitch"] = core["fin_pitch"] * 10
        core["fin_t"] = core.get("fin_t", 0.15) * 10
    p["_lite"] = True
    return p


def comb_core(field_x: float, field_y: float, fin_pitch: float, fin_t: float, fin_h: float,
              base_t: float, kerf_x: list[float], kerf_w: float, base_outline=None,
              kerf_floor_z: float | None = None) -> cq.Workplane:
    """Base + fin field + kerfs as ONE solid.

    field_x: fin length along X; field_y: fin-field width along Y; fins at fin_pitch across Y.
    base_outline: optional (bx, by) of a larger base plate (ears/land are added by the
    core script on top of this); the fin field is centred on it.
    """
    n = int(round(field_y / fin_pitch))
    bx, by = base_outline or (field_x, field_y)
    pts = [(-by / 2, 0.0), (by / 2, 0.0), (by / 2, base_t)]
    for i in range(n):
        yc = field_y / 2 - fin_pitch / 2 - i * fin_pitch
        y1, y0 = yc + fin_t / 2, yc - fin_t / 2
        pts += [(y1, base_t), (y1, base_t + fin_h), (y0, base_t + fin_h), (y0, base_t)]
    pts += [(-by / 2, base_t)]
    # drop any consecutive duplicates (zero-length edges break the polyline)
    clean = [pts[0]]
    for q in pts[1:]:
        if abs(q[0] - clean[-1][0]) > 1e-9 or abs(q[1] - clean[-1][1]) > 1e-9:
            clean.append(q)
    prof = cq.Workplane("YZ").polyline(clean).close()
    solid = prof.extrude(field_x / 2, both=True)
    if bx > field_x:   # base plate longer than the fin field along X: add the extra base
        extra = cq.Workplane("XY").box(bx, by, base_t, centered=(True, True, False))
        solid = solid.union(extra)
    if kerf_x:
        z0 = base_t if kerf_floor_z is None else kerf_floor_z
        kerf = (cq.Workplane("XY").workplane(offset=z0)
                .pushPoints([(x, 0) for x in kerf_x]).rect(kerf_w, field_y + 2).extrude(base_t + fin_h - z0 + 0.2))
        solid = solid.cut(kerf)
    return solid


def report(name: str, shape: cq.Workplane, rho: float = RHO_CU) -> dict:
    v = shape.val()
    bb = v.BoundingBox()
    vol = v.Volume()
    r = dict(part=name, valid=bool(v.isValid()), solids=shape.solids().size(), volume_mm3=round(vol, 1),
             mass_g=round(vol * rho, 1), bbox=[round(bb.xmin, 2), round(bb.ymin, 2), round(bb.zmin, 2),
                                               round(bb.xmax, 2), round(bb.ymax, 2), round(bb.zmax, 2)])
    print(json.dumps(r), flush=True)
    return r


def export_part(name: str, shape: cq.Workplane, rho: float = RHO_CU, stl_tol: float = 0.05,
                step: bool = True, xz: bool = True) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    r = report(name, shape, rho)
    tag = "-lite" if LITE else ""
    stl = OUT / f"{name}{tag}.stl"
    cq.exporters.export(shape, str(stl), tolerance=stl_tol, angularTolerance=0.3)
    r["stl"] = str(stl)
    if step:
        stp = OUT / f"{name}{tag}.step"
        cq.exporters.export(shape, str(stp))
        r["step"] = str(stp)
        r["step_MB"] = round(stp.stat().st_size / 1048576, 1)
        if xz and not LITE:
            subprocess.run(["xz", "-T4", "-6", "-k", "-f", str(stp)], check=True)
            r["step_xz_MB"] = round((OUT / f"{name}.step.xz").stat().st_size / 1048576, 2)
    r["seconds"] = round(time.time() - t0, 1)
    (OUT / f"{name}{tag}.json").write_text(json.dumps(r, indent=1))
    print(json.dumps({k: r[k] for k in r if k not in ("bbox",)}), flush=True)
    return r


def export_dxf(name: str, wp: cq.Workplane) -> str:
    """2-D artwork / flat pattern as DXF (wp must be a planar Workplane with wires or a face)."""
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{name}.dxf"
    cq.exporters.exportDXF(wp, str(path))
    return str(path)


def section(shape: cq.Workplane, axis: str = "x", at: float = 0.0, keep: str = "+") -> cq.Workplane:
    """Half-space cut for section views: keep the '+' or '-' side of the plane axis=at."""
    big = 1000.0
    if axis == "x":
        box = cq.Workplane("XY").box(big, big, big).translate(((big / 2) * (1 if keep == "-" else -1) + at, 0, 0))
    elif axis == "y":
        box = cq.Workplane("XY").box(big, big, big).translate((0, (big / 2) * (1 if keep == "-" else -1) + at, 0))
    else:
        box = cq.Workplane("XY").box(big, big, big).translate((0, 0, (big / 2) * (1 if keep == "-" else -1) + at))
    return shape.cut(box)


if __name__ == "__main__":
    # self-test in LITE mode: a small kerfed core
    os.environ["PRISM_CAD_LITE"] = "1"
    core = comb_core(108, 108, 3.0, 1.5, 2.0, 0.8, [-54 + k * 108 / 14 for k in range(15)], 0.3, (125, 125))
    report("selftest-core", core)
