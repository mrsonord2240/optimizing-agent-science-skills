"""Static/source integrity checks for the exact audited worktree tip."""
import ast
from pathlib import Path

root = Path(r"F:\OpenScience\wt\single-cell-trajectory-inference\single-cell\trajectory-inference")
for rel in ("SKILL.md", "usage-guide.md", "examples/scvelo_velocity.py", "examples/monocle3_trajectory.R", "scripts/cellrank_fate.py"):
    path = root / rel
    assert path.is_file(), f"Missing shipped file: {rel}"
ast.parse((root / "examples/scvelo_velocity.py").read_text(encoding="utf-8"))
ast.parse((root / "scripts/cellrank_fate.py").read_text(encoding="utf-8"))
skill = (root / "SKILL.md").read_text(encoding="utf-8")
assert "name: bio-single-cell-trajectory-inference" in skill
assert "primary_tool: PAGA" in skill
assert "Monocle3 and SeuratWrappers are GitHub-only R packages with no Windows binary" in skill
print("required_files=5/5; python_syntax=2/2; frontmatter_and_windows_caveat=True")
