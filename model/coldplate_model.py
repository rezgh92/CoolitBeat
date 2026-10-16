#!/usr/bin/env python3
"""
First-principles thermal / hydraulic scoping model for single-phase cold plates.

Purpose
-------
Decompose the case-to-inlet temperature rise (dT) of a direct-liquid-cooled
cold plate into its series contributions and estimate pressure drop, so that
(a) the CoolIT 15 kW benchmark (June 2026 tech brief) can be reverse-engineered
with stated assumptions, and (b) quantitative targets for a competing
architecture can be set on the same operating point:

    Q = 15 kW, flow = 1.2 LPM/kW (18 LPM), PG25 coolant, 45 C inlet.

Model (1-D series network, per unit footprint area):

    dT_case_in = dT_caloric + dT_TIM + dT_base + dT_conv

    dT_caloric : average coolant temperature rise seen by the surface.
                 Energy balance fixes the outlet rise dT_out = Q/(m cp).
                 - Long-channel plates (single pass, split-flow): the wall tracks
                   the linear fluid ramp, average ~0.5 dT_out.
                 - Short-cell manifold plates (cell < ~10 mm, isothermal at the
                   fin scale): eps-NTU result dT_cal = dT_out [1/(1-e^-NTU) - 1/NTU]
                   with NTU = h_eff A / (m cp)  (0.6-0.7 dT_out at NTU 1.2-2).
    dT_TIM     : q'' * R''_TIM
    dT_base    : q'' * t_base / k_solid
    dT_conv    : q'' / h_eff,  h_eff = h * (eta_fin * 2H + b) / pitch
                 laminar rectangular-channel Nusselt number (Shah & London, H1)
                 with a thermal-entrance enhancement (Stephan-type), straight-fin
                 efficiency with adiabatic tip.
    hot spot   : max - avg = flow-driven (long-wave manifold maldistribution or
                 intrinsic caloric ramp) + TIM / assembly scatter (max of 8 TCs).

Pressure drop (Darcy form): dp_channel = 2 (f.Re)_Fanning mu u L / Dh^2, plus
developing-flow / turning losses on channel velocity, slot-entry loss, header
loss, an optional orifice-comb metering loss, and port losses on port velocity.

Model history: v1 used the Fanning f.Re in a Darcy formula (channel friction
4x low) and a 0.5 caloric fraction for manifold plates; both corrected after
the physics-check round (docs/cooling/appendix/physics/SYNTHESIS-physics.md).
v3 (verification round, docs/cooling/appendix/verify/verify-physics.md): PG25
conductivity 0.49 W/mK, and the split-flow intrinsic hot spot scales with the
coolant rise (0.5 dT_out) instead of a fixed 6.3 K.

Scope: this is the 1-D scoping tool. The architecture-of-record numbers in
docs/cooling/03-architecture.md add each plate's own 2-D conjugate penalty
(appendix/arch/cell2d.py) and come from appendix/verify/final/*.py.

This is a scoping model (+/-25 % per term), NOT CFD. All inputs are explicit so
the team can re-run it with measured values.
Run:  python3 coldplate_model.py
"""
from __future__ import annotations

import math
from dataclasses import dataclass, replace


# ----------------------------------------------------------------------------
# Coolant: 25 vol% propylene glycol in water ("PG25"), ~50 C film temperature.
# Engineering approximations from glycol property tables (+/-5 %).
# ----------------------------------------------------------------------------
@dataclass(frozen=True)
class Fluid:
    name: str = "PG25 @ ~50C"
    rho: float = 1005.0      # kg/m3
    cp: float = 3930.0       # J/kg-K
    mu: float = 1.25e-3      # Pa-s   (water ~0.55e-3 at 50 C)
    k: float = 0.49          # W/m-K (corrected from 0.52 after verification)

    @property
    def Pr(self) -> float:
        return self.cp * self.mu / self.k


