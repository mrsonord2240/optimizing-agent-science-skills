# THEIRS, generous "ceiling" run. Their SKILLs ship no code and do not run anything; this executes ONLY the
# estimator stack their references/method-library.md names (IVW, weighted median, Egger, Q, leave-one-out,
# Steiger, MR-PRESSO) with TwoSampleMR/MRPRESSO defaults, then applies their validation-evidence-hierarchy.md
# tier rules and downgrade triggers literally. No mode, no RAPS, no Isq/NOME check (not in their stack).
# usage: r.sh 03_theirs_ceiling.R <datadir> <beta_true>
suppressMessages({library(TwoSampleMR); library(MRPRESSO)})
args <- commandArgs(TRUE); d <- args[1]; btrue <- as.numeric(args[2])
ex <- read_exposure_data(file.path(d, "exposure_gwas.tsv"), sep = "\t", snp_col = "SNP", beta_col = "BETA",
  se_col = "SE", effect_allele_col = "A1", other_allele_col = "A2", eaf_col = "EAF", pval_col = "P", samplesize_col = "N")
ex <- subset(ex, pval.exposure < 5e-8)
ex$f_stat <- (ex$beta.exposure / ex$se.exposure)^2; ex <- subset(ex, f_stat >= 10)   # "explicit F review"
oy <- read_outcome_data(file.path(d, "outcome_gwas.tsv"), snps = ex$SNP, sep = "\t", snp_col = "SNP", beta_col = "BETA",
  se_col = "SE", effect_allele_col = "A1", other_allele_col = "A2", eaf_col = "EAF", pval_col = "P", samplesize_col = "N")
dat <- harmonise_data(ex, oy, action = 2)
prim <- mr(dat, method_list = c("mr_ivw", "mr_weighted_median", "mr_egger_regression"))
prim$covers_truth <- (prim$b - 1.96 * prim$se) <= btrue & btrue <= (prim$b + 1.96 * prim$se)
print(prim[, c("method", "nsnp", "b", "se", "pval", "covers_truth")])
het <- mr_heterogeneity(dat); ivwQ <- het$Q_pval[het$method == "Inverse variance weighted"]
pl <- mr_pleiotropy_test(dat); loo <- mr_leaveoneout(dat); loo <- loo[loo$SNP != "All", ]
st <- directionality_test(dat)
set.seed(42)
pr <- mr_presso(BetaOutcome = "beta.outcome", BetaExposure = "beta.exposure", SdOutcome = "se.outcome", SdExposure = "se.exposure",
  OUTLIERtest = TRUE, DISTORTIONtest = TRUE, data = dat, NbDistribution = 1000, SignifThreshold = 0.05)
gp <- pr$`MR-PRESSO results`$`Global Test`$Pvalue; gp_n <- as.numeric(gsub("<", "", gp))
b <- setNames(prim$b, prim$method); p <- setNames(prim$pval, prim$method)
ivw <- b["Inverse variance weighted"]
cat(sprintf("Q p=%.3g | Egger intercept p=%.3g | PRESSO global p=%s | LOO sign-stable=%s | Steiger correct=%s\n",
   ivwQ, pl$pval, gp, all(sign(loo$b) == sign(ivw)), st$correct_causal_direction))
# --- their tier rules (validation-evidence-hierarchy.md), literal ---
nominal <- p["Inverse variance weighted"] < 0.05
sens_qual <- nominal && sign(b["Weighted median"]) == sign(ivw) && sign(b["MR Egger"]) == sign(ivw) && all(sign(loo$b) == sign(ivw))
acceptable_profile <- ivwQ > 0.05 && pl$pval > 0.05 && gp_n > 0.05
downgrade <- (pl$pval < 0.05) || (gp_n < 0.05)   # "evidence of directional pleiotropy or unresolved outliers"
tier <- if (!nominal) "no signal" else if (downgrade) "DOWNGRADED (trigger fired)" else if (sens_qual && acceptable_profile) "sensitivity-qualified / robust prioritized" else "nominal only"
cat("Their tier assignment:", tier, "\n")
cat("Direction-only concordance (IVW, WM, Egger same sign):", sens_qual, "\n")
saveRDS(list(prim = prim, tier = tier, sens_qual_direction_only = sens_qual, egger_p = pl$pval, presso_p = gp), file.path(d, "theirs_ceiling_result.rds"))
