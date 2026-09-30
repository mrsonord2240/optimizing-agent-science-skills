source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export R_USER_CACHE_DIR=$MD/cache/Rcache; cd $MD/work
for s in "$@"; do micromamba run -n $ENVN Rscript $MD/evidence/scripts/$s.R > $MD/logs/$s.log 2> $MD/logs/$s.err; echo $s exit $?; tail -15 $MD/logs/$s.log; done
