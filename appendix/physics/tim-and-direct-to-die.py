#!/usr/bin/env python3
"""
tim-and-direct-to-die.py
Quantitative comparison of thermal-interface strategies for a 15 kW-class
direct-liquid-cooled cold plate (CoolIT 15 kW benchmark: 117 cm2 footprint,
128 W/cm2 uniform, 18 LPM PG25, 45 C inlet) and for the 300 W/cm2 hot-spot
regime of 2027-28 packages.

Sections
  1. TIM option matrix: R'' = BLT/k + R_contact, with min / nominal / max bands
  2. dT_TIM = q'' * R'' at 128, 200, 300, 500 W/cm2
  3. Full-stack case-to-inlet dT using the team's own 1-D model
     (docs/cooling/model/coldplate_model.py, HMMC-fine core)
  4. Package bow / bond-line non-uniformity (paraboloid bow, rigid plate)
  5. Ageing (pump-out / dry-out) end-of-life multipliers
  6. Ni barrier plating penalty for liquid metal (electroless Ni-P vs electrolytic Ni)
  7. Clamp force for the required contact pressure on a 117 cm2 / 16 cm2 footprint
  8. CTE shear at the interface for direct-to-die (Si on Cu vs CuW vs Si lid)
  9. Cost-per-unit order-of-magnitude

Provenance tags used in the printed tables:
  [DS]  vendor datasheet value quoted via sibling research notes (URL in report)
  [LIT] open literature / textbook physics (Prasher 2006 Proc. IEEE; Shah & London;
        DARPA ICECool reports) - from memory, no live fetch this session
  [MEM] engineering memory, order-of-magnitude, must be verified before use in a spec
  [M]   computed here or by the sibling scoping model
"""
from __future__ import annotations

import math
import sys

import numpy as np

sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '.')))
from coldplate_model import PG25, hmmc_design, coolit_like  # noqa: E402

FOOTPRINT_CM2 = 117.0          # calibrated TTV heater footprint (108 x 108 mm)
Q_BENCH = 15_000.0             # W
LPM_PER_KW = 1.2
Q_LIST = [128.0, 200.0, 300.0, 500.0]   # W/cm2
T_IN = 45.0
T_CASE_LIMIT = 85.0


def Rpp(blt_um: float, k: float, rc: float) -> float:
    """Unit thermal resistance in cm2K/W: bulk (BLT/k) + total contact rc (cm2K/W)."""
    return blt_um * 1e-6 / k * 1e4 + rc


