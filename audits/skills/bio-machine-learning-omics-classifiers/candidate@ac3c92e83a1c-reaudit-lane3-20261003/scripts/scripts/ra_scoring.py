"""Independent OC-003 check on Golub (own splits, seeds 20-22). Usage: python ra_scoring.py <Skill dir> [seeds]
Runs the SKILL.md Core Workflow fit and the lasso+1-SE snippet verbatim logic; verifies the 1-SE rule by recomputation."""
import sys, os, re, time, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import roc_auc_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegressionCV, LogisticRegression
warnings.simplefilter('error', FutureWarning)
G = pd.read_csv('F:/OpenScience/audit-envs/cheminformatics-hit-triage-analyst/public-data/expression/golub_leukemia_openml.csv')
y = pd.factorize(G.pop('label'))[0]; X = G.values.astype(float)
X = X[:, np.argsort(-X.var(0))[:2000]]
seeds = [int(s) for s in sys.argv[2:]] or [20, 21, 22]
for seed in seeds:
    t = time.time()
    X_train, X_te, y_train, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=seed)
    # Core Workflow fit, verbatim parameters
    clf = LogisticRegressionCV(solver='saga', l1_ratios=[0.1, 0.5, 0.9], Cs=20, cv=5, max_iter=10000, scoring='neg_log_loss', use_legacy_attributes=False)
    pipe = Pipeline([('scaler', StandardScaler()), ('clf', clf)]).fit(X_train, y_train)
    nnz_dense = int((clf.coef_ != 0).sum()); auc_dense = roc_auc_score(y_te, pipe.predict_proba(X_te)[:, 1])
    # 1-SE snippet verbatim
    lasso = LogisticRegressionCV(solver='saga', l1_ratios=[1.0], Cs=20, cv=5, max_iter=10000, scoring='neg_log_loss', use_legacy_attributes=False)
    Pipeline([('scaler', StandardScaler()), ('clf', lasso)]).fit(X_train, y_train)
    folds = lasso.scores_[:, 0, :]
    mean, se = folds.mean(0), folds.std(0, ddof=1) / np.sqrt(folds.shape[0])
    c_1se = lasso.Cs_[np.flatnonzero(mean >= mean.max() - se[mean.argmax()]).min()]
    signature = Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression(solver='saga', l1_ratio=1.0, C=c_1se, max_iter=10000))]).fit(X_train, y_train)
    nnz_1se = int((signature['clf'].coef_ != 0).sum()); auc_1se = roc_auc_score(y_te, signature.predict_proba(X_te)[:, 1])
    # --- independent verification of the rule ---
    shape, ascending = folds.shape, bool(np.all(np.diff(lasso.Cs_) > 0))
    # recompute one (fold, C) score by hand: StratifiedKFold(5) unshuffled on X_train, scaler fit on all X_train as in the Pipeline
    Xs = StandardScaler().fit_transform(X_train)
    tr, va = next(iter(StratifiedKFold(5).split(Xs, y_train)))
    j = 7; m = LogisticRegression(solver='saga', l1_ratio=1.0, C=lasso.Cs_[j], max_iter=10000).fit(Xs[tr], y_train[tr])
    hand = -log_loss(y_train[va], m.predict_proba(Xs[va]))
    # rule applied by an independent expression: all C within 1 SE (of the best-mean C) of the best mean; pick smallest
    best = mean.argmax(); thr = mean[best] - se[best]; within = [i for i in range(len(mean)) if mean[i] >= thr]
    c_ref = lasso.Cs_[min(within)]
    print(f'seed {seed}: dense EN nnz {nnz_dense}/2000 AUC {auc_dense:.3f} chosen C {clf.C_} | lasso scores_ shape {shape} Cs ascending {ascending} | '
          f'hand fold0 C[{j}] {hand:.4f} vs scores_ {folds[0, j]:.4f} | 1-SE C {c_1se:.5g} (ref {c_ref:.5g}), best-mean C {lasso.Cs_[best]:.5g}, '
          f'index {min(within)} of {len(mean)} | 1-SE nnz {nnz_1se} AUC {auc_1se:.3f} | train rows in CV: {X_train.shape[0]}, test rows untouched: {X_te.shape[0]} | {time.time()-t:.0f}s', flush=True)
