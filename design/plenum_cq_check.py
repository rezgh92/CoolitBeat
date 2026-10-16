"""DDD-plenum: CadQuery sanity build of the folded plenum (square-wave corrugation with bend radii, top-flat windows,
bottom-flat slots, bleed holes, wall tabs), the two comb end frames and the 1.8 mm separator, from the DDD dimensions.
Checks single valid solids, volume/mass, bounding box and that every wall foot lands on a grate land (no hole under it).
Not the CAD deliverable (CAD lane). Output: plenum_cq_check.json. Run: python3 plenum_cq_check.py (~20 s)."""
import csv, json, math, os, time
import cadquery as cq
HERE = os.path.dirname(os.path.abspath(__file__)); RHO = 8.94e-3
P = 108 / 14; XL = [-54 + P * k for k in range(15)]; XW = [-54 - P / 2 + P * j for j in range(16)]
T, RI, H, ZG, FLANGE, L_CH, TAB = 0.80, 0.60, 5.80, 4.50, 1.50, 114.0, 1.0; RO = RI + T
SEP_T, SEP_OUT, FR_T, FR_H = 1.80, 122.6, 2.5, 5.78
rep = {}; t0 = time.time()
# ---- corrugation: centreline path in the XZ plane (x across lines, z up), offset2D by +/- t/2, extruded along Y ----
zc_lo, zc_hi = ZG + T / 2, ZG + H - T / 2            # centreline heights of bottom / top flats
rc = RI + T / 2                                        # centreline bend radius 1.0
def arc_pts(cx, cz, r, a0, a1, n=6):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cz + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
pts = [(XW[0] - rc - FLANGE, zc_hi)]                   # -x flange free edge (top level, outward)
pts += arc_pts(XW[0] - rc, zc_hi - rc, rc, 90, 0)[1:]  # flange -> wall 0 (down)
for j in range(16):
    x = XW[j]; down = (j % 2 == 0)                    # even walls go top -> bottom in the +x sweep
    if down:
        pts += [(x, zc_lo + rc)]; pts += arc_pts(x + rc, zc_lo + rc, rc, 180, 270)[1:]          # foot into bottom flat
        if j < 15: pts += [(XW[j + 1] - rc, zc_lo)]; pts += arc_pts(XW[j + 1] - rc, zc_lo + rc, rc, 270, 360)[1:]   # bottom flat -> next wall up
    else:
        pts += [(x, zc_hi - rc)]; pts += arc_pts(x + rc, zc_hi - rc, rc, 180, 90)[1:]           # top into top flat
        if j < 15: pts += [(XW[j + 1] - rc, zc_hi)]; pts += arc_pts(XW[j + 1] - rc, zc_hi - rc, rc, 90, 0)[1:]       # top flat -> next wall down
# wall 15 goes bottom -> top then flange outward (+x)
pts += [(XW[15], zc_hi - rc)]; pts += arc_pts(XW[15] + rc, zc_hi - rc, rc, 180, 90)[1:]; pts += [(XW[15] + rc + FLANGE, zc_hi)]
clean = [pts[0]]
for q in pts[1:]:
    if abs(q[0] - clean[-1][0]) > 1e-6 or abs(q[1] - clean[-1][1]) > 1e-6: clean.append(q)
path = cq.Workplane("XZ").polyline(clean)
prof = path.offset2D(T / 2, "arc")                     # closed band of thickness T around the open centreline
corr = prof.extrude(-L_CH / 2, both=True) if False else prof.extrude(L_CH / 2, both=True)
# wall tabs (straight wall region only) beyond y +/-57
tabs = None   # only the protruding tab (plus 0.05 overlap), slightly inside the straight wall in z, so no coplanar faces
for j in range(16):
    for sgn in (-1, 1):
        tb = cq.Workplane("XY").box(T, TAB + 0.05, H - 2 * RO - 0.1, centered=(True, True, False)).translate((XW[j], sgn * (L_CH / 2 + TAB / 2 - 0.025), ZG + RO + 0.05))
        tabs = tb if tabs is None else tabs.union(tb, clean=False)
corr = corr.union(tabs)
# top-flat windows (5 x 10 r1 at y -21/-7 on inlet lines), bottom-flat slots (1.8 x 110 r0.9 on outlet lines), bleed holes
cut = cq.Workplane("XY").workplane(offset=ZG - 0.1).pushPoints([(XL[k], y) for k in range(1, 15, 2) for y in (-21.0, -7.0)]).rect(5.0, 10.0).extrude(H + 0.2)
cut = cut.union(cq.Workplane("XY").workplane(offset=ZG - 0.1).pushPoints([(XL[k], 0) for k in range(0, 15, 2)]).slot2D(110.0, 1.8, angle=90).extrude(H + 0.2), clean=False)
for j in range(1, 15):
    y = 55.5 if j % 2 == 0 else -55.5
    cut = cut.union(cq.Workplane("YZ").workplane(offset=XW[j] - 1).center(y, 7.40).circle(0.55).extrude(2.0), clean=False)
