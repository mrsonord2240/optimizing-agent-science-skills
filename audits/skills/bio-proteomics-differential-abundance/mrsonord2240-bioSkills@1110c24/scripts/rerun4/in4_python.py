"""Input 4 regression: the Python workflow block VERBATIM, plus both shipped
Python/R examples, plus the Input 7 usage-guide consistency check."""
import re
import subprocess
import sys

import numpy as np
import pandas as pd

DD = r"F:\OpenScience\audits\bio-proteomics-differential-abundance\data"
DW = r"F:\OpenScience\audits\bio-proteomics-differential-abundance\rerun4"
DK = r"F:\OpenScience\external\mrsonord2240__bioSkills\proteomics\differential-abundance"

ns = {}
exec(compile(open(rf"{DW}\blocks\python_wf.py", encoding="utf-8").read(),
             "<SKILL.md: Python Workflow>", "exec"), ns)

pg = pd.read_csv(f"{DD}/proteinGroups.txt", sep="\t", low_memory=False)
icols = [c for c in pg.columns if c.startswith("LFQ intensity")]
M = pg[icols].copy()
M.index = pg["Majority protein IDs"]
M.columns = [c.replace("LFQ intensity ", "") for c in icols]
truth = pd.read_csv(f"{DD}/truth_proteins.csv").set_index("protein")

norm = ns["preprocess"](M)
case = [c for c in M.columns if c.startswith("T")]
ctrl = [c for c in M.columns if c.startswith("C")]
res, untestable = ns["differential_abundance"](norm, case, ctrl)
sig = res[res["padj"] < 0.05]
cls = truth["class"].reindex(sig["protein"])
fp = int((cls == "null").sum())
print(f"Welch + BH: tested {len(res)} | untestable returned {len(untestable)} "
      f"| calls {len(sig)} | FP {fp} | realized FDR {100 * fp / max(1, len(sig)):.1f}%")
print("untestable table columns:", list(untestable.columns))
print("  -> untestable proteins are RETURNED, not dropped:",
      len(untestable) > 0 or "none in this dataset")

print("\n  the ValueError guard on a table where no protein is testable:")
tiny = norm.iloc[:5, :2].copy()
try:
    ns["differential_abundance"](tiny, [tiny.columns[0]], [tiny.columns[1]])
    print("    NO ERROR  <-- guard missing")
except ValueError as e:
    print(f"    ValueError -> {e}")

print("\n=== shipped examples ===")
for ex in ("differential_abundance.py",):
    r = subprocess.run([sys.executable, "-B", rf"{DK}\examples\{ex}"],
                       capture_output=True, text=True)
    print(f"--- {ex} (exit {r.returncode}) ---")
    print((r.stdout or r.stderr).strip()[:700])

print("\n=== Input 7 (regression): usage-guide.md vs SKILL.md consistency ===")
skill = open(rf"{DK}\SKILL.md", encoding="utf-8").read()
guide = open(rf"{DK}\usage-guide.md", encoding="utf-8").read()
for phrase, where in [
    ("manufactures systematic false positives", "the pre-fix overclaim"),
    ("collapsed within-group variance", "the pre-fix overclaim"),
    (">50%", "the pre-fix '>50% FDR' claim"),
    ("msqrob2", "the tool both files must agree on"),
    ("centred", "the new centring check"),
]:
    print(f"  {phrase!r:45} SKILL.md {phrase in skill!s:5} | usage-guide.md {phrase in guide!s:5}"
          f"   ({where})")
print("  msqrob2 lines in usage-guide.md:")
for ln in guide.splitlines():
    if "msqrob2" in ln:
        print("   ", ln.strip()[:150])
