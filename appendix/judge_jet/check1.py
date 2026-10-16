import sys, math
sys.path.insert(0, 'docs/cooling/appendix/design/jet')
import jet_hybrid_model as J
from coldplate_model import K_CU, PG25, TIM
rho, mu, cp, k, nu = J.rho, J.mu, J.cp, J.k, J.nu
print("rho mu cp k nu Pr", rho, mu, cp, k, nu, J.Pr)

def fin_G(hprof, H, t, ks=K_CU, n=400):
    """1-D fin, h(y) piecewise; return heat per unit root dT per unit fin length per side-pair: q/(dT) [W/m/K per m of fin length]
    Solve d2T/dy2 = 2h(y)/(k t) T, T(0)=1, adiabatic tip. returns k t dT/dy at root (per unit length in x)."""
    dy = H/n
    # shooting with linear ODE: integrate two solutions
    import numpy as np
    y = np.linspace(0,H,n+1)
    hh = np.array([hprof(yy) for yy in y])
    # finite difference tridiagonal
    N=n+1
    A=np.zeros((N,N)); b=np.zeros(N)
    A[0,0]=1; b[0]=1
    for i in range(1,N-1):
        A[i,i-1]=1/dy**2; A[i,i+1]=1/dy**2; A[i,i]=-2/dy**2-2*hh[i]/(ks*t)
    A[N-1,N-2]=2/dy**2; A[N-1,N-1]=-2/dy**2-2*hh[N-1]/(ks*t)
    T=np.linalg.solve(A,b)
    # heat = integral 2 h T dy (both faces)
    Q = np.trapezoid(2*hh*T, y)
    return Q

def cell_corrected(core, j, delta_turn=0.5e-3, col_mult=1.0, verbose=False):
    c = core.cell(j)
    b,t,H,w_n,P_r,w_r = core.b, core.t, core.H, core.w_n, core.P_r, core.w_r
    p=b+t; Lc=P_r/2
    # region widths in x (per half cell)
    x_col = col_mult*w_n/2
    x_turn = c['x1'] - w_n/2
    x_ch = Lc - x_col - x_turn
    hdesc_col = J.descent_h(b,H,c['Vj'])   # column at full jet velocity
    hdesc = c['h_desc']
    hch = c['h_ch']
    Gcol = fin_G(lambda y: hdesc_col, H, t)
    Gturn = fin_G(lambda y: hdesc if y < delta_turn else hch, H, t)
    Gch = fin_G(lambda y: hch, H, t)
    Gfin = (x_col*Gcol + x_turn*Gturn + x_ch*Gch)/Lc
    # floor: keep model's weighting (stagnation over x1)
    h_base = c['h_base']
    h_eff_corr = (Gfin + h_base*b)/p
    # model as written: uniform h_fin with eta
    Gmodel = fin_G(lambda y: c['h_fin'], H, t)
    h_eff_model_check = (Gmodel + h_base*b)/p
    # ref
    Gref = fin_G(lambda y: J.channel_h(b,H,c['u_ch'],Lc)[0], H, t)
    href = J.channel_h(b,H,c['u_ch'],Lc)[0]
    h_eff_ref = (Gref + href*b)/p
    # ref with floor stagnation-free but same; also ref w/o "restart" -> same
    # alternative: no floor enhancement credit beyond column width
    h_base_strict = ((x_col)/Lc)*c['h_st'] + (1-x_col/Lc)*hch
    h_eff_strict = (Gfin + h_base_strict*b)/p
    if verbose:
        print(f"  {core.name}: Vj {c['Vj']:.2f} col h {hdesc_col/1e3:.1f} turn h {hdesc/1e3:.1f} ch h {hch/1e3:.1f}; x_col {x_col*1e3:.2f} x_turn {x_turn*1e3:.2f} x_ch {x_ch*1e3:.2f} mm")
        print(f"    model h_eff {c['h_eff']/1e3:.1f} (check {h_eff_model_check/1e3:.1f}); ref {c['h_eff_ref']/1e3:.1f} (check {h_eff_ref/1e3:.1f}); corrected {h_eff_corr/1e3:.1f}; strict-floor {h_eff_strict/1e3:.1f}")
    return dict(model=c['h_eff'], ref=c['h_eff_ref'], corr=h_eff_corr, strict=h_eff_strict, c=c)

j18 = J.j_of(18)
print("TTV 18 LPM:")
for core in (J.JH_R, J.JH_P, J.JH_X):
    for dt in (0.3e-3, 0.5e-3, 1.0e-3):
        r = cell_corrected(core, j18, delta_turn=dt, verbose=(dt==0.5e-3))
        print(f"   delta_turn {dt*1e3:.1f} mm: corr {r['corr']/1e3:.1f} strict {r['strict']/1e3:.1f} gain vs ref {r['corr']/r['ref']:.3f}/{r['strict']/r['ref']:.3f}")
