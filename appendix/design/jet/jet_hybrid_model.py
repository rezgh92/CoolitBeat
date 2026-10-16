#!/usr/bin/env python3
"""
Jet-hybrid lens (key = jet-hybrid): quantitative scoping of jet impingement and slot-jet-into-micro-fin
hybrid cold plates against the HMMC baseline, on the CoolIT 15 kW benchmark operating point
(15 kW, 18 LPM PG25, 45 C inlet, calibrated 117 cm2 footprint = 128 W/cm2).

Corrections to the earlier draft (jet_calc.py):
  * Martin (1977) ARN: Nu/Pr^0.42 = K(Ar,H/D) G(Ar,H/D) F2(Re), F2 = 0.5 Re^(2/3). The draft omitted the 0.5 (2x high).
  * The draft's 'Womac' wall-jet term (0.344 Re_L^0.8 on jet velocity) is a turbulent flat-plate form that ignores
    continuity in a confined array and gave 160-600 kW/m2K; replaced by the Womac et al. (1993) two-zone form
    Nu_L = A Re_d^0.5 Pr^0.4 (L/d) A_r + B Re_L*^0.532 Pr^0.4 (1 - A_r), A = 0.516, B = 0.491 (recalled, +/-30 %).

Sections
  A. Bare-surface jet arrays over 117 cm2 at 18 and 36 LPM (three correlations), dP, pump power.
  B. Slot-jet-into-micro-fin hybrid cell model (the proposed core): h_eff and core dP vs nozzle width, row pitch,
     fin height; cores R (0.15 mm gaps, 50 um abs screen) and X (0.30 mm gaps, screen-free on 50 um nominal loops).
  C. Full plate at the benchmark point (series network identical to coldplate_model: isothermal caloric, TIM, base,
     convection, hot spot = flow term + TIM scatter), dP budget, Q capacity; 2x flow; equal pumping power.
  D. Real 2027-28 package (4 reticle dies at 350 W/cm2 + 16 HBM), die-zone h_eff and hottest-die case dT.
  E. 1.4-3.6 kW GPU-class plates.
  F. Monte Carlo P10/P50/P90 for the nominal design.
All correlations laminar/transitional, +/-25-30 % per term. Scoping, not CFD.
"""
from __future__ import annotations
import math, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from coldplate_model import ColdPlate, hmmc, coolit_like, TIM, PG25, K_CU, K_AL  # noqa: E402

F = PG25
rho, mu, cp, k = F.rho, F.mu, F.cp, F.k
nu = mu / rho
Pr = F.Pr
A_FP = 117e-4          # benchmark footprint m2
Q0 = 15000.0           # W
T_IN = 45.0


def j_of(lpm, area=A_FP):
    return lpm / 60e3 / area


# ---------------------------------------------------------------------------------------------
# A. Bare-surface jet arrays
# ---------------------------------------------------------------------------------------------
def martin_arn_h(Re, Ar, HD, d):
    """Martin (1977) array of round nozzles; valid 2000<=Re<=1e5, 0.004<=Ar<=0.04, 2<=H/D<=12."""
    sa = math.sqrt(Ar)
    K = (1 + (HD / (0.6 / sa)) ** 6) ** (-0.05)
    G = 2 * sa * (1 - 2.2 * sa) / (1 + 0.2 * (HD - 6) * sa)
    Nu = Pr ** 0.42 * K * G * 0.5 * Re ** (2 / 3)
    return Nu * k / d


def womac_h(Vj, d, S):
    """Womac, Ramadhyani & Incropera (1993) two-zone submerged-jet form, square cell of side S."""
    Re = Vj * d / nu
    Arst = (math.pi * (1.9 * d) ** 2 / 4) / S ** 2
    Arst = min(Arst, 1.0)
    Lstar = max(0.604 * S - 0.95 * d, 0.2 * d)
    ReL = Vj * Lstar / nu
    Nu_L = 0.516 * Re ** 0.5 * Pr ** 0.4 * (S / d) * Arst + 0.491 * ReL ** 0.532 * Pr ** 0.4 * (1 - Arst)
    return Nu_L * k / S


def laminar_stag_h(Vj, d, S, C=0.80, n=0.8):
    """Laminar stagnation disc Nu0 = C Re^0.5 Pr^0.4 to r0 = 0.75 d, then h ~ (r0/r)^n (Liu-Lienhard class)."""
    Re = Vj * d / nu
    h0 = C * Re ** 0.5 * Pr ** 0.4 * k / d
    R = S / math.sqrt(math.pi)
    r0 = 0.75 * d
    if R <= r0:
        return h0
    integ = r0 ** 2 + 2 * r0 ** n * (R ** (2 - n) - r0 ** (2 - n)) / (2 - n)
    return h0 * integ / R ** 2


def jet_dp(V, Cd=0.75, Kexit=1.0):
    return 0.5 * rho * V ** 2 * (1 / Cd ** 2 + Kexit)


