"""Independent OC-001 check: own generator (not the Skill's draw()). Usage: python ra_calibration.py <Skill dir>"""
import sys, os, warnings
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
import numpy as np
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, brier_score_loss
from calibration_check import recalibrate
warnings.simplefilter('error', FutureWarning)

P, K = 80, 8
BETA = np.zeros(P); BETA[:K] = np.random.default_rng(777).normal(scale=0.7, size=K)   # own coefficients
def gen(n, seed, icpt=-3.4):
    r = np.random.default_rng(seed); X = r.normal(size=(n, P))
    p = 1 / (1 + np.exp(-(X @ BETA + icpt)))
    return X, (r.random(n) < p).astype(int), p
rows = []
for seed in range(6):
    Xtr, ytr, _ = gen(1200, 100 + seed); Xc, yc, _ = gen(1000, 200 + seed); Xte, yte, pte = gen(30000, 300 + seed)
    def lr(cw): return LogisticRegressionCV(Cs=10, l1_ratios=(0,), cv=5, scoring='neg_log_loss', use_legacy_attributes=False, max_iter=5000, class_weight=cw).fit(Xtr, ytr)
    plain, bal = lr(None), lr('balanced')
    rec = recalibrate(bal, Xc, yc)
    ev = int(min(yc.sum(), (1 - yc).sum()))
    out = {'seed': seed, 'prev_test': yte.mean(), 'true_mean_risk': pte.mean(), 'cal_events': ev}
    for nm, m in (('lr_plain', plain), ('lr_balanced', bal), ('lr_bal_recal', rec)):
        pr = m.predict_proba(Xte)[:, 1]; out[nm + '_ratio'] = pr.mean() / yte.mean(); out[nm + '_auc'] = roc_auc_score(yte, pr); out[nm + '_brier'] = brier_score_loss(yte, pr)
    for nm, cw in (('rf_plain', None), ('rf_balanced', 'balanced')):
        rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=3, class_weight=cw, random_state=0, n_jobs=4).fit(Xtr, ytr)
        pr = rf.predict_proba(Xte)[:, 1]; out[nm + '_ratio'] = pr.mean() / yte.mean(); out[nm + '_auc'] = roc_auc_score(yte, pr)
    rows.append(out); print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in out.items()}, flush=True)
import pandas as pd
df = pd.DataFrame(rows); print(df.mean().round(3).to_string())
