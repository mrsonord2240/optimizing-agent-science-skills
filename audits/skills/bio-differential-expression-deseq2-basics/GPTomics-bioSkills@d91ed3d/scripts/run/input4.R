# Input 4 (Variant B) - bio-differential-expression-deseq2-basics
# Interaction designs: the resultsNames trap, "treatment_X_vs_Y is the effect IN THE REFERENCE
# LEVEL ONLY", the apeglm-cannot-use-contrast footgun and both prescribed workarounds, and the
# combined-factor ~ 0 + group alternative. condition x sex on the SYNTHETIC pseudobulk.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(DESeq2); library(apeglm); library(ashr)})

OUT <- 'F:/OpenScience/audits/bio-differential-expression-deseq2-basics'
D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
pb <- readRDS(file.path(OUT, 'data', 'pseudobulk_cd14_mono.rds'))
truth <- read.csv(file.path(D, 'truth_de_genes.csv')); tr <- truth$gene_symbol
counts <- pb$counts; coldata <- pb$coldata
coldata$condition <- relevel(factor(coldata$condition), ref = 'control')
coldata$sex <- relevel(factor(coldata$sex), ref = 'F')
print(table(coldata$condition, coldata$sex))
cat('GROUND TRUTH: the treatment effect was injected identically in both sexes, so the true\n')
cat('interaction is ZERO for every gene.\n')

dds <- DESeqDataSetFromMatrix(counts, coldata, design = ~ sex + condition + sex:condition)
dds <- dds[rowSums(counts(dds)) >= 10, ]
dds <- DESeq(dds, quiet = TRUE)
cat('\nresultsNames:', paste(resultsNames(dds), collapse = ' | '), '\n')

r_main <- results(dds, name = 'condition_treated_vs_control', alpha = 0.05)
r_int  <- results(dds, name = tail(resultsNames(dds), 1), alpha = 0.05)
cat(sprintf('condition_treated_vs_control (F reference only): %d genes padj<0.05, TP %d\n',
            sum(r_main$padj < 0.05, na.rm = TRUE),
            length(intersect(rownames(r_main)[which(r_main$padj < 0.05)], tr))))
cat(sprintf('interaction term %-22s      : %d genes padj<0.05  (truth: 0)\n',
            tail(resultsNames(dds), 1), sum(r_int$padj < 0.05, na.rm = TRUE)))

# the Skill: "drug effect in KO requires summing" - here, treatment effect in MALES
r_m <- results(dds, contrast = list(c('condition_treated_vs_control', tail(resultsNames(dds), 1))),
               alpha = 0.05)
cat(sprintf('treatment effect in MALES (summed contrast)     : %d genes padj<0.05, TP %d\n',
            sum(r_m$padj < 0.05, na.rm = TRUE),
            length(intersect(rownames(r_m)[which(r_m$padj < 0.05)], tr))))

# --- the apeglm footgun, SKILL.md "apeglm refuses arbitrary contrasts" ---
cat('\n--- apeglm with a list contrast (the Skill predicts an error) ---\n')
e <- try(lfcShrink(dds, contrast = list(c('condition_treated_vs_control',
                                          tail(resultsNames(dds), 1))), type = 'apeglm'),
         silent = TRUE)
cat(if (inherits(e, 'try-error')) paste('  ERROR:', as.character(e)) else '  no error raised\n')
cat('  Skill predicts: "type=\'apeglm\' shrinkage only for use with \'coef\'"\n')

cat('\n--- workaround (b): ashr, which accepts contrast= ---\n')
a <- try(lfcShrink(dds, contrast = list(c('condition_treated_vs_control',
                                          tail(resultsNames(dds), 1))), type = 'ashr'),
         silent = TRUE)
if (inherits(a, 'try-error')) cat('  ashr FAILED:', as.character(a)) else
  cat(sprintf('  ashr OK: %d genes padj<0.05; median |LFC| %.3f (unshrunk %.3f)\n',
              sum(a$padj < 0.05, na.rm = TRUE), median(abs(a$log2FoldChange), na.rm = TRUE),
              median(abs(r_m$log2FoldChange), na.rm = TRUE)))

cat('\n--- workaround (a): combined factor ~ 0 + group (SKILL.md Decision Tree) ---\n')
coldata$group <- factor(paste(coldata$sex, coldata$condition, sep = '_'))
dg <- DESeqDataSetFromMatrix(counts, coldata, design = ~ 0 + group)
dg <- dg[rowSums(counts(dg)) >= 10, ]
dg <- DESeq(dg, quiet = TRUE)
cat('  resultsNames:', paste(resultsNames(dg), collapse = ' | '), '\n')
rg <- results(dg, contrast = c('group', 'M_treated', 'M_control'), alpha = 0.05)
cat(sprintf('  treatment effect in males via ~0+group: %d genes padj<0.05, TP %d\n',
            sum(rg$padj < 0.05, na.rm = TRUE),
            length(intersect(rownames(rg)[which(rg$padj < 0.05)], tr))))
cat('  agrees with the summed-contrast LFCs? cor =',
    round(cor(rg$log2FoldChange, r_m$log2FoldChange, use = 'complete.obs'), 4), '\n')
sg <- try(lfcShrink(dg, coef = 'groupM_treated', type = 'apeglm'), silent = TRUE)
cat('  apeglm on a ~0+group coefficient:',
    if (inherits(sg, 'try-error')) paste('FAILED:', substr(as.character(sg), 1, 120)) else 'OK\n')

# --- the Skill's claim that name= and contrast= now agree (betaPrior section) ---
r_n <- results(dg, contrast = c('group', 'F_treated', 'F_control'))
r_c <- results(dg, contrast = list('groupF_treated', 'groupF_control'))
cat('\nname= vs contrast= for the same comparison, LFCs identical?',
    isTRUE(all.equal(r_n$log2FoldChange, r_c$log2FoldChange)), '\n')
cat('DONE\n')
