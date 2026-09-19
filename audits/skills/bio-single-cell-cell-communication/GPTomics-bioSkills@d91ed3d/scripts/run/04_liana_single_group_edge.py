\
# Input 3 (Edge): "I only have one cluster in my data — can you find cell communication?"
# SKILL.md ("Consensus Inference (Default)") states: "CCC needs >=2 cell types in `groupby`;
# a single group yields only autocrine self-edges, not intercellular signaling."
# This tests whether that claim is empirically true: force groupby onto a constant column
# and check what LIANA actually returns.
import scanpy as sc
import liana as li

adata = sc.read_h5ad(r"F:\OpenScience\audits\bio-single-cell-cell-communication\data\adata_annotated.h5ad")
adata.obs['single_group'] = 'AllCells'

try:
    li.mt.rank_aggregate(adata, groupby='single_group', resource_name='consensus',
                         expr_prop=0.1, use_raw=False, n_perms=100, verbose=False)
    res = adata.uns['liana_res']
    print("Ran without error. Rows:", len(res))
    print("Unique (source, target) pairs:", res[['source', 'target']].drop_duplicates().to_string())
except Exception as e:
    print("EXCEPTION:", type(e).__name__, str(e))
