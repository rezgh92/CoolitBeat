#!/usr/bin/env python3
"""
PRISM-15 Rev A assembly: reads the part STEP files from out/, checks placement, interference
and mass, exports the assembly STEP (+xz), exploded-view offsets and section STLs.

usage: python3 assembly.py            # full-mode parts (out/<part>.step)
       PRISM_CAD_LITE=1 python3 assembly.py   # LITE parts (out/<part>-lite.step)
"""
import json, os, pathlib, subprocess, sys, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cadquery as cq
from prism_cad import OUT, LITE, RHO_CU, RHO_SS, section, load_params

TAG = "-lite" if LITE else ""
COPPER = (184, 115, 51)
PARTS = [  # name, colour (r,g,b), density, in plate mass?
    ("core", (184, 115, 51), RHO_CU, True),
    ("grate_land", (196, 128, 62), RHO_CU, True),
    ("grate_web", (200, 132, 66), RHO_CU, True),
    ("plenum", (206, 140, 78), RHO_CU, True),
    ("plenum_frames", (206, 140, 78), RHO_CU, True),
    ("separator", (170, 105, 50), RHO_CU, True),
    ("cap", (214, 150, 90), RHO_CU, True),
    ("boss_in", (150, 150, 155), RHO_CU, True),
    ("boss_out", (150, 150, 155), RHO_CU, True),
    ("guard", (190, 190, 195), RHO_SS, True),
    ("screws", (120, 120, 125), RHO_SS, True),
    ("frame", (90, 90, 95), RHO_SS, False),
    ("ttv_block", (120, 110, 100), RHO_CU, False),
    ("ttv_tiles", (230, 230, 225), 3.26e-3, False),
]
EXPLODE_Z = {"core": 0, "grate_land": 12, "grate_web": 20, "plenum": 30, "plenum_frames": 30, "separator": 44,
             "cap": 60, "boss_in": 78, "boss_out": 78, "guard": 90, "screws": 0, "frame": -14, "ttv_block": -8, "ttv_tiles": -8}


def load(name):
    p = OUT / f"{name}{TAG}.step"
    if not p.exists():
        return None
    return cq.importers.importStep(str(p))


def main():
    t0 = time.time()
    P = load_params()
    shapes = {}
    for name, col, rho, inplate in PARTS:
        s = load(name)
        if s is None:
            print(f"missing {name}", flush=True); continue
        shapes[name] = (s, col, rho, inplate)
    # mass and envelope
    report = {"parts": {}, "lite": LITE}
    plate_mass = 0.0
    for name, (s, col, rho, inplate) in shapes.items():
        v = sum(x.Volume() for x in s.solids().vals())
        bb = s.val().BoundingBox()
        m = v * rho
        report["parts"][name] = {"mass_g": round(m, 1), "zmin": round(bb.zmin, 2), "zmax": round(bb.zmax, 2),
                                 "solids": s.solids().size(), "valid": all(x.isValid() for x in s.solids().vals())}
        if inplate:
            plate_mass += m
    report["plate_mass_g"] = round(plate_mass, 1)
    report["height_at_bar_mm"] = round(shapes["cap"][0].val().BoundingBox().zmax, 2) if "cap" in shapes else None
    report["height_with_bosses_mm"] = round(max(shapes[n][0].val().BoundingBox().zmax for n in ("boss_in", "boss_out") if n in shapes), 2) if "boss_in" in shapes else None
    print(json.dumps({k: report[k] for k in ("plate_mass_g", "height_at_bar_mm", "height_with_bosses_mm")}), flush=True)
    # interference: the stacked copper layers, the cap skirt (121.5 inner) against the core rim / tap bosses and against everything
    # inside it, and the bosses and guard against the cap and each other
    pairs = [("core", "grate_land"), ("grate_land", "grate_web"), ("grate_web", "plenum"), ("plenum", "plenum_frames"),
             ("plenum", "separator"), ("plenum_frames", "separator"), ("separator", "cap"), ("cap", "boss_in"),
             ("cap", "boss_out"), ("core", "cap"), ("boss_in", "guard"), ("core", "screws"),
             ("grate_land", "cap"), ("grate_web", "cap"), ("plenum", "cap"), ("plenum_frames", "cap"),
             ("cap", "guard"), ("separator", "guard"), ("boss_out", "guard"), ("boss_in", "boss_out")]
    inter = []
    for a, b in pairs:
        if a in shapes and b in shapes:
            try:
                x = shapes[a][0].intersect(shapes[b][0])
                vol = sum(s.Volume() for s in x.solids().vals()) if x.solids().size() else 0.0
            except Exception as e:
                vol = -1.0
            verdict = "ok" if abs(vol) < 1.0 else ("INTERFERENCE" if vol > 0 else "check-failed")
            inter.append({"pair": f"{a}/{b}", "volume_mm3": round(vol, 2), "verdict": verdict})
            print(json.dumps(inter[-1]), flush=True)
    report["interference"] = inter
    # assembly STEP
    asm = cq.Assembly(name="PRISM15_RevA")
    for name, (s, col, rho, inplate) in shapes.items():
        asm.add(s, name=name, color=cq.Color(col[0] / 255, col[1] / 255, col[2] / 255))
    out = OUT / f"prism15_revA_assembly{TAG}.step"
    asm.save(str(out))
    report["assembly_step"] = str(out)
    if not LITE:
        subprocess.run(["xz", "-T4", "-6", "-k", "-f", str(out)], check=True)
    print("assembly written", round(time.time() - t0, 1), "s", flush=True)
    # exploded offsets
    (OUT / "exploded_offsets.json").write_text(json.dumps(EXPLODE_Z, indent=1))
    # section solids (plate parts only): YZ through an inlet line (k=7, x=0 is an inlet) and an outlet line (k=8),
    # XZ through the inlet port boss / inlet dome (y = bosses.inlet.y) and across the lines at y = 10
    L = P["lines"]
    x_in = [x for x, k in zip(L["x"], L["kind"]) if k == "in"][3]
    x_out = [x for x, k in zip(L["x"], L["kind"]) if k == "out"][3]
    y_hdr = P["bosses"]["inlet"]["y"]
    secs = {"section_inlet": ("x", x_in), "section_outlet": ("x", x_out), "section_header": ("y", y_hdr), "section_across": ("y", 10.0)}
    for sname, (axis, at) in secs.items():
        comp = None
        for name, (s, col, rho, inplate) in shapes.items():
            if not inplate or name in ("screws", "guard"):
                continue
            cut = section(s, axis, at, keep="-")
            if cut.solids().size() == 0:
                continue
            comp = cut if comp is None else comp.add(cut)
        if comp is not None:
            cq.exporters.export(comp, str(OUT / f"{sname}{TAG}.stl"), tolerance=0.05, angularTolerance=0.3)
            print("section", sname, flush=True)
    (OUT / f"assembly_report{TAG}.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report["parts"]), flush=True)
    return report


if __name__ == "__main__":
    main()