corr = corr.cut(cut)
v = corr.val(); bb = v.BoundingBox()
rep["corrugation"] = dict(valid=v.isValid(), solids=corr.solids().size(), volume_mm3=round(v.Volume(), 1), mass_g=round(v.Volume() * RHO, 1),
                          bbox=[round(c, 2) for c in (bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax)], s=round(time.time() - t0, 1))
print(json.dumps(rep["corrugation"]), flush=True)
# ---- end frames: bars 2.5 (y) x 5.78 (z) x 120.71 (x) with 16 comb slots 0.9 x 1.0 deep, at y +/-(57 .. 59.5) ----
t0 = time.time(); FR_L = 2 * (abs(XW[0]) + T / 2 + RI + FLANGE); frames = None
for sgn in (-1, 1):
    fr = cq.Workplane("XY").box(FR_L, FR_T, FR_H, centered=(True, True, False)).translate((0, sgn * (L_CH / 2 + FR_T / 2), ZG))
    slots = cq.Workplane("XY").box(0.9, 2 * TAB, FR_H + 0.2, centered=(True, True, False)).translate((XW[0], sgn * L_CH / 2, ZG - 0.1))
    for j in range(1, 16): slots = slots.union(cq.Workplane("XY").box(0.9, 2 * TAB, FR_H + 0.2, centered=(True, True, False)).translate((XW[j], sgn * L_CH / 2, ZG - 0.1)), clean=False)
    fr = fr.cut(slots); frames = fr if frames is None else frames.union(fr, clean=False)
v = frames.val(); rep["end_frames"] = dict(valid=v.isValid(), solids=frames.solids().size(), volume_mm3=round(v.Volume(), 1), mass_g=round(v.Volume() * RHO, 1), s=round(time.time() - t0, 1))
print(json.dumps(rep["end_frames"]), flush=True)
# ---- separator: 1.8 mm, 122.6 sq r2, 46 windows, datums, 2 tap holes (option) ----
t0 = time.time(); z0 = ZG + H
sep = cq.Workplane("XY").workplane(offset=z0).rect(SEP_OUT, SEP_OUT).extrude(SEP_T).edges("|Z").fillet(2.0)
win = [(XL[k], y, 5.0, 10.0) for k in range(1, 15, 2) for y in (-21.0, -7.0)] + [(XL[k], y, 5.0, 10.0) for k in range(2, 14, 2) for y in (9.0, 23.0, 37.0, 51.0)] \
    + [(XL[k], y, 5.0, 5.0) for k in (0, 14) for y in (9.0, 23.0, 37.0, 51.0)]
cutter = None
for x, y, w, h in win:
    c = cq.Workplane("XY").workplane(offset=z0 - 0.1).center(x, y).rect(w, h).extrude(SEP_T + 0.2).edges("|Z").fillet(1.0)
    cutter = c if cutter is None else cutter.union(c, clean=False)
sep = sep.cut(cutter)
sep = sep.faces(">Z").workplane().pushPoints([(-57, -57)]).hole(3.0).faces(">Z").workplane().pushPoints([(57, 57)]).slot2D(3.4, 3.0, angle=45).cutThruAll()
sep = sep.faces(">Z").workplane().pushPoints([(0.0, -53.0), (P, -53.0)]).hole(1.5)
v = sep.val(); bb = v.BoundingBox()
rep["separator_1p8"] = dict(valid=v.isValid(), solids=sep.solids().size(), windows=len(win), volume_mm3=round(v.Volume(), 1), mass_g=round(v.Volume() * RHO, 1),
                            bbox=[round(c, 2) for c in (bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax)], s=round(time.time() - t0, 1))
print(json.dumps(rep["separator_1p8"]), flush=True)
# ---- foot-on-land check against the grate artwork: no web hole within 0.30 of any bottom-flat contact strip ----
rows = list(csv.DictReader(open(os.path.join(HERE, "artwork_prism15_ttv.csv"))))
strip = []  # (x_lo, x_hi) of contact strips: |x - x_out| in [0.9, 2.857] both sides of every outlet line
for k in range(0, 15, 2): strip += [(XL[k] - 2.857, XL[k] - 0.9), (XL[k] + 0.9, XL[k] + 2.857)]
viol = [r for r in rows if any(lo - 0.30 < float(r["x_mm"]) + float(r["w_mm"]) / 2 and float(r["x_mm"]) - float(r["w_mm"]) / 2 < hi + 0.30 for lo, hi in strip)]
rep["holes_within_0p3_of_contact_strips"] = len(viol)
rep["plenum_total_mass_g"] = round(rep["corrugation"]["mass_g"] + rep["end_frames"]["mass_g"], 1)
json.dump(rep, open(os.path.join(HERE, "plenum_cq_check.json"), "w"), indent=1); print(json.dumps({k: rep[k] for k in ("plenum_total_mass_g", "holes_within_0p3_of_contact_strips")}))
