# Input 10 (NEW, auditor-authored) -- MVMR guard boundary check. The round-2 fix added
# `if (any(condF < 1)) stop(...)` to SKILL.md's MVMR section. This input asks: does the guard
# over-fire and block the ordinary weak-but-not-degenerate regime (conditional F clearly above
# 1 but still below the IVW-safe floor of 10), where qhet_mvmr is SKILL.md's documented
# fallback and should still be allowed to run? Weaker shared-instrument correlation than
# Input 4/set.seed(21) is used deliberately to land conditional F in the 2-6 range.
library(MVMR)

set.seed(99)
n_snps <- 60
true_b1 <- 0.30
true_b2 <- -0.10

# Tuned (see _tune_condf2.R) to land conditional F ~2.2 for both exposures -- clearly above
# the round-2 guard's condF<1 floor, still well below the IVW-safe condF>10 floor.
shared <- rnorm(n_snps, 0, 0.001)
beta_x1 <- shared + rnorm(n_snps, 0.05, 0.012)
beta_x2 <- shared * 0.3 + rnorm(n_snps, 0.04, 0.012)
se_x1 <- runif(n_snps, 0.006, 0.009)
se_x2 <- runif(n_snps, 0.006, 0.009)
beta_y <- true_b1 * beta_x1 + true_b2 * beta_x2 + rnorm(n_snps, 0, 0.01)
se_y <- runif(n_snps, 0.010, 0.015)

mvmr_dat <- format_mvmr(
    BXGs = cbind(beta_x1, beta_x2), BYG = beta_y,
    seBXGs = cbind(se_x1, se_x2), seBYG = se_y,
    RSID = paste0("rs", 1:n_snps)
)

condF <- strength_mvmr(r_input = mvmr_dat, gencov = 0)
cat("--- Conditional F per exposure ---\n")
print(condF)
cat("Both exposures tuned to land ~2-3 (weak but not < 1, the round-2 guard's floor)\n")

mv_ivw <- ivw_mvmr(r_input = mvmr_dat)
cat("\n--- MVMR-IVW ---\n")
print(mv_ivw)
cat("True direct effects: exposure1=", true_b1, " exposure2=", true_b2, "\n")

guard_fired <- FALSE
guard_message <- NA
qhet_result <- tryCatch({
    if (any(condF < 1)) {
        stop("Conditional F < 1 for at least one exposure -- qhet_mvmr's own estimate is unreliable ",
             "at this floor (can flip an exposure's sign; see SKILL.md caveat below). Report MVMR-IVW ",
             "with a weak-instrument caveat instead, or acquire stronger/less-correlated instruments.")
    }
    qhet_mvmr(r_input = mvmr_dat, pcor = cor(cbind(beta_x1, beta_x2)), CI = TRUE, iterations = 200)
}, error = function(e) {
    guard_fired <<- TRUE
    guard_message <<- conditionMessage(e)
    NULL
})

cat("\n--- Round-2 guard result ---\n")
cat("Guard fired:", guard_fired, "(expected FALSE -- condF is >1 here)\n")
if (guard_fired) cat("Guard message (unexpected):", guard_message, "\n")
if (!guard_fired) {
    cat("qhet_mvmr reached and ran:\n")
    print(qhet_result)
}
cat("\nNEW INPUT RESULT: guard", if (!guard_fired) "correctly did NOT fire at condF > 1 -- no false-positive blocking of the documented fallback." else "INCORRECTLY fired above its own stated floor -- over-broad guard.", "\n")
