"""Variant B: SMOTE placement and effect, own generator. (a) noise labels, 10% positives, n=300, p=100: AUC when SMOTE is applied before CV (leak) vs inside imblearn Pipeline.
(b) real-signal 8%-prevalence data: held-out AUC and risk ratio, plain vs SMOTE logistic. Usage: python r2_smote.py"""
import warnings, numpy as np
from imblearn.pipeline import Pipeline as IP
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score
warnings.simplefilter('error', FutureWarning)
leak, pipe = [], []
for s in range(8):
    r = np.random.default_rng(777 + s); X = r.normal(size=(300, 100)); y = (r.random(300) < 0.1).astype(int)
    cv = StratifiedKFold(5, shuffle=True, random_state=0)
    Xr, yr = SMOTE(random_state=0).fit_resample(X, y)
    leak.append(cross_val_score(LogisticRegression(C=1.0, max_iter=3000), Xr, yr, cv=cv, scoring='roc_auc').mean())
    pipe.append(cross_val_score(IP([('s', SMOTE(random_state=0)), ('c', LogisticRegression(C=1.0, max_iter=3000))]), X, y, cv=cv, scoring='roc_auc').mean())
print(f'(a) noise labels: SMOTE before CV AUC {np.mean(leak):.3f}; inside imblearn Pipeline {np.mean(pipe):.3f}')
beta = np.zeros(60); beta[:10] = np.random.default_rng(31).normal(scale=0.7, size=10)
d, rr = [], []
for s in range(8):
    r = np.random.default_rng(1500 + s)
    def gen(n):
        X = r.normal(size=(n, 60)); return X, (r.random(n) < 1/(1+np.exp(-(X @ beta - 3.4)))).astype(int)
    Xtr, ytr = gen(1500); Xte, yte = gen(20000)
    p0 = LogisticRegression(C=0.1, max_iter=3000).fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    p1 = IP([('s', SMOTE(random_state=0)), ('c', LogisticRegression(C=0.1, max_iter=3000))]).fit(Xtr, ytr).predict_proba(Xte)[:, 1]
    d.append(roc_auc_score(yte, p1) - roc_auc_score(yte, p0)); rr.append((p0.mean() / yte.mean(), p1.mean() / yte.mean()))
rr = np.array(rr)
print(f'(b) logistic: SMOTE minus plain test AUC mean {np.mean(d):+.4f} (range {min(d):+.4f}..{max(d):+.4f}); predicted/observed prevalence plain {rr[:,0].mean():.2f}x, SMOTE {rr[:,1].mean():.2f}x')
