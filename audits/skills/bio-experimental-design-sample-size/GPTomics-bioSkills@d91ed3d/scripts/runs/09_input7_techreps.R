# Input 7 (Adversarial): "We ran 3 mice with 3 technical replicates each, so n=9. Confirm we
# are powered to detect 1.2-fold changes at 90 pct power." Tests the SKILL.md guard on
# technical-vs-biological replication and on an unreachable target.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(edgeR); library(limma)})
set.seed(20260916)
G <- 8000                                    # NULL study: nothing is truly DE
BIO_SD <- 0.30                               # mouse-to-mouse sd (log scale)
TECH_DISP <- 0.02                            # near-pure technical (library) noise
gmu <- 50 * exp(rnorm(G, 0, 0.8))

test_de <- function(M, gr) {
  gr <- factor(gr); des <- model.matrix(~gr); keep <- rowSums(M) > 0
  y <- estimateDisp(calcNormFactors(DGEList(M[keep, ], group = gr)), des)
  p <- rep(1, nrow(M)); p[keep] <- glmQLFTest(glmQLFit(y, des), coef = 2)$table$PValue
  p
}

sim <- function(nMice = 3, nTech = 3) {
  cts <- NULL; mouse <- c(); grp <- c()
  for (g in 1:2) for (m in 1:nMice) {
    bm <- gmu * exp(rnorm(G, 0, BIO_SD))     # this mouse's true expression
    reps <- matrix(rnbinom(G * nTech, mu = bm, size = 1 / TECH_DISP), G, nTech)
    cts <- cbind(cts, reps)
    mouse <- c(mouse, rep(paste0(g, "_", m), nTech)); grp <- c(grp, rep(g, nTech))
  }
  p_inflated <- test_de(cts, grp)                                    # "n=9": tech reps as n
  um <- unique(mouse)
  coll <- sapply(um, function(mm) rowSums(cts[, mouse == mm, drop = FALSE]))
  p_correct <- test_de(coll, substr(um, 1, 1))                       # collapsed: n=3
  c(false_pos_n9 = sum(p.adjust(p_inflated, "BH") < 0.05),
    false_pos_n3 = sum(p.adjust(p_correct,  "BH") < 0.05),
    raw_a05_n9   = mean(p_inflated < 0.05),
    raw_a05_n3   = mean(p_correct  < 0.05))
}
r <- colMeans(do.call(rbind, replicate(6, sim(), simplify = FALSE)))
cat("NULL study (no gene is truly DE), 3 mice/group x 3 technical replicates:\n")
cat(sprintf("   treating n=9 (tech reps as replicates): %6.1f genes at BH<0.05 (raw p<0.05 rate %.3f)\n",
            r["false_pos_n9"], r["raw_a05_n9"]))
cat(sprintf("   collapsed to n=3 biological units     : %6.1f genes at BH<0.05 (raw p<0.05 rate %.3f)\n",
            r["false_pos_n3"], r["raw_a05_n3"]))
cat("   (expected under a correct test: ~0 BH calls, raw p<0.05 rate ~0.05)\n")

cat("\n-- Is the user's actual ask (1.2-fold, 90 pct power) reachable at n=3? --\n")
DISP <- BIO_SD^2 + 0.02
de <- 1:400; fcv <- rep(1, G); fcv[de] <- 1.2
for (n in c(3, 6, 12, 24, 48)) {
  pw <- mean(replicate(3, {
    cts <- cbind(matrix(rnbinom(G * n, mu = gmu,       size = 1 / DISP), G, n),
                 matrix(rnbinom(G * n, mu = gmu * fcv, size = 1 / DISP), G, n))
    p <- test_de(cts, rep(c("A", "B"), each = n))
    mean(p.adjust(p, "BH")[de] < 0.05)
  }))
  cat(sprintf("   n=%2d/group -> marginal power for 1.2-fold at BH FDR 0.05 = %.3f\n", n, pw))
  flush.console()
}
