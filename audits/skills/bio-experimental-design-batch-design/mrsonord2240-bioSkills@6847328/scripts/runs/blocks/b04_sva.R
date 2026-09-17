# Extracted verbatim from SKILL.md "Detecting Hidden Batch Effects (SVA)" (post-fix, commit
# 6847328). Requires `expr_normalized` and `colData` in scope.
library(sva)
mod  <- model.matrix(~ condition, data = colData)   # full model
mod0 <- model.matrix(~ 1, data = colData)           # null model

n_bad <- sum(!is.finite(expr_normalized))
if (n_bad > 0) {
  message(sprintf('%d/%d cells (%.0f%%) are missing/non-finite; sva() requires a complete matrix.',
          n_bad, length(expr_normalized), 100 * n_bad / length(expr_normalized)))
  # Option A (used here): keep only complete-observation features. Simple and defensible for SV
  # estimation, but biases the surrogate variables toward abundant, well-detected features --
  # confirm that bias is acceptable before trusting the SVs for low-abundance biology.
  complete <- expr_normalized[stats::complete.cases(expr_normalized), , drop = FALSE]
  message(sprintf('Restricting to %d/%d features with no missing values (Option A).',
          nrow(complete), nrow(expr_normalized)))
  expr_normalized <- complete
  # Option B (alternative): impute first (normalization-qc covers QRILC/missForest for
  # left-censored proteomics/metabolomics intensities), then re-run sva() on the imputed matrix --
  # but the imputer choice then shapes the estimated SVs, so record which one was used.
}
stopifnot("expr_normalized still has non-finite values after handling missingness" =
  all(is.finite(expr_normalized)))

n_sv <- num.sv(expr_normalized, mod)                # estimate number of hidden batches
svobj <- sva(expr_normalized, mod, mod0, n.sv = n_sv)
