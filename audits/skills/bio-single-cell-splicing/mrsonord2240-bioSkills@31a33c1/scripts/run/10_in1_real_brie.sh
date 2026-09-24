#!/bin/bash
# INPUT 1 (real data): run SKILL.md blocks S05 (brie-count + brie-quant) and S06 (python readout) LITERALLY on the real Smart-seq2 E6.5 130 cells.
# Only staging is done here: sample_list.tsv (absolute BAM paths), splicing_events.gff3 (BRIE tutorial 50-event file), cell_metadata.tsv (random 0/1 + z-scored log depth).
source /mnt/openscience/audit-envs/alternative-splicing/wsl_env.sh
R=/mnt/openscience/audits/bio-single-cell-splicing/run
S=$ASDATA/singlecell
W=$R/out/in1; rm -rf $W; mkdir -p $W; cd $W
awk -v d=$S '{sub(/^\.\//,d"/",$1); print $1"\t"$2}' $S/cell_table.tsv > sample_list.tsv
head -2 sample_list.tsv
cp $S/mouse_SE.lenient_50events.gff3 splicing_events.gff3
# S05 part 1 (count) -- literal block, lines up to the brie-quant call
sed -n '1,/^brie-quant/p' $R/blocks/S05_bash.sh | sed '$d' > s05_count.sh
bash s05_count.sh 2>&1 | tr '\r' '\n' | grep -v 'cells done' | tail -4
ls -la brie_counts
asenv as-sc python - <<'PY'
import anndata as ad, numpy as np, pandas as pd
a=ad.read_h5ad('brie_counts/brie_count.h5ad'); print(a); print(list(a.layers))
rng=np.random.default_rng(1)
tot=np.asarray(a.layers['isoform1'].sum(1)).ravel()+np.asarray(a.layers['isoform2'].sum(1)).ravel()
df=pd.DataFrame({'cell':a.obs_names,'rand_group':rng.integers(0,2,a.n_obs),'log_depth':np.log1p(tot)}).set_index('cell')
df['log_depth']=(df.log_depth-df.log_depth.mean())/df.log_depth.std()
df.to_csv('cell_metadata.tsv',sep='\t'); print(df.head(3))
PY
# S05 part 2 (quant): the whole literal block again (count + quant), as a user would paste it -> also proves the block end to end
bash $R/blocks/S05_bash.sh > s05_full.log 2>&1
tr '\r' '\n' < s05_full.log | grep -E 'Filtered|Traceback|Error|BRIE2|genes done' | tail -8
ls -la brie_quant.h5ad
# S06 literal python readout
asenv as-sc python $R/blocks/S06_python.py
asenv as-sc python - <<'PY'
import scanpy as sc, pandas as pd, numpy as np
a=sc.read_h5ad('brie_quant.h5ad'); print(a); print('varm keys',list(a.varm.keys()),'layers',list(a.layers)); print('Xc_ids', a.uns.get('Xc_ids'))
for k in ['ELBO_gain','pval','fdr','cell_coeff']: print(k, a.varm[k].shape)
assert a.varm['fdr'].shape==(a.n_vars,2), a.varm['fdr'].shape
assert a.layers['Psi'].shape==(130,a.n_vars)
assert {'Psi','Psi_95CI','Z_std'} <= set(a.layers)
print('ASSERT OK: varm keys/layers as SKILL.md states; n events kept', a.n_vars, 'of 50')
PY
