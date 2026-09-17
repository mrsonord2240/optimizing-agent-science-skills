# Input 4 (Variant B) -- Multivariable MR: LDL and HDL jointly on CHD, conditional F per exposure,
# IVW-MVMR, Q_A heterogeneity. Follows SKILL.md's "MVMR with Conditional F" section exactly
# (format_mvmr / strength_mvmr / ivw_mvmr / pleiotropy_mvmr).
# Synthetic data: two exposures share some SNPs (as MVMR requires), true direct effects known.

library(MVMR)

set.seed(21)
n_snps <- 60
true_b1 <- 0.30   # LDL -> CHD, direct
true_b2 <- -0.10  # HDL -> CHD, direct

beta_ldl <- rnorm(n_snps, 0.10, 0.03)
beta_hdl <- rnorm(n_snps, 0.08, 0.03) + 0.3 * beta_ldl  # some shared genetic architecture
se_ldl <- runif(n_snps, 0.01, 0.02)
se_hdl <- runif(n_snps, 0.01, 0.02)

beta_chd <- true_b1 * beta_ldl + true_b2 * beta_hdl + rnorm(n_snps, 0, 0.01)
se_chd <- runif(n_snps, 0.015, 0.025)

mvmr_dat <- format_mvmr(
  BXGs = cbind(beta_ldl, beta_hdl),
  BYG = beta_chd,
  seBXGs = cbind(se_ldl, se_hdl),
  seBYG = se_chd,
  RSID = paste0('rs', 1:n_snps)
)

cat('--- Conditional F per exposure (strength_mvmr) ---\n')
condF <- strength_mvmr(r_input = mvmr_dat, gencov = 0)
print(condF)

cat('\n--- MVMR-IVW ---\n')
mv_ivw <- ivw_mvmr(r_input = mvmr_dat)
print(mv_ivw)
cat('True direct effects were: LDL=', true_b1, ' HDL=', true_b2, '\n')

cat('\n--- Q_A heterogeneity (pleiotropy_mvmr) ---\n')
mv_qa <- tryCatch(pleiotropy_mvmr(r_input = mvmr_dat, gencov = 0),
                   error = function(e) { cat('pleiotropy_mvmr ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(mv_qa)) print(mv_qa)

# If any conditional F < 10, SKILL.md says switch to qhet_mvmr (Q-minimization).
if (any(condF[, 1] < 10)) {
  cat('\n--- Conditional F < 10 detected -- switching to qhet_mvmr per SKILL.md ---\n')
  qhet <- tryCatch(qhet_mvmr(mvmr_dat, pcor = cor(cbind(beta_ldl, beta_hdl)), CI = TRUE, iterations = 100),
                    error = function(e) { cat('qhet_mvmr ERROR:', conditionMessage(e), '\n'); NULL })
  if (!is.null(qhet)) print(qhet)
} else {
  cat('\nAll conditional F > 10; IVW-MVMR is the reported estimator (no qhet needed).\n')
}
