import sys
sys.path.insert(0, "docs/cooling/appendix/design/jet")
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import jet_hybrid_model as m
JH_R = m.JH_R
for tim in ("PCM pad", "liquid metal", "paste 0.07" if "paste 0.07" in m.TIM else list(m.TIM)[0]):
    r = m.plate_eval(JH_R, tim=tim)
    print(tim, "nominal Qcap", round(r["Qcap"],1), "LPM at Qcap (1.2/kW)", round(r["Qcap"]*1.2,1),
          "Vj at Qcap", round(r["Vj"]*r["Qcap"]*1.2/18,2))
    # fixed-flow Q cap at the 1.94 m/s continuous jet cap -> 22.5 LPM
    lpm_cap = 18*1.94/r["Vj"]
    lo, hi = 10e3, 60e3
    for _ in range(60):
        Q = 0.5*(lo+hi)
        rr = m.plate_eval(JH_R, Q=Q, lpm_per_kw=lpm_cap/(Q/1000), tim=tim)
        if rr["Tcmax"] > 85: hi = Q
        else: lo = Q
    print("   Q cap at velocity-capped flow", round(lpm_cap,1), "LPM:", round(Q/1e3,1), "kW; Vj", round(rr["Vj"],2), "dP kPa", round(rr["dp"]/1e3,1))
    # equal pump 6.5 W point Vj
print(m.TIM.keys())
# Vj at equal pumping power 28.5 LPM
print("Vj at 28.5 LPM", round(JH_R.cell(m.j_of(28.5))["Vj"],2), "at 27 LPM (150% rated)", round(JH_R.cell(m.j_of(27))["Vj"],2))
