# Follow-up to Input 3: test the literal "distinct causal variants in moderate LD" scenario
# (GWAS causal SNP != eQTL causal SNP, r2 in [0.3,0.6]) rather than the allelic-heterogeneity
# variant tried first (which resolved cleanly to H4, a useful negative finding in itself).
library(coloc)
set.seed(505)
n_ind <- 4000
n_snps <- 300
positions <- sort(sample(30000000:31000000, n_snps))
rho <- 0.90
Sigma <- rho^abs(outer(1:n_snps, 1:n_snps, '-'))
L <- chol(Sigma)
G <- scale(matrix(rnorm(n_ind * n_snps), n_ind, n_snps) %*% L)

causal_gwas <- 150
causal_eqtl <- 153
r2 <- cor(G[, causal_gwas], G[, causal_eqtl])^2
cat(sprintf('PLANTED TRUTH: GWAS causal=rs%d, eQTL causal=rs%d (DIFFERENT SNPs), r2=%.3f\n',
            causal_gwas, causal_eqtl, r2))

y_gwas <- 0.30 * G[, causal_gwas] + rnorm(n_ind, 0, 1)
y_eqtl <- 0.40 * G[, causal_eqtl] + rnorm(n_ind, 0, 1)

get_sumstats <- function(y, G) {
  beta <- se <- numeric(ncol(G))
  for (j in 1:ncol(G)) { fit <- summary(lm(y ~ G[, j]))$coefficients; beta[j] <- fit[2,1]; se[j] <- fit[2,2] }
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
cat(sprintf('\nPP.H3 = %.4f | PP.H4 = %.4f  (planted truth: distinct causal variants, PP.H3 should be prominent)\n',
            res$summary['PP.H3.abf'], res$summary['PP.H4.abf']))
top <- res$results[order(-res$results$SNP.PP.H4),][1:3,c('snp','SNP.PP.H4')]
cat('Top per-SNP PP.H4:\n'); print(top)
