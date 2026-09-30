source /mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools/env.sh
O=/mnt/openscience/audits/bio-atac-seq-single-cell-atac/reaudit-10x/logs
for t in arc atac2x_default atac1x_relaxed; do W=$SCA/work/reaudit10x_$t; for f in scatac_umap scatac_qc scatac_depth_cor; do micromamba run -n pdf-render-poppler pdftoppm -png -r 70 -singlefile $W/$f.pdf $O/${t}_$f; done; done
