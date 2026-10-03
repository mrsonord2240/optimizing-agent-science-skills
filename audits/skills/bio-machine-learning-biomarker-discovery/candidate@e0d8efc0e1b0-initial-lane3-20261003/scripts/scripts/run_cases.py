"""Audit run for bio-machine-learning-biomarker-discovery (lane 3, 2026-10-03).

Runs the SKILL.md snippets (apart from the data variables) on real Golub 1999 ALL/AML
expression (OpenML 1104, 72 x 7129; 47 ALL / 25 AML). No supervised step touches the data before
the split; the only prefilter is an unsupervised variance filter (labels unused).
Usage: python run_cases.py <case>   (case in c1..c5)
"""
import sys, json, time, warnings, collections
import numpy as np, pandas as pd

DATA = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\public-data\expression\golub_leukemia_openml.csv"
df = pd.read_csv(DATA)
y = (df.pop('label') == 'AML').astype(int)
X_full = df
case = sys.argv[1]


def load(var_keep=None):
    X = X_full
    if var_keep:                                   # unsupervised prefilter: label-free
        X = X.loc[:, X.var().sort_values(ascending=False).index[:var_keep]]
    return X


def wsummary(ws):
    return dict(collections.Counter(w.category.__name__ for w in ws))


from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler

out = {}
if case == 'c1':   # SKILL.md leakage-safe snippet on Golub raw intensities; scaled variant; permutation null
    X = load()
    pipe = Pipeline([('select', SelectKBest(f_classif, k=20)), ('clf', LogisticRegression(max_iter=5000))])
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        auc = cross_val_score(pipe, X, y, cv=cv, scoring='roc_auc')
    out['verbatim_raw'] = dict(mean=auc.mean(), std=auc.std(), warnings=wsummary(ws))
    pipe_s = Pipeline([('scale', StandardScaler()), ('select', SelectKBest(f_classif, k=20)), ('clf', LogisticRegression(max_iter=5000))])
    with warnings.catch_warnings(record=True) as ws:
        warnings.simplefilter('always')
        auc2 = cross_val_score(pipe_s, X, y, cv=cv, scoring='roc_auc')
    out['with_scaler_in_pipeline'] = dict(mean=auc2.mean(), std=auc2.std(), warnings=wsummary(ws))
    leaky, safe = [], []
    for s in range(10):
        yn = pd.Series(np.random.default_rng(100 + s).permutation(y.values))
        Xs = SelectKBest(f_classif, k=20).fit_transform(X, yn)
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            leaky.append(cross_val_score(LogisticRegression(max_iter=5000), Xs, yn, cv=cv, scoring='roc_auc').mean())
            safe.append(cross_val_score(pipe, X, yn, cv=cv, scoring='roc_auc').mean())
    out['perm_null'] = dict(leaky_mean=float(np.mean(leaky)), leaky_min=float(np.min(leaky)), safe_mean=float(np.mean(safe)),
                            safe_min=float(np.min(safe)), safe_max=float(np.max(safe)), leaky=leaky, safe=safe)
    reps = []
    for s in range(5):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            reps.append(cross_val_score(pipe_s, X, y, cv=StratifiedKFold(10, shuffle=True, random_state=s), scoring='roc_auc').mean())
    out['repeated_cv_scaled'] = reps

elif case == 'c2':  # Boruta snippet (unsupervised variance prefilter to 1000 probes) + null + in-split held-out
    from boruta import BorutaPy
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score
    X = load(1000)

    def run_boruta(Xd, yd, seed=42):
        rf = RandomForestClassifier(n_estimators=100, n_jobs=-1, class_weight='balanced', max_depth=5, random_state=42)
        b = BorutaPy(rf, n_estimators='auto', perc=100, two_step=True, max_iter=100, random_state=seed)
        b.fit(Xd.values, yd.values)
        return b
    t = time.time(); b = run_boruta(X, y)
    out['real_labels'] = dict(confirmed=int(b.support_.sum()), tentative=int(b.support_weak_.sum()), secs=time.time() - t)
    yn = pd.Series(np.random.default_rng(7).permutation(y.values))
    bn = run_boruta(X, yn)
    out['permuted_labels'] = dict(confirmed=int(bn.support_.sum()), tentative=int(bn.support_weak_.sum()))
    res = []
    for s in range(3):
        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.4, stratify=y, random_state=s)
        bb = run_boruta(Xtr, ytr)
        cols = Xtr.columns[bb.support_]
        if len(cols) == 0:
            res.append(dict(seed=s, n_confirmed=0)); continue
        rf = RandomForestClassifier(n_estimators=300, random_state=0, class_weight='balanced').fit(Xtr[cols], ytr)
        res.append(dict(seed=s, n_confirmed=len(cols), heldout_auc=float(roc_auc_score(yte, rf.predict_proba(Xte[cols])[:, 1]))))
    out['boruta_in_split_heldout'] = res

