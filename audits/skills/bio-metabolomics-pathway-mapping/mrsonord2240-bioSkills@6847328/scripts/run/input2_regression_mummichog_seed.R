# Regression of pre-fix Input 2: mummichog/PSEA on the full 1500-feature synthetic table, now
# with the fixed SKILL.md's required current.msg/err.vec predeclare AND set.seed(123) added.
# Run TWICE to assert determinism (T3 gate) now that a seed is documented.
suppressMessages(library(MetaboAnalystR))

run_once <- function(tag) {
  current.msg <- character(0); err.vec <- character(0)
  set.seed(123)
  mSet <- InitDataObjects('mass_all', 'mummichog', FALSE)
  mSet <- SetPeakFormat(mSet, 'mpt')
  mSet <- UpdateInstrumentParameters(mSet, 5.0, 'negative')
  mSet <- Read.PeakListData(mSet, '../data/input2_peaks_full_synthetic.csv')
  mSet <- SanityCheckMummichogData(mSet)
  mSet <- SetPeakEnrichMethod(mSet, 'mum', 'v2')
  mSet <- SetMummichogPval(mSet, 0.2)
  mSet <- PerformPSEA(mSet, 'hsa_mfn', 'current', permNum = 200)
  res <- as.data.frame(mSet$mummi.resmat)
  saveRDS(res, sprintf("input2_seed_run_%s.rds", tag))
  res
}

res1 <- run_once("A")
res2 <- run_once("B")

cat("=== Run A (top 5) ===\n"); print(head(res1[order(res1$Gamma),], 5))
cat("=== Run B (top 5) ===\n"); print(head(res2[order(res2$Gamma),], 5))

common_cols <- intersect(colnames(res1), colnames(res2))
res1o <- res1[order(rownames(res1)), common_cols]
res2o <- res2[order(rownames(res2)), common_cols]
identical_result <- isTRUE(all.equal(res1o, res2o))
cat("\nRun A and Run B identical with set.seed(123):", identical_result, "\n")
stopifnot(identical_result)
cat("ASSERTION PASSED: seeding makes PerformPSEA's permutation output run-to-run deterministic.\n")
