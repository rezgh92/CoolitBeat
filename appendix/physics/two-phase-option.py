#!/usr/bin/env python3
"""
two-phase-option.py  --  Should the HMMC cold-plate architecture carry a flow-boiling variant?

Scoping calculation (+/-30 % per term, correlations extrapolated where flagged) for the SAME
HMMC core used in the single-phase architecture:
    Cu fins 0.1 mm / gaps 0.1 mm / 1.0 mm tall, 2 mm flow length between inlet and return slots,
    1 mm base, 117 cm2 (108 x 108 mm) heated footprint, 15 kW (128 W/cm2) .. 35 kW (300 W/cm2).

Fluids: R1233zd(E), R515B, Novec 7000 (HFE-7000), Novec 7100 (HFE-7100), properties at Tsat ~ 60 C.
NOTE: web verification of properties was not possible in this run (search budget exhausted);
values are from memory of REFPROP / manufacturer tables, +/-10 %.

Computes, per fluid and heat load:
  * required refrigerant mass flow / liquid LPM / channel mass flux for a chosen exit quality
  * saturation temperature forced by a 45 C facility-water condenser (isothermal pinch)
  * flow-boiling HTC by three correlations (Cooper nucleate; Bertsch-Groll-Garimella 2009;
    Kandlikar-Balasubramanian 2004 laminar NBD branch) -> fin efficiency -> conv term
  * CHF by Katto-Ohno 1984, Qu-Mudawar 2004 (extrapolated), Bowers-Mudawar 1994 (extrapolated),
    and the hard energy-balance (x = 1) cap; dryout-quality margin
  * two-phase pressure drop: Lockhart-Martinelli (laminar-laminar, C = 5) + acceleration +
    return-slot + return-manifold + vapour port, versus the single-phase HMMC estimate
  * case-to-45C temperature budget versus single-phase HMMC (paste and liquid-metal TIM),
    15 kW and 30 kW, and the footprint-flux crossover where boiling starts to pay.
"""
from __future__ import annotations
import math, sys
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
from coldplate_model import hmmc_design, PG25, K_CU  # our own 1-D model (trusted repo code)

# ----------------------------------------------------------------------------------------------
# Refrigerant properties at Tsat ~ 60 C (saturated).  Psat55 = saturation pressure at 55 C.
# ----------------------------------------------------------------------------------------------
FLUIDS = {
    # name: dict(M g/mol, Tc C, Pc MPa, Psat60 MPa, Psat55 MPa, rho_l, rho_v, hfg J/kg, cp_l, k_l, mu_l, mu_v, sigma, GWP, status)
    "R1233zd(E)": dict(M=130.5, Tc=166.5, Pc=3.62, Psat60=0.385, Psat55=0.33, rho_l=1195.0, rho_v=19.5,
                       hfg=172e3, cp_l=1300.0, k_l=0.072, mu_l=0.30e-3, mu_v=11.8e-6, sigma=0.0115,
                       GWP="1 (AR5) / 3.7 (AR6), ODP 0.0003", status="HCFO, A1, in production (Honeywell/Arkema/Chinese); PFAS-restriction scope"),
    "R515B":      dict(M=117.5, Tc=108.7, Pc=3.56, Psat60=1.17, Psat55=1.03, rho_l=1040.0, rho_v=62.0,
                       hfg=128e3, cp_l=1500.0, k_l=0.063, mu_l=0.145e-3, mu_v=13.5e-6, sigma=0.0055,
                       GWP="~299 (AR4), contains 8.9 % R227ea (HFC)", status="HFO/HFC blend, A1; HFC content inside EU quota; 11-12 bar at 60 C"),
    "Novec 7000": dict(M=200.0, Tc=165.0, Pc=2.48, Psat60=0.24, Psat55=0.20, rho_l=1325.0, rho_v=17.5,
                       hfg=125e3, cp_l=1350.0, k_l=0.068, mu_l=0.30e-3, mu_v=12.0e-6, sigma=0.0095,
                       GWP="~530", status="HFE; 3M exited PFAS manufacture end-2025 -> supply ending; PFAS scope"),
    "Novec 7100": dict(M=250.0, Tc=195.0, Pc=2.23, Psat60=0.097, Psat55=0.082, rho_l=1430.0, rho_v=8.8,
                       hfg=112e3, cp_l=1250.0, k_l=0.062, mu_l=0.37e-3, mu_v=11.0e-6, sigma=0.0105,
                       GWP="~320", status="HFE; sub-atmospheric at 55 C (air ingress); 3M exit; PFAS scope"),
}

