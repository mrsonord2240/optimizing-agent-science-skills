# bio-machine-learning-model-validation -- all 7 inputs.
# Applied to the candidate's own domain: hERG ECFP4 QSAR, with scaffold as the group.
import warnings
import numpy as np
import pandas as pd
import sklearn
from sklearn.model_selection import (cross_val_score, cross_val_predict, GridSearchCV,
                                     StratifiedKFold, StratifiedGroupKFold, LeaveOneOut,
                                     RepeatedStratifiedKFold, train_test_split)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import roc_auc_score, brier_score_loss, average_precision_score

print(f"sklearn {sklearn.__version__}")
D = r"F:\OpenScience\audits\bio-qsar-modeling\run"
X = np.load(D + r"\X.npy").astype(np.float32)
yc = np.load(D + r"\y.npy")
y = (yc >= 6.0).astype(int)
smi = pd.read_csv(D + r"\herg_unique.csv").canonical_smiles
from rdkit import Chem, RDLogger
from rdkit.Chem.Scaffolds import MurckoScaffold
RDLogger.DisableLog('rdApp.*')
scaf = np.array([MurckoScaffold.MurckoScaffoldSmiles(mol=Chem.MolFromSmiles(s)) for s in smi])
print(f"[data] X={X.shape} positives={y.sum()} ({100*y.mean():.1f}%) "
      f"distinct scaffolds={len(set(scaf))}")

# keep it tractable: 1200-compound subsample, still real data
rs = np.random.RandomState(0)
idx = rs.choice(len(y), 1200, replace=False)
Xs, ys, gs = X[idx][:, X[idx].sum(0) > 0], y[idx], scaf[idx]
print(f"[subset] X={Xs.shape} positives={ys.sum()} groups={len(set(gs))}")

pipe = Pipeline([('scaler', StandardScaler()),
                 ('select', SelectKBest(f_classif)),
                 ('clf', LogisticRegression(max_iter=5000))])
grid = {'select__k': [10, 50, 200], 'clf__C': [0.01, 0.1, 1]}

# ===== INPUT 1 (Canonical): nested vs flat CV ==============================
print("\n===== INPUT 1: nested CV against flat CV -- how much optimism? =====")
inner = StratifiedKFold(5, shuffle=True, random_state=0)
outer = StratifiedKFold(5, shuffle=True, random_state=1)
search = GridSearchCV(pipe, grid, cv=inner, scoring='roc_auc', n_jobs=-1)
nested = cross_val_score(search, Xs, ys, cv=outer, scoring='roc_auc', n_jobs=1)
print(f"  Nested AUC: {nested.mean():.3f} +/- {nested.std():.3f}   (SKILL.md snippet, verbatim)")
search.fit(Xs, ys)
print(f"  Flat CV best score (the same data used to choose AND grade): "
      f"{search.best_score_:.3f}   best params={search.best_params_}")
print(f"  optimism = {search.best_score_ - nested.mean():+.3f} AUC "
      f"-- SKILL.md: 'Flat CV with tuning is a known reviewer red flag'")

# ===== INPUT 2 (Variant A): the two leakage modes, on pure noise ===========
print("\n===== INPUT 2: leakage on PURE NOISE (Ambroise 2002 claim) =====")
rs = np.random.RandomState(42)
Xn = rs.normal(size=(200, 5000))
yn = rs.randint(0, 2, 200)
print(f"  synthetic: {Xn.shape} random normal features, random labels, "
      f"true signal = ZERO by construction")
sel = SelectKBest(f_classif, k=20).fit(Xn, yn)          # chosen on ALL data -- the leak
Xn_leak = sel.transform(Xn)
clf = LogisticRegression(max_iter=5000)
auc_leak = cross_val_score(clf, Xn_leak, yn, cv=StratifiedKFold(5, shuffle=True,
                                                               random_state=0),
                           scoring='roc_auc').mean()
pipe_clean = Pipeline([('select', SelectKBest(f_classif, k=20)),
                       ('clf', LogisticRegression(max_iter=5000))])
auc_clean = cross_val_score(pipe_clean, Xn, yn, cv=StratifiedKFold(5, shuffle=True,
                                                                  random_state=0),
                            scoring='roc_auc').mean()
print(f"  selection OUTSIDE the fold (leaky):  CV AUC = {auc_leak:.3f}")
print(f"  selection INSIDE the Pipeline      :  CV AUC = {auc_clean:.3f}")
print(f"  -> the leak manufactures {auc_leak - auc_clean:+.3f} AUC out of nothing")

sc = StandardScaler().fit(Xn)                            # preprocessing leak
auc_pp_leak = cross_val_score(LogisticRegression(max_iter=5000), sc.transform(Xn), yn,
                              cv=5, scoring='roc_auc').mean()
