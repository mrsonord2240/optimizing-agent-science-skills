"""Fixer evidence: verify Skill structure, paths, and removal of audited stale claims."""

from pathlib import Path
import re

root = Path(r"F:\OpenScience\wt\backlog-statistical-annotation\skills\bio-data-visualization-statistical-annotation")
skill = (root / "SKILL.md").read_text(encoding="utf-8")
guide = (root / "usage-guide.md").read_text(encoding="utf-8")

assert re.search(r"^name: bio-data-visualization-statistical-annotation$", skill, re.M)
assert len(skill.splitlines()) <= 300
assert skill.count("```") % 2 == 0
assert guide.count("```") == 0
for relative in (
    "scripts/annotate_pairwise.R", "scripts/annotate_paired.R", "scripts/annotate_nested.R",
    "scripts/annotate_pairwise.py", "scripts/annotate_paired.py",
    "examples/data/three_group.csv", "examples/data/paired.csv", "examples/data/nested.csv",
):
    assert (root / relative).is_file(), relative
for stale in ("default is t-test", "Default ggpubr test is t-test", "Cliff d ranges", "<2.22e-16"):
    assert stale not in skill and stale not in guide, stale
print("STRUCTURE PASS", len(skill.splitlines()), "SKILL.md lines; all referenced runnable paths exist")