PG25 = Fluid()
WATER50 = Fluid("water @ 50C", 988.0, 4181.0, 0.547e-3, 0.644)

K_CU = 390.0   # W/m-K, OFHC copper
K_AL = 200.0   # W/m-K, aluminium

# TIM options: (R'' cm2K/W, max-of-8-TC assembly scatter K at ~130 W/cm2)
TIM = {
    "paste 0.07":        (0.070, 3.5),   # standard grease on a 100+ mm lid (benchmark)
    "paste thin-BLT":    (0.050, 3.5),
    "PCM pad":           (0.055, 1.5),   # phase-change pad, bow-tolerant  [Tier 1]
    "liquid metal":      (0.015, 0.6),   # Ga alloy on Ni-plated surfaces  [Tier 2]
    "indium solder":     (0.008, 0.6),
    "direct-to-die":     (0.000, 0.6),   # case = die top                  [Tier 3]
}


@dataclass
class ColdPlate:
    name: str
    footprint_cm2: float            # heated footprint (TTV heater area or die/lid area)
    fin_t_mm: float                 # fin thickness
    gap_mm: float                   # channel width (gap between fins)
    fin_h_mm: float                 # fin height (= channel height)
    flow_len_mm: float              # fluid path length in a channel between entry and exit
    base_mm: float                  # base thickness under the channels
    k_solid: float = K_CU
    tim: str = "paste 0.07"
    isothermal_cell: bool = False   # True for short-cell manifold plates (eps-NTU caloric)
    hotspot_flow_K: float = 6.3     # flow-driven (max - avg) for manifold plates (fixed K)
    ramp_hotspot: bool = False      # True for long-channel plates: hot spot = 0.5 * dT_out
    n_parallel_paths: int = 1       # channel groups in parallel along the flow direction
    slot_w_mm: float = 0.0          # width of distribution slots feeding channels (0 = none)
    K_channel: float = 2.5          # developing flow + turns, on channel velocity
    K_slot: float = 1.5             # slot entry/exit, on slot velocity
    header_u_m_s: float = 1.0       # design velocity in headers at 18 LPM (scaled with flow)
    K_header: float = 2.0           # header losses on header velocity (inlet + outlet)
    port_bore_mm: float = 12.0      # internal port bore
    K_port: float = 2.3             # port + internal turns, on port velocity
    orifice_dp_kPa_18: float = 0.0  # orifice-comb metering loss at 18 LPM (scales with flow^2)
    notes: str = ""

    def evaluate(self, Q_W: float, lpm_per_kw: float, fluid: Fluid = PG25, T_in: float = 45.0) -> dict:
        A = self.footprint_cm2 * 1e-4
        q = Q_W / A
        flow_lpm = lpm_per_kw * Q_W / 1000.0
        Vdot = flow_lpm / 60.0 / 1000.0
        mdot = Vdot * fluid.rho
        dT_out = Q_W / (mdot * fluid.cp)

        b = self.gap_mm * 1e-3
        H = self.fin_h_mm * 1e-3
        L = self.flow_len_mm * 1e-3
        t = self.fin_t_mm * 1e-3
        p = t + b
        W = math.sqrt(A)                                   # square footprint assumed
        n_across = W / p
        alpha = min(b, H) / max(b, H)
        Dh = 2 * b * H / (b + H)
        Nu_fd = 8.235 * (1 - 2.0421 * alpha + 3.0853 * alpha**2 - 2.4765 * alpha**3
                         + 1.0578 * alpha**4 - 0.1861 * alpha**5) * 0.95   # 3-side heating
        fRe = 24 * (1 - 1.3553 * alpha + 1.9467 * alpha**2 - 1.7012 * alpha**3
                    + 0.9564 * alpha**4 - 0.2537 * alpha**5)              # Fanning

        n_paths = n_across * self.n_parallel_paths
        u = Vdot / (n_paths * b * H)
        Re = fluid.rho * u * Dh / fluid.mu
        x_star = L / (Dh * Re * fluid.Pr)
        Nu = Nu_fd + 0.024 * x_star**-1.14 / (1 + 0.0358 * fluid.Pr**0.17 * x_star**-0.64)
        h = Nu * fluid.k / Dh
        m = math.sqrt(2 * h / (self.k_solid * t))
        eta = math.tanh(m * H) / (m * H)
        area_ratio = (2 * H * eta + b) / p
        h_eff = h * area_ratio
        R_conv = 1 / h_eff

        NTU = h_eff * A / (mdot * fluid.cp)
        if self.isothermal_cell:
            cal_frac = 1 / (1 - math.exp(-NTU)) - 1 / NTU
        else:
            cal_frac = 0.5
        R_tim, scatter = TIM[self.tim]
        dT_cal = cal_frac * dT_out
        dT_tim = q * R_tim * 1e-4
        dT_base = q * (self.base_mm * 1e-3) / self.k_solid
        dT_conv = q * R_conv
        dT_avg = dT_cal + dT_tim + dT_base + dT_conv
        flow_hot = 0.5 * dT_out if self.ramp_hotspot else self.hotspot_flow_K
        hotspot = flow_hot + scatter * (q / 1.28e6)   # TIM scatter scales with flux
        dT_max = dT_avg + hotspot

        # --- hydraulics (Darcy form) ---
        dp_ch = 2 * fRe * fluid.mu * u * L / Dh**2
        dp_K = self.K_channel * 0.5 * fluid.rho * u**2
        if self.slot_w_mm > 0 and self.n_parallel_paths > 1:
            n_slots = self.n_parallel_paths / 2
            u_slot = Vdot / (n_slots * W * self.slot_w_mm * 1e-3)
        else:
            u_slot = 0.0
        dp_slot = self.K_slot * 0.5 * fluid.rho * u_slot**2
        u_header = self.header_u_m_s * flow_lpm / 18.0
        dp_header = self.K_header * 0.5 * fluid.rho * u_header**2
        u_port = Vdot / (math.pi / 4 * (self.port_bore_mm * 1e-3) ** 2)
        dp_port = self.K_port * 0.5 * fluid.rho * u_port**2
        dp_orif = self.orifice_dp_kPa_18 * 1e3 * (flow_lpm / 18.0) ** 2
        dp_total = dp_ch + dp_K + dp_slot + dp_header + dp_port + dp_orif
        pump_W = dp_total * Vdot

        flux_terms = dT_tim + dT_base + dT_conv
        allowed = 85.0 - T_in - dT_cal - hotspot
        Q_cap = Q_W * allowed / flux_terms if flux_terms > 0 else float("inf")

        return dict(
            name=self.name, footprint_cm2=self.footprint_cm2, q_W_cm2=q / 1e4,
            flow_lpm=flow_lpm, dT_out=dT_out, u_ch=u, u_slot=u_slot, u_port=u_port, Re=Re, Nu=Nu,
            h=h, eta=eta, area_ratio=area_ratio, h_eff=h_eff, NTU=NTU, cal_frac=cal_frac,
            R_conv_cm2K_W=R_conv * 1e4,
            dT_cal=dT_cal, dT_tim=dT_tim, dT_base=dT_base, dT_conv=dT_conv,
            dT_avg=dT_avg, hotspot=hotspot, dT_max=dT_max, R_th_mK_W=dT_avg / Q_W * 1e3,
            R_unit_cm2K_W=dT_avg / (q / 1e4),
            dp_ch_kPa=dp_ch / 1e3, dp_K_kPa=dp_K / 1e3, dp_slot_kPa=dp_slot / 1e3,
            dp_header_kPa=dp_header / 1e3, dp_port_kPa=dp_port / 1e3, dp_orif_kPa=dp_orif / 1e3,
            dp_total_kPa=dp_total / 1e3, pump_W=pump_W,
            Q_cap_kW=Q_cap / 1e3, T_case_avg=T_in + dT_avg, T_case_max=T_in + dT_max,
        )


