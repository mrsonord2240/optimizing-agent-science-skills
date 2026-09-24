"""Exact-commit a6550a1 documentation assertions for all audited corrections."""
from pathlib import Path

skill = Path(r"F:\OpenScience\worktrees\bio-single-cell-preprocessing-fixpass\single-cell\preprocessing\SKILL.md").read_text(encoding="utf-8")
checks = {
    "SoupX creates clusters before autoEstCont": "sc <- setClusters(sc, setNames(as.character(Seurat::Idents(so)), colnames(so)))" in skill,
    "SoupX failure is actionable": "Clustering information must be supplied, run setClusters first" in skill,
    "mitochondrial caps are tissue-aware": "mito_hard_caps = {'nuclei': 1, 'pbmc': 8, 'cardiac': 30, 'hepatic': 30, 'skeletal_muscle': 40, 'unknown': None}" in skill,
    "unknown tissue has no copied hard cap": "'unknown': None" in skill,
    "MAD collapse is a hard fallback": "if mad == 0:" in skill and "survival_fraction < 0.80" in skill,
    "top20 warning protects simple populations": "platelets/megakaryocytes, erythrocytes" in skill and "removal rates per preliminary cluster" in skill,
    "batch HVG helper filters per batch": "def filter_genes_per_batch" in skill and "reciprocal condition number" in skill,
    "renormalization symptom follows Scanpy": "Values shrink and distributions compress" in skill and "already log-transformed" in skill,
}
for label, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'}: {label}")
assert all(checks.values())
print(f"PASS: {len(checks)}/{len(checks)} exact-commit documentation assertions")
