# Does IdTaxa() itself (holding the trainingSet fixed) give identical results across repeated
# calls? Isolates: is the 480-vs-482 discrepancy vs the fix log due to LearnTaxa retraining
# variance, or IdTaxa() classification variance on a fixed trainingSet?
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

r1 <- IdTaxa(dna, trainingSet, strand = "both", threshold = 60, processors = NULL)
r2 <- IdTaxa(dna, trainingSet, strand = "both", threshold = 60, processors = NULL)

ranks <- c('domain','phylum','class','order','family','genus','species')
flat <- function(x) {
  taxa <- x$taxon[-1]; taxa[startsWith(taxa, 'unclassified_')] <- NA; length(taxa) <- length(ranks); taxa
}
f1 <- t(sapply(r1, flat)); colnames(f1) <- ranks
f2 <- t(sapply(r2, flat)); colnames(f2) <- ranks

cat("IdTaxa() x2 on SAME fixed trainingSet -- identical():", identical(f1, f2), "\n")
for (rank in ranks) {
  diff <- sum(f1[, rank] != f2[, rank], na.rm = TRUE) + sum(xor(is.na(f1[,rank]), is.na(f2[,rank])))
  cat(sprintf("  %-8s differ: %d / %d\n", rank, diff, nrow(f1)))
}
