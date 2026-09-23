"""
Re-auditor's own synthetic ground-truth test for the fixed PyDESeq2 contrast API
(SKILL.md 'Pertpy Unified Framework' block, examples/run_pertpy.py).

Independent of the fixer's fixture: different RNG seed, different gene count,
different effect sizes, different number of planted-null genes, pseudobulk
(sample-level) design so PyDESeq2's own count-based assumptions are respected
without relying on any single-cell-specific code path.

Verifies:
  1. pt.tl.PyDESeq2(...).fit() works with layer='counts' (raw integer counts).
  2. de.contrast('condition', 'ctrl', 'treat') + de.test_contrasts(...) is the
     correct call sequence on pertpy 1.3.0 (no AttributeError/TypeError).
  3. Result columns are named log_fc / p_value / adj_p_value (not the stale
     log2FoldChange / padj).
  4. Planted DE genes are recovered (low adj_p_value, correct-sign log_fc);
     planted null genes are not falsely called at strict FDR.
"""
import numpy as np
import pandas as pd
import anndata as ad
import pertpy as pt

rng = np.random.default_rng(20260919)

n_genes = 150
n_planted_up = 8
n_planted_down = 8
n_samples_per_group = 6  # pseudobulk "samples" (e.g. wells/replicates), not raw cells

gene_names = [f"GENE{i:04d}" for i in range(n_genes)]
baseline_mean = rng.uniform(20, 500, size=n_genes)

# True log2 fold changes: first n_planted_up genes go up, next n_planted_down go down, rest ~0
true_lfc = np.zeros(n_genes)
true_lfc[:n_planted_up] = rng.uniform(2.0, 3.5, size=n_planted_up)          # strong up
true_lfc[n_planted_up:n_planted_up + n_planted_down] = -rng.uniform(2.0, 3.5, size=n_planted_down)  # strong down

n_samples = n_samples_per_group * 2
condition = np.array(["ctrl"] * n_samples_per_group + ["treat"] * n_samples_per_group)

counts = np.zeros((n_samples, n_genes), dtype=int)
for i in range(n_samples):
    mult = np.where(condition[i] == "treat", 2 ** true_lfc, 1.0)
    mean = baseline_mean * mult
    # negative-binomial-like overdispersion via gamma-Poisson
    disp = 0.15
    shape = 1.0 / disp
    scale = mean * disp
    lam = rng.gamma(shape, scale)
    counts[i, :] = rng.poisson(lam)

adata = ad.AnnData(
    X=counts.astype(float),
    obs=pd.DataFrame({"condition": condition}, index=[f"sample{i}" for i in range(n_samples)]),
    var=pd.DataFrame(index=gene_names),
)
adata.layers["counts"] = counts.copy()

print(f"Synthetic pseudobulk: {adata.n_obs} samples x {adata.n_vars} genes")
print(f"Planted up genes (0..{n_planted_up-1}): {gene_names[:n_planted_up]}")
print(f"Planted down genes: {gene_names[n_planted_up:n_planted_up+n_planted_down]}")

de = pt.tl.PyDESeq2(adata, design="~condition", layer="counts")
de.fit()

contrast = de.contrast("condition", "ctrl", "treat")
print("contrast vector:", contrast)

result = de.test_contrasts(contrast)
print("\nResult columns:", list(result.columns))
assert "log_fc" in result.columns, f"Expected 'log_fc' column, got {list(result.columns)}"
assert "adj_p_value" in result.columns, f"Expected 'adj_p_value' column, got {list(result.columns)}"
assert "log2FoldChange" not in result.columns, "Stale column name log2FoldChange present"
assert "padj" not in result.columns, "Stale column name padj present"

assert "variable" in result.columns, f"Expected gene names in 'variable' column, got {list(result.columns)}"
result_by_gene = result.set_index("variable")

planted_up = set(gene_names[:n_planted_up])
planted_down = set(gene_names[n_planted_up:n_planted_up + n_planted_down])
planted_null = set(gene_names[n_planted_up + n_planted_down:])

sig = result_by_gene[result_by_gene["adj_p_value"] < 0.01]
sig_up = sig[sig["log_fc"] > 0]
sig_down = sig[sig["log_fc"] < 0]

recovered_up = planted_up & set(sig_up.index)
recovered_down = planted_down & set(sig_down.index)
false_positives_in_null = planted_null & set(sig.index)

print(f"\nPlanted up recovered: {len(recovered_up)}/{n_planted_up} -> {sorted(recovered_up)}")
print(f"Planted down recovered: {len(recovered_down)}/{n_planted_down} -> {sorted(recovered_down)}")
print(f"False positives among {len(planted_null)} planted-null genes at adj_p<0.01: {len(false_positives_in_null)}")
print(f"\nTop 5 by adj_p_value overall:\n{result_by_gene.sort_values('adj_p_value').head(5)[['log_fc','p_value','adj_p_value']]}")

assert len(recovered_up) >= 6, "Expected most planted up-genes to be recovered"
assert len(recovered_down) >= 6, "Expected most planted down-genes to be recovered"
assert len(false_positives_in_null) <= 3, "Too many false positives among null genes"

print("\nPASS: contrast API works, column names correct, planted DE structure recovered on independent synthetic data.")
