# Phase 2 fresh input: generate a small synthetic EWAS-style dataset for the documented HIMA CLI.
set.seed(20260923)
n <- 300L; p <- 200L
exposure <- rnorm(n)
age <- rnorm(n, 52, 8)
sex <- rbinom(n, 1, .5)
batch <- sample(c("A", "B", "C"), n, replace = TRUE)
M <- matrix(rnorm(n * p), nrow = n, ncol = p,
            dimnames = list(NULL, paste0("cg", seq_len(p))))
for (j in 1:5) M[, j] <- 0.65 * exposure + rnorm(n, sd = .7)
outcome <- 0.20 * exposure + 0.42 * rowMeans(M[, 1:5, drop = FALSE]) + .04 * age + .10 * sex + rnorm(n)
pheno <- data.frame(outcome, exposure, age, sex, batch)
pheno$age[17] <- NA_real_
write.csv(pheno, "F:/OpenScience/audits/bio-causal-genomics-mediation-analysis/data/input14_pheno.csv", row.names = FALSE)
write.csv(as.data.frame(M), "F:/OpenScience/audits/bio-causal-genomics-mediation-analysis/data/input14_mediators.csv", row.names = FALSE)
cat("WROTE n=300 p=200 with five planted mediators and one incomplete phenotype row\n")