def section_A():
    out = []
    out.append("## A. Bare-surface round-jet arrays with distributed returns, 117 cm2 uniform (H/D = 2)\n")
    out.append("Continuity fixes the jet velocity: Vj = j / Ar, j = flow / footprint (2.56 cm/s at 18 LPM). "
               "h = area-averaged base h (no fins). dP = jet loss (1/Cd^2 + 1 dynamic heads, Cd 0.75) + 3.5 kPa ports/manifold.\n")
    out.append("| LPM | d mm | Ar | pitch mm | Vj m/s | Re_d | h Martin* | h Womac | h laminar | jet dP kPa | plate dP kPa | pump W |")
    out.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for lpm in (18, 36):
        j = j_of(lpm)
        for d in (0.3e-3, 0.5e-3):
            for Ar in (0.005, 0.01, 0.02, 0.04):
                Vj = j / Ar
                Re = Vj * d / nu
                S = d * math.sqrt(math.pi / 4 / Ar)
                hm = martin_arn_h(Re, Ar, 2.0, d)
                hw = womac_h(Vj, d, S)
                hl = laminar_stag_h(Vj, d, S)
                dpj = jet_dp(Vj)
                dpt = dpj + 3.5e3 * (lpm / 18) ** 2
                pw = dpt * lpm / 60e3
                flag = "" if Re >= 2000 else "*"
                out.append(f"| {lpm} | {d*1e3:.1f} | {Ar:.3f} | {S*1e3:.2f} | {Vj:.2f} | {Re:.0f}{flag} | {hm/1e3:.0f} | "
                           f"{hw/1e3:.0f} | {hl/1e3:.0f} | {dpj/1e3:.1f} | {dpt/1e3:.1f} | {pw:.1f} |")
    out.append("(* Re < 2000: Martin extrapolated below its validity; treat as an optimistic bound.)\n")
    # literature sanity: what j / Vj do the 100-300 kW/m2K literature arrays need?
    out.append("Literature check (same correlations, water-like Pr 4, nu 0.6e-6): a 0.1 mm nozzle at Ar 0.02 needs "
               "Re ~3000 (Vj ~18 m/s, jet dP ~250 kPa, j ~0.36 m/s = 14x our 2.56 cm/s) to reach "
               f"~{martin_arn_h_water(3000, 0.02, 2.0, 0.1e-3)/1e3:.0f} kW/m2K. The 100-300 kW/m2K microjet results (Browne/Peles, "
               "Brunschwiler/IBM 31-126 um) live at 10-40x our volumetric flux density and 5-50x our dP.\n")
    return "\n".join(out)


def martin_arn_h_water(Re, Ar, HD, d, Prw=3.6, kw=0.64):
    sa = math.sqrt(Ar)
    K = (1 + (HD / (0.6 / sa)) ** 6) ** (-0.05)
    G = 2 * sa * (1 - 2.2 * sa) / (1 + 0.2 * (HD - 6) * sa)
    return Prw ** 0.42 * K * G * 0.5 * Re ** (2 / 3) * kw / d


# ---------------------------------------------------------------------------------------------
# B. Slot-jet-into-micro-fin hybrid cell
# ---------------------------------------------------------------------------------------------
def nu_rect_fd(alpha):
    return 8.235 * (1 - 2.0421 * alpha + 3.0853 * alpha ** 2 - 2.4765 * alpha ** 3
                    + 1.0578 * alpha ** 4 - 0.1861 * alpha ** 5) * 0.95


def fRe_rect(alpha):
    return 24 * (1 - 1.3553 * alpha + 1.9467 * alpha ** 2 - 1.7012 * alpha ** 3
                 + 0.9564 * alpha ** 4 - 0.2537 * alpha ** 5)


def channel_h(b, H, u, L):
    """Same correlation as coldplate_model (rectangular duct, 3-side heating, Stephan-type entrance)."""
    alpha = min(b, H) / max(b, H)
    Dh = 2 * b * H / (b + H)
    Re = u * Dh / nu
    xs = max(L, 1e-5) / (Dh * Re * Pr)
    Nu = nu_rect_fd(alpha) + 0.024 * xs ** -1.14 / (1 + 0.0358 * Pr ** 0.17 * xs ** -0.64)
    return Nu * k / Dh, Re, Dh


def descent_h(b, H, V):
    """Fin walls inside the jet column: simultaneously developing parallel-plate flow at V over path H
    (mean Nu, Shah-London H-boundary thermal entrance, Dh = 2b)."""
    Dh = 2 * b
    Re = V * Dh / nu
    xs = H / (Dh * Re * Pr)
    Nu = 7.54 + 0.024 * xs ** -1.14 / (1 + 0.0358 * Pr ** 0.17 * xs ** -0.64)
    return Nu * k / Dh


def stag_h_plane(V, w, C=0.6):
    """Plane (Hiemenz) laminar stagnation flow, velocity gradient a = C V / w."""
    a = C * V / w
    return 0.57 * Pr ** 0.4 * k * math.sqrt(a / nu)


