# Does set.seed() before IdTaxa() (analogous to the assignTaxonomy fix) make it reproducible?
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
flat <- function(x) {
  taxa <- x$taxon[-1]; taxa[startsWith(taxa, 'unclassified_')] <- NA; length(taxa) <- length(ranks); taxa
}

cat("=== Test A: set.seed(100) before each IdTaxa() call, processors=NULL (multithreaded) ===\n")
set.seed(100)
r1 <- IdTaxa(dna, trainingSet, strand = "both", threshold = 60, processors = NULL)
set.seed(100)
r2 <- IdTaxa(dna, trainingSet, strand = "both", threshold = 60, processors = NULL)
f1 <- t(sapply(r1, flat)); colnames(f1) <- ranks
f2 <- t(sapply(r2, flat)); colnames(f2) <- ranks
cat("identical():", identical(f1, f2), "\n")
diff_genus <- sum(f1[,"genus"] != f2[,"genus"], na.rm=TRUE) + sum(xor(is.na(f1[,"genus"]), is.na(f2[,"genus"])))
cat("genus differ:", diff_genus, "/ 770\n\n")

cat("=== Test B: set.seed(100) before each call, processors=1 (single-threaded) ===\n")
set.seed(100)
r3 <- IdTaxa(dna, trainingSet, strand = "both", threshold = 60, processors = 1)
set.seed(100)
r4 <- IdTaxa(dna, trainingSet, strand = "both", threshold = 60, processors = 1)
f3 <- t(sapply(r3, flat)); colnames(f3) <- ranks
f4 <- t(sapply(r4, flat)); colnames(f4) <- ranks
cat("identical():", identical(f3, f4), "\n")
diff_genus2 <- sum(f3[,"genus"] != f4[,"genus"], na.rm=TRUE) + sum(xor(is.na(f3[,"genus"]), is.na(f4[,"genus"])))
cat("genus differ:", diff_genus2, "/ 770\n")
