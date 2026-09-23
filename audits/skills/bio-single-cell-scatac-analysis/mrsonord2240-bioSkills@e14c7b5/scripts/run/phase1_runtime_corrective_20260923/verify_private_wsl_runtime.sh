#!/usr/bin/env bash
set -euo pipefail

runtime=/home/sci/scatac-private-20260923/bin/Rscript
"$runtime" - <<'RSCRIPT'
suppressPackageStartupMessages({
  library(Signac); library(Seurat)
  library(JASPAR2020); library(TFBSTools); library(motifmatchr)
  library(BSgenome.Hsapiens.UCSC.hg38)
  library(chromVAR); library(SummarizedExperiment); library(BiocParallel)
})
for (pkg in c('Signac', 'Seurat', 'JASPAR2020', 'TFBSTools', 'motifmatchr',
              'BSgenome.Hsapiens.UCSC.hg38', 'chromVAR', 'BiocParallel')) {
  cat(pkg, as.character(packageVersion(pkg)), '\n')
}
quit(save = 'no', status = 0, runLast = FALSE)
RSCRIPT
