"""Syntax-check every copied Python executable without touching source worktree bytecode."""
from pathlib import Path
import py_compile

root = Path(r"F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis\run")
files = sorted(root.glob("*.py"))
for file in files:
    py_compile.compile(str(file), doraise=True)
print(f"python_compile_passed={len(files)}")
