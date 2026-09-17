# Input 5 (Stress / multi-part) -- "Run coloc.abf between this GWAS locus and the same gene
# across multiple GTEx-style tissues; rank tissues by PP.H4 to identify the causal cell type."
# (SKILL.md Decision Tree row: "GWAS + multi-tissue eQTL ... coloc.abf per tissue + HyPrColoc
# across tissues"; usage-guide.md Example Prompts "Multi-Tissue" section.)
#
# Planted truth: 5 simulated "tissues"; the causal variant is genuinely active (shared with GWAS)
# in tissues 1 and 2 only (simulating tissue-specific cis-regulation); tissues 3-5 have no eQTL
# signal at this SNP at all (pure noise). Self-consistent genotype-derived sumstats as in Input 2b/3.
# NOTE: hyprcoloc (for the cross-tissue clustering half of this decision-tree branch) was not yet
# installed in this environment at audit time -- see eval_viewer for how that gap is scored.

library(coloc)
set.seed(606)
n_ind <- 3000
n_snps <- 200
positions <- sort(sample(30000000:31000000, n_snps))
rho <- 0.85
Sigma <- rho^abs(outer(1:n_snps, 1:n_snps, '-'))
G <- scale(matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% chol(Sigma))
causal <- 100
cat('PLANTED TRUTH: causal SNP rs', causal, '; active (shared with GWAS) in tissues 1-2 only\n', sep='')

y_gwas <- 0.28 * G[, causal] + rnorm(n_ind, 0, 1)
get_sumstats <- function(y, G) {
  beta <- se <- numeric(ncol(G))
  for (j in 1:ncol(G)) { f <- summary(lm(y ~ G[, j]))$coefficients; beta[j] <- f[2,1]; se[j] <- f[2,2] }
  list(beta = beta, se = se)
}
gwas_ss <- get_sumstats(y_gwas, G)
snp_ids <- paste0('rs', 1:n_snps)
gwas_input <- list(beta = gwas_ss$beta, varbeta = gwas_ss$se^2, snp = snp_ids, position = positions,
                    type = 'quant', sdY = sd(y_gwas), N = n_ind)

tissue_effect <- c(0.35, 0.30, 0, 0, 0)  # tissues 3-5: no true cis effect at this SNP
results <- data.frame(tissue = paste0('Tissue', 1:5), PP.H4 = NA, PP.H3 = NA, PP.H0 = NA)
for (t in 1:5) {
  y_eqtl <- tissue_effect[t] * G[, causal] + rnorm(n_ind, 0, 1)
  eqtl_ss <- get_sumstats(y_eqtl, G)
  eqtl_input <- list(beta = eqtl_ss$beta, varbeta = eqtl_ss$se^2, snp = snp_ids, position = positions,
                      type = 'quant', sdY = sd(y_eqtl), N = n_ind)
  res <- coloc.abf(dataset1 = gwas_input, dataset2 = eqtl_input, p1 = 1e-4, p2 = 1e-4, p12 = 1e-5)
  results$PP.H4[t] <- res$summary['PP.H4.abf']
  results$PP.H3[t] <- res$summary['PP.H3.abf']
  results$PP.H0[t] <- res$summary['PP.H0.abf']
}
results <- results[order(-results$PP.H4), ]
cat('\nTissues ranked by PP.H4:\n')
print(results)
cat('\nASSERTION: top-2 ranked tissues are Tissue1/Tissue2 (planted causal tissues):',
    setequal(results$tissue[1:2], c('Tissue1','Tissue2')), '\n')
cat('ASSERTION: tissues 3-5 (no true effect) show low PP.H4 (<0.5):',
    all(results$PP.H4[results$tissue %in% c('Tissue3','Tissue4','Tissue5')] < 0.5), '\n')
cat('\nHyPrColoc cross-tissue clustering step: NOT EXECUTED -- package not installed in this\n')
cat('environment as of this audit run (see TOOLS.md); scored by inspection in the eval viewer.\n')
