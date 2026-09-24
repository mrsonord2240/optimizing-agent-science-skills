# bio-machine-learning-prediction-explanation -- all 5 inputs.
# Applied to the candidate's domain: a hERG ECFP4 random forest, plus a purpose-built
# correlated-feature probe for the conditional-vs-interventional claim.
import warnings
import numpy as np
import pandas as pd
import shap
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

print(f"shap {shap.__version__}  sklearn {sklearn.__version__}")
D = r"F:\OpenScience\audits\bio-qsar-modeling\run"
X = np.load(D + r"\X.npy").astype(np.float32)
yc = np.load(D + r"\y.npy")
y = (yc >= 6.0).astype(int)
keep = X.sum(0) >= 40
Xk = X[:, keep]
names = [f'bit_{i}' for i in np.where(keep)[0]]
print(f"[data] {Xk.shape} ECFP4 bits set in >=40 compounds; positives {y.sum()}")
Xtr, Xte, ytr, yte = train_test_split(Xk, y, test_size=0.25, random_state=0, stratify=y)
model = RandomForestClassifier(n_estimators=300, random_state=0, n_jobs=-1).fit(Xtr, ytr)
print(f"[model] RF test AUC = {roc_auc_score(yte, model.predict_proba(Xte)[:,1]):.3f}")

# ===== INPUT 1 (Canonical) =================================================
print("\n===== INPUT 1: TreeSHAP with the estimand set explicitly, then module aggregation =====")
bg = shap.utils.sample(Xtr, 200, random_state=0)
expl = shap.TreeExplainer(model, data=bg, feature_perturbation='interventional')
sv = expl(Xte[:300])
print(f"  explainer(X) returned {type(sv).__name__}; values shape {np.asarray(sv.values).shape}")
V = np.asarray(sv.values)
V2 = V[:, :, 1] if V.ndim == 3 else V
mean_abs = np.abs(V2).mean(axis=0)
order = np.argsort(mean_abs)[::-1]
print("  top 8 bits by mean |SHAP|:")
for i in order[:8]:
    print(f"    {names[i]:10} mean|SHAP|={mean_abs[i]:.5f}  set in "
          f"{int(Xk[:, i].sum())} compounds")
print(f"  bits receiving EXACTLY zero mean |SHAP| under interventional: "
      f"{int((mean_abs == 0).sum())}/{len(mean_abs)}")
# module aggregation, as the Skill prescribes: cluster correlated bits first
corr = np.corrcoef(Xk.T)
np.fill_diagonal(corr, 0)
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform
dist = 1 - np.abs(np.nan_to_num(corr))
np.fill_diagonal(dist, 0)
Z = linkage(squareform(dist, checks=False), method='average')
clusters = fcluster(Z, t=0.7, criterion='distance')
print(f"  {len(set(clusters))} bit modules from {Xk.shape[1]} bits at |r| >= 0.3")
mod = {}
for c, m in zip(clusters, mean_abs):
    mod[c] = mod.get(c, 0) + m
top_mod = sorted(mod.items(), key=lambda kv: -kv[1])[:5]
print("  top 5 modules by summed mean |SHAP|:")
for c, v in top_mod:
    members = [names[i] for i in range(len(names)) if clusters[i] == c]
    print(f"    module {c:4} size={len(members):3} summed={v:.5f}  members={members[:4]}")
raw_top = [names[i] for i in order[:5]]
mod_top = [names[i] for i in range(len(names)) if clusters[i] == top_mod[0][0]][:5]
print(f"  ranking BEFORE aggregation: {raw_top}")
print(f"  top module AFTER aggregation: {mod_top}")

# ===== INPUT 2 (Variant A): conditional vs interventional ==================
print("\n===== INPUT 2: does an UNUSED but correlated feature get nonzero credit? =====")
rs = np.random.RandomState(7)
n = 2000
A = rs.normal(size=n)
B = A + rs.normal(scale=0.03, size=n)       # correlated with A, r ~ 0.999
C = rs.normal(size=n)                       # irrelevant
target = 2.0 * A + 0.2 * rs.normal(size=n)
Xp = np.column_stack([A, B, C])
print(f"  corr(A,B)={np.corrcoef(A,B)[0,1]:.4f}  corr(A,C)={np.corrcoef(A,C)[0,1]:.4f}")
tree = DecisionTreeRegressor(max_depth=3, random_state=0).fit(Xp[:, [0, 1, 2]], target)
used = sorted(set(tree.tree_.feature[tree.tree_.feature >= 0]))
print(f"  the fitted tree splits ONLY on feature index/indices {used} "
      f"(0=A, 1=B, 2=C)")
for mode, kwargs in [('tree_path_dependent', {}),
                     ('interventional', {'data': Xp[:500]})]:
    e = shap.TreeExplainer(tree, feature_perturbation=mode, **kwargs)
    v = np.abs(e.shap_values(Xp[:500])).mean(axis=0)
    print(f"  {mode:22} mean|SHAP| A={v[0]:.4f} B={v[1]:.4f} C={v[2]:.4f}")
    unused = [i for i in [0, 1, 2] if i not in used]
    print(f"    unused features {unused}: "
          + ", ".join(f"{'ABC'[i]}={v[i]:.6f}" for i in unused)
          + ("   <- EXACTLY zero" if all(v[i] == 0 for i in unused) else
             "   <- NONZERO credit to a feature the model never splits on"))

