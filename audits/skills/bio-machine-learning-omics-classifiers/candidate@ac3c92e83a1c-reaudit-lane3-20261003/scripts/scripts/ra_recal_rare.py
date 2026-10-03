"""Does the shipped recalibrate() survive a calibration set with very few events? Usage: python ra_recal_rare.py <Skill dir>"""
import sys, os, warnings
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from calibration_check import recalibrate
warnings.filterwarnings('ignore', category=UserWarning)
r = np.random.default_rng(0); Xtr = r.normal(size=(300, 10)); ytr = (r.random(300) < 1 / (1 + np.exp(-(Xtr[:, 0] - 2)))).astype(int)
rf = RandomForestClassifier(n_estimators=50, random_state=0).fit(Xtr, ytr)
for n, ev in ((20, 5), (20, 4), (20, 3), (20, 2), (20, 1), (50, 3), (100, 8)):
    y = np.r_[np.ones(ev), np.zeros(n - ev)].astype(int); X = np.random.default_rng(n + ev).normal(size=(n, 10))
    try:
        c = recalibrate(rf, X, y); print(f'n={n} events={ev}: OK method={c.method}')
    except Exception as e:
        print(f'n={n} events={ev}: {type(e).__name__}: {str(e)[:90]}')
