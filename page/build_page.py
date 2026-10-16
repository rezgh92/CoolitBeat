#!/usr/bin/env python3
"""Builds the PRISM manager page (single HTML file) from the architecture numbers."""
import html, json, pathlib

OUT = pathlib.Path(__file__).with_name("prism.html")

# ---------------------------------------------------------------- data
TERMS = ["Coolant rise (caloric)", "Thermal interface", "Copper base", "Convection in fins", "2-D penalty"]
BARS = [
    # label, sublabel, terms (K), total shown
    ("CoolIT 15 kW", "measured, paste", [6.3, 9.0, 6.6, 12.6, 0.0], 34.4),
    ("PRISM Rev A", "same paste", [7.5, 9.0, 2.6, 10.9, 0.9], 31.0),
    ("PRISM Rev A", "PCM pad (Tier 1)", [7.5, 7.1, 2.6, 10.9, 0.9], 29.0),
    ("PRISM Rev A", "liquid metal (Tier 2)", [7.5, 1.9, 2.6, 10.9, 0.9], 23.9),
]


def chart_svg():
    W, left, right_pad = 760, 196, 70
    plot_w = W - left - right_pad
    xmax = 40.0
    sx = plot_w / xmax
    row_h, bar_h, top = 46, 22, 30
    H = top + row_h * len(BARS) + 34
    o = [f'<svg class="chart" viewBox="0 0 {W} {H}" role="img" aria-label="Stacked bars of the case-to-inlet temperature budget at 15 kW, 18 LPM, 45 C inlet: CoolIT 34.4 K, PRISM with the same paste 31.0 K, with a PCM pad 29.0 K, with liquid metal 23.9 K. PRISM cuts the copper base and convection terms and pays slightly more in coolant rise.">']
    # grid + ticks
    for t in range(0, 41, 10):
        x = left + t * sx
        o.append(f'<line x1="{x:.1f}" y1="{top-8}" x2="{x:.1f}" y2="{H-30}" class="grid"/>')
        o.append(f'<text x="{x:.1f}" y="{H-12}" text-anchor="middle" class="tick">{t} K</text>')
    for i, (lab, sub, terms, total) in enumerate(BARS):
        y = top + i * row_h
        cy = y + bar_h / 2
        o.append(f'<text x="{left-12}" y="{cy-2:.1f}" text-anchor="end" class="rowlab">{html.escape(lab)}</text>')
        o.append(f'<text x="{left-12}" y="{cy+13:.1f}" text-anchor="end" class="rowsub">{html.escape(sub)}</text>')
        x = left
        nz = [k for k, v in enumerate(terms) if v > 0]
        last = nz[-1]
        for k, v in enumerate(terms):
            if v <= 0:
                continue
            w = v * sx
            gap = 2 if k != last else 0
            ww = max(w - gap, 1)
            tip = f"{TERMS[k]}: {v:.1f} K"
            attrs = (f'class="seg s{k+1}" tabindex="0" data-tip="{html.escape(lab + " (" + sub + ") | " + tip)}"')
            if k == last:
                r = 4
                d = (f"M{x:.1f},{y} H{x+ww-r:.1f} Q{x+ww:.1f},{y} {x+ww:.1f},{y+r} "
                     f"V{y+bar_h-r} Q{x+ww:.1f},{y+bar_h} {x+ww-r:.1f},{y+bar_h} H{x:.1f} Z")
                o.append(f'<path d="{d}" {attrs}><title>{html.escape(tip)}</title></path>')
            else:
                o.append(f'<rect x="{x:.1f}" y="{y}" width="{ww:.1f}" height="{bar_h}" {attrs}><title>{html.escape(tip)}</title></rect>')
            x += w
        o.append(f'<text x="{x+8:.1f}" y="{cy+5:.1f}" class="total">{total:.1f} K</text>')
    o.append("</svg>")
    return "\n".join(o)


