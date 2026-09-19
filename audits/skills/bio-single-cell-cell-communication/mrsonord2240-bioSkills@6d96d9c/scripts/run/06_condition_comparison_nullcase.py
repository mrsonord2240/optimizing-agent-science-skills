"""Re-auditor's own Condition Comparison test: a NULL-case split, not the fixer's arbitrary 50/50.
The real PBMC 1k v3 data has no genuine experimental conditions (single sample). Rather than
reuse the fixer's synthetic 50/50 split (which cannot show whether SKILL.md's new section actually
protects against spurious differences), stratify a random split BY cell_type so per-type
composition is preserved and there is, by construction, NO true biological difference between
'conditionA' and 'conditionB' -- only sampling noise and the halved per-condition cell count.
If the section's gained/lost reporting is sound, a null split should yield a SMALL gained/lost
set relative to the shared robust set. A large gained/lost set under a null split would mean the
new section is not actually protecting against the instability it claims to guard against.
"""
import numpy as np
import pandas as pd
import liana as li
import scanpy as sc

rng = np.random.default_rng(20260919)  # different seed than the fixer's synthetic split
adata_full = sc.read_h5ad('data/adata_annotated.h5ad')

# Stratified random assignment: within each cell_type, shuffle and split ~50/50.
assign = pd.Series(index=adata_full.obs_names, dtype=object)
for ct, idx in adata_full.obs.groupby('cell_type').groups.items():
    idx = list(idx)
    rng.shuffle(idx)
    half = len(idx) // 2
    for i in idx[:half]:
        assign[i] = 'conditionA'
    for i in idx[half:]:
        assign[i] = 'conditionB'
adata_full.obs['condition'] = assign

print('Per-condition counts:')
print(adata_full.obs['condition'].value_counts())
print('Per-condition per-cell-type counts (should be ~balanced by construction):')
print(pd.crosstab(adata_full.obs['cell_type'], adata_full.obs['condition']))

conditions = {'conditionA': adata_full[adata_full.obs['condition'] == 'conditionA'].copy(),
              'conditionB': adata_full[adata_full.obs['condition'] == 'conditionB'].copy()}

robust = {}
for name, ad_ in conditions.items():
    li.mt.rank_aggregate(ad_, groupby='cell_type', resource_name='consensus',
                         expr_prop=0.1, use_raw=False, n_perms=1000, verbose=False)
    res = ad_.uns['liana_res']
    sig = res[(res['specificity_rank'] < 0.05) & (res['magnitude_rank'] < 0.05)]
    robust[name] = set(sig.apply(lambda r: (r['source'], r['target'], r['ligand_complex'], r['receptor_complex']), axis=1))
    print(name, 'n_cells', ad_.n_obs, 'robust_pairs', len(robust[name]))

gained = robust['conditionB'] - robust['conditionA']
lost = robust['conditionA'] - robust['conditionB']
shared = robust['conditionA'] & robust['conditionB']

print('NULL_CASE_GAINED', len(gained))
print('NULL_CASE_LOST', len(lost))
print('NULL_CASE_SHARED', len(shared))
print('NULL_CASE_UNION', len(robust['conditionA'] | robust['conditionB']))
frac_unstable = (len(gained) + len(lost)) / max(1, len(robust['conditionA'] | robust['conditionB']))
print('FRACTION_OF_UNION_THAT_IS_GAINED_OR_LOST (should be small if the section is sound):', round(frac_unstable, 3))