# ----------------------------------------------------------------------------
# Reference designs
# ----------------------------------------------------------------------------
def coolit_like(footprint_cm2: float) -> ColdPlate:
    """Best-guess reconstruction of a skived split-flow plate (geometry undisclosed):
    skived Cu fins 0.2 mm / 0.2 mm gaps / 4 mm tall, 2 mm base, split-flow (centre
    feed, two half-length paths in parallel), standard paste. Hot spot = intrinsic
    caloric ramp 0.5 dT_out (6.3 K at 1.2 LPM/kW) + paste scatter (3.5 K) = 9.8 K,
    matching the measured 44.2 - 34.4 K at the benchmark point."""
    side_mm = math.sqrt(footprint_cm2) * 10
    return ColdPlate(
        name=f"CoolIT-like skived split-flow ({footprint_cm2:.0f} cm2, paste)",
        footprint_cm2=footprint_cm2, fin_t_mm=0.2, gap_mm=0.2, fin_h_mm=4.0,
        flow_len_mm=0.5 * side_mm, base_mm=2.0, tim="paste 0.07", isothermal_cell=False,
        hotspot_flow_K=6.3, ramp_hotspot=True, n_parallel_paths=2, K_channel=2.0, header_u_m_s=1.2, K_header=2.0,
        port_bore_mm=12.0, K_port=2.3, notes="reconstruction; geometry not disclosed by CoolIT",
    )


