# Independent re-audit (4th agent): assignTaxonomy() determinism regression test on the SAME
# fresh 18k-sequence SILVA-138 slice (seed 4242) used for the LearnTaxa/IdTaxa test in this
# re-audit -- a data slice none of the prior 3 passes (original auditor, fixer x2, re-auditor)
# used (they used 8k/30k/60k/380k/5k draws).
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))

dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/myreaudit"
asv_dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"

# Real 770 ASVs as a seqtab-like character vector (assignTaxonomy accepts a character vector of
# sequences directly, not just a seqtab matrix)
fasta_lines <- readLines(file.path(asv_dir, "rep-seqs.fasta"))
seqs <- c(); cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (length(cur_seq) > 0) seqs <- c(seqs, paste(cur_seq, collapse = "")); cur_seq <- c()
  } else { cur_seq <- c(cur_seq, line) }
}
if (length(cur_seq) > 0) seqs <- c(seqs, paste(cur_seq, collapse = ""))
cat("Real ASVs:", length(seqs), "\n")

train_fa <- file.path(dir, "reaudit3_dada2_train.fasta")

run_one <- function(seeded, mt, label) {
  if (seeded) set.seed(100)
  t0 <- Sys.time()
  taxa <- assignTaxonomy(seqs, train_fa, minBoot = 50, tryRC = TRUE, multithread = mt)
  cat(sprintf("[%s] done in %.1f sec\n", label, as.numeric(Sys.time() - t0, units = "secs")))
  taxa
}

cat("=== assignTaxonomy seeded run 1, multithreaded ===\n")
s1 <- run_one(TRUE, TRUE, "seeded-multi-1")
cat("=== assignTaxonomy seeded run 2, multithreaded ===\n")
s2 <- run_one(TRUE, TRUE, "seeded-multi-2")
cat("=== assignTaxonomy seeded run 3, single-threaded ===\n")
s3 <- run_one(TRUE, FALSE, "seeded-single-3")

cat("\n[seeded] identical(multi-run1, multi-run2):", identical(s1, s2), "\n")
cat("[seeded] identical(multi-run1, single-run3):", identical(s1, s3), "\n")

cat("\n=== assignTaxonomy UNSEEDED run 1, multithreaded (negative control) ===\n")
u1 <- run_one(FALSE, TRUE, "unseeded-1")
cat("=== assignTaxonomy UNSEEDED run 2, multithreaded (negative control) ===\n")
u2 <- run_one(FALSE, TRUE, "unseeded-2")
cat("[UNSEEDED] identical(run1, run2):", identical(u1, u2), "\n")

genus_diff <- sum(u1[, "Genus"] != u2[, "Genus"] | (is.na(u1[, "Genus"]) != is.na(u2[, "Genus"])), na.rm = TRUE) +
              sum(is.na(u1[, "Genus"]) != is.na(u2[, "Genus"]))
cat("[UNSEEDED] genus calls differing (approx, includes NA-status flips):", genus_diff, "/", nrow(u1), "\n")

cat("\n[seeded] genus-assigned:", sum(!is.na(s1[, "Genus"])), "/", nrow(s1), "\n")

saveRDS(list(s1=s1, s2=s2, s3=s3, u1=u1, u2=u2), file.path(dir, "assigntax_all_runs.rds"))
cat("\nDone.\n")
