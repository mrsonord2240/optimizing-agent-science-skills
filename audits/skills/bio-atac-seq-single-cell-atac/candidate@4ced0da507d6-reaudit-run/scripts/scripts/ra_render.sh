source /mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/tools/env.sh
O=/mnt/openscience/audits/bio-atac-seq-single-cell-atac/reaudit-run/output
for f in qc depth_cor umap; do micromamba run -n pdf-render-poppler pdftoppm -png -r 80 -singlefile $SCA/work/ra_signac_relaxed/scatac_$f.pdf $O/signac_relaxed_$f; done; ls -la $O
