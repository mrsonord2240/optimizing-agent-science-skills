# Independent hand computation (numpy/scipy only, no metafor): DL, REML, FE pooled OR, tau2, I2, Q, PI
import numpy as np, csv
from scipy import stats, optimize
rows = list(csv.DictReader(open(r"F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots\data\bcg_logor.csv", encoding="utf-8")))
y = np.array([float(r["log_or"]) for r in rows]); se = np.array([float(r["log_or_se"]) for r in rows]); v = se**2; k = len(y)
w = 1/v; mu_fe = (w*y).sum()/w.sum(); Q = (w*(y-mu_fe)**2).sum()
C = w.sum() - (w**2).sum()/w.sum(); tau2_dl = max(0,(Q-(k-1))/C)
def negll(t):
    ww = 1/(v+t); mu = (ww*y).sum()/ww.sum()
    return 0.5*(np.log(v+t).sum() + np.log(ww.sum()) + (ww*(y-mu)**2).sum())
t = optimize.minimize_scalar(negll, bounds=(0,10), method="bounded", options={"xatol":1e-10}).x
ww = 1/(v+t); mu = (ww*y).sum()/ww.sum(); sem = np.sqrt(1/ww.sum())
z = stats.norm.ppf(.975)
I2 = max(0,(Q-(k-1))/Q)*100
# metafor's I2 uses tau2 estimated by the model: I2 = 100*tau2/(tau2+s2), s2=(k-1)*sum(w)/(sum(w)^2-sum(w^2))
s2 = (k-1)*w.sum()/(w.sum()**2-(w**2).sum()); I2m = 100*t/(t+s2)
pi = stats.t.ppf(.975,k-2)*np.sqrt(t+sem**2)
print(f"k={k} Q={Q:.4f} p={stats.chi2.sf(Q,k-1):.3g}")
print(f"FE mu={mu_fe:.6f} OR={np.exp(mu_fe):.4f} [{np.exp(mu_fe-z*np.sqrt(1/w.sum())):.4f},{np.exp(mu_fe+z*np.sqrt(1/w.sum())):.4f}]")
print(f"DL tau2={tau2_dl:.6f}; REML tau2={t:.6f}")
print(f"REML mu={mu:.6f} se={sem:.6f} ci=[{mu-z*sem:.6f},{mu+z*sem:.6f}] OR={np.exp(mu):.4f} [{np.exp(mu-z*sem):.4f},{np.exp(mu+z*sem):.4f}]")
print(f"I2 (Q-based)={I2:.3f}  I2 (metafor tau2-based)={I2m:.3f}")
print(f"PI (t_{k-2}) = [{mu-pi:.4f},{mu+pi:.4f}] -> OR [{np.exp(mu-pi):.4f},{np.exp(mu+pi):.4f}]")
