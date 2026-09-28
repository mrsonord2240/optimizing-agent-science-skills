"""Round-2 static and focused-test checks against the immutable provider source."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(r"F:\OpenScience\wt\backlog-dimensionality-reduction-plots\skills\bio-data-visualization-dimensionality-reduction-plots")
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
usage = (ROOT / "usage-guide.md").read_text(encoding="utf-8")
example = (ROOT / "examples" / "embedding_phd.py").read_text(encoding="utf-8")
tests = (ROOT / "tests" / "test_embedding_phd.py").read_text(encoding="utf-8")

links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", skill + "\n" + usage)
local_links = [link for link in links if not re.match(r"^[a-z]+://", link)]
missing = [link for link in local_links if not (ROOT / link.split("#", 1)[0]).is_file()]
print(f"SKILL lines={len(skill.splitlines())}; usage lines={len(usage.splitlines())}")
print(f"local links={local_links}")
print(f"missing links={missing}")
print(f"five output filenames present={all(name in example for name in ['pca.pdf','scree.pdf','umap_clusters.pdf','tsne.pdf','phate.pdf'])}")
print(f"documentation says five saved figures={'five saved figures' in skill}")
print(f"tab20 1-20 rule present={'up to 20 categories' in (ROOT / 'references' / 'method-recipes.md').read_text(encoding='utf-8')}")
print(f"collision regression present={'test_loading_labels_do_not_overlap' in tests}")
assert not missing
assert "five saved figures" in skill
assert "categorical_colors(len(categories))" in example
assert "categorical_colors(len(leiden.cat.categories))" in example
assert "annotate_loading_labels" in example
assert "with self.assertRaisesRegex(ValueError, \"facet\")" in tests
assert "test_loading_labels_do_not_overlap" in tests
