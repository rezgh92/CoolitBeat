#!/usr/bin/env python3
"""
manifold-maldistribution.py
1-D hydraulic network model of a two-level manifold feeding a micro-channel fin
array (HMMC cold plate, 108 x 108 mm footprint, PG25, 18 / 36 LPM).

Network
-------
Level 1 : inlet header (dividing manifold) + outlet header (combining manifold)
          along one plate edge (U-type: ports at the same end; Z-type: ports at
          opposite ends; C: centre-fed - inlet header across plate centre, two
          edge outlet headers, ports at mid-length).
          N_in branches = inlet slots at pitch P.
Level 2 : each inlet slot is itself a dividing manifold (fluid leaves through
          its bottom opening into the fin array along its length), each return
          slot a combining manifold. Discretised into M segments of dLy along y.
Level 3 : per segment, the 'branch' = descent through the opening into the fin
          gaps (turn + contraction), laminar flow along L_ch = P/2 in channels
          b x H (two directions), turn up, ascent through the return opening
          (turn + expansion).

Manifold pressure marching (per node k):
   dividing : p rises by theta_d*rho*(u_arrive^2 - u_leave^2)/2 (Bernoulli
              recovery, theta_d = 1 ideal), falls by Darcy friction per segment.
   combining: p falls by theta_c*rho*(v_leave^2 - v_arrive^2)/2 (momentum
              balance with zero axial momentum of the entering branch gives
              theta_c = 2), plus friction.
   friction : Darcy f = fRe_rect/Re laminar (Shah & London, Darcy form =
              4 x Fanning), Blasius 0.316 Re^-0.25 turbulent, blend 2300-4000.
Branch flow : q_k = branch.q(p_in,k - p_out,k + D), D (overall driving pressure)
              chosen by Brent so that sum(q) = Q; under-relaxed fixed point.

Level 2 -> Level 1 transfer: the effective slot-pair dp(q) curve from the
Level-2 solve is fitted as R1*q + R2*q^2 and used as the Level-1 branch law
together with the tee entry / exit losses. The two levels are coupled only
through this law (adjacent-slot sharing is assumed symmetric).

Run:  python3 manifold-maldistribution.py   (prints all tables, ~10 s)
"""
from __future__ import annotations
import math
import numpy as np
from scipy.optimize import brentq

# ---------------------------------------------------------------- fluid / solid
RHO, MU, CP, KF = 1005.0, 1.25e-3, 3930.0, 0.52   # PG25 @ ~50 C
LPM = 1.0 / 60.0 / 1000.0                          # m3/s per LPM

# ---------------------------------------------------------------- friction
def fRe_rect_darcy(alpha):
    """Darcy f*Re for laminar fully developed flow in a rectangular duct
    (Shah & London polynomial, Darcy = 4 x Fanning). alpha = short/long side."""
    a = np.asarray(alpha, dtype=float)
    return 96.0 * (1 - 1.3553 * a + 1.9467 * a**2 - 1.7012 * a**3 + 0.9564 * a**4 - 0.2537 * a**5)


def f_darcy(Re, alpha):
    Re = np.maximum(np.asarray(Re, dtype=float), 1e-9)
    lam = fRe_rect_darcy(alpha) / Re
    turb = 0.316 * Re**-0.25
    w = np.clip((Re - 2300.0) / 1700.0, 0.0, 1.0)
    return (1 - w) * lam + w * turb


def rect(w, h):
    """area, hydraulic diameter, aspect ratio of a w x h rectangle (m)."""
    return w * h, 2 * w * h / (w + h), min(w, h) / max(w, h)


# ---------------------------------------------------------------- branch law
class Branch:
    """dp = R1*q + R2*q|q|  (laminar linear + minor-loss quadratic)."""
    def __init__(self, R1: float, R2: float, parts: dict | None = None):
        self.R1, self.R2, self.parts = float(R1), float(R2), parts or {}

    def dp(self, q):
        q = np.asarray(q, dtype=float)
        return self.R1 * q + self.R2 * q * np.abs(q)

    def q(self, dp):
        dp = np.asarray(dp, dtype=float)
        s = np.sign(dp)
        a = np.abs(dp)
        if self.R2 < 1e-30:
            return s * a / self.R1
        return s * (-self.R1 + np.sqrt(self.R1**2 + 4 * self.R2 * a)) / (2 * self.R2)

    def breakdown(self, q):
        """component dp at flow q (Pa) from the stored parts {name: (R1_i, R2_i)}."""
        return {k: v[0] * q + v[1] * q * q for k, v in self.parts.items()}


# ---------------------------------------------------------------- manifold marching
def dividing_profile(q, A, Dh, alpha, dL, theta_d):
    """Static pressure at each branch node of a dividing header fed at node 0.
    A, Dh, alpha: arrays (per segment downstream of node k). Returns p (Pa, p_arrive[0]=0),
    segment velocities, and the (momentum, friction) totals for bookkeeping."""
    N = len(q)
    Q = q.sum()
    Qseg = Q - np.cumsum(q)                      # flow downstream of node k
    Qseg[-1] = max(Qseg[-1], 0.0)
    useg = Qseg / A
    u_arr = np.empty(N)
    u_arr[0] = Q / A[0]
    u_arr[1:] = useg[:-1]
    rec = theta_d * RHO * (u_arr**2 - useg**2) / 2
    Re = RHO * np.abs(useg) * Dh / MU
    fric = f_darcy(Re, alpha) * dL / Dh * RHO * useg**2 / 2
    step = rec - fric                            # change from p_arr[k] to p_arr[k+1]
    p_arr = np.concatenate(([0.0], np.cumsum(step[:-1])))
    p_leave = p_arr + rec
    p_br = 0.5 * (p_arr + p_leave)
    return p_br, useg, rec.sum(), fric[:-1].sum()


