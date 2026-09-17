withCallingHandlers({
  library(GenomicSEM)
}, warning = function(w) { cat("WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning") })
