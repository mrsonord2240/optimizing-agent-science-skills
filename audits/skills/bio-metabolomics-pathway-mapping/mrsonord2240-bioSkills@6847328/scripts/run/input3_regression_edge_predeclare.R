# Regression of pre-fix Input 3: mummichog fed a significant-features-only background (the
# Skill's own named pitfall), now with the fixed SKILL.md's required current.msg/err.vec
# predeclare. Pre-fix this crashed with "object 'current.msg' not found"; check it now surfaces
# a clean, catchable message instead.
suppressMessages(library(MetaboAnalystR))
current.msg <- character(0); err.vec <- character(0)
set.seed(123)
mSet <- InitDataObjects('mass_all', 'mummichog', FALSE)
mSet <- SetPeakFormat(mSet, 'mpt')
mSet <- UpdateInstrumentParameters(mSet, 5.0, 'negative')
mSet <- Read.PeakListData(mSet, '../data/input2b_peaks_significant_only_synthetic.csv')
result <- tryCatch(SanityCheckMummichogData(mSet), error = function(e) e)

cat("\n=== Outcome ===\n")
if (inherits(result, "error")) {
  cat("STILL CRASHES (predeclare fix did not help):", conditionMessage(result), "\n")
} else if (is.numeric(result)) {
  cat("Clean, catchable failure. Return value:", result, "\n")
  cat("current.msg:", paste(current.msg, collapse=" | "), "\n")
  stopifnot(length(current.msg) > 0)
  stopifnot(!grepl("not found", paste(current.msg, collapse=" ")))
  cat("\nASSERTION PASSED: predeclare fix converts the pre-fix crash into a clean, catchable\n")
  cat("diagnostic message on the exact input that crashed pre-fix.\n")
} else {
  cat("Unexpectedly succeeded (SanityCheckMummichogData did not reject the sig-only input).\n")
}