def flow_svg():
    W, H = 820, 330
    x0, mm = 32, 7.0            # 108 mm field -> 756 px
    L = 108 * mm
    o = [f'<svg class="diagram" viewBox="0 0 {W} {H}" role="img" aria-label="Side by side flow paths. In CoolIT Split-Flow, coolant enters at the centre and runs 54 mm to each edge, warming 12.7 K, so the outlet edges run hottest. In PRISM, 7 metered inlet lines and 8 outlet lines split the same field into 14 cells of 7.7 mm, so every cell starts at inlet temperature.">']
    o.append('''<defs>
  <linearGradient id="g-c2h" x1="0" x2="1" y1="0" y2="0"><stop offset="0" style="stop-color:var(--cold)"/><stop offset="1" style="stop-color:var(--hot)"/></linearGradient>
  <linearGradient id="g-h2c" x1="0" x2="1" y1="0" y2="0"><stop offset="0" style="stop-color:var(--hot)"/><stop offset="1" style="stop-color:var(--cold)"/></linearGradient>
  <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker>
  <marker id="ah-c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--cold)"/></marker>
  <marker id="ah-h" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--hot)"/></marker>
</defs>''')
    # ---- panel A
    yA, h = 74, 28
    o.append(f'<text x="{x0}" y="22" class="ptitle">CoolIT Split-Flow</text>')
    o.append(f'<text x="{x0}" y="40" class="pnote">one inlet slot at the centre, outlets at both edges</text>')
    mid = x0 + L / 2
    o.append(f'<rect x="{x0}" y="{yA}" width="{L/2:.1f}" height="{h}" fill="url(#g-h2c)" class="field"/>')
    o.append(f'<rect x="{mid:.1f}" y="{yA}" width="{L/2:.1f}" height="{h}" fill="url(#g-c2h)" class="field"/>')
    o.append(f'<line x1="{mid:.1f}" y1="48" x2="{mid:.1f}" y2="{yA-3}" class="arr-c" marker-end="url(#ah-c)"/>')
    o.append(f'<text x="{mid+8:.1f}" y="60" class="lab">inlet, 45 °C</text>')
    for xe, anchor, dx in ((x0, "start", 0), (x0 + L, "end", 0)):
        o.append(f'<line x1="{xe:.1f}" y1="{yA-3}" x2="{xe:.1f}" y2="50" class="arr-h" marker-end="url(#ah-h)"/>')
    o.append(f'<text x="{x0+8}" y="60" class="lab">outlet, 57.7 °C</text>')
    o.append(f'<text x="{x0+L-8:.1f}" y="60" text-anchor="end" class="lab">outlet, 57.7 °C</text>')
    yy = yA + h / 2
    o.append(f'<line x1="{mid-14:.1f}" y1="{yy}" x2="{x0+150:.1f}" y2="{yy}" class="arr-w" marker-end="url(#ah)"/>')
    o.append(f'<line x1="{mid+14:.1f}" y1="{yy}" x2="{x0+L-150:.1f}" y2="{yy}" class="arr-w" marker-end="url(#ah)"/>')
    o.append(f'<text x="{(x0+mid)/2:.1f}" y="{yA+h+18}" text-anchor="middle" class="lab">54 mm path, coolant +12.7 K</text>')
    o.append(f'<text x="{(mid+x0+L)/2:.1f}" y="{yA+h+18}" text-anchor="middle" class="lab">54 mm path, coolant +12.7 K</text>')
    o.append(f'<text x="{x0}" y="{yA+h+38}" class="em">The edge cells see the warmest coolant: measured hot spot 9.8 K above the average.</text>')
    # ---- panel B
    yB = 230
    o.append(f'<text x="{x0}" y="170" class="ptitle">PRISM Rev A</text>')
    o.append(f'<text x="{x0}" y="188" class="pnote">7 metered inlet lines and 8 outlet lines over the same 108 mm fin field</text>')
    seg = L / 14
    for k in range(14):
        xa = x0 + k * seg
        grad = "g-h2c" if k % 2 == 0 else "g-c2h"   # inlet lines are at odd indices
        o.append(f'<rect x="{xa:.1f}" y="{yB}" width="{seg:.1f}" height="{h}" fill="url(#{grad})" class="field"/>')
    for i in range(15):
        xl = x0 + i * seg
        if i % 2 == 1:
            o.append(f'<line x1="{xl:.1f}" y1="{yB-24}" x2="{xl:.1f}" y2="{yB-3}" class="arr-c thin" marker-end="url(#ah-c)"/>')
        else:
            o.append(f'<line x1="{xl:.1f}" y1="{yB-3}" x2="{xl:.1f}" y2="{yB-24}" class="arr-h thin" marker-end="url(#ah-h)"/>')
    # dimension for one cell
    xa, xb = x0 + 7 * seg, x0 + 8 * seg
    o.append(f'<line x1="{xa:.1f}" y1="{yB+h+8}" x2="{xb:.1f}" y2="{yB+h+8}" class="dim" marker-start="url(#ah)" marker-end="url(#ah)"/>')
    o.append(f'<text x="{(xa+xb)/2:.1f}" y="{yB+h+24}" text-anchor="middle" class="lab">7.7 mm cell</text>')
    o.append(f'<text x="{x0}" y="{yB+h+46}" class="em">Every cell starts at inlet temperature, so there is no hot edge: hot spot about 1.5 K from flow, the rest from the interface.</text>')
    o.append("</svg>")
    return "\n".join(o)


