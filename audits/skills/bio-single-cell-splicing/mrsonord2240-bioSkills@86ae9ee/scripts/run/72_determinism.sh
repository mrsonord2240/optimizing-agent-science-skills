#!/bin/bash
# T3 determinism: rerun the S05 brie-quant step twice on the planted v2 counts; compare significant set, fdr and per-cell Psi.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run; W=$R/out/in2_planted; cd $W
for k in 1 2; do brie-quant -i brie_counts/brie_count.h5ad -c cell_metadata.tsv -o det$k.h5ad --interceptMode gene --LRTindex All --testBase null --MCsize 3 -p 16 > det$k.log 2>&1; done
asenv as-sc python - <<'PY'
import scanpy as sc, numpy as np
a, b = sc.read_h5ad('det1.h5ad'), sc.read_h5ad('det2.h5ad')
sa, sb = set(a.var_names[a.varm['fdr'][:, 0] < .05]), set(b.var_names[b.varm['fdr'][:, 0] < .05])
print('determinism: significant sets', len(sa), len(sb), 'identical:', sa == sb, '; max |fdr diff|', np.abs(a.varm['fdr'] - b.varm['fdr']).max().round(4), '; max |Psi diff|', np.abs(a.layers['Psi'] - b.layers['Psi']).max().round(4), '; mean |Psi diff|', np.abs(a.layers['Psi'] - b.layers['Psi']).mean().round(5))
PY
rm -f det1.h5ad det2.h5ad
