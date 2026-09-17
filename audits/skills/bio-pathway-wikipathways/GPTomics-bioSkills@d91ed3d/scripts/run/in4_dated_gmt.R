# Input 4 (Variant B): usage-guide.md "Reproducible analysis" prompt -- pin a dated GMT release,
# split the compound term field, run enricher on the pinned sets, report the date.
suppressMessages({
  library(rWikiPathways)
  library(clusterProfiler)
  library(org.Hs.eg.db)
  library(tidyr)
})

de_results <- read.csv('../data/de_results_synthetic.csv', stringsAsFactors = FALSE)
sig_symbols <- de_results[de_results$padj < 0.05 & abs(de_results$log2FoldChange) > 1, 'gene_symbol']
sig <- bitr(sig_symbols, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)$ENTREZID
all_entrez <- bitr(de_results$gene_symbol, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)$ENTREZID

dl_dir <- tempdir()
t0 <- Sys.time()
# NOTE (audit finding): the SKILL.md/usage-guide.md worked example uses date='20240310'. That date
# 404s -- data.wikipathways.org's own index page states "This site hosts monthly data releases for
# the last 12 months" and its folder listing confirms it (checked live 2026-09-17): entries jump
# straight from 20230810 (a 3-file stray, not a full archive) to 20260110, i.e. every monthly folder
# between Aug 2023 and Jan 2026 is gone. Re-run with a currently-valid recent date to test the
# MECHANISM, and separately record the stale-example finding.
gmt <- tryCatch(
  downloadPathwayArchive(date = '20260810', organism = 'Homo sapiens', format = 'gmt', destpath = dl_dir),
  error = function(e) e
)
cat("downloadPathwayArchive took", as.numeric(Sys.time()-t0, units='secs'), "s\n")
if (inherits(gmt, 'error')) {
  cat("downloadPathwayArchive ERROR:", conditionMessage(gmt), "\n")
  quit(save='no', status=0)
}
cat("downloaded file:", gmt, "\n")
full_path <- file.path(dl_dir, gmt)
cat("file exists:", file.exists(full_path), " size:", file.info(full_path)$size, "bytes\n")

wp2gene <- read.gmt(full_path)
cat("raw GMT rows:", nrow(wp2gene), " unique terms (pre-split):", length(unique(wp2gene$term)), "\n")
cat("sample raw term:", head(wp2gene$term, 1), "\n")

wp2gene <- separate(wp2gene, term, c('name','version','wpid','org'), sep='%')
cat("post-split columns:", paste(colnames(wp2gene), collapse=','), "\n")
cat("WP554 present in this dated (2024-03-10) archive:", 'WP554' %in% wp2gene$wpid, "\n")
cat("WP430 present in this dated (2024-03-10) archive:", 'WP430' %in% wp2gene$wpid, "\n")

t2g <- wp2gene[, c('wpid','gene')]
t2n <- unique(wp2gene[, c('wpid','name')])

wp_pinned <- enricher(sig, universe = all_entrez, TERM2GENE = t2g, TERM2NAME = t2n,
                       pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500,
                       qvalueCutoff = 0.2)
res <- as.data.frame(wp_pinned)
cat("\nn significant terms (dated 2024-03-10 archive):", nrow(res), "\n")
print(head(res[order(res$p.adjust), c('ID','Description','p.adjust','Count')], 10), row.names=FALSE)
cat("\nWP554 present:", 'WP554' %in% res$ID, "\n")
cat("WP430 present:", 'WP430' %in% res$ID, "\n")

# gson_WP is NOT a reproducibility pin -- confirm it still pulls current/ (2 calls should differ from
# the dated archive's term count if the WP database has grown since 2024-03-10)
gs <- tryCatch(gson_WP(organism = 'Homo sapiens'), error = function(e) e)
if (inherits(gs, 'error')) {
  cat("\ngson_WP ERROR:", conditionMessage(gs), "\n")
} else {
  cat("\ngson_WP() term count (current/):", length(gs@gsid2gene[[1]]), "vs dated-archive term count:", length(unique(t2g$wpid)), "\n")
}