# --------------------------------------------------------------------------
# 1. TIM option matrix
# Each option: physical model inputs for (min, nominal, max) R'' and metadata.
# R'' bands are built from BLT/k + contact and then clipped to datasheet /
# literature bands so that the physics and the quoted numbers agree.
# --------------------------------------------------------------------------
OPTIONS = [
    dict(
        key="grease",
        name="Standard grease / paste (TIM2 on lid)",
        k=(3.5, 6.0, 6.0),           # W/mK: generic filled silicone 3.5; Shin-Etsu X23-7921-5 ~6 [DS]
        blt_um=(25, 40, 100),        # 25 um at 20 psi datasheet; 40 um typical; 100 um warped lid
        rc=(0.008, 0.012, 0.02),     # two contact interfaces [LIT]
        band=(0.04, 0.07, 0.17),     # Shin-Etsu 0.050 at 25 um/20 psi [DS]; CoolIT-like calibration 0.07 [M]
        pressure_psi=(15, 30), flat_um=25, ageing=(1.3, 2.0),
        reliability="pump-out under warpage cycling; silicone-oil dry-out >85 C; 1.3-2x R'' at EOL (formulation dependent) [LIT]",
        service="field-reworkable (clean, re-dispense)", cost_usd=(2, 6),
        compat="any lidded package (B200/B300/MI355X); bare die possible but pumps out fastest",
    ),
    dict(
        key="pcm",
        name="Phase-change pad (Honeywell PTM7950 class)",
        k=(8.5, 8.5, 8.5),           # 8.5 W/mK vendor [DS via sibling]
        blt_um=(20, 30, 60),
        rc=(0.015, 0.02, 0.025),
        band=(0.04, 0.055, 0.08),    # 0.04-0.08 cm2K/W [DS via sibling]
        pressure_psi=(20, 40), flat_um=30, ageing=(1.05, 1.3),
        reliability="self-heals above ~45 C; vendor claims <10 % drift after 1000 cycles / 1000 h bake [MEM]; needs sustained 20-40 psi",
        service="field-reworkable (pad is consumable)", cost_usd=(4, 12),
        compat="any lidded package; OCP OAI guideline reference TIM",
    ),
    dict(
        key="graphite",
        name="Graphite / CNT pad (Hitachi TC-001, Panasonic PGS, Carbice, NeoGraf HiTherm)",
        k=(40.0, 30.0, 20.0),        # through-plane effective of vertically oriented graphite / aligned CNT at compression [MEM]
        blt_um=(100, 150, 200),      # pads are 0.1-0.3 mm, compressed 20-40 %
        rc=(0.01, 0.015, 0.03),      # dry contacts dominate; strongly pressure dependent [LIT]
        band=(0.035, 0.065, 0.13),   # Carbice/Hitachi vendor 0.03-0.08 at 50-100 psi [MEM]; sibling LK 0.05-0.15
        pressure_psi=(50, 150), flat_um=50, ageing=(1.0, 1.15),
        reliability="no pump-out, no dry-out; creep/pressure relaxation; conductive particle shedding (PGS) [MEM]",
        service="reusable, dry, cleanest rework", cost_usd=(8, 30),
        compat="any lidded package; bare die only with soft CNT type (Carbice) at low pressure",
    ),
    dict(
        key="lm",
        name="Liquid metal Ga-In(-Sn) (Conductonaut / Galinstan / EGaIn; Indium Corp LM)",
        k=(16.5, 25.0, 40.0),        # Galinstan 16.5, EGaIn ~26 W/mK [LIT]; vendor 40-73 claims [MEM]
        blt_um=(15, 25, 50),
        rc=(0.002, 0.004, 0.008),    # wetting metal contacts [LIT]
        band=(0.005, 0.015, 0.03),   # task band 0.005-0.02; Naddod GB300 secondary 0.02 [U]; 0.03 thick/oxidised
        pressure_psi=(5, 20), flat_um=25, ageing=(1.1, 1.6),
        reliability="dissolves Cu (CuGa2) and destroys Al (LME) -> Ni barrier mandatory; oxide skin; pump-out on large bowed areas; electrically conductive -> dam/gasket; EGaIn freezes at 15.5 C, Galinstan -19 C (Ga expands ~3 % on freezing) [LIT]",
        service="reworkable by trained tech only; contamination control", cost_usd=(10, 30),
        compat="Ni-plated Cu lid (B200/B300 lids are Ni-plated Cu, verify) or bare Si die (RTX 5090 FE precedent); never Al plates",
    ),
    dict(
        key="in_foil",
        name="Indium metal foil, patterned (Indium Corp Heat-Spring)",
        k=(86.0, 86.0, 86.0),
        blt_um=(150, 200, 300),
        rc=(0.03, 0.05, 0.08),       # non-wetting solid-solid contacts; needs 50-100 psi [MEM]
        band=(0.05, 0.07, 0.12),
        pressure_psi=(50, 100), flat_um=50, ageing=(1.0, 1.2),
        reliability="no pump-out; creep-compliant; oxide; high clamp load [MEM]",
        service="reusable-ish (single compression), dry", cost_usd=(8, 20),
        compat="lidded packages where high clamp load is acceptable; not better than PCM thermally",
    ),
    dict(
        key="in_solder",
        name="Indium solder, reflowed (TIM1-style; or plate soldered to lid)",
        k=(86.0, 86.0, 86.0),
        blt_um=(50, 100, 200),       # 50 um ideal; 100-200 um production TIM1 to absorb warpage [LIT]
        rc=(0.002, 0.004, 0.008),    # metallised, wetted interfaces [LIT]
        band=(0.005, 0.015, 0.03),   # task band 0.005-0.01 only at BLT <= 60 um (see note)
        pressure_psi=(0, 0), flat_um=50, ageing=(1.0, 1.3),
        reliability="thermal-fatigue cracking at corners under warpage cycling (known TIM1 failure); voids; needs Ni/Au on both faces; reflow 157 C [LIT]",
        service="NOT field-serviceable: plate+package become one FRU", cost_usd=(20, 45),
        compat="OEM co-design only (reflow on lid requires solderable lid finish); CTE OK Cu-plate to Cu-lid; bare die needs CTE-matched plate (CuW/CuMo/Si)",
    ),
    dict(
        key="ag_sinter",
        name="Sintered silver (die-attach class)",
        k=(150.0, 200.0, 250.0),
        blt_um=(20, 30, 50),
        rc=(0.001, 0.003, 0.006),
        band=(0.002, 0.005, 0.01),
        pressure_psi=(700, 4000), flat_um=20, ageing=(1.0, 1.1),
        reliability="power-module proven (>3000 cycles); needs 200-250 C and 5-30 MPa pressure-assisted sintering; CTE buffer required Si-to-Cu [LIT]",
        service="never reworkable", cost_usd=(25, 60),
        compat="not viable for GPU TIM2; relevant for SiC power-module baseplate attach (second SKU)",
    ),
    dict(
        key="d2d_lm",
        name="Direct-to-die: plate on bare die via liquid metal + dam (lid removed)",
        k=(16.5, 25.0, 40.0),
        blt_um=(15, 25, 50),
        rc=(0.002, 0.004, 0.008),
        band=(0.005, 0.015, 0.03),   # interface identical to LM; the gain is lid + TIM1 removal (section 3)
        pressure_psi=(5, 15), flat_um=15, ageing=(1.1, 1.6),
        reliability="as LM plus: die-crack risk (keep die pressure < 0.3 MPa), two surface heights (logic vs HBM, 50-200 um), package warpage 100-300 um must be absorbed by stepped/compliant pedestals; CTE shear Si-Cu (section 8)",
        service="reworkable by trained tech; module-level", cost_usd=(25, 60),
        compat="bare-die modules (Google TPU, A100/H100 SXM per author's recollection - verify), RTX 5090 FE precedent; B200/B300/MI355X would need delidding = chip-vendor co-design",
    ),
    dict(
        key="microfluidic",
        name="In-die microfluidics (Microsoft/Corintis 2025, TSMC ECTC 2025, DARPA ICECool)",
        k=(1.0, 1.0, 1.0),           # placeholder; modelled as junction-to-fluid unit resistance band
        blt_um=(0, 0, 0),
        rc=(0.01, 0.02, 0.05),       # junction-to-fluid incl. Si conduction + microchannel convection [LIT, ICECool class]
        band=(0.01, 0.02, 0.05),
        pressure_psi=(0, 0), flat_um=0, ageing=(1.0, 1.3),
        reliability="seal/leak at die; 25-100 um channels need 10-25 um filtration; erosion; silicon vendor must warrant; 2028+ [sibling research]",
        service="not serviceable at interface; fluid connectors at package", cost_usd=(0, 0),
        compat="chip co-design only (Maia/Corintis prototype; TSMC CoWoS demo >2.6 kW)",
    ),
]


