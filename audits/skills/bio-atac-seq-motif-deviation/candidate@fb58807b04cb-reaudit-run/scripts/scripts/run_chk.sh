source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
S=/mnt/openscience/audits/bio-atac-seq-motif-deviation/reaudit-run/scripts
micromamba run -n $ENVN Rscript $S/chk_runchromvar.R
SIGNAC_LIB=$MD/rlib-signac1.16 micromamba run -n $ENVN Rscript $S/chk_runchromvar.R