def combining_profile(q, A, Dh, alpha, dL, theta_c, exit_node=0):
    """Static pressure at each node of a combining header exiting at node 0
    (exit_node=0) or at node N-1 (mirror). p = 0 at the exit."""
    if exit_node != 0:
        p, v, m, f = combining_profile(q[::-1], A[::-1], Dh[::-1], alpha[::-1], dL, theta_c, 0)
        return p[::-1], v[::-1], m, f
    N = len(q)
    Q = q.sum()
    Qseg = Q - np.cumsum(q)                      # flow in segment k (toward node 0) = sum_{j>k} q_j
    Qseg[-1] = max(Qseg[-1], 0.0)
    vseg = Qseg / A                              # velocity arriving at node k from segment k
    v_leave = np.empty(N)
    v_leave[0] = Q / A[0]                        # toward the exit port
    v_leave[1:] = vseg[:-1]
    drop = theta_c * RHO * (v_leave**2 - vseg**2) / 2
    Re = RHO * np.abs(vseg) * Dh / MU
    fric = f_darcy(Re, alpha) * dL / Dh * RHO * vseg**2 / 2
    # p_arr[k] = p_arr[k+1] - drop[k+1] - fric[k]  (marching from the dead end, p_arr[N-1] = 0)
    step = np.empty(N)                           # step[k] = p_arr[k] - p_arr[k+1] for k < N-1
    step[:-1] = -(drop[1:] + fric[:-1])
    step[-1] = 0.0
    p_arr = np.cumsum(step[::-1])[::-1] - step[-1]
    p_arr = p_arr - p_arr[-1]
    p_leave = p_arr - drop
    shift = p_leave[0]
    p_br = 0.5 * (p_arr + p_leave) - shift
    return p_br, vseg, drop.sum(), fric[:-1].sum()


def solve_manifold(Q, N, dL, geo_in, geo_out, branch: Branch, config="U",
                   theta_d=1.0, theta_c=2.0, tol=1e-6, maxit=3000, omega=0.25):
    """geo_in/geo_out: (A, Dh, alpha) arrays of length N (per segment).
    config 'U': outlet exits at node 0 (same end as inlet feed); 'Z': at node N-1.
    Returns dict with branch flows q, node pressures, driving dp D (inlet node 0 ->
    outlet exit), velocities, bookkeeping."""
    A_in, Dh_in, al_in = geo_in
    A_out, Dh_out, al_out = geo_out
    q = np.full(N, Q / N)
    exit_node = 0 if config == "U" else N - 1
    err_prev = np.inf
    for it in range(maxit):
        p_in, u_in, rec_in, fr_in = dividing_profile(q, A_in, Dh_in, al_in, dL, theta_d)
        p_out, v_out, drop_out, fr_out = combining_profile(q, A_out, Dh_out, al_out, dL, theta_c, exit_node)
        dp0 = p_in - p_out
        lo = -dp0.max() - 1.0
        hi = -dp0.min() + float(branch.dp(20 * Q / N)) + 1.0
        D = brentq(lambda d: branch.q(dp0 + d).sum() - Q, lo, hi, xtol=1e-9)
        q_new = branch.q(dp0 + D)
        err = np.max(np.abs(q_new - q)) / (Q / N)
        if err > err_prev * 1.2:
            omega = max(omega * 0.5, 0.02)
        err_prev = err
        q = (1 - omega) * q + omega * q_new
        if err < tol:
            break
    valid = bool(np.all(q > 0) and D > 0 and err < 1e-3)
    maxmin = q.max() / q.min() if valid else float("nan")
    return dict(q=q, p_in=p_in + D, p_out=p_out, D=D, u_in=u_in, v_out=v_out,
                mom_in=rec_in, fric_in=fr_in, mom_out=drop_out, fric_out=fr_out,
                iters=it + 1, err=err, maxmin=maxmin, valid=valid,
                span=(q.max() - q.min()) / q.mean())


# ---------------------------------------------------------------- geometry builders
def header_geo(w, h, N, taper=1.0):
    """Header segment areas along N nodes; taper = area at dead end / area at feed
    (linear in area, width w kept, height reduced)."""
    frac = np.linspace(1.0, taper, N)
    hs = h * frac
    A = w * hs
    Dh = 2 * w * hs / (w + hs)
    al = np.minimum(w, hs) / np.maximum(w, hs)
    return A, Dh, al


def slot_geo(w, d, M, taper=1.0):
    return header_geo(w, d, M, taper)


# ---------------------------------------------------------------- Level-3 branch (per slot segment)
def channel_branch(b, t, H, P, w_o, w_or, dLy, K_turn=1.0):
    """Branch law for the flow q leaving one dLy-long segment of an inlet slot:
    descent through the inlet opening into the fin gaps -> half goes each way along
    channels of length L_ch = P/2 -> ascent through the return opening."""
    phi = b / (b + t)                       # open fraction of the fin array
    n_side = dLy / (b + t)                  # channels per side in this segment
    A_side = n_side * b * H                 # flow area, one side (carries q/2)
    A_ch, Dh, al = rect(b, H)
    L_ch = P / 2
    # laminar friction: dp = fRe_D * mu * u * L / (2 Dh^2), u = (q/2)/A_side
    R1_ch = fRe_rect_darcy(al) * MU * L_ch / (2 * Dh**2) / (2 * A_side)
    R2_turn = 2 * K_turn * RHO / (2 * (2 * A_side)**2)          # two 90 deg turns on u_ch
    A_do = dLy * w_o * phi                                       # descending area (between fins)
    A_uo = dLy * w_or * phi
    K_do = 1.0 + 0.5 * (1 - phi)                                 # turn + contraction into gaps
    K_uo = 1.0 + (1 - phi)**2                                    # turn + expansion out of gaps
    R2_do = K_do * RHO / (2 * A_do**2)
    R2_uo = K_uo * RHO / (2 * A_uo**2)
    parts = {"opening_in": (0.0, R2_do), "channel_friction": (R1_ch, 0.0),
             "channel_turns": (0.0, R2_turn), "opening_out": (0.0, R2_uo)}
    br = Branch(R1_ch, R2_do + R2_turn + R2_uo, parts)
    br.u_ch = lambda q: (q / 2) / A_side
    br.u_do = lambda q: q / A_do
    br.u_uo = lambda q: q / A_uo
    br.Re_ch = lambda q: RHO * (q / 2) / A_side * Dh / MU
    return br


# ---------------------------------------------------------------- Level 2 (one slot pair)
def solve_slot_pair(q_slot, Ls, dLy, w_s, d_s, w_r, d_r, br3: Branch, config="U",
                    taper=1.0, theta_d=1.0, theta_c=2.0):
    M = int(round(Ls / dLy))
    gin = slot_geo(w_s, d_s, M, taper)
    gout = slot_geo(w_r, d_r, M, 1.0)
    r = solve_manifold(q_slot, M, dLy, gin, gout, br3, config, theta_d, theta_c)
    r["u_s0"] = q_slot / (w_s * d_s)
    r["u_r_exit"] = q_slot / (w_r * d_r)
    r["Re_s0"] = RHO * r["u_s0"] * gin[1][0] / MU
    r["u_ch_max"] = float(br3.u_ch(r["q"].max()))
    r["u_do_max"] = float(br3.u_do(r["q"].max()))
    r["M"] = M
    return r


