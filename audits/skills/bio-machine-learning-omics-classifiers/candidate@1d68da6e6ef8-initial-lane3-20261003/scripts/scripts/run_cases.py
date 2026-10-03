"""Audit run for bio-machine-learning-omics-classifiers (lane 3, 2026-10-03).

SKILL.md snippets run on real Golub 1999 ALL/AML expression (OpenML 1104, 72 x 7129; 47 ALL / 25 AML)
with a label-free variance prefilter (top 2000 probes) for speed, and on synthetic data where the
claim needs known prevalence / a known generative model. Held-out data scores every performance number.
Usage: python run_cases.py <case>   (o1..o7)
"""
import sys, json, warnings, collections
import numpy as np, pandas as pd

DATA = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\expression\golub_leukemia_openml.csv"
case = sys.argv[1]
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedGroupKFold, LeaveOneGroupOut, StratifiedKFold
from sklearn.metrics import roc_auc_score, brier_score_loss, log_loss
from scipy.stats import chi2_contingency


def golub(keep=2000):
    df = pd.read_csv(DATA)
    y = (df.pop('label') == 'AML').astype(int)
    X = df.loc[:, df.var().sort_values(ascending=False).index[:keep]]   # label-free prefilter
    return X, y


def ws(w):
    return dict(collections.Counter(x.category.__name__ for x in w))


def sim(n, p=500, k=15, prev=0.08, seed=0):
    """Linear logit with known intercept so the true prevalence is ~prev."""
    r = np.random.default_rng(seed)
    X = r.normal(size=(n, p))
    beta = np.zeros(p); beta[:k] = np.random.default_rng(12345).normal(scale=0.5, size=k)   # beta shared by train and test
    z = X @ beta
    # intercept chosen so mean sigmoid(z + b) = prev on a big reference draw
    ref = np.random.default_rng(999).normal(size=(20000, p)) @ beta
    lo, hi = -15, 5
    for _ in range(60):
        b = (lo + hi) / 2
        if (1 / (1 + np.exp(-(ref + b)))).mean() > prev: hi = b
        else: lo = b
    return X, (r.random(n) < 1 / (1 + np.exp(-(z + b)))).astype(int), b


out = {}
if case == 'o1':   # Core Workflow snippet verbatim on Golub, held-out; class_weight effect
    X, y = golub()
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
    for cw in ['balanced', None]:
        clf = LogisticRegressionCV(solver='saga', l1_ratios=[0.1, 0.5, 0.9], Cs=20, cv=5, max_iter=10000,
                                   class_weight=cw, scoring='neg_log_loss', use_legacy_attributes=False, random_state=0)
        pipe = Pipeline([('scaler', StandardScaler()), ('clf', clf)])
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            pipe.fit(Xtr, ytr)
        pr = pipe.predict_proba(Xte)[:, 1]
        out[f'class_weight={cw}'] = dict(heldout_auc=float(roc_auc_score(yte, pr)), brier=float(brier_score_loss(yte, pr)),
                                         logloss=float(log_loss(yte, pr)), mean_pred=float(pr.mean()), test_prevalence=float(yte.mean()),
                                         train_prevalence=float(ytr.mean()), n_selected=int((clf.coef_[0] != 0).sum()),
                                         C=float(clf.C_), l1_ratio=float(clf.l1_ratio_), coef_shape=list(clf.coef_.shape), warnings=ws(w))
    # SKILL.md first-line recommendation: LogisticRegression(solver='saga', l1_ratio=0.5)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        m = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(solver='saga', l1_ratio=0.5, max_iter=5000))]).fit(Xtr, ytr)
    out['quickref_LogisticRegression_saga_l1r0.5'] = dict(heldout_auc=float(roc_auc_score(yte, m.predict_proba(Xte)[:, 1])), warnings=ws(w))

elif case == 'o2':  # class_weight='balanced' vs prior shift on a risk model (known generative model, 8% prevalence)
    res = {}
    for seed in range(3):
        Xtr, ytr, b = sim(800, seed=seed); Xte, yte, _ = sim(20000, seed=100 + seed)
        row = {}
        for name, mk in [('logit_none', lambda: LogisticRegression(C=0.05, max_iter=5000)),
                         ('logit_balanced', lambda: LogisticRegression(C=0.05, max_iter=5000, class_weight='balanced')),
                         ('rf_none', lambda: RandomForestClassifier(300, min_samples_leaf=3, random_state=0, n_jobs=-1)),
                         ('rf_balanced', lambda: RandomForestClassifier(300, min_samples_leaf=3, class_weight='balanced', random_state=0, n_jobs=-1))]:
            m = Pipeline([('s', StandardScaler()), ('c', mk())]).fit(Xtr, ytr)
            pr = m.predict_proba(Xte)[:, 1]
            row[name] = dict(auc=float(roc_auc_score(yte, pr)), brier=float(brier_score_loss(yte, pr)),
                             mean_pred=float(pr.mean()))
        row['test_prevalence'] = float(yte.mean()); row['train_prevalence'] = float(ytr.mean())
        res[f'seed{seed}'] = row
    out = res

