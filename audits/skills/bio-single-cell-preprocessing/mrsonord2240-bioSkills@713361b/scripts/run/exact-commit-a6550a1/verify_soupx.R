.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(SoupX); library(Seurat); library(Matrix)})

# Exact-commit a6550a1 SoupX pattern on synthetic Cell Ranger raw+filtered S1.
D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples/S1/outs'
sc <- load10X(D)
if (is.null(sc$metaData$clusters)) {
  so <- Seurat::CreateSeuratObject(sc$toc)
  so <- Seurat::NormalizeData(so, verbose = FALSE)
  so <- Seurat::FindVariableFeatures(so, verbose = FALSE)
  so <- Seurat::ScaleData(so, verbose = FALSE)
  so <- Seurat::RunPCA(so, npcs = 30, verbose = FALSE)
  so <- Seurat::FindNeighbors(so, dims = 1:20, verbose = FALSE)
  so <- Seurat::FindClusters(so, resolution = 0.8, verbose = FALSE)
  sc <- setClusters(sc, setNames(as.character(Seurat::Idents(so)), colnames(so)))
}
stopifnot(!is.null(sc$metaData$clusters), length(sc$metaData$clusters) == ncol(sc$toc))
sc <- autoEstCont(sc, doPlot = FALSE, forceAccept = TRUE)
adj <- adjustCounts(sc, roundToInt = TRUE)
stopifnot(identical(dim(adj), dim(sc$toc)), sum(adj) <= sum(sc$toc))
cat('PASS: SoupX', as.character(packageVersion('SoupX')), 'clusters=', length(sc$metaData$clusters),
    'rho=', round(mean(sc$metaData$rho), 4), 'removed=', round(100 * (1 - sum(adj) / sum(sc$toc)), 2), '%\n')
