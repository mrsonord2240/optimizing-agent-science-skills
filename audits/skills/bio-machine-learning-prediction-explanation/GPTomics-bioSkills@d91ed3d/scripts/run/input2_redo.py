# Input 2, corrected probe: force the model to use EXACTLY ONE of a correlated pair,
# so the Skill's central claim can actually be tested.
import numpy as np, shap
from sklearn.tree import DecisionTreeRegressor
rs = np.random.RandomState(7); n = 2000
A = rs.normal(size=n); B = A + rs.normal(scale=0.03, size=n); C = rs.normal(size=n)
target = 2.0*A + 0.2*rs.normal(size=n)
X = np.column_stack([A, B, C])
print(f"corr(A,B)={np.corrcoef(A,B)[0,1]:.4f}")
for depth in [1, 2]:
    tree = DecisionTreeRegressor(max_depth=depth, random_state=0).fit(X, target)
    used = sorted(int(f) for f in set(tree.tree_.feature[tree.tree_.feature >= 0]))
    unused = [i for i in (0,1,2) if i not in used]
    print(f"\nmax_depth={depth}: tree splits only on {[ 'ABC'[u] for u in used]}; "
          f"unused = {['ABC'[u] for u in unused]}")
    for mode, kw in [('tree_path_dependent', {}), ('interventional', {'data': X[:500]})]:
        e = shap.TreeExplainer(tree, feature_perturbation=mode, **kw)
        v = np.abs(e.shap_values(X[:500])).mean(axis=0)
        tag = ''
        if unused:
            nz = [u for u in unused if v[u] != 0]
            tag = ("   <- NONZERO credit to unused " + ",".join('ABC'[u] for u in nz)
                   if nz else "   <- EXACTLY zero for every unused feature")
        print(f"  {mode:22} A={v[0]:.4f} B={v[1]:.4f} C={v[2]:.4f}{tag}")
