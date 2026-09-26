# Linux confirmation of the same four-lane SingleR regression using the prepared sparse query.
suppressPackageStartupMessages({
  library(Matrix); library(SingleR); library(celldex); library(SingleCellExperiment); library(scuttle)
})
O <- '/mnt/openscience/audits/bio-single-cell-cell-annotation/reaudit-optimized-scientific-skills@2dee47f-20260925/data'
counts <- readMM(file.path(O, 'input2_counts.mtx'))
genes <- read.delim(file.path(O, 'input2_genes.tsv'), header=FALSE, stringsAsFactors=FALSE)[,1]
cells <- read.csv(file.path(O, 'input2_cells.csv'), stringsAsFactors=FALSE)
rownames(counts) <- genes; colnames(counts) <- cells$cell_id
sce <- SingleCellExperiment(list(counts=counts))
sce <- logNormCounts(sce)
stopifnot('logcounts' %in% assayNames(sce))
ref <- celldex::HumanPrimaryCellAtlasData()
pred <- SingleR(test=sce, ref=ref, labels=ref$label.main, de.method='classic', fine.tune=TRUE)
lin <- function(x) {
  s <- tolower(as.character(x))
  ifelse(grepl('t_cell|t cell', s), 'T', ifelse(grepl('^nk|nk_cell', s), 'NK',
  ifelse(grepl('b_cell|b cell', s), 'B', ifelse(grepl('monocyte|macrophage', s), 'Mono',
  ifelse(grepl('^dc$|dendritic', s), 'DC', ifelse(grepl('megakaryo|platelet', s), 'Mk', 'other'))))))
}
truth_lin <- c('CD4 T cells'='T', 'CD8 T cells'='T', 'NK cells'='NK', 'B cells'='B',
               'CD14+ Monocytes'='Mono', 'FCGR3A+ Monocytes'='Mono',
               'Dendritic cells'='DC', 'Megakaryocytes'='Mk')[cells$true_cell_type]
acc <- mean(lin(pred$labels) == truth_lin)
cat(sprintf('wsl_accuracy=%.3f pruned=%d/%d\n', acc, sum(is.na(pred$pruned.labels)), nrow(pred)))
stopifnot(acc > 0.85)
saveRDS(pred, file.path(O, 'input2_wsl_pred.rds'))
cat('WSL_SINGLER_PASS\n')
