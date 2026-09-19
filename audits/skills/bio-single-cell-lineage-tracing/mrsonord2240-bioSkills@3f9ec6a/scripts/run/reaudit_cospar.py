"""
Re-auditor: 'Integrate Clones With State Using CoSpar' SKILL.md snippet on
(1) the original audit's 2-timepoint h5ad (regression) and (2) the
re-auditor's own 3-timepoint h5ad with a 3-way fate split (data2) -- CoSpar's
multitime inference is documented for exactly-2-time-point pairs, so this
also probes what happens with 3 timepoints present (edge case beyond what
the fixer verified).
"""
import cospar as cs
import anndata as ad
import scanpy as sc
import numpy as np

print('=== R0: literal SKILL.md snippet with NO scanpy preprocessing (expect KeyError: X_emb) ===')
adata0 = ad.read_h5ad('../data/lineage_traced.h5ad')
try:
    adata0 = cs.pp.initialize_adata_object(adata0, X_clone=adata0.obsm['X_clone'], time_info=adata0.obs['time_info'])
    adata0 = cs.tmap.infer_Tmap_from_multitime_clones(adata0, smooth_array=[15, 10, 5], sparsity_threshold=0.1)
    print('UNEXPECTED: literal snippet succeeded with no X_emb')
except KeyError as e:
    print(f'CONFIRMED literal SKILL.md snippet fails as documented: KeyError: {e} -- SKILL.md never calls sc.pp.pca/neighbors/umap before this, and cs.pp.initialize_adata_object only WARNS (does not raise) when X_emb is missing, so the crash surfaces several calls later with a confusing traceback')

print()
print('=== R1-regression (original 2-timepoint h5ad, WITH the scanpy preprocessing the original auditor silently added) ===')
adata = ad.read_h5ad('../data/lineage_traced.h5ad')
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
sc.pp.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
adata = cs.pp.initialize_adata_object(adata, X_clone=adata.obsm['X_clone'], time_info=adata.obs['time_info'])
adata = cs.tmap.infer_Tmap_from_multitime_clones(adata, smooth_array=[15, 10, 5], sparsity_threshold=0.1)
cs.tl.fate_bias(adata, selected_fates=['Monocyte', 'Neutrophil'])
fate_cols = [c for c in adata.obs.columns if 'fate_bias' in c or 'fate_map' in c]
print('fate-related obs columns produced:', fate_cols)
print('non-null fate_bias rows:', int(adata.obs[[c for c in fate_cols if 'fate_bias' in c][0]].notna().sum()) if any('fate_bias' in c for c in fate_cols) else 'n/a')

print()
print('=== R2-new (reauditor 3-timepoint h5ad, Day2/Day4/Day6) ===')
adata2 = ad.read_h5ad('../data2/lineage_traced2.h5ad')
try:
    sc.pp.normalize_total(adata2)
    sc.pp.log1p(adata2)
    sc.pp.pca(adata2)
    sc.pp.neighbors(adata2)
    sc.tl.umap(adata2)
    adata2 = cs.pp.initialize_adata_object(adata2, X_clone=adata2.obsm['X_clone'], time_info=adata2.obs['time_info'])
    adata2 = cs.tmap.infer_Tmap_from_multitime_clones(adata2, smooth_array=[15, 10, 5], sparsity_threshold=0.1)
    cs.tl.fate_bias(adata2, selected_fates=['Monocyte', 'Neutrophil'])
    fate_cols2 = [c for c in adata2.obs.columns if 'fate_bias' in c or 'fate_map' in c]
    print('3-timepoint run SUCCEEDED. fate-related obs columns:', fate_cols2)
except Exception as e:
    print(f'3-timepoint run FAILED (documents an edge the Skill does not warn about): {type(e).__name__}: {e}')
