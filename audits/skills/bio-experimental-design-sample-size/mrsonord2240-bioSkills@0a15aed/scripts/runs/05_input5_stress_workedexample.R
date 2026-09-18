# Input 5 (Stress) — direct regression of P0-2 (the worked example returning NA/NaN).
# Prompt: "Just run the Skill's own worked example so I can see what a real answer looks
# like before I plug in my own numbers."
#
# Runs the SHIPPED examples/sample_size_estimation.R VERBATIM from a copy in this
# audit's own scratch area (never executed in place inside F:\OpenScience\external\),
# then independently checks its headline n against a ground-truth planted-effect
# simulation (edgeR QL), since "exits 0 and prints a number" is not itself evidence the
# number is right -- the M4 gate requires positive evidence, not just no error.
cat("=== Running the shipped worked example verbatim ===\n")
source("skill/examples/sample_size_estimation.R", echo = FALSE)

cat("\n\n=== Independent ground truth: planted-effect simulation (edgeR QL) ===\n")
suppressPackageStartupMessages(library(edgeR))
set.seed(20260918)
simulate_and_test <- function(n_per_group, ngenes = 2000, p_de = 0.05, fc = 1.5,
                               mu = 200, disp = 0.2, nsim = 8) {
  size <- 1 / disp
  de_idx <- seq_len(round(ngenes * p_de))
  powers <- numeric(nsim)
  for (s in seq_len(nsim)) {
    group <- factor(rep(c("A", "B"), each = n_per_group))
    mu_mat <- matrix(mu, nrow = ngenes, ncol = 2 * n_per_group)
    mu_mat[de_idx, group == "B"] <- mu * fc
    counts <- matrix(rnbinom(ngenes * 2 * n_per_group, mu = mu_mat, size = size),
                      nrow = ngenes)
    y <- DGEList(counts = counts, group = group)
    y <- calcNormFactors(y)
    design <- model.matrix(~ group)
    y <- estimateDisp(y, design)
    fit <- glmQLFit(y, design)
    qlf <- glmQLFTest(fit, coef = 2)
    padj <- p.adjust(qlf$table$PValue, method = "BH")
    powers[s] <- mean(padj[de_idx] < 0.05)
  }
  mean(powers)
}
for (n in c(6, 20, 47, 74)) {
  p <- simulate_and_test(n)
  cat(sprintf("edgeR QL ground truth at n=%d/group (fc=1.5, disp=0.2, mu=200): mean power across DE genes = %.3f\n", n, p))
}
cat("\nInterpretation: the worked example's headline n (printed above, expected mid-40s per the\n",
    "fix log) should land where ground-truth power crosses ~0.80 in the table above.\n")
