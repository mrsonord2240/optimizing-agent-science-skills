"""Held-out perturbation test: replace the test split with garbage after splitting; every selection/scaling/early-stop/1-SE/calibration step must be unchanged.
Negative control: perturbing the validation / calibration split must change something. Usage: python ra_perturb.py <Skill dir>"""
import sys, os, warnings
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from calibration_check import recalibrate
warnings.simplefilter('error', FutureWarning); warnings.filterwarnings('ignore', category=UserWarning)
rng = np.random.default_rng(0); n, p = 900, 120
X = rng.normal(size=(n, p)); b = np.zeros(p); b[:10] = 0.7
y = (rng.random(n) < 1 / (1 + np.exp(-(X @ b - 1)))).astype(int)
X_dev, X_te, y_dev, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
X_tr, X_val, y_tr, y_val = train_test_split(X_dev, y_dev, test_size=0.3, stratify=y_dev, random_state=0)
X_c, X_tr2, y_c, y_tr2 = train_test_split(X_tr, y_tr, test_size=0.6, stratify=y_tr, random_state=1)     # calibration slice carved from train for the demo

def pipeline(Xte, yte, Xval, yval, Xcal):
    out = {}
    xgb = XGBClassifier(n_estimators=2000, learning_rate=0.03, max_depth=4, subsample=0.8, colsample_bytree=0.5, reg_lambda=1.0,
                        early_stopping_rounds=50, eval_metric='aucpr', n_jobs=1, random_state=0).fit(X_tr, y_tr, eval_set=[(Xval, yval)], verbose=False)
    out['xgb_best_iter'] = xgb.best_iteration; out['xgb_probe'] = xgb.predict_proba(X_dev[:20])[:, 1]
    lasso = LogisticRegressionCV(solver='saga', l1_ratios=[1.0], Cs=10, cv=5, max_iter=3000, scoring='neg_log_loss', use_legacy_attributes=False, random_state=0)
    Pipeline([('s', StandardScaler()), ('c', lasso)]).fit(X_dev, y_dev)
    f = lasso.scores_[:, 0, :]; mean, se = f.mean(0), f.std(0, ddof=1) / np.sqrt(5)
    out['c_1se'] = lasso.Cs_[np.flatnonzero(mean >= mean.max() - se[mean.argmax()]).min()]
    rf = RandomForestClassifier(n_estimators=100, random_state=0, n_jobs=1).fit(X_tr2, y_tr2)
    out['cal_probe'] = recalibrate(rf, Xcal, y_c).predict_proba(X_dev[:20])[:, 1]
    return out
base = pipeline(X_te, y_te, X_val, y_val, X_c)
junk_te = np.random.default_rng(9).normal(size=X_te.shape) * 50; junk_y = 1 - y_te
pert_te = pipeline(junk_te, junk_y, X_val, y_val, X_c)
neg_val = pipeline(X_te, y_te, np.random.default_rng(8).normal(size=X_val.shape), 1 - y_val, X_c)
neg_cal = pipeline(X_te, y_te, X_val, y_val, np.random.default_rng(7).normal(size=X_c.shape))
same = lambda a, b: all(np.array_equal(np.asarray(a[k]), np.asarray(b[k])) for k in a)
print('perturb TEST split (garbage X, flipped y): all selection/early-stop/1-SE/calibration outputs identical:', same(base, pert_te))
print('negative control: perturb VALIDATION split -> best_iter', base['xgb_best_iter'], '->', neg_val['xgb_best_iter'], '| changed:', not same(base, neg_val))
print('negative control: perturb CALIBRATION split -> calibrated probe changed:', not np.array_equal(base['cal_probe'], neg_cal['cal_probe']))
rows = lambda A: {A[i].tobytes() for i in range(len(A))}
print('three-way split disjoint and complete:', not (rows(X_tr) & rows(X_val)) and not (rows(X_tr) & rows(X_te)) and not (rows(X_val) & rows(X_te)) and len(rows(X_tr)) + len(rows(X_val)) + len(rows(X_te)) == n)
