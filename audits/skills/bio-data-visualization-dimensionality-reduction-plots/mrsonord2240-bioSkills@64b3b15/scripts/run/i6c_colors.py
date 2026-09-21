"""Do the example's c=cat.codes + cmap='tab20'/'tab10' colours equal the categorical palette used by sc.pl.umap(palette='tab20')?"""
import numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, Normalize
codes = np.arange(5)                                  # leiden 0..4
cont = plt.get_cmap('tab20')(Normalize(codes.min(), codes.max())(codes))[:,:3]
# scanpy sc.pl.umap(palette='tab20') assigns categories the first n entries of tab20 (0,1,2,...)
cat = np.array([plt.get_cmap('tab20')(i)[:3] for i in range(5)]) 
# NOTE: tab20 is a ListedColormap of 20 colours; cmap(i) with int i indexes the list, cmap(float) interpolates over range
print('example (continuous mapping of codes):', [tuple(np.round(c,2)) for c in cont])
print('scanpy categorical palette tab20[0:5]  :', [tuple(np.round(c,2)) for c in cat])
print('same colours per cluster across UMAP and t-SNE panels:', np.allclose(cont, cat, atol=1e-6))
c2 = plt.get_cmap('tab10')(Normalize(0,1)(np.array([0,1])))[:,:3]; print('2-level condition with cmap=tab10 ->', [tuple(np.round(c,2)) for c in c2], '(tab10[0]=blue, tab10[9]=cyan; orange not used)')
# ---- what scanpy actually assigns with palette='tab20' (real object)
import scanpy as sc, warnings, sys; warnings.filterwarnings('ignore')
sys.path.insert(0, r'F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\pylib')
from matplotlib.colors import to_rgb
a = sc.read_h5ad(r'F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\ex\processed.h5ad')
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a); sc.pp.scale(a, max_value=10); sc.tl.pca(a, n_comps=30, random_state=42); sc.pp.neighbors(a, n_neighbors=30, n_pcs=30)
sc.tl.umap(a, min_dist=0.3, random_state=42); sc.tl.leiden(a, resolution=0.5, random_state=42, flavor='igraph', n_iterations=2, directed=False)
sc.pl.umap(a, color='leiden', palette='tab20', show=False)
print('scanpy leiden_colors with palette=tab20:', [tuple(np.round(to_rgb(c),2)) for c in a.uns['leiden_colors']])
scp = np.array([to_rgb(c) for c in a.uns['leiden_colors']]); n=len(scp); cont = plt.get_cmap('tab20')(np.linspace(0,1,n))[:,:3]
print('scanpy palette == linspace-sampled tab20 (== example c=codes mapping):', np.allclose(scp, cont, atol=1e-2))
