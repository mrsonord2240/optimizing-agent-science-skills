import sys; sys.path.insert(0, r"F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots\run")
import numpy as np
from in2_egger_tf_independent import load, egger, reml, trimfill_L0
D = r"F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots\data"
for nm in ["biased", "symmetric"]:
    y, v = load(fr"{D}\synthetic_{nm}_k30.csv", "yi", "vi")
    b, t, p, df = egger(y, v); t2, mu = reml(y, v)
    k0, yy, m, sl = trimfill_L0(y, v)
    n = len(y); idx = np.argsort(yy); tr = idx[n-k0:] if k0 else []
    if k0:
        _, mt = reml(yy[idx[:n-k0]], v[idx[:n-k0]]); yf = np.r_[yy, 2*mt-yy[tr]]; vf = np.r_[v, v[tr]]
        _, mf = reml(yf, vf); adj = -mf if sl else mf
    else: adj = mu
    z = 1.96
    print(f"{nm}: REML mu={mu:.6f} tau2={t2:.6f} | Egger t={t:.4f} p={p:.5f} | TF k0={k0} adj={adj:.4f}")
    se = np.sqrt(v).max()
    print(f"   expected pseudo-95% CI limits at max se={se:.3f} around pooled: [{mu-z*se:.3f},{mu+z*se:.3f}]; contour 95 around 0: +-{z*se:.3f}")
