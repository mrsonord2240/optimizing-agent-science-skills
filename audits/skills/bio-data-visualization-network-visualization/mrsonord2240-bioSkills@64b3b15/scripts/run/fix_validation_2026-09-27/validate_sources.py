"""Compile Python sources and assert the split/dedup source invariants."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "skills" / "bio-data-visualization-network-visualization"
for path in sorted(ROOT.rglob("*.py")):
    compile(path.read_text(encoding="utf-8"), str(path), "exec")
    print("COMPILE", path.relative_to(ROOT))

for path in sorted([ROOT / "SKILL.md", ROOT / "usage-guide.md", *ROOT.joinpath("references").glob("*.md")]):
    text = path.read_text(encoding="utf-8")
    assert text.count("```") % 2 == 0, f"unbalanced fence: {path}"
    print("FENCES", path.relative_to(ROOT), text.count("```"))

skill_lines = (ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()
assert len(skill_lines) <= 300
assert "HiveNetX" not in "\n".join(skill_lines)
assert "datashader" not in "\n".join(skill_lines).lower()
print("SKILL_LINES", len(skill_lines))
