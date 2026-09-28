"""Input 4: SKILL.md openTSNE Kobak-Berens block. Synthetic 6-cluster hierarchy (3 super-groups of 2 close clusters), 1500 cells."""
import numpy as np, pandas as pd, warnings, time, openTSNE, scanpy as sc, anndata as ad, os, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from scipy.spatial.distance import pdist
from common import *
rng = np.random.default_rng(11); n, G = 1500, 1200
ct = rng.integers(0, 6, n); base = rng.gamma(0.5, 1, G); lfc = np.zeros((n, G))
for c in range(6):
    sup = c//2
    lfc[np.ix_(ct==c, np.arange(sup*150, sup*150+150))] = 2.0     # super-group programme
    lfc[np.ix_(ct==c, np.arange(500+c*40, 500+c*40+40))] = 1.5    # cluster-specific
counts = rng.poisson(base*2**lfc*rng.lognormal(0,0.3,n)[:,None]*2).astype('float32')
a = ad.AnnData(counts); a.obs['ct']=ct.astype(str)
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a); sc.pp.scale(a, max_value=10); sc.tl.pca(a, n_comps=50, random_state=42)
X = a.obsm['X_pca'][:, :50]; np.save(os.path.join(DATA,'sc_hier6_pca50.npy'), X); pd.Series(ct).to_csv(os.path.join(DATA,'sc_hier6_labels.csv'), index=False)
# ---- SKILL block, verbatim
t=time.time()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    embedding = openTSNE.TSNE(perplexity=30, n_iter=750, initialization='pca', learning_rate=X.shape[0] / 12, n_jobs=-1, random_state=42).fit(X)
print('openTSNE ran in %.1fs, shape %s, type %s, warnings: %s' % (time.time()-t, np.asarray(embedding).shape, type(embedding).__name__, sorted({str(x.message)[:100] for x in w})))
E1 = np.asarray(embedding)
e2 = np.asarray(openTSNE.TSNE(perplexity=30, n_iter=750, initialization='pca', learning_rate=X.shape[0]/12, n_jobs=-1, random_state=42).fit(X))
print('openTSNE random_state=42, n_jobs=-1, twice identical:', np.array_equal(E1, e2), ' max abs diff %.3g' % np.abs(E1-e2).max())
e3 = np.asarray(openTSNE.TSNE(perplexity=30, n_iter=750, initialization='pca', learning_rate=X.shape[0]/12, n_jobs=1, random_state=42).fit(X))
e4 = np.asarray(openTSNE.TSNE(perplexity=30, n_iter=750, initialization='pca', learning_rate=X.shape[0]/12, n_jobs=1, random_state=42).fit(X))
print('openTSNE n_jobs=1 twice identical:', np.array_equal(e3, e4))
# ---- SKILL claim: default learning_rate = 200
d = openTSNE.TSNE(random_state=1); print("openTSNE default learning_rate:", d.learning_rate, "| resolves to n/12 =", X.shape[0]/12, "| default initialization:", d.initialization, "| default early_exaggeration_iter:", d.early_exaggeration_iter)
# ---- SKILL claim: PCA init + lr n/12 recovers global structure vs default(random init, lr=200)
lab = ct
def cent(E): return pdist(np.array([E[lab==c].mean(0) for c in range(6)]))
truth = cent(X)
def score(**kw):
    r=[]
    for s in range(4):
        E = np.asarray(openTSNE.TSNE(perplexity=30, n_iter=750, n_jobs=-1, random_state=s, **kw).fit(X)); r.append(spearmanr(truth, cent(E))[0])
    return np.round(r,2)
print('Spearman(centroid dists hi-dim vs t-SNE) 4 seeds  KB (pca init, lr n/12):', score(initialization='pca', learning_rate=X.shape[0]/12))
print('                                                 random init, lr=200 (Skill\'s "default"):', score(initialization='random', learning_rate=200))
print('                                                 openTSNE defaults (pca, auto):', score())
# ---- perplexity edge: Skill says perplexity>n/3 fails
Xs = X[:60]
for p in (30, 20, 5):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try:
            r = openTSNE.TSNE(perplexity=p, n_iter=250, random_state=0).fit(Xs); print(f'n=60 perplexity={p}: ran; warnings={sorted({str(x.message)[:110] for x in w})}')
        except Exception as e: print(f'n=60 perplexity={p}: ERROR {type(e).__name__}: {str(e)[:120]}')
# ---- plot with the Skill example's labelling and colour mapping
fig, ax = plt.subplots(figsize=(4,4)); sca = ax.scatter(E1[:,0], E1[:,1], c=lab, cmap='tab20', s=2, alpha=0.7, rasterized=True)
ax.set_xlabel('t-SNE 1'); ax.set_ylabel('t-SNE 2'); ax.set_title('t-SNE (perp=30, lr=n/12, PCA init)'); fig.savefig(os.path.join(FIGS,'i4_tsne.png'), dpi=100, bbox_inches='tight')
print('embedding indexing embedding[:,0] works; colour map cluster->distinct colours:', len(set(map(tuple, sca.get_facecolor()[:,:3].round(3)))))
