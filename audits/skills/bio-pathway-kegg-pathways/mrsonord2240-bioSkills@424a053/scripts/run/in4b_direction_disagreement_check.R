# Follow-up to Input 4: the graphite route (now running after the P0 fix) reported hsa04110
# (Cell cycle, planted UP) as Inhibited with tA=-66.73, while the SAME input data through direct
# spia() reported it Activated with tA=+67.42 -- an apparent sign disagreement between the two
# routes SKILL.md presents as interchangeable ("the graphite route... works on Reactome too").
# This script checks whether that is a one-off or a systematic sign difference across all
# pathways both routes scored, using the SAME de_vec/universe (ENTREZID-prefixed for graphite,
# as the fixed SKILL.md documents) and the SAME seed, so any difference is attributable to the
# topology source, not to randomness or ID prep.
suppressMessages({
  library(SPIA); library(graphite); library(clusterProfiler); library(org.Hs.eg.db)
})

de <- read.csv('../data/SYNTHETIC_de_results.csv')
sig <- de[de$padj < 0.05, ]
map <- suppressMessages(bitr(sig$gene, 'SYMBOL', 'ENTREZID', org.Hs.eg.db))
de_vec <- setNames(sig$log2FoldChange[match(map$SYMBOL, sig$gene)], map$ENTREZID)
de_vec <- de_vec[!duplicated(names(de_vec))]
universe <- suppressMessages(bitr(de$gene[!is.na(de$pvalue)], 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID

set.seed(123)
res <- spia(de=de_vec, all=universe, organism='hsa', nB=50, plots=FALSE, verbose=FALSE)

db <- pathways('hsapiens', 'kegg')
db <- convertIdentifiers(db, 'ENTREZID')
de_vec_gr   <- setNames(de_vec, paste0('ENTREZID:', names(de_vec)))
universe_gr <- paste0('ENTREZID:', universe)
owd <- getwd(); setwd(tempdir())
prepareSPIA(db, 'kegg_hsa_spia_in4b')
set.seed(123)
gr <- runSPIA(de=de_vec_gr, all=universe_gr, 'kegg_hsa_spia_in4b', nB=50)
setwd(owd)

m <- merge(res[,c("Name","tA","Status")], gr[,c("Name","tA","Status")], by="Name", suffixes=c("_direct","_graphite"))
cat("Pathways scored by BOTH routes (matched by Name):", nrow(m), "of direct=", nrow(res), "graphite=", nrow(gr), "\n")
m$sign_agree <- sign(m$tA_direct) == sign(m$tA_graphite)
cat("tA sign AGREES between direct spia() and graphite route:", sum(m$sign_agree), "of", nrow(m), "\n")
cat("tA sign DISAGREES (opposite direction call):", sum(!m$sign_agree), "of", nrow(m), "\n")
cr <- cor(m$tA_direct, m$tA_graphite, method="pearson")
cat("Pearson correlation of tA_direct vs tA_graphite across matched pathways:", round(cr,4), "\n")
cat("\nSample rows:\n")
print(head(m[order(m$Name),], 12), row.names=FALSE)
write.csv(m, "in4b_direction_comparison.csv", row.names=FALSE)
