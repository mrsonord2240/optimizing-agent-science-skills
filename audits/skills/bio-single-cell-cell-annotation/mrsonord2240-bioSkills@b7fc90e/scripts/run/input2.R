# Input 2 (Variant A) - bio-single-cell-cell-annotation
# SingleR exactly as SKILL.md:85-101: celldex reference, de.method='classic' for a bulk
# reference, fine.tune, then pruned.labels as the rejection set. Scored against the
# SYNTHETIC ground-truth cell types; the Skill's de.method guidance tested both ways.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(SingleR); library(celldex); library(SingleCellExperiment); library(Seurat); library(scuttle)
})
cat('SingleR', as.character(packageVersion('SingleR')), '| celldex',
    as.character(packageVersion('celldex')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(tc) <- tc$cell_id
mats <- list()
for (s in paste0('S', 1:4)) {   # 4 lanes is plenty for an annotation test
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
counts <- do.call(cbind, mats)
counts <- counts[, !tc[colnames(counts), 'true_doublet'] & !tc[colnames(counts), 'true_low_quality']]
truth <- tc[colnames(counts), 'true_cell_type']
cat(ncol(counts), 'cells\n')

so <- CreateSeuratObject(counts, min.cells = 3, min.features = 200)
so <- NormalizeData(so, verbose = FALSE)
truth <- tc[colnames(so), 'true_cell_type']
sce <- as.SingleCellExperiment(so)
cat('logcounts present in the SCE handed to SingleR:', 'logcounts' %in% assayNames(sce), '\n')

ref <- celldex::HumanPrimaryCellAtlasData()
cat('reference:', nrow(ref), 'genes x', ncol(ref), 'samples;',
    length(unique(ref$label.main)), 'main labels\n')

lin <- function(x) {
  s <- tolower(as.character(x))
  ifelse(grepl('t_cell|t cell', s), 'T',
  ifelse(grepl('^nk|nk_cell', s), 'NK',
  ifelse(grepl('b_cell|b cell', s), 'B',
  ifelse(grepl('monocyte|macrophage', s), 'Mono',
  ifelse(grepl('^dc$|dendritic', s), 'DC',
  ifelse(grepl('megakaryo|platelet', s), 'Mk', paste0('other:', s)))))))
}
truth_lin <- c('CD4 T cells' = 'T', 'CD8 T cells' = 'T', 'NK cells' = 'NK', 'B cells' = 'B',
               'CD14+ Monocytes' = 'Mono', 'FCGR3A+ Monocytes' = 'Mono',
               'Dendritic cells' = 'DC', 'Megakaryocytes' = 'Mk')[truth]

for (dm in c('classic', 'wilcox')) {
  t0 <- Sys.time()
  pred <- SingleR(test = sce, ref = ref, labels = ref$label.main, de.method = dm, fine.tune = TRUE)
  dt <- round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1)
  pl <- lin(pred$labels)
  acc <- mean(pl == truth_lin)
  npruned <- sum(is.na(pred$pruned.labels))
  accp <- mean(lin(pred$pruned.labels)[!is.na(pred$pruned.labels)] ==
                 truth_lin[!is.na(pred$pruned.labels)])
  cat(sprintf(paste0('de.method=%-8s %5ss  lineage accuracy %.3f | pruned to NA: %d (%.1f%%) | ',
                     'accuracy among kept %.3f\n'),
              dm, dt, acc, npruned, 100 * npruned / length(pl), accp))
  if (dm == 'classic') {
    cat('  confusion (rows = truth lineage, cols = SingleR lineage):\n')
    print(table(truth_lin, pl))
    cat('  raw SingleR labels seen:', paste(sort(unique(pred$labels)), collapse = ', '), '\n')
    saveRDS(pred, 'F:/OpenScience/audits/bio-single-cell-cell-annotation/run/input2_pred.rds')
    # the Skill says to inspect the delta distribution rather than a hard cutoff
    d <- pred$delta.next
    cat(sprintf('  delta.next: median %.4f, IQR %.4f-%.4f; pruneScores(nmads=3) flags %d cells\n',
                median(d, na.rm = TRUE), quantile(d, .25, na.rm = TRUE),
                quantile(d, .75, na.rm = TRUE), sum(is.na(pruneScores(pred, nmads = 3)))))
  }
}
cat('DONE\n')
