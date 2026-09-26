#!/usr/bin/env bash
set -u
echo "Rscript=$(command -v Rscript || true)"
echo "micromamba=$(command -v micromamba || true)"
Rscript --version || true
Rscript -e "cat('SingleR=', requireNamespace('SingleR', quietly=TRUE), '\n'); cat('celldex=', requireNamespace('celldex', quietly=TRUE), '\n'); cat('Seurat=', requireNamespace('Seurat', quietly=TRUE), '\n'); cat('SingleCellExperiment=', requireNamespace('SingleCellExperiment', quietly=TRUE), '\n')" || true
