# Regression baseline: reproduce the ORIGINAL bug (no set.seed) on the real fixture, to confirm
# the reference and environment do exhibit genuine stochasticity absent the fix.
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))

dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"
fasta_lines <- readLines(file.path(dir, "rep-seqs.fasta"))
ids <- c(); seqs <- c(); cur_id <- NULL; cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (!is.null(cur_id)) { ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = "")) }
    cur_id <- substring(line, 2); cur_seq <- c()
  } else { cur_seq <- c(cur_seq, line) }
}
ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = ""))

ref <- file.path(dir, "regionmatched_dada2_train.fasta")

r1 <- assignTaxonomy(unname(seqs), ref, minBoot = 50, tryRC = TRUE, multithread = TRUE)
r2 <- assignTaxonomy(unname(seqs), ref, minBoot = 50, tryRC = TRUE, multithread = TRUE)

cat("identical():", identical(r1, r2), "\n")
for (rank in colnames(r1)) {
  diff <- sum(r1[, rank] != r2[, rank], na.rm = TRUE) + sum(xor(is.na(r1[,rank]), is.na(r2[,rank])))
  cat(sprintf("  %-8s differ: %d / %d\n", rank, diff, nrow(r1)))
}
