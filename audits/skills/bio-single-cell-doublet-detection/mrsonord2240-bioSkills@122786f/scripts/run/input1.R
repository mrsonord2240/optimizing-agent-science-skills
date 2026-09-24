# Input 1 (Canonical) - bio-single-cell-doublet-detection
# scDblFinder exactly as SKILL.md:76-85 prescribes: per-sample via samples=, raw counts,
# dbr inferred from cell count. Scored against the SYNTHETIC ground-truth doublet labels.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(scDblFinder); library(SingleCellExperiment); library(Seurat); library(Matrix)
})
cat('scDblFinder', as.character(packageVersion('scDblFinder')),
    '| Seurat', as.character(packageVersion('Seurat')), '\n')

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
tc <- read.csv(file.path(D, 'truth_cells.csv'))
rownames(tc) <- tc$cell_id
tc$true_doublet <- tc$true_doublet %in% c('True', 'TRUE', 'true', TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True', 'TRUE', 'true', TRUE)

# build one merged raw-count matrix with a sample_id column, as a researcher would after data-io
mats <- list()
for (s in paste0('S', 1:8)) {
  m <- Read10X(file.path(D, s, 'outs/filtered_feature_bc_matrix'))
  colnames(m) <- paste0(s, '_', colnames(m))
  mats[[s]] <- m
}
counts <- do.call(cbind, mats)
sample_id <- sub('_.*', '', colnames(counts))
cat('merged:', ncol(counts), 'cells across', length(unique(sample_id)), 'samples\n')

# --- SKILL.md Expected Doublet Rate rule, applied per lane ---
cat('\nrate rule (0.008 * recovered/1000) per lane:\n')
for (s in paste0('S', 1:8)) {
  n <- sum(sample_id == s)
  cat(sprintf('  %s n=%d -> expected %.2f%% (%d doublets); TRUE injected rate %.2f%%\n', s, n,
              100 * 0.008 * n / 1000, round(0.008 * n / 1000 * n),
              100 * mean(tc[colnames(counts)[sample_id == s], 'true_doublet'])))
}

# --- SKILL.md:76-85 verbatim (built from a counts matrix, the alternative the comment allows) ---
sce <- SingleCellExperiment(list(counts = counts))
sce$sample_id <- sample_id
set.seed(20260916)
sce <- scDblFinder(sce, samples = 'sample_id')
print(table(sce$scDblFinder.class))

truth <- tc[colnames(sce), 'true_doublet']
pred <- sce$scDblFinder.class == 'doublet'
tp <- sum(pred & truth); fp <- sum(pred & !truth); fn <- sum(!pred & truth)
cat(sprintf('\nPER-SAMPLE (samples=): called %d (%.2f%%)  TP=%d FP=%d FN=%d  recall=%.3f precision=%.3f\n',
            sum(pred), 100 * mean(pred), tp, fp, fn, tp / (tp + fn), tp / (tp + fp)))
rk <- rank(sce$scDblFinder.score); n1 <- sum(truth); n0 <- sum(!truth)
cat('AUC of scDblFinder.score vs truth:',
    round((sum(rk[truth]) - n1 * (n1 + 1) / 2) / (n1 * n0), 4), '\n')

# --- the error the Skill's first Common Errors row warns about: run on the MERGED object ---
sce2 <- SingleCellExperiment(list(counts = counts))
set.seed(20260916)
sce2 <- scDblFinder(sce2)                      # no samples= : the documented mistake
pred2 <- sce2$scDblFinder.class == 'doublet'
tp2 <- sum(pred2 & truth); fp2 <- sum(pred2 & !truth); fn2 <- sum(!pred2 & truth)
cat(sprintf('MERGED (no samples=): called %d (%.2f%%)  TP=%d FP=%d FN=%d  recall=%.3f precision=%.3f\n',
            sum(pred2), 100 * mean(pred2), tp2, fp2, fn2, tp2 / (tp2 + fn2), tp2 / (tp2 + fp2)))

# --- reproducibility: does a second run with the same seed agree? and without a seed? ---
set.seed(20260916); a <- scDblFinder(SingleCellExperiment(list(counts = counts)),
                                     samples = sample_id)$scDblFinder.class
set.seed(20260916); b <- scDblFinder(SingleCellExperiment(list(counts = counts)),
                                     samples = sample_id)$scDblFinder.class
cat('same seed, two runs agree on', sum(a == b), '/', length(a), 'cells\n')
c1 <- scDblFinder(SingleCellExperiment(list(counts = counts)), samples = sample_id)$scDblFinder.class
c2 <- scDblFinder(SingleCellExperiment(list(counts = counts)), samples = sample_id)$scDblFinder.class
cat('no seed set, two runs agree on', sum(c1 == c2), '/', length(c1), 'cells\n')

# --- Governing Principle: does doublet score track total counts? ---
cat('cor(scDblFinder.score, log10 total counts) =',
    round(cor(sce$scDblFinder.score, log10(colSums(counts))), 3), '\n')
tt <- tc[colnames(sce), 'true_cell_type']
cat('false-positive rate by true cell type (singlets called doublets):\n')
print(round(tapply(pred & !truth, tt, mean), 3))
cat('DONE\n')
