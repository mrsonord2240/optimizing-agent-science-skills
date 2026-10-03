"""OC-011 spread + OC-002 planted-signal. Own generator (30 per batch, 80 features, seeds 50000+). Usage: python r2_batch.py <Skill dir>
Arm 1 zero-signal, label confounded with batch; Arm 2 real within-batch signal (5 features) plus batch offsets and confounded label. 30 reps each."""
import sys, warnings, numpy as np
sys.path.insert(0, sys.argv[1] + '/scripts')
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from batch_checks import leave_one_batch_out, batch_predictability
warnings.simplefilter('error', FutureWarning)
probe = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(max_iter=3000))])
for arm in ('zero-signal confounded', 'real signal + confounded batch'):
    for nb in (2, 3, 6):
        res = []
        for rep in range(30):
            r = np.random.default_rng(50000 + 100 * nb + rep)
            batch = np.repeat(np.arange(nb), 30)
            y = (r.random(len(batch)) < np.where(batch < nb / 2, 0.25, 0.75)).astype(int)
            X = r.normal(batch[:, None] * 1.2, 1, (len(batch), 80))
            if arm.startswith('real'): X[:, :5] += y[:, None] * 1.0
            pooled, tab = leave_one_batch_out(probe, X, y, batch)
            res.append((cross_val_score(probe, X, y, cv=5, scoring='roc_auc').mean(), tab.auc.mean(), pooled, batch_predictability(probe, X, batch)))
        a = np.array(res)
        print(f'{arm} | {nb} batches: random-split {a[:,0].mean():.2f} | LOBO per-batch mean {a[:,1].mean():.2f} (sd across reps {a[:,1].std(ddof=1):.3f}) | pooled {a[:,2].mean():.2f} | batch predictability {a[:,3].mean():.2f}', flush=True)
