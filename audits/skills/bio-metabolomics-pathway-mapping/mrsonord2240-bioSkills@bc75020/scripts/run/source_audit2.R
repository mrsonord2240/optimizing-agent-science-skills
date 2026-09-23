suppressMessages(library(MetaboAnalystR))
options(width=200)

show_full <- function(fname, ns="MetaboAnalystR", n=60) {
  cat("\n=====", fname, "=====\n")
  f <- tryCatch(getFromNamespace(fname, ns), error=function(e) NULL)
  if (is.null(f)) { cat("NOT FOUND\n"); return(invisible(NULL)) }
  src <- deparse(f)
  print(head(src, n))
}

show_full("MetaboliteMappingExact", n=80)
show_full(".get.my.lib", n=40)
show_full("load_httr", n=15)
show_full("api.base", n=5)
cat("\napi.base value: ")
print(tryCatch(getFromNamespace("api.base","MetaboAnalystR"), error=function(e) "NOT FOUND"))
