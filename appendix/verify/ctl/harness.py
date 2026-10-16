"""Gap-closer harness: PRISM variants evaluated with the scoping model (1-D h, TIM, caloric) and the draft's own
2-D cell model (cell2d.py) for the ABSOLUTE cal+conv+base core (PRISM's own z-unmixed penalty, per verify-physics).
avg = 2-D core + q R_TIM ; max = avg + flow hot spot + TIM scatter (scaled with flux) + ripple crest (pk-pk/2)."""
import sys, math, time
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../../model')))
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../arch')))
import coldplate_model as cm
from cell2d import run as cell
TIMS = {"paste": (0.070, 3.5), "paste05": (0.050, 3.5), "PCM25": (0.055, 1.5), "PCMpkg": (0.070, 1.5), "LM": (0.015, 0.6)}
cm.TIM.update(TIMS)

def plate(A, t=0.15, gap=0.15, H=2.0, L=6.0, base=1.0, tim="paste"):
    side = math.sqrt(A) * 10; n_slots = max(1, int(round(side / (2 * L))))
    return cm.ColdPlate(name="v", footprint_cm2=A, fin_t_mm=t, gap_mm=gap, fin_h_mm=H, flow_len_mm=L, base_mm=base,
                        tim=tim, isothermal_cell=True, hotspot_flow_K=1.5, n_parallel_paths=2 * n_slots, slot_w_mm=3.0)

_cache = {}
def ev(A=117.0, Q=15000.0, lpm=18.0, t=0.15, gap=0.15, H=2.0, L=6.0, base=1.0, tim="paste", kerf=0.3, win=1.2,
       fluid=cm.PG25, hs_flow=1.5, d=None, pen=True):
    p = plate(A, t, gap, H, L, base, tim)
    r = p.evaluate(Q, lpm / (Q / 1000), fluid=fluid)
    q = r["q_W_cm2"] * 1e4
    key = (round(A, 3), Q, lpm, t, gap, H, L, base, kerf, win, fluid.name)
    if key not in _cache:
        dd = d or (0.025 if L <= 5 else 0.04)
        phi = gap / (t + gap)
        c = cell(hi=win / 2, ho=win / 2, ki=kerf / 2, ko=kerf / 2, L=L, H=H, tb=base, d=dd, q=q, dTout=r["dT_out"], h=r["h"],
                 t=t, gap=gap, kf=fluid.k, cp=fluid.cp, Kkerf_mult=((kerf / gap) ** 2 / phi) if kerf > 0 else 1.0)
        _cache[key] = c
    c = _cache[key]
    R, sc = TIMS[tim]
    core1d = r["dT_cal"] + r["dT_conv"] + r["dT_base"]
    core = c["case"] if pen else core1d
    tim_dT = q * R * 1e-4
    avg = core + tim_dT
    mx = avg + hs_flow + sc * q / 1.28e6 + c["pkpk"] / 2
    return dict(avg=avg, max=mx, core=core, core1d=core1d, pen=c["case"] - core1d, pkpk=c["pkpk"], tim=tim_dT,
                cal=r["dT_cal"], conv=r["dT_conv"], base=r["dT_base"], h=r["h"], heff=r["h_eff"], q=q / 1e4,
                dTout=r["dT_out"], u=r["u_ch"], Re=r["Re"], dp_ch=r["dp_ch_kPa"], NTU=r["NTU"])

if __name__ == "__main__":
    t0 = time.time()
    for A in (117.0, 100.0):
        for tim in ("paste", "PCM25"):
            e = ev(A=A, tim=tim)
            print(f"A {A:.0f} {tim}: avg {e['avg']:.2f} max {e['max']:.2f} | core2D {e['core']:.2f} core1D {e['core1d']:.2f} pen {e['pen']:+.2f} pkpk {e['pkpk']:.2f} [{time.time()-t0:.0f}s]", flush=True)
