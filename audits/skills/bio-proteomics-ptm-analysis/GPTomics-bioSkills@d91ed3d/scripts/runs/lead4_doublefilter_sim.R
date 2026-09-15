.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Lead 4: the Skill's regulated filter (adj.p < 0.05 & |log2FC| > 1) vs a threshold test (limma treat, lfc = 1).
# SYNTHETIC simulation: 2000 sites, 4 vs 4, 70% exact nulls, 30% true |log2FC| ~ U(0.2, 2.0); site SD ~ scaled chi.
# 'False' for a '> 2-fold regulated' claim = true |log2FC| <= 1.
suppressPackageStartupMessages(library(limma))
set.seed(20260911)
one <- function() {
  n <- 2000; g <- factor(rep(c('C', 'T'), each = 4))
  eff <- ifelse(runif(n) < 0.3, sample(c(-1, 1), n, TRUE) * runif(n, 0.2, 2.0), 0)
  sd <- sqrt(0.25 * 4 / rchisq(n, 4))
  y <- matrix(rnorm(n * 8, 0, rep(sd, 8)), n) + outer(eff, as.numeric(g == 'T'))
  d <- model.matrix(~g); f <- eBayes(lmFit(y, d))
  # unmoderated per-site t-test (groupComparisonPTM default moderated = FALSE)
  tt <- apply(y, 1, function(v) t.test(v[5:8], v[1:4], var.equal = TRUE)$p.value)
  fc <- rowMeans(y[, 5:8]) - rowMeans(y[, 1:4])
  dbl_t <- p.adjust(tt, 'BH') < 0.05 & abs(fc) > 1
  dbl_mod <- p.adjust(f$p.value[, 2], 'BH') < 0.05 & abs(fc) > 1
  tr <- treat(lmFit(y, d), lfc = 1); tr_call <- p.adjust(tr$p.value[, 2], 'BH') < 0.05
  fdp <- function(call) if (sum(call)) c(sum(call & abs(eff) <= 1) / sum(call), sum(call & eff == 0) / sum(call), sum(call)) else c(0, 0, 0)
  rbind(double_filter_ttest = fdp(dbl_t), double_filter_moderated = fdp(dbl_mod), treat_lfc1 = fdp(tr_call))
}
res <- replicate(20, one())
out <- apply(res, c(1, 2), mean)
colnames(out) <- c('FDP_vs_2fold_claim', 'FDP_exact_nulls', 'mean_calls')
print(round(out, 3))
