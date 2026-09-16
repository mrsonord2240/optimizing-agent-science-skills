# Input 5 (Stress) -- bio-crispr-screens-batch-correction audit.
# Real request simulated: "My screen has clear essentiality signal but a small
# hit set is barely significant -- I suspect a hidden confounder (not
# passage, not sequencing lane -- something I haven't identified). Use SVA to
# find latent surrogate variables and add them to my MAGeCK MLE design matrix."
#
# Runs the Skill's own documented SVA code (SKILL.md "SVA" section) verbatim
# against synthetic data with a hidden multiplicative sample-quality confound
# that is NOT the same as condition and NOT given to sva() directly -- only
# recoverable as a surrogate variable.

suppressMessages(library(sva))

set.seed(99)
n_guides <- 4000
n_samples <- 12
condition <- rep(c("ctrl", "treat"), each = 6)
# Hidden confound: continuous "sample quality" axis, uncorrelated with condition
# by construction (orthogonal design) -- this is exactly what SVA should recover
# that a condition-only model matrix cannot.
hidden_confound <- c(0.9, 1.1, 0.8, 1.2, 1.0, 0.95, 1.05, 0.85, 1.15, 0.9, 1.1, 1.0)
stopifnot(cor(hidden_confound, as.numeric(factor(condition))) < 0.3)

base <- matrix(rpois(n_guides * n_samples, lambda = 500), nrow = n_guides)
# essential guides (first 200) drop out under treat
essential_idx <- 1:200
for (j in 1:n_samples) {
  if (condition[j] == "treat") base[essential_idx, j] <- rpois(200, lambda = 500 * 0.3)
  # hidden confound scales the WHOLE sample multiplicatively (a quality/depth-like effect)
  base[, j] <- rpois(n_guides, lambda = pmax(base[, j] * hidden_confound[j], 1))
}
rownames(base) <- paste0("guide_", 1:n_guides)
colnames(base) <- paste0("S", 1:n_samples)
counts_df <- as.data.frame(base)
metadata <- data.frame(condition = condition, row.names = colnames(base))

cat(sprintf("Built %d guides x %d samples; hidden confound cor(condition)=%.3f (should be low)\n",
            n_guides, n_samples, cor(hidden_confound, as.numeric(factor(condition)))))

# === Skill's own documented pattern, verbatim ===
mod <- model.matrix(~ condition, data = metadata)
mod0 <- model.matrix(~ 1, data = metadata)
log_counts <- log2(as.matrix(counts_df) + 1)
sv_obj <- sva(log_counts, mod, mod0)
n_sv <- sv_obj$n.sv
cat(sprintf("\nsva() found n.sv = %d surrogate variable(s)\n", n_sv))

if (n_sv > 0) {
  for (i in 1:n_sv) {
    r <- cor(sv_obj$sv[, i], hidden_confound)
    cat(sprintf("  SV%d correlation with the TRUE hidden confound: r = %.3f\n", i, r))
  }
  design_mat <- cbind(mod, sv_obj$sv)
  cat(sprintf("\nCombined design matrix for MAGeCK MLE: %d x %d (mod + %d SV columns)\n",
              nrow(design_mat), ncol(design_mat), n_sv))
  best_r <- max(abs(sapply(1:n_sv, function(i) cor(sv_obj$sv[, i], hidden_confound))))
  cat(sprintf("\nBest |correlation| between a discovered SV and the true hidden confound: %.3f\n", best_r))
  cat(sprintf("Recovered the planted confound: %s\n", ifelse(best_r > 0.5, "YES", "NO")))
} else {
  cat("sva() found 0 surrogate variables -- cannot proceed to add covariates.\n")
}

write.csv(as.data.frame(if (n_sv > 0) sv_obj$sv else matrix(nrow=n_samples, ncol=0)),
          r"(F:\OpenScience\audits\bio-crispr-screens-batch-correction\run\out_input5_sv.csv)",
          row.names = FALSE)
cat("\nDone.\n")
