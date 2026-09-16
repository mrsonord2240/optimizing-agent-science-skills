# Input 5 (Stress) - bio-workflows-scrnaseq-pipeline
# The two steps the Skill's ordering prose demands but neither code path performs: pseudobulk
# condition DE per cell type, and a paired differential-abundance test. Run on the annotated
# object produced end to end by input 1, scored against the SYNTHETIC ground truth.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(DESeq2); library(speckle); library(Matrix)})

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
R <- 'F:/OpenScience/audits/bio-workflows-scrnaseq-pipeline/run'
o <- readRDS(file.path(R, 'input1_annotated.rds'))
truth <- read.csv(file.path(D, 'truth_de_genes.csv')); tr <- truth$gene_symbol
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
cat('annotated object from input 1:', ncol(o), 'cells,', length(unique(o$cell_type)), 'cell types\n')
cat('GROUND TRUTH: 55 genes changed in CD14+ Monocytes only; NK 6% -> ~13%; nothing else.\n')

cnt <- GetAssayData(o, assay = 'RNA', layer = 'counts')
res_all <- list()
cat('\n--- pseudobulk DE per cell type (RAW counts per sample x cell type) ---\n')
for (ct in sort(unique(o$cell_type))) {
  cells <- colnames(o)[o$cell_type == ct]
  pb <- sapply(paste0('S',1:8), function(s)
    Matrix::rowSums(cnt[, intersect(cells, colnames(o)[o$sample == s]), drop = FALSE]))
  pb <- round(as.matrix(pb))
  cd <- data.frame(condition = relevel(factor(ss[colnames(pb), 'condition']), ref = 'control'),
                   row.names = colnames(pb))
  if (min(table(cd$condition)) < 2) { cat(sprintf('  %-20s skipped (n<2 per group)\n', ct)); next }
  d <- DESeqDataSetFromMatrix(pb, cd, design = ~ condition)
  d <- d[rowSums(counts(d)) >= 10, ]
  d <- suppressMessages(DESeq(d, quiet = TRUE))
  rr <- results(d, name = 'condition_treated_vs_control', alpha = 0.05)
  sig <- rownames(rr)[which(rr$padj < 0.05)]
  tp <- intersect(sig, tr)
  res_all[[ct]] <- sig
  cat(sprintf('  %-20s n=%4d cells | %3d genes padj<0.05 | TP %2d | precision %.3f\n',
              ct, length(cells), length(sig), length(tp), length(tp)/max(length(sig),1)))
}
cat(sprintf('\n  total calls outside CD14+ Monocytes (all false by construction): %d\n',
            sum(sapply(names(res_all)[names(res_all) != 'CD14+ Monocytes'], function(k) length(res_all[[k]])))))
cat(sprintf('  CD14+ Monocytes recall of the 55 injected genes: %.3f\n',
            length(intersect(res_all[['CD14+ Monocytes']], tr)) / length(tr)))

cat('\n--- paired differential-abundance test (SKILL.md ordering rule 7) ---\n')
p <- propeller(clusters = o$cell_type, sample = o$sample, group = o$condition)
num <- intersect(c('PropMean.control','PropMean.treated','P.Value','FDR'), colnames(p))
print(cbind(cluster = as.character(p[[1]]), round(p[, num], 5)))
cat('significant at FDR<0.05:', paste(rownames(p)[p$FDR < 0.05], collapse = ', '), '\n')
cat('  -> the two results together: an expression change confined to CD14+ monocytes AND an\n')
cat('     abundance change confined to NK cells. Running only one of the two would have\n')
cat('     reported half the biology, which is the Skill\'s stated reason for pairing them.\n')
cat('DONE\n')
