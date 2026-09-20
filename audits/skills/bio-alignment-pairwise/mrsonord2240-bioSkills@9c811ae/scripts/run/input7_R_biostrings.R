# Skill: "R: pwalign::pairwiseAlignment() (Bioconductor 3.20 moved it out of Biostrings; Biostrings::pairwiseAlignment() still works but warns).
# Gap parameters use the BLAST convention" -> pwalign gapOpening 11/ext 1 local = 285 (= BLASTP raw) ; 10/1 local = 288 (= water 11/1); 10/1 global = 286 (= needle 11/1)
suppressPackageStartupMessages({library(Biostrings); library(pwalign)})
fa <- readAAStringSet("F:/OpenScience/audits/bio-alignment-pairwise/run/data/hba_hbb.fasta")
cat("n seqs:", length(fa), " lengths:", width(fa), "\n")
w <- NULL
r0 <- withCallingHandlers(Biostrings::pairwiseAlignment(fa[[1]], fa[[2]], substitutionMatrix = "BLOSUM62", gapOpening = 10, gapExtension = 1, type = "global"),
                          warning = function(x) { w <<- conditionMessage(x); invokeRestart("muffleWarning") })
cat("Biostrings::pairwiseAlignment warning:", ifelse(is.null(w), "none", w), "\n")
sc <- function(type, o, e) score(pwalign::pairwiseAlignment(fa[[1]], fa[[2]], substitutionMatrix = "BLOSUM62", gapOpening = o, gapExtension = e, type = type))
res <- c(global_10_1 = sc("global", 10, 1), local_11_1 = sc("local", 11, 1), local_10_1 = sc("local", 10, 1), global_11_1 = sc("global", 11, 1))
print(res)
stopifnot(res[["global_10_1"]] == 286, res[["local_11_1"]] == 285, res[["local_10_1"]] == 288, res[["global_11_1"]] == 282)
cat("PASS pwalign convention mapping in the Skill (10/1 global 286 = needle 11/1; 11/1 local 285 = blastp; 10/1 local 288 = water 11/1)\n")
cat("pwalign global 11/1 = 282 = Biopython global -12/-1 (input1d_global_conv.py)
")
