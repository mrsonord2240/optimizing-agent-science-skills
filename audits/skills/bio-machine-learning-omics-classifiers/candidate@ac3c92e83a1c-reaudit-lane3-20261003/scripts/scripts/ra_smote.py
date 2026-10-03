"""Independent SMOTE check (own generator): leak when resampling before CV vs imblearn Pipeline; held-out AUC gain and predicted risk. Usage: python ra_smote.py"""
import warnings; warnings.simplefilter('error', FutureWarning)
import numpy as np
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.metrics import roc_auc_score
rng = np.random.default_rng(11)
# 1. pure-noise labels, 8% positive: leakage check
X = rng.normal(size=(300, 60)); y = (rng.random(300) < 0.12).astype(int)
cv = StratifiedKFold(5, shuffle=True, random_state=0)
Xr, yr = SMOTE(random_state=0).fit_resample(X, y)
leak = cross_val_score(LogisticRegression(max_iter=3000), Xr, yr, cv=cv, scoring='roc_auc').mean()
proper = cross_val_score(ImbPipeline([('smote', SMOTE(random_state=0)), ('clf', LogisticRegression(max_iter=3000))]), X, y, cv=cv, scoring='roc_auc').mean()
print(f'noise labels: SMOTE-before-CV AUC {leak:.3f} vs imblearn Pipeline {proper:.3f}')
# 2. held-out: known logistic model, 8% prevalence
P, K = 40, 8; beta = np.zeros(P); beta[:K] = np.random.default_rng(31).normal(scale=0.7, size=K)
def gen(n, seed):
    r = np.random.default_rng(seed); Xg = r.normal(size=(n, P)); return Xg, (r.random(n) < 1 / (1 + np.exp(-(Xg @ beta - 3.2)))).astype(int)
gains, rp, rs = [], [], []
for s in range(8):
    Xt, yt = gen(1500, 40 + s); Xe, ye = gen(20000, 90 + s)
    a = LogisticRegression(max_iter=3000).fit(Xt, yt); b = ImbPipeline([('smote', SMOTE(random_state=0)), ('clf', LogisticRegression(max_iter=3000))]).fit(Xt, yt)
    pa, pb = a.predict_proba(Xe)[:, 1], b.predict_proba(Xe)[:, 1]
    gains.append(roc_auc_score(ye, pb) - roc_auc_score(ye, pa)); rp.append(pa.mean() / ye.mean()); rs.append(pb.mean() / ye.mean())
print(f'held-out: mean AUC gain from SMOTE {np.mean(gains):+.4f} (range {min(gains):+.4f}..{max(gains):+.4f}); predicted/observed prevalence plain {np.mean(rp):.2f}x, SMOTE {np.mean(rs):.2f}x')
