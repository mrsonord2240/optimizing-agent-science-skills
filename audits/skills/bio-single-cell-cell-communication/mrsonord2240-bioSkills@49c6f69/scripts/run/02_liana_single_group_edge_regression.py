"""Re-auditor regression: single-group groupby edge case.
Verifies the fixer's P2 text fix -- SKILL.md now says a single group raises a ValueError, not
'yields only autocrine self-edges'. Confirm the actual exception on real data.
"""
import liana as li
import scanpy as sc

adata = sc.read_h5ad('data/adata_annotated.h5ad')
adata.obs['single_group'] = 'all_cells'

try:
    li.mt.rank_aggregate(adata, groupby='single_group', resource_name='consensus',
                         expr_prop=0.1, use_raw=False, n_perms=100, verbose=False)
    print('NO_ERROR_RAISED -- unexpected, would contradict corrected SKILL.md text')
    print(adata.uns['liana_res'].head())
except Exception as e:
    print('EXCEPTION_TYPE', type(e).__name__)
    print('EXCEPTION_MESSAGE', str(e))
