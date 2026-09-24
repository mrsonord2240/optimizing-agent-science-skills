# Follows bio-causal-genomics-mendelian-randomization SKILL.md "TwoSampleMR Standard Workflow"
# + MR-PRESSO + Isq/NOME + MR-RAPS + Steiger + LOO (examples/two_sample_mr.R), on the shared synthetic data.
# usage: r.sh 02_ours.R <datadir> <beta_true> [NbDistribution, SKILL says >=10000; 3000 used here because 10000 did not finish in 40 min on a shared machine]
suppressMessages({library(TwoSampleMR); library(MRPRESSO)})
args <- commandArgs(TRUE); d <- args[1]; btrue <- as.numeric(args[2]); NB <- if (length(args) >= 3) as.integer(args[3]) else 10000L
truth <- read.delim(file.path(d, "truth_snps.tsv"), stringsAsFactors = FALSE)
ex <- read_exposure_data(file.path(d, "exposure_gwas.tsv"), sep = "\t", snp_col = "SNP", beta_col = "BETA",
  se_col = "SE", effect_allele_col = "A1", other_allele_col = "A2", eaf_col = "EAF", pval_col = "P", samplesize_col = "N")
ex <- subset(ex, pval.exposure < 5e-8)
ex$f_stat <- (ex$beta.exposure / ex$se.exposure)^2
cat("sig SNPs:", nrow(ex), " mean F:", round(mean(ex$f_stat), 1), " F<10:", sum(ex$f_stat < 10), "\n")
ex <- subset(ex, f_stat >= 10)
# LD clumping skipped: synthetic SNPs are independent by construction (no LD panel exists for rs100001..)
oy <- read_outcome_data(file.path(d, "outcome_gwas.tsv"), snps = ex$SNP, sep = "\t", snp_col = "SNP", beta_col = "BETA",
  se_col = "SE", effect_allele_col = "A1", other_allele_col = "A2", eaf_col = "EAF", pval_col = "P", samplesize_col = "N")
dat <- harmonise_data(ex, oy, action = 2)
cat("harmonised SNPs:", nrow(dat), " mr_keep:", sum(dat$mr_keep), "\n")
prim <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression", "mr_weighted_median", "mr_weighted_mode"))
prim$lo <- prim$b - 1.96 * prim$se; prim$hi <- prim$b + 1.96 * prim$se
prim$covers_truth <- prim$lo <= btrue & btrue <= prim$hi
print(prim[, c("method", "nsnp", "b", "se", "pval", "lo", "hi", "covers_truth")])
het <- mr_heterogeneity(dat); print(het[, c("method", "Q", "Q_df", "Q_pval")])
pl <- mr_pleiotropy_test(dat); cat("Egger intercept:", signif(pl$egger_intercept, 3), "se", signif(pl$se, 3), "p", signif(pl$pval, 3), "\n")
isq <- TwoSampleMR::Isq(dat$beta.exposure, dat$se.exposure); cat("I2_GX:", round(isq, 3), "\n")
raps <- TwoSampleMR::mr_raps(b_exp = dat$beta.exposure, b_out = dat$beta.outcome, se_exp = dat$se.exposure, se_out = dat$se.outcome)
cat("MR-RAPS: b", signif(raps$b, 3), "se", signif(raps$se, 3), "p", signif(raps$pval, 3), "\n")
set.seed(42)
pr <- mr_presso(BetaOutcome = "beta.outcome", BetaExposure = "beta.exposure", SdOutcome = "se.outcome", SdExposure = "se.exposure",
  OUTLIERtest = TRUE, DISTORTIONtest = TRUE, data = dat, NbDistribution = NB, SignifThreshold = 0.05)
gp <- pr$`MR-PRESSO results`$`Global Test`$Pvalue; cat("PRESSO global p:", gp, "\n")
print(pr$`Main MR results`)
ot <- pr$`MR-PRESSO results`$`Outlier Test`
out_idx <- which(as.numeric(gsub("<", "", ot$Pvalue)) < 0.05 / nrow(dat))
cat("PRESSO outliers (Bonferroni):", length(out_idx), "\n")
if (!is.null(pr$`MR-PRESSO results`$`Distortion Test`)) print(pr$`MR-PRESSO results`$`Distortion Test`[c("Coefficient","Pvalue")])
pl_bad <- truth$planted_invalid[match(dat$SNP, truth$SNP)]
flag <- rep(FALSE, nrow(dat)); flag[out_idx] <- TRUE
cat(sprintf("Outlier detection vs planted-invalid: flagged=%d, true positives=%d, planted invalid in set=%d\n", sum(flag), sum(flag & pl_bad), sum(pl_bad)))
st <- directionality_test(dat); print(st[, c("snp_r2.exposure", "snp_r2.outcome", "correct_causal_direction", "steiger_pval")])
loo <- mr_leaveoneout(dat); loo <- loo[loo$SNP != "All", ]; cat("LOO IVW range:", signif(range(loo$b), 3), "\n")
# hand-rolled 'weighted-median/PRESSO-outlier-removed' check: IVW after dropping PRESSO outliers
if (length(out_idx)) { d2 <- dat[-out_idx, ]; r2 <- mr(d2, method_list = "mr_ivw"); cat("IVW after outlier removal: b", signif(r2$b, 3), "se", signif(r2$se, 3), "\n") }
saveRDS(list(prim = prim, het = het, pl = pl, isq = isq, raps = raps, presso_global_p = gp, flagged = sum(flag), tp = sum(flag & pl_bad)), file.path(d, "ours_result.rds"))
