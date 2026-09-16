# Input 1 (Canonical) - bio-single-cell-differential-abundance
# propeller exactly as SKILL.md:149-154, on the SYNTHETIC 8-sample PBMC set where the ground
# truth is known: NK cells were injected at 6% in control and ~13% in treated, every other
# type rescaled. Nothing else changed. So the correct answer is "NK up, and the apparent
# depletions elsewhere are the simplex constraint, not biology".
# The Skill's "never recommended" per-cluster t-test is run alongside for contrast.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(speckle); library(limma); library(Seurat)})
cat('speckle', as.character(packageVersion('speckle')), '| limma',
    as.character(packageVersion('limma')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', TRUE)
ss <- read.csv(file.path(D, 'sample_sheet.csv')); rownames(ss) <- ss$sample
tc <- tc[!tc$true_doublet & !tc$true_low_quality, ]
tc$condition <- ss[tc$sample, 'condition']
tc$batch <- ss[tc$sample, 'batch']
cat(nrow(tc), 'clean cells;', length(unique(tc$sample)), 'samples\n')

prop <- prop.table(table(tc$sample, tc$true_cell_type), 1)
cat('\nTRUE cell-type proportions per sample (%):\n')
print(round(100 * prop, 1))
cat('\nmean proportion by condition (%):\n')
m <- aggregate(as.data.frame.matrix(prop), by = list(cond = ss[rownames(prop), 'condition']), mean)
print(round(100 * m[, -1], 2))
cat('GROUND TRUTH: only NK cells were changed (0.06 -> ~0.13); every other type was rescaled.\n')

# --- SKILL.md:149-154, verbatim ---
out <- propeller(clusters = tc$true_cell_type, sample = tc$sample, group = tc$condition)
cat('\npropeller (arcsin-sqrt + limma), SKILL.md:152:\n')
num <- c('PropMean.control', 'PropMean.treated', 'PropRatio', 'Tstatistic', 'P.Value', 'FDR')
num <- intersect(num, colnames(out))
cat('  columns returned:', paste(colnames(out), collapse = ', '), '
')
print(cbind(cluster = as.character(out[[1]]), round(out[, num], 5)))
cat('significant at FDR < 0.05:', paste(rownames(out)[out$FDR < 0.05], collapse = ', '), '\n')

# --- logit transform, the alternative the Skill names in the same sentence ---
out2 <- propeller(clusters = tc$true_cell_type, sample = tc$sample, group = tc$condition,
                  transform = 'logit')
cat('propeller with transform="logit":',
    paste(rownames(out2)[out2$FDR < 0.05], collapse = ', '), '\n')

# --- the method the Skill says is "never recommended as the primary test" ---
cat('\nper-cluster t-test on raw proportions (SKILL.md calls this invalid):\n')
pm <- as.data.frame.matrix(prop)
cond <- ss[rownames(pm), 'condition']
tt <- t(sapply(colnames(pm), function(ct) {
  x <- pm[cond == 'treated', ct]; y <- pm[cond == 'control', ct]
  r <- t.test(x, y)
  c(mean_ctrl = mean(y), mean_trt = mean(x), p = r$p.value)
}))
tt <- as.data.frame(tt); tt$fdr <- p.adjust(tt$p, 'BH')
print(round(tt, 5))
cat('t-test significant at FDR < 0.05:', paste(rownames(tt)[tt$fdr < 0.05], collapse = ', '), '\n')
cat('  -> only ONE type actually changed. Extra calls here are the simplex artifact the Skill\n')
cat('     describes; the count of false positives is the measurement that matters.\n')

# correlation structure the Governing Principle claims
cm <- cor(pm)
diag(cm) <- NA
cat(sprintf('\nmean pairwise correlation between cell-type proportions across the 8 samples: %.3f\n',
            mean(cm, na.rm = TRUE)))
cat(sprintf('correlation of NK proportion with the mean of all others: %.3f\n',
            cor(pm[, 'NK cells'], rowMeans(pm[, colnames(pm) != 'NK cells']))))
cat('DONE\n')
