library(MAGeCKFlute)
dir.create("r2_flutemle_output/MAGeCKFlute_test1", recursive = TRUE, showWarnings = FALSE)
res <- tryCatch({
  FluteMLE(gene_summary = "r2_input2_timecourse_mle.gene_summary.txt",
           treatname = "day21", ctrlname = "baseline",
           proj = "test1",
           organism = "hsa",
           outdir = "r2_flutemle_output/")
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
print(res)
print(list.files("r2_flutemle_output", recursive=TRUE))
