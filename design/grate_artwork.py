"""DDD-grate: graded orifice artwork generator for the PRISM-15 Rev A metered grate (meter web, 0.40 mm lamination).

Physics (appendix/verify/ctl/plenum_graded.py, PKG-A run, unchanged): 1-D centre-fed plenum pair. One inlet channel
(W x Hp, fed at y_in through the separator window) and one outlet channel (drained at y_out). 0.25 mm sub-branches
along the field; each branch = fin segment (viscous R1) + meter + outlet row + misc (inertial R2). Momentum
coefficients th_i = 1.0 (dividing), th_o = 2.0 (combining); laminar friction fRe 62/69. Along-plenum profile and
meter both scale with u^2, so orifice AREAS graded along y cancel the profile at every flow. Areas are quantised to
5 laser/punch sizes (architecture 4.1).
Outputs (same folder): artwork_prism15_ttv.csv/.dxf, artwork_prism_g_example.csv/.dxf, grate_artwork.out,
grate_artwork_params.json.   Run: python3 grate_artwork.py   (~60 s)
Conventions (cad/prism_cad.py): X along the fins (across the lines), Y along the lines, origin at the field centre."""
import csv, math, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
rho, mu = 1005.0, 1.25e-3          # PG25 at 45-50 C
LPM = 1 / 60000; CD = 0.72          # Cd: architecture 4.2, coupon-gated (E2)
# ---------------- fixed geometry (architecture 2.2 / 4.1; DDD-grate sections 3-4) ----------------
FIELD = 108.0; NLINES = 15; PITCH = FIELD / 14                       # 7.7143 mm
XLINE = [-FIELD / 2 + PITCH * k for k in range(NLINES)]
INLET_K = [k for k in range(NLINES) if k % 2 == 1]; OUTLET_K = [k for k in range(NLINES) if k % 2 == 0]
W_PLEN, H_PLEN = 6.9e-3, 5.0e-3     # inlet / outlet channel section (folded plenum, 0.8 mm legs)
Y_IN, Y_OUT = -14e-3, 14e-3         # separator window centres of the architecture-of-record model
N_ORIF, ORIF_PITCH = 54, 2.0
Y_ORIF = np.array([-(N_ORIF - 1) / 2 * ORIF_PITCH + ORIF_PITCH * j for j in range(N_ORIF)])   # -53 .. +53
W_IN, R_IN = 0.50, 0.10             # inlet orifice width (x) and corner radius
W_OUT, R_OUT = 1.00, 0.15           # interior outlet hole width and corner radius
W_EDGE, L_EDGE, R_EDGE = 0.40, 2.78, 0.10   # edge-line outlet slot, 27 at 4 mm pitch
RECESS_W, WINDOW_W, EDGE_WIN = 2.70, 1.20, 0.60   # land plate: recess, window, half-width edge window
X_OFF = 1.00                        # inlet orifice centre offset from the line centre (jet lands on the 0.75 lip)
U_MEAN_18 = 1.54; DP_METER_18 = 0.5 * rho * U_MEAN_18**2 / CD**2 / 1e3     # 2.30 kPa
DP_ROW, DP_FIN, DP_MISC = 0.50, 1.07, 0.08                                    # kPa (row, fin L7.7 viscous, misc)
A_RR = lambda w, h, r: w * h - (4 - math.pi) * r * r
H_RR = lambda A, w, r: (A + (4 - math.pi) * r * r) / w
U_ROW = CD * math.sqrt(2 * DP_ROW * 1e3 / rho)                              # 0.718 m/s

