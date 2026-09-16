# Reconciling the two numbers the Skill puts side by side:
#   (a) its Quantitative Thresholds table: ">=6 biological replicates for bulk RNA-seq DE"
#   (b) its own worked example (fc=1.5, disp=0.2, FDR .05, marginal power .80), whose
#       ssizeRNA answer is n=74/group -- visible only once maxN is raised from 30 to 200.
# Arm A plants EVERY DE gene at exactly 1.5x (what the worked example asks for).
# Arm B plants a realistic fold-change spectrum (what Schurch 2016 actually recovered).
# SYNTHETIC counts, heterogeneous means (base 40), planted dispersion 0.20.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(edgeR))
set.seed(20260916)
G <- 12000; DISP <- 0.20; nDE <- 600; de <- 1:nDE
gmu <- 40 * exp(rnorm(G, 0, 0.8))

fc_uniform <- rep(1, G); fc_uniform[de] <- rep(c(1.5, 1 / 1.5), length.out = nDE)
set.seed(7); spec <- exp(rnorm(nDE, log(1.6), 0.55))        # median 1.6, long tail
fc_spectrum <- rep(1, G); fc_spectrum[de] <- ifelse(seq_len(nDE) %% 2 == 0, spec, 1 / spec)

run <- function(n, fcv) {
  cts <- cbind(matrix(rnbinom(G * n, mu = gmu,       size = 1 / DISP), G, n),
               matrix(rnbinom(G * n, mu = gmu * fcv, size = 1 / DISP), G, n))
  gr <- factor(rep(c("A", "B"), each = n)); des <- model.matrix(~gr); keep <- rowSums(cts) > 0
  y <- estimateDisp(calcNormFactors(DGEList(cts[keep, ], group = gr)), des)
  p <- rep(1, G); p[keep] <- glmQLFTest(glmQLFit(y, des), coef = 2)$table$PValue
  sig <- p.adjust(p, "BH") < 0.05
  c(power = mean(sig[de]), fdr = if (sum(sig)) sum(sig & fcv == 1) / sum(sig) else 0)
}
cat(sprintf("Arm B fold-change spectrum: median %.2f, 90th pct %.2f, max %.2f\n",
            median(spec), quantile(spec, .9), max(spec)))
cat("\n  n/grp | Arm A (all DE at 1.5x)      | Arm B (realistic FC spectrum)\n")
for (n in c(6, 12, 20, 30, 50, 74, 100)) {
  a <- colMeans(do.call(rbind, replicate(2, run(n, fc_uniform),  simplify = FALSE)))
  b <- colMeans(do.call(rbind, replicate(2, run(n, fc_spectrum), simplify = FALSE)))
  cat(sprintf("  %5d | power %.3f  FDR %.3f      | power %.3f  FDR %.3f\n",
              n, a["power"], a["fdr"], b["power"], b["fdr"])); flush.console()
}
