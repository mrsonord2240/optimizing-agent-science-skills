# Input 2 (Variant A) + Input 3 (Edge) part B: DADA2 assignTaxonomy + addSpecies against the
# REGION-MATCHED (515-806, V4) SILVA reference -- the SKILL's recommended path for V4 data -- for
# direct comparison against the naive full-length run (assign_fulllength.R / taxa_fulllength.rds).
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
names(seqs) <- ids
cat("Loaded", length(seqs), "real V4 ASVs\n")

minBoot <- 50
t0 <- Sys.time()
taxa_rm <- assignTaxonomy(unname(seqs), file.path(data_dir, "regionmatched_dada2_train.fasta"),
                           minBoot = minBoot, tryRC = TRUE, multithread = TRUE)
cat("assignTaxonomy (REGION-MATCHED 515-806 ref) took",
    round(as.numeric(Sys.time() - t0, units = "secs"), 1), "sec\n")

cat("\n=== REGION-MATCHED classifier on V4 ASVs: assigned fraction per rank ===\n")
for (rank in colnames(taxa_rm)) {
  assigned <- sum(!is.na(taxa_rm[, rank]))
  cat(sprintf("  %-8s %d/%d (%.1f%%)\n", rank, assigned, nrow(taxa_rm), 100 * assigned / nrow(taxa_rm)))
}

# addSpecies -- exact match only (region-matched species reference)
t1 <- Sys.time()
taxa_rm_sp <- addSpecies(taxa_rm, file.path(data_dir, "regionmatched_dada2_species.fasta"), allowMultiple = FALSE)
cat("addSpecies took", round(as.numeric(Sys.time() - t1, units = "secs"), 1), "sec\n")
n_species <- sum(!is.na(taxa_rm_sp[, "Species"]))
cat(sprintf("Species assigned by EXACT match: %d/%d (%.1f%%)\n", n_species, nrow(taxa_rm_sp), 100*n_species/nrow(taxa_rm_sp)))

# Direct comparison: full-length vs region-matched genus calls on the SAME 770 ASVs
taxa_full <- readRDS(file.path(data_dir, "taxa_fulllength.rds"))
common_seq <- intersect(rownames(taxa_full), rownames(taxa_rm))
cat("\n=== Full-length vs region-matched: genus call agreement on", length(common_seq), "shared ASVs ===\n")
full_g <- taxa_full[common_seq, "Genus"]
rm_g   <- taxa_rm[common_seq, "Genus"]
both_na <- is.na(full_g) & is.na(rm_g)
agree   <- !is.na(full_g) & !is.na(rm_g) & (full_g == rm_g)
full_only_na <- is.na(full_g) & !is.na(rm_g)
rm_only_na   <- !is.na(full_g) & is.na(rm_g)
disagree <- !is.na(full_g) & !is.na(rm_g) & (full_g != rm_g)
cat(sprintf("  both NA (unassigned both ways):        %d\n", sum(both_na)))
cat(sprintf("  agree (same genus both ways):           %d\n", sum(agree)))
cat(sprintf("  full-length NA, region-matched assigned: %d  (region-matching RECOVERED a call)\n", sum(full_only_na)))
cat(sprintf("  region-matched NA, full-length assigned: %d  (full-length OVER-called vs region-matched refusal)\n", sum(rm_only_na)))
cat(sprintf("  DISAGREE (both assigned, different genus): %d\n", sum(disagree)))
if (sum(disagree) > 0) {
  cat("\nExamples of disagreement (full-length genus vs region-matched genus):\n")
  idx <- which(disagree)[1:min(10, sum(disagree))]
  print(data.frame(full_length = full_g[idx], region_matched = rm_g[idx]))
}

saveRDS(taxa_rm, file.path(data_dir, "taxa_regionmatched.rds"))
saveRDS(taxa_rm_sp, file.path(data_dir, "taxa_regionmatched_species.rds"))
write.csv(taxa_rm_sp, file.path(data_dir, "taxa_regionmatched_species.csv"))
cat("\nSaved taxa_regionmatched(.species).rds\n")
