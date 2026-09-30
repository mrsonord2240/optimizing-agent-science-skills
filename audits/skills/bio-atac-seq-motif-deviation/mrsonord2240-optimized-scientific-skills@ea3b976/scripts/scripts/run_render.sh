source /mnt/openscience/audit-envs/bio-atac-seq-motif-deviation/tools/env.sh
cd /mnt/openscience/audits/bio-atac-seq-motif-deviation/reaudit-run
micromamba run -n $ENVN Rscript scripts/render_heat.R