# ----------------------------------------------------------------------------------------------
# HMMC core geometry (identical to the single-phase architecture)
# ----------------------------------------------------------------------------------------------
A_FP = 117e-4          # m2 heated footprint
W = math.sqrt(A_FP)    # 0.108 m square
b, t, H, L, base = 0.10e-3, 0.10e-3, 1.0e-3, 2.0e-3, 1.0e-3
slot_w = 0.30e-3
pitch = b + t
n_across = W / pitch                   # channels across the plate (~540)
n_seg = W / L                          # 2 mm segments along each channel (~54)
N_SEG = n_across * n_seg               # parallel 2-mm boiling segments (~29,000)
A_FLOW = N_SEG * b * H                 # total channel cross-section (m2)
Dh = 2 * b * H / (b + H)
AR_RAW = (2 * H + b) / pitch           # wetted/footprint area ratio before fin efficiency
n_slots = round(W / (2 * L))           # inlet slots (27); same number of return slots
HOTSPOT_K = 4.0                        # same local hotspot penalty as the single-phase model
T_FW = 45.0                            # facility / benchmark inlet water, C
PINCH_K = 3.0                          # CDU condenser pinch (refrigerant Tsat - water outlet)
TIM = {"paste (thin BLT)": 0.05e-4, "liquid metal": 0.015e-4}   # m2K/W

def fin_eff(h: float) -> tuple[float, float]:
    m = math.sqrt(2 * h / (K_CU * t))
    eta = math.tanh(m * H) / (m * H)
    return eta, (2 * H * eta + b) / pitch

# ----------------------------------------------------------------------------------------------
# Boiling HTC correlations (all on wetted-wall heat flux q_w, W/m2)
# ----------------------------------------------------------------------------------------------
def h_cooper(f, q_w, Pr_red, Rp_um=1.0):
    """Cooper (1984) nucleate pool boiling; Rp = surface roughness in um (0.4-1 for machined Cu)."""
    return 55.0 * Pr_red ** (0.12 - 0.2 * math.log10(Rp_um)) * (-math.log10(Pr_red)) ** -0.55 \
        * f["M"] ** -0.5 * q_w ** 0.67

def h_hausen(k, mu, cp, G):
    """Hausen developing laminar flow in a duct of length L, used by Bertsch et al. (2009)."""
    Re = G * Dh / mu
    Pr = cp * mu / k
    Gz = (Dh / L) * Re * Pr
    Nu = 3.66 + 0.0668 * Gz / (1 + 0.04 * Gz ** (2 / 3))
    return Nu * k / Dh

def h_bertsch(f, q_w, G, x, Pr_red):
    """Bertsch, Groll & Garimella (2009) composite microchannel flow-boiling correlation."""
    Co_conf = math.sqrt(f["sigma"] / (9.81 * (f["rho_l"] - f["rho_v"]))) / Dh   # confinement number
    h_nb = h_cooper(f, q_w, Pr_red)
    cp_v = 0.75 * f["cp_l"]   # vapour cp approx (only enters through tiny x*h_v term)
    h_l = h_hausen(f["k_l"], f["mu_l"], f["cp_l"], G)
    h_v = h_hausen(0.014, f["mu_v"], cp_v, G)
    h_conv = h_l * (1 - x) + h_v * x
    return h_nb * (1 - x) + h_conv * (1 + 80 * (x ** 2 - x ** 6) * math.exp(-0.6 * Co_conf))

def h_kandlikar(f, q_w, G, x, F_fl=1.0):
    """Kandlikar & Balasubramanian (2004) microchannel form, laminar liquid-only (Re_lo < 100 -> NBD only).
    F_fl (fluid-surface parameter) is unknown for these fluids; 1.0 assumed (1.3-1.6 for R134a-class)."""
    Re_lo = G * Dh / f["mu_l"]
    Nu_lo = 5.4   # laminar rectangular duct, aspect 0.1, 3-side heating (Shah & London)
    h_lo = Nu_lo * f["k_l"] / Dh
    Co = (f["rho_v"] / f["rho_l"]) ** 0.5 * ((1 - x) / x) ** 0.8
    Bo = q_w / (G * f["hfg"])
    h_nbd = 0.6683 * Co ** -0.2 * (1 - x) ** 0.8 * h_lo + 1058 * Bo ** 0.7 * (1 - x) ** 0.8 * F_fl * h_lo
    h_cbd = 1.136 * Co ** -0.9 * (1 - x) ** 0.8 * h_lo + 667.2 * Bo ** 0.7 * (1 - x) ** 0.8 * F_fl * h_lo
    return h_nbd if Re_lo < 100 else max(h_nbd, h_cbd), Re_lo

