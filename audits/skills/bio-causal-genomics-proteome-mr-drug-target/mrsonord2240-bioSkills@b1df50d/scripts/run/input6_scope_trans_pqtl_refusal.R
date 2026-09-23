# Input 6 (Scope Boundary): "I only found 3 genome-wide-significant cis-pQTLs for my target gene GHRL
# in the +/-500kb window, which isn't very powered. I also have a trans-pQTL 4.2 Mb away that's
# genome-wide significant (P=3e-12) and strongly associated with the protein level -- can we add it to
# the instrument set to boost power for the cis-MR?"
#
# This tests the skill's own Decision-Tree row: "Trans-pQTL 'wants' to be an instrument | Refuse |
# Trans = horizontal pleiotropy by definition; use only as confirmatory". The correct agent response is
# to DECLINE adding the trans-pQTL as a primary instrument, per the skill's own documented rule, and
# explain why (exclusion-restriction violation). This script quantifies the consequence of ignoring
# that rule with a genuine executed comparison: a trans-pQTL that acts on the outcome through a
# DIFFERENT protein (not the target) is added to the instrument set, and MR-Egger/heterogeneity
# statistics are shown to flag it exactly as the skill's "Common Errors" table predicts.
# SYNTHETIC DATA, planted ground truth.

suppressPackageStartupMessages(library(TwoSampleMR))
set.seed(1010)

# 3 real cis-pQTLs (in the +/-500kb window), all instrumenting the target protein cleanly
n_cis <- 3
maf_cis <- runif(n_cis, 0.1, 0.4)
snp_cis <- sprintf("rs%07d", 7000001:7000003)
true_mr_effect <- 0.4
beta_exp_cis <- c(0.28, 0.22, 0.18)
se_exp_cis <- sqrt(1/(2*maf_cis*(1-maf_cis)*20000)) * 3
beta_exp_cis_obs <- beta_exp_cis + rnorm(n_cis, 0, se_exp_cis*0.2)
beta_out_cis <- true_mr_effect * beta_exp_cis + rnorm(n_cis, 0, se_exp_cis*0.2)

# 1 trans-pQTL, 4.2 Mb away: genuinely associated with the protein (e.g. via a trans-regulatory
# mechanism), but its effect on the OUTCOME runs through a DIFFERENT gene entirely (horizontal
# pleiotropy) -- classic exclusion-restriction violation.
trans_effect_on_protein <- 0.5
trans_direct_effect_on_outcome <- 0.9   # large, NOT mediated by the target protein
beta_exp_trans <- trans_effect_on_protein + rnorm(1, 0, 0.02)
se_exp_trans <- 0.018
beta_out_trans <- trans_direct_effect_on_outcome + rnorm(1, 0, 0.03)  # independent pleiotropic path
se_out_trans <- 0.03

a1 <- sample(c("A","C","G","T"), 4, replace = TRUE)
a2 <- sapply(a1, function(x) sample(setdiff(c("A","C","G","T"), x), 1))

exp_df <- data.frame(SNP = c(snp_cis, "rs7999999"),
                      BETA = c(beta_exp_cis_obs, beta_exp_trans),
                      SE = c(se_exp_cis, se_exp_trans),
                      A1 = a1, A2 = a2, EAF = c(maf_cis, 0.25),
                      P = 2*pnorm(-abs(c(beta_exp_cis_obs, beta_exp_trans)/c(se_exp_cis, se_exp_trans))))
out_df <- data.frame(SNP = c(snp_cis, "rs7999999"),
                      BETA = c(beta_out_cis, beta_out_trans),
                      SE = c(se_exp_cis, se_out_trans),
                      A1 = a1, A2 = a2, EAF = c(maf_cis, 0.25),
                      P = 2*pnorm(-abs(c(beta_out_cis, beta_out_trans)/c(se_exp_cis, se_out_trans))))

exposure_dat <- format_data(exp_df, type="exposure", snp_col="SNP", beta_col="BETA", se_col="SE",
                             effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
outcome_dat <- format_data(out_df, type="outcome", snp_col="SNP", beta_col="BETA", se_col="SE",
                            effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
dat_all <- suppressMessages(harmonise_data(exposure_dat, outcome_dat, action = 2))

dat_cis_only <- subset(dat_all, SNP %in% snp_cis)

cat("=== CORRECT: cis-only instrument set (per skill's Decision Tree: refuse the trans-pQTL) ===\n")
res_cis <- mr(dat_cis_only, method_list = c("mr_ivw"))
print(res_cis[, c("method","nsnp","b","se","pval")])
cat("Ground-truth cis-MR effect:", true_mr_effect, "\n")

cat("\n=== IF the trans-pQTL is added anyway (what the user asked for) ===\n")
res_all <- mr(dat_all, method_list = c("mr_ivw","mr_egger_regression"))
print(res_all[, c("method","nsnp","b","se","pval")])
egger_int <- mr_pleiotropy_test(dat_all)
cat("MR-Egger intercept test (should flag directional pleiotropy from the trans SNP):\n")
print(egger_int[, c("egger_intercept","se","pval")])
het <- mr_heterogeneity(dat_all, method_list = "mr_ivw")
cat("\nCochran's Q heterogeneity (should be inflated by the trans-pQTL outlier):\n")
print(het)

cat("\n-- Verdict --\n")
cat("Cis-only IVW b =", round(res_cis$b[1],4), "(matches ground truth ", true_mr_effect, ")\n")
cat("With trans-pQTL, IVW b =", round(res_all$b[res_all$method=="Inverse variance weighted"],4),
    "-- pulled toward the trans SNP's non-causal, pleiotropic effect, exactly the distortion the\n")
cat("skill's Decision Tree rule ('Trans-pQTL wants to be an instrument -> Refuse') exists to prevent.\n")
cat("CORRECT AGENT BEHAVIOUR: decline to add the trans-pQTL as a primary instrument; offer it only as\n")
cat("confirmatory evidence ('does the trans-regulator gene also predict outcome?'), and recommend\n")
cat("widening the cis-window (to 1Mb, if a documented distal regulatory element exists) or accepting\n")
cat("the underpowered 3-SNP cis-only analysis as 'minimum publishable cis-MR' instead.\n")
