suppressPackageStartupMessages(library(PROPER))
funcs <- ls("package:PROPER")
cat("All exported PROPER functions:\n")
print(funcs)
cat("\nSearching each function's body for 'powerAveraged'...\n")
for (f in funcs) {
  obj <- tryCatch(get(f), error = function(e) NULL)
  if (is.function(obj)) {
    src <- tryCatch(paste(deparse(body(obj)), collapse = "\n"), error = function(e) "")
    if (grepl("powerAveraged", src, fixed = TRUE)) cat("FOUND in:", f, "\n")
  }
}
cat("Done searching.\n")
