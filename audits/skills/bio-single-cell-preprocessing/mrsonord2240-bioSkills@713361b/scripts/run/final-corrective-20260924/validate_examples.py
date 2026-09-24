"""Regression checks for packaged preprocessing examples and chooser text."""

from pathlib import Path


skill_root = Path(
    "F:/OpenScience/worktrees/bio-single-cell-preprocessing-fixpass/"
    "single-cell/preprocessing"
)
scanpy = (skill_root / "examples/preprocess_scanpy.py").read_text(encoding="utf-8")
seurat = (skill_root / "examples/preprocess_seurat.R").read_text(encoding="utf-8")
skill = (skill_root / "SKILL.md").read_text(encoding="utf-8")
guide = (skill_root / "usage-guide.md").read_text(encoding="utf-8")

assert "mito_hard_caps" in scanpy
assert "MAD collapsed" in scanpy
assert "survival_fraction" in scanpy
assert "pct_counts_mt'] > 8" not in scanpy

assert "mito_hard_caps" in seurat
assert "MAD collapsed" in seurat
assert "survival_fraction" in seurat
assert "percent.mt < 20" not in seurat

assert "'nuclei': None" in skill
assert "## Prerequisites" not in guide
assert "## What the Agent Will Do" not in guide

print("packaged-example and usage-guide regression checks: PASS")