elif case == 'c3':  # elastic net snippet; scoring variants; coef shape; determinism; held-out pipeline AUC
    X = load(1000)
    Xs = StandardScaler().fit_transform(X)
    res = {}
    for sc in ['neg_log_loss', 'accuracy', 'roc_auc']:
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter('always')
            enet = LogisticRegressionCV(solver='saga', l1_ratios=[0.1, 0.5, 0.9], Cs=20, cv=10, max_iter=10000,
                                        scoring=sc, use_legacy_attributes=False, random_state=0)
            enet.fit(Xs, y)
        sel = X.columns[enet.coef_[0] != 0]
        res[sc] = dict(n_selected=len(sel), l1_ratio=float(enet.l1_ratio_), C=float(enet.C_), coef_shape=list(enet.coef_.shape), warnings=wsummary(ws))
    out['scoring_variants'] = res
    sels = []
    for _ in range(2):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            e = LogisticRegressionCV(solver='saga', l1_ratios=[0.1, 0.5, 0.9], Cs=20, cv=10, max_iter=10000,
                                     scoring='neg_log_loss', use_legacy_attributes=False).fit(Xs, y)
        sels.append(set(X.columns[e.coef_[0] != 0]))
    out['verbatim_repeat'] = dict(n1=len(sels[0]), n2=len(sels[1]), identical=sels[0] == sels[1])
    cv = StratifiedKFold(10, shuffle=True, random_state=0)
    enet_pipe = Pipeline([('scale', StandardScaler()), ('enet', LogisticRegressionCV(
        solver='saga', l1_ratios=[0.1, 0.5, 0.9], Cs=10, cv=5, max_iter=5000,
        scoring='neg_log_loss', use_legacy_attributes=False, random_state=0))])
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        honest = cross_val_score(enet_pipe, X, y, cv=cv, scoring='roc_auc')
    out['enet_pipeline_heldout_auc'] = dict(mean=honest.mean(), std=honest.std())
    yn = pd.Series(np.random.default_rng(3).permutation(y.values))
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        nullauc = cross_val_score(enet_pipe, X, yn, cv=cv, scoring='roc_auc')
    out['enet_pipeline_permuted_auc'] = dict(mean=nullauc.mean(), std=nullauc.std())

