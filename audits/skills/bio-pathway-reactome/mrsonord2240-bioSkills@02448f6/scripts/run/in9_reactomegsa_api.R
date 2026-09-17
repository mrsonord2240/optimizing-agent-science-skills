# Input 9 (new, auditor-authored / Code Usability check): "I have RNA-seq counts for treated vs
# control and want to use ReactomeGSA the way SKILL.md's ReactomeGSA section shows, comparing
# pathway activity between conditions." Verifies the SKILL.md code block's function names and
# argument names actually exist in the installed ReactomeGSA -- a network call to the hosted
# AnalysisService is out of scope (no live service call from this env), so this checks API
# surface / M4 code usability rather than executing the comparison end to end.
suppressMessages(library(ReactomeGSA))

check_fn <- function(name, expected_args) {
  ok_exists <- exists(name, where = asNamespace("ReactomeGSA"), mode = "function")
  cat(sprintf("exists('%s'): %s\n", name, ok_exists))
  if (ok_exists) {
    f <- get(name, envir = asNamespace("ReactomeGSA"))
    actual_args <- names(formals(f))
    missing <- setdiff(expected_args, actual_args)
    cat(sprintf("  formals: %s\n", paste(actual_args, collapse = ", ")))
    cat(sprintf("  SKILL.md-named args present: %s\n", length(missing) == 0))
    if (length(missing) > 0) cat("  MISSING:", paste(missing, collapse = ", "), "\n")
  }
}

check_fn("ReactomeAnalysisRequest", c("method"))
check_fn("add_dataset", c("request", "expression_values", "name", "type",
                          "comparison_factor", "comparison_group_1", "comparison_group_2", "sample_data"))
check_fn("perform_reactome_analysis", c("request"))
check_fn("pathways", c("x"))
check_fn("analyse_sc_clusters", c("scObject", "use_interactors"))

cat("\npackageVersion('ReactomeGSA'):", as.character(packageVersion("ReactomeGSA")), "\n")

# Build a request object locally (no network call) to confirm the constructor itself runs.
req <- tryCatch(ReactomeAnalysisRequest(method = "Camera"), error = function(e) {
  cat("ERROR constructing request:", conditionMessage(e), "\n"); NULL
})
cat("Request object built locally (no network):", !is.null(req), "\n")
if (!is.null(req)) cat("class:", class(req), "\n")
