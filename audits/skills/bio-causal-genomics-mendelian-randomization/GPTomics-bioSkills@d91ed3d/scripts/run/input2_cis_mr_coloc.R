# Input 2 (Variant A) -- cis-MR drug-target analysis with colocalization triangulation.
# Synthetic single-causal-variant cis-pQTL window, following SKILL.md's
# "Drug-Target / cis-MR Framework" section and examples/cis_mr_drug_target.R pattern:
# +/-500kb window, clump r2<0.1 (skipped -- single window, no live LD server), IVW/Wald ratio,
# then coloc.abf with PP.H4 >= 0.7 required for a drug-target claim.

library(TwoSampleMR)
library(coloc)

set.seed(11)
gene_start <- 50000000
gene_end <- 50050000
cis_window <- 500000
n_snps <- 30

# Ground truth: a single shared causal variant drives both signals (planted at index 15),
# true causal beta_XY = 0.5. Other SNPs carry proportional LD-tag signal (not independent pleiotropy).
causal_idx <- 15
cis_pqtl <- data.frame(
  SNP = paste0('rs', 1:n_snps),
  CHR = rep(1, n_snps),
  POS = sort(sample(seq(gene_start - cis_window, gene_end + cis_window, by = 500), n_snps)),
  BETA = rnorm(n_snps, 0.20, 0.04),
  SE = runif(n_snps, 0.02, 0.03),
  A1 = sample(c('A', 'C', 'G', 'T'), n_snps, replace = TRUE),
  A2 = sample(c('A', 'C', 'G', 'T'), n_snps, replace = TRUE),
  EAF = runif(n_snps, 0.10, 0.90),
  N = rep(54000, n_snps),
  stringsAsFactors = FALSE
)
cis_pqtl$P <- 2 * pnorm(-abs(cis_pqtl$BETA / cis_pqtl$SE))

true_beta_xy <- 0.5
outcome_assoc <- data.frame(
  SNP = cis_pqtl$SNP, CHR = cis_pqtl$CHR, POS = cis_pqtl$POS,
  BETA = cis_pqtl$BETA * true_beta_xy + rnorm(n_snps, 0, 0.01),
  SE = runif(n_snps, 0.025, 0.04),
  A1 = cis_pqtl$A1, A2 = cis_pqtl$A2,
  EAF = cis_pqtl$EAF + rnorm(n_snps, 0, 0.01),
  N = rep(250000, n_snps),
  stringsAsFactors = FALSE
)
outcome_assoc$P <- 2 * pnorm(-abs(outcome_assoc$BETA / outcome_assoc$SE))

in_window <- with(cis_pqtl, POS >= gene_start - cis_window & POS <= gene_end + cis_window)
cis_pqtl <- cis_pqtl[in_window, ]
cat('cis-pQTLs in window:', nrow(cis_pqtl), '\n')

instruments_raw <- subset(cis_pqtl, P < 5e-08)
instruments_raw$f_stat <- (instruments_raw$BETA / instruments_raw$SE)^2
instruments_raw <- subset(instruments_raw, f_stat >= 10)
cat('Genome-wide-sig cis instruments after F filter:', nrow(instruments_raw), '\n')

wd <- tempdir()
setwd(wd)
write.table(instruments_raw, 'cis_pqtl.tsv', sep = '\t', row.names = FALSE, quote = FALSE)
write.table(outcome_assoc, 'outcome_locus.tsv', sep = '\t', row.names = FALSE, quote = FALSE)

exposure_dat <- read_exposure_data(
  'cis_pqtl.tsv', sep = '\t',
  snp_col = 'SNP', beta_col = 'BETA', se_col = 'SE',
  effect_allele_col = 'A1', other_allele_col = 'A2',
  eaf_col = 'EAF', pval_col = 'P', samplesize_col = 'N'
)
outcome_dat <- read_outcome_data(
  'outcome_locus.tsv', snps = exposure_dat$SNP, sep = '\t',
  snp_col = 'SNP', beta_col = 'BETA', se_col = 'SE',
  effect_allele_col = 'A1', other_allele_col = 'A2',
  eaf_col = 'EAF', pval_col = 'P', samplesize_col = 'N'
)

dat <- harmonise_data(exposure_dat, outcome_dat, action = 2)
cat('SNPs after harmonisation:', nrow(dat), '\n')

if (nrow(dat) == 1) {
  wr <- mr(dat, method_list = 'mr_wald_ratio')
  cat('\n--- Wald ratio (single instrument) ---\n')
  print(wr[, c('method', 'b', 'se', 'pval')])
} else {
  res <- mr(dat, method_list = c('mr_ivw', 'mr_egger_regression', 'mr_weighted_median'))
  cat('\n--- cis-MR primary ---\n')
  print(res[, c('method', 'nsnp', 'b', 'se', 'pval')])
  cat('True causal beta_XY was:', true_beta_xy, '\n')
}

all_snps <- merge(cis_pqtl, outcome_assoc, by = 'SNP', suffixes = c('.exp', '.out'))
coloc_input_exp <- list(
  beta = all_snps$BETA.exp, varbeta = all_snps$SE.exp^2,
  snp = all_snps$SNP, position = all_snps$POS.exp,
  type = 'quant', N = all_snps$N.exp[1], MAF = pmin(all_snps$EAF.exp, 1 - all_snps$EAF.exp)
)
coloc_input_out <- list(
  beta = all_snps$BETA.out, varbeta = all_snps$SE.out^2,
  snp = all_snps$SNP, position = all_snps$POS.out,
  type = 'quant', N = all_snps$N.out[1], MAF = pmin(all_snps$EAF.out, 1 - all_snps$EAF.out)
)

coloc_res <- coloc.abf(coloc_input_exp, coloc_input_out, p1 = 1e-4, p2 = 1e-4, p12 = 1e-5)
cat('\n--- Coloc triangulation ---\n')
print(signif(coloc_res$summary, 3))
h4 <- coloc_res$summary['PP.H4.abf']
cat('PP.H4 (shared causal):', signif(h4, 3), if (h4 >= 0.7) ' -- DRUG-TARGET SUPPORTED' else ' -- NOT SUPPORTED', '\n')

file.remove('cis_pqtl.tsv', 'outcome_locus.tsv')
