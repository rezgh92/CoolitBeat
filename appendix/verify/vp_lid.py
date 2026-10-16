"""GPU-class uniform lid (2.3 kW / 60 cm2, 1.0 LPM/kW): does a 3 mm Cu lid (case = lid top) erase the 12 mm-cell
average advantage? Compare PRISM L=4/12 and CoolIT-like long channel, TTV-style (no lid) vs lidded."""
import sys, numpy as np
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model')))
import coldplate_model as cm
from vp_cell import solve
Q, A, lk = 2300.0, 60.0, 1.0
q = Q/(A*1e-4); c = cm.coolit_like(A).evaluate(Q, lk); dTout = c['dT_out']; half = np.sqrt(A)*10/2
Rtim = 0.07e-4; tim_t = 0.05; kz_tim = tim_t*1e-3/Rtim; tlid = 3.0
def case_lid_top(r, nlid_rows):
    Tb = r['Tb']; # rows 0.. ; lid occupies first nlid_rows rows; lid top = interface between row nlid-1 and TIM row
    zr = r['zrows']; dz1, k1 = zr[nlid_rows-1][0], zr[nlid_rows-1][2]; dz2, k2 = zr[nlid_rows][0], zr[nlid_rows][2]
    T1, T2 = Tb[nlid_rows-1], Tb[nlid_rows]
    w1 = (dz2/2/k2)/((dz1/2/k1)+(dz2/2/k2))
    return T1*w1 + T2*(1-w1)   # interface temperature
res = {}
for lab, kw, hh in (("CoolIT-like", dict(L=half, H=4.0, t=0.2, g=0.2, win_in=2.5, win_out=0.0, kerf_in=0.0, kerf_out=0.0, end_outlet=True, dx=0.1, dz=0.1), c['h']),
                    ("PRISM L4", dict(L=4.0, dx=0.025), None), ("PRISM L12", dict(L=12.0, dx=0.05, dz=0.04), None)):
    if hh is None:
        Lc = kw['L']; ns = max(1, int(round(np.sqrt(A)*10/(2*Lc))))
        p = cm.ColdPlate(name="P", footprint_cm2=A, fin_t_mm=0.15, gap_mm=0.15, fin_h_mm=2.0, flow_len_mm=Lc, base_mm=1.0, tim="paste 0.07", isothermal_cell=True, hotspot_flow_K=1.5, n_parallel_paths=2*ns, slot_w_mm=3.0)
        hh = p.evaluate(Q, lk)['h']; base = [(1.0, 390, 390)]
    else:
        base = [(2.0, 390, 390)]
    r0 = solve(q=q, dTout=dTout, h=hh, layers=base, **kw)
    avg0 = r0['case'] + q*Rtim; max0 = r0['cmax'] + q*Rtim
    lay = [(tlid, 390, 390), (tim_t, 0.5, kz_tim)] + base
    r1 = solve(q=q, dTout=dTout, h=hh, layers=lay, **kw)
    nl = sum(1 for z in r1['zrows'] if z[1] == 390 and r1['zrows'].index(z) < 1000)  # placeholder
    nlid = int(round(tlid/(kw.get('dz') or kw['dx'])))
    top = case_lid_top(r1, nlid)
    res[lab] = (avg0, max0, top.mean(), top.max())
    print(f"{lab}: no lid avg {avg0:.2f} max {max0:.2f} (pk-pk {r0['pkpk']:.2f}) | 3 mm lid, case=lid top: avg {top.mean():.2f} max {top.max():.2f} (pk-pk {top.max()-top.min():.2f}); lid shifts avg by {top.mean()-avg0:+.2f} K", flush=True)
c0 = res["CoolIT-like"]
for k in ("PRISM L4", "PRISM L12"):
    v = res[k]
    print(f"{k} minus CoolIT-like (same physics, both 2-D): no lid avg {v[0]-c0[0]:+.2f} / max {v[1]-c0[1]:+.2f}; lidded avg {v[2]-c0[2]:+.2f} / max {v[3]-c0[3]:+.2f}")
