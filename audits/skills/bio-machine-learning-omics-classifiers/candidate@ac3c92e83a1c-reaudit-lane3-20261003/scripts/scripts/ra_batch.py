"""Independent OC-002 check with planted truth. Usage: python ra_batch.py <Skill dir>"""
import sys, os, warnings
sys.path.insert(0, os.path.join(sys.argv[1], 'scripts'))
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from batch_checks import batch_predictability, leave_one_batch_out
warnings.simplefilter('error', FutureWarning)
probe = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(max_iter=3000))])

def design(nb, per, mode, rng, rate_lo=0.2, rate_hi=0.8):
    batch = np.repeat(np.arange(nb), per)
    if mode == 'batch_only':      # label tracks batch; features carry only a batch offset -> truth: no label signal within a batch
        y = (rng.random(len(batch)) < np.where(batch < nb / 2, rate_lo, rate_hi)).astype(int)
        X = rng.normal(batch[:, None] * 1.5, 1, (len(batch), 60))
    elif mode == 'real_only':     # label independent of batch; real signal in 5 features
        y = (rng.random(len(batch)) < 0.5).astype(int)
        X = rng.normal(batch[:, None] * 1.5, 1, (len(batch), 60)); X[:, :5] += y[:, None] * 1.0
    else:                         # both: confounded AND real signal
        y = (rng.random(len(batch)) < np.where(batch < nb / 2, rate_lo, rate_hi)).astype(int)
        X = rng.normal(batch[:, None] * 1.5, 1, (len(batch), 60)); X[:, :5] += y[:, None] * 1.0
    return X, y, batch

REP = 20
for nb in (2, 3, 6):
    for mode in ('batch_only', 'real_only', 'both'):
        res = []
        for rep in range(REP):
            rng = np.random.default_rng(1000 * nb + rep)
            X, y, b = design(nb, 40, mode, rng)
            pooled, tab = leave_one_batch_out(probe, X, y, b)
            res.append((cross_val_score(probe, X, y, cv=5, scoring='roc_auc').mean(), tab.auc.mean(), pooled, tab.auc.isna().sum()))
        a = np.array(res)
        print(f'{nb} batches {mode:10s}: random-split {a[:,0].mean():.2f} | LOBO per-batch mean {a[:,1].mean():.2f} (sd across reps {a[:,1].std():.2f}, min {a[:,1].min():.2f}, max {a[:,1].max():.2f}) | pooled {a[:,2].mean():.2f} | NaN batches/rep {a[:,3].mean():.2f}', flush=True)

# manual leave-one-batch-out reference (independent implementation) vs the Skill's
rng = np.random.default_rng(5); X, y, b = design(6, 40, 'both', rng)
from sklearn.metrics import roc_auc_score
man = []
for h in np.unique(b):
    m = probe.fit(X[b != h], y[b != h]); man.append(roc_auc_score(y[b == h], m.predict_proba(X[b == h])[:, 1]))
pooled, tab = leave_one_batch_out(probe, X, y, b)
print('manual per-batch AUC', np.round(man, 4), '\nskill  per-batch AUC', tab.auc.round(4).values, 'max abs diff', np.abs(np.array(man) - tab.auc.values).max())

# edge cases
print('\n-- edge: one-class held-out batch --')
b = np.repeat([0, 1, 2], 30); y = np.r_[np.zeros(30), np.tile([0, 1], 15), np.ones(30)].astype(int); X = np.random.default_rng(1).normal(size=(90, 20)) + y[:, None]
print(leave_one_batch_out(probe, X, y, b)[1].to_string(index=False))
print('-- edge: training batches single class (2 batches, batch 1 all cases; held-out 0 trained on one-class) --')
b = np.repeat([0, 1], 30); y = np.r_[np.tile([0, 1], 15), np.ones(30)].astype(int); X = np.random.default_rng(2).normal(size=(60, 10))
p, t = leave_one_batch_out(probe, X, y, b); print('pooled', p); print(t.to_string(index=False))
print('-- edge: string batch labels / pandas inputs / string class labels --')
b = pd.Series(np.repeat(['siteA', 'siteB', 'siteC'], 40)); rng = np.random.default_rng(3)
y = pd.Series(np.where(rng.random(120) < 0.5, 'ctrl', 'case')); X = pd.DataFrame(rng.normal(size=(120, 10)))
try: print(leave_one_batch_out(probe, X, y, b)[1].to_string(index=False)); print('batch_pred', batch_predictability(probe, X, b))
except Exception as e: print('ERR', type(e).__name__, e)
print('-- edge: a batch with a single sample --')
b = np.r_[np.repeat([0, 1], 30), [2]]; y = np.r_[np.tile([0, 1], 30), [1]]; X = np.random.default_rng(4).normal(size=(61, 10))
try: print('batch_pred', batch_predictability(probe, X, b))
except Exception as e: print('batch_predictability ERR', type(e).__name__, str(e)[:150])
try: print(leave_one_batch_out(probe, X, y, b)[1].to_string(index=False))
except Exception as e: print('LOBO ERR', type(e).__name__, str(e)[:150])
print('-- edge: single batch --')
try: print(leave_one_batch_out(probe, X[:30], y[:30], np.zeros(30)))
except Exception as e: print('LOBO ERR', type(e).__name__, str(e)[:150])
