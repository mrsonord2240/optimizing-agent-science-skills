"""Input 1 (Canonical) - bio-single-cell-cell-annotation
CellTypist exactly as SKILL.md:61-77: restore raw counts, CP10K + log1p, annotate with
majority_voting, keep conf_score for rejection. Scored against the SYNTHETIC ground-truth
cell types. Also tests the Skill's headline silent-failure claim (SKILL.md:50, :165) by
running the same model on non-CP10K input.
"""
import os
os.environ.setdefault('CELLTYPIST_FOLDER',
                      r'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/celltypist')
import scanpy as sc
import celltypist
from celltypist import models
import numpy as np
import pandas as pd

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
OUT = r'F:/OpenScience/audits/bio-single-cell-cell-annotation/run'
print('celltypist', celltypist.__version__)

a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_cell_type'] = tc['true_cell_type'].values
a = a[(~tc['true_doublet'].astype(bool) & ~tc['true_low_quality'].astype(bool)).values].copy()
a.layers['counts'] = a.X.copy()
print(f'{a.n_obs} cells; var_names look like: {list(a.var_names[:3])}')

# cluster first, because majority_voting needs an over-clustering
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')
sc.tl.pca(a, n_comps=50, mask_var='highly_variable', random_state=0)
sc.pp.neighbors(a, random_state=0)
sc.tl.leiden(a, resolution=1.0, flavor='igraph', n_iterations=2, directed=False, random_state=0)
print(f'{a.obs["leiden"].nunique()} Leiden clusters for majority voting')

# --- SKILL.md:66-77, verbatim ---
b = a.copy()
b.X = b.layers['counts'].copy()
sc.pp.normalize_total(b, target_sum=1e4)
sc.pp.log1p(b)
m = models.Model.load(model='Immune_All_Low.pkl')
pred = celltypist.annotate(b, model='Immune_All_Low.pkl', majority_voting=True,
                           over_clustering='leiden')
b = pred.to_adata()
b.obs['cell_type'] = b.obs['majority_voting']
b.obs['uncertain'] = b.obs['conf_score'] < 0.5
print(f'\nCORRECT input (CP10K log1p): {b.obs["majority_voting"].nunique()} distinct labels, '
      f'{int(b.obs["uncertain"].sum())} cells below conf_score 0.5 '
      f'({100*b.obs["uncertain"].mean():.1f}%)')
print(b.obs['majority_voting'].value_counts().head(10).to_string())

# coarse lineage mapping so the automated labels can be scored against the truth
LIN = {'CD4 T cells': 'T', 'CD8 T cells': 'T', 'NK cells': 'NK', 'B cells': 'B',
       'CD14+ Monocytes': 'Mono', 'FCGR3A+ Monocytes': 'Mono', 'Dendritic cells': 'DC',
       'Megakaryocytes': 'Mk'}


def lineage(lbl):
    s = str(lbl).lower()
    if 'megakaryo' in s or 'platelet' in s: return 'Mk'
    if 'nk' in s and 'cell' in s: return 'NK'
    if 'ilc' in s: return 'NK'
    if 'dendritic' in s or s.startswith('dc') or 'pdc' in s: return 'DC'
    if 'monocyt' in s or 'macrophage' in s: return 'Mono'
    if ' b cell' in s or s.endswith('b cells') or 'plasma' in s or 'germinal' in s or \
       s.startswith('naive b') or s.startswith('memory b') or 'b cells' in s: return 'B'
    if 't cell' in s or 'tcm' in s or 'tem' in s or 'treg' in s or 'mait' in s or \
       'helper' in s or 'cytotoxic' in s or 'thymocyte' in s: return 'T'
    return 'other:' + str(lbl)


true_lin = pd.Series(a.obs['true_cell_type'].map(LIN).values, index=a.obs_names)
for col, nm in [('predicted_labels', 'per-cell'), ('majority_voting', 'majority-voted')]:
    pl = pd.Series([lineage(x) for x in b.obs[col]], index=b.obs_names)
    acc = float((pl.values == true_lin.values).mean())
    print(f'  {nm} lineage accuracy vs truth: {acc:.3f}')
    if nm == 'majority-voted':
        print(pd.crosstab(true_lin.values, pl.values).to_string())

# --- the silent-failure claim: same model, wrong input ---
print('\nSILENT-FAILURE TEST (SKILL.md:50 / Common Errors row 2):')
variants = {
    'CP10K log1p (correct)': None,
    'raw counts, no normalization': 'raw',
    'log1p of raw counts, no CP10K': 'log_only',
    'median-normalized log1p (scanpy default target_sum=None)': 'median',
}
for nm, kind in variants.items():
    c = a.copy()
    c.X = c.layers['counts'].copy()
    if kind is None:
        sc.pp.normalize_total(c, target_sum=1e4); sc.pp.log1p(c)
    elif kind == 'log_only':
        sc.pp.log1p(c)
    elif kind == 'median':
        sc.pp.normalize_total(c); sc.pp.log1p(c)
    try:
        p = celltypist.annotate(c, model='Immune_All_Low.pkl', majority_voting=False)
    except Exception as e:
        print(f'  {nm:58s} ERROR RAISED: {type(e).__name__}: {str(e)[:110]}')
        continue
    pl = pd.Series([lineage(x) for x in p.predicted_labels['predicted_labels']],
                   index=c.obs_names)
    acc = float((pl.values == true_lin.values).mean())
    conf = float(p.probability_matrix.max(axis=1).mean())
    print(f'  {nm:58s} lineage accuracy {acc:.3f}  mean max-probability {conf:.3f}  '
          f'ERROR RAISED: no')
b.write_h5ad(OUT + '/input1_celltypist.h5ad')
print('DONE')
