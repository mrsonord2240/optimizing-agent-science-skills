suppressPackageStartupMessages({library(FRASER); library(OUTRIDER)})
cat("FRASER", as.character(packageVersion("FRASER")), "\n")
m <- getMethod("results", "FraserDataSet"); f <- if (length(body(m@.Data)) > 0) m@.Data
cat("results() FRASER method formals:\n"); loc <- environment(m@.Data); 
print(formals(FRASER:::FRASER.results)[c("fdrCutoff","padjCutoff","deltaPsiCutoff","psiType","aggregate","all")])
fm <- formals(FRASER::FRASER); cat("FRASER() defaults: implementation/correction =", deparse(fm$correction), "; q =", deparse(fm$q), "\n")
print(fm)
fe <- formals(FRASER::filterExpressionAndVariability); print(fe[c("minExpressionInOneSample","quantile","quantileMinExpression","minDeltaPsi","filter")])
cat("\nFRASER DESCRIPTION License:", packageDescription("FRASER")$License, "\n")
cat("OUTRIDER DESCRIPTION License:", packageDescription("OUTRIDER")$License, "\n")
cat("OUTRIDER results() zScoreCutoff default & padjCutoff:\n"); print(formals(OUTRIDER:::compileResults.OUTRIDER)[c("padjCutoff","zScoreCutoff")])
