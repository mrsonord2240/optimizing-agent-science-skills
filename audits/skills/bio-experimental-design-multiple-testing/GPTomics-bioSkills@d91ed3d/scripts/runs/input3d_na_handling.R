.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# The commonest real off-spec input for this skill: a DESeq2 p-value column containing
# NAs (independent filtering / Cook's outliers). Neither SKILL.md nor usage-guide.md
# mentions NA handling anywhere. What actually happens?
set.seed(11)
p <- c(runif(900), rep(NA_real_, 100))       # 1000 features, 100 untested
cat('length(p) =', length(p), ' non-NA =', sum(!is.na(p)), '\n')
a <- p.adjust(p, 'BH')
cat('p.adjust(p,"BH") default (n = sum(!is.na(p)) = ', sum(!is.na(p)), ') -> min padj =', signif(min(a, na.rm=TRUE), 4),
    '| discoveries<0.05 =', sum(a < 0.05, na.rm=TRUE), '\n')
b <- p.adjust(p[!is.na(p)], 'BH')
cat('p.adjust on non-NA subset       -> min padj =', signif(min(b), 4),
    '| discoveries<0.05 =', sum(b < 0.05), '\n')
cat('same result?', isTRUE(all.equal(sort(a[!is.na(a)]), sort(b))), '\n')
suppressMessages(library(qvalue))
r <- try(qvalue(p), silent = TRUE)
cat('\nqvalue(p) with NAs present:', if (inherits(r,'try-error')) 'ERROR' else 'OK', '\n')
if (inherits(r,'try-error')) cat(as.character(r))
suppressMessages(library(IHW))
r2 <- try(ihw(p, runif(1000), alpha = 0.05, nbins = 2), silent = TRUE)
cat('ihw() with NAs present:', if (inherits(r2,'try-error')) 'ERROR' else 'OK', '\n')
if (inherits(r2,'try-error')) cat(as.character(r2))
