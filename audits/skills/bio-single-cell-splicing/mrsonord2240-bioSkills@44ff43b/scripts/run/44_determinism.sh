#!/bin/bash
# T3 determinism: rerun the identical brie-quant command on the planted set; compare Psi / ELBO_gain / fdr with the first run. brie-quant has no --seed flag.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run; O=$R/out/planted_ss2; cd $R/data/synth_ss2
brie-quant -i $O/counts/brie_count.h5ad -c cellfeat.tsv -o $O/quant2.h5ad --interceptMode gene --LRTindex All --testBase null --MCsize 3 --batchSize 1000000 -p 16 > /dev/null 2>&1
asenv as-sc python - <<'PY'
import scanpy as sc, numpy as np
R='/mnt/openscience/audits/bio-single-cell-splicing/run/out/planted_ss2'
a=sc.read_h5ad(f'{R}/quant.h5ad'); b=sc.read_h5ad(f'{R}/quant2.h5ad')
print('same events:', list(a.var_names)==list(b.var_names))
pa,pb=a.layers['Psi'],b.layers['Psi']; print('max |Psi run1-run2|: %.4f  mean %.5f'%(np.abs(pa-pb).max(), np.abs(pa-pb).mean()))
ea,eb=a.varm['ELBO_gain'][:,0],b.varm['ELBO_gain'][:,0]; print('ELBO_gain corr %.5f  max abs diff %.3f'%(np.corrcoef(ea,eb)[0,1], np.abs(ea-eb).max()))
fa,fb=a.varm['fdr'][:,0]<.05,b.varm['fdr'][:,0]<.05; print('fdr<0.05 calls run1 %d run2 %d  identical set: %s'%(fa.sum(),fb.sum(),bool((fa==fb).all())))
PY
