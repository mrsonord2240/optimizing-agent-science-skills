# Exercise the documented shared balance verifier on valid, soft-warning, and invalid layouts.
source("scripts/check_balance.R")

balanced <- expand.grid(condition = c("ctrl", "case"), batch = paste0("B", 1:3), rep = 1:4)
balanced$sex <- rep(c("F", "M"), length.out = nrow(balanced))
check_balance(balanced, "batch", c("condition", "sex"))

unbalanced <- data.frame(
  condition = c(rep("ctrl", 8), rep("case", 6)),
  batch = c(rep("B1", 5), rep("B2", 3), rep("B1", 2), rep("B2", 4)),
  stringsAsFactors = FALSE
)
warning_seen <- FALSE
withCallingHandlers(
  check_balance(unbalanced, "batch", "condition"),
  warning = function(w) { warning_seen <<- TRUE; cat("EXPECTED_WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning") }
)
stopifnot(warning_seen)

confounded <- data.frame(condition = c(rep("ctrl", 4), rep("case", 4)), batch = rep(c("B1", "B2"), each = 4))
err <- tryCatch({ check_balance(confounded, "batch", "condition"); NULL }, error = function(e) conditionMessage(e))
stopifnot(!is.null(err), grepl("confounded", err, fixed = TRUE))
cat("PASS: balanced accepted; avoidable imbalance warned; confounded layout rejected.\n")
