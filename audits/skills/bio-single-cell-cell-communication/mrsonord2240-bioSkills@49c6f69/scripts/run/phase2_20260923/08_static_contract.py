"""Phase 2 static completeness checks for the exact shipped tip; no source files are modified."""
from pathlib import Path
import ast

SKILL = Path(r"F:\OpenScience\wt\single-cell-cell-communication\single-cell\cell-communication")
required = [
    SKILL / "SKILL.md", SKILL / "usage-guide.md", SKILL / "scripts" / "cellphonedb_statistical.py",
    SKILL / "scripts" / "condition_stability.py", SKILL / "references" / "cellphonedb.md",
    SKILL / "references" / "cellchat.md", SKILL / "references" / "nichenet.md",
    SKILL / "examples" / "liana_analysis.py", SKILL / "examples" / "cellchat_analysis.R",
]
for path in required:
    assert path.is_file(), path
    print("PRESENT", path.relative_to(SKILL))
for path in (SKILL / "scripts").glob("*.py"):
    ast.parse(path.read_text(encoding="utf-8"))
    print("PY_PARSE_OK", path.name)
ast.parse((SKILL / "examples" / "liana_analysis.py").read_text(encoding="utf-8"))
print("PY_PARSE_OK examples/liana_analysis.py")
