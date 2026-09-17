# Input 5 (Stress): "Draw the reaction network for my top Reactome pathway colored by my
# ranking statistic, and give me the link to open it in the Reactome Pathway Browser."
suppressMessages({
  library(ReactomePA)
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

df <- read.csv("out1_ora_results.csv", stringsAsFactors = FALSE)
ranked <- read.csv("../data/ranked_genes.csv", stringsAsFactors = FALSE)
mapped <- bitr(ranked$SYMBOL, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)
ranked <- merge(ranked, mapped, by.x = "SYMBOL", by.y = "SYMBOL")
fc <- ranked$stat
names(fc) <- ranked$ENTREZID

top_name <- df$Description[1]
top_id <- df$ID[1]
cat("Top pathway NAME (for viewPathway):", top_name, "\n")
cat("Top pathway ID (for the web link):", top_id, "\n")

out_pdf <- file.path(tempdir(), "reactome_viewpathway_audit.pdf")
ok <- tryCatch({
  pdf(out_pdf)
  p <- viewPathway(top_name, organism = "human", readable = TRUE, foldChange = fc)
  print(p)
  dev.off()
  TRUE
}, error = function(e) {
  cat("ERROR in viewPathway:", conditionMessage(e), "\n")
  if (dev.cur() != 1) dev.off()
  FALSE
})

if (ok && file.exists(out_pdf)) {
  cat("PDF written:", out_pdf, "| size (bytes):", file.info(out_pdf)$size, "\n")
}

# Verify SKILL.md's claim: passing the ID instead of the NAME should fail/misbehave.
cat("\n--- Verifying the documented misuse case: viewPathway(ID) instead of viewPathway(NAME) ---\n")
bad <- tryCatch({
  viewPathway(top_id, organism = "human", readable = TRUE)
}, error = function(e) {
  cat("ERROR raised (as SKILL.md implies an id would misbehave):", conditionMessage(e), "\n")
  NULL
})
if (!is.null(bad)) cat("No error; object class:", class(bad), "\n")

web_url <- paste0("https://reactome.org/PathwayBrowser/#/", top_id)
cat("\nPathwayBrowser URL:", web_url, "\n")
