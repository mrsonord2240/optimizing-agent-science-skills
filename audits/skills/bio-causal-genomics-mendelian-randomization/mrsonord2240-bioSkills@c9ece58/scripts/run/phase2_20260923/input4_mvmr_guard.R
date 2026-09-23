# Input 4 (regression, P2-#1 focus) -- MVMR of two correlated exposures, same generative
# process as the prior audit's Input 4 (set.seed(21), which that audit found gave conditional
# F = 0.87/0.78 and a qhet_mvmr sign flip on exposure2). This re-run follows SKILL.md's NOW
# UPDATED "MVMR with Conditional F" code block verbatim, including the new
# `if (any(condF < 1)) stop(...)` guard that round 2 added. Expectation: the guard now fires
# BEFORE qhet_mvmr is ever called, so the sign-flip is prevented rather than silently returned.
library(MVMR)

set.seed(21)
n_snps <- 60
true_b1 <- 0.30
true_b2 <- -0.10

shared <- rnorm(n_snps, 0, 0.02)
beta_x1 <- shared + rnorm(n_snps, 0.03, 0.01)
beta_x2 <- shared * 0.9 + rnorm(n_snps, 0.02, 0.01)
se_x1 <- runif(n_snps, 0.008, 0.014)
se_x2 <- runif(n_snps, 0.009, 0.015)
beta_y <- true_b1 * beta_x1 + true_b2 * beta_x2 + rnorm(n_snps, 0, 0.01)
se_y <- runif(n_snps, 0.010, 0.018)

mvmr_dat <- format_mvmr(
    BXGs = cbind(beta_x1, beta_x2), BYG = beta_y,
    seBXGs = cbind(se_x1, se_x2), seBYG = se_y,
    RSID = paste0("rs", 1:n_snps)
)

condF <- strength_mvmr(r_input = mvmr_dat, gencov = 0)
cat("--- Conditional F per exposure ---\n")
print(condF)

mv_ivw <- ivw_mvmr(r_input = mvmr_dat)
cat("\n--- MVMR-IVW ---\n")
print(mv_ivw)
cat("True direct effects: exposure1=", true_b1, " exposure2=", true_b2, "\n")

# NEW round-2 guard, copied verbatim from the updated SKILL.md "MVMR with Conditional F" block:
guard_fired <- FALSE
guard_message <- NA
result <- tryCatch({
    if (any(condF < 1)) {
        stop("Conditional F < 1 for at least one exposure -- qhet_mvmr's own estimate is unreliable ",
             "at this floor (can flip an exposure's sign; see SKILL.md caveat below). Report MVMR-IVW ",
             "with a weak-instrument caveat instead, or acquire stronger/less-correlated instruments.")
    }
    qhet <- qhet_mvmr(r_input = mvmr_dat, pcor = cor(cbind(beta_x1, beta_x2)), CI = TRUE, iterations = 100)
    qhet
}, error = function(e) {
    guard_fired <<- TRUE
    guard_message <<- conditionMessage(e)
    NULL
})

cat("\n--- Round-2 guard result ---\n")
cat("Guard fired (stop() before qhet_mvmr was reached):", guard_fired, "\n")
if (guard_fired) cat("Guard message:", guard_message, "\n")
if (!guard_fired) {
    cat("qhet_mvmr WAS reached (guard did not fire) -- estimates:\n")
    print(result)
}
cat("\nP2-#1 REGRESSION RESULT: guard", if (guard_fired) "FIRED as documented -- sign-flip prevented." else "DID NOT FIRE -- regression, sign-flip risk still live.", "\n")