# ---------------- 1-D plenum solver (ctl/plenum_graded.py run(), + target weights, zero-target cells, feed spread) ----
def plenum(W, Hp, Q, dp0, fvisc, r2scale=None, y_in=Y_IN, y_out=Y_OUT, th_i=1.0, th_o=2.0, n=432, target=None,
           Lp=FIELD * 1e-3, feed_half=0.0):
    A = W * Hp; Dh = 2 * A / (2 * (W + Hp)); fRe = 69.0 if Hp / W > 2.5 else 62.0
    dy = Lp / n; y = (np.arange(n) + 0.5) * dy - Lp / 2
    act = np.ones(n, bool) if target is None else target > 0
    q0 = Q / act.sum()
    R1 = fvisc * dp0 / q0 * np.ones(n); R2 = (1 - fvisc) * dp0 / q0**2 * (np.ones(n) if r2scale is None else r2scale)
    R2[~act] = 1e12
    q = np.where(act, q0, 0.0) if target is None else Q * target / target.sum()
    i_in = int(np.argmin(abs(y - y_in))); i_out = int(np.argmin(abs(y - y_out)))
    if feed_half > 0:
        wfeed = ((y >= y_in - feed_half) & (y <= y_in + feed_half)).astype(float); wfeed /= wfeed.sum()
    for it in range(3000):
        cum = np.cumsum(q); br_cum = np.concatenate([[0.0], cum])
        if feed_half > 0:
            F_in = np.concatenate([[0.0], np.cumsum(wfeed)]) * Q - br_cum
        else:
            F_in = np.where(np.arange(n + 1) <= i_in, -br_cum, Q - br_cum)
        F_out = np.where(np.arange(n + 1) <= i_out, br_cum, -(Q - br_cum))
        u_in = F_in / A; u_out = F_out / A
        def march(u, i0, th):
            p = np.zeros(n)
            for j in range(i0 + 1, n):
                p[j] = p[j - 1] - (fRe * mu / (2 * Dh**2)) * u[j] * dy - th * rho * (u[j + 1]**2 - u[j]**2) / 2.0
            for j in range(i0 - 1, -1, -1):
                p[j] = p[j + 1] + (fRe * mu / (2 * Dh**2)) * u[j + 1] * dy + th * rho * (u[j + 1]**2 - u[j]**2) / 2.0
            return p
        p_in = march(u_in, i_in, th_i); p_out = march(u_out, i_out, th_o)
        def qs(P):
            dp = np.maximum(P + p_in - p_out, 1e-6); return (-R1 + np.sqrt(R1**2 + 4 * R2 * dp)) / (2 * R2)
        lo, hi = 0.0, 1e6
        for _ in range(100):
            mid = 0.5 * (lo + hi)
            if qs(mid).sum() > Q: hi = mid
            else: lo = mid
        qn = qs(0.5 * (lo + hi))
        if np.max(abs(qn - q)) / q0 < 1e-9: break
        q = 0.7 * q + 0.3 * qn
    return q / q0

def profile(lpm, sc, n_in=7, meter=DP_METER_18, row=DP_ROW, fin=DP_FIN, misc=DP_MISC, target=None, **kw):
    s = lpm / 18.0; inert = (meter + misc + row) * s * s; visc = fin * s; dp0 = (inert + visc) * 1e3
    return plenum(W_PLEN, H_PLEN, lpm / n_in / 60000.0, dp0, visc / (inert + visc), r2scale=sc, target=target, **kw)

def grade(n_levels=5, n_iter_cont=8, n_iter_q=4, **kw):
    """Continuous grading, then quantisation to n_levels R2 levels (Lloyd), re-solve and correct. Returns
    (R2 scale per 0.25 mm cell, level R2 scales, per-orifice level index)."""
    sc = np.ones(432)
    for k in range(n_iter_cont):
        r = profile(18.0, sc, **kw); sc = sc * r**1.6; sc = sc / np.mean(sc)
    blk = sc.reshape(N_ORIF, 8).mean(1); levels = np.quantile(blk, np.linspace(0.1, 0.9, n_levels))
    for _ in range(50):
        idx = np.array([np.argmin(abs(levels - b)) for b in blk])
        new = np.array([blk[idx == i].mean() if np.any(idx == i) else levels[i] for i in range(n_levels)])
        if np.allclose(new, levels): break
        levels = new
    for k in range(n_iter_q):
        idx = np.array([np.argmin(abs(levels - b)) for b in blk]); scq = np.repeat(levels[idx], 8)
        r = profile(18.0, scq, **kw); blk = blk * (r.reshape(N_ORIF, 8).mean(1))**1.6; blk = blk / blk.mean()
        levels = np.array([blk[idx == i].mean() if np.any(idx == i) else levels[i] for i in range(n_levels)])
    idx = np.array([np.argmin(abs(levels - b)) for b in blk])
    return np.repeat(levels[idx], 8), levels, idx

# ---------------- DXF writer (both laminations on separate layers) ----------------
def rr_vertices(cx, cy, w, h, r):
    b = math.tan(math.pi / 8); x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    if r <= 1e-9: return [(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)]
    return [(x0 + r, y0, 0), (x1 - r, y0, b), (x1, y0 + r, 0), (x1, y1 - r, b), (x1 - r, y1, 0), (x0 + r, y1, b),
            (x0, y1 - r, 0), (x0, y0 + r, b)]

def write_dxf(path, holes, extras, title):
    try:
        import ezdxf
    except ImportError:
        return False
    doc = ezdxf.new("R2010", setup=True); doc.units = ezdxf.units.MM; msp = doc.modelspace()
    for name, color in (("WEB_ORIFICE_INLET", 1), ("WEB_ORIFICE_OUTLET", 5), ("LAND_RECESS_TOP", 3), ("LAND_WINDOW_THRU", 4),
                        ("LAND_GROOVE_BOTH_FACES", 2), ("OUTLINE_BOTH", 7), ("DATUM_BOTH", 6), ("MASK_NO_FILLER", 30), ("REF", 8)):
        doc.layers.add(name, color=color)
    for h in holes:
        msp.add_lwpolyline(rr_vertices(h["x_mm"], h["y_mm"], h["w_mm"], h["h_mm"], h["r_mm"]), format="xyb", close=True,
                           dxfattribs={"layer": "WEB_ORIFICE_INLET" if h["type"] == "inlet" else "WEB_ORIFICE_OUTLET"})
    for e in extras:
        if e["kind"] == "rr":
            msp.add_lwpolyline(rr_vertices(e["cx"], e["cy"], e["w"], e["h"], e.get("r", 0)), format="xyb", close=True, dxfattribs={"layer": e["layer"]})
        elif e["kind"] == "circle":
            msp.add_circle((e["cx"], e["cy"]), e["r"], dxfattribs={"layer": e["layer"]})
        elif e["kind"] == "line":
            msp.add_line((e["x0"], e["y0"]), (e["x1"], e["y1"]), dxfattribs={"layer": e["layer"]})
    msp.add_text(title, dxfattribs={"layer": "REF", "height": 2.0}).set_placement((-60, 68))
    doc.saveas(path); return True

