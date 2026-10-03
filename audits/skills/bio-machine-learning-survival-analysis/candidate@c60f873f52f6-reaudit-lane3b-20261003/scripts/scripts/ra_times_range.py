"""Check the Common Errors row: 'times for AUC/IBS out of range <- beyond largest uncensored test time'."""
import sys, warnings, numpy as np
sys.dont_write_bytecode = True
sys.path.insert(0, r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis\scripts"); import cox_regression as cr
from sklearn.model_selection import train_test_split
from sksurv.metrics import cumulative_dynamic_auc, integrated_brier_score
X, y = cr.load_data('gbsg2'); Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y['event'])
risk = cr.fit_coxnet_cv(Xtr, ytr).predict(Xte)
mx_all, mx_ev = yte['time'].max(), yte['time'][yte['event']].max()
print(f"test max time all {mx_all:.0f} (event={bool(yte['event'][yte['time'].argmax()])}), largest uncensored {mx_ev:.0f}, train max {ytr['time'].max():.0f}")
for label, hi in [("just below largest uncensored", mx_ev - 1), ("between largest uncensored and max test time", (mx_ev + mx_all) / 2 if mx_all > mx_ev else None), ("at max test time", mx_all), ("above max test time", mx_all + 10)]:
    if hi is None: print(label, ": n/a (largest test time is an event)"); continue
    tm = np.linspace(200, hi, 10)
    try: print(f"AUC {label} (t={hi:.0f}):", round(cumulative_dynamic_auc(ytr, yte, risk, tm)[1], 3))
    except Exception as e: print(f"AUC {label} (t={hi:.0f}): ERROR {type(e).__name__}: {str(e)[:110]}")
