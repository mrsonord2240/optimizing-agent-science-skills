"""Check the Skill's 'Kaplan-Meier baseline IBS' line in scripts/cox_regression.py against a proper KM.
The script computes km_surv = np.mean(ttr[etr] > t): the share of EVENT-ONLY training subjects with time > t,
which drops every censored subject. A correct KM (sksurv.nonparametric.kaplan_meier_estimator) keeps them.
Part 1: tiny hand table. Part 2: the script's own synthetic data. Part 3: GBSG2."""
import numpy as np, runpy
from sksurv.util import Surv
from sksurv.nonparametric import kaplan_meier_estimator
from sksurv.metrics import integrated_brier_score
SK = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis\scripts\cox_regression.py"
print("== Part 1: tiny table (time, event): (1,1)(2,0)(3,1)(4,0)(5,0); KM by hand")
t = np.array([1, 2, 3, 4, 5.]); e = np.array([1, 0, 1, 0, 0], bool)
# at-risk 5,4,3,2,1: S(1)=4/5=0.8 ; S(3)=0.8*(1-1/3)=0.5333 (hand-computed)
hand = {1: 0.8, 2: 0.8, 3: 0.8 * (2 / 3), 4: 0.8 * (2 / 3)}
tt, sv = kaplan_meier_estimator(e, t)
for h in (1, 2, 3, 4):
    km = sv[np.searchsorted(tt, h, side='right') - 1]
    naive = np.mean(t[e] > h)
    print(f"t={h}: hand KM {hand[h]:.4f}  sksurv KM {km:.4f}  Skill-script formula np.mean(t[e]>t) {naive:.4f}")
    assert abs(km - hand[h]) < 1e-9
print("== Part 2: script's own synthetic data (runpy, unmodified)")
g = runpy.run_path(SK)
ttr, etr, tte, ete, times = g['ttr'], g['etr'], g['tte'], g['ete'], g['times']
y_tr, y_te = g['y_tr'], g['y_te']
naive = np.array([np.mean(ttr[etr] > t) for t in times])
tt, sv = kaplan_meier_estimator(etr, ttr)
km = np.array([sv[np.searchsorted(tt, t, side='right') - 1] for t in times])
print("horizon grid:", np.round(times, 3))
print("naive 'KM'  :", np.round(naive, 3))
print("proper KM   :", np.round(km, 3))
n = len(tte)
ibs_naive = integrated_brier_score(y_tr, y_te, np.tile(naive, (n, 1)), times)
ibs_km = integrated_brier_score(y_tr, y_te, np.tile(km, (n, 1)), times)
print(f"IBS naive (as printed by script) {ibs_naive:.3f}   IBS proper KM {ibs_km:.3f}")
print(f"censored fraction in training = {1 - etr.mean():.2f}")
print("== Part 3: same formula on GBSG2")
from sksurv.datasets import load_gbsg2
from sksurv.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
X, y = load_gbsg2(); Xn = OneHotEncoder().fit_transform(X).astype(float)
Xtr, Xte, ytr, yte = train_test_split(Xn, y, test_size=0.3, random_state=0, stratify=y['cens'])
a = Surv.from_arrays(ytr['cens'].astype(bool), ytr['time'].astype(float))
b = Surv.from_arrays(yte['cens'].astype(bool), yte['time'].astype(float))
tm = np.percentile(b['time'][b['event']], np.linspace(10, 80, 15))
nv = np.array([np.mean(a['time'][a['event']] > t) for t in tm])
tt, sv = kaplan_meier_estimator(a['event'], a['time'])
km = np.array([sv[np.searchsorted(tt, t, side='right') - 1] for t in tm])
print(f"GBSG2 IBS naive {integrated_brier_score(a, b, np.tile(nv, (len(Xte), 1)), tm):.3f}  proper KM {integrated_brier_score(a, b, np.tile(km, (len(Xte), 1)), tm):.3f}")
