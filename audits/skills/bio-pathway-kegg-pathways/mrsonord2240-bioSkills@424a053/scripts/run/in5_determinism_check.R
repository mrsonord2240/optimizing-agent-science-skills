# Input 5 (Stress, NEW -- determinism / P1 seed-fix verification):
# "Run the same SPIA + graphite-route analysis twice in separate sessions and confirm you get
# identical numbers both times" -- probes whether the fix log's second P1 claim (set.seed(123)
# added immediately before BOTH spia() and runSPIA() in SKILL.md and examples/kegg_spia_topology.R,
# closing pre-fix's 'SPIA's own worked example omits set.seed()' finding) actually makes the
# stochastic bootstrap reproducible end to end, for BOTH the direct spia() path and the graphite
# route -- not just present in the text.
suppressMessages({
  library(SPIA)
  library(graphite)
  library(clusterProfiler)
  library(org.Hs.eg.db)
})

de <- read.csv('../data/SYNTHETIC_de_results.csv')
sig <- de[de$padj < 0.05, ]
map <- suppressMessages(bitr(sig$gene, 'SYMBOL', 'ENTREZID', org.Hs.eg.db))
de_vec <- setNames(sig$log2FoldChange[match(map$SYMBOL, sig$gene)], map$ENTREZID)
de_vec <- de_vec[!duplicated(names(de_vec))]
universe <- suppressMessages(bitr(de$gene[!is.na(de$pvalue)], 'SYMBOL', 'ENTREZID', org.Hs.eg.db))$ENTREZID

run_direct <- function() {
  set.seed(123)   # exactly as the fixed SKILL.md/examples now document before spia()
  spia(de=de_vec, all=universe, organism='hsa', nB=50, plots=FALSE, verbose=FALSE)
}
run_graphite <- function(tag) {
  db <- pathways('hsapiens', 'kegg')
  db <- convertIdentifiers(db, 'ENTREZID')
  de_vec_gr   <- setNames(de_vec, paste0('ENTREZID:', names(de_vec)))
  universe_gr <- paste0('ENTREZID:', universe)
  owd <- getwd(); setwd(tempdir())
  prepareSPIA(db, tag)
  set.seed(123)   # exactly as the fixed SKILL.md/examples now document before runSPIA()
  r <- runSPIA(de=de_vec_gr, all=universe_gr, tag, nB=50)
  setwd(owd)
  r
}

cat("=== Direct spia(), run twice with set.seed(123) before each ===\n")
r1 <- run_direct()
r2 <- run_direct()
identical_pGFdr <- isTRUE(all.equal(r1$pGFdr, r2$pGFdr))
identical_tA    <- isTRUE(all.equal(r1$tA, r2$tA))
cat("Run 1 vs Run 2 identical pGFdr column:", identical_pGFdr, "\n")
cat("Run 1 vs Run 2 identical tA column:", identical_tA, "\n")
cat("Sample pGFdr run1 vs run2 (first 3 rows, same ID order):\n")
print(data.frame(ID=r1$ID[1:3], pGFdr_run1=r1$pGFdr[1:3], pGFdr_run2=r2$pGFdr[1:3]))

cat("\n=== graphite runSPIA(), run twice with set.seed(123) before each ===\n")
g1 <- run_graphite('kegg_hsa_spia_det1')
g2 <- run_graphite('kegg_hsa_spia_det2')
g_identical_pGFdr <- isTRUE(all.equal(sort(g1$pGFdr), sort(g2$pGFdr)))
cat("graphite Run 1 vs Run 2 identical pGFdr distribution:", g_identical_pGFdr, "\n")
cat("nrow g1:", nrow(g1), " nrow g2:", nrow(g2), "\n")
