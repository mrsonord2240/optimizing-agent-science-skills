"""Input 2 (Variant A) - bio-single-cell-batch-integration
scVI / scANVI exactly as SKILL.md:99-117, including the Skill's specific API claim at
SKILL.md:119 that unlabeled_category is the SECOND POSITIONAL argument to
SCANVI.from_scvi_model, before labels_key. Checked against scvi-tools 1.5.1.
"""
import inspect
import scanpy as sc
import scvi
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score, adjusted_rand_score

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
OUT = r'F:/OpenScience/audits/bio-single-cell-batch-integration/run'
scvi.settings.seed = 20260916
print('scvi-tools', scvi.__version__)
print('SCANVI.from_scvi_model signature:', inspect.signature(scvi.model.SCANVI.from_scvi_model))

a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['cell_type'] = tc['true_cell_type'].values
a = a[(~tc['true_doublet'].astype(bool) & ~tc['true_low_quality'].astype(bool)).values].copy()

# --- SKILL.md:104-107 ---
a.layers['counts'] = a.X.copy()
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts',
                            batch_key='batch')
a = a[:, a.var.highly_variable].copy()

scvi.model.SCVI.setup_anndata(a, layer='counts', batch_key='batch')
model = scvi.model.SCVI(a, n_latent=10, gene_likelihood='zinb')
model.train(max_epochs=40, accelerator='cpu')
a.obsm['X_scVI'] = model.get_latent_representation()
print('X_scVI:', a.obsm['X_scVI'].shape)

ct, bt = a.obs['cell_type'].values, a.obs['batch'].values
for rep in ['X_scVI']:
    print(f'  {rep}: batch ASW {silhouette_score(a.obsm[rep], bt, random_state=0):+.4f} | '
          f'cell-type ASW {silhouette_score(a.obsm[rep], ct, random_state=0):+.4f}')
sc.pp.neighbors(a, use_rep='X_scVI', random_state=0)
sc.tl.leiden(a, flavor='igraph', n_iterations=2, directed=False, random_state=0)
print(f'  Leiden on X_scVI: {a.obs["leiden"].nunique()} clusters, '
      f'ARI vs true cell type {adjusted_rand_score(ct, a.obs["leiden"]):.3f}')

# --- scANVI: hide 60% of labels, as a real semi-supervised run would ---
rng = np.random.default_rng(20260916)
lab = a.obs['cell_type'].astype(str).values.copy()
hide = rng.random(len(lab)) < 0.6
lab[hide] = 'Unknown'
a.obs['cell_type_partial'] = pd.Categorical(lab)
print(f'\nscANVI with {int(hide.sum())}/{len(lab)} labels hidden')

# the Skill's exact call form: positional unlabeled_category, then labels_key
try:
    scanvi = scvi.model.SCANVI.from_scvi_model(model, 'Unknown', labels_key='cell_type_partial')
    print('SKILL.md:114 call form (positional "Unknown", then labels_key=): ACCEPTED')
except Exception as e:
    print('SKILL.md:114 call form FAILED:', type(e).__name__, str(e)[:250])
    scanvi = scvi.model.SCANVI.from_scvi_model(model, labels_key='cell_type_partial',
                                               unlabeled_category='Unknown')
    print('  recovered with keyword form unlabeled_category=')

scanvi.train(max_epochs=20, accelerator='cpu')
a.obs['scanvi_label'] = scanvi.predict()
a.obsm['X_scANVI'] = scanvi.get_latent_representation()
print(f'  X_scANVI: batch ASW {silhouette_score(a.obsm["X_scANVI"], bt, random_state=0):+.4f} | '
      f'cell-type ASW {silhouette_score(a.obsm["X_scANVI"], ct, random_state=0):+.4f}')
acc = float((a.obs['scanvi_label'].astype(str).values[hide] == ct[hide]).mean())
print(f'  scANVI predicted label accuracy on the {int(hide.sum())} HIDDEN cells: {acc:.3f}')
print('  per true type accuracy on hidden cells:')
print(pd.Series(a.obs['scanvi_label'].astype(str).values[hide] == ct[hide])
      .groupby(ct[hide]).mean().round(3).to_string())

a.write_h5ad(OUT + '/input2_scvi.h5ad')
print('DONE')