def stack_svg():
    W, H = 820, 330
    s = 12.0                       # px per mm (vertical, to scale)
    xL, xR = 150, 560
    base_y = 292
    o = [f'<svg class="diagram" viewBox="0 0 {W} {H}" role="img" aria-label="Cross-section of PRISM-15 Rev A drawn to vertical scale: 0.8 mm base, 2.0 mm skived fins kerfed at every line, 1.7 mm metered grate, 5.8 mm folded plenum with alternating inlet and outlet channels, 1.5 mm separator, and a drawn arched cap with the headers and two 20 mm ports, 20.8 mm overall.">']
    layers = [  # name, z0, z1, style, note
        ("Base, fly-cut after braze", 0.0, 0.8, "cu", "0.8 mm, ≤ 20 µm flat"),
        ("Skived fins, kerfed", 0.8, 2.8, "fins", "0.15 / 0.15 / 2.0 mm, tips brazed"),
        ("Metered grate", 2.8, 4.5, "cu2", "graded 0.5 × 1.0 mm orifices"),
        ("Folded plenum", 4.5, 10.3, "plenum", "7 inlet, 8 outlet channels"),
        ("Separator", 10.3, 11.8, "cu2", "windows to each channel"),
        ("Drawn, arched cap", 11.8, 20.8, "cap", "headers: 2 inlet, 4 outlet arches"),
    ]
    for name, z0, z1, st, note in layers:
        y0, y1 = base_y - z1 * s, base_y - z0 * s
        hh = y1 - y0
        if st == "fins":
            o.append(f'<rect x="{xL}" y="{y0:.1f}" width="{xR-xL}" height="{hh:.1f}" class="l-gap"/>')
            n = 82
            pitch = (xR - xL) / n
            for i in range(n):
                xi = xL + i * pitch
                if i % 6 == 3:
                    continue      # kerf gap
                o.append(f'<rect x="{xi:.1f}" y="{y0:.1f}" width="{pitch*0.5:.2f}" height="{hh:.1f}" class="l-cu"/>')
        elif st == "plenum":
            o.append(f'<rect x="{xL}" y="{y0:.1f}" width="{xR-xL}" height="{hh:.1f}" class="l-cu2"/>')
            nch = 15
            cw = (xR - xL) / nch
            for i in range(nch):
                cls = "l-in" if i % 2 == 1 else "l-out"
                o.append(f'<rect x="{xL+i*cw+2:.1f}" y="{y0+3:.1f}" width="{cw-4:.1f}" height="{hh-6:.1f}" class="{cls}"/>')
        elif st == "cap":
            o.append(f'<path d="M{xL},{y1:.1f} V{y0+14:.1f} Q{xL},{y0:.1f} {xL+14},{y0:.1f} H{xR-14} Q{xR},{y0:.1f} {xR},{y0+14:.1f} V{y1:.1f} Z" class="l-cu2"/>')
            cx = (xL + xR) / 2
            # header arches
            for j, (dx, cls) in enumerate(((-150, "l-in"), (-110, "l-in"), (10, "l-out"), (50, "l-out"), (90, "l-out"), (130, "l-out"))):
                ax = cx + dx
                o.append(f'<path d="M{ax-17:.1f},{y1-2:.1f} V{y1-48:.1f} Q{ax:.1f},{y1-80:.1f} {ax+17:.1f},{y1-48:.1f} V{y1-2:.1f} Z" class="{cls}"/>')
        else:
            o.append(f'<rect x="{xL}" y="{y0:.1f}" width="{xR-xL}" height="{hh:.1f}" class="l-{st}"/>')
        ym = (y0 + y1) / 2
        o.append(f'<line x1="{xR+6}" y1="{ym:.1f}" x2="{xR+30}" y2="{ym:.1f}" class="lead"/>')
        o.append(f'<text x="{xR+36}" y="{ym+1:.1f}" class="lab strong">{html.escape(name)}</text>')
        o.append(f'<text x="{xR+36}" y="{ym+15:.1f}" class="lab dim-t">{html.escape(note)}</text>')
        o.append(f'<text x="{xL-10}" y="{y0+4:.1f}" text-anchor="end" class="tick">{z1:.1f}</text>')
    o.append(f'<text x="{xL-10}" y="{base_y+4}" text-anchor="end" class="tick">0.0</text>')
    o.append(f'<text x="{xL-48}" y="{base_y-130}" text-anchor="middle" class="tick" transform="rotate(-90 {xL-48} {base_y-130})">height, mm (to scale)</text>')
    # ports
    top_y = base_y - 20.8 * s
    for px, cls, lab in ((xL + 110, "arr-c", "in, 20 mm"), (xR - 110, "arr-h", "out, 20 mm")):
        if cls == "arr-c":
            o.append(f'<line x1="{px}" y1="{top_y-26:.1f}" x2="{px}" y2="{top_y-2:.1f}" class="{cls}" marker-end="url(#ah2-c)"/>')
        else:
            o.append(f'<line x1="{px}" y1="{top_y-2:.1f}" x2="{px}" y2="{top_y-26:.1f}" class="{cls}" marker-end="url(#ah2-h)"/>')
        o.append(f'<text x="{px+8}" y="{top_y-14:.1f}" class="lab">{lab}</text>')
    o.append(f'<line x1="{xL}" y1="{base_y+10}" x2="{xR}" y2="{base_y+10}" class="tim"/>')
    o.append(f'<text x="{(xL+xR)/2:.0f}" y="{base_y+28}" text-anchor="middle" class="lab">thermal interface to the package lid, bare die or test vehicle</text>')
    o.insert(1, '''<defs>
  <marker id="ah2-c" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--cold)"/></marker>
  <marker id="ah2-h" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" style="fill:var(--hot)"/></marker>
</defs>''')
    o.append("</svg>")
    return "\n".join(o)


