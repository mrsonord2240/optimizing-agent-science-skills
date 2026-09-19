library(decontam)
seqtab_nochim <- readRDS("seqtab_nochim.rds")
meta <- read.csv("../../../../audit-envs/microbiome-metagenomics-analyst/datagen/amplicon/sample_metadata.csv",
                  stringsAsFactors = FALSE, row.names = "sample")
# align row order
meta <- meta[rownames(seqtab_nochim), ]
cat("sample order check:\n"); print(cbind(rownames(seqtab_nochim), rownames(meta)))

contam <- isContaminant(seqtab_nochim, neg = meta$is_control, conc = meta$dna_conc,
                         method = 'combined', threshold = 0.1)
cat("\ncontaminant flags:\n")
print(contam$contaminant)
cat("\nn flagged:", sum(contam$contaminant), "of", ncol(seqtab_nochim), "\n")

flagged_seqs <- colnames(seqtab_nochim)[contam$contaminant]
truth <- read.delim("../../../../audit-envs/microbiome-metagenomics-analyst/datagen/amplicon/truth.tsv", stringsAsFactors=FALSE)
for (s in flagged_seqs) {
  m <- truth[truth$sequence == s, ]
  cat("Flagged ASV matches truth id:", m$id, m$genus, m$role, "\n")
}
