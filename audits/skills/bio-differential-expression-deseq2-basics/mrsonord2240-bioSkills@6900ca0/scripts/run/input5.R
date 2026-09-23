# Input 5 (Stress) - bio-differential-expression-deseq2-basics
# Wald vs LRT on a multi-level factor, and the Skill's specific claim that after an LRT the
# reported log2FoldChange is the LAST coefficient in resultsNames, not an omnibus effect.
# A 4-level factor is built from condition x batch on the SYNTHETIC pseudobulk.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(DESeq2)})

OUT <- 'F:/OpenScience/audits/bio-differential-expression-deseq2-basics'
D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
pb <- readRDS(file.path(OUT, 'data', 'pseudobulk_cd14_mono.rds'))
truth <- read.csv(file.path(D, 'truth_de_genes.csv')); tr <- truth$gene_symbol
counts <- pb$counts; coldata <- pb$coldata
coldata$grp <- factor(paste(coldata$condition, coldata$batch, sep = '_'),
                      levels = c('control_A', 'control_B', 'treated_A', 'treated_B'))
print(table(coldata$grp))
cat('GROUND TRUTH: the injected effect is condition only; batch adds a per-gene nuisance.\n')

dds <- DESeqDataSetFromMatrix(counts, coldata, design = ~ grp)
dds <- dds[rowSums(counts(dds)) >= 10, ]

# --- LRT, omnibus "any difference among the four groups" ---
dl <- DESeq(dds, test = 'LRT', reduced = ~ 1, quiet = TRUE)
cat('\nresultsNames after LRT:', paste(resultsNames(dl), collapse = ' | '), '\n')
rl <- results(dl, alpha = 0.05)
sigl <- rownames(rl)[which(rl$padj < 0.05)]
cat(sprintf('LRT (reduced = ~1): %d genes padj<0.05 | TP %d | precision %.3f\n',
            length(sigl), length(intersect(sigl, tr)),
            length(intersect(sigl, tr)) / max(length(sigl), 1)))

# --- the claim: the LFC after LRT is the LAST coefficient, not the omnibus effect ---
dw <- DESeq(dds, quiet = TRUE)
last <- tail(resultsNames(dw), 1)
rw_last <- results(dw, name = last)
cat('\nSKILL.md "LRT reports the wrong LFC" claim:\n')
cat('  last coefficient is', last, '\n')
cat('  LRT log2FoldChange == Wald LFC of that last coefficient?',
    isTRUE(all.equal(rl$log2FoldChange, rw_last$log2FoldChange)), '\n')
rw_first <- results(dw, name = resultsNames(dw)[2])
cat('  LRT log2FoldChange == Wald LFC of the FIRST non-intercept coefficient?',
    isTRUE(all.equal(rl$log2FoldChange, rw_first$log2FoldChange)), '\n')
cat('  correlation of the LRT LFC column with the treated_A-vs-control_A Wald LFC:',
    round(cor(rl$log2FoldChange,
              results(dw, contrast = c('grp', 'treated_A', 'control_A'))$log2FoldChange,
              use = 'complete.obs'), 4), '\n')

# --- the Skill's remedy: per-level Wald coefficients for the effect sizes ---
cat('\nper-level Wald effect sizes on 3 injected genes (the Skill\'s prescribed remedy):\n')
probe <- intersect(truth$gene_symbol[truth$true_log2FC_treated_vs_control == 2][1:3], rownames(dw))
tab <- sapply(resultsNames(dw)[-1], function(n) results(dw, name = n)[probe, 'log2FoldChange'])
rownames(tab) <- probe
print(round(tab, 3))
cat('  the LRT LFC column for the same genes:',
    paste(round(rl[probe, 'log2FoldChange'], 3), collapse = ' '), '\n')

# --- LRT used correctly: screen for "any change" and compare to the 2-group Wald ---
dds2 <- DESeqDataSetFromMatrix(counts, coldata, design = ~ condition)
dds2$condition <- relevel(factor(dds2$condition), ref = 'control')
dds2 <- dds2[rowSums(counts(dds2)) >= 10, ]
dds2 <- DESeq(dds2, quiet = TRUE)
r2 <- results(dds2, name = 'condition_treated_vs_control', alpha = 0.05)
sig2 <- rownames(r2)[which(r2$padj < 0.05)]
cat(sprintf('\nsimple 2-group Wald (~ condition): %d genes | TP %d | precision %.3f\n',
            length(sig2), length(intersect(sig2, tr)),
            length(intersect(sig2, tr)) / max(length(sig2), 1)))
cat('  LRT-only genes:', length(setdiff(sigl, sig2)), '| Wald-only genes:',
    length(setdiff(sig2, sigl)), '| shared:', length(intersect(sigl, sig2)), '\n')

# --- LRT with a reduced model that keeps the nuisance, the form SKILL.md prints ---
dl2 <- DESeq(dds, test = 'LRT', reduced = ~ 1, quiet = TRUE)
coldata$batch <- factor(coldata$batch)
d3 <- DESeqDataSetFromMatrix(counts, coldata, design = ~ batch + condition)
d3 <- d3[rowSums(counts(d3)) >= 10, ]
d3 <- DESeq(d3, test = 'LRT', reduced = ~ batch, quiet = TRUE)
r3 <- results(d3, alpha = 0.05)
sig3 <- rownames(r3)[which(r3$padj < 0.05)]
cat(sprintf('LRT with reduced = ~ batch (SKILL.md:%s form): %d genes | TP %d | precision %.3f\n',
            'Wald vs LRT', length(sig3), length(intersect(sig3, tr)),
            length(intersect(sig3, tr)) / max(length(sig3), 1)))
cat('DONE\n')
