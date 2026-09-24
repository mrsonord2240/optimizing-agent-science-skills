root <- Sys.getenv('REACTOME_AUDIT_ROOT'); private <- Sys.getenv('REACTOME_AUDIT_PRIVATE_LIB')
.libPaths(c(private, .libPaths()))
library(ReactomePA); library(clusterProfiler); library(org.Hs.eg.db)
s <- bitr(c('CDK1','CCNB1','CCNB2','CDC20','BUB1','MAD2L1','PLK1','AURKA','AURKB','CDC25C','CCNA2','CDK2'),'SYMBOL','ENTREZID',org.Hs.eg.db)$ENTREZID
ora <- enrichPathway(s,organism='human',pvalueCutoff=1,qvalueCutoff=1,readable=TRUE); d <- as.data.frame(ora); stopifnot(nrow(d)>0)
pdf(file.path(root,'outputs','input06_viewpathway.pdf')); z <- viewPathway(d$Description[1], organism='human', readable=TRUE); print(z); dev.off()
stopifnot(file.info(file.path(root,'outputs','input06_viewpathway.pdf'))$size > 1000)
cat('ASSERT viewpathway_name_writes_pdf\n')
