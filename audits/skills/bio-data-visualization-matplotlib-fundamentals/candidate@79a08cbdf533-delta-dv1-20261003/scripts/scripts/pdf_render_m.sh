#!/bin/bash
B=/mnt/openscience/audits/bio-data-visualization-matplotlib-fundamentals/reaudit-dv2-20261003/out
cd $B/phd || exit 1
for f in *.pdf; do echo "== phd/$f"; micromamba run -n dv-cli pdffonts "$f"; done
micromamba run -n dv-cli pdftoppm -png -r 220 -singlefile volcano_so.pdf volcano_so_pdf
micromamba run -n dv-cli pdftoppm -png -r 220 -singlefile pca.pdf pca_pdf
micromamba run -n dv-cli pdftoppm -png -r 150 -singlefile multipanel.pdf multipanel_pdf
micromamba run -n dv-cli pdftoppm -png -r 200 -singlefile heatmap.pdf heatmap_pdf
cd $B/legend || exit 1
for f in B_long_title D_long_title_long_labels A_skill_labels I_public_on_fig_moved; do micromamba run -n dv-cli pdftoppm -png -r 220 -singlefile $f.pdf $f; done
echo rendered
