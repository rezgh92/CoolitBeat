import sys, math, numpy as np
sys.path.insert(0, __import__('os').path.normpath(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '../../model'))); sys.path.insert(0, '../arch')
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from vp_mc import mc, prism, TIMS
for g,t in (("R6","paste"),("R6","PCM25")):
    o = mc(g,t); af, mf, Af = o["fair"]; a, m, _ = o["pub"]
    sel = Af < 110
    print(f"{g} {t}: P(max<44.2 | A<110) {np.mean(mf[sel]<44.2):.2f}; P(avg<34.4 | A<105) {np.mean(af[Af<105]<34.4):.2f}; P90 avg/max pub {np.percentile(a,90):.1f}/{np.percentile(m,90):.1f}; P(avg<=31 & max<=36, PCM decisive) {np.mean((a<=31)&(m<=36)):.2f}")
