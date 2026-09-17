# go-enrichment Input 7 (new, Scope boundary / adversarial hunt): three claims not exercised
# by the pre-fix audit's 5 inputs, checked independently on this machine's clusterProfiler
# 4.14.6 / org.Hs.eg.db 3.20.0 / org.Mm.eg.db:
#  (a) "enrichGO's source default is ont='MF', not 'BP'" -- checked against the installed
#      function's actual formals, not assumed.
#  (b) "Other Organisms": swapping OrgDb to org.Mm.eg.db runs (mouse GO ORA).
#  (c) the enrichment_force_universe option (Checked, not changed in the fix log) --
#      independently re-derived here rather than trusted from the fix log.
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})

cat('--- (a) enrichGO documented default ont ---\n')
f <- formals(enrichGO)
cat('installed enrichGO() formal default for ont:', deparse(f$ont), '\n')
cat('SKILL.md claim ("source default is ont=\'MF\'") matches installed default:', identical(eval(f$ont)[1], 'MF'), '\n')

cat('\n--- (b) Other Organisms: org.Mm.eg.db swap ---\n')
mm_ok <- requireNamespace('org.Mm.eg.db', quietly = TRUE)
cat('org.Mm.eg.db installed:', mm_ok, '\n')
if (mm_ok) {
  suppressPackageStartupMessages(library(org.Mm.eg.db))
  mm_keys <- keys(org.Mm.eg.db, keytype = 'ENTREZID')
  set.seed(7)
  mm_universe <- sample(mm_keys, 3000)
  mm_genes <- sample(mm_universe, 150)
  ego_mm <- enrichGO(gene = mm_genes, universe = mm_universe, OrgDb = org.Mm.eg.db, keyType = 'ENTREZID',
                      ont = 'BP', pAdjustMethod = 'BH', pvalueCutoff = 1, qvalueCutoff = 1, readable = TRUE)
  d_mm <- as.data.frame(ego_mm)
  cat('mouse enrichGO ran; terms (pvalueCutoff=1):', nrow(d_mm), '| columns match human run:',
      identical(colnames(d_mm), c('ONTOLOGY','ID','Description','GeneRatio','BgRatio','RichFactor','FoldEnrichment','zScore','pvalue','p.adjust','qvalue','geneID','Count')) ||
      identical(colnames(d_mm), c('ID','Description','GeneRatio','BgRatio','RichFactor','FoldEnrichment','zScore','pvalue','p.adjust','qvalue','geneID','Count')), '\n')
} else {
  cat('org.Mm.eg.db NOT installed in this env -- Other Organisms claim not executable here\n')
}

cat('\n--- (c) enrichment_force_universe option ---\n')
GG <- 'F:/OpenScience/audits/bio-pathway-go-enrichment'
tab <- read.csv(file.path(GG, 'data', 'proteomics_da_table.csv'), colClasses = 'character')
tab$hit_signal <- tab$hit_signal == 'TRUE'
gene_list <- unique(tab$entrez[tab$hit_signal])
universe_ids <- unique(tab$entrez)
# inject a handful of universe genes with NO GO annotation at all, to distinguish
# "intersect with annotated genes" (default) from "keep universe as given"
unannotated <- setdiff(keys(org.Hs.eg.db, keytype='ENTREZID'), keys(org.Hs.eg.db, keytype='ENTREZID', column='GO'))
extra_unannotated <- head(setdiff(unannotated, universe_ids), 50)
universe_with_unannotated <- c(universe_ids, extra_unannotated)
cat('universe: matched genes', length(universe_ids), '+ deliberately unannotated genes', length(extra_unannotated), '=', length(universe_with_unannotated), '\n')

options(enrichment_force_universe = FALSE)
ego_default <- enrichGO(gene_list, universe = universe_with_unannotated, OrgDb = org.Hs.eg.db, keyType='ENTREZID', ont='BP', pvalueCutoff=1, qvalueCutoff=1)
n_default <- unique(sapply(strsplit(as.data.frame(ego_default)$BgRatio, '/'), `[`, 2))

options(enrichment_force_universe = TRUE)
ego_forced <- enrichGO(gene_list, universe = universe_with_unannotated, OrgDb = org.Hs.eg.db, keyType='ENTREZID', ont='BP', pvalueCutoff=1, qvalueCutoff=1)
n_forced <- unique(sapply(strsplit(as.data.frame(ego_forced)$BgRatio, '/'), `[`, 2))
options(enrichment_force_universe = FALSE)  # reset

cat('BgRatio denominator N, force_universe=FALSE (default, should intersect w/ annotated):', n_default, '\n')
cat('BgRatio denominator N, force_universe=TRUE  (should keep universe as given, full universe =', length(universe_with_unannotated), 'if truly unfiltered):', n_forced, '\n')
cat('full universe size:', length(universe_with_unannotated), '| deliberately-unannotated genes added:', length(extra_unannotated), '\n')
cat('forced N - default N =', as.numeric(n_forced) - as.numeric(n_default), '(expect this to be close to', length(extra_unannotated), 'if force_universe=TRUE keeps unannotated genes in N; expect forced N == full universe size if force_universe disables the annotated-only filter entirely)\n')
