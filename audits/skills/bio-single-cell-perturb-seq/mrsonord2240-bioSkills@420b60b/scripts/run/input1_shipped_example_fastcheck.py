'''Regression check of the FIXED shipped examples/pertpy_analysis.py, verbatim except n_perms
reduced 1000->100 for audit runtime (same reduction the original audit applied to Input 1/4;
does not change the code paths being tested: push_obs, CSR fix, Mixscape KeyError fix).'''
import numpy as np
import scanpy as sc
import pertpy as pt

mdata = pt.dt.papalexi_2021()
adata = mdata.mod['rna']

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.pp.pca(adata, n_comps=50)

gdo = mdata.mod['gdo']
gdo.X = gdo.X.tocsr()
gdo.layers['counts'] = gdo.X.copy()
ga = pt.pp.GuideAssignment()
try:
    ga.assign_mixture_model(gdo, assigned_guides_key='assigned_guide')
    print(gdo.obs['assigned_guide'].value_counts().head())
except ImportError as e:
    print(f"assign_mixture_model unavailable ({e}); using assign_by_threshold instead")
    ga.assign_by_threshold(gdo, assignment_threshold=5, output_layer='assigned_guides')

mdata.push_obs(columns=['perturbation', 'gene_target', 'replicate'], mods=['rna'])
ms = pt.tl.Mixscape()
ms.perturbation_signature(adata, pert_key='perturbation', control='NT', n_neighbors=20)
ms.mixscape(adata, pert_key='gene_target', control='NT', layer='X_pert')
print(adata.obs['mixscape_class_global'].value_counts())

dist = pt.tl.Distance(metric='edistance', obsm_key='X_pca')
pairwise = dist.pairwise(adata, groupby='gene_target')
print(pairwise.iloc[:5, :5])

np.random.seed(0)
etest = pt.tl.DistanceTest('edistance', n_perms=100)  # reduced from SKILL.md's 1000 for audit runtime
results = etest(adata, groupby='gene_target', contrast='NT')
print(results.sort_values('pvalue').head())

print("DONE input1_fastcheck")
