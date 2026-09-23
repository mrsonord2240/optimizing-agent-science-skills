# Input 1 (Canonical) - bio-differential-expression-deseq2-basics
# The single-cell pseudobulk row of the Skill's decision tree, run with the Standard Workflow
# exactly as SKILL.md prints it. SYNTHETIC 8-sample PBMC set; ground truth is 55 genes changed
# in CD14+ monocytes (15 at log2FC +2, 20 at +1, 20 at -1) and nothing anywhere else.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(DESeq2); library(apeglm); library(Seurat); library(Matrix)})
cat('DESeq2', as.character(packageVersion('DESeq2')), '| apeglm',
    as.character(packageVersion('apeglm')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
OUT <- 'F:/OpenScience/audits/bio-differential-expression-deseq2-basics'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
rownames(tc) <- tc$cell_id
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
truth <- read.csv(file.path(D, 'truth_de_genes.csv'))

mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m)); mats[[s]] <- m
}
cm <- do.call(cbind, mats)
cm <- cm[, !tc[colnames(cm), 'true_doublet'] & !tc[colnames(cm), 'true_low_quality']]
meta <- tc[colnames(cm), ]

# pseudobulk per sample x cell type - the aggregation the Skill's decision tree calls for
mono <- rownames(meta)[meta$true_cell_type == 'CD14+ Monocytes']
counts <- sapply(paste0('S', 1:8), function(s)
  Matrix::rowSums(cm[, intersect(mono, rownames(meta)[meta$sample == s]), drop = FALSE]))
counts <- round(as.matrix(counts))
coldata <- data.frame(condition = factor(ss[colnames(counts), 'condition']),
                      batch = factor(ss[colnames(counts), 'batch']),
                      sex = factor(ss[colnames(counts), 'sex']),
                      row.names = colnames(counts))
cat('pseudobulk matrix:', nrow(counts), 'genes x', ncol(counts), 'samples\n')
print(coldata)
saveRDS(list(counts = counts, coldata = coldata),
        file.path(OUT, 'data', 'pseudobulk_cd14_mono.rds'))

# --- SKILL.md Standard Workflow, verbatim ---
dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata, design = ~ condition)
dds$condition <- relevel(dds$condition, ref = 'control')
keep <- rowSums(counts(dds)) >= 10
dds <- dds[keep, ]
cat('after pre-filter rowSums >= 10:', nrow(dds), 'genes\n')
dds <- DESeq(dds)
cat('resultsNames:', paste(resultsNames(dds), collapse = ' | '), '\n')
res <- results(dds, name = 'condition_treated_vs_control', alpha = 0.05)
res_shrunk <- lfcShrink(dds, coef = 'condition_treated_vs_control', type = 'apeglm')
summary(res)

sig <- rownames(res)[which(res$padj < 0.05)]
tr <- truth$gene_symbol
up <- truth$gene_symbol[truth$true_log2FC_treated_vs_control > 0]
tp <- intersect(sig, tr)
cat(sprintf('\npadj<0.05: %d genes | TP=%d FP=%d | recall %.3f of %d injected | precision %.3f\n',
            length(sig), length(tp), length(setdiff(sig, tr)), length(tp) / nrow(truth),
            nrow(truth), length(tp) / max(length(sig), 1)))
dir_ok <- sum(sapply(tp, function(g) (res[g, 'log2FoldChange'] > 0) == (g %in% up)))
cat('direction correct:', dir_ok, '/', length(tp), '\n')
cat('\nrecovered genes by injected effect size:\n')
for (fc in c(2, 1, -1)) {
  gs <- truth$gene_symbol[truth$true_log2FC_treated_vs_control == fc]
  cat(sprintf('  true log2FC %+0.0f (%2d genes): %2d recovered; median estimated LFC %+.2f (shrunk %+.2f)\n',
              fc, length(gs), length(intersect(gs, sig)),
              median(res[intersect(gs, rownames(res)), 'log2FoldChange'], na.rm = TRUE),
              median(res_shrunk[intersect(gs, rownames(res_shrunk)), 'log2FoldChange'], na.rm = TRUE)))
}

# --- the Skill's headline insight: shrunken LFC, unshrunken Wald p ---
cat('\nSKILL.md "Single Most Important Modern Insight":\n')
cat('  p-values identical between results() and lfcShrink():',
    isTRUE(all.equal(res$pvalue, res_shrunk$pvalue)), '\n')
cat('  padj identical:', isTRUE(all.equal(res$padj, res_shrunk$padj)), '\n')
cat('  LFCs identical:', isTRUE(all.equal(res$log2FoldChange, res_shrunk$log2FoldChange)), '\n')
cat(sprintf('  median |LFC| unshrunk %.3f vs shrunk %.3f over all genes\n',
            median(abs(res$log2FoldChange), na.rm = TRUE),
            median(abs(res_shrunk$log2FoldChange), na.rm = TRUE)))

# --- the resultsNames trap: what does bare results(dds) return? ---
dds2 <- DESeqDataSetFromMatrix(counts[keep, ], coldata, design = ~ batch + condition)
dds2$condition <- relevel(dds2$condition, ref = 'control')
dds2 <- DESeq(dds2, quiet = TRUE)
cat('\nwith design ~ batch + condition, resultsNames:',
    paste(resultsNames(dds2), collapse = ' | '), '\n')
bare <- results(dds2)
named <- results(dds2, name = 'condition_treated_vs_control')
cat('  bare results(dds) == results(name="condition_treated_vs_control")?',
    isTRUE(all.equal(bare$log2FoldChange, named$log2FoldChange)), '\n')
dds3 <- dds2; design(dds3) <- ~ condition + batch
dds3 <- DESeq(dds3, quiet = TRUE)
cat('  with design ~ condition + batch, resultsNames:',
    paste(resultsNames(dds3), collapse = ' | '), '\n')
b3 <- results(dds3)
cat('  bare results() now equals the CONDITION effect?',
    isTRUE(all.equal(b3$log2FoldChange, named$log2FoldChange)),
    '- it returns the last coefficient, as the Skill warns\n')

# --- summary() alpha trap from the Common errors table ---
cat('\nsummary() alpha trap: results(alpha=0.05) but summary() default alpha=0.1\n')
cat('  genes at padj<0.05:', sum(res$padj < 0.05, na.rm = TRUE),
    '| genes at padj<0.1:', sum(res$padj < 0.1, na.rm = TRUE), '\n')
cat('DONE\n')
