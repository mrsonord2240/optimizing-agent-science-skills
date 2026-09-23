# Syntax validation of every shipped R artifact copied from the exact source tip.
files <- c("scripts/assign_batches.R", "scripts/check_balance.R", "scripts/bridge_layout.R", "examples/batch_design.R")
for (f in files) parse(f)
cat("PASS: parsed ", length(files), " shipped R files.\n", sep = "")
