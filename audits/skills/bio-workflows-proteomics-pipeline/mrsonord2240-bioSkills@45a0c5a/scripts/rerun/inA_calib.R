# NEW re-audit input A: is the MSstats route's ~10% null-calling a route defect or a property of the audit data?
# A1 = true-null proteins only (real Control/Treatment labels). A2 = full table, condition labels permuted
# so every protein is a true null but the design is balanced. Both run the SKILL.md MSstats block VERBATIM.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
blk <- list.files(file.path(PP,'rerun','blocks'), pattern='^b02', full.names=TRUE)
for (w in c('workA1','workA2')) {
  setwd(file.path(PP,'rerun',w))
  e <- new.env(parent=globalenv())
  res <- tryCatch({ suppressWarnings(sys.source(blk, envir=e)); 'OK' }, error=function(x) paste('ERROR:', conditionMessage(x)))
  cat('\n==========', w, ':', res, '\n')
  if (!exists('results', envir=e)) next
  r <- get('results', envir=e)$ComparisonResult
  p <- r$pvalue[!is.na(r$pvalue)]; a <- r$adj.pvalue[!is.na(r$adj.pvalue)]
  cat(sprintf('%s: proteins=%d  called BH<0.05 = %d/%d = %.1f%%  (ALL are true nulls)\n',
      w, nrow(r), sum(a<0.05), length(a), 100*mean(a<0.05)))
  cat(sprintf('%s: raw p<0.05 = %d/%d = %.1f%% (nominal 5%%) | mean log2FC = %+.4f (expected 0)\n',
      w, sum(p<0.05), length(p), 100*mean(p<0.05), mean(r$log2FC[is.finite(r$log2FC)])))
  cat(sprintf('%s: KS vs uniform p = %s\n', w, format.pval(ks.test(p,'punif')$p.value)))
  write.csv(r, 'comparison.csv', row.names=FALSE)
}
