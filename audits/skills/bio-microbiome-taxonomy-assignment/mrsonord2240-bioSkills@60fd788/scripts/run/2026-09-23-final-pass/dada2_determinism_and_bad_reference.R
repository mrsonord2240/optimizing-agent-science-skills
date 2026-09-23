# Fresh dynamic tests: seeded/unseeded DADA2 behavior plus the shipped example's all-NA safeguard.
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(dada2))
base <- "F:/OpenScience/audits/bio-microbiome-taxonomy-assignment"
env <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst"
seqtab <- readRDS(file.path(base, "data/2026-09-23-final-pass/moving_pictures_770_seqtab.rds"))
seqs <- colnames(seqtab)
ref <- file.path(env, "reaudit-tax/regionmatched_dada2_train.fasta")
run_one <- function(seed) { if (!is.null(seed)) set.seed(seed); assignTaxonomy(seqs, ref, minBoot=50, tryRC=TRUE, multithread=TRUE) }
s1 <- run_one(100); s2 <- run_one(100); u1 <- run_one(NULL); u2 <- run_one(NULL)
diff_rank <- function(a, b, rank) sum((is.na(a[, rank]) != is.na(b[, rank])) | (!is.na(a[, rank]) & !is.na(b[, rank]) & a[, rank] != b[, rank]))
cat("seeded_genus_diff=", diff_rank(s1, s2, "Genus"), "\n", sep="")
cat("unseeded_genus_diff=", diff_rank(u1, u2, "Genus"), "\n", sep="")
cat("seeded_genus_assigned=", sum(!is.na(s1[, "Genus"])), "/", nrow(s1), "\n", sep="")
bad <- file.path(base, "data/2026-09-23-final-pass/bad_reference.fasta")
writeLines(c(">bad1 Bacteria;Firmicutes;Bacilli;Order;Family;Genus;", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"), bad)
set.seed(100); bad_tax <- assignTaxonomy(seqs[1:10], bad, minBoot=50, tryRC=TRUE, multithread=FALSE)
cat("bad_reference_genus_assigned=", sum(!is.na(bad_tax[, "Genus"])), "/", nrow(bad_tax), "\n", sep="")
if (sum(!is.na(bad_tax[, "Genus"])) != 0) stop("bad reference unexpectedly assigned genus")
saveRDS(list(seeded1=s1, seeded2=s2, unseeded1=u1, unseeded2=u2), file.path(base, "data/2026-09-23-final-pass/dada2_determinism.rds"))
