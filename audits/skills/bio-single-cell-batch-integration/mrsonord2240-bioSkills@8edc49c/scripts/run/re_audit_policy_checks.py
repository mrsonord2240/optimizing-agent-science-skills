"""Focused assertions for the four prose-level regressions fixed in commit 8edc49c."""
from pathlib import Path

skill = Path(r"F:/OpenScience/worktrees/bio-single-cell-batch-integration-fixpass/single-cell/batch-integration/SKILL.md").read_text(encoding="utf-8")
assert "cross-tabulate condition x batch" in skill
assert "stop if any condition occurs in only one batch" in skill
assert "sort cells by batch key before calling `scanorama_integrate`" in skill
assert "roughly 0.5-5" in skill and "`theta = 0` does not disable correction" in skill
assert "SeuratWrappers" in skill and "reticulate/scvi-tools" in skill
print("PASS metadata-stop, Scanorama ordering, theta scale, and SeuratWrappers boundary")
