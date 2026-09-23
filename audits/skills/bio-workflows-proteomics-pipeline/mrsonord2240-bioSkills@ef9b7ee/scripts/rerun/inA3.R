.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
blk <- list.files(file.path(PP,'rerun','blocks'), pattern='^b02', full.names=TRUE)
setwd(file.path(PP,'rerun','workA3')); e <- new.env(parent=globalenv())
res <- tryCatch({ suppressWarnings(sys.source(blk, envir=e)); 'OK' }, error=function(x) paste('ERROR:', conditionMessage(x)))
cat('\n========== workA3 (batch-balanced global null):', res, '\n')
r <- get('results', envir=e)$ComparisonResult; p <- r$pvalue[!is.na(r$pvalue)]; a <- r$adj.pvalue[!is.na(r$adj.pvalue)]
cat(sprintf('workA3: proteins=%d  BH<0.05 = %d/%d = %.1f%%  raw p<0.05 = %.1f%% (nominal 5%%)  mean log2FC %+.4f  KS p=%s\n',
    nrow(r), sum(a<0.05), length(a), 100*mean(a<0.05), 100*mean(p<0.05), mean(r$log2FC[is.finite(r$log2FC)]), format.pval(ks.test(p,'punif')$p.value)))
write.csv(r,'comparison.csv',row.names=FALSE)
