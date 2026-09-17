"""
Round-3 re-audit, Input 3 (Edge, NEW).

The round-3 fix's headline claim for detect_cn_bias() is not just "it flags real residual bias
under low power" (Input 2, regression) but also that suspicious_despite_ns does NOT cry wolf on
a genuinely well-corrected screen -- explicitly named in this audit's dispatch as a claim to
check. Neither prior audit tested this directly for the NEW fields (the round-2 audit's Input 8
tested only the OLD bias_present field's false-positive rate, before low_power_floor/
suspicious_despite_ns existed).

Method: take REAL diploid (CN=2) HT-29 genes -- which by construction have no CN-driven
depletion -- and relabel a small (<8, so low_power_floor=True) group of them as "amplified,
successfully corrected" (CN=6). Their real LFCs are close to the diploid background by
construction (they ARE diploid genes), which is exactly what "successful correction" looks
like: an amplicon whose LFC has been brought back down to the diploid baseline. Do this for 5
independently drawn groups to avoid relying on a single lucky draw.

If suspicious_despite_ns fires here, the fix cries wolf on success. If it stays False while
low_power_floor stays True (correctly reporting "small n, but nothing suspicious"), the fix
behaves as documented.
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
        'amplified_mean_lfc': amplified.mean(),
        'diploid_mean_lfc': diploid.mean(),
        'amplified_vs_diploid_gap': gap,
        'p_amplified_more_depleted': p_gap,
        'bias_present': bool((rho < -0.1 and p < 0.01) or (gap < -0.5 and p_gap < 0.01)),
        'low_power_floor': bool(low_power),
        'suspicious_despite_ns': bool(low_power and not pd.isna(gap) and gap < -0.5),
    }

post = pd.read_csv("../ccr_ht29/ht29_post_gene_lfc_cn.csv")
diploid_pool = post[post["copy_number"].between(1.5, 2.5)].reset_index(drop=True)
print(f"Real diploid gene pool: {len(diploid_pool)} genes\n")

n_trials = 5
n_amplicon_genes = 5  # < low_power_n=8, so low_power_floor should be True every time
false_alarms = 0

for trial in range(n_trials):
    idx = np.random.choice(len(diploid_pool), size=n_amplicon_genes, replace=False)
    relabel = diploid_pool.index.isin(idx)
    trial_df = diploid_pool.copy()
    trial_df.loc[relabel, "copy_number"] = 6.0  # pretend these are a corrected amplicon, CN=6

    r = detect_cn_bias(trial_df[["gene", "lfc"]], trial_df[["gene", "copy_number"]])
    flag = "CRIED WOLF" if r["suspicious_despite_ns"] else "silent (correct)"
    print(f"trial {trial}: n_amplified={r['n_amplified_genes']} gap={r['amplified_vs_diploid_gap']:.4f} "
          f"p_gap={r['p_amplified_more_depleted']:.4f} low_power_floor={r['low_power_floor']} "
          f"suspicious_despite_ns={r['suspicious_despite_ns']} bias_present={r['bias_present']} -> {flag}")
    if r["suspicious_despite_ns"]:
        false_alarms += 1
    assert r["low_power_floor"] is True, "expected low_power_floor True at n=5 < low_power_n=8"

print(f"\nFalse-alarm rate (suspicious_despite_ns fired on a genuinely-diploid-LFC 'corrected' "
      f"amplicon): {false_alarms}/{n_trials}")
print("DONE")
