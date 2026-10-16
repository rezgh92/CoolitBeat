"""PRISM-15 Rev A predicted datasheet (lane perf, 2026-10-16). Re-runs the final_thermal.py method (verify/ctl harness:
cell2d absolute 2-D core + 1-D TIM, hot spot = flow 1.5 K + TIM scatter x flux + ripple crest) at the AS-DESIGNED values:
base 0.85 (DDD-core), meter 2.31 kPa, outlet row 0.50 kPa, segment max/min 1.092 at 18 LPM (DDD-grate), 20 mm ports.
Prints OCP Cold Plate Test Spec style tables. Run from this directory: python3 perf_datasheet.py > perf_datasheet.out (~5 min)."""
import sys, os, math, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, '../appendix/verify/ctl')))
from harness import ev, cm
A_CM2, Q_W, RATED = 117.0, 15000.0, 15.0           # TTV-A heated area, benchmark power, rated flow (1.0 LPM/kW)
BASE, L = 0.85, 7.7                                 # as designed (DDD-core); segment 7.414 between kerfs, cell 7.714
FLOWS = (3.75, 7.5, 11.25, 15.0, 18.0, 22.5)        # 25-150 % of rated; 18 LPM = CoolIT benchmark flow
PG = {45: cm.Fluid('PG25 45C', 1005.0, 3930.0, 1.25e-3, 0.49),   # table values +/-5-10 % (film ~ inlet + 5 K)
      35: cm.Fluid('PG25 35C', 1012.0, 3910.0, 1.60e-3, 0.48),
      50: cm.Fluid('PG25 50C', 1002.0, 3940.0, 1.12e-3, 0.495)}
WATER = cm.WATER50
TIMS = {"paste": "paste", "PCM": "PCM25", "LM": "LM"}
def E(lpm, tim="paste", fluid=PG[45], base=BASE, Q=Q_W, A=A_CM2):
    return ev(A=A, Q=Q, lpm=lpm, tim=TIMS.get(tim, tim), fluid=fluid, L=L, base=base)
# ---- hydraulics (architecture 4.2 budget re-based on DDD-grate as-designed meter/row; 20 mm port bore) ----
INERT_18 = dict(ports=1.60, headers=0.99, sep_windows=0.46, plenums=0.19, meter=2.31, misc=0.08, row=0.50)   # kPa at 18 LPM, scale (Q/18)^2 rho/1005
VISC_18 = dict(guard=0.30, plenums_visc=0.02, misc_visc=0.08)                                              # scale Q/18 x mu/1.25e-3
def dp_plate(lpm, fluid=PG[45], e=None):
    s = lpm / 18.0; r = fluid.rho / 1005.0; m = fluid.mu / 1.25e-3
    inert = sum(INERT_18.values()) * s * s * r; visc = sum(VISC_18.values()) * s * m
    fins = (e or E(lpm, fluid=fluid))["dp_ch"]
    return inert + visc + fins, inert, visc + fins
def dp_barbs(lpm, fluid=PG[45]):                     # two 316L stubs + 1/2-in barbs (final_system.py basis 3.0 kPa at 18 LPM)
    return 3.0 * (lpm / 18.0) ** 2 * fluid.rho / 1005.0
def dp_uqd_pair(lpm, Cv, fluid=PG[45]):              # two couplings in series, dP(psi) = SG (gpm/Cv)^2 each
    gpm = lpm / 3.7854; sg = fluid.rho / 998.0
    return 2 * sg * (gpm / Cv) ** 2 * 6.8948
def coolit(A):
    p = cm.coolit_like(A); p.tim = "paste 0.07"; p.hotspot_flow_K = 0.0; return p
def coolit_eval(lpm, tim="paste", fluid=PG[45], A=119.3):
    p = coolit(A); p.tim = "paste 0.07" if tim == "paste" else "PCM pad"
    r = p.evaluate(Q_W, lpm / 15.0, fluid=fluid); sc = 3.5 if tim == "paste" else 1.5
    return dict(avg=r["dT_avg"], max=r["dT_avg"] + 0.5 * r["dT_out"] + sc * r["q_W_cm2"] / 128, dp=r["dp_total_kPa"], dTout=r["dT_out"])
