source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh; export R_USER_CACHE_DIR=$MD/cache/Rcache
cd $MD/work/archr
micromamba run -n $ENVN Rscript /mnt/openscience/audits/bio-atac-seq-motif-deviation/initial-audit-20260930/scripts/archr_na_diag.R > /mnt/openscience/audits/bio-atac-seq-motif-deviation/initial-audit-20260930/archr_na_diag.log 2>&1
echo done $?
