# Re-audit: does set.seed(100) before EVERY assignTaxonomy() call (SKILL.md's fix) make repeated
# runs reproducible, at genus specifically and at every rank, in THIS environment's default
# threading config (multithread=TRUE, 24 cores, RcppParallel "auto")?
# Run 3 times (not 2) to see if a residual is a fluke of a particular pairing or persistent.
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
cat("Real ASVs loaded:", length(seqs), "\n")

ref <- file.path(dir, "regionmatched_dada2_train.fasta")

run_once <- function(i) {
  set.seed(100)
  t0 <- Sys.time()
  taxa <- assignTaxonomy(unname(seqs), ref, minBoot = 50, tryRC = TRUE, multithread = TRUE)
  cat(sprintf("  run %d done in %.1fs\n", i, as.numeric(Sys.time() - t0, units = "secs")))
  taxa
}

runs <- list()
for (i in 1:3) { cat("Starting run", i, "(multithread=TRUE, set.seed(100) before call)\n"); runs[[i]] <- run_once(i) }

ranks <- colnames(runs[[1]])
cat("\n=== Pairwise diffs, SEEDED, multithread=TRUE ===\n")
for (pair in list(c(1,2), c(1,3), c(2,3))) {
  a <- runs[[pair[1]]]; b <- runs[[pair[2]]]
  cat(sprintf("\nRun %d vs Run %d: identical() = %s\n", pair[1], pair[2], identical(a, b)))
  for (rank in ranks) {
    diff <- sum(a[, rank] != b[, rank], na.rm = TRUE) + sum(xor(is.na(a[, rank]), is.na(b[, rank])))
    if (diff > 0) {
      cat(sprintf("  %-8s differ: %d / %d\n", rank, diff, nrow(a)))
      idx <- which((a[, rank] != b[, rank] & !is.na(a[,rank]) & !is.na(b[,rank])) | xor(is.na(a[,rank]), is.na(b[,rank])))
      for (ix in head(idx, 5)) cat(sprintf("     row %d: '%s' vs '%s'\n", ix, a[ix,rank], b[ix,rank]))
    } else {
      cat(sprintf("  %-8s differ: 0 / %d\n", rank, nrow(a)))
    }
  }
}

saveRDS(runs, file.path(dir, "seeded_3runs.rds"))
cat("\nSaved seeded_3runs.rds\n")
