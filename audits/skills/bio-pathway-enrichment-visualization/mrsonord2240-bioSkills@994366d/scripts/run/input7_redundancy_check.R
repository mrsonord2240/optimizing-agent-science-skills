# Input 7 (redundancy-pass regression) -- "My cnetplot node labels show raw Entrez IDs like '1029'
# instead of gene symbols like 'CDKN2A'. How do I fix that, and show me the corrected plot?"
#
# This is a direct regression test of Tips bullet 9 from the PRE-redundancy-pass usage-guide.md
# ("Make the object readable (setReadable) before plotting so gene labels are symbols, not Entrez
# IDs"), which the fix log's redundancy pass DELETED from usage-guide.md, claiming it survives as
# the Common Errors row "gene labels are Entrez IDs not symbols -> setReadable(x, OrgDb, 'ENTREZID')
# before plotting" in SKILL.md. This script checks the claim is not just present as text but
# actually correct and actionable: does an enrichResult built WITHOUT readable=TRUE/setReadable show
# Entrez IDs in cnetplot, and does applying the documented fix actually produce symbols?
suppressMessages({
  library(clusterProfiler)
  library(enrichplot)
  library(org.Hs.eg.db)
  library(ggplot2)
})

d <- readRDS("../data/gene_data.rds")

# Deliberately NOT readable (mirrors an agent who skipped readable=TRUE / setReadable).
ego_raw <- enrichGO(gene = d$entrez, OrgDb = org.Hs.eg.db, ont = 'BP',
                     pvalueCutoff = 0.05, qvalueCutoff = 0.2, readable = FALSE)

gene_ids_in_result <- unlist(strsplit(as.data.frame(ego_raw)$geneID[1], "/"))
cat("Gene IDs stored before setReadable (sample):", paste(head(gene_ids_in_result, 3), collapse=", "), "\n")
cat("Are these Entrez IDs (all-numeric)?", all(grepl("^[0-9]+$", head(gene_ids_in_result, 3))), "\n")

# Apply the SKILL.md Common Errors fix.
ego_readable <- setReadable(ego_raw, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')
gene_symbols_after <- unlist(strsplit(as.data.frame(ego_readable)$geneID[1], "/"))
cat("Gene IDs stored after setReadable (sample):", paste(head(gene_symbols_after, 3), collapse=", "), "\n")
cat("Are these still all-numeric (i.e. fix failed)?", all(grepl("^[0-9]+$", head(gene_symbols_after, 3))), "\n")

# Render both to confirm the plot itself reflects the fix, not just the underlying data.frame.
out <- "input7_output.pdf"
pdf(out, width = 9, height = 7)
print(cnetplot(ego_raw, showCategory = 5) + ggtitle('Before setReadable (Entrez IDs)'))
print(cnetplot(ego_readable, showCategory = 5) + ggtitle('After setReadable (symbols)'))
dev.off()
cat("Wrote", out, "\n")
