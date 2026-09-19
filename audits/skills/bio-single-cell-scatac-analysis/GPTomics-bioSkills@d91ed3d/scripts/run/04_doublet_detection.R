.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(Seurat)
  library(scDblFinder)
  library(SingleCellExperiment)
})

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data'
obj <- readRDS(file.path(data_dir, 'obj_qc.rds'))
cat('Loaded object:', ncol(obj), 'cells x', nrow(obj), 'peaks\n')

# Inject synthetic doublets: 15 cells get counts summed from a Tcell+Bcell pair (heterotypic)
set.seed(7)
counts <- GetAssayData(obj, assay = 'peaks', layer = 'counts')
t_cells <- colnames(obj)[obj$cell_type == 'Tcell']
b_cells <- colnames(obj)[obj$cell_type == 'Bcell']
n_doublets <- 15
pairs <- data.frame(t = sample(t_cells, n_doublets), b = sample(b_cells, n_doublets))
doublet_counts <- counts[, pairs$t] + counts[, pairs$b]
colnames(doublet_counts) <- paste0('doublet', seq_len(n_doublets))
full_counts <- cbind(counts, doublet_counts)
truth <- c(rep('singlet', ncol(counts)), rep('doublet', n_doublets))
names(truth) <- colnames(full_counts)

sce <- SingleCellExperiment(assays = list(counts = full_counts))

# scDblFinder ATAC per SKILL.md: "simulate on nfeatures=25 aggregated meta-features" (TOOLS.md note:
# not the RNA default of 1000)
sce <- scDblFinder(sce, aggregateFeatures = TRUE, nfeatures = 25, processing = 'normFeatures')
cat('scDblFinder classification table:\n')
print(table(sce$scDblFinder.class))

cross <- table(called = sce$scDblFinder.class, truth = truth)
cat('Called vs ground truth:\n')
print(cross)
sensitivity <- cross['doublet', 'doublet'] / sum(cross[, 'doublet'])
precision <- cross['doublet', 'doublet'] / sum(cross['doublet', ])
cat('Heterotypic doublet recall:', round(sensitivity, 3), '| precision:', round(precision, 3), '\n')
cat('STAGE 4 DONE\n')
