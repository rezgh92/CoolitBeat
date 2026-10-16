from cell2d import run
K3=(0.3/0.15)**2/0.5
rows=[
 ("F1 recessed window 1.0/1.2 + kerf 0.3, H2.0, 128", dict(hi=0.5,ho=0.6,ki=0.15,ko=0.15,Kkerf_mult=K3)),
 ("F2 recessed window 1.0/1.2 + kerf 0.3, H2.5, 128", dict(hi=0.5,ho=0.6,ki=0.15,ko=0.15,H=2.5,Kkerf_mult=K3)),
 ("F3 slit 0.3 at tips + kerf 0.3, H2.5, 128",        dict(hi=0.15,ho=0.30,ki=0.15,ko=0.15,H=2.5,Kkerf_mult=K3)),
 ("F4 window+kerf 0.3, H3.0, 128",                     dict(hi=0.5,ho=0.6,ki=0.15,ko=0.15,H=3.0,Kkerf_mult=K3)),
 ("F5 window+kerf 0.3, H2.5, RF-10 (t0.10), 128",      dict(hi=0.5,ho=0.6,ki=0.15,ko=0.15,H=2.5,t=0.10,Kkerf_mult=K3)),
 ("F6 window+kerf 0.3, H2.5, 350 W/cm2, L4",           dict(hi=0.5,ho=0.6,ki=0.15,ko=0.15,H=2.5,q=3.5e6,dTout=12.9,Kkerf_mult=K3)),
 ("F7 window+kerf 0.3, H2.5, 350 W/cm2, L5",           dict(hi=0.5,ho=0.6,ki=0.15,ko=0.15,H=2.5,L=5.0,q=3.5e6,dTout=12.9,Kkerf_mult=K3)),
 ("F8 window+kerf 0.3, H2.0, 350 W/cm2, L4",           dict(hi=0.5,ho=0.6,ki=0.15,ko=0.15,H=2.0,q=3.5e6,dTout=12.9,Kkerf_mult=K3)),
 ("F9 P-grade gap0.10/t0.10 H1.5 window+kerf 0.3, 128",dict(hi=0.5,ho=0.6,ki=0.15,ko=0.15,H=1.5,t=0.10,gap=0.10,h=19.7e3,Kkerf_mult=(0.3/0.10)**2/0.5)),
 ("F10 P-grade no kerf, slit, 128",                    dict(hi=0.15,ho=0.30,H=1.5,t=0.10,gap=0.10,h=19.7e3)),
]
print("| case | 2-D case avg K | 1-D ref K | 2-D - 1-D K | case pk-pk K | lower-half flow |")
print("|---|---:|---:|---:|---:|---:|")
for lab,kw in rows:
    r=run(**kw)
    print(f"| {lab} | {r['case']:.2f} | {r['ref']:.2f} | {r['pen']:+.2f} | {r['pkpk']:.2f} | {r['frac_low']:.2f} |",flush=True)
