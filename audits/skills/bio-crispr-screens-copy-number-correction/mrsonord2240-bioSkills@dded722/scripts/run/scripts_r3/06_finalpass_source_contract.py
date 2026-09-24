"""Final-pass source-contract checks for bio-crispr-screens-copy-number-correction.

Inputs 8 and 9 are fresh edge cases added after the archived round-3 audit:
8. The exact committed Skill's Chronos reproducibility prescription is executable and accurately
   limited to comparable CPU reruns, not promised as cross-platform bitwise determinism.
9. The exact committed Skill documents the empty negative-control list and no longer claims that
   a pooled panel necessarily masks a per-line residual.
"""
from pathlib import Path
import re
import subprocess

import numpy as np
import pandas as pd

WORKTREE = Path(r"F:\OpenScience\worktrees\bio-crispr-screens-copy-number-correction-final")
SKILL = WORKTREE / "crispr-screens" / "copy-number-correction" / "SKILL.md"
EXPECTED = "dded722b0c3490d36f4fec2fe633eb113a05317c"

actual = subprocess.check_output(
    ["git", "-C", str(WORKTREE), "rev-parse", "HEAD"], text=True
).strip()
assert actual == EXPECTED, (actual, EXPECTED)
text = SKILL.read_text(encoding="utf-8")

print("=== Input 8 (fresh edge): reproducibility prescription ===")
assert "np.random.seed(20260924)" in text
assert "*before* constructing the model" in text
assert "do not promise bitwise-identical estimates" in text
np.random.seed(20260924)
first = np.random.normal(size=6)
np.random.seed(20260924)
second = np.random.normal(size=6)
assert np.array_equal(first, second)
print("Seeded NumPy initialization is reproducible; documentation records the correct platform limit.")

print("=== Input 9 (fresh edge): error and reconciliation contracts ===")
assert "ValueError: set of negative_control_sgrnas is empty" in text
assert "do not use an empty placeholder list" in text
assert "do not assume either view will always conceal the other" in text
assert "per cell line, not only pooled" not in text

# Execute the diagnostic function literally extracted from the exact committed source.
block = re.search(r"from scipy\.stats import spearmanr, mannwhitneyu\n(.*?)\n```", text, re.S)
assert block, "detect_cn_bias code block not found"
namespace = {"pd": pd}
exec("from scipy.stats import spearmanr, mannwhitneyu\n" + block.group(1), namespace)
detect_cn_bias = namespace["detect_cn_bias"]

genes = [f"AMP{i}" for i in range(8)] + [f"DIP{i}" for i in range(12)]
lfc = [-1.2] * 8 + [-0.1] * 12
cn = [8.0] * 8 + [2.0] * 12
result = detect_cn_bias(
    pd.DataFrame({"gene": genes, "lfc": lfc}),
    pd.DataFrame({"gene": genes, "copy_number": cn}),
)
assert result["n_amplified_genes"] == 8
assert result["low_power_floor"] is False
assert result["bias_present"] is True
print("Exact diagnostic code executes at the n=8 boundary and reports a focal bias.")
print("Exact source contract: PASS", actual)
