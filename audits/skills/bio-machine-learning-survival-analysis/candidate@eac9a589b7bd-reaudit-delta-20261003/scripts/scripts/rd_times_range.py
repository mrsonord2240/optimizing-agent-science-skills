"""Delta re-audit: check the reworded Common Errors row (SA-006) for BOTH cumulative_dynamic_auc and integrated_brier_score,
and for a censored vs event largest test time. Skill scripts used unmodified (imported)."""
import sys, numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis\scripts"); import cox_regression as cr
from sklearn.model_selection import train_test_split
from sksurv.metrics import cumulative_dynamic_auc, integrated_brier_score
from sksurv.nonparametric import kaplan_meier_estimator
X, y = cr.load_data('gbsg2'); Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y['event'])
m = cr.fit_coxnet_cv(Xtr, ytr); risk = m.predict(Xte)
mx_all, mx_ev = yte['time'].max(), yte['time'][yte['event']].max()
print(f"largest test time {mx_all:.0f} censored={not bool(yte['event'][yte['time'].argmax()])}; largest uncensored {mx_ev:.0f}")
# IBS needs survival functions; use KM baseline as estimate (pure range test)
def ibs(hi):
    tm = np.linspace(200, hi, 10)
    km_t, km_s = kaplan_meier_estimator(ytr['event'], ytr['time'])
    est = np.tile(np.interp(tm, km_t, km_s), (len(yte), 1))
    return integrated_brier_score(ytr, yte, est, tm)
for label, hi in [("below largest uncensored", mx_ev-1), ("between uncensored and max test", (mx_ev+mx_all)/2), ("max test time-1", mx_all-1), ("at max test time", mx_all), ("above", mx_all+10)]:
    tm = np.linspace(200, hi, 10)
    for nm, fn in (("AUC", lambda: round(float(cumulative_dynamic_auc(ytr, yte, risk, tm)[1]),3)), ("IBS", lambda: round(float(ibs(hi)),3))):
        try: print(f"{nm} {label} (t={hi:.0f}): {fn()}")
        except Exception as e: print(f"{nm} {label} (t={hi:.0f}): ERROR {type(e).__name__}: {str(e)[:100]}")
