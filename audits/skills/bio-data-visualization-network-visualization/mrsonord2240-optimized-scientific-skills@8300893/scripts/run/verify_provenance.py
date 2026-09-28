"""Verify immutable source commit, byte-identical execution copy, and final evidence size."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKTREE = Path(r"F:\OpenScience\wt\backlog-network-visualization")
SOURCE = WORKTREE / "skills/bio-data-visualization-network-visualization"
COPY = ROOT / "run/skill"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


source_files = sorted(p.relative_to(SOURCE) for p in SOURCE.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
copy_files = sorted(p.relative_to(COPY) for p in COPY.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
assert source_files == copy_files
mismatches = [str(rel) for rel in source_files if digest(SOURCE / rel) != digest(COPY / rel)]
assert not mismatches
head = subprocess.check_output(["git", "-C", str(WORKTREE), "rev-parse", "HEAD"], text=True).strip()
status = subprocess.check_output(
    ["git", "-C", str(WORKTREE), "status", "--short", "--untracked-files=all"],
    text=True,
).strip()
skill_status = subprocess.check_output(
    [
        "git",
        "-C",
        str(WORKTREE),
        "status",
        "--short",
        "--untracked-files=all",
        "--",
        "skills/bio-data-visualization-network-visualization",
    ],
    text=True,
).strip()
assert head == "83008933c5298af81fe4b4604a39b291817bb47f"
assert skill_status == ""
assert not list(SOURCE.rglob("__pycache__"))
assert not list((ROOT / "run").rglob("__pycache__"))
all_files = [p for p in ROOT.rglob("*") if p.is_file()]
results = {
    "commit": head,
    "repository_status": status,
    "skill_status": skill_status,
    "source_files": len(source_files),
    "copy_mismatches": mismatches,
    "source_pycache_count": 0,
    "run_pycache_count": 0,
    "audit_file_count": len(all_files),
    "audit_bytes": sum(p.stat().st_size for p in all_files),
}
(ROOT / "logs/provenance.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
