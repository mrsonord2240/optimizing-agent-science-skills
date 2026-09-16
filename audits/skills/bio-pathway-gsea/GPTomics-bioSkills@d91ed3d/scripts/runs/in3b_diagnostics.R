# INPUT 3 follow-up diagnostics: separate the two failure modes the SKILL.md
# lumps together ("Unsorted or duplicated geneList -> silently wrong ES"), and
# quantify what pmax(p, 1e-300) does to the exponent=1 weights.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
D <- 'F:/OpenScience/audits/bio-pathway-gsea/data'; R <- 'F:/OpenScience/audits/bio-pathway-gsea/runs'
suppressPackageStartupMessages({library(clusterProfiler); library(org.Hs.eg.db)})
gl <- readRDS(file.path(R, 'gene_list.rds'))   # Entrez-named DESeq2 stat vector, sorted

run <- function(v, tag) {
  o <- tryCatch({ set.seed(123)
    z <- gseGO(geneList = v, OrgDb = org.Hs.eg.db, keyType='ENTREZID', ont='BP',
               minGSSize=10, maxGSSize=500, eps=0, pvalueCutoff=0.05, seed=TRUE,
               by='fgsea', verbose=FALSE)
    paste('OK -', nrow(as.data.frame(z)), 'terms') },
    error = function(e) paste('ERROR:', conditionMessage(e)),
    warning = function(w) paste('WARNING:', conditionMessage(w)))
  cat(sprintf('%-34s %s\n', tag, o))
}
cat('--- A. is "unsorted" silent or loud? ---\n')
run(gl,                              'sorted, unique (baseline)')
run(sample(gl),                      'SHUFFLED, unique')
run(sort(gl, decreasing = FALSE),    'sorted INCREASING, unique')
dupv <- c(gl, gl[1:300]); dupv <- sort(dupv, decreasing = TRUE)
run(dupv,                            'sorted, 300 DUPLICATE names')

cat('\n--- B. does a duplicated-but-sorted vector change the ES? ---\n')
set.seed(123); a <- as.data.frame(gseGO(gl, OrgDb=org.Hs.eg.db, keyType='ENTREZID', ont='BP',
    minGSSize=10, maxGSSize=500, eps=0, pvalueCutoff=0.05, seed=TRUE, by='fgsea', verbose=FALSE))
set.seed(123); b <- tryCatch(as.data.frame(gseGO(dupv, OrgDb=org.Hs.eg.db, keyType='ENTREZID', ont='BP',
    minGSSize=10, maxGSSize=500, eps=0, pvalueCutoff=0.05, seed=TRUE, by='fgsea', verbose=FALSE)),
    error=function(e) NULL)
if (!is.null(b)) {
  m <- merge(a[,c('ID','NES')], b[,c('ID','NES')], by='ID', suffixes=c('.clean','.dup'))
  cat('terms clean =', nrow(a), '| terms with duplicates =', nrow(b),
      '| shared =', nrow(m), '| max |dNES| =', round(max(abs(m$NES.clean-m$NES.dup)),4), '\n')
} else cat('duplicated vector could not be run\n')

cat('\n--- C. what pmax(p, 1e-300) does to the exponent=1 weights ---\n')
edg <- read.csv(file.path(D, 'SYNTHETIC_edger_qlf.csv'))
edg <- edg[!duplicated(edg$gene), ]
sp <- sign(edg$logFC) * -log10(pmax(edg$PValue, 1e-300))
cat('clamped genes (PValue == 0):', sum(edg$PValue == 0), 'of', nrow(edg), '\n')
cat('their weight |stat| = 300; next-largest |stat| =',
    round(max(abs(sp[edg$PValue > 0])), 2),
    ' -> clamped genes carry', round(300/max(abs(sp[edg$PValue > 0])), 1),
    'x the weight of the strongest genuinely-measured gene\n')
cat('share of total sum(|stat|) held by the', sum(edg$PValue==0), 'clamped genes:',
    round(100*sum(abs(sp[edg$PValue==0]))/sum(abs(sp)), 2), '%\n')
gl2 <- sp; names(gl2) <- edg$gene
cat('\n--- D. same edgeR ranking with the clamp raised to 1e-30 instead ---\n')
sp2 <- sign(edg$logFC) * -log10(pmax(edg$PValue, 1e-30))
m <- bitr(edg$gene, fromType='SYMBOL', toType='ENTREZID', OrgDb=org.Hs.eg.db)
mk <- function(v){ x <- v[match(m$SYMBOL, edg$gene)]; names(x) <- m$ENTREZID
                   x <- x[!duplicated(names(x))]; sort(x, decreasing=TRUE) }
for (nm in c('1e-300','1e-30')) {
  v <- mk(if (nm=='1e-300') sp else sp2)
  set.seed(123)
  z <- as.data.frame(gseGO(v, OrgDb=org.Hs.eg.db, keyType='ENTREZID', ont='BP', minGSSize=10,
        maxGSSize=500, eps=0, pvalueCutoff=0.05, seed=TRUE, by='fgsea', verbose=FALSE))
  cat(sprintf('clamp %-7s -> %2d terms | pos %2d | neg %2d | DNA replication present: %s\n',
      nm, nrow(z), sum(z$NES>0), sum(z$NES<0),
      any(grepl('DNA replication', z$Description))))
}
cat('\nEXIT OK\n')
