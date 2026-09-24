# Input 2: funnel + Egger + trim-and-fill + contour on SYNTHETIC k=30 data, planted publication bias. Seeded.
suppressMessages(library(metafor))
D <- "F:/OpenScience/audits/bio-data-visualization-forest-funnel-plots"
set.seed(20260920)
sim <- function(biased) {
  out <- NULL
  while (is.null(out) || nrow(out) < 30) {
    se <- runif(1, 0.08, 0.45); th <- rnorm(1, 0.25, 0.2); y <- rnorm(1, th, se)
    sig <- abs(y/se) > 1.96 & y > 0
    keep <- if (!biased) TRUE else (sig || runif(1) < 0.15)
    if (keep) out <- rbind(out, data.frame(yi = y, sei = se))
  }
  out$vi <- out$sei^2; out$slab <- paste0("S", seq_len(nrow(out))); out }
biased <- sim(TRUE); sym <- sim(FALSE)
write.csv(biased, file.path(D, "data/synthetic_biased_k30.csv"), row.names = FALSE)
write.csv(sym,    file.path(D, "data/synthetic_symmetric_k30.csv"), row.names = FALSE)
for (nm in c("biased", "sym")) {
  d <- get(nm)
  studies <- d
  res <- rma(yi = yi, vi = vi, data = d, slab = slab, method = "REML")
  cat(sprintf("\n=== %s: b=%.6f tau2=%.6f I2=%.2f\n", nm, res$b, res$tau2, res$I2))
  # ---- SKILL.md funnel block ----
  png(file.path(D, sprintf("figs/in2_%s_funnel.png", nm)), width = 800, height = 650, res = 110)
  fr <- funnel(res, xlab = 'log(OR)', refline = res$b)
  dev.off()
  cat("funnel() returned points equal (yi,sei)?", isTRUE(all.equal(sort(fr$x), sort(d$yi))), isTRUE(all.equal(sort(fr$y), sort(d$sei))), "\n")
  eg <- regtest(res, model = 'lm', predictor = 'sei'); print(eg)
  cat(sprintf("EGGER t=%.4f df=%d p=%.5f\n", eg$zval, eg$dfs, eg$pval))
  res_tf <- trimfill(res)
  cat(sprintf("TF k0=%d  orig b=%.4f  adj b=%.4f  side=%s\n", res_tf$k - res$k, res$b, res_tf$b, res_tf$side))
  png(file.path(D, sprintf("figs/in2_%s_forest_tf.png", nm)), width = 900, height = 1000, res = 100)
  forest(res_tf)
  dev.off()
  png(file.path(D, sprintf("figs/in2_%s_funnel_tf.png", nm)), width = 800, height = 650, res = 110)
  funnel(res_tf)
  dev.off()
  # ---- SKILL.md contour block ----
  png(file.path(D, sprintf("figs/in2_%s_contour.png", nm)), width = 800, height = 650, res = 110)
  funnel(res, level = c(90, 95, 99), shade = c('white', 'gray55', 'gray75'),
         refline = 0, legend = TRUE)
  dev.off()
}
