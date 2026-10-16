#!/usr/bin/env python3
"""
Build a print-quality PDF from a Markdown report: pandoc (GFM -> HTML) + a print
stylesheet + headless Chromium (Playwright) for pagination, headers and page numbers.

usage: python3 build_pdf.py report.md out.pdf [--title "..."] [--subtitle "..."] [--date "..."]
Images referenced relatively in the Markdown resolve relative to the Markdown file.
"""
import argparse, pathlib, subprocess, tempfile, json, os

CSS = r"""
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
html { font-family: "IBM Plex Sans", "DejaVu Sans", "Liberation Sans", Arial, sans-serif; font-size: 10.2pt; line-height: 1.42; color: #15191c; }
body { margin: 0; }
h1 { font-size: 22pt; line-height: 1.15; margin: 0 0 6pt; letter-spacing: -0.01em; }
h2 { font-size: 15pt; margin: 18pt 0 6pt; padding-bottom: 3pt; border-bottom: 1.2pt solid #9c4f27; break-after: avoid; }
h3 { font-size: 12pt; margin: 13pt 0 4pt; break-after: avoid; }
h4 { font-size: 10.5pt; margin: 10pt 0 3pt; break-after: avoid; }
p { margin: 0 0 6pt; orphans: 3; widows: 3; }
ul, ol { margin: 0 0 6pt 0; padding-left: 18pt; }
li { margin-bottom: 2pt; }
table { border-collapse: collapse; width: 100%; font-size: 8.6pt; margin: 6pt 0 10pt; break-inside: auto; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th, td { border-bottom: 0.5pt solid #c9cfd3; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #f1f3f4; font-weight: 600; border-bottom: 0.8pt solid #8f9aa1; }
td:has(> strong) { font-weight: 600; }
code { font-family: "IBM Plex Mono", "DejaVu Sans Mono", Menlo, monospace; font-size: 8.4pt; background: #f3f4f5; padding: 0 2pt; border-radius: 2pt; }
pre { font-family: "DejaVu Sans Mono", Menlo, monospace; font-size: 7.6pt; line-height: 1.25; background: #f6f7f8; border: 0.5pt solid #d7dcdf; padding: 6pt 8pt; overflow: hidden; white-space: pre; break-inside: avoid; }
pre code { background: none; padding: 0; font-size: inherit; }
blockquote { margin: 6pt 0 8pt; padding: 4pt 10pt; border-left: 2.5pt solid #9c4f27; background: #faf5f1; color: #3b3f43; }
img { max-width: 100%; height: auto; display: block; margin: 6pt auto; }
figure { margin: 8pt 0 12pt; break-inside: avoid; }
figcaption { font-size: 8.6pt; color: #48525a; margin-top: 3pt; }
hr { border: 0; border-top: 0.5pt solid #c9cfd3; margin: 12pt 0; }
a { color: #9c4f27; text-decoration: none; }
.cover { height: 250mm; display: flex; flex-direction: column; justify-content: flex-end; break-after: page; }
.cover .kicker { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; letter-spacing: 0.12em; text-transform: uppercase; color: #9c4f27; margin-bottom: 10pt; }
.cover h1 { font-size: 34pt; max-width: 80%; }
.cover .cover-img { max-height: 118mm; width: auto; max-width: 100%; margin: 0 0 auto 0; object-fit: contain; align-self: flex-start; }
.cover .sub { font-size: 14pt; color: #48525a; margin: 8pt 0 26pt; max-width: 80%; }
.cover .meta { font-family: "DejaVu Sans Mono", monospace; font-size: 9pt; color: #48525a; border-top: 1pt solid #8f9aa1; padding-top: 8pt; }
.toc { break-after: page; }
.toc ul { list-style: none; padding-left: 0; }
.toc li { margin: 2pt 0; }
.toc li li { padding-left: 14pt; font-size: 9.4pt; color: #3b3f43; }
.page-break { break-after: page; }
.kv { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 6pt; margin: 8pt 0 12pt; }
.kv div { border: 0.5pt solid #c9cfd3; padding: 6pt 8pt; }
.kv .n { font-size: 17pt; font-weight: 600; }
.kv .k { font-size: 8pt; color: #48525a; }
"""

