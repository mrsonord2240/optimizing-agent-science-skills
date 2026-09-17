# Input 6 (NEW -- load-bearing nPerm claim) -- prompt:
# "My labmate gave me this old script: gseGO(geneList=gl, ..., nPerm=10000). It's supposed to give
# an error on the new clusterProfiler so I'd notice and fix it, right? Also show me the Skill's
# own guard code catching it."

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

# use msigdbr Hallmark instead of full GO BP so this stays fast -- the claim under test is about
# nPerm's effect on the ENGINE, not about which gene-set collection is used
suppressMessages(library(msigdbr))
h <- msigdbr(species = "Homo sapiens", collection = "H")
t2g <- h[, c("gs_name", "ncbi_gene")]

cat("--- request: 'bump nPerm to 10000 for more power' (the labmate's old-tutorial script) ---\n")
set.seed(123)
gse_nperm <- tryCatch(
  GSEA(geneList = gene_list, TERM2GENE = t2g, exponent = 1, minGSSize = 10, maxGSSize = 500,
       nPerm = 10000, pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE),
  error = function(e) { cat("nPerm call raised an ERROR:", conditionMessage(e), "\n"); NULL }
)
if (!is.null(gse_nperm)) {
  cat("nPerm=10000 was ACCEPTED, not rejected. Run completed with", nrow(as.data.frame(gse_nperm)), "terms.\n")
  cat("params slot contains nPerm:", "nPerm" %in% names(gse_nperm@params), "\n")
  if ("nPerm" %in% names(gse_nperm@params)) cat("params$nPerm =", gse_nperm@params$nPerm, "\n")
}

cat("\n--- the Skill's own documented guard: if ('nPerm' %in% names(gse@params)) stop(...) ---\n")
guard_result <- tryCatch({
  if (!is.null(gse_nperm) && "nPerm" %in% names(gse_nperm@params)) {
    stop("nPerm forced a fgseaSimple fallback - remove it")
  }
  "guard did not fire (nPerm not recorded in @params)"
}, error = function(e) paste("guard FIRED:", conditionMessage(e)))
cat(guard_result, "\n")

cat("\n--- for comparison: the call WITHOUT nPerm (Skill's actual recommendation) ---\n")
set.seed(123)
gse_clean <- GSEA(geneList = gene_list, TERM2GENE = t2g, exponent = 1, minGSSize = 10, maxGSSize = 500,
                   eps = 0, pvalueCutoff = 0.05, seed = TRUE, verbose = FALSE)
cat("clean call (eps=0, no nPerm):", nrow(as.data.frame(gse_clean)), "terms | 'nPerm' in @params:",
    "nPerm" %in% names(gse_clean@params), "\n")

cat("\nDONE\n")