elif case == 'o3':  # SMOTE: leak outside the split on noise; "no AUC gain" claim on held-out
    from imblearn.pipeline import Pipeline as ImbPipeline
    from imblearn.over_sampling import SMOTE
    r = np.random.default_rng(0)
    n, p = 120, 300
    Xn = r.normal(size=(n, p)); yn = (r.random(n) < 0.15).astype(int)
    cv = StratifiedKFold(5, shuffle=True, random_state=0)
    lr = lambda: LogisticRegression(max_iter=5000)
    Xr, yr = SMOTE(random_state=0).fit_resample(Xn, yn)
    # leaky: resample first, then CV (synthetic neighbours of test points sit in train folds)
    out['noise_smote_before_split_cv_auc'] = float(cross_val_score(lr(), Xr, yr, cv=cv, scoring='roc_auc').mean())
    imb = ImbPipeline([('smote', SMOTE(random_state=0)), ('clf', LogisticRegression(max_iter=5000))])
    out['noise_smote_in_pipeline_cv_auc'] = float(cross_val_score(imb, Xn, yn, cv=cv, scoring='roc_auc').mean())
    # claim: SMOTE gives no AUC gain; held-out on a known linear model, several draws
    gains = []
    for seed in range(8):
        Xtr, ytr, _ = sim(400, p=200, k=10, prev=0.1, seed=seed); Xte, yte, _ = sim(10000, p=200, k=10, prev=0.1, seed=500 + seed)
        base = Pipeline([('s', StandardScaler()), ('c', LogisticRegression(C=0.05, max_iter=5000))]).fit(Xtr, ytr)
        sm = ImbPipeline([('smote', SMOTE(random_state=0)), ('s', StandardScaler()), ('c', LogisticRegression(C=0.05, max_iter=5000))]).fit(Xtr, ytr)
        a0 = roc_auc_score(yte, base.predict_proba(Xte)[:, 1]); a1 = roc_auc_score(yte, sm.predict_proba(Xte)[:, 1])
        gains.append(dict(seed=seed, auc_plain=float(a0), auc_smote=float(a1), mean_pred_plain=float(base.predict_proba(Xte)[:, 1].mean()),
                          mean_pred_smote=float(sm.predict_proba(Xte)[:, 1].mean()), prevalence=float(yte.mean())))
    out['smote_vs_plain'] = gains
    out['smote_mean_auc_gain'] = float(np.mean([g['auc_smote'] - g['auc_plain'] for g in gains]))

elif case == 'o4':  # Calibration snippet verbatim on Golub (n=72 -> tiny calibration fold) and on a larger synthetic set
    from sklearn.calibration import CalibratedClassifierCV
    from sklearn.frozen import FrozenEstimator
    X, y = golub()
    Xtv, Xte, ytv, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)
    Xtr, Xcal, ytr, ycal = train_test_split(Xtv, ytv, test_size=0.4, stratify=ytv, random_state=0)
    rf = RandomForestClassifier(n_estimators=500, max_features='sqrt', min_samples_leaf=3, class_weight='balanced', n_jobs=-1, random_state=0)
    for method in ['isotonic', 'sigmoid']:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            calibrated = CalibratedClassifierCV(FrozenEstimator(rf.fit(Xtr, ytr)), method=method)
            calibrated.fit(Xcal, ycal)
        raw = rf.predict_proba(Xte)[:, 1]; cal = calibrated.predict_proba(Xte)[:, 1]
        out[f'golub_{method}'] = dict(n_cal=len(ycal), n_train=len(ytr), n_test=len(yte), auc_raw=float(roc_auc_score(yte, raw)),
                                      auc_cal=float(roc_auc_score(yte, cal)), brier_raw=float(brier_score_loss(yte, raw)),
                                      brier_cal=float(brier_score_loss(yte, cal)), n_unique_cal_probs=int(len(np.unique(cal.round(6)))),
                                      frac_exact_0_or_1=float(np.mean((cal < 1e-6) | (cal > 1 - 1e-6))), warnings=ws(w))
    Xs, ys, _ = sim(1500, p=300, k=20, prev=0.3, seed=1); Xe, ye, _ = sim(20000, p=300, k=20, prev=0.3, seed=2)
    Xa, Xc, ya, yc = train_test_split(Xs, ys, test_size=0.4, stratify=ys, random_state=0)
    rf2 = RandomForestClassifier(n_estimators=500, min_samples_leaf=3, n_jobs=-1, random_state=0).fit(Xa, ya)
    out['synthetic_raw_brier'] = float(brier_score_loss(ye, rf2.predict_proba(Xe)[:, 1]))
    for method in ['isotonic', 'sigmoid']:
        c = CalibratedClassifierCV(FrozenEstimator(rf2), method=method).fit(Xc, yc)
        out[f'synthetic_{method}_brier'] = float(brier_score_loss(ye, c.predict_proba(Xe)[:, 1]))

