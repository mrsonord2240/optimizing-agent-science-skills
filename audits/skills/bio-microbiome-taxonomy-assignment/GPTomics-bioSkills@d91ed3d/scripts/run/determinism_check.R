# Skill Veto T3 (Result Determinism) check: SKILL.md's DADA2 example (assign_silva.R) never calls
# set.seed() before assignTaxonomy(), despite the method being described in SKILL.md itself as
# "RDP naive Bayes (8-mer, 100 bootstraps)" -- bootstrap resampling is stochastic. Run the SAME
# call twice, back to back, with NO seed set (exactly as SKILL.md's shipped example does it), and
# diff the genus calls to see if this matters in practice.
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

# NOTE: deliberately NOT calling set.seed() -- reproducing exactly what SKILL.md's shipped
# assign_silva.R example does (it has no set.seed anywhere).
taxa_run1 <- assignTaxonomy(unname(seqs), file.path(data_dir, "regionmatched_dada2_train.fasta"),
                             minBoot = 50, tryRC = TRUE, multithread = TRUE)
taxa_run2 <- assignTaxonomy(unname(seqs), file.path(data_dir, "regionmatched_dada2_train.fasta"),
                             minBoot = 50, tryRC = TRUE, multithread = TRUE)

for (rank in colnames(taxa_run1)) {
  diff <- sum(taxa_run1[, rank] != taxa_run2[, rank], na.rm = TRUE) + sum(xor(is.na(taxa_run1[,rank]), is.na(taxa_run2[,rank])))
  cat(sprintf("  %-8s differing calls between run1 and run2 (no seed set): %d / %d\n", rank, diff, nrow(taxa_run1)))
}
identical_check <- identical(taxa_run1, taxa_run2)
cat("\nMatrices identical():", identical_check, "\n")
