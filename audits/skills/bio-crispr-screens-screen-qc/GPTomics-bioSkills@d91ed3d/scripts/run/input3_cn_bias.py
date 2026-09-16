"""Input 3 (Variant B). Prompt:
"Some of our top screen hits fall inside a known focal amplicon in this cell
line. Run the copy-number bias diagnostic: is the apparent essentiality of
these genes a CN artifact (Aguirre 2016 / Munoz 2016) rather than real
biology?"
Data: SYNTHETIC per-gene copy-number profile (no real matched WGS/SNP-array
ships with the cached HAP1 dataset) with a 40-gene amplified block, and a
companion synthetic gene-level LFC table where those amplified genes carry an
injected CN-artifact penalty on top of random noise.
"""
import sys
sys.path.insert(0, r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\run")
import pandas as pd
from qc_functions import cn_bias_diagnostic

CN = r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\synthetic_copy_number.txt"
LFC = r"F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\synthetic_gene_lfc_for_cn.txt"

cn_df = pd.read_csv(CN, sep="\t")
gene_lfc_df = pd.read_csv(LFC, sep="\t")

result = cn_bias_diagnostic(gene_lfc_df, cn_df)
print("cn_vs_lfc_rho:", result["cn_vs_lfc_rho"])
print("cn_vs_lfc_p:", result["cn_vs_lfc_p"])
print("amplified_mean_lfc:", result["amplified_mean_lfc"])
print("diploid_mean_lfc:", result["diploid_mean_lfc"])
print("\nper_bin:")
print(result["per_bin"])

verdict = "CN ARTIFACT FLAGGED" if result["cn_vs_lfc_rho"] < -0.1 else "no strong CN artifact detected"
print(f"\nSpearman rho={result['cn_vs_lfc_rho']:.4f} (threshold <-0.10 per SKILL.md) -> {verdict}")