def option_bands(o):
    """(min, nom, max) R'' from physics, then reconciled with quoted band."""
    phys = tuple(Rpp(o["blt_um"][i], o["k"][i], o["rc"][i]) for i in range(3))
    return phys, o["band"]


print("=" * 100)
print("1. TIM OPTION MATRIX  (R'' in cm2K/W; physics = BLT/k + contact; band = adopted min/nom/max)")
print("=" * 100)
print(f"{'option':<52} {'BLT um':>14} {'k W/mK':>14} {'phys R'' (min/nom/max)':>26} {'adopted band':>24}")
for o in OPTIONS:
    phys, band = option_bands(o)
    print(f"{o['name'][:52]:<52} {str(o['blt_um']):>14} {str(o['k']):>14} "
          f"{phys[0]:7.3f}/{phys[1]:6.3f}/{phys[2]:6.3f}   {band[0]:7.3f}/{band[1]:6.3f}/{band[2]:6.3f}")

# --------------------------------------------------------------------------
# 2. dT_TIM at the four heat fluxes
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("2. INTERFACE TEMPERATURE DROP dT_TIM = q'' x R''  (K)   [nominal, (min-max)]")
print("=" * 100)
hdr = f"{'option':<52}" + "".join(f"{q:>6.0f} W/cm2        " for q in Q_LIST)
print(hdr)
dT_table = {}
for o in OPTIONS:
    _, band = option_bands(o)
    row = []
    for q in Q_LIST:
        row.append(tuple(q * r for r in band))
    dT_table[o["key"]] = row
    print(f"{o['name'][:52]:<52}" + "".join(f"{r[1]:6.1f} ({r[0]:4.1f}-{r[2]:5.1f})  " for r in row))

