# Broaden the determinism check: (a) a different, larger real reference (full-length SILVA,
# ~380K seqs vs the 60K region-matched one) to see if the residual is reference-dependent, and
# (b) addSpecies() itself (exact-match, should be inherently deterministic -- confirm it actually
# is, since the fixer's report was ambiguous about whether species-level cells were included in
# the residual).
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

ref <- file.path(dir, "fulllength_dada2_train.fasta")
sp_ref <- file.path(dir, "fulllength_dada2_species.fasta")

cat("=== Full-length reference, 2 seeded assignTaxonomy runs ===\n")
set.seed(100)
t0 <- Sys.time()
fl1 <- assignTaxonomy(unname(seqs), ref, minBoot = 50, tryRC = TRUE, multithread = TRUE)
cat(sprintf("run 1: %.1fs\n", as.numeric(Sys.time()-t0, units="secs")))
set.seed(100)
t0 <- Sys.time()
fl2 <- assignTaxonomy(unname(seqs), ref, minBoot = 50, tryRC = TRUE, multithread = TRUE)
cat(sprintf("run 2: %.1fs\n", as.numeric(Sys.time()-t0, units="secs")))
cat("identical():", identical(fl1, fl2), "\n")
for (rank in colnames(fl1)) {
  diff <- sum(fl1[, rank] != fl2[, rank], na.rm = TRUE) + sum(xor(is.na(fl1[,rank]), is.na(fl2[,rank])))
  cat(sprintf("  %-8s differ: %d / %d\n", rank, diff, nrow(fl1)))
}

cat("\n=== addSpecies determinism, 2 runs on top of fl1 ===\n")
set.seed(100)
sp1 <- addSpecies(fl1, sp_ref)
set.seed(100)
sp2 <- addSpecies(fl1, sp_ref)
cat("identical():", identical(sp1, sp2), "\n")
diff_sp <- sum(sp1[, "Species"] != sp2[, "Species"], na.rm = TRUE) + sum(xor(is.na(sp1[,"Species"]), is.na(sp2[,"Species"])))
cat(sprintf("  Species differ: %d / %d\n", diff_sp, nrow(sp1)))
