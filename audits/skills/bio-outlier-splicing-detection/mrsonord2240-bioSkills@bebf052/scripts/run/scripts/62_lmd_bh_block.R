# SKILL.md LeafcutterMD BH block (blocks/04_r.R) verbatim, run in lmd/; asserts on content
setwd(commandArgs(TRUE)[1]); source(commandArgs(TRUE)[2], echo = FALSE)
cat("tested cluster x sample pairs:", nrow(long), "; raw p<0.05:", sum(long$p < 0.05), "; BH q<0.05 hits:", nrow(hits), "\n")
print(head(hits[order(hits$q), ], 12))
stopifnot(nrow(hits) > 0, all(c("cluster", "sampleID", "p", "q") %in% names(hits)))
cat("samples with hits:", paste(names(sort(table(hits$sampleID), decreasing = TRUE)), sort(table(hits$sampleID), decreasing = TRUE), collapse = "; "), "\n")
