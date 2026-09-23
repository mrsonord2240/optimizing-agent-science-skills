"""Syntax-check every copied executable artifact from the audited commit."""
import py_compile
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\skill_copy")
files = [ROOT / "examples" / "run_jacks.py", ROOT / "scripts" / "run_jacks_joint.py", ROOT / "scripts" / "efficacy_summary.py"]
for path in files:
    py_compile.compile(str(path), doraise=True)
    print(f"PASS: compiled {path.name}")
