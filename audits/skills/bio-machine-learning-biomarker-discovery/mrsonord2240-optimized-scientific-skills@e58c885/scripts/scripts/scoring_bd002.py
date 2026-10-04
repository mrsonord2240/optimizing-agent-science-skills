"""BD-002: LogisticRegressionCV scoring -> selected size, Golub 1000 probes, the SKILL.md enet block with scoring swapped.
Reproduces the stated table (601/203/148; perm 16/0/0; AUC .991/.983/.991) on the stated partition (cv=5 inner unshuffled; outer StratifiedKFold(5, shuffle, rs=0))
and then probes other partitions to judge over-generalization. Usage: python -W error::FutureWarning scoring_bd002.py <golub_top1000.csv>"""
import sys, time
sys.dont_write_bytecode = True
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import StratifiedKFold, cross_val_score
df = pd.read_csv(sys.argv[1]); y = (df.pop('label') == 'AML').astype(int).values; X = df
def mk(sc, cv=5, rs=None):
    return make_pipeline(StandardScaler(), LogisticRegressionCV(solver='saga', l1_ratios=[0.1, 0.5, 0.9], Cs=20, cv=cv, max_iter=10000,
                         scoring=sc, use_legacy_attributes=False, random_state=rs))
for sc in ('neg_log_loss', 'roc_auc', 'accuracy'):
    t = time.time(); m = mk(sc).fit(X, y); n = int((m[-1].coef_[0] != 0).sum())
    yp = np.random.default_rng(3).permutation(y); npm = int((mk(sc).fit(X, yp)[-1].coef_[0] != 0).sum())
    auc = cross_val_score(mk(sc), X, y, cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring='roc_auc').mean()
    print(f'STATED PARTITION scoring={sc}: selected={n} perm-label selected={npm} outer-AUC={auc:.3f} C={m[-1].C_:.3g} l1={m[-1].l1_ratio_} {time.time()-t:.0f}s', flush=True)
# other inner partitions (shuffled inner CV, different seeds): is the size ordering robust?
for seed in (1, 2):
    for sc in ('neg_log_loss', 'roc_auc', 'accuracy'):
        t = time.time(); m = mk(sc, cv=StratifiedKFold(5, shuffle=True, random_state=seed)).fit(X, y)
        print(f'OTHER PARTITION seed={seed} scoring={sc}: selected={int((m[-1].coef_[0] != 0).sum())} {time.time()-t:.0f}s', flush=True)
