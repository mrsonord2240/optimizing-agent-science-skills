"""Audit source structure and test the shipped files from the isolated copy."""
from pathlib import Path
import ast
import re

ROOT = Path(__file__).resolve().parent / "skill_copy"
skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
guide = (ROOT / "usage-guide.md").read_text(encoding="utf-8")
classifier = ROOT / "examples" / "warhead_classifier.py"
alpha = ROOT / "scripts" / "acrylamide_alpha_substitution.py"

assert skill.startswith("---\n")
frontmatter = skill.split("---", 2)[1]
for field in ("name: bio-covalent-design", "description:", "tool_type: python", "primary_tool: RDKit"):
    assert field in frontmatter, field
assert "## Scope" in skill
assert "individual patient's diagnostic or treatment decision" in skill
assert "python scripts/acrylamide_alpha_substitution.py" in skill
assert "Versions and installs: see SKILL.md's Version Compatibility." in guide
assert "## Tips" in guide and guide.count("SKILL.md's") >= 1
for path in (classifier, alpha):
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    print(f"parse_ok={path.relative_to(ROOT)}")

assert "eval(" not in classifier.read_text(encoding="utf-8")
assert "exec(" not in classifier.read_text(encoding="utf-8")
assert "eval(" not in alpha.read_text(encoding="utf-8")
assert "exec(" not in alpha.read_text(encoding="utf-8")
assert re.search(r"prepare_receptor4\.py.*prepare_flexreceptor4\.py.*prepare_gpf4\.py.*prepare_dpf4\.py", skill, re.S)
print("frontmatter_scope_references_and_no_raw_execution=PASS")