def qcap(tim, Tmax=40.0, lo=10e3, hi=30e3, n=14):
    for _ in range(n):
        mid = 0.5 * (lo + hi); e = E(1.2 * mid / 1000, tim=tim, Q=mid)
        lo, hi = (mid, hi) if e["max"] < Tmax else (lo, mid)
    return lo / 1e3
P = print; H = {}
P("## 1. Benchmark point re-run (15 kW, 18 LPM PG25 k 0.49, 45 C, 117 cm2), base 0.80 (architecture) vs 0.85 (as designed)")
P("| base | TIM | cal | TIM K | base K | conv | 2-D pen | ripple pk-pk | **avg** | **max** | R'' avg cm2K/W | shift vs architecture |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|")
ARCH = {"paste": (30.97, 38.72), "PCM": (29.05, 34.80), "LM": (23.92, 28.77)}
for base in (0.80, 0.85, 0.90, 1.00):
    for tim in ("paste", "PCM", "LM"):
        e = E(18.0, tim, base=base); a0, m0 = ARCH[tim]
        if base == BASE: H[tim] = e
        P(f"| {base:.2f} | {tim} | {e['cal']:.2f} | {e['tim']:.2f} | {e['base']:.2f} | {e['conv']:.2f} | {e['pen']:+.2f} | {e['pkpk']:.2f} | **{e['avg']:.2f}** | **{e['max']:.2f}** | {e['avg']*A_CM2/Q_W:.3f} | {e['avg']-a0:+.2f} / {e['max']-m0:+.2f} K |", flush=True)
e = H["paste"]; P(f"channel: u {e['u']:.3f} m/s, Re {e['Re']:.0f}, h {e['h']/1e3:.1f} kW/m2K, h_eff {e['heff']/1e3:.0f} kW/m2K, NTU {e['NTU']:.2f}, fin dP {e['dp_ch']:.2f} kPa, dT_out {e['dTout']:.2f} K")
P("\n## 2. Segment balance 1.092 (DDD-grate, lumped row) vs the 1.5 K flow hot-spot allowance: weakest segment re-evaluated")
for lpm, mm in ((18.0, 1.092), (27.0, 1.122), (9.0, 1.057)):
    qmin = 1 / math.sqrt(mm)                        # max/min symmetric about the mean (assumption; per-segment detail in DDD-grate 6.3)
    n = E(lpm, "paste"); w = E(lpm * qmin, "paste")   # weakest segment: same flux, flow x qmin
    d = (w["cal"] + w["conv"]) - (n["cal"] + n["conv"])
    P(f"- {lpm:.0f} LPM: max/min {mm}, weakest segment at {qmin:.3f} x mean flow -> core +{d:.2f} K over nominal (allowance 1.5 K, margin {1.5-d:.2f} K)")
P("\n## 3. Q capacity at Tcase,max <= 85 C with 45 C inlet, 1.2 LPM/kW (thermal) and the velocity-rated cap 19.5 kW (meter 2.0 m/s at 23.4 LPM)")
QC = {}
for tim in ("paste", "PCM", "LM"):
    QC[tim] = qcap(tim); P(f"- {tim}: thermal {QC[tim]:.1f} kW (architecture {dict(paste=15.7, PCM=18.5, LM=25.5)[tim]}); rated {min(QC[tim], 19.5):.1f} kW", flush=True)
