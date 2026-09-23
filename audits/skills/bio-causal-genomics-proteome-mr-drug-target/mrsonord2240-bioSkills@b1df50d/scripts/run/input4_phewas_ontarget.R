# Input 4 (Variant B / phenome-wide): "Hold the PCSK9 cis-pQTL instrument set fixed and run cis-MR
# against all OpenGWAS outcomes with sample size >= 50,000 in European-ancestry cohorts. Bonferroni-
# correct over outcomes and report a phewas-style forest plot of significant hits."
#
# OpenGWAS is confirmed gated (401 without a JWT token; see TOOLS.md check_opengwas.R, verified
# 2026-09-17) -- available_outcomes()/extract_outcome_data() are NOT executed against the live API.
# Instead this reproduces the exact looped-IVW + Bonferroni logic from examples/phewas_drug_target_mr.R
# against 50 SYNTHETIC local "outcome" GWAS, with one planted true on-target effect (mimicking the
# real PCSK9 -> T2D discovery in Schmidt 2017 the SKILL.md cites) and the rest null by construction.

suppressPackageStartupMessages(library(TwoSampleMR))
set.seed(99)

n_snp <- 8  # a fixed, already-clumped cis-pQTL instrument set (post-QC, analogous to a saved exposure_dat)
maf <- runif(n_snp, 0.08, 0.42)
snp_id <- sprintf("rs%07d", 5000000 + seq_len(n_snp))
a1 <- sample(c("A","C","G","T"), n_snp, replace = TRUE)
a2 <- sapply(a1, function(x) sample(setdiff(c("A","C","G","T"), x), 1))
true_beta_exposure <- c(0.42, 0.31, 0.28, 0.19, 0.15, 0.11, 0.09, 0.07)  # decreasing per-SNP strength
n_protein <- 54219
se_exp <- sqrt(1/(2*maf*(1-maf)*n_protein)) * 3.0
beta_exp <- true_beta_exposure + rnorm(n_snp, 0, se_exp * 0.3)
exposure_dat <- format_data(
  data.frame(SNP=snp_id, BETA=beta_exp, SE=se_exp, A1=a1, A2=a2, EAF=maf, P=2*pnorm(-abs(beta_exp/se_exp))),
  type="exposure", snp_col="SNP", beta_col="BETA", se_col="SE",
  effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
cat("Fixed instrument set:", nrow(exposure_dat), "cis-pQTLs\n")

n_outcomes <- 50
outcome_names <- c("type_2_diabetes", paste0("synthetic_trait_", sprintf("%02d", 2:n_outcomes)))
true_mr_by_outcome <- rep(0, n_outcomes)
true_mr_by_outcome[1] <- 0.18          # planted on-target adverse effect: T2D (PCSK9-mimetic)
true_mr_by_outcome[7] <- 0.06          # planted weak/borderline effect, likely NOT surviving Bonferroni
n_out_gwas <- round(runif(n_outcomes, 50000, 250000))

scan_one <- function(i) {
  se_out <- sqrt(1/(2*maf*(1-maf)*n_out_gwas[i]*0.3*0.7)) * 1.2
  beta_out <- true_mr_by_outcome[i] * beta_exp + rnorm(n_snp, 0, se_out)
  outcome_dat <- format_data(
    data.frame(SNP=snp_id, BETA=beta_out, SE=se_out, A1=a1, A2=a2, EAF=maf,
               P=2*pnorm(-abs(beta_out/se_out))),
    type="outcome", snp_col="SNP", beta_col="BETA", se_col="SE",
    effect_allele_col="A1", other_allele_col="A2", eaf_col="EAF", pval_col="P")
  dat <- suppressMessages(harmonise_data(exposure_dat, outcome_dat, action = 2))
  if (nrow(dat) < 2) return(NULL)
  res <- suppressMessages(mr(dat, method_list = "mr_ivw"))
  res$outcome_id <- outcome_names[i]
  res$n_snp <- nrow(dat)
  res
}

results <- lapply(seq_len(n_outcomes), scan_one)
results_df <- do.call(rbind, Filter(Negate(is.null), results))
n_tests <- nrow(results_df)
results_df$p_bonf <- pmin(results_df$pval * n_tests, 1)
results_df$fdr <- p.adjust(results_df$pval, method = "BH")

top_hits <- subset(results_df, p_bonf < 0.05)
top_hits <- top_hits[order(top_hits$p_bonf), ]
cat("\nOutcomes tested:", n_tests, " Bonferroni threshold: 0.05/", n_tests, "=", 0.05/n_tests, "\n")
cat("Bonferroni-significant outcomes:", nrow(top_hits), "\n")
print(top_hits[, c("outcome_id","b","se","pval","p_bonf","n_snp")])

t2d_row <- subset(results_df, outcome_id == "type_2_diabetes")
weak_row <- subset(results_df, outcome_id == "synthetic_trait_07")
cat("\nPlanted on-target adverse effect (T2D-mimetic), true b=0.18: recovered b=",
    round(t2d_row$b,4), " p_bonf=", format(t2d_row$p_bonf, scientific=TRUE),
    " -> Bonferroni-significant:", t2d_row$p_bonf < 0.05, "\n")
cat("Planted borderline effect (true b=0.06): recovered b=", round(weak_row$b,4),
    " p_bonf=", format(weak_row$p_bonf, scientific=TRUE),
    " -> Bonferroni-significant:", weak_row$p_bonf < 0.05, "\n")
cat("\nDebug-shortcut check: this scan used the FULL", n_outcomes,
    "-outcome catalogue, not an `outcomes_filt$id[1:200]`-style truncation the skill itself flags as\n")
cat("'a debug shortcut, not a defensible pheWAS protocol'.\n")
