"""Input 3: SKILL.md scanpy/umap-learn blocks on synthetic 4-cluster scRNA counts (planted labels) + real scanpy pbmc68k_reduced."""
import os, glob, warnings, numpy as np, pandas as pd, scanpy as sc, anndata as ad, umap, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.metrics import adjusted_rand_score
from common import *
os.chdir(os.path.join(AUD,'run','w3'))
counts, obs, genes = make_sc(seed=2, n_cells=600, n_clusters=4)
adata = ad.AnnData(counts, obs=obs.copy(), var=pd.DataFrame(index=genes))
adata.write_h5ad(os.path.join(DATA,'sc_synth4.h5ad'))
sc.pp.normalize_total(adata, target_sum=1e4); sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=500); sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, n_comps=50, random_state=42)
# ---- SKILL scanpy block, verbatim
sc.settings.figdir = os.path.join(AUD,'run','w3','figures')
sc.pp.neighbors(adata, n_neighbors=30, n_pcs=50)
sc.tl.umap(adata, min_dist=0.3, random_state=42)
try:
    sc.tl.leiden(adata, resolution=0.5, random_state=42)
    print('leiden OK (as called in the Skill example); n clusters', adata.obs['leiden'].nunique(), 'ARI vs planted', round(adjusted_rand_score(adata.obs.cluster_true, adata.obs.leiden),3))
except Exception as e:
    print('leiden FAILED as called:', type(e).__name__, str(e)[:200])
    sc.tl.leiden(adata, resolution=0.5, random_state=42, flavor='igraph', n_iterations=2, directed=False)
    print('leiden flavor=igraph OK; n clusters', adata.obs['leiden'].nunique(), 'ARI vs planted', round(adjusted_rand_score(adata.obs.cluster_true, adata.obs.leiden),3))
sc.pl.umap(adata, color='leiden', palette='tab20', frameon=False, legend_loc='on data', legend_fontsize=7, save='_clusters.pdf')
print('files under figdir:', [os.path.relpath(f, os.getcwd()) for f in glob.glob('**/*.pdf', recursive=True)])
print('files at cwd:', glob.glob('*.pdf'))
sc.pl.umap(adata, color='leiden', show=False, save='myplot.pdf')
print('save=myplot.pdf ->', [os.path.basename(f) for f in glob.glob('figures/*')])
# SKILL claim: save trap writes figures/umap_x.pdf ; PDF fonts / dpi_save default
print('dpi_save default:', sc.settings._vector_friendly, sc.settings.dpi_save if hasattr(sc.settings,'dpi_save') else None)
# ---- reproducibility (Skill: deterministic given seed; without seed varies)
def um(adata, seed): 
    a=adata.copy(); sc.tl.umap(a, min_dist=0.3, random_state=seed); return a.obsm['X_umap']
u1,u2 = um(adata,42), um(adata,42); u3 = um(adata,7)
print('scanpy umap seed 42 twice identical:', np.array_equal(u1,u2), '| seed 7 vs 42 identical:', np.array_equal(u1,u3))
# scanpy default (no random_state passed): deterministic?
a=adata.copy(); sc.tl.umap(a, min_dist=0.3); b=adata.copy(); sc.tl.umap(b, min_dist=0.3)
print('scanpy umap WITHOUT random_state, run twice identical:', np.array_equal(a.obsm['X_umap'], b.obsm['X_umap']), '(scanpy default random_state=0)')
# umap-learn block verbatim
X = adata.obsm['X_pca'][:, :50]
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    r1 = umap.UMAP(n_neighbors=30, min_dist=0.3, n_components=2, metric='euclidean', random_state=42).fit_transform(X)
    r2 = umap.UMAP(n_neighbors=30, min_dist=0.3, n_components=2, metric='euclidean', random_state=42).fit_transform(X)
    print('umap-learn seed=42 twice identical:', np.array_equal(r1, r2), '| warnings:', sorted({str(x.message)[:90] for x in w}))
n1 = umap.UMAP(n_neighbors=30, min_dist=0.3).fit_transform(X); n2 = umap.UMAP(n_neighbors=30, min_dist=0.3).fit_transform(X)
print('umap-learn WITHOUT random_state twice identical:', np.array_equal(n1, n2))
# ---- colour-by-group mapping: each colour in legend/points belongs to exactly the leiden group
fig, ax = plt.subplots(figsize=(4,4)); 
cols = sc.pl.palettes.default_20
sc.pl.umap(adata, color='cluster_true', ax=ax, show=False, legend_loc='right margin')
fig.savefig(os.path.join(FIGS,'i3_umap_true.png'), dpi=100)
colmap = dict(zip(adata.obs.cluster_true.cat.categories if hasattr(adata.obs.cluster_true,'cat') else sorted(adata.obs.cluster_true.unique()), adata.uns['cluster_true_colors']))
pc = ax.collections[0].get_facecolor()
from matplotlib.colors import to_rgba
exp = np.array([to_rgba(colmap[v]) for v in adata.obs.cluster_true])
print('UMAP colours point-wise equal to cluster_true palette mapping:', np.allclose(pc[:,:3], exp[:,:3], atol=1e-3))
# UMAP recovers planted clusters visually? kNN purity in embedding
from sklearn.neighbors import NearestNeighbors
def knn_purity(E, lab, k=15):
    idx = NearestNeighbors(n_neighbors=k+1).fit(E).kneighbors(E, return_distance=False)[:,1:]
    return (lab[idx]==lab[:,None]).mean()
lab = adata.obs.cluster_true.values
print('kNN purity (planted labels) PCA:', round(knn_purity(X, lab),3), ' UMAP:', round(knn_purity(r1, lab),3))
# ---- local vs global: does inter-cluster distance survive? centroid distance order across seeds/params
def cdist_mat(E, lab):
    cs = np.array([E[lab==c].mean(0) for c in sorted(set(lab))]); 
    from scipy.spatial.distance import pdist; return pdist(cs)
from scipy.stats import spearmanr
dp = cdist_mat(X, lab)
rows=[]
for nn in (5, 30, 100):
    for md in (0.1, 0.5):
        e = umap.UMAP(n_neighbors=nn, min_dist=md, random_state=42).fit_transform(X)
        rows.append((nn, md, spearmanr(dp, cdist_mat(e, lab))[0]))
print('Spearman(centroid distances PCA vs UMAP):', [(a,b,round(c,2)) for a,b,c in rows])
# ---- real data: scanpy pbmc68k_reduced (bundled offline)
pb = sc.datasets.pbmc68k_reduced()
print('pbmc68k_reduced', pb.shape, 'obs cols', list(pb.obs.columns)[:6], 'has X_pca', 'X_pca' in pb.obsm, 'X_umap', 'X_umap' in pb.obsm)
sc.pp.neighbors(pb, n_neighbors=30, n_pcs=50); sc.tl.umap(pb, min_dist=0.3, random_state=42)
sc.pl.umap(pb, color='bulk_labels', frameon=False, legend_loc='on data', legend_fontsize=7, show=False, save='_pbmc.png')
print('pbmc bulk_labels n', pb.obs.bulk_labels.nunique(), 'kNN purity UMAP', round(knn_purity(pb.obsm['X_umap'], pb.obs.bulk_labels.values),3), 'PCA', round(knn_purity(pb.obsm['X_pca'][:,:50], pb.obs.bulk_labels.values),3))
import shutil; shutil.copy('figures/umap_pbmc.png', os.path.join(FIGS,'i3_pbmc.png'))
