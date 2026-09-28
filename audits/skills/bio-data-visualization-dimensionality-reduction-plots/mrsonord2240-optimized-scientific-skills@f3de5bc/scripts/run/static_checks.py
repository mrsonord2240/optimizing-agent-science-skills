"""Static integrity checks against the immutable provider source without importing it."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(r"F:\OpenScience\wt\backlog-dimensionality-reduction-plots\skills\bio-data-visualization-dimensionality-reduction-plots")
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
usage = (ROOT / "usage-guide.md").read_text(encoding="utf-8")
example = (ROOT / "examples" / "embedding_phd.py").read_text(encoding="utf-8")

links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", skill + "\n" + usage)
local_links = [link for link in links if not re.match(r"^[a-z]+://", link)]
missing = [link for link in local_links if not (ROOT / link.split("#", 1)[0]).is_file()]
print(f"SKILL lines={len(skill.splitlines())}; usage lines={len(usage.splitlines())}")
print(f"local links={local_links}")
print(f"missing links={missing}")
print(f"five output filenames present={all(name in example for name in ['pca.pdf','scree.pdf','umap_clusters.pdf','tsne.pdf','phate.pdf'])}")
print(f"documentation says four saved figures={'four saved figures' in skill}")
assert not missing
assert "svd_solver=\"full\"" in (ROOT / "references" / "method-recipes.md").read_text(encoding="utf-8")
assert "set.seed(42)" in skill
assert "flavor=\"igraph\"" in example
assert example.index("highly_variable_genes") < example.index("normalize_total")
