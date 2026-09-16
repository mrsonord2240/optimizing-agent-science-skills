# Input 6 (Scope boundary): proteomics DIA. The SKILL.md decision tree sends this to
# pwr::pwr.t.test "per protein, with missingness caveat". Does the n it returns deliver
# the target power once multiplicity across the proteome and MNAR missingness are present?
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(pwr))
set.seed(20260916)

cat("=== A. SKILL.md prescription, run as written ===\n")
for (d in c(0.8, 1.0, 1.2)) {
  r <- pwr.t.test(d = d, sig.level = 0.05, power = 0.80, type = "two.sample")
  cat(sprintf("   pwr.t.test(d=%.1f, sig.level=0.05, power=0.80) -> n = %.2f (ceil %d) per group\n",
              d, r$n, ceiling(r$n)))
}
cat("   SKILL.md assay table says proteomics practical minimum = 3, small effects = 6-10.\n")

NPROT <- 5000; PI0 <- 0.90
cat("\n=== B. What alpha does an FDR-controlled proteome-wide screen actually need? ===\n")
for (d in c(1.0, 1.2)) {
  n05 <- ceiling(pwr.t.test(d = d, sig.level = 0.05,       power = 0.8, type = "two.sample")$n)
  nbf <- ceiling(pwr.t.test(d = d, sig.level = 0.05/NPROT, power = 0.8, type = "two.sample")$n)
  cat(sprintf("   d=%.1f: alpha=0.05 -> n=%d ; Bonferroni alpha=1e-5 -> n=%d per group\n", d, n05, nbf))
}

cat("\n=== C. Simulation: 5000 proteins, 10 pct truly changed at d=1.2, 20 pct MNAR missing ===\n")
sim_prot <- function(n, d, mnar = 0.20) {
  nde <- round(NPROT * (1 - PI0)); de <- 1:nde
  delta <- rep(0, NPROT); delta[de] <- rep(c(d, -d), length.out = nde)
  abund <- rnorm(NPROT, 20, 2)
  X <- cbind(matrix(rnorm(NPROT * n, abund, 1), NPROT, n),
             matrix(rnorm(NPROT * n, abund + delta, 1), NPROT, n))
  thr <- quantile(X, mnar); X[X < thr] <- NA          # MNAR: lowest intensities drop out
  p <- apply(X, 1, function(r) {
    a <- r[1:n]; b <- r[(n + 1):(2 * n)]
    a <- a[!is.na(a)]; b <- b[!is.na(b)]
    if (length(a) < 2 || length(b) < 2) return(NA_real_)
    tryCatch(t.test(a, b)$p.value, error = function(e) NA_real_)
  })
  ok <- !is.na(p); q <- rep(1, NPROT); q[ok] <- p.adjust(p[ok], "BH")
  sig <- q < 0.05
  c(power_marginal = mean(sig[de]),
    fdr = if (sum(sig)) sum(sig & delta == 0) / sum(sig) else 0,
    testable = mean(ok),
    pow_uncorr = mean(p[de] < 0.05, na.rm = TRUE))
}
for (n in c(3, 6, 10, 17, 26)) {
  m <- colMeans(do.call(rbind, replicate(5, sim_prot(n, 1.2), simplify = FALSE)), na.rm = TRUE)
  cat(sprintf("   n=%2d/group: BH power=%.3f realized FDR=%.3f testable=%.2f (uncorrected p<0.05 power=%.3f)\n",
              n, m["power_marginal"], m["fdr"], m["testable"], m["pow_uncorr"])); flush.console()
}
