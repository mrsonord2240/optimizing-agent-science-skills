# Input 2 (Variant A) - bio-single-cell-clustering
# The Seurat path exactly as SKILL.md:98-114: RunPCA -> ElbowPlot -> FindNeighbors ->
# FindClusters over a resolution vector -> RunUMAP -> clustree. Also checks the Skill's
# claims about FindClusters defaults (Louvain algorithm=1) and the RNA_snn_res.<r> naming
# that clustree depends on. SYNTHETIC 8-sample PBMC set.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(clustree); library(Matrix)})
cat('Seurat', as.character(packageVersion('Seurat')), '| clustree',
    as.character(packageVersion('clustree')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(tc) <- tc$cell_id

mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
counts <- do.call(cbind, mats)
keep <- !tc[colnames(counts), 'true_doublet'] & !tc[colnames(counts), 'true_low_quality']
counts <- counts[, keep]
obj <- CreateSeuratObject(counts, min.cells = 3, min.features = 200)
truth <- tc[colnames(obj), 'true_cell_type']
cat(ncol(obj), 'clean cells\n')

set.seed(20260916)
obj <- NormalizeData(obj, verbose = FALSE)
obj <- FindVariableFeatures(obj, nfeatures = 2000, verbose = FALSE)
obj <- ScaleData(obj, verbose = FALSE)
obj <- RunPCA(obj, npcs = 50, verbose = FALSE)
sdev <- Stdev(obj, reduction = 'pca')
cat('PCA stdev, first 12:', round(sdev[1:12], 3), '\n')

obj <- FindNeighbors(obj, dims = 1:30, verbose = FALSE)
obj <- FindClusters(obj, resolution = c(0.2, 0.4, 0.6, 0.8, 1.0), verbose = FALSE)
res_cols <- grep('^RNA_snn_res', colnames(obj@meta.data), value = TRUE)
cat('metadata columns created:', paste(res_cols, collapse = ', '), '\n')
cat('  (SKILL.md:114 says these are named RNA_snn_res.<r> and feed clustree directly)\n')

ari <- function(x, y) {
  t <- table(x, y); n <- sum(t)
  s <- sum(choose(t, 2)); a <- sum(choose(rowSums(t), 2)); b <- sum(choose(colSums(t), 2))
  e <- a * b / choose(n, 2)
  (s - e) / ((a + b) / 2 - e)
}
for (cl in res_cols) {
  cat(sprintf('  %s: %d clusters, ARI vs 8 true types = %.3f\n', cl,
              length(unique(obj@meta.data[[cl]])), ari(obj@meta.data[[cl]], truth)))
}

# the Skill says FindClusters defaults to Louvain (algorithm=1); check algorithm=3 (SLM) and 4 (Leiden)
for (alg in c(1, 3, 4)) {
  r <- try(FindClusters(obj, resolution = 0.6, algorithm = alg, verbose = FALSE), silent = TRUE)
  if (inherits(r, 'try-error')) {
    cat(sprintf('  algorithm=%d FAILED: %s', alg, sub('\n.*', '\n', as.character(r))))
  } else {
    cat(sprintf('  algorithm=%d: %d clusters, ARI = %.3f\n', alg,
                length(unique(Idents(r))), ari(as.character(Idents(r)), truth)))
  }
}

# clustree, the validation tool the Skill prescribes
ct <- try({
  p <- clustree(obj, prefix = 'RNA_snn_res.')
  ggplot2::ggsave(file.path('F:/OpenScience/audits/bio-single-cell-clustering/run',
                            'input2_clustree.png'), p, width = 8, height = 7, dpi = 90)
  'clustree rendered'
}, silent = TRUE)
cat('clustree:', if (inherits(ct, 'try-error')) paste('FAILED:', as.character(ct)) else ct, '\n')

obj <- RunUMAP(obj, dims = 1:30, verbose = FALSE)
cat('UMAP:', paste(dim(Embeddings(obj, 'umap')), collapse = ' x '), '\n')
cat('DONE\n')
