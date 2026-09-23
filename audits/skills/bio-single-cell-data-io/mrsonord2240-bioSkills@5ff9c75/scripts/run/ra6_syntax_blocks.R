for (i in 0:5) {
  fn <- paste0("ra6_block_", i, ".R")
  res <- tryCatch({ parse(fn); "OK" }, error = function(e) paste("SYNTAX ERROR:", conditionMessage(e)))
  cat(fn, ":", res, "\n")
}
