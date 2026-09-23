"""Re-auditor new input: SKILL.md's 'Resource-Sensitivity Check' section was never executed by the
original audit (Inputs 1-7) or by the fixer. Run it unmodified on real PBMC data.
"""
from liana.method import cellphonedb
import scanpy as sc

adata = sc.read_h5ad('data/adata_annotated.h5ad')

for resource in ['consensus', 'cellphonedb', 'cellchatdb']:
    cellphonedb(adata, groupby='cell_type', resource_name=resource,
                expr_prop=0.1, use_raw=False, key_added=f'cpdb_{resource}', verbose=False)

import pandas as pd
tops = {}
for resource in ['consensus', 'cellphonedb', 'cellchatdb']:
    res = adata.uns[f'cpdb_{resource}']
    print(resource, 'n_pairs', len(res), 'columns', list(res.columns))
    sig = res[res['cellphone_pvals'] < 0.05]
    top = set(sig.apply(lambda r: (r['source'], r['target'], r['ligand_complex'], r['receptor_complex']), axis=1))
    tops[resource] = top
    print(resource, 'n_significant', len(top))

survive_all3 = tops['consensus'] & tops['cellphonedb'] & tops['cellchatdb']
print('SURVIVE_ALL_3_RESOURCES', len(survive_all3))
print('sample surviving pairs:', list(survive_all3)[:10])
