"""Exact-commit 1730c87 assertions for every documented audit correction."""
from pathlib import Path

skill = Path(r"F:\OpenScience\worktrees\bio-qsar-modeling-fixpass\chemoinformatics\qsar-modeling\SKILL.md").read_text(encoding="utf-8")
example = Path(r"F:\OpenScience\worktrees\bio-qsar-modeling-fixpass\chemoinformatics\qsar-modeling\examples\chemprop_pipeline.sh").read_text(encoding="utf-8")

checks = {
    "predict repeats rdkit_2d featurizer": "--molecule-featurizers rdkit_2d" in skill.split("At prediction time", 1)[1].split("## Scaffold-Balanced Split", 1)[0],
    "prediction mismatch explains 517-versus-300 symptom": "517-versus-300 tensor-shape error" in skill,
    "chemprop seeds use current v2 flags": "--data-seed 42 --pytorch-seed 42" in skill and "--seed 42" not in skill,
    "pipeline uses both reproducibility flags": "--data-seed 42" in example and "--pytorch-seed 42" in example,
    "uncertainty output is documented as variance": "writes `pred_*_unc` as ensemble **variance**" in skill,
    "leverage excludes sparse ECFP use and has a sanity bound": "Do not apply directly to sparse ECFP bits" in skill and "h < 0` or `h > 1" in skill,
    "Mahalanobis requires reduced descriptor/PCA space": "Reduce/select descriptor space first" in skill,
    "conformal caveat connects split and exchangeability": "calibration and test examples non-exchangeable" in skill and "empirical coverage" in skill,
    "conformal estimator uses all cores": "RandomForestRegressor(n_estimators=500, random_state=42, n_jobs=-1)" in skill,
    "conformal cost is explicit": "fits the base estimator six times" in skill and "split-conformal" in skill,
    "missing-AD symptom covers explained variance": "explained variance or rank ordering can collapse" in skill,
    "missing-AD fix stratifies R2 or Spearman": "R2 or Spearman correlation" in skill,
}

for label, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {label}")
assert all(checks.values()), "one or more exact-commit documentation assertions failed"
print(f"PASS: {len(checks)}/{len(checks)} exact-commit documentation assertions")
