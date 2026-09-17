# Input 3 (Edge) -- "PP.H3 is dominating coloc.abf despite obvious visual overlap in LocusZoom.
# What's going on and what should I do?"
#
# Tests the Skill's documented failure mode "coloc.abf -- PP.H3 inflation under multiple causal
# variants" (SKILL.md Per-Method Failure Modes section). Planted truth: 2 independent causal SNPs
# in moderate LD (r2 ~0.3-0.6 band per the Skill's own trigger description); eQTL shares only one.
# Self-consistent genotype -> phenotype -> sumstats simulation (same approach validated in Input 2b)
# so any PP.H3 inflation reflects the real single-causal-assumption limitation, not broken demo data.

library(coloc)

set.seed(404)
n_ind <- 4000
n_snps <- 300
positions <- sort(sample(30000000:31000000, n_snps))

rho <- 0.90  # AR(1) decay; with a small index offset this gives r2 in the Skill's stated
             # moderate-LD trigger band (r2 ~0.3-0.6) between the two causal SNPs
Sigma <- rho^abs(outer(1:n_snps, 1:n_snps, '-'))
L <- chol(Sigma)
G <- scale(matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% L)

causal1 <- 150
causal2 <- 153  # 3 SNPs away -> corr ~ rho^3 ~ 0.73, r2 ~ 0.53 (moderate LD band)
r2_between <- cor(G[, causal1], G[, causal2])^2
cat(sprintf('PLANTED TRUTH: 2 distinct causal SNPs, r2(causal1,causal2) = %.3f; eQTL shares causal1 only\n', r2_between))

y_gwas <- 0.25 * G[, causal1] + 0.22 * G[, causal2] + rnorm(n_ind, 0, 1)
y_eqtl <- 0.40 * G[, causal1] + rnorm(n_ind, 0, 1)

get_sumstats <- function(y, G) {
  beta <- se <- numeric(ncol(G))
  for (j in 1:ncol(G)) {
    fit <- summary(lm(y ~ G[, j]))$coefficients
    beta[j] <- fit[2, 1]; se[j] <- fit[2, 2]
  }
  list(beta = beta, se = se)
}
gwas_ss <- get_sumstats(y_gwas, G)
eqtl_ss <- get_sumstats(y_eqtl, G)
snp_ids <- paste0('rs', 1:n_snps)

gwas_input <- list(beta = gwas_ss$beta, varbeta = gwas_ss$se^2, snp = snp_ids, position = positions,
                    type = 'quant', sdY = sd(y_gwas), N = n_ind)
eqtl_input <- list(beta = eqtl_ss$beta, varbeta = eqtl_ss$se^2, snp = snp_ids, position = positions,
                    type = 'quant', sdY = sd(y_eqtl), N = n_ind)

res <- coloc.abf(dataset1 = gwas_input, dataset2 = eqtl_input, p1 = 1e-4, p2 = 1e-4, p12 = 1e-5)
print(round(res$summary, 4))
pp3 <- res$summary['PP.H3.abf']; pp4 <- res$summary['PP.H4.abf']
cat(sprintf('\nPP.H3 = %.4f | PP.H4 = %.4f\n', pp3, pp4))
cat('ASSERTION: PP.H3 elevated relative to a single-causal locus, illustrating the documented\n')
cat('  single-causal-assumption failure mode at moderate LD (Skill Fix: escalate to coloc.susie):\n')
cat('  PP.H3 + PP.H4 both non-trivial (locus not cleanly resolved by coloc.abf):',
    (pp3 > 0.05 && pp4 < 0.9) || pp3 > 0.3, '\n')

cat('\nSensitivity over p12 (Skill: non-negotiable reporting requirement)\n')
sens <- coloc::sensitivity(res, rule = 'H4 > 0.75')
cat('Rows in sensitivity grid:', nrow(sens), '\n')
cat('Any p12 grid point where PP.H4 > 0.75:', any(sens$pass), '\n')
