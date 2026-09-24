import numpy as np
from scipy import stats, optimize
y = np.log([0.55,0.90,1.60]); se = np.array([.20,.25,.30]); v = se**2; k=3
f = lambda t: 0.5*(np.log(v+t).sum()+np.log((1/(v+t)).sum())+((1/(v+t))*(y-((1/(v+t))*y).sum()/(1/(v+t)).sum())**2).sum())
t2 = optimize.minimize_scalar(f, bounds=(0,10), method="bounded", options={"xatol":1e-10}).x
w = 1/(v+t2); mu = (w*y).sum()/w.sum(); q = (w*(y-mu)**2).sum()
se_hk = np.sqrt(q/(k-1)/w.sum()); tc = stats.t.ppf(.975,k-1)
print(f"tau2={t2:.6f} mu={mu:.6f}  z-CI=[{mu-1.96/np.sqrt(w.sum()):.6f},{mu+1.96/np.sqrt(w.sum()):.6f}]")
print(f"HKSJ: q/(k-1)={q/(k-1):.4f} se={se_hk:.6f} ci=[{mu-tc*se_hk:.6f},{mu+tc*se_hk:.6f}] df={k-1}")
