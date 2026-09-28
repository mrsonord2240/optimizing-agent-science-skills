"""Input 3b: SKILL claims (a) 'PCA color by batch exposes batch; UMAP can hide it' (b) inter-cluster UMAP distances not meaningful. Planted batch effect + planted cluster hierarchy."""
import numpy as np, pandas as pd, scanpy as sc, anndata as ad, umap, warnings
warnings.filterwarnings('ignore')
from scipy.stats import spearmanr
from scipy.spatial.distance import pdist
from sklearn.neighbors import NearestNeighbors
rng = np.random.default_rng(5)
n, G = 900, 1000
ct = rng.integers(0, 3, n); batch = rng.integers(0, 2, n)
base = rng.gamma(0.5, 1, G)
lfc = np.zeros((n, G))
for c in range(3): lfc[np.ix_(ct==c, np.arange(c*80, c*80+80))] = 2.0
bg = np.arange(600, 700); lfc[np.ix_(batch==1, bg)] += 1.0*np.where(np.arange(100)%2==0, 1, -1)   # batch effect on 100 genes
counts = rng.poisson(base*2**lfc*rng.lognormal(0,0.3,n)[:,None]*2).astype('float32')
a = ad.AnnData(counts); a.obs['ct']=ct.astype(str); a.obs['batch']=batch.astype(str)
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a); sc.pp.scale(a, max_value=10); sc.tl.pca(a, n_comps=30, random_state=42)
X = a.obsm['X_pca']
def r2(v,g):
    g=pd.Series(g); return 1-sum(((v[g==k]-v[g==k].mean())**2).sum() for k in g.unique())/((v-v.mean())**2).sum()
print('PC R2 batch:', [round(r2(X[:,i], a.obs.batch.values),2) for i in range(5)], ' PC R2 celltype:', [round(r2(X[:,i], a.obs.ct.values),2) for i in range(5)])
sc.pp.neighbors(a, n_neighbors=30, n_pcs=30); sc.tl.umap(a, min_dist=0.3, random_state=42)
U = a.obsm['X_umap']
def batch_sep(E, k=30):
    """within a cell type, fraction of kNN that share the cell's batch; 0.5 = perfectly mixed"""
    out=[]
    for c in '012':
        m = (a.obs.ct.values==c); Ec = E[m]; b = batch[m]
        idx = NearestNeighbors(n_neighbors=k+1).fit(Ec).kneighbors(Ec, return_distance=False)[:,1:]
        out.append((b[idx]==b[:,None]).mean())
    return np.round(out,3)
print('same-batch kNN fraction within cell type (0.5=mixed, 1=separated)  PCA:', batch_sep(X), ' UMAP:', batch_sep(U))
# (b) hierarchy: cluster distances in PCA vs UMAP across seeds
lab = a.obs.ct.values
cd = lambda E: pdist(np.array([E[lab==c].mean(0) for c in '012']))
print('PCA centroid distances (01,02,12):', np.round(cd(X),1))
res=[]
for s in range(5):
    e = umap.UMAP(n_neighbors=30, min_dist=0.3, random_state=s).fit_transform(X[:, :30]); d = cd(e); res.append(d/d.max())
print('UMAP centroid distances (normalised), 5 seeds:'); print(np.round(np.array(res),2))
print('PCA normalised:', np.round(cd(X)/cd(X).max(),2))
