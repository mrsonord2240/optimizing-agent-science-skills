# Windows R runtime exit probe: all packages used by scripts/run_chromvar.R.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac); library(Seurat)
  library(JASPAR2020); library(TFBSTools); library(motifmatchr)
  library(BSgenome.Hsapiens.UCSC.hg38)
  library(chromVAR); library(SummarizedExperiment); library(BiocParallel)
})
register(SerialParam())
cat('PROBE_CHROMVAR_STACK_OK\n')
quit(save = 'no', status = 0, runLast = FALSE)
