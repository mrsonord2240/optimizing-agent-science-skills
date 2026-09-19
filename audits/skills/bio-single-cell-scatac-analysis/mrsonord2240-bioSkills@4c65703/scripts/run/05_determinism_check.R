.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(Seurat)
})

# Skill Veto T3 check: SKILL.md/usage-guide/examples never call set.seed() anywhere (grep confirmed 0
# hits). Verify whether the documented pipeline (TF-IDF -> SVD -> UMAP -> clustering) is nonetheless
# deterministic run-to-run because the underlying Seurat/Signac functions default to a fixed internal
# seed, by running it twice in the SAME fresh session state (re-deriving from the identical loaded
# object each time, no explicit seed set by this script either) and diffing outputs.

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data'
obj0 <- readRDS(file.path(data_dir, 'obj_qc.rds'))
# obj_qc.rds was saved AFTER TF-IDF/SVD/clustering already ran once; strip those reductions/assays so
# both runs start from the identical raw QC'd peak counts.
obj0[['lsi']] <- NULL
obj0$seurat_clusters <- NULL

run_once <- function(obj) {
  obj <- RunTFIDF(obj, verbose = FALSE)
  obj <- FindTopFeatures(obj, min.cutoff = 'q0', verbose = FALSE)
  obj <- RunSVD(obj, verbose = FALSE)
  obj <- FindNeighbors(obj, reduction = 'lsi', dims = 2:10, verbose = FALSE)
  obj <- FindClusters(obj, algorithm = 3, resolution = 0.5, verbose = FALSE)
  list(lsi = Embeddings(obj, 'lsi')[, 1:5], clusters = as.character(obj$seurat_clusters))
}

r1 <- run_once(obj0)
r2 <- run_once(obj0)

cat('--- SVD embedding (first 5 comps) identical across two unseeded runs? ---\n')
cat('max abs diff:', max(abs(r1$lsi - r2$lsi)), '\n')
cat('identical (all.equal):', isTRUE(all.equal(r1$lsi, r2$lsi)), '\n')

cat('--- Cluster assignment identical across two unseeded runs? ---\n')
cat('identical labels:', identical(r1$clusters, r2$clusters), '\n')
tab <- table(run1 = r1$clusters, run2 = r2$clusters)
print(tab)
ari <- function(cl1, cl2) {
  t <- table(cl1, cl2); n <- sum(t)
  a <- sum(choose(t, 2)); br <- sum(choose(rowSums(t), 2)); bc <- sum(choose(colSums(t), 2))
  e <- br * bc / choose(n, 2); m <- 0.5 * (br + bc)
  (a - e) / (m - e)
}
cat('ARI(run1, run2):', round(ari(r1$clusters, r2$clusters), 4), '\n')
cat('STAGE 5 DONE\n')
