# Prior Variant A regression: SingleR on four synthetic PBMC lanes with ground truth.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(SingleR); library(celldex); library(SingleCellExperiment); library(Seurat); library(scuttle)
})
D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
O <- 'F:/OpenScience/audits/bio-single-cell-cell-annotation/reaudit-optimized-scientific-skills@2dee47f-20260925/data'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(tc) <- tc$cell_id
mats <- list()
for (s in paste0('S', 1:4)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
counts <- do.call(cbind, mats)
counts <- counts[, !tc[colnames(counts), 'true_doublet'] & !tc[colnames(counts), 'true_low_quality']]
so <- NormalizeData(CreateSeuratObject(counts, min.cells=3, min.features=200), verbose=FALSE)
sce <- as.SingleCellExperiment(so)
stopifnot('logcounts' %in% assayNames(sce))
ref <- celldex::HumanPrimaryCellAtlasData()
lin <- function(x) {
  s <- tolower(as.character(x))
  ifelse(grepl('t_cell|t cell', s), 'T', ifelse(grepl('^nk|nk_cell', s), 'NK',
  ifelse(grepl('b_cell|b cell', s), 'B', ifelse(grepl('monocyte|macrophage', s), 'Mono',
  ifelse(grepl('^dc$|dendritic', s), 'DC', ifelse(grepl('megakaryo|platelet', s), 'Mk', 'other'))))))
}
truth <- tc[colnames(so), 'true_cell_type']
truth_lin <- c('CD4 T cells'='T', 'CD8 T cells'='T', 'NK cells'='NK', 'B cells'='B',
               'CD14+ Monocytes'='Mono', 'FCGR3A+ Monocytes'='Mono',
               'Dendritic cells'='DC', 'Megakaryocytes'='Mk')[truth]
for (dm in c('classic', 'wilcox')) {
  pred <- SingleR(test=sce, ref=ref, labels=ref$label.main, de.method=dm, fine.tune=TRUE)
  acc <- mean(lin(pred$labels) == truth_lin)
  kept <- !is.na(pred$pruned.labels)
  cat(sprintf('de.method=%s accuracy=%.3f pruned=%d/%d kept_accuracy=%.3f\n',
              dm, acc, sum(!kept), length(kept), mean(lin(pred$pruned.labels[kept]) == truth_lin[kept])))
  if (dm == 'classic') {
    stopifnot(acc > 0.85)
    cat(sprintf('delta_median=%.4f delta_iqr=%.4f-%.4f\n', median(pred$delta.next),
                quantile(pred$delta.next, .25), quantile(pred$delta.next, .75)))
    saveRDS(pred, file.path(O, 'input2_pred.rds'))
  }
}
cat('SingleR regression PASS\n')