# Share of a 35 K case-to-inlet budget consumed by the TIM alone
print()
print("TIM share of a 35 K case-to-inlet budget (nominal R''):")
for o in OPTIONS:
    _, band = option_bands(o)
    print(f"  {o['key']:<13}" + "".join(f"  {q:4.0f} W/cm2: {100*q*band[1]/35:5.0f} %" for q in Q_LIST))

# --------------------------------------------------------------------------
# 3. Full stack with the team's HMMC-fine core, 15 kW (128 W/cm2) and
#    35.1 kW (300 W/cm2) on the same 117 cm2 footprint at 1.2 LPM/kW
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("3. FULL STACK: HMMC-fine core (0.075/0.075 x 1.0 mm Cu fins, 1 mm base, 2 mm flow length)")
print("   at 1.2 LPM/kW PG25, 45 C inlet, 117 cm2. Case = top of TIM (lid surface for lidded parts).")
print("=" * 100)
Q300 = 300.0 * FOOTPRINT_CM2            # W for 300 W/cm2 on the same footprint


def stack(tim_R, label, hotspot_K=4.0, base_mm=1.0):
    cp = hmmc_design(FOOTPRINT_CM2, fin_t_mm=0.075, gap_mm=0.075, fin_h_mm=1.0,
                     tim_R=tim_R, tim_label=label, hotspot_K=hotspot_K, base_mm=base_mm,
                     name="HMMC-fine")
    return cp.evaluate(Q_BENCH, LPM_PER_KW), cp.evaluate(Q300, LPM_PER_KW)


print(f"{'TIM (nominal R'')':<40} {'R'' ':>6} | {'15 kW/128 W/cm2: avg':>22} {'max':>6} {'Tcase,max':>10} {'Qcap kW':>8} | "
      f"{'35 kW/300 W/cm2: avg':>22} {'max':>6} {'Tcase,max':>10}")
ref = coolit_like(FOOTPRINT_CM2).evaluate(Q_BENCH, LPM_PER_KW)
ref300 = coolit_like(FOOTPRINT_CM2).evaluate(Q300, LPM_PER_KW)
print(f"{'CoolIT-like skived split-flow, paste 0.07':<40} {0.07:6.3f} | {ref['dT_avg']:22.1f} {ref['dT_max']:6.1f} "
      f"{ref['T_case_max']:10.1f} {ref['Q_cap_kW']:8.1f} | {ref300['dT_avg']:22.1f} {ref300['dT_max']:6.1f} {ref300['T_case_max']:10.1f}")
stack_rows = {}
for o in OPTIONS:
    _, band = option_bands(o)
    if o["key"] == "microfluidic":
        continue
    r15, r300 = stack(band[1], o["key"])
    stack_rows[o["key"]] = (r15, r300)
    print(f"{('HMMC-fine + ' + o['key'])[:40]:<40} {band[1]:6.3f} | {r15['dT_avg']:22.1f} {r15['dT_max']:6.1f} "
          f"{r15['T_case_max']:10.1f} {r15['Q_cap_kW']:8.1f} | {r300['dT_avg']:22.1f} {r300['dT_max']:6.1f} {r300['T_case_max']:10.1f}")

# Lidded-package junction stack (what the chip actually sees), to put direct-to-die and
# microfluidics on a common basis. Units cm2K/W, nominal values [LIT/MEM]:
R_TIM1_IN = 0.015      # indium TIM1 under the lid (100 um class)
R_LID = 0.25e-2 / 390 * 1e4 * 1.0   # 2.5 mm Cu lid 1-D (ignores spreading benefit) = 0.064
R_SI = 0.0775e-2 / 130 * 1e4        # 775 um Si die backside thickness, k 130 = 0.006
R_HMMC_CORE = (stack_rows["grease"][0]["dT_base"] + stack_rows["grease"][0]["dT_conv"]) / 128.0  # base+conv per W/cm2
R_CAL = stack_rows["grease"][0]["dT_cal"]   # K, fixed by flow

print()
print("Junction-to-inlet, lidded vs lidless vs in-die (nominal, 1-D, no spreading credit for the lid):")
print(f"  components cm2K/W: Si {R_SI:.3f}, TIM1 indium {R_TIM1_IN:.3f}, Cu lid 2.5 mm {R_LID:.3f}, "
      f"HMMC core (base+conv) {R_HMMC_CORE:.3f}, caloric {R_CAL:.1f} K fixed")
