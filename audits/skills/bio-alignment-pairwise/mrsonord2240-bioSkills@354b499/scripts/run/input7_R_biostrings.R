# SKILL.md line 24: "R: pairwiseAlignment() (Biostrings)". Ground truth: Biopython/EMBOSS 286.0 (open 11 / ext 1 Biopython convention) for HBA vs HBB.
suppressPackageStartupMessages({library(Biostrings); library(pwalign)})
fa <- readAAStringSet("F:/OpenScience/audits/bio-alignment-pairwise/run/data/hba_hbb.fasta")
cat("n seqs:", length(fa), " lengths:", width(fa), "\n")
# (1) Biostrings::pairwiseAlignment (as the skill names it): warning expected in Bioc 3.20
w <- NULL
r0 <- withCallingHandlers(Biostrings::pairwiseAlignment(fa[[1]], fa[[2]], substitutionMatrix = "BLOSUM62", gapOpening = 10, gapExtension = 1, type = "global"),
                          warning = function(x) { w <<- conditionMessage(x); invokeRestart("muffleWarning") })
cat("Biostrings::pairwiseAlignment warning:", ifelse(is.null(w), "none", w), "\n")
cat("global score (gapOpening=10, gapExtension=1):", score(r0), "\n")
# (2) pwalign
r1 <- pwalign::pairwiseAlignment(fa[[1]], fa[[2]], substitutionMatrix = "BLOSUM62", gapOpening = 10, gapExtension = 1, type = "global")
cat("pwalign global score:", score(r1), " (expected 286 = Biopython -11/-1 = EMBOSS needle 11/1)\n")
cat("pid (pwalign::pid, PID1..4):", sapply(c("PID1","PID2","PID3","PID4"), function(t) round(pwalign::pid(r1, type = t), 1)), "\n")
r2 <- pwalign::pairwiseAlignment(fa[[1]], fa[[2]], substitutionMatrix = "BLOSUM62", gapOpening = 11, gapExtension = 1, type = "global")
cat("pwalign gapOpening=11 (Biostrings 'open' == BLAST convention) global score:", score(r2), " -> equals Biopython -12/-1 global?\n")
rl <- pwalign::pairwiseAlignment(fa[[1]], fa[[2]], substitutionMatrix = "BLOSUM62", gapOpening = 11, gapExtension = 1, type = "local")
cat("pwalign local gapOpening=11/ext=1:", score(rl), " (BLASTP 11/1 raw score = 285)\n")
