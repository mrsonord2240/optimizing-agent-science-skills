# Re-audit (2026-09-19): independently reproduce the demuxmix glm.nb crash on FRESH
# underdispersed synthetic HTO background data (different seed from the fixer's), then
# test (a) the fixed tryCatch -> model='naive' guard, and (b) whether a manual clusterInit
# alone recovers -- the fixer's log claims clusterInit does NOT fix this specific crash,
# only model='naive' does. That is a checkable claim; test it directly.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(demuxmix))

set.seed(4271)

n_cells <- 700
tag_names <- c('HX', 'HY', 'HZ')
n_tags <- length(tag_names)

# Underdispersed (near-Poisson / sub-Poisson) background: low, tightly-controlled counts
# with an occasional strong signal boost for true singlets. Real ambient HTO background is
# usually overdispersed (NB); here we deliberately build background with variance <= mean
# (rpois, i.e. exactly Poisson-dispersed, which is what triggers demuxmix's own
# underdispersion warning in its glm.nb per-tag fit).
classes <- sample(c('singlet', 'doublet', 'negative'), n_cells, replace = TRUE,
                   prob = c(0.55, 0.05, 0.40))
counts <- matrix(0L, nrow = n_cells, ncol = n_tags, dimnames = list(NULL, tag_names))
for (i in seq_len(n_cells)) {
  bg <- rpois(n_tags, lambda = 6)  # Poisson background -> underdispersed relative to NB fit
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

cat('=== Attempt 1: raw demuxmix() call (expect crash or warning) ===\n')
res1 <- tryCatch({
  dmm <- demuxmix(as.matrix(hto_mat), rna = rna_counts)
  list(status = 'OK', obj = dmm)
}, error = function(e) {
  cat('CAUGHT ERROR:', conditionMessage(e), '\n')
  list(status = 'ERROR', msg = conditionMessage(e))
}, warning = function(w) {
  cat('CAUGHT WARNING (as warning, not error):', conditionMessage(w), '\n')
  list(status = 'WARNING', msg = conditionMessage(w))
})
cat('Attempt 1 status:', res1$status, '\n\n')

cat('=== Attempt 2: manual clusterInit alone (fixer claims this does NOT avoid the crash) ===\n')
res2 <- tryCatch({
  km <- kmeans(t(log1p(hto_mat)), centers = n_tags + 1)$cluster
  dmm <- demuxmix(as.matrix(hto_mat), rna = rna_counts, clusterInit = km)
  list(status = 'OK', obj = dmm)
}, error = function(e) {
  cat('CAUGHT ERROR with clusterInit:', conditionMessage(e), '\n')
  list(status = 'ERROR', msg = conditionMessage(e))
})
cat('Attempt 2 (clusterInit) status:', res2$status, '\n\n')

cat("=== Attempt 3: the Skill's fixed guard -- tryCatch -> model='naive' ===\n")
dmm3 <- tryCatch(
  demuxmix(as.matrix(hto_mat), rna = rna_counts),
  error = function(e) {
    message('demuxmix regression fit failed (', conditionMessage(e), '); retrying with model="naive"')
    demuxmix(as.matrix(hto_mat), model = 'naive')
  }
)
calls3 <- dmmClassify(dmm3)
cat('Attempt 3 (guard) completed. HTO call table:\n')
print(table(calls3$HTO))
cat('\nSummary: attempt1=', res1$status, ' attempt2(clusterInit)=', res2$status,
    ' attempt3(guard/naive)=completed\n', sep='')
