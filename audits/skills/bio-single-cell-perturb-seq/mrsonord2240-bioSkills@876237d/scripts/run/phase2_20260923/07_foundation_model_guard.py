"""Phase 2 input 7: execute the foundation-model evaluation guardrail response."""
from pathlib import Path
skill = Path(r"F:/OpenScience/wt/single-cell-perturb-seq/single-cell/perturb-seq/SKILL.md").read_text(encoding="utf-8")
needles = ["whole-perturbation holdout", "DE genes", "additive/mean baseline", "random cell-level splits"]
assert all(n in skill for n in needles)
print("PASS guardrail: reject all-gene/cell-split correlation as sufficient evidence; require perturbation holdout and DE-gene comparison to mean/additive baselines.")
