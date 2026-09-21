"""Input 5: SKILL.md PHATE block on synthetic continuous trajectory (pseudotime planted, 800 cells) vs UMAP."""
import numpy as np, pandas as pd, scanpy as sc, anndata as ad, umap, phate, warnings, os, time, matplotlib
warnings.filterwarnings('ignore'); matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from sklearn.neighbors import NearestNeighbors
from common import *
counts, obs, genes = make_sc(seed=3, n_cells=800, n_genes=1000, traj=True)
a = ad.AnnData(counts, obs=obs, var=pd.DataFrame(index=genes))
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a); sc.pp.scale(a, max_value=10); sc.tl.pca(a, n_comps=50, random_state=42)
X = a.obsm['X_pca'][:, :50]; pt = a.obs.pseudotime.values
# ---- SKILL block verbatim (X = matrix; pseudotime colour)
t=time.time()
phate_op = phate.PHATE(knn=10, decay=40, t='auto', n_jobs=-1, random_state=42)
emb = phate_op.fit_transform(X)
print('PHATE ran %.1fs shape %s, t used = %s' % (time.time()-t, emb.shape, phate_op.optimal_t if hasattr(phate_op,'optimal_t') else '?'))
fig, ax = plt.subplots(figsize=(4,4)); sca = ax.scatter(emb[:, 0], emb[:, 1], c=pt, cmap='viridis', s=5); ax.set_xlabel('PHATE 1'); ax.set_ylabel('PHATE 2'); plt.colorbar(sca); fig.savefig(os.path.join(FIGS,'i5_phate.png'), dpi=100)
# colour mapping check: facecolors = viridis(norm(pt))
exp = plt.get_cmap('viridis')(sca.norm(pt))[:,:3]; print('PHATE colour==viridis(pseudotime):', np.allclose(sca.get_facecolor()[:,:3], exp, atol=1e-6))
emb2 = phate.PHATE(knn=10, decay=40, t='auto', n_jobs=-1, random_state=42).fit_transform(X)
print('PHATE random_state=42 twice: identical =', np.array_equal(emb, emb2), ' max|diff| = %.2e' % np.abs(emb-emb2).max())
# ---- faithfulness to planted trajectory: neighbour pseudotime error, and ordering along embedding
def nb_err(E, k=10):
    idx = NearestNeighbors(n_neighbors=k+1).fit(E).kneighbors(E, return_distance=False)[:,1:]; return np.abs(pt[idx]-pt[:,None]).mean()
def order_rho(E):
    # spearman of pseudotime with the first principal axis of the embedding
    Ec = E-E.mean(0); u,s,vt = np.linalg.svd(Ec, full_matrices=False); return abs(spearmanr(pt, Ec@vt[0])[0])
U = umap.UMAP(n_neighbors=30, min_dist=0.3, random_state=42).fit_transform(X)
P2 = X[:, :2]
print('mean |dpseudotime| among 10-NN   PHATE %.3f  UMAP %.3f  PC1-2 %.3f  (random ~ %.3f)' % (nb_err(emb), nb_err(U), nb_err(P2), np.abs(pt[np.random.permutation(len(pt))]-pt).mean()))
print('|Spearman| pseudotime vs principal axis   PHATE %.2f  UMAP %.2f  PCA %.2f' % (order_rho(emb), order_rho(U), order_rho(P2)))
# PHATE when the Skill's own tips: knn too big/small; t='auto'
for knn in (3, 10, 40):
    e = phate.PHATE(knn=knn, decay=40, t='auto', n_jobs=-1, random_state=42, verbose=0).fit_transform(X); print('knn=%d  nb_err %.3f order_rho %.2f' % (knn, nb_err(e), order_rho(e)))
# discrete clusters: PHATE vs UMAP (Skill: "For discrete cell types, UMAP is fine", PHATE less canonical)
counts2, obs2, g2 = make_sc(seed=2, n_cells=600, n_clusters=4); b = ad.AnnData(counts2, obs=obs2); sc.pp.normalize_total(b, target_sum=1e4); sc.pp.log1p(b); sc.pp.scale(b, max_value=10); sc.tl.pca(b, n_comps=50, random_state=42)
Xb = b.obsm['X_pca']; lab = np.asarray(b.obs.cluster_true.values.astype(str))
ph = phate.PHATE(knn=10, decay=40, t='auto', n_jobs=-1, random_state=42, verbose=0).fit_transform(Xb)
def pur(E,k=15): idx = NearestNeighbors(n_neighbors=k+1).fit(E).kneighbors(E, return_distance=False)[:,1:]; return (lab[idx]==lab[:,None]).mean()
print('discrete 4 clusters kNN purity PHATE %.3f UMAP %.3f' % (pur(ph), pur(umap.UMAP(n_neighbors=30,min_dist=0.3,random_state=42).fit_transform(Xb))))
fig, axs = plt.subplots(1,2, figsize=(8,4)); axs[0].scatter(U[:,0],U[:,1],c=pt,s=5,cmap='viridis'); axs[0].set_title('UMAP'); axs[1].scatter(emb[:,0],emb[:,1],c=pt,s=5,cmap='viridis'); axs[1].set_title('PHATE'); fig.savefig(os.path.join(FIGS,'i5_umap_vs_phate.png'), dpi=100)
