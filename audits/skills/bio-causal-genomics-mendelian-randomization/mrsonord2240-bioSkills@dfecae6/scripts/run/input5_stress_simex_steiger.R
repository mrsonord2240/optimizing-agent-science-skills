# Input 5 (regression, P1 SIMEX + P2-#2 Steiger focus) -- same NOME-violated synthetic design
# as the prior audit's Input 5 (SIMEX correction), plus the round-2-fixed Steiger guard from
# SKILL.md's "Bidirectional and Steiger" section, copied verbatim: dat_fwd here has NO
# samplesize/pval columns (same as the prior audit's reproduction of the silent-NULL bug), so
# the guard should now `stop()` with a clear message instead of the prior "returned NULL"
# silent behavior.
library(TwoSampleMR)
library(simex)

set.seed(33)
n_snps <- 40
beta_exposure <- rnorm(n_snps, 0.03, 0.003)
se_exposure <- rnorm(n_snps, 0.025, 0.003)
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

cat("\n--- Bidirectional MR ---\n")
dat_fwd <- dat
dat_fwd$mr_keep <- TRUE
dat_fwd$id.exposure <- "exp"; dat_fwd$id.outcome <- "out"
dat_fwd$exposure <- "exp"; dat_fwd$outcome <- "out"
fwd <- mr(dat_fwd, method_list = "mr_ivw")
print(fwd[, c("method", "nsnp", "b", "se", "pval")])

dat_rev <- dat
dat_rev$beta.exposure <- dat$beta.outcome; dat_rev$se.exposure <- dat$se.outcome
dat_rev$beta.outcome <- dat$beta.exposure; dat_rev$se.outcome <- dat$se.exposure
dat_rev$mr_keep <- TRUE
dat_rev$id.exposure <- "out"; dat_rev$id.outcome <- "exp"
dat_rev$exposure <- "out"; dat_rev$outcome <- "exp"
rev <- mr(dat_rev, method_list = "mr_ivw")
print(rev[, c("method", "nsnp", "b", "se", "pval")])

cat("\n--- Steiger, round-2-fixed 'Bidirectional and Steiger' guard, no samplesize columns set ---\n")
guard_fired <- FALSE
guard_message <- NA
steiger_out <- tryCatch({
    dt <- directionality_test(dat_fwd)
    if (is.null(dt)) {
        stop("directionality_test() returned NULL -- dat needs samplesize_col set ",
             "on both read_*_data()/format_data() calls upstream; see the Standard ",
             "Workflow section above.")
    }
    dt
}, error = function(e) {
    guard_fired <<- TRUE
    guard_message <<- conditionMessage(e)
    NULL
})
cat("Guard fired (stop() instead of silent NULL):", guard_fired, "\n")
if (guard_fired) cat("Guard message:", guard_message, "\n")
cat("\nP2-#2 REGRESSION RESULT: Steiger guard", if (guard_fired) "FIRED with a clear stop() -- no more silent NULL." else "DID NOT FIRE -- regression, silent-NULL risk still live.", "\n")
