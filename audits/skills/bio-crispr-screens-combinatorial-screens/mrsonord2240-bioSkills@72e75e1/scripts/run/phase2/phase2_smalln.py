"""Fresh multi-seed check of the documented small-N z-score limitation."""
from __future__ import annotations

import numpy as np
from scipy.stats import zscore

rng = np.random.default_rng(230923)
results = {}
for n in (9, 20, 30, 50):
    missed = 0
    total = 0
    for _ in range(1000):
        gi = rng.normal(0.0, 0.4, n)
        gi[:2] = rng.normal(-2.5, 0.15, 2)
        z = zscore(gi)
        missed += int((z[:2] >= -2).sum())
        total += 2
    results[n] = missed / total
    print(f"N={n}: missed={missed}/{total} ({results[n]:.2%})")
assert results[9] > 0.9
assert results[50] <= 0.001
claim_reproduced = 0.02 <= results[20] <= 0.06 and 0.002 <= results[30] <= 0.01
print(f"literal_SKILL_numeric_claim_reproduced={claim_reproduced}")
if not claim_reproduced:
    print("ASSERT FAIL: the stated ~4% (N=20) and ~0.5% (N=30) rates did not reproduce under the stated model.")
