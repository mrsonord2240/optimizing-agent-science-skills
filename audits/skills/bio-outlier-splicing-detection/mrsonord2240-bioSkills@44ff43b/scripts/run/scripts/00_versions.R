suppressPackageStartupMessages({library(FRASER); library(OUTRIDER)})
for (p in c("FRASER","OUTRIDER","BiocParallel","dplyr","Rsamtools","GenomicAlignments","TxDb.Hsapiens.UCSC.hg19.knownGene","org.Hs.eg.db"))
  cat(p, tryCatch(as.character(packageVersion(p)), error=function(e) "NOT INSTALLED"), "\n")
cat(R.version.string, "\n")
ex <- function(pkg, f) cat(pkg, f, "exported:", f %in% getNamespaceExports(pkg), "\n")
for (f in c("estimateBestQ","findEncodingDim","filterExpression","OUTRIDER","results","OutriderDataSet")) ex("OUTRIDER", f)
for (f in c("currentType<-","fitMetrics<-","plotEncDimSearch","bestQ","calculatePSIValues","filterExpressionAndVariability","plotVolcano","estimateBestQ","countRNAData","FRASER","results","FraserDataSet","annotateRangesWithTxDb","createTestFraserDataSet")) ex("FRASER", f)
fm <- function(x) { f <- get(x); if (isGeneric(x)) { m <- tryCatch(findMethods(x)@names, error=function(e) NULL); cat(x, "is S4 generic; signature methods:", paste(head(m,8), collapse=" | "), "\n") } ; }
sh <- function(pkg, f) { fn <- getExportedValue(pkg, f); cat("\n", pkg, "::", f, " args:", paste(names(formals(fn)), collapse=", "), "\n") }
sh("FRASER","FraserDataSet"); sh("FRASER","FRASER"); sh("FRASER","filterExpressionAndVariability"); sh("FRASER","countRNAData"); sh("FRASER","results"); sh("FRASER","plotVolcano"); sh("FRASER","plotEncDimSearch"); sh("FRASER","calculatePSIValues")
sh("OUTRIDER","OutriderDataSet"); sh("OUTRIDER","OUTRIDER"); sh("OUTRIDER","filterExpression"); sh("OUTRIDER","estimateBestQ"); sh("OUTRIDER","findEncodingDim"); sh("OUTRIDER","results")
cat("\n--- FRASER hyperparameter API ---\n")
fe <- getNamespaceExports("FRASER"); cat("FRASER exports matching 'Q|OHT|optim|encod|hyper':", paste(sort(grep("Q$|OHT|optim|ncod|yper", fe, value=TRUE)), collapse=", "), "\n")
sh("FRASER","optimHyperParams"); sh("FRASER","bestQ"); sh("FRASER","plotEncDimSearch")
