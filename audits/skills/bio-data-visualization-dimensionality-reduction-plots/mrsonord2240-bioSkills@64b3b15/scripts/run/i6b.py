import numpy as np, scanpy as sc, warnings, sys, os
warnings.filterwarnings('ignore'); sys.path.insert(0, r'F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\pylib')
from sklearn.metrics import adjusted_rand_score
a = sc.read_h5ad(r'F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\ex\processed.h5ad')
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a); sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3'); sc.pp.scale(a, max_value=10); sc.tl.pca(a, n_comps=50, random_state=42)
v = a.uns['pca']['variance_ratio']; print('PC1..5 %% var:', np.round(v[:5]*100,2), ' sum first 5: %.1f%%' % (v[:5].sum()*100))
sc.pp.neighbors(a, n_neighbors=30, n_pcs=50); sc.tl.leiden(a, resolution=0.5, random_state=42, flavor='igraph', n_iterations=2, directed=False)
print('ARI leiden vs 5 planted clusters: %.3f ; PC1-2 cluster R2 shown by kNN' % adjusted_rand_score(a.obs.cluster_true, a.obs.leiden))
