# Failure guard: depth.tsv missing one sample must stop early with stopifnot; plus depth = colSums(counts) misuse effect
source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export R_USER_CACHE_DIR=$MD/cache/Rcache
RR=/mnt/openscience/audits/bio-atac-seq-motif-deviation/reaudit-run
R=$RR/guard_missing; rm -rf $R; mkdir -p $R; cd $R
cp $MD/work/peaks.bed $MD/work/counts.tsv .; head -6 $RR/inputs/depth.tsv > depth.tsv   # drops K562_rep3
cp $SKILL/scripts/chromvar_bulk_analysis.R s.R
micromamba run -n $ENVN Rscript s.R > run.log 2> run.err; echo exit $? > exit.txt
ls > files.txt
