"""PRISM-15 factory cost (US$/plate), corrected copper (LME ~US$14.4-14.7k/t Sep 2026 per judges; OFE mill product US$17-19/kg;
scrap credit ~US$11.5/kg), fixture-loaded vacuum braze (30-80 plates/load), 100 % IR flow screen. +/-20 %, to be replaced by RFQs."""
items = [  # (element, 10k/yr, 100k/yr, 1M/yr)
 ("OFE copper: ~2.5 kg buy, ~0.85 kg scrap credit", 38, 35, 32),
 ("skived RF-15 core (360 fins, 3-4 min) + tip planing", 40, 22, 15),
 ("fin kerfing (gang saw, 18 cuts) + deburr/bright-dip", 6, 3, 2),
 ("floor grate + meter sheet + separator (laser-cut -> stamped)", 24, 5, 3),
 ("plenum layer (CNC -> 2 stamped laminations)", 30, 4, 2.5),
 ("header bar (CNC -> forged + finish CNC)", 30, 12, 7),
 ("filler (Ag plate / BAg-8 preforms) + clean", 9, 5, 4),
 ("vacuum braze, fixture-loaded, 30-80 per load", 25, 16, 10),
 ("post-braze fly-cut of face to 1.0 mm, flatness", 8, 5, 3),
 ("316L stubs + 50 um abs guard screen", 14, 8, 6),
 ("hardware: springs, backplate, screws", 20, 14, 10),
 ("test: He leak, proof + pressurised flatness scan, 3-point dP, IR flow screen, ISO 16232 flush", 14, 9, 6),
]
oh = (0.18, 0.15, 0.12)
tot = [sum(i[k] for i in items) for k in (1, 2, 3)]
for e in items: print(f"| {e[0]} | {e[1]} | {e[2]} | {e[3]} |")
print(f"| yield, scrap, overhead ({oh[0]*100:.0f} / {oh[1]*100:.0f} / {oh[2]*100:.0f} %) | {tot[0]*oh[0]:.0f} | {tot[1]*oh[1]:.0f} | {tot[2]*oh[2]:.0f} |")
print(f"| **factory cost** | **{tot[0]*(1+oh[0]):.0f}** | **{tot[1]*(1+oh[1]):.0f}** | **{tot[2]*(1+oh[2]):.0f}** |")
for lab, c, q in (("PRISM-15 PCM", tot[1]*(1+oh[1]), 19.4), ("PRISM-15 paste", tot[1]*(1+oh[1]), 16.6), ("CoolIT-like paste", 112, 12.9), ("CoolIT-like PCM", 112, 14.8)):
    print(f"{lab}: US$/kW of Tcase-limited capacity = {c/q:.1f}")
