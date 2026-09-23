.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))
dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/myreaudit"
prev <- readRDS(file.path(dir, "assigntax_all_runs.rds"))
sp_fa <- file.path(dir, "reaudit3_dada2_species.fasta")
sp1 <- addSpecies(prev$s1, sp_fa)
sp2 <- addSpecies(prev$s1, sp_fa)
cat("identical(addSpecies run1, run2):", identical(sp1, sp2), "\n")
cat("Done.\n")
