"""OC-004/OC-011 recalibrate(): branch boundaries and degenerate warning through the shipped code path (own data). Usage: python r2_recal_paths.py <Skill dir>"""
import sys, warnings, numpy as np
sys.path.insert(0, sys.argv[1] + '/scripts')
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from calibration_check import recalibrate
warnings.simplefilter('error', FutureWarning)
def data(n, prev, seed, sep=1.0):
    r = np.random.default_rng(seed); y = (r.random(n) < prev).astype(int); return r.normal(size=(n, 6)) + y[:, None] * sep, y
Xt, yt = data(400, .3, 1)
stump = DecisionTreeClassifier(max_depth=1, random_state=0).fit(Xt, yt)
for n, prev in ((999, .5), (1000, .5), (1000, .05), (1000, .10), (1200, .5), (200, .5)):
    Xc, yc = data(n, prev, 7)
    ev = int(min(yc.sum(), (1 - yc).sum()))
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always'); cal = recalibrate(stump, Xc, yc)
    print(f'n={n} rarer-class events={ev}: method={cal.method}; warnings={[str(x.message)[:50] for x in w]}')
# healthy RF + sigmoid: no warning
rf = RandomForestClassifier(n_estimators=100, random_state=0).fit(Xt, yt); Xc, yc = data(300, .3, 8)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); cal = recalibrate(rf, Xc, yc)
print('healthy RF n=300:', cal.method, 'warnings', len(w), 'distinct', len(np.unique(cal.predict_proba(Xc)[:,1].round(6))))
