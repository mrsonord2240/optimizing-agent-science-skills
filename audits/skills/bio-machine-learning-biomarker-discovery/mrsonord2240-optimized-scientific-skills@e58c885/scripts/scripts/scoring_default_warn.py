"""Does sklearn 1.9.1 warn about the 1.11 default change when scoring is omitted? (BD-002 wording check)"""
import sys, warnings
sys.dont_write_bytecode = True
import numpy as np, sklearn
from sklearn.linear_model import LogisticRegressionCV
r = np.random.default_rng(0); X = r.normal(size=(60, 10)); y = (X[:, 0] + r.normal(size=60) > 0).astype(int)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); LogisticRegressionCV(Cs=3, cv=3, use_legacy_attributes=False).fit(X, y)
print('sklearn', sklearn.__version__, 'warnings when scoring omitted:', [str(x.message)[:200] for x in w])
m = LogisticRegressionCV(Cs=3, cv=3, use_legacy_attributes=False).fit(X, y); print('default scoring ->', m.scoring)