def hmmc(footprint_cm2: float, *, core: str = "R", tim: str = "PCM pad", base_mm: float = 1.0,
         hotspot_flow_K: float = 1.5, name: str | None = None, k_solid: float = K_CU) -> ColdPlate:
    """Hierarchical manifold micro-channel (HMMC) plate, manifold 'design H':
    centre-fed / centre-collected two-level headers (10x15 / 14x20 mm), 3.5 x 8 mm slots
    at 8 mm pitch (4 mm flow length), 16 mm ports, orifice comb where channel friction
    is below ~2 kPa so the branch stays the dominant resistance (flow uniformity 1.10).
    Cores:  R = robust  0.15 mm gap / 0.10 mm fin / 2.0 mm tall  (10-year drop-in, 50 um screen)
            P = performance 0.10 / 0.10 / 1.5 mm (requires <= 33 um absolute loop filtration)
            F = fine 0.075 / 0.075 / 1.0 mm (reference only; NOT deployable, fouling)"""
    cores = {
        "R": dict(gap_mm=0.15, fin_t_mm=0.10, fin_h_mm=2.0, orifice=2.0),
        "P": dict(gap_mm=0.10, fin_t_mm=0.10, fin_h_mm=1.5, orifice=1.5),
        "F": dict(gap_mm=0.075, fin_t_mm=0.075, fin_h_mm=1.0, orifice=1.0),
    }[core]
    side_mm = math.sqrt(footprint_cm2) * 10
    flow_len = 4.0
    n_slots = max(1, int(round(side_mm / (2 * flow_len))))
    label = name or f"HMMC-{core}"
    return ColdPlate(
        name=f"{label} ({footprint_cm2:.0f} cm2, {tim})",
        footprint_cm2=footprint_cm2, fin_t_mm=cores["fin_t_mm"], gap_mm=cores["gap_mm"],
        fin_h_mm=cores["fin_h_mm"], flow_len_mm=flow_len, base_mm=base_mm, k_solid=k_solid,
        tim=tim, isothermal_cell=True, hotspot_flow_K=hotspot_flow_K,
        n_parallel_paths=2 * n_slots, slot_w_mm=3.5, K_channel=3.0, K_slot=1.5,
        header_u_m_s=1.0, K_header=1.0, port_bore_mm=16.0, K_port=2.3,
        orifice_dp_kPa_18=cores["orifice"],
        notes="design H manifold; tied sandwich (fin tips bonded to manifold webs)",
    )


