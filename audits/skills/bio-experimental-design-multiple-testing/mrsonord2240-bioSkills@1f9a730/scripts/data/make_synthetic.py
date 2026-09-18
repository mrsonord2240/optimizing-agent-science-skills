"""Synthetic data for re-audit of bio-experimental-design-multiple-testing (2026-09-18).
Independently generated (different seed, different generator) from the pre-fix audit's
data/make_synthetic.py, so this is a fresh probe, not a replay of the same random draw.
All data is SYNTHETIC; gene IDs are prefixed REGENE / REHOM so nothing looks real.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260918)

# 18,000-feature DE table, 6 vs 6 design, pooled two-sample t-test so null p is uniform.
n_genes = 18000
n_de = 1500
mean_expression = rng.gamma(shape=2.0, scale=2.0, size=n_genes)  # covariate independent of null p
# noise falls with mean expression -> power rises with mean expression (legit IHW covariate)
sigma = 2.0 / np.sqrt(1.0 + mean_expression)
effect = np.zeros(n_genes)
de_idx = rng.choice(n_genes, size=n_de, replace=False)
effect[de_idx] = rng.normal(loc=2.6, scale=0.6, size=n_de) * rng.choice([-1, 1], size=n_de)

n1 = n2 = 6
x1 = rng.normal(0, 1, size=(n_genes, n1)) * sigma[:, None]
x2 = (rng.normal(0, 1, size=(n_genes, n2)) * sigma[:, None]) + effect[:, None]

from scipy import stats
tstat, pval = stats.ttest_ind(x2, x1, axis=1)

df = pd.DataFrame({
    "gene_id": [f"REGENE{i:05d}" for i in range(n_genes)],
    "pvalue": pval,
    "mean_expression": mean_expression,
    "is_true_alt": np.isin(np.arange(n_genes), de_idx),
})
df.to_csv("de_pvalues_reaudit.csv", index=False)

null_mask = ~df["is_true_alt"].values
print(f"REAUDIT SYNTHETIC DE table: {df.shape} | true alternatives: {n_de} | pi0(true) = {1-n_de/n_genes:.4f}")
print(f"raw p<0.05: {(df.pvalue<0.05).sum()} | null p<0.05 (expect ~{int(null_mask.sum()*0.05)}): {(df.pvalue[null_mask]<0.05).sum()}")
print(f"corr(mean_expression, pvalue | null) = {np.corrcoef(df.mean_expression[null_mask], df.pvalue[null_mask])[0,1]:.4f}")

# 40-term all-null GO-style set for the edge input
n_terms = 40
go_p = rng.uniform(0, 1, size=n_terms)
go_df = pd.DataFrame({"term_id": [f"REGO{i:03d}" for i in range(n_terms)], "pvalue": go_p})
go_df.to_csv("go_all_null_reaudit.csv", index=False)
print(f"REAUDIT all-null GO set: {n_terms} terms, min p = {go_p.min():.4f}")
