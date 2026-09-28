"""Input 5b: PHATE vs UMAP on a planted BRANCHING trajectory (Y shape), 900 cells; tests the Skill's 'PHATE more faithful for continuous biology' claim."""
import numpy as np, pandas as pd, scanpy as sc, anndata as ad, umap, phate, warnings, os
warnings.filterwarnings('ignore')
from sklearn.neighbors import NearestNeighbors, kneighbors_graph
from scipy.sparse.csgraph import connected_components
from scipy.stats import spearmanr
rng = np.random.default_rng(9); n, G = 900, 1000
branch = rng.integers(0, 3, n)                # 0 = stem->A ; 1 = stem->B ; 2 = stem shared? use: cells 0..: stem first 1/3
t = rng.uniform(0, 1, n); br = np.where(t < 0.4, 0, rng.integers(1, 3, n))       # stem for t<0.4, else branch 1 or 2
gs = rng.choice(G, 300, replace=False); lfc = np.zeros((n, G))
for k, g in enumerate(gs[:100]): lfc[:, g] = 2*np.minimum(t, 0.4)*(1 if k%2 else -1)*2       # stem programme
for k, g in enumerate(gs[100:200]): lfc[:, g] = np.where(br==1, 3*(t-0.4)*(1 if k%2 else -1), 0)*(t>0.4)
for k, g in enumerate(gs[200:300]): lfc[:, g] = np.where(br==2, 3*(t-0.4)*(1 if k%2 else -1), 0)*(t>0.4)
base = rng.gamma(0.5, 1, G); counts = rng.poisson(base*2**lfc*rng.lognormal(0,0.3,n)[:,None]*2).astype('float32')
a = ad.AnnData(counts); sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a); sc.pp.scale(a, max_value=10); sc.tl.pca(a, n_comps=50, random_state=42); X = a.obsm['X_pca']
def nb_err(E,k=10):
    idx = NearestNeighbors(n_neighbors=k+1).fit(E).kneighbors(E, return_distance=False)[:,1:]; return np.abs(t[idx]-t[:,None]).mean()
def ncomp(E,k=10): return connected_components(kneighbors_graph(E, k))[0]
def sep_br(E,k=10):
    # fraction of kNN of branch-1/2 cells (t>0.6) that lie on the OTHER branch (0 = branches fully separated)
    m = (t>0.6); idx = NearestNeighbors(n_neighbors=k+1).fit(E).kneighbors(E[m], return_distance=False)[:,1:]
    return (br[idx]!=br[m][:,None]).mean()
print('HIGH-DIM (PCA-50): nb_err %.3f  comps %d  cross-branch %.3f' % (nb_err(X), ncomp(X), sep_br(X)))
for name, E in [('PHATE', phate.PHATE(knn=10, decay=40, t='auto', n_jobs=-1, random_state=42, verbose=0).fit_transform(X)),
                ('UMAP nn30 md0.3', umap.UMAP(n_neighbors=30, min_dist=0.3, random_state=42).fit_transform(X)),
                ('UMAP nn15 md0.1', umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=42).fit_transform(X))]:
    print('%-16s nb_err %.3f  knn-graph components %d  cross-branch %.3f' % (name, nb_err(E), ncomp(E), sep_br(E)))
    if name=='PHATE': np.save(r'F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\data\phate_branch.npy', E)
