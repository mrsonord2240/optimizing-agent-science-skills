# bio-qsar-modeling -- Input 3 (Edge): conformal prediction, exactly as SKILL.md writes it,
# and a test of whether the Skill's version bound (MAPIE >=0.8,<1.0) is the right one.
import sys
import numpy as np
import sklearn
from sklearn.ensemble import RandomForestRegressor

print(f"python={sys.executable}")
print(f"sklearn={sklearn.__version__}")
import mapie
print(f"mapie={mapie.__version__}")

D = r"F:\OpenScience\audits\bio-qsar-modeling\run"
X = np.load(D + r"\X.npy").astype(float)
y = np.load(D + r"\y.npy")
tr = np.load(D + r"\tr.npy")
te = np.load(D + r"\te.npy")
X_train, y_train, X_test, y_test = X[tr], y[tr], X[te], y[te]
print(f"train={X_train.shape} test={X_test.shape}")

# --- the SKILL.md snippet, verbatim -----------------------------------------
try:
    from mapie.regression import MapieRegressor
    base = RandomForestRegressor(n_estimators=500, random_state=42)
    m = MapieRegressor(estimator=base, method='plus', cv=5)
    m.fit(X_train, y_train)
    y_pred, y_intervals = m.predict(X_test, alpha=0.1)   # alpha=0.1 -> 90% coverage
    lo, hi = y_intervals[:, 0, 0], y_intervals[:, 1, 0]
    cov = float(((y_test >= lo) & (y_test <= hi)).mean())
    print(f"  SKILL.md snippet RAN. intervals shape={y_intervals.shape}")
    print(f"  empirical coverage at alpha=0.1 -> {cov:.3f}  (target 0.90)")
    print(f"  mean interval width = {(hi-lo).mean():.3f} log units "
          f"(label range {y.min():.2f}-{y.max():.2f})")
    # is the interval width itself a usable AD signal?
    err = np.abs(y_test - y_pred)
    w = hi - lo
    med = np.median(w)
    print(f"  narrow-interval half:  n={(w<=med).sum()} MAE={err[w<=med].mean():.3f} "
          f"coverage={float(((y_test>=lo)&(y_test<=hi))[w<=med].mean()):.3f}")
    print(f"  wide-interval half:    n={(w>med).sum()} MAE={err[w>med].mean():.3f} "
          f"coverage={float(((y_test>=lo)&(y_test<=hi))[w>med].mean()):.3f}")
    for a in (0.05, 0.2):
        yp, yi = m.predict(X_test, alpha=a)
        c = float(((y_test >= yi[:, 0, 0]) & (y_test <= yi[:, 1, 0])).mean())
        print(f"  alpha={a}: target {1-a:.2f}, empirical {c:.3f}, "
              f"mean width {(yi[:,1,0]-yi[:,0,0]).mean():.3f}")
except Exception as e:                                        # noqa: BLE001
    print(f"  SKILL.md snippet FAILED: {type(e).__name__}: {e}")
    print("  (this is the expected outcome outside the Skill's own version bound)")
