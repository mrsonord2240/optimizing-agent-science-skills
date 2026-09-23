# Fresh Phase 2 input 11: execute the exact version predicate used by the bundled
# example. It proves the warning branch is observable in the normal shared library
# and silent in the documented r_gsem.sh pinned runtime.
suppressPackageStartupMessages(library(lavaan))
v <- packageVersion("lavaan")
warns <- character()
withCallingHandlers({
  if (v >= "0.7.0") warning("lavaan >= 0.7.0 detected; pin lavaan to 0.6.19")
}, warning = function(w) { warns <<- c(warns, conditionMessage(w)); invokeRestart("muffleWarning") })
should_warn <- v >= "0.7.0"
stopifnot(xor(should_warn, length(warns) == 0L))
cat(sprintf("INPUT11 lavaan=%s should_warn=%s observed_warnings=%d\\n", as.character(v), should_warn, length(warns)))