auc_pp_clean = cross_val_score(Pipeline([('s', StandardScaler()),
                                         ('c', LogisticRegression(max_iter=5000))]),
                               Xn, yn, cv=5, scoring='roc_auc').mean()
print(f"  scaler fit on all data: {auc_pp_leak:.3f}  vs inside the Pipeline: "
      f"{auc_pp_clean:.3f}  (difference {auc_pp_leak-auc_pp_clean:+.3f})")

# ===== INPUT 3 (Variant B): group-aware CV ================================
print("\n===== INPUT 3: StratifiedGroupKFold with scaffold as the unit of independence =====")
plain = cross_val_score(pipe, Xs, ys, cv=StratifiedKFold(5, shuffle=True, random_state=0),
                        scoring='roc_auc', n_jobs=-1)
gcv = StratifiedGroupKFold(n_splits=5)
grouped = cross_val_score(pipe, Xs, ys, cv=gcv, groups=gs, scoring='roc_auc', n_jobs=-1)
print(f"  StratifiedKFold (ignores scaffold):  AUC {plain.mean():.3f} +/- {plain.std():.3f}")
print(f"  StratifiedGroupKFold (scaffold):     AUC {grouped.mean():.3f} +/- {grouped.std():.3f}")
print(f"  inflation from ignoring the group: {plain.mean()-grouped.mean():+.3f} AUC")
leak = 0
for tr, te in StratifiedKFold(5, shuffle=True, random_state=0).split(Xs, ys):
    leak += len(set(gs[tr]) & set(gs[te]))
print(f"  scaffolds spanning train and test under plain KFold: {leak} (summed over folds)")
leak_g = sum(len(set(gs[tr]) & set(gs[te])) for tr, te in gcv.split(Xs, ys, groups=gs))
print(f"  same count under StratifiedGroupKFold: {leak_g}")
rcv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=0)
r = cross_val_score(pipe, Xs, ys, cv=rcv, scoring='roc_auc', n_jobs=-1)
print(f"  RepeatedStratifiedKFold 5x10: AUC {r.mean():.3f} +/- {r.std():.3f}  "
      f"(90% of draws in [{np.percentile(r,5):.3f}, {np.percentile(r,95):.3f}])")

# ===== INPUT 4 (Edge): the documented sklearn API drift ===================
print("\n===== INPUT 4: the CalibratedClassifierCV API drift the Skill flags =====")
Xtr, Xte, ytr, yte = train_test_split(Xs, ys, test_size=0.3, random_state=0, stratify=ys)
Xfit, Xcal, yfit, ycal = train_test_split(Xtr, ytr, test_size=0.33, random_state=0,
                                          stratify=ytr)
base = RandomForestClassifier(n_estimators=300, random_state=0, n_jobs=-1).fit(Xfit, yfit)
try:
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        c = CalibratedClassifierCV(base, cv='prefit', method='isotonic')
        c.fit(Xcal, ycal)
    print("  cv='prefit' still works silently (no warning, no error)")
except Exception as e:                                       # noqa: BLE001
    print(f"  cv='prefit' -> {type(e).__name__}: {str(e)[:110]}")
try:
    from sklearn.frozen import FrozenEstimator               # SKILL.md fix
    cal = CalibratedClassifierCV(FrozenEstimator(base), method='isotonic')
    cal.fit(Xcal, ycal)
    p_raw = base.predict_proba(Xte)[:, 1]
    p_cal = cal.predict_proba(Xte)[:, 1]
    print(f"  FrozenEstimator route -> OK")
    print(f"    uncalibrated: AUC={roc_auc_score(yte,p_raw):.3f} "
          f"Brier={brier_score_loss(yte,p_raw):.4f}")
    print(f"    calibrated  : AUC={roc_auc_score(yte,p_cal):.3f} "
          f"Brier={brier_score_loss(yte,p_cal):.4f}")
except Exception as e:                                       # noqa: BLE001
    print(f"  FrozenEstimator route FAILED: {type(e).__name__}: {e}")
for m in ['sigmoid', 'isotonic', 'temperature']:
    try:
        from sklearn.frozen import FrozenEstimator
        CalibratedClassifierCV(FrozenEstimator(base), method=m).fit(Xcal, ycal)
        print(f"    method={m!r}: available")
    except Exception as e:                                   # noqa: BLE001
        print(f"    method={m!r}: {type(e).__name__}: {str(e)[:60]}")

# ===== INPUT 5 (Stress): calibration curve + decision curve ===============
print("\n===== INPUT 5: reliability curve, Brier, and net benefit =====")
for strat in ['uniform', 'quantile']:
    pt_true, pt_pred = calibration_curve(yte, p_raw, n_bins=10, strategy=strat)
    gap = float(np.mean(np.abs(pt_true - pt_pred)))
    print(f"  calibration_curve strategy={strat!r}: {len(pt_true)} non-empty bins, "
          f"mean |gap| = {gap:.4f}")