def fit_branch_from_slot(q_nom, slot_fn, A_s_entry, A_h_in, A_r_exit, A_h_out, n_ends=1):
    """Fit R1,R2 to the slot-pair dp(q) over 0.5..1.5 q_nom and add tee losses.
    slot_fn(q) -> dict from solve_slot_pair for a slot carrying q (full slot flow).
    n_ends: 1 = slot fed from one end; 2 = centre-fed (two half slots each q/2)."""
    qs = q_nom * np.array([0.5, 0.75, 1.0, 1.25, 1.5])
    sols = [slot_fn(q) for q in qs]
    dps = np.array([sl["D"] for sl in sols])
    if (not all(sl["valid"] for sl in sols)) or np.any(dps <= 0) or np.any(np.diff(dps) <= 0):
        return None, (float("nan"), float("nan"))
    X = np.vstack([qs, qs**2]).T
    R1, R2 = np.linalg.lstsq(X, dps, rcond=None)[0]
    if R1 < 0 or R2 < 0:          # keep monotonic law: fall back to a pure power fit through nominal point
        R1, R2 = max(R1, 0.0), max(R2, 0.0)
        if R1 + R2 == 0:
            return None, (float("nan"), float("nan"))
    # tee entry: turn (K=1) + contraction into slot on slot entry velocity (per end)
    A_e = A_s_entry * n_ends
    K_in = 1.0 + 0.5 * (1 - min(A_s_entry / A_h_in, 1.0))
    R2_in = K_in * RHO / (2 * A_e**2)
    A_x = A_r_exit * n_ends
    K_out = 1.0 + (1 - min(A_r_exit / A_h_out, 1.0))**2
    R2_out = K_out * RHO / (2 * A_x**2)
    parts = {"tee_in": (0.0, R2_in), "slot_pair": (R1, R2), "tee_out": (0.0, R2_out)}
    return Branch(R1, R2 + R2_in + R2_out, parts), (R1, R2)


