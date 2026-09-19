"""
Input 4 (Variant B) -- FINAL run. "Run scVelo dynamical mode and check
velocity confidence first" on real pancreatic endocrinogenesis data.

Environment findings (see eval report for full detail, each independently
reproduced with a full traceback):
  1. SKILL.md's own inline call `scv.pp.filter_and_normalize(adata,
     min_shared_counts=20, n_top_genes=2000)` (identical in bundled
     examples/scvelo_velocity.py line 13) TypeErrors against installed
     scvelo 0.3.4 -- n_top_genes was removed from that function. Worked
     around per the Skill's own "introspect and adapt" instruction using
     sc.pp.highly_variable_genes.
  2. mode='dynamical' (the mode SKILL.md explicitly tells the agent to
     pass) cannot run: scv.tl.recover_dynamics() crashes inside scvelo's
     own make_unique_list() due to a pandas-3.x incompatibility (unique()
     no longer accepts a plain list). Two workarounds tried, both fail
     identically -- this is not adaptable from the call site.
  3. mode='stochastic' (scvelo's own default) ALSO crashes: scv.tl.velocity
     -> compute_stochastic -> leastsq_generalized raises "ValueError:
     setting an array element with a sequence" from a numpy 2.x
     incompatibility in scvelo's internal least-squares fit.
  4. mode='deterministic' is the only one of the three that runs.

This run therefore uses mode='deterministic' (still one of the three
methods in SKILL.md's own RNA Velocity table) and substitutes
velocity_pseudotime (does not require recover_dynamics/latent_time) for
the ground-truth ordering check, since latent_time is unreachable here.
"""
import scvelo as scv
import scanpy as sc
import numpy as np

scv.settings.verbosity = 2

adata = sc.read_h5ad('../data/pancreas_raw.h5ad')

scv.pp.filter_and_normalize(adata, min_shared_counts=20)
adata.layers['normalized_X'] = adata.X.copy()
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']].copy()
adata.X = adata.layers.pop('normalized_X')
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)

scv.tl.velocity(adata, mode='deterministic')
# n_jobs=1 avoids scvelo's multiprocessing.Manager() path, which needs an
# `if __name__=='__main__':` guard to spawn on Windows -- unrelated to the
# Skill's own content, just a Windows script-vs-notebook execution detail.
scv.tl.velocity_graph(adata, n_jobs=1, show_progress_bar=False)
scv.tl.velocity_confidence(adata)
scv.tl.velocity_pseudotime(adata)

order = ['Ductal', 'Ngn3 low EP', 'Ngn3 high EP', 'Pre-endocrine']
terminal = ['Alpha', 'Beta', 'Delta', 'Epsilon']

conf = adata.obs.groupby('clusters', observed=True)['velocity_confidence'].mean()
print('\nMean velocity_confidence per known cluster (deterministic mode):')
for c in order + terminal:
    if c in conf.index:
        print(f'  {c:16s} {conf[c]:.4f}')
print(f'\nOverall mean velocity_confidence: {adata.obs["velocity_confidence"].mean():.4f}')

vpt = adata.obs.groupby('clusters', observed=True)['velocity_pseudotime'].mean()
print('\nMean velocity_pseudotime per known cluster (should increase Ductal -> terminal):')
for c in order + terminal:
    if c in vpt.index:
        print(f'  {c:16s} {vpt[c]:.4f}')

ductal_vpt = vpt.get('Ductal', np.nan)
terminal_vpt_mean = np.mean([vpt[c] for c in terminal if c in vpt.index])
print(f'\nDuctal (start) velocity_pseudotime: {ductal_vpt:.4f}, mean terminal-fate velocity_pseudotime: {terminal_vpt_mean:.4f}')
print(f'ASSERTION velocity_pseudotime_increases_from_progenitor_to_terminal: {ductal_vpt < terminal_vpt_mean}')

pre_series = ['Ductal', 'Ngn3 low EP', 'Ngn3 high EP', 'Pre-endocrine']
pre_vpt = [vpt[c] for c in pre_series if c in vpt.index]
monotone = all(pre_vpt[i] <= pre_vpt[i+1] for i in range(len(pre_vpt)-1))
print(f'velocity_pseudotime along committed series {pre_series}: {[round(v,4) for v in pre_vpt]}')
print(f'ASSERTION monotone_along_committed_series: {monotone}')

print('\nDone.')
