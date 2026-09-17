# Follow-up to Input 2: the Skill's OWN shipped examples/coloc_susie.R and
# examples/coloc_susie_multicausal.R both crash on this installed coloc 5.2.3 / susieR 0.14.2
# (see skill_own_example_check.txt, skill_own_example2_check.txt, input2_output.txt) because their
# toy LD matrix (a hand-built exponential-decay band) is generated independently of the simulated
# betas/SEs -- it is not actually consistent with any real genotype structure that could produce
# those z-scores. This script tests whether that is a demo-data defect (fixable by generating a
# genuinely self-consistent genotype -> phenotype -> LD pipeline) or a defect in the Skill's method
# guidance itself, by simulating real dosage genotypes with true LD, deriving z-scores AND the LD
# matrix from the SAME genotype matrix (as the Skill's own text prescribes: "LD matrix MUST be in
# the same SNP order as the beta vector" / in-sample LD), and running runsusie() + coloc.susie()
# exactly as documented.

library(coloc)
library(susieR)

set.seed(303)
n_ind <- 4000
n_snps <- 300
positions <- sort(sample(30000000:31000000, n_snps))

# Simulate genotype dosages with AR(1)-like LD via a latent factor structure
rho <- 0.85
Sigma <- rho^abs(outer(1:n_snps, 1:n_snps, '-'))
L <- chol(Sigma)
G <- matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% L
# standardize each column (dosage-like continuous genotype)
G <- scale(G)

causal1 <- which.min(abs(positions - 30300000))
causal2 <- which.min(abs(positions - 30700000))
cat('PLANTED TRUTH: causal1 idx', causal1, '(shared GWAS+eQTL), causal2 idx', causal2, '(GWAS-only)\n')

# GWAS phenotype: driven by causal1 + causal2
y_gwas <- 0.25 * G[, causal1] + 0.20 * G[, causal2] + rnorm(n_ind, 0, 1)
# eQTL phenotype: driven by causal1 only
y_eqtl <- 0.40 * G[, causal1] + rnorm(n_ind, 0, 1)

# Per-SNP marginal regression (as a real GWAS/eQTL summary-stats pipeline would produce)
get_sumstats <- function(y, G) {
  beta <- se <- numeric(ncol(G))
  for (j in 1:ncol(G)) {
    fit <- summary(lm(y ~ G[, j]))$coefficients
    beta[j] <- fit[2, 1]
    se[j] <- fit[2, 2]
  }
  list(beta = beta, se = se)
}
gwas_ss <- get_sumstats(y_gwas, G)
eqtl_ss <- get_sumstats(y_eqtl, G)

# In-sample LD, exactly matching the genotype matrix used for both traits (Skill's own
# recommendation: "Use in-sample LD when at all possible")
ld_matrix <- cor(G)
snp_ids <- paste0('rs', 1:n_snps)
dimnames(ld_matrix) <- list(snp_ids, snp_ids)

z_gwas <- gwas_ss$beta / gwas_ss$se
lam_gwas <- susieR::estimate_s_rss(z = z_gwas, R = ld_matrix, n = n_ind)
cat(sprintf('GWAS estimate_s_rss lambda = %.4f\n', lam_gwas))
z_eqtl <- eqtl_ss$beta / eqtl_ss$se
lam_eqtl <- susieR::estimate_s_rss(z = z_eqtl, R = ld_matrix, n = n_ind)
cat(sprintf('eQTL estimate_s_rss lambda = %.4f\n', lam_eqtl))

gwas_data <- list(beta = gwas_ss$beta, varbeta = gwas_ss$se^2, snp = snp_ids, position = positions,
                   type = 'quant', sdY = sd(y_gwas), N = n_ind, LD = ld_matrix)
eqtl_data <- list(beta = eqtl_ss$beta, varbeta = eqtl_ss$se^2, snp = snp_ids, position = positions,
                   type = 'quant', sdY = sd(y_eqtl), N = n_ind, LD = ld_matrix)

s_gwas <- runsusie(gwas_data, L = 10)
s_eqtl <- runsusie(eqtl_data, L = 10)

n_cs_gwas <- if (!is.null(summary(s_gwas)$cs)) nrow(summary(s_gwas)$cs) else 0
n_cs_eqtl <- if (!is.null(summary(s_eqtl)$cs)) nrow(summary(s_eqtl)$cs) else 0
cat(sprintf('\nGWAS credible sets: %d (planted truth: 2) | eQTL credible sets: %d (planted truth: 1)\n',
            n_cs_gwas, n_cs_eqtl))

res_susie <- coloc.susie(s_gwas, s_eqtl)
if (is.null(res_susie$summary) || nrow(res_susie$summary) == 0) {
  cat('\nNo overlapping credible sets -> unexpected given planted truth\n')
} else {
  print(res_susie$summary[, c('idx1', 'idx2', 'hit1', 'hit2', 'PP.H3.abf', 'PP.H4.abf')])
  best <- res_susie$summary[which.max(res_susie$summary$PP.H4.abf), ]
  cat(sprintf('\nBest CS pair: %s x %s | PP.H4 = %.3f\n', best$hit1, best$hit2, best$PP.H4.abf))
  cat('ASSERTION: best pair PP.H4 > 0.75:', best$PP.H4.abf > 0.75, '\n')
  cat('ASSERTION: best pair lead SNP is causal1 (rs', causal1, '):',
      (best$hit1 == paste0('rs', causal1)) || (best$hit2 == paste0('rs', causal1)), '\n', sep='')
}
