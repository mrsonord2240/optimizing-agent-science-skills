"""
Round-3 re-audit, Input 4 (Boundary, NEW).

Two checks on the new fields that neither the round-2 audit nor the fix log's own verification
exercised:

  (a) Exact boundary behavior of low_power_n=8: low_power_floor is defined as
      `len(amplified) < low_power_n`, so n=7 -> True, n=8 -> False, n=9 -> False. Off-by-one
      errors in floor/threshold logic are a common, easy-to-miss defect class -- worth checking
      directly rather than assuming the docstring's prose matches the code's `<`.
  (b) NaN-guard: when there are fewer than 3 amplified OR fewer than 3 diploid genes, gap and
      p_gap stay NaN (existing code path, unchanged by this fix). suspicious_despite_ns's new
      `not pd.isna(gap)` guard must not crash and must correctly resolve to False in that case
      (a plain `gap < -0.5` on NaN would silently evaluate False anyway in Python/pandas, but
      it's worth confirming no exception and no accidental True).

Uses real HT-29 diploid genes as the base pool throughout (same source as script 03), swapping
only the count of genes relabeled "amplified" and their LFCs.
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, mannwhitneyu

np.random.seed(20260917)

def detect_cn_bias(gene_lfc_df, cn_df, amplified_cn=4, diploid_cn=(1.5, 2.5), low_power_n=8):
    merged = gene_lfc_df.merge(cn_df, on='gene')
    rho, p = spearmanr(merged['copy_number'], merged['lfc'])
    amplified = merged[merged['copy_number'] > amplified_cn]['lfc']
    diploid = merged[merged['copy_number'].between(*diploid_cn)]['lfc']
    gap, p_gap = float('nan'), float('nan')
    if len(amplified) >= 3 and len(diploid) >= 3:
        gap = amplified.mean() - diploid.mean()
        p_gap = mannwhitneyu(amplified, diploid, alternative='less').pvalue
    low_power = len(amplified) < low_power_n
    return {
        'n_amplified_genes': len(amplified),
        'amplified_vs_diploid_gap': gap,
        'p_amplified_more_depleted': p_gap,
        'bias_present': bool((rho < -0.1 and p < 0.01) or (gap < -0.5 and p_gap < 0.01)),
        'low_power_floor': bool(low_power),
        'suspicious_despite_ns': bool(low_power and not pd.isna(gap) and gap < -0.5),
    }

post = pd.read_csv("../ccr_ht29/ht29_post_gene_lfc_cn.csv")
diploid_pool = post[post["copy_number"].between(1.5, 2.5)].reset_index(drop=True)

print("=== (a) Boundary of low_power_n=8 at n_amplified = 7, 8, 9 ===")
for n in (7, 8, 9):
    idx = np.random.choice(len(diploid_pool), size=n, replace=False)
    trial_df = diploid_pool.copy()
    trial_df.loc[diploid_pool.index.isin(idx), "copy_number"] = 6.0
    r = detect_cn_bias(trial_df[["gene", "lfc"]], trial_df[["gene", "copy_number"]])
    expected = n < 8
    ok = r["low_power_floor"] == expected
    print(f"  n_amplified={r['n_amplified_genes']}  low_power_floor={r['low_power_floor']}  "
          f"expected={expected}  {'OK' if ok else 'MISMATCH'}")
    assert ok, f"boundary mismatch at n={n}"

print("\n=== (b) NaN guard: fewer than 3 amplified genes (gap/p_gap stay NaN) ===")
idx = np.random.choice(len(diploid_pool), size=2, replace=False)  # only 2 -> below the n>=3 floor
trial_df = diploid_pool.copy()
trial_df.loc[diploid_pool.index.isin(idx), "copy_number"] = 6.0
try:
    r = detect_cn_bias(trial_df[["gene", "lfc"]], trial_df[["gene", "copy_number"]])
    print(f"  n_amplified={r['n_amplified_genes']}  gap={r['amplified_vs_diploid_gap']}  "
          f"suspicious_despite_ns={r['suspicious_despite_ns']}  low_power_floor={r['low_power_floor']}")
    assert pd.isna(r["amplified_vs_diploid_gap"]), "expected gap to stay NaN below the n>=3 floor"
    assert r["suspicious_despite_ns"] is False, "NaN gap must not be read as suspicious"
    print("  No exception raised on NaN gap; suspicious_despite_ns correctly resolves to False. OK")
except Exception as e:
    print(f"  CRASHED: {type(e).__name__}: {e}")
    raise

print("\nDONE")
