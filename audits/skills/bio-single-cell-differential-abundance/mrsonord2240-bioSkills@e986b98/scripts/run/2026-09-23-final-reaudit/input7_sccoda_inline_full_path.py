"""Input 7 (Adversarial): exact repaired scCODA block, including default HMC draws."""
import pandas as pd
import tensorflow as tf
from sccoda.util import cell_composition_data as dat
from sccoda.util import comp_ana as mod

root = 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
cells = pd.read_csv(root + '/truth_cells.csv')
cells = cells[~cells.true_doublet.astype(bool) & ~cells.true_low_quality.astype(bool)]
sample_sheet = pd.read_csv(root + '/sample_sheet.csv').set_index('sample')
cells['condition'] = cells['sample'].map(sample_sheet['condition'])
cells['cell_type'] = cells['true_cell_type']
adata = type('AdataHolder', (), {'obs': cells})()

# --- exact repaired SKILL.md inline block ---
counts = pd.crosstab(adata.obs['sample'], adata.obs['true_cell_type']).reset_index()
meta = adata.obs[['sample', 'condition']].drop_duplicates()
counts = counts.merge(meta, on='sample')

data = dat.from_pandas(counts, covariate_columns=['sample', 'condition'])
tf.random.set_seed(42)
model = mod.CompositionalAnalysis(data, formula='condition', reference_cell_type='automatic')
result = model.sample_hmc()
result.set_fdr(est_fdr=0.1)
result.summary()
effects = result.credible_effects()
print(effects)
assert len(counts) == 8
assert bool(effects.to_numpy().any())
print('PASS_SCCODA_INLINE_FULL_PATH samples=', len(counts), ' reference=', model.reference_cell_type, sep='')