elif case == 'c4':  # stability snippet: determinism (unseeded), raw vs scaled, null labels, empty selection
    X = load(1000)

    def stab(Xd, yd, C=0.1):
        n_subsample, p = 100, Xd.shape[1]
        counts = np.zeros(p); subsets = []
        for _ in range(n_subsample):
            idx = np.random.choice(len(Xd), size=len(Xd) // 2, replace=False)
            fit = LogisticRegression(l1_ratio=1, solver='liblinear', C=C, max_iter=2000).fit(Xd.iloc[idx], yd.iloc[idx])
            mask = fit.coef_[0] != 0
            counts += mask; subsets.append(mask.astype(int))
        stable = Xd.columns[counts / n_subsample > 0.6]
        Z = np.array(subsets); k = Z.sum(axis=1)
        with np.errstate(all='ignore'):
            st = 1 - (Z.var(axis=0, ddof=1).mean()) / ((k.mean() / p) * (1 - k.mean() / p))
        return dict(n_stable=len(stable), nogueira=float(st), mean_k=float(k.mean()))
    out['verbatim_raw_run1'] = stab(X, y)
    out['verbatim_raw_run2'] = stab(X, y)
    Xs = pd.DataFrame(StandardScaler().fit_transform(X), columns=X.columns)
    out['scaled_C0.1'] = stab(Xs, y)
    yn = pd.Series(np.random.default_rng(11).permutation(y.values))
    out['permuted_raw_C0.1'] = stab(X, yn)
    out['permuted_scaled_C0.1'] = stab(Xs, yn)
    out['tiny_C_raw_empty_selection'] = stab(X, y, C=1e-7)

elif case == 'c5':  # mRMR: input types; outside-CV leakage with permuted labels
    from mrmr import mrmr_classif
    X = load(1000)
    r = mrmr_classif(X=X, y=y, K=5, show_progress=False)
    out['pandas_ok'] = [str(i) for i in r]
    try:
        r2 = mrmr_classif(X=X.values, y=y.values, K=5, show_progress=False); out['numpy_result'] = str(r2)[:200]
    except Exception as e:
        out['numpy_error'] = f'{type(e).__name__}: {str(e)[:160]}'
    yn = pd.Series(np.random.default_rng(5).permutation(y.values))
    top = mrmr_classif(X=X, y=yn, K=20, show_progress=False)
    cv = StratifiedKFold(10, shuffle=True, random_state=0)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        out['mrmr_outside_cv_permuted_auc'] = float(cross_val_score(
            LogisticRegression(max_iter=5000), StandardScaler().fit_transform(X[top]), yn, cv=cv, scoring='roc_auc').mean())

elif case == 'c6':  # claim check: minimal-optimal (L1/elastic net) keeps ~1 of a 5-gene module (boruta script data)
    rng = np.random.default_rng(0)
    n, p = 200, 60
    latent = rng.normal(size=n)
    Xm = rng.normal(size=(n, p))
    Xm[:, :5] = latent[:, None] + rng.normal(scale=0.3, size=(n, 5))
    ym = (latent + rng.normal(scale=0.3, size=n) > 0).astype(int)
    Xm = pd.DataFrame(Xm, columns=[f'g{i}' for i in range(p)])
    Xz = StandardScaler().fit_transform(Xm)
    res = {}
    for name, l1r in [('lasso', [1.0]), ('enet', [0.1, 0.5, 0.9])]:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            m = LogisticRegressionCV(solver='saga', l1_ratios=l1r, Cs=20, cv=5, max_iter=10000,
                                     scoring='neg_log_loss', use_legacy_attributes=False, random_state=0).fit(Xz, ym)
        nz = np.flatnonzero(m.coef_[0] != 0)
        res[name] = dict(selected=[f'g{i}' for i in nz], module_kept=int(sum(i < 5 for i in nz)), C=float(m.C_), l1_ratio=float(m.l1_ratio_))
    for C in [0.01, 0.05, 0.2]:
        m = LogisticRegression(l1_ratio=1, solver='liblinear', C=C).fit(Xz, ym)
        nz = np.flatnonzero(m.coef_[0] != 0)
        res[f'lasso_C{C}'] = dict(selected=[f'g{i}' for i in nz], module_kept=int(sum(i < 5 for i in nz)))
    out = res

elif case == 'c7':  # convergence warning lead: SKILL.md pipeline on tooling's 50%-variance subset, raw vs scaled
    X = X_full.loc[:, X_full.var() > X_full.var().quantile(0.5)]
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=0)
    for name, pipe in [('raw', Pipeline([('select', SelectKBest(f_classif, k=20)), ('clf', LogisticRegression(max_iter=5000))])),
                       ('scaled', Pipeline([('scale', StandardScaler()), ('select', SelectKBest(f_classif, k=20)), ('clf', LogisticRegression(max_iter=5000))]))]:
        with warnings.catch_warnings(record=True) as ws:
            warnings.simplefilter('always')
            a = cross_val_score(pipe, X, y, cv=cv, scoring='roc_auc')
        out[name] = dict(shape=list(X.shape), mean=a.mean(), std=a.std(), warnings=wsummary(ws))

print(json.dumps(out, indent=1, default=float))
