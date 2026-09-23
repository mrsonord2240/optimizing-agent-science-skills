# Input 2 (Variant A) - bio-differential-expression-deseq2-basics
# Design formulas: nuisance covariates (batch, sex) and a paired design. Tests the Skill's
# "variable of interest LAST" rule, the pairing-variable-FIRST rule, and whether adding the
# nuisance terms changes recall against the known injected truth.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(DESeq2); library(apeglm); library(Seurat); library(Matrix)})

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
OUT <- 'F:/OpenScience/audits/bio-differential-expression-deseq2-basics'
pb <- readRDS(file.path(OUT, 'data', 'pseudobulk_cd14_mono.rds'))
truth <- read.csv(file.path(D, 'truth_de_genes.csv'))
tr <- truth$gene_symbol
counts <- pb$counts; coldata <- pb$coldata
print(coldata)

score <- function(res, label) {
  sig <- rownames(res)[which(res$padj < 0.05)]
  tp <- intersect(sig, tr)
  cat(sprintf('%-40s %3d called | TP %2d FP %2d | recall %.3f precision %.3f\n',
              label, length(sig), length(tp), length(setdiff(sig, tr)),
              length(tp) / nrow(truth), length(tp) / max(length(sig), 1)))
  invisible(sig)
}

fit <- function(form, name) {
  d <- DESeqDataSetFromMatrix(counts, coldata, design = form)
  d$condition <- relevel(d$condition, ref = 'control')
  d <- d[rowSums(counts(d)) >= 10, ]
  d <- DESeq(d, quiet = TRUE)
  cat('  resultsNames:', paste(resultsNames(d), collapse = ' | '), '\n')
  results(d, name = name, alpha = 0.05)
}

cat('\n--- nuisance covariates, variable of interest LAST (SKILL.md Design Formulas) ---\n')
score(fit(~ condition, 'condition_treated_vs_control'), '~ condition')
score(fit(~ batch + condition, 'condition_treated_vs_control'), '~ batch + condition')
score(fit(~ sex + condition, 'condition_treated_vs_control'), '~ sex + condition')
score(fit(~ batch + sex + condition, 'condition_treated_vs_control'), '~ batch + sex + condition')

cat('\n--- what if the variable of interest is NOT last? ---\n')
d <- DESeqDataSetFromMatrix(counts, coldata, design = ~ condition + batch)
d$condition <- relevel(d$condition, ref = 'control')
d <- d[rowSums(counts(d)) >= 10, ]; d <- DESeq(d, quiet = TRUE)
cat('  resultsNames:', paste(resultsNames(d), collapse = ' | '), '\n')
score(results(d, name = 'condition_treated_vs_control', alpha = 0.05),
      '~ condition + batch, name= explicit')
cat('  -> the named contrast is identical; only bare results(dds) changes. The Skill says\n')
cat('     "put the variable of interest LAST for readability" - readability is the whole reason.\n')

cat('\n--- PAIRED design (SKILL.md: pairing variable FIRST) ---\n')
# each donor contributes both CD14+ and FCGR3A+ monocytes: a genuine within-donor pair
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
cells <- list(); cd <- list()
for (s in paste0('S', 1:8)) for (ct in c('CD14+ Monocytes', 'FCGR3A+ Monocytes')) {
  id <- paste0(s, '_', ifelse(ct == 'CD14+ Monocytes', 'CD14', 'CD16'))
  idx <- rownames(meta)[meta$sample == s & meta$true_cell_type == ct]
  cells[[id]] <- Matrix::rowSums(cm[, idx, drop = FALSE])
  cd[[id]] <- data.frame(donor = ss[s, 'donor'], subtype = ifelse(ct == 'CD14+ Monocytes', 'CD14', 'CD16'),
                         condition = ss[s, 'condition'], row.names = id)
}
pc <- round(as.matrix(do.call(cbind, cells))); pcd <- do.call(rbind, cd)
pcd$donor <- factor(pcd$donor); pcd$subtype <- factor(pcd$subtype, levels = c('CD14', 'CD16'))
cat('  paired pseudobulk:', nrow(pc), 'genes x', ncol(pc), 'samples (8 donors x 2 subtypes)\n')

dp <- DESeqDataSetFromMatrix(pc, pcd, design = ~ donor + subtype)
dp <- dp[rowSums(counts(dp)) >= 10, ]
dp <- DESeq(dp, quiet = TRUE)
rp <- results(dp, name = 'subtype_CD16_vs_CD14', alpha = 0.05)
cat('  ~ donor + subtype:', sum(rp$padj < 0.05, na.rm = TRUE), 'genes at padj<0.05\n')
du <- DESeqDataSetFromMatrix(pc, pcd, design = ~ subtype)
du <- du[rowSums(counts(du)) >= 10, ]; du <- DESeq(du, quiet = TRUE)
ru <- results(du, name = 'subtype_CD16_vs_CD14', alpha = 0.05)
cat('  ~ subtype (unpaired)  :', sum(ru$padj < 0.05, na.rm = TRUE), 'genes at padj<0.05\n')
cat(sprintf('  -> pairing changed the call count by %+d genes; the Skill says pairing "absorbs\n',
            sum(rp$padj < 0.05, na.rm = TRUE) - sum(ru$padj < 0.05, na.rm = TRUE)))
cat('     subject variability", which should raise power when donor variance is real.\n')
known <- intersect(c('FCGR3A', 'CD14', 'LYZ', 'MS4A7', 'CDKN1C'), rownames(rp))
cat('  known CD16-monocyte markers, paired LFC (CD16 vs CD14):\n')
print(round(as.data.frame(rp[known, c('log2FoldChange', 'padj')]), 4))
cat('DONE\n')