# ----------------------------------------------------------------------------------------------
# CHF correlations (wetted-wall basis)
# ----------------------------------------------------------------------------------------------
def chf_katto_ohno(f, G, dh_sub=0.0):
    rr = f["rho_v"] / f["rho_l"]
    LD = L / Dh
    We = G ** 2 * L / (f["sigma"] * f["rho_l"])
    Ghfg = G * f["hfg"]
    C = 0.25 if LD < 50 else (0.25 + 0.0009 * (LD - 50) if LD <= 150 else 0.34)
    q1 = C * Ghfg * We ** -0.043 / LD
    q2 = 0.10 * Ghfg * rr ** 0.133 * We ** (-1 / 3) / (1 + 0.0031 * LD)
    q3 = 0.098 * Ghfg * rr ** 0.133 * We ** -0.433 * LD ** 0.27 / (1 + 0.0031 * LD)
    q4 = 0.0384 * Ghfg * rr ** 0.60 * We ** -0.173 / (1 + 0.280 * We ** -0.233 * LD)
    q5 = 0.234 * Ghfg * rr ** 0.513 * We ** -0.433 * LD ** 0.27 / (1 + 0.0031 * LD)
    K1 = 1.043 / (4 * C * We ** -0.043)
    K2 = (5 / 6) * (0.0124 + 1 / LD) * rr ** -0.133 * We ** (-1 / 3)
    K3 = 1.12 * (1.52 * We ** -0.233 + 1 / LD) * rr ** 0.6 * We ** -0.173
    if rr < 0.15:
        qco = q1 if q1 < q2 else (q2 if q2 < q3 else q3)
        K = K1 if K1 > K2 else K2
        regime = "L-regime (x->1 energy limit)" if q1 < q2 else "H/N-regime"
    else:
        qco = q1 if q1 < q5 else (q5 if q5 > q4 else q4)
        K = K1 if K1 > K2 else (K2 if K2 < K3 else K3)
        regime = "L-regime" if q1 < q5 else "HP-regime"
    return qco * (1 + K * dh_sub / f["hfg"]), regime, We

def chf_qu_mudawar(f, G):
    We = G ** 2 * L / (f["rho_l"] * f["sigma"])
    return 33.43 * G * f["hfg"] * (f["rho_v"] / f["rho_l"]) ** 1.11 * We ** -0.21 * (L / Dh) ** -0.36

def chf_bowers_mudawar(f, G):
    We = G ** 2 * L / (f["rho_l"] * f["sigma"])
    return 0.16 * G * f["hfg"] * We ** -0.19 * (L / Dh) ** -0.54

def q_w_energy_cap(f, G, x_in=0.0):
    """Wetted flux at which the segment exit quality reaches 1 (hard physical cap)."""
    return G * b * H * f["hfg"] * (1 - x_in) / ((2 * H + b) * L)

# ----------------------------------------------------------------------------------------------
# Two-phase pressure drop
# ----------------------------------------------------------------------------------------------
def fRe_rect(alpha):
    return 24 * (1 - 1.3553 * alpha + 1.9467 * alpha ** 2 - 1.7012 * alpha ** 3 + 0.9564 * alpha ** 4 - 0.2537 * alpha ** 5)

