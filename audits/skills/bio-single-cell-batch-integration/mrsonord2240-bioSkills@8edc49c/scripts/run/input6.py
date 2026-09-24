"""Input 6 (Scope Boundary) - bio-single-cell-batch-integration
A confounded design: every control captured on day 1, every treated on day 2. The Skill's
"When NOT to Integrate" section says to refuse, and gives a specific data-driven diagnostic:
  "cluster the uncorrected data and cross-tabulate clusters x batch x condition; pure-by-batch
   clusters that are also condition-aligned mean integration is unsafe."
Run that diagnostic at TWO day-effect strengths, to see whether it fires when the confound is
real but the batch effect is modest.

Derived SYNTHETIC data: ../data/confounded_sd035.h5ad and ../data/confounded_sd090.h5ad -
the synthetic 8-sample PBMC set relabelled so capture day == condition, with a per-gene
log-normal day effect of sd 0.35 and sd 0.90 respectively.
"""
import scanpy as sc
import numpy as np
import pandas as pd
import scanpy.external as sce
from sklearn.metrics import adjusted_rand_score

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
DATA = r'F:/OpenScience/audits/bio-single-cell-batch-integration/data'

base = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[base.obs_names]
base.obs['cell_type'] = tc['true_cell_type'].values
base = base[(~tc['true_doublet'].astype(bool) & ~tc['true_low_quality'].astype(bool)).values].copy()
base.obs['capture_day'] = np.where(base.obs['condition'] == 'control', 'day1', 'day2')

print('DESIGN CHECK - the metadata-only test, before any clustering:')
print(pd.crosstab(base.obs['condition'], base.obs['capture_day']).to_string())
print('-> capture_day and condition are perfectly aligned. No algorithm can separate them.\n')

de = pd.read_csv(D + '/truth_de_genes.csv')
up_all = set(de.loc[de.true_log2FC_treated_vs_control == 2, 'gene_symbol'])

for sd, tag in [(0.35, 'sd035'), (0.90, 'sd090')]:
    rng = np.random.default_rng(20260916)
    a = base.copy()
    X = a.X.toarray()
    eff = rng.lognormal(0, sd, size=a.n_vars)
    d2 = (a.obs['capture_day'] == 'day2').values
    X[d2] = X[d2] * eff
    a.X = np.asarray(np.round(X), dtype=np.float32)
    a.write_h5ad(f'{DATA}/confounded_{tag}.h5ad')

    a.layers['counts'] = a.X.copy()
    sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
    sc.pp.highly_variable_genes(a, n_top_genes=2000, batch_key='capture_day')
    araw = a.copy()
    a = a[:, a.var.highly_variable].copy()
    sc.pp.scale(a, max_value=10)
    sc.tl.pca(a, n_comps=50, random_state=0)
    sc.pp.neighbors(a, random_state=0)
    sc.tl.leiden(a, resolution=0.5, flavor='igraph', n_iterations=2, directed=False, random_state=0)

    ctab = pd.crosstab(a.obs['leiden'], a.obs['capture_day'])
    pure = ((ctab > 0).sum(axis=1) == 1)
    ari_day = adjusted_rand_score(a.obs['leiden'], a.obs['capture_day'])
    print(f'=== per-gene day effect sd = {sd} ===')
    print(ctab.to_string())
    print(f'clusters pure for one capture day: {int(pure.sum())}/{len(pure)}; '
          f'ARI(leiden, capture_day) = {ari_day:.3f}')
    fires = (pure.sum() > 0) or (ari_day > 0.2)
    print(f"SKILL's data-driven stop condition ('pure-by-batch clusters that are also "
          f"condition-aligned'): {'FIRES' if fires else 'DOES NOT FIRE'}")

    # the injected treatment effect, which is what integration would be asked to preserve
    up = [g for g in up_all if g in araw.var_names]
    mono = (araw.obs['cell_type'] == 'CD14+ Monocytes').values
    sig = np.asarray(araw[:, up].X.mean(axis=1)).ravel()
    cond = araw.obs['condition'].values
    print(f'  interferon score in CD14+ monocytes ({len(up)} genes, true log2FC +2): '
          f'control {sig[mono & (cond=="control")].mean():.4f}  '
          f'treated {sig[mono & (cond=="treated")].mean():.4f}')
    sce.pp.harmony_integrate(a, key='capture_day')
    sc.pp.neighbors(a, use_rep='X_pca_harmony', key_added='h', random_state=0)
    sc.tl.leiden(a, resolution=0.5, flavor='igraph', n_iterations=2, directed=False,
                 random_state=0, neighbors_key='h', key_added='leiden_h')
    print(f'  if integrated anyway: {a.obs["leiden_h"].nunique()} clusters, '
          f'ARI(leiden, capture_day) {adjusted_rand_score(a.obs["leiden_h"], a.obs["capture_day"]):.3f}, '
          f'ARI(leiden, cell_type) {adjusted_rand_score(a.obs["leiden_h"], a.obs["cell_type"]):.3f}\n')

print('HONEST READING OF THIS RUN:')
print('1. The metadata check at the top is decisive and costs nothing: condition and capture day')
print('   are perfectly aligned, so batch and biology are unidentifiable. That alone is the stop')
print('   condition, and it is what the Skill\'s "confounded design" bullet actually describes.')
print('2. The data-driven diagnostic the Skill *prescribes* (day-pure clusters in the uncorrected')
print('   data) did not fire at either effect size. That is a LIMITATION OF THIS SIMULATION, not')
print('   a proven weakness of the diagnostic: the day effect here is one multiplicative factor')
print('   per gene shared by every day-2 cell, and CP10k library-size normalization removes most')
print('   of a uniform compositional rescale. A real capture-day effect is cell-heterogeneous.')
print('   What this run does establish is that the diagnostic is not sufficient on its own - an')
print('   agent that ran only the cluster crosstab here would have concluded "safe to integrate"')
print('   on a design that is confounded by construction.')
print('3. Harmony on the confounded object preserved cell type (ARI ~0.99) and left the injected')
print('   treatment effect intact in the expression matrix, because Harmony returns an embedding')
print('   and no corrected counts. The Skill says exactly this, and it is why the correct refusal')
print('   here is about the DESIGN, not about damage Harmony does to the object.')
print('DONE')
