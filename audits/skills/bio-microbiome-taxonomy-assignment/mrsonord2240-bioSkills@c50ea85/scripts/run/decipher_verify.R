# Re-audit: independently verify the DECIPHER IdTaxa flattening fix end-to-end.
# Train a real LearnTaxa() trainingSet from the real 60k region-matched SILVA subsample (no rank=
# argument -- the natural/only path SKILL.md demonstrates), classify the real 770 ASVs with IdTaxa,
# then flatten with the FIXED positional code from SKILL.md's DECIPHER section, and independently
# recompute the genus-assignment rate rather than trusting the fix log's 482/770 (62.6%) number.
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(DECIPHER))
suppressPackageStartupMessages(library(dada2))

dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"

# --- Load real 770 ASVs ---
fasta_lines <- readLines(file.path(dir, "rep-seqs.fasta"))
ids <- c(); seqs <- c(); cur_id <- NULL; cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (!is.null(cur_id)) { ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = "")) }
    cur_id <- substring(line, 2); cur_seq <- c()
  } else { cur_seq <- c(cur_seq, line) }
}
ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = ""))
cat("Real ASVs:", length(seqs), "\n")

# --- Load the real region-matched SILVA taxonomy TSV (fid\ttaxonomy\tseq), same file the DADA2
# ref was derived from, and build a DNAStringSet + taxonomy vector for LearnTaxa() -- NO rank=
# argument, exactly what SKILL.md's new training example shows. ---
tax_tsv <- file.path(dir, "regionmatched_decipher_tax.tsv")
con <- file(tax_tsv, "r", encoding = "UTF-8")
fids <- c(); taxons <- c(); refseqs <- c()
repeat {
  line <- readLines(con, n = 1)
  if (length(line) == 0) break
  parts <- strsplit(line, "\t", fixed = TRUE)[[1]]
  if (length(parts) < 3) next
  fids <- c(fids, parts[1]); taxons <- c(taxons, parts[2]); refseqs <- c(refseqs, parts[3])
}
close(con)
cat("Reference training seqs:", length(refseqs), "\n")

refset <- DNAStringSet(refseqs)
names(refset) <- fids

cat("\nTraining LearnTaxa() (no rank= argument) -- this takes a while on 60k real seqs...\n")
t0 <- Sys.time()
trainingSet <- LearnTaxa(refset, taxonomy = taxons)
cat(sprintf("LearnTaxa done in %.1f min\n", as.numeric(Sys.time() - t0, units = "mins")))
saveRDS(trainingSet, file.path(dir, "trainingSet.rds"))

dna <- DNAStringSet(unname(seqs))
names(dna) <- ids

cat("\nRunning IdTaxa() on real 770 ASVs...\n")
t0 <- Sys.time()
ids_result <- IdTaxa(dna, trainingSet, strand = "both", threshold = 60, processors = NULL)
cat(sprintf("IdTaxa done in %.1f sec\n", as.numeric(Sys.time() - t0, units = "secs")))
saveRDS(ids_result, file.path(dir, "idtaxa_result_reaudit.rds"))

cat("\nDoes trainingSet have rank= metadata (should be NULL/absent -- the natural-path case)?\n")
cat("x$rank of first result is.null:", is.null(ids_result[[1]]$rank), "\n")

ranks <- c("domain", "phylum", "class", "order", "family", "genus", "species")

# OLD (broken) flattening, for regression confirmation it's still silently all-NA:
old_flat <- t(sapply(ids_result, function(x) {
  x$taxon[match(ranks, x$rank)]
}))
colnames(old_flat) <- ranks
cat("\n[REGRESSION] OLD flattening (x$taxon[match(ranks, x$rank)]) -- genus assigned:",
    sum(!is.na(old_flat[, "genus"])), "/", nrow(old_flat), "\n")

# NEW (fixed) flattening, exactly as shipped in SKILL.md:
new_flat <- t(sapply(ids_result, function(x) {
  taxa <- x$taxon[-1]
  taxa[startsWith(taxa, "unclassified_")] <- NA
  length(taxa) <- length(ranks)
  taxa
}))
colnames(new_flat) <- ranks

cat("\n[FIX] NEW positional flattening -- assigned counts per rank:\n")
for (rank in ranks) {
  n <- sum(!is.na(new_flat[, rank]))
  cat(sprintf("  %-8s %d/%d (%.1f%%)\n", rank, n, nrow(new_flat), 100*n/nrow(new_flat)))
}

genus_n <- sum(!is.na(new_flat[, "genus"]))
cat(sprintf("\nIndependently re-derived genus-assignment rate: %d/%d (%.1f%%)\n",
            genus_n, nrow(new_flat), 100*genus_n/nrow(new_flat)))

write.csv(new_flat, file.path(dir, "idtaxa_new_flat.csv"))
cat("\nSaved idtaxa_new_flat.csv\n")
