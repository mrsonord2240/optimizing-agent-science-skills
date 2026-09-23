"""Structural and code-usability checks for the exact final-pass source tree."""
from __future__ import annotations

import ast
import json
from pathlib import Path


REPO = Path(r"F:\OpenScience\wt\crispr-screens-drugz-chemogenomic")
SKILL = REPO / "crispr-screens" / "drugz-chemogenomic"


def main() -> None:
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    related = []
    capture = False
    for line in text.splitlines():
        if line == "## Related Skills":
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture and line.startswith("- "):
            rel = line[2:].split(" - ", 1)[0].strip()
            related.append({"path": rel, "exists": (REPO / rel / "SKILL.md").is_file()})
    py_files = [SKILL / "scripts" / "dose_consistent_hits.py", SKILL / "examples" / "run_drugz.py"]
    for file in py_files:
        ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
    result = {
        "skill_line_count": len(text.splitlines()),
        "required_files_exist": all((SKILL / item).is_file() for item in ("SKILL.md", "usage-guide.md", "references/reference-gene-removal.md", "references/failure-modes.md", "scripts/dose_consistent_hits.py", "examples/run_drugz.py")),
        "related_skills": related,
        "related_skills_all_exist": all(item["exists"] for item in related),
        "parsed_python": [str(file.relative_to(SKILL)) for file in py_files],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
