source_path <- "F:/OpenScience/wt/p2-reaudit-bio-power-analysis/experimental-design/power-analysis/examples/rnaseq_power.R"
lines <- readLines(source_path, warn = FALSE)
marker <- grep("^# ---------------------------------------------------------------------------$", lines)[1]
eval(parse(text = lines[1:(marker - 1)]))
must_fail <- function(expr) inherits(try(force(expr), silent = TRUE), "try-error")
valid <- checked_rnapower(depth = 2, n = 14, cv = .3, effect = 1.5, alpha = .05)
stopifnot(is.finite(valid), must_fail(checked_rnapower(depth = 2, n = 14, cv = .3, effect = 1.5, alpha = 1.5)), must_fail(checked_rnapower(depth = 2, n = 14, cv = -.3, effect = 1.5, alpha = .05)), must_fail(checked_rnapower(depth = 2, n = 14, cv = .3, effect = 1, alpha = .05)))
gate <- assess_realized_fdr(cbind(SS1 = c(3, 5, 8), `Actual FDR` = c(.04, .06, NaN), `Marginal power` = c(.4, .5, .6)), .05, 0)
stopifnot(identical(gate$decision, c("ACCEPT", "REJECT", "REJECT")))
cat(sprintf("valid_canonical_power=%.6f\n", valid))
print(gate)
cat("BULK_GUARD=PASS\n")