stacks_j = {
    "lidded + paste TIM2 (0.07)":            R_SI + R_TIM1_IN + R_LID + 0.07 + R_HMMC_CORE,
    "lidded + PCM TIM2 (0.055)":             R_SI + R_TIM1_IN + R_LID + 0.055 + R_HMMC_CORE,
    "lidded + liquid-metal TIM2 (0.015)":    R_SI + R_TIM1_IN + R_LID + 0.015 + R_HMMC_CORE,
    "lidded + indium-soldered plate (0.015)": R_SI + R_TIM1_IN + R_LID + 0.015 + R_HMMC_CORE,
    "direct-to-die, LM on bare die (0.015)": R_SI + 0.015 + R_HMMC_CORE,
    "micro-channel lid soldered to die (In 0.015)": R_SI + 0.015 + R_HMMC_CORE * 0.9,
    "in-die microfluidics (0.02 j-to-fluid)": 0.02,
}
print(f"  {'stack':<46} {'R'' cm2K/W':>10} {'dTj-in @128':>12} {'@300':>8} {'Tj @300 (45 in)':>16}")
for k_, v in stacks_j.items():
    print(f"  {k_:<46} {v:10.3f} {R_CAL + 128*v:12.1f} {R_CAL + 300*v:8.1f} {T_IN + R_CAL + 300*v:16.1f}")
base = stacks_j["lidded + paste TIM2 (0.07)"]
mf = stacks_j["in-die microfluidics (0.02 j-to-fluid)"]
print(f"  -> in-die vs lidded-paste at 128 W/cm2: {(1 - (R_CAL + 128*mf)/(R_CAL + 128*base))*100:.0f} % lower junction rise "
      f"(Microsoft/Corintis quote 65 % peak-rise reduction, 'up to 3x')")

# --------------------------------------------------------------------------
# 4. Package bow / bond-line non-uniformity: paraboloid bow w(x,y) against a rigid flat plate.
#    BLT(x,y) = BLT_min + w0 * ((x/L)^2 + (y/L)^2)/2 ; contact at centre, corners gap by w0.
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("4. BOND-LINE NON-UNIFORMITY FROM PACKAGE BOW (108 mm square, rigid plate, q'' = 128 W/cm2)")
print("   dT_TIM average and corner-minus-centre spread; TIM fills the wedge (no air gap assumed).")
print("=" * 100)
L = 54.0  # mm half side
xs = np.linspace(-L, L, 201)
X, Y = np.meshgrid(xs, xs)
bow_cases = [0, 50, 100, 200, 300]
fillers = [
    ("grease k 3.5, BLT_min 25 um, Rc 0.012", 3.5, 25, 0.012),
    ("premium grease k 6, BLT_min 25, Rc 0.012", 6.0, 25, 0.012),
    ("PCM k 8.5, BLT_min 20, Rc 0.02", 8.5, 20, 0.02),
    ("liquid metal k 20, BLT_min 15, Rc 0.004", 20.0, 15, 0.004),
]
print(f"{'filler':<44}" + "".join(f"  bow {w:3d} um: avg/spread" for w in bow_cases))
bow_results = {}
for name, k, bltmin, rc in fillers:
    row = []
    for w0 in bow_cases:
        blt = bltmin + w0 * ((X / L) ** 2 + (Y / L) ** 2) / 2.0
        R = blt * 1e-6 / k * 1e4 + rc
        dT = 128.0 * R
        row.append((dT.mean(), dT.max() - dT.min()))
    bow_results[name] = row
    print(f"{name:<44}" + "".join(f"  {a:6.1f} / {s:5.1f} K    " for a, s in row))
print("  Note: CoolIT measured a 10 K plate-to-plate spread at TC8 (27.6-37.7 K) with 'standard paste';")
print("  a 100-200 um uncompensated bow with grease reproduces that order of spread.")
print("  Graphite/CNT pads (0.1-0.3 mm, 20-40 % compressible) absorb 50-100 um bow at nearly constant R''.")