def dp_two_phase(f, G, x_out, x_in=0.0, n=40):
    """Core: Lockhart-Martinelli separated flow, laminar-laminar C = 5, x linear along L; Zivi void for
    acceleration; return slot and return manifold on homogeneous mixture; vapour-return port sized for 12 m/s."""
    alpha_g = min(b, H) / max(b, H)
    fRe = fRe_rect(alpha_g)
    xs = np.linspace(x_in, x_out, n + 1)
    dz = L / n
    dp_fric = 0.0
    for i in range(n):
        x = 0.5 * (xs[i] + xs[i + 1])
        x = max(x, 1e-6)
        Gl, Gv = G * (1 - x), G * x
        Re_l = Gl * Dh / f["mu_l"]
        Re_v = Gv * Dh / f["mu_v"]
        dpdz_l = fRe / max(Re_l, 1e-9) * Gl ** 2 / (2 * f["rho_l"] * Dh)      # laminar liquid alone
        dpdz_v = fRe / max(Re_v, 1e-9) * Gv ** 2 / (2 * f["rho_v"] * Dh)      # laminar vapour alone
        X2 = dpdz_l / max(dpdz_v, 1e-12)
        X = math.sqrt(X2)
        C = 5.0 if (Re_l < 2000 and Re_v < 2000) else 12.0
        phi_l2 = 1 + C / X + 1 / X2
        dp_fric += phi_l2 * dpdz_l * dz
    S = (f["rho_l"] / f["rho_v"]) ** (1 / 3)                              # Zivi slip
    def spec_vol(x):
        if x <= 0:
            return 1 / f["rho_l"]
        a = 1 / (1 + ((1 - x) / x) * (f["rho_v"] / f["rho_l"]) * S)
        return x ** 2 / (f["rho_v"] * a) + (1 - x) ** 2 / (f["rho_l"] * (1 - a))
    dp_acc = G ** 2 * (spec_vol(x_out) - spec_vol(x_in))
    rho_h = 1 / (x_out / f["rho_v"] + (1 - x_out) / f["rho_l"])          # homogeneous mixture at exit
    mdot = G * A_FLOW
    Vmix = mdot / rho_h
    u_slot = Vmix / (n_slots * W * slot_w)
    dp_slot = 1.5 * 0.5 * rho_h * u_slot ** 2
    u_man = 5.0                                                          # design mixture velocity in return headers
    dp_man = 4.0 * 0.5 * rho_h * u_man ** 2
    A_man = Vmix / u_man
    u_port = 12.0
    d_port = math.sqrt(4 * Vmix / (math.pi * u_port))
    dp_port = 1.5 * 0.5 * rho_h * u_port ** 2
    dp_inlet_liq = 2.0e3                                                 # liquid inlet slots + port + inlet-orifice throttling (design choice)
    total = dp_fric + dp_acc + dp_slot + dp_man + dp_port + dp_inlet_liq
    return dict(dp_fric=dp_fric, dp_acc=dp_acc, dp_slot=dp_slot, dp_man=dp_man, dp_port=dp_port,
                dp_inlet=dp_inlet_liq, total=total, rho_h=rho_h, Vmix_lpm=Vmix * 6e4, u_slot=u_slot,
                A_man_cm2=A_man * 1e4, d_port_mm=d_port * 1e3, pump_W=total * mdot / f["rho_l"])

