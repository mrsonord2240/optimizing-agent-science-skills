"""Input 3 (Edge) - bio-single-cell-batch-integration
BBKNN, the graph-only method. The Skill's specific claims: it "rewrites the neighbor graph in
place (very fast, feeds Leiden/UMAP only)", produces "no embedding or corrected counts for
other uses", and "leans toward batch removal". All three tested, plus what actually happens
downstream when a pipeline assumes an embedding exists.
"""
import scanpy as sc
import scanpy.external as sce
import numpy as np
import pandas as pd
import time
from sklearn.metrics import silhouette_score, adjusted_rand_score

R = r'F:/OpenScience/audits/bio-single-cell-batch-integration/run'
a = sc.read_h5ad(R + '/input1_harmony.h5ad')
ct, bt = a.obs['cell_type'].values, a.obs['batch'].values
print(f'{a.n_obs} cells; obsm before BBKNN: {sorted(a.obsm)}')

t0 = time.time()
sce.pp.bbknn(a, batch_key='batch')
t_bbknn = time.time() - t0
print(f'bbknn ran in {t_bbknn:.2f} s')
print(f'obsm after BBKNN: {sorted(a.obsm)}  <- SKILL.md:143 says it gives no embedding')
print(f'obsp keys: {sorted(a.obsp)} (the graph it rewrote)')

sc.tl.leiden(a, key_added='leiden_bbknn', flavor='igraph', n_iterations=2, directed=False,
             random_state=0)
print(f'Leiden on the BBKNN graph: {a.obs["leiden_bbknn"].nunique()} clusters, '
      f'ARI vs true cell type {adjusted_rand_score(ct, a.obs["leiden_bbknn"]):.3f}')

# the consequence the Skill warns about: no embedding to score or to hand downstream
print('\nCan the Skill\'s own evaluation recipe (silhouette on the corrected embedding) be run?')
try:
    silhouette_score(a.obsm['X_bbknn'], bt)
except KeyError as e:
    print(f'  no: KeyError {e} - there is no corrected embedding, exactly as the Skill says.')
print('  the graph-level substitute is a kNN batch-mixing score; computed here from obsp:')
conn = a.obsp['connectivities']
same = []
bi = pd.Categorical(bt).codes
for i in range(0, a.n_obs, 7):     # every 7th cell, ~860 cells
    nb = conn[i].indices
    if len(nb):
        same.append(float((bi[nb] == bi[i]).mean()))
print(f'  mean fraction of graph neighbours from the SAME batch (BBKNN): {np.mean(same):.3f} '
      f'(0.50 = perfectly mixed for two equal batches)')

# compare with the uncorrected graph
b = sc.read_h5ad(R + '/input1_harmony.h5ad')
sc.pp.neighbors(b, use_rep='X_pca', random_state=0)
conn2 = b.obsp['connectivities']
same2 = []
for i in range(0, b.n_obs, 7):
    nb = conn2[i].indices
    if len(nb):
        same2.append(float((bi[nb] == bi[i]).mean()))
print(f'  same fraction on the UNCORRECTED graph:                       {np.mean(same2):.3f}')
sc.tl.leiden(b, key_added='leiden_unc', flavor='igraph', n_iterations=2, directed=False,
             random_state=0)
print(f'  uncorrected Leiden ARI vs true cell type: {adjusted_rand_score(ct, b.obs["leiden_unc"]):.3f}')

# --- Scanorama, which the Skill says DOES produce corrected counts that must not feed DE ---
c = sc.read_h5ad(R + '/input1_harmony.h5ad')
t0 = time.time()
try:
    sce.pp.scanorama_integrate(c, key='batch')
except ValueError as e:
    print(f'\nscanorama_integrate raised: {e}  -- undocumented precondition: the object must be '
          f'sorted by batch. The Skill gives Scanorama a table row and no code, so this is not '
          f'a broken snippet, but it is a gotcha it does not name.')
    c = c[np.argsort(pd.Categorical(c.obs['batch']).codes, kind='stable')].copy()
    sce.pp.scanorama_integrate(c, key='batch')
ct2, bt2 = c.obs['cell_type'].values, c.obs['batch'].values
print(f'\nscanorama_integrate ran in {time.time()-t0:.1f} s; obsm: '
      f'{[k for k in c.obsm if "scanorama" in k.lower()]}')
k = [x for x in c.obsm if 'scanorama' in x.lower()][0]
print(f'  {k}: batch ASW {silhouette_score(c.obsm[k], bt2, random_state=0):+.4f} | '
      f'cell-type ASW {silhouette_score(c.obsm[k], ct2, random_state=0):+.4f}')
print('DONE')
