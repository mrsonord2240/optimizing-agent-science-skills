"""Fresh regression for the documented explicit Python FDR methods.

Usage: python audit_statsmodels.py <output-dir>
"""
from pathlib import Path
import sys
import numpy as np
from statsmodels.stats.multitest import multipletests

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
pvalues = np.array([0.0001, 0.001, 0.004, 0.02, 0.2, 0.7])
bh_rej, bh_padj, _, _ = multipletests(pvalues, alpha=0.05, method="fdr_bh")
by_rej, by_padj, _, _ = multipletests(pvalues, alpha=0.05, method="fdr_by")
assert bh_padj.shape == pvalues.shape and by_padj.shape == pvalues.shape
assert np.all((0 <= bh_padj) & (bh_padj <= 1))
assert np.all((0 <= by_padj) & (by_padj <= 1))
assert by_rej.sum() <= bh_rej.sum()
(out / "input1_python_equivalent.txt").write_text(
    f"bh_rejections={bh_rej.sum()}\nby_rejections={by_rej.sum()}\nstatus=PASS\n",
    encoding="utf-8",
)
