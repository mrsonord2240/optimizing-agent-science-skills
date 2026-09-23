"""Phase 2 input 6: execute the documented high-MOI boundary response."""
from pathlib import Path
skill = Path(r"F:/OpenScience/wt/single-cell-perturb-seq/single-cell/perturb-seq/SKILL.md").read_text(encoding="utf-8")
needles = ["no bundled worked example", "scmageck_lr()", "scmageck_rra()", "NEGCTRL"]
assert all(n in skill for n in needles)
print("PASS boundary response: route high-MOI users to verified upstream scMAGeCK entry points; do not fabricate a local executable.")
