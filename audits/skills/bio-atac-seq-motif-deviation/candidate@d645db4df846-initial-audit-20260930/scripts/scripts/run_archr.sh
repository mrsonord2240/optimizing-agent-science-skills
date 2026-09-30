source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
export R_USER_CACHE_DIR=$MD/cache/Rcache MACS2=/mnt/openscience/audit-envs/atac-seq/tools/bin/macs2
cd $MD/work; /usr/bin/time -v micromamba run -n $ENVN Rscript $MD/evidence/scripts/smoke_archr.R > $MD/logs/smoke_archr.log 2> $MD/logs/smoke_archr.err; echo exit $?