class SlotJetFin:
    """Slot-jet-into-micro-fin cell.
    Geometry: parallel skived fins (gap b, thickness t, height H) run along x. A nozzle/return lamina (thickness
    t_lam) is bonded to every fin tip (tie). It carries nozzle slots (width w_n) and return slots (width w_r)
    alternating at pitch P_r/2, both running across the fins (along y). Fluid issues from the nozzle slot straight
    into the fin gaps, impinges on the base between the fins, turns, runs a flow length ~P_r/2 along the channel and
    rises into the return slot. Every channel is fed by every nozzle slot (no unfed channels)."""

    def __init__(self, name, b, t, H, w_n, P_r, w_r=1.0e-3, t_lam=0.3e-3, base=1.0e-3, ksol=K_CU,
                 c_turn=0.5, C_stag=0.6, enh=1.0):
        self.name, self.b, self.t, self.H = name, b, t, H
        self.w_n, self.P_r, self.w_r, self.t_lam = w_n, P_r, w_r, t_lam
        self.base, self.ksol = base, ksol
        self.c_turn, self.C_stag, self.enh = c_turn, C_stag, enh

    def cell(self, j):
        b, t, H, w_n, P_r, w_r = self.b, self.t, self.H, self.w_n, self.P_r, self.w_r
        p = b + t
        phi = b / p
        qline = j * P_r                       # m2/s per metre of nozzle slot
        V_slot = qline / w_n                  # velocity in the lamina slot (gross)
        Vj = V_slot / phi                     # velocity entering the fin gaps under the slot
        u_ch = qline / (2 * H * phi)          # channel velocity after the turn
        Lc = P_r / 2
        x1 = min(w_n / 2 + self.c_turn * H, Lc - w_r / 2 - 0.2e-3)
        L2 = max(Lc - w_r / 2 - x1, 0.2e-3)
        # region 1: jet column and turn
        V1 = 0.5 * (Vj + u_ch)
        h_desc = descent_h(b, H, V1) * self.enh
        h_st = stag_h_plane(Vj, w_n, self.C_stag) * self.enh
        # region 2: channel at u_ch, thermal entrance restarted after impingement
        h_ch, Re_ch, Dh = channel_h(b, H, u_ch, L2)
        # region 3 (return rise, w_r/2): channel h (conservative)
        f1 = x1 / Lc
        h_fin = f1 * h_desc + (1 - f1) * h_ch
        h_base = f1 * h_st + (1 - f1) * h_ch
        m = math.sqrt(2 * h_fin / (self.ksol * t))
        eta = math.tanh(m * H) / (m * H)
        h_eff = (h_fin * 2 * H * eta + h_base * b) / p
        # open-slot reference (HMMC-like) on the same fins/flow length: whole length is channel flow
        h_ref_ch, _, _ = channel_h(b, H, u_ch, Lc)
        m0 = math.sqrt(2 * h_ref_ch / (self.ksol * t))
        eta0 = math.tanh(m0 * H) / (m0 * H)
        h_eff_ref = h_ref_ch * (2 * H * eta0 + b) / p
        # core dP (Pa): lamina slot entry (K 0.5 on V_slot) + slot friction + gap contraction 0.5(1-phi)
        # + jet dynamic head lost at impingement (1.0) on Vj; channel friction (Darcy) + 90-deg turn (1.2) on u_ch
        # + return rise/expansion (1.0 on u_ch) + return slot exit (1.0 on V_ret)
        alpha = min(b, H) / max(b, H)
        fRe = fRe_rect(alpha)
        Dh_slot = 2 * w_n
        Re_slot = V_slot * Dh_slot / nu
        f_slot = 96 / max(Re_slot, 1)
        dp_noz = 0.5 * rho * (0.5 * V_slot ** 2 + f_slot * self.t_lam / Dh_slot * V_slot ** 2
                              + (1 + 0.5 * (1 - phi)) * Vj ** 2)
        dp_ch = 2 * fRe * mu * u_ch * (L2 + 0.5 * x1) / Dh ** 2 + 0.5 * rho * u_ch ** 2 * (1.2 + 1.0)
        V_ret = qline / w_r
        dp_ret = 0.5 * rho * V_ret ** 2 * 1.0
        return dict(p=p, phi=phi, Vj=Vj, V_slot=V_slot, u_ch=u_ch, Re_ch=Re_ch, Re_jet=Vj * 2 * b / nu,
                    Re_slot=V_slot * w_n / nu, x1=x1, Lc=Lc, f1=f1, h_desc=h_desc, h_st=h_st, h_ch=h_ch,
                    h_fin=h_fin, h_base=h_base, eta=eta, h_eff=h_eff, h_eff_ref=h_eff_ref,
                    gain=h_eff / h_eff_ref, dp_noz=dp_noz, dp_ch=dp_ch, dp_ret=dp_ret,
                    dp_core=dp_noz + dp_ch + dp_ret)


