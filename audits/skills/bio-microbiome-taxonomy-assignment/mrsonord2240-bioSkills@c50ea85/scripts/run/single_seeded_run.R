.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))
args <- commandArgs(trailingOnly = TRUE)
outfile <- args[1]
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
set.seed(100)
taxa <- assignTaxonomy(unname(seqs), ref, minBoot = 50, tryRC = TRUE, multithread = TRUE)
saveRDS(taxa, outfile)
cat("saved", outfile, "\n")
