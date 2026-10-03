"""Run the SKILL.md 'Fitting Predictive Survival Models' and 'Prediction-Grade Evaluation' code blocks VERBATIM (extracted from the file)
on real GBSG2 (686 patients, bundled in scikit-survival) with a stratified held-out split, as an agent copying them would.
Records what must be supplied by the user (undefined names) and the resulting held-out metrics, then a Kaplan-Meier IBS comparison."""
import re, traceback
import numpy as np
from sksurv.datasets import load_gbsg2
from sksurv.preprocessing import OneHotEncoder
from sksurv.nonparametric import kaplan_meier_estimator
from sksurv.metrics import integrated_brier_score
from sksurv.util import Surv
from sklearn.model_selection import train_test_split
SK = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis\SKILL.md"
blocks = re.findall(r"```python\n(.*?)```", open(SK, encoding="utf-8").read(), re.S)
fit_block = next(b for b in blocks if "CoxnetSurvivalAnalysis(" in b); eval_block = next(b for b in blocks if "concordance_index_ipcw(y_train" in b)
X, y = load_gbsg2(); Xn = OneHotEncoder().fit_transform(X).astype(float)
df = Xn.copy(); df['status'] = y['cens'].astype(int); df['time'] = y['time'].astype(float)
Xtr, Xte, dtr, dte = train_test_split(Xn, df, test_size=0.3, random_state=0, stratify=df['status'])
ns = {"df": df, "X_train": Xtr, "X_test": Xte}
# the snippets use y_train / y_test without defining them (the fitting block builds `y` from the whole df, which would leak); supply held-out targets
ns["y_train"] = Surv.from_arrays(dtr['status'].astype(bool), dtr['time']); ns["y_test"] = Surv.from_arrays(dte['status'].astype(bool), dte['time'])
exec(fit_block.replace("coxnet.fit(X_train, y_train)", "coxnet.fit(X_train, y_train)"), ns)
print("fitting block ran; note block builds y from the FULL df:", "y" in ns and len(ns["y"]) == len(df))
try:
    exec(eval_block, ns)
except NameError as e:
    print("evaluation block as written fails:", type(e).__name__, e)
    ns["t_horizon"] = float(np.percentile(ns["y_train"]['time'][ns["y_train"]['event']], 90))
    exec(eval_block, ns)
yt, ys = ns["y_train"], ns["y_test"]; times = ns["times"]
tt, sv = kaplan_meier_estimator(yt['event'], yt['time'])
km = np.array([sv[np.searchsorted(tt, t, side='right') - 1] for t in times])
ibs_km = integrated_brier_score(yt, ys, np.tile(km, (len(Xte), 1)), times)
print(f"proper KM-only IBS {ibs_km:.3f} (model IBS above must be lower to add value)")
rsf = ns["rsf"]; print("RSF Uno C:", round(ns["concordance_index_ipcw"](yt, ys, rsf.predict(Xte), tau=ns["t_horizon"])[0], 3))
