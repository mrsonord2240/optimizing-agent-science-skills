"""Fresh all-null Inzolia-scale test of raw z calls versus BH-FDR."""
from __future__ import annotations

import numpy as np
from scipy.stats import norm, zscore
from statsmodels.stats.multitest import multipletests

rng = np.random.default_rng(9232026)
gi = rng.normal(0.0, 0.06, 4435)
z = zscore(gi)
p = 2 * norm.sf(np.abs(z))
reject, q, _, _ = multipletests(p, alpha=0.05, method="fdr_bh")
raw = int((np.abs(z) > 2).sum())
bh = int(reject.sum())
print(f"all-null pairs=4435 raw_abs_z_gt_2={raw} bh_fdr_lt_0_05={bh} min_q={q.min():.6g}")
assert raw >= 150
assert bh == 0
print("ASSERT PASS: raw cutoff generates many chance calls; BH-FDR makes zero false calls.")
