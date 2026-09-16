"""
Runs the Skill's OWN documented diagnostic function (SKILL.md, "Detect Uncorrected
CN Bias" section) verbatim against the real MAGeCK gene-level LFC output from the
planted HAP1 TKOv3 screen, merged with the planted (known, honest) CN profile.
"""
import pandas as pd
from scipy.stats import spearmanr

def detect_cn_bias(gene_lfc_df, cn_df):
    '''Test whether gene-level LFC negatively correlates with copy number.
    A bias-free screen has Spearman rho near zero between CN and LFC.'''
    merged = gene_lfc_df.merge(cn_df, on='gene')
    rho, p = spearmanr(merged['copy_number'], merged['lfc'])
    return {
        'cn_lfc_rho': rho,
        'p_value': p,
        'amplified_mean_lfc': merged[merged['copy_number'] > 4]['lfc'].mean(),
        'diploid_mean_lfc': merged[(merged['copy_number'] >= 1.5) & (merged['copy_number'] <= 2.5)]['lfc'].mean(),
        'bias_present': rho < -0.1 and p < 0.01,
    }

gene_summary = pd.read_csv("mageck_out/planted.gene_summary.txt", sep="\t")
gene_lfc = gene_summary.rename(columns={"id": "gene", "neg|lfc": "lfc"})[["gene", "lfc"]]

cn = pd.read_csv("../data/hap1_tkov3_planted_cn_profile.txt", sep="\t")

result = detect_cn_bias(gene_lfc, cn)
print("=== Whole-genome Spearman diagnostic (18,056 genes, only 8 planted-amplified) ===")
for k, v in result.items():
    print(f"  {k}: {v}")

print()
print("=== Amplicon-subset-only check (what a real analyst would actually look at) ===")
amplicon = ["ERBB2", "GRB7", "STARD3", "PGAP3", "MIEN1", "PNMT", "CASC3", "IKZF3"]
merged = gene_lfc.merge(cn, on="gene")
amp_rows = merged[merged["gene"].isin(amplicon)]
print(amp_rows.to_string(index=False))
print(f"\nAmplicon-gene mean LFC: {amp_rows['lfc'].mean():.3f}")
print(f"Genome-wide median LFC (all genes): {merged['lfc'].median():.3f}")
diploid_only = merged[merged['copy_number'] == 2.0]
print(f"Diploid (CN=2) gene mean LFC (n={len(diploid_only)}): {diploid_only['lfc'].mean():.3f}")
