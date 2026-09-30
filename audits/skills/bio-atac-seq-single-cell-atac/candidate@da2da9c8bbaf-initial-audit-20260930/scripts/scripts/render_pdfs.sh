export PATH=/home/sci/.local/bin:$PATH MAMBA_ROOT_PREFIX=/home/sci/micromamba
SCA=/mnt/openscience/audit-envs/bio-atac-seq-single-cell-atac/audit-initial-20260930
O=/mnt/openscience/audits/bio-atac-seq-single-cell-atac/initial-audit-20260930/out
for f in qc depth_cor umap; do micromamba run -n pdf-render-poppler pdftoppm -png -r 80 -singlefile $SCA/work/patched/scatac_$f.pdf $O/signac_$f; done
