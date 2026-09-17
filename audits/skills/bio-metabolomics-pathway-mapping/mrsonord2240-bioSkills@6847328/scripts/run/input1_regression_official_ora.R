# Regression of pre-fix Input 1: the OFFICIAL documented background-corrected ORA path, exactly
# as the FIXED SKILL.md now shows it (with the required current.msg/err.vec predeclare and the
# required Setup.KEGGReferenceMetabolome() call added ahead of SetMetabolomeFilter).
suppressMessages(library(MetaboAnalystR))

current.msg <- character(0); err.vec <- character(0)  # required -- fixed SKILL.md's Version Compatibility

mSet <- InitDataObjects('conc', 'pathora', FALSE)
mSet <- SetOrganism(mSet, 'hsa')
compounds <- c('Pyruvate', 'L-Lactate', 'Citrate', 'Succinate', 'Fumarate', 'L-Alanine',
               'L-Glutamate', 'L-Glutamine', 'Malate', 'Isocitrate', 'Oxaloacetate', 'Acetyl-CoA')
mSet <- Setup.MapData(mSet, compounds)
mSet <- CrossReferencing(mSet, 'name')
mSet <- CreateMappingResultTable(mSet)
mSet <- SetKEGG.PathLib(mSet, 'hsa', 'current')

mSet <- SetMetabolomeFilter(mSet, TRUE)
mSet <- Setup.KEGGReferenceMetabolome(mSet, '../data/input1_reference_metabolome_synthetic.txt')

result <- CalculateOraScore(mSet, 'rbc', 'hyperg')

cat("\n=== Result class/value ===\n")
cat("is.numeric(result):", is.numeric(result), "\n")
if (is.numeric(result)) {
  cat("Result value:", result, "\n")
  cat("current.msg:", paste(current.msg, collapse=" | "), "\n")
  stopifnot(length(current.msg) > 0)           # assert the REAL diagnostic message printed, not a crash
  stopifnot(!grepl("current.msg", paste(current.msg, collapse=" "), fixed=TRUE))  # not the meta-crash message itself
  cat("\nASSERTION PASSED: predeclare fix works -- clean, catchable failure with a real message,\n")
  cat("no 'object current.msg not found' crash.\n")
} else {
  ora <- as.data.frame(result$analSet$ora.mat)
  cat("Filtered ORA SUCCEEDED (unexpected vs SKILL.md's documented behavior) -- printing result:\n")
  print(head(ora, 10))
}
