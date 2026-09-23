set.seed(424242)
library(lme4)
library(lmerTest)
one_sim <- function() {
  d <- expand.grid(run = factor(seq_len(8)), flask = seq_len(4), KEEP.OUT.ATTRS = FALSE)
  medium_by_run <- rep(c("A", "B"), each = 4)
  d$medium <- factor(medium_by_run[d$run])
  d$cell_line <- factor(rep(c("L1", "L1", "L2", "L2"), 8))
  d$growth <- 0.65 * (d$cell_line == "L2") + rnorm(8, 0, 2.0)[d$run] + rnorm(nrow(d), 0, 1.0)
  c(flat = coef(summary(lm(growth ~ medium + cell_line, data = d)))["mediumB", "Pr(>|t|)"],
    mixed = coef(summary(lmer(growth ~ medium + cell_line + (1 | run), data = d)))["mediumB", "Pr(>|t|)"])
}
p <- replicate(400, one_sim())
rates <- rowMeans(p < 0.05)
stopifnot(rates["flat"] > 0.15, rates["mixed"] >= 0.015, rates["mixed"] <= 0.10, rates["flat"] - rates["mixed"] > 0.10)
cat(sprintf("flat_type1=%.3f mixed_type1=%.3f\n", rates["flat"], rates["mixed"]))
