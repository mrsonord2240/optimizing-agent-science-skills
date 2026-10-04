"""Leakage by test: (1) held-out rows perturbed -> in-fold selection, scaling and tuning unchanged (exact SKILL.md blocks 0-2 exec'd);
(2) leaky-vs-in-pipeline gap on permuted labels (Golub 1000 probes). Usage: python -W error::FutureWarning leakage_tests.py <SKILL.md> <golub_top1000.csv>"""
import sys, re, time
sys.dont_write_bytecode = True
import numpy as np, pandas as pd
from sklearn.base import clone
from sklearn.model_selection import cross_validate, cross_val_score, StratifiedKFold
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
df = pd.read_csv(sys.argv[2]); y = (df.pop('label') == 'AML').astype(int); X = df.astype(float)
blocks = re.findall(r"```python\n(.*?)```", open(sys.argv[1], encoding='utf-8').read(), re.S)
ns = {'X': X, 'y': y, '__name__': '__skill__'}
for i in (0, 1, 2): exec(compile(blocks[i], f'SKILL.md#block{i}', 'exec'), ns)
pipe, tuned, mrmr_pipe, cv = ns['pipe'], ns['tuned'], ns['mrmr_pipe'], ns['cv']
print('block0 AUC', ns['auc'].mean().round(3), 'nested AUC', ns['nested_auc'].mean().round(3), 'mrmr AUC', ns['mrmr_auc'].mean().round(3), flush=True)
splits = list(cv.split(X, y))
def garbage(k):
    tr, te = splits[k]; X2 = X.copy(); y2 = y.copy()
    r = np.random.default_rng(99 + k)
    X2.iloc[te] = r.normal(loc=500, scale=300, size=(len(te), X.shape[1]))
    y2.iloc[te] = 1 - y.iloc[te].values
    return X2, y2
def fold_est(est, Xm, ym, k):
    res = cross_validate(est, Xm, ym, cv=splits, scoring='roc_auc', return_estimator=True)
    return res['estimator'][k], res['test_score'][k]
ok = True
for k in (0, 3):
    X2, y2 = garbage(k)
    # in-pipeline: scaler mean/scale, selected idx, coef
    e1, s1 = fold_est(pipe, X, y, k); e2, s2 = fold_est(pipe, X2, y2, k)
    same = (np.array_equal(e1['scale'].mean_, e2['scale'].mean_) and np.array_equal(e1['select'].get_support(), e2['select'].get_support())
            and np.array_equal(e1['clf'].coef_, e2['clf'].coef_))
    print(f'fold{k} PIPELINE scaler/selection/coef identical after held-out perturbation: {same}; fold score {s1:.3f} -> {s2:.3f}', flush=True); ok &= same
    # nested tuning
    t1, ts1 = fold_est(tuned, X, y, k); t2, ts2 = fold_est(tuned, X2, y2, k)
    same = t1.best_params_ == t2.best_params_ and np.array_equal(t1.cv_results_['mean_test_score'], t2.cv_results_['mean_test_score'])
    print(f'fold{k} NESTED GridSearchCV best_params {t1.best_params_} identical & inner cv scores identical: {same}; outer score {ts1:.3f} -> {ts2:.3f}', flush=True); ok &= same
    # mrmr in fold
    m1, ms1 = fold_est(mrmr_pipe, X, y, k); m2, ms2 = fold_est(mrmr_pipe, X2, y2, k)
    same = list(m1['select'].cols_) == list(m2['select'].cols_) and np.array_equal(m1['scale'].mean_, m2['scale'].mean_)
    print(f'fold{k} MRMR in-fold cols_ identical: {same} (K={len(m1["select"].cols_)}); fold score {ms1:.3f} -> {ms2:.3f}', flush=True); ok &= same
# positive control: the WRONG pre-CV selection does change when held-out rows change
X2, y2 = garbage(0)
a = SelectKBest(f_classif, k=20).fit(X, y).get_support(); b = SelectKBest(f_classif, k=20).fit(X2, y2).get_support()
print(f'POSITIVE CONTROL (selection on all rows) differs after the same perturbation: {not np.array_equal(a, b)}  ({int((a != b).sum())//2} of 20 swapped)')
# permuted-label gap
leaky, honest, nest = [], [], []
for i in range(5):
    yp = pd.Series(np.random.default_rng(500 + i).permutation(y.values))
    top = SelectKBest(f_classif, k=20).fit(X, yp).get_support(indices=True)
    leaky.append(cross_val_score(LogisticRegression(max_iter=5000), X.iloc[:, top], yp, cv=cv, scoring='roc_auc').mean())
    honest.append(cross_val_score(pipe, X, yp, cv=cv, scoring='roc_auc').mean())
    nest.append(cross_val_score(tuned, X, yp, cv=cv, scoring='roc_auc').mean())
    print(f'PERM{i}: leaky(select-before-CV) AUC={leaky[-1]:.2f} in-pipeline={honest[-1]:.2f} nested-tuned={nest[-1]:.2f}', flush=True)
print(f'PERMUTED SUMMARY mean leaky {np.mean(leaky):.2f} in-pipeline {np.mean(honest):.2f} nested {np.mean(nest):.2f}')
print('RESULT', 'PASS' if ok else 'FAIL')
