"""Where do lbfgs ConvergenceWarnings occur for the SKILL.md leakage-safe pipeline on raw Golub intensities?"""
import warnings, collections, json
import numpy as np, pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
df = pd.read_csv(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\expression\golub_leukemia_openml.csv")
y = (df.pop('label') == 'AML').astype(int); X = df
cv = StratifiedKFold(10, shuffle=True, random_state=0)
pipe = Pipeline([('select', SelectKBest(f_classif, k=20)), ('clf', LogisticRegression(max_iter=5000))])
out = {}
def run(name, fn):
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always'); v = fn()
    out[name] = dict(auc=float(np.mean(v)), warnings=dict(collections.Counter(w.category.__name__ for w in ws)))
run('real_labels_pipeline', lambda: cross_val_score(pipe, X, y, cv=cv, scoring='roc_auc'))
yn = pd.Series(np.random.default_rng(100).permutation(y.values))
run('permuted_labels_pipeline', lambda: cross_val_score(pipe, X, yn, cv=cv, scoring='roc_auc'))
Xs = SelectKBest(f_classif, k=20).fit_transform(X, yn)
run('permuted_labels_leaky_lr', lambda: cross_val_score(LogisticRegression(max_iter=5000), Xs, yn, cv=cv, scoring='roc_auc'))
print(json.dumps(out, indent=1))
