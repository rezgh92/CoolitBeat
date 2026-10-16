from cell2d import run
cases=[
 ("A0 PSM slit 0.30/0.60, no kerf, H2.0",            dict(hi=0.15,ho=0.30)),
 ("A1 slit 0.30 + kerf 0.6 in / 0.6 out, H2.0",      dict(hi=0.15,ho=0.30,ki=0.30,ko=0.30)),
 ("A2 slit 0.30 + kerf 0.8 / 0.8, H2.0",             dict(hi=0.15,ho=0.40,ki=0.40,ko=0.40)),
 ("A3 slit 0.30 + kerf 0.5 / 0.5, H2.0",             dict(hi=0.15,ho=0.25,ki=0.25,ko=0.25)),
 ("A4 kerf 0.6/0.6, H2.5",                           dict(hi=0.15,ho=0.30,ki=0.30,ko=0.30,H=2.5)),
 ("A5 kerf 0.6/0.6, H1.5",                           dict(hi=0.15,ho=0.30,ki=0.30,ko=0.30,H=1.5)),
 ("A6 kerf 0.6/0.6, z-mixed check",                  dict(hi=0.15,ho=0.30,ki=0.30,ko=0.30,kfz_mult=1e4)),
 ("A7 kerf 0.6/0.6, floor h halved",                 dict(hi=0.15,ho=0.30,ki=0.30,ko=0.30,h_floor_in=7.5e3,h_floor_out=4e3)),
 ("A8 inlet kerf only 0.6, no outlet kerf",          dict(hi=0.15,ho=0.30,ki=0.30,ko=0.0)),
 ("A9 RF-10 (t0.10) kerf 0.6/0.6, H2.0",             dict(hi=0.15,ho=0.30,ki=0.30,ko=0.30,t=0.10)),
 ("A10 no kerf, H1.5",                               dict(hi=0.15,ho=0.30,H=1.5)),
]
print("| case | case avg K | 1-D ref K | 2-D minus 1-D K | case pk-pk K | lower-half flow |")
print("|---|---:|---:|---:|---:|---:|")
for lab,kw in cases:
    r=run(**kw)
    print(f"| {lab} | {r['case']:.2f} | {r['ref']:.2f} | {r['pen']:+.2f} | {r['pkpk']:.2f} | {r['frac_low']:.2f} |",flush=True)
# die zone 350 W/cm2 (10 mm pitch => 5 mm half-cell), 1.0 mm base
for lab,kw in (("D0 die zone no kerf, 350 W/cm2, L5",dict(hi=0.15,ho=0.30,L=5.0,q=3.5e6,dTout=12.9)),
               ("D1 die zone kerf 0.6/0.6, 350 W/cm2, L5",dict(hi=0.15,ho=0.30,ki=0.3,ko=0.3,L=5.0,q=3.5e6,dTout=12.9)),
               ("D2 die zone kerf 0.6/0.6, 350 W/cm2, L4",dict(hi=0.15,ho=0.30,ki=0.3,ko=0.3,L=4.0,q=3.5e6,dTout=12.9))):
    r=run(**kw)
    print(f"| {lab} | {r['case']:.2f} | {r['ref']:.2f} | {r['pen']:+.2f} | {r['pkpk']:.2f} | {r['frac_low']:.2f} |",flush=True)