# --------------------------------------------------------------------------
# 5. Ageing: end-of-life dT at 128 and 300 W/cm2
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("5. AGEING: end-of-life interface dT (nominal R'' x EOL multiplier)   K")
print("=" * 100)
print(f"{'option':<14} {'mult (lo-hi)':>14} {'BOL@128':>8} {'EOL@128 lo-hi':>16} {'BOL@300':>8} {'EOL@300 lo-hi':>16}")
for o in OPTIONS:
    _, band = option_bands(o)
    lo, hi = o["ageing"]
    print(f"{o['key']:<14} {lo:6.2f}-{hi:4.2f}     {128*band[1]:8.1f} {128*band[1]*lo:7.1f}-{128*band[1]*hi:5.1f}   "
          f"{300*band[1]:8.1f} {300*band[1]*lo:7.1f}-{300*band[1]*hi:5.1f}")

# --------------------------------------------------------------------------
# 6. Ni barrier plating penalty (liquid metal on copper)
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("6. NICKEL BARRIER PLATING PENALTY (liquid metal requires Ni on Cu; Au must NOT be left on top)")
print("=" * 100)
platings = [
    ("electroless Ni-P high-P (10-12 % P), k ~ 5 W/mK [LIT]", 5.0),
    ("electroless Ni-P mid-P (6-9 % P), k ~ 10 W/mK [MEM]", 10.0),
    ("electroless Ni-P low-P (2-4 % P), k ~ 25 W/mK [MEM]", 25.0),
    ("electrolytic sulfamate Ni, k ~ 70-90 W/mK [LIT]", 80.0),
]
print(f"{'plating':<56} {'3 um':>14} {'5 um':>14} {'8 um':>14} {'12 um':>14}    (R'' cm2K/W ; dT at 300 W/cm2)")
for name, k in platings:
    cells = []
    for t in (3, 5, 8, 12):
        R = t * 1e-6 / k * 1e4
        cells.append(f"{R:6.4f} ; {300*R:4.1f}K")
    print(f"{name:<56} " + " ".join(f"{c:>14}" for c in cells))
print("  Rule: a 10 um high-P electroless Ni layer (0.02 cm2K/W) would cost more than the liquid metal itself (0.015).")
print("  Specify electrolytic Ni 3-5 um (or low-P ENi <= 5 um), no Au top coat (Au dissolves into Ga within hours).")
print("  Ga-Ni intermetallic growth is slow below ~100 C; 5 um Ni is the industry floor (PS5 / ASUS ROG practice) [MEM].")

# --------------------------------------------------------------------------
# 7. Clamp force for contact pressure
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("7. CLAMP FORCE = pressure x contact area   (117 cm2 TTV footprint; 16 cm2 Blackwell-class bare die pair)")
print("=" * 100)
print(f"{'option':<14} {'pressure psi':>14} {'MPa':>12} {'force on 117 cm2 (N / lbf)':>28} {'force on 16 cm2 (N / lbf)':>28}")
for o in OPTIONS:
    p_lo, p_hi = o["pressure_psi"]
    if p_hi == 0:
        continue
    mpa = (p_lo * 6.895e-3, p_hi * 6.895e-3)
    f117 = (mpa[0] * 117e-4 * 1e6, mpa[1] * 117e-4 * 1e6)
    f16 = (mpa[0] * 16e-4 * 1e6, mpa[1] * 16e-4 * 1e6)
    print(f"{o['key']:<14} {p_lo:6d}-{p_hi:<6d} {mpa[0]:5.2f}-{mpa[1]:<5.2f} "
          f"{f117[0]:7.0f}-{f117[1]:6.0f} N ({f117[0]/4.448:4.0f}-{f117[1]/4.448:4.0f} lbf) "
          f"{f16[0]:7.0f}-{f16[1]:6.0f} N ({f16[0]/4.448:4.0f}-{f16[1]/4.448:4.0f} lbf)")
for F in (300.0, 600.0, 1000.0):
    print(f"  retention load {F:5.0f} N over 117 cm2 = {F/117e-4/1e3:5.1f} kPa = {F/117e-4/6895:4.1f} psi ; over 50 cm2 = {F/50e-4/6895:4.1f} psi ; over 16 cm2 = {F/16e-4/6895:5.1f} psi")
print("  Rule: module retention loads on current GPU/OAM modules are of order 300-1000 N [MEM - verify vs OAM / SXM mech. spec];")
print("  on a 100+ cm2 lid that is only 4-12 psi, below every pad's minimum. Pressure-hungry TIMs (graphite >= 50 psi,")
print("  indium foil) are therefore incompatible with large lids; liquid metal (5-10 psi) and PCM at its low end fit.")
print("  Bare die: limit local pressure to ~0.1-0.3 MPa and avoid edge loading (die-crack) [MEM].")

