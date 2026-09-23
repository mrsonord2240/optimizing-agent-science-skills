# Independent re-audit (4th agent) determinism test on a FRESH data slice:
# an 18,000-sequence SILVA-138 subsample drawn with seed 4242, never used by the original
# auditor, the two fixers, or the prior re-auditor (who used 8k/30k/60k/380k/5k draws).
# Tests, on this new slice: LearnTaxa() reproducibility under set.seed(), IdTaxa() reproducibility
# under set.seed() (single- and multi-threaded), and a negative-control unseeded IdTaxa() pair to
# confirm the underlying stochasticity is still real on this slice (i.e. the test is sound).
.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
suppressPackageStartupMessages(library(DECIPHER))

dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/myreaudit"
asv_dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"

# --- Real 770 ASVs (moving-pictures, the only real biological ASV set cached; reused since it
# is the query set, not the stochastic reference being varied here) ---
fasta_lines <- readLines(file.path(asv_dir, "rep-seqs.fasta"))
ids <- c(); seqs <- c(); cur_id <- NULL; cur_seq <- c()
for (line in fasta_lines) {
  if (startsWith(line, ">")) {
    if (!is.null(cur_id)) { ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = "")) }
    cur_id <- substring(line, 2); cur_seq <- c()
  } else { cur_seq <- c(cur_seq, line) }
}
ids <- c(ids, cur_id); seqs <- c(seqs, paste(cur_seq, collapse = ""))
cat("Real ASVs:", length(seqs), "\n")
dna <- DNAStringSet(unname(seqs)); names(dna) <- ids

# --- Fresh 18k reference slice (seed 4242, never used before this re-audit) ---
tax_tsv <- file.path(dir, "reaudit3_decipher_tax.tsv")
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
cat("Fresh reference seqs (seed 4242, n=18000 draw):", length(refseqs), "\n")
refset <- DNAStringSet(refseqs); names(refset) <- fids

# === LearnTaxa() determinism under set.seed(), exactly as SKILL.md's commented example ===
cat("\n=== Training LearnTaxa() run A (set.seed(100)) ===\n")
t0 <- Sys.time()
set.seed(100)
trainA <- LearnTaxa(refset, taxonomy = taxons)
cat(sprintf("done in %.1f min\n", as.numeric(Sys.time() - t0, units = "mins")))
saveRDS(trainA, file.path(dir, "trainA.rds"))

cat("\n=== Training LearnTaxa() run B (set.seed(100)) ===\n")
t0 <- Sys.time()
set.seed(100)
trainB <- LearnTaxa(refset, taxonomy = taxons)
cat(sprintf("done in %.1f min\n", as.numeric(Sys.time() - t0, units = "mins")))
saveRDS(trainB, file.path(dir, "trainB.rds"))

cat("\n[LearnTaxa seeded] identical(trainA, trainB):", identical(trainA, trainB), "\n")

cat("\n=== Training LearnTaxa() run C (UNSEEDED, negative control) ===\n")
t0 <- Sys.time()
trainC <- LearnTaxa(refset, taxonomy = taxons)
cat(sprintf("done in %.1f min\n", as.numeric(Sys.time() - t0, units = "mins")))
saveRDS(trainC, file.path(dir, "trainC.rds"))
cat("[LearnTaxa unseeded] identical(trainB, trainC) [trainB ended w/ seeded RNG state, trainC unseeded after]:",
    identical(trainB, trainC), "\n")

# === IdTaxa() determinism under set.seed(), using the seeded trainA trainingSet ===
cat("\n=== IdTaxa() seeded, run 1, multithreaded (processors=NULL) ===\n")
set.seed(100)
id1_multi <- IdTaxa(dna, trainA, strand = "both", threshold = 60, processors = NULL)

cat("=== IdTaxa() seeded, run 2, multithreaded (processors=NULL) ===\n")
set.seed(100)
id2_multi <- IdTaxa(dna, trainA, strand = "both", threshold = 60, processors = NULL)

cat("[IdTaxa seeded, multithreaded] identical(run1, run2):", identical(id1_multi, id2_multi), "\n")

cat("\n=== IdTaxa() seeded, run 1, single-threaded (processors=1) ===\n")
set.seed(100)
id1_single <- IdTaxa(dna, trainA, strand = "both", threshold = 60, processors = 1)

cat("=== IdTaxa() seeded, run 2, single-threaded (processors=1) ===\n")
set.seed(100)
id2_single <- IdTaxa(dna, trainA, strand = "both", threshold = 60, processors = 1)

cat("[IdTaxa seeded, single-threaded] identical(run1, run2):", identical(id1_single, id2_single), "\n")
cat("[IdTaxa seeded] multithreaded run1 identical to single-threaded run1 (cross-check):",
    identical(id1_multi, id1_single), "\n")

cat("\n=== IdTaxa() UNSEEDED, negative control (2 runs, default multithreaded) ===\n")
id_uns1 <- IdTaxa(dna, trainA, strand = "both", threshold = 60, processors = NULL)
id_uns2 <- IdTaxa(dna, trainA, strand = "both", threshold = 60, processors = NULL)
cat("[IdTaxa UNSEEDED] identical(run1, run2):", identical(id_uns1, id_uns2), "\n")

ranks <- c("domain", "phylum", "class", "order", "family", "genus", "species")
flatten <- function(ids_result) {
  t(sapply(ids_result, function(x) {
    taxa <- x$taxon[-1]
    taxa[startsWith(taxa, "unclassified_")] <- NA
    length(taxa) <- length(ranks)
    taxa
  }))
}
fl_uns1 <- flatten(id_uns1); colnames(fl_uns1) <- ranks
fl_uns2 <- flatten(id_uns2); colnames(fl_uns2) <- ranks
diffs <- sapply(ranks, function(r) sum(fl_uns1[, r] != fl_uns2[, r] | (is.na(fl_uns1[, r]) != is.na(fl_uns2[, r])), na.rm = TRUE))
cat("\n[IdTaxa UNSEEDED] per-rank differing calls out of", nrow(fl_uns1), ":\n")
print(diffs)

fl_seeded <- flatten(id1_multi); colnames(fl_seeded) <- ranks
cat("\n[IdTaxa seeded, fresh 18k-seq reference] genus-assigned:",
    sum(!is.na(fl_seeded[, "genus"])), "/", nrow(fl_seeded), "\n")

saveRDS(list(id1_multi=id1_multi, id2_multi=id2_multi, id1_single=id1_single, id2_single=id2_single,
             id_uns1=id_uns1, id_uns2=id_uns2), file.path(dir, "idtaxa_all_runs.rds"))
cat("\nDone.\n")
