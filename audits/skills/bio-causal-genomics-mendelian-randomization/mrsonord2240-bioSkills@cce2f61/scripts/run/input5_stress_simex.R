# Input 5 (regression) -- NOME violation + SIMEX correction (now using the FIXED SKILL.md
# inline code block, precomputed weights vector) + bidirectional MR + Steiger, on a
# directional-pleiotropy, weak-NOME synthetic exposure. Also independently reproduces the
# pre-fix "naive/bare-column" crash to confirm it is still a real footgun (informational,
# not a regression -- SKILL.md's own new code no longer uses that pattern).
library(TwoSampleMR)
library(simex)

set.seed(33)
n_snps <- 40
# Weak NOME: se.exposure large relative to beta.exposure spread -> I^2_GX low
beta_exposure <- rnorm(n_snps, 0.03, 0.003)
se_exposure <- rnorm(n_snps, 0.025, 0.003)  # large measurement error -> NOME violated
true_slope <- 0.40
beta_outcome <- true_slope * beta_exposure + rnorm(n_snps, 0, 0.01)
se_outcome <- runif(n_snps, 0.010, 0.020)

dat <- data.frame(
    SNP = paste0("rs", 1:n_snps),
    beta.exposure = beta_exposure, se.exposure = se_exposure,
    beta.outcome = beta_outcome, se.outcome = se_outcome
)

isq <- TwoSampleMR::Isq(dat$beta.exposure, dat$se.exposure)
cat("I^2_GX:", round(isq, 3), if (isq < 0.9) " -- NOME VIOLATED; SIMEX correction required per SKILL.md\n" else " -- NOME OK\n")

cat("\n--- SIMEX correction, FIXED SKILL.md code (precomputed weights vector) ---\n")
w <- 1 / dat$se.outcome^2
egger_lm <- lm(beta.outcome ~ beta.exposure, weights = w, data = dat, x = TRUE, y = TRUE)
egger_simex <- simex(model = egger_lm, SIMEXvariable = "beta.exposure",
                      measurement.error = dat$se.exposure,
                      lambda = seq(0.5, 2, 0.5), B = 200,
                      fitting.method = "quadratic", asymptotic = FALSE)
cat("SIMEX-corrected slope:", round(coef(egger_simex)["beta.exposure"], 4),
    " (true slope:", true_slope, ")\n")
cat("Naive Egger slope:   ", round(coef(egger_lm)["beta.exposure"], 4), "\n")

cat("\n--- Naive/bare-column pattern (informational; SKILL.md no longer ships this) ---\n")
naive_result <- tryCatch({
    egger_lm_naive <- lm(beta.outcome ~ beta.exposure, weights = 1 / se.outcome^2, data = dat, x = TRUE, y = TRUE)
    simex(model = egger_lm_naive, SIMEXvariable = "beta.exposure",
          measurement.error = dat$se.exposure,
          lambda = seq(0.5, 2, 0.5), B = 200,
          fitting.method = "quadratic", asymptotic = FALSE)
    "did not crash"
}, error = function(e) paste("CRASH:", conditionMessage(e)))
cat("Naive pattern result:", naive_result, "\n")

cat("\n--- Bidirectional MR ---\n")
dat_fwd <- dat
dat_fwd$mr_keep <- TRUE
dat_fwd$id.exposure <- "exp"; dat_fwd$id.outcome <- "out"
dat_fwd$exposure <- "exp"; dat_fwd$outcome <- "out"
fwd <- mr(dat_fwd, method_list = "mr_ivw")
print(fwd[, c("method", "nsnp", "b", "se", "pval")])

# Reverse: swap exposure/outcome roles
dat_rev <- dat
dat_rev$beta.exposure <- dat$beta.outcome; dat_rev$se.exposure <- dat$se.outcome
dat_rev$beta.outcome <- dat$beta.exposure; dat_rev$se.outcome <- dat$se.exposure
dat_rev$mr_keep <- TRUE
dat_rev$id.exposure <- "out"; dat_rev$id.outcome <- "exp"
dat_rev$exposure <- "out"; dat_rev$outcome <- "exp"
rev <- mr(dat_rev, method_list = "mr_ivw")
print(rev[, c("method", "nsnp", "b", "se", "pval")])

cat("\n--- Steiger (per SKILL.md's own inline code -- no samplesize columns set) ---\n")
steiger_result <- tryCatch({
    dt <- directionality_test(dat_fwd)
    if (is.null(dt)) "returned NULL" else paste("dir=", dt$correct_causal_direction, "p=", signif(dt$steiger_pval, 3))
}, error = function(e) paste("ERROR:", conditionMessage(e)))
cat("Steiger result:", steiger_result, "\n")
