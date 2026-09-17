f <- "F:/OpenScience/wt/ra-gsem/causal-genomics/genomic-sem/examples/genomic_sem_commonfactor.R"
e <- tryCatch({ parse(f); "OK" }, error=function(e) paste("PARSE ERROR:", conditionMessage(e)))
cat(e, "\n")
# Also confirm the version guard triggers correctly under lavaan 0.7.2 (shared R-lib) vs
# silently under the pinned 0.6.19 (R-lib-genomicsem)
cat("Installed here: lavaan", as.character(packageVersion("lavaan")), "\n")
if (packageVersion('lavaan') >= '0.7.0') {
  cat("GUARD WOULD FIRE (as intended) under this lavaan version.\n")
} else {
  cat("GUARD CORRECTLY SILENT under pinned lavaan 0.6.19.\n")
}
