"""
Input 4 (Variant B) -- "Run scVelo dynamical mode and check velocity
confidence first", on real pancreatic endocrinogenesis data
(scv.datasets.pancreas(), Bergen et al. 2020's own real tutorial dataset,
3696 cells with real spliced/unspliced counts).

Ground truth: known real differentiation order Ductal -> Ngn3 low EP ->
Ngn3 high EP -> Pre-endocrine -> {Alpha, Beta, Delta, Epsilon} (terminal
endocrine fates). latent_time should increase along this order; velocity
streams should point from Ductal toward the endocrine clusters.
"""
import scvelo as scv
import scanpy as sc
import numpy as np
import pandas as pd

scv.settings.verbosity = 2

# NOTE: SKILL.md's own bundled examples/scvelo_velocity.py calls
# `scv.read('velocyto_output.loom')`, but installed scvelo 0.3.4 (the
# exact version the file declares compatibility with, "scVelo 0.3+") has
# no `scv.read` attribute at all -- see finding recorded separately.
# Using the correct current loader here instead.
adata = sc.read_h5ad('../data/pancreas_raw.h5ad')
print(adata)
print('spliced/unspliced layers present:', 'spliced' in adata.layers, 'unspliced' in adata.layers)

# --- SKILL.md "RNA Velocity" code block ---
# As written, `scv.pp.filter_and_normalize(adata, min_shared_counts=20,
# n_top_genes=2000)` (SKILL.md line 154, and examples/scvelo_velocity.py
# line 13, byte-identical call) raises
# `TypeError: normalize_per_cell() got an unexpected keyword argument
# 'n_top_genes'` against installed scvelo 0.3.4 -- the version the file
# itself declares compatibility with ("scVelo 0.3+"). filter_and_normalize
# in this version only wraps filter_genes + normalize_per_cell; HVG
# selection (n_top_genes) was removed from it, and scv.pp has no
# filter_genes_dispersion replacement either. Following SKILL.md's own
# recovery instruction ("introspect the installed package and adapt the
# example to match the actual API"): split the call and do HVG selection
# via scanpy instead. See finding recorded separately.
scv.pp.filter_and_normalize(adata, min_shared_counts=20)
adata.layers['normalized_X'] = adata.X.copy()
sc.pp.log1p(adata)  # HVG detection (default flavor) needs logged data; filter_and_normalize does not log-transform
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']].copy()
adata.X = adata.layers.pop('normalized_X')  # restore non-log X as scvelo's moments step expects
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

scv.tl.recover_dynamics(adata)          # dynamical only
scv.tl.velocity(adata, mode='dynamical')  # DEFAULT is 'stochastic'; SKILL.md says pass 'dynamical' explicitly
scv.tl.velocity_graph(adata)
scv.tl.velocity_confidence(adata)

order = ['Ductal', 'Ngn3 low EP', 'Ngn3 high EP', 'Pre-endocrine']
terminal = ['Alpha', 'Beta', 'Delta', 'Epsilon']

conf = adata.obs.groupby('clusters', observed=True)['velocity_confidence'].mean()
print('\nMean velocity_confidence per known cluster (progenitor -> terminal order):')
for c in order + terminal:
    if c in conf.index:
        print(f'  {c:16s} {conf[c]:.4f}')

scv.tl.latent_time(adata)
lt = adata.obs.groupby('clusters', observed=True)['latent_time'].mean()
print('\nMean scVelo latent_time per known cluster (should increase Ductal -> terminal):')
lt_order = [c for c in order + terminal if c in lt.index]
for c in lt_order:
    print(f'  {c:16s} {lt[c]:.4f}')
lt_vals = [lt[c] for c in lt_order]
# Ductal (start) should have low latent time; the four terminal fates should
# have higher latent time than Ductal (order among themselves is fate-specific,
# not strictly linear, since they are parallel terminal branches)
ductal_lt = lt.get('Ductal', np.nan)
terminal_lt_mean = np.mean([lt[c] for c in terminal if c in lt.index])
print(f'\nDuctal (start) latent_time: {ductal_lt:.4f}, mean terminal-fate latent_time: {terminal_lt_mean:.4f}')
print(f'ASSERTION latent_time_increases_from_progenitor_to_terminal: {ductal_lt < terminal_lt_mean}')

# progression through the committed pre-endocrine series should be monotone
pre_series = ['Ductal', 'Ngn3 low EP', 'Ngn3 high EP', 'Pre-endocrine']
pre_lt = [lt[c] for c in pre_series if c in lt.index]
monotone = all(pre_lt[i] <= pre_lt[i+1] for i in range(len(pre_lt)-1))
print(f'Latent time along committed series {pre_series}: {[round(v,4) for v in pre_lt]}')
print(f'ASSERTION monotone_along_committed_series: {monotone}')

print(f'\nOverall mean velocity_confidence: {adata.obs["velocity_confidence"].mean():.4f}')
adata.write('../data/pancreas_with_velocity.h5ad')
print('Done.')
