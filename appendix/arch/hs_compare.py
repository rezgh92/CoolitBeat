"""Compare fin-level opening geometries with the two judges' 2-D Hele-Shaw conjugate models.
Model A = judge_hmmc/heleshaw.py (two-equation porous, case-average dT incl. base, vs 1-D ref)
Model B = judge_risk/hele_shaw_cell.py (gap-averaged fluid + 2-D fin, heat ratio 2-D/1-D)
Geometry: half-cell from inlet-opening centre (x=0) to outlet-opening centre (x=L)."""
import sys, io, contextlib
sys.path.insert(0, '../judge_hmmc'); sys.path.insert(0, '../judge_risk')
import heleshaw as A
import hele_shaw_cell as B
cases = [
 # label, half_in, half_out, H, t, gap
 ("PSM slit 0.30/0.60 at fin tips, RF-15", 0.15, 0.30, 2.0, 0.15, 0.15),
 ("PRISM window 1.0/1.2, RF-15 H2.0",      0.50, 0.60, 2.0, 0.15, 0.15),
 ("PRISM window 1.0/1.2, RF-15 H1.5",      0.50, 0.60, 1.5, 0.15, 0.15),
 ("PRISM window 0.8/1.0, RF-15 H2.0",      0.40, 0.50, 2.0, 0.15, 0.15),
 ("PRISM window 1.0/1.2, RF-10 H2.0",      0.50, 0.60, 2.0, 0.10, 0.15),
 ("hmmc-elite 3.3/0.7 (no grate), RF-10",  1.65, 1.65, 2.0, 0.10, 0.15),
]
print("| geometry | A: case avg K | A: 1-D ref K | A: penalty K | A: penalty (z-mixed) K | B: heat ratio 2D/1D | B: lower-half flow |")
print("|---|---:|---:|---:|---:|---:|---:|")
for lab, hi, ho, H, t, g in cases:
    L = 4.0
    pitch = (t + g) * 1e-3
    with contextlib.redirect_stdout(io.StringIO()):
        ca, ra = A.run([(0.0, hi)], [(L - ho, L)], H=H, tb=1.0, d=0.025, pitch=pitch, gap=g*1e-3, label=lab)
        cm, rm = A.run([(0.0, hi)], [(L - ho, L)], H=H, tb=1.0, d=0.025, pitch=pitch, gap=g*1e-3, kfz_mult=1e4, label=lab)
    rb = B.run(H=H*1e-3, L=L*1e-3, b=g*1e-3, t=t*1e-3, a_in=hi*1e-3, a_out=ho*1e-3, d=0.04e-3 if H <= 2.0 else 0.05e-3)
    print(f"| {lab} | {ca:.2f} | {ra:.2f} | {ca-ra:+.2f} | {cm-rm:+.2f} | {rb['heat_ratio']:.3f} | {rb['frac_low']:.2f} |")
