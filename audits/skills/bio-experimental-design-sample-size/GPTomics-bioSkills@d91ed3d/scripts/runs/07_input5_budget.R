# Input 5 (Stress / multi-part): fixed sequencing budget -- replicates vs depth, plus the
# 10-20 pct failure margin. Tests the SKILL.md 'Replicates vs Depth Under a Fixed Budget'
# rule at the SYNTHETIC study's planted dispersion (0.35).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(edgeR))
set.seed(20260916)
G <- 12000; FC <- 2.5; DISP <- 0.35
nDE <- 600; de <- 1:nDE
fcv <- rep(1, G); fcv[de] <- rep(c(FC, 1 / FC), length.out = nDE)
gmu <- exp(rnorm(G, 0, 0.8)); gmu <- gmu / mean(gmu)      # relative abundance, mean 1

run <- function(n, depth_scale) {        # depth_scale = mean counts per gene
  mu <- gmu * depth_scale
  cts <- cbind(matrix(rnbinom(G * n, mu = mu,       size = 1 / DISP), G, n),
               matrix(rnbinom(G * n, mu = mu * fcv, size = 1 / DISP), G, n))
  gr <- factor(rep(c("A", "B"), each = n)); des <- model.matrix(~gr); keep <- rowSums(cts) > 0
  y <- estimateDisp(calcNormFactors(DGEList(cts[keep, ], group = gr)), des)
  p <- rep(1, G); p[keep] <- glmQLFTest(glmQLFit(y, des), coef = 2)$table$PValue
  sig <- p.adjust(p, "BH") < 0.05
  c(power = mean(sig[de]), fdr = if (sum(sig)) sum(sig & fcv == 1) / sum(sig) else 0)
}

cfg <- data.frame(n = c(2, 3, 4, 6, 8, 12), depth = c(120, 80, 60, 40, 30, 20))
cat("Equal total sequencing spend (n x mean-counts-per-gene = 240), FC 1.5, dispersion 0.35:\n")
res <- do.call(rbind, lapply(seq_len(nrow(cfg)), function(i) {
  m <- colMeans(do.call(rbind, replicate(5, run(cfg$n[i], cfg$depth[i]), simplify = FALSE)))
  cat(sprintf("   n=%2d/group  mean counts/gene=%3d  -> power=%.3f  FDR=%.3f\n",
              cfg$n[i], cfg$depth[i], m["power"], m["fdr"])); flush.console()
  data.frame(cfg[i, ], t(m))
}))
write.csv(res, "runs/07_input5_budget.csv", row.names = FALSE)

cat("\nDepth-only ladder at fixed n=3 (does deeper sequencing rescue n=3?):\n")
for (d in c(20, 80, 320)) {
  m <- colMeans(do.call(rbind, replicate(5, run(3, d), simplify = FALSE)))
  cat(sprintf("   n=3, counts/gene=%3d -> power=%.3f\n", d, m["power"])); flush.console()
}
cat("\nReplicate-only ladder at fixed depth=40 counts/gene:\n")
for (n in c(3, 6, 12)) {
  m <- colMeans(do.call(rbind, replicate(5, run(n, 40), simplify = FALSE)))
  cat(sprintf("   n=%2d, counts/gene= 40 -> power=%.3f\n", n, m["power"])); flush.console()
}
