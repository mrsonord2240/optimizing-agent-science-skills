args <- commandArgs(trailingOnly = TRUE)
input <- as.integer(args[[1]])
run_dir <- '/mnt/openscience/audits/bio-pathway-wikipathways/run'
source_dir <- '/mnt/openscience/wt/pathway-analysis-wikipathways/pathway-analysis/wikipathways'
rscript_bin <- file.path(R.home('bin'), 'Rscript')

if (input == 1L) {
  suppressPackageStartupMessages(library(rWikiPathways))
  orgs <- listOrganisms()
  human <- listPathways('Homo sapiens')
  info <- getPathwayInfo('WP554')
  xrefs <- getXrefList('WP554', 'L')
  stopifnot(length(orgs) >= 20, nrow(human) >= 500, length(xrefs) >= 10)
  cat(sprintf('ASSERT input1 organisms=%d human_pathways=%d wp554_entrez=%d info_class=%s\n', length(orgs), nrow(human), length(xrefs), class(info)[1]))
}

if (input == 2L) {
  cmd <- c(file.path(source_dir, 'scripts/wikipathways_pinned_enrich.R'), file.path(run_dir, 'sig_entrez.txt'), file.path(run_dir, 'universe_entrez.txt'), shQuote('Homo sapiens'), file.path(run_dir, 'pinned.csv'))
  status <- system2(rscript_bin, cmd)
  stopifnot(status == 0, file.exists(file.path(run_dir, 'pinned.csv')))
  tab <- read.csv(file.path(run_dir, 'pinned.csv'))
  stopifnot(nrow(tab) > 0, any(tab$ID == 'WP554'))
  cat(sprintf('ASSERT input2 pinned_rows=%d wp554=%s\n', nrow(tab), 'WP554' %in% tab$ID))
}

if (input == 3L) {
  suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
  de <- read.csv(file.path(run_dir, 'de_results.csv'))
  sig <- bitr(de$gene_symbol[de$padj < .05], 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  all_entrez <- bitr(de$gene_symbol, 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  ora <- enrichWP(sig, organism = 'Homo sapiens', universe = all_entrez, minGSSize = 10, maxGSSize = 500)
  gmap <- bitr(de$gene_symbol, 'SYMBOL', 'ENTREZID', org.Hs.eg.db)
  gl <- setNames(de$log2FoldChange[match(gmap$SYMBOL, de$gene_symbol)], gmap$ENTREZID)
  gl <- sort(gl[!duplicated(names(gl))], decreasing = TRUE)
  set.seed(123); gsea <- gseWP(gl, organism = 'Homo sapiens', minGSSize = 10, maxGSSize = 500)
  stopifnot(nrow(as.data.frame(ora)) > 0, nrow(as.data.frame(gsea)) > 0)
  cat(sprintf('ASSERT input3 ora=%d gsea=%d wp554_ora=%s\n', nrow(as.data.frame(ora)), nrow(as.data.frame(gsea)), 'WP554' %in% as.data.frame(ora)$ID))
}

if (input == 4L) {
  suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
  de <- read.csv(file.path(run_dir, 'de_results.csv'))
  sig <- bitr(de$gene_symbol[de$padj < .05], 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  all_entrez <- bitr(de$gene_symbol, 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  matched <- enrichWP(sig, organism = 'Homo sapiens', universe = all_entrez, minGSSize = 10)
  default <- enrichWP(sig, organism = 'Homo sapiens', minGSSize = 10)
  m <- as.data.frame(matched); d <- as.data.frame(default)
  stopifnot(nrow(m) > 0, nrow(d) > 0, 'WP554' %in% m$ID, 'WP554' %in% d$ID)
  cat(sprintf('ASSERT input4 matched_bg=%s default_bg=%s wp554_matched=%g wp554_default=%g\n', m$BgRatio[match('WP554', m$ID)], d$BgRatio[match('WP554', d$ID)], m$p.adjust[match('WP554', m$ID)], d$p.adjust[match('WP554', d$ID)]))
}

if (input == 5L) {
  suppressPackageStartupMessages(library(rWikiPathways))
  absent <- exists('get_wp_organisms', where = asNamespace('rWikiPathways'), inherits = FALSE)
  standalone_call <- try(get_wp_organisms(), silent = TRUE)
  parsed <- try(parse(file.path(source_dir, 'examples/wikipathways_explore.R')), silent = TRUE)
  stopifnot(!inherits(parsed, 'try-error'))
  cat(sprintf('ASSERT input5 get_wp_organisms_export=%s standalone_rwiki_error=%s explore_parses=TRUE\n', absent, inherits(standalone_call, 'try-error')))
}

if (input == 6L) {
  old <- getwd(); on.exit(setwd(old), add = TRUE); setwd(run_dir)
  status <- system2(rscript_bin, file.path(source_dir, 'examples/wikipathways_ora.R'))
  stopifnot(status == 0)
  cat('ASSERT input6 shipped_ora_exit=0\n')
}

if (input == 7L) {
  old <- getwd(); on.exit(setwd(old), add = TRUE); setwd(run_dir)
  status <- system2(rscript_bin, file.path(source_dir, 'examples/wikipathways_explore.R'))
  cat(sprintf('ASSERT input7 shipped_explore_exit=%d\n', status))
  if (status != 0) quit(status = 7)
}
