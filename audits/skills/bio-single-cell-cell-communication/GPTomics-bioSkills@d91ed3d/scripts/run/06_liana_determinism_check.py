\
# Determinism check for T3 (Skill Veto) / 8.4 Idempotency: run LIANA rank_aggregate twice on the
# same real annotated PBMC data with the exact SKILL.md-documented call (no seed override) and diff
# the robust-interaction set and the magnitude/specificity ranks.
import scanpy as sc
import liana as li
import pandas as pd

def run_once():
    adata = sc.read_h5ad(r"F:\OpenScience\audits\bio-single-cell-cell-communication\data\adata_annotated.h5ad")
    li.mt.rank_aggregate(adata, groupby='majority_voting', resource_name='consensus',
                         expr_prop=0.1, use_raw=False, n_perms=1000, verbose=False)
    return adata.uns['liana_res'].sort_values(['source', 'target', 'ligand_complex', 'receptor_complex']).reset_index(drop=True)

r1 = run_once()
r2 = run_once()

print("Run1 rows:", len(r1), "Run2 rows:", len(r2))
merged = r1.merge(r2, on=['source', 'target', 'ligand_complex', 'receptor_complex'], suffixes=('_1', '_2'))
print("Merged rows:", len(merged))
mag_diff = (merged['magnitude_rank_1'] - merged['magnitude_rank_2']).abs()
spec_diff = (merged['specificity_rank_1'] - merged['specificity_rank_2']).abs()
print("Max |magnitude_rank diff| across runs:", mag_diff.max())
print("Max |specificity_rank diff| across runs:", spec_diff.max())
print("Mean |magnitude_rank diff|:", mag_diff.mean())
print("Mean |specificity_rank diff|:", spec_diff.mean())

robust1 = set(zip(r1[(r1['specificity_rank'] < 0.05) & (r1['magnitude_rank'] < 0.05)]['source'],
                   r1[(r1['specificity_rank'] < 0.05) & (r1['magnitude_rank'] < 0.05)]['target'],
                   r1[(r1['specificity_rank'] < 0.05) & (r1['magnitude_rank'] < 0.05)]['ligand_complex'],
                   r1[(r1['specificity_rank'] < 0.05) & (r1['magnitude_rank'] < 0.05)]['receptor_complex']))
robust2 = set(zip(r2[(r2['specificity_rank'] < 0.05) & (r2['magnitude_rank'] < 0.05)]['source'],
                   r2[(r2['specificity_rank'] < 0.05) & (r2['magnitude_rank'] < 0.05)]['target'],
                   r2[(r2['specificity_rank'] < 0.05) & (r2['magnitude_rank'] < 0.05)]['ligand_complex'],
                   r2[(r2['specificity_rank'] < 0.05) & (r2['magnitude_rank'] < 0.05)]['receptor_complex']))
print("Robust set 1 size:", len(robust1), "Robust set 2 size:", len(robust2))
print("Identical robust sets:", robust1 == robust2)
print("Symmetric difference size:", len(robust1.symmetric_difference(robust2)))
