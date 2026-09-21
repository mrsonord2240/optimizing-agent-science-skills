# Independent Egger (weighted regression y ~ 1 + se, w=1/v, multiplicative dispersion) and Duval-Tweedie L0 trim-and-fill, no metafor
import numpy as np, csv, sys
from scipy import stats, optimize
def load(p, ycol, vcol):
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    return np.array([float(r[ycol]) for r in rows]), np.array([float(r[vcol]) for r in rows])
def egger(y, v):
    se = np.sqrt(v); w = 1/v; X = np.c_[np.ones(len(y)), se]; W = np.diag(w)
    beta = np.linalg.solve(X.T@W@X, X.T@W@y); r = y - X@beta
    df = len(y)-2; s2 = (w*r**2).sum()/df; cov = s2*np.linalg.inv(X.T@W@X)
    t = beta[1]/np.sqrt(cov[1,1]); return beta, t, 2*stats.t.sf(abs(t), df), df
def reml(y, v):
    f = lambda t: 0.5*(np.log(v+t).sum() + np.log((1/(v+t)).sum()) + ((1/(v+t))*(y-((1/(v+t))*y).sum()/(1/(v+t)).sum())**2).sum())
    t = optimize.minimize_scalar(f, bounds=(0,10), method="bounded", options={"xatol":1e-10}).x
    w = 1/(v+t); return t, (w*y).sum()/w.sum()
def trimfill_L0(y, v):
    k = len(y); se = np.sqrt(v)
    beta, t, p, df = egger(y, v)
    side_left = t < 0     # metafor: if Egger slope negative -> missing studies on the right, trim from the LEFT? (checked against output)
    # Work in orientation where missing studies are on the left: flip so that trimmed (extreme) ones are on the right
    yy = -y if not side_left else y  # side_left True -> flip? see below
    # L0 (Duval & Tweedie 2000): iterate
    yy = -y if side_left else y.copy()
    k0 = 0
    for _ in range(100):
        n = k - k0; idx = np.argsort(yy)  # ascending
        keep = idx[:n]
        t2, mu = reml(yy[keep], v[keep])
        d = yy - mu; order = np.argsort(np.abs(d)); ranks = np.empty(k); ranks[order] = np.arange(1, k+1)
        Tn = ranks[d > 0].sum()
        k0_new = max(0, int(round((4*Tn - k*(k+1)) / (2*k - 1)))) if False else max(0, int(round((4*Tn - k*(k+1))/(2*k-1))))
        # L0 = (4 Tn - n(n+1)) / (2n-1) with n = k (all)
        if k0_new == k0: break
        k0 = k0_new
    return k0, yy, mu, side_left
if __name__ == "__main__":
    y, v = load(r"F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots\data\example_studies.csv", "yi", "vi")
    b, t, p, df = egger(y, v)
    print(f"EXAMPLE Egger: intercept-on-se slope={b[1]:.4f} t={t:.4f} df={df} p={p:.5f}  limit est (se->0) b0={b[0]:.4f}")
    k0, yy, mu, sl = trimfill_L0(y, v); print("L0 k0 =", k0)
    # fill: mirror k0 most extreme (largest yy) around mu, refit RE
    n = len(y); idx = np.argsort(yy); trimmed = idx[n-k0:] if k0 else []
    if k0:
        t2, mu_t = reml(yy[idx[:n-k0]], v[idx[:n-k0]])
        yf = np.r_[yy, 2*mu_t - yy[trimmed]]; vf = np.r_[v, v[trimmed]]
        t3, mu_f = reml(yf, vf)
        adj = -mu_f if sl else mu_f
        print(f"adjusted pooled log = {adj:.4f}  OR={np.exp(adj):.3f}  (metafor: 0.3674 / 1.44)")
