# Supplementary check (not one of the 7 scored inputs): verifies SKILL.md's specific
# quantitative claim that omitting `universe=` inflates significance and defaults the
# background to ~11,200 Reactome-annotated genes (vs. the 3000-gene measured background).
suppressMessages({
  library(ReactomePA)
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

sig_symbols <- read.csv("../data/significant_genes.csv", stringsAsFactors = FALSE)$SYMBOL
bg_symbols  <- read.csv("../data/background_genes.csv", stringsAsFactors = FALSE)$SYMBOL
sig_entrez <- bitr(sig_symbols, fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)$ENTREZID
universe   <- bitr(bg_symbols,  fromType = "SYMBOL", toType = "ENTREZID", OrgDb = org.Hs.eg.db)$ENTREZID

with_u <- enrichPathway(gene = sig_entrez, organism = "human", universe = universe,
                        pvalueCutoff = 1, qvalueCutoff = 1, minGSSize = 10, maxGSSize = 500)
without_u <- enrichPathway(gene = sig_entrez, organism = "human",
                           pvalueCutoff = 1, qvalueCutoff = 1, minGSSize = 10, maxGSSize = 500)

df_with <- as.data.frame(with_u)
df_without <- as.data.frame(without_u)

pw <- df_with[df_with$ID == "R-HSA-877300", ]
pwo <- df_without[df_without$ID == "R-HSA-877300", ]
cat("With universe (3000-gene background):    p.adjust =", pw$p.adjust,
    "| BgRatio =", pw$BgRatio, "\n")
cat("Without universe (implicit background):  p.adjust =", pwo$p.adjust,
    "| BgRatio =", pwo$BgRatio, "\n")
cat("Implicit background denominator matches SKILL.md's ~11,200 claim:",
    as.numeric(sub(".*/", "", pwo$BgRatio)), "\n")
cat("p.adjust smaller without universe (inflated significance):", pwo$p.adjust < pw$p.adjust, "\n")
