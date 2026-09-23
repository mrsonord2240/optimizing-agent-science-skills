.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
r <- read.csv(file.path(PP,'rerun','work5','msstats_comparison.csv'))
truth <- read.csv(file.path(PP,'data','truth_proteins.csv'), na.strings=character(0))
cls <- truth$class[match(as.character(r$Protein), truth$protein)]
cat('classes of ComparisonResult rows:', paste(names(table(cls,useNA='ifany')), table(cls,useNA='ifany'), collapse=' | '), '\n')
pn <- r$pvalue[cls=='null']
cat('null rows:', length(pn), '| NA pvalue:', sum(is.na(pn)), '\n')
pn <- pn[!is.na(pn)]
cat(sprintf('nulls raw p<0.05: %d/%d = %.1f%%\n', sum(pn<0.05), length(pn), 100*mean(pn<0.05)))
cat(sprintf('nulls raw p<0.01: %d/%d = %.1f%%\n', sum(pn<0.01), length(pn), 100*mean(pn<0.01)))
cat('null p deciles:', paste(round(quantile(pn, seq(0,1,0.1)),4), collapse=' '), '\n')
cat('KS vs uniform p =', format.pval(ks.test(pn,'punif')$p.value), '\n')
# realized FDR in the call list
sig <- !is.na(r$adj.pvalue) & r$adj.pvalue < 0.05
cat(sprintf('calls: %d | true nulls among calls: %d | realized FDR %.1f%% (nominal 5%%)\n',
    sum(sig), sum(cls[sig]=='null', na.rm=TRUE), 100*mean(cls[sig]=='null', na.rm=TRUE)))
# what do the false positives look like?
fp <- r[sig & cls=='null', c('Protein','log2FC','SE','pvalue','adj.pvalue','issue')]
cat('\nFalse positives (true nulls called):\n'); print(head(fp[order(fp$pvalue),], 25))
cat('\nSE summary, nulls called vs nulls not called:\n')
print(summary(r$SE[sig & cls=='null'])); print(summary(r$SE[!sig & cls=='null']))
cat('\nlog2FC of false positives: abs median', round(median(abs(fp$log2FC), na.rm=TRUE),3),
    '| max', round(max(abs(fp$log2FC), na.rm=TRUE),3), '\n')
cat('issue column values among calls:', paste(names(table(r$issue[sig],useNA='ifany')), table(r$issue[sig],useNA='ifany'), collapse=' | '), '\n')
