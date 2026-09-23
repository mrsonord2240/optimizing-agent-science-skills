# Phase 2 regression: execute the EValue call exactly as the fixed SKILL.md documents it.
suppressPackageStartupMessages(library(EValue))
acme_rr <- 1.30
acme_lower_rr <- 1.10
observed <- evalues.RR(acme_rr, lo = acme_lower_rr)
point_manual <- acme_rr + sqrt(acme_rr * (acme_rr - 1))
lower_manual <- acme_lower_rr + sqrt(acme_lower_rr * (acme_lower_rr - 1))
print(observed)
cat(sprintf("manual point=%.8f lower=%.8f\n", point_manual, lower_manual))
stopifnot(abs(observed["E-values", "point"] - point_manual) < 1e-8)
stopifnot(abs(observed["E-values", "lower"] - lower_manual) < 1e-8)
cat("ASSERT PASS: fixed SKILL.md invocation omits hi and agrees with the formula.\n")
