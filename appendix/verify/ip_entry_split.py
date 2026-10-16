"""Independent IP-lane check (not a re-run of cell2d.py).
Question: in PRISM's half-cell, how much inlet flow enters a fin segment through its END face
(from the 0.3 mm kerf) versus through its TOP (fin tips exposed under the 1.2 mm floor-grate window,
i.e. through an opening in a plate positioned over the channel between its ends)?
Model: 2-D (x along channel, z up) Darcy/Hele-Shaw. Fin gaps g: K = g^2/12 * porosity (g/(g+t)).
Kerf (open, width w): K = w^2/12 (fully open). Unit pressure at inlet window, 0 at outlet window.
Geometry from ARCHITECTURE-draft.md 2.2/3.2: L(inlet-centre to outlet-centre)=6 mm, H=2.0 mm fins,
window 1.2 mm (half 0.6), kerf 0.3 mm (half 0.15), g=t=0.15 mm. Also a no-kerf case and a 'dam' case."""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla

def solve(L=6.0, H=2.0, win=0.6, kerf=0.15, g=0.15, t=0.15, d=0.0125, dam=False):
    nx, nz = int(round(L/d)), int(round(H/d))
    xs = (np.arange(nx)+0.5)*d
    Kfin = g**2/12*(g/(g+t))
    Kk = (2*kerf)**2/12 if kerf > 0 else Kfin
    isk = np.array([(x < kerf) or (x > L-kerf) for x in xs])
    K = np.where(isk, Kk, Kfin)
    if dam:  # solid dam replaces inlet kerf: fins continuous, but x<kerf column impermeable below window
        K = np.where(xs < kerf, 1e-12, Kfin); K = np.where(xs > L-kerf, Kk, K)
    top = np.full(nx, np.nan); top[xs < win] = 1.0; top[xs > L-win] = 0.0
    N = nx*nz; idx = lambda i, k: k*nx+i
    rows, cols, vals = [], [], []; b = np.zeros(N); diag = np.zeros(N)
    for k in range(nz):
        for i in range(nx):
            p = idx(i, k)
            for di, dk in ((1,0),(-1,0),(0,1),(0,-1)):
                ii, kk = i+di, k+dk
                if 0 <= ii < nx and 0 <= kk < nz:
                    c = 2*K[i]*K[ii]/(K[i]+K[ii]); rows.append(p); cols.append(idx(ii,kk)); vals.append(-c); diag[p] += c
                elif kk == nz and not np.isnan(top[i]):
                    c = 2*K[i]; diag[p] += c; b[p] += c*top[i]
    A = sp.csr_matrix((vals+list(diag), (rows+list(range(N)), cols+list(range(N)))), shape=(N, N))
    P = spla.spsolve(A, b).reshape(nz, nx)
    qtop = np.array([2*K[i]*(top[i]-P[-1,i]) if not np.isnan(top[i]) else 0.0 for i in range(nx)])
    Qin = qtop[qtop > 0].sum()
    q_kerf_top = qtop[(qtop > 0) & isk].sum() if not dam else 0.0
    q_fin_top = qtop[(qtop > 0) & ~isk].sum() if not dam else qtop[(qtop>0)].sum()
    # flux across the kerf/fin interface (x = kerf) = flow entering the segment through its end face
    i0 = int(round(kerf/d))
    Kf = 2*K[i0-1]*K[i0]/(K[i0-1]+K[i0])
    q_end = (-(P[:, i0]-P[:, i0-1])*Kf).sum()
    return dict(Qin=Qin, end_face=q_end/Qin, top_under_window=(Qin-q_end)/Qin if not dam else 1-q_end/Qin,
                kerf_top_share=q_kerf_top/Qin)

for lab, kw in (("PRISM-15 window 1.2 + kerf 0.3", {}),
                ("no kerf (R1 fallback)", dict(kerf=0.0)),
                ("window narrowed to kerf (0.3)", dict(win=0.15)),
                ("window 1.2, kerf 0.6", dict(kerf=0.3))):
    if kw.get("kerf", 0.15) == 0.0:
        r = solve(kerf=0.0125, **{k: v for k, v in kw.items() if k != "kerf"})  # 1-cell 'kerf' = plain fins
    else:
        r = solve(**kw)
    print(f"{lab:34s}  end-face share {r['end_face']:.2f}   via fin tops under window {r['top_under_window']:.2f}")

# geometry facts used in the report
win, kerf, Lseg = 1.2, 0.3, 6.0-0.3
over = (win-kerf)/2
print(f"window width over fin tops each side: {over:.2f} mm = {over/Lseg*100:.1f} % of a {Lseg:.1f} mm segment, measured from the kerf face")
print(f"window area over fin tops / total window area: {(win-kerf)/win:.2f}")
print(f"kerf thermal value (draft 3.2 table): 0.6 K of 22.83 K = {0.6/22.83*100:.1f} % of the cell dT")
# term arithmetic
from datetime import date, timedelta
print("2008 family statutory end:", date(2028,8,11), "; '906 Google est. 2028-09-09 => PTA", (date(2028,9,9)-date(2028,8,11)).days, "days")
print("'330 max B-delay PTA bound (draft gap report): 1034 d ->", date(2028,8,11)+timedelta(days=1034))
print("2012 CIP ('691 app 13/401,618 filed 2012-02-21) statutory end:", date(2032,2,21))
print("TW I606224 (TW101110072, filed ~Mar 2012) 20-y end ~", date(2032,3,15), "(filing day unverified)")
print("Microfabrica 12,255,123 filed 2022-03-18, provisional 2021-03-18 -> statutory end", date(2042,3,18))
print("Toyota 11,428,478 priority 2019-12-16, non-prov ~2020 -> ~2040; Intel 12,133,357 filed 2020-12-16 -> ", date(2040,12,16))
