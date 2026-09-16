library(MAGeCKFlute)
res <- tryCatch({
  FluteRRA(gene_summary = "input1_canonical.gene_summary.txt",
           sgrna_summary = "input1_canonical.sgrna_summary.txt",
           organism = "hsa",
           proj = "test2",
           outdir = "flute_output3")
  "OK"
}, error = function(e) paste("ERROR:", conditionMessage(e)))
print(res)
print(list.files("flute_output3", recursive=TRUE))
