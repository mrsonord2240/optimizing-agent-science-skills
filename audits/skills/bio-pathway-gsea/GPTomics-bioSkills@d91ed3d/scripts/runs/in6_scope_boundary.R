# INPUT 6 (Scope boundary) - "I pulled 180 hit genes out of my CRISPR screen.
# There's no statistic attached, just the hit list. Run GSEA on them and tell me
# which pathways are enriched."
#
# The SKILL.md Scope line says: "A pre-selected unranked gene LIST -> go-enrichment
# (ORA)." This script checks (1) that the routing rule is stated where an agent
# will see it, and (2) what actually happens if the Skill is pushed past it.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
D <- 'F:/OpenScience/audits/bio-pathway-gsea/data'
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
hits <- readLines(file.path(D,'SYNTHETIC_screen_hits.txt'))
cat('SYNTHETIC screen hit list:', length(hits), 'gene symbols, no statistic\n')
m <- bitr(hits, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)
ids <- unique(m$ENTREZID); cat('mapped to', length(ids), 'Entrez IDs\n')

cat('\n--- (1) forcing GSEA anyway, with a constant pseudo-rank (all 1) ---\n')
v <- setNames(rep(1, length(ids)), ids)
o <- tryCatch({ set.seed(123)
  z <- gseGO(v, OrgDb=org.Hs.eg.db, keyType='ENTREZID', ont='BP', minGSSize=10, maxGSSize=500,
             eps=0, pvalueCutoff=0.05, seed=TRUE, by='fgsea', verbose=FALSE)
  paste('returned', nrow(as.data.frame(z)), 'terms') },
  error=function(e) paste('ERROR:', conditionMessage(e)),
  warning=function(w) paste('WARNING:', conditionMessage(w)))
cat('  ->', o, '\n')

cat('\n--- (2) forcing GSEA with an arbitrary descending pseudo-rank ---\n')
v2 <- setNames(seq(length(ids), 1), ids)
o2 <- tryCatch({ set.seed(123)
  z <- gseGO(v2, OrgDb=org.Hs.eg.db, keyType='ENTREZID', ont='BP', minGSSize=10, maxGSSize=500,
             eps=0, pvalueCutoff=0.05, seed=TRUE, by='fgsea', verbose=FALSE)
  d <- as.data.frame(z); cat('  terms:', nrow(d), '\n')
  if (nrow(d)) print(head(d[order(d$p.adjust), c('Description','setSize','NES','p.adjust')], 5), row.names=FALSE)
  'completed' },
  error=function(e) paste('ERROR:', conditionMessage(e)),
  warning=function(w) paste('WARNING:', conditionMessage(w)))
cat('  ->', o2, '\n')

cat('\n--- (3) the route the SKILL.md actually prescribes: ORA (go-enrichment) ---\n')
ora <- enrichGO(gene=ids, OrgDb=org.Hs.eg.db, keyType='ENTREZID', ont='BP',
                pAdjustMethod='BH', pvalueCutoff=0.05, qvalueCutoff=0.2,
                minGSSize=10, maxGSSize=500)
d <- as.data.frame(ora)
cat('  enrichGO terms:', nrow(d), '\n')
if (nrow(d)) print(head(d[order(d$p.adjust), c('Description','GeneRatio','BgRatio','p.adjust')], 5), row.names=FALSE)
cat('\nEXIT OK\n')
