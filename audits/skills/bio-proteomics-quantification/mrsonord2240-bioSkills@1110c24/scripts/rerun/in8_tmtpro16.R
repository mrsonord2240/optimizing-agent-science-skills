# Quant Input 8 (NEW): TMTpro 16plex reporter extraction + impurity correction, following block b04 with the plex changed.
# SYNTHETIC reporter matrix (no TMTpro mzML available): true channel intensities mixed by a known bleed matrix.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(MSnbase))
cat('TMT16 reporter set exists:', exists('TMT16'), '| names:', paste(reporterNames(TMT16), collapse = ','), '\n')
cat('TMT18 reporter set exists:', exists('TMT18'), '\n')
imp16 <- tryCatch(makeImpuritiesMatrix(x = 16, edit = FALSE), error = function(e) { cat("makeImpuritiesMatrix(x = 16, edit = FALSE) ERROR:", conditionMessage(e), "
"); NULL })
cat("template returned:", !is.null(imp16), "
")
set.seed(16)
n <- 300
truth <- matrix(2^rnorm(n * 16, 14, 1.5), n, 16, dimnames = list(paste0('psm', 1:n), reporterNames(TMT16)))
B <- diag(0.92, 16)                                        # synthetic lot bleed: 5% to +1 Da neighbour (2 positions), 2% to -1 Da, 1% to +2 Da
for (i in 1:16) { if (i + 2 <= 16) B[i, i + 2] <- 0.05; if (i - 2 >= 1) B[i, i - 2] <- 0.02; if (i + 4 <= 16) B[i, i + 4] <- 0.01 }
obs <- truth %*% B; colnames(obs) <- colnames(truth)   # observed reporter = true signal bled across channels
es <- new('MSnSet', exprs = obs)
rel <- function(m) m / rowSums(m)
err <- function(m) median(abs(rel(m) - rel(truth)))
c_id <- obs
Bt <- t(B); rownames(Bt) <- paste('% reporter', colnames(obs)); colnames(Bt) <- colnames(obs)
c_ok <- exprs(purityCorrect(es, Bt))
cat(sprintf('median |relative error|: uncorrected %.4f | (no template available, uncorrected) %.4f | purityCorrect(true lot matrix) %.4f\n', err(obs), err(c_id), err(c_ok)))
