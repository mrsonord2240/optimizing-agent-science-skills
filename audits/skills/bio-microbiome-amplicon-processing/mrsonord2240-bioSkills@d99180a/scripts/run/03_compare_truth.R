seqtab <- readRDS("seqtab_nochim.rds")
asvs <- colnames(seqtab)
truth <- read.delim("../../../../audit-envs/microbiome-metagenomics-analyst/datagen/amplicon/truth.tsv", stringsAsFactors=FALSE)
cat("n ASVs in output:", length(asvs), "\n")
cat("n truth entries:", nrow(truth), "\n\n")
cat("ASV lengths:\n"); print(table(nchar(asvs)))
cat("\n")
for (i in seq_len(nrow(truth))) {
  ref <- truth$sequence[i]
  retained <- ref %in% asvs
  cat(sprintf("%-15s %-20s %-15s retained=%s\n", truth$id[i], truth$genus[i], truth$role[i], retained))
}
cat("\nExtra ASVs not matching any truth entry:\n")
extra <- asvs[!asvs %in% truth$sequence]
cat(length(extra), "\n")
