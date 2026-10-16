"""DDD-grate: CadQuery sanity build of the two grate laminations from the DDD dimensions and the TTV artwork CSV.
Checks that the land plate (1.30 mm: 7 recess pockets, 13 + 2 windows, 2 datums) and the meter web (0.40 mm, 756 holes)
are valid single solids, and reports volume, mass and bounding box. Not the CAD deliverable (that is the CAD lane)."""
import csv, json, os, time
import cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__))
RHO = 8.94e-3
PITCH = 108 / 14; XL = [-54 + PITCH * k for k in range(15)]
OUT, T_LAND, T_WEB = 122.6, 1.30, 0.40
RECESS_W, RECESS_D, WIN, EDGE_WIN = 2.70, 0.80, 1.20, 0.60
t0 = time.time()
# ---- land plate: bottom face at z = 2.8 (fin tips), top at 4.1 ----
land = cq.Workplane("XY").workplane(offset=2.8).rect(OUT, OUT).extrude(T_LAND).edges("|Z").fillet(2.0)
land = land.faces(">Z").workplane().pushPoints([(XL[k], 0) for k in range(1, 15, 2)]).slot2D(109.0, RECESS_W, angle=90).cutBlind(-RECESS_D)
land = land.faces("<Z").workplane().pushPoints([(XL[k], 0) for k in range(2, 14, 2)]).slot2D(108.0, WIN, angle=90).cutThruAll()
land = land.faces("<Z").workplane().pushPoints([(-54 + EDGE_WIN / 2, 0), (54 - EDGE_WIN / 2, 0)]).rect(EDGE_WIN, 108.0).cutThruAll()
land = land.faces("<Z").workplane().pushPoints([(-57, -57)]).hole(3.0).faces("<Z").workplane().pushPoints([(57, 57)]).slot2D(3.4, 3.0, angle=45).cutThruAll()
v = land.val(); bb = v.BoundingBox()
rep = dict(land_plate=dict(valid=v.isValid(), solids=land.solids().size(), volume_mm3=round(v.Volume(), 1), mass_g=round(v.Volume() * RHO, 1),
                           bbox=[round(bb.xmin, 2), round(bb.ymin, 2), round(bb.zmin, 2), round(bb.xmax, 2), round(bb.ymax, 2), round(bb.zmax, 2)], s=round(time.time() - t0, 1)))
print(json.dumps(rep["land_plate"]), flush=True)
# ---- meter web: z 4.1 .. 4.5, holes from the artwork CSV (rounded rectangles as slots/rects) ----
t0 = time.time()
web = cq.Workplane("XY").workplane(offset=2.8 + T_LAND).rect(OUT, OUT).extrude(T_WEB).edges("|Z").fillet(2.0)
rows = list(csv.DictReader(open(os.path.join(HERE, "artwork_prism15_ttv.csv"))))
# one boolean: all holes as plain rectangles (corner radii 0.10/0.15 omitted: < 2 % area, irrelevant to validity/mass)
groups = {}
for r in rows:
    groups.setdefault((float(r["w_mm"]), float(r["h_mm"])), []).append((float(r["x_mm"]), float(r["y_mm"])))
cutter = None
for (w, h), pts in groups.items():
    g = cq.Workplane("XY").workplane(offset=2.8 + T_LAND - 0.1).pushPoints(pts).rect(w, h).extrude(T_WEB + 0.2)
    cutter = g if cutter is None else cutter.union(g, clean=False)
web = web.cut(cutter)
web = web.faces(">Z").workplane().pushPoints([(-57, -57)]).hole(3.0).faces(">Z").workplane().pushPoints([(57, 57)]).slot2D(3.4, 3.0, angle=45).cutThruAll()
v = web.val(); bb = v.BoundingBox()
rep["meter_web"] = dict(valid=v.isValid(), solids=web.solids().size(), holes=len(rows), volume_mm3=round(v.Volume(), 1), mass_g=round(v.Volume() * RHO, 1),
                        bbox=[round(bb.xmin, 2), round(bb.ymin, 2), round(bb.zmin, 2), round(bb.xmax, 2), round(bb.ymax, 2), round(bb.zmax, 2)], s=round(time.time() - t0, 1))
print(json.dumps(rep["meter_web"]), flush=True)
rep["grate_total_mass_g"] = round(rep["land_plate"]["mass_g"] + rep["meter_web"]["mass_g"], 1)
# open-area check from the web: field area minus solid
json.dump(rep, open(os.path.join(HERE, "grate_cq_check.json"), "w"), indent=1)
print(json.dumps({"grate_total_mass_g": rep["grate_total_mass_g"]}))
