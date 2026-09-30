source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh; export R_USER_CACHE_DIR=$MD/cache/Rcache
micromamba run -n $ENVN Rscript /mnt/openscience/audits/bio-atac-seq-motif-deviation/initial-audit-20260930/scripts/introspect_chromvar.R
