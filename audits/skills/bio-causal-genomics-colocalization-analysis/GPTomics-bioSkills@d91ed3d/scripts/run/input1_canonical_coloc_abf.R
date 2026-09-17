# Input 1 (Canonical) -- "Test if my GWAS lead SNP at this locus colocalizes with the eQTL
# for the nearest gene using coloc.abf. Report PP.H4 with p12 sensitivity."
#
# SYNTHETIC planted-truth data: single shared causal variant at position 30,500,000.
# Ground truth: PP.H4 should dominate (shared causal variant).
# Follows the Skill's "Standard coloc.abf Pipeline" section verbatim (harmonise -> format -> coloc.abf -> sensitivity).

library(coloc)

harmonise_summary_stats <- function(df1, df2) {
  m <- merge(df1, df2, by = 'SNP', suffixes = c('.1', '.2'))
  same <- m$A1.1 == m$A1.2 & m$A2.1 == m$A2.2
  flip <- m$A1.1 == m$A2.2 & m$A2.1 == m$A1.2
  palindromic <- (m$A1.1 %in% c('A', 'T') & m$A2.1 %in% c('A', 'T')) |
                 (m$A1.1 %in% c('C', 'G') & m$A2.1 %in% c('C', 'G'))
  high_maf_palin <- palindromic & pmin(m$MAF.1, 1 - m$MAF.1) > 0.42
  m$BETA.2[flip] <- -m$BETA.2[flip]
  keep <- (same | flip) & !high_maf_palin
  m[keep, ]
}

set.seed(101)
n_snps <- 1000
positions <- sort(sample(30000000:31000000, n_snps))
causal_idx <- which.min(abs(positions - 30500000))

gwas_beta <- rnorm(n_snps, 0, 0.02); gwas_beta[causal_idx] <- 0.15
gwas_se <- rep(0.03, n_snps)
gwas_df <- data.frame(SNP = paste0('rs', 1:n_snps), CHR = 6, POS = positions,
                       A1 = 'A', A2 = 'G', MAF = runif(n_snps, 0.05, 0.5),
                       BETA = gwas_beta, SE = gwas_se)

eqtl_beta <- rnorm(n_snps, 0, 0.03); eqtl_beta[causal_idx] <- 0.4
eqtl_se <- rep(0.05, n_snps)
eqtl_df <- data.frame(SNP = paste0('rs', 1:n_snps), CHR = 6, POS = positions,
                       A1 = 'A', A2 = 'G', MAF = runif(n_snps, 0.05, 0.5),
                       BETA = eqtl_beta, SE = eqtl_se)

harm <- harmonise_summary_stats(gwas_df, eqtl_df)
cat('PLANTED TRUTH: single shared causal variant at rs', causal_idx, ' (pos ~30.5Mb)\n', sep='')
cat('Harmonised SNPs:', nrow(harm), 'of', nrow(gwas_df), '\n')

gwas_input <- list(beta = harm$BETA.1, varbeta = harm$SE.1^2,
                    snp = harm$SNP, position = harm$POS.1,
                    type = 'cc', s = 0.30, N = 50000)

eqtl_input <- list(beta = harm$BETA.2, varbeta = harm$SE.2^2,
                    snp = harm$SNP, position = harm$POS.1,
                    type = 'quant', sdY = 1, N = 500)

res <- coloc.abf(dataset1 = gwas_input, dataset2 = eqtl_input,
                  p1 = 1e-4, p2 = 1e-4, p12 = 5e-6)

cat('\nPosterior probabilities:\n')
print(round(res$summary, 4))

pp4 <- res$summary['PP.H4.abf']
pp3 <- res$summary['PP.H3.abf']
cat(sprintf('\nPP.H4 = %.4f | PP.H3 = %.4f\n', pp4, pp3))

cat('\nASSERTION CHECK: PP.H4 > 0.75 (planted truth is shared causal variant):', pp4 > 0.75, '\n')

cat('\nRunning p12 sensitivity over the grid\n')
sens <- coloc::sensitivity(res, rule = 'H4 > 0.75')
print(sens)

top_snps <- res$results[order(-res$results$SNP.PP.H4), ][1:5, ]
cat('\nTop 5 SNPs by per-SNP PP.H4:\n')
print(top_snps[, c('snp', 'SNP.PP.H4')])
cat('\nCausal SNP correctly in top-5:', paste0('rs', causal_idx) %in% top_snps$snp, '\n')
