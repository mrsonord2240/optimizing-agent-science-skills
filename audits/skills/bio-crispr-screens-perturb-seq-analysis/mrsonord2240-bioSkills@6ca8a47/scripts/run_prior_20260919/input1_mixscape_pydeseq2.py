"""Input 1 (Canonical) -- follow SKILL.md 'Pertpy Unified Framework' section verbatim
on synthetic Perturb-seq data (NOT real biology): normalize, Mixscape escaper filtering,
PyDESeq2 pseudobulk DE per perturbation vs NTC.
"""
import pertpy as pt
import scanpy as sc
import anndata as ad
import numpy as np
import pandas as pd

adata = ad.read_h5ad("F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/synthetic_perturbseq.h5ad")
adata.layers["counts"] = adata.X.copy()

# === Standard scRNA-seq preprocessing (verbatim pattern from SKILL.md) ===
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=100)

# === Mixscape escaper filtering (verbatim call pattern from SKILL.md) ===
ms = pt.tl.Mixscape()
ms.perturbation_signature(adata, pert_key='perturbation', control='NTC', n_neighbors=20)
ms.mixscape(adata, pert_key='perturbation', control='NTC')

print("mixscape_class_global counts:")
print(adata.obs['mixscape_class_global'].value_counts())
print("\nmixscape_class counts (per-perturbation KO/NP):")
print(adata.obs['mixscape_class'].value_counts())

# KO retention rate per perturbation (as the Skill instructs to report)
for pert in ["GENE_A", "GENE_B", "GENE_C", "GENE_D"]:
    sub = adata.obs[adata.obs['perturbation'] == pert]
    ko_rate = (sub['mixscape_class_global'] == 'KO').mean()
    print(f"{pert}: KO retention = {ko_rate:.1%} (n={len(sub)})")

# Filter to KO cells + NTC controls
adata_filtered = adata[adata.obs['mixscape_class_global'].isin(['KO', 'NTC'])].copy()
print(f"\nCells after Mixscape filtering: {adata_filtered.n_obs} / {adata.n_obs}")

# === Restore raw counts for PyDESeq2 (pseudobulk DE needs counts, not log-normalized) ===
adata_filtered.X = adata_filtered.layers["counts"].copy()

# === Differential expression via pertpy's PyDESeq2 wrapper (verbatim call pattern) ===
de = pt.tl.PyDESeq2(adata_filtered, design='~perturbation')
de.fit()

all_de = []
for pert in adata_filtered.obs['perturbation'].unique():
    if pert == 'NTC':
        continue
    # NOTE: SKILL.md's documented call `de.test_contrasts(contrast=('perturbation', pert, 'NTC'))`
    # TypeErrors against installed pertpy 1.3.0 (test_contrasts requires a numeric contrast vector,
    # not a tuple, and the kwarg is `contrasts` not `contrast`). Corrected call below using the
    # `.contrast()` builder that pertpy 1.3.0 actually exposes -- this is an audit fix, not part of
    # the Skill's own instructions.
    contrast_df = de.test_contrasts(de.contrast('perturbation', 'NTC', pert))
    contrast_df['perturbation'] = pert
    all_de.append(contrast_df)
de_result = pd.concat(all_de)
de_result.to_csv("F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/run/pertpy_de_results.tsv", sep='\t')
print(f"\nDE results shape: {de_result.shape}")

for pert in de_result['perturbation'].unique():
    sub = de_result[de_result['perturbation'] == pert].sort_values('padj')
    n_sig = (sub['padj'] < 0.05).sum()
    print(f"{pert}: {n_sig}/{len(sub)} genes padj<0.05")
    print(sub.head(5)[['log2FoldChange', 'padj']].to_string())
