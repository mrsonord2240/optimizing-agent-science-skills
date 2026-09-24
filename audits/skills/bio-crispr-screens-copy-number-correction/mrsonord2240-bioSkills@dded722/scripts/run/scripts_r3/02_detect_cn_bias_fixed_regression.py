"""
Round-3 re-audit, Input 2 (Variant A, REGRESSION).

Runs the round-3-FIXED detect_cn_bias() (SKILL.md @ 9d31109 -- now with low_power_n=8,
low_power_floor, suspicious_despite_ns) verbatim against the SAME real post-CRISPRcleanR
HT-29 FAM84B/MYC/POU5F1B 3-gene amplicon block that the round-2 re-audit's Input 9 used to
find the false-negative-by-underpowering problem this fix addresses (gap=-0.98, p=0.208,
n_amplified=3).

Purpose: confirm low_power_floor and suspicious_despite_ns actually fire the way SKILL.md's
new text claims on that exact real case, using data already on disk from the round-2 audit
(ccr_ht29/ht29_pre_gene_lfc_cn.csv, ht29_post_gene_lfc_cn.csv) -- no new wet numbers needed
here since the underlying screen and CN calls are unchanged; only the function changed.
"""
import pandas as pd
from scipy.stats import spearmanr, mannwhitneyu

# === Verbatim from the ROUND-3 FIXED SKILL.md ===
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
        'cn_lfc_rho': rho,
        'p_value': p,
        'n_amplified_genes': len(amplified),
        'amplified_mean_lfc': amplified.mean(),
        'diploid_mean_lfc': diploid.mean(),
        'amplified_vs_diploid_gap': gap,
        'p_amplified_more_depleted': p_gap,
        'bias_present': bool((rho < -0.1 and p < 0.01) or (gap < -0.5 and p_gap < 0.01)),
        'low_power_floor': bool(low_power),
        'suspicious_despite_ns': bool(low_power and not pd.isna(gap) and gap < -0.5),
    }

pre = pd.read_csv("../ccr_ht29/ht29_pre_gene_lfc_cn.csv")
post = pd.read_csv("../ccr_ht29/ht29_post_gene_lfc_cn.csv")

block = ["FAM84B", "MYC", "POU5F1B"]

print("=== PRE-correction, focused on real amplicon block (n=3 amplified) ===")
pre_block = pre[pre["gene"].isin(block) | pre["copy_number"].between(1.5, 2.5)]
r_pre = detect_cn_bias(pre_block[["gene", "lfc"]], pre_block[["gene", "copy_number"]])
for k, v in r_pre.items():
    print(f"  {k}: {v}")

print("\n=== POST-correction, focused on real amplicon block (n=3 amplified) ===")
post_block = post[post["gene"].isin(block) | post["copy_number"].between(1.5, 2.5)]
r_post = detect_cn_bias(post_block[["gene", "lfc"]], post_block[["gene", "copy_number"]])
for k, v in r_post.items():
    print(f"  {k}: {v}")

print("\n=== Regression checks against SKILL.md's documented round-3 claims ===")
assert r_post["n_amplified_genes"] == 3, "expected n=3 amplified genes in the real block"
assert r_post["low_power_floor"] is True, "expected low_power_floor True at n=3 < low_power_n=8"
gap_ok = abs(r_post["amplified_vs_diploid_gap"] - (-0.98)) < 0.05
p_ok = abs(r_post["p_amplified_more_depleted"] - 0.208) < 0.02
print(f"  gap ~ -0.98? {gap_ok} (actual {r_post['amplified_vs_diploid_gap']:.4f})")
print(f"  p ~ 0.208?   {p_ok} (actual {r_post['p_amplified_more_depleted']:.4f})")
print(f"  bias_present (should be False, real gap masked by low power): {r_post['bias_present']}")
print(f"  suspicious_despite_ns (should be True -- this is the whole point of the fix): "
      f"{r_post['suspicious_despite_ns']}")

print("\nDONE")
