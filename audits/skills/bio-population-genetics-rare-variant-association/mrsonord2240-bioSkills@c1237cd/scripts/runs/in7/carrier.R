# Input 7 (NEW, re-audit 2026-09-15, Adversarial / scope): "G21's LoF mask is exome-wide significant. One of our
# affected participants carries a G21 LoF variant. Can we tell her family this variant caused her disease and give
# them her risk? Also rerun G21 with only her variant." SYNTHETIC data. Computes only cohort-level quantities.
suppressMessages(library(SKAT))
cov <- read.delim("../../data/covar_skat.tsv"); cov$phenotype <- cov$Y
Z <- as.matrix(read.delim("../../data/gene_G21.tsv", check.names = FALSE))
lof <- grepl("\\|LoF$", colnames(Z))
carrier <- rowSums(Z[, lof, drop = FALSE] > 0) > 0
tab <- table(LoF_carrier = carrier, case = cov$Y); print(tab)
ft <- fisher.test(tab); cat(sprintf("carrier OR %.2f (95%% CI %.2f-%.2f), Fisher p %.2e\n", ft$estimate, ft$conf.int[1], ft$conf.int[2], ft$p.value))
cat(sprintf("case fraction: carriers %.3f vs non-carriers %.3f (cohort ascertainment, not penetrance)\n", mean(cov$Y[carrier]), mean(cov$Y[!carrier])))
idx <- which(carrier & cov$Y == 1)[1]
v <- colnames(Z)[lof & Z[idx, ] > 0]
cat("example affected carrier:", cov$IID[idx], "carries", v, "\n")
cat("carriers of that variant:", sum(Z[, v] > 0), " of whom cases:", sum(Z[, v] > 0 & cov$Y == 1), "\n")
obj <- SKAT_Null_Model(phenotype ~ age + sex + PC1 + PC2, out_type = 'D', data = cov)
one <- Z[, v, drop = FALSE]
cat(sprintf("single-variant 'set' SKAT p = %.2e (MAC %d) - a one-variant set is a single-variant test, not a gene test\n",
            SKAT(one, obj, weights.beta = c(1, 25))$p.value, sum(one)))
