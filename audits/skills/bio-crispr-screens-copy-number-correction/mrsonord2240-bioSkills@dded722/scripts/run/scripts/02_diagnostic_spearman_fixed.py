"""
Runs the FIXED Skill's own documented detect_cn_bias() function (SKILL.md,
"Detect Uncorrected CN Bias" section, mrsonord2240/bioSkills@6847328) verbatim,
against REAL data: gene-level mean logFC from CRISPRcleanR's own bundled real
HT-29 screen (see run/ccr_ht29_real_run.R), merged with real GDSC.geneLevCNA
copy-number calls for HT-29 (COSMIC 905939). No synthetic/planted data here --
this is a real screen and a real CN profile, exactly as the fixer verified
during the fix pass (fixes/bio-crispr-screens-copy-number-correction.md).

Real focal amplicon: FAM84B/MYC/POU5F1B, chr8:~128.6-128.9Mb, CN=8 in HT-29.

Purpose: regression-test the P1 fix (genome-wide Spearman rho alone misses a
small real amplicon; the fixed function adds an amplified-vs-diploid gap +
one-sided Mann-Whitney check). Run on both pre-correction and post-correction
gene-level LFCs.
"""
import pandas as pd
from scipy.stats import spearmanr, mannwhitneyu

# === Verbatim from the FIXED SKILL.md ===
def detect_cn_bias(gene_lfc_df, cn_df, amplified_cn=4, diploid_cn=(1.5, 2.5)):
    '''Test whether amplified genes are depleted relative to diploid ones.'''
    merged = gene_lfc_df.merge(cn_df, on='gene')
    rho, p = spearmanr(merged['copy_number'], merged['lfc'])
    amplified = merged[merged['copy_number'] > amplified_cn]['lfc']
    diploid = merged[merged['copy_number'].between(*diploid_cn)]['lfc']
    gap, p_gap = float('nan'), float('nan')
    if len(amplified) >= 3 and len(diploid) >= 3:
        gap = amplified.mean() - diploid.mean()
        p_gap = mannwhitneyu(amplified, diploid, alternative='less').pvalue
    return {
        'cn_lfc_rho': rho,
        'p_value': p,
        'n_amplified_genes': len(amplified),
        'amplified_mean_lfc': amplified.mean(),
        'diploid_mean_lfc': diploid.mean(),
        'amplified_vs_diploid_gap': gap,
        'p_amplified_more_depleted': p_gap,
        'bias_present': bool((rho < -0.1 and p < 0.01) or (gap < -0.5 and p_gap < 0.01)),
    }

pre = pd.read_csv("../ccr_ht29/ht29_pre_gene_lfc_cn.csv")
post = pd.read_csv("../ccr_ht29/ht29_post_gene_lfc_cn.csv")

print("=== PRE-correction, genome-wide (n=%d genes) ===" % len(pre))
r = detect_cn_bias(pre[["gene", "lfc"]], pre[["gene", "copy_number"]])
for k, v in r.items():
    print(f"  {k}: {v}")

print("\n=== POST-correction, genome-wide (n=%d genes) ===" % len(post))
r = detect_cn_bias(post[["gene", "lfc"]], post[["gene", "copy_number"]])
for k, v in r.items():
    print(f"  {k}: {v}")

# === Focused: only the real 3-gene amplicon block + a diploid background sample ===
block = ["FAM84B", "MYC", "POU5F1B"]
print(f"\n=== PRE-correction, focused on real amplicon block {block} vs diploid background ===")
pre_block = pre[pre["gene"].isin(block) | pre["copy_number"].between(1.5, 2.5)]
r = detect_cn_bias(pre_block[["gene", "lfc"]], pre_block[["gene", "copy_number"]])
for k, v in r.items():
    print(f"  {k}: {v}")

print(f"\n=== POST-correction, focused on real amplicon block {block} vs diploid background ===")
post_block = post[post["gene"].isin(block) | post["copy_number"].between(1.5, 2.5)]
r = detect_cn_bias(post_block[["gene", "lfc"]], post_block[["gene", "copy_number"]])
for k, v in r.items():
    print(f"  {k}: {v}")

print("\n=== Per-gene detail for the amplicon block ===")
print(pre[pre["gene"].isin(block)].to_string(index=False))
print(post[post["gene"].isin(block)].to_string(index=False))
