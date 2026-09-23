# Regression test for the shipped example's NA-safe SVA helper.
source("examples/batch_design.R")
stopifnot(exists("svobj_na"), all(is.finite(expr[stats::complete.cases(expr_na), , drop = FALSE])))
cat("PASS: shipped example completed with NA-present matrix; complete rows=", sum(stats::complete.cases(expr_na)), "/", nrow(expr_na), "\n", sep = "")
