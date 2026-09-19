# Re-audit (2026-09-19), round 3: same fresh near-constant-background dataset that
# reproduced the hard glm.nb crash (demuxmix_crash_test2.R). Now test, with the CORRECT
# clusterInit format (list of named 1/2 vectors, one per HTO row, from ?demuxmix):
#   (a) manual clusterInit alone -- does it avoid the crash?
#   (b) the Skill's fixed guard: tryCatch -> model='naive' on error
# to independently check the fixer's claim that clusterInit does NOT fix this crash but
# model='naive' does.
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
rna_counts <- rpois(n_cells, lambda = 150)

cat('=== (a) manual clusterInit alone, correct format ===\n')
cluster_init <- lapply(tag_names, function(tag) {
  v <- hto_mat[tag, ]
  as.integer(v > median(v)) + 1L   # 1 = below median (negative component), 2 = above (positive)
})
names(cluster_init) <- tag_names

res_a <- tryCatch({
  dmm <- demuxmix(as.matrix(hto_mat), rna = rna_counts, clusterInit = cluster_init)
  cat('clusterInit run completed without error\n')
  list(status = 'OK', obj = dmm)
}, error = function(e) {
  cat('CAUGHT ERROR with manual clusterInit:', conditionMessage(e), '\n')
  list(status = 'ERROR', msg = conditionMessage(e))
})
cat('Result (a) clusterInit alone:', res_a$status, '\n\n')

cat("=== (b) the Skill's fixed guard: tryCatch -> model='naive' ===\n")
dmm_b <- tryCatch(
  demuxmix(as.matrix(hto_mat), rna = rna_counts),
  error = function(e) {
    message('demuxmix regression fit failed (', conditionMessage(e), '); retrying with model="naive"')
    demuxmix(as.matrix(hto_mat), model = 'naive')
  }
)
calls_b <- dmmClassify(dmm_b)
cat('Result (b) guard/naive: completed. HTO call table:\n')
print(table(calls_b$HTO))

cat('\n=== SUMMARY ===\n')
cat('(a) manual clusterInit alone :', res_a$status, '\n')
cat('(b) guard -> model=naive     : OK (completed)\n')
