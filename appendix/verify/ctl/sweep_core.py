from harness import ev
import time
t0=time.time()
rows=[("baseline R6 (0.15/0.15x2.0, L6, base1.0, kerf0.3)",{}),
      ("base 0.8",dict(base=0.8)),("base 0.6",dict(base=0.6)),
      ("L5",dict(L=5.0)),("L8",dict(L=8.0)),("L10",dict(L=10.0)),
      ("H1.5",dict(H=1.5)),("H2.5",dict(H=2.5)),
      ("fin t0.10 gap0.15",dict(t=0.10)),("fin t0.10 gap0.15 H1.5",dict(t=0.10,H=1.5)),
      ("gap0.12 t0.12 H1.8",dict(t=0.12,gap=0.12,H=1.8)),("gap0.12 t0.10 H1.8",dict(t=0.10,gap=0.12,H=1.8)),
      ("gap0.20 t0.15 H2.0",dict(gap=0.20)),("gap0.20 t0.15 H2.5",dict(gap=0.20,H=2.5)),
      ("no kerf",dict(kerf=0.0)),("kerf 0.5",dict(kerf=0.5)),
      ("base0.8 + L8",dict(base=0.8,L=8.0)),("base0.8 + L5",dict(base=0.8,L=5.0)),
      ("P-grade 0.10/0.10x1.5 L4",dict(t=0.10,gap=0.10,H=1.5,L=4.0)),("P-grade L5",dict(t=0.10,gap=0.10,H=1.5,L=5.0)),("P-grade L6",dict(t=0.10,gap=0.10,H=1.5,L=6.0)),
     ]
print("| variant | A | core 2-D | pen | pk-pk | paste avg/max | PCM avg/max | h_eff | ch dP kPa |")
print("|---|---|---|---|---|---|---|---|---|")
for lab,kw in rows:
    for A in (100.0,117.0):
        e=ev(A=A,tim="paste",**kw); f=ev(A=A,tim="PCM25",**kw)
        print(f"| {lab} | {A:.0f} | {e['core']:.2f} | {e['pen']:+.2f} | {e['pkpk']:.2f} | {e['avg']:.2f} / {e['max']:.2f} | {f['avg']:.2f} / {f['max']:.2f} | {e['heff']/1e3:.0f} | {e['dp_ch']:.2f} |",flush=True)
print(f"[{time.time()-t0:.0f}s]")