def chip(v):
    m = {"win": "Win", "par": "Parity", "loss": "Loss", "con": "Concession", "prob": "Probable win"}
    return f'<span class="chip {v}">{m[v]}</span>'


SCORE = [
    ("Average case-to-inlet ΔT, same paste", "34.4 K", "31.0 K (−10 %)", "35.3 K", "23.9 K", "win"),
    ("Maximum case-to-inlet ΔT, same paste", "44.2 K", "38.7 K (−12 %)", "43.6 K", "28.8 K", "win"),
    ("Average / maximum on a PCM pad", "32.5 / 40.3 K (est.)", "29.0 / 34.8 K", "32.3 / 38.5 K", "–", "win"),
    ("Maximum minus average (uniformity), paste", "9.8 K", "7.8 K", "9.5 K", "4.8 K", "win"),
    ("Plate pressure drop at 18 LPM", "undisclosed (~22 kPa reconstructed)", "7.6 kPa", "≤ 10 kPa", "7.6 kPa", "win"),
    ("Load at 85 °C case, 1.2 LPM/kW (paste / PCM)", "12.9 / 14.8 kW", "15.7 / 18.5 kW", "13.8 / 15.6 kW", "19.5 kW rated", "win"),
    ("Inlet allowed at 15 kW (paste / PCM)", "40.8 / 44.7 °C", "46.3 / 50.2 °C", "41.4 / 46.5 °C", "52.3 °C", "win"),
    ("Height at the header", "est. 22–28 mm", "20.8 mm", "22 mm", "18.8 mm", "prob"),
    ("Mass", "est. 1.2–1.6 kg", "1.24 kg", "1.3 kg", "1.12 kg", "prob"),
    ("Cost per kW of capacity (paste / PCM)", "US$9.8 / 8.5", "US$10.5 / 8.9", "–", "US$9.2 / 7.8", "par"),
    ("Factory cost per plate, 100k/yr", "~US$126", "US$165 (+31 %)", "US$175", "US$144", "loss"),
    ("Average if CoolIT's heaters were 100 cm², paste", "34.4 K", "34.7 K", "39.8 K", "26.5 K", "par"),
    ("Average at very low flow (≤ 0.5 LPM/kW)", "–", "lost at 0.25, parity at 0.5", "–", "–", "loss"),
    ("CoolIT's 4 kW single-die point", "< 0.009 °C/W", "0.0095 (PCM)", "–", "0.0076 (LM)", "loss"),
    ("Fouling life at equal filtration", "~15 y (0.2 mm gap)", "~7 y; ~12 y with supplied filter", "–", "–", "loss"),
    ("Drop-in without extra parts", "yes", "ships with a tray filter", "–", "–", "con"),
    ("Field record", "years", "none yet", "–", "–", "loss"),
]


