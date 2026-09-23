# Input 6 (Scope Boundary) - bio-differential-expression-deseq2-basics
# "Can I just run this on my single cells, treating cells as replicates?" The Skill's decision
# tree says pseudobulk (Crowell 2020). Tested on a NULL contrast with no injected effect:
# donors split {S1,S3,S5,S7} vs {S2,S4,S6,S8}, which is balanced 2+2 on condition, 2+2 on
# batch and 2+2 on sex, so every call is a false positive by construction.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(DESeq2); library(Seurat); library(presto); library(Matrix)})

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(tc) <- tc$cell_id
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
cm <- do.call(cbind, mats)
cm <- cm[, !tc[colnames(cm), 'true_doublet'] & !tc[colnames(cm), 'true_low_quality']]
meta <- tc[colnames(cm), ]
mono <- rownames(meta)[meta$true_cell_type == 'CD14+ Monocytes']
cmm <- cm[, mono]; mm <- meta[mono, ]
grpX <- c('S1', 'S3', 'S5', 'S7')
mm$fake <- ifelse(mm$sample %in% grpX, 'X', 'Y')
cat(length(mono), 'CD14+ monocytes\n')
cat('NULL split balance (condition x fake, batch x fake, sex x fake):\n')
print(table(ss[unique(mm$sample), 'condition'], ifelse(unique(mm$sample) %in% grpX, 'X', 'Y')))
print(table(ss[unique(mm$sample), 'batch'], ifelse(unique(mm$sample) %in% grpX, 'X', 'Y')))
print(table(ss[unique(mm$sample), 'sex'], ifelse(unique(mm$sample) %in% grpX, 'X', 'Y')))
cat('-> no real difference exists between X and Y. Every call below is a FALSE POSITIVE.\n')

# --- (a) cell-level test, cells as replicates (what the Skill says not to do) ---
so <- CreateSeuratObject(cmm); so <- NormalizeData(so, verbose = FALSE)
so$fake <- factor(mm[colnames(so), 'fake'], levels = c('X', 'Y'))
w <- wilcoxauc(so, group_by = 'fake', seurat_assay = 'RNA')
w <- w[w$group == 'X', ]
w$padj_bh <- p.adjust(w$pval, 'BH')
cat(sprintf('\n(a) CELL-LEVEL Wilcoxon on %d cells: %d genes at BH<0.05, %d at BH<0.05 & |logFC|>0.25\n',
            ncol(cmm), sum(w$padj_bh < 0.05, na.rm = TRUE),
            sum(w$padj_bh < 0.05 & abs(w$logFC) > 0.25, na.rm = TRUE)))
cat('    smallest adjusted p:', formatC(min(w$padj_bh, na.rm = TRUE), format = 'e', digits = 2), '\n')

# --- (b) the same null through cell-level DESeq2 (cells as columns) ---
set.seed(20260916)
sub <- sample(colnames(cmm), 400)
cd_cell <- data.frame(fake = factor(mm[sub, 'fake']), row.names = sub)
dc <- DESeqDataSetFromMatrix(round(as.matrix(cmm[, sub])), cd_cell, design = ~ fake)
dc <- dc[rowSums(counts(dc)) >= 10, ]
dc <- DESeq(dc, sfType = 'poscounts', quiet = TRUE)
rc <- results(dc, name = 'fake_Y_vs_X', alpha = 0.05)
cat(sprintf('(b) CELL-LEVEL DESeq2 on a 400-cell subsample: %d genes padj<0.05 (all false)\n',
            sum(rc$padj < 0.05, na.rm = TRUE)))

# --- (c) the pseudobulk route the Skill prescribes, same null ---
pbc <- sapply(paste0('S', 1:8), function(s)
  Matrix::rowSums(cmm[, rownames(mm)[mm$sample == s], drop = FALSE]))
pbc <- round(as.matrix(pbc))
cd <- data.frame(fake = factor(ifelse(colnames(pbc) %in% grpX, 'X', 'Y')), row.names = colnames(pbc))
dp <- DESeqDataSetFromMatrix(pbc, cd, design = ~ fake)
dp <- dp[rowSums(counts(dp)) >= 10, ]
dp <- DESeq(dp, quiet = TRUE)
rp <- results(dp, name = 'fake_Y_vs_X', alpha = 0.05)
cat(sprintf('(c) PSEUDOBULK DESeq2, 8 samples: %d genes padj<0.05 (all would be false)\n',
            sum(rp$padj < 0.05, na.rm = TRUE)))
cat('    smallest padj:', formatC(min(rp$padj, na.rm = TRUE), format = 'e', digits = 2), '\n')

cat('\n--- and on the REAL contrast, for contrast ---\n')
mm$cond <- ss[mm$sample, 'condition']
so$cond <- factor(mm[colnames(so), 'cond'], levels = c('control', 'treated'))
w2 <- wilcoxauc(so, group_by = 'cond', seurat_assay = 'RNA')
w2 <- w2[w2$group == 'treated', ]; w2$padj_bh <- p.adjust(w2$pval, 'BH')
truth <- read.csv(file.path(D, 'truth_de_genes.csv')); tr <- truth$gene_symbol
sigc <- w2$feature[w2$padj_bh < 0.05 & abs(w2$logFC) > 0.25]
cat(sprintf('cell-level Wilcoxon, real contrast: %d called | TP %d | precision %.3f\n',
            length(sigc), length(intersect(sigc, tr)),
            length(intersect(sigc, tr)) / max(length(sigc), 1)))
cat('pseudobulk DESeq2, real contrast (from input 1): 19 called | TP 19 | precision 1.000\n')
cat('DONE\n')