def calibrate_footprint(target_dT: float, Q: float, lpm_kw: float, lo=50.0, hi=300.0) -> float:
    """Footprint at which the CoolIT-like reconstruction reproduces the measured avg dT."""
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if coolit_like(mid).evaluate(Q, lpm_kw)["dT_avg"] > target_dT:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


# ----------------------------------------------------------------------------
# Reporting
# ----------------------------------------------------------------------------
HEADER = ("| design | q'' W/cm2 | caloric | TIM | base | conv | **avg dT** | max dT | "
          "R'' cm2K/W | dP kPa | pump W | Q cap kW |\n"
          "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")


def fmt_row(r: dict) -> str:
    return (f"| {r['name']:<52} | {r['q_W_cm2']:6.0f} | {r['dT_cal']:5.1f} | {r['dT_tim']:5.1f} | "
            f"{r['dT_base']:5.1f} | {r['dT_conv']:5.1f} | **{r['dT_avg']:5.1f}** | {r['dT_max']:5.1f} | "
            f"{r['R_unit_cm2K_W']:5.3f} | {r['dp_total_kPa']:5.1f} | {r['pump_W']:5.1f} | {r['Q_cap_kW']:5.1f} |")


def main():
    Q, lpm_kw = 15000.0, 1.2
    f = PG25
    Vdot = lpm_kw * Q / 1000 / 60 / 1000
    dT_out = Q / (Vdot * f.rho * f.cp)
    print("# Cold plate scoping model - CoolIT 15 kW benchmark operating point")
    print(f"Q = {Q/1000:.0f} kW, {lpm_kw} LPM/kW -> {lpm_kw*Q/1000:.0f} LPM PG25, 45 C inlet\n")
    print(f"Coolant outlet rise (energy balance): {dT_out:.1f} K  "
          f"(mdot = {Vdot*f.rho:.3f} kg/s, cp = {f.cp:.0f} J/kgK, Pr = {f.Pr:.1f}); "
          f"average caloric term for a long-channel plate: {0.5*dT_out:.1f} K; "
          f"for an isothermal short-cell plate: 0.60-0.68 x {dT_out:.1f} K\n")

    print("## 1. Reverse-engineering the CoolIT 15 kW result (measured avg dT 34.4 K, max 44.2 K)")
    print("Footprint is undisclosed. Sweep it for a plausible skived split-flow plate:\n")
    print(HEADER)
    for A in (60, 80, 100, 120, 150, 200):
        print(fmt_row(coolit_like(A).evaluate(Q, lpm_kw)))
    A_cal = calibrate_footprint(34.4, Q, lpm_kw)
    rc = coolit_like(A_cal).evaluate(Q, lpm_kw)
    print(f"\nCalibrated footprint: {A_cal:.0f} cm2 ({math.sqrt(A_cal)*10:.0f} x {math.sqrt(A_cal)*10:.0f} mm, "
          f"{rc['q_W_cm2']:.0f} W/cm2) reproduces 34.4 K -> adopted as the working assumption "
          f"(CoolIT's 4 kW plate was 50 x 50 mm at ~0.225 cm2K/W, consistent with ~100-120 cm2 here).")
    print(f"Budget: caloric {rc['dT_cal']:.1f} | TIM {rc['dT_tim']:.1f} | base {rc['dT_base']:.1f} | "
          f"conv {rc['dT_conv']:.1f} K; channel u = {rc['u_ch']:.2f} m/s, Re = {rc['Re']:.0f}; "
          f"dP ~ {rc['dp_total_kPa']:.0f} kPa port-to-port (estimate; undisclosed; 17-42 kPa for plausible fin pitches).\n")

    A0 = round(A_cal)
    print(f"## 2. Lever-by-lever at the calibrated footprint ({A0} cm2), same flow, inlet and paste")
    print(HEADER)
    cp = coolit_like(A0)
    print(fmt_row(cp.evaluate(Q, lpm_kw)))
    n_slots = int(round(math.sqrt(A0) * 10 / 8))
    steps = [
        ("+ base 2.0 -> 1.0 mm (tied sandwich)", dict(base_mm=1.0)),
        ("+ fins 0.2/0.2x4 -> 0.10/0.15x2 mm, still split-flow", dict(fin_t_mm=0.10, gap_mm=0.15, fin_h_mm=2.0)),
        ("+ manifold feed, 4 mm flow length (HMMC-R core)", dict(flow_len_mm=4.0, n_parallel_paths=2 * n_slots, slot_w_mm=3.5, isothermal_cell=True, hotspot_flow_K=1.5, ramp_hotspot=False, K_channel=3.0, K_header=1.0, header_u_m_s=1.0, port_bore_mm=16.0, orifice_dp_kPa_18=2.0)),
        ("+ PCM pad TIM (Tier 1)", dict(tim="PCM pad")),
        ("+ liquid metal TIM on Ni (Tier 2)", dict(tim="liquid metal")),
    ]
    for label, kw in steps:
        cp = replace(cp, name=label, **kw)
        print(fmt_row(cp.evaluate(Q, lpm_kw)))
    print()

    print(f"## 3. Product tiers at {A0} cm2 (15 kW, 18 LPM, 45 C)")
    print(HEADER)
    rows = [
        coolit_like(A0),
        hmmc(A0, core="R", tim="paste 0.07", name="HMMC-R like-for-like"),
        hmmc(A0, core="R", tim="PCM pad", name="HMMC-R Tier 1 drop-in"),
        hmmc(A0, core="R", tim="liquid metal", name="HMMC-R Tier 2 OEM"),
        hmmc(A0, core="P", tim="PCM pad", name="HMMC-P (<=33um loops)"),
        hmmc(A0, core="P", tim="liquid metal", name="HMMC-P (<=33um loops)"),
        hmmc(A0, core="R", tim="direct-to-die", base_mm=0.8, name="HMMC-R Tier 3 D2D"),
        hmmc(A0, core="F", tim="liquid metal", name="HMMC-F (NOT deployable, ref.)"),
        hmmc(A0, core="R", tim="PCM pad", name="HMMC-R aluminium", k_solid=K_AL),
    ]
    for v in rows:
        print(fmt_row(v.evaluate(Q, lpm_kw)))
    r1 = rows[2].evaluate(Q, lpm_kw)
    print(f"\nTier 1 detail: NTU {r1['NTU']:.2f}, caloric fraction {r1['cal_frac']:.2f}, h {r1['h']/1e3:.1f} kW/m2K, "
          f"eta {r1['eta']:.2f}, h_eff {r1['h_eff']/1e3:.0f} kW/m2K, channel u {r1['u_ch']:.3f} m/s (Re {r1['Re']:.0f}), "
          f"port u {r1['u_port']:.2f} m/s; dP split: channel {r1['dp_ch_kPa']:.2f} + turns {r1['dp_K_kPa']:.2f} + slot "
          f"{r1['dp_slot_kPa']:.2f} + header {r1['dp_header_kPa']:.2f} + orifice {r1['dp_orif_kPa']:.2f} + ports "
          f"{r1['dp_port_kPa']:.2f} = {r1['dp_total_kPa']:.1f} kPa (quick disconnects excluded).\n")

    print(f"## 4. Fin/channel geometry sweep (HMMC manifold, {A0} cm2, PCM pad, 4 mm flow length)")
    print("Deployability: gap >= 0.15 mm behind a 50 um absolute screen (10-year SKU); 0.10 mm only")
    print("behind <= 33 um absolute filtration; < 0.10 mm not deployable (fouling).\n")
    print("| gap (mm) | fin (mm) | H (mm) | h kW/m2K | eta | h_eff kW/m2K | NTU | cal K | conv K | avg dT K | max dT K | dP kPa |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for g, t in ((0.075, 0.075), (0.10, 0.10), (0.15, 0.10), (0.15, 0.15), (0.20, 0.15)):
        for Hf in (1.0, 1.5, 2.0, 3.0):
            base = hmmc(A0, core="R")
            v = replace(base, gap_mm=g, fin_t_mm=t, fin_h_mm=Hf)
            r = v.evaluate(Q, lpm_kw)
            print(f"| {g:.3f} | {t:.3f} | {Hf:.1f} | {r['h']/1e3:.1f} | {r['eta']:.2f} | {r['h_eff']/1e3:.0f} | {r['NTU']:.2f} | "
                  f"{r['dT_cal']:.1f} | {r['dT_conv']:.1f} | {r['dT_avg']:.1f} | {r['dT_max']:.1f} | {r['dp_total_kPa']:.1f} |")
    print()

    print(f"## 5. Flow sensitivity ({A0} cm2): CoolIT-like (paste) vs HMMC-R Tier 1 (PCM) vs Tier 2 (LM)")
    print("| LPM/kW | flow LPM | CoolIT avg | max | dP kPa | pump W | T1 avg | max | dP kPa | pump W | T2 avg | max |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for lk in (0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5):
        a = coolit_like(A0).evaluate(Q, lk)
        b = hmmc(A0, core="R", tim="PCM pad").evaluate(Q, lk)
        c = hmmc(A0, core="R", tim="liquid metal").evaluate(Q, lk)
        print(f"| {lk:.1f} | {a['flow_lpm']:.0f} | {a['dT_avg']:.1f} | {a['dT_max']:.1f} | {a['dp_total_kPa']:.1f} | {a['pump_W']:.1f} | "
              f"{b['dT_avg']:.1f} | {b['dT_max']:.1f} | {b['dp_total_kPa']:.1f} | {b['pump_W']:.1f} | {c['dT_avg']:.1f} | {c['dT_max']:.1f} |")
    print("\nEqual-pumping-power reading: the HMMC at 2.0 LPM/kW spends about what the skived plate spends at 1.2 LPM/kW.\n")

    print("## 6. Scaling to other loads / footprints (1.2 LPM/kW)")
    print(HEADER)
    for Qk, A in ((1.4, 45), (2.3, 60), (3.6, 80), (15, A0), (25, A0), (30, 150), (50, 250)):
        print(fmt_row(coolit_like(A).evaluate(Qk * 1e3, lpm_kw)))
        print(fmt_row(hmmc(A, core="R", tim="PCM pad").evaluate(Qk * 1e3, lpm_kw)))
        print(fmt_row(hmmc(A, core="R", tim="liquid metal").evaluate(Qk * 1e3, lpm_kw)))
    print()

    print(f"## 7. Water vs PG25 (HMMC-R Tier 1, {A0} cm2, 15 kW, 1.2 LPM/kW)")
    for fl in (PG25, WATER50):
        r = hmmc(A0, core="R", tim="PCM pad").evaluate(Q, lpm_kw, fluid=fl)
        print(f"- {fl.name}: avg dT {r['dT_avg']:.1f} K, max {r['dT_max']:.1f} K, dP {r['dp_total_kPa']:.1f} kPa")
    print("\nCaveats: 1-D series network, laminar correlations, uniform heating; non-uniform GPU+HBM packages,")
    print("manifold maldistribution (assumed +/-10 % -> 1.5 K) and TIM bond-line variation are handled as")
    print("lumped hot-spot terms. Treat +/-25 % per term; see the physics-check reports for the 2-D/network checks.")


if __name__ == "__main__":
    main()
