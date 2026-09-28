"""Input 7 (Adversarial): user wants to read inter-cluster UMAP distance as biology. Tests the Skill's factual basis:
 'local neighborhoods are preserved by construction' vs measured k-NN retention (real pbmc68k_reduced + synthetic), and distance instability across seeds."""
import numpy as np, scanpy as sc, umap, warnings; warnings.filterwarnings('ignore')
from sklearn.neighbors import NearestNeighbors
from scipy.stats import spearmanr
from scipy.spatial.distance import pdist
def retention(Xhi, Elo, k=15):
    a = NearestNeighbors(n_neighbors=k+1).fit(Xhi).kneighbors(Xhi, return_distance=False)[:,1:]
    b = NearestNeighbors(n_neighbors=k+1).fit(Elo).kneighbors(Elo, return_distance=False)[:,1:]
    return np.mean([len(set(x)&set(y))/k for x,y in zip(a,b)])
pb = sc.datasets.pbmc68k_reduced(); X = pb.obsm['X_pca']
for nn, md in [(15,0.1),(30,0.3),(30,0.5)]:
    E = umap.UMAP(n_neighbors=nn, min_dist=md, random_state=42).fit_transform(X)
    print('pbmc68k_reduced (700 cells, real) UMAP nn=%d md=%.1f: mean fraction of high-dim 15-NN kept in 2-D = %.2f' % (nn, md, retention(X, E)))
Xs = np.load(r'F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\data\sc_hier6_pca50.npy')
import openTSNE
E = umap.UMAP(n_neighbors=30, min_dist=0.3, random_state=42).fit_transform(Xs); print('synthetic 6-cluster (1500): UMAP retention %.2f' % retention(Xs, E))
T = np.asarray(openTSNE.TSNE(perplexity=30, random_state=42, n_jobs=-1).fit(Xs)); print('synthetic 6-cluster: t-SNE retention %.2f' % retention(Xs, T))
# distance instability: real pbmc cluster centroid distances across 5 UMAP seeds
lab = pb.obs.bulk_labels.values.astype(str); groups = sorted(set(lab))
def cent(E): return pdist(np.array([E[lab==g].mean(0) for g in groups]))
hi = cent(X); rs=[]
for s in range(5):
    E = umap.UMAP(n_neighbors=30, min_dist=0.3, random_state=s).fit_transform(X); rs.append(spearmanr(hi, cent(E))[0])
print('pbmc: Spearman(centroid distances, high-dim vs UMAP) across 5 seeds:', np.round(rs,2), ' between-seed pairwise:', end=' ')
Es = [cent(umap.UMAP(n_neighbors=30, min_dist=0.3, random_state=s).fit_transform(X)) for s in range(4)]
print(np.round([spearmanr(Es[i],Es[j])[0] for i in range(4) for j in range(i+1,4)],2))
