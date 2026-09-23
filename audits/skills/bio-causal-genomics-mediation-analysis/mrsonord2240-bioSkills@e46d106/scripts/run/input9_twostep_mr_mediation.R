# Input 9 (NEW -- not in pre-fix audit's 7 inputs) -- bio-causal-genomics-mediation-analysis
# Prompt: "I have independent GWAS summary statistics for a genetic instrument set on
# exposure E (LDL) and a separate set on a candidate mediator M (a liver enzyme
# biomarker), and outcome Y (CHD). Some SNPs might affect both E and M. Run two-step MR
# mediation (not MVMR) and check whether instrument independence holds before trusting
# the indirect effect."
#
# Following SKILL.md "MR-Mediation: Two-Step vs MVMR-Mediation" pattern (product-of-
# coefficients via two independent MR analyses) AND the "Two-step MR instrument
# independence" Common-Errors entry (SNP shared between E- and M-instruments biases the
# indirect effect toward the direct effect; documented fix = Steiger-filter M-instruments
# by keeping only SNPs where SNP-M F exceeds SNP-E F).
#
# This is a DIFFERENT method than Input 4 (MVMR-mediation, total-minus-direct) -- the
# pre-fix audit's 7 inputs never exercised two-step MR or the instrument-independence
# pitfall at all. SYNTHETIC SNP-level summary statistics (OpenGWAS is gated, confirmed
# 401 in audit-env TOOLS.md), built from an explicit structural model (not just noise) so
# a genuine bias mechanism (E has an unmediated direct effect c' on Y; pleiotropic SNPs
# leak that direct effect into a naive M-instrument set) is planted and checkable.

library(TwoSampleMR)

set.seed(9009)

# --- Structural truth ---
beta_EM_true <- 0.50   # E -> M causal effect
beta_MY_true <- 0.60   # M -> Y causal effect (via M only)
c_prime      <- 0.40   # E -> Y DIRECT effect, NOT through M (the confound that makes a
                        # pleiotropic SNP's Y-association not "exclusively through M")

n_Eonly  <- 40  # valid E-instruments: affect E only (no direct, non-E-mediated path to M)
n_shared <- 20  # PLEIOTROPIC: affect E strongly AND have a smaller direct (non-E-mediated) effect on M
n_Monly  <- 40  # valid M-instruments: affect M directly, no effect on E at all

se_snp <- 0.02  # flat per-SNP SE for simplicity (all well-powered, so any bias below is not just noise)

## E-only SNPs: instruments for Step 1 only
eff_E_Eonly <- rnorm(n_Eonly, 0.30, 0.04)
directM_Eonly <- rep(0, n_Eonly)                                   # no direct (pleiotropic) M path
effM_Eonly <- directM_Eonly + beta_EM_true * eff_E_Eonly + rnorm(n_Eonly, 0, 0.01)
effY_Eonly <- c_prime * eff_E_Eonly + beta_MY_true * effM_Eonly + rnorm(n_Eonly, 0, 0.01)

## Shared SNPs: strong E-effect (so they get pulled into exp_E) + a real but smaller direct M-path
## (i.e., genuinely pleiotropic -- this is what "same SNP set used for E in step 1 and M in step 2" means)
eff_E_shared <- rnorm(n_shared, 0.40, 0.04)
directM_shared <- rnorm(n_shared, 0.08, 0.02)
effM_shared <- directM_shared + beta_EM_true * eff_E_shared + rnorm(n_shared, 0, 0.01)
effY_shared <- c_prime * eff_E_shared + beta_MY_true * effM_shared + rnorm(n_shared, 0, 0.01)

## M-only SNPs: no effect on E at all -- the CORRECT, exclusion-respecting M-instruments
eff_E_Monly <- rep(0, n_Monly)
directM_Monly <- rnorm(n_Monly, 0.32, 0.04)
effM_Monly <- directM_Monly + rnorm(n_Monly, 0, 0.01)
effY_Monly <- beta_MY_true * effM_Monly + rnorm(n_Monly, 0, 0.01)   # no c_prime term: effect_on_E = 0

cat("=== Input 9: Two-step MR mediation with a planted instrument-independence violation ===\n")
cat("Planted: E->M =", beta_EM_true, ", M->Y =", beta_MY_true,
    ", E->Y direct (c') =", c_prime, "\n")
cat(n_Eonly, "SNPs valid for E only |", n_shared,
    "SNPs pleiotropic (strong E-effect + real direct M-effect) |", n_Monly, "SNPs valid for M only\n\n")

## ---- Step 1: E -> M, using ALL of E's instruments (E-only + shared), per SKILL.md's sketch ----
eff_E_step1 <- c(eff_E_Eonly, eff_E_shared)
effM_step1  <- c(effM_Eonly, effM_shared)
se_step1    <- rep(se_snp, n_Eonly + n_shared)

