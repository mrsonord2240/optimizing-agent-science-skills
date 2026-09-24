"""
NEW input (not in the pre-fix audit): negative-control specificity check for the
FIXED detect_cn_bias(). Split the real HT-29 diploid (CN=2) genes into two random
halves and relabel one half as a fake "amplified" (CN=15) group -- there is no
real CN difference or biological reason for a gap, so the function should NOT
report bias_present=True. Real screen data (same source as script 02), no
manufactured effect at all -- this tests the false-positive rate of the fixed
gap+Mann-Whitney addition, not just its sensitivity (already shown by script 02).
"""
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, mannwhitneyu

def detect_cn_bias(gene_lfc_df, cn_df, amplified_cn=4, diploid_cn=(1.5, 2.5)):
    merged = gene_lfc_df.merge(cn_df, on='gene')
    rho, p = spearmanr(merged['copy_number'], merged['lfc'])
    amplified = merged[merged['copy_number'] > amplified_cn]['lfc']
    diploid = merged[merged['copy_number'].between(*diploid_cn)]['lfc']
    gap, p_gap = float('nan'), float('nan')
    if len(amplified) >= 3 and len(diploid) >= 3:
        gap = amplified.mean() - diploid.mean()
        p_gap = mannwhitneyu(amplified, diploid, alternative='less').pvalue
    return {
        'cn_lfc_rho': rho, 'p_value': p, 'n_amplified_genes': len(amplified),
        'amplified_mean_lfc': amplified.mean(), 'diploid_mean_lfc': diploid.mean(),
        'amplified_vs_diploid_gap': gap, 'p_amplified_more_depleted': p_gap,
        'bias_present': bool((rho < -0.1 and p < 0.01) or (gap < -0.5 and p_gap < 0.01)),
    }

pre = pd.read_csv("../ccr_ht29/ht29_pre_gene_lfc_cn.csv")
diploid = pre[pre["copy_number"].between(1.5, 2.5)][["gene", "lfc"]].copy()
print(f"n real diploid genes available: {len(diploid)}")

rng = np.random.default_rng(20260917)
n_trials = 5
false_positives = 0
for trial in range(n_trials):
    shuffled = diploid.sample(frac=1.0, random_state=int(rng.integers(0, 1_000_000))).reset_index(drop=True)
    half = len(shuffled) // 2
    fake_amplified = shuffled.iloc[:half].copy()
    fake_amplified["gene"] = fake_amplified["gene"] + f"__trial{trial}"
    fake_cn = pd.concat([
        pd.DataFrame({"gene": fake_amplified["gene"], "copy_number": 15.0}),
        pd.DataFrame({"gene": shuffled.iloc[half:]["gene"], "copy_number": 2.0}),
    ])
    fake_lfc = pd.concat([fake_amplified[["gene", "lfc"]], shuffled.iloc[half:][["gene", "lfc"]]])
    r = detect_cn_bias(fake_lfc, fake_cn)
    flag = r["bias_present"]
    false_positives += int(flag)
    print(f"trial {trial}: gap={r['amplified_vs_diploid_gap']:.4f} p_gap={r['p_amplified_more_depleted']:.4f} "
          f"rho={r['cn_lfc_rho']:.4f} bias_present={flag}")

print(f"\nFalse positive rate over {n_trials} random relabelings with no real CN difference: "
      f"{false_positives}/{n_trials}")
