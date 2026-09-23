library(crisprScore)
fn <- get("getAzimuthScores", envir = asNamespace("crisprScore"))
cat("crisprScore_version=", as.character(packageVersion("crisprScore")), "\n", sep = "")
cat("formals=", paste(names(formals(fn)), collapse = ","), "\n", sep = "")
result <- tryCatch({
  fn("ACCTATCGATGCTGATGCTAGATAAGGTTG", fork = FALSE)
}, error = function(e) {
  cat("expected_runtime_error=", conditionMessage(e), "\n", sep = "")
  NULL
})
if (!is.null(result)) {
  cat("unexpected_success=", paste(result, collapse = ","), "\n", sep = "")
  quit(status = 2)
}
