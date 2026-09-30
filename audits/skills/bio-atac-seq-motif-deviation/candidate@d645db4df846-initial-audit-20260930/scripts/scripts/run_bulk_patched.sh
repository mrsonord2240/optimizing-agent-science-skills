# Same script + ONE evidence-side patch: add colData depth (filterSamples requirement). Skill bytes untouched.
source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export R_USER_CACHE_DIR=$MD/cache/Rcache
R=$MD/work/run_bulk_patched; rm -rf $R; mkdir -p $R; cd $R
cp $MD/work/peaks.bed $MD/work/counts.tsv .
python3 - <<'P'
import pandas as pd,os
md=os.environ['MD']
s=pd.read_csv(md+'/work/fc.txt.summary',sep='\t',index_col=0)
s.columns=['GM_rep1','GM_rep2','GM_rep3','K562_rep1','K562_rep2','K562_rep3']
s.sum().rename('depth').to_csv('depth.tsv',sep='\t')
src=open(os.environ['SKILL']+'/scripts/chromvar_bulk_analysis.R').read()
key="levels=c('control','treated'))\n"
assert key in src
src=src.replace(key,key+"colData(se)$depth <- read.delim('depth.tsv', row.names=1)[colnames(se),1]  # EVIDENCE PATCH\n",1)
open('chromvar_bulk_patched.R','w').write(src)
P
/usr/bin/time -v micromamba run -n $ENVN Rscript chromvar_bulk_patched.R > run.log 2> run.err; echo exit $?
tail -45 run.log; grep -E "Elapsed|Maximum res" run.err; head -15 run.err | grep -v "^\s"; ls -la
