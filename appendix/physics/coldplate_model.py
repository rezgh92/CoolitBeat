#!/usr/bin/env python3
# Frozen copy of the scoping model as used by the round-2 physics checks (git 3a14c9f, v1).
# The physics scripts in this folder import this copy so their stored outputs reproduce.
# The current model lives in docs/cooling/model/.
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
                 Energy balance fixes the outlet rise Q/(m cp); a uniformly
                 heated surface sees ~half of it on average (`caloric_fraction`
                 = 0.5 for a single pass and also for split-flow, since each
                 half-length path carries half the flow and half the heat).
    dT_TIM     : q'' * R''_TIM
    dT_base    : q'' * t_base / k_solid
    dT_conv    : q'' / h_eff,  h_eff = h * (eta_fin * 2H + b) / pitch
                 laminar rectangular-channel Nusselt number (Shah & London, H1)
                 with a thermal-entrance enhancement (Stephan-type), straight-fin
                 efficiency with adiabatic tip.

Pressure drop: laminar rectangular-duct friction (Shah & London f*Re) over the
channel flow length + developing-flow/turning loss on channel velocity + slot
(distribution opening) loss + manifold header loss + port/fitting allowance.

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
    k: float = 0.52          # W/m-K

    @property
    def Pr(self) -> float:
        return self.cp * self.mu / self.k


PG25 = Fluid()
WATER50 = Fluid("water @ 50C", 988.0, 4181.0, 0.547e-3, 0.644)

K_CU = 390.0   # W/m-K, OFHC copper
K_AL = 200.0   # W/m-K, aluminium


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
    tim_R_cm2K_W: float = 0.07      # paste 0.05-0.10; liquid metal 0.01-0.02; indium 0.005-0.01
    tim_label: str = "paste"
    caloric_fraction: float = 0.5
    hotspot_penalty_K: float = 10.0 # (max - avg) case dT; measured 9.8 K for CoolIT 15 kW
    n_parallel_paths: int = 1       # channel groups in parallel along the flow direction
    slot_w_mm: float = 0.0          # width of distribution slots feeding channels (0 = none)
    K_channel: float = 2.5          # developing flow + turns, on channel velocity
    K_slot: float = 1.5             # slot entry/exit, on slot velocity
    manifold_u_m_s: float = 1.0     # design velocity in headers
    K_manifold: float = 3.0         # header losses on manifold velocity (inlet + outlet)
    port_dp_kPa: float = 3.0        # fittings / UQD / internal ports at rated flow
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
                    + 0.9564 * alpha**4 - 0.2537 * alpha**5)

        n_paths = n_across * self.n_parallel_paths
        u = Vdot / (n_paths * b * H)
        Re = fluid.rho * u * Dh / fluid.mu
        x_star = L / (Dh * Re * fluid.Pr)
        Nu = Nu_fd + 0.024 * x_star**-1.14 / (1 + 0.0358 * fluid.Pr**0.17 * x_star**-0.64)
        h = Nu * fluid.k / Dh
        m = math.sqrt(2 * h / (self.k_solid * t))
        eta = math.tanh(m * H) / (m * H)
        area_ratio = (2 * H * eta + b) / p
        R_conv = 1 / (h * area_ratio)

        dT_cal = self.caloric_fraction * dT_out
        dT_tim = q * self.tim_R_cm2K_W * 1e-4
        dT_base = q * (self.base_mm * 1e-3) / self.k_solid
        dT_conv = q * R_conv
        dT_avg = dT_cal + dT_tim + dT_base + dT_conv
        dT_max = dT_avg + self.hotspot_penalty_K

        dp_ch = fRe * fluid.mu * u * L / (2 * Dh**2)
        dp_K = self.K_channel * 0.5 * fluid.rho * u**2
        if self.slot_w_mm > 0 and self.n_parallel_paths > 1:
            n_slots = self.n_parallel_paths / 2            # inlet slots (each feeds two directions)
            u_slot = Vdot / (n_slots * W * self.slot_w_mm * 1e-3)
        else:
            u_slot = 0.0
        dp_slot = self.K_slot * 0.5 * fluid.rho * u_slot**2
        dp_man = self.K_manifold * 0.5 * fluid.rho * self.manifold_u_m_s**2
        dp_total = dp_ch + dp_K + dp_slot + dp_man + self.port_dp_kPa * 1e3
        pump_W = dp_total * Vdot

        flux_terms = dT_tim + dT_base + dT_conv
        allowed = 85.0 - T_in - dT_cal - self.hotspot_penalty_K   # T_case,max <= 85 C
        Q_cap = Q_W * allowed / flux_terms if flux_terms > 0 else float("inf")

        return dict(
            name=self.name, footprint_cm2=self.footprint_cm2, q_W_cm2=q / 1e4,
            flow_lpm=flow_lpm, dT_out=dT_out, u_ch=u, u_slot=u_slot, Re=Re, Nu=Nu, h=h, eta=eta,
            area_ratio=area_ratio, R_conv_cm2K_W=R_conv * 1e4,
            dT_cal=dT_cal, dT_tim=dT_tim, dT_base=dT_base, dT_conv=dT_conv,
            dT_avg=dT_avg, dT_max=dT_max, R_th_mK_W=dT_avg / Q_W * 1e3,
            R_unit_cm2K_W=dT_avg / (q / 1e4),
            dp_ch_kPa=dp_ch / 1e3, dp_K_kPa=dp_K / 1e3, dp_slot_kPa=dp_slot / 1e3,
            dp_man_kPa=dp_man / 1e3, dp_total_kPa=dp_total / 1e3, pump_W=pump_W,
            Q_cap_kW=Q_cap / 1e3, T_case_avg=T_in + dT_avg, T_case_max=T_in + dT_max,
        )


