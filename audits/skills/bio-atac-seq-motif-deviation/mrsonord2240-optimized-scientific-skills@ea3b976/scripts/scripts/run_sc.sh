# Usage: run_sc.sh <script.R> <tag> [SIGNAC_LIB]
source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export R_USER_CACHE_DIR=$MD/cache/Rcache
RR=/mnt/openscience/audits/bio-atac-seq-motif-deviation/reaudit-run
export SIGNAC_LIB=$3 OUTD=$RR/out_$2; mkdir -p $OUTD
cd $MD/work; micromamba run -n $ENVN Rscript $RR/scripts/$1 > $RR/logs/$2.log 2> $RR/logs/$2.err; echo exit $? >> $RR/logs/$2.log
