# Cross-cutting check (used by Inputs 1 and 2): the Skill's headline deliverable is
# "marginal power >= 0.80 at FDR 0.05". A researcher usually hears "80% chance of finding
# MY gene". Measure the gap: at the n where marginal power hits 0.80, what is the per-gene
# power in each expression decile?  SYNTHETIC data, planted dispersion 0.35, planted FC 1.5.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(edgeR))
set.seed(20260916)

G <- 12000; DISP <- 0.35; FC <- 1.5
nDE <- 600; de <- 1:nDE
fcv <- rep(1, G); fcv[de] <- rep(c(FC, 1 / FC), length.out = nDE)
gmu <- 40 * exp(rnorm(G, 0, 0.8))            # same generative model as the SYNTHETIC pilots
dec <- cut(rank(gmu[de]), breaks = quantile(rank(gmu[de]), probs = seq(0, 1, 0.2)),
           include.lowest = TRUE, labels = paste0("Q", 1:5))

run <- function(n) {
  cts <- cbind(matrix(rnbinom(G * n, mu = gmu,       size = 1 / DISP), G, n),
               matrix(rnbinom(G * n, mu = gmu * fcv, size = 1 / DISP), G, n))
  gr <- factor(rep(c("A", "B"), each = n)); des <- model.matrix(~gr); keep <- rowSums(cts) > 0
  y <- estimateDisp(calcNormFactors(DGEList(cts[keep, ], group = gr)), des)
  p <- rep(1, G); p[keep] <- glmQLFTest(glmQLFit(y, des), coef = 2)$table$PValue
  sig <- p.adjust(p, "BH") < 0.05
  list(marg = mean(sig[de]),
       fdr  = if (sum(sig)) sum(sig & fcv == 1) / sum(sig) else 0,
       byq  = tapply(sig[de], dec, mean))
}

cat("n/grp  marginal_power  realized_FDR | per-gene power by expression quintile (Q1=lowest)\n")
tab <- list()
for (n in c(4, 6, 8, 10, 12, 16, 20)) {
  reps <- replicate(4, run(n), simplify = FALSE)
  marg <- mean(sapply(reps, `[[`, "marg")); fdr <- mean(sapply(reps, `[[`, "fdr"))
  byq  <- rowMeans(sapply(reps, `[[`, "byq"))
  cat(sprintf("%4d   %.3f           %.3f        | %s\n", n, marg, fdr,
              paste(sprintf("%s=%.2f", names(byq), byq), collapse = "  "))); flush.console()
  tab[[as.character(n)]] <- c(n = n, marginal = marg, fdr = fdr, byq)
}
write.csv(do.call(rbind, tab), "runs/12_marginal_vs_pergene.csv", row.names = FALSE)