P("\n## 4. OCP-style R table: 15 kW, 45 C inlet, PG25, 117 cm2; R = dT/Q, R'' = dT A/Q; average and max basis; CoolIT-like = model-only")
P("| LPM | LPM/kW | % rated | dT_out K | Tout C | PCM avg/max K | PCM R mK/W avg/max | PCM R'' cm2K/W avg/max | paste avg/max K | paste R mK/W avg/max | paste R'' avg/max | LM avg/max K | CoolIT-like paste avg/max | CoolIT-like PCM avg/max |")
P("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
SW = {}
for lpm in FLOWS:
    a, b, c = E(lpm, "paste"), E(lpm, "PCM"), E(lpm, "LM"); ca, cb = coolit_eval(lpm, "paste"), coolit_eval(lpm, "PCM"); SW[lpm] = (a, b, c, ca, cb)
    f = lambda e: f"{e['avg']:.1f} / {e['max']:.1f}"; r = lambda e: f"{e['avg']/15:.2f} / {e['max']/15:.2f}"; rr = lambda e: f"{e['avg']*A_CM2/Q_W:.3f} / {e['max']*A_CM2/Q_W:.3f}"
    flag = " (!)" if 45 + a["dTout"] > 65 else ""
    P(f"| {lpm:.2f} | {lpm/15:.2f} | {lpm/15*100:.0f} | {a['dTout']:.1f} | {45+a['dTout']:.1f}{flag} | {f(b)} | {r(b)} | {rr(b)} | {f(a)} | {r(a)} | {rr(a)} | {f(c)} | {f(ca)} | {f(cb)} |", flush=True)
P("(!) outlet > 65 C at 15 kW: test at reduced power (R is power-independent to first order); CoolIT-like off 1.2 LPM/kW is model-only.")
P("\n## 5. Pressure drop at the same flows, PG25 45 C (kPa); three boundaries + UQD08 pairs; CoolIT-like = model-only reconstruction")
P("| LPM | % rated | plate port-to-port (20 mm bore) | inertial / viscous | + stubs & 1/2-in barbs | + UQD08 pair Cv 4.75 | + UQD08 pair Cv 3.65 | CoolIT-like port-to-port | water port-to-port |")
P("|---|---|---|---|---|---|---|---|---|")
DP = {}
for lpm in FLOWS + (27.0, 36.0):
    e = SW[lpm][0] if lpm in SW else E(lpm, "paste"); t, i, v = dp_plate(lpm, e=e); bb = dp_barbs(lpm); tw = dp_plate(lpm, WATER)[0]
    cdp = SW[lpm][3]["dp"] if lpm in SW else coolit_eval(lpm)["dp"]; DP[lpm] = (t, i, v, bb)
    P(f"| {lpm:.2f} | {lpm/15*100:.0f} | **{t:.2f}** | {i:.2f} / {v:.2f} | {t+bb:.1f} | {t+bb+dp_uqd_pair(lpm,4.75):.1f} | {t+bb+dp_uqd_pair(lpm,3.65):.1f} | {cdp:.1f} | {tw:.2f} |")
P("plate at 18 LPM by element (kPa): " + ", ".join(f"{k} {v:.2f}" for k, v in INERT_18.items()) + f", guard+visc {sum(VISC_18.values()):.2f}, fins {H['paste']['dp_ch']:.2f}; 36 LPM for the <= 30 kPa claim")
P("\n## 6. Inlet temperature 35 / 45 / 50 C (PG25 properties at film ~ inlet + 5 K; +/-10 % on mu) and water vs PG25 at 45 C; 15 kW")
P("| case | LPM | PCM avg/max K | Tcase avg/max C | paste avg/max K | Tcase avg/max C | Tout C | plate dP kPa | fin dP kPa |")
P("|---|---|---|---|---|---|---|---|---|")
for lab, fl, tin in (("PG25 35 C", PG[35], 35), ("PG25 45 C", PG[45], 45), ("PG25 50 C", PG[50], 50), ("water 45 C", WATER, 45)):
    for lpm in (15.0, 18.0, 22.5):
        a, b = E(lpm, "paste", fl), E(lpm, "PCM", fl); t = dp_plate(lpm, fl, e=a)[0]
        P(f"| {lab} | {lpm:.1f} | {b['avg']:.1f} / {b['max']:.1f} | {tin+b['avg']:.1f} / {tin+b['max']:.1f} | {a['avg']:.1f} / {a['max']:.1f} | {tin+a['avg']:.1f} / {tin+a['max']:.1f} | {tin+a['dTout']:.1f} | {t:.2f} | {a['dp_ch']:.2f} |", flush=True)
P("\n## 7. Design margins at rated (15 LPM), benchmark (18) and 150 % rated (22.5 LPM)")
P("| quantity | 15 LPM | 18 LPM | 22.5 LPM | cap | basis |")
P("|---|---|---|---|---|---|")
rows = [("port velocity m/s (20 mm bore)", lambda s: 0.955 * s, "<= 1.5 at 150 % rated", "architecture 4.1"),
        ("meter mean orifice velocity m/s", lambda s: 1.538 * s, "<= 2.0 (reached at 23.4 LPM)", "DDD-grate 6.1, 195.1 mm2"),
        ("meter max single orifice m/s", lambda s: 1.64 * s, "mean-velocity rule; 2.05 at 22.5", "DDD-grate 6.1"),
        ("outlet row velocity m/s", lambda s: 0.718 * s, "0.5 kPa row", "DDD-grate 6.3"),
        ("inlet header m/s", lambda s: 0.93 * s, "<= 1.5", "architecture 4.1"),
        ("plenum half-channel m/s", lambda s: 0.62 * s, "<= 0.9 CDA (return > 60 C)", "DDD-plenum P3"),
        ("window face mean m/s", lambda s: 0.331 * s, "fin-top <= 0.5 (E2 CFD)", "DDD-grate 5"),
        ("fin channel m/s", lambda s: H['paste']['u'] * s, "Re ~44, laminar", "harness ev"),
        ("guard face m/s (25 cm2)", lambda s: 0.12 * s, "0.1-0.2 kPa clean", "architecture 4.1")]
for lab, fn, cap, basis in rows:
    P(f"| {lab} | {fn(15/18):.2f} | {fn(1.0):.2f} | {fn(22.5/18):.2f} | {cap} | {basis} |")
P("\n| pressure / structure | value | allowable or limit | margin | basis |")
P("|---|---|---|---|---|")
for lab, v, lim, mg, basis in (
        ("MAWP / proof (100 %) / design burst / sample burst", "1.03 / 1.55 / >= 3.1 / >= 4.5 MPa", "150 psi class; leak-before-break", "burst >= 3x MAWP", "architecture 5.2"),
        ("folded plenum wall 0.8 at 7.7 pitch, tension at 3.1 MPa", "29.8 MPa", "40 MPa (annealed OFE design)", "1.34x", "ctl/pkgA_dp_stress.out"),
        ("separator 1.8 over 6.9 channel at 3.1 MPa", f"{32.8*(1.5/1.8)**2:.1f} MPa", "40 MPa", f"{40/(32.8*(1.5/1.8)**2):.2f}x", "pkgA_dp_stress 32.8 at 1.5 mm, scaled (t)^-2"),
        ("arched cap 1.0 mm r 6 hoop / port pocket r 12 at 1.5", "18.6 / 24.8 MPa", "40 MPa", "2.2x / 1.6x", "pkgA_dp_stress.out"),
        ("grate web 0.40 over 2.70 recess at 36 LPM meter dP 9.2 kPa", "0.21 MPa", "40 MPa", "190x", "DDD-grate 8"),
        ("recess floor cantilever 0.75 lip at t 0.50", "7.5 MPa", "40 MPa", "5.3x", "DDD-grate 8"),
        ("defect: one unbonded land strip, base 0.85, kerf-to-kerf 7.4 span", f"collapse {1.6*(0.85/0.8)**2:.1f}-{2.3*(0.85/0.8)**2:.1f} MPa; proof bulge {2.2*(0.8/0.85)**3:.1f} um", "leak-tight at MAWP; confocal 1 um sees it", "below design burst: gated on E1 per-strip detection", "pkgA_dp_stress at 0.8 scaled t^2 / t^-3"),
        ("clamp bow 2 kN TTV (2-side lands) / 480 N product", "22.6 / 5.4 um concave", "thermal bow +18.7 um convex at 15 kW", "net -4.0 um TTV; form rule 0-10 um concave", "DDD-mech 7"),
        ("fin ties: pressure load 1.03 MPa x 117 cm2", "12 kN self-equilibrated", "no clamp entry", "-", "DDD-mech 5 / architecture 5.2")):
    P(f"| {lab} | {v} | {lim} | {mg} | {basis} |")
P("\n## 8. Headline JSON (params-perf.json content)")
sw18 = SW[18.0]; sw15 = SW[15.0]
out = dict(key="perf", date="2026-10-16", doc="docs/cooling/design/DDD-perf.md", basis="final_thermal.py method, base 0.85, meter 2.31, row 0.50, seg max/min 1.092, 20 mm ports, PG25 k 0.49, 117 cm2, 15 kW, 45 C",
           benchmark_18lpm={t: dict(avg_K=round(H[t]["avg"], 2), max_K=round(H[t]["max"], 2), R_avg_mK_W=round(H[t]["avg"] / 15, 3), R_max_mK_W=round(H[t]["max"] / 15, 3),
                                    Rpp_avg_cm2K_W=round(H[t]["avg"] * A_CM2 / Q_W, 4), Rpp_max_cm2K_W=round(H[t]["max"] * A_CM2 / Q_W, 4)) for t in H},
           shift_vs_architecture_K={t: [round(H[t]["avg"] - ARCH[t][0], 2), round(H[t]["max"] - ARCH[t][1], 2)] for t in H},
           rated_15lpm={"paste": [round(sw15[0]["avg"], 1), round(sw15[0]["max"], 1)], "PCM": [round(sw15[1]["avg"], 1), round(sw15[1]["max"], 1)]},
           dp_kPa={f"{l:g}": dict(plate=round(DP[l][0], 2), inertial=round(DP[l][1], 2), viscous=round(DP[l][2], 2), with_barbs=round(DP[l][0] + DP[l][3], 1),
                                  with_barbs_uqd08_cv4p75=round(DP[l][0] + DP[l][3] + dp_uqd_pair(l, 4.75), 1), with_barbs_uqd08_cv3p65=round(DP[l][0] + DP[l][3] + dp_uqd_pair(l, 3.65), 1)) for l in DP},
           q_cap_kW={t: dict(thermal=round(QC[t], 1), rated=round(min(QC[t], 19.5), 1)) for t in QC},
           sweep={f"{l:g}": dict(paste=[round(SW[l][0]["avg"], 1), round(SW[l][0]["max"], 1)], PCM=[round(SW[l][1]["avg"], 1), round(SW[l][1]["max"], 1)], LM=[round(SW[l][2]["avg"], 1), round(SW[l][2]["max"], 1)],
                                 coolit_like_paste=[round(SW[l][3]["avg"], 1), round(SW[l][3]["max"], 1)], coolit_like_PCM=[round(SW[l][4]["avg"], 1), round(SW[l][4]["max"], 1)], coolit_like_dp=round(SW[l][3]["dp"], 1), Tout_C=round(45 + SW[l][0]["dTout"], 1)) for l in FLOWS},
           channel=dict(u_m_s=round(H["paste"]["u"], 3), Re=round(H["paste"]["Re"], 1), h_eff_kW_m2K=round(H["paste"]["heff"] / 1e3, 1), fin_dp_kPa=round(H["paste"]["dp_ch"], 2)),
           velocity_caps=dict(meter_m_s_18=1.538, meter_cap=2.0, meter_cap_lpm=23.4, port_m_s_18=0.955, port_cap=1.5, rated_kW_velocity=19.5))
json.dump(out, open(os.path.join(HERE, "params-perf.json"), "w"), indent=1); P(json.dumps(out["benchmark_18lpm"]))
