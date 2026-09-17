library(MAGeCKFlute)
dir.create("r2_flute_output/MAGeCKFlute_test1", recursive = TRUE, showWarnings = FALSE)

res <- tryCatch({
  FluteRRA(gene_summary = "r2_input1_canonical.gene_summary.txt",
           sgrna_summary = "r2_input1_canonical.sgrna_summary.txt",
           proj = "test1",
           organism = "hsa",
           outdir = "r2_flute_output/")
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
print(res)
print(list.files("r2_flute_output", recursive=TRUE))