def land_extras(outline, pins, lines, win_len, field_x):
    """lines: list of (x, kind) with kind in {'in','out','edge'}; recess + grooves at inlets, windows at all lines."""
    ox, oy = outline
    ex = [dict(kind="rr", cx=0, cy=0, w=ox, h=oy, r=2.0, layer="OUTLINE_BOTH")]
    ex.append(dict(kind="circle", cx=pins[0][0], cy=pins[0][1], r=1.5, layer="DATUM_BOTH"))
    ex.append(dict(kind="rr", cx=pins[1][0], cy=pins[1][1], w=3.4, h=3.0, r=1.5, layer="DATUM_BOTH"))
    for x, kind in lines:
        if kind == "in":
            ex.append(dict(kind="rr", cx=x, cy=0, w=RECESS_W, h=win_len + 1.0, r=RECESS_W / 2, layer="LAND_RECESS_TOP"))
            ex.append(dict(kind="rr", cx=x, cy=0, w=RECESS_W + 0.6, h=win_len + 1.6, r=RECESS_W / 2 + 0.3, layer="MASK_NO_FILLER"))
            for sgn in (-1, 1):   # top-face groove outside the recess, inside the mask zone
                xg = x + sgn * (RECESS_W / 2 + 0.175)
                ex.append(dict(kind="line", x0=xg, y0=-(win_len / 2 + 0.8), x1=xg, y1=win_len / 2 + 0.8, layer="LAND_GROOVE_BOTH_FACES"))
        if kind == "edge":
            sgn = -1 if x < 0 else 1; cx = x - sgn * EDGE_WIN / 2
            ex.append(dict(kind="rr", cx=cx, cy=0, w=EDGE_WIN, h=win_len, r=0.2, layer="LAND_WINDOW_THRU"))
            ex.append(dict(kind="rr", cx=cx - sgn * 0.15, cy=0, w=EDGE_WIN + 0.3, h=win_len + 0.6, r=0.3, layer="MASK_NO_FILLER"))
            xg = cx - sgn * (EDGE_WIN / 2 + 0.175)
            ex.append(dict(kind="line", x0=xg, y0=-(win_len / 2 + 0.3), x1=xg, y1=win_len / 2 + 0.3, layer="LAND_GROOVE_BOTH_FACES"))
        else:
            ex.append(dict(kind="rr", cx=x, cy=0, w=WINDOW_W, h=win_len, r=0.6, layer="LAND_WINDOW_THRU"))
            ex.append(dict(kind="rr", cx=x, cy=0, w=WINDOW_W + 0.6, h=win_len + 0.6, r=0.9, layer="MASK_NO_FILLER"))
            for sgn in (-1, 1):   # underside groove 0.775 from the window centre; top-face groove at outlets too
                xg = x + sgn * (WINDOW_W / 2 + 0.175)
                ex.append(dict(kind="line", x0=xg, y0=-(win_len / 2 + 0.3), x1=xg, y1=win_len / 2 + 0.3, layer="LAND_GROOVE_BOTH_FACES"))
    return ex

COLS = ["line_id", "line_x_mm", "orifice_index", "x_mm", "y_mm", "w_mm", "h_mm", "type", "r_mm", "area_mm2", "size_step",
        "lip_side", "zone", "q_rel_18lpm", "u_18lpm_m_s", "lamination"]
def hole(line_id, xl, j, x, y, w, h, typ, r, A, step, side, zone, qrel, u):
    return dict(line_id=line_id, line_x_mm=round(xl, 4), orifice_index=j, x_mm=round(x, 4), y_mm=round(y, 3), w_mm=w, h_mm=h, type=typ,
                r_mm=r, area_mm2=round(A, 4), size_step=step, lip_side=side, zone=zone, q_rel_18lpm=round(qrel, 4),
                u_18lpm_m_s=round(u, 3), lamination="meter_web_0.40")
def write_csv(path, holes):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS); w.writeheader()
        for h in holes: w.writerow({c: h.get(c, "") for c in COLS})

