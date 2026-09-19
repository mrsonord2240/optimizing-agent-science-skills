import pertpy as pt
mdata = pt.dt.papalexi_2021()
for k in mdata.mod:
    print('===', k, mdata.mod[k].shape)
    print(list(mdata.mod[k].obs.columns))
print()
print('mdata.obs columns:')
print(list(mdata.obs.columns))
if 'perturbation' in mdata.obs.columns:
    print(mdata.obs['perturbation'].value_counts().head(10))
else:
    print('no perturbation col in mdata.obs')
if 'gene_target' in mdata.obs.columns:
    print(mdata.obs['gene_target'].value_counts().head(10))
else:
    print('no gene_target col in mdata.obs')
