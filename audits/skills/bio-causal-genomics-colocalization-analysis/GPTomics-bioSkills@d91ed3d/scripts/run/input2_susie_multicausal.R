# Input 2 (Variant A) -- "GCTA-COJO conditional analysis identified two independent GWAS
# signals at this locus. Run coloc.susie with the LD matrix and report all credible-set pair PPs."
#
# SYNTHETIC planted truth: GWAS has 2 independent causal SNPs (causal1, causal2); eQTL shares
# ONLY causal1. Expect: 2 GWAS credible sets, 1 eQTL credible set, and the (CS-causal1, eQTL-CS)
# pair should show high PP.H4 while causal2 has no eQTL counterpart (PP.H4 low/H1 for that CS).
# Follows the Skill's "coloc.susie Multi-Causal Pipeline" section, including the
# estimate_s_rss z-vs-LD diagnostic the Skill requires before running SuSiE.

library(coloc)
library(susieR)

set.seed(202)
n_snps <- 500
positions <- sort(sample(30000000:31000000, n_snps))

causal1 <- which.min(abs(positions - 30300000))
causal2 <- which.min(abs(positions - 30700000))
cat('PLANTED TRUTH: GWAS causal1 at index', causal1, '(shared w/ eQTL), causal2 at index', causal2, '(GWAS-only)\n')

ld_matrix <- diag(n_snps)
for (i in 1:n_snps) {
  j_range <- max(1, i - 5):min(n_snps, i + 5)
  for (j in j_range) {
    if (i != j) ld_matrix[i, j] <- 0.8^abs(i - j)
  }
}
ld_matrix <- (ld_matrix + t(ld_matrix)) / 2

gwas_beta <- rnorm(n_snps, 0, 0.01)
gwas_beta[causal1] <- 0.12
gwas_beta[causal2] <- 0.10
gwas_se <- rep(0.025, n_snps)
gwas_N <- 50000

eqtl_beta <- rnorm(n_snps, 0, 0.02)
eqtl_beta[causal1] <- 0.35
eqtl_se <- rep(0.04, n_snps)
eqtl_N <- 500

snp_ids <- paste0('rs', 1:n_snps)
dimnames(ld_matrix) <- list(snp_ids, snp_ids)

z_gwas <- gwas_beta / gwas_se
lam_gwas <- susieR::estimate_s_rss(z = z_gwas, R = ld_matrix, n = gwas_N)
cat(sprintf('GWAS estimate_s_rss lambda = %.4f (Skill requires abort if > 0.05)\n', lam_gwas))

z_eqtl <- eqtl_beta / eqtl_se
lam_eqtl <- susieR::estimate_s_rss(z = z_eqtl, R = ld_matrix, n = eqtl_N)
cat(sprintf('eQTL estimate_s_rss lambda = %.4f\n', lam_eqtl))

gwas_data <- list(beta = gwas_beta, varbeta = gwas_se^2, snp = snp_ids, position = positions,
                   type = 'cc', s = 0.3, N = gwas_N, LD = ld_matrix)
eqtl_data <- list(beta = eqtl_beta, varbeta = eqtl_se^2, snp = snp_ids, position = positions,
                   type = 'quant', sdY = 1, N = eqtl_N, LD = ld_matrix)

s_gwas <- runsusie(gwas_data, L = 10)
s_eqtl <- runsusie(eqtl_data, L = 10)

n_cs_gwas <- if (!is.null(summary(s_gwas)$cs)) nrow(summary(s_gwas)$cs) else 0
n_cs_eqtl <- if (!is.null(summary(s_eqtl)$cs)) nrow(summary(s_eqtl)$cs) else 0
cat(sprintf('\nGWAS credible sets: %d (planted truth: 2) | eQTL credible sets: %d (planted truth: 1)\n',
            n_cs_gwas, n_cs_eqtl))

res_susie <- coloc.susie(s_gwas, s_eqtl)

if (is.null(res_susie$summary) || nrow(res_susie$summary) == 0) {
  cat('\nNo overlapping credible sets between traits -> no colocalization signal\n')
} else {
  cat('\nPer-(CS1, CS2) colocalization PP:\n')
  print(res_susie$summary[, c('idx1', 'idx2', 'hit1', 'hit2', 'PP.H3.abf', 'PP.H4.abf')])
  best <- res_susie$summary[which.max(res_susie$summary$PP.H4.abf), ]
  cat(sprintf('\nBest CS pair: GWAS CS%d (%s) x eQTL CS%d (%s) | PP.H4 = %.3f\n',
              best$idx1, best$hit1, best$idx2, best$hit2, best$PP.H4.abf))
  cat('\nASSERTION CHECK: best pair PP.H4 > 0.75 (causal1 correctly shared):', best$PP.H4.abf > 0.75, '\n')
  cat('ASSERTION CHECK: best-pair lead SNP == causal1 SNP (rs', causal1, '):',
      best$hit1 == paste0('rs', causal1) || best$hit2 == paste0('rs', causal1), '\n', sep='')
}
