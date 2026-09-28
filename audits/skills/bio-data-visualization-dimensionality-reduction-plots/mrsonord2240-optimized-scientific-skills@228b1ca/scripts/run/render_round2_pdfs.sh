#!/usr/bin/env bash
set -euo pipefail
base=/mnt/openscience/audits/bio-data-visualization-dimensionality-reduction-plots
for suite in example boundary twenty; do
  mkdir -p "$base/figs/${suite}_rendered"
  for pdf in "$base/run/$suite/figures"/*.pdf; do
    name=$(basename "$pdf" .pdf)
    gs -q -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r110 -dFirstPage=1 -dLastPage=1 \
      -sOutputFile="$base/figs/${suite}_rendered/${name}.png" "$pdf"
  done
done
gs -q -dSAFER -dBATCH -dNOPAUSE -sDEVICE=png16m -r110 -dFirstPage=1 -dLastPage=1 \
  -sOutputFile="$base/figs/input3_umap_clusters.png" "$base/figs/input3_umap_clusters.pdf"
