import header_net3 as h3, header_net as hn, numpy as np
# monkeypatch meter strength through a wrapper: re-implement with meter param
import inspect
src = inspect.getsource(h3.run).replace("a_m=1.88e3", "a_m=meter*1e3").replace("out_meter=0.0):", "out_meter=0.0, meter=1.88):")
ns = {}; exec(src, h3.__dict__, ns); run = ns['run']
for lab, kw in (("as drafted geometry, 19 lines, matched edge windows", {}), ("inlet meter 1.3 + outlet orifice 0.6 kPa", dict(meter=1.3, out_meter=0.6)),
                ("inlet meter 1.88 + outlet header x2", dict(A_out_scale=2.0)), ("same + port jet undiffused", dict(A_out_scale=2.0, s_jet=1.0))):
    for lpm in (18, 36):
        r = run(lpm, **kw); print(f"{lab}, {lpm} LPM: line {r[0]:.3f} segment {r[1]:.3f} (min {r[2]:.3f}) ok {r[3]}")