# ----------------------------------------------------------------------------------------------
# Two-phase cold-plate evaluation
# ----------------------------------------------------------------------------------------------
def evaluate_2phase(fname, Q, Tsat, x_out=0.3, dT_sub=3.0, tim="paste (thin BLT)", htc="cooper"):
    f = FLUIDS[fname]
    q_fp = Q / A_FP
    Pr_red = (f["Psat60"] if Tsat >= 58 else f["Psat55"]) / f["Pc"]
    mdot = Q / (x_out * f["hfg"] + f["cp_l"] * dT_sub)
    G = mdot / A_FLOW
    lpm = mdot / f["rho_l"] * 6e4
    x_mean = 0.5 * x_out
    # solve wetted flux with fin efficiency coupled to the chosen HTC
    def resid(q_w):
        if htc == "cooper":
            h = h_cooper(f, q_w, Pr_red)
        elif htc == "enhanced":
            h = 2.5 * h_cooper(f, q_w, Pr_red)
        elif htc == "bertsch":
            h = h_bertsch(f, q_w, G, x_mean, Pr_red)
        else:
            h = h_kandlikar(f, q_w, G, x_mean)[0]
        eta, ar = fin_eff(h)
        return q_w - q_fp / ar
    q_w = brentq(resid, 1e3, 5e6)
    if htc == "cooper":
        h = h_cooper(f, q_w, Pr_red)
    elif htc == "enhanced":
        h = 2.5 * h_cooper(f, q_w, Pr_red)
    elif htc == "bertsch":
        h = h_bertsch(f, q_w, G, x_mean, Pr_red)
    else:
        h = h_kandlikar(f, q_w, G, x_mean)[0]
    eta, ar = fin_eff(h)
    h_eff = h * ar
    dT_conv = q_fp / h_eff
    dT_tim = q_fp * TIM[tim]
    dT_base = q_fp * base / K_CU
    dT_sat_shift = Tsat - T_FW
    dT_avg = dT_sat_shift + dT_tim + dT_base + dT_conv
    # CHF
    dh_sub = f["cp_l"] * dT_sub
    q_ko, regime, We = chf_katto_ohno(f, G, dh_sub)
    q_qm = chf_qu_mudawar(f, G)
    q_bm = chf_bowers_mudawar(f, G)
    q_cap = q_w_energy_cap(f, G)
    q_dry = q_cap * 0.6          # dryout assumed at x ~ 0.6 for G ~ 100-300 in microchannels (literature band 0.5-0.9)
    dp = dp_two_phase(f, G, x_out)
    return dict(fluid=fname, Q=Q, Tsat=Tsat, q_fp=q_fp / 1e4, mdot=mdot, G=G, lpm=lpm, lpm_per_kw=lpm / (Q / 1e3),
                x_out=x_out, q_w=q_w / 1e4, h=h / 1e3, eta=eta, ar=ar, h_eff=h_eff / 1e3,
                dT_sat=dT_sat_shift, dT_tim=dT_tim, dT_base=dT_base, dT_conv=dT_conv, dT_avg=dT_avg,
                dT_max=dT_avg + HOTSPOT_K, Pr_red=Pr_red, We=We,
                chf_ko=q_ko / 1e4, chf_regime=regime, chf_qm=q_qm / 1e4, chf_bm=q_bm / 1e4, q_cap=q_cap / 1e4,
                q_dry=q_dry / 1e4, margin_dry=q_dry / q_w, margin_cap=q_cap / q_w, dp=dp, tim=tim, htc=htc)

def single_phase(Q, tim_R, label, lpm_kw=1.2):
    cp = hmmc_design(117.0, tim_R=tim_R, tim_label=label)
    return cp.evaluate(Q, lpm_kw, fluid=PG25, T_in=T_FW)

