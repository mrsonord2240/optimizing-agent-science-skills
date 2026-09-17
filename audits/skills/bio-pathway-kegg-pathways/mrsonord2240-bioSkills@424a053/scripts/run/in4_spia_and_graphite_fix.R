# Input 4 (Variant B, regression + P0 FIX VERIFICATION): "I have a human DE list with log2
# fold-changes and a universe. Run SPIA so direction and network position are used, tell me which
# signaling pathways are activated vs inhibited, and explain why this is not appropriate for
# metabolic pathways." Also runs the graphite route exactly as the FIXED SKILL.md now documents it
# (relative pathwaySetName + setwd(tempdir())/setwd(owd) pair, 'ENTREZID:' prefix on de_vec/universe
# before calling runSPIA) -- this is the code the pre-fix audit's Research Veto M4 failed on.
# nB reduced from the shipped 2000 to 50 for audit turnaround only (same reduction the fixer used
# in their own verification, F:\optimizing-agent-science-skills\fixes\bio-pathway-kegg-pathways.md);
# the mechanism under test is whether the join/path bug is fixed, not bootstrap-count precision,
# which pre-fix Input 4 already validated for the direct spia() path.
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

cat("=== Direct spia() ===\n")
cat("DE vec length:", length(de_vec), " universe:", length(universe), "\n")
set.seed(123)
t0 <- Sys.time()
res <- spia(de=de_vec, all=universe, organism='hsa', nB=50, plots=FALSE, verbose=FALSE)
cat("SPIA wall time:", round(as.numeric(Sys.time()-t0,units="secs"),1), "s\n")
cat("Pathways scored:", nrow(res), "\n")
row_cc <- res[res$ID=="04110",]
row_ins <- res[res$ID=="04910",]
cat("Planted hsa04110 (Cell cycle): pGFdr=", if(nrow(row_cc)>0) signif(row_cc$pGFdr,3) else "NOT SCORED",
    " Status=", if(nrow(row_cc)>0) row_cc$Status else "NA", " tA=", if(nrow(row_cc)>0) round(row_cc$tA,2) else "NA", "\n")
cat("Planted hsa04910 (Insulin signaling): pGFdr=", if(nrow(row_ins)>0) signif(row_ins$pGFdr,3) else "NOT SCORED",
    " Status=", if(nrow(row_ins)>0) row_ins$Status else "NA", " tA=", if(nrow(row_ins)>0) round(row_ins$tA,2) else "NA", "\n")
row_gly <- res[res$ID=="00010",]
cat("Metabolic hsa00010 (Glycolysis) present in SPIA output at all:", nrow(row_gly)>0, "(documented: absent, not scored)\n")

cat("\n=== graphite route, EXACTLY as the FIXED SKILL.md documents it ===\n")
db <- pathways('hsapiens', 'kegg')
db <- convertIdentifiers(db, 'ENTREZID')
de_vec_gr   <- setNames(de_vec, paste0('ENTREZID:', names(de_vec)))
universe_gr <- paste0('ENTREZID:', universe)
owd <- getwd(); setwd(tempdir())
prepareSPIA(db, 'kegg_hsa_spia_in4')
cat("prepareSPIA wrote the file:", file.exists(file.path(tempdir(), 'kegg_hsa_spia_in4SPIA.RData')), "\n")
set.seed(123)
gr <- tryCatch(
  runSPIA(de=de_vec_gr, all=universe_gr, 'kegg_hsa_spia_in4', nB=50),
  error=function(e) paste("ERROR:", conditionMessage(e)))
setwd(owd)

if (is.character(gr)) {
  cat("graphite runSPIA FAILED (P0 NOT fixed):", gr, "\n")
} else {
  cat("graphite runSPIA succeeded:", nrow(gr), "rows returned (pre-fix: 0 rows / hard error)\n")
  print(head(gr[order(gr$pGFdr), c("Name","pSize","NDE","pNDE","tA","pPERT","pG","pGFdr","Status")], 5), row.names=FALSE)
  gr_cc  <- gr[gr$Name=="Cell cycle",]
  gr_ins <- gr[grepl("Insulin signaling", gr$Name),]
  cat("\nPlanted Cell cycle row via graphite: pGFdr=", if(nrow(gr_cc)>0) signif(gr_cc$pGFdr,3) else "NOT FOUND",
      " Status=", if(nrow(gr_cc)>0) gr_cc$Status else "NA", "\n")
  cat("Planted Insulin signaling row via graphite: pGFdr=", if(nrow(gr_ins)>0) signif(gr_ins$pGFdr,3) else "NOT FOUND",
      " Status=", if(nrow(gr_ins)>0) gr_ins$Status else "NA", "\n")
  cat("\ngraphite runSPIA() output has ID/KEGGLINK columns (SKILL.md claims it does NOT):",
      any(c("ID","KEGGLINK") %in% colnames(gr)), "\n")
}
write.csv(res, "in4_spia_full.csv", row.names=FALSE)
