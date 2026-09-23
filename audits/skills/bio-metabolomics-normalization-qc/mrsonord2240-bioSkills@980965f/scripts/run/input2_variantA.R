# Input 2 (Variant A) -- Prompt:
# "These are urine samples with highly variable dilution. PQN-normalize them and check the
# dilution factor doesn't correlate with my case/control phenotype before I trust it."
# REGRESSION TEST (post-fix): the fixed SKILL.md now documents the ACTUAL API path for the
# per-sample PQN factor (attr(normalized, 'flags')[, 'pqn_coef'] for a plain matrix) instead of
# a manual quotient recomputation, and replaces the fixed |r|>0.3 cutoff with a permutation test
# (999 label-shuffles, empirical p<0.05) per examples/normalize_data.R's updated guardrail.

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
library(pmp)

run_case <- function(confound_dilution_with_group) {
  d <- make_dataset(n_features = 100, n_bio = 40, n_qc_per_batch = 5, n_batches = 1, seed = 7)
  mat <- d$mat
  is_qc <- d$class == "QC"
  group <- d$group

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

  # --- FIXED path: documented attribute, not a manual recomputation ---
  factors <- attr(norm, "flags")[, "pqn_coef"]
  stopifnot(!is.null(factors), length(factors) == ncol(fmat))
  # Sanity: normalized * factor should reconstruct the input (pmp's own guarantee, per fix log).
  recon_err <- max(abs(sweep(norm, 2, factors, "*") - fmat), na.rm = TRUE)
  cat(sprintf("pqn_coef attribute present; max |reconstruction error| = %.2e (fix log claimed 2.8e-14)\n", recon_err))

  bio_idx <- which(!is_qc)
  cor_dil <- suppressWarnings(cor(factors[bio_idx], dil[bio_idx]))
  group_bin <- as.integer(group[bio_idx] == "case")
  cor_grp <- suppressWarnings(cor(factors[bio_idx], group_bin))

  # --- FIXED guardrail: permutation test instead of fixed |r|>0.3 ---
  set.seed(2)
  n_perm <- 999
  perm_cor <- replicate(n_perm, suppressWarnings(cor(factors[bio_idx], sample(group_bin))))
  perm_p <- (sum(abs(perm_cor) >= abs(cor_grp)) + 1) / (n_perm + 1)
  verdict <- if (perm_p < 0.05) "TRIPPED (permutation p<0.05)" else "ok (not distinguishable from label-shuffling noise)"
  cat(sprintf("[confound=%s] PQN factor vs true dilution r=%.3f | PQN factor vs group r=%.3f, perm_p=%.3f -> %s\n",
              confound_dilution_with_group, cor_dil, cor_grp, perm_p, verdict))
  invisible(list(cor_grp = cor_grp, perm_p = perm_p))
}

cat("Case 1: dilution independent of group (expected: ok; old fixed-r=0.3 cutoff falsely tripped here)\n")
r1 <- run_case(FALSE)
cat("\nCase 2: dilution confounded with group (expected: TRIPPED)\n")
r2 <- run_case(TRUE)
