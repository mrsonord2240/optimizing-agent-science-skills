'''Isolate the Mixscape KeyError/CSC fix on a random cell subsample of the real papalexi_2021
data, to confirm correctness of the fixed code path without perturbation_signature's apparent
unbounded memory growth on the full ~20,729-cell dataset (confirmed separately: two clean, isolated
attempts at the full-size verbatim example grew past 20GB and were killed to protect the shared
machine -- a real, undocumented resource-cost finding, tracked separately from correctness).'''
import numpy as np
import scanpy as sc
import pertpy as pt

mdata = pt.dt.papalexi_2021()
adata = mdata.mod['rna']
print("full adata shape:", adata.shape)

np.random.seed(0)
idx = np.random.choice(adata.n_obs, size=4000, replace=False)
adata = adata[idx].copy()
print("subsampled adata shape:", adata.shape)

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.pp.pca(adata, n_comps=50)

gdo = mdata.mod['gdo'][idx].copy()
gdo.X = gdo.X.tocsr()
gdo.layers['counts'] = gdo.X.copy()
ga = pt.pp.GuideAssignment()
try:
    ga.assign_mixture_model(gdo, assigned_guides_key='assigned_guide')
except ImportError as e:
    print(f"assign_mixture_model unavailable ({e}); using assign_by_threshold instead")
    ga.assign_by_threshold(gdo, assignment_threshold=5, output_layer='assigned_guides')
print("guide assignment step OK")

mdata.push_obs(columns=['perturbation', 'gene_target', 'replicate'], mods=['rna'])
adata.obs[['perturbation', 'gene_target', 'replicate']] = mdata.mod['rna'].obs.loc[
    adata.obs_names, ['perturbation', 'gene_target', 'replicate']]
print("push_obs + subsample alignment OK; adata.obs columns:", list(adata.obs.columns))

ms = pt.tl.Mixscape()
ms.perturbation_signature(adata, pert_key='perturbation', control='NT', n_neighbors=20)
print("perturbation_signature OK on subsample")
ms.mixscape(adata, pert_key='gene_target', control='NT', layer='X_pert')
print("mixscape() OK")
print(adata.obs['mixscape_class_global'].value_counts())

print("DONE input1_mixscape_subsample")