# ---------------------------------------------------------------- Plate model
class Plate:
    def __init__(self, Q_lpm=18.0, W=0.108, P=4e-3, w_o=0.4e-3, w_s=0.4e-3, d_s=3e-3,
                 w_r=None, d_r=None, b=0.1e-3, t=0.1e-3, H=1.0e-3, hdr=(6e-3, 10e-3),
                 hdr_out=None, hdr_taper=1.0, slot_taper=1.0, config="U", dLy=2e-3,
                 port_d=12.7e-3, uqd_cv=3.5, theta_d=1.0, theta_c=2.0, name=""):
        self.__dict__.update(locals()); del self.__dict__["self"]
        self.w_r = w_r if w_r is not None else w_s
        self.d_r = d_r if d_r is not None else d_s
        self.hdr_out = hdr_out if hdr_out is not None else hdr
        self.Q = Q_lpm * LPM
        self.N = int(round(W / P))                 # inlet slots (and return slots)
        self.w_or = w_o

    def run(self):
        c = self.config
        Q, N, W = self.Q, self.N, self.W
        br3 = channel_branch(self.b, self.t, self.H, self.P, self.w_o, self.w_or, self.dLy)
        # ---- Level 2 definition depends on config
        if c in ("C", "CC"):  # centre-fed: half-length slots each carrying q/2. C: returns exit at the edges (Z halves);
            #                    CC: returns collected at the centre too (U halves, both L1 headers on the centre line)
            Ls, slot_cfg, n_ends = W / 2, ("Z" if c == "C" else "U"), 2
            def slot_fn(q):
                return solve_slot_pair(q / 2, Ls, self.dLy, self.w_s, self.d_s, self.w_r, self.d_r,
                                       br3, slot_cfg, self.slot_taper, self.theta_d, self.theta_c)
        else:
            Ls, slot_cfg, n_ends = W, c, 1
            def slot_fn(q):
                return solve_slot_pair(q, Ls, self.dLy, self.w_s, self.d_s, self.w_r, self.d_r,
                                       br3, slot_cfg, self.slot_taper, self.theta_d, self.theta_c)
        self.slot_fn = slot_fn
        q_nom = Q / N
        A_s = self.w_s * self.d_s
        A_r = self.w_r * self.d_r
        A_h = self.hdr[0] * self.hdr[1]
        A_ho = self.hdr_out[0] * self.hdr_out[1]
        br2, (R1s, R2s) = fit_branch_from_slot(q_nom, slot_fn, A_s, A_h, A_r, A_ho, n_ends)
        if br2 is None:
            s_nom = slot_fn(q_nom)
            self.res = dict(valid=False, reason="along-slot back-flow (slot dynamic pressure >> branch dp)",
                            u_s0=s_nom["u_s0"], q_dyn_s=RHO * s_nom["u_s0"]**2 / 2, s_nom=s_nom, N=N,
                            maxmin_slot=float("nan"), maxmin_y=float("nan"), maxmin_global=float("nan"),
                            phi_min_global=float("nan"), dp_internal=float("nan"), dp_with_uqd=float("nan"),
                            branch_dp_nom=float("nan"), q_dyn_h=float("nan"), u_h0=float("nan"),
                            seg_dp_nom=float(br3.dp(q_nom / s_nom["M"])), u_ch_max=float("nan"), Re_ch=float("nan"))
            return self.res
        # ---- Level 1
        if c in ("C", "CC"):
            # half plate: N_h slots, Q/2 in each half of the centre inlet header (port at plate centre).
            # C : two edge outlet headers (area 2*A_ho in parallel) each half Q/4, ports at edge mid-length -> U
            # CC: one outlet header beside the inlet header on the centre line, Q/2 per half -> U
            N1 = int(math.ceil(N / 2))
            Q1 = Q * N1 / N
            gin = header_geo(self.hdr[0], self.hdr[1], N1, self.hdr_taper)
            mult = 2 if c == "C" else 1
            gout = header_geo(self.hdr_out[0] * mult, self.hdr_out[1], N1, 1.0)
            r1 = solve_manifold(Q1, N1, self.P, gin, gout, br2, "U", self.theta_d, self.theta_c)
            u_h0 = (Q / 2) / A_h
            u_ho = (Q / 2) / (mult * A_ho)
        else:
            gin = header_geo(self.hdr[0], self.hdr[1], N, self.hdr_taper)
            gout = header_geo(self.hdr_out[0], self.hdr_out[1], N, 1.0)
            r1 = solve_manifold(Q, N, self.P, gin, gout, br2, c, self.theta_d, self.theta_c)
            u_h0 = Q / A_h
            u_ho = Q / A_ho
        q1 = r1["q"]
        if not r1["valid"]:
            s_nom = slot_fn(q_nom)
            self.res = dict(valid=False, reason="slot-to-slot back-flow (header dynamic pressure >> branch dp)",
                            u_s0=s_nom["u_s0"], q_dyn_s=RHO * s_nom["u_s0"]**2 / 2, s_nom=s_nom, N=N, q1=q1,
                            maxmin_slot=float("nan"), maxmin_y=s_nom["maxmin"], maxmin_global=float("nan"),
                            phi_min_global=float("nan"), dp_internal=float("nan"), dp_with_uqd=float("nan"),
                            branch_dp_nom=float(br2.dp(q_nom)), q_dyn_h=RHO * u_h0**2 / 2, u_h0=u_h0,
                            seg_dp_nom=float(br3.dp(s_nom["q"].mean())), u_ch_max=s_nom["u_ch_max"],
                            Re_ch=float(br3.Re_ch(s_nom["q"].mean())))
            return self.res
        # ---- along-slot profiles for the min / max slot
        s_min = slot_fn(q1.min()); s_max = slot_fn(q1.max()); s_nom = slot_fn(q_nom)
        phi_slot = q1 / q1.mean()
        phi_y_min = s_min["q"] / s_min["q"].mean()
        phi_y_max = s_max["q"] / s_max["q"].mean()
        glob_min = phi_slot.min() * phi_y_min.min()
        glob_max = phi_slot.max() * phi_y_max.max()
        # ---- dp bookkeeping (Pa) at nominal/mean flows
        A_port = math.pi * self.port_d**2 / 4
        u_port = Q / A_port
        dp_port = 2 * 1.0 * RHO * u_port**2 / 2 + (1 - A_port / A_h)**2 * RHO * u_port**2 / 2 \
                  + 0.5 * (1 - A_port / A_ho) * RHO * u_port**2 / 2     # 2 turns + expansion + contraction
        gpm = self.Q / LPM / 3.785
        dp_uqd = 2 * (gpm / self.uqd_cv)**2 * 6894.76                    # pair, Cv law, SG~1
        b2 = br2.breakdown(q_nom)
        b3 = br3.breakdown(s_nom["q"].mean())
        comp = {
            "UQD pair (Cv %.1f)" % self.uqd_cv: dp_uqd,
            "ports (%.1f mm bore, 2 turns, exp/contr)" % (self.port_d * 1e3): dp_port,
            "L1 inlet header (friction - recovery)": r1["fric_in"] - r1["mom_in"],
            "L1 outlet header (friction + momentum)": r1["fric_out"] + r1["mom_out"],
            "L1->L2 tee entry": b2["tee_in"],
            "L2 inlet slot (friction - recovery)": s_nom["fric_in"] - s_nom["mom_in"],
            "L2 return slot (friction + momentum)": s_nom["fric_out"] + s_nom["mom_out"],
            "L3 opening in (turn+contraction)": b3["opening_in"],
            "L3 channel laminar friction": b3["channel_friction"],
            "L3 channel 2x90deg turns": b3["channel_turns"],
            "L3 opening out (turn+expansion)": b3["opening_out"],
            "L2->L1 tee exit": b2["tee_out"],
        }
        # exact plate dp (header node0 -> outlet exit) = r1['D']; add ports and UQD
        dp_internal = r1["D"] + dp_port
        self.res = dict(
            r1=r1, s_nom=s_nom, s_min=s_min, s_max=s_max, br2=br2, br3=br3, comp=comp,
            dp_internal=dp_internal, dp_with_uqd=dp_internal + dp_uqd, dp_uqd=dp_uqd,
            maxmin_slot=r1["maxmin"], maxmin_y=s_nom["maxmin"], maxmin_global=glob_max / glob_min,
            phi_min_global=glob_min, phi_max_global=glob_max,
            u_port=u_port, u_h0=u_h0, u_ho=u_ho, u_s0=s_max["u_s0"], u_r_exit=s_max["u_r_exit"],
            u_ch_max=s_max["u_ch_max"], u_do_max=s_max["u_do_max"], Re_ch=float(br3.Re_ch(s_nom["q"].mean())),
            branch_dp_nom=float(br2.dp(q_nom)), slot_dp_nom=R1s * q_nom + R2s * q_nom**2,
            seg_dp_nom=float(br3.dp(s_nom["q"].mean())),
            q_dyn_h=RHO * u_h0**2 / 2, q_dyn_s=RHO * s_nom["u_s0"]**2 / 2,
            N=N, q1=q1, valid=True,
        )
        return self.res


def dT_hot_caloric(phi_min, Q_lpm):
    """Extra local caloric temperature rise (K) in the most starved segment for a
    single-pass array: the segment's mean coolant rise is 0.5*dT_out/phi."""
    dT_out = 15000 / (Q_lpm * LPM * RHO * CP)
    if not np.isfinite(phi_min) or phi_min <= 0:
        return float("nan")
    return 0.5 * dT_out * (1 / phi_min - 1)


# ---------------------------------------------------------------- reporting helpers
def kpa(x): return x / 1e3


def line(*cols, w=None):
    print("| " + " | ".join(str(c) for c in cols) + " |")


def run_and_row(label, **kw):
    p = Plate(name=label, **kw)
    r = p.run()
    return p, r



def fmt(x, nd=2):
    return "backflow" if (x is None or not np.isfinite(x)) else f"{x:.{nd}f}"


