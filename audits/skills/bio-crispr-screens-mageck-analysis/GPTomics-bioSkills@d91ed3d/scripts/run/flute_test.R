library(MAGeCKFlute)
res <- tryCatch({
  FluteRRA(gene_summary = "input1_canonical.gene_summary.txt",
           sgrna_summary = "input1_canonical.sgrna_summary.txt",
           organism = "hsa",
           outdir = "flute_output")
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
print(res)
