#!/bin/bash
# Parse-check the delta-cat2 candidate R script in the lane R env (read-only).
eval "$(micromamba shell hook -s bash)"; micromamba activate bio-atac-seq-nucleosome-positioning-r
S=/mnt/openscience/wt/atac-nucleosome-positioning/skills/bio-atac-seq-nucleosome-positioning/scripts/nucleosome_analysis.R
sha256sum "$S"; Rscript -e "x <- parse(file='$S'); cat('PARSE OK, top-level expressions:', length(x), '\n')"; echo "parse_rc=$?"
