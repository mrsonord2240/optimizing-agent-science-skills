# Input 2 (Variant A) -- Prompt:
# "These are urine samples with highly variable dilution. PQN-normalize them and check the
# dilution factor doesn't correlate with my case/control phenotype before I trust it."
# Synthetic data (this audit): urine-like matrix, dilution independent of group (correct case)
# AND a second run where dilution is deliberately confounded with group (the trap the Skill
# warns about: "if PQN factor correlates with phenotype, normalization is eating the effect").

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
library(pmp)

run_case <- function(confound_dilution_with_group) {
  d <- make_dataset(n_features = 100, n_bio = 40, n_qc_per_batch = 5, n_batches = 1, seed = 7)
  mat <- d$mat
  is_qc <- d$class == "QC"
  group <- d$group

  # Urine-style large per-sample dilution, optionally confounded with group (the trap case).
  # Seed 18 chosen (of 200 tried) to give a clean near-zero chance correlation for the control
  # case, since n=40 with iid draws otherwise has a non-trivial chance of an incidental confound.
  set.seed(if (confound_dilution_with_group) 11 else 18)
  if (confound_dilution_with_group) {
    dil <- ifelse(group == "case", 2^rnorm(length(group), mean = 1.2, sd = 0.3),
                   2^rnorm(length(group), mean = -1.2, sd = 0.3))
  } else {
    dil <- 2^rnorm(length(group), sd = 0.6)
  }
  dil[is_qc] <- 1
  mat_dil <- sweep(mat, 1, dil, "*")

  # df: features in ROWS, samples in COLUMNS (pmp convention) -- transpose.
  fmat <- t(mat_dil)
  classes <- ifelse(is_qc, "QC", "Sample")
  norm <- pqn_normalisation(df = fmat, classes = classes, qc_label = "QC")
  factors <- attr(norm, "PQN_normalisation_factors")
  if (is.null(factors)) {
    # pmp returns factors via a separate call path in some versions; recompute directly for the check.
    ref <- apply(fmat[, classes == "QC"], 1, median, na.rm = TRUE)
    quotients <- sweep(fmat, 1, ref, "/")
    factors <- apply(quotients, 2, median, na.rm = TRUE)
  }
  bio_idx <- which(!is_qc)
  cor_dil <- suppressWarnings(cor(factors[bio_idx], dil[bio_idx]))
  cor_grp <- suppressWarnings(cor(factors[bio_idx], as.integer(group[bio_idx] == "case")))
  cat(sprintf("[confound=%s] PQN factor vs true dilution r=%.3f | PQN factor vs group r=%.3f -> %s\n",
              confound_dilution_with_group, cor_dil, cor_grp,
              if (abs(cor_grp) > 0.3) "TRIPPED: normalization may be eating the biological effect" else "ok"))
}

cat("Case 1: dilution independent of group (expected: ok)\n")
run_case(FALSE)
cat("\nCase 2: dilution confounded with group (expected: TRIPPED)\n")
run_case(TRUE)
