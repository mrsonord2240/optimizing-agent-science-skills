"""Static regression checks against exact source commit c3ca7ea."""

from pathlib import Path
import subprocess


ROOT = Path(
    "F:/OpenScience/worktrees/bio-single-cell-preprocessing-fixpass/"
    "single-cell/preprocessing"
)
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
scanpy = (ROOT / "examples/preprocess_scanpy.py").read_text(encoding="utf-8")
seurat = (ROOT / "examples/preprocess_seurat.R").read_text(encoding="utf-8")
guide = (ROOT / "usage-guide.md").read_text(encoding="utf-8")
head = subprocess.check_output(
    ["git", "rev-parse", "HEAD"], cwd=ROOT.parents[1], text=True
).strip()

checks = {
    "source commit is 9918c63": head == "9918c631d94f81dd418cf71d5c40be59f4850677",
    "Scanpy example has MAD-collapse guard": "MAD collapsed" in scanpy,
    "Scanpy example has survival guard": "survival_fraction < 0.80" in scanpy,
    "Scanpy example has no flat 8 percent filter": "pct_counts_mt'] > 8" not in scanpy,
    "Seurat example has MAD-collapse guard": "MAD collapsed" in seurat,
    "Seurat example has survival guard": "survival_fraction < 0.80" in seurat,
    "Seurat example has no flat 20 percent filter": "percent.mt < 20" not in seurat,
    "nuclei use MAD-only policy": "'nuclei': None" in skill,
    "authoritative Skill retains installation guidance": all(
        text in skill
        for text in (
            "pip install scanpy matplotlib scikit-misc",
            "pip install cellbender",
            "install.packages(c('Seurat', 'SoupX'))",
            "BiocManager::install(c('scran', 'celda'))",
        )
    ),
    "usage guide omits prerequisites": "## Prerequisites" not in guide,
    "usage guide omits duplicated workflow": "## What the Agent Will Do" not in guide,
}

for label, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {label}")
assert all(checks.values())
print(f"PASS: {len(checks)}/{len(checks)} exact-source assertions")
