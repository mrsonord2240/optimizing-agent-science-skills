"""Input 1 (Canonical) - bio-single-cell-batch-integration
Harmony exactly as SKILL.md:73-90, then the evaluation the Skill prescribes at SKILL.md:150-160
(batch silhouette AND cell-type silhouette, read jointly), scored against the SYNTHETIC
ground-truth cell types. Also tests the Skill's theta warning by sweeping it.
"""
import scanpy as sc
import scanpy.external as sce
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, adjusted_rand_score

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
OUT = r'F:/OpenScience/audits/bio-single-cell-batch-integration/run'

a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['cell_type'] = tc['true_cell_type'].values
a = a[(~tc['true_doublet'].astype(bool) & ~tc['true_low_quality'].astype(bool)).values].copy()
a.layers['counts'] = a.X.copy()
print(f'{a.n_obs} cells, batches {a.obs["batch"].value_counts().to_dict()}, '
      f'{a.obs["cell_type"].nunique()} true cell types')
print('design check - condition x batch (the Skill says to do this BEFORE integrating):')
print(pd.crosstab(a.obs['condition'], a.obs['batch']).to_string())

# --- SKILL.md:77-84 preprocessing, verbatim ---
sc.pp.normalize_total(a, target_sum=1e4)
sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, batch_key='batch')
a.raw = a
a = a[:, a.var.highly_variable].copy()
sc.pp.scale(a, max_value=10)
sc.tl.pca(a, n_comps=50, random_state=0)

ct, bt = a.obs['cell_type'].values, a.obs['batch'].values


def score(rep, name):
    X = a.obsm[rep] if rep in a.obsm else a.obsm['X_pca']
    bs = silhouette_score(X, bt, random_state=0)
    cs = silhouette_score(X, ct, random_state=0)
    print(f'  {name:28s} batch ASW {bs:+.4f} (lower=mixed) | cell-type ASW {cs:+.4f} (higher=kept)')
    return bs, cs


print('\nUNCORRECTED (the Skill says to keep this for before/after):')
score('X_pca', 'X_pca')

# --- SKILL.md:86 : harmony_integrate ---
sce.pp.harmony_integrate(a, key='batch')
print('harmony key written:', [k for k in a.obsm if 'harmony' in k])
print('CORRECTED:')
score('X_pca_harmony', 'X_pca_harmony')

sc.pp.neighbors(a, use_rep='X_pca_harmony', random_state=0)
sc.tl.leiden(a, flavor='igraph', n_iterations=2, directed=False, random_state=0)
print(f'  Leiden on the corrected embedding: {a.obs["leiden"].nunique()} clusters, '
      f'ARI vs true cell type {adjusted_rand_score(ct, a.obs["leiden"]):.3f}')
sc.pp.neighbors(a, use_rep='X_pca', key_added='unc', random_state=0)
sc.tl.leiden(a, flavor='igraph', n_iterations=2, directed=False, random_state=0,
             neighbors_key='unc', key_added='leiden_unc')
print(f'  Leiden on the UNCORRECTED embedding: {a.obs["leiden_unc"].nunique()} clusters, '
      f'ARI vs true cell type {adjusted_rand_score(ct, a.obs["leiden_unc"]):.3f}')

# --- the Skill's theta warning: "larger theta over-corrects" ---
print('\ntheta sweep (SKILL.md Strength Parameters: "higher theta -> more aggressive mixing"):')
rows = []
rare = a.obs['cell_type'].value_counts().idxmin()
for th in [0.5, 2.0, 8.0]:
    b = a.copy()
    sce.pp.harmony_integrate(b, key='batch', theta=th, adjusted_basis=f'X_h{th}')
    bs = silhouette_score(b.obsm[f'X_h{th}'], bt, random_state=0)
    cs = silhouette_score(b.obsm[f'X_h{th}'], ct, random_state=0)
    # does the rarest type still separate?
    m = ct == rare
    rs = silhouette_score(b.obsm[f'X_h{th}'], m.astype(int), random_state=0)
    rows.append(dict(theta=th, batch_ASW=round(bs, 4), celltype_ASW=round(cs, 4),
                     rare_type_ASW=round(rs, 4)))
print(pd.DataFrame(rows).to_string(index=False))
print(f'  (rarest true type here is {rare}, n={int((ct==rare).sum())})')

a.write_h5ad(OUT + '/input1_harmony.h5ad')
print('DONE')
