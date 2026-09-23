# Input 1 -- Canonical: "Take this 1 Mb window centred on the GWAS lead SNP and run
# coloc.abf against the eQTL for the nearest gene. Report PP.H4 with p12 sensitivity."
# Fresh synthetic single-shared-causal-variant locus, following SKILL.md's
# "Standard coloc.abf Pipeline" code block verbatim (including the flag_excluded_region gate).

library(coloc)
set.seed(20260918)
n_snps <- 1000
positions <- sort(sample(10000000:11000000, n_snps))
maf <- runif(n_snps, 0.05, 0.5)

causal_idx <- 501
snp_ids <- paste0('rs', 1:n_snps)

gwas_df <- data.frame(CHR = 10, SNP = snp_ids, POS = positions, MAF = maf)
eqtl_df <- gwas_df

# Simulate GWAS (case-control) and eQTL (quant) beta/se around one shared causal SNP,
# with a modest LD-decay-like correlation structure between adjacent SNP effects
# to mimic real fine-mapping-adjacent noise (not literally fitted from genotypes here --
# this input targets the *pipeline mechanics*, cf. Input 2/3 which are genotype-derived).
true_beta_gwas <- 0.30
true_beta_eqtl <- 0.55
gwas_df$BETA <- rnorm(n_snps, 0, 0.02)
gwas_df$BETA[causal_idx] <- true_beta_gwas + rnorm(1, 0, 0.01)
gwas_df$SE <- runif(n_snps, 0.015, 0.03)
eqtl_df$BETA <- rnorm(n_snps, 0, 0.03)
eqtl_df$BETA[causal_idx] <- true_beta_eqtl + rnorm(1, 0, 0.02)
eqtl_df$SE <- runif(n_snps, 0.02, 0.05)

cat('PLANTED TRUTH: shared causal SNP =', snp_ids[causal_idx], '(index', causal_idx, ')\n')

# Programmatic MHC / chr8 inversion gate (verbatim from SKILL.md) -- locus here is chr10, expect no flag
flag_excluded_region <- function(chr, pos_bp, build = 'hg38') {
  if (build != 'hg38') stop('flag_excluded_region: liftover to hg38 first -- this Skill only documents hg38 MHC / chr8 inversion boundaries')
  chr <- gsub('^chr', '', as.character(chr))
  if (chr == '6' && pos_bp >= 25000000 && pos_bp <= 35000000) return('MHC')
  if (chr == '8' && pos_bp >= 8100000  && pos_bp <= 11900000) return('chr8_inversion')
  NA_character_
}
region_flag <- flag_excluded_region(chr = gwas_df$CHR[1], pos_bp = gwas_df$POS[causal_idx])
cat('Region flag (expect NA for this chr10 synthetic locus):', region_flag, '\n')
if (!is.na(region_flag)) stop('Unexpected exclusion flag for a chr10 test locus')

gwas_input <- list(beta = gwas_df$BETA, varbeta = gwas_df$SE^2, snp = gwas_df$SNP,
                    position = gwas_df$POS, type = 'cc', s = 0.30, N = 50000)
eqtl_input <- list(beta = eqtl_df$BETA, varbeta = eqtl_df$SE^2, snp = eqtl_df$SNP,
                    position = eqtl_df$POS, type = 'quant', sdY = 1, N = 500)

res <- coloc.abf(dataset1 = gwas_input, dataset2 = eqtl_input, p1 = 1e-4, p2 = 1e-4, p12 = 5e-6)
print(res$summary)

top_snp <- res$results$snp[which.max(res$results$SNP.PP.H4)]
cat(sprintf('\nTop per-SNP PP.H4: %s (planted causal: %s) match=%s\n',
            top_snp, snp_ids[causal_idx], top_snp == snp_ids[causal_idx]))

sens <- coloc::sensitivity(res, rule = 'H4 > 0.75', plot.manhattans = FALSE)
cat('\np12 sensitivity grid (subset):\n')
print(head(sens, 5))
cat(sprintf('\nPP.H4 stays > 0.75 across %d / %d grid points\n', sum(sens$pass), nrow(sens)))
