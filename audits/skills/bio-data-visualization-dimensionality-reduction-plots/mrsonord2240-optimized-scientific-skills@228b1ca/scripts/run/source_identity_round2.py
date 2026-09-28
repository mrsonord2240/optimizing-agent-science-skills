"""Record immutable round-2 source identity and byte hashes."""
from __future__ import annotations

from pathlib import Path
import hashlib
import subprocess

WORKTREE = Path(r"F:\OpenScience\wt\backlog-dimensionality-reduction-plots")
SKILL = WORKTREE / "skills" / "bio-data-visualization-dimensionality-reduction-plots"

def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(WORKTREE), *args], text=True, encoding="utf-8").strip()

head = git("rev-parse", "HEAD")
status = git("status", "--short")
print(f"HEAD={head}")
print(f"worktree_status={status!r}")
for path in sorted(SKILL.rglob("*")):
    if path.is_file():
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"sha256 {path.relative_to(WORKTREE).as_posix()} {digest}")
pycache = list(SKILL.rglob("__pycache__"))
print(f"ignored_source_pycache_count={len(pycache)}")
assert head == "228b1caf42f42053a16db2dfe0f67fcb2005a413"
assert status == ""
assert not pycache
