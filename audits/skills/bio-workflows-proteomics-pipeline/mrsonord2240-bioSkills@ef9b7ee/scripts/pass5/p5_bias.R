.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
r <- read.csv(file.path(PP,'pass5','work5','msstats_comparison.csv'))
truth <- read.csv(file.path(PP,'data','truth_proteins.csv'), na.strings=character(0))
i <- match(as.character(r$Protein), truth$protein); cls <- truth$class[i]; tfc <- truth$true_log2fc[i]
n <- !is.na(cls) & cls=='null' & !is.na(r$log2FC)
cat(sprintf('true nulls: n=%d  mean log2FC=%+.4f  median=%+.4f  (expected 0)\n', sum(n), mean(r$log2FC[n]), median(r$log2FC[n])))
cat('sign of nulls called at BH .05:', paste(table(sign(r$log2FC[n & r$adj.pvalue<0.05])), collapse='/'), '\n')
for (k in c('up','down','on_off')) { m <- !is.na(cls) & cls==k & !is.na(r$log2FC)
  cat(sprintf('%7s n=%3d  mean est log2FC=%+.3f  mean true=%+.3f  bias=%+.3f\n', k, sum(m), mean(r$log2FC[m]), mean(tfc[m]), mean(r$log2FC[m]-tfc[m]))) }
cat('\ncomposition of the 296 summarized proteins:', paste(names(table(cls)), table(cls), collapse=' '), '\n')
# one-sample t of the null centre
cat(sprintf('t-test of null log2FC vs 0: p=%.3g\n', t.test(r$log2FC[n])$p.value))
