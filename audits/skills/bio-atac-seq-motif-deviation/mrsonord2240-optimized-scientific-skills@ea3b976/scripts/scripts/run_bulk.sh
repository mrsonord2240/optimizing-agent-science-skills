# Usage: run_bulk.sh <tag> [unseeded]   Runs the shipped bulk script from a clean dir; 'unseeded' = control copy with the set.seed line removed.
source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export R_USER_CACHE_DIR=$MD/cache/Rcache
RR=/mnt/openscience/audits/bio-atac-seq-motif-deviation/reaudit-run
R=$RR/bulk_$1; rm -rf $R; mkdir -p $R; cd $R
cp $MD/work/peaks.bed $MD/work/counts.tsv .
cp $RR/inputs/depth.tsv .
if [ "$2" = unseeded ]; then grep -v '^set.seed(2024)' $SKILL/scripts/chromvar_bulk_analysis.R > s.R; else cp $SKILL/scripts/chromvar_bulk_analysis.R s.R; fi
micromamba run -n $ENVN Rscript s.R > run.log 2> run.err; echo exit $? > exit.txt
sha256sum chromvar_*.csv > csv.sha256
