# Input 5 (Stress / multi-part) -- bio-causal-genomics-mediation-analysis RE-AUDIT (post-fix)
# Prompt: "I have RNA-seq-derived log-CPM expression for 2000 genes, n=300 subjects,
# a continuous exposure (PRS), a categorical batch covariate (3 levels), and a
# continuous outcome. Use HIMA to screen for genes that mediate the PRS-outcome
# relationship, control FDR at 0.05, and tell me how many mediators you find and
# whether they match the ones I planted."
#
# REGRESSION TEST of the fixed "HIMA covariate or data.pheno error" section.
# Unlike the pre-fix audit (which used only a binary numeric sex covariate to dodge
# the documented-fix defect), this input ADDS a genuinely categorical covariate
# (batch, 3 levels) so the fixed SKILL.md's literal instructions -- dummy-code with
# model.matrix(), NOT factor() -- are exercised end-to-end, following SKILL.md's
# own fix example (lines ~137-145) verbatim.
# SYNTHETIC DATA: n=300, p=2000 candidate mediators, 8 true planted mediators.

library(HIMA)

set.seed(5005)
n <- 300
p <- 2000
n_true <- 8

exposure <- rnorm(n)
age <- rnorm(n, 50, 8)
sex <- rbinom(n, 1, 0.5)
batch <- factor(sample(c("A", "B", "C"), n, replace = TRUE, prob = c(0.4, 0.35, 0.25)))
cell_pc1 <- rnorm(n)
cell_pc2 <- rnorm(n)

M <- matrix(rnorm(n * p, 0, 1), nrow = n, ncol = p)
colnames(M) <- paste0("gene_", seq_len(p))

true_idx <- sample(seq_len(p), n_true)
alpha_true <- runif(n_true, 0.5, 0.9)   # exposure -> mediator
beta_true <- runif(n_true, 0.4, 0.8)    # mediator -> outcome

for (i in seq_along(true_idx)) {
  M[, true_idx[i]] <- alpha_true[i] * exposure + rnorm(n, 0, 0.7)
}

# Batch has a small nuisance effect on outcome so it is a real covariate, not decorative
batch_effect <- c(A = 0, B = 0.25, C = -0.2)[as.character(batch)]
outcome <- 0.2 * exposure + 0.03 * age + batch_effect + rnorm(n, 0, 3)
for (i in seq_along(true_idx)) {
  outcome <- outcome + beta_true[i] * M[, true_idx[i]]
}

dat <- data.frame(outcome, exposure, age, sex, batch, cell_pc1, cell_pc2)
write.csv(dat, "../data/input5_hima_phenotype_synthetic.csv", row.names = FALSE)
write.csv(data.frame(gene = paste0("gene_", true_idx), alpha = alpha_true, beta = beta_true),
          "../data/input5_hima_true_mediators_synthetic.csv", row.names = FALSE)
saveRDS(M, "../data/input5_hima_mediator_matrix_synthetic.rds")

cat("=== Input 5 (post-fix regression): High-D HIMA EWAS-style mediation, categorical batch covariate (SYNTHETIC DATA) ===\n")
cat("n =", n, ", p =", p, "candidate mediators, ", n_true, "true planted mediators\n")
cat("Planted true mediator indices:", paste(true_idx, collapse = ", "), "\n\n")

dat_clean <- na.omit(dat[, c("outcome", "exposure", "age", "sex", "batch", "cell_pc1", "cell_pc2")])

cat("--- Step A: literally follow the OLD (pre-fix) instruction -- factor() -- to confirm\n")
cat("    it still fails the same way the pre-fix audit found (regression check on the bug report) ---\n")
dat_factor_attempt <- dat_clean
dat_factor_attempt$batch <- factor(dat_factor_attempt$batch)
result_factor_attempt <- tryCatch({
  hima(
    outcome ~ exposure + age + sex + batch + cell_pc1 + cell_pc2,
    data.pheno = dat_factor_attempt,
    data.M = M,
    mediator.type = "gaussian",
    penalty = "DBlasso",
    scale = TRUE,
    sigcut = 0.05,
    verbose = FALSE
  )
}, error = function(e) e)
if (inherits(result_factor_attempt, "error")) {
  cat("CONFIRMED: factor() covariate still throws an error on installed HIMA 2.3.4:\n")
  cat("  ", conditionMessage(result_factor_attempt), "\n\n")
} else {
  cat("UNEXPECTED: factor() covariate did NOT error this time -- re-check HIMA version behavior.\n\n")
}

cat("--- Step B: follow the FIXED SKILL.md instruction -- model.matrix() dummy-coding ---\n")
batch_dummy <- model.matrix(~ batch, data = dat_clean)[, -1, drop = FALSE]
dat_fixed <- cbind(dat_clean[, setdiff(names(dat_clean), "batch")], batch_dummy)
cat("Dummy columns created:", paste(colnames(batch_dummy), collapse = ", "), "\n")

result <- hima(
  as.formula(paste("outcome ~ exposure + age + sex +",
                    paste(colnames(batch_dummy), collapse = " + "), "+ cell_pc1 + cell_pc2")),
  data.pheno = dat_fixed,
  data.M = M,
  mediator.type = "gaussian",
  penalty = "DBlasso",
  scale = TRUE,
  sigcut = 0.05,
  verbose = TRUE
)

cat("\n--- HIMA result (fixed dummy-coded covariate) ---\n")
print(result)

cat("\n--- Verify fixed SKILL.md's return-type documentation ---\n")
cat("class(result):", paste(class(result), collapse = ", "), "\n")
cat("is.list(result):", is.list(result), "\n")
cat("nrow(result) [SKILL.md now says this is NULL, not usable]:", is.null(nrow(result)), "\n")
cat("rownames(result) [SKILL.md now says this is NULL, not usable]:", is.null(rownames(result)), "\n")

n_sig <- length(result$ID)
cat("\nNumber of significant mediators (sigcut=0.05) via result$ID:", n_sig, "\n")

if (!is.null(result) && n_sig > 0) {
  found_genes <- result$ID
  true_genes <- paste0("gene_", true_idx)
  recovered <- intersect(found_genes, true_genes)
  false_pos <- setdiff(found_genes, true_genes)
  cat("Recovered true mediators:", length(recovered), "/", n_true, "->", paste(recovered, collapse = ", "), "\n")
  cat("False positives (not in planted set):", length(false_pos), "\n")
} else {
  cat("HIMA returned zero significant mediators.\n")
}
