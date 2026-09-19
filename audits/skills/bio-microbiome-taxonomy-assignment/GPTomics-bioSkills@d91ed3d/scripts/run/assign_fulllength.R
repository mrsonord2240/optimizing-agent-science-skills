# Input 3 (Edge) part A: naive full-length classifier applied to real V4 ASVs.
# Tests SKILL.md's "Trap 1" claim: a full-length-trained classifier on a V4 (~250bp) read
# mismatches k-mer composition and degrades calls, vs the region-matched classifier (part B).
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))

data_dir <- "F:/OpenScience/audits/bio-microbiome-taxonomy-assignment/data"

# Read the 770 real V4 ASVs (moving-pictures dataset, EMP 515F/806R, DADA2-denoised in QIIME2)
fasta_lines <- readLines(file.path(data_dir, "rep-seqs.fasta"))
ids <- c(); seqs <- c(); cur_id <- NULL; cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (!is.null(cur_id)) { ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = "")) }
    cur_id <- substring(line, 2); cur_seq <- c()
  } else {
    cur_seq <- c(cur_seq, line)
  }
}
ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = ""))
names(seqs) <- ids
cat("Loaded", length(seqs), "real V4 ASVs (moving-pictures, 515F/806R, DADA2-denoised)\n")
cat("Example length:", nchar(seqs[1]), "bp\n")

t0 <- Sys.time()
taxa_full <- assignTaxonomy(unname(seqs), file.path(data_dir, "fulllength_dada2_train.fasta"),
                             minBoot = 50, tryRC = TRUE, multithread = TRUE)
cat("assignTaxonomy (FULL-LENGTH ref, 60000-seq SILVA subsample) took",
    round(as.numeric(Sys.time() - t0, units = "secs"), 1), "sec\n")
# NOTE: keep rownames as the actual ASV sequences (dada2 default: this is what assignTaxonomy()
# already set them to). addSpecies() re-derives the query sequence FROM rownames(taxtab) -- do
# not overwrite them with the ASV hash IDs or addSpecies() will try to parse the ID as DNA.
id_by_seq <- setNames(ids, unname(seqs))

cat("\n=== FULL-LENGTH classifier on V4 ASVs: assigned fraction per rank ===\n")
for (rank in colnames(taxa_full)) {
  assigned <- sum(!is.na(taxa_full[, rank]))
  cat(sprintf("  %-8s %d/%d (%.1f%%)\n", rank, assigned, nrow(taxa_full), 100 * assigned / nrow(taxa_full)))
}

saveRDS(taxa_full, file.path(data_dir, "taxa_fulllength.rds"))
saveRDS(id_by_seq, file.path(data_dir, "id_by_seq.rds"))
write.csv(taxa_full, file.path(data_dir, "taxa_fulllength.csv"))
cat("\nSaved taxa_fulllength.rds / .csv (rownames = ASV sequences, ASV IDs saved separately)\n")
