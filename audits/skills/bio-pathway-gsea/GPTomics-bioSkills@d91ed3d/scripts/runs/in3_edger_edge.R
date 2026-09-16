# INPUT 3 (Edge) - "My DE came out of edgeR QL so there is no Wald stat column,
# only logFC and PValue - and a few PValue are exactly 0. The table is keyed by
# gene SYMBOL, it is not sorted, and my symbol table has ~300 duplicate rows.
# Build the ranking correctly from this and run GO BP GSEA."
#
# Code = the SKILL.md signed-p ranking recipe + the dedup/sort rules + the
# Common Errors bitr route, applied to the messy table VERBATIM as written.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
D <- 'F:/OpenScience/audits/bio-pathway-gsea/data'; R <- 'F:/OpenScience/audits/bio-pathway-gsea/runs'
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})

edg <- read.csv(file.path(D, 'SYNTHETIC_edger_qlf.csv'))
cat('edgeR table rows =', nrow(edg), '| duplicate gene names =', sum(duplicated(edg$gene)),
    '| PValue == 0 exactly:', sum(edg$PValue == 0), '| has a stat column:', 'stat' %in% names(edg), '\n')

# --- what the SKILL.md says NOT to do, to check the documented symptom ------
naive <- -log10(pmax(edg$PValue, 1e-300)); names(naive) <- edg$gene
cat('\n[control] unsigned -log10(p): correlation with signed metric =',
    round(cor(naive, sign(edg$logFC) * naive, method = 'spearman'), 3),
    '| fraction of the top 200 that are DOWN-regulated:',
    round(mean(edg$logFC[order(-naive)][1:200] < 0), 3), '\n')

# ================= SKILL.md recipe, verbatim ===============================
# "Ranking by sign(log2FC) * -log10(pmax(pvalue, 1e-300)) (for edgeR, or when a
#  Wald stat is unavailable) preserves direction and clamps p==0 from Inf."
gene_list <- sign(edg$logFC) * -log10(pmax(edg$PValue, 1e-300))
names(gene_list) <- edg$gene
gene_list <- gene_list[!is.na(gene_list)]
gene_list <- gene_list[!duplicated(names(gene_list))]   # one statistic per gene
gene_list <- sort(gene_list, decreasing = TRUE)         # REQUIRED
# ===========================================================================
cat('\nsigned-p vector: n =', length(gene_list), '| any Inf:', any(is.infinite(gene_list)),
    '| max', round(max(gene_list),2), '| min', round(min(gene_list),2),
    '| duplicates left:', sum(duplicated(names(gene_list))), '\n')

# --- Common Errors row: "--> No gene can be mapped" when IDs are SYMBOLs ----
cat('\n[Common Errors check] gseGO with SYMBOL names but keyType="ENTREZID":\n')
msg <- tryCatch({ set.seed(123)
  x <- gseGO(geneList = head(gene_list, 3000), OrgDb = org.Hs.eg.db, keyType = 'ENTREZID',
             ont = 'BP', minGSSize = 10, maxGSSize = 500, eps = 0, seed = TRUE, verbose = TRUE)
  paste('returned', nrow(as.data.frame(x)), 'rows') },
  error = function(e) paste('ERROR:', conditionMessage(e)),
  warning = function(w) paste('WARNING:', conditionMessage(w)))
cat('  ->', msg, '\n')

# --- the documented fix: bitr to the expected ID type ----------------------
map <- bitr(names(gene_list), fromType = 'SYMBOL', toType = 'ENTREZID', OrgDb = org.Hs.eg.db)
cat('\nbitr SYMBOL->ENTREZID: mapped', nrow(map), 'of', length(gene_list),
    '(', round(100*nrow(map)/length(gene_list),1), '% ) | one-to-many symbol rows:',
    sum(duplicated(map$SYMBOL)), '\n')
gl <- gene_list[map$SYMBOL]; names(gl) <- map$ENTREZID
gl <- gl[!duplicated(names(gl))]
gl <- sort(gl, decreasing = TRUE)
cat('final Entrez-named vector n =', length(gl), '\n')

set.seed(123)
gse <- gseGO(geneList = gl, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID', ont = 'BP',
             exponent = 1, minGSSize = 10, maxGSSize = 500, eps = 0,
             pvalueCutoff = 0.05, pAdjustMethod = 'BH', seed = TRUE, by = 'fgsea', verbose = FALSE)
gse <- setReadable(gse, OrgDb = org.Hs.eg.db, keyType = 'ENTREZID')
r <- as.data.frame(gse)
cat('\nsignificant GO BP terms from the signed-p ranking:', nrow(r),
    '| pos NES', sum(r$NES>0), '| neg NES', sum(r$NES<0), '\n')
print(head(r[order(r$p.adjust), c('Description','setSize','NES','p.adjust')], 8), row.names=FALSE)
cat('\nplanted UP recovered:', any(grepl('respirat|oxidative phosph|electron transport', r$Description[r$NES>0], ignore.case=TRUE)),
    '| planted DOWN recovered:', any(grepl('DNA replication', r$Description[r$NES<0], ignore.case=TRUE)), '\n')

# --- the documented symptom of skipping dedup+sort -------------------------
cat('\n[failure-mode check] same data WITHOUT dedup and WITHOUT sorting:\n')
raw <- sign(edg$logFC) * -log10(pmax(edg$PValue, 1e-300)); names(raw) <- edg$gene
m2 <- bitr(names(raw), fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)
r2 <- raw[m2$SYMBOL]; names(r2) <- m2$ENTREZID          # duplicates KEPT, order KEPT
out <- tryCatch({ set.seed(123)
  z <- gseGO(geneList = r2, OrgDb = org.Hs.eg.db, keyType='ENTREZID', ont='BP', minGSSize=10,
             maxGSSize=500, eps=0, pvalueCutoff=0.05, seed=TRUE, by='fgsea', verbose=FALSE)
  paste('returned', nrow(as.data.frame(z)), 'terms') },
  error=function(e) paste('ERROR:', conditionMessage(e)),
  warning=function(w) paste('WARNING:', conditionMessage(w)))
cat('  ->', out, '\n')
write.csv(r, file.path(R, 'in3_terms.csv'), row.names = FALSE)
cat('\nEXIT OK\n')
