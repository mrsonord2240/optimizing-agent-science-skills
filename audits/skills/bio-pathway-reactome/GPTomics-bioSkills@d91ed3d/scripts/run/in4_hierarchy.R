# Input 4 (Variant B / hierarchy interpretation): "My Reactome results have 'Interferon gamma
# signaling', 'Interferon Signaling', 'Cytokine Signaling in Immune system', and 'Immune System'
# all stacked at the top with tiny p-values. Are those four separate findings, or one signal?
# Which should I report?" -- verifies SKILL.md's central claim that nesting double-counts (a
# parent and child enrich on the SAME genes) using the real Input-1 ORA result.
df <- read.csv("out1_ora_results.csv", stringsAsFactors = FALSE)

top4 <- df[df$ID %in% c("R-HSA-877300", "R-HSA-913531", "R-HSA-1280215", "R-HSA-168256"), ]
top4 <- top4[order(top4$p.adjust), ]
cat("Top 4 candidate parent/child pathways:\n")
print(top4[, c("ID", "Description", "Count", "p.adjust")])

gene_sets <- lapply(strsplit(top4$geneID, "/"), unique)
names(gene_sets) <- top4$Description

cat("\nPairwise gene-set overlap (Jaccard) among the 4 top hits:\n")
n <- length(gene_sets)
for (i in 1:(n - 1)) {
  for (j in (i + 1):n) {
    a <- gene_sets[[i]]; b <- gene_sets[[j]]
    jacc <- length(intersect(a, b)) / length(union(a, b))
    is_subset <- all(a %in% b) || all(b %in% a)
    cat(sprintf("  %s vs %s: Jaccard=%.3f, one-is-subset-of-other=%s\n",
                names(gene_sets)[i], names(gene_sets)[j], jacc, is_subset))
  }
}

cat("\nConclusion check: the deepest node (Interferon gamma signaling, most specific,",
    "lowest p.adjust) should be reported; the other three are ancestors/context, not",
    "independent findings, per SKILL.md's hierarchy-deduplication guidance.\n")