# ----------------------------------------------------------------------------
# Reference designs
# ----------------------------------------------------------------------------
def coolit_like(footprint_cm2: float) -> ColdPlate:
    """Best-guess reconstruction of a skived split-flow plate (geometry undisclosed):
    skived Cu fins 0.2 mm / 0.2 mm gaps / 4 mm tall, 2 mm base, split-flow (centre
    feed, two half-length paths in parallel), standard paste. Hotspot penalty =
    measured (44.2 - 34.4) = 9.8 K."""
    side_mm = math.sqrt(footprint_cm2) * 10
    return ColdPlate(
        name=f"CoolIT-like skived split-flow ({footprint_cm2:.0f} cm2)",
        footprint_cm2=footprint_cm2, fin_t_mm=0.2, gap_mm=0.2, fin_h_mm=4.0,
        flow_len_mm=0.5 * side_mm, base_mm=2.0, tim_R_cm2K_W=0.07, tim_label="paste",
        caloric_fraction=0.5, hotspot_penalty_K=9.8, n_parallel_paths=2,
        K_channel=2.0, manifold_u_m_s=1.2, K_manifold=2.0, port_dp_kPa=3.0,
        notes="reconstruction; geometry not disclosed by CoolIT",
    )


def hmmc_design(footprint_cm2: float, *, fin_t_mm=0.10, gap_mm=0.10, fin_h_mm=1.0,
                flow_len_mm=2.0, base_mm=1.0, tim_R=0.05, tim_label="paste (thin BLT)",
                hotspot_K=4.0, slot_w_mm=0.3, name="HMMC", k_solid=K_CU) -> ColdPlate:
    """Hierarchical manifold micro-channel (HMMC) plate: a two-level manifold feeds
    inlet slots every 2*flow_len along the channels; every fluid parcel travels only
    flow_len in a micro-channel before leaving through the neighbouring return slot.
    Parallel paths = 2 * (plate length / slot pitch)."""
    side_mm = math.sqrt(footprint_cm2) * 10
    n_slots = max(1, int(round(side_mm / (2 * flow_len_mm))))
    return ColdPlate(
        name=f"{name} ({footprint_cm2:.0f} cm2, {tim_label})",
        footprint_cm2=footprint_cm2, fin_t_mm=fin_t_mm, gap_mm=gap_mm, fin_h_mm=fin_h_mm,
        flow_len_mm=flow_len_mm, base_mm=base_mm, k_solid=k_solid,
        tim_R_cm2K_W=tim_R, tim_label=tim_label, caloric_fraction=0.5,
        hotspot_penalty_K=hotspot_K, n_parallel_paths=2 * n_slots, slot_w_mm=slot_w_mm,
        K_channel=3.0, K_slot=1.5, manifold_u_m_s=1.0, K_manifold=4.0, port_dp_kPa=4.0,
        notes="two-level manifold feeding short micro-channel segments",
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
    return (f"| {r['name']:<48} | {r['q_W_cm2']:6.0f} | {r['dT_cal']:5.1f} | {r['dT_tim']:5.1f} | "
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
          f"average caloric term for a uniformly heated single pass: {0.5*dT_out:.1f} K\n")

    print("## 1. Reverse-engineering the CoolIT 15 kW result (measured avg dT 34.4 K, max 44.2 K)")
    print("Footprint is undisclosed. Sweep it for a plausible skived split-flow plate:\n")
    print(HEADER)
    for A in (60, 80, 100, 120, 150, 200):
        print(fmt_row(coolit_like(A).evaluate(Q, lpm_kw)))
    A_cal = calibrate_footprint(34.4, Q, lpm_kw)
    rc = coolit_like(A_cal).evaluate(Q, lpm_kw)
    print(f"\nCalibrated footprint: {A_cal:.0f} cm2 ({math.sqrt(A_cal)*10:.0f} x {math.sqrt(A_cal)*10:.0f} mm, "
          f"{rc['q_W_cm2']:.0f} W/cm2) reproduces 34.4 K -> adopted as the working assumption.")
    print(f"Budget at that point: caloric {rc['dT_cal']:.1f} | TIM {rc['dT_tim']:.1f} | base {rc['dT_base']:.1f} | "
          f"conv {rc['dT_conv']:.1f} K; channel u = {rc['u_ch']:.2f} m/s, Re = {rc['Re']:.0f}, "
          f"dP ~ {rc['dp_total_kPa']:.0f} kPa (estimate; undisclosed).\n")

    A0 = round(A_cal)
    print(f"## 2. Lever-by-lever at the calibrated footprint ({A0} cm2), same flow, same inlet, same paste")
    print(HEADER)
    cp = coolit_like(A0)
    print(fmt_row(cp.evaluate(Q, lpm_kw)))
    steps = [
        ("+ base 2.0 -> 1.0 mm", dict(base_mm=1.0)),
        ("+ fins 0.2/0.2x4 -> 0.1/0.1x2 mm (still split-flow)", dict(fin_t_mm=0.1, gap_mm=0.1, fin_h_mm=2.0)),
        ("+ manifold feed, 2 mm flow length (HMMC)", dict(flow_len_mm=2.0, n_parallel_paths=2 * int(round(math.sqrt(A0) * 10 / 4)), slot_w_mm=0.3, hotspot_penalty_K=4.0, K_channel=3.0, K_manifold=4.0, manifold_u_m_s=1.0, port_dp_kPa=4.0)),
        ("+ fins 0.075/0.075 x 1.0 mm", dict(fin_t_mm=0.075, gap_mm=0.075, fin_h_mm=1.0)),
        ("+ thin-BLT paste 0.05 cm2K/W", dict(tim_R_cm2K_W=0.05)),
    ]
    for label, kw in steps:
        cp = replace(cp, name=label, **kw)
        print(fmt_row(cp.evaluate(Q, lpm_kw)))
    print()

    print(f"## 3. Candidate HMMC variants at {A0} cm2")
    print(HEADER)
    for v in [
        hmmc_design(A0),
        hmmc_design(A0, fin_t_mm=0.075, gap_mm=0.075, fin_h_mm=0.8, name="HMMC-fine"),
        hmmc_design(A0, fin_t_mm=0.05, gap_mm=0.05, fin_h_mm=0.6, name="HMMC-ultrafine"),
        hmmc_design(A0, fin_h_mm=1.5, name="HMMC-tall"),
        hmmc_design(A0, flow_len_mm=4.0, name="HMMC-L4"),
        hmmc_design(A0, tim_R=0.015, tim_label="liquid metal", name="HMMC"),
        hmmc_design(A0, tim_R=0.008, tim_label="indium solder", name="HMMC"),
        hmmc_design(A0, tim_R=0.0, tim_label="direct-to-die/no TIM", base_mm=0.8, name="HMMC-D2D"),
        hmmc_design(A0, name="HMMC-aluminium", k_solid=K_AL),
    ]:
        print(fmt_row(v.evaluate(Q, lpm_kw)))
    print()

    print(f"## 4. Fin/channel geometry sweep (HMMC, {A0} cm2, paste 0.05, flow length 2 mm)")
    print("| gap=fin (mm) | H (mm) | h kW/m2K | eta | area ratio | conv K | avg dT K | dP kPa |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for g in (0.05, 0.075, 0.1, 0.15, 0.2):
        for Hf in (0.5, 1.0, 1.5, 2.0, 3.0):
            r = hmmc_design(A0, fin_t_mm=g, gap_mm=g, fin_h_mm=Hf).evaluate(Q, lpm_kw)
            print(f"| {g:.3f} | {Hf:.1f} | {r['h']/1e3:.1f} | {r['eta']:.2f} | {r['area_ratio']:.1f} | "
                  f"{r['dT_conv']:.1f} | {r['dT_avg']:.1f} | {r['dp_total_kPa']:.1f} |")
    print()

    print(f"## 5. Flow sensitivity ({A0} cm2, paste): CoolIT-like vs HMMC")
    print("| LPM/kW | flow LPM | CoolIT-like avg dT | max | dP kPa | HMMC avg dT | max | dP kPa |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|")
    for lk in (0.6, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5):
        a = coolit_like(A0).evaluate(Q, lk)
        b = hmmc_design(A0).evaluate(Q, lk)
        print(f"| {lk:.1f} | {a['flow_lpm']:.0f} | {a['dT_avg']:.1f} | {a['dT_max']:.1f} | {a['dp_total_kPa']:.1f} | "
              f"{b['dT_avg']:.1f} | {b['dT_max']:.1f} | {b['dp_total_kPa']:.1f} |")
    print()

    print("## 6. Scaling to other loads / footprints (1.2 LPM/kW, paste)")
    print(HEADER)
    for Qk, A in ((1.4, 45), (2.3, 60), (3.6, 80), (15, A0), (25, A0), (30, 150), (50, 250)):
        print(fmt_row(coolit_like(A).evaluate(Qk * 1e3, lpm_kw)))
        print(fmt_row(hmmc_design(A).evaluate(Qk * 1e3, lpm_kw)))
    print()

    print(f"## 7. Water vs PG25 (HMMC, {A0} cm2, 15 kW, 1.2 LPM/kW)")
    for fl in (PG25, WATER50):
        r = hmmc_design(A0).evaluate(Q, lpm_kw, fluid=fl)
        print(f"- {fl.name}: avg dT {r['dT_avg']:.1f} K, max {r['dT_max']:.1f} K, dP {r['dp_total_kPa']:.1f} kPa")
    print("\nCaveats: 1-D series network, laminar correlations, uniform heating; manifold maldistribution,")
    print("spreading under non-uniform chips and TIM bond-line variation are not resolved. Treat +/-25 %.")


if __name__ == "__main__":
    main()
