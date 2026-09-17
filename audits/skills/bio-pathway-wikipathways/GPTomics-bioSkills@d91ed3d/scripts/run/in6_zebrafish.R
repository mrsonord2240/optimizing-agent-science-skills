# Input 6 (Scope Boundary): "Run WikiPathways enrichment for zebrafish Entrez genes, and first
# confirm the exact organism string." Uses a REAL zebrafish WikiPathways pathway (WP468, the
# zebrafish "ACE inhibitor pathway") as the planted-truth gene list.
suppressMessages({
  library(rWikiPathways)
  library(clusterProfiler)
})

zorgs <- get_wp_organisms()
cat("Danio rerio in get_wp_organisms():", 'Danio rerio' %in% zorgs, "\n")
zorgs2 <- listOrganisms()
cat("Danio rerio in listOrganisms():", 'Danio rerio' %in% zorgs2, "\n")

zgenes <- getXrefList('WP468', 'L')  # zebrafish ACE inhibitor pathway, real WikiPathways xrefs
cat("WP468 (zebrafish ACE inhibitor pathway) n genes:", length(zgenes), "\n")

# background: WP468's genes plus a broader real sample of zebrafish Entrez ids annotated in WP
# (pull from a second, larger zebrafish pathway union to build a plausible tested-universe)
extra <- getXrefList('WP1330', 'L')  # a larger zebrafish pathway, for background bulk only
universe <- unique(c(zgenes, extra))
cat("universe size:", length(universe), "\n")

t0 <- Sys.time()
wp_zfish <- enrichWP(gene = zgenes, organism = 'Danio rerio', universe = universe,
                      pvalueCutoff = 0.05, pAdjustMethod = 'BH', minGSSize = 5, maxGSSize = 500)
cat("enrichWP (Danio rerio) took", as.numeric(Sys.time()-t0, units='secs'), "s\n")

if (is.null(wp_zfish)) {
  cat("enrichWP returned NULL\n")
} else {
  res <- as.data.frame(wp_zfish)
  cat("n significant terms:", nrow(res), "\n")
  print(res[order(res$p.adjust), c('ID','Description','p.adjust','Count')], row.names=FALSE)
  cat("\nWP468 present:", 'WP468' %in% res$ID, "\n")
}

# wrong organism string (a plausible mistake: common name instead of scientific binomial)
wrong <- tryCatch(enrichWP(gene = zgenes, organism = 'zebrafish', universe = universe), error=function(e) e)
if (inherits(wrong, 'error')) {
  cat("\norganism='zebrafish' (common name, not the exact scientific-name string) -> ERROR:", conditionMessage(wrong), "\n")
} else {
  cat("\norganism='zebrafish' -> ", if (is.null(wrong)) "NULL result" else paste(nrow(as.data.frame(wrong)), "terms"), "\n")
}
