input <- as.integer(commandArgs(trailingOnly = TRUE)[1])
stopifnot(input %in% 1:7)
root <- '/mnt/openscience/wt/pathway-kegg-pathways/pathway-analysis/kegg-pathways'
data_dir <- '/mnt/openscience/audits/bio-pathway-kegg-pathways/data'
run_dir <- '/mnt/openscience/audits/bio-pathway-kegg-pathways/run'
de <- read.csv(file.path(data_dir, 'de_results.csv'))

if (input == 1L) {
  library(clusterProfiler); library(org.Hs.eg.db); library(gson)
  sig <- de$gene[de$padj < .05 & abs(de$log2FoldChange) > 1]
  sig_entrez <- bitr(sig, 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  universe <- bitr(de$gene[!is.na(de$pvalue)], 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  kk <- enrichKEGG(sig_entrez, organism = 'hsa', keyType = 'ncbi-geneid', universe = universe, pvalueCutoff = 1, minGSSize = 10, maxGSSize = 500)
  mkk <- enrichMKEGG(sig_entrez, organism = 'hsa', keyType = 'ncbi-geneid', universe = universe, pvalueCutoff = 1)
  k <- gson_KEGG('hsa'); k@accessed_date <- as.character(Sys.Date())
  snapshot <- file.path(run_dir, 'kegg_hsa.gson'); write.gson(k, snapshot); k2 <- read.gson(snapshot)
  pinned <- enricher(sig_entrez, gson = k2, universe = universe, pvalueCutoff = 1)
  stopifnot(file.exists(snapshot), k2@accessed_date == as.character(Sys.Date()), nrow(as.data.frame(kk)) > 0, nrow(as.data.frame(pinned)) > 0)
  cat(sprintf('ASSERT input1 ora=%d modules=%d pinned=%d date=%s\n', nrow(as.data.frame(kk)), nrow(as.data.frame(mkk)), nrow(as.data.frame(pinned)), k2@accessed_date))
}

if (input == 2L) {
  library(clusterProfiler)
  gl <- sort(setNames(de$log2FoldChange[!is.na(de$log2FoldChange)], de$entrez[!is.na(de$log2FoldChange)]), decreasing = TRUE)
  set.seed(123)
  g <- gseKEGG(gl, organism = 'hsa', keyType = 'ncbi-geneid', minGSSize = 10, maxGSSize = 500, pvalueCutoff = 1, seed = TRUE, verbose = FALSE)
  stopifnot(is.data.frame(as.data.frame(g)), nrow(as.data.frame(g)) > 0, isTRUE(all.equal(gl, sort(gl, decreasing = TRUE))))
  cat(sprintf('ASSERT input2 gsea_terms=%d\n', nrow(as.data.frame(g))))
}

if (input == 3L) {
  library(clusterProfiler); library(org.Hs.eg.db)
  up <- bitr(de$gene[de$padj < .05 & de$log2FoldChange > 1], 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  down <- bitr(de$gene[de$padj < .05 & de$log2FoldChange < -1], 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  ck <- compareCluster(geneClusters = list(up = up, down = down), fun = 'enrichKEGG', organism = 'hsa', keyType = 'ncbi-geneid', pvalueCutoff = 1)
  result <- as.data.frame(ck)
  stopifnot(is.data.frame(result), nrow(result) > 0, all(result$Cluster %in% c('up', 'down')))
  cat(sprintf('ASSERT input3 compare_rows=%d clusters=%d\n', nrow(result), length(unique(result$Cluster))))
}

if (input == 4L) {
  library(SPIA); library(graphite); library(clusterProfiler); library(org.Hs.eg.db)
  sig <- de[de$padj < .05, ]
  sm <- bitr(sig$gene, 'SYMBOL', 'ENTREZID', org.Hs.eg.db)
  de_vec <- setNames(sig$log2FoldChange[match(sm$SYMBOL, sig$gene)], sm$ENTREZID)
  de_vec <- de_vec[!duplicated(names(de_vec))]
  universe <- bitr(de$gene[!is.na(de$pvalue)], 'SYMBOL', 'ENTREZID', org.Hs.eg.db)$ENTREZID
  set.seed(123); direct <- spia(de = de_vec, all = universe, organism = 'hsa', nB = 10, plots = FALSE)
  db <- convertIdentifiers(pathways('hsapiens', 'kegg'), 'ENTREZID')
  owd <- getwd(); setwd(run_dir); prepareSPIA(db, 'kegg_hsa_spia'); set.seed(123)
  # Structural audit only: the shipped example omits nB here, which invokes SPIA's
  # costly default of 2,000 bootstraps.  Keep this isolated branch executable
  # with one bootstrap; the omission itself is evaluated as a code-usability defect.
  graph <- runSPIA(setNames(de_vec, paste0('ENTREZID:', names(de_vec))), paste0('ENTREZID:', universe), 'kegg_hsa_spia', nB = 1)
  setwd(owd)
  stopifnot(nrow(direct) > 0, nrow(graph) > 0, all(c('pG', 'pGFdr', 'Status') %in% names(direct)), all(c('pG', 'pGFdr', 'Status') %in% names(graph)))
  cat(sprintf('ASSERT input4 spia=%d graphite=%d direct_cellcycle=%s\n', nrow(direct), nrow(graph), 'hsa04110' %in% direct$ID))
}

if (input == 5L) {
  library(clusterProfiler)
  eco <- c('b0002', 'b0003', 'b0004', 'b0008', 'b0014', 'b0025', 'b0030', 'b0040', 'b0050', 'b0060')
  r <- enrichKEGG(eco, organism = 'eco', keyType = 'kegg', pvalueCutoff = 1, minGSSize = 1)
  stopifnot(is.data.frame(as.data.frame(r)))
  cat(sprintf('ASSERT input5 prokaryotic_terms=%d keytype=kegg\n', nrow(as.data.frame(r))))
}

if (input == 6L) {
  library(pathview)
  vals <- setNames(de$log2FoldChange[!is.na(de$entrez)], de$entrez[!is.na(de$entrez)])
  old <- getwd(); setwd(run_dir)
  pathview(gene.data = vals, pathway.id = 'hsa04110', species = 'hsa', gene.idtype = 'entrez')
  setwd(old)
  outputs <- list.files(run_dir, pattern = 'hsa04110.*pathview.*(png|pdf)$', full.names = TRUE)
  stopifnot(length(outputs) > 0, all(file.info(outputs)$size > 1000))
  cat(sprintf('ASSERT input6 pathview_files=%d\n', length(outputs)))
}

if (input == 7L) {
  parse(file.path(root, 'examples', 'kegg_enrichment.R'))
  parse(file.path(root, 'examples', 'kegg_spia_topology.R'))
  stopifnot('enrichKEGG' %in% getNamespaceExports('clusterProfiler'), 'spia' %in% getNamespaceExports('SPIA'))
  cat('ASSERT input7 examples_parse_and_exports=TRUE\n')
}