def section_B():
    out = ["## B. Slot-jet-into-micro-fin cell (uniform 128 W/cm2, j = 2.56 cm/s at 18 LPM)\n",
           "h_eff = (h_fin 2H eta + h_base b)/p with region weighting: jet column + turn (x1 = w_n/2 + 0.5 H: descent "
           "flow at (Vj+u_ch)/2 on the fin walls, plane stagnation on the floor) and channel flow (entrance restarted). "
           "'open-slot ref' = same fins and flow length fed like an HMMC (no jet). Core dP excludes ports/manifold.\n",
           "| core | b/t/H mm | w_n mm | P_r mm | flow len mm | Vj m/s | u_ch m/s | h_st | h_desc | h_ch | eta | h_eff jet | h_eff open-slot ref | gain | dP noz | dP ch+ret | core dP kPa |",
           "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    j = j_of(18)
    rows = []
    for core, b, t, Hs in (("R", 0.15e-3, 0.10e-3, (1.5e-3, 2.0e-3)), ("X", 0.30e-3, 0.20e-3, (2.0e-3, 3.0e-3))):
        for H in Hs:
            for w_n in ((0.20e-3, 0.25e-3, 0.30e-3) if core == "R" else (0.30e-3, 0.40e-3)):
                for P_r in (4e-3, 6e-3, 8e-3):
                    c = SlotJetFin(core, b, t, H, w_n, P_r).cell(j)
                    rows.append((core, b, t, H, w_n, P_r, c))
                    out.append(f"| {core} | {b*1e3:.2f}/{t*1e3:.2f}/{H*1e3:.1f} | {w_n*1e3:.2f} | {P_r*1e3:.0f} | {P_r/2*1e3:.0f} | "
                               f"{c['Vj']:.2f} | {c['u_ch']:.3f} | {c['h_st']/1e3:.0f} | {c['h_desc']/1e3:.0f} | {c['h_ch']/1e3:.1f} | "
                               f"{c['eta']:.2f} | **{c['h_eff']/1e3:.0f}** | {c['h_eff_ref']/1e3:.0f} | {c['gain']:.2f} | "
                               f"{c['dp_noz']/1e3:.2f} | {(c['dp_ch']+c['dp_ret'])/1e3:.2f} | {c['dp_core']/1e3:.2f} |")
    out.append("")
    return "\n".join(out), rows


# ---------------------------------------------------------------------------------------------
# C. Full plate on the benchmark point
# ---------------------------------------------------------------------------------------------
PLUMB_18 = dict(ports=2.57e3, manifold=0.61e3)   # design-H class ports (16 mm) + troughs/loops/tees (HMMC-elite)


def plate_eval(core: SlotJetFin, Q=Q0, lpm_per_kw=1.2, tim="PCM pad", area=A_FP, screen_kPa=0.40,
               hotspot_flow=1.5, ports_mm=16.0):
    lpm = lpm_per_kw * Q / 1000
    j = j_of(lpm, area)
    c = core.cell(j)
    q = Q / area
    Vdot = lpm / 60e3
    mdot = Vdot * rho
    dT_out = Q / (mdot * cp)
    NTU = c["h_eff"] * area / (mdot * cp)
    cal = dT_out * (1 / (1 - math.exp(-NTU)) - 1 / NTU)
    R_tim, scatter = TIM[tim]
    dT_tim = q * R_tim * 1e-4
    dT_base = q * core.base / core.ksol
    dT_conv = q / c["h_eff"]
    avg = cal + dT_tim + dT_base + dT_conv
    hs = hotspot_flow + scatter * (q / 1.28e6)
    mx = avg + hs
    s = (lpm / 18.0) ** 2
    port_scale = (16.0 / ports_mm) ** 4
    dp = c["dp_core"] + (PLUMB_18["ports"] * port_scale + PLUMB_18["manifold"]) * s + screen_kPa * 1e3 * s
    flux = dT_tim + dT_base + dT_conv
    allowed = 85.0 - T_IN - cal - hs
    Qcap = Q * allowed / flux
    return dict(lpm=lpm, q=q / 1e4, dT_out=dT_out, NTU=NTU, cal=cal, tim=dT_tim, base=dT_base, conv=dT_conv,
                avg=avg, hs=hs, max=mx, Rpp=avg / (q / 1e4), dp=dp, pump=dp * Vdot, Qcap=Qcap / 1e3,
                h_eff=c["h_eff"], Vj=c["Vj"], u_ch=c["u_ch"], dp_core=c["dp_core"], dp_noz=c["dp_noz"],
                Tcmax=T_IN + mx, ratio_head=(c["dp_noz"] + c["dp_ch"]) / (0.5 * rho * 0.78 ** 2 * s))


def hmmc_eval(core="R", tim="PCM pad", lpm_per_kw=1.2, Q=Q0, area_cm2=117):
    r = hmmc(area_cm2, core=core, tim=tim).evaluate(Q, lpm_per_kw)
    # add the 0.4 kPa clean screen used in HMMC-elite's 6.0 kPa budget
    r = dict(r)
    r["dp_total_kPa"] += 0.40 * (r["flow_lpm"] / 18) ** 2
    r["pump_W"] = r["dp_total_kPa"] * 1e3 * r["flow_lpm"] / 60e3
    return r


def fmt(name, r):
    return (f"| {name} | {r['lpm']:.0f} | {r['Vj']:.2f} | {r['h_eff']/1e3:.0f} | {r['cal']:.1f} | {r['tim']:.1f} | {r['base']:.1f} | "
            f"{r['conv']:.1f} | **{r['avg']:.1f}** | {r['max']:.1f} | {r['Rpp']:.3f} | {r['dp']/1e3:.1f} | {r['pump']:.1f} | {r['Qcap']:.1f} |")


def fmt_h(name, r):
    return (f"| {name} | {r['flow_lpm']:.0f} | - | {r['h_eff']/1e3:.0f} | {r['dT_cal']:.1f} | {r['dT_tim']:.1f} | {r['dT_base']:.1f} | "
            f"{r['dT_conv']:.1f} | **{r['dT_avg']:.1f}** | {r['dT_max']:.1f} | {r['R_unit_cm2K_W']:.3f} | {r['dp_total_kPa']:.1f} | "
            f"{r['pump_W']:.1f} | {r['Q_cap_kW']:.1f} |")


HDR = ("| design | LPM | Vj m/s | h_eff kW/m2K | caloric | TIM | base | conv | **avg dT** | max dT | R'' cm2K/W | dP kPa | pump W | Q cap kW |\n"
       "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

# Nominal designs of record
JH_R = SlotJetFin("JH-R", 0.15e-3, 0.10e-3, 2.0e-3, 0.22e-3, 8e-3)    # robust core, 50 um abs screen
JH_X = SlotJetFin("JH-X", 0.30e-3, 0.25e-3, 4.0e-3, 0.30e-3, 10e-3)   # screen-free extended-fouling core
JH_P = SlotJetFin("JH-P", 0.10e-3, 0.10e-3, 1.5e-3, 0.18e-3, 6e-3)    # performance core (<= 33 um loops)


def section_C():
    out = ["## C. Full plate at 15 kW / 18 LPM PG25 / 45 C / 117 cm2\n",
           "Plumbing as HMMC-elite design H: 16 mm ports 2.57 kPa + troughs/loops/tees 0.61 kPa at 18 LPM; integrated "
           "screen 0.40 kPa clean (R, P cores); X core has only a 100 um installation strainer (0.10 kPa). Hot spot = "
           "1.5 K flow term (nozzle-metered, branch/head >= 6) + TIM scatter.\n", HDR]
    rows = []
    rows.append(("CoolIT-like skived split-flow, paste (calibration)", None))
    out.append(fmt_h("CoolIT-like skived split-flow, paste (calibration)", coolit_like(117).evaluate(Q0, 1.2)))
    out.append(fmt_h("HMMC-R 0.15/0.10x2.0, PCM (reference)", hmmc_eval("R", "PCM pad")))
    out.append(fmt_h("HMMC-R, liquid metal (reference)", hmmc_eval("R", "liquid metal")))
    for core, scr in ((JH_R, 0.40), (JH_X, 0.10), (JH_P, 0.40)):
        for tim in ("paste 0.07", "PCM pad", "liquid metal"):
            r = plate_eval(core, tim=tim, screen_kPa=scr)
            out.append(fmt(f"{core.name} b/t/H {core.b*1e3:.2f}/{core.t*1e3:.2f}/{core.H*1e3:.1f}, w_n {core.w_n*1e3:.2f}, P_r {core.P_r*1e3:.0f}, {tim}", r))
    out.append("")
    # direct-to-die
    r = plate_eval(SlotJetFin("JH-R D2D", 0.15e-3, 0.10e-3, 1.5e-3, 0.25e-3, 6e-3, base=0.8e-3), tim="direct-to-die")
    out.append(f"JH-R Tier 3 direct-to-die (case = die top, base 0.8 mm, model R''=0 row): avg {r['avg']:.1f} K, max {r['max']:.1f} K.\n")

    # detail of nominal
    rr = plate_eval(JH_R, tim="PCM pad")
    c = JH_R.cell(j_of(18))
    out.append(f"JH-R Tier-1 detail: Vj {c['Vj']:.2f} m/s in the gaps (lamina slot {c['V_slot']:.2f} m/s, Re_slot {c['Re_slot']:.0f}), "
               f"u_ch {c['u_ch']:.3f} m/s (Re {c['Re_ch']:.0f}), impingement fraction of cell {c['f1']:.2f}, "
               f"h_stag {c['h_st']/1e3:.0f} / h_desc {c['h_desc']/1e3:.0f} / h_ch {c['h_ch']/1e3:.1f} kW/m2K, eta {c['eta']:.2f}, "
               f"h_eff {c['h_eff']/1e3:.0f} kW/m2K (open-slot ref {c['h_eff_ref']/1e3:.0f}, gain {c['gain']:.2f}); "
               f"NTU {rr['NTU']:.2f}; core dP {c['dp_core']/1e3:.2f} kPa (nozzle {c['dp_noz']/1e3:.2f}); "
               f"plate {rr['dp']/1e3:.1f} kPa; branch/header-head ratio {rr['ratio_head']:.1f}.\n")

    # flow sweep
    out.append("### C2. Flow sweep (15 kW, PCM): JH-R vs HMMC-R\n")
    out.append("| LPM/kW | LPM | JH-R Vj | JH-R avg | max | dP kPa | pump W | HMMC-R avg | max | dP kPa | pump W | JH-X avg | dP kPa |")
    out.append("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for lk in (0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.4):
        a = plate_eval(JH_R, lpm_per_kw=lk)
        h = hmmc_eval("R", "PCM pad", lpm_per_kw=lk)
        x = plate_eval(JH_X, lpm_per_kw=lk, screen_kPa=0.10)
        out.append(f"| {lk:.1f} | {a['lpm']:.0f} | {a['Vj']:.2f} | {a['avg']:.1f} | {a['max']:.1f} | {a['dp']/1e3:.1f} | {a['pump']:.1f} | "
                   f"{h['dT_avg']:.1f} | {h['dT_max']:.1f} | {h['dp_total_kPa']:.1f} | {h['pump_W']:.1f} | {x['avg']:.1f} | {x['dp']/1e3:.1f} |")
    out.append("")
    # equal pumping power
    out.append("### C3. Equal pumping power and equal dP comparisons (15 kW, PCM)\n")
    for target_W, label in ((1.8, "HMMC-R hydraulic power at 18 LPM (1.8 W)"), (6.5, "CoolIT-like at 18 LPM (6.5 W)")):
        def find(f):
            lo, hi = 0.2, 4.0
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if f(mid) > target_W:
                    hi = mid
                else:
                    lo = mid
            return 0.5 * (lo + hi)
        lkj = find(lambda lk: plate_eval(JH_R, lpm_per_kw=lk)["pump"])
        lkh = find(lambda lk: hmmc_eval("R", "PCM pad", lpm_per_kw=lk)["pump_W"])
        a = plate_eval(JH_R, lpm_per_kw=lkj)
        h = hmmc_eval("R", "PCM pad", lpm_per_kw=lkh)
        out.append(f"- at {label}: JH-R runs {a['lpm']:.1f} LPM -> {a['avg']:.1f} / {a['max']:.1f} K ({a['dp']/1e3:.1f} kPa); "
                   f"HMMC-R runs {h['flow_lpm']:.1f} LPM -> {h['dT_avg']:.1f} / {h['dT_max']:.1f} K ({h['dp_total_kPa']:.1f} kPa).")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------
# D. Real package: 4 reticle dies 350 W/cm2 + 16 HBM, heat-proportional zoning
# ---------------------------------------------------------------------------------------------
def die_zone(core: SlotJetFin, j_die, P_r_die, w_n_die):
    c = SlotJetFin(core.name + "-die", core.b, core.t, core.H, w_n_die, P_r_die, w_r=0.8e-3,
                   base=core.base).cell(j_die)
    return c


def hot_die_dT(h_eff, R_tim, cal_die=6.7, q=350e4, base=1.0e-3, extra=0.0):
    return cal_die + q * base / K_CU + q * R_tim * 1e-4 + q / h_eff + extra


def section_D():
    out = ["## D. Real 2027-28 package: 4 x 26 x 33 mm dies at 350 W/cm2 + 16 HBM at 40 W/cm2 (12.85 kW, 15.4 LPM)\n",
           "Heat-proportional zoning (die block 91 % of flow, j_die = 3.0 x 2.19 = 6.6 cm/s), base 1.0 mm. Hottest-die case-to-inlet = "
           "caloric 6.7 + base 9.0 + TIM + q/h_eff_die (the nonuniform-heatmap fit dT = 33 + 3500/h_eff + 350(R_TIM - 0.05) "
           "reproduces HMMC-R 60.5/48.3 K). Nozzle zoning: equal nozzle dP in all zones, so die-zone jets run at the same "
           "velocity with ~3x the nozzle open area (shorter row pitch), HBM zone uses sparse 0.5 mm round orifices at the same dP.\n",
           "| core (die zone) | P_r mm | w_n mm | Vj m/s | u_ch m/s | h_eff die kW/m2K | open-slot ref | paste 0.05 | PCM 0.055 | LM 0.015 | T_case,max LM (1.0 mm base) | T_case,max LM (0.8 mm finished base) |",
           "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    j_die = 3.0 * j_of(15.4)
    res = {}
    for core, P_r, w_n in ((JH_R, 8.0e-3, 0.50e-3), (JH_R, 6.0e-3, 0.42e-3), (JH_R, 4.0e-3, 0.28e-3), (JH_X, 6.0e-3, 0.47e-3), (JH_P, 6.0e-3, 0.51e-3), (JH_P, 4.0e-3, 0.34e-3)):
        c = die_zone(core, j_die, P_r, w_n)
        he = c["h_eff"]
        ps = hot_die_dT(he, 0.05)
        pc = hot_die_dT(he, 0.055)
        lm = hot_die_dT(he, 0.015)
        res[(core.name, P_r)] = (he, lm, c)
        lm08 = hot_die_dT(he, 0.015, base=0.8e-3)
        out.append(f"| {core.name} | {P_r*1e3:.1f} | {w_n*1e3:.2f} | {c['Vj']:.2f} | {c['u_ch']:.3f} | **{he/1e3:.0f}** | {c['h_eff_ref']/1e3:.0f} | "
                   f"{ps:.1f} | {pc:.1f} | {lm:.1f} | {T_IN+lm:.1f} C | {T_IN+lm08:.1f} C |")
    for name, he in (("HMMC-R (synthesis)", 127e3), ("HMMC-P (synthesis, <=33 um loops)", 187e3), ("CoolIT-like split-flow", 101e3)):
        out.append(f"| {name} | - | - | - | - | {he/1e3:.0f} | - | {hot_die_dT(he,0.05):.1f} | {hot_die_dT(he,0.055):.1f} | "
                   f"{hot_die_dT(he,0.015):.1f} | {T_IN+hot_die_dT(he,0.015):.1f} C | {T_IN+hot_die_dT(he,0.015,base=0.8e-3):.1f} C |")
    out.append("(CoolIT-like rows in the heatmap report are worse than this fit because its fluid under the die is "
               "13.9 K, not 6.7 K: 88.6 K with paste, ~76 K with LM.)\n")
    # die-zone dP at 15.4 LPM
    c = res[("JH-R", 6.0e-3)][2]
    out.append(f"Die-zone core dP (JH-R, P_r 6.0 mm): {c['dp_core']/1e3:.2f} kPa (nozzle {c['dp_noz']/1e3:.2f}); the HBM/margin zones are "
               f"orificed to the same branch dP.\n")
    return "\n".join(out), res


# ---------------------------------------------------------------------------------------------
# E. GPU-class plates
# ---------------------------------------------------------------------------------------------
def section_E():
    out = ["## E. GPU-class plates (uniform-footprint convention of model_output section 6, 1.2 LPM/kW, PCM unless noted)\n",
           "| case | footprint cm2 | q W/cm2 | LPM | CoolIT-like avg/max | HMMC-R avg/max | JH-R avg/max | JH-R Vj m/s | JH-R plate dP kPa | JH-R LM avg/max |",
           "|---|---:|---:|---:|---|---|---|---:|---:|---|"]
    for Qk, A, label in ((1.4, 45, "B300-class 1.4 kW"), (2.3, 60, "Rubin 2.3 kW"), (3.6, 80, "Rubin Ultra 3.6 kW")):
        Q = Qk * 1e3
        cl = coolit_like(A).evaluate(Q, 1.2)
        hm = hmmc(A, core="R", tim="PCM pad").evaluate(Q, 1.2)
        # small plates: keep Vj useful by narrowing the nozzle (0.20 mm) and lengthening P_r (8 mm); ports 10 mm-class
        core = SlotJetFin("JH-R small", 0.15e-3, 0.10e-3, 1.5e-3, 0.20e-3, 8e-3)
        jr = plate_eval(core, Q=Q, area=A * 1e-4, tim="PCM pad", screen_kPa=0.4 * (18 / (1.2 * Qk)) ** 0)
        jl = plate_eval(core, Q=Q, area=A * 1e-4, tim="liquid metal")
        out.append(f"| {label} | {A} | {Q/A:.0f} | {1.2*Qk:.2f} | {cl['dT_avg']:.1f}/{cl['dT_max']:.1f} | {hm['dT_avg']:.1f}/{hm['dT_max']:.1f} | "
                   f"{jr['avg']:.1f}/{jr['max']:.1f} | {jr['Vj']:.2f} | {jr['dp']/1e3:.1f} | {jl['avg']:.1f}/{jl['max']:.1f} |")
    out.append("\nAt 1.2 LPM/kW a 2-4 kW plate has 4-10x less flow per unit area than the 15 kW TTV; the jet velocity "
               "collapses (0.1-0.3 m/s at the same nozzle geometry) and the hybrid degenerates to a slot-fed manifold "
               "plate. Re-zoned (all nozzle area over the dies, see D) is where the GPU-class plate gets its jet benefit.\n")
    # Rubin-class die-concentrated: 2 dies 16.5 cm2 at 2.3 kW -> ~120 W/cm2 die avg w/ HBM; 90% flow over dies
    out.append("Die-concentrated GPU plate check (Rubin-class 2.3 kW, 2 reticle dies 16.5 cm2 carrying ~2.0 kW = 121 W/cm2, "
               "90 % of 2.76 LPM over the 17 cm2 die block):")
    j_die = 0.9 * 2.76 / 60e3 / 17e-4
    for name, core, P_r, w_n in (("JH-R", JH_R, 3.0e-3, 0.20e-3), ("open-slot ref", JH_R, 3.0e-3, 0.20e-3)):
        c = SlotJetFin(name, core.b, core.t, core.H, w_n, P_r, w_r=0.8e-3).cell(j_die)
        he = c["h_eff"] if name == "JH-R" else c["h_eff_ref"]
        q = 121e4
        dT_lm = 0.65 * (2.0e3 / (2.76 / 60e3 * rho * cp) / 0.9) + q * 1.0e-3 / K_CU + q * 0.015e-4 + q / he
        dT_pcm = dT_lm - q * 0.015e-4 + q * 0.055e-4
        out.append(f"  - {name}: j_die {j_die*100:.1f} cm/s, Vj {c['Vj']:.2f} m/s, h_eff {he/1e3:.0f} kW/m2K; die case-to-inlet ~{dT_pcm:.1f} K (PCM) / {dT_lm:.1f} K (LM); core dP {c['dp_core']/1e3:.1f} kPa")
    out.append("")
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------
# F. Monte Carlo
# ---------------------------------------------------------------------------------------------
def section_F(n=20000, seed=7):
    random.seed(seed)
    out = ["## F. Monte Carlo (20k samples), JH-R at 15 kW / 18 LPM\n",
           "h_eff: jet-model uncertainty (enhancement-region terms x lognormal sigma 0.30) and channel term +/-25 %; "
           "TIM lognormal with P90 at the upper datasheet value; base +/-10 %; caloric +/-5 %; hot-spot terms +/-40 %; "
           "dP: nozzle/inertial +/-45 %, viscous +/-25 %, plumbing +/-30 %.\n",
           "| design | avg P10 / P50 / P90 K | max P10 / P50 / P90 K | dP P10 / P50 / P90 kPa | Q cap P10 / P50 / P90 kW |",
           "|---|---|---|---|---|"]
    results = {}
    for tim in ("paste 0.07", "PCM pad", "liquid metal"):
        A, M, D, QC = [], [], [], []
        base_r = plate_eval(JH_R, tim=tim)
        c = JH_R.cell(j_of(18))
        R_nom, sc = TIM[tim]
        R_p90 = {"paste 0.07": 0.12, "PCM pad": 0.08, "liquid metal": 0.03}[tim]
        sig_tim = math.log(R_p90 / R_nom) / 1.2816
        for _ in range(n):
            f_jet = math.exp(random.gauss(0, 0.30))
            f_ch = 1 + random.gauss(0, 0.25 / 1.645)
            # rebuild h_eff with perturbed region h's
            h_fin = c["f1"] * c["h_desc"] * f_jet + (1 - c["f1"]) * c["h_ch"] * f_ch
            h_base = c["f1"] * c["h_st"] * f_jet + (1 - c["f1"]) * c["h_ch"] * f_ch
            m = math.sqrt(2 * max(h_fin, 1) / (K_CU * JH_R.t))
            eta = math.tanh(m * JH_R.H) / (m * JH_R.H)
            he = (h_fin * 2 * JH_R.H * eta + h_base * JH_R.b) / c["p"]
            q = Q0 / A_FP
            mdot = 18 / 60e3 * rho
            dT_out = Q0 / (mdot * cp)
            NTU = he * A_FP / (mdot * cp)
            cal = dT_out * (1 / (1 - math.exp(-NTU)) - 1 / NTU) * (1 + random.gauss(0, 0.05 / 1.645))
            Rt = R_nom * math.exp(random.gauss(0, sig_tim))
            tim_dT = q * Rt * 1e-4
            base = q * JH_R.base / K_CU * (1 + random.gauss(0, 0.10 / 1.645))
            conv = q / he
            avg = cal + tim_dT + base + conv
            hs = (1.5 + sc) * max(0.2, 1 + random.gauss(0, 0.40 / 1.645))
            mx = avg + hs
            dp = (c["dp_noz"] * max(0.3, 1 + random.gauss(0, 0.45 / 1.645)) + (c["dp_ch"] + c["dp_ret"]) * (1 + random.gauss(0, 0.25 / 1.645))
                  + (PLUMB_18["ports"] + PLUMB_18["manifold"] + 400) * (1 + random.gauss(0, 0.30 / 1.645)))
            flux = tim_dT + base + conv
            qc = Q0 * (85 - T_IN - cal - hs) / flux / 1e3
            A.append(avg); M.append(mx); D.append(dp / 1e3); QC.append(qc)

        def pct(v, p):
            v = sorted(v)
            return v[int(p * (len(v) - 1))]
        results[tim] = dict(avg=(pct(A, .1), pct(A, .5), pct(A, .9)), max=(pct(M, .1), pct(M, .5), pct(M, .9)),
                            dp=(pct(D, .1), pct(D, .5), pct(D, .9)), qc=(pct(QC, .9), pct(QC, .5), pct(QC, .1)))
        r = results[tim]
        out.append(f"| JH-R, {tim} | {r['avg'][0]:.1f} / {r['avg'][1]:.1f} / {r['avg'][2]:.1f} | {r['max'][0]:.1f} / {r['max'][1]:.1f} / {r['max'][2]:.1f} | "
                   f"{r['dp'][0]:.1f} / {r['dp'][1]:.1f} / {r['dp'][2]:.1f} | {r['qc'][0]:.1f} / {r['qc'][1]:.1f} / {r['qc'][2]:.1f} |")
    out.append("(Q cap column ordered pessimistic / median / optimistic.)\n")
    return "\n".join(out), results


# ---------------------------------------------------------------------------------------------
# G. Scorecard extras
# ---------------------------------------------------------------------------------------------
def section_G():
    out = ["## G. Scorecard extras (JH-R unless noted)\n"]
    for tim in ("PCM pad", "liquid metal"):
        r36 = plate_eval(JH_R, lpm_per_kw=2.4, tim=tim)
        r36b = plate_eval(JH_R, lpm_per_kw=2.4, tim=tim, ports_mm=20.0)
        out.append(f"- 36 LPM ({tim}): avg {r36['avg']:.1f} K / max {r36['max']:.1f} K, Vj {r36['Vj']:.2f} m/s, dP {r36['dp']/1e3:.1f} kPa (16 mm ports) "
                   f"/ {r36b['dp']/1e3:.1f} kPa (20 mm ports), pump {r36['pump']:.1f} / {r36b['pump']:.1f} W")
    r18b = plate_eval(JH_R, tim="PCM pad", ports_mm=20.0)
    out.append(f"- 18 LPM with 20 mm ports: dP {r18b['dp']/1e3:.1f} kPa, pump {r18b['pump']:.1f} W")
    # flow for CoolIT's 34.4 K average
    for tim in ("PCM pad", "liquid metal", "paste 0.07"):
        lo, hi = 0.2, 2.0
        for _ in range(60):
            mid = 0.5 * (lo + hi)
            if plate_eval(JH_R, lpm_per_kw=mid, tim=tim)["avg"] > 34.4:
                lo = mid
            else:
                hi = mid
        r = plate_eval(JH_R, lpm_per_kw=hi, tim=tim)
        out.append(f"- flow for 34.4 K average ({tim}): {r['lpm']:.1f} LPM ({hi:.2f} LPM/kW), dP {r['dp']/1e3:.1f} kPa, pump {r['pump']:.2f} W, Vj {r['Vj']:.2f} m/s")
    for tim in ("paste 0.07", "PCM pad", "liquid metal"):
        r = plate_eval(JH_R, tim=tim)
        out.append(f"- inlet allowed for T_case,max 85 C at 15 kW / 18 LPM ({tim}): {85 - r['max']:.1f} C; T_case,max at 45 C inlet {r['Tcmax']:.1f} C")
    # CoolIT 4 kW plate: 50 x 50 mm, < 0.009 C/W max-case incl. TIM at 6 LPM
    out.append("- CoolIT 4 kW plate comparison (50 x 50 mm, 4 kW, 6 LPM, PG25 45 C; CoolIT < 0.009 C/W max-case incl. TIM):")
    small = SlotJetFin("JH-R 50mm", 0.15e-3, 0.10e-3, 2.0e-3, 0.22e-3, 8e-3)
    for tim in ("paste 0.07", "PCM pad", "liquid metal"):
        r = plate_eval(small, Q=4000.0, lpm_per_kw=1.5, tim=tim, area=25e-4, screen_kPa=0.4 * (6 / 18) ** 0)
        out.append(f"    - JH-R {tim}: avg {r['avg']:.1f} K, max {r['max']:.1f} K -> {r['max']/4000:.4f} C/W max-case; Vj {r['Vj']:.2f} m/s; core dP {r['dp_core']/1e3:.2f} kPa")
    # die-concentrated GPU-class plates (90 % of flow over the die block; 1.2 LPM/kW)
    out.append("\n### G2. Die-concentrated GPU-class plates (1.2 LPM/kW, 90 % of flow over the die block, base 1.0 mm)\n")
    out.append("| device (assumed) | Q kW | die block cm2 | die W/cm2 | LPM | Vj m/s | JH-R h_eff | open-slot ref h_eff | JH-R die case-to-inlet PCM / LM K | ref PCM / LM K | JH-R gain K |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---|---|---:|")
    for label, Q, Qdie, Adie, P_r, w_n in (("B300-class (2 dies)", 1.4e3, 1.2e3, 17e-4, 4e-3, 0.15e-3),
                                           ("Rubin-class (2 dies)", 2.3e3, 2.0e3, 17e-4, 4e-3, 0.20e-3),
                                           ("Rubin-Ultra-class (4 dies)", 3.6e3, 3.2e3, 35e-4, 4e-3, 0.20e-3),
                                           ("15 kW-class (4 dies, 350 W/cm2)", 12.85e3, 12.0e3, 35.5e-4, 4e-3, 0.28e-3)):
        lpm = 1.2 * Q / 1e3
        mdot = lpm / 60e3 * rho
        j_die = 0.9 * lpm / 60e3 / Adie
        c = SlotJetFin(label, 0.15e-3, 0.10e-3, 2.0e-3, w_n, P_r, w_r=0.8e-3).cell(j_die)
        q = Qdie / Adie
        dT_out = Qdie / (0.9 * mdot * cp)
        res = []
        for he in (c["h_eff"], c["h_eff_ref"]):
            NTU = he * Adie / (0.9 * mdot * cp)
            cal = dT_out * (1 / (1 - math.exp(-NTU)) - 1 / NTU)
            core_dT = cal + q * 1.0e-3 / K_CU + q / he + 1.5
            res.append((core_dT + q * 0.055e-4 + 1.5 * q / 1.28e6, core_dT + q * 0.015e-4 + 0.6 * q / 1.28e6))
        out.append(f"| {label} | {Q/1e3:.2f} | {Adie*1e4:.0f} | {q/1e4:.0f} | {lpm:.2f} | {c['Vj']:.2f} | {c['h_eff']/1e3:.0f} | {c['h_eff_ref']/1e3:.0f} | "
                   f"{res[0][0]:.1f} / {res[0][1]:.1f} | {res[1][0]:.1f} / {res[1][1]:.1f} | {res[1][0]-res[0][0]:.1f} |")
    out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    print("# Jet-hybrid scoping model output (jet_hybrid_model.py)\n")
    print(f"PG25 ~50 C: nu {nu:.3e} m2/s, Pr {Pr:.2f}; j = {j_of(18)*100:.2f} cm/s at 18 LPM, {j_of(36)*100:.2f} at 36 LPM over 117 cm2\n")
    print(section_A())
    sB, _ = section_B()
    print(sB)
    print(section_C())
    sD, _ = section_D()
    print(sD)
    print(section_E())
    sF, _ = section_F()
    print(sF)
    print(section_G())