mr_EM <- mr_ivw(b_exp = eff_E_step1, b_out = effM_step1, se_exp = se_step1, se_out = se_step1)
cat("--- Step 1 (E -> M), all", length(eff_E_step1), "E-instruments ---\n")
cat("beta_EM:", round(mr_EM$b, 4), " SE:", round(mr_EM$se, 4), " p:", format.pval(mr_EM$pval),
    " [true =", beta_EM_true, "]\n\n")

## ---- Step 2a (NAIVE / WRONG): M-instruments = shared SNPs (same as used for E) + M-only SNPs ----
effM_step2_naive <- c(effM_shared, effM_Monly)
effY_step2_naive <- c(effY_shared, effY_Monly)
se_step2_naive   <- rep(se_snp, n_shared + n_Monly)

mr_MY_naive <- mr_ivw(b_exp = effM_step2_naive, b_out = effY_step2_naive,
                       se_exp = se_step2_naive, se_out = se_step2_naive)
indirect_naive <- mr_EM$b * mr_MY_naive$b
cat("--- Step 2a (NAIVE, M-instruments include the 20 SNPs shared with E's instrument set) ---\n")
cat("beta_MY:", round(mr_MY_naive$b, 4), " SE:", round(mr_MY_naive$se, 4),
    " [true =", beta_MY_true, "]\n")
cat("Indirect (product of coefficients):", round(indirect_naive, 4),
    " [true =", beta_EM_true * beta_MY_true, "]\n\n")

## ---- Step 2b (FIXED): Steiger-filter -- keep only SNPs where SNP-M F > SNP-E F ----
## SKILL.md's documented fix: F = (beta/se)^2; keep SNP as an M-instrument only if its
## F-stat for M exceeds its F-stat for E (SNP "looks like" an M-instrument, not an E-instrument).
F_M_shared <- (effM_shared / se_snp)^2
F_E_shared <- (eff_E_shared / se_snp)^2
steiger_keep_shared <- F_M_shared > F_E_shared
cat("--- Steiger filter on the 20 shared SNPs: SNP-M F > SNP-E F ---\n")
cat("Shared SNPs retained as valid M-instruments:", sum(steiger_keep_shared), "/", n_shared, "\n")
cat("Shared SNPs correctly EXCLUDED (fail the filter):", sum(!steiger_keep_shared), "/", n_shared, "\n\n")

effM_step2_filtered <- c(effM_shared[steiger_keep_shared], effM_Monly)
effY_step2_filtered <- c(effY_shared[steiger_keep_shared], effY_Monly)
se_step2_filtered   <- rep(se_snp, sum(steiger_keep_shared) + n_Monly)

mr_MY_filtered <- mr_ivw(b_exp = effM_step2_filtered, b_out = effY_step2_filtered,
                          se_exp = se_step2_filtered, se_out = se_step2_filtered)
indirect_filtered <- mr_EM$b * mr_MY_filtered$b
cat("--- Step 2b (Steiger-filtered M-instruments) ---\n")
cat("beta_MY:", round(mr_MY_filtered$b, 4), " SE:", round(mr_MY_filtered$se, 4),
    " [true =", beta_MY_true, "]\n")
cat("Indirect (product of coefficients):", round(indirect_filtered, 4),
    " [true =", beta_EM_true * beta_MY_true, "]\n\n")

## ---- Delta-method CI for the filtered (correct) indirect effect ----
indirect_se <- sqrt(mr_EM$b^2 * mr_MY_filtered$se^2 + mr_MY_filtered$b^2 * mr_EM$se^2)
indirect_ci <- indirect_filtered + c(-1.96, 1.96) * indirect_se
cat("--- Delta-method 95% CI, Steiger-filtered indirect effect ---\n")
cat("Indirect:", round(indirect_filtered, 4), " SE:", round(indirect_se, 4),
    " 95% CI: [", round(indirect_ci[1], 4), ",", round(indirect_ci[2], 4), "]\n\n")

true_indirect <- beta_EM_true * beta_MY_true
cat("=== Summary: does the documented pitfall reproduce, and does the documented fix correct it? ===\n")
cat("True indirect effect:", round(true_indirect, 4), "\n")
cat("Naive (pleiotropic SNPs left in M-instrument set):", round(indirect_naive, 4),
    " -- bias:", round(indirect_naive - true_indirect, 4), "\n")
cat("Steiger-filtered:", round(indirect_filtered, 4),
    " -- bias:", round(indirect_filtered - true_indirect, 4), "\n")
cat("Filtered closer to true than naive:", abs(indirect_filtered - true_indirect) < abs(indirect_naive - true_indirect), "\n")
