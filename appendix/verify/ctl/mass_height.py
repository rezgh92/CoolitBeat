"""Mass (same boundary as the draft: plate + stubs/guard/springs/backplate 0.15 kg, no 2 kN TTV load frame) and height."""
RHO=8.94e-3  # g/mm3 -> kg via /1000
def kg(mm3, rho=8.94): return mm3*rho/1e6
draft = {"base+fins (1.0 base)":0.27,"grate 1.0":0.11,"meter 0.4":0.05,"plenum laminations 9.0":0.55,"separator 1.5":0.21,"header bar 10.5":0.41,"stubs/guard/springs/backplate":0.15}
pkgA = {"base+fins (0.8 base)": kg(125*125*0.8 + (125**2-108**2)*1.0 + 108*108*1.0),
        "metered grate 1.7 (meter merged)": kg(125*125*1.7 - 8*1.2*108*1.7 - 7*1.2*108*1.3),
        "folded plenum 0.8 mm, 5.0 mm channels + end frame": kg(108*108*0.8*(2*5.8+6.9+6.9)/15.4) + kg(2*2*5.8*125 + 2*2*5.8*108),
        "separator 1.5": kg(125*125*1.5 - 14*6.9*14*1.5),
        "arched drawn cap 1.0 mm + 2 port bosses": kg(113*125*1.0) + 0.05,
        "stubs/guard/springs/backplate": 0.15}
pkgA_ss = dict(pkgA); pkgA_ss["separator 0.6 mm 316L (Ni strike)"] = kg(125*125*0.6 - 14*6.9*14*0.6, 7.95); del pkgA_ss["separator 1.5"]
for lab, d in (("draft", draft), ("PKG-A", pkgA), ("PKG-A + 316L separator", pkgA_ss)):
    print(f"{lab}: total {sum(d.values()):.2f} kg  [" + "; ".join(f"{k} {v:.3f}" for k, v in d.items()) + "]")
stack = {"draft": [1.0, 2.0, 1.0, 0.4, 9.0, 1.5, 10.5], "draft (mfg-corrected bar)": [1.0, 2.0, 1.0, 0.4, 9.0, 1.5, 11.5],
         "PKG-A (8 mm arched header)": [0.8, 2.0, 1.7, 0.0, 5.8, 1.5, 9.0], "PKG-A (6 mm triple-arch header)": [0.8, 2.0, 1.7, 0.0, 5.8, 1.5, 7.0]}
for k, v in stack.items(): print(f"{k}: body {sum(v[:-1]):.1f} mm, at the bar {sum(v):.1f} mm")
