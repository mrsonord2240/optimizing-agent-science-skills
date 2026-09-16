# Does a SORTED vector with duplicate gene names actually change the ES, as the
# SKILL.md "Unsorted or duplicated geneList" failure mode claims?
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
R <- 'F:/OpenScience/audits/bio-pathway-gsea/runs'
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
gl <- readRDS(file.path(R, 'gene_list.rds'))
dupv <- sort(c(gl, gl[1:300]), decreasing = TRUE)
cat('clean n =', length(gl), '| with duplicates n =', length(dupv),
    '| duplicated names =', sum(duplicated(names(dupv))), '\n')
go <- function(v) { set.seed(123)
  gseGO(v, OrgDb=org.Hs.eg.db, keyType='ENTREZID', ont='BP', minGSSize=10, maxGSSize=500,
        eps=0, pvalueCutoff=0.05, pAdjustMethod='BH', seed=TRUE, by='fgsea', verbose=FALSE) }
a <- as.data.frame(go(gl))
b <- tryCatch(as.data.frame(go(dupv)), error=function(e){cat('dup run ERROR:', conditionMessage(e), '\n'); NULL})
if (!is.null(b)) {
  m <- merge(a[,c('ID','NES','p.adjust')], b[,c('ID','NES','p.adjust')], by='ID', suffixes=c('.clean','.dup'))
  cat('terms clean =', nrow(a), '| terms dup =', nrow(b), '| shared =', nrow(m), '\n')
  cat('max |dNES| among shared terms =', signif(max(abs(m$NES.clean - m$NES.dup)), 4), '\n')
  cat('terms only in clean:', nrow(a) - nrow(m), '| only in dup:', nrow(b) - nrow(m), '\n')
  cat('top term clean:', a$ID[which.min(a$p.adjust)], 'NES', round(a$NES[which.min(a$p.adjust)],4),
      '| dup:', b$ID[which.min(b$p.adjust)], 'NES', round(b$NES[which.min(b$p.adjust)],4), '\n')
}
cat('EXIT OK\n')
