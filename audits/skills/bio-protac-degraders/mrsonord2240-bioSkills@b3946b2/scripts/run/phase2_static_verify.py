"""Static-contract checks for the final-pass source copy."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "phase2_skill_copy"
SKILL = ROOT / "SKILL.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    text = SKILL.read_text(encoding="utf-8")
    lines = text.splitlines()
    require(lines[0] == "---" and "name: bio-protac-degraders" in text and "description:" in text,
            "frontmatter contract incomplete")
    require(len(lines) <= 300, f"SKILL.md over final-pass compactness limit: {len(lines)}")
    expected = [
        ROOT / "usage-guide.md",
        ROOT / "references" / "ternary-prediction-tools.md",
        ROOT / "examples" / "protac_enumerate.py",
        ROOT / "examples" / "ternary_geometry_screen.py",
        ROOT / "examples" / "cooperativity_dc50.py",
    ]
    require(all(path.is_file() for path in expected), "documented primary file missing")
    require("does not predict a structure or an interface score" in text,
            "local versus external ternary scope unclear")
    require("report Dmax as\na lower bound" in text and "plateau_reached" in text,
            "narrow-hook limitation/caveat absent")
    scripts = sorted((ROOT / "examples").glob("*.py"))
    for script in scripts:
        source = script.read_text(encoding="utf-8")
        ast.parse(source, filename=str(script))
        require("eval(" not in source and "exec(" not in source,
                f"unsafe dynamic-code call in {script.name}")
    print(f"STATIC PASS: lines={len(lines)} files={len(expected)} scripts_compiled={len(scripts)}")


if __name__ == "__main__":
    main()