print(f"  Brier (raw)={brier_score_loss(yte,p_raw):.4f}  "
      f"Brier (calibrated)={brier_score_loss(yte,p_cal):.4f}")
print(f"  AUPRC={average_precision_score(yte,p_raw):.3f} against a prevalence baseline "
      f"of {yte.mean():.3f}  (SKILL.md: 'Baseline is the prevalence, not 0.5')")


def net_benefit(y_true, p, pt):                              # SKILL.md formula verbatim
    n = len(y_true)
    pred = p >= pt
    tp = int(((pred == 1) & (y_true == 1)).sum())
    fp = int(((pred == 1) & (y_true == 0)).sum())
    return tp / n - (fp / n) * (pt / (1 - pt))


print(f"  {'pt':>6} {'model':>9} {'treat-all':>10} {'treat-none':>11}  useful?")
for pt in [0.2, 0.4, 0.5, 0.6, 0.8]:
    nb = net_benefit(yte, p_cal, pt)
    nb_all = net_benefit(yte, np.ones_like(p_cal), pt)
    print(f"  {pt:>6.2f} {nb:>9.4f} {nb_all:>10.4f} {0.0:>11.4f}  "
          f"{'yes' if nb > max(nb_all, 0) else 'no'}")

# ===== INPUT 6 (Scope boundary): SMOTE for a risk model ==================
print("\n===== INPUT 6: does resampling for imbalance break calibration? =====")
try:
    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import Pipeline as ImbPipeline
    sm = ImbPipeline([('sm', SMOTE(random_state=0)),
                      ('clf', RandomForestClassifier(n_estimators=300, random_state=0,
                                                     n_jobs=-1))]).fit(Xfit, yfit)
    p_sm = sm.predict_proba(Xte)[:, 1]
    print(f"  no resampling : AUC={roc_auc_score(yte,p_raw):.3f} "
          f"Brier={brier_score_loss(yte,p_raw):.4f} mean predicted p={p_raw.mean():.3f}")
    print(f"  with SMOTE    : AUC={roc_auc_score(yte,p_sm):.3f} "
          f"Brier={brier_score_loss(yte,p_sm):.4f} mean predicted p={p_sm.mean():.3f}")
    print(f"  observed prevalence in the test set = {yte.mean():.3f}")
    print(f"  -> SKILL.md (van den Goorbergh 2022): 'Changing training prevalence "
          f"inflates minority-class probabilities; no AUC gain'")
except Exception as e:                                       # noqa: BLE001
    print(f"  imbalanced-learn route FAILED: {type(e).__name__}: {e}")

# ===== INPUT 7 (Adversarial): LOO with AUC, and cross_val_predict =========
print("\n===== INPUT 7: 'just use leave-one-out, we only have 120 samples' =====")
small = rs.choice(len(ys), 120, replace=False)
Xsm, ysm = Xs[small][:, Xs[small].sum(0) > 0], ys[small]
print(f"  small set: {Xsm.shape}, positives={ysm.sum()}")
try:
    with warnings.catch_warnings():
        warnings.simplefilter('error')
        loo = cross_val_score(LogisticRegression(max_iter=5000), Xsm, ysm,
                              cv=LeaveOneOut(), scoring='roc_auc')
    print(f"  LOO + roc_auc: mean={np.nanmean(loo):.3f}")
except Exception as e:                                       # noqa: BLE001
    print(f"  LOO + roc_auc -> {type(e).__name__}: {str(e)[:120]}")
oof = cross_val_predict(LogisticRegression(max_iter=5000), Xsm, ysm,
                        cv=LeaveOneOut(), method='predict_proba')[:, 1]
print(f"  pooled LOO OOF predictions scored once: AUC={roc_auc_score(ysm, oof):.3f}")
fold_scores = cross_val_score(LogisticRegression(max_iter=5000), Xsm, ysm,
                              cv=StratifiedKFold(5, shuffle=True, random_state=0),
                              scoring='roc_auc')
print(f"  averaged per-fold 5-fold AUC (the Skill's prescription): "
      f"{fold_scores.mean():.3f} +/- {fold_scores.std():.3f}")
oof5 = cross_val_predict(LogisticRegression(max_iter=5000), Xsm, ysm,
                         cv=StratifiedKFold(5, shuffle=True, random_state=0),
                         method='predict_proba')[:, 1]
print(f"  pooled 5-fold OOF scored once: AUC={roc_auc_score(ysm, oof5):.3f}  "
      f"(difference from the fold average: "
      f"{roc_auc_score(ysm, oof5) - fold_scores.mean():+.3f})")
rep = cross_val_score(LogisticRegression(max_iter=5000), Xsm, ysm,
                      cv=RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=0),
                      scoring='roc_auc')
print(f"  repeated 5x10 (the Skill's fix): {rep.mean():.3f} +/- {rep.std():.3f}, "
      f"range [{rep.min():.3f}, {rep.max():.3f}]")
