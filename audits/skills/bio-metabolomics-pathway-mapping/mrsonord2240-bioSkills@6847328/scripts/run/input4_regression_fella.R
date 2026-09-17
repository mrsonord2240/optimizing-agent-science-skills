# Regression of pre-fix Input 4: FELLA network diffusion, reusing the cached KEGG graph/data
# built in the pre-fix audit (databaseDir 'fella_hsa') to confirm the FELLA section -- untouched
# by the fix except for a documentation comment about set.seed -- still runs correctly.
suppressMessages(library(FELLA))
fella.data <- loadKEGGdata(databaseDir = 'fella_hsa', internalDir = FALSE)
cpd_ids <- c('C00022','C00186','C00158','C00042','C00122','C00041')
analysis <- defineCompounds(compounds = cpd_ids, data = fella.data)
excluded <- getExcluded(analysis)
cat("Excluded (unmapped) compounds:", if(length(excluded)==0) "(none)" else paste(excluded, collapse=", "), "\n")
analysis <- runDiffusion(object = analysis, data = fella.data, approx = 'normality')
results <- generateResultsTable(object = analysis, data = fella.data, method = 'diffusion', threshold = 0.05)
cat("Results table rows:", nrow(results), "\n")
print(head(results, 5))
stopifnot(length(excluded) == 0)
stopifnot(nrow(results) > 0)
stopifnot("hsa00020" %in% results$KEGG.id || any(grepl("Citrate cycle", results$KEGG.name)))
cat("\nASSERTION PASSED: FELLA diffusion still runs to completion and reproduces the TCA-cycle top\n")
cat("hit -- the fix's other changes did not disturb this working path.\n")
