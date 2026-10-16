from harness import ev
rows=[("R base0.8 L8",dict(base=0.8,L=8.0)),("R base0.6 L8",dict(base=0.6,L=8.0)),("R base0.8 L7",dict(base=0.8,L=7.0)),
      ("R+ g0.13 t0.13 H1.9 L6 b1.0",dict(t=0.13,gap=0.13,H=1.9)),("R+ g0.13 t0.13 H1.9 L6 b0.8",dict(t=0.13,gap=0.13,H=1.9,base=0.8)),
      ("R+ g0.13 t0.13 H1.9 L8 b0.8",dict(t=0.13,gap=0.13,H=1.9,base=0.8,L=8.0)),
      ("R+ g0.12 t0.12 H1.5 L6 b0.8",dict(t=0.12,gap=0.12,H=1.5,base=0.8)),("R+ g0.12 t0.12 H1.8 L6 b0.8",dict(t=0.12,gap=0.12,H=1.8,base=0.8)),
      ("R+ g0.12 t0.12 H2.0 L6 b0.8",dict(t=0.12,gap=0.12,H=2.0,base=0.8)),("R+ g0.12 t0.12 H1.8 L8 b0.8",dict(t=0.12,gap=0.12,H=1.8,base=0.8,L=8.0)),
      ("R g0.14 t0.14 H2.0 L6 b0.8",dict(t=0.14,gap=0.14,H=2.0,base=0.8)),
      ("P L6 b0.8",dict(t=0.10,gap=0.10,H=1.5,L=6.0,base=0.8))]
print("| variant | A | pen | pk-pk | paste avg/max | PCM avg/max | LM avg/max | ch dP kPa |")
print("|---|---|---|---|---|---|---|---|")
for lab,kw in rows:
    for A in (100.0,117.0):
        e=ev(A=A,tim="paste",**kw); f=ev(A=A,tim="PCM25",**kw); g=ev(A=A,tim="LM",**kw)
        print(f"| {lab} | {A:.0f} | {e['pen']:+.2f} | {e['pkpk']:.2f} | {e['avg']:.2f} / {e['max']:.2f} | {f['avg']:.2f} / {f['max']:.2f} | {g['avg']:.2f} / {g['max']:.2f} | {e['dp_ch']:.2f} |",flush=True)
