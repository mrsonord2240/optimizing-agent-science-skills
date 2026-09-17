# Input 2 (Variant A, regression) -- the usage-guide's own example prompt:
# "Run GSEA against the MSigDB Hallmark collection on my ranked human gene list, then also run
# gseKEGG and note that KEGG queries the live database."

suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
  library(msigdbr)
})

de <- read.csv("F:/OpenScience/audits/bio-pathway-gsea/data/SYNTHETIC_deseq2_results.csv")
gene_list <- de$stat
names(gene_list) <- de$entrez_id
gene_list <- gene_list[!is.na(gene_list)]
gene_list <- gene_list[!duplicated(names(gene_list))]
gene_list <- sort(gene_list, decreasing = TRUE)

h   <- msigdbr(species = "Homo sapiens", collection = "H")
cat("msigdbr collection= accepted:", TRUE, "| ncbi_gene column present:", "ncbi_gene" %in% names(h), "\n")
t2g <- h[, c("gs_name", "ncbi_gene")]

set.seed(123)
gse_h <- GSEA(geneList = gene_list, TERM2GENE = t2g, exponent = 1,
              minGSSize = 10, maxGSSize = 500, eps = 0,
              pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE)
res_h <- as.data.frame(gse_h)
cat("significant Hallmarks:", nrow(res_h), "\n")
print(res_h[order(res_h$p.adjust), c("ID","NES","p.adjust")])

up_rank   <- which(res_h$ID[order(res_h$p.adjust)] == "HALLMARK_TNFA_SIGNALING_VIA_NFKB")
down_rank <- which(res_h$ID[order(res_h$p.adjust)] == "HALLMARK_G2M_CHECKPOINT")
cat("planted UP set rank (by p.adjust):", ifelse(length(up_rank)==0, "NOT SIGNIFICANT", up_rank), "\n")
cat("planted DOWN set rank (by p.adjust):", ifelse(length(down_rank)==0, "NOT SIGNIFICANT", down_rank), "\n")

set.seed(123)
gse_kegg <- tryCatch(
  gseKEGG(geneList = gene_list, organism = "hsa", keyType = "ncbi-geneid",
          minGSSize = 10, maxGSSize = 500, eps = 0,
          pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE),
  error = function(e) { cat("gseKEGG ERROR:", conditionMessage(e), "\n"); NULL }
)
if (!is.null(gse_kegg)) {
  res_kegg <- as.data.frame(gse_kegg)
  cat("significant KEGG pathways:", nrow(res_kegg), "| run date:", as.character(Sys.Date()), "\n")
  print(head(res_kegg[order(res_kegg$p.adjust), c("ID","Description","NES","p.adjust")], 8))
  write.csv(res_kegg, "F:/OpenScience/audits/bio-pathway-gsea/run/in2_kegg_terms.csv", row.names = FALSE)
}

write.csv(res_h, "F:/OpenScience/audits/bio-pathway-gsea/run/in2_hallmark_terms.csv", row.names = FALSE)
cat("DONE\n")
