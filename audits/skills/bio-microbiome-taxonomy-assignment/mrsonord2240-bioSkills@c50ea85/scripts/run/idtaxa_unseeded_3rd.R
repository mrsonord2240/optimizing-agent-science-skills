.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(DECIPHER))
dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"
trainingSet <- readRDS(file.path(dir, "trainingSet.rds"))
fasta_lines <- readLines(file.path(dir, "rep-seqs.fasta"))
ids <- c(); seqs <- c(); cur_id <- NULL; cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (!is.null(cur_id)) { ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = "")) }
    cur_id <- substring(line, 2); cur_seq <- c()
  } else { cur_seq <- c(cur_seq, line) }
}
ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = ""))
dna <- DNAStringSet(unname(seqs)); names(dna) <- ids
ranks <- c('domain','phylum','class','order','family','genus','species')
flat <- function(x) { taxa <- x$taxon[-1]; taxa[startsWith(taxa, 'unclassified_')] <- NA; length(taxa) <- length(ranks); taxa }

r5 <- IdTaxa(dna, trainingSet, strand = "both", threshold = 60, processors = NULL)
f5 <- t(sapply(r5, flat)); colnames(f5) <- ranks
saveRDS(f5, file.path(dir, "idtaxa_unseeded_run3.rds"))
f1 <- readRDS(file.path(dir, "idtaxa_new_flat.csv"))  # not rds, skip
cat("3rd unseeded run genus assigned:", sum(!is.na(f5[,"genus"])), "/770\n")
