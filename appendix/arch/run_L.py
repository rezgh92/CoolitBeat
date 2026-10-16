from cell2d import run
K3=(0.3/0.15)**2/0.5
# flow length 3 mm: per-cell flow 3/4 of the 4 mm cell (same total flow, more cells) -> dTout per cell unchanged, q same
for L,lab in ((3.0,"L3 window 0.8/1.0+kerf"),(4.0,"L4 window 1.0/1.2+kerf"),(5.0,"L5 window 1.0/1.2+kerf")):
    hi,ho=(0.4,0.5) if L==3.0 else (0.5,0.6)
    r=run(hi=hi,ho=ho,ki=0.15,ko=0.15,L=L,Kkerf_mult=K3)
    print(f"{lab}: 2-D {r['case']:.2f} K, 1-D {r['ref']:.2f} K, pk-pk {r['pkpk']:.2f}",flush=True)