# ===== INPUT 3 (Variant B): permutation importance dilution ===============
print("\n===== INPUT 3: permutation importance with correlated predictors =====")
rf = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1)
ybin = (target > np.median(target)).astype(int)
Xtr2, Xte2, ytr2, yte2 = train_test_split(Xp, ybin, test_size=0.3, random_state=0)
rf.fit(Xtr2, ytr2)
pi = permutation_importance(rf, Xte2, yte2, n_repeats=20, random_state=0,
                            scoring='roc_auc')
print(f"  with A AND B present:  A={pi.importances_mean[0]:+.4f} "
      f"B={pi.importances_mean[1]:+.4f} C={pi.importances_mean[2]:+.4f}")
rf2 = RandomForestClassifier(n_estimators=200, random_state=0,
                             n_jobs=-1).fit(Xtr2[:, [0, 2]], ytr2)
pi2 = permutation_importance(rf2, Xte2[:, [0, 2]], yte2, n_repeats=20, random_state=0,
                             scoring='roc_auc')
print(f"  with B REMOVED:        A={pi2.importances_mean[0]:+.4f} "
      f"C={pi2.importances_mean[1]:+.4f}")
print(f"  -> A's importance changes by {pi2.importances_mean[0]-pi.importances_mean[0]:+.4f} "
      f"purely because a correlated copy was dropped")
print(f"  does sklearn's permutation_importance have a conditional= flag? "
      f"{'conditional' in permutation_importance.__doc__}")

# ===== INPUT 4 (Edge): background choice and the 'auto' default ===========
print("\n===== INPUT 4: background choice, and the feature_perturbation='auto' flip =====")
import inspect
sig = inspect.signature(shap.TreeExplainer.__init__)
default_fp = sig.parameters['feature_perturbation'].default
print(f"  shap {shap.__version__}: TreeExplainer default feature_perturbation = "
      f"{default_fp!r}  (SKILL.md: \"'auto' became the default in 0.47\")")
neg = Xtr[ytr == 0]
pos = Xtr[ytr == 1]
tops = {}
for lbl, bgd in [('mixed background', shap.utils.sample(Xtr, 200, random_state=0)),
                 ('inactive-only background', shap.utils.sample(neg, 200, random_state=0)),
                 ('active-only background', shap.utils.sample(pos, 200, random_state=0))]:
    e = shap.TreeExplainer(model, data=bgd, feature_perturbation='interventional')
    v = np.asarray(e.shap_values(Xte[:150]))
    v = v[:, :, 1] if v.ndim == 3 else v
    ma = np.abs(v).mean(axis=0)
    o = np.argsort(ma)[::-1][:10]
    tops[lbl] = [names[i] for i in o]
    print(f"  {lbl:26} base_value={np.mean(e.expected_value):+.4f} "
          f"top5={[names[i] for i in o[:5]]}")
keys = list(tops)
for i in range(len(keys)):
    for j in range(i + 1, len(keys)):
        ov = len(set(tops[keys[i]]) & set(tops[keys[j]]))
        print(f"    top-10 overlap, {keys[i]} vs {keys[j]}: {ov}/10")
print("  check_additivity behaviour:")
try:
    e = shap.TreeExplainer(model, data=bg, feature_perturbation='interventional')
    _ = e.shap_values(Xte[:50], check_additivity=True)
    print("    check_additivity=True passed on a correctly configured explainer")
except Exception as ex:                                      # noqa: BLE001
    print(f"    check_additivity=True raised {type(ex).__name__}: {str(ex)[:90]}")

# ===== INPUT 5 (Stress/Adversarial): LIME instability =====================
print("\n===== INPUT 5: is LIME reproducible enough for a global ranking? =====")
from lime.lime_tabular import LimeTabularExplainer
inst = Xte[0]
runs = []
for seed in range(5):
    le = LimeTabularExplainer(Xtr, feature_names=names, mode='classification',
                              discretize_continuous=True, random_state=seed)
    ex = le.explain_instance(inst, model.predict_proba, num_features=10,
                             num_samples=5000)
    runs.append([f for f, _ in ex.as_list()])
print("  top-10 feature sets across 5 seeds (same instance, same model):")
for s, r in enumerate(runs):
    print(f"    seed {s}: {[x.split(' ')[0][:14] for x in r][:5]}")
inter = set(runs[0])
for r in runs[1:]:
    inter &= set(r)
print(f"  features appearing in ALL 5 seeds' top-10: {len(inter)}/10")
pairs = [len(set(runs[i]) & set(runs[j])) for i in range(5) for j in range(i + 1, 5)]
print(f"  mean pairwise top-10 overlap across seeds: {np.mean(pairs):.1f}/10")
le0 = LimeTabularExplainer(Xtr, feature_names=names, mode='classification',
                           discretize_continuous=True, random_state=0)
a = [f for f, _ in le0.explain_instance(inst, model.predict_proba, num_features=10,
                                        num_samples=5000).as_list()]
b = [f for f, _ in le0.explain_instance(inst, model.predict_proba, num_features=10,
                                        num_samples=5000).as_list()]
print(f"  same pinned seed, two calls on the same explainer: identical? {a == b} "
      f"(overlap {len(set(a)&set(b))}/10)")
print("  -> SKILL.md: 'pin the seed; still only conditional stability'")
