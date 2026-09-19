"""
Input 2 (Variant A) -- "Give me fate probabilities at the branch point, not
hard branch labels" / "Compute differentiation potential (entropy) across
the manifold", following SKILL.md's "Fate Probabilities With Palantir" code
block, on the same real Paul15 myeloid/erythroid progenitor data (has a
genuine branch: MEP/GMP progenitors -> erythroid lineage vs. myeloid
lineage).

Ground truth check: entropy of the fate-probability vector should be high
near the MEP/GMP progenitor pool and fall toward 0 in mature, lineage-
committed cells (1Ery erythroid vs 16Neu/15Mo/11DC myeloid) -- this is
exactly what the Skill claims ("Entropy ... high near multipotent cells,
falling toward 0 as cells commit").
"""
import numpy as np
import pandas as pd
import scanpy as sc
import palantir

sc.settings.verbosity = 1

adata = sc.read_h5ad('../data/paul15_raw.h5ad')
adata.X = adata.X.astype('float64')
sc.pp.recipe_zheng17(adata)
sc.tl.pca(adata, svd_solver='arpack')
sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca')

# --- SKILL.md "Fate Probabilities With Palantir" block, run against real API ---
dm_res = palantir.utils.run_diffusion_maps(adata, n_components=5)
ms_data = palantir.utils.determine_multiscale_space(dm_res)
print('ms_data type:', type(ms_data))

mep_cells = adata.obs_names[adata.obs['paul15_clusters'] == '7MEP']
early_cell = mep_cells[0]
print('early_cell (real MEP progenitor cell id):', early_cell)

# SKILL.md passes ms_data (the DataFrame), not adata, as the first arg:
pr_res = palantir.core.run_palantir(ms_data, early_cell=early_cell, terminal_states=None, num_waypoints=1200)
print('pr_res type:', type(pr_res))
print('pr_res attributes:', [a for a in dir(pr_res) if not a.startswith('_')])

pt = pr_res.pseudotime
ent = pr_res.entropy
fate_probs = pr_res.branch_probs
print('\nFate probability matrix shape:', None if fate_probs is None else fate_probs.shape)
if fate_probs is not None:
    print('Terminal states auto-detected:', list(fate_probs.columns))

df = adata.obs[['paul15_clusters']].copy()
df['pseudotime'] = pt.values
df['entropy'] = ent.values

mep_entropy = df.loc[df['paul15_clusters'] == '7MEP', 'entropy'].mean()
mature_labels = ['1Ery', '16Neu', '15Mo', '11DC']
mature_present = [l for l in mature_labels if l in df['paul15_clusters'].unique()]
mature_entropy = df.loc[df['paul15_clusters'].isin(mature_present), 'entropy'].mean()
print(f'\nMean entropy in MEP progenitor pool: {mep_entropy:.4f}')
print(f'Mean entropy in mature/committed cells {mature_present}: {mature_entropy:.4f}')
print(f'ASSERTION entropy_falls_with_commitment (MEP entropy > mature entropy): {mep_entropy > mature_entropy}')

mep_pt = df.loc[df['paul15_clusters'] == '7MEP', 'pseudotime'].mean()
mature_pt = df.loc[df['paul15_clusters'].isin(mature_present), 'pseudotime'].mean()
print(f'\nMean Palantir pseudotime in MEP: {mep_pt:.4f}, in mature cells: {mature_pt:.4f}')
print(f'ASSERTION pseudotime_increases_toward_maturity: {mep_pt < mature_pt}')

print('\nDone.')
