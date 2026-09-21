# FRASER 2.6.1 (as-drop): block 01 verbatim, then block 08 (tissue-mismatch check), block 09 (Choosing q), then the
# Reproducibility claim: AE fits twice with set.seed()+default BPPARAM vs BPPARAM = SerialParam(RNGseed = 1).
suppressPackageStartupMessages({library(FRASER); library(BiocParallel)})
a <- commandArgs(TRUE); setwd(a[1]); blk <- a[2]

unlink("fraser_workdir", recursive = TRUE)
source(file.path(blk, "01_r.R"), echo = FALSE)
cat("== block 08 (mismatch check) printed:\n"); source(file.path(blk, "08_r.R"), print.eval = TRUE, echo = FALSE)
cat("== block 09 (Choosing q):\n")
pdf("q_plots.pdf")
src09 <- readLines(file.path(blk, "09_r.R")); print(src09)
for (i in seq_along(src09)) {
  ln <- src09[i]; if (grepl("^#", ln)) next
  r <- try(withVisible(eval(parse(text = ln))), silent = TRUE)
  if (inherits(r, "try-error")) cat("LINE", i, "ERROR:", conditionMessage(attr(r, "condition")), "\n")
  else if (r$visible) { cat("LINE", i, "value: "); print(if (inherits(r$value, "gg")) class(r$value) else r$value) }
  if (i %in% c(1, 4) && !inherits(r, 'try-error')) { fds <- r$value; cat('   bestQ after line', i, ':', bestQ(fds, 'jaccard'), "\n") }
}
dev.off()
# NOTE: block 09 line 3 reassigns fds via the grid search (useOHT=FALSE); the loop above only tracks line 1's value; take bestQ from both
# ---- reproducibility claim ----
fds0 <- fds
fit_ae <- function(bp, seed = NULL) { if (!is.null(seed)) set.seed(seed); f <- suppressWarnings(FRASER(fds0, q = c(jaccard = 5), implementation = "AE", BPPARAM = bp)); pVals(f, type = "jaccard") }
nd <- function(x, y) sum(abs(x - y) > 1e-6, na.rm = TRUE)
p1 <- fit_ae(MulticoreParam(4)); p2 <- fit_ae(MulticoreParam(4)); cat("AE no seed: cells differing >1e-6:", nd(p1, p2), "of", length(p1), "\n")
p3 <- fit_ae(MulticoreParam(4), seed = 1); p4 <- fit_ae(MulticoreParam(4), seed = 1); cat("AE set.seed(1) only: differing:", nd(p3, p4), "\n")
p5 <- fit_ae(SerialParam(RNGseed = 1)); p6 <- fit_ae(SerialParam(RNGseed = 1)); cat("AE SerialParam(RNGseed=1): differing:", nd(p5, p6), "\n")
q1 <- FRASER(fds0, q = c(jaccard = 5), implementation = "PCA", BPPARAM = MulticoreParam(4)); q2 <- FRASER(fds0, q = c(jaccard = 5), implementation = "PCA", BPPARAM = MulticoreParam(4))
cat("PCA q=5 twice: differing:", nd(pVals(q1, type = "jaccard"), pVals(q2, type = "jaccard")), "\n")
