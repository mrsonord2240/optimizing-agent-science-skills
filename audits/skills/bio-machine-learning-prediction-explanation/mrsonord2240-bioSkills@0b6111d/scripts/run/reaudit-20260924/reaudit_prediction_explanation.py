"""Exact-commit re-audit checks for bio-machine-learning-prediction-explanation.

Run from the existing cheminformatics shared audit environment.  This script keeps
the precision claims testable: it checks the TreeSHAP unused-feature boundary,
the mode-dependent split for features used by the tree, executable module-map
construction, and both bundled examples.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import shap
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor


ROOT = Path(os.environ["SKILL_ROOT"])
SKILL = ROOT / "machine-learning" / "prediction-explanation"
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")
GUIDE = (SKILL / "usage-guide.md").read_text(encoding="utf-8")


def mean_abs(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values)
    return np.abs(values[..., 1] if values.ndim == 3 else values).mean(axis=0)


print(f"source={ROOT}")
print(f"shap={shap.__version__}")

# Regression for the former false claim. A fitted tree that never splits on B or C
# gives those features exactly zero under both TreeSHAP modes.
rng = np.random.RandomState(7)
n = 2000
a = rng.normal(size=n)
b = a + rng.normal(scale=0.03, size=n)
c = rng.normal(size=n)
y = 2.0 * a + 0.2 * rng.normal(size=n)
x = np.column_stack([a, b, c])

depth1 = DecisionTreeRegressor(max_depth=1, random_state=0).fit(x, y)
used1 = set(depth1.tree_.feature[depth1.tree_.feature >= 0])
assert used1 == {0}, f"unexpected depth-1 splits: {used1}"
path1 = mean_abs(shap.TreeExplainer(depth1, feature_perturbation="tree_path_dependent").shap_values(x[:500]))
inter1 = mean_abs(
    shap.TreeExplainer(depth1, data=x[:500], feature_perturbation="interventional").shap_values(x[:500])
)
assert path1[1] == path1[2] == inter1[1] == inter1[2] == 0.0
print("unused-feature boundary: PASS (B,C exactly zero in both modes)")

# The useful, supported claim: for correlated features that the tree does use, the
# estimands can allocate credit differently.
depth2 = DecisionTreeRegressor(max_depth=2, random_state=0).fit(x, y)
used2 = set(depth2.tree_.feature[depth2.tree_.feature >= 0])
assert {0, 1}.issubset(used2), f"expected A and B in depth-2 tree, got {used2}"
path2 = mean_abs(shap.TreeExplainer(depth2, feature_perturbation="tree_path_dependent").shap_values(x[:500]))
inter2 = mean_abs(
    shap.TreeExplainer(depth2, data=x[:500], feature_perturbation="interventional").shap_values(x[:500])
)
assert abs(path2[1] - inter2[1]) > 0.01
assert path2[2] == inter2[2] == 0.0
print(f"used-correlated split: PASS (B path={path2[1]:.4f}, interventional={inter2[1]:.4f})")

# Execute the documented Spearman/average-linkage module-map construction.
frame = pd.DataFrame({"A": a[:160], "B": b[:160], "C": c[:160], "D": rng.normal(size=160)})
abs_rho = frame.corr(method="spearman").abs().fillna(0.0)
abs_rho_values = abs_rho.to_numpy(copy=True)
np.fill_diagonal(abs_rho_values, 1.0)
tree = linkage(squareform(1.0 - abs_rho_values, checks=False), method="average")
module_id = fcluster(tree, t=0.7, criterion="distance")
clusters = dict(zip(frame.columns, module_id))
assert set(clusters) == set(frame.columns)
assert clusters["A"] == clusters["B"]
print(f"module map: PASS ({len(set(module_id))} modules; A/B share module {clusters['A']})")

# Permutation remains a correlation-diluted global screen, not a workaround for
# the SHAP estimand choice.  This reproduces the documented held-out contrast.
y_binary = (y > np.median(y)).astype(int)
x_train, x_test, y_train, y_test = train_test_split(x, y_binary, test_size=0.3, random_state=0)
both_model = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1).fit(x_train, y_train)
both = permutation_importance(both_model, x_test, y_test, n_repeats=12, random_state=0, scoring="roc_auc")
only_a_model = RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1).fit(x_train[:, [0, 2]], y_train)
only_a = permutation_importance(only_a_model, x_test[:, [0, 2]], y_test, n_repeats=12, random_state=0, scoring="roc_auc")
assert only_a.importances_mean[0] > both.importances_mean[0]
print(
    "permutation correlation dilution: PASS "
    f"(A with B={both.importances_mean[0]:.4f}, without B={only_a.importances_mean[0]:.4f})"
)

# The corrected background guidance asks for this measurement rather than a
# universal claim that every top feature will move.
background_model = RandomForestClassifier(n_estimators=150, random_state=0).fit(x, y_binary)
low_bg, high_bg = x[a < np.median(a)][:100], x[a >= np.median(a)][:100]
low_values = mean_abs(
    shap.TreeExplainer(background_model, data=low_bg, feature_perturbation="interventional").shap_values(x[:250])
)
high_values = mean_abs(
    shap.TreeExplainer(background_model, data=high_bg, feature_perturbation="interventional").shap_values(x[:250])
)
low_top = set(np.argsort(low_values)[-3:])
high_top = set(np.argsort(high_values)[-3:])
overlap = len(low_top & high_top)
assert 0 <= overlap <= 3
print(f"background rank-overlap measurement: PASS (top-3 overlap={overlap}/3)")

# The corrected guidance asks users to measure, not presume, ranking movement.
assert "top-k rank overlap" in TEXT
assert TEXT.count("top-k rank overlap") >= 2
assert "a feature the model *never uses* can still receive nonzero" not in TEXT
assert "unused-but-correlated" not in TEXT
assert "Path-dependent SHAP can give a gene nonzero credit" not in GUIDE
print("claim text: PASS (removed false unused-feature and absolute-instability claims)")

for example, expected in [
    ("shap_omics_classifier.py", "The A-vs-B split differs by mode"),
    ("lime_explanation.py", "Mean pairwise top-5 overlap:"),
]:
    result = subprocess.run(
        [sys.executable, str(SKILL / "examples" / example)],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert expected in result.stdout, f"{example} did not print its claimed conclusion"
    print(f"example {example}: PASS")

print("REAUDIT PASS")
