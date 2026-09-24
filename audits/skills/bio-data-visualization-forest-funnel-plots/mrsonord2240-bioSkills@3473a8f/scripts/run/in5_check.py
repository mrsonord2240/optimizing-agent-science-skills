import numpy as np, csv
rows = list(csv.DictReader(open(r"F:\OpenScience\audits\bio-data-visualization-forest-funnel-plots\data\mr_ldlc_chd.csv", encoding="utf-8")))
bx,bxse,by,byse = [np.array([float(r[c]) for r in rows]) for c in ["bx","bxse","by","byse"]]
w = 1/byse**2
ivw = (w*bx*by).sum()/(w*bx**2).sum(); se_fe = 1/np.sqrt((w*bx**2).sum())
res = by - ivw*bx; phi = (w*res**2).sum()/(len(bx)-1); se_re = se_fe*max(1,np.sqrt(phi))
print(f"IVW est={ivw:.6f} se_FE={se_fe:.6f} se_RE(resid, >=1)={se_re:.6f}")
# MR-Egger: orient so bx>0, weighted regression by ~ 1 + bx
sg = np.sign(bx); X = np.c_[np.ones(len(bx)), np.abs(bx)]; yy = by*sg; W = np.diag(w)
beta = np.linalg.solve(X.T@W@X, X.T@W@yy); r = yy - X@beta; s2 = (w*r**2).sum()/(len(bx)-2)
cov = s2*np.linalg.inv(X.T@W@X); print(f"Egger int={beta[0]:.4f} slope={beta[1]:.4f} se_slope(resid scaled)={np.sqrt(cov[1,1]):.4f}")
