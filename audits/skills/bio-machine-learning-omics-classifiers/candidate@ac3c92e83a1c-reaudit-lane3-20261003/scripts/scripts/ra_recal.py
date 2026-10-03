"""Independent OC-004 check: recalibrate() branch + degenerate-warning paths through the shipped code. Usage: python ra_recal.py <Skill dir>"""
import sys, os, warnings
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
from calibration_check import recalibrate, calibration_table

def sep(n, seed, shift=4.0):
    r = np.random.default_rng(seed); y = (r.random(n) < 0.4).astype(int)
    return r.normal(size=(n, 6)) + y[:, None] * shift, y

def run(label, model, Xc, yc, Xt=None, yt=None):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always'); cal = recalibrate(model, Xc, yc)
    d = len(np.unique(cal.predict_proba(Xc)[:, 1].round(6)))
    msg = f'{label}: n_cal={len(yc)} method={cal.method} distinct_on_cal={d} warnings={[str(x.message)[:70] for x in w]}'
    if Xt is not None: msg += f' | test Brier {brier_score_loss(yt, cal.predict_proba(Xt)[:, 1]):.4f}'
    print(msg)
    return cal
# (a) separable, n=1000 with >=100 events -> isotonic chosen, base separates the calibration set perfectly -> degenerate -> must warn
Xtr, ytr = sep(400, 1); rf = RandomForestClassifier(n_estimators=100, random_state=0).fit(Xtr, ytr)
Xc, yc = sep(1000, 2); Xt, yt = sep(5000, 3)
run('(a) separable n=1000 isotonic', rf, Xc, yc, Xt, yt)
# (b) separable, n=20 -> sigmoid; no warning expected, but sigmoid probabilities nearly 0/1?
Xc, yc = sep(20, 4); cal = run('(b) separable n=20 sigmoid', rf, Xc, yc, *sep(5000, 5))
# (c) honest overlapping case n=1000 -> isotonic, no warning
r = np.random.default_rng(6); Xtr = r.normal(size=(400, 20)); ytr = (r.random(400) < 1 / (1 + np.exp(-(Xtr[:, :3].sum(1))))).astype(int)
rf2 = RandomForestClassifier(n_estimators=100, min_samples_leaf=3, random_state=0).fit(Xtr, ytr)
Xc = r.normal(size=(1000, 20)); yc = (r.random(1000) < 1 / (1 + np.exp(-(Xc[:, :3].sum(1))))).astype(int)
run('(c) overlapping n=1000', rf2, Xc, yc)
# (d) rare class 54 events at n=1000 -> sigmoid
Xc = r.normal(size=(1000, 20)); yc = (r.random(1000) < 0.055).astype(int); print('events', int(yc.sum()))
run('(d) n=1000 rare', rf2, Xc, yc)
# (e) boundaries: n=999, events 100 / n=1000 events 99
for n, ev in ((999, 400), (1000, 99), (1000, 100)):
    yc = np.r_[np.ones(ev), np.zeros(n - ev)].astype(int); Xc = np.random.default_rng(n + ev).normal(size=(n, 20))
    run(f'(e) boundary n={n} rarer={ev}', rf2, Xc, yc)
# (f) logistic base (rule derived on RF/XGB only)
lrm = LogisticRegression(max_iter=2000).fit(Xtr, ytr)
Xc = r.normal(size=(1000, 20)); yc = (r.random(1000) < 1 / (1 + np.exp(-(Xc[:, :3].sum(1))))).astype(int)
run('(f) logistic base n=1000', lrm, Xc, yc)
# (g) does warnings.warn reach a user under default filters (UserWarning shown once per location)?
print('-- (g) default-filter, run twice in one process --')
Xc, yc = sep(1000, 2)
for i in range(2):
    with warnings.catch_warnings(record=True) as w:
        warnings.resetwarnings(); warnings.simplefilter('default'); recalibrate(rf, Xc, yc)
    print('call', i, 'warnings:', len(w))
