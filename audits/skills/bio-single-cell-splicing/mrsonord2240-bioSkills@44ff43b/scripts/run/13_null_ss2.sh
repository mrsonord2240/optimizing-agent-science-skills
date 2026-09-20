#!/bin/bash
# Input 2 null control: 100 all-null events, 80 cells, random group labels A/B. Any LRT hit is a false positive.
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run
cd $R; asenv as-core python 10_gen_planted_sc.py data/synth_ss2_null ss2 21 allnull
sed -i 's#data/synth_ss2_null/bams#bams#' data/synth_ss2_null/cell_table.tsv
D=$R/data/synth_ss2_null; O=$R/out/null_ss2; rm -rf $O; mkdir -p $O; cd $D
brie-count -a events.gff3 -S cell_table.tsv -o $O/counts -p 16 2>&1 | tr '\r' '\n' | grep -v "cells done" | tail -2
brie-quant -i $O/counts/brie_count.h5ad -c cellfeat.tsv -o $O/quant.h5ad --interceptMode gene --LRTindex All --testBase null --MCsize 3 --batchSize 1000000 -p 16 2>&1 | tr '\r' '\n' | grep -E "genes done|Traceback" | tail
asenv as-sc python - <<'PY'
import scanpy as sc, numpy as np, pandas as pd
R='/mnt/openscience/audits/bio-single-cell-splicing/run'
a=sc.read_h5ad(f'{R}/out/null_ss2/quant.h5ad')
p=a.varm['pval'][:,0]; f=a.varm['fdr'][:,0]; e=a.varm['ELBO_gain'][:,0]
print('NULL run: n events', len(p), ' raw p<0.05:', int((p<0.05).sum()), ' fdr<0.05:', int((f<0.05).sum()), ' ELBO_gain>3:', int((e>3).sum()), ' max ELBO', e.max().round(2))
PY