HEADER_TPL = """<div style="font-family: DejaVu Sans, Arial, sans-serif; font-size:7.5pt; color:#6b757c; width:100%; padding:0 16mm; display:flex; justify-content:space-between;">
<span>{title}</span><span>{subtitle}</span></div>"""
FOOTER_TPL = """<div style="font-family: DejaVu Sans, Arial, sans-serif; font-size:7.5pt; color:#6b757c; width:100%; padding:0 16mm; display:flex; justify-content:space-between;">
<span>{date}</span><span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>"""


def md_to_html(md_path: pathlib.Path) -> str:
    out = subprocess.run(["pandoc", "-f", "gfm-tex_math_dollars", "-t", "html5", "--wrap=none", str(md_path)],
                         check=True, capture_output=True, text=True)
    return out.stdout


import re


def make_toc(body_html: str) -> str:
    """Two-level table of contents from the h2/h3 ids pandoc emits."""
    items = re.findall(r'<h([23]) id="([^"]+)">(.*?)</h\1>', body_html, flags=re.S)
    if not items:
        return ""
    out = ['<div class="toc"><h2>Contents</h2><ul>']
    for lvl, hid, text in items:
        text = re.sub(r"<[^>]+>", "", text)
        if lvl == "2":
            out.append(f'<li><a href="#{hid}">{text}</a></li>')
        else:
            out.append(f'<li><ul><li><a href="#{hid}">{text}</a></li></ul></li>')
    out.append("</ul></div>")
    return "".join(out)


def cover(title: str, subtitle: str, date: str, meta_lines: list[str], image: str = "") -> str:
    meta = "<br>".join(meta_lines)
    img = f'<img class="cover-img" src="{image}" alt="">' if image else ""
    return (f'<div class="cover">{img}<div class="kicker">Design report</div><h1>{title}</h1>'
            f'<div class="sub">{subtitle}</div><div class="meta">{date}<br>{meta}</div></div>')


def build(md_path: str, pdf_path: str, title: str, subtitle: str, date: str, cover_html: str = "", toc: bool = True):
    md_path = pathlib.Path(md_path).resolve()
    body = md_to_html(md_path)
    if toc:
        body = make_toc(body) + body
    html = f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{cover_html}{body}</body></html>"
    tmp = md_path.parent / (md_path.stem + ".print.html")
    tmp.write_text(html)
    js = pathlib.Path(__file__).with_name("_print.js")
    js.write_text(r"""
const { chromium } = require('playwright');
(async () => {
  const [src, out, header, footer] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + src, { waitUntil: 'load' });
  await p.emulateMedia({ media: 'print' });
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true, headerTemplate: header, footerTemplate: footer,
    margin: { top: '18mm', bottom: '20mm', left: '16mm', right: '16mm' } });
  await b.close();
})();
""")
    header = HEADER_TPL.format(title=title, subtitle=subtitle)
    footer = FOOTER_TPL.format(date=date)
    subprocess.run(["node", str(js), str(tmp), str(pathlib.Path(pdf_path).resolve()), header, footer], check=True)
    return pdf_path


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("md"); ap.add_argument("pdf")
    ap.add_argument("--title", default="PRISM-15 Rev A"); ap.add_argument("--subtitle", default="Design report")
    ap.add_argument("--date", default="October 2026")
    ap.add_argument("--meta", default="")
    ap.add_argument("--cover-image", default="")
    a = ap.parse_args()
    cov = cover(a.title, a.subtitle, a.date, [m for m in a.meta.split("|") if m], image=a.cover_image)
    build(a.md, a.pdf, a.title, a.subtitle, a.date, cover_html=cov)
    print("wrote", a.pdf)
