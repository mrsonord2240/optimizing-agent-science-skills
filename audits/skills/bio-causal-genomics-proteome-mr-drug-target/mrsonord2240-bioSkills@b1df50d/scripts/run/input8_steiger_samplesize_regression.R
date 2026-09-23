# Input 8 (new regression): apply the exact reverse-causation block in
# references/failure-modes.md after the final-pass repair.  This is synthetic
# summary data with a planted forward protein-to-disease effect.
suppressPackageStartupMessages(library(TwoSampleMR))
set.seed(20260923)

snps <- paste0("rssteiger", 1:4)
ea <- c("A", "C", "G", "T")
oa <- c("G", "T", "A", "C")
eaf <- c(0.18, 0.24, 0.31, 0.39)
bx <- c(0.22, 0.18, 0.15, 0.12)
bxse <- c(0.012, 0.011, 0.013, 0.012)
by <- 0.40 * bx + rnorm(4, 0, 0.004)
byse <- c(0.009, 0.010, 0.009, 0.011)

exposure_pQTL <- format_data(data.frame(SNP=snps, BETA=bx, SE=bxse, A1=ea, A2=oa,
                                         EAF=eaf, P=2*pnorm(-abs(bx/bxse))),
                              type="exposure", snp_col="SNP", beta_col="BETA", se_col="SE",
                              effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
outcome_GWAS <- format_data(data.frame(SNP=snps, BETA=by, SE=byse, A1=ea, A2=oa,
                                        EAF=eaf, P=2*pnorm(-abs(by/byse))),
                           type="outcome", snp_col="SNP", beta_col="BETA", se_col="SE",
                           effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")

# Literal workflow from failure-modes.md lines 42-48.
dat <- harmonise_data(exposure_pQTL, outcome_GWAS)
dat$samplesize.exposure <- 54219
dat$samplesize.outcome <- 122733
dat <- steiger_filtering(dat)
dat_forward <- dat[dat$steiger_dir, ]
dir_test <- directionality_test(dat_forward)

cat("Steiger rows:", nrow(dat), " forward:", nrow(dat_forward), "\n")
print(dat[, c("SNP", "steiger_dir", "steiger_pval")])
print(dir_test)
stopifnot(nrow(dat) == 4, nrow(dat_forward) >= 3, all(!is.na(dat$steiger_dir)),
          all(c("rsq.exposure", "rsq.outcome") %in% names(dat)))
cat("PASS: explicit sample sizes prevent the former steiger_filtering failure.\n")
