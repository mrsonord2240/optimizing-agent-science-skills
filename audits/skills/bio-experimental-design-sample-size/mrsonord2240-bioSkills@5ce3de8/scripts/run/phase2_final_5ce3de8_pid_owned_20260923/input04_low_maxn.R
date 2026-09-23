source("/mnt/openscience/audits/bio-experimental-design-sample-size/run/phase2_final_5ce3de8_pid_owned_20260923/source_copy/sample-size/examples/sample_size_estimation.R")
low_result <- tryCatch({
  res <- safe_ssize(function() ssizeRNA_single(nGenes = 20000, pi0 = 0.95, m = 200,
                                                mu = 200, disp = 0.2, fc = 1.5, fdr = 0.05,
                                                power = 0.80, maxN = 2))
  require_reachable_n(res, maxN = 2)
  "unexpected-success"
}, error = conditionMessage)
stopifnot(identical(low_result, "no n <= 2 reaches the target; raise maxN or revise fc/dispersion"))
cat("OK source low-maxN contract emits documented unreachable-target message\n")
