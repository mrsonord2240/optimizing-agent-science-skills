suppressPackageStartupMessages(library(FRASER))
m <- getMethod("results", "FraserDataSet"); b <- body(m@.Data); loc <- b[[2]]
lf <- tryCatch(formals(eval(loc[[3]])), error=function(e) NULL)
if (is.null(lf)) { cat(paste(deparse(m@.Data)[1:40], collapse="\n"), "\n") } else { for (n in c("padjCutoff","deltaPsiCutoff","psiType","aggregate","all","minCount","rhoCutoff")) if (n %in% names(lf)) cat("results():", n, "default =", deparse(lf[[n]]), "\n") else cat("results():", n, "not a formal\n") }
if ("estimateBestQ" %in% getNamespaceExports("FRASER")) { e <- formals(FRASER::estimateBestQ); print(e[intersect(names(e), c("type","useOHT","q_param","noise_param"))]) }
for (p in c("FRASER","OUTRIDER")) { lic <- file.path(system.file(package = p), "LICENSE"); cat(p, "LICENSE file:", if (file.exists(lic)) paste(head(readLines(lic), 3), collapse=" | ") else "absent", "\n") }