# ----------------------------------------------------------------------------------------------
def main():
    out = []
    P = out.append
    P("# Two-phase (flow boiling) option for the HMMC core -- script output\n")
    P(f"HMMC core: b={b*1e3:.2f} mm, t={t*1e3:.2f} mm, H={H*1e3:.1f} mm, L={L*1e3:.1f} mm, Dh={Dh*1e6:.0f} um, "
      f"L/Dh={L/Dh:.1f}, segments={N_SEG:.0f}, flow area={A_FLOW*1e4:.2f} cm2, raw area ratio={AR_RAW:.1f}, "
      f"inlet/return slots={n_slots} each\n")

    # 1. Tsat forced by the condenser
    P("## 1. Saturation temperature forced by a 45 C facility-water condenser (isothermal pinch 3 K)")
    P("| facility flow LPM/kW | coolant | water rise K | Tsat required C |")
    P("|---:|---|---:|---:|")
    for lk in (1.0, 1.2, 1.5, 2.0, 2.5, 3.0):
        for nm, rho, cp in (("PG25", 1005.0, 3930.0), ("water", 988.0, 4181.0)):
            rise = 1e3 / (lk / 6e4 * rho * cp)       # per kW: Q=1000 W, flow = lk LPM
            P(f"| {lk:.1f} | {nm} | {rise:.1f} | {T_FW + rise + PINCH_K:.1f} |")
    P("Single-phase comparison basis: benchmark plate inlet 45 C (CoolIT TTV); 'system basis' adds a 3 K liquid-liquid CDU approach (48 C).\n")

    # 2. Flow, quality, mass flux
    P("## 2. Refrigerant flow for x_out = 0.2-0.5 (15 kW; 3 K inlet subcooling)")
    P("| fluid | x_out | mdot kg/s | liquid LPM | LPM/kW | G kg/m2s | Re_lo | vapour+liquid at exit LPM |")
    P("|---|---:|---:|---:|---:|---:|---:|---:|")
    for fname in FLUIDS:
        f = FLUIDS[fname]
        for xo in (0.2, 0.3, 0.4, 0.5):
            r = evaluate_2phase(fname, 15e3, 60.0, x_out=xo)
            Re_lo = r["G"] * Dh / f["mu_l"]
            P(f"| {fname} | {xo:.1f} | {r['mdot']:.3f} | {r['lpm']:.1f} | {r['lpm_per_kw']:.2f} | {r['G']:.0f} | {Re_lo:.0f} | {r['dp']['Vmix_lpm']:.0f} |")
    P("Single-phase PG25 reference: 18 LPM (1.2 LPM/kW), G = 103 kg/m2s, Re = 15 in the same channels.\n")

    # 3. HTC by correlation, 15 kW and 30 kW, R1233zd(E)
    P("## 3. Flow-boiling HTC and convective term (x_out = 0.3, Tsat 60 C, paste TIM)")
    P("| fluid | Q kW | q_fp W/cm2 | q_w W/cm2 | h Cooper | h Bertsch | h Kandlikar(F=1) | eta (Cooper) | h_eff kW/m2K | conv K (Cooper) | conv K (Bertsch) | conv K (Kandlikar) | SP PG25 conv K |")
    P("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for fname in FLUIDS:
        for Q in (15e3, 30e3, 35e3):
            rc = evaluate_2phase(fname, Q, 60.0, htc="cooper")
            rb = evaluate_2phase(fname, Q, 60.0, htc="bertsch")
            rk = evaluate_2phase(fname, Q, 60.0, htc="kandlikar")
            sp = single_phase(Q, 0.05, "paste (thin BLT)")
            P(f"| {fname} | {Q/1e3:.0f} | {rc['q_fp']:.0f} | {rc['q_w']:.1f} | {rc['h']:.1f} | {rb['h']:.1f} | {rk['h']:.1f} | "
              f"{rc['eta']:.2f} | {rc['h_eff']:.0f} | {rc['dT_conv']:.1f} | {rb['dT_conv']:.1f} | {rk['dT_conv']:.1f} | {sp['dT_conv']:.1f} |")
    sp15 = single_phase(15e3, 0.05, "paste (thin BLT)")
    P(f"Single-phase PG25 HMMC at 15 kW: h = {sp15['h']/1e3:.1f} kW/m2K, eta = {sp15['eta']:.2f}, area ratio {sp15['area_ratio']:.1f}, "
      f"h_eff = {sp15['h']*sp15['area_ratio']/1e3:.0f} kW/m2K.\n")

    # 4. CHF
    P("## 4. CHF / dryout margin on the wetted wall (x_out = 0.3 design flow, 3 K subcooling)")
    P("| fluid | q_fp W/cm2 | G | q_w W/cm2 | We_L | Katto-Ohno W/cm2 (regime) | Qu-Mudawar W/cm2* | Bowers-Mudawar W/cm2* | x=1 energy cap W/cm2 | dryout (x~0.6) W/cm2 | margin to dryout | margin to x=1 |")
    P("|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|")
    for fname in FLUIDS:
        for Q in (15e3, 30e3, 35e3):
            r = evaluate_2phase(fname, Q, 60.0)
            P(f"| {fname} | {r['q_fp']:.0f} | {r['G']:.0f} | {r['q_w']:.1f} | {r['We']:.2f} | {r['chf_ko']:.0f} ({r['chf_regime']}) | "
              f"{r['chf_qm']:.0f} | {r['chf_bm']:.0f} | {r['q_cap']:.0f} | {r['q_dry']:.0f} | {r['margin_dry']:.2f} | {r['margin_cap']:.2f} |")
    P("*Qu-Mudawar (valid L/Dh >= 20, We_L >~ 5) and Bowers-Mudawar are extrapolated here and exceed the energy-balance cap -> non-physical; "
      "the binding limit at these low mass fluxes is dryout (quality), i.e. margin = x_dry/x_out ~ 2 at x_out = 0.3.")
    P("Fixed-flow stress test (flow sized for 15 kW at x_out = 0.3, then load raised):")
    P("| fluid | Q kW | x_out at fixed G | dryout? |")
    P("|---|---:|---:|---|")
    for fname in ("R1233zd(E)", "R515B"):
        f = FLUIDS[fname]
        r15 = evaluate_2phase(fname, 15e3, 60.0)
        for Q in (15e3, 20e3, 25e3, 30e3, 35e3):
            xo = (Q - r15["mdot"] * f["cp_l"] * 3.0) / (r15["mdot"] * f["hfg"])
            P(f"| {fname} | {Q/1e3:.0f} | {xo:.2f} | {'YES (x > 0.6)' if xo > 0.6 else ('marginal' if xo > 0.45 else 'no')} |")
    P("")

    # 5. Pressure drop
    P("## 5. Two-phase pressure drop budget (x_out = 0.3, Tsat 60 C)")
    P("| fluid | Q kW | core friction Pa | accel Pa | return slot Pa (u m/s) | return manifold Pa | vapour port Pa (d mm) | liquid inlet+orifice Pa | total kPa | exit mixture LPM | rho_mix kg/m3 | pump W |")
    P("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for fname in FLUIDS:
        for Q in (15e3, 30e3):
            r = evaluate_2phase(fname, Q, 60.0)
            d = r["dp"]
            P(f"| {fname} | {Q/1e3:.0f} | {d['dp_fric']:.0f} | {d['dp_acc']:.0f} | {d['dp_slot']:.0f} ({d['u_slot']:.1f}) | {d['dp_man']:.0f} | "
              f"{d['dp_port']:.0f} ({d['d_port_mm']:.0f}) | {d['dp_inlet']:.0f} | {d['total']/1e3:.1f} | {d['Vmix_lpm']:.0f} | {d['rho_h']:.0f} | {d['pump_W']:.1f} |")
    sp30 = single_phase(30e3, 0.05, "paste (thin BLT)")
    P(f"Single-phase HMMC PG25: {sp15['dp_total_kPa']:.1f} kPa / {sp15['pump_W']:.1f} W at 15 kW; {sp30['dp_total_kPa']:.1f} kPa / {sp30['pump_W']:.1f} W at 30 kW (36 LPM).\n")

    # 6. Temperature budget comparison
    P("## 6. Case-to-45C budget: two-phase HMMC vs single-phase HMMC (hotspot +4 K on both)")
    P("| design | Q kW | q W/cm2 | Tsat-45 / caloric K | TIM K | base K | conv K | **avg dT K** | max dT K | flow LPM | dP kPa |")
    P("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    comparison = {}
    for Q in (15e3, 30e3):
        for tim_R, lab in ((0.05, "paste (thin BLT)"), (0.015, "liquid metal")):
            s = single_phase(Q, tim_R, lab)
            comparison[("SP", lab, Q)] = s
            P(f"| SP HMMC PG25, {lab}, plate inlet 45 C | {Q/1e3:.0f} | {s['q_W_cm2']:.0f} | {s['dT_cal']:.1f} | {s['dT_tim']:.1f} | {s['dT_base']:.1f} | {s['dT_conv']:.1f} | "
              f"**{s['dT_avg']:.1f}** | {s['dT_max']:.1f} | {s['flow_lpm']:.0f} | {s['dp_total_kPa']:.1f} |")
            P(f"| SP HMMC PG25, {lab}, system basis (+3 K CDU) | {Q/1e3:.0f} | {s['q_W_cm2']:.0f} | {s['dT_cal']+3:.1f} | {s['dT_tim']:.1f} | {s['dT_base']:.1f} | {s['dT_conv']:.1f} | "
              f"**{s['dT_avg']+3:.1f}** | {s['dT_max']+3:.1f} | {s['flow_lpm']:.0f} | {s['dp_total_kPa']:.1f} |")
        for Tsat in (60.0, 55.0, 50.0):
            for lab in ("paste (thin BLT)", "liquid metal"):
                for htc in ("cooper", "enhanced", "kandlikar"):
                    r = evaluate_2phase("R1233zd(E)", Q, Tsat, tim=lab, htc=htc)
                    comparison[("2P", lab, Q, Tsat, htc)] = r
                    P(f"| 2P HMMC R1233zd(E), {lab}, Tsat {Tsat:.0f} C, h={htc} | {Q/1e3:.0f} | {r['q_fp']:.0f} | {r['dT_sat']:.1f} | {r['dT_tim']:.1f} | {r['dT_base']:.1f} | {r['dT_conv']:.1f} | "
                      f"**{r['dT_avg']:.1f}** | {r['dT_max']:.1f} | {r['lpm']:.0f} | {r['dp']['total']/1e3:.1f} |")
    P("")
    P("### Net benefit of the two-phase variant (negative = two-phase is hotter), vs SP HMMC + liquid metal, plate-inlet basis")
    P("| Q kW | Tsat C | benefit K (Cooper h, plain Cu) | benefit K (2.5x Cooper, enhanced surface) | benefit K (Kandlikar h, upper bound) |")
    P("|---:|---:|---:|---:|---:|")
    for Q in (15e3, 30e3):
        s = comparison[("SP", "liquid metal", Q)]
        for Tsat in (60.0, 55.0, 50.0):
            c = comparison[("2P", "liquid metal", Q, Tsat, "cooper")]
            e = comparison[("2P", "liquid metal", Q, Tsat, "enhanced")]
            k = comparison[("2P", "liquid metal", Q, Tsat, "kandlikar")]
            P(f"| {Q/1e3:.0f} | {Tsat:.0f} | {s['dT_avg']-c['dT_avg']:+.1f} | {s['dT_avg']-e['dT_avg']:+.1f} | {s['dT_avg']-k['dT_avg']:+.1f} |")
    P("")

    # 7. Crossover flux
    P("## 7. Footprint-flux crossover (liquid metal TIM, 117 cm2, SP at 1.2 LPM/kW; 2P R1233zd(E), x_out = 0.3)")
    P("| q W/cm2 | Q kW | SP avg dT | 2P Tsat 60 (Cooper/enhanced/Kandlikar) | 2P Tsat 55 (Cooper/enhanced/Kandlikar) | SP ultrafine 0.05/0.05x0.6 avg dT |")
    P("|---:|---:|---:|---|---|---:|")
    for q in (128, 200, 256, 300, 400, 500):
        Q = q * 1e4 * A_FP
        s = single_phase(Q, 0.015, "liquid metal")
        su = hmmc_design(117.0, fin_t_mm=0.05, gap_mm=0.05, fin_h_mm=0.6, tim_R=0.015, tim_label="liquid metal", name="HMMC-ultrafine").evaluate(Q, 1.2)
        c60 = evaluate_2phase("R1233zd(E)", Q, 60.0, tim="liquid metal", htc="cooper")
        e60 = evaluate_2phase("R1233zd(E)", Q, 60.0, tim="liquid metal", htc="enhanced")
        k60 = evaluate_2phase("R1233zd(E)", Q, 60.0, tim="liquid metal", htc="kandlikar")
        c55 = evaluate_2phase("R1233zd(E)", Q, 55.0, tim="liquid metal", htc="cooper")
        e55 = evaluate_2phase("R1233zd(E)", Q, 55.0, tim="liquid metal", htc="enhanced")
        k55 = evaluate_2phase("R1233zd(E)", Q, 55.0, tim="liquid metal", htc="kandlikar")
        P(f"| {q} | {Q/1e3:.0f} | {s['dT_avg']:.1f} | {c60['dT_avg']:.1f} / {e60['dT_avg']:.1f} / {k60['dT_avg']:.1f} | {c55['dT_avg']:.1f} / {e55['dT_avg']:.1f} / {k55['dT_avg']:.1f} | {su['dT_avg']:.1f} |")
    P("")

    # 8. Pressure / fluid practicalities
    P("## 8. Fluid practicalities")
    P("| fluid | Psat 55 C bar | Psat 60 C bar | Psat ~80 C (no-flow fault) bar est. | rho_v kg/m3 | vapour LPM per kW at x_out 0.3 | GWP | status |")
    P("|---|---:|---:|---:|---:|---:|---|---|")
    for fname, f in FLUIDS.items():
        # Clausius-Clapeyron estimate for 80 C
        T1, T2 = 333.15, 353.15
        p80 = f["Psat60"] * math.exp(f["hfg"] * f["M"] * 1e-3 / 8.314 * (1 / T1 - 1 / T2))
        vap_lpm_kw = (1e3 / (0.3 * f["hfg"])) * 0.3 / f["rho_v"] * 6e4
        P(f"| {fname} | {f['Psat55']*10:.1f} | {f['Psat60']*10:.1f} | {p80*10:.1f} | {f['rho_v']:.1f} | {vap_lpm_kw:.0f} | {f['GWP']} | {f['status']} |")
    P("")
    P("Tsat sensitivity to pressure drop, R1233zd(E) ~60 C: dP/dT ~ 11 kPa/K -> a 10 kPa plate+line drop lowers outlet Tsat by ~0.9 K (benign).")
    text = "\n".join(out)
    print(text)
    with open(__import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), 'two-phase-option_output.md')), "w") as fh:
        fh.write(text + "\n")

if __name__ == "__main__":
    main()
