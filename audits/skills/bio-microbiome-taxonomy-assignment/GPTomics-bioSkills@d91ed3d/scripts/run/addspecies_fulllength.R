# addSpecies mechanism check (exact-match only) against the full-length species reference,
# applied to the full-length assignTaxonomy() genus calls from assign_fulllength.R.
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))
data_dir <- "F:/OpenScience/audits/bio-microbiome-taxonomy-assignment/data"

taxa <- readRDS(file.path(data_dir, "taxa_fulllength.rds"))
cat("Before addSpecies, columns:", paste(colnames(taxa), collapse=", "), "\n")

t0 <- Sys.time()
taxa_sp <- addSpecies(taxa, file.path(data_dir, "fulllength_dada2_species.fasta"), allowMultiple = FALSE)
cat("addSpecies took", round(as.numeric(Sys.time() - t0, units = "secs"), 1), "sec\n")

n_species <- sum(!is.na(taxa_sp[, "Species"]))
cat(sprintf("Species assigned by EXACT match: %d/%d (%.1f%%)\n", n_species, nrow(taxa_sp), 100*n_species/nrow(taxa_sp)))
if (n_species > 0) {
  cat("\nExamples of exact-match species calls:\n")
  idx <- which(!is.na(taxa_sp[, "Species"]))[1:min(5, n_species)]
  print(taxa_sp[idx, c("Genus", "Species")])
}
saveRDS(taxa_sp, file.path(data_dir, "taxa_fulllength_species.rds"))
write.csv(taxa_sp, file.path(data_dir, "taxa_fulllength_species.csv"))
