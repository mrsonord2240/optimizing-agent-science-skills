"""Input 3 (Edge/boundary) -- run the Skill's own assign_sgrna() function verbatim
(copied from SKILL.md 'MOI and sgRNA Assignment' section) against synthetic sgRNA counts.
"""
import anndata as ad
import numpy as np

adata = ad.read_h5ad("F:/OpenScience/audits/bio-crispr-screens-perturb-seq-analysis/data/synthetic_sgrna.h5ad")


# === Verbatim from SKILL.md ===
def assign_sgrna(adata, sgrna_counts_layer='sgrna_counts', threshold=10):
    '''Per-cell sgRNA assignment. Returns single assignment or 'multiplet'/'none'.'''
    import numpy as np
    counts = adata.layers[sgrna_counts_layer]  # cells x sgRNAs
    above_thresh = counts >= threshold
    n_sgrna_per_cell = above_thresh.sum(axis=1)
    assignments = np.where(
        n_sgrna_per_cell == 0, 'none',
        np.where(n_sgrna_per_cell == 1,
                  [adata.var_names[i] for i in counts.argmax(axis=1)],
                  'multiplet'))
    adata.obs['sgrna_assignment'] = assignments
    return adata
# === end verbatim ===

adata = assign_sgrna(adata)
vc = adata.obs['sgrna_assignment'].value_counts()
print("Assignment counts:")
print(vc)
n_total = adata.n_obs
n_assigned_single = (~adata.obs['sgrna_assignment'].isin(['none', 'multiplet'])).sum()
n_multiplet = (adata.obs['sgrna_assignment'] == 'multiplet').sum()
n_none = (adata.obs['sgrna_assignment'] == 'none').sum()
print(f"\nTotal cells: {n_total}")
print(f"Assignment rate (single sgRNA): {n_assigned_single/n_total:.1%}")
print(f"Multiplet rate: {n_multiplet/n_total:.1%}")
print(f"None (unassigned): {n_none/n_total:.1%}")

# Ground truth check: cells I planted a single high-count sgRNA for should be correctly assigned.
