"""Re-auditor regression: SKILL.md 'Consensus Inference' block, unmodified except file path.
Reuses the real, CellTypist-annotated PBMC 1k v3 data produced by the original audit's own
01_annotate_pbmc.py (data/adata_annotated.h5ad) -- annotation itself is not in dispute, only
the cell-communication Skill's own code blocks are being re-verified here.
"""
import liana as li
import scanpy as sc

adata = sc.read_h5ad('data/adata_annotated.h5ad')

li.mt.rank_aggregate(adata, groupby='cell_type', resource_name='consensus',
                     expr_prop=0.1, use_raw=False, n_perms=1000, verbose=True)

res = adata.uns['liana_res']
robust = res[(res['specificity_rank'] < 0.05) & (res['magnitude_rank'] < 0.05)]

print('TOTAL_PAIRS', len(res))
print('ROBUST_PAIRS', len(robust))
print('COLUMNS', list(res.columns))
print(robust.sort_values('magnitude_rank').head(10)[['source','target','ligand_complex','receptor_complex','magnitude_rank','specificity_rank']].to_string())

res.to_csv('run/reaudit_liana_all.csv', index=False)
robust.to_csv('run/reaudit_liana_robust.csv', index=False)
