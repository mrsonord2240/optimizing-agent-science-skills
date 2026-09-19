.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac); library(Seurat); library(scDblFinder); library(SingleCellExperiment)
})
data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit_v2_20260919'
obj <- readRDS(file.path(data_dir, 'obj_qc.rds'))
cat('Loaded object:', ncol(obj), 'cells x', nrow(obj), 'peaks\n')

set.seed(55)
counts <- GetAssayData(obj, assay = 'peaks', layer = 'counts')
t_cells <- colnames(obj)[obj$cell_type == 'Tcell']
m_cells <- colnames(obj)[obj$cell_type == 'Monocyte']
n_doublets <- 12
pairs <- data.frame(t = sample(t_cells, n_doublets), m = sample(m_cells, n_doublets))
doublet_counts <- counts[, pairs$t] + counts[, pairs$m]
colnames(doublet_counts) <- paste0('doubletv2_', seq_len(n_doublets))
full_counts <- cbind(counts, doublet_counts)
truth <- c(rep('singlet', ncol(counts)), rep('doublet', n_doublets))
names(truth) <- colnames(full_counts)

sce <- SingleCellExperiment(assays = list(counts = full_counts))
sce <- scDblFinder(sce, aggregateFeatures = TRUE, nfeatures = 25, processing = 'normFeatures')
cross <- table(called = sce$scDblFinder.class, truth = truth)
print(cross)
sensitivity <- cross['doublet', 'doublet'] / sum(cross[, 'doublet'])
cat('Heterotypic (Tcell x Monocyte) doublet recall:', round(sensitivity, 3), '\n')
cat('STAGE 5 (v2 doublets) DONE\n')
