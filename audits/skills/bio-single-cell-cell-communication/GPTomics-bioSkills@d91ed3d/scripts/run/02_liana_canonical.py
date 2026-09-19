\
# Input 1 (Canonical): "Rank ligand-receptor interactions between my annotated PBMC cell types
# with a consensus method." Follows SKILL.md 'Consensus Inference (Default)' code block verbatim,
# adapted only for our file path and groupby column name.
import scanpy as sc
import liana as li
import pandas as pd

adata = sc.read_h5ad(r"F:\OpenScience\audits\bio-single-cell-cell-communication\data\adata_annotated.h5ad")
print("cell_type counts:\n", adata.obs["majority_voting"].value_counts())

# expr_prop=0.1 drops pairs expressed in <10% of a cluster (sparse-noise floor)
# n_perms=1000 builds the specificity null; use_raw=False uses log-normalized .X
li.mt.rank_aggregate(adata, groupby='majority_voting', resource_name='consensus',
                     expr_prop=0.1, use_raw=False, n_perms=1000, verbose=True)

res = adata.uns['liana_res']
print("Total interactions scored:", len(res))
print(res.columns.tolist())

# rank_aggregate yields magnitude_rank and specificity_rank (NOT a single 'liana_rank')
robust = res[(res['specificity_rank'] < 0.05) & (res['magnitude_rank'] < 0.05)]
print("Robust interactions (both ranks < 0.05):", len(robust))
print(robust[['source', 'target', 'ligand_complex', 'receptor_complex',
              'magnitude_rank', 'specificity_rank']].sort_values('magnitude_rank').head(30).to_string())

robust.to_csv(r"F:\OpenScience\audits\bio-single-cell-cell-communication\run\out_liana_robust.csv", index=False)
res.to_csv(r"F:\OpenScience\audits\bio-single-cell-cell-communication\run\out_liana_all.csv", index=False)

# check known immune biology: does Classical monocytes -> T cell / NK antigen presentation
# or cytokine signaling surface? Check for HLA-* / B2M / CD74 (APC) and IL/TNF family pairs.
mono_source = robust[robust['source'].str.contains('monocyte', case=False)]
print("\nInteractions with a monocyte source (n={}):".format(len(mono_source)))
print(mono_source[['source', 'target', 'ligand_complex', 'receptor_complex']].head(20).to_string())