elif case == 'o5':  # XGBoost snippet verbatim: early-stopping validation set vs an untouched test set
    from xgboost import XGBClassifier
    X, y = golub()
    gaps = []
    for seed in range(5):
        Xtv, Xte, ytv, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=seed)
        Xtr, Xval, ytr, yval = train_test_split(Xtv, ytv, test_size=0.3, stratify=ytv, random_state=seed)
        xgb = XGBClassifier(n_estimators=2000, learning_rate=0.03, max_depth=4, subsample=0.8, colsample_bytree=0.5, reg_lambda=1.0,
                            early_stopping_rounds=50, eval_metric='aucpr', n_jobs=-1, random_state=0)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            xgb.fit(Xtr, ytr, eval_set=[(Xval, yval)], verbose=False)
        gaps.append(dict(seed=seed, best_iteration=int(xgb.best_iteration), best_val_aucpr=float(xgb.best_score),
                         val_auc_reused=float(roc_auc_score(yval, xgb.predict_proba(Xval)[:, 1])),
                         test_auc=float(roc_auc_score(yte, xgb.predict_proba(Xte)[:, 1])), n_val=len(yval), warnings=ws(w)))
    out['xgb_early_stop'] = gaps

elif case == 'o6':  # Batch snippet verbatim with 6 / 3 / 2 batches (synthetic batch labels; label confounded)
    def make(nb, n_per=40, seed=0):
        r = np.random.default_rng(seed)
        batch = np.repeat(np.arange(nb), n_per)
        case_rate = np.where(batch < nb / 2, 0.15, 0.85)
        label = (r.random(len(batch)) < case_rate).astype(int)
        Xb = r.normal(batch[:, None] * 2.0, 1.0, (len(label), 100))
        return Xb, label, batch
    for nb in [6, 3, 2]:
        X, y, batch_labels = make(nb)
        clf = LogisticRegressionCV(solver='saga', l1_ratios=[0.1, 0.5, 0.9], Cs=5, cv=3, max_iter=3000, class_weight='balanced',
                                   scoring='neg_log_loss', use_legacy_attributes=False, random_state=0)
        pipe = Pipeline([('scaler', StandardScaler()), ('clf', clf)])
        row = {}
        def attempt(name, fn):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                try: row[name] = float(np.mean(fn()))
                except Exception as e: row[name] = f'{type(e).__name__}: {str(e)[:150]}'
            fw = [x.category.__name__ for x in w if 'FitFailed' in x.category.__name__]
            if fw: row[name + '_warnings'] = ws([x for x in w if 'FitFailed' in x.category.__name__])
        attempt('batch_predictability_snippet', lambda: cross_val_score(pipe, X, batch_labels, cv=5, scoring='roc_auc'))
        row['chi2_p'] = float(chi2_contingency(pd.crosstab(y, batch_labels))[1])
        attempt('random_split_auc', lambda: cross_val_score(pipe, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring='roc_auc'))
        attempt('StratifiedGroupKFold5_snippet', lambda: cross_val_score(pipe, X, y, cv=StratifiedGroupKFold(n_splits=5), groups=batch_labels, scoring='roc_auc'))
        attempt('LeaveOneGroupOut', lambda: cross_val_score(pipe, X, y, cv=LeaveOneGroupOut(), groups=batch_labels, scoring='roc_auc'))
        out[f'{nb}_batches'] = row

elif case == 'o8':  # lead: scoring='neg_log_loss' (normalizer) vs accuracy (origin default) vs roc_auc: sparsity and held-out result
    X, y = golub()
    res = {}
    for seed in range(3):
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, stratify=y, random_state=seed)
        for sc in ['neg_log_loss', 'accuracy', 'roc_auc']:
            clf = LogisticRegressionCV(solver='saga', l1_ratios=[0.1, 0.5, 0.9], Cs=20, cv=5, max_iter=10000,
                                       class_weight='balanced', scoring=sc, use_legacy_attributes=False, random_state=0)
            pipe = Pipeline([('scaler', StandardScaler()), ('clf', clf)])
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter('always')
                pipe.fit(Xtr, ytr)
            pr = pipe.predict_proba(Xte)[:, 1]
            res[f'seed{seed}_{sc}'] = dict(n_selected=int((clf.coef_[0] != 0).sum()), C=float(clf.C_), l1_ratio=float(clf.l1_ratio_),
                                           heldout_auc=float(roc_auc_score(yte, pr)), logloss=float(log_loss(yte, pr)), warnings=ws(w))
    out = res

print(json.dumps(out, indent=1, default=float))
