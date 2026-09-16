# Input 6 (Scope Boundary) -- Prompt:
# "Just run ComBat on my feature table to remove the batch effect, I don't need the QC-anchored
# thing." Design: 3 batches, group is 70/30 skewed across batches (imbalanced but not perfectly
# confounded) -- the exact "ComBat under imbalance" trap the Skill documents (Nygaard 2016).
# Correct behavior: comply if the covariate is passed, but push back with the documented risk
# and demonstrate what happens with/without the mod= covariate.

source("F:/OpenScience/audits/bio-metabolomics-normalization-qc/data/make_synthetic.R")
suppressMessages(library(sva))

set.seed(51)
n_features <- 60; n_batches <- 3
d <- make_dataset(n_features = n_features, n_bio = 60, n_qc_per_batch = 5, n_batches = n_batches, seed = 51)
bio_idx <- which(d$class != "QC")
fmat <- t(d$mat)[, bio_idx]  # ComBat operates on biological samples; features in rows
batch_v <- d$batch[bio_idx]
group_v <- d$group[bio_idx]

# The generator's default alternation is balanced per batch; manually re-skew group WITHIN each
# batch (independent of the underlying data) to get an IMBALANCED-but-not-perfectly-confounded
# design: batch 1 mostly control, batch 2 even, batch 3 mostly case.
set.seed(52)
for (b in sort(unique(batch_v))) {
  idx_b <- which(batch_v == b)
  p_case <- c(`1` = 0.15, `2` = 0.5, `3` = 0.85)[as.character(b)]
  group_v[idx_b] <- sample(c("case", "control"), length(idx_b), replace = TRUE,
                            prob = c(p_case, 1 - p_case))
}

tab <- table(batch_v, group_v)
cat("Batch x group (imbalanced, not perfectly confounded):\n"); print(tab)

log_fmat <- log2(fmat)

cat("\n--- Case A: ComBat WITHOUT the biological covariate (the unsafe way the user asked for) ---\n")
combat_naive <- tryCatch(
  ComBat(dat = log_fmat, batch = batch_v, mod = NULL, par.prior = TRUE, mean.only = FALSE),
  error = function(e) { cat("ComBat error:", conditionMessage(e), "\n"); NULL })
if (!is.null(combat_naive)) {
  cat(sprintf("Ran: %d features corrected. Group means before -> after (feature 1, a null/no-effect feature):\n",
              nrow(combat_naive)))
}

cat("\n--- Case B: ComBat WITH mod= biological covariate (the Skill's documented safe usage) ---\n")
mod <- model.matrix(~as.factor(group_v))
combat_safe <- tryCatch(
  ComBat(dat = log_fmat, batch = batch_v, mod = mod, par.prior = TRUE, mean.only = FALSE),
  error = function(e) { cat("ComBat error:", conditionMessage(e), "\n"); NULL })
if (!is.null(combat_safe)) cat(sprintf("Ran: %d features corrected with covariate protected.\n", nrow(combat_safe)))

# Quantify the risk across ALL true-null features (outside the effect[1:6] block in make_dataset
# for n_features=60) rather than a single feature -- the false-positive RATE under imbalance is
# the actual Nygaard 2016 claim, not any one gene/feature's p-value.
null_features <- 7:n_features
p_raw <- sapply(null_features, function(f)
  t.test(log_fmat[f, group_v == "case"], log_fmat[f, group_v == "control"])$p.value)
p_naive <- if (!is.null(combat_naive)) sapply(null_features, function(f)
  t.test(combat_naive[f, group_v == "case"], combat_naive[f, group_v == "control"])$p.value) else rep(NA, length(null_features))
p_safe <- if (!is.null(combat_safe)) sapply(null_features, function(f)
  t.test(combat_safe[f, group_v == "case"], combat_safe[f, group_v == "control"])$p.value) else rep(NA, length(null_features))
cat(sprintf("\nFalse-positive rate (p<0.05) across %d true-null features:\n", length(null_features)))
cat(sprintf("  Raw (uncorrected)              : %d/%d = %.1f%%\n",
            sum(p_raw < 0.05), length(null_features), 100 * mean(p_raw < 0.05)))
cat(sprintf("  Naive ComBat (no covariate)     : %d/%d = %.1f%%\n",
            sum(p_naive < 0.05, na.rm = TRUE), length(null_features), 100 * mean(p_naive < 0.05, na.rm = TRUE)))
cat(sprintf("  Covariate-protected ComBat      : %d/%d = %.1f%%\n",
            sum(p_safe < 0.05, na.rm = TRUE), length(null_features), 100 * mean(p_safe < 0.05, na.rm = TRUE)))
cat("Expected under Nygaard 2016: naive ComBat's false-positive rate on true-null features exceeds\n")
cat("both raw and the covariate-protected rate under this batch/group imbalance.\n\n")
cat("RECOMMENDATION TO USER: prefer QC-anchored between-batch alignment (input 5's method) since\n")
cat("it needs no group covariate at all; if ComBat is used, mod= is mandatory here given the imbalance.\n")
