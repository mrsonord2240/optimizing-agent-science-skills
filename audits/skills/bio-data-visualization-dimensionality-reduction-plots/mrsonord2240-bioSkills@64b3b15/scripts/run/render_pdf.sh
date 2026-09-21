#!/bin/bash
# render example PDFs to PNG with WSL Ghostscript for inspection
D=/mnt/openscience/audits/bio-data-visualization-dimensionality-reduction-plots
for f in pca tsne; do micromamba run -n dv-cli gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r70 -sOutputFile=$D/figs/i6_$f.png $D/run/ex/$f.pdf; done
micromamba run -n dv-cli gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r70 -sOutputFile=$D/figs/i6_umap_clusters.png $D/run/ex/figures/umap_clusters.pdf
ls -l $D/figs/i6_*