# =====================================================================================================
def ttv(out):
    Q18 = 18 * LPM; n_in = 7
    A_total = Q18 / U_MEAN_18 * 1e6; A_mean = A_total / (n_in * N_ORIF)
    out += [f"# grate_artwork.py output (DDD-grate)", f"geometry: field {FIELD} mm, {NLINES} lines at {PITCH:.4f} mm, inlets at x = " +
            ", ".join(f"{XLINE[k]:+.3f}" for k in INLET_K),
            f"meter: mean u {U_MEAN_18} m/s at 18 LPM, Cd {CD} -> {DP_METER_18:.3f} kPa; outlet row {DP_ROW} kPa; fin {DP_FIN} kPa viscous; misc {DP_MISC}",
            f"total inlet open area {A_total:.1f} mm2 -> mean orifice area {A_mean:.4f} mm2 ({n_in * N_ORIF} orifices); orifice centre at x_line +/- {X_OFF} (lip 0.60-1.35)"]
    scq, levels, idx = grade()
    a_rel = 1 / np.sqrt(levels); a_rel = a_rel / np.mean(a_rel[idx]); areas = a_rel * A_mean
    lengths_r = np.round([H_RR(a, W_IN, R_IN) for a in areas], 2); areas_r = np.array([A_RR(W_IN, L, R_IN) for L in lengths_r])
    order = np.argsort(-areas_r); step_of = {lv: s + 1 for s, lv in enumerate(order)}
    out += ["\n## TTV inlet orifice size steps (w 0.50 mm, r 0.10; length along the line, y)",
            "| step | R2 scale | relative area | area mm2 | length mm | count (7 lines) | share |", "|---|---|---|---|---|---|---|"]
    for s, lv in enumerate(order):
        cnt = int(np.sum(idx == lv)) * n_in
        out.append(f"| {s + 1} | {levels[lv]:.4f} | {a_rel[lv]:.4f} | {areas_r[lv]:.4f} | {lengths_r[lv]:.2f} | {cnt} | {cnt / 378 * 100:.1f} % |")
    out.append(f"area span (largest/smallest) {areas_r.max() / areas_r.min():.3f}x; total open area as drawn {areas_r[idx].sum() * n_in:.1f} mm2")
    sc_drawn = np.repeat((A_mean / areas_r[idx])**2, 8); sc_drawn = sc_drawn / sc_drawn.mean() * scq.mean()
    out += ["\n## TTV along-plenum flow ratio (feed windows at y -14 / +14 mm)",
            "| LPM | ungraded max/min (cell) | graded max/min (cell) | graded max/min per orifice | per-orifice min / max |", "|---|---|---|---|---|"]
    rows = []
    for lpm in (9, 18, 22.5, 27, 36):
        r0 = profile(lpm, None); r1 = profile(lpm, sc_drawn); b1 = r1.reshape(N_ORIF, 8).mean(1)
        rows.append((lpm, b1.max() / b1.min())); out.append(f"| {lpm} | {r0.max() / r0.min():.3f} | {r1.max() / r1.min():.3f} | {b1.max() / b1.min():.3f} | {b1.min():.3f} / {b1.max():.3f} |")
    r18 = profile(18, sc_drawn); q_orif = r18.reshape(N_ORIF, 8).mean(1); q_abs = q_orif * Q18 / n_in / N_ORIF
    u_orif = q_abs / (areas_r[idx] * 1e-6); dp_orif = 0.5 * rho * u_orif**2 / CD**2 / 1e3
    out += [f"\nper-orifice flow at 18 LPM: {q_abs.mean() * 6e7:.3f} mL/min mean, spread {q_orif.min():.3f} .. {q_orif.max():.3f} (+/-{(q_orif.max() - q_orif.min()) / 2 * 100:.1f} %)",
            f"orifice velocity at 18 LPM: mean {u_orif.mean():.3f}, min {u_orif.min():.3f}, max {u_orif.max():.3f} m/s (step {step_of[idx[np.argmax(u_orif)]]}, y = {Y_ORIF[np.argmax(u_orif)]:+.0f} mm)",
            f"orifice dp at 18 LPM: flow-weighted mean {np.average(dp_orif, weights=q_orif):.3f} kPa (check <= 2.3), min {dp_orif.min():.3f}, max {dp_orif.max():.3f} kPa"]
    for lpm in (15, 18, 22.5, 23.4, 27, 36):
        s = lpm / 18; out.append(f"  {lpm} LPM: mean u {u_orif.mean() * s:.2f} m/s, max orifice u {u_orif.max() * s:.2f} m/s, mean dp {np.average(dp_orif, weights=q_orif) * s * s:.2f} kPa")
    out += ["\n## TTV sensitivity (as drawn; per-orifice max/min)", "| case | 18 LPM | 36 LPM |", "|---|---|---|"]
    for lab, kw in (("as designed", {}), ("Cd 0.80 (meter 1.86 kPa)", dict(meter=0.5 * rho * U_MEAN_18**2 / 0.80**2 / 1e3)),
                    ("Cd 0.65 (meter 2.82 kPa)", dict(meter=0.5 * rho * U_MEAN_18**2 / 0.65**2 / 1e3)), ("no outlet row", dict(row=0.0)),
                    ("window centres at -16 / +16 mm", dict(y_in=-16e-3, y_out=16e-3)), ("window centres at -12 / +12 mm", dict(y_in=-12e-3, y_out=12e-3)),
                    ("feed spread over 2 arches (y -26 .. -2)", dict(feed_half=12e-3)), ("ungraded artwork", "ungraded")):
        res = []
        for lpm in (18, 36):
            r = profile(lpm, None) if kw == "ungraded" else profile(lpm, sc_drawn, **kw); b = r.reshape(N_ORIF, 8).mean(1); res.append(b.max() / b.min())
        out.append(f"| {lab} | {res[0]:.3f} | {res[1]:.3f} |")
    Q_line = Q18 / n_in; A_int = A_RR(W_OUT, 1.12, R_OUT); A_edge = A_RR(W_EDGE, L_EDGE, R_EDGE)
    dp_int = 0.5 * rho * (Q_line / (54 * A_int * 1e-6))**2 / CD**2 / 1e3; dp_edge = 0.5 * rho * (Q_line / 2 / (27 * A_edge * 1e-6))**2 / CD**2 / 1e3
    out += [f"\n## Outlet rows: interior 54 x ({W_OUT} x 1.12 r{R_OUT}) = {54 * A_int:.1f} mm2 -> {dp_int:.3f} kPa at 2.571 LPM; edge 27 x ({W_EDGE} x {L_EDGE} r{R_EDGE}) at 4 mm = {27 * A_edge:.1f} mm2 -> {dp_edge:.3f} kPa at 1.286 LPM",
            f"outlet holes {6 * 54 + 2 * 27}; outlet open area {6 * 54 * A_int + 2 * 27 * A_edge:.1f} mm2; grate holes total {378 + 6 * 54 + 2 * 27}"]
    holes = []
    for li, k in enumerate(INLET_K):
        for j in range(N_ORIF):
            side = +1 if j % 2 == 0 else -1; lv = idx[j]
            holes.append(hole(f"I{li + 1}", XLINE[k], j + 1, XLINE[k] + side * X_OFF, Y_ORIF[j], W_IN, float(lengths_r[lv]), "inlet", R_IN,
                              float(areas_r[lv]), step_of[lv], "+x" if side > 0 else "-x", "uniform", float(q_orif[j]), float(u_orif[j])))
    for oi, k in enumerate(OUTLET_K):
        if k in (0, NLINES - 1):
            sgn = -1 if XLINE[k] < 0 else 1; xc = XLINE[k] - sgn * EDGE_WIN / 2
            for n_ in range(27):
                holes.append(hole(f"O{oi + 1}", XLINE[k], n_ + 1, xc, -52.0 + 4.0 * n_, W_EDGE, L_EDGE, "outlet", R_EDGE, A_edge, 0, "edge", "outlet", 1.0,
                                  Q_line / 2 / (27 * A_edge * 1e-6)))
        else:
            for j in range(N_ORIF):
                holes.append(hole(f"O{oi + 1}", XLINE[k], j + 1, XLINE[k], Y_ORIF[j], W_OUT, 1.12, "outlet", R_OUT, A_int, 0, "centre", "outlet", 1.0,
                                  Q_line / (54 * A_int * 1e-6)))
    write_csv(os.path.join(HERE, "artwork_prism15_ttv.csv"), holes)
    lines = [(XLINE[k], "edge" if k in (0, 14) else ("in" if k in INLET_K else "out")) for k in range(NLINES)]
    ok = write_dxf(os.path.join(HERE, "artwork_prism15_ttv.dxf"), holes, land_extras((122.6, 122.6), ((-57.0, -57.0), (57.0, 57.0)), lines, 108.0, FIELD),
                   "PRISM-15 Rev A TTV grate artwork - DDD-grate - mm - datum: field centre; pins (-57,-57) round, (57,57) slot")
    inl = [h for h in holes if h["type"] == "inlet"]
    out += [f"\nTTV CSV: {len(holes)} holes; DXF written: {ok}; inlet area {sum(h['area_mm2'] for h in inl):.1f} mm2, mean u {Q18 / (sum(h['area_mm2'] for h in inl) * 1e-6):.3f} m/s",
            "step sequence along each inlet line, y = -53 .. +53 (step 1 = largest): " + " ".join(str(step_of[lv]) for lv in idx)]
    return dict(inlet_steps=[dict(step=s + 1, length_mm=float(lengths_r[lv]), area_mm2=round(float(areas_r[lv]), 4), count=int(np.sum(idx == lv)) * n_in) for s, lv in enumerate(order)],
                inlet_area_span=round(float(areas_r.max() / areas_r.min()), 3), inlet_total_area_mm2=round(float(areas_r[idx].sum() * n_in), 1),
                mean_u_18lpm=round(float(u_orif.mean()), 3), max_u_18lpm=round(float(u_orif.max()), 3), mean_dp_18lpm_kpa=round(float(np.average(dp_orif, weights=q_orif)), 3),
                per_orifice_maxmin={str(a): round(b, 3) for a, b in rows}, outlet_interior=dict(n=54, w_mm=W_OUT, h_mm=1.12, r_mm=R_OUT, area_mm2=round(A_int, 4), dp_18lpm_kpa=round(dp_int, 3)),
                outlet_edge=dict(n=27, w_mm=W_EDGE, h_mm=L_EDGE, r_mm=R_EDGE, pitch_mm=4.0, area_mm2=round(A_edge, 4), dp_18lpm_kpa=round(dp_edge, 3)),
                step_sequence=[step_of[lv] for lv in idx], holes_total=len(holes))

