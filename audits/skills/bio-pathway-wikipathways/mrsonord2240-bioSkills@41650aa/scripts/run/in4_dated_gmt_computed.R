# Regression test for Input 4 / P1 fix: SKILL.md's "Reproducible Analysis with a Dated GMT"
# section now computes archive_date <- format(Sys.Date() - 60, '%Y%m10') instead of hardcoding
# '20240310'. Re-run the ORIGINAL Input 4 scenario (synthetic DE data, same assertions) but using
# the Skill's own current worked code block verbatim, to confirm the computed date (a) downloads
# successfully today and (b) still recovers the planted WP554/WP430 signal with correct stats.
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

# --- verbatim from the FIXED SKILL.md "Reproducible Analysis with a Dated GMT" code block ---
archive_date <- format(Sys.Date() - 60, '%Y%m10')   # e.g. '20260710'; report this date in methods
cat("computed archive_date:", archive_date, "\n")
gmt <- tryCatch(
  downloadPathwayArchive(date = archive_date, organism = 'Homo sapiens', format = 'gmt', destpath = dl_dir),
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
wp2gene <- separate(wp2gene, term, c('name','version','wpid','org'), sep='%')
cat("WP554 present in computed-date archive:", 'WP554' %in% wp2gene$wpid, "\n")
cat("WP430 present in computed-date archive:", 'WP430' %in% wp2gene$wpid, "\n")

t2g <- wp2gene[, c('wpid','gene')]
t2n <- unique(wp2gene[, c('wpid','name')])

wp_pinned <- enricher(sig, universe = all_entrez, TERM2GENE = t2g, TERM2NAME = t2n,
                       pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 10, maxGSSize = 500,
                       qvalueCutoff = 0.2)
res <- as.data.frame(wp_pinned)
cat("\nn significant terms (computed-date archive):", nrow(res), "\n")
print(head(res[order(res$p.adjust), c('ID','Description','p.adjust','Count')], 10), row.names=FALSE)
cat("\nWP554 present:", 'WP554' %in% res$ID, "\n")
cat("WP430 present:", 'WP430' %in% res$ID, "\n")

# --- New check for this re-audit: what happens if the archive_date lands one step outside the
# retention window (simulating a partial miss)? Does the script/Skill offer any documented
# recovery path, or does it just error like the pre-fix hardcoded date did?
cat("\n--- Simulated retention-window miss (archive_date - 400 days) ---\n")
stale_date <- format(Sys.Date() - 400, '%Y%m10')
cat("stale simulated date:", stale_date, "\n")
gmt2 <- tryCatch(
  downloadPathwayArchive(date = stale_date, organism = 'Homo sapiens', format = 'gmt', destpath = dl_dir),
  error = function(e) e
)
if (inherits(gmt2, 'error')) {
  cat("downloadPathwayArchive ERROR (expected, simulating an unlucky computed date):", conditionMessage(gmt2), "\n")
} else {
  cat("downloaded (unexpected success):", gmt2, "\n")
}
