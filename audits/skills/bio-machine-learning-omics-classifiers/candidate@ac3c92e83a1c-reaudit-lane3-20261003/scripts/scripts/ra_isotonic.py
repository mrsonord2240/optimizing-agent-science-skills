"""Independent OC-004 rule check with own generator, RF base (rule's derivation base) and logistic base (not used to derive it).
Share of repeats where isotonic had lower test Brier than sigmoid, by calibration size. Usage: python ra_isotonic.py"""
import warnings; warnings.simplefilter('error', FutureWarning); warnings.filterwarnings('ignore', category=UserWarning); warnings.filterwarnings('ignore', category=RuntimeWarning)
import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.frozen import FrozenEstimator
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
P, K = 40, 8; beta = np.zeros(P); beta[:K] = np.random.default_rng(55).normal(scale=0.6, size=K)
def gen(n, seed, icpt):
    r = np.random.default_rng(seed); X = r.normal(size=(n, P)); return X, (r.random(n) < 1 / (1 + np.exp(-(X @ beta + icpt)))).astype(int)
for prev_name, icpt in (('~30%', -1.0), ('~10%', -2.6)):
    for base in ('rf', 'logistic'):
        wins = {n: [] for n in (20, 100, 300, 1000, 3000)}; gap = {n: [] for n in wins}
        for rep in range(25):
            Xtr, ytr = gen(300, 10 * rep + 1, icpt); Xp, yp = gen(3000, 10 * rep + 2, icpt); Xte, yte = gen(10000, 10 * rep + 3, icpt)
            m = (RandomForestClassifier(n_estimators=150, min_samples_leaf=3, random_state=0, n_jobs=4) if base == 'rf' else LogisticRegression(max_iter=2000, C=0.3)).fit(Xtr, ytr)
            for n in wins:
                if len(np.unique(yp[:n])) < 2: continue          # a calibration draw with no events cannot be calibrated at all
                b = {}
                for meth in ('sigmoid', 'isotonic'):
                    b[meth] = brier_score_loss(yte, CalibratedClassifierCV(FrozenEstimator(m), method=meth).fit(Xp[:n], yp[:n]).predict_proba(Xte)[:, 1])
                wins[n].append(b['isotonic'] < b['sigmoid']); gap[n].append(b['isotonic'] - b['sigmoid'])
        print(f'prevalence {prev_name} base {base:8s}: ' + ' | '.join(f'n={n}: iso wins {np.mean(wins[n]):.2f}, mean gap {np.mean(gap[n]):+.4f}' for n in wins), flush=True)