# =====================================================================================================
def prism_g(out):
    """Zoned example: 4 dies 26 x 33 at 350 W/cm2 + 16 HBM 11 x 12 at 40 W/cm2 on 110 x 120. Flux-graded line pitch
    (architecture 3.3): 5.5 mm over the die block (L 5.5), 11 mm over HBM/margin (L 11); 17 lines, edge outlets."""
    FX, FY = 110.0, 120.0; Qg = 18 * LPM
    lines = [(0.0, "out")] + [(s * x, k) for s in (-1, 1) for x, k in ((5.5, "in"), (11.0, "out"), (16.5, "in"), (22.0, "out"), (27.5, "in"), (33.0, "out"), (44.0, "in"), (55.0, "edge"))]
    lines.sort(); xs_in = [x for x, k in lines if k == "in"]; xs_out = [x for x, k in lines if k != "in"]
    dies = [(sx * 15.0, sy * 18.5, 26.0, 33.0) for sx in (-1, 1) for sy in (-1, 1)]
    hbm = [(sx * cx, cy, 11.0, 12.0) for sx in (-1, 1) for cx in (35.5, 48.5) for cy in (-21.0, -7.0, 7.0, 21.0)]
    Q_DIE, Q_HBM = 350.0, 40.0; DIL_DIE, DIL_HBM = 3.0, 2.0
    def flux(x, y):
        for (cx, cy, w, h) in dies:
            if abs(x - cx) <= w / 2 + DIL_DIE and abs(y - cy) <= h / 2 + DIL_DIE: return Q_DIE
        for (cx, cy, w, h) in hbm:
            if abs(x - cx) <= w / 2 + DIL_HBM and abs(y - cy) <= h / 2 + DIL_HBM: return Q_HBM
        return 0.0
    P_die = 4 * 26 * 33 * Q_DIE / 100; P_hbm = 16 * 11 * 12 * Q_HBM / 100
    n_cells = 480; ycell = (np.arange(n_cells) + 0.5) * (FY / n_cells) - FY / 2; n_pos = 60; y_pos = -59.0 + 2.0 * np.arange(n_pos)
    out += [f"\n# PRISM-G example artwork: 4 dies 26 x 33 at 350 W/cm2 ({P_die:.0f} W) + 16 HBM 11 x 12 at 40 W/cm2 ({P_hbm:.0f} W) = {P_die + P_hbm:.0f} W on 110 x 120 mm",
            "lines (x, kind): " + ", ".join(f"{x:+.1f} {k}" for x, k in lines), "line pitch 5.5 mm (L 5.5) over the die block, 11 mm (L 11) over HBM and margin; mid-fed plenums at y -14 / +14 (assumed)"]
    # per-line targets: heat under the strip served by each inlet (half-way to each neighbouring outlet)
    targets, heat_line, Lseg, Wch = {}, {}, {}, {}
    for x in xs_in:
        lo = max(xo for xo in xs_out if xo < x); hi = min(xo for xo in xs_out if xo > x); Lseg[x] = (hi - lo) / 2; Wch[x] = Lseg[x] - 0.8   # channel width = line pitch - 0.8 leg
        xs = np.linspace(lo, hi, 24)
        t = np.array([np.mean([flux(xx, y) for xx in xs]) for y in ycell]); targets[x] = t; heat_line[x] = t.sum() * (FY / n_cells) * (hi - lo) / 100
    Ptot = sum(heat_line.values())
    # branch dp per zone: fin viscous dp scales with (segment velocity x L); die zone at heat-proportional flow
    def fin_dp(flow_per_area_lpm_cm2, L):
        u = flow_per_area_lpm_cm2 * LPM / 1e-4 * L * 1e-3 / (0.5 * 2.0e-3); return DP_FIN * (u * L) / (0.20 * 7.7), u
    # flow allocation on the dilated footprints (as drawn): zone shares and dilated zone areas from the strip integrals
    H_die = sum(np.sum(targets[x][targets[x] >= Q_DIE * 0.5]) * (FY / n_cells) * Lseg[x] * 2 / 100 for x in xs_in)
    H_hbm = Ptot - H_die
    A_die_d = sum(np.sum(targets[x] >= Q_DIE * 0.5) * (FY / n_cells) * Lseg[x] * 2 / 100 for x in xs_in)
    A_hbm_d = sum(np.sum((targets[x] > 0) & (targets[x] < Q_DIE * 0.5)) * (FY / n_cells) * Lseg[x] * 2 / 100 for x in xs_in)
    fpa_die = (H_die / Ptot) * 18 / A_die_d; fpa_hbm = (H_hbm / Ptot) * 18 / A_hbm_d
    dpf_die, u_die = fin_dp(fpa_die, 5.5); dpf_hbm, u_hbm = fin_dp(fpa_hbm, 11.0)
    dp_branch = DP_METER_18 + dpf_die + DP_ROW + DP_MISC; dpm_hbm = dp_branch - dpf_hbm - DP_ROW - DP_MISC
    u_or_hbm = CD * math.sqrt(2 * dpm_hbm * 1e3 / rho)
    out += [f"real heat shares: die {P_die / (P_die + P_hbm) * 100:.1f} %, HBM {P_hbm / (P_die + P_hbm) * 100:.1f} %; flow allocation on the dilated footprints (die +3 mm, HBM +2 mm): die zone {H_die / Ptot * 100:.1f} % ({A_die_d:.1f} cm2), HBM zone {H_hbm / Ptot * 100:.1f} % ({A_hbm_d:.1f} cm2); margin: plenum-end bleeds only, no orifices",
            f"flow per area: die zone {fpa_die:.3f} LPM/cm2 ({fpa_die / (18 / 132):.2f}x field mean), HBM zone {fpa_hbm:.3f} ({fpa_hbm / (18 / 132):.2f}x; architecture 0.3-0.5x)",
            f"fin segment: die u {u_die:.2f} m/s, dp {dpf_die:.2f} kPa (L 5.5); HBM u {u_hbm:.3f} m/s, dp {dpf_hbm:.2f} kPa (L 11)",
            f"branch dp {dp_branch:.2f} kPa (die meter {DP_METER_18:.2f} at 1.54 m/s); HBM meter {dpm_hbm:.2f} kPa -> HBM orifice u {u_or_hbm:.2f} m/s at 18 LPM, {u_or_hbm * 23 / 18:.2f} at 23 LPM"]
    L_steps = np.round(np.arange(0.50, 1.501, 0.05), 2); A_steps = np.array([A_RR(W_IN, L, R_IN) for L in L_steps]); A_min = A_steps.min()
    holes, summ, zone_area = [], [], {"die": 0.0, "hbm": 0.0}
    for li, x in enumerate(xs_in):
        t = targets[x]; Q_line = Qg * heat_line[x] / Ptot; tgt = t / t[t > 0].mean()
        zone = "die" if Lseg[x] < 8 else "hbm"; u_zone = U_MEAN_18 if zone == "die" else u_or_hbm
        dpf = dpf_die if zone == "die" else dpf_hbm; dp0 = dp_branch * 1e3; fv = dpf / dp_branch
        sc = np.where(t > 0, 1 / np.maximum(tgt, 1e-9)**2, 1.0); sc = sc / sc[t > 0].mean()
        for it in range(6):
            r = plenum(Wch[x] * 1e-3, H_PLEN, Q_line, dp0, fv, r2scale=sc, target=tgt, n=n_cells, Lp=FY * 1e-3)
            corr = np.where(t > 0, r / np.maximum(tgt, 1e-9), 1.0); sc = sc * corr**1.6; sc = sc / sc[t > 0].mean()
        a_cell = np.where(t > 0, 1 / np.sqrt(sc), 0.0); a_pos = a_cell.reshape(n_pos, 8).sum(1)
        a_pos = a_pos / a_pos.sum() * (Q_line / u_zone * 1e6)          # mm2 per 2 mm position
        acc = 0.0; line_A = 0.0
        for j in range(n_pos):
            A_need = a_pos[j]
            if A_need <= 0: continue
            if A_need < A_min:                                           # dither the minimum site along the line
                acc += A_need
                if acc < A_min: continue
                acc -= A_min; sites = [(+1 if j % 2 == 0 else -1, L_steps[0], A_min)]
            elif A_need <= A_steps.max():
                si = int(np.argmin(abs(A_steps - A_need))); sites = [(+1 if j % 2 == 0 else -1, L_steps[si], A_steps[si])]
            else:
                si = int(np.argmin(abs(A_steps - A_need / 2))); sites = [(+1, L_steps[si], A_steps[si]), (-1, L_steps[si], A_steps[si])]
            for (side, L, A) in sites:
                holes.append(hole(f"I{li + 1}", x, j + 1, x + side * X_OFF, y_pos[j], W_IN, float(L), "inlet", R_IN, float(A), int(np.argmin(abs(L_steps - L))) + 1,
                                  "+x" if side > 0 else "-x", zone, float(tgt.reshape(n_pos, 8).mean(1)[j]), u_zone)); line_A += A; zone_area[zone] += A
        summ.append((li + 1, x, zone, heat_line[x], Q_line / LPM, line_A, Q_line / (line_A * 1e-6), Q_line / 2 / (Wch[x] * 1e-3 * H_PLEN)))
    out += ["\n| inlet line | x mm | zone | strip heat W (dilated) | flow LPM | open area mm2 | mean orifice u m/s | plenum half-channel u m/s |", "|---|---|---|---|---|---|---|---|"]
    for (i, x, z, hw, ql, al, u, up) in summ: out.append(f"| I{i} | {x:+.1f} | {z} | {hw:.0f} | {ql:.2f} | {al:.1f} | {u:.2f} | {up:.2f} |")
    A_g = sum(h["area_mm2"] for h in holes); u_max = max(h["u_18lpm_m_s"] for h in holes)
    out += [f"inlet orifices {len(holes)}; total open area {A_g:.1f} mm2 -> area-mean u {Qg / (A_g * 1e-6):.2f} m/s; die orifices at 1.54 m/s (meter {DP_METER_18:.2f} kPa, check <= 2.3), max orifice u {u_max:.2f} m/s (HBM zone)",
            f"flow share: die {zone_area['die'] * 1.54 / (zone_area['die'] * 1.54 + zone_area['hbm'] * u_or_hbm) * 100:.1f} % (>= 85 required), HBM {zone_area['hbm'] * u_or_hbm / (zone_area['die'] * 1.54 + zone_area['hbm'] * u_or_hbm) * 100:.1f} %, margin 0 % + bleeds",
            f"at the package's rated 1.2 LPM/kW ({(P_die + P_hbm) / 1000 * 1.2:.1f} LPM) velocities scale x{(P_die + P_hbm) / 1000 * 1.2 / 18:.2f}"]
    flow_in = {x: Qg * heat_line[x] / Ptot for x in xs_in}
    for oi, xo in enumerate(xs_out):
        edge = abs(xo) > 54; neigh = [x for x in xs_in if abs(x - xo) <= 11.01]
        Qo = sum(flow_in[x] for x in neigh) / 2; A_row = Qo / U_ROW * 1e6
        if edge:
            n = 30; h = max(0.50, round(H_RR(A_row / n, W_EDGE, R_EDGE), 2)); w, r = W_EDGE, R_EDGE; sgn = -1 if xo < 0 else 1; xc = xo - sgn * EDGE_WIN / 2; ys = -58.0 + 4.0 * np.arange(n)
        else:
            n = 60; h = min(1.40, max(0.50, round(H_RR(A_row / n, W_OUT, R_OUT), 2))); w, r = W_OUT, R_OUT; xc = xo; ys = y_pos
        A = A_RR(w, h, r); dp = 0.5 * rho * (Qo / (n * A * 1e-6))**2 / CD**2 / 1e3
        for n_, y in enumerate(ys): holes.append(hole(f"O{oi + 1}", xo, n_ + 1, xc, y, w, h, "outlet", r, A, 0, "edge" if edge else "centre", "outlet", 1.0, Qo / (n * A * 1e-6)))
        out.append(f"outlet O{oi + 1} at x {xo:+.1f}: collects {Qo / LPM:.2f} LPM -> {n} holes {w} x {h} -> {dp:.2f} kPa")
    write_csv(os.path.join(HERE, "artwork_prism_g_example.csv"), holes)
    ex = land_extras((124.6, 134.6), ((-58.0, -63.0), (58.0, 63.0)), lines, FY, FX)
    for (cx, cy, w, h) in dies + hbm: ex.append(dict(kind="rr", cx=cx, cy=cy, w=w, h=h, r=0, layer="REF"))
    ok = write_dxf(os.path.join(HERE, "artwork_prism_g_example.dxf"), holes, ex, "PRISM-G zoned artwork EXAMPLE - 4 dies 350 W/cm2 + 16 HBM - DDD-grate - mm")
    out.append(f"PRISM-G CSV: {len(holes)} holes; DXF written: {ok}")
    return dict(lines=lines, inlet_holes=sum(1 for h in holes if h["type"] == "inlet"), total_open_area_mm2=round(A_g, 1), die_orifice_u=U_MEAN_18,
                hbm_orifice_u_18lpm=round(u_or_hbm, 2), max_orifice_u_18lpm=round(u_max, 2), branch_dp_kpa=round(dp_branch, 2), holes_total=len(holes))

if __name__ == "__main__":
    out = []; p_ttv = ttv(out); p_g = prism_g(out)
    json.dump(dict(ttv=p_ttv, prism_g_example=p_g), open(os.path.join(HERE, "grate_artwork_params.json"), "w"), indent=1)
    txt = "\n".join(out); open(os.path.join(HERE, "grate_artwork.out"), "w").write(txt + "\n"); print(txt)
