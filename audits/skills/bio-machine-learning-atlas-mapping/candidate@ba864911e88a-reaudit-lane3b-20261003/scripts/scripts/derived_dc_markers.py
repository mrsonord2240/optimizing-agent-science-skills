import scanpy as sc
a=sc.read_h5ad(r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\derived\atlas-pair-holdout\reference_no_monocytes.h5ad")
a.X=a.layers['counts'].copy(); sc.pp.normalize_total(a,target_sum=1e4); sc.pp.log1p(a)
sc.tl.rank_genes_groups(a,'cell_type',method='wilcoxon')
d=sc.get.rank_genes_groups_df(a,group='DC'); d=d[d.logfoldchanges>0]
print("DC derived markers (no-Mono ref):", d.names.head(10).tolist())
print("cell_type counts:", a.obs.cell_type.value_counts().to_dict())
