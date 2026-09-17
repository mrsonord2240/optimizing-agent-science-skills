# Input 5 (Stress / multi-part) -- bio-causal-genomics-mediation-analysis audit
# Prompt: "I have RNA-seq-derived log-CPM expression for 2000 genes, n=300 subjects,
# a continuous exposure (PRS) and a continuous outcome. Use HIMA to screen for genes
# that mediate the PRS-outcome relationship, control FDR at 0.05, and tell me how
# many mediators you find and whether they match the ones I planted."
#
# Following SKILL.md "High-Dimensional EWAS Mediation (HIMA2)" pattern.
# SYNTHETIC DATA: n=300, p=2000 candidate mediators, 8 true planted mediators with
# both a (exposure->mediator) and b (mediator->outcome) paths; the rest pure noise.

library(HIMA)

set.seed(5005)
n <- 300
p <- 2000
n_true <- 8

exposure <- rnorm(n)
age <- rnorm(n, 50, 8)
sex <- rbinom(n, 1, 0.5)
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

outcome <- 0.2 * exposure + 0.03 * age + rnorm(n, 0, 3)
for (i in seq_along(true_idx)) {
  outcome <- outcome + beta_true[i] * M[, true_idx[i]]
}

dat <- data.frame(outcome, exposure, age, sex, cell_pc1, cell_pc2)
write.csv(dat, "../data/input5_hima_phenotype_synthetic.csv", row.names = FALSE)
write.csv(data.frame(gene = paste0("gene_", true_idx), alpha = alpha_true, beta = beta_true),
          "../data/input5_hima_true_mediators_synthetic.csv", row.names = FALSE)
saveRDS(M, "../data/input5_hima_mediator_matrix_synthetic.rds")

cat("=== Input 5: High-D HIMA EWAS-style mediation (SYNTHETIC DATA) ===\n")
cat("n =", n, ", p =", p, "candidate mediators, ", n_true, "true planted mediators\n")
cat("Planted true mediator indices:", paste(true_idx, collapse = ", "), "\n\n")

dat_clean <- na.omit(dat[, c("outcome", "exposure", "age", "sex", "cell_pc1", "cell_pc2")])
# sex kept numeric 0/1 (HIMA rejects factor covariates - see finding)

result <- hima(
  outcome ~ exposure + age + sex + cell_pc1 + cell_pc2,
  data.pheno = dat_clean,
  data.M = M,
  mediator.type = "gaussian",
  penalty = "DBlasso",
  scale = TRUE,
  sigcut = 0.05,
  verbose = TRUE
)

cat("\n--- HIMA result ---\n")
print(result)
# NOTE: SKILL.md's code comment claims "# result is a data.frame of significant
# mediators below sigcut" -- the actual return from HIMA 2.3.4's hima() is a
# *list* of class "hima" ($ID, $alpha, $beta, $`alpha*beta`, $rimp, $`p-value`),
# not a data.frame. nrow(result) is NA and rownames(result) is NULL on this
# object. Use result$ID, not row-based accessors.
n_sig <- length(result$ID)
cat("\nNumber of significant mediators (sigcut=0.05):", n_sig, "\n")

if (!is.null(result) && n_sig > 0) {
  found_genes <- result$ID
  true_genes <- paste0("gene_", true_idx)
  recovered <- intersect(found_genes, true_genes)
  false_pos <- setdiff(found_genes, true_genes)
  cat("Recovered true mediators:", length(recovered), "/", n_true, "->", paste(recovered, collapse = ", "), "\n")
  cat("False positives (not in planted set):", length(false_pos), "\n")
} else {
  cat("HIMA returned zero significant mediators.\n")
  cat("Per SKILL.md Common Errors: 'HIMA returns zero significant mediators -> Screening too\n")
  cat("aggressive; or no true mediators -> Try topN=2*sqrt(n) instead of default; verify with\n")
  cat("permutation null.'\n")
}
