# Input 1 (Canonical, regression) -- prompt:
# "Here are my full DESeq2 results for 14,000 genes -- Wald stat in `stat`, Entrez IDs in
# `entrez_id`. Build the ranked vector the right way and run GO biological-process GSEA with a
# fixed seed. Give me the top terms by adjusted p-value with NES and the leading-edge genes."
#
# SKILL.md "Build the Ranked Vector" + "Run Preranked GSEA on GO" blocks, copied verbatim.

suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de <- read.csv("F:/OpenScience/audits/bio-pathway-gsea/data/SYNTHETIC_deseq2_results.csv")
gene_list <- de$stat
names(gene_list) <- de$entrez_id
gene_list <- gene_list[!is.na(gene_list)]
gene_list <- gene_list[!duplicated(names(gene_list))]
gene_list <- sort(gene_list, decreasing = TRUE)

cat("ranked vector: n =", length(gene_list), "| max", round(max(gene_list),3),
    "| min", round(min(gene_list),3), "| strictly decreasing:", !is.unsorted(-gene_list), "\n")

t0 <- Sys.time()
set.seed(123)
gse_go <- gseGO(geneList = gene_list, OrgDb = org.Hs.eg.db, keyType = "ENTREZID",
                ont = "BP", exponent = 1, minGSSize = 10, maxGSSize = 500,
                eps = 0, pvalueCutoff = 0.05, pAdjustMethod = "BH",
                seed = TRUE, by = "fgsea", verbose = FALSE)
t1 <- Sys.time()
gse_go <- setReadable(gse_go, OrgDb = org.Hs.eg.db, keyType = "ENTREZID")
res <- as.data.frame(gse_go)

cat("gseGO wall time:", round(as.numeric(difftime(t1, t0, units="secs")),1), "s\n")
cat("significant GO BP terms (p.adjust < 0.05):", nrow(res), "\n")
cat("columns returned:", paste(colnames(res), collapse=", "), "\n")
cat("positive NES:", sum(res$NES > 0), "| negative NES:", sum(res$NES < 0), "\n")

up_genes   <- readLines("F:/OpenScience/audits/bio-pathway-gsea/data/planted_up_entrez.txt")
down_genes <- readLines("F:/OpenScience/audits/bio-pathway-gsea/data/planted_down_entrez.txt")

# planted-set recovery via leading-edge overlap fraction (GO BP terms are not the Hallmark sets
# themselves, so check whether the top terms' core_enrichment is enriched for the planted genes)
res_sorted <- res[order(res$p.adjust), ]
if (nrow(res_sorted) > 0) {
  top_core <- unique(unlist(strsplit(res_sorted$core_enrichment[seq_len(min(5, nrow(res_sorted)))], "/")))
  cat("top-5-term leading edge genes overlapping planted UP:", length(intersect(top_core, up_genes)), "\n")
  cat("top-5-term leading edge genes overlapping planted DOWN:", length(intersect(top_core, down_genes)), "\n")
  print(head(res_sorted[, c("Description","NES","pvalue","p.adjust")], 10))
}

# reproducibility check
set.seed(123)
gse_go2 <- gseGO(geneList = gene_list, OrgDb = org.Hs.eg.db, keyType = "ENTREZID",
                 ont = "BP", exponent = 1, minGSSize = 10, maxGSSize = 500,
                 eps = 0, pvalueCutoff = 0.05, pAdjustMethod = "BH",
                 seed = TRUE, by = "fgsea", verbose = FALSE)
res2 <- as.data.frame(gse_go2)
cat("rerun identical: nrow", nrow(res2) == nrow(res), "| p.adjust all.equal:",
    isTRUE(all.equal(sort(res$p.adjust), sort(res2$p.adjust))), "\n")

write.csv(res_sorted, "F:/OpenScience/audits/bio-pathway-gsea/run/in1_go_terms.csv", row.names = FALSE)
cat("DONE\n")
