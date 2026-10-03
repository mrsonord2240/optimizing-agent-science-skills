"""Re-audit SA-001: KM baseline IBS must be censoring-aware, same estimator/grid/split as the model.
Independent checks: (1) hand table; (2) pure-numpy product-limit KM and pure-numpy Graf IBS (IPCW) vs sksurv/lifelines;
(3) the Skill's km_baseline_surv + printed baseline, GBSG2 expected ~0.178 (old naive 0.263)."""
import sys, warnings, numpy as np
sys.dont_write_bytecode = True
SK = r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis\scripts"
sys.path.insert(0, SK); import cox_regression as cr
from sklearn.model_selection import train_test_split
from sksurv.metrics import integrated_brier_score
from lifelines import KaplanMeierFitter

def km_np(time, event):
    """Product-limit estimator in plain numpy: returns (unique event times, S)."""
    ut = np.unique(time[event]); S = []; s = 1.0
    for t in ut:
        d = np.sum((time == t) & event); n = np.sum(time >= t); s *= 1 - d / n; S.append(s)
    return ut, np.array(S)
def step(ut, S, t):
    i = np.searchsorted(ut, t, side='right'); return 1.0 if i == 0 else S[i - 1]
def ibs_np(ytr, yte, surv, times):
    """Graf IBS in plain numpy; censoring distribution G = KM of censoring on TRAIN data."""
    ct, cS = km_np(ytr['time'], ~ytr['event'])
    T, E = yte['time'], yte['event']; bs = []
    for k, t in enumerate(times):
        s = surv[:, k]
        w_ev = np.array([1.0 / max(step(ct, cS, Ti), 1e-12) for Ti in T])      # G(T_i) (sksurv uses G(T_i))
        gt = step(ct, cS, t)
        term = np.where((T <= t) & E, s ** 2 * w_ev, 0.0) + np.where(T > t, (1 - s) ** 2 / gt, 0.0)
        bs.append(term.mean())
    bs = np.array(bs); return np.trapezoid(bs, times) / (times[-1] - times[0])

print("== Part 1: hand table (time,event): (1,1)(2,0)(3,1)(4,0)(5,0)")
t = np.array([1, 2, 3, 4, 5.]); e = np.array([1, 0, 1, 0, 0], bool)
hand = {0.5: 1.0, 1: 0.8, 2: 0.8, 3: 0.8 * 2 / 3, 4: 0.8 * 2 / 3, 5: 0.8 * 2 / 3}   # at risk 5,(4 censored),3 -> 0.8*(1-1/3)
ys = cr.Surv.from_arrays(e, t); ut, S = km_np(t, e)
for h, v in hand.items():
    sk = cr.km_baseline_surv(ys, np.array([h]), 1)[0, 0]
    print(f"  t={h}: hand {v:.6f} numpy-KM {step(ut,S,h):.6f} Skill km_baseline_surv {sk:.6f} naive np.mean(t[e]>t) {np.mean(t[e] > h):.4f}")
    assert abs(sk - v) < 1e-12 and abs(step(ut, S, h) - v) < 1e-12
print("  PASS hand table")

def case(name, X, y):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y['event'])
    tm = np.percentile(yte['time'][yte['event']], np.linspace(10, 80, 15))     # same grid construction as the script
    km_skill = cr.km_baseline_surv(ytr, tm, len(yte))
    ut, S = km_np(ytr['time'], ytr['event']); km_own = np.tile([step(ut, S, x) for x in tm], (len(yte), 1))
    lk = KaplanMeierFitter().fit(ytr['time'], ytr['event']); km_ll = np.tile(lk.predict(tm, interpolate=False).values, (len(yte), 1))
    naive = np.tile([np.mean(ytr['time'][ytr['event']] > x) for x in tm], (len(yte), 1))
    i_skill = integrated_brier_score(ytr, yte, km_skill, tm); i_own = ibs_np(ytr, yte, km_own, tm)
    i_ll = integrated_brier_score(ytr, yte, km_ll, tm); i_naive = integrated_brier_score(ytr, yte, naive, tm)
    print(f"== {name}: n_train={len(ytr)} n_test={len(yte)} censored train={1-ytr['event'].mean():.0%}")
    print(f"  max|S_skill - S_numpyKM| = {np.abs(km_skill-km_own).max():.2e}; max|S_skill - S_lifelinesKM| = {np.abs(km_skill-km_ll).max():.2e}")
    print(f"  IBS: Skill-KM(sksurv metric) {i_skill:.4f} | own numpy IBS on own KM {i_own:.4f} | lifelines KM {i_ll:.4f} | naive event-only (old defect) {i_naive:.4f}")
    assert np.abs(km_skill - km_own).max() < 1e-12 and np.abs(km_skill - km_ll).max() < 1e-12
    assert abs(i_skill - i_own) < 5e-3, (i_skill, i_own)
    return i_skill

X, y = cr.load_data('gbsg2'); g = case('GBSG2', X, y)
assert 0.17 < g < 0.185 and abs(g - 0.263) > 0.05
X, y = cr.load_data('synthetic'); case('synthetic', X, y)
# model-vs-baseline consistency: model rows evaluated on same tm/ytr/yte via the same sksurv function (checked by reading main()).
print("  PASS SA-001: baseline censoring-aware; matches independent KM and independent IBS")
