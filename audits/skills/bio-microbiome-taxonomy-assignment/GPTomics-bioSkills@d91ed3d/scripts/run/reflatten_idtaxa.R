# Correct flattening of IdTaxa results (working around the SKILL.md code defect: x$rank is NULL
# unless LearnTaxa() was called with an explicit rank= data.frame, which SKILL.md's own LearnTaxa
# example does not do -- so SKILL.md's `match(ranks, x$rank)` line silently returns all-NA).
# This script recovers the REAL classification (positional, since taxonomy depth = rank position)
# to evaluate what IdTaxa actually produced, separately from documenting the SKILL.md bug itself.
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
data_dir <- "F:/OpenScience/audits/bio-microbiome-taxonomy-assignment/data"
ids_result <- readRDS(file.path(data_dir, "idtaxa_result.rds"))

ranks <- c("domain", "phylum", "class", "order", "family", "genus")
n_rank <- length(ranks)

flat <- t(sapply(ids_result, function(x) {
  # x$taxon[1] is always "Root"; positions 2..7 are domain..genus if present
  taxa <- x$taxon[-1]
  conf <- x$confidence[-1]
  taxa[startsWith(taxa, "unclassified_")] <- NA
  length(taxa) <- n_rank  # pad/truncate to fixed length with NA
  taxa
}))
colnames(flat) <- ranks
rownames(flat) <- names(ids_result)

cat("=== IdTaxa (region-matched training), CORRECTLY flattened: assigned fraction per rank ===\n")
for (rank in ranks) {
  assigned <- sum(!is.na(flat[, rank]))
  cat(sprintf("  %-8s %d/%d (%.1f%%)\n", rank, assigned, nrow(flat), 100 * assigned / nrow(flat)))
}

n_refused_early <- sum(sapply(ids_result, function(x) length(x$taxon) < 7))
cat(sprintf("\nRefused before reaching genus (conservative stop, tree-descent refusal): %d/%d (%.1f%%)\n",
            n_refused_early, length(ids_result), 100*n_refused_early/length(ids_result)))
cat(sprintf("Reached genus: %d/%d (%.1f%%)\n", sum(!is.na(flat[,"genus"])), nrow(flat), 100*sum(!is.na(flat[,"genus"]))/nrow(flat)))

# Compare to region-matched DADA2 naive-Bayes genus calls on the same 770 ASVs
taxa_rm <- readRDS(file.path(data_dir, "taxa_regionmatched.rds"))
common <- intersect(rownames(taxa_rm), rownames(flat))
nb_g <- taxa_rm[common, "Genus"]
idt_g <- flat[common, "genus"]
agree <- !is.na(nb_g) & !is.na(idt_g) & (nb_g == idt_g)
idt_more_conservative <- !is.na(nb_g) & is.na(idt_g)
nb_more_conservative <- is.na(nb_g) & !is.na(idt_g)
cat(sprintf("\n=== IdTaxa vs DADA2 naive-Bayes genus agreement (both region-matched, %d shared ASVs) ===\n", length(common)))
cat(sprintf("  Both agree on genus:                          %d\n", sum(agree)))
cat(sprintf("  IdTaxa refused (NA), NB called a genus:        %d  (IdTaxa MORE conservative)\n", sum(idt_more_conservative)))
cat(sprintf("  NB refused (NA), IdTaxa called a genus:        %d  (NB MORE conservative)\n", sum(nb_more_conservative)))
disagree <- !is.na(nb_g) & !is.na(idt_g) & (nb_g != idt_g)
cat(sprintf("  Both called, DIFFERENT genus:                  %d\n", sum(disagree)))

saveRDS(flat, file.path(data_dir, "taxa_idtaxa_correct.rds"))
write.csv(flat, file.path(data_dir, "taxa_idtaxa_correct.csv"))
cat("\nSaved taxa_idtaxa_correct.rds\n")

# --- Fix: id_by_seq mapping (rownames mismatch: taxa_rm keyed by sequence, flat keyed by ASV id) ---
id_by_seq <- readRDS(file.path(data_dir, "id_by_seq.rds"))  # names=sequence, value=ASV id
seq_by_id <- setNames(names(id_by_seq), id_by_seq)
common_ids <- intersect(rownames(flat), names(seq_by_id))
nb_g2 <- taxa_rm[seq_by_id[common_ids], "Genus"]
idt_g2 <- flat[common_ids, "genus"]
agree2 <- !is.na(nb_g2) & !is.na(idt_g2) & (nb_g2 == idt_g2)
idt_more2 <- !is.na(nb_g2) & is.na(idt_g2)
nb_more2  <- is.na(nb_g2) & !is.na(idt_g2)
disagree2 <- !is.na(nb_g2) & !is.na(idt_g2) & (nb_g2 != idt_g2)
cat(sprintf("\n=== FIXED comparison: IdTaxa vs DADA2-NB genus agreement (%d shared ASVs) ===\n", length(common_ids)))
cat(sprintf("  Both agree on genus:                     %d\n", sum(agree2)))
cat(sprintf("  IdTaxa refused, NB called (IdTaxa MORE conservative): %d\n", sum(idt_more2)))
cat(sprintf("  NB refused, IdTaxa called (NB MORE conservative):     %d\n", sum(nb_more2)))
cat(sprintf("  Both called, DIFFERENT genus:             %d\n", sum(disagree2)))
