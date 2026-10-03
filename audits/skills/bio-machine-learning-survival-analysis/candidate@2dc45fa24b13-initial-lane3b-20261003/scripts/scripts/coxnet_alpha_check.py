"""Which penalty does the Skill's Coxnet snippet actually use? CoxnetSurvivalAnalysis(l1_ratio=0.9, alpha_min_ratio=0.01, fit_baseline_model=True)
fits a whole alpha path. Inspect what predict() uses, how many coefficients are nonzero there, and what a CV-selected alpha gives (held-out Uno C)."""
import inspect
import numpy as np
from sksurv.datasets import load_gbsg2
from sksurv.preprocessing import OneHotEncoder
from sksurv.linear_model import CoxnetSurvivalAnalysis
from sksurv.util import Surv
from sksurv.metrics import concordance_index_ipcw
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
X, y = load_gbsg2(); Xn = OneHotEncoder().fit_transform(X).astype(float)
Xtr, Xte, ytr, yte = train_test_split(Xn, y, test_size=0.3, random_state=0, stratify=y['cens'])
ytr = Surv.from_arrays(ytr['cens'].astype(bool), ytr['time'].astype(float))
yte = Surv.from_arrays(yte['cens'].astype(bool), yte['time'].astype(float))
m = CoxnetSurvivalAnalysis(l1_ratio=0.9, alpha_min_ratio=0.01, fit_baseline_model=True).fit(Xtr, ytr)
print("alphas_ in path:", len(m.alphas_), "max", m.alphas_.max(), "min", m.alphas_.min())
print("coef_ shape", m.coef_.shape, "nonzero at alpha_max / alpha_min:", int((m.coef_[:, 0] != 0).sum()), int((m.coef_[:, -1] != 0).sum()), "of", Xtr.shape[1])
print("predict signature:", inspect.signature(m.predict))
r_default = m.predict(Xte); r_min = m.predict(Xte, alpha=m.alphas_[-1]); r_max = m.predict(Xte, alpha=m.alphas_[0])
print("predict() default equals smallest-alpha end of path:", bool(np.allclose(r_default, r_min)), "; equals largest alpha (null model):", bool(np.allclose(r_default, r_max)))
tau = np.percentile(ytr['time'][ytr['event']], 90)
print(f"Uno C with default predict: {concordance_index_ipcw(ytr, yte, r_default, tau=tau)[0]:.3f}")
gs = GridSearchCV(CoxnetSurvivalAnalysis(l1_ratio=0.9, fit_baseline_model=True), {"alphas": [[a] for a in m.alphas_[::5]]}, cv=KFold(5, shuffle=True, random_state=0), n_jobs=1).fit(Xtr, ytr)
best = gs.best_estimator_
print("CV best alpha", best.alphas_[0], "nonzero", int((best.coef_ != 0).sum()))
print(f"Uno C with CV-selected alpha: {concordance_index_ipcw(ytr, yte, best.predict(Xte), tau=tau)[0]:.3f}")
