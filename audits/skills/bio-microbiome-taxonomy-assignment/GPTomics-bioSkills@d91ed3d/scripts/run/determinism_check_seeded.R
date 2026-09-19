# Confirm the fix: does set.seed() before each call make assignTaxonomy() reproducible?
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))
data_dir <- "F:/OpenScience/audits/bio-microbiome-taxonomy-assignment/data"

fasta_lines <- readLines(file.path(data_dir, "rep-seqs.fasta"))
ids <- c(); seqs <- c(); cur_id <- NULL; cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (!is.null(cur_id)) { ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = "")) }
    cur_id <- substring(line, 2); cur_seq <- c()
  } else { cur_seq <- c(cur_seq, line) }
}
ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = ""))

set.seed(100)
taxa_run1 <- assignTaxonomy(unname(seqs), file.path(data_dir, "regionmatched_dada2_train.fasta"),
                             minBoot = 50, tryRC = TRUE, multithread = TRUE)
set.seed(100)
taxa_run2 <- assignTaxonomy(unname(seqs), file.path(data_dir, "regionmatched_dada2_train.fasta"),
                             minBoot = 50, tryRC = TRUE, multithread = TRUE)

for (rank in colnames(taxa_run1)) {
  diff <- sum(taxa_run1[, rank] != taxa_run2[, rank], na.rm = TRUE) + sum(xor(is.na(taxa_run1[,rank]), is.na(taxa_run2[,rank])))
  cat(sprintf("  %-8s differing calls WITH set.seed(100) before each call: %d / %d\n", rank, diff, nrow(taxa_run1)))
}
cat("\nMatrices identical() WITH set.seed(100):", identical(taxa_run1, taxa_run2), "\n")