def main():
    np.set_printoptions(precision=2, suppress=True, linewidth=150)
    print("# Manifold maldistribution / pressure-drop network model (HMMC, 108 x 108 mm, PG25)\n")

    # ------------------------------------------------------------------ 0. Level-3 branch alone
    print("## 0. Per-segment branch (opening + channel + turns) at uniform flow, 18 LPM, P = 4 mm, 27 inlet slots")
    print("| gap=fin mm | H mm | w_o mm | u_ch m/s | Re_ch | opening in Pa | channel friction Pa | turns Pa | opening out Pa | branch dp Pa |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for (g, H, wo) in [(0.1, 1.0, 0.4), (0.1, 1.0, 0.15), (0.075, 1.0, 0.4), (0.05, 1.0, 0.4), (0.05, 0.6, 0.4), (0.15, 1.0, 0.4), (0.15, 1.5, 0.4)]:
        br = channel_branch(g * 1e-3, g * 1e-3, H * 1e-3, 4e-3, wo * 1e-3, wo * 1e-3, 2e-3)
        q_seg = 18 * LPM / 27 / 54
        b = br.breakdown(q_seg)
        print(f"| {g:.3f} | {H:.1f} | {wo:.2f} | {br.u_ch(q_seg):.3f} | {br.Re_ch(q_seg):.0f} | {b['opening_in']:.0f} | {b['channel_friction']:.0f} | "
              f"{b['channel_turns']:.0f} | {b['opening_out']:.0f} | {float(br.dp(q_seg)):.0f} |")
    print("(channel friction uses Darcy f*Re = 4 x Fanning; the 1-D scoping model used Fanning fRe in the Darcy formula and under-predicts channel friction 4x.)\n")

    # ------------------------------------------------------------------ 1. Along-slot (Level 2) non-uniformity
    print("## 1. Along-slot non-uniformity (Level 2): one slot pair, q_slot = 18 LPM / 27 = 0.667 LPM, fins 0.1/0.1 x 1.0, P = 4 mm")
    print("| slot w x d mm | w_o mm | feed | taper | u_s0 m/s | Re_s0 | q_dyn_s kPa | branch dp kPa | dp_br/q_dyn | max/min along slot | phi_min | slot-pair dp kPa | dT_hot K |")
    print("|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    q_slot = 18 * LPM / 27
    cases = [((0.4, 3), 0.4, [1.0]), ((0.4, 6), 0.4, [1.0]), ((1.0, 3), 0.4, [1.0]), ((1.5, 3), 0.4, [1.0]),
             ((1.5, 4), 0.4, [1.0, 0.5]), ((1.5, 6), 0.4, [1.0, 0.5, 0.3]), ((1.5, 8), 0.4, [1.0]),
             ((1.5, 6), 0.15, [1.0, 0.5]), ((1.5, 8), 0.15, [1.0])]
    for (ws, ds), wo, tapers in cases:
        br = channel_branch(0.1e-3, 0.1e-3, 1.0e-3, 4e-3, wo * 1e-3, wo * 1e-3, 2e-3)
        for feed in ["U", "Z", "C", "CC"]:
            for taper in tapers:
                if feed in ("C", "CC"):
                    r = solve_slot_pair(q_slot / 2, 0.054, 2e-3, ws * 1e-3, ds * 1e-3, ws * 1e-3, ds * 1e-3, br, "Z" if feed == "C" else "U", taper)
                else:
                    r = solve_slot_pair(q_slot, 0.108, 2e-3, ws * 1e-3, ds * 1e-3, ws * 1e-3, ds * 1e-3, br, feed, taper)
                phi = r["q"] / r["q"].mean()
                qd = RHO * r["u_s0"]**2 / 2
                bdp = float(br.dp(r["q"].mean()))
                ok = r["valid"]
                print(f"| {ws:.1f} x {ds:.0f} | {wo:.2f} | {feed} | {taper:.1f} | {r['u_s0']:.2f} | {r['Re_s0']:.0f} | {kpa(qd):.2f} | {kpa(bdp):.2f} | {bdp/qd:.1f} | "
                      f"{fmt(r['maxmin'])} | {fmt(phi.min() if ok else float('nan'))} | {fmt(kpa(r['D']) if ok else float('nan'))} | "
                      f"{fmt(dT_hot_caloric(phi.min(), 18) if ok else float('nan'), 1)} |")
    print("\nfeed: U = fed and returned at the same slot end (both headers on one edge); Z = opposite ends; "
          "C = centre-fed inlet slot, returns exit at both ends (half-length, half-flow Z halves); "
          "CC = centre-fed inlet and centre-collected return (half-length, half-flow U halves).")
    print("taper = inlet-slot area at dead end / at feed. 'backflow' = manifold momentum/friction exceeds the branch resistance; "
          "flow reverses in part of the slot and the 1-D model is no longer meaningful (the design is unusable).\n")

    br = channel_branch(0.1e-3, 0.1e-3, 1.0e-3, 4e-3, 0.4e-3, 0.4e-3, 2e-3)
    for (ws, ds, feed, lab) in [(1.5, 6, "U", "1.5 x 6 mm slot, U feed"), (1.5, 6, "Z", "1.5 x 6 mm slot, Z feed"),
                                (1.5, 6, "C", "1.5 x 6 mm slot, centre-fed C (half slot, Z)"), (1.5, 6, "CC", "1.5 x 6 mm slot, centre-fed/collected CC (half slot, U)")]:
        if feed in ("C", "CC"):
            r = solve_slot_pair(q_slot / 2, 0.054, 2e-3, ws * 1e-3, ds * 1e-3, ws * 1e-3, ds * 1e-3, br, "Z" if feed == "C" else "U")
        else:
            r = solve_slot_pair(q_slot, 0.108, 2e-3, ws * 1e-3, ds * 1e-3, ws * 1e-3, ds * 1e-3, br, feed)
        phi = r["q"] / r["q"].mean()
        print(f"Along-slot profile, {lab} (phi every 5th 2-mm segment from the fed end): {np.round(phi[::5], 2)}")
        print(f"   inlet slot: recovery {r['mom_in']:.0f} Pa, friction {r['fric_in']:.0f} Pa; return slot: momentum {r['mom_out']:.0f} Pa, friction {r['fric_out']:.0f} Pa")
    print()

    # ------------------------------------------------------------------ 2. Slot-to-slot (Level 1) non-uniformity vs header size
    print("## 2. Slot-to-slot non-uniformity (Level 1) vs header cross-section, taper, config")
    print("Slots 1.5 x 6 mm (w_o 0.4), fins 0.1/0.1 x 1.0 mm, P = 4 mm, 27 inlet slots. 'global' = slot-to-slot x along-slot.")
    for Qlpm in (18.0, 36.0):
        print(f"\n### {Qlpm:.0f} LPM")
        print("| header w x h mm | config | taper | u_h0 m/s | q_dyn_h kPa | L1 branch dp kPa | dp_br/q_dyn | slot-slot max/min | along-slot max/min | global max/min | phi_min | dT_hot K | plate dp (no UQD) kPa |")
        print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for hdr in [(4, 8), (6, 10), (8, 12), (10, 15), (12, 20)]:
            for cfg in ["U", "Z", "C", "CC"]:
                for taper in [1.0, 0.5]:
                    if taper != 1.0 and hdr not in [(6, 10), (8, 12)]:
                        continue
                    p, r = run_and_row("", Q_lpm=Qlpm, w_s=1.5e-3, d_s=6e-3, hdr=(hdr[0] * 1e-3, hdr[1] * 1e-3),
                                       hdr_taper=taper, config=cfg)
                    ratio = r["branch_dp_nom"] / r["q_dyn_h"] if np.isfinite(r["q_dyn_h"]) else float("nan")
                    print(f"| {hdr[0]} x {hdr[1]} | {cfg} | {taper:.1f} | {fmt(r['u_h0'])} | {fmt(kpa(r['q_dyn_h']))} | {fmt(kpa(r['branch_dp_nom']))} | "
                          f"{fmt(ratio,1)} | {fmt(r['maxmin_slot'])} | {fmt(r['maxmin_y'])} | {fmt(r['maxmin_global'])} | {fmt(r['phi_min_global'])} | "
                          f"{fmt(dT_hot_caloric(r['phi_min_global'], Qlpm),1)} | {fmt(kpa(r['dp_internal']),1)} |")

    for cfg in ["U", "Z"]:
        p, r = run_and_row("", Q_lpm=18, w_s=1.5e-3, d_s=6e-3, hdr=(8e-3, 12e-3), config=cfg)
        if r["valid"]:
            print(f"\nSlot-to-slot profile, 8 x 12 header, {cfg}, 18 LPM (phi per slot from the port end): {np.round(r['q1'] / r['q1'].mean(), 2)}")
            r1 = r["r1"]
            print(f"   inlet header: recovery {r1['mom_in']:.0f} Pa, friction {r1['fric_in']:.0f} Pa; outlet header: momentum {r1['mom_out']:.0f} Pa, friction {r1['fric_out']:.0f} Pa")
    print()

    # ------------------------------------------------------------------ 3. Design-rule sweep
    print("## 3. Design rule: Level-1 slot-to-slot max/min vs (L1 branch dp / header-inlet dynamic pressure)")
    print("Header area scanned (square section), slots 1.5 x 6 (w_o 0.4), 18 LPM. For C the dynamic pressure is that of the half-flow.")
    print("| header area mm2 | u_h0 (U/Z) m/s | dp_br/q_dyn (U) | U max/min | Z max/min | dp_br/q_dyn (C) | C max/min | dp_br/q_dyn (CC) | CC max/min |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for Ah in [32, 48, 60, 80, 96, 120, 150, 200, 300, 400, 600]:
        side = math.sqrt(Ah) * 1e-3
        out = {}
        for cfg in ["U", "Z", "C", "CC"]:
            p, r = run_and_row("", Q_lpm=18, w_s=1.5e-3, d_s=6e-3, hdr=(side, side), config=cfg)
            out[cfg] = r
        def ratio(r):
            return r["branch_dp_nom"] / r["q_dyn_h"] if np.isfinite(r["q_dyn_h"]) else float("nan")
        print(f"| {Ah} | {fmt(out['U']['u_h0'])} | {fmt(ratio(out['U']),1)} | {fmt(out['U']['maxmin_slot'],3)} | {fmt(out['Z']['maxmin_slot'],3)} | "
              f"{fmt(ratio(out['C']),1)} | {fmt(out['C']['maxmin_slot'],3)} | {fmt(ratio(out['CC']),1)} | {fmt(out['CC']['maxmin_slot'],3)} |")
    print()

    # ------------------------------------------------------------------ 4. Channel width sensitivity
    print("## 4. Channel-width sensitivity (fin = gap), slots 1.5 x 6 (w_o 0.4), P = 4 mm, header 10 x 15 centre-fed/collected (CC), 18 LPM")
    print("| gap mm | H mm | u_ch m/s | Re_ch | seg branch dp Pa | along-slot max/min | slot-slot max/min | global max/min | dT_hot K | plate dp kPa |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for (g, H) in [(0.05, 1.0), (0.05, 0.6), (0.075, 1.0), (0.075, 0.8), (0.1, 1.0), (0.15, 1.0), (0.15, 1.5)]:
        p, r = run_and_row("", Q_lpm=18, b=g * 1e-3, t=g * 1e-3, H=H * 1e-3, w_s=1.5e-3, d_s=6e-3, hdr=(10e-3, 15e-3), config="CC")
        print(f"| {g:.3f} | {H:.1f} | {fmt(r['u_ch_max'],3)} | {fmt(r['Re_ch'],0)} | {fmt(r['seg_dp_nom'],0)} | {fmt(r['maxmin_y'])} | {fmt(r['maxmin_slot'])} | "
              f"{fmt(r['maxmin_global'])} | {fmt(dT_hot_caloric(r['phi_min_global'], 18),1)} | {fmt(kpa(r['dp_internal']),1)} |")
    print()

    # ------------------------------------------------------------------ 5. Pitch / flow-length sensitivity
    print("## 5. Slot pitch / channel flow length (fins 0.075/0.075 x 1.0 mm, slot width = P/2 - 0.5 mm wall, w_o = slot width, depth 6 mm, header 10 x 15, 18 LPM)")
    print("| P mm | L_ch mm | N slots | slot w mm | config | u_s0 m/s | seg branch dp Pa | slot-pair dp kPa | along-slot max/min | slot-slot max/min | global | dT_hot K | plate dp kPa |")
    print("|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    for P in [4, 6, 8, 12]:
        ws = P / 2 - 0.5
        for cfg in ["U", "C", "CC"]:
            p, r = run_and_row("", Q_lpm=18, P=P * 1e-3, b=0.075e-3, t=0.075e-3, H=1.0e-3, w_o=ws * 1e-3, w_s=ws * 1e-3, d_s=6e-3,
                               hdr=(10e-3, 15e-3), config=cfg)
            print(f"| {P} | {P/2:.0f} | {r['N']} | {ws:.1f} | {cfg} | {fmt(r['u_s0'])} | {fmt(r['seg_dp_nom'],0)} | {fmt(kpa(r.get('slot_dp_nom', float('nan'))))} | "
                  f"{fmt(r['maxmin_y'])} | {fmt(r['maxmin_slot'])} | {fmt(r['maxmin_global'])} | {fmt(dT_hot_caloric(r['phi_min_global'], 18),1)} | {fmt(kpa(r['dp_internal']),1)} |")
    print()

    # ------------------------------------------------------------------ 6. Search for designs meeting global max/min <= 1.10
    print("## 6. Search: smallest manifold meeting global max/min <= 1.10 at 18 LPM; dp = plate port-to-port without UQD, 16 mm ports")
    print("Slot depth scanned 4/6/8 mm, header 8x12 / 10x15 / 12x20 / 15x25 mm. Area ratio = total header area (both halves) / total slot entry area.")
    print("| P mm | gap mm | H mm | w_o mm | config | slot w x d mm | header mm | A_hdr/A_slots | u_s0 m/s | u_h0 m/s | dp_br/q_dyn_slot | along-slot | slot-slot | global | plate dp kPa | dp @36 LPM kPa | global @36 |")
    print("|---:|---:|---:|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    found = []
    for P, g, H in [(4, 0.1, 1.0), (4, 0.075, 1.0), (4, 0.05, 0.8), (6, 0.075, 1.0), (8, 0.075, 1.0), (8, 0.1, 1.0), (8, 0.05, 0.8), (12, 0.075, 1.0), (12, 0.1, 1.0)]:
        ws = P / 2 - 0.5
        for wo in ([ws, 0.15] if P == 4 else [ws]):
            for cfg in ["C", "CC"]:
                best = None
                for ds in [4, 6, 8]:
                    for hdr in [(8, 12), (10, 15), (12, 20), (15, 25)]:
                        kw = dict(P=P * 1e-3, b=g * 1e-3, t=g * 1e-3, H=H * 1e-3, w_o=wo * 1e-3, w_s=ws * 1e-3, d_s=ds * 1e-3,
                                  hdr=(hdr[0] * 1e-3, hdr[1] * 1e-3), config=cfg, port_d=16e-3)
                        p, r = run_and_row("", Q_lpm=18, **kw)
                        if r["valid"] and r["maxmin_global"] <= 1.10:
                            best = (ds, hdr, r, kw)
                            break
                    if best:
                        break
                if best:
                    ds, hdr, r, kw = best
                    p36, r36 = run_and_row("", Q_lpm=36, **kw)
                    N = r["N"]
                    ar = 2 * hdr[0] * hdr[1] / (N * ws * ds)
                    print(f"| {P} | {g:.3f} | {H:.1f} | {wo:.2f} | {cfg} | {ws:.1f} x {ds} | {hdr[0]} x {hdr[1]} | {ar:.2f} | {r['u_s0']:.2f} | {r['u_h0']:.2f} | "
                          f"{r['slot_dp_nom']/r['q_dyn_s']:.0f} | {r['maxmin_y']:.3f} | {r['maxmin_slot']:.3f} | {r['maxmin_global']:.3f} | {kpa(r['dp_internal']):.1f} | "
                          f"{fmt(kpa(r36['dp_internal']),1)} | {fmt(r36['maxmin_global'])} |")
                    found.append((P, g, H, wo, cfg, ds, hdr, r, kw))
                else:
                    print(f"| {P} | {g:.3f} | {H:.1f} | {wo:.2f} | {cfg} | none up to {ws:.1f} x 8 / 15 x 25 | | | | | | | | | | | |")
    print()

    # ------------------------------------------------------------------ 7. dp budgets
    print("## 7. Pressure-drop budgets (Pa). UQD pair by Cv law with Cv 3.5 (UQD08-class; +/-50 %).")
    designs = {
        "A": ("as specified: P 4, fins 0.1x1.0, slots 0.4 x 3 (w_o 0.4), 4x8 hdr Z, 12.7 mm ports",
              dict(w_s=0.4e-3, d_s=3e-3, w_o=0.4e-3, hdr=(4e-3, 8e-3), config="Z", port_d=12.7e-3)),
        "B": ("widened slots 1.5 x 6 (w_o 0.4), 8x12 hdr U, 12.7 mm ports",
              dict(w_s=1.5e-3, d_s=6e-3, w_o=0.4e-3, hdr=(8e-3, 12e-3), config="U", port_d=12.7e-3)),
        "C": ("P 4 orifice-regulated: w_o 0.15, slots 1.5 x 6, 10x15 hdr centre-fed, 16 mm ports",
              dict(w_s=1.5e-3, d_s=6e-3, w_o=0.15e-3, hdr=(10e-3, 15e-3), config="C", port_d=16e-3)),
        "D": ("P 8, fins 0.075x1.0, slots 3.5 x 6 (open), 10x15 hdr centre-fed, 16 mm ports",
              dict(P=8e-3, w_s=3.5e-3, d_s=6e-3, w_o=3.5e-3, b=0.075e-3, t=0.075e-3, H=1.0e-3, hdr=(10e-3, 15e-3), config="C", port_d=16e-3)),
        "E": ("D + inlet-slot taper 0.5 + header taper 0.5",
              dict(P=8e-3, w_s=3.5e-3, d_s=6e-3, w_o=3.5e-3, b=0.075e-3, t=0.075e-3, H=1.0e-3, hdr=(10e-3, 15e-3), config="C", port_d=16e-3,
                   slot_taper=0.5, hdr_taper=0.5)),
        "F": ("RECOMMENDED: as D but centre-fed AND centre-collected (CC), 16 mm ports",
              dict(P=8e-3, w_s=3.5e-3, d_s=6e-3, w_o=3.5e-3, b=0.075e-3, t=0.075e-3, H=1.0e-3, hdr=(10e-3, 15e-3), config="CC", port_d=16e-3)),
        "G": ("CC, P 4, fins 0.1x1.0, slots 1.5 x 6 (w_o 0.3), 10x15 hdr, 16 mm ports",
              dict(P=4e-3, w_s=1.5e-3, d_s=6e-3, w_o=0.3e-3, b=0.1e-3, t=0.1e-3, H=1.0e-3, hdr=(10e-3, 15e-3), config="CC", port_d=16e-3)),
        "H": ("RECOMMENDED: CC, P 8, fins 0.075x1.0, slots 3.5 x 8, inlet hdr 10x15, outlet hdr 14x20, 16 mm ports",
              dict(P=8e-3, w_s=3.5e-3, d_s=8e-3, w_o=3.5e-3, b=0.075e-3, t=0.075e-3, H=1.0e-3, hdr=(10e-3, 15e-3), hdr_out=(14e-3, 20e-3),
                   config="CC", port_d=16e-3)),
        "I": ("H scaled for 36 LPM: inlet hdr 14x20, outlet hdr 20x25, slots 3.5 x 10, 20 mm ports",
              dict(P=8e-3, w_s=3.5e-3, d_s=10e-3, w_o=3.5e-3, b=0.075e-3, t=0.075e-3, H=1.0e-3, hdr=(14e-3, 20e-3), hdr_out=(20e-3, 25e-3),
                   config="CC", port_d=20e-3)),
    }
    for k, (lab, kw) in designs.items():
        print(f"- **{k}**: {lab}")
    for Qlpm in (18.0, 36.0):
        print(f"\n### {Qlpm:.0f} LPM")
        res = {k: run_and_row(k, Q_lpm=Qlpm, **kw)[1] for k, (lab, kw) in designs.items()}
        print("| component (Pa) | " + " | ".join(designs.keys()) + " |")
        print("|---|" + "---:|" * len(designs))
        names = ["UQD pair", "internal ports (2 turns, expansion, contraction)", "L1 inlet header (friction - recovery)",
                 "L1 outlet header (friction + momentum)", "L1->L2 tee entry", "L2 inlet slot (friction - recovery)",
                 "L2 return slot (friction + momentum)", "L3 opening in (turn + contraction)", "L3 channel laminar friction",
                 "L3 channel 2 x 90 deg turns", "L3 opening out (turn + expansion)", "L2->L1 tee exit"]
        for i, nm in enumerate(names):
            vals = []
            for r in res.values():
                vals.append(list(r["comp"].values())[i] if r["valid"] else float("nan"))
            print(f"| {nm} | " + " | ".join(fmt(v, 0) for v in vals) + " |")
        print("| **plate dp port-to-port (exact network incl. ports)** | " + " | ".join(f"**{fmt(r['dp_internal'],0)}**" for r in res.values()) + " |")
        print("| **plate + UQD pair** | " + " | ".join(f"**{fmt(r['dp_with_uqd'],0)}**" for r in res.values()) + " |")
        print("| slot-to-slot max/min | " + " | ".join(fmt(r['maxmin_slot']) for r in res.values()) + " |")
        print("| along-slot max/min | " + " | ".join(fmt(r['maxmin_y']) for r in res.values()) + " |")
        print("| global max/min | " + " | ".join(fmt(r['maxmin_global']) for r in res.values()) + " |")
        print("| phi_min (most starved segment) | " + " | ".join(fmt(r['phi_min_global']) for r in res.values()) + " |")
        print("| caloric hot-spot penalty K | " + " | ".join(fmt(dT_hot_caloric(r['phi_min_global'], Qlpm), 1) for r in res.values()) + " |")
        print("| u port m/s | " + " | ".join(fmt(r.get('u_port', float('nan'))) for r in res.values()) + " |")
        print("| u header inlet m/s | " + " | ".join(fmt(r['u_h0']) for r in res.values()) + " |")
        print("| u slot entry m/s | " + " | ".join(fmt(r['u_s0']) for r in res.values()) + " |")
        print("| u opening (between fins) m/s | " + " | ".join(fmt(r.get('u_do_max', float('nan'))) for r in res.values()) + " |")
        print("| u channel m/s | " + " | ".join(fmt(r['u_ch_max'], 3) for r in res.values()) + " |")
        print("| pump power, plate only W | " + " | ".join(fmt(r['dp_internal'] * Qlpm * LPM, 1) for r in res.values()) + " |")

    # ------------------------------------------------------------------ 8. theta sensitivity on design D
    print("\n## 8. Momentum-coefficient sensitivity (designs D, F, H, 18 LPM)")
    print("| design | theta_d | theta_c | slot-slot max/min | along-slot max/min | global | plate dp kPa |")
    print("|---|---:|---:|---:|---:|---:|---:|")
    for dk in ["D", "F", "H"]:
        for td, tc in [(1.0, 2.0), (0.6, 1.5), (1.3, 2.0), (1.0, 1.0), (0.5, 2.5)]:
            p, r = run_and_row("", Q_lpm=18, theta_d=td, theta_c=tc, **designs[dk][1])
            print(f"| {dk} | {td} | {tc} | {fmt(r['maxmin_slot'],3)} | {fmt(r['maxmin_y'],3)} | {fmt(r['maxmin_global'],3)} | {fmt(kpa(r['dp_internal']),2)} |")
    # port-size sensitivity for F
    print("\nPort bore sensitivity, design H: " + "; ".join(
        f"{d} mm -> u {run_and_row('', Q_lpm=18, **{**designs['H'][1], 'port_d': d*1e-3})[1]['u_port']:.2f} m/s, plate dp "
        f"{kpa(run_and_row('', Q_lpm=18, **{**designs['H'][1], 'port_d': d*1e-3})[1]['dp_internal']):.1f} kPa @18 LPM, "
        f"{kpa(run_and_row('', Q_lpm=36, **{**designs['H'][1], 'port_d': d*1e-3})[1]['dp_internal']):.1f} kPa @36 LPM"
        for d in (12.7, 16, 20)))
    # flow sweep for H (laminar branch -> uniformity degrades with flow; thermal penalty does not)
    print("\nFlow sweep, design H (fixed geometry):")
    print("| LPM | plate dp kPa | slot-slot | along-slot | global | phi_min | caloric hot-spot penalty K | u header m/s | u port m/s |")
    print("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for Ql in (9, 12, 18, 24, 30, 36):
        p, r = run_and_row("", Q_lpm=Ql, **designs["H"][1])
        print(f"| {Ql} | {fmt(kpa(r['dp_internal']),1)} | {fmt(r['maxmin_slot'],3)} | {fmt(r['maxmin_y'],3)} | {fmt(r['maxmin_global'],3)} | "
              f"{fmt(r['phi_min_global'])} | {fmt(dT_hot_caloric(r['phi_min_global'], Ql),1)} | {fmt(r['u_h0'])} | {fmt(r['u_port'])} |")

    # ------------------------------------------------------------------ 9. UQD estimates
    print("\n## 9. Quick-disconnect allowance (Cv law dp = (gpm/Cv)^2 psi; Cv values are engineering estimates, +/-50 %)")
    print("| coupling | Cv (est.) | pair dp @18 LPM kPa | pair dp @36 LPM kPa |")
    print("|---|---:|---:|---:|")
    for name, cv in [("UQD04 (1/4 in)", 0.6), ("UQD06 (3/8 in)", 1.8), ("UQD08 (1/2 in)", 3.5), ("3/4 in barb / UQD12-class", 8.0)]:
        d18 = 2 * (18 / 3.785 / cv)**2 * 6.89476
        d36 = 2 * (36 / 3.785 / cv)**2 * 6.89476
        print(f"| {name} | {cv} | {d18:.0f} | {d36:.0f} |")


if __name__ == "__main__":
    main()