def score_table():
    rows = []
    for m, c, n, p90, st, v in SCORE:
        rows.append(f"<tr><th scope=\"row\">{m}</th><td>{c}</td><td class=\"num strong\">{n}</td><td class=\"num\">{p90}</td><td class=\"num\">{st}</td><td>{chip(v)}</td></tr>")
    return "\n".join(rows)


def budget_table():
    head = "".join(f"<th scope=\"col\">{t}</th>" for t in TERMS)
    rows = []
    for lab, sub, terms, total in BARS:
        cells = "".join(f'<td class="num">{v:.1f}</td>' for v in terms)
        rows.append(f'<tr><th scope="row">{lab}, {sub}</th>{cells}<td class="num strong">{total:.1f}</td></tr>')
    return f'<table class="tbl"><thead><tr><th scope="col">Build</th>{head}<th scope="col">Average ΔT</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'


page = (pathlib.Path(__file__).with_name("template.html").read_text()
        .replace("{{FLOW_SVG}}", flow_svg())
        .replace("{{CHART_SVG}}", chart_svg())
        .replace("{{BUDGET_TABLE}}", budget_table())
        .replace("{{STACK_SVG}}", stack_svg())
        .replace("{{SCORE_ROWS}}", score_table()))
OUT.write_text(page)
print("wrote", OUT, len(page), "bytes")
