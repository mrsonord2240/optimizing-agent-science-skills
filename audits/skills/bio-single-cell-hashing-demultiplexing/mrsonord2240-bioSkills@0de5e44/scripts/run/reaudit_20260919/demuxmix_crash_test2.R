# Re-audit (2026-09-19), round 2: my first underdispersed dataset only produced a
# warning, not the hard glm.nb error the original audit/fixer found. Try harder to
# reproduce the actual crash: even more underdispersed (near-constant) background,
# and inspect demuxmix::clusterInit's real expected format before re-testing it.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(demuxmix))

cat('=== clusterInit argument docs ===\n')
print(args(demuxmix))
cat('\n')

set.seed(90210)
n_cells <- 600
tag_names <- c('HX', 'HY', 'HZ')
n_tags <- length(tag_names)

classes <- sample(c('singlet', 'doublet', 'negative'), n_cells, replace = TRUE,
                   prob = c(0.55, 0.05, 0.40))
counts <- matrix(0L, nrow = n_cells, ncol = n_tags, dimnames = list(NULL, tag_names))
for (i in seq_len(n_cells)) {
  # Near-constant background (very low variance, well below Poisson) -- this is a
  # stronger underdispersion stress than plain Poisson.
  bg <- pmax(0L, 6L + sample(-1:1, n_tags, replace = TRUE))
  counts[i, ] <- bg
  if (classes[i] == 'singlet') {
    t <- sample(n_tags, 1)
    counts[i, t] <- counts[i, t] + rpois(1, 140)
  } else if (classes[i] == 'doublet') {
    two <- sample(n_tags, 2)
    counts[i, two] <- counts[i, two] + rpois(2, 140)
  }
}
hto_mat <- t(counts)
rna_counts <- rpois(n_cells, lambda = 150)

cat('=== Attempt 1 (no warning/error suppression): raw demuxmix() ===\n')
out1 <- tryCatch({
  dmm <- demuxmix(as.matrix(hto_mat), rna = rna_counts)
  cat('demuxmix() returned normally (possibly with warnings printed above)\n')
  'OK'
}, error = function(e) {
  cat('CAUGHT ERROR:', conditionMessage(e), '\n')
  'ERROR'
})
cat('Attempt 1 result:', out1, '\n\n')
