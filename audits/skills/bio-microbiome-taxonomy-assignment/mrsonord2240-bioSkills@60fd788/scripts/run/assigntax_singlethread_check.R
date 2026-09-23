# Follow-up: the first script found seeded multithreaded assignTaxonomy() != seeded single-threaded
# assignTaxonomy() (identical()==FALSE) on the fresh 18k slice. Two questions this script answers:
# (1) Is single-threaded seeded assignTaxonomy() reproducible with ITSELF (2 single-threaded runs)?
# (2) How large is the multi-vs-single residual, specifically at genus (the rank the veto/SKILL.md
#     claims turn on) -- a handful of cells (as fixer-1 found, "1-3 among ~4600") or something bigger?
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))

dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/myreaudit"
asv_dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"

fasta_lines <- readLines(file.path(asv_dir, "rep-seqs.fasta"))
seqs <- c(); cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (length(cur_seq) > 0) seqs <- c(seqs, paste(cur_seq, collapse = "")); cur_seq <- c()
  } else { cur_seq <- c(cur_seq, line) }
}
if (length(cur_seq) > 0) seqs <- c(seqs, paste(cur_seq, collapse = ""))

train_fa <- file.path(dir, "reaudit3_dada2_train.fasta")

cat("=== single-threaded seeded run 4 ===\n")
set.seed(100)
s4 <- assignTaxonomy(seqs, train_fa, minBoot = 50, tryRC = TRUE, multithread = FALSE)
cat("=== single-threaded seeded run 5 ===\n")
set.seed(100)
s5 <- assignTaxonomy(seqs, train_fa, minBoot = 50, tryRC = TRUE, multithread = FALSE)
cat("[seeded] identical(single-run4, single-run5):", identical(s4, s5), "\n")

prev <- readRDS(file.path(dir, "assigntax_all_runs.rds"))
s1 <- prev$s1  # multithreaded seeded run1
s3 <- prev$s3  # single-threaded seeded run3 (from first script)

cat("[seeded] identical(single-run3, single-run4):", identical(s3, s4), "\n")
cat("[seeded] identical(single-run4, single-run5):", identical(s4, s5), "\n")

for (rank in colnames(s1)) {
  d <- sum(s1[, rank] != s3[, rank] | (is.na(s1[, rank]) != is.na(s3[, rank])), na.rm = TRUE) +
       sum(is.na(s1[, rank]) != is.na(s3[, rank]))
  cat(sprintf("[multi-run1 vs single-run3] rank %-8s differing: %d / %d\n", rank, d, nrow(s1)))
}

saveRDS(list(s4=s4, s5=s5), file.path(dir, "assigntax_single_reruns.rds"))
cat("\nDone.\n")
