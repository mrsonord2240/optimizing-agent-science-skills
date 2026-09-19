# Re-audit: T3 (Skill Veto determinism gate) check for the fixed guard's model='naive'
# fallback path specifically (not previously verified this round), on the same
# crash-triggering dataset as demuxmix_crash_test3.R.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(demuxmix))

set.seed(90210)
n_cells <- 600
tag_names <- c('HX', 'HY', 'HZ')
n_tags <- length(tag_names)
classes <- sample(c('singlet', 'doublet', 'negative'), n_cells, replace = TRUE,
                   prob = c(0.55, 0.05, 0.40))
counts <- matrix(0L, nrow = n_cells, ncol = n_tags, dimnames = list(NULL, tag_names))
for (i in seq_len(n_cells)) {
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

run_naive <- function() {
  dmm <- demuxmix(as.matrix(hto_mat), model = 'naive')
  dmmClassify(dmm)$HTO
}

r1 <- suppressWarnings(run_naive())
r2 <- suppressWarnings(run_naive())
cat('model="naive" fallback identical across 2 runs on identical input:', all(r1 == r2), '\n')
