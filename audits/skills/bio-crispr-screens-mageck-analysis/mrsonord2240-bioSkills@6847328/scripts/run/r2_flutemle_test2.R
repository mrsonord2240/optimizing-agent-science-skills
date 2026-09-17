library(MAGeCKFlute)
dir.create("r2_flutemle_output2/MAGeCKFlute_test2", recursive = TRUE, showWarnings = FALSE)
res <- tryCatch({
  FluteMLE(gene_summary = "r2_input2_timecourse_mle.gene_summary.txt",
           treatname = "day21", ctrlname = "day7",
           proj = "test2",
           organism = "hsa",
           outdir = "r2_flutemle_output2/")
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
print(res)