# --------------------------------------------------------------------------
# 8. CTE shear at the interface for direct-to-die (per thermal cycle)
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("8. CTE-DRIVEN SHEAR DISPLACEMENT AT THE DIE EDGE PER CYCLE (free expansion, upper bound)")
print("=" * 100)
cte = {"Si": 2.6e-6, "Cu": 17.0e-6, "CuW (W85)": 7.0e-6, "CuMo": 7.5e-6, "AlSiC": 8.0e-6, "Si lid": 2.6e-6, "Mo": 5.0e-6}
dT_cycle = 40.0   # K, idle-to-full swing of the interface (20 -> 60 C plate; die backside)
die_half = {"Blackwell 2-die (~40 mm)": 20.0, "Rubin Ultra 4-die (~60 mm)": 30.0, "15 kW TTV lid-less (108 mm)": 54.0}
print(f"{'plate material':<14}" + "".join(f"{k:>32}" for k in die_half))
for mat, a in cte.items():
    if mat == "Si":
        continue
    cells = []
    for _, half in die_half.items():
        d_um = (a - cte["Si"]) * dT_cycle * half * 1e-3 * 1e6
        cells.append(f"{d_um:6.1f} um (strain {d_um/25:4.1f} at 25 um BLT)")
    print(f"{mat:<14}" + "".join(f"{c:>32}" for c in cells))
print("  Rule: grease at shear strain >= ~0.3-0.5 per cycle pumps out within 10^2-10^3 cycles [LIT];")
print("  solder at strain >> 0.05 fatigues; liquid metal tolerates strain (liquid) but migrates on large bowed areas.")
print("  => Direct-to-die with a copper plate: liquid metal or soft CNT pad only; soldered direct-to-die needs CuW/CuMo/Si lid.")

# --------------------------------------------------------------------------
# 9. Cost per unit (order of magnitude)
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("9. COST PER PLATE (117 cm2 footprint), order-of-magnitude, material + process adder  [MEM]")
print("=" * 100)
lm_g = 117 * 25e-4 * 6.4         # cm3 -> g at 6.4 g/cm3, 25 um
in_g = 117 * 100e-4 * 7.3        # 100 um indium
print(f"  liquid metal mass at 25 um over 117 cm2: {lm_g:.1f} g ; indium solder at 100 um: {in_g:.1f} g (In ~US$0.4-0.8/g 2025-26 [MEM])")
for o in OPTIONS:
    lo, hi = o["cost_usd"]
    cost = "n/a (silicon vendor)" if hi == 0 else f"US${lo:3d}-{hi:<3d}"
    print(f"  {o['key']:<14} {cost:<22} {o['service']}")

# --------------------------------------------------------------------------
# 10. Tier recommendation summary numbers
# --------------------------------------------------------------------------
print()
print("=" * 100)
print("10. TIER SUMMARY at 128 / 300 W/cm2 (HMMC-fine core, avg case-to-inlet K, nominal TIM, BOL)")
print("=" * 100)
tiers = [
    ("Tier 1 drop-in retrofit: PCM pad (fallback graphite)", "pcm"),
    ("Tier 2 OEM co-designed: liquid metal on Ni-plated lid", "lm"),
    ("Tier 2b OEM sealed FRU: indium-soldered plate", "in_solder"),
    ("Tier 3 chip co-designed: direct-to-die LM / micro-channel lid", "d2d_lm"),
]
for label, key in tiers:
    r15, r300 = stack_rows[key]
    print(f"  {label:<62} 128: {r15['dT_avg']:5.1f} avg / {r15['dT_max']:5.1f} max  |  300: {r300['dT_avg']:5.1f} avg / {r300['dT_max']:5.1f} max")
print(f"  {'Benchmark CoolIT-like, paste':<62} 128: {ref['dT_avg']:5.1f} avg / {ref['dT_max']:5.1f} max  |  300: {ref300['dT_avg']:5.1f} avg / {ref300['dT_max']:5.1f} max")
print()
print("Caveats: 1-D; TIM bands are datasheet/literature/memory (no live search this session); +/-30 % per term.")
