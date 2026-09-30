# Run the Skill's bulk script UNMODIFIED on the ENCODE GM12878 vs K562 chr1 slice
source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export R_USER_CACHE_DIR=$MD/cache/Rcache
R=$MD/work/run_bulk; rm -rf $R; mkdir -p $R; cd $R
cp $MD/work/peaks.bed $MD/work/counts.tsv .
/usr/bin/time -v micromamba run -n $ENVN Rscript $SKILL/scripts/chromvar_bulk_analysis.R > run.log 2> run.err; echo exit $?
tail -40 run.log; tail -15 run.err | head -8; ls -la
