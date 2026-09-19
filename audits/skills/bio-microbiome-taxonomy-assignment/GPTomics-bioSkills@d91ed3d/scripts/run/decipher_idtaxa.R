# Input 4 (Variant B): DECIPHER IdTaxa -- conservative, novelty-aware classification --
# trained (LearnTaxa) on the real, region-matched (515-806) SILVA 138 subset, applied to the
# same 770 real V4 ASVs used for Inputs 1-3.
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(DECIPHER))
data_dir <- "F:/OpenScience/audits/bio-microbiome-taxonomy-assignment/data"

# Load region-matched reference: seqid \t Root;domain;...;genus; \t seq
tax_lines <- readLines(file.path(data_dir, "regionmatched_decipher_tax.tsv"))
ref_ids <- character(length(tax_lines)); ref_tax <- character(length(tax_lines)); ref_seq <- character(length(tax_lines))
for (i in seq_along(tax_lines)) {
  parts <- strsplit(tax_lines[i], "\t", fixed = TRUE)[[1]]
  ref_ids[i] <- parts[1]; ref_tax[i] <- parts[2]; ref_seq[i] <- parts[3]
}
cat("Reference (region-matched V4) sequences for training:", length(ref_seq), "\n")
ref_dna <- DNAStringSet(ref_seq)
names(ref_dna) <- ref_ids

t0 <- Sys.time()
trainingSet <- LearnTaxa(ref_dna, taxonomy = ref_tax)
cat("LearnTaxa (real region-matched SILVA subset) took",
    round(as.numeric(Sys.time() - t0, units = "mins"), 2), "min\n")

# Load the 770 real V4 query ASVs
fasta_lines <- readLines(file.path(data_dir, "rep-seqs.fasta"))
ids <- c(); seqs <- c(); cur_id <- NULL; cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (!is.null(cur_id)) { ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = "")) }
    cur_id <- substring(line, 2); cur_seq <- c()
  } else { cur_seq <- c(cur_seq, line) }
}
ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = ""))
query <- DNAStringSet(seqs)
names(query) <- ids

t1 <- Sys.time()
ids_result <- IdTaxa(query, trainingSet, strand = "both", threshold = 60, processors = NULL)
cat("IdTaxa took", round(as.numeric(Sys.time() - t1, units = "secs"), 1), "sec\n")

ranks <- c("domain", "phylum", "class", "order", "family", "genus")
taxa_idtaxa <- t(sapply(ids_result, function(x) {
  out <- x$taxon[match(ranks, x$rank)]
  out[startsWith(replace(out, is.na(out), ""), "unclassified_")] <- NA
  out
}))
colnames(taxa_idtaxa) <- ranks
rownames(taxa_idtaxa) <- ids

cat("\n=== IdTaxa (region-matched training): assigned fraction per rank ===\n")
for (rank in ranks) {
  assigned <- sum(!is.na(taxa_idtaxa[, rank]))
  cat(sprintf("  %-8s %d/%d (%.1f%%)\n", rank, assigned, nrow(taxa_idtaxa), 100 * assigned / nrow(taxa_idtaxa)))
}
n_unclassified_root <- sum(sapply(ids_result, function(x) length(x$taxon) == 1))
cat(sprintf("\nCompletely unclassified (refused at root): %d/%d\n", n_unclassified_root, length(ids_result)))

saveRDS(ids_result, file.path(data_dir, "idtaxa_result.rds"))
saveRDS(taxa_idtaxa, file.path(data_dir, "taxa_idtaxa.rds"))
write.csv(taxa_idtaxa, file.path(data_dir, "taxa_idtaxa.csv"))
cat("\nSaved idtaxa_result.rds / taxa_idtaxa.rds\n")
